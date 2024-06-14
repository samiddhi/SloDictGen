from common.imports import *
from dataclasses import dataclass
import os
import re
import sqlite3
from tqdm import tqdm


from bs4 import BeautifulSoup
import pickle

from slo_dict_gen_pkg.grammar_utils import ordered_grammar_name, de_critic, ALPHA


@dataclass
class SskjEntry:
    """
    :html: str
    :accentuation: str
    :lemma: str
    :definitions: List[str]
    :sub_words: List[SskjEntry]
    """
    html: str
    accentuation: str
    lemma: str
    definitions: List[str]
    sub_words: List['SskjEntry']


class HTMLParser:
    """
    self.sskjentrys is a list of all SskjEntry objects generated from given
    file
    """
    def __init__(
            self,
            html_path: str,
            save_path: str = None
    ) -> None:
        """
        Initializes an HTMLParser instance for a given HTML file path.

        :param html_file: Path to the HTML file to parse.
        :param save_path: Saves file if path is given
        """
        if os.path.exists(html_path):
            content: str = self._html_content(html_path)
            soup: BeautifulSoup = self._parse_html(content)
            self.sskjentrys: List[SskjEntry] = self._soup_to_sskjentrys(soup)
            if save_path:
                self._save_pickle(self.sskjentrys, save_path)

    @staticmethod
    def _html_content(filepath: str) -> str:
        with open(filepath, 'r', encoding='utf-8') as file:
            html_content = file.read()

        return html_content

    @staticmethod
    def _parse_html(html_content: str) -> BeautifulSoup:
        return BeautifulSoup(html_content, 'html.parser')

    def _soup_to_sskjentrys(self, soup: BeautifulSoup) -> List[SskjEntry]:
        entries = soup.find_all("div", class_="list-group-item entry")
        all_sskjentrys = []
        for entry in entries:
            entry_clone = BeautifulSoup(str(entry), 'html.parser').div
            orange_entries = entry_clone.find_all("ul", class_="manual")

            # Now pass each <ul class="manual"> individually
            sub_words: List[SskjEntry] = [self._html_to_sskjentry(ul) for ul in
                                          orange_entries]

            # Remove all <ul class="manual"> elements from the clone and
            # finally create clone entry with all subwords
            for ul in orange_entries:
                ul.decompose()
            head_word = self._html_to_sskjentry(html=entry_clone,
                                          sub_words=sub_words)

            all_sskjentrys.extend([head_word] + sub_words)

        return all_sskjentrys

    @staticmethod
    def _html_to_sskjentry(
            html: BeautifulSoup,
            sub_words: List[SskjEntry] = None
    ) -> SskjEntry:
        try:
            accentuation = html.find("span", class_="font_xlarge").get_text(
                strip=True)
        except AttributeError:
            accentuation = html.find("span", class_="color_orange").get_text(
                strip=True)
        lemma = de_critic(accentuation)
        explanations = [
            re.sub(r'\s+', ' ', span.get_text(strip=True))
            # Replaces all whitespace with a single space
            for span in
            html.find_all("span", {"data-group": "explanation "})
        ]
        return SskjEntry(
            html=str(html),
            lemma=lemma,
            accentuation=accentuation,
            definitions=explanations,
            sub_words=sub_words
        )

    @staticmethod
    def _save_pickle(
            data: ...,
            filename: str
    ) -> None:
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

class SskjEntrystoSQLite:
    def __init__(self, db_name: str, data: List[SskjEntry]):
        db_dir = os.path.abspath(
            os.path.join(proj_dir, 'data', 'db'))
        db_path = os.path.abspath(
            os.path.join(db_dir, db_name))
        # Create database and table
        self.create_database(db_path)

        # Insert entries into the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            for entry in tqdm(data):
                self.insert_entry(entry, None, cursor)
            conn.commit()
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            conn.rollback()
        finally:
            conn.close()

    @staticmethod
    def parse_html_for_header_qualifiers(html: str) -> List[str]:
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all(attrs={"data-group": "header qualifier"})
        return [tag.text for tag in tags]

    @staticmethod
    def create_database(db_path: str):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sskj_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                html TEXT,
                accentuation TEXT,
                lemma TEXT,
                definitions TEXT,
                header_qualifiers TEXT,
                parent INTEGER,
                children TEXT,
                UNIQUE(html, accentuation)
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def find_entry_id(html: str, accentuation: str, cursor) -> Optional[int]:
        cursor.execute('''
            SELECT id FROM sskj_entries WHERE html = ? AND accentuation = ?
        ''', (html, accentuation))
        result = cursor.fetchone()
        return result[0] if result else None

    def insert_entry(self, entry: SskjEntry, parent_id: Optional[int],
                     cursor) -> int:
        existing_id = self.find_entry_id(entry.html, entry.accentuation, cursor)
        if existing_id is not None:
            return existing_id

        definitions = '; '.join(entry.definitions)
        header_qualifiers = ';'.join(
            self.parse_html_for_header_qualifiers(entry.html))
        cursor.execute('''
            INSERT INTO sskj_entries (html, accentuation, lemma, definitions, header_qualifiers, parent, children)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (entry.html, entry.accentuation, entry.lemma, definitions,
              header_qualifiers, parent_id, ''))
        entry_id = cursor.lastrowid
        children_ids = []
        if entry.sub_words:
            for sub_entry in entry.sub_words:
                sub_entry_id = self.insert_entry(sub_entry, entry_id, cursor)
                children_ids.append(sub_entry_id)
        cursor.execute('''
            UPDATE sskj_entries
            SET children = ?
            WHERE id = ?
        ''', (';'.join(map(str, children_ids)), entry_id))
        return entry_id

def get_sskjentrys(pkl_path) -> List[SskjEntry]:
    """
    :return:
    """
    all_objs = []
    for letter in ALPHA:
        with open(pkl_path + f'\\Letter_{letter}.pkl', 'rb') as file:
            all_objs.extend(pickle.load(file))
    return all_objs


if __name__ == "__main__":
    pkl_dir = os.path.abspath(
        os.path.join(proj_dir, 'data', 'pickles', 'sskj_html_objs'))
    all_sskjentrys: List[SskjEntry] = get_sskjentrys(pkl_dir)

    SskjEntrystoSQLite(db_name="sskj_entries_trie.db", data=all_sskjentrys)





