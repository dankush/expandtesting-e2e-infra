"""End-to-end tests for the complete user and notes workflow."""
import pytest
from http import HTTPStatus
from typing import Dict, Any

from core.api_client import APIClient
from utils.data_generator import generate_random_email

@pytest.fixture
def test_user_data() -> Dict[str, Any]:
    """Fixture to generate unique test user data."""
    return {
        "name": "e2e_test_user",
        "email": generate_random_email(domain="test.com"),
        "password": "TestPassword123!"
    }

@pytest.fixture
def test_note_data() -> Dict[str, Any]:
    """Fixture to generate test note data."""
    return {
        "title": "E2E Test Note",
        "description": "This is a test note created during E2E testing",
        "category": "Work",
        "completed": False  # Added required field
    }

@pytest.mark.e2e
def test_complete_user_note_workflow(
    api_client: APIClient,
    test_user_data: Dict[str, Any],
    test_note_data: Dict[str, Any]
) -> None:
    """
    Test the complete user and note workflow.

    Steps:
    1. Register a new user
    2. Login with the registered user
    3. Create a new note
    4. Update the note
    5. Delete the note
    """
    # Step 1: Register new user
    register_response = api_client.post(
        endpoint="/users/register",
        data=test_user_data,
        content_type="form"
    )
    assert register_response.status_code == HTTPStatus.CREATED
    assert register_response.json()["success"] is True

    # Step 2: Login
    login_response = api_client.login(
        email=test_user_data["email"],
        password=test_user_data["password"]
    )
    assert "token" in login_response["data"]

    # Step 3: Create note
    create_response = api_client.post(
        endpoint="/notes",
        data=test_note_data
    )
    assert create_response.status_code == HTTPStatus.OK
    create_data = create_response.json()
    assert create_data["success"] is True
    note_id = create_data["data"]["id"]

    # Step 4: Update note
    updated_data = {
        "title": "Updated E2E Test Note",
        "description": test_note_data["description"],
        "category": "Personal",
        "completed": True
    }
    update_response = api_client.put(
        endpoint=f"/notes/{note_id}",
        data=updated_data
    )
    assert update_response.status_code == HTTPStatus.OK
    assert update_response.json()["success"] is True

    # Step 5: Delete note
    delete_response = api_client.delete(f"/notes/{note_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["success"] is True
