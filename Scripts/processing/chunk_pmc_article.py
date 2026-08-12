import json
from pathlib import Path


INPUT_FILE = Path(
    "data/raw/PMC7033891/parsed_article.json"
)

OUTPUT_FILE = Path(
    "data/processed/chunks/PMC7033891_chunks.json"
)


def create_chunk(
    pmcid,
    chunk_id,
    path,
    text
):
    return {
        "chunk_id": chunk_id,
        "pmcid": pmcid,
        "path": path,
        "text": text
    }


def process_section(
    section,
    pmcid,
    chunks,
    chunk_counter
):
    path = section.get("path", section.get("title", ""))

    paragraphs = section.get("paragraphs", [])

    for paragraph in paragraphs:

        if not paragraph.strip():
            continue

        chunk_counter[0] += 1

        chunk_id = (
            f"{pmcid}_chunk_{chunk_counter[0]:04d}"
        )

        chunks.append(
            create_chunk(
                pmcid=pmcid,
                chunk_id=chunk_id,
                path=path,
                text=paragraph.strip()
            )
        )

    subsections = section.get("subsections", [])

    for subsection in subsections:

        process_section(
            subsection,
            pmcid,
            chunks,
            chunk_counter
        )

def main():
    print("Loading article...")
    with open(INPUT_FILE,"r",encoding="utf-8") as file:
        article = json.load(file)

    print("Article loaded successfully")
    pmcid = article["pmcid"]
    chunks = []
    chunk_counter = [0]
    for section in article.get("sections", []):
        process_section(
            section,
            pmcid,
            chunks,
            chunk_counter
        )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(OUTPUT_FILE,"w",encoding="utf-8") as file:
        json.dump(
            chunks,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("Chunks saved successfully")
    print(f"Output: {OUTPUT_FILE}")

    print()
    print("==============================")
    print("CHUNKING STATISTICS")
    print("==============================")

    print(f"Total chunks: {len(chunks)}")
    paths = {}
    for chunk in chunks:
        path = chunk["path"]
        paths[path] = paths.get(path, 0) + 1

    print()
    print("Chunks by section:")

    for path, count in paths.items():
        print(f"  {path}: {count}")

if __name__ == "__main__":
    main()