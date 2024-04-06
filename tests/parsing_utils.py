from common.imports import *

import os
from typing import List, Set, Dict
from xml.etree import ElementTree as Et

from icecream import ic
from tqdm import tqdm

from slo_dict_gen_pkg import SloleksEntry, XMLParser


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


def sample_entry_obj(p_o_s: str = "noun") -> SloleksEntry:
    file = (r"C:\Users\sangha\Documents\Danny's\SloDictGen"
            r"\data"
            r"\Markdown\XML\sloleks_3.0_sample.xml")
    parser: XMLParser = XMLParser(file)
    for entry in parser.entries:
        if entry.part_of_speech == p_o_s:
            return entry
    raise ic(Exception(f"No '{p_o_s}' found in entries from {file}"))


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


def parse_xml_files_in_directory(path):
    results: Dict[str, Dict[str, Dict[str, ...]]] = {}

    def example_usage(path_name):
        entries_info = parse_xml_files_in_directory(path_name)
        for pos, formctdict in entries_info.items():
            print(f'\n{pos}:')
            for formct, info in formctdict.items():
                print(
                    f"\t{formct:<12} : {str(info['ct']) + ' entries ':<15} -e.g.- "
                    f"{info['lemma']:<15} -> {info['file'].split('_')[-1]}")

    def parse_xml_file(file_path):
        tree = Et.parse(file_path)
        root = tree.getroot()

        entries = root.findall('entry')

        for entry in entries:
            category = entry.find('head/grammar/category').text
            lemma = entry.find('head/headword/lemma').text
            word_forms = entry.findall('body/wordFormList/wordForm')
            num_word_forms = len(word_forms)
            num_word_forms_str = f'{num_word_forms} form(s)'
            if category not in results:
                results[category] = {num_word_forms_str: {'ct': 1}}
                if not lemma.istitle():
                    results[category][num_word_forms_str].update({
                        'lemma': lemma,
                        'file': file_path
                    })
            elif num_word_forms_str not in results[category]:
                results[category][num_word_forms_str] = {'ct': 1}
                if not lemma.istitle():
                    results[category][num_word_forms_str].update({
                        'lemma': lemma,
                        'file': file_path
                    })
            else:
                results[category][num_word_forms_str]['ct'] += 1

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

    return results


if __name__ == "__main__":
    sample_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                   r"\Markdown\XML\sloleks_3.0_sample.xml")
    sample_parent = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                     r"\Markdown\XML")
    parent_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                   r"\Sloleks.3.0")
    example_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                    r"\Sloleks.3.0\sloleks_3.0_020.xml")

    entries_info = parse_xml_files_in_directory(parent_path)
    for pos, formctdict in entries_info.items():
        print(f'\n{pos}:')
        for formct, info in formctdict.items():
            print(
                f"\t{formct:<12} : {str(info['ct']) + ' entries ':<15} -e.g.- "
                f"{info.get('lemma'," "):<15} ->"
                f" {info.get('file'," ").split('_')[-1]}")
