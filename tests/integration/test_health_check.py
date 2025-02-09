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