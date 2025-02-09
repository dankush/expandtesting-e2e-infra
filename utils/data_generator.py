"""Utility functions for generating test data."""
import random
import string
from typing import Optional

def generate_random_string(length: int = 10) -> str:
    """Generate a random string of specified length."""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def generate_random_email(domain: Optional[str] = None) -> str:
    """Generate a random email address."""
    if domain is None:
        domain = "example.com"
    return f"{generate_random_string()}@{domain}" 