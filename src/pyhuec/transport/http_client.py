from typing import Any, Dict, Optional

import httpx

from pyhuec.models import HttpClientProtocol


class HttpClient(HttpClientProtocol):
    """Protocol for HTTP client operations."""

    def __init__(
        self,
        base_url: str,
        client: Optional[httpx.AsyncClient] = None,
        timeout: float = 10.0,
        verify: bool = False,
    ):
        if client is not None:
            self.client = client
        else:
            self.client = httpx.AsyncClient(
                verify=verify, timeout=httpx.Timeout(timeout), follow_redirects=True
            )
        self.base_url = base_url
        self._auth_token: Optional[str] = None
        self._timeout = timeout

    def set_base_url(self, base_url: str) -> None:
        """Set the base URL for API requests."""
        self.base_url = base_url

    def set_auth_token(self, token: str) -> None:
        """Set the authentication token for API requests."""
        self._auth_token = token

    def set_timeout(self, timeout: float) -> None:
        """Set the request timeout."""
        self._timeout = timeout

    def _get_headers(self, headers: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Build headers with auth token."""
        merged_headers = headers.copy() if headers else {}
        if self._auth_token:
            merged_headers["hue-application-key"] = self._auth_token
        return merged_headers

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Perform HTTP GET request.

        Args:
            endpoint: API endpoint path
            params: Optional query parameters

        Returns:
            Response data as dictionary
        """
        response = await self.client.get(
            url=f"{self.base_url}{endpoint}",
            params=params,
            headers=self._get_headers(headers),
        )
        return response.json()

    async def post(
        self,
        endpoint: str,
        params: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
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
        response = await self.client.post(
            url=f"{self.base_url}{endpoint}",
            params=params,
            headers=self._get_headers(headers),
            json=body,
        )
        return response.json()

    async def put(
        self,
        endpoint: str,
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[str] = None,
        body: Optional[Dict[str, Any]] = None,
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
        response = await self.client.put(
            url=f"{self.base_url}{endpoint}",
            params=params,
            headers=self._get_headers(headers),
            json=body,
        )
        return response.json()

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Perform HTTP DELETE request.

        Args:
            endpoint: API endpoint path

        Returns:
            Response data as dictionary
        """
        response = await self.client.delete(url=f"{self.base_url}{endpoint}")
        return response.json()
