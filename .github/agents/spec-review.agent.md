---
name: spec-review
description: 'Reviews RPM spec and component changes for defects and non-idiomatic packaging.'
argument-hint: 'Specs, components or a diff to review.'
agents: ["*"]
user-invocable: true
disable-model-invocation: false
---

# Spec review

Read and follow the [spec-review skill](../../.agents/skills/spec-review/SKILL.md); it owns the scope,
severity rules and output, and uses the rpm-packaging-idioms skill for the packaging rules.

If you delegate, give each reviewer the skill paths, the target and the scope.
