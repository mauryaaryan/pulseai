"""
conftest.py — Adds voice_agent root to sys.path so pytest can find
services, database, utils, and models packages when running tests.
"""
import sys
import os

# Point to the voice_agent directory (parent of this conftest.py)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
