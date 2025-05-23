import string
import random


def generate_short_code(length:int=6):
    """Returns a random string of alphanumeric characters with default length 6."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
