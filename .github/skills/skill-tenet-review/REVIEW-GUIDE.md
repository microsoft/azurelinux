# Tenet Review Guide

This document contains the full procedure for reviewing changes against Azure Linux tenets. It is designed to be self-contained — an agent reading only this file and the tenet documents has everything it needs to perform a review.

## Tenet Documents

Read ALL tenet files before reviewing - they must all be read in their entirety:

- `./docs/tenets/tenets.*.md`

It is important to read and understand ALL tenets. Even if some seem irrelevant at first glance, they may contain anti-goals that are critical to check against. Do not skip any tenet files.

## Nomenclature

Every tenet document uses the same classification:

- **Goal**: Must be included, supported, and maintained in the distro.
- **Non-goal**: Not required, but may be included if there is demand.
- **Anti-goal**: Explicitly excluded from the distro.

**Anti-goal violations are critical.** Any plan that conflicts with an anti-goal must be rejected or require significant revision.

## Review Procedure

1. **Read ALL tenet files** listed above. Do not skip files or guess at relevance.
2. **Identify applicable tenets.** Match the changes/plan to the relevant topic areas.
3. **Check for anti-goal violations first.** Highest priority — flag immediately.
4. **Assess goal alignment.** Does the change support or undermine stated goals?
5. **Note non-goal implications.** If the change touches non-goal areas, note but don't block.
6. **Provide a structured verdict** using the output format below.

## Output Format

```markdown
## Tenet Review

### Verdict: PASS | WARN | FAIL

### Anti-Goal Violations
- (list any, or "None")

### Goal Alignment
- (list relevant goals and whether the change aligns, with brief explanation)

### Non-Goal Notes
- (list any non-goal areas touched, or "None")

### Recommendations
- (specific suggestions for improvement, if any)
```

- **FAIL**: Anti-goal violation detected. Must resolve before proceeding.
- **WARN**: Partial misalignment or risky implications. Review recommendations.
- **PASS**: Change aligns with all applicable tenets. Proceed.
