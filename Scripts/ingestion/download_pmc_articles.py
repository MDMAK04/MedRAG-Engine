import json
import time
import tarfile
import requests
from io import BytesIO
from pathlib import Path
import xml.etree.ElementTree as ET

OA_URL = "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi"

INPUT_FILE = Path("data/metadata/pmc_ids.json")
OUTPUT_DIR = Path("data/raw")


def load_pmc_ids():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["pmc_ids"]

def get_article_package(pmc_id):

    params = {
        "id": f"PMC{pmc_id}"
    }

    response = requests.get(
        OA_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    root = ET.fromstring(response.text)

    record = root.find(".//record")

    if record is None:
        raise RuntimeError(
            f"No OA record found for PMC{pmc_id}"
        )

    package_link = None

    for link in record.findall("link"):
        if link.attrib.get("format") == "tgz":
            package_link = link.attrib.get("href")
            break

    if package_link is None:
        raise RuntimeError(
            f"No TGZ package available for PMC{pmc_id}"
        )

    return package_link

def download_file(url):

    # PMC may return an FTP URL.
    # Convert it to HTTPS for requests.
    if url.startswith("ftp://"):
        url = url.replace(
            "ftp://ftp.ncbi.nlm.nih.gov",
            "https://ftp.ncbi.nlm.nih.gov"
        )

    response = requests.get(
        url,
        timeout=120
    )

    response.raise_for_status()

    return response.content


def extract_package(package_data, article_dir):

    article_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    with tarfile.open(
        fileobj=BytesIO(package_data),
        mode="r:gz"
    ) as archive:

        archive.extractall(article_dir)


def main():

    pmc_ids = load_pmc_ids()[:1]

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print(f"Articles to download: {len(pmc_ids)}")

    success = 0
    failed = 0

    for index, pmc_id in enumerate(
        pmc_ids,
        start=1
    ):

        print(
            f"[{index}/{len(pmc_ids)}] "
            f"Downloading PMC{pmc_id}"
        )

        article_dir = (
            OUTPUT_DIR /
            f"PMC{pmc_id}"
        )

        try:

            package_url = get_article_package(
                pmc_id
            )

            print(
                f"  Package found"
            )

            package_data = download_file(
                package_url
            )

            print(
                f"  Downloaded "
                f"{len(package_data) / 1024 / 1024:.2f} MB"
            )

            extract_package(
                package_data,
                article_dir
            )

            print(
                "  Extracted successfully"
            )

            success += 1

        except Exception as error:

            print(
                f"  Error: {error}"
            )

            failed += 1

        time.sleep(1)

    print()
    print("================================")
    print("Download completed")
    print("================================")
    print(f"Successful: {success}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()