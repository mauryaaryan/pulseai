"""
conftest.py — Adds backend/app to sys.path so pytest can find modules when
running tests from any directory.
"""
import sys
import os

# Point to the backend/app directory (parent of this conftest.py)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Also ensure Database/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Database'))
