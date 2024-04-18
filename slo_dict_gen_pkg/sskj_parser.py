from common.imports import *
from dataclasses import dataclass
import os
import re

from bs4 import BeautifulSoup
import pickle

from slo_dict_gen_pkg.grammar_utils import ordered_grammar_name, de_critic


@dataclass
class SskjEntry:
    """
    :html: str
    :accentuation: str
    :lemma: str
    :definitions: List[str]
    :sub_words: List[SskjEntry]
    """
    html: str
    accentuation: str
    lemma: str
    definitions: List[str]
    sub_words: List['SskjEntry']


class HTMLParser:
    """
    self.sskjentrys is a list of all SskjEntry objects generated from given
    file
    """
    def __init__(
            self,
            html_path: str,
            save_path: str = None
    ) -> None:
        """
        Initializes an HTMLParser instance for a given HTML file path.

        :param html_file: Path to the HTML file to parse.
        :param save_path: Saves file if path is given
        """
        if os.path.exists(html_path):
            content: str = self._html_content(html_path)
            soup: BeautifulSoup = self._parse_html(content)
            self.sskjentrys: List[SskjEntry] = self._soup_to_sskjentrys(soup)
            if save_path:
                self._save_pickle(self.sskjentrys, save_path)

    @staticmethod
    def _html_content(filepath: str) -> str:
        with open(filepath, 'r', encoding='utf-8') as file:
            html_content = file.read()

        return html_content

    @staticmethod
    def _parse_html(html_content: str) -> BeautifulSoup:
        return BeautifulSoup(html_content, 'html.parser')

    def _soup_to_sskjentrys(self, soup: BeautifulSoup) -> List[SskjEntry]:
        entries = soup.find_all("div", class_="list-group-item entry")
        all_sskjentrys = []
        for entry in entries:
            entry_clone = BeautifulSoup(str(entry), 'html.parser').div
            orange_entries = entry_clone.find_all("ul", class_="manual")

            # Now pass each <ul class="manual"> individually
            sub_words: List[SskjEntry] = [self._html_to_sskjentry(ul) for ul in
                                          orange_entries]

            # Remove all <ul class="manual"> elements from the clone and
            # finally create clone entry with all subwords
            for ul in orange_entries:
                ul.decompose()
            head_word = self._html_to_sskjentry(html=entry_clone,
                                          sub_words=sub_words)

            all_sskjentrys.extend([head_word] + sub_words)

        return all_sskjentrys

    @staticmethod
    def _html_to_sskjentry(
            html: BeautifulSoup,
            sub_words: List[SskjEntry] = None
    ) -> SskjEntry:
        try:
            accentuation = html.find("span", class_="font_xlarge").get_text(
                strip=True)
        except AttributeError:
            accentuation = html.find("span", class_="color_orange").get_text(
                strip=True)
        lemma = de_critic(accentuation)
        explanations = [
            re.sub(r'\s+', ' ', span.get_text(strip=True))
            # Replaces all whitespace with a single space
            for span in
            html.find_all("span", {"data-group": "explanation "})
        ]
        return SskjEntry(
            html=str(html),
            lemma=lemma,
            accentuation=accentuation,
            definitions=explanations,
            sub_words=sub_words
        )

    @staticmethod
    def _save_pickle(
            data: ...,
            filename: str
    ) -> None:
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

letter = "c"
HTMLParser(
    r"C:\Users\sangha\Documents\Danny's\SloDictGen\data\HTML"
    f"\\SSKJ_entries_html\\Letter_{letter}.html",
    r"C:\Users\sangha\Documents\Danny's\SloDictGen\data\pickles"
    f"\\html_objects\\Letter_{letter}.pkl"
)


