"""Unit tests for dependency override functionality."""

import subprocess
import sys

import pytest

from packaging.requirements import Requirement
from packaging.specifiers import Specifier, SpecifierSet

from pyproject_buildrequires import Requirements
from pyproject_dependency_overrides import (
    parse_override_string, apply_overrides_to_specifiers,
)

import pyproject_patch_metadata


# ---- parse_override_string (shared module) ----

class TestParseOverrideString:
    def test_basic(self):
        assert parse_override_string('numpy:drop_upper') == ('numpy', 'drop_upper', None)

    def test_with_value(self):
        assert parse_override_string('numpy:set_upper:2.0') == ('numpy', 'set_upper', '2.0')

    def test_name_normalization(self):
        pkg, action, value = parse_override_string('My_Package:drop_upper')
        assert pkg == 'my-package'

    def test_invalid_format(self):
        with pytest.raises(ValueError, match='Invalid dependency override format'):
            parse_override_string('justpackage')

    def test_invalid_action(self):
        with pytest.raises(ValueError, match='Invalid dependency override action'):
            parse_override_string('pkg:nonexistent')

    def test_set_missing_value(self):
        with pytest.raises(ValueError, match='requires a value'):
            parse_override_string('pkg:set_upper')

    def test_valueless_rejects_value(self):
        with pytest.raises(ValueError, match='does not accept a value'):
            parse_override_string('pkg:drop_upper:2.0')

    def test_invalid_version(self):
        with pytest.raises(ValueError, match='Invalid version'):
            parse_override_string('pkg:set_upper:not_a_version!!!')


# ---- CLI validation (pyproject_dependency_overrides.py __main__) ----

SCRIPT = 'pyproject_dependency_overrides.py'


class TestCLIValidation:
    def _run(self, arg):
        return subprocess.run(
            [sys.executable, '-Bs', SCRIPT, arg],
            capture_output=True, text=True,
        )

    def test_valid_drop_upper(self):
        assert self._run('numpy:drop_upper').returncode == 0

    def test_valid_set_upper(self):
        assert self._run('numpy:set_upper:2.0').returncode == 0

    def test_valid_ignore_br_only(self):
        assert self._run('pkg:ignore:br_only').returncode == 0

    def test_valid_set_lower_br_only(self):
        assert self._run('pkg:set_lower:1.0:br_only').returncode == 0

    def test_invalid_no_colon(self):
        r = self._run('justpackage')
        assert r.returncode == 1
        assert 'Invalid dependency override format' in r.stderr

    def test_invalid_action(self):
        r = self._run('pkg:bogus')
        assert r.returncode == 1
        assert 'Invalid dependency override action' in r.stderr

    def test_set_upper_missing_value(self):
        r = self._run('pkg:set_upper')
        assert r.returncode == 1
        assert 'requires a value' in r.stderr

    def test_drop_upper_rejects_value(self):
        r = self._run('pkg:drop_upper:2.0')
        assert r.returncode == 1
        assert 'does not accept a value' in r.stderr

    def test_invalid_version(self):
        r = self._run('pkg:set_upper:not_a_version!!!')
        assert r.returncode == 1
        assert 'Invalid version' in r.stderr


# ---- apply_overrides_to_specifiers (shared module) ----

class TestApplyOverridesToSpecifiers:
    def _specs(self, spec_str):
        return list(SpecifierSet(spec_str))

    def test_drop_upper(self):
        specs = self._specs('>=1.0,<2.0')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'drop_upper', 'value': None}])
        assert len(result) == 1
        assert result[0].operator == '>='

    def test_drop_lower(self):
        specs = self._specs('>=1.0,<2.0')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'drop_lower', 'value': None}])
        assert len(result) == 1
        assert result[0].operator == '<'

    def test_drop_constraints(self):
        specs = self._specs('>=1.0,<2.0')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'drop_constraints', 'value': None}])
        assert result == []

    def test_set_upper(self):
        specs = self._specs('>=1.0,<2.0')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'set_upper', 'value': '3.0'}])
        assert len(result) == 2
        upper = [s for s in result if s.operator == '<'][0]
        assert upper.version == '3.0'

    def test_set_lower(self):
        specs = self._specs('>=1.0,<2.0')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'set_lower', 'value': '0.5'}])
        assert len(result) == 2
        lower = [s for s in result if s.operator == '>='][0]
        assert lower.version == '0.5'

    def test_ignore_skipped(self):
        specs = self._specs('>=1.0,<2.0')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'ignore', 'value': None}])
        assert len(result) == 2

    def test_drop_upper_decomposes_pin(self):
        """drop_upper on == decomposes to >= (keeps lower half)."""
        specs = self._specs('==25.3.0')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'drop_upper', 'value': None}])
        assert len(result) == 1
        assert result[0].operator == '>='
        assert result[0].version == '25.3.0'

    def test_exclusions_preserved(self):
        """!= exclusions are always preserved."""
        specs = self._specs('>=1.0,!=1.5,<3.0')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'drop_upper', 'value': None}])
        ops = [s.operator for s in result]
        assert '>=' in ops
        assert '!=' in ops
        assert '<' not in ops

    def test_drop_upper_decomposes_tilde(self):
        """drop_upper on ~= decomposes to >= (PEP 440: ~=V.N is >=V.N, ==V.*)."""
        specs = self._specs('~=1.4')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'drop_upper', 'value': None}])
        assert len(result) == 1
        assert result[0].operator == '>='
        assert result[0].version == '1.4'

    def test_drop_lower_decomposes_pin(self):
        """drop_lower on == decomposes to <= (keeps upper half)."""
        specs = self._specs('==25.3.0')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'drop_lower', 'value': None}])
        assert len(result) == 1
        assert result[0].operator == '<='
        assert result[0].version == '25.3.0'

    def test_drop_lower_removes_tilde(self):
        """drop_lower on ~= removes entirely (effective upper bound is complex)."""
        specs = self._specs('~=1.4')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'drop_lower', 'value': None}])
        assert result == []

    def test_drop_upper_removes_wildcard_pin(self):
        """==1.* (prefix match) can't be decomposed, removed entirely."""
        specs = self._specs('==1.*')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'drop_upper', 'value': None}])
        assert result == []

    def test_drop_lower_removes_wildcard_pin(self):
        """==1.* (prefix match) can't be decomposed, removed entirely."""
        specs = self._specs('==1.*')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'drop_lower', 'value': None}])
        assert result == []

    def test_drop_upper_removes_arbitrary_equality(self):
        """=== has no meaningful decomposition, removed atomically."""
        specs = [Specifier('===1.0')]
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'drop_upper', 'value': None}])
        assert result == []

    def test_set_upper_decomposes_pin(self):
        """set_upper on == decomposes to >= (keeps lower half) then adds <VALUE."""
        specs = self._specs('==25.3.0')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'set_upper', 'value': '30.0'}])
        assert len(result) == 2
        ops = {s.operator: s.version for s in result}
        assert ops['>='] == '25.3.0'
        assert ops['<'] == '30.0'

    def test_set_lower_decomposes_pin(self):
        """set_lower on == decomposes to <= (keeps upper half) then adds >=VALUE."""
        specs = self._specs('==25.3.0')
        result = apply_overrides_to_specifiers(
            specs, [{'action': 'set_lower', 'value': '20.0'}])
        assert len(result) == 2
        ops = {s.operator: s.version for s in result}
        assert ops['<='] == '25.3.0'
        assert ops['>='] == '20.0'

    def test_log_fn_called(self):
        messages = []
        specs = self._specs('>=1.0,<2.0')
        apply_overrides_to_specifiers(
            specs, [{'action': 'drop_upper', 'value': None}],
            package_name='numpy', log_fn=messages.append)
        assert len(messages) == 1
        assert 'numpy' in messages[0]


# ---- Requirements._parse_dependency_overrides ----

class TestParseDependencyOverrides:
    def _parse(self, overrides):
        def mock_version(name):
            raise Exception('not installed')
        r = Requirements(mock_version, dependency_overrides=overrides)
        return r.dependency_overrides

    def test_empty(self):
        assert self._parse([]) == {}

    def test_basic_drop_upper(self):
        result = self._parse(['cython:drop_upper'])
        assert 'cython' in result
        assert result['cython'] == [{'action': 'drop_upper', 'value': None}]

    def test_set_upper_with_value(self):
        result = self._parse(['numpy:set_upper:2.0'])
        assert result['numpy'] == [{'action': 'set_upper', 'value': '2.0'}]

    def test_set_lower_with_value(self):
        result = self._parse(['requests:set_lower:2.28'])
        assert result['requests'] == [{'action': 'set_lower', 'value': '2.28'}]

    def test_drop_lower(self):
        result = self._parse(['attrs:drop_lower'])
        assert result['attrs'] == [{'action': 'drop_lower', 'value': None}]

    def test_drop_constraints(self):
        result = self._parse(['flask:drop_constraints'])
        assert result['flask'] == [{'action': 'drop_constraints', 'value': None}]

    def test_ignore(self):
        result = self._parse(['sibling-pkg:ignore'])
        assert result['sibling-pkg'] == [{'action': 'ignore', 'value': None}]

    def test_br_only_suffix_stripped(self):
        result = self._parse(['sibling-pkg:ignore:br_only'])
        assert result['sibling-pkg'] == [{'action': 'ignore', 'value': None}]

    def test_br_only_with_value(self):
        result = self._parse(['numpy:set_upper:2.0:br_only'])
        assert result['numpy'] == [{'action': 'set_upper', 'value': '2.0'}]

    def test_name_normalization(self):
        result = self._parse(['My_Package:drop_upper'])
        assert 'my-package' in result

    def test_multiple_overrides_same_package(self):
        result = self._parse(['pkg:drop_upper', 'pkg:drop_lower'])
        assert len(result['pkg']) == 2

    def test_multiple_packages(self):
        result = self._parse(['pkg-a:drop_upper', 'pkg-b:ignore'])
        assert 'pkg-a' in result
        assert 'pkg-b' in result

    def test_invalid_format(self):
        with pytest.raises(ValueError, match='Invalid dependency override format'):
            self._parse(['justpackage'])

    def test_invalid_action(self):
        with pytest.raises(ValueError, match='Invalid dependency override action'):
            self._parse(['pkg:nonexistent'])

    def test_set_upper_missing_value(self):
        with pytest.raises(ValueError, match='requires a value'):
            self._parse(['pkg:set_upper'])

    def test_set_lower_missing_value(self):
        with pytest.raises(ValueError, match='requires a value'):
            self._parse(['pkg:set_lower'])

    def test_invalid_version(self):
        with pytest.raises(ValueError, match='Invalid version'):
            self._parse(['pkg:set_upper:not_a_version!!!'])

    def test_drop_upper_rejects_value(self):
        with pytest.raises(ValueError, match='does not accept a value'):
            self._parse(['pkg:drop_upper:2.0'])

    def test_ignore_rejects_value(self):
        with pytest.raises(ValueError, match='does not accept a value'):
            self._parse(['pkg:ignore:somevalue'])


# ---- Requirements._should_ignore_dependency ----

class TestShouldIgnoreDependency:
    def _make_req(self, overrides):
        def mock_version(name):
            raise Exception('not installed')
        return Requirements(mock_version, dependency_overrides=overrides)

    def test_not_ignored(self):
        r = self._make_req(['numpy:drop_upper'])
        assert not r._should_ignore_dependency('numpy')

    def test_ignored(self):
        r = self._make_req(['sibling:ignore'])
        assert r._should_ignore_dependency('sibling')

    def test_not_in_overrides(self):
        r = self._make_req(['other:ignore'])
        assert not r._should_ignore_dependency('unrelated')


# ---- Requirements._apply_dependency_overrides ----

class TestApplyDependencyOverrides:
    def _make_req(self, overrides):
        def mock_version(name):
            raise Exception('not installed')
        return Requirements(mock_version, dependency_overrides=overrides)

    def test_no_overrides(self):
        r = self._make_req([])
        result = r._apply_dependency_overrides(Requirement('numpy>=1.0,<2.0'))
        assert len(list(result.specifier)) == 2

    def test_drop_upper(self):
        r = self._make_req(['numpy:drop_upper'])
        result = r._apply_dependency_overrides(Requirement('numpy>=1.0,<2.0'))
        specs = list(result.specifier)
        assert len(specs) == 1
        assert specs[0].operator == '>='

    def test_drop_lower(self):
        r = self._make_req(['numpy:drop_lower'])
        result = r._apply_dependency_overrides(Requirement('numpy>=1.0,<2.0'))
        specs = list(result.specifier)
        assert len(specs) == 1
        assert specs[0].operator == '<'

    def test_drop_constraints(self):
        r = self._make_req(['numpy:drop_constraints'])
        result = r._apply_dependency_overrides(Requirement('numpy>=1.0,<2.0'))
        assert list(result.specifier) == []

    def test_set_upper(self):
        r = self._make_req(['numpy:set_upper:3.0'])
        result = r._apply_dependency_overrides(Requirement('numpy>=1.0,<2.0'))
        specs = list(result.specifier)
        assert len(specs) == 2
        ops = {s.operator for s in specs}
        assert '>=' in ops
        assert '<' in ops
        upper = [s for s in specs if s.operator == '<'][0]
        assert upper.version == '3.0'

    def test_set_lower(self):
        r = self._make_req(['numpy:set_lower:0.5'])
        result = r._apply_dependency_overrides(Requirement('numpy>=1.0,<2.0'))
        specs = list(result.specifier)
        assert len(specs) == 2
        ops = {s.operator for s in specs}
        assert '>=' in ops
        assert '<' in ops
        lower = [s for s in specs if s.operator == '>='][0]
        assert lower.version == '0.5'

    def test_drop_upper_decomposes_pin(self):
        """drop_upper on == decomposes to >= (keeps lower half)."""
        r = self._make_req(['attrs:drop_upper'])
        result = r._apply_dependency_overrides(Requirement('attrs==25.3.0'))
        specs = list(result.specifier)
        assert len(specs) == 1
        assert specs[0].operator == '>='
        assert specs[0].version == '25.3.0'

    def test_drop_lower_decomposes_pin(self):
        """drop_lower on == decomposes to <= (keeps upper half)."""
        r = self._make_req(['attrs:drop_lower'])
        result = r._apply_dependency_overrides(Requirement('attrs==25.3.0'))
        specs = list(result.specifier)
        assert len(specs) == 1
        assert specs[0].operator == '<='
        assert specs[0].version == '25.3.0'

    def test_drop_upper_preserves_exclusions(self):
        """!= exclusions are always preserved."""
        r = self._make_req(['pkg:drop_upper'])
        result = r._apply_dependency_overrides(Requirement('pkg>=1.0,!=1.5,<3.0'))
        ops = [s.operator for s in result.specifier]
        assert '>=' in ops
        assert '!=' in ops
        assert '<' not in ops

    def test_ignore_action_passthrough(self):
        """ignore action is handled separately; _apply_dependency_overrides skips it."""
        r = self._make_req(['pkg:ignore'])
        result = r._apply_dependency_overrides(Requirement('pkg>=1.0,<2.0'))
        assert len(list(result.specifier)) == 2

    def test_unrelated_package_not_affected(self):
        r = self._make_req(['other:drop_upper'])
        result = r._apply_dependency_overrides(Requirement('numpy>=1.0,<2.0'))
        assert len(list(result.specifier)) == 2

    def test_extras_stripped_for_lookup(self):
        r = self._make_req(['numpy:drop_upper'])
        result = r._apply_dependency_overrides(Requirement('numpy[extra1]>=1.0,<2.0'))
        specs = list(result.specifier)
        assert len(specs) == 1
        assert specs[0].operator == '>='

    def test_drop_upper_decomposes_tilde(self):
        """drop_upper on ~= decomposes to >= (PEP 440: ~=V.N is >=V.N, ==V.*)."""
        r = self._make_req(['pkg:drop_upper'])
        result = r._apply_dependency_overrides(Requirement('pkg~=1.4'))
        specs = list(result.specifier)
        assert len(specs) == 1
        assert specs[0].operator == '>='
        assert specs[0].version == '1.4'


# ---- pyproject_patch_metadata ----

class TestPatchMetadataParseOverrides:
    def test_br_only_skipped(self):
        result = pyproject_patch_metadata.parse_overrides(['pkg:ignore:br_only'])
        assert result == {}

    def test_non_br_only_included(self):
        result = pyproject_patch_metadata.parse_overrides(['pkg:ignore'])
        assert 'pkg' in result

    def test_mixed(self):
        result = pyproject_patch_metadata.parse_overrides([
            'pkg-a:ignore:br_only',
            'pkg-b:drop_upper',
        ])
        assert 'pkg-a' not in result
        assert 'pkg-b' in result

    def test_rejects_value_for_valueless_action(self):
        with pytest.raises(ValueError, match='does not accept a value'):
            pyproject_patch_metadata.parse_overrides(['pkg:drop_upper:2.0'])

    def test_rejects_invalid_version(self):
        with pytest.raises(ValueError, match='Invalid version'):
            pyproject_patch_metadata.parse_overrides(['pkg:set_upper:!!!'])


class TestApplyOverridesToRequirement:
    def test_ignore_returns_none(self):
        req = Requirement('numpy>=1.0')
        result = pyproject_patch_metadata.apply_overrides_to_requirement(
            req, [{'action': 'ignore', 'value': None}])
        assert result is None

    def test_drop_upper(self):
        req = Requirement('numpy>=1.0,<2.0')
        result = pyproject_patch_metadata.apply_overrides_to_requirement(
            req, [{'action': 'drop_upper', 'value': None}])
        assert result is not None
        specs = list(result.specifier)
        assert len(specs) == 1
        assert specs[0].operator == '>='

    def test_set_upper(self):
        req = Requirement('numpy>=1.0,<2.0')
        result = pyproject_patch_metadata.apply_overrides_to_requirement(
            req, [{'action': 'set_upper', 'value': '3.0'}])
        specs = list(result.specifier)
        ops = {s.operator for s in specs}
        assert '<' in ops
        upper = [s for s in specs if s.operator == '<'][0]
        assert upper.version == '3.0'

    def test_drop_constraints(self):
        req = Requirement('numpy>=1.0,<2.0')
        result = pyproject_patch_metadata.apply_overrides_to_requirement(
            req, [{'action': 'drop_constraints', 'value': None}])
        assert result is not None
        assert list(result.specifier) == []

    def test_preserves_extras_and_markers(self):
        req = Requirement('numpy[extra1]>=1.0,<2.0; python_version>="3"')
        result = pyproject_patch_metadata.apply_overrides_to_requirement(
            req, [{'action': 'drop_upper', 'value': None}])
        assert result is not None
        assert result.extras == {'extra1'}
        assert result.marker is not None


class TestPatchMetadataFile:
    def _write_metadata(self, tmp_path, content):
        p = tmp_path / 'METADATA'
        p.write_text(content)
        return str(p)

    def test_drop_upper(self, tmp_path):
        metadata = self._write_metadata(tmp_path,
            'Metadata-Version: 2.1\n'
            'Name: mypackage\n'
            'Requires-Dist: numpy (>=1.0,<2.0)\n'
            'Requires-Dist: requests\n'
        )
        overrides = pyproject_patch_metadata.parse_overrides(['numpy:drop_upper'])
        pyproject_patch_metadata.patch_metadata(metadata, overrides)
        with open(metadata) as f:
            content = f.read()
        assert 'numpy' in content
        assert '<2.0' not in content
        assert 'requests' in content

    def test_ignore(self, tmp_path):
        metadata = self._write_metadata(tmp_path,
            'Metadata-Version: 2.1\n'
            'Name: mypackage\n'
            'Requires-Dist: sibling-pkg\n'
            'Requires-Dist: requests\n'
        )
        overrides = pyproject_patch_metadata.parse_overrides(['sibling-pkg:ignore'])
        pyproject_patch_metadata.patch_metadata(metadata, overrides)
        with open(metadata) as f:
            content = f.read()
        assert 'sibling-pkg' not in content
        assert 'requests' in content

    def test_no_overrides(self, tmp_path):
        original = (
            'Metadata-Version: 2.1\n'
            'Name: mypackage\n'
            'Requires-Dist: numpy (>=1.0,<2.0)\n'
        )
        metadata = self._write_metadata(tmp_path, original)
        pyproject_patch_metadata.patch_metadata(metadata, {})
        with open(metadata) as f:
            content = f.read()
        assert content == original

    def test_br_only_not_applied_to_metadata(self, tmp_path):
        original = (
            'Metadata-Version: 2.1\n'
            'Name: mypackage\n'
            'Requires-Dist: sibling-pkg\n'
        )
        metadata = self._write_metadata(tmp_path, original)
        overrides = pyproject_patch_metadata.parse_overrides(['sibling-pkg:ignore:br_only'])
        pyproject_patch_metadata.patch_metadata(metadata, overrides)
        with open(metadata) as f:
            content = f.read()
        assert 'sibling-pkg' in content
