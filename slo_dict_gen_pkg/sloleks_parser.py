from slo_dict_gen_pkg.sloleks_objs import SloleksEntry, WordForm, \
    Representation
from common.imports import *
from collections import defaultdict
import xml.etree.ElementTree as Et
import json
import os


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


if __name__ == "__main__":
    pass
