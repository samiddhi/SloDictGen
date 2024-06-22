'''
To Do:
 - REPLACE 'of "to' <----> "of 'to"
'''

from common.imports import proj_dir
import os
from utils.json_utils import read_json
import json

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




def show(s, n, c=5):
    """
    Identifies char in string from index with context

    :param s: string
    :param n: position of letter
    :param c: context size
    :return:
    """
    start = max(0, n - c)
    end = min(len(s), n + c)
    context = s[start:end]
    caret_position = n - start
    caret_spaces = " " * (caret_position - 1)
    caret = "^"
    print(context)
    print(caret_spaces + caret)


def shows(s, n, c=5):
    start = max(0, n - c)
    end = min(len(s), n + c)
    print(f'{s[start:n - 1]}>>>{s[n - 1]}<<<{s[n:end]}')

insolubles = read_json(insoluble_path)

ins = insolubles[0]
print(repr(ins))
json.loads(ins)


shows(repr(ins), 6973, 20)
