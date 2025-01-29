"""
decorators.py
-------------
Provides decorators for function tracing, auditing, etc., with optional PII masking,
tamper-proof hashing, correlation IDs, etc.
"""

import time
import re
from functools import wraps
from typing import Any
from .trace_manager import TraceManager, TraceEvent
from .config import PII_PATTERNS, PII_REPLACEMENTS
from .config import LOGGER
from .utils.hashing import sign_event
from .config import DEFAULT_SECRET_KEY

def mask_pii(value: Any):
    """
    Basic PII masking. Extend as needed for complex data structures.
    """
    if isinstance(value, str):
        for k, pattern in PII_PATTERNS.items():
            replacement = PII_REPLACEMENTS.get(k, "[REDACTED]")
            value = re.sub(pattern, replacement, value)
        return value
    elif isinstance(value, (list, tuple)):
        return [mask_pii(v) for v in value]
    elif isinstance(value, dict):
        return {k: mask_pii(v) for k, v in value.items()}
    return value

def trace(func):
    """
    A simple decorator that traces function calls (with optional PII masking).
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        masked_args = mask_pii(args)
        masked_kwargs = mask_pii(kwargs)

        event = TraceEvent(
            event_type="function_call",
            function_name=func.__name__,
            timestamp=start_time,
            duration=end_time - start_time,
            meta={
                "args": masked_args,
                "kwargs": masked_kwargs
            }
        )
        TraceManager().record_event(event)
        return result
    return wrapper

def audit(func):
    """
    A specialized decorator for auditing critical functions.
    Automatically signs the event data for tamper-proof logs.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        masked_args = mask_pii(args)
        masked_kwargs = mask_pii(kwargs)

        event_data = {
            "event_type": "audit_call",
            "function_name": func.__name__,
            "timestamp": start_time,
            "duration": end_time - start_time,
            "args": masked_args,
            "kwargs": masked_kwargs
        }
        # Sign the event:
        signature = sign_event(event_data, DEFAULT_SECRET_KEY)

        event = TraceEvent(
            event_type="audit_call",
            function_name=func.__name__,
            timestamp=start_time,
            duration=end_time - start_time,
            meta={
                "args": masked_args,
                "kwargs": masked_kwargs,
                "signature": signature
            }
        )
        TraceManager().record_event(event)
        return result
    return wrapper
