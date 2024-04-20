from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from typing import List, Optional
import os
import time
import sys
from unidecode import unidecode
import string


class ScraperOld:
    """                a one use wonder                 """
    ''' USED ON 12 APRIL 2024 FOR SSKJ ENTRY COLLECTION '''
    '''           requires: import requests             '''

    # has duplicates. i.e. "ozreti se" will appear for letter "s". Lots of
    # extra stuff.
    def fetch_page_content(self, url: str) -> str:
        """
        Fetches and returns the page content for a given URL.

        :param url: The URL of the page to fetch.
        :return: The content of the fetched page as a string.
        """
        response = requests.get(url)
        return response.content

    def parse_entries(self, html_content: str) -> List[str]:
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
        return [entry.prettify(formatter="html5") + '<br>' for entry in
                entries]

    def find_next_page_url(self, html_content: str, base_url: str) -> Optional[
        str]:
        """
        Finds and returns the next page URL if available, otherwise returns None.

        :param html_content: The HTML content of the current page.
        :param base_url: The base URL of the website.
        :return: The URL of the next page, or None if not available.
        """
        print(html_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        next_button = soup.find('ul', class_='pagination').find_all('a')[-1]
        if next_button and (
                "Next" in next_button.text or "Naslednja" in next_button.text):
            return base_url + next_button['href']
        return None

    def save_entries(self, entries: List[str], output_file: str) -> None:
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

    def __init__(self, start_url: str, base_url: str, output_folder: str,
                 letter: str) -> None:
        """
        Main interface to scrape the website starting from the base URL and save entries to an output file.

        :param start_url: The base URL of the website to scrape.
        :param base_url: The base e.g. "https://www.site.net/"
        :param output_folder: The directory to save the scraped HTML files.
        :param letter: The letter used to filter queries on the website.
        :return: None
        """
        output_file = f'{output_folder}/Letter_{letter}.html'
        current_url = start_url
        total_entries = 0
        while current_url:
            html_content = self.fetch_page_content(current_url)
            entries = self.parse_entries(html_content)
            for i in entries:
                print(i)
            total_entries += len(entries)
            self.save_entries(entries, output_file)
            current_url = self.find_next_page_url(html_content,
                                                  base_url)
            time.sleep(0.2)
        print(f'"{letter}" entries: {total_entries}\n\n')


class Cleaner:
    """Used to clean the above outputs which had duplicates. i.e. 'sex appeal'
    was in the outputs for "a". Could be improved upon, but it's a one hit
    wonder...
    """

    def __init__(self, directory, letters):
        for letter in letters:
            file_path = os.path.join(directory, f'Letter_{letter}.html')

            removed_entries = self.remove_entries(file_path, letter)
            print(f"Removed entries from Letter_{letter}.html:")
            for entry in removed_entries:
                print(entry)

    def remove_entries(self, file_path, letter):
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


class Scraper:
    """
    A class designed to scrape web content using Selenium. tailored for fran.si
    """

    def __init__(
            self,
            start_url: str,
            output_folder: str,
            file_name: str
    ) -> None:
        """
        Initializes the Scraper instance, sets up the Selenium WebDriver in 
        headless mode, and determines base URL from the start URL. It also 
        initiates the scraping process.

        :param start_url: The URL from which scraping starts. Assumes a proper
            URL format.
        :param output_folder: The directory path where output files are saved.
        :param file_name: The output file name
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver_path = (r"C:\Users\sangha\Documents\Danny's\SloDictGen"
                       r"\data\chromedriver.exe")
        self.driver: webdriver.Chrome = webdriver.Chrome(
            service=Service(driver_path),
            options=chrome_options
        )
        self.start_url: str = start_url
        self.base_url: str = (f"{urlparse(start_url).scheme}:"
                              f"//{urlparse(start_url).netloc}")
        self.output_folder: str = output_folder
        self.filename: str = file_name
        self.output_file: str = f'{output_folder}/{file_name}.html'
        self.scrape()

    def scrape(self) -> None:
        """
        Manages the complete scraping cycle, from fetching page content to 
        finding the next page.

        :return: None.
        """
        current_url = self.start_url
        total_entries = 0
        while current_url:
            html_content = self.fetch_page_content(current_url)
            entries = self.parse_entries(html_content)
            total_entries += len(entries)
            self.save_entries(entries)
            current_url = self.find_next_page_url(html_content)
            time.sleep(0.2)  # to mitigate potential rate-limiting issues
        print(f'Entries: {total_entries}\n\n')

    def fetch_page_content(self, url: str) -> str:
        """
        Utilizes Selenium WebDriver to navigate to a URL and fetches the 
        entire HTML content of the page.

        :param url: The URL to navigate to and fetch content.
        :return: HTML content of the page as a string.
        """
        self.driver.get(url)
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


def main() -> None:
    x = Scraper(
        start_url=r"https://fran.si/iskanje?FilteredDictionaryIds=133&View=1&Query=w*",
        file_name="All_Scraped",
        output_folder=r"C:\Users\sangha\Desktop\scraped_en_slo"
    )


if __name__ == "__main__":
    main()
