"""Configuration for API router - allows switching between Phase 0 and Phase 1."""

import os

# Configuration: Set to True to use real agents (Phase 1), False for dummy agent (Phase 0)
USE_REAL_AGENTS = os.getenv("USE_REAL_AGENTS", "true").lower() == "true"

# Show banner on startup
if USE_REAL_AGENTS:
    print("🚀 Atlas Phase 1: Using real agents (News, Financial, Hiring, GitHub)")
else:
    print("🧪 Atlas Phase 0: Using dummy agent for testing")
