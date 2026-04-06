## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT
# License text: https://spdx.org/licenses/MIT.html
# Copyright (c) 2023 Maxwell G <maxwell@gtmx.me>
# Copyright (c) Fedora Project Authors

# Specfile compatability: EPEL >= 9 or Fedora >= 37 and RPM >= 4.16

%bcond tests 1
# Not yet in EPEL10: https://bugzilla.redhat.com/show_bug.cgi?id=2356387
%bcond pendulum %{undefined el10}

Name:           python-orjson
Version:        3.11.7
Release:        %autorelease
Summary:        Fast, correct Python JSON library

# Most source files are either MPL-2.0 (“for files only modified by ijl”) or
# (Apache-2.0 OR MIT), as indicated by SPDX-License-Identifier headers in
# individual sources, resulting in upstream’s SPDX license expression (MPL-2.0
# AND (Apache-2.0 OR MIT)). The exception is the yyjson sources,
# include/yyjson/yyjson.{c,h}, which are both MIT.
License:        MPL-2.0 AND (Apache-2.0 OR MIT) AND MIT
URL:            https://github.com/ijl/orjson
# We must be careful about the source archive.
#
# The PyPI releases have a vendored Rust dependency bundle in include/cargo/,
# which we would remove in %%prep, but which we must still check to make sure
# everything has a license acceptable for distribution in Fedora before
# uploading to the lookaside cache.
# Source:         %%{pypi_source orjson}
# The GitHub archives from
# %%{url}/archive/%%{version}/orjson-%%{version}.tar.gz do not have the
# vendored crates, but they contain benchmark data in data/, some of which is
# lacking its license text (e.g.  data/blns.txt.xz, which is from
# https://github.com/minimaxir/big-list-of-naughty-strings and should carry the
# corresponding MIT license text), and some of which looks like it might have
# at best unclear license status. Since the benchmark data is potentially
# problematic, we would need to filter the GitHub archives with a script.
Source0:        orjson-%{version}-filtered.tar.xz
# ./get_source ${COMMIT} (or ${TAG})
Source1:        get_source

# Still allow PyO3 0.27 for now (upstream wants 0.28):
# https://bugzilla.redhat.com/show_bug.cgi?id=2435852
Patch:          orjson-3.11.7-pyo3-0.27.patch

BuildRequires:  tomcli
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pytest-forked}
# Upstream restricts these test dependencies to particular Python interpreter
# versions and architectures, but we would like to run the corresponding tests
# everywhere.
BuildRequires:  %{py3_dist numpy}
%if %{with pendulum}
BuildRequires:  %{py3_dist pendulum}
%endif
# These are not in tests/requirements.txt, but they enable additional tests
%ifnarch %{ix86}
BuildRequires:  %{py3_dist pandas}
%endif
BuildRequires:  %{py3_dist psutil}
BuildRequires:  cargo-rpm-macros >= 24


%global _description %{expand:
orjson is a fast, correct Python JSON library supporting dataclasses,
datetimes, and numpy}


%description %{_description}

%package -n     python3-orjson
Summary:        %{summary}
# Output of %%{cargo_license_summary}:
#
# (Apache-2.0 OR MIT) AND BSD-3-Clause
# Apache-2.0 OR MIT
# BSD-2-Clause OR Apache-2.0 OR MIT
# BSL-1.0
# MIT
# MIT OR Apache-2.0
# MPL-2.0 AND (Apache-2.0 OR MIT)
# Unlicense OR MIT
#
# Note that this must include the terms of the base package License expression,
# which are all in the first line of the expresion below.
License:        %{shrink:
                MPL-2.0 AND (Apache-2.0 OR MIT) AND MIT AND
                (Apache-2.0 OR BSD-2-Clause OR MIT) AND
                BSD-3-Clause AND
                BSL-1.0 AND
                (Unlicense OR MIT)
                }

# Version from YYJSON_VERSION_STRING in include/yyjson/yyjson.h
#
# Since version 3.11.4, orjson unconditionally uses a bundled copy of the C
# library yyjson, https://github.com/ibireme/yyjson, as the JSON
# deserialization backend. It is forked (customized) and compiled with a
# particular set of options via preprocessor defines (see build.rs), so it is
# not a candidate for unbundling. (Prior to version 3.11.4, this could be
# disabled, and the json crate from the Rust standard library,
# https://docs.rs/json, would be used instead, but this is no longer
# supported.)
Provides:       bundled(yyjson) = 0.9.0

%description -n python3-orjson %{_description}


%prep
%autosetup -p1 -n orjson-%{version}
%cargo_prep

# Remove unwind feature, which is not useful here: the comment above it says
# “Avoid bundling libgcc on musl.”
tomcli-set Cargo.toml del 'features.unwind'
tomcli-set Cargo.toml del 'dependencies.unwinding'

%if %{without pendulum}
sed -i '/^pendulum\b/d' test/requirements.txt
%endif
# Test dependency on arrow appears spurious
# https://github.com/ijl/orjson/issues/559
sed -i '/^arrow\b/d' test/requirements.txt
# Remove unpackaged PyPI plugin
sed -i '/pytest-random-order/d' test/requirements.txt


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:test/requirements.txt}
%cargo_generate_buildrequires -a


%build
export RUSTFLAGS='%{build_rustflags}'
%cargo_license_summary
%{cargo_license} > LICENSES.dependencies
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l orjson


%check
%pyproject_check_import
%if %{with tests}
# --forked: protect the pytest process against test segfaults
# -rs: print the reasons for skipped tests
%pytest --forked -rs
%endif


%files -n python3-orjson -f %{pyproject_files}
%doc README.md


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 3.11.7-2
- Latest state for python-orjson

* Mon Feb 02 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 3.11.7-1
- Update to 3.11.7 (close RHBZ#2436019)

* Thu Jan 29 2026 Benjamin A. Beasley <code@musicinmybrain.net> - 3.11.6-1
- Update to 3.11.6 (close RHBZ#2435304)

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Nov 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.11.4-1
- Update to 3.11.4 (close RHBZ#2406238)
- Bundling yyjson is no longer optional

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.11.3-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Sun Aug 31 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.11.3-1
- Update to 3.11.3 (close RHBZ#2391102)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.11.2-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Aug 12 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.11.2-1
- Update to 3.11.2 (close RHBZ#2387852)

* Sat Jul 26 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.11.1-1
- Update to 3.11.1 (close RHBZ#2383473)

* Wed Jul 23 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.11.0-3
- Patch for PyStr regression on big-endian architectures

* Mon Jul 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.11.0-2
- Package from a GitHub archive, with data/ filtered out

* Wed Jul 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.11.0-1
- Update to 3.11.0 (close RHBZ#2380202)
- Upstream no longer bundles a forked copy of PyO3
- More carefully audit and account for all licenses in the source
- Add a build conditional to allow building with the yyjson backend

* Thu Jun 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.18-5
- PyO3 32-bit fix is now included in upstream Python 3.14 PR

* Thu Jun 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.18-4
- Cherry-pick pyo3-ffi fix for Python 3.14 i686 segfaults

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.10.18-3
- Rebuilt for Python 3.14

* Mon May 26 2025 Karolina Surma <ksurma@redhat.com> - 3.10.18-2
- Support Python 3.14

* Wed Apr 30 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.18-1
- Update to 3.10.18; close RHBZ#2362920

* Sat Apr 12 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.16-3
- No longer allow compact_str 0.8

* Fri Apr 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.16-2
- Expect maturin to handle license files, except LICENSES.vendored/

* Thu Apr 03 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.16-1
- Update to 3.10.6 (close RHBZ#2354600)
- Fixes compatibility with CPython 3.14 alpha 6 (close RHBZ#2349447)

* Thu Apr 03 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.14-5
- Remove spurious test dependency on arrow

* Thu Apr 03 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.14-4
- Omit Pendulum integration tests in EPEL10

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.14-1
- Update to 3.10.14 (close RHBZ#2336424)

* Mon Dec 30 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.13-1
- Update to 3.10.13 (close RHBZ#2334886)
- Work around upstream’s maturin version pin to allow building with maturin
  1.8.0

* Mon Nov 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.12-1
- Update to 3.10.12. Fixes rhbz#2328508

* Sun Nov 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.11-1
- Update to 3.10.11. Fixes rhbz#2319918
- Both pyo3-ffi and pyo3-build-config are now vendored and forked
- Add license files for vendored PyO3 crates

* Sun Aug 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.7-1
- Update to 3.10.7. Fixes rhbz#2303811

* Mon Jul 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.6-1
- Update to 3.10.6. Fixes rhbz#2291190.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 3.10.3-2
- Rebuilt for Python 3.13

* Sat Jun 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.3-1
- Update to 3.10.3. Fixes rhbz#2278078.

* Fri May 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.10.1-2
- Rebuild with Rust 1.78 to fix incomplete debuginfo and backtraces

* Mon Apr 15 2024 Maxwell G <maxwell@gtmx.me> - 3.10.1-1
- Update to 3.10.1. Fixes rhbz#2264126.

* Tue Feb 6 2024 Maxwell G <maxwell@gtmx.me> - 3.9.13-1
- Update to 3.9.13. Fixes rhbz#2262570.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Maxwell G <maxwell@gtmx.me> - 3.9.12-1
- Update to 3.9.12. Fixes rhbz#2259025.

* Wed Nov 22 2023 Maxwell G <maxwell@gtmx.me> - 3.9.10-1
- Update to 3.9.10. Fixes rhbz#2243767.

* Tue Oct 10 2023 Maxwell G <maxwell@gtmx.me> - 3.9.8-1
- Update to 3.9.8. Fixes rhbz#2229530.

* Tue Jul 25 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.2-2
- Backport patch to add PyType_GetDict for Python 3.12
- Fixes: rhbz#2220383

* Fri Jul 21 2023 Maxwell G <maxwell@gtmx.me> - 3.9.2-1
- Update to 3.9.2. Fixes rhbz#2211703.

* Fri Jul 21 2023 Maxwell G <maxwell@gtmx.me> - 3.8.14-1
- Update to 3.8.14.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Python Maint <python-maint@redhat.com> - 3.8.12-2
- Rebuilt for Python 3.12

* Thu May 18 2023 Maxwell G <maxwell@gtmx.me> - 3.8.12-1
- Update to 3.8.12.
- Use maturin as a build system when available

* Fri May 5 2023 Maxwell G <maxwell@gtmx.me> - 3.8.11-1
- Update to 3.8.11. Fixes rhbz#2193468.

* Wed Apr 12 2023 Maxwell G <maxwell@gtmx.me> - 3.8.10-1
- Initial package (rhbz#2184237).

## END: Generated by rpmautospec
