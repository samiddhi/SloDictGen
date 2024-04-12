import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import os
import time
import sys
from unidecode import unidecode
import string

class Scraper:
    """                a one use wonder                 """
    ''' USED ON 12 APRIL 2024 FOR SSKJ ENTRY COLLECTION '''

    # has duplicates. i.e. "ozreti se" will appear for letter "s". Lots of
    # extra stuff.
    def fetch_page_content(url: str) -> str:
        """
        Fetches and returns the page content for a given URL.

        :param url: The URL of the page to fetch.
        :return: The content of the fetched page as a string.
        """
        response = requests.get(url)
        return response.content

    def parse_entries(html_content: str) -> List[str]:
        """
        Parses HTML content and returns a list of entries as HTML strings, formatted with tabs.

        :param html_content: The HTML content to parse.
        :return: A list of parsed and formatted HTML entries as strings.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        entries = soup.find_all('div', class_='list-group-item entry')
        for entry in entries:
            div_to_remove = entry.find('div', class_='badges pull-right')
            if div_to_remove:
                div_to_remove.decompose()
        return [entry.prettify(formatter="html5") + '<br>' for entry in entries]

    def find_next_page_url(html_content: str, base_url: str) -> Optional[str]:
        """
        Finds and returns the next page URL if available, otherwise returns None.

        :param html_content: The HTML content of the current page.
        :param base_url: The base URL of the website.
        :return: The URL of the next page, or None if not available.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        next_button = soup.find('ul', class_='pagination').find_all('a')[-1]
        if next_button and ("Next" in next_button.text or "Naslednja" in next_button.text):
            return base_url + next_button['href']
        return None

    def save_entries(entries: List[str], output_file: str) -> None:
        """
        Saves parsed entries to the specified file, ensuring entries are written with proper HTML formatting.

        :param entries: A list of parsed entries.
        :param output_file: The file path to save the entries.
        :return: None
        """
        if not os.path.exists(os.path.dirname(output_file)):
            os.makedirs(os.path.dirname(output_file))
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write('\n'.join(entries) + '\n')

    def scrape_website(base_url: str, output_folder: str, letter: str) -> None:
        """
        Main interface to scrape the website starting from the base URL and save entries to an output file.

        :param base_url: The base URL of the website to scrape.
        :param output_folder: The directory to save the scraped HTML files.
        :param letter: The letter used to filter queries on the website.
        :return: None
        """
        output_file = f'{output_folder}/Letter_{letter}.html'
        current_url = base_url
        total_entries = 0
        while current_url:
            html_content = fetch_page_content(current_url)
            entries = parse_entries(html_content)
            total_entries += len(entries)
            save_entries(entries, output_file)
            current_url = find_next_page_url(html_content, 'https://www.fran.si')
            time.sleep(0.2)
        print(f'"{letter}" entries: {total_entries}\n\n')

class Cleaner:
    """Used to clean the above outputs which had duplicates. i.e. 'sex appeal'
    was in the outputs for "a". Could be improved upon, but it's a one hit
    wonder...
    """
    def remove_entries(file_path, letter):
        removed_entries = []

        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        entries = soup.find_all('div', class_='list-group-item entry')
        for entry in entries:
            entry_text = entry.find('span', class_='font_xlarge').text.strip()
            entry_text_ascii = unidecode(entry_text) if letter in ['a', 'e',
                                                                   'i',
                                                                   'o', 'u',
                                                                   'r'] else entry_text
            if not entry_text_ascii.lower().startswith(
                    letter.lower()) and not entry_text_ascii.startswith('&'):
                removed_entry_content = entry.find('a').text.strip()
                removed_entries.append(removed_entry_content)
                entry.extract()

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        return removed_entries

    def main():
        directory = r"C:\Users\sangha\Documents\Danny's\SloDictGen\scraper\Scraped_HTML"
        for letter in "čšž":  # abcdefghijklmnopqrstuvwxyz
            file_path = os.path.join(directory, f'Letter_{letter}.html')

            removed_entries = remove_entries(file_path, letter)
            print(f"Removed entries from Letter_{letter}.html:")
            for entry in removed_entries:
                print(entry)
