"""
middlewares.py
--------------
Example: Integrate with a microservice web framework (FastAPI, Flask, or Django)
to trace inbound/outbound requests automatically.
"""

from .trace_manager import TraceManager, TraceEvent
import time

# Example for FastAPI
try:
    from fastapi import Request, Response
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.types import ASGIApp

    class TracingMiddleware(BaseHTTPMiddleware):
        """
        Middleware that traces every inbound/outbound HTTP request.
        """
        def __init__(self, app: ASGIApp, **options):
            super().__init__(app)
            self.options = options

        async def dispatch(self, request: Request, call_next):
            start_time = time.time()
            response: Response = await call_next(request)
            end_time = time.time()

            event = TraceEvent(
                event_type="api_request",
                function_name="HTTP " + request.url.path,
                timestamp=start_time,
                duration=(end_time - start_time),
                meta={
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code,
                }
            )
            TraceManager().record_event(event)
            return response

except ImportError:
    # If fastapi/starlette not installed
    TracingMiddleware = None

# For Flask or Django, you'd implement a similar approach with their middleware system.
