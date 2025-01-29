"""
dashboard.py
------------
A FastAPI-based dashboard for real-time trace monitoring.
Includes a basic WebSocket endpoint for advanced visualization if installed.
"""

try:
    from fastapi import FastAPI, WebSocket
    from fastapi.responses import JSONResponse
    import uvicorn
except ImportError:
    FastAPI = None
    uvicorn = None

import asyncio
from .trace_manager import TraceManager

def run_dashboard(host: str = "127.0.0.1", port: int = 8000):
    """
    Run the PyTraceX dashboard with optional real-time WebSocket streaming.
    """
    if not FastAPI or not uvicorn:
        raise ImportError("FastAPI/Uvicorn not installed. Install with 'poetry install --extras dashboard'.")

    app = FastAPI(title="PyTraceX Dashboard")
    manager = TraceManager()

    @app.get("/traces")
    def get_traces():
        return JSONResponse(content=manager.get_events())

    @app.delete("/traces")
    def clear_traces():
        manager.clear_events()
        return {"message": "All trace events cleared."}

    # Optional real-time WebSocket endpoint
    @app.websocket("/ws/traces")
    async def websocket_traces(websocket: WebSocket):
        await websocket.accept()
        # In a real scenario, you'd push events as they come in (e.g., hooking record_event).
        # For simplicity, let's just periodically send the entire event list.
        try:
            while True:
                await websocket.send_json(manager.get_events())
                await asyncio.sleep(2)  # Send every 2 seconds
        except Exception:
            pass

    uvicorn.run(app, host=host, port=port)
