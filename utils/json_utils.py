import json
import os
import re
from collections import defaultdict
from typing import List, Dict, Any, TypeVar
from utils.grammar_utils import OKRS
from icecream import ic

from common.imports import proj_dir


def extend_json_array(json_path: str, new_entries: List[any]):
    """
    Appends new entries to a JSON array in the specified file.

    :param json_path: Path to the JSON file.
    :param new_entries: List of objects-to-be-added to array.
    """
    try:
        with open(json_path, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("JSON file does not contain a list")
            data.extend(new_entries)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(new_entries, f, ensure_ascii=False, indent=4)


def add_to_json_array(json_path: str, new_object: Any):
    """
    Adds a new object to the JSON array in the specified file.

    :param json_path: Path to the JSON file.
    :param new_object: Object to be added to the array.
    """
    try:
        with open(json_path, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("JSON file does not contain a list")
            data.append(new_object)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump([new_object], f, ensure_ascii=False, indent=4)


def add_to_json_object(json_path: str, new_pairs: Dict[Any, Any]):
    """
    Adds key-value pairs to the JSON object in the specified file.

    :param json_path: Path to the JSON file.
    :param new_pairs: Dictionary of key-value pairs to be added to the JSON object.
    """
    try:
        with open(json_path, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("JSON file does not contain a dictionary")
            data.update(new_pairs)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.truncate()
    except FileNotFoundError:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(new_pairs, f, ensure_ascii=False, indent=4)

T = TypeVar('T')

class JSONKeyFrequency:
    def __init__(self):
        self.frequency: Dict[str, int] = defaultdict(int)

    def update_frequency(self, json_obj: Dict[str, Any]) -> None:
        for key in json_obj.keys():
            self.frequency[key] += 1

    def process_json_array(self, json_array: List[Dict[str, Any]], batch_size: int) -> None:
        for i in range(0, len(json_array), batch_size):
            batch = json_array[i:i + batch_size]
            for obj in batch:
                self.update_frequency(obj)

    def get_frequency(self) -> Dict[str, int]:
        return self.frequency


def read_json(file_path: str) -> T:
    with open(file_path, 'r', encoding="utf-8") as f:
        return json.load(f)


def save_json(data: T, file_path: str) -> None:
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def get_key_frequencies(json_path: str, batch_size: int, output_file: str) -> None:
    """
    Creates frequency mapping (.json) for keys found in JSON array of Dicts

    :param json_path: Path to JSON with form ``List[Dict[str, Any]]``
    :param batch_size: ``int``
    :param output_file: Path
    :return: None
    """
    json_key_frequency = JSONKeyFrequency()
    json_array = read_json(json_path)
    json_key_frequency.process_json_array(json_array, batch_size)
    frequency = json_key_frequency.get_frequency()
    save_json(frequency, output_file)


if __name__ == '__main__':
    with open('frequency.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Filter keys with values >= 2
    filtered_keys = [key for key, value in data.items() if value >= 0]

    # Filter keys that consist of one word ending with a period
    filtered_keys = [key for key in filtered_keys if re.match(r'^\w+\.$', key)]

    for key in OKRS:
        if key in filtered_keys:
            ic(filtered_keys.remove(key))

    print(len(filtered_keys))
    print(filtered_keys)
