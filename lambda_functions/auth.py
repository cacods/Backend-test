MOCK_TOKENS = {
    "mock-user-1-token": {"user_id": "test-user-1", "name": "Alice"},
    "mock-user-2-token": {"user_id": "test-user-2", "name": "Bob"},
}


class InvalidTokenException(Exception):
    """Custom exception for invalid token errors."""


def validate_token(token):
    """Mock JWT validation - returns user claims if token is 'valid'."""
    if not token or not token.startswith("Bearer "):
        raise InvalidTokenException("Unauthorized")

    user = MOCK_TOKENS.get(token.replace("Bearer ", "").strip())
    if not user:
        raise InvalidTokenException("Unauthorized")
