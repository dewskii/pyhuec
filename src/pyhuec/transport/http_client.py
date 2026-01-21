from typing import Any, Dict, Optional

from pyhuec.models import HttpClientProtocol


class HttpClient(HttpClientProtocol):
    """Protocol for HTTP client operations."""

    async def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform HTTP GET request.

        Args:
            endpoint: API endpoint path
            params: Optional query parameters

        Returns:
            Response data as dictionary
        """
        ...

    async def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Perform HTTP POST request.

        Args:
            endpoint: API endpoint path
            data: Optional form data
            json: Optional JSON body

        Returns:
            Response data as dictionary
        """
        ...

    async def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Perform HTTP PUT request.

        Args:
            endpoint: API endpoint path
            data: Optional form data
            json: Optional JSON body

        Returns:
            Response data as dictionary
        """
        ...

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Perform HTTP DELETE request.

        Args:
            endpoint: API endpoint path

        Returns:
            Response data as dictionary
        """
        ...

    async def request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Perform generic HTTP request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional request parameters

        Returns:
            Response data as dictionary
        """
        ...

    def set_base_url(self, base_url: str) -> None:
        """
        Set the base URL for all requests.

        Args:
            base_url: Base URL (e.g., https://192.168.1.100)
        """
        ...

    def set_auth_token(self, token: str) -> None:
        """
        Set authentication token for requests.

        Args:
            token: Authentication token/app key
        """
        ...

    def set_timeout(self, timeout: float) -> None:
        """
        Set request timeout.

        Args:
            timeout: Timeout in seconds
        """
        ...
