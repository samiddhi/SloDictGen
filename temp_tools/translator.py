"""This is one well-built one-use MF"""

from openai import OpenAI
import tiktoken

import json
import sqlite3
from functools import partial

from common.imports import *
from utils.html_utils import extract_htmltext_except
from utils.sqlite_utils import fetch_by_id, sskj_entries_db
from utils.py_utils import batch_and_process, get_os
from utils.grammar_utils import has_chars, de_critic
from utils.json_utils import extend_json_array, add_to_json_array

from dotenv import load_dotenv

dotenv_path = os.path.join(proj_dir, '.env')
load_dotenv(dotenv_path)

# Set up the client with API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def log_input_output(log_file_path: str, inpt: any, output: any):
    """Log the input and output to a text file.

    :param log_file_path: The path to the log file.
    :param inpt: The user input.
    :param output: The output from the GPT API.
    """
    log = {
        "in": inpt,
        "out": output
    }
    add_to_json_array(log_file_path, log)


def slo_to_en_gpt(
        user_input: List[Dict[str, None]],
        connect: bool = False,
        verify: bool = False
) -> Tuple[List[Dict[str, str]], Optional[str]]:
    """Translate a Slovenian dictionary into English.

    :param user_input: The user input containing the Slovenian dictionary.
    :param connect: default ``False``, Safeguard against unnecessary API calls
    :param verify: default ``False``, Safeguard against unnecessary API calls
    :return: A JSON object with the translated dictionary or empty list.
    :return: The text response from GPT or ``None``
    """
    prompt = user_input.__str__() + """
    You are a translator tasked with translating the above list of entries from 
    a Slovenian lexicon into English. Each entry is represented as a py dict 
    with a key-value pair with an untranslated Slovenian key and a null value. 
    Your job is to replace the null value with the English translation of the 
    corresponding Slovenian word or phrase. The first key is the term being 
    defined, so pick a good translation based on the context of the definition.
    Be as accurate and contextually aware as possible in your translations. 
    Return the list of dictionaries as a JSON array. 
    
    Example Input:
    [
        {'pregoreče': None, 'pregoreče ljubiti': None}, 
        {'imenitniški': None, 'ekspr.': None, 'značilen za imenitnike:': None, 'gledal je nanje z imenitniško prezirljivostjo': None, 'imenitniške besede': None}
    ]
    
    Example Output:
    [
        {
            "pregoreče": "burning", 
            "pregoreče ljubiti": "to love passionately"
            "": null
        }, 
        {
            "imenitniški": "denominative", 
            "ekspr.": "expr.", 
            "značilen za imenitnike:": "characteristic of dignitaries", 
            "imenitniške besede": "dignitary words"
        }
    ]
    
    Your JSON response MUST CONTAIN ENGLISH TRANSLATIONS. Do not leave any 
    values null
    
    """

    if not (connect and verify):
        blank_response = [{key: "" for key in entry} for entry in user_input]
        return blank_response, blank_response.__str__()

    try:
        # Use the client instance to make the API call
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are translating a Slovenian dictionary into "
                            "English."},
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as e:
        logging.critical(f'{e} --- user_input: {user_input}')
        return [], None

    if completion.choices and completion.choices[0].message and \
            completion.choices[0].message.content:
        generated_text = completion.choices[0].message.content

        # unicode bullshit
        gtf = generated_text.replace("\\n", "\n")
        gtf = gtf.encode('utf-8').decode('utf-8')
        gtf = gtf.replace("{'", '{\"').replace(" '", ' "')
        gtf = gtf.replace("' :", '" :').replace("':", '":')
        gtf = gtf.replace("\\", "\\\\").replace('\n', ' ')
        gtf = gtf.replace('of "to', "of 'to")
        generated_text_fixed = gtf.replace(': None', ': null')

        try:
            translated_data = json.loads(generated_text_fixed)
            return translated_data, generated_text_fixed
        except:
            return [], generated_text_fixed

        # Handle the case where generated_text is None or empty
    return [], None


def num_tokens(string: str,
               encoding_name: str = "gpt-3.5-turbo") -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    token_ct = len(encoding.encode(string.__str__()))
    return token_ct


def id_html_text_entry_sequence(id_code: any, cursor_obj):
    """Takes id of sskj_entry database entry and returns a
    ready-to-translate dictionary for GPT translator

    :param cursor_obj: SQLite cursor object
    :param id_code: sskj_entry.db entry id :param cursor_obj: SQLite cursor
    :return: ``Dict[str, None]`` for GPT to translate by replacing ``None``
    with translation of ``str``
    """
    html = fetch_by_id(cursor_obj, 'html', 'sskj_entries', id_code)
    if html:
        extracted_text = extract_htmltext_except(html)
        extracted_text[0] = de_critic(extracted_text[0])
        strings_only = []
        for item in extracted_text:
            if has_chars(item):
                strings_only.append(item)
        return {line: None for line in strings_only}
    else:
        return None


def translate_and_save(
        batch: List[Dict[str, None]],
        output_json_path: str,
        error_logging_path: str,
        std_logging_path: str,
        _connect: bool = False,
        _verify: bool = False
) -> None:
    obj_response, raw_response = slo_to_en_gpt(
        user_input=batch,
        connect=_connect,
        verify=_verify
    )

    log_input_output(
        log_file_path=std_logging_path,
        inpt=batch,
        output=raw_response
    )

    # Handle different call/response situations
    if obj_response:
        extend_json_array(output_json_path, obj_response)
    elif raw_response:
        # Log un-JSON-able responses
        add_to_json_array(error_logging_path, raw_response)


def main_translate_sequence() -> None:
    """
    Translates from sskj_entries.db into GPTranslations.json

    :return: None
    """
    translation_station = os.path.abspath(os.path.join(
        proj_dir, 'data', 'db', 'translation_station'))

    translated_en = os.path.abspath(os.path.join(
        translation_station, 'translated_en.json'))
    insoluble_path = os.path.abspath(os.path.join(
        translation_station, 'insoluble.json'))
    std_log = os.path.abspath(os.path.join(
        translation_station, 'std_log.json'))
    id_log = os.path.abspath(os.path.join(
        translation_station, 'id_log.json'))

    conn = sqlite3.connect(sskj_entries_db)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM sskj_entries")
    ids: List = [row[0] for row in cursor.fetchall()]

    # Tracks which IDs have been translated already
    try:
        with open(id_log, 'r', encoding='utf-8') as f:
            translated_ids = json.load(f)
    except FileNotFoundError:
        pass

    ids.sort()

    # to run dual opposite direction translations for faster processing
    if get_os() == "mac":
        # ids.reverse()
        pass

    ids = [None if i in translated_ids else i for i in ids]

    batch_and_process(
        data=ids,
        process_func=partial(id_html_text_entry_sequence, cursor_obj=cursor),
        length_func=num_tokens,
        max_length=1800,
        batch_func=partial(
            translate_and_save,
            output_json_path=translated_en,
            _connect=True,
            _verify=True,
            error_logging_path=insoluble_path,
            std_logging_path=std_log
        ),
        log_path=id_log,
        _track=True
    )


# Example usage
if __name__ == "__main__":
    main_translate_sequence()
