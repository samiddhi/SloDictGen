from common.imports import *

import os
from typing import List, Set, Dict
from xml.etree import ElementTree as Et

from icecream import ic
from tqdm import tqdm

from slo_dict_gen_pkg import SloleksEntry, XMLParser

import random


def find_type_attributes(
        path: str,
        tag_name: str = "grammarFeature",
        attribute_name: str = "name"
) -> List[str]:
    """
    SUPER USEFUL. DON'T FORGET THIS EXISTS!!

    Indexes xml for all items of a given attribute for all elements of
    specified type. Default parses for all "name" in <grammarFeature>.

    e.g. <grammarFeature name="degree"> -> "degree"

    :param path: (str)
    :param tag_name: (str) <TYPE attribute="value">
    :param attribute_name: (str) <type ATTRIBUTE="value">
    :return: (List[str]) attribute values <type attribute="VALUE">
    """
    tree = Et.parse(path)
    root = tree.getroot()
    names = set()
    for element in root.findall(f'.//{tag_name}'):
        name = element.get(attribute_name)
        if name:
            names.add(name)
    return list(names)


def find_element_contents(
        path: str,
        tag_name: str = "grammarFeature",
        attribute_name: str = "name",
        attribute_value: str = "degree"
) -> Set[str]:
    """
    SUPER USEFUL. DON'T FORGET THIS EXISTS!!

    Finds all contents within elements of a specified type,
    attribute, and attribute value in a given XML file

    :param path: (str) The file path to the XML file.
    :param tag_name: (str) <TYPE attribute="value">
    :param attribute_name: (str) <type ATTRIBUTE="value">
    :param attribute_value: (str) <type attribute="VALUE">
    :return: Set[str] <type attribute="value">CONTENT</type>
    """
    tree = Et.parse(path)
    root = tree.getroot()
    element_contents = set()
    for element in root.findall(
            f'.//{tag_name}[@{attribute_name}="{attribute_value}"]'):
        element_contents.add(element.text)
    return element_contents


def generate_all_grammar_features(path: str) -> Dict[str, Set]:
    """
    Used to create the dictionary in grammar_utilities.return_gram_feat_type().
    Parses all xml files at path and returns a complete dict of grammar feature
    attributes and their corresponding element contents.

    e.g. dict['gender'] -> {'neuter', 'feminine', 'masculine'}

    :param path: (str)
    :return: Dict[str, Set]
    """
    if os.path.isfile(path):  # If path leads to a file
        files = [path]
    elif os.path.isdir(path):  # If path leads to a directory
        files = [os.path.join(path, f) for f in os.listdir(path) if
                 f.endswith('.xml')]
    else:
        raise ValueError("Invalid path provided.")

    dict_return = {}
    x = 0
    for file_path in files:
        attributes = find_type_attributes(
            path=file_path,
            tag_name="grammarFeature",
            attribute_name="name"
        )

        for attribute in attributes:
            if attribute not in dict_return:
                dict_return[attribute] = set()
            dict_return[attribute].update(
                find_element_contents(
                    path=file_path,
                    tag_name="grammarFeature",
                    attribute_name="name",
                    attribute_value=attribute
                )
            )
        print(f'{x} files done.')
        x += 1

    return dict_return


def sample_entry_obj(
        p_o_s: str = None,
        path: str = r"C:\Users\sangha\Documents\Danny's\SloDictGen"
                    r"\data\XML\all_isotopes.xml",
        lemma: str = None
) -> SloleksEntry:
    """
    Returns item with given part of speech OR given lemma

    :param p_o_s: default None
    :param lemma: default None
    :param path: default all_isotopes.xml
    :return:
    """
    parser: XMLParser = XMLParser(path)
    random.shuffle(parser.entries)
    if lemma is not None and p_o_s is not None:
        for entry in parser.entries:
            if entry.part_of_speech == p_o_s and entry.lemma == lemma:
                return entry
        raise ic(Exception(f"No {p_o_s} '{lemma}' found in entries from"
                           f" {path}"))
    elif lemma is not None or p_o_s is not None:
        for entry in parser.entries:
            if entry.part_of_speech == p_o_s or entry.lemma == lemma:
                return entry
        raise ic(Exception(f"No matching entries from {path}"))
    else:
        return parser.entries[0]


def find_file_with_grammar_feature_content(
        path: str,
        tag_name: str,
        attribute_name: str,
        attribute_value: str,
        element_content: str,
        all: bool = False
):
    """
    Finds all files containing instance of provided element content

    :param path: The file path to the XML file.
    :param tag_name: (str) <TYPE attribute="value">
    :param attribute_name: (str) <type ATTRIBUTE="value">
    :param attribute_value: (str) <type attribute="VALUE">
    :param element_content: (str) <type attribute="value">CONTENT</type>
    :return: (List[str]) list of files containing
    """

    '''
    Args:
        path=,
        tag_name="",
        attribute_name="name",
        attribute_value="",
        element_content=""
        '''
    filepaths = []
    for filename in os.listdir(path):
        if filename.endswith('.xml'):
            filepath = os.path.join(path, filename)
            tree = Et.parse(filepath)
            root = tree.getroot()
            for element in root.iter():
                if (element.tag == tag_name and element.attrib.get(
                        attribute_name) == attribute_value and element.text
                        == element_content):
                    if all:
                        filepaths.append(filename)
                        break
                    else:
                        return ic(filename)

    return ic(filepaths)


def record_pos_isotopes(
        path: str,
        write: bool = False,
        count: bool = False
) -> Dict[str, Dict[int, Dict[str, ...]]]:
    """
    Parses XML files and records the total number of each isotope instance.
    Where isotope refers to the number of wordforms a particular part of
    speech has.

    E.g. a verb with 2 conjugations is isotope "verb-2".

    :param write: Whether to save a new XML or not
    :param count: Whether to tally the total for each isotope
    :param path: Either one file or directory containing multiple
    :return: Dictionary with structure:
            {
                "part_of_speech" : {
                    wordforms_int : {
                        "ct": isotope_quantity_int,
                        "lemma": example_entry_lemma,
                        "file": example_entry_location
                    },
                    ...
                },
                ...
            }
    """

    ''' EXAMPLE USAGE
    entries_info = record_pos_isotopes(parent_path)
    for pos, formctdict in entries_info.items():
        print(f'\n{pos}:')
        for formct, info in formctdict.items():
            print(
                f"\t{formct:<12} : {str(info['ct']) + ' entries ':<15} -e.g.- "
                f"{info.get('lemma', ' '):<15} ->"
                f" {info.get('file', ' ').split('_')[-1]}")
    '''
    results: Dict[str, Dict[int, Dict[str, ...]]] = {}
    lexicon = Et.Element('lexicon')

    def parse_xml_file(file_path):
        tree = Et.parse(file_path)
        root = tree.getroot()

        entries = root.findall('entry')
        #random.shuffle(entries)

        for entry in entries:
            part_of_speech = entry.find('head/grammar/category').text
            lemma = entry.find('head/headword/lemma').text
            word_forms = entry.findall(
                'body/wordFormList/wordForm/formRepresentations'
                '/orthographyList/orthography/form')
            isotope = len(word_forms)

            # Only tallies isotopes if count = True
            if ((part_of_speech not in results or isotope not in results) or
                    count[
                    part_of_speech]):
                if part_of_speech not in results:
                    results[part_of_speech] = {}
                if isotope not in results[part_of_speech]:
                    results[part_of_speech][isotope] = {'ct': 0}

                results[part_of_speech][isotope]['ct'] += 1

                isotope_name = f'{part_of_speech}-{isotope}'

                comment_element = Et.Comment(isotope_name)
                lexicon.append(comment_element)

                # Construct full entry XML element only for isotope examples
                full_entry = Et.Element('entry')
                full_entry.extend(entry)
                lexicon.append(full_entry)

                # use entry as isotope example
                results[part_of_speech][isotope].update({
                    'lemma': lemma,
                    'file': file_path
                })

    if os.path.isdir(path):
        xml_files = [f for f in os.listdir(path) if f.endswith('.xml')]
        with tqdm(total=len(xml_files), desc='Parsing XML files') as pbar:
            for filename in xml_files:
                file_path = os.path.join(path, filename)
                parse_xml_file(file_path)
                pbar.update(1)
    elif os.path.isfile(path) and path.endswith('.xml'):
        parse_xml_file(path)
    else:
        print(f"Invalid path: {path}")

    if write:
        # Write lexicon to a new XML file with formatting
        formatted_xml = Et.tostring(lexicon, encoding='unicode', method='xml')
        root = Et.fromstring(
            formatted_xml)  # Parse string back into ElementTree object
        Et.indent(root)  # Add proper indentation
        formatted_xml = Et.tostring(root, encoding='unicode',
                                    method='xml')  # Convert back to string

        destination = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                       r"\Markdown\XML\all_isotopes.xml")
        with open(destination, 'w', encoding='utf-8') as f:
            f.write(formatted_xml)

    return results


if __name__ == "__main__":
    sample_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                   r"\Markdown\XML\sloleks_3.0_sample.xml")
    sample_parent = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                     r"\Markdown\XML")
    parent_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                   r"\Sloleks.3.0")
    example_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                    r"\Sloleks.3.0\sloleks_3.0_009.xml")

    entries_info = record_pos_isotopes(example_path)
    for pos, formctdict in entries_info.items():
        print(f'\n{pos}:')
        for formct, info in formctdict.items():
            print(
                f"\t{formct:<12} : {str(info['ct']) + ' entries ':<15} -e.g.- "
                f"{info.get('lemma', ' '):<15} ->"
                f" {info.get('file', ' ').split('_')[-1]}")