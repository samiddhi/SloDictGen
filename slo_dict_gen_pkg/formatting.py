from common.imports import *
from slo_dict_gen_pkg.entry_parser import SloleksEntry, WordForm, XMLParser, sample_entry_obj
from slo_dict_gen_pkg.grammar_utilities import ordered_grammar_name, return_gram_feat_type, number, case, gender, vform, person

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


def noun_table(entry: SloleksEntry, pos_to_copy: str) -> str:
    format_string(entry, "nominative_singular")
    table: str = f'''
        <div class="content hidden" id="inflection_{entry.lemma}">
            <p class="heading"> <b><em>noun</em></b>; <em>{entry.lemma_grammatical_features["type"]}</em>, 
            <em>{entry.lemma_grammatical_features["gender"]}</em>
            <table class="inflection">
                <tr>
                    <th></th>
                    <th>singular</th>
                    <th>dual</th>
                    <th>plural</th>
                </tr>
                <tr>
                    <th>nom.</th>
                    <td title="nom sg" class="pop-up">{format_string(entry, "nominative_singular")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["nominative_singular"])}</span></td>
                    <td title="nom dl" class="pop-up">{format_string(entry, "nominative_dual")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["nominative_dual"])}</span></td>
                    <td title="nom pl" class="pop-up">{format_string(entry, "nominative_plural")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["nominative_plural"])}</span></td>
                </tr>
                <tr>
                    <th>gen.</th>
                    <td title="gen sg" class="pop-up">{format_string(entry, "genitive_singular")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["genitive_singular"])}</span></td>
                    <td title="gen dl" class="pop-up">{format_string(entry, "genitive_dual")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["genitive_dual"])}</span></td>
                    <td title="gen pl" class="pop-up">{format_string(entry, "genitive_plural")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["genitive_plural"])}</span></td>
                </tr>
                <tr>
                    <th>dat.</th>
                    <td title="dat sg" class="pop-up">{format_string(entry, "dative_singular")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["dative_singular"])}</span></td>
                    <td title="dat dl" class="pop-up">{format_string(entry, "dative_dual")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["dative_dual"])}</span></td>
                    <td title="dat pl" class="pop-up">{format_string(entry, "dative_plural")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["dative_plural"])}</span></td>
                </tr>
                <tr>
                    <th>acc.</th>
                    <td title="acc sg" class="pop-up">{format_string(entry, "accusative_singular")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["accusative_singular"])}</span></td>
                    <td title="acc dl" class="pop-up">{format_string(entry, "accusative_dual")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["accusative_dual"])}</span></td>
                    <td title="acc pl" class="pop-up">{format_string(entry, "accusative_plural")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["accusative_plural"])}</span></td>
                </tr>
                <tr>
                    <th>loc.</th>
                    <td title="loc sg" class="pop-up">{format_string(entry, "locative_singular")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["locative_singular"])}</span></td>
                    <td title="loc dl" class="pop-up">{format_string(entry, "locative_dual")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["locative_dual"])}</span></td>
                    <td title="loc pl" class="pop-up">{format_string(entry, "locative_plural")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["locative_plural"])}</span></td>
                </tr>
                <tr>
                    <th>ins.</th>
                    <td title="ins sg" class="pop-up">{format_string(entry, "instrumental_singular")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["instrumental_singular"])}</span></td>
                    <td title="ins dl" class="pop-up">{format_string(entry, "instrumental_dual")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["instrumental_dual"])}</span></td>
                    <td title="ins pl" class="pop-up">{format_string(entry, "instrumental_plural")}<span class="pop-up-content">Pronunciation:{ipa(entry.forms_dict["instrumental_plural"])}</span></td>
                </tr>
            </table>

            {gigafida_footer}
        </div>
        '''
    table = wrap(entry, table)

    if pos_to_copy == "noun":
        pyperclip.copy(table)
    return table


def wrap(entry: SloleksEntry, table: str):
    style = f'''
        body {{
            font-family: Verdana, sans-serif;
            margin: 0;
            padding: 0;
        }}
    
        .container {{
            max-width: 800px;
            margin: 20px auto;
            padding: 10px
        }}
    
        .content {{
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-bottom: 20px;
            padding: 20px;
            overflow-x: auto;
        }}
    
        .heading {{
            background-color: #f2f2f2;
            padding: 10px 20px;
            margin: 0;
        }}
    
        .inflection {{
            width: 100%;
            border-collapse: collapse;
            padding: 0px
        }}
    
        .inflection th, .inflection td {{
            border: 1px solid #ccc;
            padding: 8px;
            text-align: center;
        }}
    
        .inflection th {{
            background-color: #f2f2f2;
        }}
    
        .hidden {{
            display: none;
        }}
    
        .button {{
            font-family: Verdana, sans-serif;
            background-color: #fa7d7d;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
        }}
    
        .button:hover {{
            background-color: #7ac3ff;
        }}
    
        .lineabove {{
            border-top: 1px solid #ccc; /* Added line above */
            margin-top: 10px; /* Added margin top */
            margin-bottom: 6px;
            padding-top: 10px
        }}
    
        .gray {{
            font-family: Verdana, sans-serif;
            color:#838383
        }}
    
        .pop-up {{
            position: relative;
            cursor: pointer;
        }}
    
        .pop-up .pop-up-content {{
            visibility: hidden;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 8px;
            position: absolute;
            z-index: 1;
            top: -30px;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0;
            transition: opacity 0.3s;
            white-space: nowrap; /* Prevent text wrapping */
            width: max-content; /* Adjust width to fit content dynamically */
        }}
    
        .pop-up:hover .pop-up-content {{
            visibility: visible;
            opacity: 1;
        }}
    '''

    head = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{entry.lemma}</title>
            <style>
                {style}
            </style>
            </head>
    '''

    return f'''
                {head}

                <body>
                    <div class="container">
                        <button class="button" onclick="toggleTable('inflection_{entry.lemma}')">Inflections</button>
                        {table}
                    </div>

                    <script>
                        function toggleTable(id) {{
                            var element = document.getElementById(id);
                            element.classList.toggle("hidden");
                        }}
                    </script>
                </body>
                </html>
            '''.strip()


def gigafida_footer():
    return '''
        <p class=lineabove> Inflections not found in the <a 
        href="https://viri.cjvt.si/gigafida/">Gigafida Corpus</a> are 
        <span class=gray>grayed out</span>. 
        They are the correct inflections, but this is a non-exhaustive database of 
        <em>written</em> Slovene. For instance, the locative dual form of Stalin 
        (<em>stalinih</em>) is unsurprisingly absent -- but fear not, as the locative <em>plural</em> (also <em>stalinih</em>) 
        has one occurrence in the corpus.</p>
    '''


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


def airhead_embody(*html: Union[Airium, str], entry: SloleksEntry) -> Airium:
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
    return a


def airbut(*html: Union[Airium, str], entry: SloleksEntry, id: str = "inflection") -> Airium:
    a: Airium = Airium()

    with a.div(klass='container'):
        a.button(klass='button', onclick=f"toggleTable('inflection_{entry.lemma}')", _t='Inflections')
        with a.div(klass='content hidden', id=f'{id}_{entry.lemma}'):
            for input in html:
                a(str(input))
    return a


def airheading(*html: Union[Airium, str], entry: SloleksEntry, id: str = "inflection") -> Airium:
    a = Airium()
    with a.p(klass='heading'):
        with a.b():
            a.em(_t=entry.part_of_speech)
        a(';')
        a.em(_t=entry.lemma_grammatical_features['type'])
        lg.warning("Assumes entry has 'type' feature.")
        a(',')
        a.em(_t=entry.lemma_grammatical_features['gender'])
        lg.warning("Assumes entry has 'gender' feature. Cancelled")
        for input in html:
            a(str(input))

    return a


def airtable(entry: SloleksEntry, top_labels: List[str], left_labels: List[str]) -> Airium:
    """
    Takes a number of parameters and generates an unstyled html table

    :param entry: (SloleksEntry)
    :param top_labels: (List[str]) Labels at the top of the table
    :param left_labels: (List[str]) Labels on the left side of the table
    :return a: (Airium)
    """
    table = Airium()

    with table.table(klass='inflection'):
        with table.tr():
            table.th()
            for item in top_labels:
                table.th(_t=item)
        for row in ic(left_labels):
            with table.tr():
                table.th(_t=f'{row[:3]}.')  ####
                for col in top_labels:
                    ic.disable()
                    row_feature = ic(return_gram_feat_type(row))
                    col_feature = ic(return_gram_feat_type(col))
                    grammar_name = ic(ordered_grammar_name(
                        v_form=row if row_feature == "vform" else (col if col_feature == "vform" else None),
                        case=row if row_feature == "case" else (col if col_feature == "case" else None),
                        person=row if row_feature == "person" else (col if col_feature == "person" else None),
                        number=row if row_feature == "number" else (col if col_feature == "number" else None),
                        gender=row if row_feature == "gender" else (col if col_feature == "gender" else None)
                    ))
                    ic.enable()
                    form: WordForm = entry.forms_dict[grammar_name]

                    with table.td(klass='pop-up', title=grammar_name):  # @
                        table(format_string(entry, grammar_name))
                        with table.span(klass='pop-up-content'):
                            table("Pronunciation:")
                            table.br()
                            table(ipa(entry.forms_dict[grammar_name]))

    return table


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


if __name__ == "__main__":
    entry = sample_entry_obj("noun")
    table_unprocessed = airtable(entry, number, case)
    pyperclip.copy(str(
        airhead_embody(
            airbut(
                airheading(
                    table_unprocessed,
                    entry=entry),
                entry=entry,
                id="inflection"),
            entry=entry
        )
    ))
