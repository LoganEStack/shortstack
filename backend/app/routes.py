import re
from datetime import date, datetime, timezone, timedelta
from flask import Blueprint, request, jsonify, redirect
from sqlalchemy import text
from .models import URL
from .db import db
from .limiter import limiter
from .utils import is_valid_url
from .short_code_gen import generate_short_code

main = Blueprint('main', __name__)
MAX_DB_SIZE_BYTES = 200 * 1024 * 1024  # 200 MB


def validate_shorten_request(original_url:str, expiration_date:date, alias:str):
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


def get_db_size():
    result = db.session.execute(text("SELECT pg_database_size(current_database());"))
    return result.scalar()


@main.route('/shorten', methods=['POST'])
@limiter.limit("10 per minute")
def shorten_url():
    """Returns a string to be used as a short URL and writes it to a DB."""

    current_size = get_db_size()
    if current_size >= MAX_DB_SIZE_BYTES:
        return jsonify({
            'error': 'Database is currently full. Links expire after 1 week. Apologies for the inconvenience.'
        }), 507
    
    data = request.get_json()
    original_url = data.get('url')
    alias = data.get('alias')
    timestamp = datetime.now(timezone.utc)
    expiration_date = (timestamp + timedelta(7)).isoformat()

    error = validate_shorten_request(original_url, expiration_date, alias)
    if error:
        return error
    
    code = alias
    if not alias:
        code = generate_short_code(original_url, timestamp)
        # Avoids duplicate short codes by checking the database.
        while URL.query.filter_by(short_code=code).first():
            code = generate_short_code(original_url, timestamp)

    new_url = URL(original_url=original_url, short_code=code,
                  expiration_date=expiration_date)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({'short_url': request.host_url + code, 'expiration_date': expiration_date})


@main.route('/<short_code>')
def redirect_to_url(short_code:str):
    """Redirects from a short URL to its associated long URL."""
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if url_entry:
        return redirect(url_entry.original_url)
    return jsonify({'error': 'URL not found'}), 404
