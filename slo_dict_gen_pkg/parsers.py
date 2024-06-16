
from common.imports import *
from slo_dict_gen_pkg.sloleks_objs import SloleksEntry, WordForm, \
    Representation
from slo_dict_gen_pkg.grammar_utils import ordered_grammar_name, de_critic, ALPHA

from dataclasses import dataclass
from collections import defaultdict

import xml.etree.ElementTree as Et
from bs4 import BeautifulSoup

import sqlite3
import pickle
import json
import os
import re


# SLOLEKS

class XMLtoSloleksEntrys:
    """
    Parses XML files containing entries and forms data into SloleksEntry
    objects.

    Public Methods:
        none.

    Instance Variables:
        xml_file (str): Path to the XML file.
        entries (List[SloleksEntry]): List of SloleksEntry objects parsed from
        the XML file.
    """

    def __init__(self, xml_file: str):
        """
        Initializes an XMLParser instance.

        :param xml_file: Path to the XML file to parse.
        """
        self.xml_file: str = xml_file
        self.entries: List[SloleksEntry] = self._parse_xml_file()

    def __str__(self):
        return self.entries

    def __iter__(self):
        return iter(self.entries)

    def __len__(self):
        return len(self.entries)

    def _parse_xml_file(self) -> List[SloleksEntry]:
        """
        Parses xml file for all <entry> ElementTree elements and initiates
        processing them into SloleksEntry class objects.

        :return: List of SloleksEntry class objects.
        """
        tree = Et.parse(self.xml_file)
        root = tree.getroot()
        entry_list = [self._parse_entry(entry_element) for entry_element
                      in root.findall('.//entry')]

        return entry_list

    def _parse_entry(self, entry_element: Et.Element) -> SloleksEntry:
        """
        Parses an <entry> ElementTree element into a SloleksEntry object.

        :param entry_element: <entry> ElementTree element to parse.
        :return: SloleksEntry object representing the parsed entry.
        """
        lemma = entry_element.find('.//lemma').text
        part_of_speech = entry_element.find('.//category').text.lower()
        lemma_grammatical_features = self._parse_grammatical_features(
            entry_element)

        # Compiles a general list of forms and a dict by each grammar name
        forms: List[WordForm] = []
        word_forms: Dict[str, List[WordForm]] = defaultdict()
        for wordForm_element in entry_element.findall('.//wordForm'):
            form: WordForm = self._parse_wordform(
                wordForm_element,
                lemma,
                part_of_speech
            )
            forms.append(form)
            key: List[str] = form.grammar_names
            if key not in word_forms:
                word_forms[key] = []
            word_forms[key].append(form)

        return SloleksEntry(
            lemma=lemma,
            part_of_speech=part_of_speech,
            lemma_grammatical_features=lemma_grammatical_features,
            xml_file=self.xml_file,
            forms_dict=word_forms,
            all_forms=forms
        )

    def _parse_wordform(
            self,
            wordform_element: Et.Element,
            lemma: str,
            part_of_speech: str
    ) -> WordForm:
        """
        Parses a <wordForm> ElementTree element into a WordForm object.

        :param wordform_element: <wordForm> ElementTree element to parse.
        :param lemma: Lemma of the wordForm's parent entry.
        :param part_of_speech: Part of speech of the wordForm/lemma.
        :return: WordForm object representing the parsed wordForm element.
        """

        msd = wordform_element.find('.//msd').text

        gram_features: Dict[str, str] = self._parse_grammatical_features(
            wordform_element)

        # Compiles a general list of forms and a dict by each grammar name
        representations: List[Representation] = []

        # <orthography> and <accentuation> are twins in <formRepresentations>
        orthographies: List = wordform_element.findall('.//orthography')
        accentuations: List = wordform_element.findall('.//accentuation')
        pronunciations: List = wordform_element.findall('.//pronunciation')

        for orthography in orthographies:
            while 0 < len(orthographies) < len(accentuations):
                representation: Representation = self._parse_representation(
                    part_of_speech=part_of_speech,
                    orthography_element=orthographies.pop(0),
                    accentuation_elements=[accentuations.pop(0),
                                           accentuations.pop(0)],
                    pronunciation_elements=[pronunciations.pop(0),
                                            pronunciations.pop(0)],
                    wordform_grammar_features=gram_features
                )
                representations.append(representation)

        while orthographies:
            representation: Representation = self._parse_representation(
                part_of_speech=part_of_speech,
                orthography_element=orthographies.pop(0),
                accentuation_elements=[] if not accentuations else
                [accentuations.pop(0)],
                pronunciation_elements=[] if not pronunciations else
                [pronunciations.pop(0)],
                wordform_grammar_features=gram_features
            )
            representations.append(representation)

        return WordForm(
            lemma=lemma,
            part_of_speech=part_of_speech,
            representations=representations,
            msd=msd,
            grammatical_features=gram_features
        )

    @staticmethod
    def _parse_representation(
            orthography_element: Et.Element,
            accentuation_elements: List[Et.Element],
            pronunciation_elements: List[Et.Element],
            wordform_grammar_features: Dict[str, str],
            part_of_speech: str

    ) -> Representation:

        norms = []

        if part_of_speech in ["pronoun", "adjective", "numeral"]:
            norms.append(wordform_grammar_features.get("gender", "agender"))

        try:
            norms.append(orthography_element.attrib['norm'])
        except KeyError:
            pass

        if wordform_grammar_features.get("negative", None) == "yes":
            norms.append("negative")
        if wordform_grammar_features.get("definiteness", None) == "yes":
            norms.append("definite")
        if wordform_grammar_features.get("definiteness", None) == "no":
            norms.append("indefinite")
        if wordform_grammar_features.get("animate", None) == "yes":
            norms.append("animate")
        if wordform_grammar_features.get("animate", None) == "no":
            norms.append("inanimate")
        if wordform_grammar_features.get("degree", None) == 'positive':
            norms.append('positive')
        if wordform_grammar_features.get("degree", None) == 'comparative':
            norms.append('comparative')
        if wordform_grammar_features.get("degree", None) == 'superlative':
            norms.append('superlative')

        form_representation: str = orthography_element.find('.//form').text
        freq: int = int(orthography_element.find('.//measure['
                                                 '@type="frequency"]').text)

        accentuations: List[str] = []
        for accentuation_element in accentuation_elements:
            accentuations.extend(
                [form_element.text for form_element
                 in accentuation_element.findall('.//form')]
            )

        pronunciations: defaultdict[str, str] = defaultdict(str)
        for pronunciation_element in pronunciation_elements:
            for form_element in pronunciation_element.findall('.//form'):
                pronunciations[
                    form_element.attrib['script']] += '\n' + form_element.text

        return Representation(
            form_representation=form_representation,
            norms=norms,
            frequency=freq,
            accentuations=accentuations,
            pronunciation_dict=pronunciations
        )

    @staticmethod
    def _parse_grammatical_features(element: Et.Element) -> Dict[str, str]:
        """
        Parses grammatical features from an ElementTree element.

        :param element: ElementTree element containing grammatical features.
        :return: Dictionary mapping feature names to their corresponding
            values.
        """
        return {
            feature.get('name'): feature.text
            for feature in element.findall('.//grammarFeature')
        }

    @staticmethod
    def _parse_pronunciation_data(word_form_element: Et.Element) -> list[
        Dict[str, str]]:
        """
        Parses pronunciation data from an ElementTree Element.

        :param word_form_element: <wordForm> (ElementTree module) element.
        :return: List of dictionaries with key as script (IPA, SAMPA) and
            value as pronunciation string.
        """
        pronunciation_data = []
        for pronunciation_element in word_form_element.findall(
                './/pronunciation'):
            pronunciation_data.append(
                {form_element.attrib['script']: form_element.text
                 for form_element in pronunciation_element.findall('.//form')})
        return pronunciation_data

    @staticmethod
    def test(path) -> None:
        """
        Test XMLParser class.
        """
        parser = XMLtoSloleksEntrys(path)
        for entry in parser.entries:
            print(f'{entry.lemma}:')
            for wordform_list in entry.forms_dict.values():
                for wordform in wordform_list:
                    print(f'\t{wordform.grammar_names}')
                    for rep in wordform.representations:
                        print(f'\t\t{rep}')


class LemmaFormsParser:
    """Parses xml file for the lemma of each entry and its respective forms"""

    def __init__(self, directory: str) -> None:
        """
        :param directory: The directory path containing XML files.
        """
        self.directory = directory
        self.data: Dict[str, List[str]] = {}

    def parse_xml_files(self) -> None:
        """Parse XML files in the specified directory and build the data dictionary."""
        for filename in os.listdir(self.directory):
            if filename.endswith(".xml"):
                filepath = os.path.join(self.directory, filename)
                tree = Et.parse(filepath)
                root = tree.getroot()
                for entry in root.findall(".//entry"):
                    lemma = entry.find(".//lemma").text.strip()
                    for orthlist in entry.findall(".//orthographyList"):
                        for form in orthlist.findall(".//form"):
                            wordform = form.text.strip()
                            if lemma in self.data:
                                self.data[lemma].append(wordform)
                            else:
                                self.data[lemma] = [wordform]

    def save_data_as_json(self, filepath: str) -> None:
        """
        Save the parsed data as JSON to a file.

        :param filepath: The file path to save the JSON data.
        """
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)


def sloleks_to_pickles() -> None:
    from tqdm import tqdm
    import pickle
    slolex_dir = os.path.abspath(os.path.join(proj_dir, 'data', 'Sloleks.3.0'))

    xml_files = [f for f in os.listdir(slolex_dir) if f.endswith(".xml")]

    for filename in tqdm(xml_files, desc='Processing files'):
        # Process the current XML file
        entries = list(XMLtoSloleksEntrys(os.path.join(slolex_dir, filename)))

        # Save the entries as a pickle file with the same name as the XML file
        pickle_file_path = os.path.join(
            proj_dir, 'data', 'pickles', 'sloleksentry_objects',
            os.path.splitext(filename)[0] + '.pkl'
        )
        with open(pickle_file_path, 'wb') as f:
            pickle.dump(entries, f)

# /SLOLEKS

#SSKJ

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

# /SSKJ

if __name__ == "__main__":
    pkl_dir = os.path.abspath(
        os.path.join(proj_dir, 'data', 'pickles', 'sskj_html_objs'))
    all_sskjentrys: List[SskjEntry] = get_sskjentrys(pkl_dir)

    SskjEntrystoSQLite(
        db_name="sskj_entries.db",
        data=all_sskjentrys
    )
