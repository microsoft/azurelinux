---
applyTo: 'SPECS*/**/*.spec'
---

## Instructions context

- We're using `some-package` as a placeholder for the actual package name.
- The spec file is placed in the `SPECS` or `SPECS-<SUBTYPE>` directory, e.g.:
  - `SPECS/some-package/some-package.spec`
  - `SPECS-EXTENDED/some-package/some-package.spec`
- The spec file `some-package.spec` builds OOT modules and places them in one of its subpackages.

## General RPM spec instructions

- The spec file name and the directory name should be the same, if only one version of the package needs to be maintained.
- Keep one spec subdirectory per package.
  
  GOOD:
  - `SPECS/some-package/some-package.spec`
  - `SPECS/some-package-similar/some-package-similar.spec`
  
  BAD:
  - `SPECS/some-package/some-package.spec`
  - `SPECS/some-package/some-package-similar.spec`
- All packages must have a license file included through the `%license` macro in the `%files` section. This can be omitted only for subpackages that depend on another subpackage from the same spec, where that other subpackage already includes the license file. The expected end result of installing any package is that a license file for that package ends up being installed along with it.
- If multiple versions need to be maintained, use versioned spec files names within the same directory. If you're adding a new version to an existing directory with a single spec file, keep the original spec file unchanged. Example:
  - `SPECS/some-package/some-package.spec`
  - `SPECS/some-package/some-package-v2.spec`
- The `Name` tag in the spec file should match the spec file name except for the version suffix (if present). Example:
  - For `some-package.spec`, use `Name: some-package`
  - For `some-package-v2.spec`, use `Name: some-package`
- Packages, which need their internal files (kernel or EFI modules for instance) signed, must have a separate signed spec file variant in its own `SPECS*-SIGNED` directory. The signed subdirectory and spec file should have the `-signed` suffix. Example:
  - For `SPECS/some-package/some-package.spec` -> `SPECS-SIGNED/some-package-signed/some-package-signed.spec`
- The signed spec file must define only subpackages, which contain the signed files. The name of these subpackages must be identical to their unsigned counterparts. Example:
  - For `some-package-kmod` subpackage in the unsigned spec, define `some-package-kmod` subpackage in the signed spec as well.
  **NOTE**: since the signed spec only defines subpackages, either make `Name:` tag in the signed spec file match the subpackage name or define `%package -n <subpackage-name>` and `%files -n <subpackage-name>` explicitly in the signed spec file.
- The signed specs DO NOT use the original sources. Instead, they use the RPM package built from the unsigned spec as the source of unsigned files and separately a `SourceX` entry for each of the signed files. No other source files are allowed. The files inside the original RPM should be extracted to the same installation paths as in the original RPM and then the signed files should replace the unsigned ones.
- The signed subpackage must have the same pre- and post-install scripts as the unsigned subpackage (if any) to ensure proper installation and removal.

## Out-of-Tree kernel module RPM spec instructions

- Keep the OOT module and other components dependent on internal kernel APIs in a separate subpackage within the spec file, than the components using only the user space APIs and libraries. This allows to prevent building duplicate user space components for cases when we need to support OOTs for multiple kernel versions and flavours. Example:
  - `some-package` main package for user space components (tools, libraries, services, etc.)
  - `some-package-kmod` subpackage for the kernel module built against the default `kernel-devel` package
  - `some-package-flavour1-kmod` subpackage for the kernel module built against `kernel-flavour1-devel` package
- All subpackages with OOT modules must run-time depend on the exact kernel version and flavour they were built for. This must be mentioned explicitly through the `Requires` tag:
  - For OOT modules built against the default `kernel-devel` you can get this value through this set of macros:
    ```rpm-spec
    %global target_kernel_version_full %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers))
    %global target_azl_build_kernel_version %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}' $(/bin/rpm -q --whatprovides kernel-headers))
    %global target_kernel_release %(/bin/rpm -q --queryformat '%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers) | /bin/cut -d . -f 1)
    ```
  - For OOT modules built against a specific kernel flavour `kernel-flavour1-devel` this value must be hard-coded into the spec file as we cannot detect it dynamically:
    ```rpm-spec
    %global target_azl_build_kernel_version 6.12.57.1
    %global target_kernel_release 1
    %global target_kernel_version_full %{target_azl_build_kernel_version}-%{target_kernel_release}%{?dist}
    ```
    
  With that you can then define:
    - `Requires: kernel = %{target_kernel_version_full}`
    - `Requires: kernel-flavour1 = %{target_kernel_version_full}`
- To auto-bump and build OOT module packages for new kernel versions, use the following macro and use it in the `Release` tag:
  ```rpm-spec
  %global release_suffix _%{target_azl_build_kernel_version}.%{target_kernel_release}
  (...)
  Release:        1%{release_suffix}%{?dist}
  ```

### Reference example

- `SPECS/isert/isert.spec` -> `SPECS-SIGNED/isert-signed/isert-signed.spec`
- `SPECS/isert-hwe/isert-hwe.spec` -> `SPECS-SIGNED/isert-hwe-signed/isert-hwe-signed.spec`
