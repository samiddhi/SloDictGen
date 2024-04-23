from typing import List

def combine_html_files(file_paths: List[str], output_file_path: str) -> None:
    """
    Combines multiple HTML files into a single file in the order provided.

    :param file_paths: List of strings representing the file paths of HTML files to be combined
    :param output_file_path: String representing the path of the output HTML file
    """
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read() + "\n")  # Add a newline between files for readability

# Specify the paths to your files in alphabetical order
file_paths = [
    '1. á-soslédica.html',
    '2. soslédje-žvrkljáti.html'
]
output_file_path = 'si_sskj.html'

combine_html_files(file_paths, output_file_path)
