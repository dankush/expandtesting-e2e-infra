"""Global pytest configuration and fixtures."""
import pytest
from core.api_client import APIClient
from core.data_models import UserRegisterRequest

@pytest.fixture(scope="session")
def authenticated_api_client(base_url):  # Assuming base_url fixture is defined
    client = APIClient(base_url)

    # Register a user
    register_data = UserRegisterRequest(name="test_user", email="test@example.com", password="password")
    client.post("/users/register", data=register_data.model_dump())

    # Login the user
    client.login("test@example.com", "password")

    return client

def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command line options."""
    parser.addoption(
        "--base-url",
        action="store",
        default="https://practice.expandtesting.com/notes/api",
        help="Base URL for the API",
    )