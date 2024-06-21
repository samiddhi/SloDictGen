from bs4 import BeautifulSoup
from typing import Dict, List
from common.imports import proj_dir
from utils.grammar_utils import de_critic, has_chars

import sqlite3
import random

import os

def extract_htmltext_except(
        html: str,
        exclusions: List[Dict[str, str]] = (
                {"data-group": "header"},
                {"data-group": "header qualifier"}
        )
) -> List[str]:
    """
    Convert HTML content to a list of text elements with option to exclude certain tag attributes.

    :param html: The HTML content as a string.
    :param exclusions: A list of dictionaries where key-value pairs
    represent attribute name-value pairs to be excluded from the output.
    :return: A list of extracted text element strings.
    """
    soup = BeautifulSoup(html, 'html.parser')
    html_text_elements = []

    for elem in soup.find_all(string=True):
        if not elem.strip():
            continue

        exclusions = list(exclusions)
        exclude = any(all(elem.parent.get(attr) == value for attr, value in attrs.items()) for attrs in exclusions)
        if not exclude:
            html_text_elements.append(elem.strip())

    return html_text_elements

def get_random_html_entry(db_path: str) -> str:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT html FROM sskj_entries")  # Adjust table and column names accordingly
        rows = cursor.fetchall()
        if rows:
            random_row = random.choice(rows)
            return random_row[0]
        else:
            raise ValueError("No entries found in the database")

def random_test_entries(db: str, count: int) -> List[Dict[str,None]]:
    """
    :param db: path to source .db SQLite database
    :param count: number of entries to include
    :return: sample of `count` many dictionaries containing html elements
    """
    entries = []
    for i in range(0, count):
        html_text = get_random_html_entry(db_path)
        processed_html: List[str] = extract_htmltext_except(
            html=html_text,
            exclusions=exclusions)
        processed_html[0] = de_critic(processed_html[0])
        strings_only = []
        for item in processed_html:
            if has_chars(item):
                strings_only.append(item)

        entries.append({x: None for x in strings_only})
    return entries



if __name__ == "__main__":
    db_path = os.path.abspath(os.path.join(proj_dir, 'data', 'db', 'sskj_entries.db'))

    sample = random_test_entries(db=db_path, count=3)
    print(sample)
