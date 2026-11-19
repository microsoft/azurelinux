# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Configure helper-unit-test imports without loading image fixtures."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
