"""
Event DTOs for Hue API v2 event stream.
Based on: https://developers.meethue.com/develop/hue-api-v2/api-reference/
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class OnDTO(BaseModel):
    """On/off state."""

    on: bool


class DimmingDTO(BaseModel):
    """Dimming/brightness state."""

    brightness: float = Field(ge=0.0, le=100.0)


class ResourceIdentifierDTO(BaseModel):
    """Reference to another resource by ID and type."""

    rid: str
    rtype: str


class EventType(str, Enum):
    """Types of events from Hue Bridge."""

    UPDATE = "update"
    ADD = "add"
    DELETE = "delete"
    ERROR = "error"


class ResourceType(str, Enum):
    """Resource types that can emit events."""

    LIGHT = "light"
    GROUPED_LIGHT = "grouped_light"
    ROOM = "room"
    ZONE = "zone"
    SCENE = "scene"
    DEVICE = "device"
    BRIDGE = "bridge"
    BRIDGE_HOME = "bridge_home"
    BUTTON = "button"
    MOTION = "motion"
    TEMPERATURE = "temperature"
    LIGHT_LEVEL = "light_level"
    ENTERTAINMENT = "entertainment"
    ENTERTAINMENT_CONFIGURATION = "entertainment_configuration"
    BEHAVIOR_INSTANCE = "behavior_instance"
    BEHAVIOR_SCRIPT = "behavior_script"
    GEOFENCE = "geofence"
    GEOFENCE_CLIENT = "geofence_client"
    GEOLOCATION = "geolocation"


class EventDataDTO(BaseModel):
    """Data payload within an event."""

    id: str = Field(description="Resource UUID")
    id_v1: Optional[str] = Field(None, description="Legacy v1 API ID")
    type: ResourceType = Field(description="Type of resource")

    owner: Optional[ResourceIdentifierDTO] = Field(
        None, description="Owner resource reference"
    )

    on: Optional[OnDTO] = Field(None, description="On/off state")
    dimming: Optional[DimmingDTO] = Field(None, description="Brightness state")

    service_id: Optional[int] = Field(None, description="Service identifier")

    model_config = ConfigDict(extra="allow")


class EventDTO(BaseModel):
    """Individual event from the event stream."""

    creationtime: datetime = Field(description="When the event was created")
    id: str = Field(description="Event UUID")
    type: EventType = Field(description="Type of event")
    data: List[EventDataDTO] = Field(
        description="List of affected resources in this event"
    )


class EventStreamMessageDTO(BaseModel):
    """Completemessage containing multiple events."""

    id: Optional[str] = Field(None, description="SSE message ID")
    data: List[EventDTO] = Field(description="List of events in this message")
    timestamp: Optional[datetime] = Field(
        None, description="When this message was received"
    )


class InternalEventDTO(BaseModel):
    """
    Internal event for application-level event handling.
    This represents processed events ready for consumption by application logic.
    """

    event_id: str = Field(description="Unique event identifier")
    event_type: EventType = Field(description="Type of event")
    resource_type: ResourceType = Field(description="Resource that changed")
    resource_id: str = Field(description="ID of the resource that changed")
    timestamp: datetime = Field(description="When the event occurred")
    data: EventDataDTO = Field(description="Event payload data")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class EventFilterDTO(BaseModel):
    """Filter criteria for event subscription."""

    event_types: Optional[List[EventType]] = Field(
        None, description="Filter by event types"
    )
    resource_types: Optional[List[ResourceType]] = Field(
        None, description="Filter by resource types"
    )
    resource_ids: Optional[List[str]] = Field(
        None, description="Filter by specific resource IDs"
    )


class EventSubscriptionDTO(BaseModel):
    """Event subscription configuration."""

    subscription_id: str = Field(description="Unique subscription identifier")
    filter: Optional[EventFilterDTO] = Field(None, description="Event filter criteria")
    active: bool = Field(default=True, description="Whether subscription is active")
