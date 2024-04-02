import xml.etree.ElementTree as ET
from typing import List, Dict, Union
import tkinter as tk
from tkhtmlview import HTMLLabel
import os
import pyperclip


class Entry:
    def __init__(self, lemma: str, part_of_speech: str, lemma_grammatical_features: Dict[str, str], xml_file: str, word_forms: List['WordForm']):
        self.lemma: str = lemma
        self.part_of_speech: str = part_of_speech
        self.xml_file: str = xml_file
        self.gender: Union[str, None] = lemma_grammatical_features.get("gender")
        self.type: Union[str, None] = lemma_grammatical_features.get("type")
        self.aspect: Union[str, None] = lemma_grammatical_features.get("aspect")
        self.word_forms: List['WordForm'] = word_forms
        self.lemma_base_str = self.common_prefix([form.form_representation for form in self.word_forms])

        #add formatted element to each word form object
        for form in word_forms:
            form.formatted = self.bold_except(form.form_representation, self.lemma_base_str)
            form.formatted = self.gray_unused(form)


    """def add_word_form(self, word_form: 'WordForm') -> None:
        self.word_forms.append(word_form)"""

    def common_prefix(self, strings) -> str:
        if not strings:
            return ""
        return os.path.commonprefix(strings)

    def bold_except(self, word, not_bold) -> str:
        to_bold = word.replace(not_bold, "")
        return word.replace(to_bold, f"<b>{to_bold}</b>")

    def gray_unused(self, form: 'WordForm') -> str:
        print("Running")
        if form.frequency == 0:
            print(form.formatted)
            return f"<span class=gray>{form.formatted}</span>"
        else:
            return form.formatted

    def generate_table(self) -> Union[str, None]:
        function_string: str = f"self.{self.part_of_speech}_table()"
        if hasattr(self, f"{self.part_of_speech}_table"):
            table_html = eval(function_string)
            return self.wrap_table(table_html)
        else:
            return None

    def noun_table(self) -> Union[str, None]:
        nom_sg = nom_dl = nom_pl = gen_sg = gen_dl = gen_pl = dat_sg = dat_dl = dat_pl = acc_sg = acc_dl = acc_pl = loc_sg = loc_dl = loc_pl = ins_sg = ins_dl = ins_pl = "Undefined"

        for word_form in self.word_forms:
            if "case" in word_form.grammatical_features and "number" in word_form.grammatical_features:
                case = word_form.grammatical_features["case"]
                number = word_form.grammatical_features["number"]
                if case == "nominative" and number == "singular":
                    nom_sg = word_form.form_representation
                elif case == "nominative" and number == "dual":
                    nom_dl = word_form.form_representation
                elif case == "nominative" and number == "plural":
                    nom_pl = word_form.form_representation
                elif case == "genitive" and number == "singular":
                    gen_sg = word_form.form_representation
                elif case == "genitive" and number == "dual":
                    gen_dl = word_form.form_representation
                elif case == "genitive" and number == "plural":
                    gen_pl = word_form.form_representation
                elif case == "dative" and number == "singular":
                    dat_sg = word_form.form_representation
                elif case == "dative" and number == "dual":
                    dat_dl = word_form.form_representation
                elif case == "dative" and number == "plural":
                    dat_pl = word_form.form_representation
                elif case == "accusative" and number == "singular":
                    acc_sg = word_form.form_representation
                elif case == "accusative" and number == "dual":
                    acc_dl = word_form.form_representation
                elif case == "accusative" and number == "plural":
                    acc_pl = word_form.form_representation
                elif case == "locative" and number == "singular":
                    loc_sg = word_form.form_representation
                elif case == "locative" and number == "dual":
                    loc_dl = word_form.form_representation
                elif case == "locative" and number == "plural":
                    loc_pl = word_form.form_representation
                elif case == "instrumental" and number == "singular":
                    ins_sg = word_form.form_representation
                elif case == "instrumental" and number == "dual":
                    ins_dl = word_form.form_representation
                elif case == "instrumental" and number == "plural":
                    ins_pl = word_form.form_representation

        table_html: str = """
        <div class="content hidden" id="declension_{lemma}">
            <p class="heading"><b>{lemma}</b> is a <b>{gender}</b> declension</p>
            <table class="inflection">
                <tr>
                    <th></th>
                    <th>singular</th>
                    <th>dual</th>
                    <th>plural</th>
                </tr>
                <tr>
                    <th>nom.</th>
                    <td title="nom sg">{nom_sg}</td>
                    <td title="nom dl">{nom_dl}</td>
                    <td title="nom pl">{nom_pl}</td>
                </tr>
                <tr>
                    <th>gen.</th>
                    <td title="gen sg">{gen_sg}</td>
                    <td title="gen dl">{gen_dl}</td>
                    <td title="gen pl">{gen_pl}</td>
                </tr>
                <tr>
                    <th>dat.</th>
                    <td title="dat sg">{dat_sg}</td>
                    <td title="dat dl">{dat_dl}</td>
                    <td title="dat pl">{dat_pl}</td>
                </tr>
                <tr>
                    <th>acc.</th>
                    <td title="acc sg">{acc_sg}</td>
                    <td title="acc dl">{acc_dl}</td>
                    <td title="acc pl">{acc_pl}</td>
                </tr>
                <tr>
                    <th>loc.</th>
                    <td title="loc sg">{loc_sg}</td>
                    <td title="loc dl">{loc_dl}</td>
                    <td title="loc pl">{loc_pl}</td>
                </tr>
                <tr>
                    <th>ins.</th>
                    <td title="ins sg">{ins_sg}</td>
                    <td title="ins dl">{ins_dl}</td>
                    <td title="ins pl">{ins_pl}</td>
                </tr>
            </table>
        </div>
        """.format(
            lemma=self.lemma,
            gender=self.gender,
            nom_sg=nom_sg,
            nom_dl=nom_dl,
            nom_pl=nom_pl,
            gen_sg=gen_sg,
            gen_dl=gen_dl,
            gen_pl=gen_pl,
            dat_sg=dat_sg,
            dat_dl=dat_dl,
            dat_pl=dat_pl,
            acc_sg=acc_sg,
            acc_dl=acc_dl,
            acc_pl=acc_pl,
            loc_sg=loc_sg,
            loc_dl=loc_dl,
            loc_pl=loc_pl,
            ins_sg=ins_sg,
            ins_dl=ins_dl,
            ins_pl=ins_pl
        )

        return table_html

    def verb_table(self) -> Union[str, None]:
        form_representation_strings: list(str) = []
        for word_form in self.word_forms:
            form_representation_strings.append(word_form.formatted)
            vform = getattr(word_form, "vform", None)
            number = getattr(word_form, "number", None)
            person = getattr(word_form, "person", None)
            gender = getattr(word_form, "gender", None)

            if vform == "infinitive":
                self.infinitive = word_form.formatted
            elif vform == "supine":
                self.supine = word_form.formatted
            else:
                # Since participles dont have 1,2,or3rd person but do have gender
                if gender and not person:
                    middle_item = gender
                elif person and not gender:
                    middle_item = person
                else:
                    print("\n\nERROR in verb_table!")
                    print("word_form:", word_form.formatted)
                    print("gender:", gender)
                    print("person:", person, end="\n\n")

                # Constructing variable name dynamically
                variable_name = f"{vform}_{middle_item}_{number}"

                # Assigning value to the dynamically constructed variable
                setattr(self, variable_name, word_form.formatted)

        table_html = f'''
                <div class="content hidden" id=conjugation_{self.lemma}>
                    <p class=heading> <em>verb</em>; <em>{self.aspect}</em>, <em>{self.type}</em>

                        <p class=lineabove> <b>Present Tense</b>
                            <table class=inflection>
                                <tr>
                                    <th></th>
                                    <th>singular</th>
                                    <th>dual</th>
                                    <th>plural</th>
                                </tr>
                                <tr>
                                    <th>1st person</th>
                                    <td title="present first singular">{self.present_first_singular}</td>
                                    <td title="present first dual">{self.present_first_dual}</td>
                                    <td title="present first plural">{self.present_first_plural}</td>
                                </tr>
                                <tr>
                                    <th>2nd person</th>
                                    <td title="present second singular">{self.present_second_singular}</td>
                                    <td title="present second dual">{self.present_second_dual}</td>
                                    <td title="present second plural">{self.present_second_plural}</td>
                                </tr>
                                <tr>
                                    <th>3rd person</th>
                                    <td title="present third singular">{self.present_third_singular}</td>
                                    <td title="present third dual">{self.present_third_dual}</td>
                                    <td title="present third plural">{self.present_third_plural}</td>
                                </tr>
                            </table>
                        </p>

                        <p class=lineabove> <b>Imperative</b>
                            <table class=inflection>
                                <tr>
                                    <th></th>
                                    <th>singular</th>
                                    <th>dual</th>
                                    <th>plural</th>
                                </tr>
                                <tr>
                                    <th>1st person</th>
                                    <td title="imperative first singular">{getattr(self, "imperative_first_singular", "")}</td>
                                    <td title="imperative first dual">{self.imperative_first_dual}</td>
                                    <td title="imperative first plural">{self.imperative_first_plural}</td>
                                </tr>
                                <tr>
                                    <th>2nd person</th>
                                    <td title="imperative second singular">{self.imperative_second_singular}</td>
                                    <td title="imperative second dual">{self.imperative_second_dual}</td>
                                    <td title="imperative second plural">{self.imperative_second_plural}</td>
                                </tr>
                            </table>
                        </p>

                        <p class=lineabove> <b>Participle</b>
                            <table class=inflection>
                                <tr>
                                    <th></th>
                                    <th>singular</th>
                                    <th>dual</th>
                                    <th>plural</th>
                                </tr>
                                <tr>
                                    <th>masculine</th>
                                    <td title="participle singular masculine">{self.participle_masculine_singular}</td>
                                    <td title="participle dual masculine">{self.participle_masculine_dual}</td>
                                    <td title="participle plural masculine">{self.participle_masculine_plural}</td>
                                </tr>
                                <tr>
                                    <th>feminine</th>
                                    <td title="participle singular feminine">{self.participle_feminine_singular}</td>
                                    <td title="participle dual feminine">{self.participle_feminine_dual}</td>
                                    <td title="participle plural feminine">{self.participle_feminine_plural}</td>
                                </tr>
                                <tr>
                                    <th>neuter</th>
                                    <td title="participle singular neuter">{self.participle_neuter_singular}</td>
                                    <td title="participle dual neuter">{self.participle_neuter_dual}</td>
                                    <td title="participle plural neuter">{self.participle_neuter_plural}</td>
                                </tr>
                            </table>
                        </p>

                        <p class=lineabove> <b>Infinitive and Supine</b>
                            <table class=inflection>
                                <tr>
                                    <th>infinitive</th>
                                    <td title="infinitive">{self.infinitive}</td>
                                </tr>
                                <tr>
                                    <th>supine</th>
                                    <td title="supine">{self.supine}</td>
                                </tr>
                            </table>
                        </p>

                    </p>


                    <p class=lineabove> Inflections not found in the <a 
                        href="https://viri.cjvt.si/gigafida/">Gigafida Corpus</a> are 
                        <span class=gray>grayed out</span>. 
                        They are the correct inflections, but this is a non-exhaustive database of 
                        <em>written</em> Slovene. For instance, the locative dual form of Stalin 
                        (<em>stalinih</em>) is unsurprisingly absent -- though oddly enough, the locative plural (also <em>stalinih</em>) 
                        has one occurrence in the corpus.
                    </p>
                </div>
                '''
        save_to_clipboard(self.wrap_table(table_html))
        return table_html

    def adjective_table(self):
        return None

    def adverb_table(self):
        return None

    def pronoun_table(self):
        return None

    def numeral_table(self):
        return None

    def preposition_table(self):
        return None

    def conjunction_table(self):
        return None

    def particle_table(self):
        return None

    def interjection_table(self):
        return None

    def abbreviation_table(self):
        return None

    def residual_table(self):
        return None

    def wrap_table(self, string: str) -> Union[str, None]:
        if string is not None:
            wrapped = \
                f'''<!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>samooklicati</title>
                <style>
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
                </style>
                </head>
                <body>
                
                <div class="container">
                    <button class="button" onclick="toggleTable('conjugation_{self.lemma}')">Inflections</button>
                    {string}
                </div>
                <script>
                function toggleTable(id) {{
                    var element = document.getElementById(id);
                    element.classList.toggle("hidden");
                }}
                </script>
        
                </body>
                </html>
            '''
            return wrapped
        else:
            return None


class WordForm:
    def __init__(self, form_representation: str, morphosyntactic_tags: str, grammatical_features: dict,
                 pronunciation: Union[str, None], accentuation: Union[str, None], frequency: Union[int, None]):
        self.form_representation: str = form_representation
        self.morphosyntactic_tags: str = morphosyntactic_tags
        self.grammatical_features: dict = grammatical_features
        self.accentuation: Union[str, None] = accentuation
        self.frequency: Union[str, None] = frequency
        self.pronunciation: Union[str, None] = pronunciation
        self.vform: Union[str, None] = grammatical_features.get("vform")
        self.number: Union[str, None] = grammatical_features.get("number")
        self.gender: Union[str, None] = grammatical_features.get("gender")
        self.person: Union[str, None] = grammatical_features.get("person")
        self.formatted: Union[str, None] = None



from typing import List, Dict
import xml.etree.ElementTree as ET


def parse_xml_file(xml_file: str) -> List[Entry]:
    entries: List[Entry] = []
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for entry_element in root.findall('.//entry'):
        lemma: str = entry_element.find('.//lemma').text
        part_of_speech: str = entry_element.find('.//category').text.lower()
        lemma_grammatical_features: Dict[str, str] = {feature.get('name'): feature.text for feature in
                                                      entry_element.findall('.//grammarFeature')}
        word_forms = []
        for word_form_element in entry_element.findall('.//wordForm'):
            form_representation: str = word_form_element.find('.//form').text
            morphosyntactic_tags: str = word_form_element.find('.//msd').text
            grammatical_features: Dict[str, str] = {feature.get('name'): feature.text for feature in
                                                    word_form_element.findall('.//grammarFeature')}
            pronunciation_element = word_form_element.find('.//pronunciation/form[@script="IPA"]')
            pronunciation: str = pronunciation_element.text if pronunciation_element is not None else None

            # Extract accentuation and frequency
            accentuation_element = word_form_element.find('.//accentuation/form')
            accentuation: str = accentuation_element.text if accentuation_element is not None else None
            frequency_element = word_form_element.find('.//measureList/measure[@type="frequency"]')
            frequency: Union[int, None] = int(frequency_element.text) if frequency_element is not None else None

            word_form = WordForm(form_representation, morphosyntactic_tags, grammatical_features, pronunciation,
                                 accentuation, frequency)
            word_forms.append(word_form)
        entry = Entry(lemma, part_of_speech, lemma_grammatical_features, xml_file, word_forms)
        entries.append(entry)
    return entries


def get_one_of_each() -> List[Entry]:
    directory: str = "C:\\Users\\sangha\\Documents\\Danny's\\slodict\\Sloleks.3.0\\"
    xml_file: str = "C:\\Users\\sangha\\Documents\\Danny's\\slodict\\sloleks_3.0_sample.xml"
    return parse_xml_file(xml_file)


def display_html(html_content):
    root = tk.Tk()
    root.title("HTML Display")
    root.geometry("800x600")

    html_widget = tkhtml.HtmlFrame(root, horizontal_scrollbar="auto", vertical_scrollbar="auto")
    html_widget.set_content(html_content)
    html_widget.pack(fill="both", expand=True)

    root.mainloop()

def display_html(content):
    root = tk.Tk()
    html_label = HTMLLabel(root, html=content)
    html_label.pack(fill="both", expand=True)
    html_label.fit_height()
    root.mainloop()

def save_to_clipboard(text):
    pyperclip.copy(text)

def main():
    entries = get_one_of_each()

    for entry in entries:
        html_content = entry.generate_table()
        if html_content is not None:
            print(html_content)




if __name__ == "__main__":
    main()
