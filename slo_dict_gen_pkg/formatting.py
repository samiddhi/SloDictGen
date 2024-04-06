from common.imports import *
from slo_dict_gen_pkg.entry_parser import SloleksEntry, WordForm, XMLParser
from tests.parsing_utils import sample_entry_obj
from slo_dict_gen_pkg.grammar_utils import ordered_grammar_name, return_gram_feat_type, gfcat, table_types

from airium import Airium
# from itertools import product
import pyperclip
import os
import sys

# Add the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def format_string(entry: SloleksEntry, grammar_name: str):
    com_pref = common_prefix(
        [rep.form_representation for gn, rep in entry.forms_dict.items()])
    bolded = bold_except(entry.forms_dict[grammar_name].form_representation,
                         com_pref)
    grayed = gray_unused(entry.forms_dict[grammar_name].frequency, bolded)
    return grayed


def common_prefix(strings) -> str:
    if not strings:
        return ""
    return str(os.path.commonprefix(strings))


def bold_except(word: str, prefix: str) -> str:
    to_bold = word[len(prefix):]  # Remove the prefix from the word
    if to_bold != '':
        return f"{prefix}<b>{to_bold}</b>"
    else:
        return word


def gray_unused(frequency: int, to_gray: str) -> str:
    if frequency == 0:
        return f"<span class=gray>{to_gray}</span>"
    else:
        return to_gray


def ipa(form: WordForm) -> str:
    formatted = ""
    for pronunciation_style in form.pronunciation_data:
        formatted += f'<br>{pronunciation_style["IPA"]}'
    return formatted


### IMPLEMENTING

class GrammarTableGen:
    """
    Generates a grammar table from a SloleksEntry object

    Instance variables:
        table (str)
    """

    def __init__(self, entry: SloleksEntry, pos_to_copy: str = None):
        """
        Manages the creation of a table from SloleksEntry object

        :param entry: (SloleksEntry)
        :param pos_to_copy: (str) Indicates which (default None) part of
            speech to copy to clipboard
        """
        raise NotImplementedError


class Definition:
    def __init__(self, entry: SloleksEntry, test: bool = False):
        self.entry = entry
        self.button_sections = [InflectionSection(entry, test=True)]

        button_stuff = ''
        for section in self.button_sections:
            button_stuff += air_button(section, entry=self.entry)

        self.formatted = airhead_embody(button_stuff, entry=self.entry)

    def __str__(self):
        return str(self.formatted)


class InflectionSection:
    def __init__(self, entry: SloleksEntry, test: bool = False):
        """
        Generates table based on entry part of speech

        :param entry: (SloleksEntry)
        :param test: (bool) determines whether output is plain table or fully implemented
            code with a head, body, styling, etc. for test purposes
        """
        self.entry: SloleksEntry = entry
        pos = self.entry.part_of_speech
        self.test: bool = test
        self.tables = []

        self.made_table: str = ''
        for table_type_value in table_types[pos]:
            t_type = (table_type_value, table_types[pos][table_type_value])
            self.tables.append(self.table_maker(table_type=t_type, vform=table_type_value if pos == "verb" else None))

        '''
        if pos == 'noun':
            t_type = ("declension", table_types["noun"]["declension"])
            self.tables.append(self.table_maker(table_type=t_type))

        if pos == 'verb':
            self.made_table: str = ''
            for verb_form in table_types['verb']:
                t_type = (verb_form, table_types['verb'][verb_form])
                self.tables.append(self.table_maker(table_type=t_type, vform=verb_form))
        '''

        self.section = air_section_info('\n'.join(self.tables), entry=self.entry)

    def __str__(self):
        if self.test:
            return airhead_embody(self.section, entry=self.entry)
        return self.section

    def table_maker(
            self,
            table_type: Tuple[str, Tuple[Tuple, Tuple]],
            test: bool = False,
            **gram_feat
    ) -> str:
        """
        Generates table

        :param table_type: (Tuple[str, Tuple[Tuple, Tuple]]) one key+val pair from grammar_utils.py dict
        :param gram_feat: (kwargs) additional grammarFeature contents needed for grammar_name generation
        ":param test: (bool) True returns fully formatted html
        :return: (Airium) final product as Airium object
        """
        raw_table = str(air_table(entry, table_type=table_type, gram_feat=gram_feat))

        return_val = raw_table if not test else self._table_test(entry=self.entry, *raw_table)

        return str(return_val)

    def _table_test(
            id_val: str = "inflection",
            *to_section: str) -> str:
        tables_section = air_section_info('\n'.join(to_section), entry=self.entry)
        tables_section_button = air_button(tables_section, entry=self.entry, id=id_val)
        test_page = airhead_embody(tables_section_button, entry=self.entry)


def airhead_embody(*html: Union[Airium, str], entry: SloleksEntry) -> str:
    a: Airium = Airium()

    a('<!DOCTYPE html>')
    with (a.html(lang="en")):
        with a.head():
            a.meta(charset="utf-8")
            a.meta(name="viewport", content="width=device-width, initial-scale=1.0")
            a.meta(charset="utf-8")
            a.title(_t=entry.lemma)
            with a.style():
                a(css("modern"))
        with a.body():
            for item in html:
                a(str(item))
            with a.script():
                a(js())
    return str(a)


def air_button(*html: Union[Airium, str], entry: SloleksEntry, id: str = "inflection") -> str:
    a: Airium = Airium()

    with a.div(klass='container'):
        a.button(klass='button', onclick=f"toggleTable('inflection_{entry.lemma}')", _t=f'{id}s')
        with a.div(klass='content hidden', id=f'{id}_{entry.lemma}'):
            for input in html:
                a(str(input))
    return str(a)


def air_section_info(*html: Union[Airium, str], entry: SloleksEntry) -> str:
    a = Airium(base_indent="")
    with a.p(klass='heading'):
        a(f'<b>{entry.part_of_speech}</b>; '
          f'<em>{entry.lemma_grammatical_features['type']}</em>, '
          f'<em>{entry.lemma_grammatical_features['gender']}</em>')
        lg.warning("Assumes entry has 'type' feature.")
        lg.warning("Assumes entry has 'gender' feature. Cancelled")
        for input in html:
            a(str(input))

    return str(a) + footer()


def air_table(entry: SloleksEntry, table_type: Tuple[str, Tuple[Tuple, Tuple]], gram_feat: Dict[str, str]) -> str:
    """
    Takes a number of parameters and generates an unstyled html table

    :param entry: (SloleksEntry)
    :param table_type: (Tuple[Tuple, Tuple]): item from dict defined in grammar_utils.py
    :param gram_feat: (Dict[str,str]) additional grammarFeature contents needed for grammar_name generation
    :return a: (Airium)
    """
    table = Airium()
    ic.disable()
    with table.p(klass="lineabove"):
        with table.b():
            table(table_type[0].title())
        with table.table(klass='inflection'):
            with table.tr():
                table.th()
                for item in table_type[1][0]:
                    table.th(_t=item)
            for row in ic(table_type[1][1]):
                with table.tr():

                    table.th(_t=row)  ####
                    for col in ic(table_type[1][0]):
                        row_feature = ic(return_gram_feat_type(row))
                        col_feature = ic(return_gram_feat_type(col))
                        grammar_name = ic(ordered_grammar_name(
                            v_form=table_type[0] if table_type[0] in gfcat['vform'] else None,
                            case=row if row_feature == "case" else (col if col_feature == "case" else None),
                            person=row if row_feature == "person" else (col if col_feature == "person" else None),
                            number=row if row_feature == "number" else (col if col_feature == "number" else None),
                            gender=row if row_feature == "gender" else (col if col_feature == "gender" else None)
                        ))
                        form: WordForm = entry.forms_dict.get(grammar_name, None)
                        if form is not None:
                            with table.td(klass='pop-up', title=grammar_name):  # @
                                table(format_string(entry, grammar_name))
                                with table.span(klass='pop-up-content'):
                                    table("Pronunciation:")
                                    table.br()
                                    table(ipa(entry.forms_dict[grammar_name]))
    ic.enable()
    return str(table)


def css(aesthetic: str = "modern") -> str:
    """
    Takes css aesthetic and returns relevant style element contents

    :param aesthetic:
    :return: CSS text
    """
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'CSS', f'{aesthetic}.css'))
    with open(path, "r") as file:
        return file.read()


def js(filename: str = "scripts") -> str:
    """
    Fetches JS script file contents

    :return: JS text
    """
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'JS', f'{filename}.js'))
    with open(path, "r") as file:
        return file.read()


def footer():
    return '''
        <p class=lineabove> Inflections not found in the <a 
        href="https://viri.cjvt.si/gigafida/">Gigafida Corpus</a> are 
        <span class=gray>grayed out</span>. 
        They are the correct inflections, but this is a non-exhaustive database of 
        <em>written</em> Slovene. For instance, the locative dual form of Stalin 
        (<em>stalinih</em>) is unsurprisingly absent -- but fear not, as the locative <em>plural</em> (also <em>stalinih</em>) 
        has one occurrence in the corpus.</p>
    '''


if __name__ == "__main__":
    entry = sample_entry_obj("verb")
    infsec = Definition(entry, test=True)
    pyperclip.copy(str(infsec))
