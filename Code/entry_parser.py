from dataclasses import dataclass
from typing import List, Dict, Union
import xml.etree.ElementTree as ET


@dataclass(kw_only=True)
class Entry:
    lemma: str
    part_of_speech: str
    lemma_grammatical_features: Dict[str, str]
    xml_file: str
    forms_dict: Dict[str, 'WordForm']   ### ctrl+f "word_forms_dict_info"

    def __post_init__(self):
        self.gender: str = self.lemma_grammatical_features.get("gender")
        self.type: str = self.lemma_grammatical_features.get("type")
        self.aspect: str = self.lemma_grammatical_features.get("aspect")


@dataclass(kw_only=True)
class WordForm:
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
        self.grammar_name = ordered_gn(
            v_form=self.v_form,
            case=self.case,
            person=self.person,
            number=self.number,
            gender=self.gender
        )


class XMLParser:
    def __init__(self, xml_file: str):
        self.xml_file = xml_file
        self.entries = self.parse_xml_file()

    def parse_xml_file(self) -> List[Entry]:
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        entry_list = []

        for entry_element in root.findall('.//entry'):
            entry = self.parse_entry(entry_element)
            entry_list.append(entry)

        return entry_list

    def parse_entry(self, entry_element: ET.Element) -> Entry:
        lemma: str = entry_element.find('.//lemma').text
        part_of_speech: str = entry_element.find('.//category').text.lower()
        lemma_grammatical_features: Dict[
            str, str] = self.parse_grammatical_features(entry_element)



        word_forms_dict = {}  ### ctrl+f "word_forms_dict_info"
        for word_form_element in entry_element.findall('.//wordForm'):
            word_form = self.parse_form(word_form_element, lemma,
                                        part_of_speech)
            word_forms_dict[word_form.grammar_name] = word_form


        entry = Entry(
            lemma=lemma,
            part_of_speech=part_of_speech,
            lemma_grammatical_features=lemma_grammatical_features,
            xml_file=self.xml_file,
            forms_dict=word_forms_dict  ### ctrl+f "word_forms_dict_info"
        )

        return entry

    def parse_form(self, form_element: ET.Element, lemma: str,
                   part_of_speech: str) -> WordForm:
        form_representation: str = form_element.find('.//form').text

        msd: str = form_element.find('.//msd').text

        accentuation_element = form_element.find('.//accentuation/form')
        accentuation: str = accentuation_element.text if (
                accentuation_element is not None) else None

        freq_element = form_element.find(
            './/measureList/measure[@type="frequency"]')
        frequency: Union[int, None] = int(freq_element.text) if (
                freq_element is not None) else None

        gram_features: Dict[str, str] = self.parse_grammatical_features(
            form_element)

        pronunciation_data: list[
            dict[str, str]] = self.parse_pronunciation_data(form_element)

        word_form = WordForm(
            lemma=lemma,
            part_of_speech=part_of_speech,
            form_representation=form_representation,
            msd=msd,
            accentuation=accentuation,
            frequency=frequency,
            grammatical_features=gram_features,
            pronunciation_data=pronunciation_data
        )
        return word_form

    @staticmethod
    def parse_grammatical_features(element: ET.Element) -> Dict[
        str, str]:
        return {
            feature.get('name'): feature.text
            for feature in element.findall('.//grammarFeature')
        }

    @staticmethod
    def parse_pronunciation_data(word_form_element: ET.Element) -> list[
            Dict[str, str]]:
        pronunciation_data = []
        pronunciation_elements = word_form_element.findall('.//pronunciation')
        for pronunciation_element in pronunciation_elements:
            form_elements = pronunciation_element.findall('.//form')
            form_dict = {}
            for form_element in form_elements:
                key = form_element.attrib['script']
                define = form_element.text
                form_dict[key] = define
            pronunciation_data.append(form_dict)
        return pronunciation_data


def ordered_gn(
        *,
        v_form: str = None,
        case: str = None,
        person: str = None,
        number: str = None,
        gender: str = None,
):
    return concatenate_variables(v_form, case, person, number, gender)


def concatenate_variables(*items):
    result = "_".join(str(item) for item in items if item is not None)
    return result

# region TESTING
def test_formclass():
    word_form_instance = WordForm(
        form_representation="cats",
        lemma="cat",
        part_of_speech="noun",
        msd="akfhaso",
        accentuation="none",
        frequency=100,
        grammatical_features={"case": "nominative", "number": "plural",
                              "gender": "masculine"},
        pronunciation_data=[{"ipa": "/kæts/", "stress": "none"}]
    )

def test_parser():
    xml_path = (r"C:\Users\sangha\Documents\Danny's\slodict\Resources"
                r"\Markdown\XML\sloleks_3.0_sample.xml")
    parser = XMLParser(xml_path)
    print('\n'.join(map(str, parser.entries)))


if __name__ == "__main__":
    #test_formclass()
    test_parser()
# endregion
