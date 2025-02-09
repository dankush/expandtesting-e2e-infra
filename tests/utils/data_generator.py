import random
import string

def generate_random_string(length: int = 10) -> str:
    """Generate a random string of specified length.

    Args:
        length (int): The length of the random string to generate. Default is 10.

    Returns:
        str: A random string composed of ASCII letters.
    """
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def generate_random_email() -> str:
    """Generate a random email address.

    Returns:
        str: A random email address in the format 'randomstring@example.com'.
    """
    return f"{generate_random_string()}@example.com"