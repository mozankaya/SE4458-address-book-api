"""Vercel entry point: exposes the FastAPI app to Vercel's Python runtime."""

import os
import sys

# Make the project root importable so the `app` package can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app  # noqa: E402,F401
