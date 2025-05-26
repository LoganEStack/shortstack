import os
from flask import Blueprint, request, jsonify, abort
from datetime import datetime
from .models import URL
from .db import db

debug = Blueprint('debug', __name__)
API_KEY = os.getenv('SECRET_KEY')


def require_api_key():
    """Checks if a request contains a valid API key."""
    key = request.headers.get('key')
    print(API_KEY)
    if key != API_KEY:
        abort(401, description="Invalid or missing API key")

@debug.route('/debug/urls', methods=['GET'])
def list_urls():
    """Lists short codes currently in DB. Can specify pagination."""
    require_api_key()

    try:    # Pagination params
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({"error": "Invalid pagination values"}), 400

    query = URL.query.order_by(URL.created_at.desc())
    paginated = query.paginate(page=page, per_page=limit, error_out=False)

    results = []
    for url in paginated.items:
        results.append({
            "original_url": url.original_url,
            "short_code": url.short_code,
            "created_at": url.created_at.isoformat(),
            "expiration_date": url.expiration_date.isoformat() if url.expiration_date else None,
        })

    return jsonify({
        "page": page,
        "limit": limit,
        "total": paginated.total,
        "pages": paginated.pages,
        "urls": results
    })


@debug.route('/debug/urls/<short_code>', methods=['GET'])
def get_url_by_code(short_code):
    """Look up a specific short code in the DB."""
    require_api_key()

    url = URL.query.filter_by(short_code=short_code).first()
    if not url:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify({
        "original_url": url.original_url,
        "short_code": url.short_code,
        "created_at": url.created_at.isoformat(),
        "expiration_date": url.expiration_date.isoformat() if url.expiration_date else None,
    })


@debug.route('/debug/urls/<short_code>', methods=['DELETE'])
def delete_short_code(short_code):
    """Delete a specific short code in the DB."""
    require_api_key()

    url_entry = URL.query.filter_by(short_code=short_code).first()
    if not url_entry:
        return jsonify({'error': 'Short code not found'}), 404

    db.session.delete(url_entry)
    db.session.commit()
    return jsonify({'message': f'Short code "{short_code}" deleted'}), 200


@debug.route('/debug/urls/recent/<int:count>', methods=['DELETE'])
def delete_recent_short_codes(count):
    """Delete X least recent short codes in the DB."""
    require_api_key()

    urls = URL.query.order_by(URL.created_at.desc()).limit(count).all()
    if not urls:
        return jsonify({'message': 'No URLs to delete'}), 200

    deleted = [url.short_code for url in urls]
    for url in urls:
        db.session.delete(url)

    db.session.commit()
    return jsonify({'message': f'Deleted {len(deleted)} URLs', 'short_codes': deleted}), 200
