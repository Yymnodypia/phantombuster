"""
Global exceptions for the PhantomBuster SDK.
"""

class PhantomBusterAPIError(Exception):
    """Base exception for all PhantomBuster API errors."""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code

class AuthenticationError(PhantomBusterAPIError):
    """Raised for 401 authentication errors."""
    pass

class NotFoundError(PhantomBusterAPIError):
    """Raised for 404 not found errors."""
    pass

class RateLimitError(PhantomBusterAPIError):
    """Raised for 429 rate limit errors."""
    pass

class ServerError(PhantomBusterAPIError):
    """Raised for 5xx server errors."""
    pass
