import argparse

from app.parser import BeautifulSoupParser
from app.export import HtmlExport


def generate_output_file(input_file: str, output_file: str) -> None:
    parser = BeautifulSoupParser(input_file)

    exporter = HtmlExport(parser.get_teidocument())

    with open(output_file, "w") as file:
        file.write(exporter.export())


if __name__ == '__main__':
    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--input_file_path", required=True, help="Path to a XML file.")
    ap.add_argument("-o", "--output_file_path", required=True, help="Path to HTML output file.")

    args = vars(ap.parse_args())

    input_file_path = args['input_file_path']
    output_file_path = args['output_file_path']

    try:
        generate_output_file(input_file_path, output_file_path)
    except FileNotFoundError:
        print(f"Input file incorrect, please check the path, paths provided: \n input_file_path: {input_file_path} "
              f"\n output_file_path: {output_file_path}")
