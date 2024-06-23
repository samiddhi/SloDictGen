from utils.json_utils import read_json, extend_json_array, add_to_json_object
from utils.sqlite_utils import sskj_entries_db
from common.imports import *

from pprint import pprint
import sqlite3
import json
import re
from tqdm import tqdm

conn = sqlite3.connect(sskj_entries_db)
cursor = conn.cursor()

cursor.execute("SELECT id FROM sskj_entries")
ids: List = [row[0] for row in cursor.fetchall()]

# path declarations
tdir = os.path.abspath(os.path.join(proj_dir, 'data', 'translations'))
mdir = os.path.abspath(os.path.join(tdir, 'merged_station'))



std_log_dir = os.path.abspath(os.path.join(mdir, 'std_log.json'))
trans_dir = os.path.abspath(os.path.join(mdir, 'translated_en.json'))
insol_dir = os.path.abspath(os.path.join(mdir, 'insoluble.json'))
unworked_dir = os.path.abspath(os.path.join(mdir, 'unworked.json'))

id_text_dir = os.path.abspath(os.path.join(mdir, 'id_entrytext.json'))
final_dir = os.path.abspath(os.path.join(mdir, 'id_final_trans.json'))


# Save JSONS (comment out as needed)
#std_log: List[Dict] = read_json(std_log_dir)
#trans_en: List[Dict[str, str]] = read_json(trans_dir)
#insol: List[str] = read_json(insol_dir)

id_entrytext: Dict[str, Dict] = read_json(id_text_dir)
#unworked: List[Dict[str, Dict]] = read_json(unworked_dir)
final: Dict[str, Dict] = read_json(final_dir)



# Used
def match_successes_to_keys(in_list: List[Dict]):
    """Sorry for the shit docstring. Takes a list of {"slo":"eng", ...}
    dictionaries and checks them against the original text extracted from the
    html and fed to GPT. If there is a match (that is, in_list shares all keys
    with a dict in id_entrytext.json, id_final_trans.json is updated
    with in_list for the corresponding ID - basically you can feed this
    attempts at translations and it'll pick out the best candidates for full
    translations"""

    # Index trans_en by normalized keys for faster lookup
    input_index: Dict[str, Dict] = {frozenset(key.replace('\n', '') for key in entry.keys()): entry for entry in in_list}

    # Does every translation have the right keys?
    good = 0
    bad = 0

    for entrydict in tqdm(id_entrytext.values()):
        normalized_keys = frozenset(key.replace('\n', '') for key in entrydict.keys())
        if normalized_keys in input_index:
            good += 1
        else:
            bad += 1

    print(f'\nGood: {good}\nBad: {bad}\n')


    # Create a dictionary with normalized keys
    d = {}
    for i, entrydict in tqdm(id_entrytext.items()):
        normalized_keys = frozenset(key.replace('\n', '') for key in entrydict.keys())
        if normalized_keys in input_index:
            matching_entry = input_index[normalized_keys]
            matching_entry_with_newlines = {key: matching_entry.get(key.replace('\n', ''), '') for key in entrydict.keys()}
            d[i] = matching_entry_with_newlines

    add_to_json_object(final_dir, d, update=False)

def extract_braces_with_symbols(s: str) -> list[str]:
    """
    Extracts all instances of substrings enclosed in {...} from the given
    string where the substrings contain at least one of the symbols: colon (:),
    quote ("), or comma (,).

    :param s: The input string
    :return: A list of substrings matching the criteria
    """
    pattern = r'\{[^{}]*[:",][^{}]*\}'
    matches = re.findall(pattern, s)
    return matches

unworked = []
for id_, value in id_entrytext.items():
    if id_ not in final:
        unworked.append({id_: value})

print(f'{len(final)}+{len(unworked)}={len(final)+len(unworked)}')
print(len(unworked))
extend_json_array(unworked_dir, unworked)
