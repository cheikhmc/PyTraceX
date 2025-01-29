"""
PyTraceX
--------
A lightweight and extensible Python library for:
 - Execution flow tracing
 - Audit logging
 - Correlation IDs for microservices
 - ML pipeline tracking
 - Optional I/O tracing
 - Optional FastAPI-based dashboard
"""

__version__ = "0.4.0"

from .trace_manager import TraceManager
from .decorators import trace, audit
from .ml_tracking import ml_step
from .context import set_correlation_id, get_correlation_id
from .io_tracing import trace_file_ops  

# Optional modules (conditionally imported)
try:
    from .dashboard import run_dashboard
except ImportError:
    def run_dashboard(*args, **kwargs):
        raise ImportError("Dashboard not installed. Install with 'poetry install --extras dashboard'.")

__all__ = [
    "TraceManager",
    "trace",
    "audit",
    "ml_step",
    "run_dashboard",
    "set_correlation_id",
    "get_correlation_id",
    "trace_file_ops"
]
