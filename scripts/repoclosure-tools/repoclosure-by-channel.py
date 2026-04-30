#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Per-channel repoclosure analysis for Azure Linux.

Given one or more pre-published RPM repositories and a binary-package →
publish-channel mapping (sourced from ``azldev package list -O json``),
synthesize new per-channel repodata that reorganises the existing RPMs
according to the *current* tree's channel split, then run ``dnf5
repoclosure`` against the synthesized repos to verify that:

  * the ``base`` channel is runtime-dep closed on its own; and
  * the ``base`` + ``sdk`` channels together are runtime-dep closed.

The synthesized repodata references the *original* RPM URLs (via
``xml:base``), so no RPMs are downloaded or copied — only metadata.

Multi-arch
----------
Both ``x86_64`` and ``aarch64`` are analysed. Repository URLs containing
the literal token ``$basearch`` are substituted per-arch.

Multiple input repos
--------------------
``--repo`` may be passed multiple times. Earlier repos win on collision
(by name + arch). This lets you stack a base snapshot with override
repos.

Container execution
-------------------
``dnf5``'s ``repoclosure`` plugin is required, and the version in
Fedora 44 contains fixes that earlier versions lack. Unless
``--no-container`` is given, the script self-launches inside a
``fedora:44`` Docker container with ``dnf5-plugins`` and
``python3-createrepo_c`` pre-installed, mounting the output directory
and any local-path input repos read-only.

Outputs
-------
Default layout under ``--output``:

  channel-map.json                        (channel mapping snapshot)
  base/x86_64/repodata/                   (synthesized repodata)
  base/aarch64/repodata/
  sdk/x86_64/repodata/
  sdk/aarch64/repodata/
  reports/repoclosure-base-x86_64.{txt,json}
  reports/repoclosure-base-aarch64.{txt,json}
  reports/repoclosure-base+sdk-x86_64.{txt,json}
  reports/repoclosure-base+sdk-aarch64.{txt,json}
  reports/srpm-consistency.{txt,json}
  reports/summary.txt                     (one-line-per-scope summary)
"""
from __future__ import annotations

import argparse
import dataclasses
import fnmatch
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


# ---------------------------------------------------------------------------
# Configurable constants
# ---------------------------------------------------------------------------

# Closure scopes to evaluate. A scope name maps to the ordered list of
# channels that participate. Packages from *all* listed channels are made
# available to the resolver, but only packages from channels in
# ``check`` are *checked* for unresolved deps.
#
# Tweak this constant (or add a CLI flag) when introducing new channels.
SCOPES: list[dict] = [
    {"name": "base",     "available": ["base"],          "check": ["base"]},
    {"name": "base+sdk", "available": ["base", "sdk"],   "check": ["base", "sdk"]},
]

# Architectures to analyse. ``$basearch`` in repo URLs is substituted with
# each of these in turn.
ARCHES: list[str] = ["x86_64", "aarch64"]

# Default container image (overridable via --container-image).
DEFAULT_CONTAINER_IMAGE = "fedora:44"

# Marker env var to indicate the script is running inside its own
# auto-launched container, so we don't recurse on re-exec.
IN_CONTAINER_ENV = "REPOCLOSURE_BY_CHANNEL_IN_CONTAINER"

# Mount points used inside the container.
CONTAINER_OUTPUT = "/repoclosure/output"
CONTAINER_REPO_MOUNTS = "/repoclosure/repos"  # parent dir for local repos
CONTAINER_SCRIPT = "/repoclosure/repoclosure-by-channel.py"

# Filename used to snapshot the channel map into the output dir before
# entering the container.
CHANNEL_MAP_FILENAME = "channel-map.json"


# ---------------------------------------------------------------------------
# Repo-input model
# ---------------------------------------------------------------------------

@dataclasses.dataclass
class RepoSpec:
    """A single ``--repo`` argument, parsed.

    *original* preserves the user-supplied string for diagnostics.
    *kind* is ``"url"`` or ``"local"``.
    *value* is either an HTTP(S) URL template (possibly containing
    ``$basearch``) or an absolute local filesystem path.
    """
    original: str
    kind: str
    value: str

    @classmethod
    def parse(cls, raw: str) -> "RepoSpec":
        if raw.startswith(("http://", "https://", "ftp://", "file://")):
            return cls(original=raw, kind="url", value=raw)
        # Treat as local path.
        p = Path(raw).expanduser()
        if not p.is_absolute():
            p = p.resolve()
        return cls(original=raw, kind="local", value=str(p))

    def base_for_arch(self, arch: str) -> str:
        """Return the per-arch base URL/path for this repo."""
        v = self.value.replace("$basearch", arch)
        if self.kind == "local":
            return v.rstrip("/")
        return v.rstrip("/")

    def public_base_for_arch(self, arch: str) -> str:
        """Return the URL/path used for ``xml:base`` in synthesized
        repodata. For URL repos this is the same as the per-arch URL.
        For local-path repos we still emit the original local path
        because we can't predict where the user will host it; downstream
        consumers can rewrite the xml:base if needed.
        """
        return self.base_for_arch(arch)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="repoclosure-by-channel",
        description=(
            "Synthesize per-channel repodata from one or more input RPM "
            "repos using a binary-package -> channel mapping, then run "
            "dnf5 repoclosure for each scope (base, base+sdk) on each "
            "architecture (x86_64, aarch64)."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument(
        "--repo",
        action="append",
        required=False,  # required only on host; container reads from snapshot
        metavar="URL_OR_PATH",
        help=(
            "Input RPM repository, repeatable. URL templates may contain "
            "the literal token '$basearch' which is substituted per arch. "
            "Local filesystem paths are also supported (auto-mounted into "
            "the container). When repeated, earlier repos win on collision "
            "(by name+arch)."
        ),
    )
    p.add_argument(
        "--output", "-o",
        required=True,
        type=Path,
        help="Output directory.",
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help=(
            "Path to the azurelinux repo root (where azldev.toml lives). "
            "Defaults to auto-detection."
        ),
    )
    p.add_argument(
        "--channel-map",
        type=Path,
        default=None,
        help=(
            "Path to a pre-generated channel-map JSON file (the JSON output "
            "of `azldev package list -a -O json`). If omitted, the script "
            "runs azldev itself."
        ),
    )
    p.add_argument(
        "--allowlist",
        type=Path,
        default=None,
        help=(
            "TOML file with intentional repoclosure-violation suppressions. "
            "If omitted, no suppression is applied."
        ),
    )
    p.add_argument(
        "--srpm-allowlist",
        type=Path,
        default=None,
        help=(
            "TOML file with per-SRPM channel-consistency exceptions. "
            "If omitted, no suppression is applied."
        ),
    )
    p.add_argument(
        "--arches",
        default=",".join(ARCHES),
        help=f"Comma-separated list of arches (default: {','.join(ARCHES)}).",
    )
    p.add_argument(
        "--skip-repoclosure",
        action="store_true",
        help="Skip the dnf repoclosure runs.",
    )
    p.add_argument(
        "--skip-srpm-consistency",
        action="store_true",
        help="Skip the SRPM channel-consistency check.",
    )
    p.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help=(
            "Console output format for the final summary (default: text). "
            "Per-report JSON files are always produced regardless."
        ),
    )
    p.add_argument(
        "--no-fail-on-srpm-violations",
        action="store_true",
        help="Do not exit non-zero on uncovered SRPM-consistency violations.",
    )
    p.add_argument(
        "--no-fail-on-repoclosure",
        action="store_true",
        help="Do not exit non-zero when unresolved deps remain.",
    )
    p.add_argument(
        "--force", "-f",
        action="store_true",
        help=(
            "Wipe the --output directory before running. Uses the "
            "container to clean up files that may have been written as "
            "root by an earlier run, so the host user never needs sudo."
        ),
    )
    # Container orchestration
    p.add_argument(
        "--no-container",
        action="store_true",
        help=(
            "Run entirely on the host (do not auto-launch a container). "
            "Requires dnf5 with the repoclosure plugin and "
            "python3-createrepo_c to be installed locally."
        ),
    )
    p.add_argument(
        "--container-image",
        default=DEFAULT_CONTAINER_IMAGE,
        help=f"Container image (default: {DEFAULT_CONTAINER_IMAGE}).",
    )
    p.add_argument(
        "--docker",
        default=os.environ.get("DOCKER", "docker"),
        help="Docker CLI to invoke (default: docker; honours $DOCKER env).",
    )
    return p


# ---------------------------------------------------------------------------
# Channel map (azldev integration)
# ---------------------------------------------------------------------------

def load_channel_map_from_azldev(repo_root: Path | None) -> list[dict]:
    """Run ``azldev package list -a -O json`` and return its parsed output."""
    cmd = ["azldev"]
    if repo_root is not None:
        cmd += ["-C", str(repo_root)]
    cmd += ["package", "list", "-a", "-q", "-O", "json"]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


def channel_map_to_pkg_dict(entries: list[dict]) -> tuple[dict[str, str], set[str]]:
    """Reduce ``azldev package list`` output to ``(pkg_to_channel,
    exceptions_pkg_names)``.

    The channel name has any ``rpm-`` prefix stripped so it matches the
    per-channel directory layout (``base/``, ``sdk/`` ...).

    ``exceptions_pkg_names`` is the set of package names whose
    ``group`` field is ``exceptions-packages`` — by Azure Linux
    convention these are sub-packages from a primarily-base SRPM that
    are intentionally published to ``sdk``. They are auto-allowlisted
    by the SRPM-consistency check.
    """
    out: dict[str, str] = {}
    exceptions: set[str] = set()
    for e in entries:
        name = e["packageName"]
        ch = e.get("publishChannel", "none")
        if not ch or ch == "none":
            continue
        if ch.startswith("rpm-"):
            ch = ch[len("rpm-"):]
        out[name] = ch
        if e.get("group") == "exceptions-packages":
            exceptions.add(name)
    return out, exceptions


# ---------------------------------------------------------------------------
# Repodata: fetch primary/filelists/other for a given (repo, arch)
# ---------------------------------------------------------------------------

def _is_local_path(base: str) -> bool:
    return not base.startswith(("http://", "https://", "ftp://", "file://"))


def _fetch_text(url_or_path: str, dest: Path) -> None:
    """Fetch a file from URL or copy from local filesystem."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if _is_local_path(url_or_path):
        shutil.copyfile(url_or_path, dest)
        return
    if url_or_path.startswith("file://"):
        src = urllib.parse.urlparse(url_or_path).path
        shutil.copyfile(src, dest)
        return
    # http/https/ftp
    with urllib.request.urlopen(url_or_path) as resp, dest.open("wb") as out:
        shutil.copyfileobj(resp, out)


def _join(base: str, rel: str) -> str:
    if _is_local_path(base):
        return os.path.join(base, rel)
    if not base.endswith("/"):
        base = base + "/"
    return urllib.parse.urljoin(base, rel)


def fetch_repo_metadata(base: str, cache_dir: Path) -> tuple[str, str, str]:
    """Download repomd.xml + primary/filelists/other to *cache_dir*.

    Returns (primary_path, filelists_path, other_path) as absolute strings.
    """
    import createrepo_c as cr

    repodata_dir = cache_dir / "repodata"
    repodata_dir.mkdir(parents=True, exist_ok=True)

    repomd_url = _join(base, "repodata/repomd.xml")
    repomd_path = repodata_dir / "repomd.xml"
    _fetch_text(repomd_url, repomd_path)

    repomd = cr.Repomd()
    cr.xml_parse_repomd(str(repomd_path), repomd, lambda *_: True)

    paths: dict[str, Path] = {}
    for record in repomd.records:
        if record.type in ("primary", "filelists", "other"):
            url = _join(base, record.location_href)
            dest = cache_dir / record.location_href
            _fetch_text(url, dest)
            paths[record.type] = dest

    missing = {"primary", "filelists", "other"} - paths.keys()
    if missing:
        raise RuntimeError(
            f"repomd.xml at {repomd_url} missing record(s): {sorted(missing)}"
        )
    return str(paths["primary"]), str(paths["filelists"]), str(paths["other"])


# ---------------------------------------------------------------------------
# Repodata: merge across input repos (priority order) and split by channel
# ---------------------------------------------------------------------------

class _ChannelWriter:
    """Manages the repodata XML + SQLite writers for one channel/arch."""

    def __init__(self, repodata_dir: Path, pkg_count: int):
        import createrepo_c as cr

        if repodata_dir.exists():
            shutil.rmtree(repodata_dir)
        repodata_dir.mkdir(parents=True, exist_ok=True)
        self._dir = repodata_dir

        self.pri_xml_path = str(repodata_dir / "primary.xml.gz")
        self.fil_xml_path = str(repodata_dir / "filelists.xml.gz")
        self.oth_xml_path = str(repodata_dir / "other.xml.gz")
        self.pri_db_path = str(repodata_dir / "primary.sqlite")
        self.fil_db_path = str(repodata_dir / "filelists.sqlite")
        self.oth_db_path = str(repodata_dir / "other.sqlite")

        self.pri_xml = cr.PrimaryXmlFile(self.pri_xml_path)
        self.fil_xml = cr.FilelistsXmlFile(self.fil_xml_path)
        self.oth_xml = cr.OtherXmlFile(self.oth_xml_path)
        self.pri_db = cr.PrimarySqlite(self.pri_db_path)
        self.fil_db = cr.FilelistsSqlite(self.fil_db_path)
        self.oth_db = cr.OtherSqlite(self.oth_db_path)

        self.pri_xml.set_num_of_pkgs(pkg_count)
        self.fil_xml.set_num_of_pkgs(pkg_count)
        self.oth_xml.set_num_of_pkgs(pkg_count)

    def add_pkg(self, pkg) -> None:
        self.pri_xml.add_pkg(pkg)
        self.fil_xml.add_pkg(pkg)
        self.oth_xml.add_pkg(pkg)
        self.pri_db.add_pkg(pkg)
        self.fil_db.add_pkg(pkg)
        self.oth_db.add_pkg(pkg)

    def finish(self) -> None:
        import createrepo_c as cr

        self.pri_xml.close()
        self.fil_xml.close()
        self.oth_xml.close()
        repomd = cr.Repomd()
        records = [
            ("primary",      self.pri_xml_path, self.pri_db),
            ("filelists",    self.fil_xml_path, self.fil_db),
            ("other",        self.oth_xml_path, self.oth_db),
            ("primary_db",   self.pri_db_path,  None),
            ("filelists_db", self.fil_db_path,  None),
            ("other_db",     self.oth_db_path,  None),
        ]
        for name, path, db in records:
            rec = cr.RepomdRecord(name, path)
            rec.fill(cr.SHA256)
            if db is not None:
                db.dbinfo_update(rec.checksum)
                db.close()
            repomd.set_record(rec)
        (self._dir / "repomd.xml").write_text(repomd.xml_dump())


def _strip_srpm_suffix(srpm_filename: str) -> str:
    """Convert ``foo-1.0-1.src.rpm`` to ``foo``."""
    if srpm_filename.endswith(".src.rpm"):
        srpm_filename = srpm_filename[: -len(".src.rpm")]
    if "-" in srpm_filename:
        srpm_filename = srpm_filename.rsplit("-", 1)[0]
    if "-" in srpm_filename:
        srpm_filename = srpm_filename.rsplit("-", 1)[0]
    return srpm_filename


def synthesize_per_channel_repodata(
    repos: list[RepoSpec],
    arch: str,
    pkg_to_channel: dict[str, str],
    output_arch_root: Path,
    cache_root: Path,
) -> tuple[dict[str, int], dict[str, str], dict[str, int],
           set[str], set[str]]:
    """Fetch metadata from each input repo (in priority order), merge,
    and write per-channel synthesized repodata under
    ``<output>/{channel}/{arch}/repodata/``.

    Returns:
      ``(written_per_channel, pkg_to_srpm, kept_per_repo,
         seen_names, unmatched_names)``

    where:
      * ``seen_names`` is the set of every binary-RPM name that appeared
        in any input repo for *arch* (regardless of channel-map
        matching).
      * ``unmatched_names`` is the subset of ``seen_names`` that have no
        entry in the channel map and were therefore excluded from the
        synthesized repodata.
    """
    import createrepo_c as cr

    print(f"  [{arch}] fetching upstream repodata from {len(repos)} repo(s) ...")

    # Phase 1: fetch + parse each repo's package iterator. We don't pull
    # everything into memory yet — we track which packages we *will* take
    # from each repo via a name+arch precedence dict.
    repo_meta: list[tuple[str, str, str, str]] = []  # (public_base, primary, fil, oth)
    for i, r in enumerate(repos):
        rcache = cache_root / f"repo{i}-{arch}"
        rcache.mkdir(parents=True, exist_ok=True)
        per_arch_base = r.base_for_arch(arch)
        public_base = r.public_base_for_arch(arch)
        print(f"    repo{i} ({r.original}) → {per_arch_base}")
        primary, fil, oth = fetch_repo_metadata(per_arch_base, rcache)
        repo_meta.append((public_base, primary, fil, oth))

    # Phase 2: precedence pass — walk repos in order, claim (name, arch).
    # We do a quick primary-only pass first to know counts per channel.
    # Also accumulates *seen_names*: every package name observed in any
    # input repo for this arch, used downstream for repo-vs-channel-map
    # reporting.
    claim: dict[tuple[str, str], int] = {}  # (name, arch) -> repo index
    seen_names: set[str] = set()
    for i, (_, primary, _, _) in enumerate(repo_meta):
        def _claim_cb(pkg, _i=i):
            seen_names.add(pkg.name)
            key = (pkg.name, pkg.arch)
            claim.setdefault(key, _i)
        cr.xml_parse_primary(primary, pkgcb=_claim_cb,
                             do_files=False, warningcb=lambda *_: True)
    if not seen_names:
        raise RuntimeError(f"No packages found in any input repo for arch={arch}")

    # Phase 3: count per-channel claims (and capture pkg→SRPM).
    counts: dict[str, int] = defaultdict(int)
    pkg_to_srpm: dict[str, str] = {}
    unmatched_names: set[str] = set()
    pkg_repo_choice: dict[str, int] = {}  # name -> repo index winning
    for i, (_, primary, _, _) in enumerate(repo_meta):
        def _count_cb(pkg, _i=i):
            if claim.get((pkg.name, pkg.arch)) != _i:
                return
            channel = pkg_to_channel.get(pkg.name)
            if channel is None:
                unmatched_names.add(pkg.name)
                return
            counts[channel] += 1
            pkg_repo_choice[pkg.name] = _i
            srpm = pkg.rpm_sourcerpm or ""
            if srpm:
                pkg_to_srpm[pkg.name] = _strip_srpm_suffix(srpm)
        cr.xml_parse_primary(primary, pkgcb=_count_cb,
                             do_files=False, warningcb=lambda *_: True)

    if unmatched_names:
        sample = sorted(unmatched_names)[:5]
        suffix = "..." if len(unmatched_names) > 5 else ""
        print(f"    [{arch}] note: {len(unmatched_names)} package name(s) "
              f"in input repo(s) had no channel assignment and will be "
              f"excluded (e.g. {', '.join(sample)}{suffix})")

    if not counts:
        raise RuntimeError(
            f"[{arch}] none of the packages in the input repo(s) match "
            f"any channel in the channel map"
        )

    channels = sorted(counts)
    print(f"    [{arch}] channels: {', '.join(f'{c}={counts[c]}' for c in channels)}")

    # Phase 4: open writers per channel, then walk each repo's full
    # iterator (primary+filelists+other) and dispatch claimed pkgs.
    writers: dict[str, _ChannelWriter] = {}
    for ch in channels:
        wdir = output_arch_root / ch / arch / "repodata"
        writers[ch] = _ChannelWriter(wdir, counts[ch])

    written: dict[str, int] = defaultdict(int)
    kept_per_repo: dict[str, int] = defaultdict(int)
    for i, (public_base, primary, fil, oth) in enumerate(repo_meta):
        pkg_iter = cr.PackageIterator(
            primary_path=primary, filelists_path=fil, other_path=oth,
            warningcb=lambda *_: True,
        )
        for pkg in pkg_iter:
            if claim.get((pkg.name, pkg.arch)) != i:
                continue
            channel = pkg_to_channel.get(pkg.name)
            if channel is None:
                continue
            # Set xml:base so the synthesized repodata still resolves to
            # the original package URLs.
            if not pkg.location_base:
                pkg.location_base = public_base + "/"
            writers[channel].add_pkg(pkg)
            written[channel] += 1
            kept_per_repo[f"repo{i}"] += 1

    for ch in channels:
        writers[ch].finish()
        print(f"    wrote {written[ch]} pkgs → "
              f"{output_arch_root / ch / arch}/repodata/")

    return (
        dict(written),
        pkg_to_srpm,
        dict(kept_per_repo),
        seen_names,
        unmatched_names,
    )


# ---------------------------------------------------------------------------
# Repoclosure: run dnf5, parse JSON, apply allowlist
# ---------------------------------------------------------------------------

def load_repoclosure_allowlist(path: Path | None) -> list[dict]:
    if path is None or not path.exists():
        return []
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    entries = list(data.get("ignore", []) or [])
    for e in entries:
        e.setdefault("scope", "any")
        e.setdefault("reason", "")
        e.setdefault("confidence", "")
        e.setdefault("overlay", "")
        e.setdefault("verified_at_commit", "")
        for field in ("package", "requires"):
            v = e.get(field, "")
            if isinstance(v, str):
                e[field] = [v]
            elif isinstance(v, list):
                e[field] = list(v)
            else:
                raise ValueError(
                    f"allowlist entry field '{field}' must be a string "
                    f"or list of strings"
                )
    return entries


def _nevra_name(nevra: str) -> str:
    base = nevra.rsplit(".", 1)[0]   # drop arch
    base = base.rsplit("-", 1)[0]    # drop release
    base = base.rsplit("-", 1)[0]    # drop version
    return base


def _entry_matches(entry: dict, scope: str, pkg_name: str, requires: str) -> bool:
    if entry["scope"] not in ("any", scope):
        return False
    if not any(fnmatch.fnmatchcase(pkg_name, p) for p in entry["package"]):
        return False
    if not any(fnmatch.fnmatchcase(requires, r) for r in entry["requires"]):
        return False
    return True


def run_repoclosure(
    *,
    scope_name: str,
    arch: str,
    output_root: Path,
    repos_for_resolver: list[tuple[str, Path]],
    check_repo_ids: list[str],
    allowlist: list[dict],
    reports_dir: Path,
) -> dict:
    """Run ``dnf5 repoclosure`` for one (scope, arch) combination.

    Returns a dict summarising the result:
      ``{scope, arch, raw, suppressed, remaining, report_paths: {...}}``.
    """
    cmd: list[str] = [
        "dnf5", "--no-plugins", "-q",
        "--setopt=reposdir=/dev/null",
    ]
    cache_dir = output_root / ".dnf-cache" / f"{scope_name}-{arch}"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cmd.append(f"--setopt=cachedir={cache_dir}")
    for repo_id, repo_path in repos_for_resolver:
        cmd.append(f"--repofrompath={repo_id},{repo_path}")
        cmd.append(f"--setopt={repo_id}.enabled=1")
        cmd.append(f"--setopt={repo_id}.gpgcheck=0")
    cmd += [
        "repoclosure",
        f"--check={','.join(check_repo_ids)}",
        f"--arch={arch},noarch",
        "--json",
    ]
    # `--forcearch` configures the *resolver* arch (so e.g. aarch64
    # packages are seen as candidates when the host is x86_64).
    # `--arch=` filters which packages are *checked* for unresolved deps.
    # We need both: without `--forcearch`, dnf5 silently drops every
    # non-host-arch provider, producing thousands of bogus "unresolved"
    # findings on cross-arch runs.
    cmd.insert(cmd.index("repoclosure"), f"--forcearch={arch}")
    print(f"    $ {' '.join(shlex.quote(c) for c in cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    raw_stdout = proc.stdout or ""
    raw_stderr = proc.stderr or ""
    # dnf5 returns non-zero when there are unresolved deps; that's expected.
    # But it should never fail to *run*; if stdout is empty, treat as error.
    if not raw_stdout.strip():
        raise RuntimeError(
            f"dnf5 repoclosure produced no JSON output for "
            f"scope={scope_name} arch={arch}\n"
            f"stderr:\n{raw_stderr}"
        )
    try:
        findings_raw = json.loads(raw_stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"dnf5 repoclosure produced non-JSON output for "
            f"scope={scope_name} arch={arch}: {exc}\n"
            f"stdout (first 400 bytes):\n{raw_stdout[:400]}\n"
            f"stderr (first 400 bytes):\n{raw_stderr[:400]}"
        ) from exc

    # Flatten findings: one row per (consumer, missing requirement) pair.
    flat: list[dict] = []
    for entry in findings_raw:
        nevra = entry["package"]
        repo = entry.get("repo", "")
        for req in entry.get("unresolved_dependencies", []):
            flat.append({
                "consumer_nevra": nevra,
                "consumer_name": _nevra_name(nevra),
                "consumer_repo": repo,
                "requires": req,
            })

    suppressed: list[tuple[dict, dict]] = []
    kept: list[dict] = []
    for f in flat:
        match = next(
            (e for e in allowlist
             if _entry_matches(e, scope_name, f["consumer_name"], f["requires"])),
            None,
        )
        if match:
            suppressed.append((f, match))
        else:
            kept.append(f)

    report_basename = f"repoclosure-{scope_name}-{arch}"
    raw_path = reports_dir / f"{report_basename}.raw.txt"
    txt_path = reports_dir / f"{report_basename}.txt"
    json_path = reports_dir / f"{report_basename}.json"
    hits_path = reports_dir / f"{report_basename}.allowlist-hits.txt"
    raw_path.write_text(raw_stdout)

    grouped: dict[str, list[str]] = defaultdict(list)
    for f in kept:
        grouped[f["consumer_nevra"]].append(f["requires"])

    with txt_path.open("w") as fh:
        fh.write(
            f"# scope={scope_name} arch={arch}\n"
            f"# raw={len(flat)} suppressed={len(suppressed)} "
            f"remaining={len(kept)}\n"
        )
        if not grouped:
            fh.write("# No unresolved dependencies.\n")
        else:
            for nevra in sorted(grouped):
                fh.write(f"\nPackage {nevra}\n")
                for req in sorted(set(grouped[nevra])):
                    fh.write(f"  unresolved dependency: {req}\n")

    with hits_path.open("w") as fh:
        if not suppressed:
            fh.write("# No allowlist entries matched.\n")
        else:
            fh.write(f"# {len(suppressed)} dependency line(s) suppressed.\n")
            for f, entry in suppressed:
                disp = (entry["package"][0] if len(entry["package"]) == 1
                        else f"[{', '.join(entry['package'])}]")
                fh.write(
                    f"\nPackage {f['consumer_nevra']}  "
                    f"(matched package={disp})\n"
                    f"  unresolved dependency: {f['requires']}\n"
                    f"  reason     : {entry.get('reason', '')}\n"
                    f"  confidence : {entry.get('confidence', '')}\n"
                )
                if entry.get("overlay"):
                    fh.write(f"  overlay    : {entry['overlay']}\n")
                if entry.get("verified_at_commit"):
                    fh.write(
                        f"  verified-at: {entry['verified_at_commit']}\n"
                    )

    json_payload = {
        "scope": scope_name,
        "arch": arch,
        "command": cmd,
        "totals": {
            "raw": len(flat),
            "suppressed": len(suppressed),
            "remaining": len(kept),
        },
        "remaining": kept,
        "suppressed": [
            {**f, "allowlist_entry": entry} for f, entry in suppressed
        ],
    }
    json_path.write_text(json.dumps(json_payload, indent=2))

    return {
        "scope": scope_name,
        "arch": arch,
        "totals": json_payload["totals"],
        "report_paths": {
            "raw": str(raw_path),
            "text": str(txt_path),
            "json": str(json_path),
            "allowlist_hits": str(hits_path),
        },
    }


# ---------------------------------------------------------------------------
# SRPM channel-consistency check
# ---------------------------------------------------------------------------

def load_srpm_allowlist(path: Path | None) -> dict[str, dict]:
    if path is None or not path.exists():
        return {}
    with path.open("rb") as fh:
        data = tomllib.load(fh)
    out: dict[str, dict] = {}
    for entry in data.get("exception", []) or []:
        srpm = entry.get("srpm")
        if not srpm:
            continue
        entry.setdefault("expected_channel", "")
        entry.setdefault("allowed_in_other", [])
        entry.setdefault("reason", "")
        out[srpm] = entry
    return out


def check_srpm_consistency(
    pkg_to_channel: dict[str, str],
    pkg_to_srpm: dict[str, str],
    allowlist: dict[str, dict],
    exceptions_pkg_names: set[str],
    reports_dir: Path,
) -> dict:
    """Verify that every SRPM publishes its binary RPMs to a single
    channel. Returns a summary dict including ``uncovered`` count.

    Two coverage sources are recognised for cross-channel SRPMs:

    * ``exceptions-group`` — package is a member of the
      ``exceptions-packages`` group in ``azldev package list``. Such
      packages are intentionally cross-channel siblings of base SRPMs
      and require no further allowlisting.

    * ``allowlist`` — explicit per-SRPM TOML entry (see
      ``--srpm-allowlist``).

    A violation is *covered* if every cross-channel binary is either an
    exceptions-group member, in the allowlist's ``expected_channel``,
    or matches one of the allowlist's ``allowed_in_other`` glob
    patterns.
    """
    srpm_to_chan_pkgs: dict[str, dict[str, list[str]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for pkg, channel in pkg_to_channel.items():
        srpm = pkg_to_srpm.get(pkg)
        if not srpm:
            continue
        srpm_to_chan_pkgs[srpm][channel].append(pkg)

    raw_violations: list[dict] = []
    for srpm, by_chan in srpm_to_chan_pkgs.items():
        if len(by_chan) > 1:
            raw_violations.append({
                "srpm": srpm,
                "channels": {ch: sorted(pkgs) for ch, pkgs in by_chan.items()},
                "total_pkgs": sum(len(p) for p in by_chan.values()),
            })

    group_covered: list[dict] = []
    allowlist_covered: list[dict] = []
    uncovered: list[dict] = []

    for v in raw_violations:
        # Step 1: strip exceptions-packages members from the per-channel
        # view. If what remains is single-channel (or empty), the
        # exceptions group fully covers the violation.
        all_binaries = [p for pkgs in v["channels"].values() for p in pkgs]
        exception_binaries = sorted(
            p for p in all_binaries if p in exceptions_pkg_names
        )
        non_exc_by_chan = {
            ch: [p for p in pkgs if p not in exceptions_pkg_names]
            for ch, pkgs in v["channels"].items()
        }
        non_exc_by_chan = {
            ch: pkgs for ch, pkgs in non_exc_by_chan.items() if pkgs
        }

        if len(non_exc_by_chan) <= 1:
            group_covered.append({
                **v,
                "coverage_source": "exceptions-group",
                "exception_binaries": exception_binaries,
                "non_exception_channel": (
                    next(iter(non_exc_by_chan)) if non_exc_by_chan else None
                ),
            })
            continue

        # Step 2: try the TOML allowlist on the non-exceptions view.
        entry = allowlist.get(v["srpm"])
        if not entry:
            uncovered.append({
                **v,
                "exception_binaries": exception_binaries,
                "stray_pkgs": [],
            })
            continue

        expected = entry["expected_channel"]
        patterns = entry["allowed_in_other"]
        stray: list[tuple[str, str]] = []
        for ch, pkgs in v["channels"].items():
            if ch == expected:
                continue
            for p in pkgs:
                if p in exceptions_pkg_names:
                    continue  # absorbed by exceptions-group
                if not any(fnmatch.fnmatchcase(p, pat) for pat in patterns):
                    stray.append((p, ch))
        annotated = {
            **v,
            "coverage_source": (
                "allowlist+exceptions-group" if exception_binaries
                else "allowlist"
            ),
            "allowlist_entry": entry,
            "exception_binaries": exception_binaries,
            "stray_pkgs": stray,
        }
        if stray:
            uncovered.append(annotated)
        else:
            allowlist_covered.append(annotated)

    raw_violations.sort(key=lambda v: -v["total_pkgs"])
    group_covered.sort(key=lambda v: v["srpm"])
    allowlist_covered.sort(key=lambda v: v["srpm"])
    uncovered.sort(key=lambda v: -v["total_pkgs"])

    total_covered = len(group_covered) + len(allowlist_covered)

    txt_path = reports_dir / "srpm-consistency.txt"
    json_path = reports_dir / "srpm-consistency.json"

    with txt_path.open("w") as fh:
        fh.write(
            "# Policy: every binary RPM produced by an SRPM must publish "
            "to the same channel.\n"
            f"# Total cross-channel SRPMs            : {len(raw_violations)}\n"
            f"# Covered by exceptions-packages group : {len(group_covered)}\n"
            f"# Covered by allowlist                 : {len(allowlist_covered)}\n"
            f"# Uncovered (real)                     : {len(uncovered)}\n"
        )
        if uncovered:
            fh.write("\n## UNCOVERED VIOLATIONS\n")
            for v in uncovered:
                fh.write(
                    f"\nSRPM {v['srpm']}  ({v['total_pkgs']} pub pkgs)\n"
                )
                for ch in sorted(v["channels"]):
                    fh.write(f"  {ch}:\n")
                    for p in v["channels"][ch]:
                        marker = "*" if p in exceptions_pkg_names else " "
                        fh.write(f"    {marker} {p}\n")
                if v.get("stray_pkgs"):
                    fh.write("  stray (not allowlisted, not in exceptions group):\n")
                    for p, ch in v["stray_pkgs"]:
                        fh.write(f"    {p}  (in {ch})\n")
            fh.write(
                "\n# `*` marks binaries that are members of the "
                "exceptions-packages group.\n"
            )
        if group_covered:
            fh.write(
                "\n## COVERED BY exceptions-packages GROUP\n"
                "# (every cross-channel binary is a member of the "
                "exceptions-packages group, so this is not a real "
                "violation per Azure Linux convention).\n"
            )
            for v in group_covered:
                fh.write(f"\nSRPM {v['srpm']}  ({v['total_pkgs']} pub pkgs)")
                if v["non_exception_channel"]:
                    fh.write(
                        f"  base channel={v['non_exception_channel']}\n"
                    )
                else:
                    fh.write("  (all binaries are exceptions)\n")
                for ch in sorted(v["channels"]):
                    fh.write(f"  {ch}:\n")
                    for p in v["channels"][ch]:
                        marker = "*" if p in exceptions_pkg_names else " "
                        fh.write(f"    {marker} {p}\n")
        if allowlist_covered:
            fh.write("\n## COVERED BY ALLOWLIST\n")
            for v in allowlist_covered:
                e = v["allowlist_entry"]
                fh.write(
                    f"\nSRPM {v['srpm']}  expected={e['expected_channel']}  "
                    f"reason: {e['reason']}\n"
                )
                for ch in sorted(v["channels"]):
                    marker = "  " if ch == e["expected_channel"] else "* "
                    fh.write(f"  {marker}{ch}:\n")
                    for p in v["channels"][ch]:
                        excmark = "[exc]" if p in exceptions_pkg_names else ""
                        fh.write(f"      {p} {excmark}\n")

    json_path.write_text(json.dumps({
        "policy": (
            "every binary RPM produced by an SRPM must publish to the same "
            "channel"
        ),
        "totals": {
            "cross_channel_srpms": len(raw_violations),
            "covered_by_exceptions_group": len(group_covered),
            "covered_by_allowlist": len(allowlist_covered),
            "covered_total": total_covered,
            "uncovered": len(uncovered),
        },
        "uncovered": uncovered,
        "covered_by_exceptions_group": group_covered,
        "covered_by_allowlist": allowlist_covered,
    }, indent=2))

    return {
        "raw_violations": len(raw_violations),
        "covered_by_exceptions_group": len(group_covered),
        "covered_by_allowlist": len(allowlist_covered),
        "covered": total_covered,
        "uncovered": len(uncovered),
        "report_paths": {
            "text": str(txt_path),
            "json": str(json_path),
        },
    }


# ---------------------------------------------------------------------------
# Reporting / summary
# ---------------------------------------------------------------------------

def write_drift_reports(
    *,
    arches: list[str],
    seen_per_arch: dict[str, set[str]],
    unmatched_per_arch: dict[str, set[str]],
    pkg_to_channel: dict[str, str],
    reports_dir: Path,
) -> dict:
    """Write the two repo-vs-channel-map drift reports.

    1. ``rpms-missing-from-channel-map.txt`` (and ``.json``):
       Binary-RPM names that appeared in the input repo(s) for each arch
       but have *no* entry in the channel map (``azldev package list``).
       Typical causes: package recently removed from the tree's package
       lists; package excluded via ``publishChannel = "none"``; typo.
       Reported per-arch.

    2. ``channel-map-missing-from-repos.txt`` (and ``.json``):
       Binary-RPM names that *do* have a channel-map entry but did not
       appear in *any* input repo on *any* arch. Per-arch misses are
       intentionally not reported here because they are dominated by
       legitimate arch-specific exclusions (``ExclusiveArch`` /
       ``ExcludeArch``); only "missing everywhere" is high-signal.

    Returns a summary dict with per-direction totals, also embedded in
    the top-level ``summary.json``.
    """
    channel_map_names = set(pkg_to_channel)

    # Direction 1: RPMs in repos but not in channel map (per-arch).
    direction1: dict[str, list[str]] = {
        arch: sorted(unmatched_per_arch[arch]) for arch in arches
    }
    union1 = sorted(set().union(*direction1.values())) if arches else []

    # Direction 2: channel-map entries missing from EVERY arch's repos.
    seen_anywhere: set[str] = set().union(*seen_per_arch.values()) if arches else set()
    missing_everywhere = sorted(channel_map_names - seen_anywhere)
    direction2 = [
        {"name": n, "expected_channel": pkg_to_channel[n]}
        for n in missing_everywhere
    ]

    # Direction-1 text report.
    txt1 = reports_dir / "rpms-missing-from-channel-map.txt"
    with txt1.open("w") as fh:
        fh.write(
            "# Binary-RPM names found in the input repo(s) that have no "
            "entry in the channel map (`azldev package list`).\n"
            "# These are excluded from the synthesized per-channel "
            "repodata.\n"
            "# Possible causes: package removed from the tree but still "
            "in the published snapshot; publishChannel = \"none\"; typo.\n"
        )
        for arch in arches:
            fh.write(f"\n## arch={arch}  ({len(direction1[arch])} package(s))\n")
            for name in direction1[arch]:
                fh.write(f"{name}\n")
    json1 = reports_dir / "rpms-missing-from-channel-map.json"
    json1.write_text(json.dumps({
        "policy": (
            "binary-RPM names present in the input repos but absent from "
            "the channel map"
        ),
        "per_arch": direction1,
        "any_arch": union1,
        "totals": {arch: len(direction1[arch]) for arch in arches},
    }, indent=2))

    # Direction-2 text report (single list, "missing everywhere").
    txt2 = reports_dir / "channel-map-missing-from-repos.txt"
    with txt2.open("w") as fh:
        fh.write(
            "# Binary-RPM names listed in the channel map (`azldev "
            "package list`) that were NOT found in ANY input repo on "
            "ANY of the analysed arches.\n"
            "# Per-arch misses are intentionally NOT reported here\n"
            "# (they are dominated by legitimate arch-specific\n"
            "# exclusions like ExclusiveArch / ExcludeArch).\n"
            "# Typical causes: package newly added to the tree but not "
            "yet built/published; upstream removal pending sync; typo.\n"
            f"# Total: {len(missing_everywhere)} package(s) "
            f"(across arches: {','.join(arches)})\n\n"
        )
        for entry in direction2:
            fh.write(f"[channel={entry['expected_channel']}] "
                     f"{entry['name']}\n")
    json2 = reports_dir / "channel-map-missing-from-repos.json"
    json2.write_text(json.dumps({
        "policy": (
            "binary-RPM names present in the channel map but absent from "
            "every input repo on every analysed arch"
        ),
        "arches": arches,
        "missing": direction2,
        "total": len(missing_everywhere),
    }, indent=2))

    return {
        "rpms_missing_from_channel_map": {
            arch: len(direction1[arch]) for arch in arches
        },
        "channel_map_missing_from_repos": len(missing_everywhere),
        "report_paths": {
            "rpms_missing_from_channel_map_text": str(txt1),
            "rpms_missing_from_channel_map_json": str(json1),
            "channel_map_missing_from_repos_text": str(txt2),
            "channel_map_missing_from_repos_json": str(json2),
        },
    }


def write_summary(
    summary: dict,
    reports_dir: Path,
    fmt: str,
) -> None:
    summary_txt = reports_dir / "summary.txt"
    summary_json = reports_dir / "summary.json"
    summary_json.write_text(json.dumps(summary, indent=2))

    lines: list[str] = []
    lines.append(
        f"# repoclosure-by-channel summary  scopes={','.join(s['name'] for s in SCOPES)}  "
        f"arches={','.join(summary['arches'])}"
    )
    for r in summary["repoclosure"]:
        t = r["totals"]
        lines.append(
            f"  repoclosure  {r['scope']:<10s} {r['arch']:<8s}  "
            f"raw={t['raw']:>5d}  suppressed={t['suppressed']:>4d}  "
            f"remaining={t['remaining']:>5d}"
        )
    if "srpm_consistency" in summary:
        s = summary["srpm_consistency"]
        lines.append(
            f"  srpm         (any-arch)        cross={s['raw_violations']:>5d}  "
            f"group-cov={s['covered_by_exceptions_group']:>4d}  "
            f"allowlist-cov={s['covered_by_allowlist']:>4d}  "
            f"uncovered={s['uncovered']:>5d}"
        )
    if "drift" in summary:
        d = summary["drift"]
        for arch in summary["arches"]:
            lines.append(
                f"  drift        rpms-no-channel  {arch:<8s}  "
                f"count={d['rpms_missing_from_channel_map'][arch]:>5d}"
            )
        lines.append(
            f"  drift        channel-not-in-repos (every arch)  "
            f"count={d['channel_map_missing_from_repos']:>5d}"
        )
    summary_txt.write_text("\n".join(lines) + "\n")

    if fmt == "json":
        sys.stdout.write(json.dumps(summary, indent=2) + "\n")
    else:
        sys.stdout.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Container self-launch
# ---------------------------------------------------------------------------

def _short_hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:10]


def _build_container_command(
    args: argparse.Namespace,
    repos: list[RepoSpec],
    output_dir: Path,
    docker: str,
    image: str,
) -> tuple[list[str], list[RepoSpec]]:
    """Build the ``docker run`` command and the rewritten RepoSpec list
    that the in-container script should see (with local paths translated
    to mount points).
    """
    docker_cmd: list[str] = [
        docker, "run", "--rm",
        "-e", f"{IN_CONTAINER_ENV}=1",
        # Run as the invoking host user so output files (and intermediate
        # caches under --output) remain owned by the host user. Without
        # this, root-owned artefacts pile up and a re-run fails on
        # `rm -rf` of stale state.
        "--user", f"{os.getuid()}:{os.getgid()}",
        # `dnf5` and `python3` need a writable HOME for caches and
        # locale files; with --user we lose root's /root, so point HOME
        # at the output mount which is guaranteed writable.
        "-e", f"HOME={CONTAINER_OUTPUT}",
        "-v", f"{output_dir}:{CONTAINER_OUTPUT}",
        "-v", f"{Path(__file__).resolve()}:{CONTAINER_SCRIPT}:ro",
    ]
    rewritten: list[RepoSpec] = []
    local_seen: dict[str, str] = {}  # host -> in-container
    for r in repos:
        if r.kind == "local":
            host = r.value
            if host not in local_seen:
                # Use a stable hashed mount dir name so concurrent
                # invocations don't collide.
                cn = f"{CONTAINER_REPO_MOUNTS}/r-{_short_hash(host)}"
                local_seen[host] = cn
                docker_cmd += ["-v", f"{host}:{cn}:ro"]
            rewritten.append(RepoSpec(
                original=r.original, kind="local", value=local_seen[host]
            ))
        else:
            rewritten.append(r)

    # Translate other paths (allowlists, channel-map, output) to in-container.
    docker_cmd += [image, "python3", CONTAINER_SCRIPT]
    docker_cmd += ["--no-container"]  # important: don't recurse
    docker_cmd += ["--output", CONTAINER_OUTPUT]
    docker_cmd += ["--channel-map",
                   f"{CONTAINER_OUTPUT}/{CHANNEL_MAP_FILENAME}"]
    if args.allowlist:
        ah = Path(args.allowlist).resolve()
        ac = f"{CONTAINER_OUTPUT}/.allowlist.toml"
        # We'll copy the allowlist into the output dir before running so
        # we don't need an extra mount; that copying is the caller's
        # responsibility (handled in main()).
        docker_cmd += ["--allowlist", ac]
    if args.srpm_allowlist:
        sah = Path(args.srpm_allowlist).resolve()
        sac = f"{CONTAINER_OUTPUT}/.srpm-allowlist.toml"
        docker_cmd += ["--srpm-allowlist", sac]
    if args.skip_repoclosure:
        docker_cmd.append("--skip-repoclosure")
    if args.skip_srpm_consistency:
        docker_cmd.append("--skip-srpm-consistency")
    if args.no_fail_on_srpm_violations:
        docker_cmd.append("--no-fail-on-srpm-violations")
    if args.no_fail_on_repoclosure:
        docker_cmd.append("--no-fail-on-repoclosure")
    docker_cmd += ["--arches", args.arches]
    docker_cmd += ["--format", args.format]
    for r in rewritten:
        docker_cmd += ["--repo", r.value]
    return docker_cmd, rewritten


_DERIVED_DOCKERFILE = """\
FROM {base}
RUN dnf install -y --setopt=install_weak_deps=False -q \\
        dnf5-plugins python3-createrepo_c && \\
    dnf clean all
"""


def _ensure_image(docker: str, image: str) -> str:
    """Ensure a runnable image with our required packages is available.

    Builds (or rebuilds, layer-cached) a tiny derived image
    ``<image>-repoclosure-tools`` that adds ``dnf5-plugins`` and
    ``python3-createrepo_c``. We need these baked in because we run the
    container as the invoking host user (``--user``), which means we
    cannot ``dnf install`` at runtime.

    Returns the name of the derived image to use.
    """
    try:
        proc = subprocess.run(
            [docker, "image", "inspect", image],
            capture_output=True, text=True,
        )
    except FileNotFoundError as e:
        raise SystemExit(
            f"error: '{docker}' not found on PATH. Install Docker, or "
            f"pass --docker /path/to/docker, or use --no-container."
        ) from e
    if proc.returncode != 0:
        print(f"==> pulling {image} ...")
        subprocess.run([docker, "pull", image], check=True)

    # Sanitize the base image name into a valid tag suffix.
    suffix = re.sub(r"[^a-zA-Z0-9._-]", "-", image)
    derived = f"repoclosure-tools-derived:{suffix}"
    dockerfile = _DERIVED_DOCKERFILE.format(base=image)
    print(f"==> building derived image {derived} (cached on subsequent runs) ...")
    proc = subprocess.run(
        [docker, "build", "-t", derived, "-"],
        input=dockerfile,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise SystemExit(
            f"error: failed to build derived image:\n"
            f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return derived


def _prepare_container_payload(
    output_dir: Path,
    channel_map: list[dict],
    args: argparse.Namespace,
) -> None:
    """Write channel-map snapshot and copy allowlists into the output dir
    so the in-container invocation can see them via the single output mount.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / CHANNEL_MAP_FILENAME).write_text(
        json.dumps(channel_map, indent=2)
    )
    if args.allowlist:
        shutil.copyfile(
            Path(args.allowlist).resolve(),
            output_dir / ".allowlist.toml",
        )
    if args.srpm_allowlist:
        shutil.copyfile(
            Path(args.srpm_allowlist).resolve(),
            output_dir / ".srpm-allowlist.toml",
        )


def _force_wipe_output(args: argparse.Namespace) -> None:
    """Honour ``--force`` by wiping the output dir.

    First tries a plain ``shutil.rmtree``; if that fails (typically
    because previous runs left root-owned artefacts) and we have docker
    available, fall back to letting the container do the wipe.
    """
    output_dir = args.output.resolve()
    if not output_dir.exists():
        return
    try:
        shutil.rmtree(output_dir)
        return
    except PermissionError:
        if args.no_container:
            raise SystemExit(
                f"error: cannot wipe {output_dir} (permission denied) and "
                f"--no-container is set; remove it manually."
            )
        # Fall through to container-assisted wipe.
    print(f"==> using container to wipe root-owned files in {output_dir} ...")
    abs_out = str(output_dir)
    parent = str(output_dir.parent)
    name = output_dir.name
    proc = subprocess.run(
        [
            args.docker, "run", "--rm",
            "-v", f"{parent}:/wipe",
            args.container_image,
            "rm", "-rf", f"/wipe/{name}",
        ],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(
            f"error: container-assisted wipe failed:\n"
            f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )


def maybe_relaunch_in_container(args: argparse.Namespace,
                                repos: list[RepoSpec]) -> None:
    """If we're outside a container and ``--no-container`` is not set,
    set up a fedora:44 container, copy the channel-map snapshot in, and
    re-exec the script inside it. Returns only if running on the host
    (i.e. ``--no-container`` was specified).
    """
    if args.no_container or os.environ.get(IN_CONTAINER_ENV) == "1":
        return  # already inside, or user asked for host execution

    output_dir = args.output.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate channel map on host (where azldev lives).
    if args.channel_map:
        channel_map = json.loads(Path(args.channel_map).read_text())
    else:
        print("==> running azldev package list (host) ...")
        channel_map = load_channel_map_from_azldev(args.repo_root)

    _prepare_container_payload(output_dir, channel_map, args)
    derived_image = _ensure_image(args.docker, args.container_image)

    docker_cmd, _ = _build_container_command(
        args, repos, output_dir,
        docker=args.docker, image=derived_image,
    )
    print(f"==> launching container ({derived_image}) ...")
    print(f"    $ {' '.join(shlex.quote(c) for c in docker_cmd)}")
    rc = subprocess.run(docker_cmd).returncode
    sys.exit(rc)


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------

def main() -> int:
    parser = build_argparser()
    args = parser.parse_args()

    if not args.repo:
        parser.error("at least one --repo is required")

    arches = [a.strip() for a in args.arches.split(",") if a.strip()]
    if not arches:
        parser.error("--arches must specify at least one architecture")

    repos = [RepoSpec.parse(r) for r in args.repo]

    # Honour --force on the host side only (so we don't wipe inside the
    # container after we've already populated the channel-map snapshot).
    if args.force and os.environ.get(IN_CONTAINER_ENV) != "1":
        _force_wipe_output(args)

    # On the host, possibly relaunch in container. The function will
    # exit() if it does so.
    maybe_relaunch_in_container(args, repos)

    # We are now either:
    #   - the host invocation with --no-container; or
    #   - inside the auto-launched container.
    output_dir: Path = args.output.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    reports_dir = output_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    cache_root = output_dir / ".repodata-cache"
    cache_root.mkdir(parents=True, exist_ok=True)

    # Channel map: prefer explicit --channel-map; fall back to azldev.
    if args.channel_map and Path(args.channel_map).exists():
        channel_entries = json.loads(Path(args.channel_map).read_text())
    else:
        channel_entries = load_channel_map_from_azldev(args.repo_root)
    pkg_to_channel, exceptions_pkg_names = channel_map_to_pkg_dict(channel_entries)
    print(
        f"==> channel map: {len(pkg_to_channel)} package(s) with publish info"
        f"  ({len(exceptions_pkg_names)} in exceptions-packages group)"
    )

    # Phase: per-arch synthesize per-channel repodata.
    per_arch_summary: dict[str, dict] = {}
    pkg_to_srpm_global: dict[str, str] = {}
    seen_per_arch: dict[str, set[str]] = {}
    unmatched_per_arch: dict[str, set[str]] = {}
    for arch in arches:
        print(f"==> [{arch}] synthesizing per-channel repodata ...")
        written, pkg_to_srpm, kept_per_repo, seen_names, unmatched_names = (
            synthesize_per_channel_repodata(
                repos=repos,
                arch=arch,
                pkg_to_channel=pkg_to_channel,
                output_arch_root=output_dir,
                cache_root=cache_root,
            )
        )
        per_arch_summary[arch] = {
            "written_per_channel": written,
            "kept_per_repo": kept_per_repo,
            "rpms_in_repos_count": len(seen_names),
            "rpms_missing_from_channel_map": sorted(unmatched_names),
        }
        seen_per_arch[arch] = seen_names
        unmatched_per_arch[arch] = unmatched_names
        # Merge SRPM mapping across arches (later arch can fill gaps).
        for k, v in pkg_to_srpm.items():
            pkg_to_srpm_global.setdefault(k, v)

    # Phase: write the repo-vs-channel-map drift reports.
    print("==> writing repo / channel-map drift reports ...")
    drift_summary = write_drift_reports(
        arches=arches,
        seen_per_arch=seen_per_arch,
        unmatched_per_arch=unmatched_per_arch,
        pkg_to_channel=pkg_to_channel,
        reports_dir=reports_dir,
    )
    rpms_no_channel_str = ", ".join(
        f"{a}={drift_summary['rpms_missing_from_channel_map'][a]}"
        for a in arches
    )
    print(f"    rpms-missing-from-channel-map: {rpms_no_channel_str}")
    print(
        "    channel-map-missing-from-repos (any arch): "
        f"{drift_summary['channel_map_missing_from_repos']}"
    )

    summary: dict = {
        "arches": arches,
        "per_arch": per_arch_summary,
        "scopes": SCOPES,
        "drift": drift_summary,
        "repoclosure": [],
    }

    # Phase: SRPM consistency (arch-independent).
    if not args.skip_srpm_consistency:
        print("==> checking SRPM channel-consistency ...")
        srpm_allow = load_srpm_allowlist(args.srpm_allowlist)
        if srpm_allow:
            print(f"    loaded {len(srpm_allow)} SRPM exception(s) from allowlist")
        srpm_summary = check_srpm_consistency(
            pkg_to_channel=pkg_to_channel,
            pkg_to_srpm=pkg_to_srpm_global,
            allowlist=srpm_allow,
            exceptions_pkg_names=exceptions_pkg_names,
            reports_dir=reports_dir,
        )
        summary["srpm_consistency"] = srpm_summary
        print(
            f"    cross-channel={srpm_summary['raw_violations']} "
            f"group-covered={srpm_summary['covered_by_exceptions_group']} "
            f"allowlist-covered={srpm_summary['covered_by_allowlist']} "
            f"uncovered={srpm_summary['uncovered']}"
        )
    else:
        srpm_summary = {"uncovered": 0}

    # Phase: repoclosure for each (scope, arch).
    if not args.skip_repoclosure:
        allowlist = load_repoclosure_allowlist(args.allowlist)
        if allowlist:
            print(f"==> loaded {len(allowlist)} repoclosure allowlist entr(ies)")
        for scope in SCOPES:
            scope_name = scope["name"]
            for arch in arches:
                # Verify the necessary per-channel/per-arch repos exist.
                missing = []
                for ch in scope["available"]:
                    rd = output_dir / ch / arch / "repodata" / "repomd.xml"
                    if not rd.exists():
                        missing.append(ch)
                if missing:
                    print(f"    [{scope_name}/{arch}] skipping; missing "
                          f"channel(s): {','.join(missing)}")
                    continue
                print(f"==> repoclosure scope={scope_name} arch={arch}")
                repos_for_resolver = [
                    (ch, output_dir / ch / arch)
                    for ch in scope["available"]
                ]
                check_ids = list(scope["check"])
                result = run_repoclosure(
                    scope_name=scope_name,
                    arch=arch,
                    output_root=output_dir,
                    repos_for_resolver=repos_for_resolver,
                    check_repo_ids=check_ids,
                    allowlist=allowlist,
                    reports_dir=reports_dir,
                )
                summary["repoclosure"].append(result)
                t = result["totals"]
                print(f"    raw={t['raw']} suppressed={t['suppressed']} "
                      f"remaining={t['remaining']}")

    write_summary(summary, reports_dir, args.format)

    # Cleanup transient cache (keep .dnf-cache for reproducibility? no,
    # it can be huge). Skip on error so the user can debug.
    shutil.rmtree(cache_root, ignore_errors=True)
    shutil.rmtree(output_dir / ".dnf-cache", ignore_errors=True)

    rc = 0
    if (
        not args.skip_srpm_consistency
        and not args.no_fail_on_srpm_violations
        and srpm_summary.get("uncovered", 0) > 0
    ):
        print(
            f"\nERROR: {srpm_summary['uncovered']} SRPM-consistency "
            f"violation(s) not covered by allowlist.",
            file=sys.stderr,
        )
        rc = 1
    if not args.skip_repoclosure and not args.no_fail_on_repoclosure:
        for r in summary["repoclosure"]:
            if r["totals"]["remaining"] > 0:
                print(
                    f"\nERROR: {r['scope']}/{r['arch']} has "
                    f"{r['totals']['remaining']} unresolved dep(s).",
                    file=sys.stderr,
                )
                rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
