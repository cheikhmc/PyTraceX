"""
trace_manager.py
----------------
Manages trace/audit events. Supports correlation IDs, etc.
"""

import time
import json
import uuid
from typing import Any, Dict, List
from .config import TRACE_STORAGE, LOGGER
from .context import get_correlation_id

class TraceEvent:
    """
    Represents a single trace or audit event.
    """

    def __init__(
        self,
        event_type: str,
        function_name: str = "",
        timestamp: float = None,
        duration: float = 0.0,
        meta: Dict[str, Any] = None
    ):
        self.event_id = str(uuid.uuid4())
        self.event_type = event_type
        self.function_name = function_name
        self.timestamp = timestamp or time.time()
        self.duration = duration
        self.meta = meta or {}
        # Attach correlation ID automatically if present in context
        self.meta["correlation_id"] = get_correlation_id()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "function_name": self.function_name,
            "timestamp": self.timestamp,
            "duration": self.duration,
            "meta": self.meta
        }

    def __repr__(self):
        return f"<TraceEvent {self.event_id} ({self.event_type} - {self.function_name})>"


class TraceManager:
    """
    A singleton manager for storing/retrieving trace events.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TraceManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._storage = TRACE_STORAGE

    def record_event(self, event: TraceEvent):
        LOGGER.info(f"Recording event {event.event_id} ({event.event_type}).")
        self._storage.append(event.to_dict())

    def get_events(self) -> List[Dict[str, Any]]:
        return self._storage

    def clear_events(self):
        LOGGER.info("Clearing all trace events.")
        self._storage.clear()

    def to_json(self) -> str:
        return json.dumps(self._storage, indent=2)
