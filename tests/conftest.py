"""Global pytest configuration and fixtures."""
import pytest
from core.api_client import APIClient
from core.data_models import UserRegisterRequest
from typing import Dict, Any
from utils.data_generator import generate_random_email

@pytest.fixture(scope="session")
def authenticated_api_client() -> APIClient:
    """
    Fixture to provide an authenticated API client instance for the session.
    
    :return: An authenticated instance of APIClient.
    """
    client = APIClient(base_url)

    # Register a user
    register_data = UserRegisterRequest(
        name="test_user",
        email="test@example.com",
        password="password"
    )
    client.post("/users/register", data=register_data.model_dump())

    # Login the user
    client.login("test@example.com", "password")

    return client

@pytest.fixture(scope="session")
def base_url(pytestconfig) -> str:
    """
    Fixture to get the base URL from pytest configuration.
    
    :param pytestconfig: The pytest configuration object.
    :return: The base URL for the API.
    """
    return pytestconfig.getoption("--base-url")

def pytest_addoption(parser: pytest.Parser) -> None:
    """
    Add custom command line options for pytest.
    
    :param parser: The pytest parser object.
    """
    parser.addoption(
        "--base-url",
        action="store",
        default="https://practice.expandtesting.com/notes/api",
        help="Base URL for the API",
    )

@pytest.fixture
def api_client(base_url: str) -> APIClient:
    """
    Fixture to provide an API client instance.
    
    :param base_url: The base URL for the API.
    :return: An instance of APIClient.
    """
    return APIClient(base_url=base_url)

@pytest.fixture
def registration_data() -> Dict[str, Any]:
    """
    Fixture for generating valid registration data.
    
    :return: A dictionary containing valid registration data.
    """
    return {
        "name": "test_user",
        "email": generate_random_email(),
        "password": "ValidPassword123!"
    }