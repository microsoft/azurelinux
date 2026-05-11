# SPDX-License-Identifier: MIT
"""Repo definitions and CLI parsing.

Three input forms are supported, all produce a list of :class:`Repo`:

1. ``--repos-file path.repo`` — a standard yum/dnf ``.repo`` ini file.
   The file is parsed with :mod:`configparser`. Each section becomes
   one repo; required keys are ``baseurl``, plus a custom ``kind``
   key (``binary`` / ``srpm`` / ``debuginfo``) since the dnf format
   has no equivalent. The section name is the repo name.

2. ``--repo name=...,kind=...,url=...`` — inline form for ad-hoc
   invocations and CI matrix jobs that don't want to ship a separate
   .repo file.

3. ``--repo-prefix URL`` — convenience shorthand: the URL is assumed
   to host the *Standard Azure Linux Repo Layout* (the same layout
   produced by ``scripts/synthesize-repodata.py``). The prefix is
   expanded into the six conventional sub-repos (``base`` / ``sdk``
   binary, debuginfo, and srpms); each is probed and ones that 404
   are silently dropped. Use this when you just want to point the
   suite at a published mirror without spelling out every URL.

All three forms accept ``$basearch`` / ``$arch`` / ``$releasever``
in URLs; substitution happens at fetch time inside librepo.
"""

from __future__ import annotations

import configparser
import errno
import hashlib
import logging
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from .types import ALL_REPO_KINDS, RepoKind

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Repo:
    """A logical repository under test.

    The ``fingerprint`` is a stable short hash that uniquely identifies
    this repo for cache-keying purposes. It does NOT cover ``arch`` or
    ``releasever`` — those live in cache-path components above the repo
    fingerprint, so the same repo's metadata across two arches lands in
    two different cache subdirs.
    """

    name: str
    kind: RepoKind
    url: str

    @property
    def fingerprint(self) -> str:
        """Stable short hash over (name, kind, url) for cache paths."""
        h = hashlib.sha256()
        h.update(self.name.encode())
        h.update(b"\0")
        h.update(self.kind.encode())
        h.update(b"\0")
        h.update(self.url.encode())
        return h.hexdigest()[:16]


class RepoSpecError(ValueError):
    """Raised when a ``--repo`` flag value or repos-file is malformed."""


_REQUIRED_KEYS = ("name", "kind", "url")


def _validate(name: str, kind: str, url: str, source: str) -> Repo:
    if not name:
        raise RepoSpecError(f"{source}: name must be non-empty")
    if kind not in ALL_REPO_KINDS:
        raise RepoSpecError(
            f"{source}: kind {kind!r} is invalid; "
            f"must be one of {', '.join(ALL_REPO_KINDS)}"
        )
    if not url:
        raise RepoSpecError(f"{source}: url must be non-empty")
    return Repo(name=name, kind=kind, url=url)  # type: ignore[arg-type]


def parse_repo_spec(raw: str) -> Repo:
    """Parse a ``--repo name=...,kind=...,url=...`` value into a :class:`Repo`.

    The first ``=`` in each comma-segment separates key from value, so
    URLs containing ``=`` are tolerated. Keys are case-sensitive.
    """
    if not raw or not raw.strip():
        raise RepoSpecError("--repo value is empty")
    fields: dict[str, str] = {}
    for segment in raw.split(","):
        segment = segment.strip()
        if not segment:
            continue
        if "=" not in segment:
            raise RepoSpecError(
                f"--repo segment {segment!r} is not of the form key=value"
            )
        key, _, value = segment.partition("=")
        key, value = key.strip(), value.strip()
        if not key:
            raise RepoSpecError(f"--repo segment {segment!r} has empty key")
        if key in fields:
            raise RepoSpecError(f"--repo key {key!r} specified twice")
        fields[key] = value

    missing = [k for k in _REQUIRED_KEYS if k not in fields]
    if missing:
        raise RepoSpecError(
            f"--repo {raw!r} is missing required key(s): {', '.join(missing)}"
        )
    extra = sorted(set(fields) - set(_REQUIRED_KEYS))
    if extra:
        raise RepoSpecError(
            f"--repo {raw!r} has unknown key(s): {', '.join(extra)}. "
            f"Allowed: {', '.join(_REQUIRED_KEYS)}."
        )
    return _validate(fields["name"], fields["kind"], fields["url"], f"--repo {raw!r}")


def parse_repos_file(path: Path) -> list[Repo]:
    """Parse a ``.repo``-style ini file into a list of :class:`Repo`.

    The format is the standard yum/dnf one with one extension: every
    section MUST include a ``kind`` key (one of ``binary`` / ``srpm`` /
    ``debuginfo``) since the dnf format has no equivalent.

    Example::

        [base]
        name=Azure Linux base
        baseurl=https://example.com/base/$basearch/
        kind=binary

        [base-srpms]
        baseurl=https://example.com/base-srpms/
        kind=srpm

    The repo name is taken from the section header (``[base]``); the
    optional ``name=`` key is ignored (kept only for compatibility
    with hand-edited dnf .repo files).
    """
    cp = configparser.ConfigParser(interpolation=None)
    try:
        with open(path) as fh:
            cp.read_file(fh)
    except (OSError, configparser.Error) as exc:
        raise RepoSpecError(f"failed to read --repos-file {path}: {exc}") from exc

    repos: list[Repo] = []
    seen: set[str] = set()
    for section in cp.sections():
        if section in seen:
            raise RepoSpecError(
                f"--repos-file {path}: section [{section}] appears twice"
            )
        seen.add(section)
        url = cp[section].get("baseurl", "").strip()
        kind = cp[section].get("kind", "").strip()
        repos.append(_validate(
            section, kind, url, f"--repos-file {path} [{section}]"
        ))
    return repos


def collect_repos(
    *,
    inline: list[str],
    file_paths: list[str],
    prefixes: list[str] | None = None,
    probe_arch: str = "x86_64",
    probe_timeout: float = 10.0,
) -> list[Repo]:
    """Combine inline ``--repo``, ``--repos-file`` and ``--repo-prefix`` inputs.

    Repo *names* must be globally unique across all inputs (regardless
    of source). Earlier versions of this code allowed two repos to
    share a base name as long as their kinds differed, but that
    invariant proved unenforceable downstream:

    * the rendered ``.repo`` file uses ``[name]`` as the section
      header — duplicate sections cause dnf to merge or reject;
    * fixture lookups (``require_named_repos``, repoclosure result
      attribution) key on name alone and silently overwrote the
      earlier entry;
    * dnf5 ``repoclosure --json`` reports source repos by name only,
      so per-repo filtering can't disambiguate same-named binary vs
      srpm repos.

    The conventional naming is ``base`` for the binary repo and
    ``base-srpms`` for the matching SRPM repo — distinct names, no
    behaviour change for well-formed inputs.

    Precedence rules:

    * Two explicit definitions (``--repo`` / ``--repos-file``) for the
      same name are an error — the user almost certainly didn't mean
      to typo a name twice with different URLs.
    * An explicit definition silently *overrides* a same-name
      definition that came from ``--repo-prefix`` expansion. This lets
      you point at a published prefix for the bulk of the layout while
      pinning one channel (e.g., a development SDK) to a different
      URL.
    * Two ``--repo-prefix`` flags producing the same conventional name
      are an error (the prefixes would shadow each other).
    """
    repos: list[Repo] = []
    explicit_seen: dict[str, str] = {}
    prefix_seen: dict[str, str] = {}

    def _add_explicit(repo: Repo, source: str) -> None:
        if repo.name in explicit_seen:
            raise RepoSpecError(
                f"repo name={repo.name!r} specified more than once "
                f"(previously: {explicit_seen[repo.name]!r}, now: {source!r}). "
                f"Repo names must be globally unique — pick distinct "
                f"names (e.g. 'base' for the binary repo and "
                f"'base-srpms' for the matching SRPM repo)."
            )
        explicit_seen[repo.name] = source
        repos.append(repo)

    def _add_prefix(repo: Repo, source: str) -> None:
        if repo.name in prefix_seen:
            raise RepoSpecError(
                f"--repo-prefix name={repo.name!r} produced by more than one "
                f"prefix (previously: {prefix_seen[repo.name]!r}, now: "
                f"{source!r}). Each conventional sub-repo name must come "
                f"from at most one prefix; drop one --repo-prefix or use "
                f"explicit --repo for the conflicting entry."
            )
        prefix_seen[repo.name] = source
        repos.append(repo)

    for raw in inline:
        _add_explicit(parse_repo_spec(raw), f"--repo {raw!r}")
    for fp in file_paths:
        for r in parse_repos_file(Path(fp)):
            _add_explicit(r, f"--repos-file {fp} [{r.name}]")
    for prefix in prefixes or []:
        for r in expand_repo_prefix(
            prefix, probe_arch=probe_arch, probe_timeout=probe_timeout,
        ):
            if r.name in explicit_seen:
                logger.info(
                    "--repo-prefix %r: skipping conventional sub-repo %r "
                    "(overridden by %s)",
                    prefix, r.name, explicit_seen[r.name],
                )
                continue
            _add_prefix(r, f"--repo-prefix {prefix!r} -> {r.name}")

    return repos


# ---------------------------------------------------------------------------
# --repo-prefix: probe the Standard Azure Linux Repo Layout
# ---------------------------------------------------------------------------


# The fixed Standard Azure Linux Repo Layout (two channels x three kinds,
# yielding six conventional sub-repos) is loaded from the canonical
# ``base/packages/repo-layout.json`` via :mod:`utils.repo_layout`. The
# loader runs structural validation at import time so a malformed
# layout file fails immediately rather than producing mysterious
# downstream errors. The same JSON is consumed by
# ``scripts/synthesize-repodata.py`` and ``scripts/dnf-with-azl-repos``
# so the layout is described in exactly one place.
from .repo_layout import load_repo_layout

_PREFIX_LAYOUT = load_repo_layout().subrepos


def _probe_repomd(repo_url: str, *, timeout: float) -> bool:
    """Return True if ``<repo_url>/repodata/repomd.xml`` is present.

    For HTTP(S) URLs: returns True on a 2xx response, False on a clean
    404 (the conventional "this sub-repo is not published" signal). Any
    other HTTP/network error is fatal — raising :class:`RepoSpecError` —
    because we cannot tell the difference between "skip, this isn't
    published" and "the user typo'd a hostname / the network is down" in
    a way that is safe to treat as a silent skip.

    For ``file://`` URLs: returns True if the file exists, False if it
    doesn't. Any other OSError (permission denied, bad path, etc.) is
    fatal.

    HEAD is preferred for HTTP (cheap; ``repomd.xml`` is small but
    compounding over six probes per prefix it adds up). A handful of
    static-file hosts return 405/501 for HEAD; we transparently retry
    as GET in that case.
    """
    repomd_url = repo_url.rstrip("/") + "/repodata/repomd.xml"
    scheme = urllib.parse.urlparse(repomd_url).scheme.lower()
    # ``file://`` URLs go through ``urllib`` but don't speak HTTP, so
    # ``resp.status`` is ``None`` and missingness surfaces as ``URLError``
    # wrapping ``FileNotFoundError``. Handle them via a direct filesystem
    # check instead — clearer, and avoids the HEAD/GET retry dance.
    if scheme == "file":
        local_path = urllib.request.url2pathname(
            urllib.parse.urlparse(repomd_url).path
        )
        try:
            return Path(local_path).is_file()
        except OSError as exc:
            raise RepoSpecError(
                f"--repo-prefix probe of {repomd_url!r} failed: {exc}"
            ) from exc
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(repomd_url, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                if status is None:
                    # Non-HTTP scheme that succeeded: treat the successful
                    # open as proof of existence (e.g. ftp://).
                    return True
                return 200 <= status < 300
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return False
            if exc.code in (405, 501) and method == "HEAD":
                # Server doesn't support HEAD — fall through to GET.
                continue
            raise RepoSpecError(
                f"--repo-prefix probe of {repomd_url!r} failed: "
                f"HTTP {exc.code} {exc.reason}"
            ) from exc
        except urllib.error.URLError as exc:
            # Non-HTTP backends (e.g. file://, ftp://) report a missing
            # target via URLError wrapping the underlying OSError. Treat
            # that as "not present" so prefix expansion can silently skip
            # the sub-repo, mirroring the HTTP 404 path. Anything else is
            # fatal.
            reason = exc.reason
            if (isinstance(reason, OSError)
                    and reason.errno == errno.ENOENT):
                return False
            raise RepoSpecError(
                f"--repo-prefix probe of {repomd_url!r} failed: {reason}"
            ) from exc
    # Both HEAD and GET were attempted without raising; treat as missing.
    return False


def expand_repo_prefix(
    prefix: str, *, probe_arch: str, probe_timeout: float = 10.0,
) -> list[Repo]:
    """Expand a single ``--repo-prefix`` URL into existing conventional repos.

    The Standard Azure Linux Repo Layout is::

        <prefix>/base/<arch>/                 -> base           (binary)
        <prefix>/base/debuginfo/<arch>/       -> base-debuginfo (debuginfo)
        <prefix>/base/srpms/                  -> base-srpms     (srpm)
        <prefix>/sdk/<arch>/                  -> sdk            (binary)
        <prefix>/sdk/debuginfo/<arch>/        -> sdk-debuginfo  (debuginfo)
        <prefix>/sdk/srpms/                   -> sdk-srpms      (srpm)

    Each of the six is probed for ``repodata/repomd.xml``; entries
    that 404 are silently skipped. For binary / debuginfo, the probe
    URL uses *probe_arch* as a sentinel (typically the first
    ``--arch``); the registered :class:`Repo` keeps the ``$basearch``
    placeholder so it still fans out across every ``--arch`` at test
    time. If a particular arch isn't actually published under the
    prefix, that arch will fail at fetch time — use explicit
    ``--repo`` for asymmetric layouts.

    Raises :class:`RepoSpecError` if *all* six sub-repos 404 — the
    prefix itself is presumed bogus / mis-typed in that case, since a
    real Azure Linux mirror will publish at least one of them.
    """
    base = prefix.rstrip("/")
    if not base:
        raise RepoSpecError("--repo-prefix value is empty")

    found: list[Repo] = []
    for sub in _PREFIX_LAYOUT:
        repo_url = f"{base}/{sub.subpath}"
        # Substitute $basearch with the probing arch for the presence check
        # only; the registered Repo keeps the placeholder so librepo can
        # expand it per-arch at fetch time.
        probe_url = repo_url.replace("$basearch", probe_arch)
        logger.debug("--repo-prefix: probing %s", probe_url)
        if _probe_repomd(probe_url, timeout=probe_timeout):
            logger.info(
                "--repo-prefix %r: found %s -> %s", prefix, sub.name, repo_url,
            )
            found.append(Repo(name=sub.name, kind=sub.kind, url=repo_url))  # type: ignore[arg-type]
        else:
            logger.info(
                "--repo-prefix %r: skipping %s (no repodata/repomd.xml at %s)",
                prefix, sub.name, probe_url,
            )

    if not found:
        raise RepoSpecError(
            f"--repo-prefix {prefix!r}: none of the {len(_PREFIX_LAYOUT)} "
            f"conventional Azure Linux sub-repos were found under this "
            f"prefix (probed with arch={probe_arch!r}). Verify the URL "
            f"points at the root of a published Azure Linux repo tree."
        )
    return found
