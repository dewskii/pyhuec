"""
Bridge DTOs for Hue API v2 requests and responses.
Based on: https://developers.meethue.com/develop/hue-api-v2/api-reference/
"""

from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class BridgeConfigDTO(BaseModel):
    """Bridge configuration information."""

    name: str
    swversion: str
    apiversion: str
    mac: str
    bridgeid: str
    factorynew: bool
    replacesbridgeid: Optional[str] = None
    modelid: str
    datastoreversion: str
    starterkit_id: str


class BridgeResponseDTO(BaseModel):
    """Bridge resource response."""

    model_config = ConfigDict(extra="allow")

    id: str
    bridge_id: str
    time_zone: Dict[str, str]
    type: str = Field(default="bridge")
