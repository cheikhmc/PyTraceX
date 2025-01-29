import pytest
from pytracex.trace_manager import TraceManager
from pytracex.ml_tracking import ml_step

@ml_step("preprocess_data")
def preprocess(data):
    return [d.lower() for d in data]

@ml_step("train_model")
def train_model(data):
    return {"model": "fake_model", "data_size": len(data)}

def test_ml_step_decorator():
    manager = TraceManager()
    manager.clear_events()

    out = preprocess(["Hello", "World"])
    assert out == ["hello", "world"]

    results = train_model(out)
    assert results["data_size"] == 2

    events = manager.get_events()
    assert len(events) == 2
    assert events[0]["event_type"] == "ml_step"
    assert events[0]["function_name"] == "preprocess_data"
    assert events[1]["function_name"] == "train_model"
