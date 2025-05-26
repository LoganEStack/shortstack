from urllib.parse import urlparse


def is_valid_url(url: str):
    """Returns True if url is a valid URL format."""
    try:
        result = urlparse(url)
        return result.scheme in ['http', 'https'] and result.netloc
    except:
        return False