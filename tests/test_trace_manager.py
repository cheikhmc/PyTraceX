import pytest
from pytracex.trace_manager import TraceManager, TraceEvent

def test_record_and_retrieve_events():
    manager = TraceManager()
    manager.clear_events()

    event = TraceEvent(event_type="test_event", function_name="test_func")
    manager.record_event(event)

    events = manager.get_events()
    assert len(events) == 1
    assert events[0]["event_type"] == "test_event"
    assert events[0]["function_name"] == "test_func"

def test_clear_events():
    manager = TraceManager()
    manager.clear_events()
    event = TraceEvent(event_type="clear_test")
    manager.record_event(event)
    assert len(manager.get_events()) == 1

    manager.clear_events()
    assert len(manager.get_events()) == 0
