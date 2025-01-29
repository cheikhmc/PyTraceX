"""
ml_tracking.py
--------------
A simple module for tracking ML pipeline steps (preprocessing, training, etc.).
Users can optionally install "ml" extra if they want to group ML features.
"""

import time
from functools import wraps
from .trace_manager import TraceManager, TraceEvent

def ml_step(step_name: str = None):
    """
    Decorator for ML pipeline steps. Records input/output shapes, data, or metadata.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            TraceManager().record_event(
                TraceEvent(
                    event_type="ml_step",
                    function_name=step_name or func.__name__,
                    timestamp=start_time,
                    duration=end_time - start_time,
                    meta={
                        "args_repr": repr(args),
                        "kwargs_repr": repr(kwargs),
                        "output_repr": repr(result),
                    }
                )
            )
            return result
        return wrapper
    return decorator
