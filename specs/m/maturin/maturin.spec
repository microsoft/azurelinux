## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
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

Name:           maturin
Version:        1.9.6
Release:        %autorelease
Summary:        Build and publish Rust crates as Python packages
SourceLicense:  MIT OR Apache-2.0

%global pypi_version %(echo %{version} | tr -d "~")

# (Apache-2.0 OR MIT) AND BSD-3-Clause
# (MIT OR Apache-2.0) AND Unicode-3.0
# (MIT OR Apache-2.0) AND Unicode-DFS-2016
# 0BSD
# 0BSD OR MIT OR Apache-2.0
# Apache-2.0
# Apache-2.0 OR BSD-2-Clause
# Apache-2.0 OR BSL-1.0
# Apache-2.0 OR MIT
# Apache-2.0 WITH LLVM-exception
# Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT
# BSD-2-Clause OR Apache-2.0 OR MIT
# MIT
# MIT OR Apache-2.0
# MIT OR Zlib OR Apache-2.0
# MIT-0 OR Apache-2.0
# MPL-2.0
# Unicode-3.0
# Unlicense OR MIT
License:        %{shrink:
    0BSD AND
    Apache-2.0 AND
    Apache-2.0 WITH LLVM-exception AND
    BSD-3-Clause AND
    MIT AND
    MPL-2.0 AND
    Unicode-3.0 AND
    Unicode-DFS-2016 AND
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
Source0:        %{pypi_source maturin %{pypi_version}}

# * disable features with missing dependencies:
#   - cross (support for cross compiling with zig / xwin)
#   - upload (support for uploading wheels to PyPI)
# * drop unused test dependencies
Patch:          0001-drop-unavailable-features-and-unused-dev-dependencie.patch

# * drop incompatible arguments from setuptools_rust cargo invocations
Patch:          0002-drop-incompatible-cargo-flags-from-setuptools_rust.patch

# * drop #!/usr/bin/env python3 shebang from maturin/__init__.py
#   https://github.com/PyO3/maturin/pull/2775
Patch:          0003-remove-shebang-from-non-executable-__init__.py-file.patch

# * Update base64 from 0.21 to 0.22
#   https://github.com/PyO3/maturin/pull/2776
# * Update itertools dependency from 0.12 to 0.14
#   https://github.com/PyO3/maturin/pull/2779
Patch:          0004-Bump-base64-from-0.21-to-0.22-and-itertools-from-0.1.patch

# * revert to building maturin with setuptools instead of boostrapping maturin
Patch:          0005-revert-to-using-setuptools-for-non-maturin-bootstrap.patch

# * Update cargo_metadata to 0.20.0: https://github.com/PyO3/maturin/pull/2864.
#   Further widen the allowed versions to permit cargo_metadata 0.23, which was
#   considered upstream in https://github.com/PyO3/maturin/pull/2817, but
#   rejected for now due (solely) to MSRV.
Patch:          0006-Update-cargo_metadata-to-0.20.0-2864.patch

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  python3-devel

# maturin requires cargo to be available in $PATH
Requires:       cargo

%py_provides python3-maturin

%description
Build and publish crates with pyo3, rust-cpython and cffi bindings as
well as rust binaries as python packages.

%prep
%autosetup -n maturin-%{pypi_version} -p1
%cargo_prep

%generate_buildrequires
%pyproject_buildrequires
%cargo_generate_buildrequires -f schemars

%build
export RUSTFLAGS="%{build_rustflags}"
%pyproject_wheel

# write license summary and breakdown
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
%pyproject_install
%pyproject_save_files maturin

# generate and install shell completions
target/rpm/maturin completions bash > maturin.bash
target/rpm/maturin completions fish > maturin.fish
target/rpm/maturin completions zsh > _maturin

install -Dpm 0644 maturin.bash -t %{buildroot}/%{bash_completions_dir}
install -Dpm 0644 maturin.fish -t %{buildroot}/%{fish_completions_dir}
install -Dpm 0644 _maturin -t %{buildroot}/%{zsh_completions_dir}

%if %{with check}
%check
# * skip tests for which fixtures are not included in published sources
%{cargo_test -- -- --exact %{shrink:
    --skip build_options::test::test_find_bridge_bin
    --skip build_options::test::test_find_bridge_cffi
    --skip build_options::test::test_find_bridge_pyo3
    --skip build_options::test::test_find_bridge_pyo3_abi3
    --skip build_options::test::test_find_bridge_pyo3_feature
    --skip metadata::test::test_implicit_readme
    --skip metadata::test::test_merge_metadata_from_pyproject_dynamic_license_test
    --skip metadata::test::test_merge_metadata_from_pyproject_toml
    --skip metadata::test::test_merge_metadata_from_pyproject_toml_with_customized_python_source_dir
    --skip metadata::test::test_pep639
    --skip pyproject_toml::tests::test_warn_missing_maturin_version
}}
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
* Mon Apr 06 2026 azldev <> - 1.9.6-5
- Latest state for maturin

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
