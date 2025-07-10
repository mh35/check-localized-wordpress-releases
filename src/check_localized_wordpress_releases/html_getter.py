"""Fetch and parse HTML module."""

import requests
from lxml.html import HtmlElement, fromstring


def fetch_html(url: str) -> HtmlElement:
    """Fetch HTML and parse.

    Args:
        url(str): Target URL

    Returns:
        HtmlElement: Parsed HTML
    """
    res = requests.get(url)
    res.raise_for_status()
    return fromstring(res.content)
