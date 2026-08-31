## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 5;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond check 1

# Fedora and EPEL have patchelf; RHEL/ELN don’t want it.
%bcond patchelf %[ %{undefined rhel} || %{defined epel} ]

Name:           maturin
Version:        1.14.1
Release:        %autorelease
Summary:        Build and publish Rust crates as Python packages
SourceLicense:  MIT OR Apache-2.0

# (Apache-2.0 OR MIT) AND BSD-3-Clause
# (MIT OR Apache-2.0) AND Apache-2.0 AND CC0-1.0
# (MIT OR Apache-2.0) AND Unicode-3.0
# (MIT OR Apache-2.0) AND Unicode-DFS-2016
# 0BSD
# 0BSD OR MIT OR Apache-2.0
# Apache-2.0
# Apache-2.0 AND MIT
# Apache-2.0 OR BSD-2-Clause
# Apache-2.0 OR MIT
# Apache-2.0 WITH LLVM-exception
# Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
# BSD-2-Clause OR Apache-2.0 OR MIT
# MIT
# MIT OR Apache-2.0
# MIT OR Zlib OR Apache-2.0
# MIT-0
# MIT-0 OR Apache-2.0
# MPL-2.0
# Unicode-3.0
# Unlicense OR MIT
# Zlib
# bzip2-1.0.6
License:        %{shrink:
    0BSD AND
    Apache-2.0 AND
    Apache-2.0 WITH LLVM-exception AND
    BSD-3-Clause AND
    CC0-1.0 AND
    MIT AND
    MIT-0 AND
    MPL-2.0 AND
    Unicode-3.0 AND
    Unicode-DFS-2016 AND
    Zlib AND
    bzip2-1.0.6 AND
    (0BSD OR MIT OR Apache-2.0) AND
    (Apache-2.0 OR BSD-2-Clause) AND
    (Apache-2.0 OR BSL-1.0) AND
    (Apache-2.0 OR MIT) AND
    (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND
    (BSD-2-Clause OR Apache-2.0 OR MIT) AND
    (MIT OR Zlib OR Apache-2.0) AND
    (MIT-0 OR Apache-2.0) AND
    (Unlicense OR MIT)
}
# LICENSE.dependencies contains a full license breakdown

URL:            https://github.com/PyO3/maturin
Source:         %{url}/archive/v%{version}/maturin-%{version}.tar.gz

# * Remove unwanted feature groups and optional dependencies, and/or those with
#   missing dependencies:
#
#   - “cross compile”: optional dependencies cargo-zigbuild, cargo-xwin, xz2.
#     Neither cargo-zigbuild nor cargo-xwin is packaged.
#   - “cross compile using zig or xwin”: features cross-compile, zig, xwin.
#     These would depend on “cross compile” optional dependencies. Note that
#     “cross-compile” is removed from the “full” feature, which is a default
#     feature.
#   - arwen-codesign, “Pure-Rust ad-hoc codesigning, only needed for
#     cross-compilation from non-macOS”, dropped with cross-compiling features
#     and not packaged anyway
#   - static feature: only applies to xz2, which we dropped, and we would not
#     want to link liblzma or any other system libraries statically anyway.
#
#   - upload feature: The “maturin upload” command is deprecated since 1.11.0,
#     and we lack some dependencies. Note that upload is removed from the
#     full feature, which is a default feature.
#   - “upload”: optional dependencies bytesize, configparser, dirs, ureq,
#     native-tls, rustls, rustls-pki-types, keyring, wild. These all support
#     the upload feature.
#   - rustls, native-tls; also only needed for the upload feature. Note that
#     rustls is removed from the default features.
#   - password-storage feature; associated with and requires the upload feature
#
#   - auditwheel feature: requires arwen, arwen-codesign, which we *could*
#     package but haven’t. Note that auditwheel is removed from the full
#     feature, which is a default feature.
Patch:          0001-drop-unavailable-features.patch

# * drop incompatible arguments from setuptools_rust cargo invocations
Patch:          0002-drop-incompatible-cargo-flags-from-setuptools_rust.patch

# * revert to building maturin with setuptools instead of bootstrapping maturin
Patch:          0003-revert-to-using-setuptools-for-non-maturin-bootstrap.patch

# Don’t specify generate-import-lib for PyO3 0.29
# https://github.com/PyO3/maturin/pull/3258
Patch:          %{url}/pull/3258.patch

BuildRequires:  cargo-rpm-macros >= 24
%if %{with patchelf}
BuildRequires:  tomcli
%endif

# Some sdist tests expect to see .gitignore files in the sdist, which only
# happens when they are run from inside a git repository, which we create via
# %%autosetup -S git, regardless of whether the check bcond is enabled or not.
BuildRequires:  git-core
# Some tests need to create virtualenvs, preferring “uv venv” (which would be a
# circular dependency) and falling back to “virtualenv.” It turns out that all
# such tests would try to pip-install things from PyPI and therefore must be
# skipped, so we don’t need either of these possible dependencies.

# maturin requires cargo to be available in $PATH
Requires:       cargo

%py_provides python3-maturin

%description
Build and publish crates with pyo3, rust-cpython and cffi bindings as
well as rust binaries as python packages.

# There are two Python extras defined in pyproject.toml:
# zig:
#   We do have zig in Fedora. We don’t have python3dist(ziglang), which is just
#   a hack for installing the zig toolchain via PyPI, but we could work around
#   that. More importantly, we have patched out support for cross-compiling
#   with cargo-zigbuild, so there is no point in exposing this extra.
%if %{with patchelf}
# Based on %%pyproject_extras_subpkg -n maturin patchelf, but we have added
# a dependency on the patchelf command-line tool.
%package -n maturin+patchelf
Summary:        Metapackage for maturin: patchelf extras

Requires:       maturin%{?_isa} = %{version}-%{release}
Requires:       /usr/bin/patchelf

%description -n maturin+patchelf
This is a metapackage bringing in patchelf extras requires for maturin.
It makes sure the dependencies are installed.

%files -n maturin+patchelf -f %{_pyproject_ghost_distinfo}
%endif

%prep
%autosetup -n maturin-%{version} -p1 -S git
%cargo_prep

%if %{with patchelf}
# We don’t have python3dist(patchelf), corresponding to
# https://pypi.org/project/patchelf/, which is just a hack for installing the
# patchelf tool via PyPI. We can still provide the extra by ensuring the
# system-wide patchelf command-line tool is installed.
tomcli set pyproject.toml lists delitem \
    project.optional-dependencies.patchelf patchelf
%endif

# Ensure we don’t use Cargo.lock files from any of the test crates.
find test-crates -type f -name Cargo.lock -print -delete

# Remove pre-compiled Windows executable, “Mock for the windows python launcher
# we can insert in path,” to prove it is unused.
rm test-data/py.exe

%generate_buildrequires
%pyproject_buildrequires -x patchelf
%cargo_generate_buildrequires -f schemars

%if %{with check}
for toml in test-crates/*/Cargo.toml
do
  dir="$(dirname "${toml}")"
  case "${dir}" in
  # Relies on pinned PyO3 0.25; avoid a compat-package dependency.
  test-crates/pyo3-no-extension-module) continue ;;
  # We have no rust-uniffi package.
  test-crates/uniffi-*) continue ;;
  esac
  pushd "${dir}" >/dev/null
  %cargo_generate_buildrequires -a
  popd >/dev/null
done
%endif

%build
# No longer needs to be done manually in Fedora; needed in EPEL
export RUSTFLAGS="%{build_rustflags}"

# write license summary and breakdown
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l maturin

# generate and install shell completions
target/rpm/maturin completions bash > maturin.bash
target/rpm/maturin completions fish > maturin.fish
target/rpm/maturin completions zsh > _maturin

install -Dpm 0644 maturin.bash -t %{buildroot}/%{bash_completions_dir}
install -Dpm 0644 maturin.fish -t %{buildroot}/%{fish_completions_dir}
install -Dpm 0644 _maturin -t %{buildroot}/%{zsh_completions_dir}

%if %{with check}
%check
# We chose not to generate a dependency on a pinned PyO3 0.25 in order to avoid
# an otherwise-unnecessary dependency on a rust-pyo3_0.25 compat package.
skip="${skip-} --skip=errors::pyo3_no_extension_module"

# These would try to install Python packages into virtualenvs from the network,
# such as cffi, pip, or uv, even if they are already installed system-wide.
# Some may also have other obstacles, e.g. no uniffi crate.
skip="${skip-} --skip=develop::develop_backend_parameterized_cases::"
skip="${skip-} --skip=develop::develop_cffi_cases::"
skip="${skip-} --skip=develop::develop_pip_cases::"
skip="${skip-} --skip=develop::develop_uv_cases::"
skip="${skip-} --skip=integration::integration_cases::"
skip="${skip-} --skip=integration::integration_cffi_cases::"
skip="${skip-} --skip=integration::integration_pyo3_abi3t"
skip="${skip-} --skip=integration::integration_pyo3_bin"
skip="${skip-} --skip=integration::pyo3_cffi_build_script"
skip="${skip-} --skip=pep517::pep517_default_profile"
skip="${skip-} --skip=pep517::pep517_editable_profile"

# This relies on a hard-coded PyO3 version number, which needs to match the one
# in test-crates/pyo3-pure/Cargo.lock. This is correct upstream as long as the
# two versions are kept synchronized; it doesn’t work downstream where we use
# system-packaged crates to build test crates, and we don’t respect the
# Cargo.lock files. Since only this test relies on a particular patch version
# specified in the upstream lock files, it’s best to simply skip it.
skip="${skip-} --skip=build_options::tests::test_find_bridge_pyo3_abi3"

# Don’t attempt WASM-related tests.
# (“Failed to build a native library through cargo”)
skip="${skip-} --skip=integration::integration_wasm_hello_world"

# We are not sure why this sdist has extra contents:
#   pyo3_pure-0.1.0+abc123de/.cargo/.global-cache
#   pyo3_pure-0.1.0+abc123de/.cargo/.package-cache
#   pyo3_pure-0.1.0+abc123de/.cargo/.package-cache-mutate
#   pyo3_pure-0.1.0+abc123de/.cargo/registry/CACHEDIR.TAG
skip="${skip-} --skip=sdist::workspace_members_non_local_dep_sdist"

# Unclear exactly what’s going wrong here (“`cargo metadata` exited with an
# error:” with no further output), but this test is creating a local git
# repository and then a dependency on it, and it is little surprise that this
# turns out to be a bit brittle.
skip="${skip-} --skip=sdist::lib_with_parent_workspace_git_dep_sdist"

%{cargo_test -- -- ${skip-}}
%endif

%files -f %{pyproject_files}
%license license-apache
%license license-mit
%license LICENSE.dependencies
%doc README.md
%doc Changelog.md

%{_bindir}/maturin

%{bash_completions_dir}/maturin.bash
%{fish_completions_dir}/maturin.fish
%{zsh_completions_dir}/_maturin

%changelog
## START: Generated by rpmautospec
* Tue Sep 01 2026 Unknown User <please-configure-git-user@example.com> - 1.14.1-5
- Uncommitted changes

* Tue Aug 04 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.1-4
- Fix a typo in a spec-file comment

* Tue Aug 04 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.1-3
- Skip a test that requires a particular locked PyO3 version

* Mon Jul 27 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.1-2
- Fix patchelf extra metapackage; needs to be arched

* Mon Jul 27 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 1.14.1-1
- Update to version 1.14.1; Fixes RHBZ#2413756

* Wed Jul 22 2026 Python Maint <python-maint@redhat.com> - 1.9.6-9
- Rebuilt for Python 3.15.0b4 ABI change

* Thu Jul 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Fri Jul 10 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9.6-7
- Update dialoguer to 0.12

* Wed Jun 03 2026 Python Maint <python-maint@redhat.com> - 1.9.6-6
- Rebuilt for Python 3.15

* Sat Mar 21 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9.6-5
- Rebuilt with rust-tar 0.4.45 for CVE-2026-33056

* Sat Feb 07 2026 Fabio Valentini <decathorpe@gmail.com> - 1.9.6-4
- Rebuild for RUSTSEC-2026-{0007,0008,0009} and CVE-2026-25537

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Dec 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9.6-2
- Allow cargo_metadata 0.23

* Thu Oct 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9.6-1
- Update to version 1.9.6; Fixes RHBZ#2401408

* Tue Sep 23 2025 Fabio Valentini <decathorpe@gmail.com> - 1.9.4-1
- Update to version 1.9.4; Fixes RHBZ#2371174

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.8.7-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Tue Sep 02 2025 Fabio Valentini <decathorpe@gmail.com> - 1.8.7-2
- Rebuild with tracing-subscriber v0.3.20 for CVE-2025-58160

* Tue Aug 19 2025 Fabio Valentini <decathorpe@gmail.com> - 1.8.7-1
- Update to version 1.8.7

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.8.6-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 30 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8.6-4
- Allow console 0.16

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.8.6-2
- Rebuilt for Python 3.14

* Wed May 21 2025 Fabio Valentini <decathorpe@gmail.com> - 1.8.6-1
- Update to version 1.8.6; Fixes RHBZ#2365325

* Wed Mar 19 2025 Fabio Valentini <decathorpe@gmail.com> - 1.8.3-1
- Update to version 1.8.3; Fixes RHBZ#2329012

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 25 2024 Fabio Valentini <decathorpe@gmail.com> - 1.7.4-3
- Bump base64 from 0.21 to 0.22 and itertools from 0.12 to 0.13

* Wed Oct 30 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.7.4-2
- Update goblin to 0.9

* Sun Oct 20 2024 Fabio Valentini <decathorpe@gmail.com> - 1.7.4-1
- Update to version 1.7.4; Fixes RHBZ#2307244

* Sun Sep 29 2024 Fabio Valentini <decathorpe@gmail.com> - 1.7.3-1
- Update to version 1.7.3

* Fri Aug 09 2024 Fabio Valentini <decathorpe@gmail.com> - 1.7.0-1
- Update to version 1.7.0; Fixes RHBZ#2296221

* Mon Jul 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.6.0-3
- Update clap_complete_command to v0.6.1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 16 2024 Fabio Valentini <decathorpe@gmail.com> - 1.6.0-1
- Update to version 1.6.0; Fixes RHBZ#2290642

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.5.1-3
- Rebuilt for Python 3.13

* Thu May 23 2024 Fabio Valentini <decathorpe@gmail.com> - 1.5.1-2
- Rebuild with Rust 1.78 to fix incomplete debuginfo and backtraces

* Sat Apr 13 2024 Fabio Valentini <decathorpe@gmail.com> - 1.5.1-1
- Update to version 1.5.1; Fixes RHBZ#2267946

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 12 2023 Fabio Valentini <decathorpe@gmail.com> - 1.4.0-1
- Update to version 1.4.0; Fixes RHBZ#2252654

* Wed Nov 29 2023 Fabio Valentini <decathorpe@gmail.com> - 1.3.2-1
- Update to version 1.3.2; Fixes RHBZ#2241889

* Tue Sep 05 2023 Fabio Valentini <decathorpe@gmail.com> - 1.2.3-1
- Update to version 1.2.3; Fixes RHBZ#2229485

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jun 24 2023 Python Maint <python-maint@redhat.com> - 1.1.0-2
- Rebuilt for Python 3.12

* Sat Jun 24 2023 Fabio Valentini <decathorpe@gmail.com> - 1.1.0-1
- Update to version 1.1.0; Fixes RHBZ#2214007

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.0.1-3
- Rebuilt for Python 3.12

* Wed Jun 07 2023 Fabio Valentini <decathorpe@gmail.com> - 1.0.1-2
- Enable log and scaffolding features

* Mon May 29 2023 Fabio Valentini <decathorpe@gmail.com> - 1.0.1-1
- Update to version 1.0.1; Fixes RHBZ#2210549

* Tue May 23 2023 Fabio Valentini <decathorpe@gmail.com> - 1.0.0-1
- Update to version 1.0.0

* Tue May 23 2023 Fabio Valentini <decathorpe@gmail.com> - 1.0.0~b9-1
- Update to version 1.0.0b9

* Thu May 18 2023 Fabio Valentini <decathorpe@gmail.com> - 1.0.0~b7-1
- Initial import (#2187698)
## END: Generated by rpmautospec
