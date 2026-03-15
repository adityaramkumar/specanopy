# generated_from: behaviors/ingest
# spec_hash: a46bf4c24197a3b855328de74eab6c7676c144c326dc88fd066bc5484a1f8221
# generated_at: 2026-03-15T02:32:11.592232+00:00
# agent: implementation-agent
from pydantic import BaseModel, validator
from typing import Dict, Any, Optional
import uuid
from datetime import datetime

class RawEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: str
    user_id: Optional[str] = None
    properties: Dict[str, Any]
    source: str

    @validator('event_id')
    def validate_event_id(cls, v):
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError('event_id must be a valid UUID')
        return v

    @validator('event_type')
    def validate_event_type(cls, v):
        allowed = {'page_view', 'click', 'purchase', 'signup'}
        if v not in allowed:
            raise ValueError(f'event_type must be one of {allowed}')
        return v

    @validator('timestamp')
    def validate_timestamp(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError('timestamp must be valid ISO 8601')
        return v

    @validator('source')
    def validate_source(cls, v):
        allowed = {'web', 'mobile', 'api'}
        if v not in allowed:
            raise ValueError(f'source must be one of {allowed}')
        return v

    @validator('properties')
    def validate_properties(cls, v):
        if not isinstance(v, dict):
            raise ValueError('properties must be a dict')
        return v

    class Config:
        extra = 'forbid'


def validate_raw_event(event_json: dict) -> tuple[RawEvent | None, str | None]:
    """
    Validate a raw event dict against the schema.

    Args:
        event_json: Dict representing a single event

    Returns:
        Tuple of (validated_event or None, error_message or None)

    Raises:
        None - validation errors returned via return value
    """
    try:
        return RawEvent(**event_json), None
    except Exception as e:
        return None, str(e)
