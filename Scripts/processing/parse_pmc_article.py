import json
import xml.etree.ElementTree as ET
from pathlib import Path


ARTICLE_DIR = Path("data/raw/PMC7033891")

XML_FILE = ARTICLE_DIR / "article.xml"

OUTPUT_FILE = ARTICLE_DIR / "parsed_article.json"


def clean_text(element):
    if element is None:
        return ""

    return " ".join(
        " ".join(element.itertext()).split()
    )


def extract_metadata(root):

    metadata = {}

    article_title = root.find(".//article-title")

    metadata["title"] = clean_text(article_title)

    authors = []

    for author in root.findall(
        ".//contrib[@contrib-type='author']"
    ):

        surname = author.find(".//surname")
        given_names = author.find(".//given-names")

        name = " ".join(
            filter(
                None,
                [
                    clean_text(given_names),
                    clean_text(surname)
                ]
            )
        )

        if name:
            authors.append(name)

    metadata["authors"] = authors

    journal = root.find(".//journal-title")

    metadata["journal"] = clean_text(journal)

    year = root.find(".//pub-date/year")

    metadata["publication_year"] = clean_text(year)

    return metadata


def parse_section(section, parent_path=None):

    title_element = section.find("./title")

    title = clean_text(title_element)

    if parent_path:
        section_path = parent_path + " > " + title
    else:
        section_path = title

    section_data = {

        "title": title,

        "path": section_path,

        "paragraphs": [],

        "subsections": []

    }

    # Paragraphes directement contenus dans cette section
    for paragraph in section.findall("./p"):

        text = clean_text(paragraph)

        if text:
            section_data["paragraphs"].append(text)

    # Sous-sections
    for subsection in section.findall("./sec"):

        subsection_data = parse_section(
            subsection,
            section_path
        )

        section_data["subsections"].append(
            subsection_data
        )

    return section_data


def extract_sections(root):

    sections = []

    body = root.find(".//body")

    if body is None:
        return sections

    # Seulement les sections principales
    for section in body.findall("./sec"):

        section_data = parse_section(section)

        sections.append(section_data)

    return sections


def extract_figures(root):

    figures = []

    for figure in root.findall(".//fig"):

        label = figure.find("./label")

        caption = figure.find("./caption")

        graphic = figure.find(".//graphic")

        figure_data = {

            "label": clean_text(label),

            "caption": clean_text(caption),

            "image": None

        }

        if graphic is not None:

            image_path = graphic.attrib.get(
                "{http://www.w3.org/1999/xlink}href"
            )

            figure_data["image"] = image_path

        figures.append(figure_data)

    return figures


def extract_tables(root):

    tables = []

    for table_wrap in root.findall(".//table-wrap"):

        label = table_wrap.find("./label")

        caption = table_wrap.find("./caption")

        table = table_wrap.find(".//table")

        table_data = {

            "label": clean_text(label),

            "caption": clean_text(caption),

            "rows": []

        }

        if table is not None:

            for row in table.findall(".//tr"):

                cells = []

                for cell in row:

                    cells.append(
                        clean_text(cell)
                    )

                table_data["rows"].append(cells)

        tables.append(table_data)

    return tables


def count_sections(sections):

    count = 0

    for section in sections:

        count += 1

        count += count_sections(
            section["subsections"]
        )

    return count


def parse_article():

    print("Loading XML...")

    tree = ET.parse(XML_FILE)

    root = tree.getroot()

    print("XML loaded successfully")

    sections = extract_sections(root)

    document = {

        "pmcid": "PMC7033891",

        "metadata": extract_metadata(root),

        "sections": sections,

        "figures": extract_figures(root),

        "tables": extract_tables(root)

    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            document,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()

    print("Parsing completed")

    print(
        f"Output: {OUTPUT_FILE}"
    )

    print()

    print("Statistics")

    print(
        "Total sections:",
        count_sections(sections)
    )

    print(
        "Figures:",
        len(document["figures"])
    )

    print(
        "Tables:",
        len(document["tables"])
    )


if __name__ == "__main__":

    parse_article()