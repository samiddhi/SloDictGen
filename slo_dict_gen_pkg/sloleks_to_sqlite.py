import os
import pickle
import sqlite3
from tqdm import tqdm
from typing import List
from slo_dict_gen_pkg import SloleksEntry, Representation, logging
from formatting import InflectionSection

def create_tables(conn) -> None:
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

def insert_sloleks_entry(conn, sloleks_entries: List[SloleksEntry]) -> None:
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
        c.execute(sloleks_entry_stmt, (sloleks_entry.lemma, sloleks_entry.part_of_speech, sloleks_entry.xml_file, inflection_section))
        sloleks_entry_id = c.lastrowid

        c.execute(lemma_grammatical_feature_stmt,
                  (sloleks_entry_id, sloleks_entry.lemma_grammatical_features.get('type'),
                   sloleks_entry.lemma_grammatical_features.get('aspect'),
                   sloleks_entry.lemma_grammatical_features.get('vform'),
                   sloleks_entry.lemma_grammatical_features.get('number'),
                   sloleks_entry.lemma_grammatical_features.get('gender'),
                   sloleks_entry.lemma_grammatical_features.get('person')))

        for word_form in sloleks_entry.all_forms:
            c.execute(word_form_stmt,
                      (sloleks_entry_id, word_form.lemma, word_form.part_of_speech, word_form.msd,
                       word_form.v_form, word_form.case, word_form.person, word_form.number,
                       word_form.gender, word_form.degree, word_form.clitic))
            word_form_id = c.lastrowid

            for representation in word_form.representations:
                c.execute(representation_stmt,
                          (sloleks_entry_id, word_form_id,
                           representation.form_representation, str(representation.norms),
                           representation.frequency, str(representation.accentuations),
                           representation.pronunciation_dict.get('IPA'),
                           representation.pronunciation_dict.get('SAMPA')))

    conn.commit()

def main() -> None:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pickles_dir = os.path.join(base_dir, 'data', 'pickles', 'sloleksentry_objects')

    conn = sqlite3.connect(os.path.join(base_dir, 'sloleks.db'))
    create_tables(conn)

    for file_name in tqdm(os.listdir(pickles_dir)):
        if file_name.endswith('.pkl'):
            file_path = os.path.join(pickles_dir, file_name)
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
                insert_sloleks_entry(conn, data)

    conn.close()

if __name__ == "__main__":
    main()
