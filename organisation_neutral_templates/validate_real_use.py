#!/usr/bin/env python3
"""Deprecated compatibility alias; use validate_demo_data.py instead."""
import runpy
import sys
from pathlib import Path

print("Deprecated filename: run validate_demo_data.py for synthetic demo data only.", file=sys.stderr)
runpy.run_path(str(Path(__file__).with_name("validate_demo_data.py")), run_name="__main__")
