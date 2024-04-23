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


def main() -> None:
    # Specify the paths to your files in alphabetical order
    file_paths = [
        '1. á-kíhavec.html',
        '2. kíhavica-previjálka.html',
        '3. previjálnica-squint.html',
        '4. strabismus-zvrkljáti.html'
    ]
    output_file_path = 'en_sskj.html'

    file_paths = [
        '1. á-nacvréti.html',
        '2. načákati_se-soslédica.html',
        '3. soslédje-žvrkljáti.html'
    ]
    output_file_path = 'si_sskj.html'

    combine_html_files(file_paths, output_file_path)


if __name__ == "__main__":
    main()
