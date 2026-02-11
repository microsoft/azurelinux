# Azure Linux — Agent Guide

For project context and architecture, see [`.github/copilot-instructions.md`](.github/copilot-instructions.md).

## Mandatory Testing

> **USE YOUR BEST JUDGEMENT**, but when in doubt, test. If your change could affect the built RPMs, smoke-test before reporting success. See [`azl-mock`](.github/skills/azl-mock/SKILL.md).

### Examples of changes that should trigger a final test prior to sign-off (not an exhaustive list)

- Version bumps or pinning a new upstream version
- Adding, modifying, or removing overlays (trivial edits may only require `prep-sources` verification, but when in doubt, do a full build + smoke-test)
- Changing build config (`build.defines`, `build.with`, `build.without`)
- Modifying local spec files or source files (again, trivial edits may not require a full rebuild, but when in doubt, test)
- Adding a new component (first build)

### Examples of changes that may not require testing (no effect on RPM output)

- Moving a component definition between files (inline `components.toml` → dedicated `<name>.comp.toml` or vice versa)
- Editing only component metadata fields (e.g., overlay descriptions, build descriptions, comments) without changing actual build config or overlays
- Adding or editing TOML comments
- Pure documentation or formatting changes

### Minimum required testing

1. **Build** — `azldev comp build -p <name>` succeeds, RPMs appear in `base/out/`.
2. **Inspect** — Use `mock --copyin` to copy the RPM into the chroot and inspect with `rpm -qlp` without installing. See [`azl-mock`](.github/skills/azl-mock/SKILL.md).
3. **Smoke-test** — Use a mock chroot (`azldev adv mock shell --add-package /path/to/rpm`) to install and validate basic functionality (e.g., `<binary> --version`, service starts, library loads). See [`azl-mock`](.github/skills/azl-mock/SKILL.md).

Do NOT skip testing for changes that affect RPM output. Do NOT tell the user "the build succeeded" without also running the smoke-test. If testing cannot be performed (e.g., the package has no runnable binary, or some other issue), explicitly document why and what was verified instead.

## Conventions

- Always run `azldev comp list -p <name> -q -O json` before modifying a component.
- Prefer overlays over forking/local specs when customizing upstream packages.
- Use `azldev comp prep-sources -p <name> -o <dir> -q` to verify overlays apply cleanly before building.
- Follow the inner loop cycle: investigate → modify → verify → build → test → inspect. See [`azl-build-component`](.github/skills/azl-build-component/SKILL.md).
  - Note: Use your best judgement, some packages are VERY slow to build (e.g., `kernel`), in those cases you may want to do multiple iterations of investigate → modify → verify with `prep-sources` before doing a full build + test.
- `prep-sources -o <dir>` output is ad-hoc (user-chosen dir). `comp build` output goes to project-configured dirs (`base/out/`, `base/build/`). Don't conflate them.
- For temporary files, ensure they are all placed inside the project's defined work directory (`azldev config dump -q -f json 2>&1 | grep 'workDir'`). Example commands use `my/build/dir`, when starting work on a component **check the actual path** once, and ensure all temp directories are inside it unless there's a specific reason not to be (e.g., truly global temp dir for some reason).

Example: `workDir="/home/user/azurelinux/base/build/work"`, use "./base/build/work/scratch/" for all temp dirs, or a subdir like "./base/build/work/scratch/thing".

## Skills

Detailed workflows live in skills (loaded on-demand when relevant):

| Task | Skill |
| ---- | ----- |
| Build a component, debug build failures | [`azl-build-component`](.github/skills/azl-build-component/SKILL.md) |
| Add a new component to the distro | [`azl-add-component`](.github/skills/azl-add-component/SKILL.md) |
| Diagnose and fix overlay issues | [`azl-fix-overlay`](.github/skills/azl-fix-overlay/SKILL.md) |
| Test and inspect packages in mock chroot | [`azl-mock`](.github/skills/azl-mock/SKILL.md) |
| Review component for hygiene and best practices | [`azl-review-component`](.github/skills/azl-review-component/SKILL.md) |

## Directory Guidance

- **Components:** [`base/comps/AGENTS.md`](base/comps/AGENTS.md) — file organization rules
- **Distro config:** [`distro/AGENTS.md`](distro/AGENTS.md) — build defaults, shared config
