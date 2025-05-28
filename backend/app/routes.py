from datetime import datetime, timezone, timedelta
from flask import Blueprint, request, jsonify, redirect
from sqlalchemy.exc import IntegrityError

from config import Config
from .db import db
from .models import URL
from .limiter import limiter
from .utils import validate_db_not_full, validate_shorten_request
from .short_code_gen import generate_short_code

main = Blueprint('main', __name__)
TTL = 7  # days til expiration


@main.route('/shorten', methods=['POST'])
@limiter.limit(Config.RATE_LIMIT)
def shorten_url():
    """Returns a string to be used as a short URL and writes it to a DB."""
    validate_db_not_full()
    
    data = request.get_json()
    original_url = data.get('url')
    alias = data.get('alias')
    timestamp = datetime.now(timezone.utc)
    expiration_date = (timestamp + timedelta(TTL)).isoformat()

    error = validate_shorten_request(original_url, expiration_date, alias)
    if error:
        return error

    code = alias
    max_attempts = 3
    for _ in range(max_attempts):
        if not alias:
            code = generate_short_code(original_url, timestamp)
            while URL.query.filter_by(short_code=code).first():
                code = generate_short_code(original_url, timestamp)

        try:
            new_url = URL(original_url=original_url, short_code=code,
                        expiration_date=expiration_date)
            db.session.add(new_url)
            db.session.commit()
            return jsonify({
                'short_url': request.host_url + code,
                'expiration_date': expiration_date
            })
        except IntegrityError:
            db.session.rollback()

    return jsonify({'error': 'Could not generate a unique short code, please try again.'}), 500



@main.route('/<short_code>')
def redirect_to_url(short_code:str):
    """Redirects from a short URL to its associated long URL."""
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if url_entry:
        return redirect(url_entry.original_url)
    return jsonify({'error': 'URL not found'}), 404
