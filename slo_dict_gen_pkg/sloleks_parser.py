from slo_dict_gen_pkg.grammar_utils import ordered_grammar_name
from common.imports import *
from dataclasses import dataclass
import xml.etree.ElementTree as Et
from collections import defaultdict



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

    all_forms: List['WordForm']
    forms_dict: Dict[str, List['WordForm']]

    all_reps: List['Representation'] = None
    reps_dict: Dict[str, List['Representation']] = None


    def __post_init__(self):
        self.all_reps = []
        self.reps_dict = defaultdict(list)

        for word_form in self.all_forms:
            for representation in word_form.representations:
                self.all_reps.append(representation)
                self.reps_dict[word_form.grammar_names].append(representation)

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

    # List of sublists whose first element is the representation string
    # and whose second element is the "norm" attribute value (aka. what the
    # gray-small-ital css format text will be under it in the table)
    representations: List['Representation']

    #
    grammatical_features: Dict[str, str]

    # Vars to be pulled from grammatical_features & pronunciation_data
    v_form: str = None
    case: str = None
    person: str = None
    number: str = None
    gender: str = None
    degree: str = None
    clitic: str = None

    def __post_init__(self):
        self.v_form = self.grammatical_features.get("vform", None)
        self.case = self.grammatical_features.get("case", None)
        self.person = self.grammatical_features.get("person", None)
        self.number = self.grammatical_features.get("number", None)
        self.gender = self.grammatical_features.get(
            "gender",
             "agender" if self.part_of_speech in ["pronoun",
                                                  "adjective",
                                                  "numeral"]
             else
             None)
        self.degree = self.grammatical_features.get("degree", None)
        self.clitic = self.grammatical_features.get("clitic", None)
        self.grammar_names = ordered_grammar_name(
            v_form=self.v_form,
            case=self.case,
            person=self.person,
            number=self.number,
            gender=self.gender,
            degree=self.degree,
            clitic=self.clitic,
            return_type="tuple"
        )


@dataclass(kw_only=True)
class Representation:
    form_representation: str
    norms: List[str]
    frequency: int
    accentuations: List[str]
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
        forms: List[WordForm] = []
        word_forms: Dict[str, List[WordForm]] = {}
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

        accentuations: List(str) = []
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


# region TESTING
def test_parser(path):
    """
    Test XMLParser class.
    """
    parser = XMLParser(path)
    for entry in parser.entries:
        print(f'{entry.lemma}:')
        for wordform_list in entry.forms_dict.values():
            for wordform in wordform_list:
                print(f'\t{wordform.grammar_names}')
                for rep in wordform.representations:
                    print(f'\t\t{rep}')


if __name__ == "__main__":
    sample_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                   r"\Markdown\XML\all_isotopes.xml")
    parent_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                   r"\Sloleks.3.0")
    example_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                    r"\Sloleks.3.0\sloleks_3.0_002.xml")

    test_parser(sample_path)

# endregion
