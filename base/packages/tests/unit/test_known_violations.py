# SPDX-License-Identifier: MIT
"""Pure-python unit tests for the known-violations loader and classifier.

These tests pin the loader's TOML / JSON-Schema acceptance rules and
the four-way classifier (real-fail / known-violation / stale-consumer
/ stale-dep) without touching the dnf stack, the network, or any
real RPM repo. They run in well under a second.

Coverage targets:

* schema / loader regression cases (M3 / S3 / S4 / S2 from the deep
  reviews) and the rest of the loader contract;
* classifier 4-way matrix, the empty-observed S2 guard, arch-gated
  projection, and the ST2 metadata round-trip
  (``KnownViolationsEntry.reason`` / ``.issue`` propagating into
  ``Verdict``).
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from utils.known_violations import (
    KnownViolationsEntry,
    KnownViolationsError,
    classify_violations,
    load_known_violations,
    resolve_known_violations_for_arch,
)


def _write_toml(tmp_path: Path, body: str) -> Path:
    """Write ``body`` to a ``.toml`` under ``tmp_path`` and return the path."""
    path = tmp_path / "known-violations.toml"
    path.write_text(textwrap.dedent(body).lstrip("\n"))
    return path


# ---------------------------------------------------------------------------
# Loader / schema regression
# ---------------------------------------------------------------------------


class TestLoaderHappyPaths:
    def test_minimal_flat_section(self, tmp_path: Path) -> None:
        path = _write_toml(
            tmp_path,
            """
            schema-version = 1

            [runtime-missing]
            foo = ["bar"]
            """,
        )
        f = load_known_violations(path)
        assert f.schema_version == 1
        section = f.section("runtime-missing")
        assert "foo" in section
        entry = section["foo"]
        assert isinstance(entry, KnownViolationsEntry)
        assert entry.deps == frozenset({"bar"})
        assert entry.reason is None
        assert entry.issue is None

    def test_arch_gated_section(self, tmp_path: Path) -> None:
        path = _write_toml(
            tmp_path,
            """
            schema-version = 1

            [runtime-missing-arch-gated.foo]
            x86_64 = ["only-x86"]
            aarch64 = ["only-arm"]
            """,
        )
        f = load_known_violations(path)
        section = f.section("runtime-missing")
        assert set(section) == {"foo"}
        per_arch = section["foo"]
        assert set(per_arch) == {"x86_64", "aarch64"}
        assert per_arch["x86_64"].deps == frozenset({"only-x86"})
        assert per_arch["aarch64"].deps == frozenset({"only-arm"})

    def test_long_form_round_trip(self, tmp_path: Path) -> None:
        """ST2 inline-table form populates ``reason`` / ``issue``."""
        path = _write_toml(
            tmp_path,
            """
            schema-version = 1

            [runtime-missing]
            foo = { deps = ["bar"], reason = "deprecated upstream", issue = "AB#42" }
            """,
        )
        entry = load_known_violations(path).section("runtime-missing")["foo"]
        assert entry.deps == frozenset({"bar"})
        assert entry.reason == "deprecated upstream"
        assert entry.issue == "AB#42"

    def test_long_form_optional_fields_default_to_none(
        self, tmp_path: Path
    ) -> None:
        path = _write_toml(
            tmp_path,
            """
            schema-version = 1

            [runtime-missing]
            foo = { deps = ["bar"] }
            """,
        )
        entry = load_known_violations(path).section("runtime-missing")["foo"]
        assert entry.deps == frozenset({"bar"})
        assert entry.reason is None
        assert entry.issue is None

    def test_short_and_long_form_mixed(self, tmp_path: Path) -> None:
        path = _write_toml(
            tmp_path,
            """
            schema-version = 1

            [runtime-missing]
            short = ["a"]
            long = { deps = ["b"], reason = "r" }
            """,
        )
        section = load_known_violations(path).section("runtime-missing")
        assert section["short"].deps == frozenset({"a"})
        assert section["short"].reason is None
        assert section["long"].deps == frozenset({"b"})
        assert section["long"].reason == "r"

    def test_empty_section_placeholder_accepted(self, tmp_path: Path) -> None:
        """S3: an empty section body is a valid scaffolding placeholder."""
        path = _write_toml(
            tmp_path,
            """
            schema-version = 1

            [runtime-missing]
            """,
        )
        assert load_known_violations(path).section("runtime-missing") == {}

    def test_section_without_explicit_entry_returns_empty(
        self, tmp_path: Path
    ) -> None:
        """``KnownViolationsFile.section`` defaults missing sections to {}."""
        path = _write_toml(
            tmp_path,
            """
            schema-version = 1
            """,
        )
        assert load_known_violations(path).section("missing-section") == {}


class TestLoaderRejections:
    def test_missing_file_raises_clear_error(self, tmp_path: Path) -> None:
        with pytest.raises(KnownViolationsError, match="not found"):
            load_known_violations(tmp_path / "nope.toml")

    def test_invalid_toml(self, tmp_path: Path) -> None:
        path = tmp_path / "bad.toml"
        path.write_text("schema-version = 1\n[unterminated\n")
        with pytest.raises(KnownViolationsError, match="invalid TOML"):
            load_known_violations(path)

    def test_bad_schema_version_rejected_by_schema(
        self, tmp_path: Path
    ) -> None:
        """S4: schema's ``const: 1`` is the only enforcement we keep."""
        path = _write_toml(
            tmp_path,
            """
            schema-version = 2

            [runtime-missing]
            foo = ["bar"]
            """,
        )
        with pytest.raises(KnownViolationsError, match="1 was expected"):
            load_known_violations(path)

    def test_missing_schema_version_rejected(self, tmp_path: Path) -> None:
        path = _write_toml(
            tmp_path,
            """
            [runtime-missing]
            foo = ["bar"]
            """,
        )
        with pytest.raises(
            KnownViolationsError, match="'schema-version' is a required property"
        ):
            load_known_violations(path)

    def test_m3a_flat_named_section_with_arch_gated_content(
        self, tmp_path: Path
    ) -> None:
        """M3 case (a): a flat-named section with arch-gated content
        is now rejected at schema level (was previously misclassified).
        """
        path = _write_toml(
            tmp_path,
            """
            schema-version = 1

            [runtime-missing.foo]
            x86_64 = ["bad-dep"]
            """,
        )
        with pytest.raises(
            KnownViolationsError, match="schema violation at runtime-missing"
        ):
            load_known_violations(path)

    def test_m3b_arch_gated_named_section_with_flat_content(
        self, tmp_path: Path
    ) -> None:
        """M3 case (b): an arch-gated-named section with flat content
        is now rejected at schema level (was previously an opaque
        AttributeError deep in the loader).
        """
        path = _write_toml(
            tmp_path,
            """
            schema-version = 1

            [runtime-missing-arch-gated]
            foo = ["bar"]
            """,
        )
        with pytest.raises(
            KnownViolationsError,
            match="schema violation at runtime-missing-arch-gated",
        ):
            load_known_violations(path)

    def test_long_form_missing_deps_rejected(self, tmp_path: Path) -> None:
        path = _write_toml(
            tmp_path,
            """
            schema-version = 1

            [runtime-missing]
            foo = { reason = "no deps -- nonsense" }
            """,
        )
        with pytest.raises(
            KnownViolationsError, match="'deps' is a required property"
        ):
            load_known_violations(path)

    def test_long_form_empty_deps_rejected(self, tmp_path: Path) -> None:
        path = _write_toml(
            tmp_path,
            """
            schema-version = 1

            [runtime-missing]
            foo = { deps = [] }
            """,
        )
        with pytest.raises(KnownViolationsError, match="should be non-empty"):
            load_known_violations(path)

    def test_long_form_extra_property_rejected(self, tmp_path: Path) -> None:
        path = _write_toml(
            tmp_path,
            """
            schema-version = 1

            [runtime-missing]
            foo = { deps = ["a"], owner = "alice" }
            """,
        )
        with pytest.raises(
            KnownViolationsError, match="Additional properties are not allowed"
        ):
            load_known_violations(path)

    def test_duplicate_name_in_flat_and_arch_gated(self, tmp_path: Path) -> None:
        """Existing _merge_section guard: same name in both tables."""
        path = _write_toml(
            tmp_path,
            """
            schema-version = 1

            [runtime-missing]
            foo = ["a"]

            [runtime-missing-arch-gated.foo]
            x86_64 = ["b"]
            """,
        )
        with pytest.raises(
            KnownViolationsError, match="appears in both"
        ):
            load_known_violations(path)


# ---------------------------------------------------------------------------
# resolve_known_violations_for_arch
# ---------------------------------------------------------------------------


class TestArchProjection:
    def test_flat_entries_apply_on_every_arch(self) -> None:
        amap = {"foo": KnownViolationsEntry(deps=frozenset({"a"}))}
        for arch in ("x86_64", "aarch64", "ppc64le"):
            out = resolve_known_violations_for_arch(amap, arch)
            assert out == amap

    def test_arch_gated_entry_present_only_on_listed_arch(self) -> None:
        per_arch = {
            "x86_64": KnownViolationsEntry(deps=frozenset({"only-x86"})),
        }
        amap = {"foo": per_arch}
        x86 = resolve_known_violations_for_arch(amap, "x86_64")
        assert x86["foo"].deps == frozenset({"only-x86"})
        arm = resolve_known_violations_for_arch(amap, "aarch64")
        assert "foo" not in arm

    def test_invalid_value_type_raises(self) -> None:
        with pytest.raises(TypeError, match="must be KnownViolationsEntry"):
            resolve_known_violations_for_arch(
                {"foo": ["not-an-entry"]},  # type: ignore[arg-type]
                "x86_64",
            )


# ---------------------------------------------------------------------------
# Classifier 4-way matrix
# ---------------------------------------------------------------------------


def _classify(findings, allowlist, *, arch="x86_64"):
    return classify_violations(
        findings=findings,
        consumer_of=lambda key: key,
        arch=arch,
        allowlist=allowlist,
    )


class TestClassifier:
    def test_observed_subset_of_listed_is_xfail(self) -> None:
        amap = {"foo": KnownViolationsEntry(deps=frozenset({"a", "b"}))}
        c = _classify({"foo": ["a"]}, amap)
        assert len(c.known_violations) == 1
        assert c.real_fails == []
        v = c.known_violations[0]
        assert v.observed == frozenset({"a"})
        assert v.listed == frozenset({"a", "b"})
        assert v.classification == "xfail"

    def test_observed_equal_to_listed_is_xfail(self) -> None:
        amap = {"foo": KnownViolationsEntry(deps=frozenset({"a"}))}
        c = _classify({"foo": ["a"]}, amap)
        assert len(c.known_violations) == 1
        assert c.real_fails == []
        assert all(s.kind != "stale-dep" for s in c.stale)

    def test_observed_exceeds_listed_is_real_fail(self) -> None:
        amap = {"foo": KnownViolationsEntry(deps=frozenset({"a"}))}
        c = _classify({"foo": ["a", "b"]}, amap)
        assert c.known_violations == []
        assert len(c.real_fails) == 1
        v = c.real_fails[0]
        assert v.listed == frozenset({"a"})

    def test_consumer_not_in_allowlist_is_real_fail_with_listed_none(
        self,
    ) -> None:
        c = _classify({"foo": ["a"]}, {})
        assert c.known_violations == []
        assert len(c.real_fails) == 1
        assert c.real_fails[0].listed is None

    def test_consumer_in_allowlist_but_no_findings_is_stale_consumer(
        self,
    ) -> None:
        amap = {"foo": KnownViolationsEntry(deps=frozenset({"a"}))}
        c = _classify({}, amap)
        assert c.real_fails == []
        assert c.known_violations == []
        assert any(
            s.kind == "stale-consumer" and s.consumer == "foo"
            for s in c.stale
        )

    def test_listed_dep_not_observed_is_stale_dep(self) -> None:
        amap = {"foo": KnownViolationsEntry(deps=frozenset({"a", "b"}))}
        c = _classify({"foo": ["a"]}, amap)
        assert any(
            s.kind == "stale-dep" and s.consumer == "foo" and s.listed_dep == "b"
            for s in c.stale
        )
        assert not any(
            s.kind == "stale-dep" and s.listed_dep == "a"
            for s in c.stale
        )

    def test_empty_observed_skipped_no_phantom_xfail(self) -> None:
        """S2 guard: empty observed must NOT vacuously match every entry
        and must not silence the stale-consumer signal.
        """
        amap = {"foo": KnownViolationsEntry(deps=frozenset({"a"}))}
        c = _classify({"foo": ()}, amap)
        assert c.known_violations == []
        assert c.real_fails == []
        assert any(
            s.kind == "stale-consumer" and s.consumer == "foo" for s in c.stale
        )

    def test_arch_gated_missing_arch_treats_as_unlisted(self) -> None:
        amap = {
            "foo": {
                "x86_64": KnownViolationsEntry(deps=frozenset({"a"})),
            }
        }
        c = _classify({"foo": ["a"]}, amap, arch="aarch64")
        assert c.known_violations == []
        assert len(c.real_fails) == 1
        assert c.real_fails[0].listed is None
        assert not any(
            s.kind == "stale-consumer" and s.consumer == "foo" for s in c.stale
        )

    def test_metadata_propagates_to_verdict(self) -> None:
        """ST2: ``reason`` / ``issue`` round-trip into Verdict."""
        amap = {
            "foo": KnownViolationsEntry(
                deps=frozenset({"a"}),
                reason="deprecated upstream",
                issue="AB#42",
            )
        }
        c = _classify({"foo": ["a"]}, amap)
        v = c.known_violations[0]
        assert v.reason == "deprecated upstream"
        assert v.issue == "AB#42"

    def test_metadata_propagates_to_over_ceiling_real_fail(self) -> None:
        """Listed entry whose ceiling is exceeded still surfaces metadata."""
        amap = {
            "foo": KnownViolationsEntry(
                deps=frozenset({"a"}),
                reason="r",
                issue="i",
            )
        }
        c = _classify({"foo": ["a", "b"]}, amap)
        v = c.real_fails[0]
        assert v.listed == frozenset({"a"})
        assert v.reason == "r"
        assert v.issue == "i"

    def test_metadata_absent_for_unlisted_consumer_real_fail(self) -> None:
        c = _classify({"foo": ["a"]}, {})
        v = c.real_fails[0]
        assert v.listed is None
        assert v.reason is None
        assert v.issue is None

    def test_per_consumer_aggregation_across_findings(self) -> None:
        """Multiple findings with the same consumer pool for stale-dep."""
        amap = {"foo": KnownViolationsEntry(deps=frozenset({"a", "b"}))}
        c = classify_violations(
            findings={"k1": ["a"], "k2": ["b"]},
            consumer_of=lambda _: "foo",
            arch="x86_64",
            allowlist=amap,
        )
        assert all(s.kind != "stale-dep" for s in c.stale)
        assert all(s.kind != "stale-consumer" for s in c.stale)
