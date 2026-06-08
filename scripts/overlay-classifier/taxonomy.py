# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Overlay classification taxonomy — labels, sub-categories, and heuristic signal patterns.

This module defines the shared vocabulary for the overlay classifier:
- Top-level labels (Backport-fedora, Upstream-fix, AZL-customization)
- AZL-customization sub-categories (10 buckets)
- Signal patterns: compiled regexes + field checks used by the heuristic engine
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------


class TopLevel(Enum):
    """Top-level overlay classification labels."""

    BACKPORT_FEDORA = "Backport-fedora"
    UPSTREAM_FIX = "Upstream-fix"
    AZL_CUSTOMIZATION = "AZL-customization"


class SubCategory(Enum):
    """Sub-categories for AZL-customization and Upstream-fix."""

    # Upstream-fix sub-categories
    UPSTREAMABLE = "Upstreamable"
    WAITING_FOR_FEDORA = "Waiting-for-fedora"

    # AZL-customization sub-categories
    DEPENDENCY_PRUNING = "Dependency-pruning"
    FEATURE_DISABLEMENT = "Feature-disablement"
    BRANDING = "Branding"
    BUILD_ENVIRONMENT = "Build-environment"
    TEST_DISABLEMENT = "Test-disablement"
    SECURITY_COMPLIANCE = "Security/compliance"
    RELEASE_MANAGEMENT = "Release-management"
    MISSING_DEPENDENCY_WORKAROUND = "Missing-dependency-workaround"
    PLATFORM_ADAPTATION = "Platform-adaptation"
    DISTRO_POLICY_ALIGNMENT = "Distro-policy-alignment"


# ---------------------------------------------------------------------------
# Signal pattern definitions
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Signal:
    """A single heuristic signal that can fire against an overlay's data."""

    name: str
    fields: Sequence[str]
    """Which text fields to search: 'description', 'comments', 'commit_header',
    'commit_body', 'all_text', or structured fields like 'overlay_type', 'tag'."""
    pattern: re.Pattern[str] | None = None
    """Regex to match against the text fields. None for structural checks."""
    structural_check: str | None = None
    """Name of a structural check function (handled in classify_overlays.py)."""


@dataclass(frozen=True)
class Rule:
    """A classification rule: a set of signals that, when matched, assign a label."""

    name: str
    top_level: TopLevel
    sub_category: SubCategory | None = None
    signals: Sequence[Signal] = field(default_factory=list)
    priority: int = 0
    """Higher priority rules are evaluated first. Ties broken by definition order."""
    require_all: bool = False
    """When True, ALL signals must match for the rule to fire (AND logic).
    Default False means ANY signal match fires the rule (OR logic)."""


# ---------------------------------------------------------------------------
# Compiled signal patterns
# ---------------------------------------------------------------------------

# -- Backport-fedora signals --

_SIG_FEDORA_COMMIT_URL = Signal(
    name="fedora-commit-url",
    fields=["comments", "commit_body", "all_text"],
    pattern=re.compile(r"src\.fedoraproject\.org/rpms/.*/c/", re.IGNORECASE),
)

_SIG_BACKPORT_KEYWORD = Signal(
    name="backport-keyword",
    fields=["all_text"],
    pattern=re.compile(r"\b(?:backport\w*|cherry[- ]?pick\w*)\b", re.IGNORECASE),
)

_SIG_TEMPORARY_SNAPSHOT = Signal(
    name="temporary-snapshot",
    fields=["description"],
    pattern=re.compile(r"[Tt]emporary.*[Rr]emove when snapshot includes", re.IGNORECASE),
)

_SIG_FIXED_UPSTREAM_FEDORA = Signal(
    name="fixed-upstream-fedora",
    fields=["all_text"],
    pattern=re.compile(
        r"(?:fixed (?:upstream )?in f4\d|fixed in fedora|landed in rawhide)",
        re.IGNORECASE,
    ),
)

# -- Upstream-fix signals --

_SIG_CVE = Signal(
    name="cve-reference",
    fields=["all_text"],
    pattern=re.compile(r"CVE-\d{4}-\d+", re.IGNORECASE),
)

_SIG_UPSTREAM_BUG_URL = Signal(
    name="upstream-bug-url",
    fields=["comments", "commit_body"],
    pattern=re.compile(
        r"(?:github\.com/.*/issues/|bugzilla\.redhat\.com|bugs\..*\.org)",
        re.IGNORECASE,
    ),
)

_SIG_UPSTREAM_COMMIT_URL = Signal(
    name="upstream-commit-url",
    fields=["comments", "commit_body"],
    pattern=re.compile(
        r"github\.com/.*/commit/[0-9a-f]",
        re.IGNORECASE,
    ),
)

_SIG_UPSTREAM_PR_URL = Signal(
    name="upstream-pr-url",
    fields=["all_text"],
    pattern=re.compile(
        r"github\.com/[^\s/]+/[^\s/]+/pull/\d+",
        re.IGNORECASE,
    ),
)

_SIG_UPSTREAM_BUG_ID = Signal(
    name="upstream-bug-id",
    fields=["all_text"],
    pattern=re.compile(
        r"\b(?:[A-Z]{2,10}-\d+|GH-\d+)\b",
    ),
)

_SIG_PATCH_ADD_NO_FEDORA = Signal(
    name="patch-add-no-fedora-url",
    fields=[],
    structural_check="patch_add_without_fedora_url",
)

_SIG_PATCH_FROM_UPSTREAM_AUTHOR = Signal(
    name="patch-from-upstream-author",
    fields=[],
    structural_check="patch_from_upstream_author",
)

_SIG_FIX_COMMIT_HEADER = Signal(
    name="fix-commit-header-no-azl",
    fields=[],
    structural_check="fix_header_without_azl_keywords",
)

_SIG_UPSTREAM_FIX_KEYWORD = Signal(
    name="upstream-fix-keyword",
    fields=["all_text"],
    pattern=re.compile(r"(?:fix for upstream|upstream bug|upstream regression)", re.IGNORECASE),
)

# -- Workaround signal (overrides upstream-fix when overlay is a workaround, not the fix) --

_SIG_WORKAROUND_KEYWORD = Signal(
    name="workaround-keyword",
    fields=["all_text"],
    pattern=re.compile(
        r"\b(?:work[- ]?around|workaround|until (?:the )?(?:upstream|fix)|for now[,:]?\s+disable)\b",
        re.IGNORECASE,
    ),
)

# -- AZL-customization / Dependency-pruning --

_SIG_REMOVE_DEP_TAG = Signal(
    name="remove-dep-tag",
    fields=[],
    structural_check="remove_dep_tag",
)

_SIG_NOT_AVAILABLE = Signal(
    name="not-available-in-azl",
    fields=["all_text"],
    pattern=re.compile(
        r"not (?:available|shipped|packaged|imported) (?:in|for) (?:AZL|Azure Linux)",
        re.IGNORECASE,
    ),
)

_SIG_REMOVING_FROM_DISTRO = Signal(
    name="removing-from-distro",
    fields=["all_text"],
    pattern=re.compile(
        r"(?:removing .* from the distro|drop.*(?:BuildRequires|Requires))",
        re.IGNORECASE,
    ),
)

# -- AZL-customization / Feature-disablement --

_SIG_BUILD_WITHOUT = Signal(
    name="build-without",
    fields=[],
    structural_check="has_build_without",
)

_SIG_MINGW_GROUP = Signal(
    name="mingw-group",
    fields=[],
    structural_check="in_mingw_group",
)

_SIG_DISABLE_KEYWORD = Signal(
    name="disable-keyword",
    fields=["all_text"],
    pattern=re.compile(
        r"\b(?:disable|disabling|drop.*subpackage|remove.*subpackage)\b",
        re.IGNORECASE,
    ),
)

_SIG_WITH_X_ZERO = Signal(
    name="with-x-zero",
    fields=["value", "replacement"],
    pattern=re.compile(r"%global\s+with_\w+\s+0|with_\w+\s+0"),
)

_SIG_MESON_CMAKE_OFF = Signal(
    name="meson-cmake-off",
    fields=["replacement", "value"],
    pattern=re.compile(r"=(?:false|off|disabled)\b", re.IGNORECASE),
)

_SIG_REMOVE_SUBPACKAGE = Signal(
    name="remove-subpackage-type",
    fields=["overlay_type"],
    pattern=re.compile(r"^spec-remove-subpackage$"),
)

# -- AZL-customization / Branding --

_SIG_FEDORA_TO_AZL = Signal(
    name="fedora-to-azl-replacement",
    fields=["regex", "replacement"],
    pattern=re.compile(r"(?:[Ff]edora|redhat).*(?:[Aa]zure[Ll]inux|azurelinux)", re.IGNORECASE),
)

_SIG_SET_DISTRO_VARIANT = Signal(
    name="set-distro-variant",
    fields=["description"],
    pattern=re.compile(r"[Ss]et (?:distro|variant|vendor) to azurelinux", re.IGNORECASE),
)

_SIG_BRANDING_KEYWORD = Signal(
    name="branding-keyword",
    fields=["all_text"],
    pattern=re.compile(r"\b(?:branding|rebrand)\b", re.IGNORECASE),
)

# -- AZL-customization / Build-environment --

_SIG_COMPILER_FLAGS = Signal(
    name="compiler-flags",
    fields=["all_text"],
    pattern=re.compile(r"(?:-std=gnu\d+|CFLAGS|LDFLAGS|compiler flag)", re.IGNORECASE),
)

_SIG_TRIPLET = Signal(
    name="triplet-fix",
    fields=["all_text"],
    pattern=re.compile(r"\b(?:triple|triplet|_target_platform)\b", re.IGNORECASE),
)

_SIG_MOCK_CONTAINER = Signal(
    name="mock-container-env",
    fields=["all_text"],
    pattern=re.compile(r"\b(?:mock|containerized|container build|Koji builder)\b", re.IGNORECASE),
)

_SIG_TOOLCHAIN = Signal(
    name="toolchain-keyword",
    fields=["all_text"],
    pattern=re.compile(r"\b(?:toolchain|compiler-rt|gcc|clang)\b", re.IGNORECASE),
)

_SIG_AUTOSETUP = Signal(
    name="autosetup-keyword",
    fields=["description"],
    pattern=re.compile(r"%autosetup", re.IGNORECASE),
)

# -- AZL-customization / Test-disablement --

_SIG_CHECK_SKIP_GROUP = Signal(
    name="check-skip-group",
    fields=[],
    structural_check="in_check_skip_group",
)

_SIG_CHECK_SKIP_CONFIG = Signal(
    name="check-skip-config",
    fields=[],
    structural_check="has_check_skip",
)

_SIG_SKIP_TEST_KEYWORD = Signal(
    name="skip-test-keyword",
    fields=["all_text"],
    pattern=re.compile(
        r"(?:[Ss]kip.*test|[Dd]isable.*test|expected failure|skip.*check)",
        re.IGNORECASE,
    ),
)

# -- AZL-customization / Security/compliance --

_SIG_FIPS = Signal(
    name="fips-keyword",
    fields=["all_text"],
    pattern=re.compile(r"\b(?:[Ff]ips|fips\.so|fips-provider|fipsmodule)\b"),
)

_SIG_CRYPTO_SECURITY = Signal(
    name="crypto-security-keyword",
    fields=["all_text"],
    pattern=re.compile(
        r"\b(?:crypto[- ]?policy|compliance|security hardening|malware.scan)\b",
        re.IGNORECASE,
    ),
)

# -- AZL-customization / Release-management --

_SIG_RELEASE_TAG = Signal(
    name="release-tag-overlay",
    fields=[],
    structural_check="is_release_tag_overlay",
)

_SIG_RELEASE_KEYWORD = Signal(
    name="release-keyword",
    fields=["description"],
    pattern=re.compile(
        r"(?:Release tag|%autorelease|pkgrelease|specrelease|baserelease)",
        re.IGNORECASE,
    ),
)

# -- AZL-customization / Missing-dependency-workaround --

_SIG_WORKAROUND_PREFIX = Signal(
    name="workaround-prefix",
    fields=["description"],
    pattern=re.compile(r"^WORKAROUND:", re.IGNORECASE),
)

_SIG_NOT_YET = Signal(
    name="not-yet-keyword",
    fields=["all_text"],
    pattern=re.compile(r"not yet (?:in AZL|imported|available|packaged)", re.IGNORECASE),
)

_SIG_BOOTSTRAP = Signal(
    name="bootstrap-keyword",
    fields=["all_text"],
    pattern=re.compile(r"\bbootstrap\b", re.IGNORECASE),
)

# -- AZL-customization / Platform-adaptation --

_SIG_ARCH_KEYWORD = Signal(
    name="arch-keyword",
    fields=["description"],
    pattern=re.compile(r"\b(?:aarch64|ARM64|SVE|ExcludeArch|ExclusiveArch)\b", re.IGNORECASE),
)

# -- AZL-customization / Distro-policy-alignment --

_SIG_RHEL_ALIGNMENT = Signal(
    name="rhel-alignment",
    fields=["all_text"],
    pattern=re.compile(r"(?:RHEL[- ]aligned|enterprise|--with-distro=redhat)", re.IGNORECASE),
)

_SIG_RHEL_DEFINE = Signal(
    name="rhel-build-define",
    fields=[],
    structural_check="has_rhel_define",
)


# ---------------------------------------------------------------------------
# Rule registry — evaluated in priority order (highest first)
# ---------------------------------------------------------------------------

RULES: list[Rule] = [
    # -- Backport-fedora (priority 100) --
    Rule(
        name="backport-fedora-commit-url",
        top_level=TopLevel.BACKPORT_FEDORA,
        signals=[_SIG_FEDORA_COMMIT_URL],
        priority=100,
    ),
    Rule(
        name="backport-keyword",
        top_level=TopLevel.BACKPORT_FEDORA,
        signals=[_SIG_BACKPORT_KEYWORD],
        priority=95,
    ),
    Rule(
        name="backport-temporary-snapshot",
        top_level=TopLevel.BACKPORT_FEDORA,
        signals=[_SIG_TEMPORARY_SNAPSHOT],
        priority=90,
    ),
    Rule(
        name="backport-fixed-upstream-fedora",
        top_level=TopLevel.BACKPORT_FEDORA,
        signals=[_SIG_FIXED_UPSTREAM_FEDORA],
        priority=90,
    ),
    # -- Workaround override (priority 85) --
    # When an overlay explicitly says "workaround" or "until upstream fix" AND
    # disables a feature, it's AZL-customization even if upstream URLs are present.
    Rule(
        name="azl-workaround-feature-disable",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.FEATURE_DISABLEMENT,
        signals=[_SIG_WORKAROUND_KEYWORD, _SIG_DISABLE_KEYWORD],
        priority=85,
        require_all=True,
    ),
    # -- Upstream-fix / Waiting-for-fedora (has upstream refs) --
    Rule(
        name="upstream-fix-cve",
        top_level=TopLevel.UPSTREAM_FIX,
        sub_category=SubCategory.WAITING_FOR_FEDORA,
        signals=[_SIG_CVE],
        priority=80,
    ),
    Rule(
        name="upstream-fix-bug-url",
        top_level=TopLevel.UPSTREAM_FIX,
        sub_category=SubCategory.WAITING_FOR_FEDORA,
        signals=[_SIG_UPSTREAM_BUG_URL],
        priority=75,
    ),
    Rule(
        name="upstream-fix-commit-url",
        top_level=TopLevel.UPSTREAM_FIX,
        sub_category=SubCategory.WAITING_FOR_FEDORA,
        signals=[_SIG_UPSTREAM_COMMIT_URL],
        priority=75,
    ),
    Rule(
        name="upstream-fix-pr-url",
        top_level=TopLevel.UPSTREAM_FIX,
        sub_category=SubCategory.WAITING_FOR_FEDORA,
        signals=[_SIG_UPSTREAM_PR_URL],
        priority=75,
    ),
    Rule(
        name="upstream-fix-bug-id",
        top_level=TopLevel.UPSTREAM_FIX,
        sub_category=SubCategory.WAITING_FOR_FEDORA,
        signals=[_SIG_UPSTREAM_BUG_ID],
        priority=70,
    ),
    # -- Upstream-fix / Upstreamable (no upstream refs yet) --
    Rule(
        name="upstream-fix-patch-from-upstream",
        top_level=TopLevel.UPSTREAM_FIX,
        sub_category=SubCategory.WAITING_FOR_FEDORA,
        signals=[_SIG_PATCH_FROM_UPSTREAM_AUTHOR],
        priority=72,
    ),
    Rule(
        name="upstream-fix-patch-add",
        top_level=TopLevel.UPSTREAM_FIX,
        sub_category=SubCategory.UPSTREAMABLE,
        signals=[_SIG_PATCH_ADD_NO_FEDORA],
        priority=70,
    ),
    Rule(
        name="upstream-fix-commit-header",
        top_level=TopLevel.UPSTREAM_FIX,
        sub_category=SubCategory.UPSTREAMABLE,
        signals=[_SIG_FIX_COMMIT_HEADER],
        priority=65,
    ),
    Rule(
        name="upstream-fix-keyword",
        top_level=TopLevel.UPSTREAM_FIX,
        sub_category=SubCategory.UPSTREAMABLE,
        signals=[_SIG_UPSTREAM_FIX_KEYWORD],
        priority=65,
    ),
    # -- AZL-customization sub-categories (priority 50 down) --
    # Test-disablement
    Rule(
        name="azl-test-skip-group",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.TEST_DISABLEMENT,
        signals=[_SIG_CHECK_SKIP_GROUP],
        priority=55,
    ),
    Rule(
        name="azl-test-skip-config",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.TEST_DISABLEMENT,
        signals=[_SIG_CHECK_SKIP_CONFIG],
        priority=55,
    ),
    Rule(
        name="azl-test-skip-keyword",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.TEST_DISABLEMENT,
        signals=[_SIG_SKIP_TEST_KEYWORD],
        priority=50,
    ),
    # Security/compliance
    Rule(
        name="azl-security-fips",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.SECURITY_COMPLIANCE,
        signals=[_SIG_FIPS],
        priority=52,
    ),
    Rule(
        name="azl-security-crypto",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.SECURITY_COMPLIANCE,
        signals=[_SIG_CRYPTO_SECURITY],
        priority=50,
    ),
    # Missing-dependency-workaround
    Rule(
        name="azl-missing-dep-workaround-prefix",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.MISSING_DEPENDENCY_WORKAROUND,
        signals=[_SIG_WORKAROUND_PREFIX],
        priority=52,
    ),
    Rule(
        name="azl-missing-dep-not-yet",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.MISSING_DEPENDENCY_WORKAROUND,
        signals=[_SIG_NOT_YET],
        priority=50,
    ),
    Rule(
        name="azl-missing-dep-bootstrap",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.MISSING_DEPENDENCY_WORKAROUND,
        signals=[_SIG_BOOTSTRAP],
        priority=45,
    ),
    # Release-management
    Rule(
        name="azl-release-tag-overlay",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.RELEASE_MANAGEMENT,
        signals=[_SIG_RELEASE_TAG],
        priority=50,
    ),
    Rule(
        name="azl-release-keyword",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.RELEASE_MANAGEMENT,
        signals=[_SIG_RELEASE_KEYWORD],
        priority=48,
    ),
    # Branding
    Rule(
        name="azl-branding-replacement",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.BRANDING,
        signals=[_SIG_FEDORA_TO_AZL],
        priority=50,
    ),
    Rule(
        name="azl-branding-set-distro",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.BRANDING,
        signals=[_SIG_SET_DISTRO_VARIANT],
        priority=50,
    ),
    Rule(
        name="azl-branding-keyword",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.BRANDING,
        signals=[_SIG_BRANDING_KEYWORD],
        priority=45,
    ),
    # Feature-disablement
    Rule(
        name="azl-feature-mingw-group",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.FEATURE_DISABLEMENT,
        signals=[_SIG_MINGW_GROUP],
        priority=55,
    ),
    Rule(
        name="azl-feature-build-without",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.FEATURE_DISABLEMENT,
        signals=[_SIG_BUILD_WITHOUT],
        priority=50,
    ),
    Rule(
        name="azl-feature-disable-keyword",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.FEATURE_DISABLEMENT,
        signals=[_SIG_DISABLE_KEYWORD],
        priority=45,
    ),
    Rule(
        name="azl-feature-with-x-zero",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.FEATURE_DISABLEMENT,
        signals=[_SIG_WITH_X_ZERO],
        priority=45,
    ),
    Rule(
        name="azl-feature-meson-cmake-off",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.FEATURE_DISABLEMENT,
        signals=[_SIG_MESON_CMAKE_OFF],
        priority=40,
    ),
    Rule(
        name="azl-feature-remove-subpackage",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.FEATURE_DISABLEMENT,
        signals=[_SIG_REMOVE_SUBPACKAGE],
        priority=45,
    ),
    # Dependency-pruning
    Rule(
        name="azl-dep-remove-tag",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.DEPENDENCY_PRUNING,
        signals=[_SIG_REMOVE_DEP_TAG],
        priority=48,
    ),
    Rule(
        name="azl-dep-not-available",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.DEPENDENCY_PRUNING,
        signals=[_SIG_NOT_AVAILABLE],
        priority=50,
    ),
    Rule(
        name="azl-dep-removing-from-distro",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.DEPENDENCY_PRUNING,
        signals=[_SIG_REMOVING_FROM_DISTRO],
        priority=48,
    ),
    # Build-environment
    Rule(
        name="azl-build-compiler-flags",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.BUILD_ENVIRONMENT,
        signals=[_SIG_COMPILER_FLAGS],
        priority=45,
    ),
    Rule(
        name="azl-build-triplet",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.BUILD_ENVIRONMENT,
        signals=[_SIG_TRIPLET],
        priority=45,
    ),
    Rule(
        name="azl-build-mock-container",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.BUILD_ENVIRONMENT,
        signals=[_SIG_MOCK_CONTAINER],
        priority=40,
    ),
    Rule(
        name="azl-build-toolchain",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.BUILD_ENVIRONMENT,
        signals=[_SIG_TOOLCHAIN],
        priority=38,
    ),
    Rule(
        name="azl-build-autosetup",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.BUILD_ENVIRONMENT,
        signals=[_SIG_AUTOSETUP],
        priority=35,
    ),
    # Platform-adaptation
    Rule(
        name="azl-platform-arch",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.PLATFORM_ADAPTATION,
        signals=[_SIG_ARCH_KEYWORD],
        priority=45,
    ),
    # Distro-policy-alignment
    Rule(
        name="azl-distro-rhel-alignment",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.DISTRO_POLICY_ALIGNMENT,
        signals=[_SIG_RHEL_ALIGNMENT],
        priority=45,
    ),
    Rule(
        name="azl-distro-rhel-define",
        top_level=TopLevel.AZL_CUSTOMIZATION,
        sub_category=SubCategory.DISTRO_POLICY_ALIGNMENT,
        signals=[_SIG_RHEL_DEFINE],
        priority=40,
    ),
]

# Pre-sort by descending priority for evaluation order
RULES.sort(key=lambda r: r.priority, reverse=True)
