# Copyright (c) 2026 Microsoft Corporation.
# Licensed under the MIT License.
"""Configure imports for MCP server tests."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
