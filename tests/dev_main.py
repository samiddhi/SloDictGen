from slo_dict_gen_pkg import *
from random import shuffle
from tkhtmlview import HTMLLabel
import tkinter as tk


def display_html(content):
    """
    Displays HTML (no css)

    :param content: string of HTML
    """
    root = tk.Tk()
    html_label = HTMLLabel(root, html=content)
    html_label.pack(fill="both", expand=True)
    html_label.fit_height()
    root.mainloop()


def copy_table(xml_path: str, to_copy: str) -> str:
    """
    takes xml path + part of speech and returns a random entry with that
    part of speech as a formatted table

    :param xml_path: (str) XML file path
    :param to_copy: (str) part of speech to be copied, lowercase
    :return table_html (str): html format of a given
    """
    parser_obj: XMLParser = XMLParser(xml_path)


    entry_obj_list: List[SloleksEntry] = parser_obj.entries
    shuffle(entry_obj_list)

    table_html: str = ""
    for entry in entry_obj_list:
        table_html = eval(f'formatting.{to_copy}_table({entry}, '
                          f'"{to_copy}")') if (entry.part_of_speech ==
                                               to_copy) else table_html
    return table_html


def print_sample(text: str, percent: float = 0.5) -> None:
    """
    Prints a sample of a string based on a given percentage.

    :param text: (str) Text to sample
    :param percent: (float) Percentage of string to show on either side
    """
    sample_size = int(round(len(text) * float(percent / 100)))
    print(f"\nNoun Table Copied:\n\n{text[:sample_size]}\n...\
    n{text[-sample_size:]}")


def main():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.dirname(current_directory)
    data_directory = os.path.join(parent_directory, 'data')
    filename = 'sloleks_3.0_sample.xml'
    filepath = os.path.join(data_directory, 'Markdown', 'XML', filename)
    print_sample(copy_table(xml_path=filepath, to_copy="noun"))


if __name__ == "__main__":
    main()
