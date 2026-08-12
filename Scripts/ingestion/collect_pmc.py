import requests
import json
from pathlib import Path


# Configuration

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

QUERY = (
    '("ischemic stroke"[Title/Abstract]) '
    'AND open access[filter] '
    'AND ("2018"[Publication Date] : "2026"[Publication Date])'
)

RETMAX = 100

OUTPUT_DIR = Path("data/metadata")
OUTPUT_FILE = OUTPUT_DIR / "pmc_ids.json"



# Search PMC

def search_pmc(query: str, retmax: int = 100):

    params = {
        "db": "pmc",
        "term": query,
        "retstart": 0,
        "retmax": retmax,
        "retmode": "json",
        "sort": "relevance",
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return data["esearchresult"]


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    result = search_pmc(
        QUERY,
        RETMAX
    )

    count = int(result["count"])
    ids = result["idlist"]

    print(f"Total results found by PMC: {count}")
    print(f"Articles retrieved: {len(ids)}")

    print("\nFirst 10 PMC IDs:")

    for pmc_id in ids[:10]:
        print(pmc_id)

    output = {
        "query": QUERY,
        "total_results": count,
        "retrieved": len(ids),
        "pmc_ids": ids
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output,
            f,
            indent=4
        )

    print(f"\nSaved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()