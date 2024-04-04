from typing import Dict, List
from dataclasses import dataclass
import xml.etree.ElementTree as Et

from slo_dict_gen_pkg.grammar_utilities import ordered_grammar_name


@dataclass(kw_only=True)
class SloleksEntry:
    """
    Represents an entry in the Sloleks database.

    Instance Variables:
        lemma (str)

        part_of_speech (str)

        lemma_grammatical_features (Dict[str, str]):
            Dictionary that may contain:  ['gender', 'vform', 'form',
            'animate', 'definiteness', 'number', 'person', 'type', 'degree',
            'aspect', 'case']

        xml_file (str):
            XML file path

        forms_dict (Dict[str, WordForm]):
            Dictionary mapping form grammar names to WordForm objects.
    """
    lemma: str
    part_of_speech: str
    lemma_grammatical_features: Dict[str, str]
    xml_file: str
    forms_dict: Dict[str, 'WordForm']


@dataclass(kw_only=True)
class WordForm:
    """
    Represents a word form with associated grammatical information.

    Instance Variables:
        lemma (str): Lemma of form's parent entry.

        part_of_speech (str): Part of speech of form/lemma.

        form_representation (str): The word form.

        msd (str): Morphosyntactic descriptor of the form.

        accentuation (str): Accentuation of the form.

        frequency (int): Form's frequency in gigafida.

        grammatical_features (Dict[str, str]): Gram. features of the form.

        pronunciation_data (List[Dict[str, str]]):  Pronunciation data of the
        form. List of dicts with key as pronunciation notation (IPA,
        SAMPA), and value as pronunciation string.

        v_form (str): Verb form.

        case (str): Grammatical case.

        person (str): Grammatical person.

        number (str): Singular/Dual/Plural.

        gender (str): Grammatical gender.

        grammar_name (str): Grammar name used for indexing WordForms within
        Entry.
    """
    # info from parent entry
    lemma: str
    part_of_speech: str

    # info for word form
    form_representation: str
    msd: str
    accentuation: str
    frequency: int
    grammatical_features: Dict[str, str]
    pronunciation_data: List[Dict[str, str]]

    # Vars to be pulled from grammatical_features & pronunciation_data
    v_form: str = None
    case: str = None
    person: str = None
    number: str = None
    gender: str = None

    def __post_init__(self):
        self.v_form = self.grammatical_features.get("vform", None)
        self.case = self.grammatical_features.get("case", None)
        self.person = self.grammatical_features.get("person", None)
        self.number = self.grammatical_features.get("number", None)
        self.gender = self.grammatical_features.get("gender", None)
        self.grammar_name = ordered_grammar_name(
            v_form=self.v_form,
            case=self.case,
            person=self.person,
            number=self.number,
            gender=self.gender
        )


class XMLParser:
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
        self.xml_file = xml_file
        self.entries = self._parse_xml_file()

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

        word_forms_dict = {
            self._parse_form(form_element, lemma, part_of_speech).grammar_name:
                self._parse_form(form_element, lemma, part_of_speech)
            for form_element in entry_element.findall('.//wordForm')}

        return SloleksEntry(
            lemma=lemma,
            part_of_speech=part_of_speech,
            lemma_grammatical_features=lemma_grammatical_features,
            xml_file=self.xml_file,
            forms_dict=word_forms_dict
        )

    def _parse_form(
            self,
            form_element: Et.Element,
            lemma: str,
            part_of_speech: str
    ) -> WordForm:
        """
        Parses a <wordForm> ElementTree element into a WordForm object.

        :param form_element: <wordForm> ElementTree element to parse.
        :param lemma: Lemma of the wordForm's parent entry.
        :param part_of_speech: Part of speech of the wordForm/lemma.
        :return: WordForm object representing the parsed wordForm element.
        """
        form_representation = form_element.find('.//form').text
        msd = form_element.find('.//msd').text

        accentuation_element = form_element.find('.//accentuation/form')
        accentuation = accentuation_element.text if (accentuation_element is
                                                     not None) else None

        freq_element = form_element.find(
            './/measureList/measure[@type="frequency"]')
        frequency = int(
            freq_element.text) if freq_element is not None else None

        gram_features = self._parse_grammatical_features(form_element)
        pronunciation_data = self._parse_pronunciation_data(form_element)

        return WordForm(
            lemma=lemma,
            part_of_speech=part_of_speech,
            form_representation=form_representation,
            msd=msd,
            accentuation=accentuation,
            frequency=frequency,
            grammatical_features=gram_features,
            pronunciation_data=pronunciation_data
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


# region TESTING
def test_form_class():
    """
    Test WordForm class. Contains sample WordForm initialization data so no
    parse necessary
    """
    word_form_instance = WordForm(
        form_representation="cats",
        lemma="cat",
        part_of_speech="noun",
        msd="idk",
        accentuation="none",
        frequency=100,
        grammatical_features={"case": "nominative", "number": "plural",
                              "gender": "masculine"},
        pronunciation_data=[{"DPA": "/katz/", "stress": "none"}]
    )
    print(word_form_instance)


def test_parser(path):
    """
    Test XMLParser class.
    """
    parser = XMLParser(path)
    print('\n'.join(map(str, parser.entries)))


def find_element_titles(
        path,
        element="grammarFeature",
        title="name"
):
    """
    SUPER USEFUL. DON'T FORGET THIS EXISTS!!

    Indexes xml for all items of a
    given title
    for all elements of specified
    type. Default parses for all "name" in <grammarFeature>.

    e.g. <grammarFeature name="degree">positive</grammarFeature> -> "positive"

    :param path:
    :param title: <element TITLE="value">
    :param element: <ELEMENT title="value">
    :return: list of all values for <element title="VALUE">
    """
    tree = Et.parse(path)
    root = tree.getroot()
    names = set()
    for element in root.findall(f'.//{element}'):
        name = element.get(title)
        if name:
            names.add(name)
    return list(names)


if __name__ == "__main__":
    xml_path = (r"C:\Users\sangha\Documents\Danny's\slodict\Resources"
                r"\Markdown\XML\sloleks_3.0_sample.xml")

# endregion
