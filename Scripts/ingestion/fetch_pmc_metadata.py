import json
import time
import requests
from pathlib import Path


BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

INPUT_FILE = Path("data/metadata/pmc_ids.json")
OUTPUT_FILE = Path("data/metadata/pmc_metadata.json")


def load_pmc_ids():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["pmc_ids"]


def fetch_metadata(pmc_id):
    params = {
        "db": "pmc",
        "id": pmc_id,
        "retmode": "json"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def main():

    pmc_ids = load_pmc_ids()

    print(f"Articles to process: {len(pmc_ids)}")

    metadata = []

    for index, pmc_id in enumerate(pmc_ids, start=1):

        print(f"[{index}/{len(pmc_ids)}] Fetching PMC{pmc_id}")

        try:

            data = fetch_metadata(pmc_id)

            metadata.append({
                "pmc_id": pmc_id,
                "data": data
            })

        except requests.RequestException as error:

            print(f"Error for PMC{pmc_id}: {error}")

        time.sleep(0.2)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
            ensure_ascii=False
        )

    print()
    print(f"Saved metadata to: {OUTPUT_FILE}")
    print(f"Articles processed: {len(metadata)}")


if __name__ == "__main__":
    main()