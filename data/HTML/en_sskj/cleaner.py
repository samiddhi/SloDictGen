import os
import re
from bs4 import BeautifulSoup

class HTMLTagRemover:
    def __init__(self, directory: str):
        self.directory = directory
        self.removed_count = 0

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
        cleaned_content = re.sub(r'^\s*$', '', html_content, flags=re.MULTILINE)
        return cleaned_content

    def process_html_content(self, html_content: str) -> str:
        """Process HTML content to modify tags."""
        soup = BeautifulSoup(html_content, 'html.parser')
        #self.remove_citation_tags(soup)
        #self.remove_and_preserve_tags(soup)
        #self.remove_font_tags(soup)
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

    def get_removal_count(self) -> int:
        """Get the total count of modifications made."""
        return self.removed_count

# Example usage
directory_path = './'  # Assumes this file is in the same directory with HTML files
remover = HTMLTagRemover(directory_path)
remover.process_files()
print(f"Total modifications made: {remover.get_removal_count()}")
