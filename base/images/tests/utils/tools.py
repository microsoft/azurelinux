# SPDX-License-Identifier: MIT
"""Native tool dependency registry.

Each :class:`NativeTool` instance registers itself on construction.
Util modules declare their dependencies as module-level constants and
use them at the call site::

    # in utils/extract.py
    GUESTMOUNT = NativeTool("guestmount", package_hint="libguestfs-tools",
                            reason="FUSE-mount VM images", when="vm")

    def mount_vm_image(...):
        subprocess.run([GUESTMOUNT.name, "--ro", ...])

This keeps the dependency declaration next to its use — renaming the
symbol breaks visibly — and avoids a parallel ``REQUIRED_TOOLS`` list
that would have to be maintained in lock-step with the call sites.

The pytest plugin imports every sibling module at preflight time so
that all tools are registered before :func:`check_tools` is called.

Direct invocation::

    uv run python -m utils.tools          # human-readable
    uv run python -m utils.tools --json   # machine-readable
"""

from __future__ import annotations

import importlib
import pkgutil
import shutil
from dataclasses import dataclass

# Module-level registry, populated by ``NativeTool.__post_init__``.
_REGISTRY: list["NativeTool"] = []


@dataclass(frozen=True)
class NativeTool:
    """A required external CLI tool.

    Construction registers the instance in the module-level registry
    so that :func:`required_tools` and :func:`check_tools` can find it
    after :func:`_import_all` has loaded every sibling module.
    """

    name: str
    package_hint: str = ""
    reason: str = ""
    when: str = "always"  # "always", "vm", "container"

    def __post_init__(self) -> None:
        _REGISTRY.append(self)


def _import_all() -> None:
    """Import every sibling module so module-level NativeTool instances register.

    Required because ``pytest_configure`` runs before conftest loads,
    so the imports it depends on (``utils.extract``, ``utils.parsers``,
    etc.) haven't happened yet at preflight time.
    """
    package = importlib.import_module(__package__ or "utils")
    for info in pkgutil.iter_modules(package.__path__):
        if info.name == "tools":
            continue
        importlib.import_module(f"{__package__}.{info.name}")


def required_tools(when: str | None = None) -> list[NativeTool]:
    """Return required tools, optionally filtered by *when*.

    Args:
        when: ``"vm"``, ``"container"``, or ``None`` for all tools.
    """
    _import_all()
    if when is None:
        return list(_REGISTRY)
    return [t for t in _REGISTRY if t.when in ("always", when)]


def check_tools(when: str | None = None) -> list[NativeTool]:
    """Return list of tools that are **missing** from ``$PATH``."""
    return [t for t in required_tools(when) if shutil.which(t.name) is None]


if __name__ == "__main__":
    # When run via `python -m utils.tools`, this module is loaded twice
    # (once as `__main__`, once as `utils.tools`). The registry lives in
    # `utils.tools`, so re-import to read it.
    import json
    import sys

    from utils.tools import check_tools, required_tools

    fmt = "--json" in sys.argv

    tools = required_tools()
    missing = check_tools()

    if fmt:
        out = [
            {
                "name": t.name,
                "package_hint": t.package_hint,
                "reason": t.reason,
                "when": t.when,
                "available": shutil.which(t.name) is not None,
            }
            for t in tools
        ]
        print(json.dumps(out, indent=2))
    else:
        for t in tools:
            available = "OK" if shutil.which(t.name) else "MISSING"
            scope = f"({t.when})" if t.when != "always" else ""
            hint = f"  [{t.package_hint}]" if t.package_hint else ""
            print(f"  {available:>9}  {t.name:<18} {scope:<14} {t.reason}{hint}")

        if missing:
            print(f"\n{len(missing)} missing tool(s). Install them before running tests.")
            sys.exit(1)
        else:
            print(f"\nAll {len(tools)} tools available.")
