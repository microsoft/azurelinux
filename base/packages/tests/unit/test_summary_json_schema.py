# SPDX-License-Identifier: MIT
"""Round-trip the ``--summary-json`` writer against its companion schema.

Drives the writer end-to-end (configure pytest with ``--summary-json``,
emit a record via the same code path the real fixture uses, run the
``pytest_sessionfinish`` hook, then validate the on-disk file against
``cases/summary-json.schema.json``). Keeps the two artefacts honest:
any future change to the writer's payload shape that the schema
doesn't allow will fail this test.
"""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from utils.known_violations import (
    ClassifiedViolations,
    KnownViolationsEntry,
    StaleEntry,
    Verdict,
    classify_violations,
)
from utils import pytest_plugin

_SCHEMA_PATH = (
    Path(__file__).resolve().parent.parent
    / "cases"
    / "summary-json.schema.json"
)


def _load_schema() -> dict:
    return json.loads(_SCHEMA_PATH.read_text())


@pytest.fixture
def summary_path(tmp_path: Path) -> Path:
    return tmp_path / "summary.json"


def _run_writer_with_records(
    summary_path: Path, records: list[dict], *, exit_status: int = 0
) -> dict:
    """Drive the writer hook directly with a synthetic config + records."""

    class _StubConfig:
        def __init__(self) -> None:
            self._azl_summary_json_path = summary_path
            self._azl_summary_records = records

    class _StubSession:
        def __init__(self) -> None:
            self.config = _StubConfig()

    pytest_plugin.pytest_sessionfinish(_StubSession(), exit_status)  # type: ignore[arg-type]

    assert summary_path.exists(), f"writer did not produce {summary_path}"
    return json.loads(summary_path.read_text())


class TestSummaryJsonSchema:
    def test_empty_run_produces_well_formed_file(
        self, summary_path: Path
    ) -> None:
        payload = _run_writer_with_records(summary_path, [])
        jsonschema.validate(payload, _load_schema())
        assert payload["records"] == []
        assert payload["exit_status"] == 0

    def test_each_pytest_exit_code_is_valid(
        self, summary_path: Path
    ) -> None:
        for code in (0, 1, 2, 3, 4, 5):
            payload = _run_writer_with_records(
                summary_path, [], exit_status=code
            )
            jsonschema.validate(payload, _load_schema())
            assert payload["exit_status"] == code

    def test_full_record_with_every_bucket_validates(
        self, summary_path: Path
    ) -> None:
        # Build verdicts directly so we exercise both the unlisted
        # (listed=None) branch and the listed branch (with metadata).
        verdicts_real_fail = [
            Verdict(
                key="cinnamon-1.0-1.x86_64",
                consumer="cinnamon",
                observed=frozenset({"a", "b"}),
                listed=frozenset({"a"}),
                classification="real-fail",
                reason="ceiling exceeded",
                issue="AB#1",
            ),
            Verdict(
                key="newpkg-1.0-1.x86_64",
                consumer="newpkg",
                observed=frozenset({"missing-dep"}),
                listed=None,
                classification="real-fail",
            ),
        ]
        verdicts_xfail = [
            Verdict(
                key="gnome-1.0-1.x86_64",
                consumer="gnome",
                observed=frozenset({"libgcr-3"}),
                listed=frozenset({"libgcr-3"}),
                classification="xfail",
                reason="gcr3 deprecated",
                issue="AB#2",
            ),
        ]
        stale = [
            StaleEntry(consumer="ghost", kind="stale-consumer"),
            StaleEntry(
                consumer="halfghost", kind="stale-dep", listed_dep="dep-x"
            ),
        ]

        # Mirror conftest._verdict_dict's omit-when-absent metadata
        # contract directly so we don't have to import the conftest
        # helper into a unit test.
        def _verdict_dict(v: Verdict) -> dict:
            d = {
                "key": str(v.key),
                "consumer": v.consumer,
                "observed": sorted(v.observed),
                "listed": sorted(v.listed) if v.listed is not None else None,
            }
            if v.reason is not None:
                d["reason"] = v.reason
            if v.issue is not None:
                d["issue"] = v.issue
            return d

        record = {
            "test_nodeid": "cases/test_repoclosure_base_plus_sdk_full.py::test_repoclosure_base_plus_sdk_full[x86_64]",
            "arch": "x86_64",
            "source_label": "runtime-missing",
            "real_fails": [_verdict_dict(v) for v in verdicts_real_fail],
            "known_violations": [_verdict_dict(v) for v in verdicts_xfail],
            "stale": [
                {"consumer": s.consumer, "kind": s.kind, "listed_dep": s.listed_dep}
                for s in stale
            ],
        }

        payload = _run_writer_with_records(summary_path, [record])
        jsonschema.validate(payload, _load_schema())

        emitted = payload["records"][0]
        # ST2 metadata round-trips through the writer.
        assert emitted["real_fails"][0]["reason"] == "ceiling exceeded"
        assert emitted["real_fails"][0]["issue"] == "AB#1"
        assert emitted["known_violations"][0]["reason"] == "gcr3 deprecated"
        # Unlisted-consumer real-fail has no metadata fields.
        assert "reason" not in emitted["real_fails"][1]
        assert "issue" not in emitted["real_fails"][1]
        # listed=None survives the round trip.
        assert emitted["real_fails"][1]["listed"] is None

    def test_classifier_output_serialises_against_schema(
        self, summary_path: Path
    ) -> None:
        """End-to-end: classifier -> conftest-style dict -> writer -> schema."""
        amap = {
            "foo": KnownViolationsEntry(
                deps=frozenset({"a"}),
                reason="r",
                issue="i",
            )
        }
        c: ClassifiedViolations = classify_violations(
            findings={"foo": ["a"]},
            consumer_of=lambda k: k,
            arch="x86_64",
            allowlist=amap,
        )

        def _verdict_dict(v: Verdict) -> dict:
            d = {
                "key": str(v.key),
                "consumer": v.consumer,
                "observed": sorted(v.observed),
                "listed": sorted(v.listed) if v.listed is not None else None,
            }
            if v.reason is not None:
                d["reason"] = v.reason
            if v.issue is not None:
                d["issue"] = v.issue
            return d

        record = {
            "test_nodeid": "unit/test_summary_json_schema.py::synthetic",
            "arch": "x86_64",
            "source_label": "runtime-missing",
            "real_fails": [_verdict_dict(v) for v in c.real_fails],
            "known_violations": [_verdict_dict(v) for v in c.known_violations],
            "stale": [
                {"consumer": s.consumer, "kind": s.kind, "listed_dep": s.listed_dep}
                for s in c.stale
            ],
        }
        payload = _run_writer_with_records(summary_path, [record])
        jsonschema.validate(payload, _load_schema())


class TestSchemaRejects:
    """Sanity checks that the schema actually catches drifts."""

    def test_rejects_wrong_schema_version(self) -> None:
        payload = {"schema_version": 2, "exit_status": 0, "records": []}
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(payload, _load_schema())

    def test_rejects_unknown_top_level_field(self) -> None:
        payload = {
            "schema_version": 1,
            "exit_status": 0,
            "records": [],
            "extra": "not allowed",
        }
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(payload, _load_schema())

    def test_rejects_unknown_verdict_field(self) -> None:
        payload = {
            "schema_version": 1,
            "exit_status": 0,
            "records": [
                {
                    "test_nodeid": "x",
                    "arch": "x86_64",
                    "source_label": "y",
                    "real_fails": [
                        {
                            "key": "k",
                            "consumer": "c",
                            "observed": ["a"],
                            "listed": ["a"],
                            "owner": "alice",
                        }
                    ],
                    "known_violations": [],
                    "stale": [],
                }
            ],
        }
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(payload, _load_schema())

    def test_rejects_unknown_stale_kind(self) -> None:
        payload = {
            "schema_version": 1,
            "exit_status": 0,
            "records": [
                {
                    "test_nodeid": "x",
                    "arch": "x86_64",
                    "source_label": "y",
                    "real_fails": [],
                    "known_violations": [],
                    "stale": [
                        {"consumer": "c", "kind": "made-up", "listed_dep": None}
                    ],
                }
            ],
        }
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(payload, _load_schema())
