from common.imports import *
from dataclasses import dataclass
import xml.etree.ElementTree as Et

from slo_dict_gen_pkg.grammar_utils import ordered_grammar_name


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
    forms_dict: Dict[str, List['WordForm']]
    all_forms: List['WordForm']
    all_reps: List['Representation']
    non_weird_forms: List[str] = None
    why_its_weird: Dict[str, str] = None

    def __post_init__(self):
        self.non_weird_forms: List[str] = []
        self.why_its_weird: Dict[str, str] = {}
        for word_form in self.all_forms:
            for representation in word_form.representation_list:
                if word_form.grammatical_features.get("negative", None) == "yes":
                    self.why_its_weird[representation.form] = "negative"
                elif word_form.grammatical_features.get("animate", None) == "no":
                    self.why_its_weird[representation.form] = "inanimate"
                elif word_form.grammatical_features.get("animate", None) == "yes":
                    self.why_its_weird[representation.form] = "animate"
                else:
                    self.non_weird_forms.append(representation.form)


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
    msd: str
    accentuation: str
    frequency: int

    # List of sublists whose first element is the representation string
    # and whose second element is the "norm" attribute value (aka. what the
    # gray-small-ital css format text will be under it in the table)
    representation_list: List['Representation']

    #
    grammatical_features: Dict[str, str]

    #
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


@dataclass(kw_only=True)
class Representation:
    form: str
    norm: str
    frequency: int
    accentuation: str
    pronunciation_dict: dict


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

        # Compiles a general list of forms and a dict by each grammar name
        forms_list = []
        word_forms_dict: Dict[str, List[WordForm]] = {}
        for wordForm_element in entry_element.findall('.//wordForm'):
            form: WordForm = self._parse_wordForm(
                wordForm_element,
                lemma,
                part_of_speech
            )
            forms_list.append(form)
            key: str = form.grammar_name
            if key not in word_forms_dict:
                word_forms_dict[key] = []
            word_forms_dict[key].append(form)

        return SloleksEntry(
            lemma=lemma,
            part_of_speech=part_of_speech,
            lemma_grammatical_features=lemma_grammatical_features,
            xml_file=self.xml_file,
            forms_dict=word_forms_dict,
            all_forms=forms_list
        )

    def _parse_wordForm(
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

        representation_list: List[Representation] = []
        for formrepresentation_element in wordform_element.findall(
                'formRepresentations'):
            orthography_elements = formrepresentation_element.findall(
                'orthographyList/orthography')
            for orthography_element in orthography_elements:
                form = orthography_element.find('form').text
                norm = orthography_element.get('norm', '')
                frequency_element = orthography_element.find(
                    'measureList/measure[@type="frequency"]')
                frequency = int(
                    frequency_element.text) if frequency_element is not None else 0
            accentuation = ""  # Implement this
            pronunciation_dict = {}  # Implement this


            representation_obj = Representation(
                form=form,
                norm=norm,
                frequency=frequency,
                accentuation=accentuation,
                pronunciation_dict=pronunciation_dict
            )
            representation_list.append(representation_obj)

        msd = wordform_element.find('.//msd').text

        accentuation_element = wordform_element.find('.//accentuation/form')
        accentuation = accentuation_element.text if (accentuation_element is
                                                     not None) else None

        freq_element = wordform_element.find(
            './/measureList/measure[@type="frequency"]')
        frequency = int(
            freq_element.text) if freq_element is not None else None

        gram_features = self._parse_grammatical_features(wordform_element)
        pronunciation_data = self._parse_pronunciation_data(wordform_element)

        return WordForm(
            lemma=lemma,
            part_of_speech=part_of_speech,
            representation_list=representation_list,
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


if __name__ == "__main__":
    sample_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                   r"\Markdown\XML\sloleks_3.0_sample.xml")
    parent_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                   r"\Sloleks.3.0")
    example_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                    r"\Sloleks.3.0\sloleks_3.0_028.xml")

# endregion
