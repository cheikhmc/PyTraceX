# tests/test_io_tracing.py

import pytest
import os

from pytracex.io_tracing import trace_file_ops, untrace_file_ops
from pytracex.trace_manager import TraceManager

def test_io_tracing(tmp_path):
    """
    Test that file open/read/write/close events are captured when file ops are traced.
    """
    manager = TraceManager()
    manager.clear_events()

    trace_file_ops()  # Enable file ops tracing

    test_file = tmp_path / "testfile.txt"
    with open(test_file, 'w') as f:
        f.write("Hello World")

    with open(test_file, 'r') as f:
        data = f.read()

    untrace_file_ops()  # Restore original open

    events = manager.get_events()
    assert len(events) >= 4

    # We expect something like: file_open (write), file_write, file_close,
    #                          file_open (read), file_read, file_close
    # Let's confirm at least the event types:
    event_types = [e["event_type"] for e in events]
    assert "file_open" in event_types
    assert "file_write" in event_types
    assert "file_read" in event_types
    assert "file_close" in event_types
