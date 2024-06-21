from common.imports import *
from slo_dict_gen_pkg import SloleksEntry, Representation, logging, SskjEntry
from slo_dict_gen_pkg.formatting import InflectionSection
from utils.html_utils import extract_htmltext_except

from tqdm import tqdm
from bs4 import BeautifulSoup

import pickle
import sqlite3

sskj_entries_db: str = os.path.abspath(os.path.join(
    proj_dir, 'data', 'db', 'sskj_entries.db'))
sloleks_db: str = os.path.abspath(os.path.join(
    proj_dir, 'data', 'db', 'sloleks.db'))


class SloleksToSQLite:
    def __init__(self, db_name: str, working_directory: str):
        """
        Instantiation generates SQLite database from all pkl'd SloleksEntry objects at path

        :param db_name: name of db including .db
        :param working_directory: directory with pickles and db destination
        """
        conn = sqlite3.connect(os.path.join(working_directory, db_name))
        self.create_tables(conn)

        for file_name in tqdm(os.listdir(working_directory)):
            if file_name.endswith('.pkl'):
                file_path = os.path.join(working_directory, file_name)
                with open(file_path, 'rb') as f:
                    data = pickle.load(f)
                    self.insert_sloleks_entry(conn, data)

        conn.close()

    @staticmethod
    def create_tables(self, conn) -> None:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS SloleksEntry (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        lemma TEXT,
                        part_of_speech TEXT,
                        xml_file TEXT,
                        inflection_section TEXT
                     )''')
        c.execute('''CREATE TABLE IF NOT EXISTS LemmaGrammaticalFeature (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sloleks_entry_id INTEGER,
                        type TEXT,
                        aspect TEXT,
                        vform TEXT,
                        number TEXT,
                        gender TEXT,
                        person TEXT,
                        FOREIGN KEY(sloleks_entry_id) REFERENCES SloleksEntry(id)
                     )''')
        c.execute('''CREATE TABLE IF NOT EXISTS WordForm (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sloleks_entry_id INTEGER,
                        lemma TEXT,
                        part_of_speech TEXT,
                        msd TEXT,
                        v_form TEXT,
                        grammatical_case TEXT,
                        person TEXT,
                        number TEXT,
                        gender TEXT,
                        degree TEXT,
                        clitic TEXT,
                        FOREIGN KEY(sloleks_entry_id) REFERENCES SloleksEntry(id)
                     )''')
        c.execute('''CREATE TABLE IF NOT EXISTS Representation (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            sloleks_entry_id INTEGER,
                            word_form_id INTEGER,
                            form_representation TEXT,
                            norms TEXT,
                            frequency INTEGER,
                            accentuations TEXT,
                            ipa TEXT,
                            sampa TEXT,
                            FOREIGN KEY(word_form_id) REFERENCES WordForm(id),
                            FOREIGN KEY(sloleks_entry_id) REFERENCES SloleksEntry(id)
                         )''')
        conn.commit()

    @staticmethod
    def insert_sloleks_entry(self, conn,
                             sloleks_entries: List[SloleksEntry]) -> None:
        c = conn.cursor()

        sloleks_entry_stmt = '''INSERT INTO SloleksEntry (lemma, part_of_speech, xml_file, inflection_section) 
                                VALUES (?, ?, ?, ?)'''
        lemma_grammatical_feature_stmt = '''INSERT INTO LemmaGrammaticalFeature (sloleks_entry_id, type, aspect, vform, number, gender, person) 
                                            VALUES (?, ?, ?, ?, ?, ?, ?)'''
        word_form_stmt = '''INSERT INTO WordForm (sloleks_entry_id, lemma, part_of_speech, msd, v_form, grammatical_case, person, number, gender, degree, clitic) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        representation_stmt = '''INSERT INTO Representation (sloleks_entry_id, word_form_id, form_representation, norms, frequency, accentuations, ipa, sampa) 
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

        for sloleks_entry in sloleks_entries:
            inflection_section = str(InflectionSection(sloleks_entry))
            c.execute(sloleks_entry_stmt, (
            sloleks_entry.lemma, sloleks_entry.part_of_speech,
            sloleks_entry.xml_file, inflection_section))
            sloleks_entry_id = c.lastrowid

            c.execute(lemma_grammatical_feature_stmt,
                      (sloleks_entry_id,
                       sloleks_entry.lemma_grammatical_features.get('type'),
                       sloleks_entry.lemma_grammatical_features.get('aspect'),
                       sloleks_entry.lemma_grammatical_features.get('vform'),
                       sloleks_entry.lemma_grammatical_features.get('number'),
                       sloleks_entry.lemma_grammatical_features.get('gender'),
                       sloleks_entry.lemma_grammatical_features.get('person')))

            for word_form in sloleks_entry.all_forms:
                c.execute(word_form_stmt,
                          (sloleks_entry_id, word_form.lemma,
                           word_form.part_of_speech, word_form.msd,
                           word_form.v_form, word_form.case, word_form.person,
                           word_form.number,
                           word_form.gender, word_form.degree,
                           word_form.clitic))
                word_form_id = c.lastrowid

                for representation in word_form.representations:
                    c.execute(representation_stmt,
                              (sloleks_entry_id, word_form_id,
                               representation.form_representation,
                               str(representation.norms),
                               representation.frequency,
                               str(representation.accentuations),
                               representation.pronunciation_dict.get('IPA'),
                               representation.pronunciation_dict.get('SAMPA')))

        conn.commit()


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
        unique_qualifiers = set()
        for tag in tags:
            unique_qualifiers.add(str(tag.text).strip())

        return list(unique_qualifiers)

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
        existing_id = self.find_entry_id(entry.html, entry.accentuation,
                                         cursor)
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


class Merger:
    def __init__(self):
        # Instantiation generates merged SQLite database from local SloleksToSQLite and parsers.py/HTMLParser classes
        raise NotImplementedError("y'ain't done it")


### from sqlite_utils.py
def fetch_by_id(cursor: sqlite3.Cursor, col: str, table: str, row_id: int) -> str:
    """
    Fetches the specified column content from a given table for a specific row id.

    :param cursor: SQLite cursor object.
    :param col: Column name to fetch.
    :param table: Table name to fetch from.
    :param row_id: The id of the row to fetch.
    :return: Column content as a string.
    """
    query = f"SELECT {col} FROM {table} WHERE id = ?"
    cursor.execute(query, (row_id,))
    row = cursor.fetchone()
    return row[0] if row else ""



if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pickles_dir = os.path.join(base_dir, 'data', 'pickles',
                               'sloleksentry_objects')

    Merger()
