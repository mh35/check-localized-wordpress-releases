"""Parse releases HTML and get releases."""

from lxml.html import HtmlElement


def parse_releases_html(html: HtmlElement) -> dict[str, list[tuple[str, str]]]:
    """Parse releases HTML.

    Args:
        html(HtmlElement): Target HTML
    Returns:
        dict: Key is the major version. Value is the list of tuples.
        A tuple consists of version and zip URL.
    """
    release_sections = html.cssselect(
        ".wp-block-wporg-release-tables__section"
    )
    ret: dict[str, list[tuple[str, str]]] = {}
    for release_section in release_sections:
        if release_section.attrib["id"] == "latest":
            continue
        elif release_section.attrib["id"] == "betas":
            section_title = "Beta & RC"
        elif release_section.attrib["id"] == "mu":
            section_title = "MU"
        elif release_section.attrib["id"].startswith("branch-"):
            section_title = (
                release_section.attrib["id"][7:8]
                + "."
                + release_section.attrib["id"][8:]
            )
        releases: list[tuple[str, str]] = []
        for row in release_section.cssselect("tbody tr"):
            release_version = row.cssselect("th")[0].text_content()
            zip_url = row.cssselect(
                ".wp-block-wporg-release-tables__cell-zip a"
            )[0].attrib["href"]
            releases.append((release_version, zip_url))
            ret[section_title] = releases
    return ret
