from http import HTTPStatus
import pytest

# Import your APIClient from your project.
from core.api_client import APIClient


@pytest.mark.integration
def test_user_profile_security_missing_token(api_client: APIClient) -> None:
    """
    Verify that accessing the user profile endpoint without an authentication token
    results in an Unauthorized (401) response.

    Test Steps:
        1. Clear the x-auth-token by setting the underlying _auth_token attribute to None.
        2. Send a GET request to the /users/profile endpoint.
        3. Verify that the response status code is 401.
    """
    # Save the original token to restore later.
    original_token = api_client._auth_token  # accessing the internal attribute

    # Remove the token to simulate a missing authentication scenario.
    api_client._auth_token = None

    try:
        # When: Attempt to retrieve the user profile without token.
        response = api_client.get("/users/profile")

        # Then: Verify that access is denied.
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            f"Expected status code {HTTPStatus.UNAUTHORIZED} but got {response.status_code}"
        )
    finally:
        # Restore the original token to prevent side effects on other tests.
        api_client._auth_token = original_token