from flask import Blueprint, request, jsonify
from datetime import datetime, timezone

from .utils import require_api_key
from .models import URL
from .db import db

admin = Blueprint('admin', __name__)


@admin.route('/admin/db/stats', methods=['GET'])
def get_stats():
    """Gets database usage statistics."""
    require_api_key()

    count = URL.query.count()
    
    estimated_row_size = 300  # Estimated row size in bytes
    estimated_total_size_bytes = count * estimated_row_size
    estimated_total_size_mb = round(estimated_total_size_bytes / (1024 * 1024), 2)

    now = datetime.now(timezone.utc)
    expired_count = URL.query.filter(URL.expiration_date < now).count()

    return jsonify({
        'estimated_size_mb': estimated_total_size_mb,
        'total_entries': count,
        'total_entries_expired': expired_count,
        'time_of_report': now
    }), 200


@admin.route('/admin/db/urls', methods=['GET'])
def get_urls():
    """Gets all short codes currently in DB. Can specify pagination."""
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


@admin.route('/admin/db/<short_code>', methods=['GET'])
def get_url_by_code(short_code):
    """Gets a specific entry by short code in the DB."""
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


@admin.route('/admin/db', methods=['GET'])
def get_urls_by_url_query():
    """Gets a list of entries based on a URL query."""
    require_api_key()

    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    matches = URL.query.filter(URL.original_url.ilike(f'%{query}%')).all()
    results = [{
        'short_code': url.short_code,
        'original_url': url.original_url,
        'expiration_date': url.expiration_date.isoformat()
    } for url in matches]

    return jsonify(results)


@admin.route('/admin/db/<short_code>', methods=['DELETE', "OPTIONS"])
def delete_short_code(short_code):
    """Delete a specific short code in the DB."""
    require_api_key()

    url_entry = URL.query.filter_by(short_code=short_code).first()
    if not url_entry:
        return jsonify({'error': 'Short code not found'}), 404

    db.session.delete(url_entry)
    db.session.commit()
    return jsonify({'message': f"Short code '{short_code}' deleted"}), 200


@admin.route('/admin/db/<int:count>', methods=['DELETE', "OPTIONS"])
def delete_old_short_codes(count):
    """Delete X least recent short codes in the DB."""
    require_api_key()

    urls = URL.query.order_by(URL.created_at.desc()).limit(count).all()
    if not urls:
        return jsonify({'message': 'No URLs to delete'}), 200

    deleted = [url.short_code for url in urls]
    for url in urls:
        db.session.delete(url)

    db.session.commit()
    return jsonify({'message': f'Deleted {len(deleted)} least recent URLs', 'short_codes': deleted}), 200


@admin.route('/admin/db/cleanup', methods=['DELETE', "OPTIONS"])
def delete_expired_codes():
    """Deletes all expired short codes."""
    require_api_key()

    now = datetime.now(timezone.utc)
    expired_urls = URL.query.filter(URL.expiration_date < now).all()
    count = len(expired_urls)

    for url in expired_urls:
        db.session.delete(url)
    db.session.commit()

    return jsonify({'deleted': count})