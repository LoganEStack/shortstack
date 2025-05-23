from flask import Blueprint, request, jsonify, redirect
import string
import random
import re
from urllib.parse import urlparse
from .models import URL
from .db import db

main = Blueprint('main', __name__)


def is_valid_url(url):
    """Returns True if url is a valid URL format."""
    try:
        result = urlparse(url)
        print(result, all([result.scheme, result.netloc, result.path]))
        return result.scheme in ['http', 'https'] and result.netloc
    except:
        return False


def generate_short_code(length=10):
    """Returns a random string of alphanumeric characters with default length 10."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@main.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    alias = data.get('alias')
    
    # Validate URL
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400
    if not is_valid_url(original_url):
        return jsonify({'error': 'URL is not valid'}), 400
    
    # Validate alias or generate code
    if alias:
        code = alias
        if not re.search("^[a-zA-Z0-9_-]{0,16}$", code) or len(code) < 5 or len(code) >= 16:
            return jsonify({'error': 'Alias must contain 5-16 alphanumeric characters, dashes, or underscores'}), 400
        if URL.query.filter_by(short_code=code).first():
            return jsonify({'error': 'Alias is already taken'}), 400
    else:
        code = generate_short_code()
        while URL.query.filter_by(short_code=code).first(): # Avoids duplicate short codes by checking the database.
            code = generate_short_code()

    new_url = URL(original_url=original_url, short_code=code)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({'short_url': request.host_url + code})


@main.route('/<short_code>')
def redirect_to_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if url_entry:
        return redirect(url_entry.original_url)
    return jsonify({'error': 'URL not found'}), 404
