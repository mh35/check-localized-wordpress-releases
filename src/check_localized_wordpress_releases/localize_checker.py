"""Get all localized WordPress release pages."""

from lxml.html import HtmlElement


def get_localized_release_pages(html: HtmlElement) -> dict[str, str]:
    """Get localized release page URLs.

    Args:
        html(HtmlElement): Page HTML

    Returns:
        dict: Language and release page URLs
    """
    ret: dict[str, str] = {}
    for elem in html.cssselect('link[rel="alternate"][hreflang]'):
        ret[elem.attrib["hreflang"]] = elem.attrib["href"]
    return ret
