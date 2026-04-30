## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond tests 1

#global commit xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#global snapdate YYYYMMDD

Name:           python-cramjam
Version:        2.11.0
Release:        %autorelease
Summary:        Thin Python bindings to de/compression algorithms in Rust

# SPDX
License:        MIT
URL:            https://github.com/milesgranger/cramjam

%if !%{defined commit}

# This handles pre-release versioning:
%global srcversion %(echo '%{version}' | tr -d '~')
# Future PyPI sdists should not include benchmark data (some of which has
# complicated or unclear license status). See: “Consider excluding benchmarks
# from PyPI sdists” https://github.com/milesgranger/cramjam/issues/178
Source:         %{pypi_source cramjam %{srcversion}}

%else

%global srcversion %{commit}
# For snapshots, we must filter the source archive from GitHub using the script
# in Source1, since some of the benchmark data has complicated or unclear
# license status.
Source0:        cramjam-%{commit}-filtered.tar.gz
# ./get_source ${COMMIT} (or ${TAG})
Source1:        get_source

%endif

BuildSystem:            pyproject
BuildOption(install):   -l cramjam

BuildRequires:  tomcli >= 0.8.0
BuildRequires:  cargo-rpm-macros >= 24

%if %{with tests}
# These (along with some unwanted dependencies like linters) are listed in the
# dev extra in pyproject.toml.
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist hypothesis}
%endif

%global common_description %{expand:
%{summary}.}

%description %{common_description}


%package -n     python3-cramjam
Summary:        %{summary}
# 0BSD OR MIT OR Apache-2.0
# Apache-2.0
# BSD-3-Clause
# BSD-3-Clause AND MIT
# MIT
# MIT OR Apache-2.0
# MIT OR Zlib OR Apache-2.0
License:        %{shrink:
                (0BSD OR MIT OR Apache-2.0) AND
                Apache-2.0 AND
                BSD-3-Clause AND
                MIT AND
                (MIT OR Zlib OR Apache-2.0)
                }
# LICENSE.dependencies contains a full license breakdown

%description -n python3-cramjam %{common_description}


%prep -a
# Downstream-only: patch out the generate-import-lib feature, which is only
# relevant on Windows, and which depends on the corresponding pyo3 feature –
# which is not packaged for that reason.
tomcli set Cargo.toml del 'features.generate-import-lib'

# Downstream-only: patch out the wasm-compat feature, which is unnecessary and
# would bring in unwanted dependencies
tomcli set Cargo.toml del 'features.wasm32-compat'

# Downstream-only: patch out the "experimental" feature and all of the features
# related to blosc2 and isa-l support. We only want to build the Python
# extension with the default features, and we only want maturin to check
# dependencies for those features.
blosc2_isal_features="$(
  tomcli get Cargo.toml features -F newline-keys |
    grep -E 'blosc2|ideflate|igzip|isal|izlib' |
    tr '\n' ' '
)"
for feature in experimental ${blosc2_isal_features}
do
  tomcli set Cargo.toml del "features.${feature}"
done

# Downstream-only: remove all the static-linking features, and make the
# dynamic-linking ones default, as we do in rust-libcramjam.
static_features="$(
  tomcli get Cargo.toml features -F newline-keys |
    grep -E '.-static$' |
    tr '\n' ' '
)"
for sf in ${static_features}
do
  tomcli set Cargo.toml del "features.${sf}"
  if ! echo "${sf}" | grep -E '^use-system-' >/dev/null
  then
    binding="$(echo "${sf}" | sed -r 's/-static//')"
    tomcli set Cargo.toml lists replace --type regex \
        "features.${binding}" "${binding}-static" "${binding}-shared"
  fi
done

%cargo_prep


%generate_buildrequires -a
%cargo_generate_buildrequires


%build -p
%cargo_license_summary
%{cargo_license} > LICENSES.dependencies


%check -a
%if %{with tests}
# Test failures in test_variants_decompress_into with recent hypothesis
# versions: https://github.com/milesgranger/cramjam/issues/201
#
# It is hard to be really sure what is going on here. The failures are
# concerning, and might (or might not) reflect a serious problem. Nevertheless,
# since the problem appears to be linked to newer hypothesis versions, there’s
# not reason to believe that the package has *new* problems. It *might* have
# newly *revealed* problems. This merits further investigation.
k="${k-}${k+ and }not test_variants_decompress_into"

# Regression with miniz_oxide>0.8.5
# https://github.com/milesgranger/cramjam/issues/211
# Failed: DID NOT RAISE <class 'cramjam.DecompressionError'>
k="${k-}${k+ and }not test_variants_raise_exception[deflate]"

%pytest -k "${k-}" --ignore=benchmarks/test_bench.py -v
%endif


%files -n python3-cramjam -f %{pyproject_files}
%doc README.md


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2.11.0-4
- test: add initial lock files

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.11.0-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.11.0-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Jul 28 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.11.0-1
- Update to 2.11.0 (close RHBZ#2383690)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0~rc3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jun 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.11.0~rc3-3
- No longer run tests in parallel

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.11.0~rc3-2
- Rebuilt for Python 3.14

* Sun Jun 01 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.11.0~rc3-1
- Update to 2.11.0rc3 (close RHBZ#2369614)

* Sun Jun 01 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.11.0~rc2-3
- Updated Python 3.14 patch

* Fri May 23 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.11.0~rc2-2
- Patch for Python 3.14 (close RHBZ#2367779)

* Mon May 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.11.0~rc2-1
- Update to 2.11.0~rc2 (close RHBZ#2361989)

* Sun May 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.10.0-3
- Report and skip test that fails with miniz_oxide>0.8.5

* Thu Apr 24 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.10.0-2
- Adjust .rpmlintrc file for updated rpmlint

* Sun Apr 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.10.0-1
- Update to 2.10.0 (close RHBZ#2359237)

* Tue Apr 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.10.0~rc1-8
- Use the provisional pyproject declarative buildsystem
- Drop EPEL10 conditionals

* Tue Apr 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.10.0~rc1-7
- Remove workarounds for older versions of tomcli

* Tue Apr 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.10.0~rc1-6
- Expect maturin to handle license files

* Tue Apr 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.10.0~rc1-5
- Update PyO3 to 0.24

* Mon Mar 03 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.10.0~rc1-3
- No longer need to patch pyproject.toml to keep maturin from stripping
  binaries

* Sun Mar 02 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.10.0~rc1-2
- Prepare for EPEL10 branching

* Sun Mar 02 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.10.0~rc1-1
- Update to 2.10.0~rc1

* Tue Feb 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.10.0~20250222gitcdc7d30-1
- Update to a later pre-release snapshot of 2.10.0
- Builds with rust-libcramjam 0.7

* Fri Feb 07 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.10.0~20250104git61564e7-1
- Update to a pre-release snapshot of 2.10.0
- Disable experimental features (blosc2/isa-l)

* Fri Feb 07 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.9.1-5
- Restore i686 support

* Fri Feb 07 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.9.1-4
- Ignore test failures with recent hypothesis versions, for now
- https://github.com/milesgranger/cramjam/issues/201

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2.9.1-2
- Patch for maturin 1.8.0

* Fri Dec 13 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.9.1-1
- Update to 2.9.1 (close RHBZ#2332068)

* Tue Dec 10 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.9.0-2
- Skip blosc2 variants tests since they may segfault

* Wed Oct 16 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.9.0-1
- Update to 2.9.0 (close RHBZ#2310247)

* Wed Oct 16 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.8.3-10
- Revert "Fix automatic provides on Python extension due to SONAME"
- The root cause is fixed in rust-1.81.0-4 and later.

* Wed Oct 02 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.8.3-9
- Rebuilt with rust-brotli 7.0.0

* Mon Sep 30 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.8.3-8
- F41+: Drop i686 support (leaf package on that architecture)

* Thu Sep 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.8.3-7
- Fix automatic provides on Python extension due to SONAME

* Wed Aug 07 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.8.3-6
- Rebuilt with latest crate dependencies

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.8.3-4
- Rebuilt with rust-lz4 1.25.0

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 2.8.3-3
- Rebuilt for Python 3.13

* Fri May 24 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.8.3-2
- Rebuild with Rust 1.78 to fix incomplete debuginfo and backtraces

* Tue Mar 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.8.3-1
- Update to 2.8.3

* Sun Mar 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.8.2-1
- Update to 2.8.2 (close RHBZ#2267466)

* Wed Feb 14 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.8.1-1
- Initial package (close RHBZ#2257285)
## END: Generated by rpmautospec
