# generated_from: contracts/schemas/raw-events
# spec_hash: 85ff15643dade015b7da1836a539898f4bf3ba1c18eca0ca704255f3b1f21ad3
# generated_at: 2026-03-15T02:31:17.888575+00:00
# agent: implementation-agent
from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional
import uuid
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    PAGE_VIEW = "page_view"
    CLICK = "click"
    PURCHASE = "purchase"
    SIGNUP = "signup"


class Source(str, Enum):
    WEB = "web"
    MOBILE = "mobile"
    API = "api"


class RawEvent(BaseModel):
    event_id: str = Field(..., description="UUID string")
    event_type: EventType
    timestamp: str = Field(..., description="ISO 8601 datetime string")
    user_id: Optional[str] = Field(None, description="UUID string, nullable")
    properties: Dict[str, Any] = Field(..., description="Arbitrary key-value pairs")
    source: Source

    @validator('event_id')
    def validate_event_id(cls, v):
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError('event_id must be a valid UUID')
        return v

    @validator('timestamp')
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError('timestamp must be valid ISO 8601 format')
        return v

    @validator('properties')
    def validate_properties(cls, v):
        if not isinstance(v, dict):
            raise ValueError('properties must be a dictionary')
        return v

    class Config:
        extra = 'forbid'


def validate_raw_event(event_dict: Dict[str, Any]) -> RawEvent:
    """
    Validate a raw event dictionary and return a validated RawEvent model.

    Args:
        event_dict: Dictionary representing a single raw event

    Returns:
        RawEvent: Validated event model

    Raises:
        ValueError: If validation fails for any field
    """
    return RawEvent(**event_dict)


def validate_ndjson_events(ndjson_data: str) -> list[RawEvent]:
    """
    Parse and validate newline-delimited JSON events.

    Args:
        ndjson_data: String containing NDJSON events (one per line)

    Returns:
        list[RawEvent]: List of successfully validated events

    Raises:
        ValueError: If NDJSON parsing or individual event validation fails
    """
    validated_events = []
    lines = ndjson_data.strip().split('\n')
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            raise ValueError(f'Empty line at position {line_num}')
        try:
            event_dict = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f'JSON parsing failed at line {line_num}: {str(e)}')
        try:
            validated_event = validate_raw_event(event_dict)
            validated_events.append(validated_event)
        except ValueError as e:
            raise ValueError(f'Event validation failed at line {line_num}: {str(e)}')
    return validated_events