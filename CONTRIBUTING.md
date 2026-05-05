# Contribution Guide

Thanks for your interest in contributing to Azure Linux! This document describes how to
get your changes reviewed and merged. For project setup and the `azldev` workflow, see
[`README.md`](README.md).

> **Note:** This repo also contains [`AGENTS.md`](AGENTS.md) and
> [`.github/copilot-instructions.md`](.github/copilot-instructions.md). Those files
> are instructions for AI coding agents (GitHub Copilot, etc.) — they contain useful
> reference material about the repo layout and tooling.

## Contributor License Agreement

This project welcomes contributions and suggestions. Most contributions require you to
agree to a Contributor License Agreement (CLA) declaring that you have the right to,
and actually do, grant us the rights to use your contribution. For details, visit
<https://cla.microsoft.com>.

When you submit a pull request, a CLA-bot will automatically determine whether you need
to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the
instructions provided by the bot. You will only need to do this once across all repositories using our CLA.

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Security

Please see [SECURITY.md](SECURITY.md) for how to report security vulnerabilities. Do
**not** open public issues or PRs for security problems.

## Pull Request Workflow

We use a **patch-series workflow with rebase-merge**. When a PR is merged, its commits
are replayed onto the target branch — individual commits are preserved, there is no
squash and no merge commit. This makes each commit part of the permanent history, so
each commit must stand on its own.

### Before starting work

For non-trivial changes — new components, large refactors, design shifts — please open
an issue or start a discussion first so we can agree on direction before you invest
significant time. This avoids surprises and duplicate effort. Trivial fixes (typos,
small bug fixes) can go straight to a PR.

### What we expect from a PR

- **Focused patch series.** Keep PRs small and focused on a single concern. Aim for a
  small number of commits — ideally one, and only as many as are needed to make the
  change reviewable. Split unrelated work into separate PRs.
- **Self-contained, reviewable commits.** Every commit should represent one logical
  change with a clear message. A reviewer should be able to read each commit on its own
  and understand what it does and why.
- **Buildable / bisectable history.** Each commit should leave the tree in a working
  state so `git bisect` remains useful. Don't introduce a regression in one commit and
  fix it in the next.
- **No WIP / fixup / "address review feedback" commits in the final history.** Fold
  those into the commits they belong to before the PR is approved (see
  [Responding to review feedback](#responding-to-review-feedback) below).

### Conventional Commits

Commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/)
specification:

```
<type>(<optional scope>): <short summary>

<optional body explaining the what and why>

<optional footers>
```

Use the standard types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`,
`build`, `ci`, `chore`, `revert`. Scope is free-form — use whatever helps reviewers
locate the change (e.g., a component name, subsystem, or directory). Keep the summary
line short, in the imperative mood, and lowercase after the type.

Examples:

```
feat(cowsay): add new component imported from Fedora
fix(kernel): correct kmod-macros include path
docs: clarify overlay description requirement
ci: pin azldev runner image to a tagged release
```

Use the body to explain *why* a change is needed when the reason isn't obvious from the
diff. Reference issues or upstream bugs in footers when applicable.

### Writing commit messages

Because we rebase-merge, every commit message becomes part of the permanent linear
history of the development branch. A reviewer (and `git log` / `git blame` years from
now) should be able to understand a change from its message alone, without opening the
PR. Concretely:

- **Always include a body** for any non-trivial change. The summary line tells you
  *what* changed; the body should tell you *why*, what alternatives were considered,
  and any context a future reader will need (linked issues, upstream bugs, behavioral
  implications, follow-up work). One-liners are only appropriate for changes that are
  self-evident from the diff (e.g., a typo fix).
- **Wrap the summary at ~50 characters** and the body at ~72. Hard limits aren't
  enforced, but staying close keeps `git log` readable in a standard terminal.
- **Separate the summary from the body with a blank line.** Without it, `git` and most
  tooling treat the entire message as the summary.
- **Write in the imperative mood** ("add cowsay component", not "added" or "adds"), as
  if completing the sentence "If applied, this commit will…".
- **Don't rely on auto-generated trailers alone.** Trailers like agent-log or
  co-authored-by links are fine *in addition to* a real message, but a commit whose
  body contains only trailers is not acceptable on the development branch.

### Validating your commits

Before pushing, validate each commit, not just the tip of the branch. CI enforces that
rendered specs match the committed state, so re-render any components you touched.
For changes that affect RPM output, build and smoke-test the result. Pure documentation
or metadata changes don't require a rebuild. See the [`README.md`](README.md) for
`azldev` commands.

### Responding to review feedback

You can address review comments however you like *during* review — additional commits
on top of your branch are fine if you find that easier than amending. Before a
maintainer approves and merges, however, the branch must be rebased and cleaned up so
the commit history reflects the final logical change set. In practice that means:

- Use `git rebase -i` to fold fixup / "address review feedback" commits into the
  commits they belong to.
- Use `git commit --amend` for small follow-up tweaks to the most recent commit.
- Force-push the cleaned-up branch (`git push --force-with-lease`) to update the PR.
- Make sure each remaining commit still has a proper Conventional Commits message and
  leaves the tree buildable.

If you'd rather keep history clean as you go, rebasing and force-pushing throughout
review is also welcome.

### Keeping up to date with the target branch

Rebase your branch onto the latest target branch rather than merging it back in — merge
commits aren't allowed in the final history. Resolve conflicts during rebase and
force-push the result.
