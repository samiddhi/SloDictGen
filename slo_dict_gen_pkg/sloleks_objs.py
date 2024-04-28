from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

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

    all_forms: List['WordForm']
    forms_dict: Dict[str, List['WordForm']]

    all_reps: List['Representation'] = None
    reps_dict: Dict[str, List['Representation']] = None

    def __post_init__(self) -> None:
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
