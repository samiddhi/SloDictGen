from openai import OpenAI
from typing import Dict, List
import pickle
import ast
from icecream import ic
from unidecode import unidecode


def string_to_data(string) -> ...:
    """

    :param string:
    :return:
    """
    list_of_dicts = ast.literal_eval(string)
    return list_of_dicts


def de_critic(word: str, inpt: str = ''):
    # if word + if word[0] not in "čžšČŽŠ"
    if word:
        if word[0] not in "čžšČŽŠ":
            outpt = inpt + unidecode(word[0])
        else:
            outpt = inpt + word[0]
        return de_critic(word[1:], outpt)
    else:
        return inpt


def message_gpt(client: OpenAI, package: str) -> str:
    """

    :param client:
    :param package:
    :return:
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": ("You are a translator receiving entries from a "
                            "Slovenian dictionary, each consisting of a "
                            "Slovenian word sometimes a few definitions. "
                            "Translate each word and its definitions into "
                            "English. For each [...] entry, you will create a "
                            "one with an identical structure, but with each section between "
                            "'||' being translated into english by you. The "
                            "first section will be your translation of the "
                            "word itself (NOT a definition - a TRANSLATION "
                            "of the WORD.), and all "
                            "subsequent sections will "
                            "be your translation of the "
                            "corresponding slovenian definition.  "
                            "in your response, send my original entry in the [], and send your translated version in [[]]")
            },
            {
                "role": "user",
                "content": package
            }
        ],
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content


def open_pickle_jar(char: str) -> any:
    file_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data\HTML"
                 f"\\SSKJ_entries_html\\{char}_output.pkl")
    with open(file_path, 'rb') as pickle_file:
        pickle_object = pickle.load(pickle_file)

    return pickle_object


def gpt_packager(entries: Dict[str, List[str]], inpt: str = "") -> str:
    if entries and len(inpt) < 1025:
        entry_keys = list(entries.keys())
        key: str = entry_keys[0]
        definitions: List[str] = entries[key]
        output = inpt + f'"[{"||".join([de_critic(key)] + definitions)}]"\n\n'
        new_entries = entries.copy()
        new_entries.pop(key)
        return gpt_packager(new_entries, output)
    else:
        print(inpt)
        return inpt


def char_to_package(char: str) -> str:
    pickle_object = open_pickle_jar(char)
    package = gpt_packager(pickle_object)
    return package


def for_letter_add_to_string(letters: str, func, inpt: str = ""):
    if letters:
        char = letters[0]
        func_output = func(char)
        output = inpt + func_output
        return for_letter_add_to_string(letters[1:], func, output)
    else:
        return inpt


def main() -> None:
    api_key = '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'
    client = OpenAI(api_key=api_key)
    LETTER = "c"
    pickle_object = open_pickle_jar(LETTER)
    package = gpt_packager(pickle_object)
    print(package)


    run = False
    if run:
        message = message_gpt(client, gpt_package)
        print(f'-----MESSAGE-----\n\n{message}\n\n')

        try:
            data_object = string_to_data(message)
            print('\n\n-----OBJECT-----\n\n')
            print(data_object)
            with open(r"C:\Users\sangha\Documents\Danny's\SloDictGen\data\HTML"
                      f"\\SSKJ_entries_html\\{letters_to_run}_dict.pkl",
                      'wb') as f:
                pickle.dump(data_object, f)
        except Exception as e:
            print(e)
        return None


"""
DONE: qwxy
"""
main()
