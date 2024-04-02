from typing import List, Dict, Union
import tkinter as tk
from tkhtmlview import HTMLLabel
from entry_parser import Entry, WordForm, XMLParser
import formatting

COPY = "noun"


def get_one_of_each() -> None:
    return None


def display_html(content):
    root = tk.Tk()
    html_label = HTMLLabel(root, html=content)
    html_label.pack(fill="both", expand=True)
    html_label.fit_height()
    root.mainloop()


def main():
    directory: str = (r"C:\Users\sangha\Documents\Danny's\slodict"
                      r"\Resources\Sloleks.3.0")
    xml_file: str = (r"C:\Users\sangha\Documents\Danny's\slodict"
                     r"\Resources\Markdown\XML\sloleks_3.0_sample.xml")
    parser: XMLParser = XMLParser(xml_file)
    entries: List[Entry] = parser.entries

    for entry in entries:
        pos = entry.part_of_speech
        if pos == "noun":
            table_html = eval(f'formatting.{pos}_table({entry}, "{COPY}")')
            print(table_html)


if __name__ == "__main__":
    main()
