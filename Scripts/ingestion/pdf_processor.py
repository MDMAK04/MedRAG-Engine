import pymupdf


def extract_pages_from_pdf(pdf_path: str):

    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text").strip()

        if not text:
            continue

        pages.append({
            "page": page_number,
            "text": text
        })

    document.close()

    return pages


def extract_text_from_pdf(pdf_path: str) -> str:

    pages = extract_pages_from_pdf(pdf_path)

    return "\n\n".join(
        f"PAGE {page['page']}\n\n{page['text']}"
        for page in pages
    )