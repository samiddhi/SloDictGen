import xml.etree.ElementTree as ET
from typing import List, Dict, Union
import tkinter as tk
from tkhtmlview import HTMLLabel
#from entry_classes import Entry, WordForm
from entry_parser import Entry, WordForm

COPY = "noun"


def parse_xml_file(xml_file: str) -> List[Entry]:
    entries: List[Entry] = []
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for entry_element in root.findall('.//entry'):
        lemma: str = entry_element.find('.//lemma').text
        part_of_speech: str = entry_element.find('.//category').text.lower()
        lemma_grammatical_features: Dict[str, str] = {
            feature.get('name'): feature.text for feature in
            entry_element.findall('.//grammarFeature')}

        word_forms_dict = {}
        for word_form_element in entry_element.findall('.//wordForm'):

            form_representation: str = word_form_element.find('.//form').text

            # Get pronunciation stuff
            pronunciation_data: list[dict[str, str]] = []
            pronunciation_elements = word_form_element.findall(
                './/pronunciation')
            for pronunciation_element in pronunciation_elements:
                form_elements = pronunciation_element.findall('.//form')
                form_dict = {}
                for form_element in form_elements:
                    key = form_element.attrib['script']
                    define = form_element.text
                    form_dict[key] = define
                pronunciation_data.append(form_dict)

            morphosyntactic_tags: str = word_form_element.find('.//msd').text

            grammatical_features: Dict[str, str] = {
                feature.get('name'): feature.text for feature in
                word_form_element.findall('.//grammarFeature')}

            accentuation_element = word_form_element.find(
                './/accentuation/form')
            accentuation: str = accentuation_element.text if (
                    accentuation_element is not None) else None

            freq_element = word_form_element.find(
                './/measureList/measure[@type="frequency"]')
            frequency: Union[int, None] = int(
                freq_element.text) if freq_element is not None else None

            word_form = WordForm(
                form_representation=form_representation,
                part_of_speech=part_of_speech,
                lemma=lemma,
                msd=morphosyntactic_tags,
                accentuation=accentuation,
                frequency=frequency,
                grammatical_features=grammatical_features,
                pronunciation_data=pronunciation_data
            )

            word_forms_dict[word_form.grammar_name] = word_form

        entry = Entry(
                    lemma=lemma,
                    part_of_speech=part_of_speech,
                    lemma_grammatical_features=lemma_grammatical_features,
                    xml_file=xml_file,
                    forms_dict=word_forms_dict
                )
        entries.append(entry)
    return entries


def get_one_of_each() -> List[Entry]:
    directory: str = (r"C:\Users\sangha\Documents\Danny's\slodict"
                      r"\Resources\Sloleks.3.0")
    xml_file: str = (r"C:\Users\sangha\Documents\Danny's\slodict"
                     r"\Resources\Markdown\XML\sloleks_3.0_sample.xml")
    return (xml_file)


def display_html(content):
    root = tk.Tk()
    html_label = HTMLLabel(root, html=content)
    html_label.pack(fill="both", expand=True)
    html_label.fit_height()
    root.mainloop()


def main():
    entries = get_one_of_each()

    for entry in entries:
        pos = entry.part_of_speech
        if pos == "noun":
            table_html = eval(f'formatting.{pos}()')


if __name__ == "__main__":
    main()
