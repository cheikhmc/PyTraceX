"""
hashing.py
----------
Provides tamper-proof hashing for trace events.
"""

import hashlib
import hmac
from typing import Dict, Union
from ..config import DEFAULT_SECRET_KEY

def sign_event(event_data: Dict, secret_key: Union[str, bytes] = DEFAULT_SECRET_KEY) -> str:
    """
    Generate a cryptographic signature for an event.
    """
    if isinstance(secret_key, str):
        secret_key = secret_key.encode("utf-8")
    
    message = str(event_data).encode("utf-8")
    return hmac.new(secret_key, message, hashlib.sha256).hexdigest()

def verify_signature(event_data: Dict, signature: str, secret_key: Union[str, bytes] = DEFAULT_SECRET_KEY) -> bool:
    """
    Verify that the event signature is valid.
    """
    expected_sig = sign_event(event_data, secret_key)
    return hmac.compare_digest(expected_sig, signature)
