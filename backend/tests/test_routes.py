import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_shorten_valid_url(client):
    response = client.post('/shorten', json={'url': 'https://example.com'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'short_url' in data

def test_shorten_missing_url(client):
    response = client.post('/shorten', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_shorten_invalid_json(client):
    response = client.post('/shorten', data='not-json', content_type='application/json')
    assert response.status_code == 400

def test_redirect_existing_code(client):
    # First shorten a URL
    shorten = client.post('/shorten', json={'url': 'https://example.com'})
    short_url = shorten.get_json()['short_url']
    code = short_url.rsplit('/', 1)[-1]

    # Then request the short URL
    redirect = client.get(f'/{code}')
    assert redirect.status_code == 302
    assert redirect.location == 'https://example.com'

def test_redirect_unknown_code(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404
