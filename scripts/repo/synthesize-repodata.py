#!/usr/bin/env python3
"""Route packages from one or more upstream RPM repos into the standard
Azure Linux per-channel/per-arch layout.

Reads multiple input RPM repositories (with `$basearch` expansion), unions
their packages, asks `azldev package list --rpm-file ...` to assign each
package to a publish channel, then writes per-channel/per-arch repodata
under the Standard Azure Linux Repo Layout:

    <out>/base/<arch>/                # main binary RPMs, base channel
    <out>/base/debuginfo/<arch>/      # debuginfo/debugsource, base channel
    <out>/base/srpms/                 # source RPMs, base channel
    <out>/sdk/<arch>/                 # main binary RPMs, sdk channel
    <out>/sdk/debuginfo/<arch>/       # debuginfo/debugsource, sdk channel
    <out>/sdk/srpms/                  # source RPMs, sdk channel

Each emitted repo's `<location href>` references the original upstream RPM
URL (so consumers download from the source repos).

Two input-flag flavours, both repeatable and mixable:

  --repo-prefix URL
      Shorthand: assume URL is the prefix of a Standard Azure Linux Repo
      Layout (i.e. the directory above `base/` and `sdk/`). The script
      enumerates all six sub-repos under it and tolerates 404s on any of
      them (silently skipped).

  --repo TYPE:URL              (TYPE in {main, debuginfo, srpms})
      Explicit single repo. URL may contain `$basearch`, expanded to each
      configured arch. 404s on explicit repos are fatal.

Dependencies: python3-createrepo_c, azldev, dnf
"""

from __future__ import annotations

import argparse
import contextlib
import json
import shutil
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import createrepo_c as cr

# `_repo_layout` is a sibling module in this directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _repo_layout import (  # noqa: E402
    ALL_KINDS,
    CHANNELS,
    KIND_DEBUGINFO,
    KIND_MAIN,
    KIND_SRPMS,
    SUBREPOS,
)

# Repo root: this file lives at <repo>/scripts/repo/<name>.py, so the
# project root is three parents up.
DEFAULT_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_ARCHES = ("x86_64", "aarch64")
SRPM_ARCH = "src"
CHANNEL_PREFIX = "rpm-"
# The fixed Standard Azure Linux Repo Layout has exactly two output channels.
# Anything else returned by azldev is treated as unpublished (and reported).
ALLOWED_OUTPUT_CHANNELS = frozenset(CHANNELS)

# HTTP knobs for repodata fetches.
USER_AGENT = "synthesize-repodata/1"
HTTP_TIMEOUT = 60.0
HTTP_RETRIES = 3
HTTP_BACKOFF_BASE = 1.0     # seconds; doubled per attempt.

# repomd record types we generate ourselves in the output. The synth
# tool only emits these — auxiliary records (updateinfo, group,
# group_gz, modules, ...) are intentionally NOT propagated because the
# routing decisions can split a contributing input's packages across
# destinations, so blindly copying e.g. a groupfile that references
# packages by NEVRA would mis-reference packages routed elsewhere.
# Consumers who need updateinfo/groups should fetch them from the
# upstream repos directly (e.g. via a layered repo config) rather
# than relying on the synth output.
PACKAGE_RECORD_TYPES = frozenset({
    "primary", "filelists", "other",
    "primary_db", "filelists_db", "other_db",
})

# When the Phase-4 channel-inheritance fallback finds two or more channels
# tied for the top spot among a component's published sibling rpms, prefer
# this one explicitly rather than letting the decision fall out of a lex
# sort over ALLOWED_OUTPUT_CHANNELS. The pick is still surfaced in the
# decision's reason string AND a per-decision ``tie_break_used`` flag, and
# decide_routing emits a WARN log once per tied component, so the case is
# never silently masked.
INHERITANCE_TIE_BREAK_DEFAULT = "base"


# ---------------------------------------------------------------------------
# Logging helpers (everything goes to stderr; stdout left clean)
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def warn(msg: str) -> None:
    print(f"WARN: {msg}", file=sys.stderr, flush=True)


def fatal(msg: str) -> int:
    print(f"ERROR: {msg}", file=sys.stderr, flush=True)
    return 1


# ---------------------------------------------------------------------------
# Input-repo modelling
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class InputRepo:
    """One concrete (post-`$basearch`-expansion) upstream repo to ingest."""

    kind: str            # main | debuginfo | srpms
    arch: str            # x86_64 | aarch64 | src
    url: str             # e.g. https://.../base/x86_64
    origin: str          # 'prefix' (404 silent) | 'explicit' (404 fatal)

    def cache_key(self) -> str:
        # Stable, filesystem-safe; uniqueness comes from the full URL.
        safe = self.url.replace("://", "_").replace("/", "_").replace(":", "_")
        return f"{self.kind}-{self.arch}-{safe}"


def expand_repo_prefix(prefix: str, arches: Iterable[str]) -> list[InputRepo]:
    base = prefix.rstrip("/")
    out: list[InputRepo] = []
    for sub in SUBREPOS:
        if sub.per_arch:
            for arch in arches:
                out.append(InputRepo(
                    sub.kind, arch,
                    f"{base}/{sub.subpath.replace('$basearch', arch)}",
                    "prefix",
                ))
        else:
            out.append(InputRepo(
                sub.kind, SRPM_ARCH, f"{base}/{sub.subpath}", "prefix",
            ))
    return out


def parse_explicit_repo(spec: str, arches: Iterable[str]) -> list[InputRepo]:
    """Parse `--repo TYPE:URL` into one or more InputRepos.

    URL handling for `main` and `debuginfo`:
      * If URL contains `$basearch`, expand it once per arch in *arches*.
      * Otherwise, the URL is taken as a single-arch repo and the arch is
        inferred from the URL's final path segment (which must match one
        of *arches*). Pass `--arch <arch>` with a single value to control
        which arch list this is matched against.

    `srpms` URLs are arch-agnostic and rejected if they contain `$basearch`.
    """
    if ":" not in spec:
        raise ValueError(
            f"--repo {spec!r}: expected TYPE:URL where TYPE in "
            f"{{{', '.join(ALL_KINDS)}}}"
        )
    kind, url = spec.split(":", 1)
    kind = kind.strip().lower()
    url = url.strip()
    if kind not in ALL_KINDS:
        raise ValueError(
            f"--repo {spec!r}: unknown TYPE {kind!r}; expected one of "
            f"{{{', '.join(ALL_KINDS)}}}"
        )
    if kind == KIND_SRPMS:
        if "$basearch" in url:
            raise ValueError(
                f"--repo {spec!r}: srpms repos are arch-agnostic; "
                f"`$basearch` is not allowed in the URL"
            )
        return [InputRepo(KIND_SRPMS, SRPM_ARCH, url.rstrip("/"), "explicit")]
    out: list[InputRepo] = []
    if "$basearch" in url:
        for arch in arches:
            out.append(InputRepo(
                kind, arch, url.replace("$basearch", arch).rstrip("/"),
                "explicit",
            ))
    else:
        # No $basearch: caller is asserting "this URL is for one specific
        # arch". We can't tell which from the URL alone, so we infer from the
        # last path component if it matches a known arch; otherwise refuse.
        # Strip query/fragment first so signed URLs (`...?sig=...`) don't
        # poison the inference.
        parts = urllib.parse.urlsplit(url)
        path = parts.path.rstrip("/")
        last = path.rsplit("/", 1)[-1] if path else ""
        if last in arches:
            out.append(InputRepo(kind, last, url.rstrip("/"), "explicit"))
        else:
            raise ValueError(
                f"--repo {spec!r}: URL has no `$basearch` and its final path "
                f"component {last!r} is not a known arch ({', '.join(arches)}); "
                f"cannot determine arch"
            )
    return out


def dedup_input_repos(repos: Iterable[InputRepo]) -> list[InputRepo]:
    """Drop duplicate (kind, arch, url) entries, preserving order. Explicit
    origin wins over prefix origin so 404s remain fatal where the user asked
    for them explicitly."""
    seen: dict[tuple[str, str, str], InputRepo] = {}
    for r in repos:
        key = (r.kind, r.arch, r.url)
        existing = seen.get(key)
        if existing is None:
            seen[key] = r
        elif r.origin == "explicit" and existing.origin == "prefix":
            seen[key] = r
    return list(seen.values())


# ---------------------------------------------------------------------------
# Phase 1: download repodata
# ---------------------------------------------------------------------------

def _http_get(
    url: str, dest: Path, ssl_context: ssl.SSLContext | None,
    *, timeout: float = HTTP_TIMEOUT, retries: int = HTTP_RETRIES,
) -> None:
    """Download *url* to *dest* with timeout, User-Agent, and bounded retry.

    Retries on TimeoutError / OSError / URLError and on HTTP 5xx; bails
    immediately on HTTP 4xx and on permanent local-fs errors
    (``FileNotFoundError`` wrapped in URLError, e.g. for ``file://``
    URLs that point at a missing file) so the caller can react
    (e.g. silently skip 404 / ENOENT from a prefix-derived sub-repo).
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_exc: BaseException | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(
                req, timeout=timeout, context=ssl_context,
            ) as resp, open(dest, "wb") as fh:
                shutil.copyfileobj(resp, fh)
            return
        except urllib.error.HTTPError as e:
            if 500 <= e.code < 600 and attempt < retries - 1:
                last_exc = e
                log(f"    HTTP {e.code} fetching {url}; retrying")
                time.sleep(HTTP_BACKOFF_BASE * (2 ** attempt))
                continue
            raise
        except urllib.error.URLError as e:
            if isinstance(e.reason, FileNotFoundError):
                raise
            if attempt < retries - 1:
                last_exc = e
                log(f"    URL error fetching {url} ({e.reason}); retrying")
                time.sleep(HTTP_BACKOFF_BASE * (2 ** attempt))
                continue
            raise
        except (TimeoutError, OSError) as e:
            if attempt < retries - 1:
                last_exc = e
                log(f"    transport error fetching {url} ({e}); retrying")
                time.sleep(HTTP_BACKOFF_BASE * (2 ** attempt))
                continue
            raise
    # Defensive: loop only exits via return/raise above.
    if last_exc is not None:
        raise last_exc


# ---------------------------------------------------------------------------
# SSL configuration
# ---------------------------------------------------------------------------

def build_ssl_context(ca_bundle: Path | None, insecure: bool) -> ssl.SSLContext | None:
    """Return an SSLContext honouring --ca-bundle / --insecure, or None for
    Python's default behaviour.
    """
    if insecure:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        warn("TLS certificate verification disabled (--insecure); "
             "connections are NOT authenticated")
        return ctx
    if ca_bundle is not None:
        ctx = ssl.create_default_context(cafile=str(ca_bundle))
        log(f"    using custom CA bundle: {ca_bundle}")
        return ctx
    return None


def download_repo_metadata(
    repo: InputRepo, cache_root: Path,
    ssl_context: ssl.SSLContext | None,
) -> Path | None:
    """Download every record listed in *repo*'s repomd into a cache dir.

    We pull primary/filelists/other for the package universe AND every
    auxiliary record (updateinfo, group, modules, ...) so phase 6 can
    copy non-package metadata through to routed destinations.

    Returns the path to the dir containing ``repodata/``, or None if
    the repo's ``repomd.xml`` returned 404 and *repo* was prefix-derived
    (silent skip). Other HTTP errors and explicit-origin 404s raise.
    """
    cache_dir = cache_root / repo.cache_key()
    repodata_dir = cache_dir / "repodata"
    repodata_dir.mkdir(parents=True, exist_ok=True)

    repomd_url = urllib.parse.urljoin(repo.url.rstrip("/") + "/",
                                      "repodata/repomd.xml")
    repomd_path = repodata_dir / "repomd.xml"
    log(f"  fetching {repomd_url}")
    try:
        _http_get(repomd_url, repomd_path, ssl_context)
    except urllib.error.HTTPError as e:
        if e.code == 404 and repo.origin == "prefix":
            log(f"    -> 404, skipping (prefix-derived, non-fatal)")
            shutil.rmtree(cache_dir, ignore_errors=True)
            return None
        raise
    except urllib.error.URLError as e:
        # ``file://`` URLs surface a missing file as
        # URLError(FileNotFoundError) rather than HTTPError(404); treat
        # that as the local-fs equivalent so prefix-derived sub-repos
        # under ``file://`` fixtures are silently skipped just like 404s.
        if (
            isinstance(e.reason, FileNotFoundError)
            and repo.origin == "prefix"
        ):
            log(f"    -> not found, skipping (prefix-derived, non-fatal)")
            shutil.rmtree(cache_dir, ignore_errors=True)
            return None
        raise

    repomd = cr.Repomd()
    cr.xml_parse_repomd(str(repomd_path), repomd, lambda *_: True)

    base = repo.url.rstrip("/") + "/"
    for record in repomd.records:
        # Only fetch the records we'll actually consume (primary,
        # filelists, other, plus their _db variants). See
        # PACKAGE_RECORD_TYPES above for why we skip aux records.
        if record.type not in PACKAGE_RECORD_TYPES:
            continue
        href = record.location_href or ""
        if not href:
            continue
        url = urllib.parse.urljoin(base, href)
        # Constrain the cache destination path so a hostile/malformed
        # repomd can't write outside cache_dir.
        safe_rel = href.lstrip("/")
        if ".." in Path(safe_rel).parts:
            raise RuntimeError(
                f"refusing to write metadata record outside cache: {href!r}"
            )
        dest = cache_dir / safe_rel
        log(f"  fetching {url}")
        _http_get(url, dest, ssl_context)
    return cache_dir


# ---------------------------------------------------------------------------
# Phase 2: build the package universe + RPM source map
# ---------------------------------------------------------------------------

# Universe key: (repo_kind, repo_arch, pkg_name, pkg_epoch, pkg_version,
# pkg_release, pkg_arch). The first two fields identify the destination
# (channel/arch) slot; the last five form the package's NEVRA so that two
# different versions of the same package occupy different slots and are both
# preserved in the output.
UniverseKey = tuple[str, str, str, str, str, str, str]


@dataclass
class UniverseEntry:
    """One NEVRA slot in the unioned package universe (one entry per
    distinct package version)."""

    repo: InputRepo
    source_pkg_name: str  # extracted from rpm_sourcerpm (or pkg name for srpms)


def _pkg_identity(pkg) -> tuple[str, str, str, str, str]:
    """Return the package's NEVRA tuple (name, epoch, version, release, arch).

    Epoch is normalised to '0' when missing/empty so two records that differ
    only by `epoch=None` vs `epoch="0"` compare equal.
    """
    return (pkg.name, pkg.epoch or "0", pkg.version, pkg.release, pkg.arch)


def _format_nevra(pkg) -> str:
    """Return a human-readable NEVRA string, suitable for log/warn messages."""
    epoch = pkg.epoch or "0"
    epoch_prefix = f"{epoch}:" if epoch != "0" else ""
    return f"{pkg.name}-{epoch_prefix}{pkg.version}-{pkg.release}.{pkg.arch}"


def _strip_srpm_suffix(rpm_sourcerpm: str | None) -> str:
    """Extract the source-package name from an RPM's `<sourcerpm>` field.

    Example: `bash-5.2.21-1.azl4.src.rpm` -> `bash`.
    """
    if not rpm_sourcerpm:
        return ""
    s = rpm_sourcerpm
    if s.endswith(".src.rpm"):
        s = s[: -len(".src.rpm")]
    # Strip -release then -version (best-effort; matches the inspiration
    # script's approach).
    parts = s.rsplit("-", 2)
    if len(parts) >= 3:
        return parts[0]
    return s


def _find_metadata_path(repo_dir: Path, kind: str) -> str:
    """Return the absolute path of *kind* (primary|filelists|other) for the
    cached repo at *repo_dir*."""
    repomd = cr.Repomd()
    cr.xml_parse_repomd(
        str(repo_dir / "repodata" / "repomd.xml"), repomd, lambda *_: True
    )
    for rec in repomd.records:
        if rec.type == kind:
            return str(repo_dir / rec.location_href)
    raise RuntimeError(f"{repo_dir}/repodata: no `{kind}` record in repomd.xml")


def build_package_universe(
    repo_to_dir: dict[InputRepo, Path],
) -> tuple[
    dict[UniverseKey, UniverseEntry],
    list[dict],
]:
    """First pass: scan only primary.xml of each repo to build the
    package universe (one entry per distinct NEVRA) and the rpm_source_map
    for azldev.

    Returns (universe, rpm_source_map) where:
      universe[(kind, arch, name, epoch, version, release, pkg_arch)]
          -> UniverseEntry
      rpm_source_map: list of {packageName, sourcePackageName} (deduped).

    Duplicate-NEVRA collisions are deduped:
      * cross-repo (same NEVRA in two input repos) -> WARN, keep first.
      * same-repo (broken upstream metadata) -> quiet log, keep first.
    Multiple distinct versions of the same package name are NOT collisions:
    each NEVRA gets its own universe entry and lands in the output.
    """
    universe: dict[UniverseKey, UniverseEntry] = {}
    src_map_set: set[tuple[str, str]] = set()

    for repo, repo_dir in repo_to_dir.items():
        primary = _find_metadata_path(repo_dir, "primary")
        log(f"  scanning {repo.kind}/{repo.arch}: {repo.url}")

        def pkgcb(pkg, *, _repo=repo):
            key: UniverseKey = (_repo.kind, _repo.arch) + _pkg_identity(pkg)
            if _repo.kind == KIND_SRPMS:
                source_name = pkg.name
            else:
                source_name = _strip_srpm_suffix(pkg.rpm_sourcerpm)
                if not source_name:
                    # An RPM with no sourcerpm is unusual but harmless: route
                    # it as if it were its own SRPM so azldev still receives
                    # an entry.
                    source_name = pkg.name
            # Always feed the source map; set semantics dedupe.
            src_map_set.add((pkg.name, source_name))
            existing = universe.get(key)
            if existing is None:
                universe[key] = UniverseEntry(_repo, source_name)
                return
            nevra = _format_nevra(pkg)
            if existing.repo.url != _repo.url:
                warn(
                    f"duplicate NEVRA in {_repo.kind}/{_repo.arch}: "
                    f"{nevra} found in both {existing.repo.url} and "
                    f"{_repo.url}; keeping the copy from the first repo"
                )
            else:
                # Same NEVRA listed twice within one repo -> broken upstream
                # metadata. Worth a note but not alarming.
                log(
                    f"    note: NEVRA {nevra} appears multiple times in "
                    f"{_repo.url}; deduping"
                )

        cr.xml_parse_primary(
            primary, pkgcb=pkgcb, do_files=False, warningcb=lambda *_: True
        )

    rpm_source_map = sorted(
        ({"packageName": pn, "sourcePackageName": sn}
         for pn, sn in src_map_set),
        key=lambda r: (r["packageName"], r["sourcePackageName"]),
    )
    return universe, rpm_source_map


# ---------------------------------------------------------------------------
# Phase 3: ask azldev for routing
# ---------------------------------------------------------------------------

def query_known_components(repo_root: Path) -> set[str]:
    """Return the set of legitimate Azure Linux component names.

    Used to gate package routing: a row whose `component` is not in this
    set was synthesised by azldev's project-default fallback for an
    unknown source package, so the row's `publishChannel` is meaningless
    and we treat the package as foreign / unpublished.
    """
    log("  querying azldev comp list for legitimate component names")
    proc = subprocess.run(
        ["azldev", "comp", "list", "-a", "-q", "-O", "json"],
        capture_output=True, text=True, cwd=repo_root, check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise RuntimeError("azldev comp list -a failed")
    rows = json.loads(proc.stdout)
    names = {row["name"] for row in rows if row.get("name")}
    log(f"    {len(names)} legitimate component(s)")
    return names


@dataclass
class AzldevRouting:
    """Resolved azldev routing tables, keyed for lookup."""

    # By type, then by package name. publishChannel may be empty.
    rpm: dict[str, dict] = field(default_factory=dict)
    srpm: dict[str, dict] = field(default_factory=dict)
    # Component -> Counter[channel-suffix] for inheritance fallback. Only
    # populated from rpm rows whose component is a legitimate Azure Linux
    # component AND that have a non-empty, allowed publishChannel.
    component_channels: dict[str, Counter] = field(default_factory=dict)
    # Names rejected because their component is not a legitimate AZL
    # component (i.e. azldev fell back to project-default routing for
    # something that isn't actually built by AZL).
    foreign_names: set[str] = field(default_factory=set)


def query_azldev(
    repo_root: Path,
    rpm_source_map: list[dict],
    scratch_dir: Path,
    known_components: set[str],
) -> AzldevRouting:
    map_path = scratch_dir / "rpm_source_map.json"
    map_path.write_text(json.dumps(rpm_source_map, indent=2))

    log(f"  invoking azldev (map: {len(rpm_source_map)} entries)")
    proc = subprocess.run(
        ["azldev", "package", "list", "--rpm-file", str(map_path),
         "-q", "-O", "json"],
        capture_output=True, text=True, cwd=repo_root, check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise RuntimeError("azldev package list --rpm-file failed")
    rows = json.loads(proc.stdout)

    routing = AzldevRouting()
    component_channels: dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        name = row.get("packageName", "")
        rtype = row.get("type", "")
        component = row.get("component", "") or ""
        raw_channel = row.get("publishChannel", "") or ""
        channel = (
            raw_channel[len(CHANNEL_PREFIX):]
            if raw_channel.startswith(CHANNEL_PREFIX) else raw_channel
        )
        if component and component not in known_components:
            # Foreign package: azldev synthesised a default channel for
            # something not actually built by AZL. Track and skip.
            routing.foreign_names.add(name)
            continue
        record = {
            "component": component,
            "channel": channel,         # may be ""
            "raw_channel": raw_channel,
            "group": row.get("group", "") or "",
        }
        if rtype == "srpm":
            routing.srpm[name] = record
        else:  # default to rpm
            routing.rpm[name] = record
            if (channel and component
                    and channel in ALLOWED_OUTPUT_CHANNELS):
                component_channels[component][channel] += 1
    routing.component_channels = dict(component_channels)
    return routing


# ---------------------------------------------------------------------------
# Phase 4: route each universe entry -> (channel, kind, arch) destination
# ---------------------------------------------------------------------------

@dataclass
class RoutingDecision:
    """Per-universe-entry decision: where the package should land, or why
    it was excluded."""

    dest_channel: str | None = None     # 'base' | 'sdk' | None (=excluded)
    reason: str = ""                    # human-readable provenance
    inherited: bool = False             # was Phase-4 inheritance used?
    tie_break_used: bool = False        # did inheritance pick via tie-break?


def _inherit_channel(
    component: str,
    component_channels: dict[str, Counter],
    tie_break_default: str = INHERITANCE_TIE_BREAK_DEFAULT,
) -> tuple[str | None, str, bool]:
    """Infer a publish channel for *component* from its sibling rpms.

    Returns ``(channel, reason, tie_break_used)``. ``channel`` is None
    when there are no published siblings to inherit from. When two or
    more channels tie for the top spot ``tie_break_default`` is
    preferred, with lex sort as a defensive fallback if the configured
    default isn't among the tied channels (which shouldn't be reachable
    today since only ALLOWED_OUTPUT_CHANNELS are added to
    ``component_channels`` in :func:`query_azldev`, but the code
    shouldn't silently do the wrong thing if that invariant ever
    breaks). ``tie_break_used`` lets callers surface the case
    explicitly rather than letting the pick masquerade as "the data
    said so".
    """
    counts = component_channels.get(component)
    if not counts:
        return None, "no sibling rpm has a published channel", False

    ranked = counts.most_common()
    top_count = ranked[0][1]
    tied = [ch for ch, n in ranked if n == top_count]

    if len(tied) > 1:
        picked = (
            tie_break_default if tie_break_default in tied else sorted(tied)[0]
        )
        reason = (
            f"inherited from sibling rpms (component={component}, "
            f"channels={dict(ranked)}, tied at {top_count}, picked "
            f"{picked} via tie-break default)"
        )
        return picked, reason, True

    picked = tied[0]
    if len(counts) == 1:
        return picked, (
            f"inherited from sibling rpms (component={component})"
        ), False
    return picked, (
        f"inherited from sibling rpms (component={component}, "
        f"channels={dict(ranked)}, picked {picked})"
    ), False


def decide_routing(
    universe: dict[UniverseKey, UniverseEntry],
    routing: AzldevRouting,
    tie_break_default: str = INHERITANCE_TIE_BREAK_DEFAULT,
) -> dict[UniverseKey, RoutingDecision]:
    """Produce one RoutingDecision per universe entry (i.e. per NEVRA).

    Routing lookup is name-based: every NEVRA of a given package name lands
    in the same destination channel. Decisions are still keyed per NEVRA so
    that downstream emit + count logic can iterate them 1:1 with the
    universe.

    NOTE: TODO(channel-inheritance) -- the new `azldev package list
    --rpm-file` output reports an empty publishChannel for type=srpm rows
    and for binary RPMs not explicitly configured (e.g. *-debuginfo,
    *-debugsource). We work around this by inheriting the channel from the
    parent component's published binary rpms. Once the underlying TOML
    config (and azldev) is updated to publish srpm/debuginfo channels
    explicitly, remove this inference and treat empty publishChannel
    strictly (i.e. mark the package as unpublished).
    """
    decisions: dict[UniverseKey, RoutingDecision] = {}
    tied_components_warned: set[str] = set()
    for key, entry in universe.items():
        kind = key[0]
        name = key[2]
        # Foreign packages (azldev fell back to project defaults for an
        # unknown source component) are unpublished by definition.
        if name in routing.foreign_names:
            decisions[key] = RoutingDecision(
                None,
                "azldev row had a project-default channel but the resolved "
                "component is not a legitimate Azure Linux component",
            )
            continue
        if kind == KIND_SRPMS:
            row = routing.srpm.get(name)
        else:
            row = routing.rpm.get(name)
        if row is None:
            decisions[key] = RoutingDecision(
                None, "no azldev entry for package"
            )
            continue
        channel = row["channel"]
        if channel:
            if channel not in ALLOWED_OUTPUT_CHANNELS:
                decisions[key] = RoutingDecision(
                    None,
                    f"azldev publishChannel={row['raw_channel']!r} is not "
                    f"one of the allowed standard-layout channels "
                    f"({sorted(ALLOWED_OUTPUT_CHANNELS)})",
                )
                continue
            decisions[key] = RoutingDecision(
                channel, f"azldev publishChannel={row['raw_channel']!r}"
            )
            continue
        # Empty channel -> inheritance fallback (TODO above).
        inherited, why, tie_break_used = _inherit_channel(
            row["component"],
            routing.component_channels,
            tie_break_default,
        )
        if inherited is None:
            decisions[key] = RoutingDecision(
                None, f"azldev publishChannel empty and {why}"
            )
        else:
            # Warn at most once per tied component: the tie depends
            # only on (component, component_channels) so emitting on
            # every affected NEVRA would just spam.
            if (
                tie_break_used
                and row["component"] not in tied_components_warned
            ):
                tied_components_warned.add(row["component"])
                warn(
                    f"channel-inheritance tie for component "
                    f"{row['component']!r}: {why}; the configured "
                    f"tie-break default ({tie_break_default!r}) was "
                    f"used, not the data -- fix the source TOML if "
                    f"this is wrong"
                )
            decisions[key] = RoutingDecision(
                inherited,
                f"azldev publishChannel empty; {why}",
                inherited=True,
                tie_break_used=tie_break_used,
            )
    return decisions


# ---------------------------------------------------------------------------
# Phase 5: per-destination writers
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Destination:
    channel: str        # 'base' | 'sdk'
    kind: str           # main | debuginfo | srpms
    arch: str           # x86_64 | aarch64 | src

    def relpath(self) -> str:
        if self.kind == KIND_MAIN:
            return f"{self.channel}/{self.arch}"
        if self.kind == KIND_DEBUGINFO:
            return f"{self.channel}/debuginfo/{self.arch}"
        if self.kind == KIND_SRPMS:
            return f"{self.channel}/srpms"
        raise ValueError(f"unknown kind: {self.kind}")


class _RepoWriter:
    """Manages the createrepo_c XML+sqlite triple for one destination."""

    # (xml record name, db record name, xml class, db class)
    _STREAMS: tuple[tuple[str, str, type, type], ...] = (
        ("primary",   "primary_db",   cr.PrimaryXmlFile,   cr.PrimarySqlite),
        ("filelists", "filelists_db", cr.FilelistsXmlFile, cr.FilelistsSqlite),
        ("other",     "other_db",     cr.OtherXmlFile,     cr.OtherSqlite),
    )

    def __init__(self, dest: Destination, output_dir: Path, pkg_count: int):
        self.dest = dest
        self.repodata_dir = output_dir / dest.relpath() / "repodata"
        if self.repodata_dir.exists():
            shutil.rmtree(self.repodata_dir)
        self.repodata_dir.mkdir(parents=True, exist_ok=True)

        self._streams: list[tuple[str, str, str, str, object, object]] = []
        for xml_name, db_name, xml_cls, db_cls in self._STREAMS:
            xml_path = str(self.repodata_dir / f"{xml_name}.xml.gz")
            db_path = str(self.repodata_dir / f"{xml_name}.sqlite")
            xml = xml_cls(xml_path)
            db = db_cls(db_path)
            xml.set_num_of_pkgs(pkg_count)
            self._streams.append(
                (xml_name, db_name, xml_path, db_path, xml, db)
            )
        self.added = 0

    def add_pkg(self, pkg: cr.Package) -> None:
        for _, _, _, _, xml, db in self._streams:
            xml.add_pkg(pkg)
            db.add_pkg(pkg)
        self.added += 1

    def finish(self) -> None:
        """Close all streams and write repomd.xml."""
        repomd = cr.Repomd()
        xml_records: list[cr.RepomdRecord] = []
        db_records: list[cr.RepomdRecord] = []
        for xml_name, db_name, xml_path, db_path, xml, db in self._streams:
            xml.close()
            xml_rec = cr.RepomdRecord(xml_name, xml_path)
            xml_rec.fill(cr.SHA256)
            db.dbinfo_update(xml_rec.checksum)
            db.close()
            db_rec = cr.RepomdRecord(db_name, db_path)
            db_rec.fill(cr.SHA256)
            xml_records.append(xml_rec)
            db_records.append(db_rec)
        for rec in xml_records:
            repomd.set_record(rec)
        for rec in db_records:
            repomd.set_record(rec)
        (self.repodata_dir / "repomd.xml").write_text(repomd.xml_dump())


# ---------------------------------------------------------------------------
# Phase 6: emit packages into writers
# ---------------------------------------------------------------------------


def emit_repos(
    repo_to_dir: dict[InputRepo, Path],
    universe: dict[UniverseKey, UniverseEntry],
    decisions: dict[UniverseKey, RoutingDecision],
    output_dir: Path,
) -> tuple[dict[Destination, int], list[dict], list[dict]]:
    """Second pass over each input repo: stream every package, decide its
    destination, set its absolute location_href, hand it to the writer.

    Returns (per_destination_counts, unpublished_records, fallback_records).

    Counts are per NEVRA. The unpublished and fallback reports both dedupe
    by (kind, arch, name) since the routing reason is name-based and
    listing every NEVRA of an affected name would just be noise.
    """
    # Precompute counts per destination (for XML headers), unpublished
    # records (excluded from output), and fallback records (routed via
    # Phase-4 inheritance rather than an explicit publishChannel).
    dest_counts: Counter[Destination] = Counter()
    unpublished: list[dict] = []
    unpub_seen: set[tuple[str, str, str]] = set()
    fallbacks: list[dict] = []
    fb_seen: set[tuple[str, str, str]] = set()
    for key, decision in decisions.items():
        kind = key[0]
        arch = key[1]
        name = key[2]
        entry = universe[key]
        if decision.dest_channel is None:
            nameslot = (kind, arch, name)
            if nameslot not in unpub_seen:
                unpub_seen.add(nameslot)
                unpublished.append({
                    "name": name,
                    "kind": kind,
                    "arch": arch,
                    "source_repo": entry.repo.url,
                    "source_package": entry.source_pkg_name,
                    "reason": decision.reason,
                })
            continue
        dest = Destination(decision.dest_channel, kind, arch)
        dest_counts[dest] += 1
        if decision.inherited:
            nameslot = (kind, arch, name)
            if nameslot not in fb_seen:
                fb_seen.add(nameslot)
                fallbacks.append({
                    "name": name,
                    "kind": kind,
                    "arch": arch,
                    "source_repo": entry.repo.url,
                    "source_package": entry.source_pkg_name,
                    "dest_channel": decision.dest_channel,
                    "reason": decision.reason,
                    "tie_break_used": decision.tie_break_used,
                })

    # Open writers up-front with correct counts.
    writers: dict[Destination, _RepoWriter] = {
        d: _RepoWriter(d, output_dir, n) for d, n in dest_counts.items()
    }

    # Iterate each input repo's full metadata and route packages.
    emitted: set[UniverseKey] = set()
    for repo, repo_dir in repo_to_dir.items():
        primary = _find_metadata_path(repo_dir, "primary")
        filelists = _find_metadata_path(repo_dir, "filelists")
        other = _find_metadata_path(repo_dir, "other")

        repo_base = repo.url.rstrip("/") + "/"
        pkg_iter = cr.PackageIterator(
            primary_path=primary,
            filelists_path=filelists,
            other_path=other,
            warningcb=lambda *_: True,
        )
        for pkg in pkg_iter:
            key: UniverseKey = (repo.kind, repo.arch) + _pkg_identity(pkg)
            entry = universe.get(key)
            if entry is None or entry.repo.url != repo.url:
                # Either filtered out earlier (shouldn't happen) or this is
                # the cross-repo duplicate copy already warned about during
                # the first pass; skip silently.
                continue
            if key in emitted:
                # Same NEVRA appearing twice within this repo: already
                # logged in build_package_universe; skip silently so writer
                # counts stay consistent with the XML headers.
                continue
            decision = decisions[key]
            if decision.dest_channel is None:
                continue
            dest = Destination(decision.dest_channel, repo.kind, repo.arch)
            # Rewrite location_href to an absolute upstream URL so consumers
            # download from the source repo. urljoin honors absolute hrefs
            # in the input (in case the input repo already published one)
            # and respects any xml:base on the input package.
            input_base = pkg.location_base or repo_base
            absolute_href = urllib.parse.urljoin(
                input_base, pkg.location_href or ""
            )
            pkg.location_href = absolute_href
            pkg.location_base = ""
            writers[dest].add_pkg(pkg)
            emitted.add(key)

    for dest, writer in writers.items():
        writer.finish()
        if writer.added != dest_counts[dest]:
            warn(
                f"writer for {dest.relpath()} expected "
                f"{dest_counts[dest]} pkgs but emitted {writer.added}"
            )

    return dict(dest_counts), unpublished, fallbacks


# ---------------------------------------------------------------------------
# Phase 7: unpublished-packages and fallback-channel reports
# ---------------------------------------------------------------------------

def write_unpublished_report(
    unpublished: list[dict], output_dir: Path
) -> tuple[Path, Path]:
    json_path = output_dir / "unpublished-packages.json"
    txt_path = output_dir / "unpublished-packages.txt"
    json_path.write_text(json.dumps(unpublished, indent=2))

    by_reason: dict[str, list[dict]] = defaultdict(list)
    for r in unpublished:
        by_reason[r["reason"]].append(r)

    with txt_path.open("w") as fh:
        fh.write(
            f"# {len(unpublished)} package(s) excluded from the routed repos "
            f"because no publish channel could be assigned.\n"
            f"# Grouped by reason; within each group, sorted by "
            f"(kind, arch, name).\n"
        )
        for reason in sorted(by_reason):
            entries = by_reason[reason]
            fh.write(f"\n## {reason}  ({len(entries)} package(s))\n")
            for r in sorted(entries, key=lambda x: (x["kind"], x["arch"], x["name"])):
                fh.write(
                    f"  {r['kind']:9s} {r['arch']:7s} {r['name']}  "
                    f"(srpm={r['source_package']!r}, src={r['source_repo']})\n"
                )
    return json_path, txt_path


def write_fallback_report(
    fallbacks: list[dict], output_dir: Path
) -> tuple[Path, Path]:
    """Mirror :func:`write_unpublished_report` for inheritance-fallback
    routings. These packages WERE routed (so they appear in the published
    repos) but only because Phase-4 inferred a channel from sibling rpms
    rather than reading an explicit ``publishChannel`` from azldev. Once
    the underlying TOML config publishes srpm/debuginfo channels
    explicitly the fallback path goes away and these reports should
    shrink to zero.
    """
    json_path = output_dir / "fallback-channel-packages.json"
    txt_path = output_dir / "fallback-channel-packages.txt"
    json_path.write_text(json.dumps(fallbacks, indent=2))

    by_reason: dict[str, list[dict]] = defaultdict(list)
    for r in fallbacks:
        by_reason[r["reason"]].append(r)

    with txt_path.open("w") as fh:
        fh.write(
            f"# {len(fallbacks)} package(s) routed via the Phase-4 channel "
            f"inheritance fallback (no explicit publishChannel from azldev).\n"
            f"# These packages ARE published, but only because a sibling rpm's "
            f"channel was inferred. Once azldev publishes channels explicitly "
            f"for srpm/debuginfo/etc. this list should be empty.\n"
            f"# Grouped by reason; within each group, sorted by "
            f"(kind, arch, name).\n"
        )
        for reason in sorted(by_reason):
            entries = by_reason[reason]
            fh.write(f"\n## {reason}  ({len(entries)} package(s))\n")
            for r in sorted(entries, key=lambda x: (x["kind"], x["arch"], x["name"])):
                marker = " [tie-break]" if r.get("tie_break_used") else ""
                fh.write(
                    f"  {r['kind']:9s} {r['arch']:7s} {r['name']}  "
                    f"-> {r['dest_channel']}{marker}  "
                    f"(srpm={r['source_package']!r}, src={r['source_repo']})\n"
                )
    return json_path, txt_path


# ---------------------------------------------------------------------------
# CLI / orchestration
# ---------------------------------------------------------------------------

class _OrderedRepoSourceAction(argparse.Action):
    """Append (option_string, value) into a single shared list across
    --repo-prefix and --repo, preserving CLI order.

    This matters because cross-repo NEVRA dedup keeps the first repo
    seen, so command-line order is the user's only knob to control
    which input wins for an overlapping NEVRA.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None)
        if items is None:
            items = []
            setattr(namespace, self.dest, items)
        items.append((option_string, values))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--output-dir", required=True, type=Path,
        help="Directory to write the routed per-channel/per-arch repos into.",
    )
    parser.add_argument(
        "--repo-prefix", action=_OrderedRepoSourceAction,
        dest="repo_sources", default=None, metavar="URL",
        help=(
            "URL prefix assumed to host the Standard Azure Linux Repo "
            "Layout. Expanded into all six sub-repos (404s on any are "
            "silently skipped). Repeatable; CLI order is preserved and "
            "interleaved with --repo for cross-repo NEVRA-dedup precedence."
        ),
    )
    parser.add_argument(
        "--repo", action=_OrderedRepoSourceAction,
        dest="repo_sources", default=None, metavar="TYPE:URL",
        help=(
            "Explicit single repo: TYPE:URL where TYPE is main, debuginfo, "
            "or srpms. URL may contain `$basearch` for main/debuginfo. "
            "404s are fatal. Repeatable; CLI order is preserved (see "
            "--repo-prefix)."
        ),
    )
    parser.add_argument(
        "--repo-root", type=Path, default=DEFAULT_REPO_ROOT,
        help="Path to the azurelinux project root (default: %(default)s).",
    )
    parser.add_argument(
        "--arch", action="append", default=[],
        help=(
            f"Arch to expand `$basearch` into (default: "
            f"{', '.join(DEFAULT_ARCHES)}). Repeatable."
        ),
    )
    parser.add_argument(
        "--keep-cache", action="store_true",
        help="Don't delete the metadata cache dir under <output-dir>/.cache/.",
    )
    tls = parser.add_mutually_exclusive_group()
    tls.add_argument(
        "--ca-bundle", type=Path, default=None,
        help=(
            "Path to a PEM-encoded CA bundle to trust for HTTPS repo "
            "fetches (e.g. for repos served by a self-signed CA). "
            "Mutually exclusive with --insecure."
        ),
    )
    tls.add_argument(
        "--insecure", action="store_true",
        help=(
            "Disable TLS certificate verification entirely for HTTPS repo "
            "fetches. Use only for trusted networks; prefer --ca-bundle "
            "when possible. Mutually exclusive with --ca-bundle."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    arches = tuple(args.arch) if args.arch else DEFAULT_ARCHES

    if args.ca_bundle is not None and not args.ca_bundle.is_file():
        return fatal(f"--ca-bundle path does not exist: {args.ca_bundle}")
    ssl_context = build_ssl_context(args.ca_bundle, args.insecure)

    repo_sources: list[tuple[str, str]] = args.repo_sources or []
    if not repo_sources:
        return fatal("at least one --repo-prefix or --repo must be provided")

    output_dir: Path = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    cache_root = output_dir / ".cache"
    cache_root.mkdir(parents=True, exist_ok=True)

    # ---- Resolve the InputRepo list ------------------------------------
    log("==> Resolving input repos ...")
    repos: list[InputRepo] = []
    for option, value in repo_sources:
        if option == "--repo-prefix":
            repos.extend(expand_repo_prefix(value, arches))
        else:  # --repo
            try:
                repos.extend(parse_explicit_repo(value, arches))
            except ValueError as e:
                return fatal(str(e))
    repos = dedup_input_repos(repos)
    log(f"    {len(repos)} candidate input repo(s) after dedup")

    # ---- Phase 1: download repodata ------------------------------------
    log("==> Downloading repodata ...")
    repo_to_dir: dict[InputRepo, Path] = {}
    for repo in repos:
        try:
            cache_dir = download_repo_metadata(repo, cache_root, ssl_context)
        except urllib.error.HTTPError as e:
            return fatal(
                f"HTTP {e.code} fetching {repo.url}/repodata/repomd.xml "
                f"(origin={repo.origin})"
            )
        if cache_dir is not None:
            repo_to_dir[repo] = cache_dir
    log(f"    {len(repo_to_dir)} repo(s) successfully downloaded "
        f"({len(repos) - len(repo_to_dir)} skipped)")

    if not repo_to_dir:
        return fatal("no input repos with usable repodata; nothing to route")

    # ---- Phase 2: build package universe + source map ------------------
    log("==> Building package universe ...")
    universe, src_map = build_package_universe(repo_to_dir)
    log(f"    {len(universe)} unique (kind, arch, NEVRA) entries; "
        f"{len(src_map)} unique (pkg, srpm) pairs for azldev")

    # ---- Phase 3: query azldev -----------------------------------------
    log("==> Querying azldev for routing ...")
    known_components = query_known_components(args.repo_root)
    routing = query_azldev(
        args.repo_root, src_map, output_dir, known_components
    )
    log(f"    azldev returned {len(routing.rpm)} rpm row(s), "
        f"{len(routing.srpm)} srpm row(s), "
        f"{len(routing.foreign_names)} foreign name(s) (excluded)")

    # ---- Phase 4: per-entry routing decisions --------------------------
    log("==> Computing routing decisions ...")
    decisions = decide_routing(universe, routing)
    n_pub = sum(1 for d in decisions.values() if d.dest_channel is not None)
    n_unpub = sum(1 for d in decisions.values() if d.dest_channel is None)
    n_inh = sum(1 for d in decisions.values() if d.inherited)
    log(f"    routed: {n_pub} | unpublished: {n_unpub} | "
        f"inheritance-fallback used: {n_inh}")

    # ---- Phase 5+6: open writers and emit ------------------------------
    log("==> Writing per-destination repos ...")
    dest_counts, unpublished, fallbacks = emit_repos(
        repo_to_dir, universe, decisions, output_dir
    )

    # ---- Phase 7: unpublished + fallback reports -----------------------
    log("==> Writing unpublished-packages report ...")
    json_path, txt_path = write_unpublished_report(unpublished, output_dir)
    log(f"    -> {json_path.name}, {txt_path.name}")

    log("==> Writing fallback-channel-packages report ...")
    fb_json, fb_txt = write_fallback_report(fallbacks, output_dir)
    log(f"    -> {fb_json.name}, {fb_txt.name}")

    # ---- Summary -------------------------------------------------------
    log("\n==> Summary")
    for dest in sorted(dest_counts, key=lambda d: (d.channel, d.kind, d.arch)):
        log(f"    {dest.relpath():35s}  {dest_counts[dest]:6d} pkg(s)")
    log(f"    {'(unpublished)':35s}  {len(unpublished):6d} pkg(s)")
    log(f"    {'(fallback-channel)':35s}  {len(fallbacks):6d} pkg(s)")

    if not args.keep_cache:
        with contextlib.suppress(FileNotFoundError):
            shutil.rmtree(cache_root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
