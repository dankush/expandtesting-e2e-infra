"""API Client module for making HTTP requests to the ExpandTesting API."""
from typing import Dict, Optional, Any, Union
from urllib.parse import urlencode
import json
import requests
from requests import Response, Session
from .exceptions import APIError

class APIClient:
    """Client for interacting with the ExpandTesting API.
    
    This class provides methods for making HTTP requests to the API endpoints
    with proper error handling, authentication, and response processing.
    """
    
    def __init__(
        self,
        base_url: str = "https://practice.expandtesting.com/notes/api",
        timeout: int = 30,
        verify_ssl: bool = True
    ) -> None:
        """Initialize API client.
        
        Args:
            base_url: Base URL for the API endpoints
            timeout: Default request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = Session()
        self._auth_token: Optional[str] = None

    @property
    def auth_token(self) -> Optional[str]:
        """Get the current authentication token."""
        return self._auth_token

    @property
    def default_headers(self) -> Dict[str, str]:
        """Get default headers for API requests."""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self._auth_token:
            headers["x-auth-token"] = self._auth_token
        return headers

    def _build_url(self, endpoint: str) -> str:
        """Build full URL for the API endpoint.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Full URL including base URL and endpoint
        """
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{endpoint}"

    def _handle_response(self, response: Response) -> Response:
        """Handle API response and raise appropriate exceptions.
        
        Args:
            response: Response object from request
            
        Returns:
            Response object if successful
            
        Raises:
            APIError: If response indicates an error
        """
        try:
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            error_data = {}
            try:
                error_data = response.json()
            except ValueError:
                pass
            
            raise APIError(
                message=error_data.get('message', str(e)),
                status_code=response.status_code,
                response=error_data
            ) from e

    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        content_type: str = "json"
    ) -> Response:
        """Make a generic request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request payload data
            params: Query parameters
            headers: Additional headers
            timeout: Request timeout override
            content_type: Content type for request (json/form)
            
        Returns:
            Response object
            
        Raises:
            APIError: If request fails
        """
        url = self._build_url(endpoint)
        request_headers = {**self.default_headers, **(headers or {})}
        
        if data and content_type == "form":
            request_headers["Content-Type"] = "application/x-www-form-urlencoded"
            processed_data = urlencode(data)
        elif data:
            processed_data = json.dumps(data)
        else:
            processed_data = None

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=request_headers,
                params=params,
                data=processed_data,
                timeout=timeout or self.timeout,
                verify=self.verify_ssl
            )
            return self._handle_response(response)
        except requests.RequestException as e:
            raise APIError(
                message=f"Request failed: {str(e)}",
                status_code=getattr(e.response, 'status_code', None),
                response=getattr(e.response, 'text', None)
            ) from e

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate user and store token.
        
        Args:
            email: User's email
            password: User's password
            
        Returns:
            Response data containing authentication token
            
        Raises:
            APIError: If authentication fails
        """
        response = self.request(
            method="POST",
            endpoint="/users/login",
            data={"email": email, "password": password},
            content_type="form"
        )
        
        data = response.json()
        if data.get("success"):
            self._auth_token = data["data"]["token"]
        return data

    def health_check(self, headers: Optional[Dict[str, str]] = None) -> Response:
        """Check API health status.
        
        Args:
            headers (Optional[Dict[str, str]]): Optional headers to include in the request.
        
        Returns:
            Response: Response object containing health status
            
        Raises:
            APIError: If health check fails
        """# For debugging purposes
        # Pass the headers to the request method
        return self.request(method="GET", endpoint="/health-check", headers=headers)

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Response:
        """Send GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            **kwargs: Additional request parameters
            
        Returns:
            Response object
        """
        return self.request(method="GET", endpoint=endpoint, params=params, **kwargs)

    def post(
        self,
        endpoint: str,
        data: Dict[str, Any],
        content_type: str = "json",
        **kwargs: Any
    ) -> Response:
        """Send POST request.
        
        Args:
            endpoint: API endpoint
            data: Request payload
            content_type: Content type (json/form)
            **kwargs: Additional request parameters
            
        Returns:
            Response object
        """
        return self.request(
            method="POST",
            endpoint=endpoint,
            data=data,
            content_type=content_type,
            **kwargs
        )

    def put(
        self,
        endpoint: str,
        data: Dict[str, Any],
        **kwargs: Any
    ) -> Response:
        """Send PUT request.
        
        Args:
            endpoint: API endpoint
            data: Request payload
            **kwargs: Additional request parameters
        
        Returns:
            Response object
        """
        return self.request(
            method="PUT",
            endpoint=endpoint,
            data=data,
            **kwargs
        )

    def delete(
        self,
        endpoint: str,
        **kwargs: Any
    ) -> Response:
        """Send DELETE request.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional request parameters
        
        Returns:
            Response object
        """
        return self.request(
            method="DELETE",
            endpoint=endpoint,
            **kwargs
        )