# src/pytracex/io_tracing.py

"""
io_tracing.py
-------------
Provides a function to trace file I/O (open, read, write) using only the standard library.
"""

import builtins
import time
from typing import Callable
from .trace_manager import TraceManager, TraceEvent

_original_open = builtins.open

def traced_open(file, mode='r', *args, **kwargs):
    """
    A monkey-patched version of open() that logs file open operations.
    Returns a wrapped file object that can trace read/write calls if desired.
    """
    start_time = time.time()
    f = _original_open(file, mode, *args, **kwargs)
    end_time = time.time()

    # Log the open event
    manager = TraceManager()
    event = TraceEvent(
        event_type="file_open",
        function_name="open",
        timestamp=start_time,
        duration=end_time - start_time,
        meta={
            "filename": file,
            "mode": mode
        }
    )
    manager.record_event(event)

    # Optionally wrap the file object to intercept read/write
    return _wrap_file_object(f, file, mode)

def _wrap_file_object(f, file, mode):
    """
    Wrap the file object to trace read, write, close calls, etc.
    """
    class TracedFile:
        def __init__(self, original_file):
            self._f = original_file

        def read(self, *args, **kwargs):
            start_time = time.time()
            data = self._f.read(*args, **kwargs)
            end_time = time.time()

            TraceManager().record_event(TraceEvent(
                event_type="file_read",
                function_name="read",
                timestamp=start_time,
                duration=end_time - start_time,
                meta={
                    "filename": file,
                    "mode": mode,
                    "bytes_returned": len(data) if data else 0
                }
            ))
            return data

        def write(self, content, *args, **kwargs):
            start_time = time.time()
            result = self._f.write(content, *args, **kwargs)
            end_time = time.time()

            TraceManager().record_event(TraceEvent(
                event_type="file_write",
                function_name="write",
                timestamp=start_time,
                duration=end_time - start_time,
                meta={
                    "filename": file,
                    "mode": mode,
                    "bytes_written": len(content) if content else 0
                }
            ))
            return result

        def close(self):
            start_time = time.time()
            self._f.close()
            end_time = time.time()

            TraceManager().record_event(TraceEvent(
                event_type="file_close",
                function_name="close",
                timestamp=start_time,
                duration=end_time - start_time,
                meta={
                    "filename": file,
                    "mode": mode
                }
            ))

        def __enter__(self):
            """
            Make this object compatible with the 'with' statement.
            """
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            """
            Automatically close the file on exiting the 'with' block.
            """
            self.close()

        # Forward any other attributes to the underlying file object
        def __getattr__(self, name):
            return getattr(self._f, name)

    return TracedFile(f)



def trace_file_ops():
    """
    Monkey-patch Python's built-in open() with traced_open().

    Call `untrace_file_ops()` if you need to revert back to the original open().
    """
    builtins.open = traced_open


def untrace_file_ops():
    """
    Restore the original built-in open() function.
    """
    builtins.open = _original_open
