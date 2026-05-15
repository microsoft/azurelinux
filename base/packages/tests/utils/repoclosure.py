# SPDX-License-Identifier: MIT
"""In-process repoclosure using ``libdnf5`` (libsolv).

This module mirrors what ``dnf5 repoclosure`` itself does — it builds
a :class:`libdnf5.base.Base`, loads each universe repo, and asks
libsolv (via :class:`libdnf5.rpm.PackageQuery.is_dep_satisfied`)
whether each ``Requires:`` of every checked package is satisfied.

Why ``libdnf5`` rather than ``hawkey`` directly
-----------------------------------------------

Earlier revisions of this module used ``hawkey.Query.filter(provides=)``
to look up providers. That works fine for plain (name [op evr]) deps
but is the **wrong API** for rich/boolean dependencies — for an entry
like ``(foo if bar)`` it asks libsolv to find a Solvable that
literally provides the rich expression as a single Provides string,
which never matches; the conditional is not evaluated. The result was
a flood of false-positive closure violations any time an upstream
package used rich deps (which Fedora-derived packages do
extensively, e.g. ``(appstream-data if PackageKit)``,
``(kernel-rt-devel if kernel-rt-core)``).

``PackageQuery.is_dep_satisfied`` calls libsolv's
``pool_satisfieddep_map`` directly, which evaluates the full rich
grammar — ``if`` / ``unless`` / ``and`` / ``or`` / ``with`` /
``else`` — against the loaded universe. A conditional whose
trigger-side has no provider in the universe is correctly reported
as satisfied, because the consequence-side never fires. This is the
same call the upstream ``dnf5-plugins/repoclosure_plugin``
(``repoclosure.cpp``) makes, so our findings now match
``dnf5 repoclosure``'s own.

Tests do not import this directly — they consume the ``repoclosure``
fixture in ``conftest.py``.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

import pytest

from .known_violations import KnownViolationsMap, classify_violations
from .repos import Repo
from .types import NEVRA, RepoclosureResult

if TYPE_CHECKING:
    from .metadata import MetadataService

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Arch-set for the configured check_kind
# ---------------------------------------------------------------------------


_ARCH_SETS_BY_KIND: dict[str, tuple[str, ...]] = {
    # Each entry is the set of *additional* arches (beyond the test's
    # target arch) that the checker should examine.
    #
    # "binary"    — pure runtime closure of binary packages. Only
    #               packages of arch ∈ {target, noarch} are checked;
    #               source-arch packages are ignored.
    # "buildtime" — checks BOTH source packages (so an SRPM's
    #               BuildRequires must close) AND the binary packages
    #               that satisfy them (so the binary providers'
    #               runtime deps must also close — without this, a
    #               broken provider would silently still be considered
    #               a "valid" BuildRequires source). This is the
    #               correct kind for asserting that an SRPM repo is
    #               actually buildable against a binary universe.
    # "all"       — no arch filter; report findings for every package
    #               in the universe.
    "binary": ("noarch",),
    "buildtime": ("noarch", "src", "nosrc"),
    "all": (),
}


def _arches_to_check(check_kind: str, arch: str) -> set[str] | None:
    """Return the arches whose packages should be checked, or None for "all"."""
    if check_kind not in _ARCH_SETS_BY_KIND:
        raise ValueError(
            f"unknown check_kind: {check_kind!r}; "
            f"expected one of {sorted(_ARCH_SETS_BY_KIND)}"
        )
    if check_kind == "all":
        return None
    extras = _ARCH_SETS_BY_KIND[check_kind]
    return {arch, *extras}


# ---------------------------------------------------------------------------
# Repoclosure runner
# ---------------------------------------------------------------------------


class Repoclosure:
    """Run libdnf5-based repoclosure against a set of repos.

    Holds a reference to the :class:`MetadataService` only to share
    its workdir / xdist-worker scoping for the libdnf5-side cache.
    libdnf5 fetches its own copy of repomd/primary/filelists via its
    internal librepo handle (see ``_build_base`` for the rationale —
    the earlier "share MetadataService destdir as a ``file://``
    baseurl" trick fought both layers and was reverted). The
    duplicate fetch is roughly 10MB per repo, paid once per session.
    """

    def __init__(self, metadata_service: "MetadataService") -> None:
        self._metadata = metadata_service

    # ------------------------------------------------------------------
    # libdnf5 setup
    # ------------------------------------------------------------------

    def _libdnf5_cache_dir(self, arch: str) -> Path:
        """Per-arch cache dir for libdnf5's own metadata mirror.

        libdnf5 fetches repomd/primary/filelists/other/updateinfo into
        this directory the first time ``load_repos`` is called. Scoping
        by arch keeps multiple ``--arch`` runs from clobbering each
        other; scoping by xdist worker mirrors
        :meth:`MetadataService.cache_dir_for` so parallel workers never
        share a cache and never race on writes. Reused across
        :meth:`run` invocations so the second and later calls for the
        same arch hit a warm cache.
        """
        worker = os.environ.get("PYTEST_XDIST_WORKER", "main")
        return self._metadata._workdir / "libdnf5-cache" / worker / arch

    def _build_base(
        self,
        repos: list[Repo],
        arch: str,
    ) -> Any:
        """Build a fully loaded :class:`libdnf5.base.Base` for *repos* at *arch*.

        Each call produces a fresh ``Base`` because libdnf5 doesn't
        support reconfiguring an already-set-up Base. Callers that
        need to run several queries against the same universe should
        do so via the returned object rather than rebuilding.
        """
        from ._dnf_stack import get_libdnf5
        libdnf5 = get_libdnf5()

        base = libdnf5.base.Base()
        config = base.get_config()

        cache_dir = self._libdnf5_cache_dir(arch)
        cache_dir.mkdir(parents=True, exist_ok=True)
        config.get_cachedir_option().set(str(cache_dir))
        # /var/empty is owned by root and intentionally empty on
        # Fedora/AZL/RHEL; pointing installroot at it stops libdnf5
        # from reading the host's rpm db / dnf config / system
        # metadata and keeps the run hermetic. We never install
        # anything — Base is purely a query surface here.
        config.get_installroot_option().set("/var/empty")
        # Filelists are required because some packages in the repos
        # under test have file-path Requires (e.g. ``Requires:
        # /usr/bin/python3``) that only the filelists metadata can
        # satisfy. The same Option.add() pattern dnf5 itself uses.
        config.get_optional_metadata_types_option().add(
            libdnf5.conf.Option.Priority_RUNTIME, "filelists"
        )

        # Override the target architecture via Vars *before*
        # ``setup()``. libdnf5 derives the default ``arch`` /
        # ``basearch`` from the running kernel; without this override,
        # checking aarch64 closure on an x86_64 host would silently
        # filter out all aarch64 packages (because libsolv treats
        # foreign-arch solvables as uninstallable on the configured
        # arch). We set ``arch`` and ``basearch`` to the same value
        # because URL substitution and solver-arch checks each look
        # at one or the other (matching dnf5's own convention).
        vars_ = base.get_vars().get()
        vars_.set("arch", arch, libdnf5.conf.Vars.Priority_RUNTIME)
        vars_.set("basearch", arch, libdnf5.conf.Vars.Priority_RUNTIME)
        # When MetadataService was created with an explicit
        # releasever, propagate it into libdnf5 too so any
        # ``$releasever`` placeholder in a repo URL substitutes to
        # that value. Without this override, libdnf5 falls back to
        # its host-derived default (read from /etc/os-release on
        # the machine running the suite), which on a Fedora/RHEL
        # dev box checking an AZL repo silently substitutes the
        # wrong number and fetches the wrong tree.
        releasever = self._metadata._releasever
        if releasever is not None:
            vars_.set(
                "releasever", releasever, libdnf5.conf.Vars.Priority_RUNTIME
            )

        base.setup()

        repo_sack = base.get_repo_sack()
        for repo in repos:
            ld_repo = repo_sack.create_repo(repo.name)
            # Hand libdnf5 the original repo URL (with $basearch /
            # $releasever placeholders intact — libdnf5 substitutes
            # via the Vars we just set above) and let it fetch +
            # cache via its own librepo handle into the cachedir we
            # configured. Earlier revisions tried to share our
            # MetadataService.fetch() destdir as a ``file://`` baseurl
            # to avoid the second fetch, but that fights both layers:
            # libdnf5's internal librepo treats ``file://`` baseurl
            # as a remote mirror and (a) demands every record listed
            # in repomd.xml (other.xml.zst, updateinfo.xml.zst — not
            # what our fetch_repo asks for), and (b) refuses to start
            # if the destdir is already populated. The "double fetch"
            # is roughly 10MB per repo, paid once per session; the
            # win in fragility / clarity is well worth it.
            ld_repo.get_config().get_baseurl_option().set([repo.url])

        repo_sack.load_repos(libdnf5.repo.Repo.Type_AVAILABLE)
        return base

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(
        self,
        *,
        target_repos: list[Repo],
        arch: str,
        universe_repos: list[Repo] | None = None,
        check_kind: str = "binary",
    ) -> RepoclosureResult:
        """Run repoclosure and return the typed result.

        See :func:`utils.conftest.repoclosure` for argument semantics.
        """
        if not target_repos:
            raise ValueError("target_repos must be non-empty")
        if universe_repos is None:
            universe_repos = target_repos
        universe_names = {r.name for r in universe_repos}
        missing_targets = [
            r.name for r in target_repos if r.name not in universe_names
        ]
        if missing_targets:
            raise ValueError(
                f"target_repos {missing_targets} are not in universe_repos "
                f"{sorted(universe_names)}"
            )

        from ._dnf_stack import get_libdnf5
        libdnf5 = get_libdnf5()

        base = self._build_base(universe_repos, arch)

        # ``available_query`` is the set of providers the solver may
        # use to satisfy any dep — the full universe filtered to the
        # *latest EVR per name*. This matches ``dnf5 repoclosure``'s
        # default behaviour (``best=1``): the universe of "what dnf
        # would actually pick at install time" is what closure should
        # be evaluated against, not "any version that ever existed in
        # the repo". Without this filter, a partial-rebuild scenario
        # where a published repo carries N-1 of every subpackage but
        # only N for the parent would falsely close — the parent's
        # ``Requires: subpkg = N`` would resolve against the still-
        # present N-1 build of a peer subpackage, even though dnf
        # would never actually combine them. With the filter, the
        # mismatch surfaces (which is exactly what catches the
        # kernel/anaconda/azurelinux-release partial-rebuild bugs in
        # real Koji output).
        #
        # ``to_check_query`` is ALSO filtered to latest EVR per name,
        # which deviates from ``dnf5 repoclosure`` (it checks every
        # NEVRA). The deviation removes a class of stale-EVR noise:
        # when the published repo carries both N-1 and N of a
        # tightly-pinned package family (e.g. all of
        # ``azurelinux-release-*`` exists at both ``-12.azl4`` and
        # ``-13.azl4``), dnf5 reports the older ``-12.azl4`` set as
        # broken because the latest-EVR filter on the available side
        # leaves only ``-13.azl4`` peers — i.e. "you can no longer
        # downgrade to ``-12.azl4``". That is technically true but
        # not actionable: the repo's *latest installable* state is
        # the only thing closure is meant to validate. Filtering the
        # to-check side too means we only ask "what would
        # ``dnf install <pkg>`` actually pick, and does it close?".
        # This still catches the kernel/anaconda style
        # version-pinning bugs (those have a *single* EVR that pins
        # a *missing* peer, not an *older* EVR pinning an older but
        # present peer), so no real signal is lost.
        available_query = libdnf5.rpm.PackageQuery(base)
        available_query.filter_latest_evr()
        to_check_query = libdnf5.rpm.PackageQuery(base)

        # For "buildtime" we deliberately do NOT filter findings to
        # ``target_repos`` — see test_repoclosure_base_plus_sdk_full
        # for the rationale (we MUST surface broken runtime closure of
        # binary providers from non-target repos that satisfy a
        # checked SRPM's BuildRequires; otherwise the check is moot).
        if check_kind != "buildtime":
            to_check_query.filter_repo_id([r.name for r in target_repos])

        # Apply latest-EVR to the to-check side AFTER the repo
        # filter so "latest" means "latest EVR present in the
        # target repos", not "latest EVR anywhere in the universe".
        # In the universe == target case (every existing call site
        # today) the order doesn't matter, but the API contract
        # supports target ⊊ universe and the wrong order would
        # silently mask target-side findings whose universe peers
        # carry a higher EVR.
        to_check_query.filter_latest_evr()

        check_arches = _arches_to_check(check_kind, arch)
        if check_arches is not None:
            to_check_query.filter_arch(sorted(check_arches))

        # Cache reldep -> satisfied? by the libsolv reldep id. The
        # same reldep is shared across many packages, so this turns
        # an O(packages × deps) lookup loop into roughly O(distinct
        # reldeps) — exactly what dnf5's own repoclosure plugin does.
        resolved: dict[int, bool] = {}

        unresolved: dict[NEVRA, list[str]] = {}
        repos_by_nevra: dict[NEVRA, str] = {}

        for pkg in to_check_query:
            missing: list[str] = []
            for reldep in pkg.get_requires():
                rid = reldep.get_id().id
                cached = resolved.get(rid)
                if cached is None:
                    sat = available_query.is_dep_satisfied(reldep)
                    resolved[rid] = sat
                else:
                    sat = cached
                if not sat:
                    missing.append(reldep.to_string())
            if not missing:
                continue
            # Deduplicate while preserving order (a single Requires:
            # entry can appear more than once on a package via
            # weak-dep machinery in some upstream specs).
            seen: set[str] = set()
            unique_missing: list[str] = []
            for entry in missing:
                if entry in seen:
                    continue
                seen.add(entry)
                unique_missing.append(entry)

            epoch_str = pkg.get_epoch() or "0"
            try:
                epoch_int = int(epoch_str)
            except ValueError:
                epoch_int = 0
            nevra = NEVRA(
                name=pkg.get_name(),
                epoch=epoch_int,
                version=pkg.get_version(),
                release=pkg.get_release(),
                arch=pkg.get_arch(),
            )
            unresolved[nevra] = unique_missing
            repos_by_nevra[nevra] = pkg.get_repo_id()

        result = RepoclosureResult(
            target_repo_names=tuple(r.name for r in target_repos),
            arch=arch,
            unresolved=unresolved,
            repos_by_nevra=repos_by_nevra,
        )
        logger.debug(
            "repoclosure(%s, arch=%s, kind=%s): %d unresolved package(s)",
            result.target_repo_names, arch, check_kind, len(unresolved),
        )
        return result


def make_repoclosure(metadata_service: "MetadataService") -> Repoclosure:
    """Construct a :class:`Repoclosure`.

    libdnf5 availability is checked lazily on first use (via
    :func:`utils._dnf_stack.get_libdnf5`) — the resulting
    :class:`MissingDependencyError` carries an actionable install
    message — so we don't probe at construction time. Doing so here
    would run during fixture setup for *every* invocation, including
    sessions that select only metadata-only tests and never actually
    need libdnf5.
    """
    return Repoclosure(metadata_service)


def assert_known_violations(
    result: RepoclosureResult,
    arch: str,
    known_violations: KnownViolationsMap,
    *,
    subtests,
    dep_kind: str = "dep",
    source_label: str = "the known-violations file",
    recorder: Callable[..., None],
) -> None:
    """Classify a :class:`RepoclosureResult` against an allowlist and
    emit subtests for the four outcomes (real failure, known
    violation / xfail, stale-consumer, stale-dep).

    ``known_violations`` is keyed by consumer name (no
    epoch/version/release/arch). Each value is either a flat
    ``frozenset[str]`` of permitted missing-dep strings (applies on
    every arch) or a ``Mapping[arch_name, Iterable[str]]`` (applies
    only on the listed arches; on other arches the consumer is
    treated as absent from the allowlist).

    ``dep_kind`` is the human word used in failure / xfail messages
    (e.g. ``"dep"`` for build-time, ``"runtime dep"`` for runtime).

    ``source_label`` is the human-readable origin used in failure
    messages (e.g. a path + section like
    ``"cases/known-violations/test_foo.toml [runtime-missing]"``)
    so the curator knows where to add or remove an entry. Defaults
    to a generic placeholder when the caller didn't pass one.

    ``recorder`` is required (keyword-only). It is called once with
    ``arch=arch, source_label=source_label, classified=<result>``
    *before* any subtests are emitted, so the structured-summary
    JSON sees every classification regardless of how many subtests
    later xfail or fail. Pass the ``summary_recorder`` fixture
    (defined in ``conftest.py``); when ``--summary-json`` is unset
    the fixture is a no-op-but-callable, so callers don't have to
    branch.

    The four-way classification itself is delegated to
    :func:`utils.known_violations.classify_violations`. This wrapper
    is the per-NEVRA emission layer: subtest-key shape
    (``package=str(NEVRA), arch=arch``) and per-finding message
    rendering (with the ``(from <repo>)`` annotation pulled from
    ``result.repos_by_nevra``) are repoclosure-specific.
    """
    classified = classify_violations(
        findings={
            nevra: tuple(missing) for nevra, missing in result.unresolved.items()
        },
        consumer_of=lambda nevra: nevra.name,
        arch=arch,
        allowlist=known_violations,
    )

    recorder(arch=arch, source_label=source_label, classified=classified)

    def _meta_suffix(v) -> str:
        # Per-entry metadata (ST2). Surface in subtest message bodies
        # only -- subtest IDs stay stable so they remain diff-targets.
        bits: list[str] = []
        if v.reason:
            bits.append(f"reason: {v.reason}")
        if v.issue:
            bits.append(f"tracked: {v.issue}")
        return "\n[" + "; ".join(bits) + "]" if bits else ""

    for v in sorted(classified.real_fails, key=lambda v: str(v.key)):
        nevra = v.key
        repo = result.repos_by_nevra.get(nevra)
        suffix = f" (from {repo!r})" if repo else ""
        with subtests.test(package=str(nevra), arch=arch):
            if v.listed is None:
                pytest.fail(
                    f"{nevra}{suffix} has unresolved {dep_kind}(s) "
                    f"and the consumer name is not yet listed in "
                    f"{source_label}:\n"
                    + "\n".join(f"  - {d}" for d in sorted(v.observed))
                    + f"\n\nAdd a {nevra.name!r} entry to "
                    f"{source_label} if intentional."
                )
            new_deps = sorted(v.observed - v.listed)
            pytest.fail(
                f"{nevra}{suffix} has unresolved {dep_kind}(s):\n"
                + "\n".join(f"  - {d}" for d in sorted(v.observed))
                + f"\n\nNew (un-allowlisted) {dep_kind}(s) for "
                f"{nevra.name!r} -- extend its entry in "
                f"{source_label} if intentional:\n"
                + "\n".join(f"  - {d}" for d in new_deps)
                + _meta_suffix(v)
            )

    for v in sorted(classified.known_violations, key=lambda v: str(v.key)):
        nevra = v.key
        repo = result.repos_by_nevra.get(nevra)
        suffix = f" (from {repo!r})" if repo else ""
        with subtests.test(package=str(nevra), arch=arch):
            pytest.xfail(
                f"known violation -- missing {dep_kind}(s) (tracked "
                f"in {source_label} under {nevra.name!r}): "
                f"{nevra}{suffix}:\n"
                + "\n".join(f"  - {d}" for d in sorted(v.observed))
                + _meta_suffix(v)
            )

    for entry in classified.stale:
        if entry.kind == "stale-consumer":
            with subtests.test(
                consumer=entry.consumer, arch=arch, kind="stale-consumer",
            ):
                pytest.fail(
                    f"consumer {entry.consumer!r} is listed in "
                    f"{source_label} but no NEVRA of that name is "
                    f"reporting unresolved deps on {arch}. Please "
                    f"remove the entry."
                )
        else:
            with subtests.test(
                consumer=entry.consumer, missing_dep=entry.listed_dep,
                arch=arch, kind="stale-dep",
            ):
                pytest.fail(
                    f"dep {entry.listed_dep!r} is listed in "
                    f"{source_label} under {entry.consumer!r} but is "
                    f"no longer reported as missing for any NEVRA of "
                    f"{entry.consumer!r} on {arch}. Please remove "
                    f"that dep from the entry."
                )
