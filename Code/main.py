from typing import List, Dict, Union
import tkinter as tk
from tkhtmlview import HTMLLabel
from entry_parser import SloleksEntry, WordForm, XMLParser
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
    xml_file: str = (r"C:\Users\sangha\Documents\Danny's\slodict"
                     r"\Resources\Markdown\XML\sloleks_3.0_sample.xml")
    parser: XMLParser = XMLParser(xml_file)
    entries: List[SloleksEntry] = parser.entries

    for entry in entries:
        pos = entry.part_of_speech
        if pos == "noun":
            table_html = eval(f'formatting.{pos}_table({entry}, '
                              f'"{COPY}")')
            print(f"Noun Table Coppied:\n\n{table_html[:29]}\n...\n"
                  f"{table_html[-10:]}")


if __name__ == "__main__":
    main()
