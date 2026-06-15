#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
merge_yaml.py

Deep-merge two YAML files: apply a delta YAML onto a base YAML and output the
result, preserving field hierarchy. Mappings are merged recursively, lists are
appended by default (base + delta), and scalars are overridden by the delta.

Usage:
  merge_yaml.py BASE.yaml DELTA.yaml [-o OUTPUT.yaml]

Notes:
  - Requires PyYAML at runtime for file I/O. If unavailable, you'll get a
    helpful installation message. The core merge function works on Python
    dict/list primitives and is unit-tested.
"""

from __future__ import annotations

import argparse
import os
import io
import sys
from typing import Any, MutableMapping, Sequence

try:
    import yaml  # type: ignore
except Exception:
    yaml = None  # defer error until we actually need YAML I/O


def deep_merge(base: Any, delta: Any) -> Any:
    """Recursively merge delta into base and return the merged structure.

    Rules:
    - If both values are dict-like: merge keys recursively.
    - If both values are list-like: append (concatenate) delta items to base.
    - Otherwise: return delta (override).

    This function does not mutate the input objects; it constructs and returns
    a merged copy.
    """

    # Mapping -> Mapping: recursive merge
    if isinstance(base, dict) and isinstance(delta, dict):
        result: MutableMapping[str, Any] = {}
        # Start with base keys to preserve base ordering where possible
        for k in base:
            result[k] = base[k]
        for k, v in delta.items():
            if k in result:
                result[k] = deep_merge(result[k], v)
            else:
                result[k] = v
        return result

    # Sequence (list) -> Sequence: append (concatenate)
    if isinstance(base, list) and isinstance(delta, list):
        return list(base) + list(delta)

    # Fallback: override with delta
    return delta


def _load_yaml(path: str) -> Any:
    if yaml is None:
        sys.stderr.write(
            "PyYAML is required. Install with: pip install pyyaml\n"
        )
    with io.open(path, "r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f) if yaml else None
        except Exception as e:
            raise SystemExit(f"Failed to parse YAML '{path}': {e}")


def _dump_yaml(data: Any, path: str | None, header: str | None = None) -> None:
    if yaml is None:
        sys.stderr.write(
            "PyYAML is required. Install with: pip install pyyaml\n"
        )
        # If PyYAML missing, fall back to printing Python repr to help debugging
        if path in (None, "-"):
            if header:
                print(header)
                if not header.endswith("\n"):
                    print()
                else:
                    # Ensure a blank line after header for readability
                    print()
            print(repr(data))
            return
        with io.open(path, "w", encoding="utf-8") as f:
            if header:
                f.write(header)
                if not header.endswith("\n"):
                    f.write("\n")
                f.write("\n")
            f.write(repr(data))
            return

    out_stream = sys.stdout if path in (None, "-") else io.open(path, "w", encoding="utf-8")
    close_stream = path not in (None, "-")
    try:
        if header:
            out_stream.write(header)
            if not header.endswith("\n"):
                out_stream.write("\n")
            out_stream.write("\n")
        yaml.safe_dump(
            data,
            out_stream,  # type: ignore[arg-type]
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            indent=2,
        )
    finally:
        if close_stream:
            out_stream.close()  # type: ignore[union-attr]


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Deep-merge two YAML files")
    p.add_argument("base", help="Path to base YAML file")
    p.add_argument("delta", help="Path to delta YAML file to apply on top of base")
    p.add_argument(
        "-o",
        "--output",
        help="Output YAML file path (default: stdout)",
        default="-",
    )
    return p.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    ns = parse_args(sys.argv[1:] if argv is None else argv)

    base_data = _load_yaml(ns.base)
    delta_data = _load_yaml(ns.delta)

    merged = deep_merge(base_data, delta_data)

    # Compute header paths relative to the output file location when possible
    if ns.output not in (None, "-"):
        out_dir = os.path.dirname(os.path.abspath(ns.output)) or "."
        base_path = os.path.relpath(os.path.abspath(ns.base), start=out_dir)
        delta_path = os.path.relpath(os.path.abspath(ns.delta), start=out_dir)
    else:
        base_path = ns.base
        delta_path = ns.delta

    header = (
        "# This file was automatically generated by merge_yaml.py\n"
        f"# Sources: base={base_path} delta={delta_path}"
    )
    _dump_yaml(merged, ns.output, header=header)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
