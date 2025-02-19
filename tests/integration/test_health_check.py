"""Integration tests for the Health Check endpoint."""

from http import HTTPStatus
from typing import Any

import pytest

# Import your APIClient from your project.
# Ensure that APIClient implements the methods used in these tests.
from core.api_client import APIClient


@pytest.fixture(scope="session")
def api_client(pytestconfig) -> APIClient:
    """
    Fixture to provide a configured API client instance.

    Args:
        pytestconfig: Pytest configuration object.

    Returns:
        APIClient: Configured API client instance.
    """
    base_url = pytestconfig.getoption("--base-url") or "https://practice.expandtesting.com/notes/api"
    client = APIClient(base_url=base_url)
    print("APIClient instantiated:", client)
    return client


@pytest.mark.integration
def test_health_check_success(api_client: APIClient) -> None:
    """
    Verify that the health check endpoint returns a successful response.

    Test Steps:
        1. Send a GET request to the health-check endpoint.
        2. Verify that the response status code is 200.
        3. Verify that the response JSON contains the expected success fields.

    Expected Results:
        - The response status code is 200.
        - The response JSON includes 'success': True, 'status': 200,
          and 'message': "Notes API is Running".
    """
    # When
    response = api_client.health_check()
    response_data: dict[str, Any] = response.json()

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response_data.get("success") is True
    assert response_data.get("status") == HTTPStatus.OK
    assert response_data.get("message") == "Notes API is Running"


@pytest.mark.integration
def test_health_check_response_time(api_client: APIClient) -> None:
    """
    Verify that the health check endpoint responds within acceptable time limits.

    Test Steps:
        1. Send a GET request to the health-check endpoint.
        2. Verify that the response time is below 1 second.

    Expected Results:
        - The response time is less than 1.0 seconds.
    """
    # When
    response = api_client.health_check()

    # Then
    assert response.elapsed.total_seconds() < 1.0, "Response time exceeded 1 second"


@pytest.mark.integration
@pytest.mark.parametrize(
    "headers, expected_status, expected_message",
    [
        ({"accept": "application/json"}, HTTPStatus.OK, "Notes API is Running"),
        ({"accept": "application/xml"}, HTTPStatus.OK, "Notes API is Running"),
        ({"accept": "*/*"}, HTTPStatus.OK, "Notes API is Running"),
        ({}, HTTPStatus.OK, "Notes API is Running"),
        ({"accept": "application/json", "x-custom-header": "test"}, HTTPStatus.OK, "Notes API is Running"),
    ],
    ids=[
        "happy_path",
        "xml_accept_header",
        "any_accept_header",
        "no_headers",
        "additional_headers"
    ]
)
def test_health_check_with_headers(
    api_client: APIClient,
    headers: dict[str, str],
    expected_status: HTTPStatus,
    expected_message: str,
) -> None:
    """
    Verify the health check endpoint behavior with various header configurations.

    Args:
        api_client: The API client fixture.
        headers: Request headers to send.
        expected_status: Expected HTTP status code.
        expected_message: Expected response message.
    """
    # When
    response = api_client.health_check(headers=headers)
    response_data: dict[str, Any] = response.json()

    # Then
    assert response.status_code == expected_status
    assert response_data.get("message") == expected_message


@pytest.mark.integration
@pytest.mark.parametrize(
    "timeout, expected_error",
    [
        (0.001, "Connection timed out"),  # Very short timeout should trigger an error.
        (0.5, None),  # Normal timeout should work.
        (1.0, None),  # Extended timeout should work.
    ],
    ids=["short_timeout", "normal_timeout", "extended_timeout"]
)
def test_health_check_timeouts(
    api_client: APIClient,
    timeout: float,
    expected_error: str | None,
) -> None:
    """
    Verify the health check endpoint under various timeout settings.

    Args:
        api_client: The API client fixture.
        timeout: The timeout value (in seconds) for the request.
        expected_error: Expected error message if a timeout is anticipated; otherwise, None.
    """
    try:
        response = api_client.health_check(timeout=timeout)
        if expected_error is None:
            assert response.status_code == HTTPStatus.OK
        else:
            pytest.fail("Expected a timeout error, but the request succeeded.")
    except Exception as exc:
        if expected_error is not None:
            assert expected_error in str(exc)
        else:
            raise


@pytest.mark.integration
@pytest.mark.parametrize(
    "method",
    ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    ids=lambda m: f"method_{m.lower()}"
)
def test_health_check_methods(api_client: APIClient, method: str) -> None:
    """
    Verify the health check endpoint's behavior with different HTTP methods.

    Args:
        api_client: The API client fixture.
        method: The HTTP method to use.
    """
    # When
    response = api_client.request(method=method, endpoint="/health-check")

    # Then: Only GET should succeed, while other methods may not be allowed or implemented.
    if method == "GET":
        assert response.status_code == HTTPStatus.OK
    else:
        assert response.status_code in (HTTPStatus.METHOD_NOT_ALLOWED, HTTPStatus.NOT_IMPLEMENTED)