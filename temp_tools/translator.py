import os
from openai import OpenAI
import json
from common.imports import *

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set up the client with API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def slo_to_en_gpt(user_input: str, test: bool = True) -> List[Dict[str,str]]:
    """Translate a Slovenian dictionary into English.

    :param user_input: The user input containing the Slovenian dictionary.
    :param test: default ``True`` - returns example output. Safeguard against
    unnecessary API calls.
    :return: A JSON object with the translated dictionary.
    """
    prompt = user_input + """
    You are a translator tasked with translating the above list of entries from a 
    Slovenian lexicon into English. Each entry is represented as a dictionary with 
    a key-value pair where the key is a Slovenian word or phrase, and the value is 
    currently set to None. Your job is to replace the None value with the English 
    translation of the corresponding Slovenian word or phrase. Be as literal and 
    accurate as possible in your translations. Once you have translated all the 
    entries, return the list of dictionaries as a JSON array.
    
    Example Input:
    [
        {'pregoreče': None, 'pregoreče ljubiti': None}, 
        {'imenitniški': None, 'ekspr.': None, 'značilen za imenitnike:': None, 'gledal je nanje z imenitniško prezirljivostjo': None, 'imenitniške besede': None}
    ]
    
    Example Output:
    [
        {'pregoreče': 'burning', 'pregoreče ljubiti': 'to love passionately'}, 
        {'imenitniški': 'denominative', 'ekspr.': 'expr.', 'značilen za imenitnike:': 'characteristic of dignitaries', 'gledal je nanje z imenitniško prezirljivostjo': 'he looked at them with dignitary disdain', 'imenitniške besede': 'dignitary words'}
    ]"""

    if test:
        return [{'pregoreče': 'burning', 'pregoreče ljubiti': 'to love passionately'},
                {'imenitniški': 'denominative', 'ekspr.': 'expr.', 'značilen za imenitnike:': 'characteristic of dignitaries', 'gledal je nanje z imenitniško prezirljivostjo': 'he looked at them with dignitary disdain', 'imenitniške besede': 'dignitary words'}]
    if not test:
        # Use the client instance to make the API call
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are translating a Slovenian dictionary into English."},
                {"role": "user", "content": prompt}
            ]
        )

    print("Completion:",
          completion)  # Print the completion object to see if it's None or has data

    if completion.choices and completion.choices[0].message and \
            completion.choices[0].message.content:
        generated_text = completion.choices[0].message.content
        generated_text_fixed = generated_text.replace("'", '"')

        return json.loads(generated_text_fixed)
    else:
            # Handle the case where generated_text is None or empty
            logging.critical(user_input)
            return {}


# Example usage
if __name__ == "__main__":
    sl_input = """
    [
        {'pregoreče': None, 'pregoreče ljubiti': None}, 
        {'imenitniški': None, 'ekspr.': None, 'značilen za imenitnike:': None, 'gledal je nanje z imenitniško prezirljivostjo': None, 'imenitniške besede': None}
    ]
    """
    en_output = slo_to_en_gpt(sl_input, test=True)
    print(en_output)