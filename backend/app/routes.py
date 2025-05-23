from flask import Blueprint, request, jsonify, redirect
from .models import URL
from .db import db
import string
import random

main = Blueprint('main', __name__)


def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@main.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    alias = data.get('alias')

    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    if alias:
        code = alias
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
