# app/limiter.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import request, jsonify

limiter = Limiter(get_remote_address)

@limiter.request_filter
def exempt_internal_ips():
    """Skip rate limits for requests coming from localhost."""
    return request.remote_addr in ["127.0.0.1", "::1", "localhost"]


@limiter.error_handler
def rate_limit_exceeded(e):
    """Custom error response."""
    return jsonify({
        "error": "Rate limit exceeded",
        "message": "You've hit the limit. Please try again later.",
        "retry_after": e.description  # This provides Retry-After header info
    }), 429
