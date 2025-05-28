import pytest
from datetime import datetime, timedelta, timezone
from app import create_app
from config import Config

API_KEY = Config.API_KEY


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def get_future_expiration(days=7):
    return (datetime.now(timezone.utc) + timedelta(days=days)).isoformat()


def test_redirect_unknown_code(client):
    """Invalid route."""
    response = client.get('/nonexistent')
    assert response.status_code == 404


def test_api_key(client):
    """Valid API key."""
    response = client.get('/admin/db/stats', headers={'X-API-Key': API_KEY})
    assert response.status_code == 200


def test_invalid_api_key(client):
    """Invalid API key."""
    response = client.get('/admin/db/stats', headers={'X-API-Key': 'wrong-key'})
    assert response.status_code == 401


def test_no_api_key(client):
    """No API key."""
    response = client.get('/admin/db/stats')
    assert response.status_code == 401
    response = client.get('/admin/db/stats', headers={'X-API-Key': ''})
    assert response.status_code == 401


def test_shorten_valid_url(client):
    """/shorten valid request."""
    response = client.post(
        '/shorten', json={'url': 'https://example.com', 'expiration_date': get_future_expiration()})
    assert response.status_code == 200
    data = response.get_json()
    assert 'short_url' in data

    # Clean up
    short_url = data['short_url']
    short_code = short_url.rstrip('/').split('/')[-1]

    delete_response = client.delete(
        f'/admin/db/{short_code}',
        headers={'X-API-Key': API_KEY}
    )
    assert delete_response.status_code == 200


def test_shorten_valid_url_alias(client):
    """/shorten valid request with alias."""
    ALIAS = "test_alias"
    client.delete(f'/admin/db/{ALIAS}', headers={'X-API-Key': API_KEY})

    response = client.post(
        '/shorten',
        json={'url': 'https://example.com', 
              'expiration_date': get_future_expiration(),
              'alias': ALIAS},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'short_url' in data
    assert data['short_url'].endswith(f'/{ALIAS}')

    # Clean up
    short_url = data['short_url']
    short_code = short_url.rstrip('/').split('/')[-1]

    delete_response = client.delete(
        f'/admin/db/{short_code}',
        headers={'X-API-Key': API_KEY}
    )
    assert delete_response.status_code == 200


def test_shorten_alias_taken(client):
    """/shorten valid request but alias already taken."""
    ALIAS = "test_alias"
    client.delete(f'/admin/db/{ALIAS}', headers={'X-API-Key': API_KEY})
    
    response = client.post(
        '/shorten',
        json={'url': 'https://example.com', 'expiration_date': get_future_expiration(),
              'alias': ALIAS},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'short_url' in data
    assert data['short_url'].endswith(f'/{ALIAS}')

    response = client.post(
        '/shorten',
        json={'url': 'https://example.com', 'expiration_date': get_future_expiration(),
              'alias': ALIAS},
    )
    assert response.status_code == 400

    # Clean up
    short_url = data['short_url']
    short_code = short_url.rstrip('/').split('/')[-1]

    delete_response = client.delete(
        f'/admin/db/{short_code}',
        headers={'X-API-Key': API_KEY}
    )
    assert delete_response.status_code == 200


def test_shorten_alias_length(client):
    """/shorten valid request but alias too long / too short."""
    response = client.post(
        '/shorten',
        json={'url': 'https://example.com', 'expiration_date': get_future_expiration(),
              'alias': 'test_alias_but_too_long'},
    )
    assert response.status_code == 400
    response = client.post(
        '/shorten',
        json={'url': 'https://example.com', 'expiration_date': get_future_expiration(),
              'alias': 'test'},
    )
    assert response.status_code == 400


def test_shorten_missing_url(client):
    """/shorten empty request."""
    response = client.post('/shorten', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_shorten_invalid_json(client):
    """/shorten invalid request."""
    response = client.post('/shorten', data='not-json',
                           content_type='application/json')
    assert response.status_code == 400


def test_redirect_existing_code(client):
    """/shorten valid request redirect."""
    response = client.post(
        '/shorten', json={'url': 'https://example.com', 'expiration_date': get_future_expiration()})
    short_url = response.get_json()['short_url']
    code = short_url.rsplit('/', 1)[-1]

    redirect = client.get(f'/{code}')
    assert redirect.status_code == 302
    assert redirect.location == 'https://example.com'


def test_get_stats(client):
    """/admin/db/stats valid request."""
    response = client.get('/admin/db/stats', headers={'X-API-Key': API_KEY})
    assert response.status_code == 200


def test_get_urls(client):
    """/admin/db/urls valid request."""
    response = client.get('/admin/db/urls', headers={'X-API-Key': API_KEY})
    assert response.status_code == 200
    response = client.get('/admin/db/urls?page=1&limit=10',
                           headers={'X-API-Key': API_KEY})
    assert response.status_code == 200
    response = client.get('/admin/db/urls?page=10&limit=10',
                           headers={'X-API-Key': API_KEY})
    assert response.status_code == 200


def test_get_url_by_code(client):
    """/admin/db/<short_code> valid request."""
    response = client.post(
        '/shorten', json={'url': 'https://example.com', 'expiration_date': get_future_expiration()}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'short_url' in data

    # Test
    short_url = data['short_url']
    short_code = short_url.rstrip('/').split('/')[-1]

    response = client.get(f'/admin/db/{short_code}', headers={'X-API-Key': API_KEY})
    assert response.status_code == 200

    # Clean up
    delete_response = client.delete(
        f'/admin/db/{short_code}',
        headers={'X-API-Key': API_KEY}
    )
    assert delete_response.status_code == 200


def test_get_urls_by_url_query(client):
    """Test searching URLs by a partial match via /admin/db."""
    # Create a short URL entry
    test_url = 'https://example.com'
    response = client.post(
        '/shorten',
        json={'url': test_url, 'expiration_date': get_future_expiration()}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'short_url' in data

    # Extract short code for later cleanup
    short_url = data['short_url']
    short_code = short_url.rstrip('/').split('/')[-1]

    # Query the DB using a substring of the original URL
    query_term = 'example'
    response = client.get(
        f'/admin/db?query={query_term}',
        headers={'X-API-Key': API_KEY}
    )
    assert response.status_code == 200
    results = response.get_json()
    assert any(query_term in entry['original_url'] for entry in results)

    # Clean up the test entry
    delete_response = client.delete(
        f'/admin/db/{short_code}',
        headers={'X-API-Key': API_KEY}
    )
    assert delete_response.status_code == 200


def test_get_urls_by_url_query_missing(client):
    """/admin/db query missing."""
    response = client.get('/admin/db', headers={'X-API-Key': API_KEY})
    assert response.status_code == 400


def test_delete_short_code_nonexistent(client):
    """/admin/db/<short_code> where short code does not exist."""
    delete_response = client.delete(
        '/admin/db/non_existent_code',
        headers={'X-API-Key': API_KEY}
    )
    assert delete_response.status_code == 404


def test_delete_old_short_codes(client):
    """/admin/db/<int> valid request.  
    * if there are other entries in the DB these entries will not be the ones deleted."""
    NUM_TO_DELETE = 3
    created_short_codes = []

    # Create multiple short code entries and track the short codes
    for i in range(NUM_TO_DELETE):
        response = client.post(
            '/shorten',
            json={'url': f'https://example.com/delete-test-{i}'}
        )
        assert response.status_code == 200
        data = response.get_json()
        short_url = data['short_url']
        short_code = short_url.rstrip('/').split('/')[-1]
        created_short_codes.append(short_code)

    # Delete the X most recent
    delete_response = client.delete(
        f'/admin/db/{NUM_TO_DELETE}', 
        headers={'X-API-Key': API_KEY}
    )
    assert delete_response.status_code == 200
    data = delete_response.get_json()
    assert data['message'].startswith(f'Deleted {NUM_TO_DELETE}')
    assert len(data['short_codes']) == NUM_TO_DELETE
