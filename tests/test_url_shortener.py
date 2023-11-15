import pytest

from url_shortener import url_shortener


def test_shorten_url():
    url = "127.0.0.1"
    expected = (
        b"EsoXtJryKJQ28wPgFmAwoh5SXSZuIJJnQzgBqP1AcaA=",
        b"\x12\xca\x17\xb4\x9a\xf2(\x946\xf3\x03\xe0\x16`0\xa2\x1eR]&n \x92gC8\x01\xa8\xfd@q\xa0",
    )
    assert expected == url_shortener.shorten_url(url)
