from openai import OpenAI
from typing import Dict, List, Tuple
import pickle
import ast
from icecream import ic
from unidecode import unidecode
from dataclasses import dataclass
from slo_dict_gen_pkg.grammar_utils import de_critic
import sys

sys.setrecursionlimit(1000000)


class SskjLetterEntries:
    def __init__(self, letter: str) -> None:
        pkl_obj: Dict[str, List[str]] = self.open_pickle_jar(letter)
        raw_entries: Tuple[Tuple[str, List[str]]] = tuple(pkl_obj.items())
        self.entries = self.pickle_to_sskjentry_objs(raw_entries)

    def pickle_to_sskjentry_objs(
            self,
            entries: Tuple[Tuple[str, List[str]]],
            inpt: Tuple['SskjEntry', ...] = ()
    ) -> Tuple['SskjEntry', ...]:
        if entries:
            entry = entries[0]
            accentuation = entry[0]
            lemma = de_critic(accentuation)
            definitions = entry[-1]
            entry_obj: SskjEntry = SskjEntry(
                lemma=lemma,
                accentuation=accentuation,
                definitions=definitions
            )
            outpt = inpt + tuple([entry_obj])
            return self.pickle_to_sskjentry_objs(entries[1:], outpt)
        else:
            return inpt

    @staticmethod
    def open_pickle_jar(char: str) -> any:
        file_path = (
            r"C:\Users\sangha\Documents\Danny's\SloDictGen\data\HTML"
            f"\\SSKJ_entries_html\\{char}_output.pkl")
        with open(file_path, 'rb') as pickle_file:
            pickle_object = pickle.load(pickle_file)

        return pickle_object


@dataclass(frozen=True)
class SskjEntry:
    accentuation: str
    lemma: str
    definitions: List[str]

    def __str__(self) -> str:
        def numerical_list(items: list, inpt: str = '') -> str:
            """
            Takes a list and returns a string of its items enumerated.
            Purely functional beauty

            :param items:
            :param inpt:
            :return: str
            """
            try:
                # My try at branchless programming. Strips trailing ; and :
                to_strip = items[-1][-1] in (";", ":")
                item_stripped = (items[-1] * int(not to_strip) + items[-1][
                                                                 :-1] * int(
                    to_strip))

                outpt: str = f'{len(items)}. {item_stripped}\n' + inpt
                return numerical_list(items[:-1], outpt)
            except IndexError:
                return inpt

        return f'~{self.lemma}~\n{numerical_list(self.definitions)}'


@dataclass(frozen=True)
class GPT:
    api_key: str = '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'
    client: OpenAI = OpenAI(api_key=api_key)

    def message(self, package: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": '''
                        You are a translator receiving entries from a Slovenian 
                        dictionary, each consisting of a Slovenian word 
                        sometimes a few definitions and translating each entry 
                        in its entirety (the word itself & all its definitions) 
                        into English. Your output will be a series of 
                        simple dictionary entries entirely in English (NO 
                        SLOVENIAN whatsoever!) Maintain the format of the 
                        content provided.
                        
                        For example, with such an input:
                        
                        ~Celzij~
                        1. enota za merjenje temperature po skali, pri kateri je vrelišče vode pri 100°
                        
                        You will return:
                        
                        ~Celsius~
                        1. A unit of measurement for temperature of a scale for which the boiling point of water is 100°
                        
                        Return only the string of your english dictionary 
                        entries and nothing else.
                        '''
                },
                {
                    "role": "user",
                    "content": package
                }
            ],
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content


def gpt_packager(
        entries: Tuple[SskjEntry, ...],
        inpt_str: str = '',
        inpt_tuple: Tuple[str, ...] = ()
) -> Tuple[str, ...]:
    """
    Takes list of SSKJ Entry objects and returns a tuple of GPT-readable
    strings just under 2000 characters. Purely functional.
    
    :param entries: List of SskjEntry objects
    :param inpt_str: ~ignore~
    :param inpt_tuple: ~ignore~
    :return: Tuple of strings
    """
    if entries:
        inpt_plus_entry = f'{inpt_str}\n{str(entries[0])}'
        if len(inpt_plus_entry) < 2000:
            return gpt_packager(
                entries[1:],
                inpt_plus_entry,
                inpt_tuple
            )
        else:
            return gpt_packager(
                entries,
                '',
                inpt_tuple + (inpt_str,)
            )
    else:
        return inpt_tuple + (inpt_str,)


def main() -> None:
    LETTER = "c"
    entries: Tuple[SskjEntry, ...] = SskjLetterEntries(LETTER).entries
    assemble_packages = gpt_packager(entries)
    bot = GPT()
    for i in assemble_packages:
        print(i)

    for package in assemble_packages[0]:
        go = False
        #### CHECK CELSIUS DEFINITION ####
        #### + CHECK CHARACTER LIMIT! ####
        if go:
            print(bot.message(package=package))


if __name__ == "__main__":
    main()
