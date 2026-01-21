"""
Protocol definitions for HTTP client and transport operations.
These protocols define the interface contracts for network communication with the Hue bridge.
"""

from typing import Any, Dict, Optional, Protocol

from zeroconf import ServiceStateChange
from pyhuec.models.dto import (
    ApiResponseDTO,
    ErrorResponseDTO,
)


class HttpClientProtocol(Protocol):
    """Protocol for HTTP client operations."""
    
    async def get(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None
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


class EventClientProtocol(Protocol):
    """Protocol for Server-Sent Events (SSE) client operations."""
    
    async def connect(self, endpoint: str) -> None:
        """
        Connect to SSE endpoint.
        
        Args:
            endpoint: SSE endpoint path
        """
        ...
    
    async def disconnect(self) -> None:
        """
        Disconnect from SSE endpoint.
        """
        ...
    
    async def listen(self) -> Any:
        """
        Listen for incoming events.
        
        Yields:
            Event data from the stream
        """
        ...
    
    def is_connected(self) -> bool:
        """
        Check if connected to event stream.
        
        Returns:
            True if connected
        """
        ...


class MdnsClientProtocol(Protocol):
    """Protocol for mDNS (multicast DNS) service discovery."""
    
    def _handler(self,
        zeroconf,
        service_type: str,
        name: str,
        state_change: ServiceStateChange,
    ) -> None:
        """
        Handler for service discovery over mDNS.
        
        Args:
            service_type: mDNS service type to discover
            timeout: Discovery timeout in seconds
            
        Returns:
            List of discovered services with addresses and ports
        """
        ...
        
    async def discover_services(
        self,
        service_type: str = "_hue._tcp.local.",
        timeout: float = 5.0,
    ) -> list[Dict[str, Any]]:
        """
        Discover services using mDNS.
        
        Args:
            service_type: mDNS service type to discover
            timeout: Discovery timeout in seconds
            
        Returns:
            List of discovered services with addresses and ports
        """
        ...
    
    async def resolve_hostname(self, hostname: str) -> Optional[str]:
        """
        Resolve hostname to IP address using mDNS.
        
        Args:
            hostname: Hostname to resolve
            
        Returns:
            IP address or None if not found
        """
        ...


class ApiClientProtocol(Protocol):
    """Protocol for high-level API client operations."""
    
    async def initialize(self, bridge_ip: str, app_key: str) -> None:
        """
        Initialize API client with bridge connection.
        
        Args:
            bridge_ip: IP address of the bridge
            app_key: Application key for authentication
        """
        ...
    
    async def close(self) -> None:
        """
        Close API client and cleanup resources.
        """
        ...
    
    async def health_check(self) -> bool:
        """
        Check if the bridge is reachable and responsive.
        
        Returns:
            True if bridge is healthy
        """
        ...
    
    async def validate_response(self, response: Dict[str, Any]) -> bool:
        """
        Validate API response for errors.
        
        Args:
            response: API response dictionary
            
        Returns:
            True if response is valid (no errors)
        """
        ...
    
    def get_base_url(self) -> str:
        """
        Get the configured base URL.
        
        Returns:
            Base URL string
        """
        ...


class RateLimiterProtocol(Protocol):
    """Protocol for API rate limiting."""
    
    async def acquire(self) -> None:
        """
        Acquire permission to make an API request.
        Blocks if rate limit is exceeded.
        """
        ...
    
    def get_rate_limit(self) -> int:
        """
        Get current rate limit (requests per second).
        
        Returns:
            Rate limit value
        """
        ...
    
    def set_rate_limit(self, rate: int) -> None:
        """
        Set rate limit for API requests.
        
        Args:
            rate: Maximum requests per second
        """
        ...
    
    def reset(self) -> None:
        """
        Reset rate limiter state.
        """
        ...


class CacheProtocol(Protocol):
    """Protocol for API response caching."""
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get cached value by key.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        ...
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[float] = None,
    ) -> None:
        """
        Set cached value with optional TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
        """
        ...
    
    async def delete(self, key: str) -> None:
        """
        Delete cached value.
        
        Args:
            key: Cache key
        """
        ...
    
    async def clear(self) -> None:
        """
        Clear all cached values.
        """
        ...
    
    def is_enabled(self) -> bool:
        """
        Check if caching is enabled.
        
        Returns:
            True if caching is enabled
        """
        ...
