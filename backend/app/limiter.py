from redis import Redis
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
from flask import request, jsonify
from config import Config

limiter = Limiter(get_remote_address, storage_uri=Config.REDIS_URL)


@limiter.request_filter
def exempt_internal_ips():
    """Skip rate limits for requests coming from localhost."""
    return request.remote_addr in ["127.0.0.1", "::1", "localhost"]


def register_error_handlers(app):
    """Custom error response."""
    @app.errorhandler(RateLimitExceeded)
    def ratelimit_handler(e):
        return jsonify({"error": "Too many requests have been sent. Please wait before sending more."}), 429
