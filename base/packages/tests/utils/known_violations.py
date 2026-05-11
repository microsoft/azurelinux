# SPDX-License-Identifier: MIT
"""Loader for tracked-but-tolerated violation allowlists.

The Azure Linux repo-validation tests classify each observed
violation against a per-test allowlist of *known violations* — gaps
that are real, tracked, and intentionally tolerated for now (so the
overall test stays green and a single new regression stands out)
while still being reported as ``XFAIL`` subtests so they remain
visible.

Each test that uses an allowlist reads a TOML file at
``cases/known-violations/<test-stem>.toml``. The file format is
documented in detail in ``cases/known-violations.schema.json``.
Briefly, each "logical section" maps consumer/binary names to the
strings whose presence is allowed for that name. There are two
parallel forms:

* ``[<section>]`` — flat: ``"<name>" = ["item", ...]`` (applies on
  every arch).
* ``[<section>-arch-gated."<name>"]`` — per-arch:
  ``"<arch>" = ["item", ...]`` (applies only on listed arches; on
  other arches the entry is treated as absent).

A given ``<name>`` must appear in at most one of the two parallel
tables for a section. The loader merges the two back into a single
in-memory mapping per section.

The schema is validated at load time using the ``jsonschema``
library so authoring mistakes (typo'd section name, empty value,
wrong shape) surface with a clear message rather than as a confusing
runtime ``KeyError`` deep in the test.

Why TOML? It is the same on-disk format used elsewhere in this repo
(``azldev`` component config, the file-conflicts allowlists), keeps
section comments first-class (cluster comments are the most useful
organisational feature in these allowlists), and is unambiguously
parseable by Python's stdlib ``tomllib``.
"""

from __future__ import annotations

import sys
import tomllib
from collections import defaultdict
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generic, Literal, TypeVar, Union

import jsonschema

SCHEMA_VERSION = 1


@dataclass(frozen=True)
class KnownViolationsEntry:
    """One allowlist entry: the deps it permits, plus optional metadata.

    The TOML on-disk form may be either bare (just the array of deps,
    the short form used everywhere by default) or an inline table
    ``{deps = [...], reason = "...", issue = "..."}`` (the long form,
    for entries the curator wants to annotate). Both desugar to this
    in-memory dataclass; downstream code (the classifier, the
    summary recorder, the test emitters) treats the two forms
    uniformly. The metadata is propagated into ``Verdict`` (so
    subtest messages and the JSON summary surface it) but does not
    influence classification at all -- it is purely human-readable
    context for the curator.
    """

    deps: frozenset[str]
    """The allowlisted strings."""

    reason: str | None = None
    """Free-text rationale for why this entry is tolerated."""

    issue: str | None = None
    """Tracking link (URL or shorthand like ``AB#12345``)."""


# Per-name value: either a flat entry (applies on every arch)
# or an arch-keyed mapping of entries (applies only on listed arches).
KnownViolationsValue = Union[KnownViolationsEntry, Mapping[str, KnownViolationsEntry]]
KnownViolationsMap = Mapping[str, KnownViolationsValue]


class KnownViolationsError(Exception):
    """Raised when a known-violations file is malformed."""


# Suffix that distinguishes the parallel "arch-gated" table from
# the flat one (i.e. ``[runtime-missing]`` vs
# ``[runtime-missing-arch-gated.<name>]``).
_ARCH_GATED_SUFFIX = "-arch-gated"

_SCHEMA_PATH = Path(__file__).resolve().parent.parent / "cases" / "known-violations.schema.json"


def _load_schema() -> dict:
    import json
    return json.loads(_SCHEMA_PATH.read_text())


@dataclass(frozen=True)
class KnownViolationsFile:
    """In-memory representation of one ``cases/known-violations/*.toml`` file."""

    path: Path
    schema_version: int
    sections: Mapping[str, KnownViolationsMap]

    def section(self, name: str) -> KnownViolationsMap:
        """Return one section's allowlist, or empty if the section is absent.

        Returning empty rather than raising lets a test that doesn't
        currently need a section omit it from the file entirely
        without having to add an explicit empty stub.
        """
        return self.sections.get(name, {})


def _format_path(path: list[str | int]) -> str:
    out: list[str] = []
    for p in path:
        if isinstance(p, int):
            out.append(f"[{p}]")
        else:
            out.append(f".{p}" if out else p)
    return "".join(out) or "<root>"


def _validate_jsonschema(data: dict, src: Path) -> None:
    try:
        jsonschema.validate(data, _load_schema())
    except jsonschema.ValidationError as exc:
        raise KnownViolationsError(
            f"{src}: schema violation at "
            f"{_format_path(list(exc.absolute_path))}: {exc.message}"
        ) from exc


def _value_to_entry(raw: list[str] | dict) -> KnownViolationsEntry:
    """Build a :class:`KnownViolationsEntry` from a schema-validated value.

    Schema guarantees ``raw`` is either ``list[str]`` (short form) or
    a dict with required ``deps`` and optional ``reason`` / ``issue``
    (long form). Both desugar to the same dataclass.
    """
    if isinstance(raw, list):
        return KnownViolationsEntry(deps=frozenset(raw))
    return KnownViolationsEntry(
        deps=frozenset(raw["deps"]),
        reason=raw.get("reason"),
        issue=raw.get("issue"),
    )


def _flat_section_to_value(name: str, raw: list[str] | dict) -> KnownViolationsEntry:
    return _value_to_entry(raw)


def _arch_gated_section_to_value(
    name: str, raw: dict[str, list[str] | dict]
) -> Mapping[str, KnownViolationsEntry]:
    return {arch: _value_to_entry(items) for arch, items in raw.items()}


def _merge_section(
    src: Path,
    section_name: str,
    flat_table: dict[str, list[str] | dict],
    arch_gated_table: dict[str, dict[str, list[str] | dict]],
) -> dict[str, KnownViolationsValue]:
    """Merge the parallel flat + arch-gated tables for one logical section.

    Each name must appear in exactly one of the two tables.
    """
    merged: dict[str, KnownViolationsValue] = {}
    for name, raw in flat_table.items():
        merged[name] = _flat_section_to_value(name, raw)
    for name, raw in arch_gated_table.items():
        if name in merged:
            raise KnownViolationsError(
                f"{src}: name {name!r} appears in both "
                f"[{section_name}] and "
                f"[{section_name}{_ARCH_GATED_SUFFIX}.{name}] -- "
                f"each name may appear in only one of the two."
            )
        merged[name] = _arch_gated_section_to_value(name, raw)
    return merged


def load_known_violations(path: Path) -> KnownViolationsFile:
    """Read and validate a known-violations TOML file."""
    if not path.exists():
        raise KnownViolationsError(
            f"known-violations file not found: {path}"
        )
    try:
        with path.open("rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as exc:
        raise KnownViolationsError(f"{path}: invalid TOML: {exc}") from exc
    if not isinstance(data, dict):
        raise KnownViolationsError(
            f"{path}: top-level value must be a TOML table, got {type(data).__name__}"
        )

    _validate_jsonschema(data, path)

    # ``schema-version`` is enforced by the schema itself (``const: 1``);
    # by the time we get here the value is guaranteed to equal
    # ``SCHEMA_VERSION``. Pop it so it doesn't pollute the section
    # iteration below.
    schema_version = data.pop("schema-version")

    # Collect logical sections: every top-level key whose name does
    # NOT end in ``-arch-gated`` is a flat section; the matching
    # arch-gated table (if present) is merged into it. Any
    # arch-gated table without a matching flat section is also a
    # logical section in its own right (just with no flat entries).
    flat_keys = [k for k in data if not k.endswith(_ARCH_GATED_SUFFIX)]
    arch_keys = [k for k in data if k.endswith(_ARCH_GATED_SUFFIX)]

    section_names: set[str] = set(flat_keys)
    for k in arch_keys:
        section_names.add(k[: -len(_ARCH_GATED_SUFFIX)])

    sections: dict[str, KnownViolationsMap] = {}
    for section_name in sorted(section_names):
        flat_table = data.get(section_name, {})
        arch_gated_table = data.get(section_name + _ARCH_GATED_SUFFIX, {})
        sections[section_name] = _merge_section(
            path, section_name, flat_table, arch_gated_table
        )

    return KnownViolationsFile(
        path=path,
        schema_version=schema_version,
        sections=sections,
    )


def __getattr__(name: str):  # pragma: no cover - import-time helper
    # Friendly error for code that imported the old names.
    if name in ("ExpectedMissingMap", "ExpectedMissingValue", "assert_expected_missing"):
        raise AttributeError(
            f"{name!r} was renamed in the known-violations refactor; "
            f"use the corresponding KnownViolations* / "
            f"assert_known_violations name (see "
            f"utils/repoclosure.py for assert_known_violations and "
            f"utils/known_violations.py for KnownViolationsMap)."
        )
    raise AttributeError(name)


# ---------------------------------------------------------------------------
# Four-way classification engine
# ---------------------------------------------------------------------------
#
# A test produces a set of *findings* keyed by some test-specific consumer
# key (e.g. NEVRA for repoclosure, binary-name for duplicate-subpackage).
# Each finding carries a set of observed value-strings (e.g. unresolved
# dep names, or contributing SRPM names). The allowlist (a
# ``KnownViolationsMap``) maps consumer-name to the value-strings whose
# presence is tolerated for that consumer.
#
# The four classifications are::
#
#   * real-fail      consumer not in allowlist, OR observed values are not
#                    a subset of the allowlist entry. The test should fail.
#   * known-violation consumer in allowlist and observed values ⊆ listed
#                    values. The test reports XFAIL.
#   * stale-consumer consumer is in the allowlist but no finding aggregates
#                    to it on this arch. Fail the run -- the entry is
#                    obsolete and must be pruned.
#   * stale-dep      consumer is in the allowlist AND has at least one
#                    finding, but a value listed in the allowlist did not
#                    appear in any finding for that consumer on this arch.
#                    Fail the run -- prune the dep from the entry.
#
# The classifier is intentionally generic on the finding key type so the
# same engine can drive both repoclosure (per-NEVRA findings) and
# duplicate-subpackage (per-binary-name findings); per-test message
# rendering and subtest-key shape are kept in the calling test.

K = TypeVar("K")


def resolve_known_violations_for_arch(
    known_violations: KnownViolationsMap, arch: str,
) -> dict[str, KnownViolationsEntry]:
    """Project ``known_violations`` down to the entries that apply on ``arch``.

    A flat :class:`KnownViolationsEntry` value applies on every arch.
    A ``Mapping`` value applies only on the arches it explicitly lists;
    consumers whose entry is arch-gated and does not mention ``arch``
    are omitted from the projection (so they are treated as absent
    from the allowlist on this arch -- neither classified as known
    violations nor subject to the stale-entry safety rails).
    """
    out: dict[str, KnownViolationsEntry] = {}
    for name, entry in known_violations.items():
        if isinstance(entry, KnownViolationsEntry):
            out[name] = entry
        elif isinstance(entry, Mapping):
            arch_entry = entry.get(arch)
            if arch_entry is not None:
                out[name] = arch_entry
        else:
            raise TypeError(
                f"known-violations entry for {name!r} must be "
                f"KnownViolationsEntry or Mapping[arch, "
                f"KnownViolationsEntry], got {type(entry).__name__}"
            )
    return out


@dataclass(frozen=True)
class Verdict(Generic[K]):
    """One finding's classification."""

    key: K
    """The original finding key (NEVRA, binary-name, ...)."""

    consumer: str
    """The allowlist consumer name extracted from ``key``."""

    observed: frozenset[str]
    """Values observed for this finding."""

    listed: frozenset[str] | None
    """Values listed in the (arch-resolved) allowlist for ``consumer``,
    or ``None`` if the consumer is not in the allowlist on this arch."""

    classification: Literal["xfail", "real-fail"]

    reason: str | None = None
    """Free-text rationale carried over from the matched allowlist
    entry's ``reason`` field, when present. ``None`` for real-fails
    where the consumer is unlisted (``listed is None``)."""

    issue: str | None = None
    """Tracking link (URL or shorthand) carried over from the matched
    allowlist entry's ``issue`` field, when present. ``None`` for
    real-fails where the consumer is unlisted."""


@dataclass(frozen=True)
class StaleEntry:
    """A single stale-allowlist-entry verdict."""

    consumer: str
    kind: Literal["stale-consumer", "stale-dep"]
    listed_dep: str | None = None
    """Populated only for ``kind == "stale-dep"``."""


@dataclass
class ClassifiedViolations(Generic[K]):
    """Result of :func:`classify_violations`. Three independent buckets."""

    real_fails: list[Verdict[K]] = field(default_factory=list)
    known_violations: list[Verdict[K]] = field(default_factory=list)
    stale: list[StaleEntry] = field(default_factory=list)


def classify_violations(
    *,
    findings: Mapping[K, Iterable[str]],
    consumer_of: Callable[[K], str],
    arch: str,
    allowlist: KnownViolationsMap,
) -> ClassifiedViolations[K]:
    """Run the four-way classification.

    ``findings`` -- each finding key (test-specific) maps to the set of
    value-strings observed for it on this arch. The classifier groups
    findings by ``consumer_of(key)`` so multiple findings with the same
    consumer name are pooled when computing stale-dep.

    ``consumer_of`` -- extracts the allowlist consumer-name from a
    finding key. For repoclosure this is ``lambda nevra: nevra.name``;
    for duplicate-subpackage this is ``lambda name: name``.

    ``arch`` -- the arch the run targets, used to project arch-gated
    allowlist entries.

    ``allowlist`` -- the raw allowlist for the relevant section
    (the loader's ``KnownViolationsFile.section(...)`` output).

    The returned :class:`ClassifiedViolations` carries three independent
    buckets; the caller is responsible for emitting subtests with
    test-appropriate keys and messages.
    """
    effective = resolve_known_violations_for_arch(allowlist, arch)

    # Aggregate observed values per consumer so the per-dep stale-entry
    # rail can fire even when one finding carries only a subset of the
    # observed values for its consumer. Empty findings are skipped here
    # too (mirrors the per-finding loop below) so an empty finding for
    # a consumer can't accidentally promote it from "absent" to "seen
    # with empty observed set" -- the latter would silently squash a
    # legitimate stale-consumer signal into a chain of stale-dep hits.
    observed_by_consumer: dict[str, set[str]] = defaultdict(set)
    for key, values in findings.items():
        values_set = set(values)
        if not values_set:
            continue
        observed_by_consumer[consumer_of(key)].update(values_set)

    real_fails: list[Verdict[K]] = []
    known_violations: list[Verdict[K]] = []
    for key, values in findings.items():
        observed = frozenset(values)
        if not observed:
            # Empty observed set: no deps were actually reported as
            # missing for this key on this arch. Skip classification --
            # otherwise the listed-allowlist subset check would
            # vacuously match every entry, treating a transient empty
            # finding as a known violation and (worse) double-reporting
            # via stale-dep when the same consumer has a non-empty
            # finding elsewhere. Callers should not normally pass
            # empty value sets, but guarding here keeps the classifier
            # robust to future emitters that build per-finding sets
            # incrementally.
            continue
        consumer = consumer_of(key)
        entry = effective.get(consumer)
        listed_deps = entry.deps if entry is not None else None
        # Carry the entry's metadata onto the verdict so the test
        # emitters and the JSON summary can surface it. Real-fails
        # for unlisted consumers carry None metadata (there is no
        # entry to source it from); real-fails for over-the-ceiling
        # listed entries do carry the entry's metadata so the curator
        # sees the original rationale alongside the new gap.
        reason = entry.reason if entry is not None else None
        issue = entry.issue if entry is not None else None
        if listed_deps is not None and observed <= listed_deps:
            known_violations.append(
                Verdict(
                    key=key, consumer=consumer, observed=observed,
                    listed=listed_deps, classification="xfail",
                    reason=reason, issue=issue,
                )
            )
        else:
            real_fails.append(
                Verdict(
                    key=key, consumer=consumer, observed=observed,
                    listed=listed_deps, classification="real-fail",
                    reason=reason, issue=issue,
                )
            )

    stale: list[StaleEntry] = []
    # stale-consumer: consumer in allowlist but no finding aggregates to
    # it on this arch.
    for consumer in sorted(effective):
        if consumer not in observed_by_consumer:
            stale.append(StaleEntry(consumer=consumer, kind="stale-consumer"))
    # stale-dep: consumer present in both, but a listed value was not
    # observed for any finding under that consumer.
    for consumer in sorted(effective):
        if consumer not in observed_by_consumer:
            continue
        seen = observed_by_consumer[consumer]
        for dep in sorted(effective[consumer].deps):
            if dep not in seen:
                stale.append(
                    StaleEntry(
                        consumer=consumer, kind="stale-dep", listed_dep=dep,
                    )
                )

    return ClassifiedViolations(
        real_fails=real_fails,
        known_violations=known_violations,
        stale=stale,
    )


__all__ = [
    "ClassifiedViolations",
    "KnownViolationsEntry",
    "KnownViolationsError",
    "KnownViolationsFile",
    "KnownViolationsMap",
    "KnownViolationsValue",
    "SCHEMA_VERSION",
    "StaleEntry",
    "Verdict",
    "classify_violations",
    "load_known_violations",
    "resolve_known_violations_for_arch",
]
