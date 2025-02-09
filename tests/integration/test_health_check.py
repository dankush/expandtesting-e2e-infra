"""Integration tests for the Health Check endpoint."""
from http import HTTPStatus
from typing import Any

import pytest
from _pytest.fixtures import FixtureRequest

from core.api_client import APIClient


@pytest.fixture(scope="session")
def api_client(request: FixtureRequest) -> APIClient:
    """
    Fixture to provide configured API client.

    Args:
        request: Pytest fixture request object

    Returns:
        APIClient: Configured API client instance
    """
    config = request.config
    base_url = config.getoption("--base-url") or "https://practice.expandtesting.com/notes/api"
    return APIClient(base_url=base_url)


@pytest.mark.integration
def test_health_check_success(api_client: APIClient) -> None:
    """
    Test health check endpoint returns successful response.

    Test Steps:
        1. Send GET request to health-check endpoint
        2. Verify response status code is 200
        3. Verify response body contains expected data

    Expected Results:
        - Response status code is 200
        - Response indicates API is running
        - Response contains expected fields
    """
    # When
    response = api_client.health_check()
    response_data: dict[str, Any] = response.json()

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response_data["success"] is True
    assert response_data["status"] == HTTPStatus.OK
    assert response_data["message"] == "Notes API is Running"


@pytest.mark.integration
def test_health_check_response_time(api_client: APIClient) -> None:
    """
    Test health check endpoint response time is within acceptable limits.

    Test Steps:
        1. Send GET request to health-check endpoint
        2. Verify response time is under threshold

    Expected Results:
        - Response time is under 1 second
    """
    # When
    response = api_client.health_check()

    # Then
    assert response.elapsed.total_seconds() < 1.0, "Response time exceeded 1 second"


# Test data for different scenarios
@pytest.mark.parametrize(
    "headers, expected_status, expected_message",
    [
        # Happy path
        (
            {"accept": "application/json"},
            HTTPStatus.OK,
            "Notes API is Running"
        ),
        # Different accept headers
        (
            {"accept": "application/xml"},
            HTTPStatus.OK,
            "Notes API is Running"
        ),
        (
            {"accept": "*/*"},
            HTTPStatus.OK,
            "Notes API is Running"
        ),
        # Missing headers
        (
            {},
            HTTPStatus.OK,
            "Notes API is Running"
        ),
        # Additional headers
        (
            {
                "accept": "application/json",
                "x-custom-header": "test"
            },
            HTTPStatus.OK,
            "Notes API is Running"
        ),
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
    expected_message: str
) -> None:
    """
    Test health check endpoint with different header combinations.

    Args:
        api_client: API client fixture
        headers: Request headers to send
        expected_status: Expected HTTP status code
        expected_message: Expected response message
    """
    # When
    response = api_client.health_check(headers=headers)
    response_data: dict[str, Any] = response.json()

    # Then
    assert response.status_code == expected_status
    assert response_data["message"] == expected_message


@pytest.mark.parametrize(
    "timeout, expected_error",
    [
        (0.001, "Connection timed out"),  # Very short timeout
        (0.5, None),  # Normal timeout
        (1.0, None),  # Extended timeout
    ],
    ids=["short_timeout", "normal_timeout", "extended_timeout"]
)
def test_health_check_timeouts(
    api_client: APIClient,
    timeout: float,
    expected_error: str | None
) -> None:
    """
    Test health check endpoint with different timeout settings.

    Args:
        api_client: API client fixture
        timeout: Request timeout in seconds
        expected_error: Expected error message or None for success
    """
    try:
        response = api_client.health_check(timeout=timeout)
        
        if expected_error is None:
            assert response.status_code == HTTPStatus.OK
        else:
            pytest.fail("Expected timeout error did not occur")
    except Exception as e:
        if expected_error is not None:
            assert expected_error in str(e)
        else:
            raise


@pytest.mark.parametrize(
    "method",
    ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    ids=lambda x: f"method_{x.lower()}"
)
def test_health_check_methods(api_client: APIClient, method: str) -> None:
    """
    Test health check endpoint with different HTTP methods.

    Args:
        api_client: API client fixture
        method: HTTP method to use
    """
    # When
    response = api_client.request(method=method, endpoint="/health-check")
    
    # Then
    if method == "GET":
        assert response.status_code == HTTPStatus.OK
    else:
        assert response.status_code in [
            HTTPStatus.METHOD_NOT_ALLOWED,
            HTTPStatus.NOT_IMPLEMENTED
        ]