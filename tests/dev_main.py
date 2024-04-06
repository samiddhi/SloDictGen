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
    print_sample(return_table(xml_path=filepath, to_copy="noun"))


if __name__ == "__main__":
    main()
