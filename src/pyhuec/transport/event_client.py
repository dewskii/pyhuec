from typing import Any
from pyhuec.models import EventClientProtocol


class EventClient(EventClientProtocol):
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