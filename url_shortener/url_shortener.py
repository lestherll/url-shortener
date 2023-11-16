import base64
import hashlib


def shorten_url(url: str) -> tuple[bytes, bytes]:
    """
    Shortens a given URL using a hash function and base64 encoding.

    Args:
        url (str): The original URL to be shortened.

    Returns:
        tuple[bytes, bytes]: A tuple containing the shortened URL in base64 encoding and its hash.

    Example:
        >>> shorten_url("https://www.example.com")
        ('aHR0cHM6Ly93d3cue...encoded hash...', 'hashed_url')
    """
    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
    url_b64 = base64.urlsafe_b64encode(url_hash.encode("utf-8"))
    return url_b64, url_hash
