"""Integration tests for User Registration endpoint."""
import pytest
from http import HTTPStatus
from typing import Any, Dict
from core.api_client import APIClient
from core.exceptions import APIError
from utils.data_generator import generate_random_email

@pytest.fixture
def registration_data() -> Dict[str, Any]:
    """Fixture for generating valid registration data."""
    return {
        "name": "test_user",
        "email": generate_random_email(),
        "password": "ValidPassword123!"
    }

@pytest.mark.integration
@pytest.mark.parametrize(
    "test_data, expected_status, expected_message",
    [
        (
            {
                "name": "test_user",
                "email": generate_random_email(),
                "password": "ValidPass123!"
            },
            HTTPStatus.CREATED,
            "User account created successfully"
        ),
        (
            {
                "name": "test_user",
                "email": "a@a.com",
                "password": "short"
            },
            HTTPStatus.BAD_REQUEST,
            "Password must be between 6 and 30 characters"
        ),
        (
            {
                "name": "test_user",
                "email": "invalid-email",
                "password": "ValidPass123!"
            },
            HTTPStatus.BAD_REQUEST,
            "A valid email address is required"
        ),
    ],
    ids=[
        "valid_registration",
        "invalid_password_length",
        "invalid_email_format"
    ]
)
def test_user_registration(
    api_client: APIClient,
    test_data: Dict[str, Any],
    expected_status: HTTPStatus,
    expected_message: str
) -> None:
    """Test user registration with various scenarios."""
    try:
        response = api_client.post(
            endpoint="/users/register",
            data=test_data,
            content_type="form"
        )
        
        # For successful registration
        assert response.status_code == expected_status
        response_data = response.json()
        assert response_data["message"] == expected_message
        
    except APIError as e:
        # For error cases
        assert e.status_code == expected_status
        assert expected_message in str(e)

@pytest.mark.integration
def test_duplicate_registration(
    api_client: APIClient,
    registration_data: Dict[str, Any]
) -> None:
    """Test registration with duplicate email address."""
    # First registration should succeed
    try:
        response = api_client.post(
            endpoint="/users/register",
            data=registration_data,
            content_type="form"
        )
        assert response.status_code == HTTPStatus.CREATED
        
        # Second registration with same email should fail
        with pytest.raises(APIError) as exc_info:
            api_client.post(
                endpoint="/users/register",
                data=registration_data,
                content_type="form"
            )
        
        # Verify error details
        assert exc_info.value.status_code == HTTPStatus.CONFLICT
        assert "An account already exists with the same email address" in str(exc_info.value)
        
    except APIError as e:
        pytest.fail(f"First registration should succeed but failed with: {str(e)}")