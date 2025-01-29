import pytest
from pytracex.trace_manager import TraceManager
from pytracex.decorators import trace, audit
from pytracex.config import DEFAULT_SECRET_KEY
from pytracex.utils.hashing import verify_signature

@trace
def sample_func(x, y):
    return x + y

@audit
def critical_func(amount):
    return f"Processed {amount}"

def test_trace_decorator():
    manager = TraceManager()
    manager.clear_events()

    assert sample_func(2, 3) == 5
    events = manager.get_events()
    assert len(events) == 1
    e = events[0]
    assert e["function_name"] == "sample_func"
    assert e["event_type"] == "function_call"
    assert e["meta"]["args"] == [2, 3]

def test_audit_decorator():
    manager = TraceManager()
    manager.clear_events()

    msg = critical_func(100)
    assert msg == "Processed 100"

    events = manager.get_events()
    assert len(events) == 1
    e = events[0]
    assert e["event_type"] == "audit_call"
    assert "signature" in e["meta"]

    # Verify the signature
    event_data = {
        "event_type": "audit_call",
        "function_name": "critical_func",
        "timestamp": e["timestamp"],
        "duration": e["duration"],
        "args": e["meta"]["args"],
        "kwargs": e["meta"]["kwargs"]
    }
    assert verify_signature(event_data, e["meta"]["signature"], DEFAULT_SECRET_KEY)
