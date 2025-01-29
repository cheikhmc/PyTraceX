"""
context.py
----------
Holds context variables such as correlation IDs for microservices.
"""

import contextvars

# A context variable for correlation IDs in microservices
_correlation_id_var = contextvars.ContextVar("correlation_id", default=None)

def set_correlation_id(corr_id: str):
    """
    Set a correlation ID in the context. Typically set at the start of each request.
    """
    _correlation_id_var.set(corr_id)

def get_correlation_id() -> str:
    """
    Retrieve the current correlation ID from the context.
    """
    return _correlation_id_var.get()
