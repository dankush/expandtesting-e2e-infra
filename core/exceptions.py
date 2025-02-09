"""Custom exceptions for the automation framework."""

class AutomationError(Exception):
    """Base exception for all automation framework errors."""
    pass

class APIError(AutomationError):
    """Raised when API requests fail."""
    def __init__(self, message: str, status_code: int | None = None, response: str | None = None):
        self.status_code = status_code
        self.response = response
        super().__init__(message) 