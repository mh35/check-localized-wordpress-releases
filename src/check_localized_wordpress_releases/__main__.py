"""Main program."""

import csv
import sys
import time
from argparse import ArgumentParser
from logging import INFO, basicConfig, getLogger

from requests.exceptions import HTTPError

from .html_getter import fetch_html
from .localize_checker import get_localized_release_pages
from .releases_parser import parse_releases_html


MAIN_RELEASES_URL = "https://wordpress.org/download/releases/"
BASE_SLEEP = 5

parser = ArgumentParser(description="WordPress list generator")
parser.add_argument("-o", "--output", required=True, help="Output filename")
args = parser.parse_args()

output_filename: str = args.output

logger = getLogger(__name__)
logger.setLevel(INFO)
basicConfig(stream=sys.stdout)

logger.info("Fetching: " + MAIN_RELEASES_URL)
base_html = fetch_html(MAIN_RELEASES_URL)
htmls = {MAIN_RELEASES_URL: base_html}
localized_pages = get_localized_release_pages(base_html)

rows: list[list[str]] = []

for locale, url in localized_pages.items():
    if url in htmls:
        locale_html = htmls[url]
    else:
        for i in range(3):
            time.sleep(BASE_SLEEP * (2 ** i))
            logger.info("Fetching: " + url)
            try:
                locale_html = fetch_html(url)
                break
            except HTTPError as e:
                if isinstance(e.args[0], str) and e.args[0].startswith("429"):
                    logger.warning("Failed to get " + url + ": " + str(i + 1))
                    continue
                else:
                    raise
        if "locale_html" not in locals():
            raise RuntimeError("Failed to get: " + url)
        htmls[url] = locale_html
    parse_results = parse_releases_html(locale_html)
    for branch, branch_data in parse_results.items():
        rows.extend(
            [locale, branch, item[0], item[1]]
            for item in branch_data
        )

with open(output_filename, "w", encoding="utf-8") as fp:
    writer = csv.writer(fp)
    writer.writerow(["Locale", "Branch", "Version", "URL"])
    writer.writerows(rows)
