"""Shared logic for dependency override parsing and application."""

from packaging.specifiers import Specifier
from packaging.utils import canonicalize_name


VALID_ACTIONS = ['drop_upper', 'drop_lower', 'set_upper', 'set_lower',
                 'drop_constraints', 'ignore']

# Operators classified as upper or lower bounds.
# == and ~= impose both bounds and are decomposed by drop_upper/drop_lower
# (see _remove_upper_bounds / _remove_lower_bounds).
# === is removed atomically (no meaningful decomposition).
# != (exclusions) are always preserved.
UPPER_OPS = ['<', '<=', '==', '===', '~=']
LOWER_OPS = ['>', '>=', '==', '===', '~=']


def parse_override_string(override_str):
    """Parse and validate a single dependency override string.

    The br_only suffix must be handled by the caller before calling this.

    Returns (canonical_package_name, action, value_or_None).
    Raises ValueError on invalid input.
    """
    parts = override_str.split(':')

    if len(parts) < 2:
        raise ValueError(
            f'Invalid dependency override format: {override_str!r}. '
            f'Expected format: package:action[:value][:br_only]')

    package = canonicalize_name(parts[0].strip())
    action = parts[1].strip()
    value = parts[2].strip() if len(parts) > 2 else None

    if action not in VALID_ACTIONS:
        raise ValueError(
            f'Invalid dependency override action: {action!r}. '
            f'Valid actions: {VALID_ACTIONS}')

    if action.startswith('set_') and not value:
        raise ValueError(
            f'Action {action!r} requires a value: {override_str!r}')

    if action in ('drop_upper', 'drop_lower', 'drop_constraints',
                  'ignore') and value:
        raise ValueError(
            f'Action {action!r} does not accept a value: {override_str!r}')

    if value:
        try:
            Specifier(f'<{value}')
        except Exception:
            raise ValueError(
                f'Invalid version in dependency override: {value!r} '
                f'from {override_str!r}')

    return (package, action, value)


def _remove_upper_bounds(specifiers):
    """Remove upper-bound specifiers, decomposing == and ~= into their lower half.

    PEP 440 defines ~= V.N as >= V.N, == V.*, so the lower half is >= V.N.
    == V is mathematically >= V AND <= V, so the lower half is >= V.
    === has no meaningful decomposition and is removed entirely.
    """
    result = []
    for s in specifiers:
        if s.operator not in UPPER_OPS:
            result.append(s)
        elif s.operator == '~=':
            result.append(Specifier(f'>={s.version}'))
        elif s.operator == '==' and not s.version.endswith('.*'):
            result.append(Specifier(f'>={s.version}'))
    return result


def _remove_lower_bounds(specifiers):
    """Remove lower-bound specifiers, decomposing == into its upper half.

    == V is mathematically >= V AND <= V, so the upper half is <= V.
    ~= has a complex effective upper bound (prefix match), so it is removed.
    === has no meaningful decomposition and is removed entirely.
    """
    result = []
    for s in specifiers:
        if s.operator not in LOWER_OPS:
            result.append(s)
        elif s.operator == '==' and not s.version.endswith('.*'):
            result.append(Specifier(f'<={s.version}'))
    return result


def apply_overrides_to_specifiers(specifiers, overrides, package_name=None,
                                  log_fn=None):
    """Apply a list of override dicts to a list of Specifier objects.

    Each override is {'action': str, 'value': str or None}.
    Returns a new list of Specifier objects.
    The 'ignore' action is skipped (handled separately by callers).
    If log_fn is provided, it is called with a message string per action.
    """
    new_specifiers = list(specifiers)

    for override in overrides:
        action = override['action']
        value = override['value']

        if action == 'ignore':
            continue
        elif action == 'drop_constraints':
            if log_fn:
                log_fn(f'Applying override: removing all constraints for {package_name}')
            new_specifiers = []
        elif action == 'drop_upper':
            if log_fn:
                log_fn(f'Applying override: removing upper bounds for {package_name}')
            new_specifiers = _remove_upper_bounds(new_specifiers)
        elif action == 'drop_lower':
            if log_fn:
                log_fn(f'Applying override: removing lower bounds for {package_name}')
            new_specifiers = _remove_lower_bounds(new_specifiers)
        elif action == 'set_upper':
            if log_fn:
                log_fn(f'Applying override: setting upper bound for {package_name} to < {value}')
            new_specifiers = _remove_upper_bounds(new_specifiers)
            new_specifiers.append(Specifier(f'<{value}'))
        elif action == 'set_lower':
            if log_fn:
                log_fn(f'Applying override: setting lower bound for {package_name} to >= {value}')
            new_specifiers = _remove_lower_bounds(new_specifiers)
            new_specifiers.append(Specifier(f'>={value}'))

    return new_specifiers


if __name__ == '__main__':
    import sys
    override_str = sys.argv[1].removesuffix(':br_only')
    try:
        parse_override_string(override_str)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
