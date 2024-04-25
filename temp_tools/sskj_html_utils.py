import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import os
import time
import sys
from unidecode import unidecode
import string

from tqdm import tqdm
import re

from lxml import etree
import json

from icecream import ic

# Add the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class PairToJson:
    def __init__(self):
        slo_entries = self.parse_html_stream('si_sskj.html')
        eng_entries = self.parse_html_stream('en_sskj.html')

        paired_data = {}
        count = 0

        for slo, eng in zip(slo_entries, eng_entries):
            slo_content = self.serialize_div_content(slo)
            eng_content = self.serialize_div_content(eng)
            # Use the link as the key; it's expected to be found in each entry
            slo_link = \
                slo.xpath(".//span[contains(@class, 'font_xlarge')]/a/@href")[
                    0]
            eng_link = \
                eng.xpath(".//span[contains(@class, 'font_xlarge')]/a/@href")[
                    0]
            if slo_link == eng_link:
                paired_data[slo_link] = {
                    'slovenian_content': slo_content,
                    'english_content': eng_content
                }
                count += 1
                if count % 10000 == 0:
                    self.save_data(paired_data)
                    print(f'{count} pairs saved')
            else:
                print(
                    f'{'/'.join(str(slo_link).split("/")[-2:]).split("?page=")[0]}'
                    f'(slo) is not'
                    f'{'/'.join(str(eng_link).split("/")[-2:]).split("?page=")[0]}')
                break

        if count % 10000 != 0:
            self.save_data(paired_data)

    @staticmethod
    def parse_html_stream(file_path: str):
        context = etree.iterparse(file_path, events=('end',), tag='div',
                                  html=True)
        for event, elem in context:
            if 'entry-content' in elem.get('class', '').split():
                yield elem
            # Clear the element to save memory
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

    @staticmethod
    def serialize_div_content(entry):
        return etree.tostring(entry, encoding='unicode', method='html')

    @staticmethod
    def save_data(paired_data, filename='paired_entries.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(paired_data, f, ensure_ascii=False, indent=4)


class HTMLTagRemover:
    """
    Removes citations, redundant <div class="entry-content">,  <font> tags,
    and lastly blank lines from an html file. Specifically for data scraped
    from franDOTsi
    """

    def __init__(self, directory: str):
        self.directory = directory
        self.removed_count = 0
        self.process_files

    def read_file(self, file_path: str) -> str:
        """Read the contents of a file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def write_file(self, file_path: str, content: str) -> None:
        """Write content to a file."""
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    def remove_citation_tags(self, soup: BeautifulSoup) -> None:
        """Remove the citation tags."""
        tags_to_remove = soup.findAll("p", {"class": "entry-citation"})
        for tag in tags_to_remove:
            tag.decompose()
            self.removed_count += 1

    def remove_and_preserve_tags(self, soup: BeautifulSoup) -> None:
        """Remove specific outer div tags while preserving the inner div contents."""
        target_divs = soup.findAll("div", {"class": "list-group-item entry"})
        for div in target_divs:
            inner_content = div.find("div", {"class": "entry-content"})
            if inner_content:
                div.replace_with(inner_content)
                self.removed_count += 1

    def remove_font_tags(self, soup: BeautifulSoup) -> None:
        """Remove all <font> tags but preserve the content within."""
        font_tags = soup.findAll("font")
        for tag in font_tags:
            tag.unwrap()  # Unwrap removes the tag but keeps its contents intact.
            self.removed_count += 1

    def remove_blank_lines(self, html_content: str) -> str:
        """Remove all blank lines from the HTML content using regex."""
        cleaned_content = re.sub(r'^\s*$', '', html_content,
                                 flags=re.MULTILINE)
        return cleaned_content

    def process_html_content(self, html_content: str) -> str:
        """Process HTML content to modify tags."""
        soup = BeautifulSoup(html_content, 'html.parser')
        self.remove_citation_tags(soup)
        self.remove_and_preserve_tags(soup)
        self.remove_font_tags(soup)
        processed_html = self.remove_blank_lines(str(soup))
        return processed_html

    def process_files(self) -> None:
        """Process each HTML file in the directory."""
        for filename in os.listdir(self.directory):
            if filename.endswith(".html"):
                file_path = os.path.join(self.directory, filename)
                content = self.read_file(file_path)
                updated_content = self.process_html_content(content)
                self.write_file(file_path, updated_content)
                print(f'{filename} done!')


class Scraper:
    """
    A class designed to scrape web content using Selenium, tailored for fran.si
    """

    def __init__(
            self,
            start_url: str,
            output_folder: str,
            file_name: str,
            total_pages: int = 4884  # Add total pages if known or
            # expected
    ) -> None:
        driver_path = r"C:\Users\sangha\Documents\Danny's\SloDictGen\data\chromedriver.exe"
        options = Options()
        self.driver = webdriver.Chrome(service=Service(driver_path),
                                       options=options)
        self.start_url: str = start_url
        self.base_url: str = f"{urlparse(start_url).scheme}://{urlparse(start_url).netloc}"
        self.output_folder: str = output_folder
        self.filename: str = file_name
        self.output_file: str = os.path.join(output_folder,
                                             f'{file_name}.html')
        self.total_pages = total_pages
        self.pages_scraped = 0
        self.scrape()

    def scrape(self) -> None:
        current_url = self.start_url
        total_entries = 0
        timings = []

        with tqdm(total=self.total_pages) as pbar:
            while current_url:
                start_time = time.time()

                html_content = self.fetch_page_content(current_url)
                entries = self.parse_entries(html_content)
                total_entries += len(entries)
                self.save_entries(entries)

                elapsed_time = time.time() - start_time
                timings.append(elapsed_time)

                current_url = self.find_next_page_url(html_content)
                self.pages_scraped += 1
                pbar.update(1)

                # Calculate average time per page from all collected timings
                avg_time = sum(timings) / len(timings)
                remaining_pages = self.total_pages - self.pages_scraped
                estimated_time_left = remaining_pages * avg_time

                pbar.set_postfix_str(
                    f"Est. Time Left: {estimated_time_left / 60:.2f} min")

        print(f'Entries: {total_entries}\n\n')

    def fetch_page_content(self, url: str) -> str:
        """
        Utilizes Selenium WebDriver to navigate to a URL and fetches the
        entire HTML content of the page.

        :param url: The URL to navigate to and fetch content.
        :return: HTML content of the page as a string.
        """
        self.driver.get(url)
        time.sleep(.1)
        return self.driver.page_source

    def parse_entries(self, html_content: str) -> List[str]:
        """
        Parses HTML content to extract specific entries, removes unwanted
        elements, and formats them.

        :param html_content: The HTML content as a string.
        :return: A list of cleaned and formatted HTML entries as strings.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        entries = soup.find_all('div', class_='list-group-item entry')
        for entry in entries:
            div_to_remove = entry.find('div', class_='badges pull-right')
            if div_to_remove:
                div_to_remove.decompose()
        return [entry.prettify(formatter="html5") + '<br>' for entry in
                entries]

    def find_next_page_url(self, html_content: str) -> Optional[str]:
        """
        Analyzes HTML content to find the URL of the next page, if available.

        :param html_content: The HTML content of the current page.
        :return: The URL of the next page or None if no next page is found.
        """
        self.pages_scraped += 1

        soup = BeautifulSoup(html_content, 'html.parser')
        next_button = soup.find('ul', class_='pagination').find_all('a')[-1]
        if next_button and ("Next" in next_button.text or "Naslednja" in
                            next_button.text):
            return self.base_url + next_button['href']
        return None

    def save_entries(self, entries: List[str]) -> None:
        """
        Writes the parsed entries to a file with appropriate formatting.

        :param entries: A list of HTML formatted strings to be saved.
        """
        if not os.path.exists(os.path.dirname(self.output_file)):
            os.makedirs(os.path.dirname(self.output_file))
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write('\n'.join(entries) + '\n')

    def close_driver(self) -> None:
        """
        Closes the Selenium WebDriver cleanly.

        :return: None.
        """
        self.driver.quit()


class FindUntranslatedHTML:
    def __init__(
            self,
            path: str = (r"C:\Users\sangha\Documents\Danny's\SloDictGen\data"
                         r"\html\sskj\paired_entries.json")
    ) -> None:
        """
        Reads JSON file generated with PairToJson class for untranslated
        English versions of HTML

        :param path: path to JSON
        """
        self.untranslated: List[str] = []

        with open(path, 'rb') as file:
            pairs: Dict[str, Dict[str, str]] = json.load(file)

        for unique_link in pairs:
            stripped: List[str] = [
                self.stripchars(
                    html,
                    [' ', ' ', '\r', '\n', '\t']
                ) for html in pairs[unique_link].values()
            ]

            frontsearch, backsearch = True, True
            front, back = 0, 0
            en, slo = stripped[0], stripped[1]
            longest = max(len(en), len(slo))
            for i in range(0, longest-1):
                if frontsearch and en[i] == slo[i]:
                    front += 1
                elif backsearch:
                    frontsearch = False
                else:
                    break

                if backsearch and en[-i] == slo[-i]:
                    back += 1
                elif frontsearch:
                    backsearch = False
                else:
                    break

            if max(front, back) >= longest/4:
                self.untranslated.append(pairs[unique_link]["english_content"])

        with open('untranslated.txt', 'w') as f:
            print('\n\n'.join(self.untranslated), file=f)


    def stripchars(self, inpt: str, chars: List[str]) -> str:
        if not chars:
            return inpt
        outpt = ''.join(inpt.split(chars[0]))
        return self.stripchars(outpt, chars[1:])

def main() -> None:
    FindUntranslatedHTML()


if __name__ == "__main__":
    main()
