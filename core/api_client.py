from typing import Dict, Optional
import requests
from requests import Response
from .exceptions import APIError

class APIClient:
    """Client for interacting with the ExpandTesting API."""
    
    def __init__(self, base_url: str = "https://practice.expandtesting.com/notes/api"):
        """Initialize API client with base URL.
        
        Args:
            base_url (str): Base URL for the API
        """
        self.base_url = base_url
        self.session = requests.Session()
        
    def get_headers(self) -> Dict[str, str]:
        """Get default headers for API requests."""
        return {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        
    def health_check(self) -> Response:
        """Perform health check request.
        
        Returns:
            Response: Response object from the health check endpoint
        
        Raises:
            APIError: If the request fails
        """
        try:
            endpoint = f"{self.base_url}/health-check"
            response = self.session.get(
                url=endpoint,
                headers=self.get_headers()
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise APIError(
                message=f"Health check request failed: {str(e)}",
                status_code=getattr(e.response, 'status_code', None),
                response=getattr(e.response, 'text', None)
            ) from e

    def login(self, email, password):
        """Logs in and retrieves the authentication token."""
        endpoint = "/users/login"
        data = {"email": email, "password": password}
        response = requests.post(f"{self.base_url}{endpoint}", data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        response_json = response.json()
        if not response_json["success"]:
            raise APIError(response_json["message"])

        self.token = response_json["data"]["token"]  # Store the token
        return response_json

    def get(self, endpoint, params=None):
        """Generic GET request with authentication."""
        headers = {"x-auth-token": self.token} if self.token else {}
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None):
        """Generic POST request with authentication."""
        headers = {"x-auth-token": self.token} if self.token else {}
        response = requests.post(f"{self.base_url}{endpoint}", headers=headers, data=data)
        response.raise_for_status()
        return response.json()