from typing import Any, Dict, Optional

import httpx

from pyhuec.models import HttpClientProtocol


class HttpClient(HttpClientProtocol):
    """Protocol for HTTP client operations."""

    def __init__(
        self,
        base_url: str,
        client: httpx.AsyncClient = httpx.AsyncClient,
        timeout: float = 3.0,
        verify: bool = False,
    ):
        self.client = (
            client if client else httpx.AsyncClient(verify=verify, timeout=timeout)
        )
        self.base_url = base_url

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
        return self.client.get(
            url=f"{self.base_url}{endpoint}", params=params, headers=headers
        )

    async def post(
        self,
        endpoint: str,
        params: str,
        headers: Optional[Dict[str, Any]],
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
        return self.client.post(
            url=f"{self.base_url}{endpoint}", params=params, headers=headers, json=body
        )

    async def put(
        self,
        endpoint: str,
        params: str,
        headers: Optional[Dict[str, Any]],
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
        return self.client.put(
            url=f"{self.base_url}{endpoint}", params=params, headers=headers, json=body
        )

    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Perform HTTP DELETE request.

        Args:
            endpoint: API endpoint path

        Returns:
            Response data as dictionary
        """
        return self.client
