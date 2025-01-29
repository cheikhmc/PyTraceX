"""
config.py
---------
Global defaults for PyTraceX. These can be customized by the user.
"""

import logging
import os

LOGGER_NAME = "pytracex"
LOGGER = logging.getLogger(LOGGER_NAME)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# In-memory default storage (could be replaced by DB or external store)
TRACE_STORAGE = []

# Default PII masking rules
PII_PATTERNS = {
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "ssn": r"\d{3}-\d{2}-\d{4}"
}
PII_REPLACEMENTS = {
    "email": "[EMAIL REDACTED]",
    "ssn": "[SSN REDACTED]"
}

# Default secret key for tamper-proof hashing. (User should override in production!)
DEFAULT_SECRET_KEY = os.environ.get("PYTRACEX_SECRET_KEY", "CHANGEME")
