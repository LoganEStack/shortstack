import os
import re

from flask import request, jsonify, abort
from datetime import date
from sqlalchemy import text
from urllib.parse import urlparse

from config import Config
from .db import db
from .models import URL

API_KEY = Config.API_KEY
MAX_DB_SIZE_BYTES = 200 * 1024 * 1024  # 200 MB


def require_api_key():
    """Checks if a request contains a valid API key."""
    key = request.headers.get('X-API-Key')
    if key != API_KEY:
        abort(401, description="Invalid or missing API key")


def is_valid_url(url: str):
    """Returns True if url is a valid URL format."""
    try:
        result = urlparse(url)
        return result.scheme in ['http', 'https'] and result.netloc
    except:
        return False
    

def get_db_size():
    result = db.session.execute(text("SELECT pg_database_size(current_database());"))
    return result.scalar()


def validate_db_not_full():
    current_size = get_db_size()
    if current_size >= MAX_DB_SIZE_BYTES:
        return jsonify({
            'error': 'Database is currently full. Links expire after 1 week. Apologies for the inconvenience.'
        }), 507

def validate_shorten_request(url:str, expiration_date:date, alias:str):
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    elif not is_valid_url(url):
        return jsonify({'error': 'URL is not valid'}), 400
    
    if not expiration_date:
        return jsonify({'error': 'Expiration date not included in request.'}), 400
    
    if alias:
        if not re.search("^[a-zA-Z0-9_-]{0,16}$", alias) or len(alias) < 5 or len(alias) >= 16:
            return jsonify({'error': 'Alias must contain 5-16 alphanumeric characters, dashes, or underscores'}), 400
        if URL.query.filter_by(short_code=alias).first():
            return jsonify({'error': 'Alias is already taken'}), 400