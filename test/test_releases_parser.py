"""Test releases_parser module."""

import os

from lxml.html import fromstring

from check_localized_wordpress_releases.releases_parser import parse_releases_html


def test_parse_releases_html() -> None:
    """Test parse_releases_html function."""
    html_path = os.path.join(
        os.path.dirname(__file__), "assets", "en_releases.html"
    )
    with open(html_path, "r", encoding="utf-8") as fp:
        html = fromstring(fp.read())
    ret = parse_releases_html(html)
    assert ret["6.7"][0][0] == "6.7.2"
    assert ret["6.7"][0][1] == "https://wordpress.org/wordpress-6.7.2.zip"
    assert ret["Beta & RC"][1][0] == "6.8.1-RC1"
    assert ret["Beta & RC"][1][1] == "https://wordpress.org/wordpress-6.8.1-RC1.zip"
