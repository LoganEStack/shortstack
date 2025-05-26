import hashlib
from datetime import datetime

def generate_short_code(original_url: str, timestamp: datetime, length: int = 6) -> str:
    """Generates a short code by hashing the original URL and timestamp."""

    raw_input = f"{original_url}{timestamp.isoformat()}".encode('utf-8')
    # Create a SHA-256 hash and take the first `length` characters of its hex digest
    hash_digest = hashlib.sha256(raw_input).hexdigest()

    return hash_digest[:length]
