"""Test localize_checker module."""

import os

from lxml.html import fromstring

from check_localized_wordpress_releases.localize_checker import (
    get_localized_release_pages,
)


def test_get_localized_release_pages() -> None:
    """Test get_localized_release_pages function."""
    html_path = os.path.join(
        os.path.dirname(__file__), "assets", "en_releases.html"
    )
    with open(html_path, "r", encoding="utf-8") as fp:
        html = fromstring(fp.read())
    ret = get_localized_release_pages(html)
    assert ret["ja-jp"] == "https://ja.wordpress.org/download/releases/"
