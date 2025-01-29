import pytest
from pytracex.trace_manager import TraceManager

def test_dashboard_import():
    """
    Test if the dashboard is importable. If not installed, it should raise ImportError.
    """
    try:
        from pytracex.dashboard import run_dashboard
    except ImportError:
        pytest.skip("Dashboard extras not installed.")

def test_dashboard_routes():
    """
    Example test for the dashboard routes. This is tricky without an async test client.
    If using FastAPI test client, you can do more thorough tests here.
    """
    try:
        from pytracex.dashboard import run_dashboard
        # Typically you'd use starlette.testclient or httpx to test the routes
    except ImportError:
        pytest.skip("Dashboard extras not installed.")
