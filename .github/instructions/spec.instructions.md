---
applyTo: 'SPECS*/**/*.spec'
description: Always apply these instructions when editing `*.spec` files. They live under
the `SPECS*` directories and their subdirectories. The exact directory structure may vary,
but all spec files must follow the conventions outlined in this document.
---

## Instructions context

- We're using `some-package` as a placeholder for the actual package name.
- The spec file is placed in the `SPECS` or `SPECS-<SUBTYPE>` directory, e.g.:
  - `SPECS/some-package/some-package.spec`
  - `SPECS-NVIDIA/some-package/some-package.spec`
  - `SPECS-AMD/some-package/some-package.spec`

## General RPM spec instructions

- The spec file name and the directory name should be the same, if only one version of the package needs to be maintained.
- Keep one spec subdirectory per package.
  
  GOOD:
  - `SPECS/some-package/some-package.spec`
  - `SPECS/some-package-similar/some-package-similar.spec`
  
  BAD:
  - `SPECS/some-package/some-package.spec`
  - `SPECS/some-package/some-package-similar.spec`
- All packages must have a license file included through the `%license` macro in the `%files` section. Exceptions:
  - Subpackages that depend on another subpackage from the same spec, where that other subpackage already includes the license file. The expected end result of installing any package is that a license file for that package ends up being installed along with it.
  - "Metapackages", which don't build and install any of its own files but are a collection of run-time `Requires` dependencies.
- If multiple versions need to be maintained, use versioned spec files names within the same directory. If you're adding a new version to an existing directory with a single spec file, keep the original spec file unchanged. Example:
  - `SPECS/some-package/some-package.spec`
  - `SPECS/some-package/some-package-v2.spec`
- The `Name` tag in the spec file should match the spec file name except for the version suffix (if present). Example:
  - For `some-package.spec`, use `Name: some-package`
  - For `some-package-v2.spec`, use `Name: some-package`
- Packages, which need their internal files (kernel or EFI modules for instance) signed, must have a separate signed spec file variant in its own `SPECS*-SIGNED` directory. The signed subdirectory and spec file should have the `-signed` suffix. Example:
  - For `SPECS-NVIDIA/some-package/some-package.spec` -> `SPECS-NVIDIA-SIGNED/some-package-signed/some-package-signed.spec`
- The signed spec file must define only subpackages, which contain the signed files. The name of these subpackages must be identical to their unsigned counterparts. Example:
  - For `some-package-kmod` subpackage in the unsigned spec, define `some-package-kmod` subpackage in the signed spec as well.
  **NOTE**: since the signed spec only defines subpackages, either make `Name:` tag in the signed spec file match the subpackage name or define `%package -n <subpackage-name>` and `%files -n <subpackage-name>` explicitly in the signed spec file.
- The signed specs DO NOT use the original sources. Instead, they use the RPM package built from the unsigned spec as the source of unsigned files and separately a `SourceX` entry for each of the signed files. No other source files are allowed. The files inside the original RPM should be extracted to the same installation paths as in the original RPM and then the signed files should replace the unsigned ones.
- The signed subpackage must have the same pre- and post-install scripts as the unsigned subpackage (if any) to ensure proper installation and removal.

## Instructions specific to spec files building out-of-tree kernel modules

**IN ADDITION TO THESE INSTRUCTIONS**, follow instructions under `.github/instructions/oot-modules.instructions.md`.
