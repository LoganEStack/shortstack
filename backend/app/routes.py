from flask import Blueprint, request, jsonify, redirect
from datetime import date
import re
from datetime import datetime
from urllib.parse import urlparse
from .models import URL
from .db import db
from .short_code_gen import generate_short_code

main = Blueprint('main', __name__)


def is_valid_url(url: str):
    """Returns True if url is a valid URL format."""
    try:
        result = urlparse(url)
        return result.scheme in ['http', 'https'] and result.netloc
    except:
        return False


def validate_request(original_url:str, expiration_date:date, alias:str):
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400
    if not is_valid_url(original_url):
        return jsonify({'error': 'URL is not valid'}), 400
    
    if not expiration_date:
        return jsonify({'error': 'Expiration date not included in request.'}), 400
    
    if alias:
        if not re.search("^[a-zA-Z0-9_-]{0,16}$", alias) or len(alias) < 5 or len(alias) >= 16:
            return jsonify({'error': 'Alias must contain 5-16 alphanumeric characters, dashes, or underscores'}), 400
        if URL.query.filter_by(short_code=alias).first():
            return jsonify({'error': 'Alias is already taken'}), 400
    
    return


@main.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    expiration_date = data.get('expiration_date')
    alias = data.get('alias')

    error = validate_request(original_url, expiration_date, alias)
    if error:
        return error

    try:
        expiration_date = datetime.fromisoformat(expiration_date)
    except ValueError:
        return jsonify({'error': 'Invalid expiration_date format'}), 400
    
    code = alias
    if not alias:
        code = generate_short_code()
        # Avoids duplicate short codes by checking the database.
        while URL.query.filter_by(short_code=code).first():
            code = generate_short_code()

    new_url = URL(original_url=original_url, short_code=code,
                  expiration_date=expiration_date)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({'short_url': request.host_url + code, 'expiration_date': expiration_date})


@main.route('/<short_code>')
def redirect_to_url(short_code:str):
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if url_entry:
        return redirect(url_entry.original_url)
    return jsonify({'error': 'URL not found'}), 404
