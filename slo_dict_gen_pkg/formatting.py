from common.imports import *
from slo_dict_gen_pkg.entry_parser import SloleksEntry, WordForm, Representation, XMLParser
from tests.parsing_utils import sample_entry_obj
from slo_dict_gen_pkg.grammar_utils import ordered_grammar_name, return_gram_feat_type, gfcat, table_types

from airium import Airium
from itertools import product
import pyperclip
import os
import sys

# Add the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

failure: bool = False

class Definition:
    def __init__(self, entry: SloleksEntry, test: bool = False):
        self.entry = entry
        self.button_sections = [InflectionSection(entry)]

        button_stuff = ''
        for section in self.button_sections:
            button_stuff += HTMLib.air_button(str(section), entry=self.entry)

        self.formatted = HTMLib.airhead_embody(button_stuff, entry=self.entry)

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
        self.test: bool = test
        tables = Tables(entry)
        raw_tables = str(tables)
        wordforms_displayed = int(tables)
        self.section = raw_tables

        if wordforms_displayed != len(entry.all_reps):
            lg.critical(f"{wordforms_displayed}/{len(entry.all_reps)} forms displayed for {entry.lemma}")
        print(f"{wordforms_displayed}/{len(entry.all_reps)} forms displayed for {entry.lemma}")

    def __str__(self):
        if self.test:
            return airhead_embody(self.section, entry=self.entry)
        return self.section


class Tables:
    def __init__(self, entry: SloleksEntry):
        self.tables: str = ''
        self.representations_displayed: int = 0

        part_of_speech: str = entry.part_of_speech
        table_type_index: List[Tuple[str, List[List[str]]]] = list(table_types[part_of_speech].items())

        for table_type in table_type_index:
            table_type_matrix: List[List] = self.make_table_type_matrix(table_type)
            reps_matrix: List[List[List[Representation]]] = self.make_representations_matrix(
                entry,
                table_type_matrix
            )
            raw_table, representations_added = self.table_from_matrix(entry, reps_matrix)
            if representations_added > 0:
                self.tables += raw_table
                self.representations_displayed += representations_added

    def __str__(self):
        return str(self.tables)

    def __int__(self):
        return int(self.representations_displayed)

    @staticmethod
    def make_table_type_matrix(table_type: tuple[str, list[list[str]]]) -> List[List]:
        table_name: str = table_type[0]
        table_col_labels: List[str] = table_type[1][0]
        table_row_labels: List[str] = table_type[1][1]

        table_type_matrix: List[List[str]] = [[table_type[0]] * (len(table_col_labels) + 1) for _ in range(len(table_row_labels) + 1)]

        table_type_matrix[0][1:] = table_col_labels
        for i, label in enumerate(table_row_labels):
            table_type_matrix[i + 1][0] = label

        # Fill in the cell values based on row and column labels
        for i, row in enumerate(table_row_labels):
            for j, col in enumerate(table_col_labels):
                row_feature = return_gram_feat_type(row)
                col_feature = return_gram_feat_type(col)

                # Handle exceptions for when the table type name is needed
                v_form: str = table_type[0] if table_type[0] in gfcat['vform'] else row if row in {"infinitive", "supine"} else None
                case: str = row if row_feature == "case" else (col if col_feature == "case" else None)
                person: str = row if row_feature == "person" else (col if col_feature == "person" else None)
                number: str = row if row_feature == "number" else (col if col_feature == "number" else None)
                gender: str = table_type[0] if table_type[0] in gfcat['gender'] + ['agender'] else (row if row_feature == "gender" else (col if col_feature == "gender" else None))
                degree: str = row if row_feature == "degree" else None
                clitic: str = row if row_feature == "clitic" else None

                grammar_names: List(str) = ordered_grammar_name(
                    v_form=v_form,
                    case=case,
                    person=person,
                    number=number,
                    gender=gender,
                    degree=degree,
                    clitic=clitic,
                    return_type="list"
                )

                table_type_matrix[i + 1][j + 1] = [grammar_names]
        return table_type_matrix

    @staticmethod
    def make_representations_matrix(entry: SloleksEntry, table_type_matrix: List[List]):
        table_name = table_type_matrix[0][0]
        row_labels = [row[0] for row in table_type_matrix]
        col_labels = table_type_matrix[0][1:]
        matrix_core = [row[1:] for row in table_type_matrix[1:]]

        for cell in [cell for row in matrix_core for cell in row]:
            cell_grammar_names = cell.pop(0)
            for rep_grammar_names in entry.reps_dict:
                if all(grammar_feature in rep_grammar_names for grammar_feature in cell_grammar_names):
                    cell.extend(entry.reps_dict.get(rep_grammar_names, []))

        row_labels[0] = table_name
        matrix_restored = [col_labels] + matrix_core
        for row, row_label in zip(matrix_restored, row_labels):
            row.insert(0, row_label)

        empty_rows = [i for i, row in enumerate(matrix_restored[1:]) if all(cell == [] for cell in row[1:])]
        empty_columns = [j for j in range(len(matrix_restored[0])) if all(matrix_restored[i][j] == [] for i in range(1, len(matrix_restored)))]
        for i in reversed(empty_rows):
            del matrix_restored[i + 1]
        for j in reversed(empty_columns):
            for row in matrix_restored:
                del row[j]

        return matrix_restored

    def table_from_matrix(self, entry: SloleksEntry, representation_matrix: List):
        row_labels = [row[0] for row in representation_matrix[1:]]
        col_labels = representation_matrix[0][1:]
        matrix_core = [row[1:] for row in representation_matrix[1:]]
        added = 0
        table = Airium()
        with table.p(klass="lineabove"):
            with table.b():
                header: str = representation_matrix[0][0]
                table(header.title() if header != 'agender' else 'General')
            with table.table(klass='inflection'):
                # Prevent header in table for non-inflected words
                if col_labels and col_labels[0] != 'form':
                    with table.tr():
                        table.th()
                        for col_label in col_labels:
                            table.th(_t=col_label)
                for row_label, row in zip(row_labels, matrix_core):
                    with table.tr():
                        if row_label != 'form':
                            table.th(_t=row_label)
                        for cell in row:
                            with table.td():
                                for index, representation in enumerate(cell):
                                    with table.span(klass='pop-up'):
                                        representation_formatted = self.format_forms_for_table(entry, representation)
                                        table(representation_formatted)
                                        if representation_formatted != '':
                                            added += 1
                                        # Add pronunciation popup for each word
                                        with table.span(klass='pop-up-content'):
                                            table("Pronunciation:")
                                            table.br()
                                            table(representation.pronunciation_dict.get("IPA", None))
        return str(table), added

    def format_forms_for_table(self, entry: SloleksEntry, to_format_rep_obj: Representation):
        """
        Takes given word forms by reference to a shared grammar name
        :param rep_index:
        :param entry:
        :param grammar_name:
        :return:
        """

        # Removing negative forms from consideration because they do not share a prefix with the
        # other wordForms. Otherwise, this breaks the bolded inflection suffixes for the entire entry
        non_negative_forms = []
        for rep in entry.all_reps:
            non_negative_forms = non_negative_forms + [rep.form_representation] if "negative" not in rep.norms else non_negative_forms

        shared_prefix = self.common_prefix(non_negative_forms)
        bolded = self.bold_except(to_format_rep_obj.form_representation, shared_prefix)
        grayed = self.gray_unused(to_format_rep_obj.frequency, bolded)

        formatted = grayed
        if to_format_rep_obj.norms:
            formatted += '<br>'
        for norm in to_format_rep_obj.norms:
            if norm in ["masculine", "feminine", "neuter", "agender"]:
                color = {
                    "masculine": "blue",
                    "feminine": "red",
                    "neuter": "yellow"
                }.get(norm, None)
                formatted = f'\n<span class={color}-underline>{formatted}</span>' if norm != "agender" else formatted
            else:
                formatted += f'\n<span class=gray-small-ital>{norm}</span>'

        return formatted

    @staticmethod
    def common_prefix(strings) -> str:
        if not strings:
            return ""
        return str(os.path.commonprefix(strings))

    @staticmethod
    def bold_except(word: str, infix: str):
        if infix in word and infix != '':
            split = word.split(infix)
            sections = [split.pop(0), infix.join(split)]
            front = f'<b>{sections[0]}</b>' if sections[0] != '' else ''
            end = f'<b>{sections[1]}</b>' if sections[1] != '' else ''
            output = front + infix + end
            return output
        else:
            return word

    @staticmethod
    def gray_unused(frequency: int, to_gray: str) -> str:
        if frequency == 0:
            return f"<span class=gray>{to_gray}</span>"
        else:
            return to_gray


class HTMLib:
    @staticmethod
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
                    a(HTMLib.css("modern"))
            with a.body():
                for item in html:
                    a(str(item))
                with a.script():
                    a(HTMLib.js())
        return str(a)

    @staticmethod
    def air_button(*html: Union[Airium, str], entry: SloleksEntry, id: str = "inflection") -> str:
        a: Airium = Airium()

        with a.div(klass='container'):
            a.button(klass='button', onclick=f"toggleTable('inflection_{entry.lemma}')", _t=f'{id}s')
            with a.div(klass='content', id=f'{id}_{entry.lemma}'):
                lg.warning("after debugging, must reset klass to 'content hidden'")
                for input in html:
                    a(str(input))
        return str(a)

    @staticmethod
    def air_section_info(*html: Union[Airium, str], entry: SloleksEntry) -> str:
        a = Airium(base_indent="")
        with a.p(klass='heading'):
            a(f'<b>{entry.part_of_speech}-{len(entry.forms_dict)}</b>; ')
            feature_string = ''
            for feature_type, feature in entry.lemma_grammatical_features.items():
                a(f'<em>{feature_type}: {feature}</em>,')
            a(feature_string[:-1])
            for input in html:
                a(str(input))

        return str(a) + footer()

    @staticmethod
    def css(aesthetic: str = "modern") -> str:
        """
        Takes css aesthetic and returns relevant style element contents

        :param aesthetic:
        :return: CSS text
        """
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'CSS', f'{aesthetic}.css'))
        with open(path, "r") as file:
            return file.read()

    @staticmethod
    def js(filename: str = "scripts") -> str:
        """
        Fetches JS script file contents

        :return: JS text
        """
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'JS', f'{filename}.js'))
        with open(path, "r") as file:
            return file.read()

    @staticmethod
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
    def criterion(obj: SloleksEntry, specific: str, verified: List[str]):
        """
        Delete when done.

        Allows you to get new sample objects until the one you get is either a specific entry,
        or any random one that has not already been verified.

        :param verified:
        :param obj:
        :param specific:
        :return:
        """
        if specific == "":
            return True if obj.lemma in verified else False
        else:
            return True if obj.lemma != specific else False


    pos = ("pronoun")

    # Issues: se (pron)

    sample_entry = sample_entry_obj(pos)
    while criterion(sample_entry,
                    'on',
                    []
                    ):
        sample_entry = sample_entry_obj(pos)
    infsec = Definition(sample_entry, test=True)
    pyperclip.copy(str(infsec))
