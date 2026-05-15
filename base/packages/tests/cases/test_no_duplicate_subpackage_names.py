# SPDX-License-Identifier: MIT
"""Across all binary repos, no two distinct SRPMs may produce a
sub-package of the same name.

A binary package's source SRPM is identified by RPM's ``SourceRPM``
header (which becomes ``<rpm:sourcerpm>`` in primary metadata). The
SRPM's *name* (i.e. the part before the version) is what we compare
— two binary RPMs with the same NAME built from SRPMs that share the
same SRPM name are fine; two different SRPM names producing the same
binary NAME are not.

This catches both intentional collisions (a renamed package built
twice from different sources) and accidental ones (fork-and-build
mistakes).

Rules-as-code: two policy dicts, both keyed by binary name -> the
*expected* SRPM set producing it.

* :data:`ALLOWLIST` -- *intentional* multi-SRPM coexistence (compat
  shims, etc.). Silently skipped as long as the observed SRPM set is
  a subset of the listed set. This is mechanism *(b) intentional
  silent allowlist* in the
  ``Allowlist mechanism taxonomy`` section of ``docs/architecture.md``;
  it intentionally bypasses the known-violations engine and its
  cleanup rails.
* The known-violations TOML (``cases/known-violations/
  test_no_duplicate_subpackage_names.toml`` under section
  ``[duplicate-subpackages]``) -- *known violations we have not yet
  cleaned up*. Reported as ``XFAIL`` subtests via the shared
  :func:`utils.known_violations.classify_violations` engine: visible
  in pytest output and counted toward the xfail tally, but they do
  not fail the run. Stale-allowlist rails (consumer no longer
  multi-SRPM, or a listed contributing SRPM no longer in the
  observed set) fail the run as a cleanup nudge. This is mechanism
  *(c) tracked-but-tolerated allowlist* in the same taxonomy.

The known-violations file format is documented in
``cases/known-violations.schema.json``. The arch-gated form is
supported but not currently used by any entry in this file.
"""

from __future__ import annotations

import logging
import re
from collections import defaultdict

import pytest

from utils.known_violations import classify_violations
from utils.repos import Repo
from utils.types import Package


_SECTION = "duplicate-subpackages"


# rules-as-code: package names that are *intentionally* produced by
# multiple SRPMs (e.g. compatibility shims). Each entry is a (name,
# {srpm_names...}) pair and is allowed only if the observed SRPM set
# is a subset of the listed set. Edit with a comment justifying the
# entry. Allowlisted entries are silently skipped (no XFAIL noise).
ALLOWLIST: dict[str, frozenset[str]] = {
    # "compat-foo": frozenset({"foo", "foo-compat"}),  # example
}


_SRPM_RE = re.compile(r"^(?P<name>.+)-(?P<ver>[^-]+)-(?P<rel>[^-]+)\.(?:src|nosrc)\.rpm$")


def _srpm_name_of(pkg: Package) -> str | None:
    """Extract the SRPM *name* from ``pkg.sourcerpm``.

    ``sourcerpm`` is of the form ``foo-1.2-3.azl4.src.rpm``; we want
    just ``foo``.
    """
    if not pkg.sourcerpm:
        return None
    m = _SRPM_RE.match(pkg.sourcerpm)
    if m is None:
        return None
    return m.group("name")


def test_no_duplicate_subpackage_names(
    arch, all_binary_packages, binary_repos: list[Repo], subtests, known_violations,
    summary_recorder,
) -> None:
    if not binary_repos:
        pytest.fail(
            "misconfigured run: no binary --repo provided. This test "
            "validates a cross-repo invariant and is only meaningful "
            "with the full set of binary repos provided. Pass at least "
            "one --repo name=...,kind=binary,url=... — or use pytest -k "
            "/ --ignore to deselect this test if you intentionally want "
            "to skip it."
        )

    section = known_violations.section(_SECTION)
    source_label = f"{known_violations.path.name} [{_SECTION}]"

    by_repo: dict[Repo, list[Package]] = all_binary_packages(arch)

    # binary name -> set of SRPM names contributing.
    name_to_srpms: dict[str, set[str]] = defaultdict(set)
    # binary name -> example NEVRA + repo-name pairs (one per SRPM).
    name_to_examples: dict[str, dict[str, str]] = defaultdict(dict)

    seen_nevras: set[tuple] = set()
    for repo, packages in by_repo.items():
        for pkg in packages:
            if pkg.is_source:
                continue
            # Dedupe by NEVRA across repos.
            key = (pkg.nevra,)
            if key in seen_nevras:
                continue
            seen_nevras.add(key)

            srpm_name = _srpm_name_of(pkg)
            if srpm_name is None:
                # Missing or unparseable sourcerpm: use a per-NEVRA
                # *unique* sentinel so two such packages never get
                # silently grouped into the same SRPM bucket (which
                # would let cross-package collisions slip through). The
                # sentinel deliberately includes the NEVRA so the
                # failure message points straight at the offending
                # package.
                srpm_name = f"<unparseable-sourcerpm:{pkg.nevra}>"
            name_to_srpms[pkg.name].add(srpm_name)
            name_to_examples[pkg.name].setdefault(
                srpm_name, f"{pkg.nevra} (from repo {repo.name!r})"
            )

    # Pre-filter into the *finding* shape the shared classifier
    # consumes: only multi-SRPM names participate (single-SRPM is the
    # expected normal case), and silently-allowlisted intentional
    # collisions are dropped before classification so they neither
    # XFAIL nor trip stale rails.
    findings: dict[str, set[str]] = {}
    for name, srpms in name_to_srpms.items():
        if len(srpms) <= 1:
            continue
        allowed = ALLOWLIST.get(name)
        if allowed is not None and srpms.issubset(allowed):
            logging.info(
                "Allowlisted multi-SRPM binary name: %s from %s",
                name, sorted(srpms),
            )
            continue
        findings[name] = srpms

    classified = classify_violations(
        findings=findings,
        consumer_of=lambda name: name,
        arch=arch,
        allowlist=section,
    )

    summary_recorder(arch=arch, source_label=source_label, classified=classified)

    def _example_lines(name: str, srpms) -> list[str]:
        return [
            f"  example from SRPM {srpm!r}: "
            f"{name_to_examples[name].get(srpm, '<no example>')}"
            for srpm in sorted(srpms)
        ]

    def _meta_suffix(v) -> str:
        # Per-entry metadata (ST2): surface in message bodies only;
        # subtest IDs stay stable as diff-targets.
        bits: list[str] = []
        if v.reason:
            bits.append(f"reason: {v.reason}")
        if v.issue:
            bits.append(f"tracked: {v.issue}")
        return "\n[" + "; ".join(bits) + "]" if bits else ""

    # Each verdict / stale entry becomes its own subtest so it
    # appears as a distinct entry in pytest output (and in junitxml).
    # Sorted for stable reporting order.
    for verdict in sorted(classified.real_fails, key=lambda v: v.consumer):
        name = verdict.consumer
        srpms = verdict.observed
        with subtests.test(binary_name=name, arch=arch):
            if verdict.listed is not None:
                # Listed in the known-violations file but the observed
                # set exceeds the listed ceiling — flag the new SRPM(s).
                new = sorted(set(srpms) - verdict.listed)
                pytest.fail(
                    f"binary name {name!r} on {arch} is produced by "
                    f"{len(srpms)} distinct SRPMs: {sorted(srpms)}; "
                    f"{source_label} allows {sorted(verdict.listed)} but "
                    f"observed new SRPM(s): {new}\n"
                    + "\n".join(_example_lines(name, srpms))
                    + _meta_suffix(verdict)
                )
            pytest.fail(
                f"binary name {name!r} on {arch} is produced by "
                f"{len(srpms)} distinct SRPMs: {sorted(srpms)}\n"
                + "\n".join(_example_lines(name, srpms))
            )

    for verdict in sorted(classified.known_violations, key=lambda v: v.consumer):
        name = verdict.consumer
        srpms = verdict.observed
        with subtests.test(binary_name=name, arch=arch):
            pytest.xfail(
                f"known violation -- multi-SRPM binary (tracked in "
                f"{source_label}): {name!r} on {arch} is produced "
                f"by {sorted(srpms)}\n"
                + "\n".join(_example_lines(name, srpms))
                + _meta_suffix(verdict)
            )

    for entry in classified.stale:
        if entry.kind == "stale-consumer":
            with subtests.test(
                binary_name=entry.consumer, arch=arch, kind="stale-consumer",
            ):
                observed = sorted(name_to_srpms.get(entry.consumer, set()))
                pytest.fail(
                    f"{entry.consumer!r} is listed in {source_label} "
                    f"but is no longer produced by multiple SRPMs on "
                    f"{arch} (observed: {observed}). Please remove "
                    f"the entry."
                )
        else:
            with subtests.test(
                binary_name=entry.consumer, missing_srpm=entry.listed_dep,
                arch=arch, kind="stale-dep",
            ):
                observed = sorted(name_to_srpms.get(entry.consumer, set()))
                pytest.fail(
                    f"SRPM {entry.listed_dep!r} is listed in "
                    f"{source_label} under {entry.consumer!r} but no "
                    f"longer contributes to {entry.consumer!r} on "
                    f"{arch} (observed contributing SRPMs: "
                    f"{observed}). Please remove that SRPM from the "
                    f"entry."
                )

