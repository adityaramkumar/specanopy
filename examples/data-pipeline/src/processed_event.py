# generated_from: contracts/schemas/processed
# spec_hash: aa16370c504b0bb024d13816449c4fa02a1383a6f8b296b1bb744bc743ac33db
# generated_at: 2026-03-15T02:31:00.526378+00:00
# agent: implementation-agent
from dataclasses import dataclass
from datetime import datetime
import uuid
from typing import Any, Dict

from pydantic import BaseModel, validator


class ProcessedEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp_utc: str
    date: str
    hour: int
    user_id: str
    is_anonymous: bool
    source: str
    properties: Dict[str, Any]

    @validator('event_id')
    def validate_event_id(cls, v):
        if not uuid.UUID(str(v), version=4):
            raise ValueError('event_id must be a valid UUID')
        return v

    @validator('timestamp_utc')
    def validate_timestamp_utc(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError('timestamp_utc must be valid ISO 8601 UTC')
        return v

    @validator('date')
    def validate_date(cls, v):
        if not (len(v) == 10 and v[4] == '-' and v[7] == '-'):
            raise ValueError('date must be YYYY-MM-DD format')
        return v

    @validator('hour')
    def validate_hour(cls, v):
        if not isinstance(v, int) or not 0 <= v <= 23:
            raise ValueError('hour must be integer between 0-23')
        return v

    class Config:
        extra = 'forbid'


def parse_processed_event(data: Dict[str, Any]) -> ProcessedEvent:
    """
    Parse and validate a dictionary into a ProcessedEvent.

    Args:
        data: Raw event data dictionary

    Returns:
        Validated ProcessedEvent object

    Raises:
        ValueError: If validation fails
    """
    return ProcessedEvent(**data)


def serialize_processed_event(event: ProcessedEvent) -> Dict[str, Any]:
    """
    Serialize ProcessedEvent to dictionary for JSON output.

    Args:
        event: ProcessedEvent to serialize

    Returns:
        Dictionary representation
    """
    return event.dict()
