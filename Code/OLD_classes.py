from typing import List, Dict, Union
import pyperclip
from formatting import common_prefix, bold_except, gray_unused

COPY = "verb"


class Entry:
    def __init__(
            self,
            lemma: str,
            part_of_speech: str,
            lemma_grammatical_features: Dict[str, str],
            xml_file: str,
            grammarname_forms_dict: Dict[str, 'WordForm'],
            table_to_copy: str = None
    ):
        self.lemma: str = lemma
        self.part_of_speech: str = part_of_speech
        self.xml_file: str = xml_file
        self.gender: Union[str, None] = lemma_grammatical_features.get(
            "gender")
        self.type: Union[str, None] = lemma_grammatical_features.get("type")
        self.aspect: Union[str, None] = lemma_grammatical_features.get(
            "aspect")

        self.grammarname_form_dict: Dict[str, 'WordForm'] = (
            grammarname_forms_dict)

        self.lemma_base_str = common_prefix([form.form_representation for
                                             form in
                                             self.grammarname_form_dict.values()])

        self.add_formatted_to_word_forms()

        # Dealing with word form objects
        """I THINK DEPRICATED???"""
        ##self.formatted_forms_dict: Dict[str, str] = (
        ##    self.compile_formatted_forms_dict())

        self.pronunciation_index_dict: dict[str, list[dict[str, str]]] = (
            self.compile_pron_index_dict())

        self.initialize_formatters()
        self.table_to_copy = table_to_copy

        self.table = self.generate_table(self.table_to_copy)

    # To Migrate
    def initialize_formatters(self):

        css = f'''body {{
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

        self.fida_footer = '''
            <p class=lineabove> Inflections not found in the <a 
            href="https://viri.cjvt.si/gigafida/">Gigafida Corpus</a> are 
            <span class=gray>grayed out</span>. 
            They are the correct inflections, but this is a non-exhaustive database of 
            <em>written</em> Slovene. For instance, the locative dual form of Stalin 
            (<em>stalinih</em>) is unsurprisingly absent -- but fear not, as the locative <em>plural</em> (also <em>stalinih</em>) 
            has one occurrence in the corpus.</p>
        '''giga

        self.head = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{self.lemma}</title>
                <style>
                    {css}
                </style>
                </head>
        '''

    # Migrate to trash?
    def compile_formatted_forms_dict(self) -> Dict[str, str]:
        out_dict: Dict[str, str] = {}
        for key, form in self.grammarname_form_dict.items():
            out_dict[form.form_representation] = form.formatted
        return out_dict

    def add_formatted_to_word_forms(self) -> None:
        # add formatted element to each word form object
        for grammar_name, form in self.grammarname_form_dict.items():
            form.formatted = bold_except(form.form_representation,
                                         self.lemma_base_str)
            form.formatted = gray_unused(to_gray=form.formatted,
                                         frequency=form.frequency)

    def compile_pron_index_dict(self) -> Dict[str, List[Dict[str, str]]]:
        dict_list_dict: dict[str, list[dict[str, str]]] = {}
        for grammar_name, form in self.grammarname_form_dict.items():
            dict_list: list[dict[str, str]] = form.pronunciation_data
            dict_list_dict[form.form_representation] = dict_list
        return dict_list_dict

    def generate_table(self, copy: str = None) -> Union[str, None]:
        function_string: str = f"self.{self.part_of_speech}()"
        if hasattr(self, f"{self.part_of_speech}"):
            table_html = eval(function_string)
            formatted_table = self.wrap_table(table_html)

            # Copy relevant HTML to clipboard
            if self.part_of_speech == copy:
                print(self.part_of_speech, "coppied")
                pyperclip.copy(formatted_table)
            return formatted_table
        else:
            return None

    def noun(self) -> Union[str, None]:
        table_package = {
            "lemma": self.lemma,
            "type": self.type,
            "gender": self.gender,
        }

        for grammar_name, form in self.grammarname_form_dict.items():
            table_package[grammar_name] = {
                "word": form.form_representation,
                "html": form.formatted,
                "pron": form.ipa,
                "freq": form.frequency,
                "emph": form.accentuation
            }

        print("table package:", table_package)

        return None

    def xverb(self) -> Union[str, None]:
        form_representation_strings: list[str] = []
        for gn, word_form in self.grammarname_form_dict.items():
            form_representation_strings.append(word_form.formatted)
            vform = getattr(word_form, "vform", None)
            number = getattr(word_form, "number", None)
            person = getattr(word_form, "person", None)
            gender = getattr(word_form, "gender", None)

            pronunciation: str = ""
            for pronunciation_style in word_form.pronunciation_data:
                pronunciation += f'<br>{pronunciation_style["IPA"]}'

            if vform == "infinitive":
                self.infinitive = {"w": word_form.formatted,
                                   "p": pronunciation}
            elif vform == "supine":
                self.supine = {"w": word_form.formatted, "p": pronunciation}
            else:
                # Since participles dont have person, but do have gender
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
                setattr(self, variable_name,
                        {"w": word_form.formatted, "p": pronunciation})

        table_html = f'''
        <div class="content hidden" id="inflection_{self.lemma}">
            <p class="heading"> <em><b>verb</b></em>; <em>{getattr(self, "aspect", "")}</em>, <em>{getattr(self, "type", "")}</em>

                <p class="lineabove"> <b>Present Tense</b>
                    <table class="inflection">
                        <tr>
                            <th></th>
                            <th>singular</th>
                            <th>dual</th>
                            <th>plural</th>
                        </tr>
                        <tr>
                            <th>1st person</th>
                            <td title="present first singular" class="pop-up">{getattr(self, "present_first_singular", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "present_first_singular", dict(w='', p=''))["p"]}</span></td>
                            <td title="present first dual" class="pop-up">{getattr(self, "present_first_dual", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "present_first_dual", dict(w='', p=''))["p"]}</span></td>
                            <td title="present first plural" class="pop-up">{getattr(self, "present_first_plural", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "present_first_plural", dict(w='', p=''))["p"]}</span></td>
                        </tr>
                        <tr>
                            <th>2nd person</th>
                            <td title="present second singular" class="pop-up">{getattr(self, "present_second_singular", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "present_second_singular", dict(w='', p=''))["p"]}</span></td>
                            <td title="present second dual" class="pop-up">{getattr(self, "present_second_dual", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "present_second_dual", dict(w='', p=''))["p"]}</span></td>
                            <td title="present second plural" class="pop-up">{getattr(self, "present_second_plural", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "present_second_plural", dict(w='', p=''))["p"]}</span></td>
                        </tr>
                        <tr>
                            <th>3rd person</th>
                            <td title="present third singular" class="pop-up">{getattr(self, "present_third_singular", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "present_third_singular", dict(w='', p=''))["p"]}</span></td>
                            <td title="present third dual" class="pop-up">{getattr(self, "present_third_dual", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "present_third_dual", dict(w='', p=''))["p"]}</span></td>
                            <td title="present third plural" class="pop-up">{getattr(self, "present_third_plural", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "present_third_plural", dict(w='', p=''))["p"]}</span></td>
                        </tr>
                    </table>
                </p>

                <p class="lineabove"> <b>Imperative</b>
                    <table class="inflection">
                        <tr>
                            <th></th>
                            <th>singular</th>
                            <th>dual</th>
                            <th>plural</th>
                        </tr>
                        <tr>
                            <th>1st person</th>
                            <td title="imperative first singular" class="pop-up">{getattr(self, "imperative_first_singular", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "imperative_first_singular", dict(w='', p=''))["p"]}</span></td>
                            <td title="imperative first dual" class="pop-up">{getattr(self, "imperative_first_dual", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "imperative_first_dual", dict(w='', p=''))["p"]}</span></td>
                            <td title="imperative first plural" class="pop-up">{getattr(self, "imperative_first_plural", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "imperative_first_plural", dict(w='', p=''))["p"]}</span></td>
                        </tr>
                        <tr>
                            <th>2nd person</th>
                            <td title="imperative second singular" class="pop-up">{getattr(self, "imperative_second_singular", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "imperative_second_singular", dict(w='', p=''))["p"]}</span></td>
                            <td title="imperative second dual" class="pop-up">{getattr(self, "imperative_second_dual", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "imperative_second_dual", dict(w='', p=''))["p"]}</span></td>
                            <td title="imperative second plural" class="pop-up">{getattr(self, "imperative_second_plural", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "imperative_second_plural", dict(w='', p=''))["p"]}</span></td>
                        </tr>
                    </table>
                </p>

                <p class="lineabove"> <b>Participle</b>
                    <table class="inflection">
                        <tr>
                            <th></th>
                            <th>singular</th>
                            <th>dual</th>
                            <th>plural</th>
                        </tr>
                        <tr>
                            <th>masculine</th>
                            <td title="participle singular masculine" class="pop-up">{getattr(self, "participle_masculine_singular", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "participle_masculine_singular", dict(w='', p=''))["p"]}</span></td>
                            <td title="participle dual masculine" class="pop-up">{getattr(self, "participle_masculine_dual", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "participle_masculine_dual", dict(w='', p=''))["p"]}</span></td>
                            <td title="participle plural masculine" class="pop-up">{getattr(self, "participle_masculine_plural", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "participle_masculine_plural", dict(w='', p=''))["p"]}</span></td>
                        </tr>
                        <tr>
                            <th>feminine</th>
                            <td title="participle singular feminine" class="pop-up">{getattr(self, "participle_feminine_singular", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "participle_feminine_singular", dict(w='', p=''))["p"]}</span></td>
                            <td title="participle dual feminine" class="pop-up">{getattr(self, "participle_feminine_dual", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "participle_feminine_dual", dict(w='', p=''))["p"]}</span></td>
                            <td title="participle plural feminine" class="pop-up">{getattr(self, "participle_feminine_plural", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "participle_feminine_plural", dict(w='', p=''))["p"]}</span></td>
                        </tr>
                        <tr>
                            <th>neuter</th>
                            <td title="participle singular neuter" class="pop-up">{getattr(self, "participle_neuter_singular", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "participle_neuter_singular", dict(w='', p=''))["p"]}</span></td>
                            <td title="participle dual neuter" class="pop-up">{getattr(self, "participle_neuter_dual", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "participle_neuter_dual", dict(w='', p=''))["p"]}</span></td>
                            <td title="participle plural neuter" class="pop-up">{getattr(self, "participle_neuter_plural", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "participle_neuter_plural", dict(w='', p=''))["p"]}</span></td>
                        </tr>
                    </table>
                </p>

                <p class="lineabove"> <b>Infinitive and Supine</b>
                    <table class="inflection">
                        <tr>
                            <th>infinitive</th>
                            <td title="infinitive" class="pop-up">{getattr(self, "infinitive", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "infinitive", dict(w='', p=''))["p"]}</span></td>
                        </tr>
                        <tr>
                            <th>supine</th>
                            <td title="supine" class="pop-up">{getattr(self, "supine", dict(w='', p=''))["w"]}<span class="pop-up-content">Pronunciation:{getattr(self, "supine", dict(w='', p=''))["p"]}</span></td>
                        </tr>
                    </table>
                </p>

            </p>
            {self.gigafida_footer}
        </div>
        '''

        return table_html

    def verb(self) -> None:  # PLACEHOLDER
        return None

    # region undefined p_o_s
    def adjective(self):
        form_representation_strings: list[str] = []
        for gn, word_form in self.grammarname_form_dict.items():
            form_representation_strings.append(word_form.formatted)

            # defining attributes such as number, gender, person, etc.
            # gender = getattr(word_form, "gender", None)
            var1: str = ''
            var2: str = ''
            var3: str = ''

            # conditionals for determining what the variable name should be
            # i.e. (what table it goes in)

            variable_name = f'{var1}_{var2}_{var3}'

            # declare variable_name
            setattr(self, variable_name, word_form.formatted)

        table_html = f'''
        <div class="content hidden" id=inflection_{self.lemma}>
        </div>
        '''

        return None  # Replace with table_html

    def adverb(self):
        form_representation_strings: list[str] = []
        for gn, word_form in self.grammarname_form_dict.items():
            form_representation_strings.append(word_form.formatted)

            # defining attributes such as number, gender, person, etc.
            # gender = getattr(word_form, "gender", None)
            var1: str = ''
            var2: str = ''
            var3: str = ''

            # conditionals for determining what the variable name should be
            # i.e. (what table it goes in)

            variable_name = f'{var1}_{var2}_{var3}'

            # declare variable_name
            setattr(self, variable_name, word_form.formatted)

        table_html = f'''
                <div class="content hidden" id=inflection_{self.lemma}>
                </div>
                '''

        return None  # Replace with table_html

    def pronoun(self):
        form_representation_strings: list[str] = []
        for gn, word_form in self.grammarname_form_dict.items():
            form_representation_strings.append(word_form.formatted)

            # defining attributes such as number, gender, person, etc.
            # gender = getattr(word_form, "gender", None)
            var1: str = ''
            var2: str = ''
            var3: str = ''

            # conditionals for determining what the variable name should be
            # i.e. (what table it goes in)

            variable_name = f'{var1}_{var2}_{var3}'

            # declare variable_name
            setattr(self, variable_name, word_form.formatted)

        table_html = f'''
                <div class="content hidden" id=inflection_{self.lemma}>
                </div>
                '''

        return None  # Replace with table_html

    def numeral(self):
        form_representation_strings: list[str] = []
        for gn, word_form in self.grammarname_form_dict.items():
            form_representation_strings.append(word_form.formatted)

            # defining attributes such as number, gender, person, etc.
            # gender = getattr(word_form, "gender", None)
            var1: str = ''
            var2: str = ''
            var3: str = ''

            # conditionals for determining what the variable name should be
            # i.e. (what table it goes in)

            variable_name = f'{var1}_{var2}_{var3}'

            # declare variable_name
            setattr(self, variable_name, word_form.formatted)

        table_html = f'''
                <div class="content hidden" id=inflection_{self.lemma}>
                </div>
                '''

        return None  # Replace with table_html

    def preposition(self):
        form_representation_strings: list[str] = []
        for gn, word_form in self.grammarname_form_dict.items():
            form_representation_strings.append(word_form.formatted)

            # defining attributes such as number, gender, person, etc.
            # gender = getattr(word_form, "gender", None)
            var1: str = ''
            var2: str = ''
            var3: str = ''

            # conditionals for determining what the variable name should be
            # i.e. (what table it goes in)

            variable_name = f'{var1}_{var2}_{var3}'

            # declare variable_name
            setattr(self, variable_name, word_form.formatted)

        table_html = f'''
                <div class="content hidden" id=inflection_{self.lemma}>
                </div>
                '''

        return None  # Replace with table_html

    def conjunction(self):
        form_representation_strings: list[str] = []
        for gn, word_form in self.grammarname_form_dict.items():
            form_representation_strings.append(word_form.formatted)

            # defining attributes such as number, gender, person, etc.
            # gender = getattr(word_form, "gender", None)
            var1: str = ''
            var2: str = ''
            var3: str = ''

            # conditionals for determining what the variable name should be
            # i.e. (what table it goes in)

            variable_name = f'{var1}_{var2}_{var3}'

            # declare variable_name
            setattr(self, variable_name, word_form.formatted)

        table_html = f'''
                <div class="content hidden" id=inflection_{self.lemma}>
                </div>
                '''

        return None  # Replace with table_html

    def particle(self):
        form_representation_strings: list[str] = []
        for gn, word_form in self.grammarname_form_dict.items():
            form_representation_strings.append(word_form.formatted)

            # defining attributes such as number, gender, person, etc.
            # gender = getattr(word_form, "gender", None)
            var1: str = ''
            var2: str = ''
            var3: str = ''

            # conditionals for determining what the variable name should be
            # i.e. (what table it goes in)

            variable_name = f'{var1}_{var2}_{var3}'

            # declare variable_name
            setattr(self, variable_name, word_form.formatted)

        table_html = f'''
                <div class="content hidden" id=inflection_{self.lemma}>
                </div>
                '''

        return None  # Replace with table_html

    def interjection(self):
        form_representation_strings: list[str] = []
        for gn, word_form in self.grammarname_form_dict.items():
            form_representation_strings.append(word_form.formatted)

            # defining attributes such as number, gender, person, etc.
            # gender = getattr(word_form, "gender", None)
            var1: str = ''
            var2: str = ''
            var3: str = ''

            # conditionals for determining what the variable name should be
            # i.e. (what table it goes in)

            variable_name = f'{var1}_{var2}_{var3}'

            # declare variable_name
            setattr(self, variable_name, word_form.formatted)

        table_html = f'''
                <div class="content hidden" id=inflection_{self.lemma}>
                </div>
                '''

        return None  # Replace with table_html

    def abbreviation(self):
        form_representation_strings: list[str] = []
        for gn, word_form in self.grammarname_form_dict.items():
            form_representation_strings.append(word_form.formatted)

            # defining attributes such as number, gender, person, etc.
            # gender = getattr(word_form, "gender", None)
            var1: str = ''
            var2: str = ''
            var3: str = ''

            # conditionals for determining what the variable name should be
            # i.e. (what table it goes in)

            variable_name = f'{var1}_{var2}_{var3}'

            # declare variable_name
            setattr(self, variable_name, word_form.formatted)

        table_html = f'''
                <div class="content hidden" id=inflection_{self.lemma}>
                </div>
                '''

        return None  # Replace with table_html

    def residual(self):
        form_representation_strings: list[str] = []
        for gn, word_form in self.grammarname_form_dict.items():
            form_representation_strings.append(word_form.formatted)

            # defining attributes such as number, gender, person, etc.
            # gender = getattr(word_form, "gender", None)
            var1: str = ''
            var2: str = ''
            var3: str = ''

            # conditionals for determining what the variable name should be
            # i.e. (what table it goes in)

            variable_name = f'{var1}_{var2}_{var3}'

            # declare variable_name
            setattr(self, variable_name, word_form.formatted)

        table_html = f'''
                <div class="content hidden" id=inflection_{self.lemma}>
                </div>
                '''

        return None  # Replace with table_html

    # endregion

    def wrap_table(self, string: str) -> Union[str, None]:
        if string is not None:
            wrapped = f'''
                {self.head}

                <body>
                    <div class="container">
                        <button class="button" onclick="toggleTable('inflection_{self.lemma}')">Inflections</button>
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
    def __init__(self, lemma: str, frequency: int, type=None, gender=None,
                 form_representation=None, morphosyntactic_tags=None,
                 grammatical_features=None, pronunciation_data=None,
                 accentuation=None, formatted=None):

        self.form_representation: str = form_representation
        self.lemma: str = lemma
        self.type: str = type
        self.gender: str = gender
        self.morphosyntactic_tags: str = morphosyntactic_tags
        self.accentuation: str = accentuation
        self.formatted: str = formatted

        self.frequency: int = frequency

        self.grammatical_features: Dict[str, str] = grammatical_features
        self.pronunciation_data: List[Dict[str, str]] = pronunciation_data

        # Belongs in entry class?
        self.table_package: Dict[str, Union[str, Dict]] = {
            "lemma": self.lemma,
            "type": self.type,
            "gender": self.gender,
            "forms": {}
        }

        self.vform = self.grammatical_features.get("vform", None)
        self.case = self.grammatical_features.get("case", None)
        self.person = self.grammatical_features.get("person", None)
        self.number = self.grammatical_features.get("number", None)
        self.gender = self.grammatical_features.get("gender", None)

        # string with each IPA pronunciation on its own line
        self.ipa = ""
        self.sampa = ""
        for pronunciation_style in self.pronunciation_data:
            self.ipa += f'<br>{pronunciation_style["IPA"]}'
        for pronunciation_style in self.pronunciation_data:
            self.sampa += f'<br>{pronunciation_style["SAMPA"]}'

        self.grammar_name = concatenate_variables(
            self.vform,
            self.case,
            self.person,
            self.number,
            self.gender
        )

        print(f"{self.form_representation}'s grammar name is "
              f" {self.grammar_name}")


