## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# The Python extension tests now segfault on i686. Starting with Fedora 42, we
# no longer build the Python extension on i686; in the medium term, we wish to
# drop i686 support altogether, but we must coordinate all reverse dependencies
# doing so first; see the notes in %%check.
%bcond python %[ %{?__isa_bits} != 32 || %{defined fc41} ]

Name:           re2
%global tag 2025-11-05
%global so_version 11
%global base_version %(echo '%{tag}' | tr -d -)
# Ensure this matches the version in the metadata / setup.py!
%global py_version 1.1.%{base_version}
Version:        %{base_version}
Epoch:          2
Release:        %autorelease
Summary:        C++ fast alternative to backtracking RE engines

# The entire source is BSD-3-Clause, except:
#   - lib/git/commit-msg.hook is Apache-2.0, but is not used in the build and
#     is removed in %%prep
License:        BSD-3-Clause
SourceLicense:  %{license} AND Apache-2.0
URL:            https://github.com/google/re2
Source:         %{url}/archive/%{tag}/re2-%{tag}.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++

BuildRequires:  cmake(absl)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  cmake(GTest)

%if %{with python}
# Python extension
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pybind11}
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_packaging_header_only_libraries
BuildRequires:  pybind11-static

# Python extension tests
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist absl-py}
%endif

%global common_description %{expand:
RE2 is a fast, safe, thread-friendly alternative to backtracking regular
expression engines like those used in PCRE, Perl, and Python. It is a C++
library.}

%description %{common_description}


%package        devel
Summary:        C++ header files and library symbolic links for re2

Requires:       re2%{?_isa} = %{epoch}:%{base_version}-%{release}

%description    devel %{common_description}

This package contains the C++ header files and symbolic links to the shared
libraries for re2. If you would like to develop programs using re2, you will
need to install re2-devel.


%if %{with python}
%package -n     python3-google-re2
Summary:        RE2 Python bindings
Version:        %{py_version}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_requiring_base_package
Requires:       re2%{?_isa} = %{epoch}:%{base_version}-%{release}

Conflicts:      python3-fb-re2
Obsoletes:      python3-fb-re2 < 1.0.7-19

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%py_provides python3-re2

%description -n python3-google-re2
A drop-in replacement for the re module.

It uses RE2 under the hood, of course, so various PCRE features (e.g.
backreferences, look-around assertions) are not supported. See
https://github.com/google/re2/wiki/Syntax for the canonical reference, but
known syntactic ”gotchas” relative to Python are:

  • PCRE supports \Z and \z; RE2 supports \z; Python supports \z,
    but calls it \Z. You must rewrite \Z to \z in pattern strings.

Known differences between this module’s API and the re module’s API:

  • The error class does not provide any error information as attributes.
  • The Options class replaces the re module’s flags with RE2’s options as
    gettable/settable properties. Please see re2.h for their documentation.
  • The pattern string and the input string do not have to be the same type.
    Any str will be encoded to UTF-8.
  • The pattern string cannot be str if the options specify Latin-1 encoding.
%endif


%prep
%autosetup -n re2-%{tag}
# Show that a file licensed Apache-2.0 is not used in the build and does not
# contribute to the licenses of the binary RPMs:
rm lib/git/commit-msg.hook


%if %{with python}
%generate_buildrequires
cd python
%pyproject_buildrequires
%endif


%conf
%cmake \
    -DRE2_TEST:BOOL=ON \
    -DRE2_BENCHMARK:BOOL=OFF \
    -DRE2_USE_ICU:BOOL=ON \
    -GNinja

%if %{with python}
cat >> python/setup.cfg <<EOF
[build_ext]
include_dirs=${PWD}
library_dirs=${PWD}/%{_vpath_builddir}
EOF
%endif


%build
%cmake_build
%if %{with python}
cd python
%pyproject_wheel
%endif


%install
%cmake_install

%if %{with python}
cd python
%pyproject_install
%pyproject_save_files -l re2
%endif


%check
%ctest

%if %{with python}
# Python tests now segfault on i686, but we cannot drop support under
# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval because re2
# is not yet a leaf package on that architecture. Instead, we skip the Python
# tests on i686.
#
# The following directly-dependent packages are ExcludeArch: %%{ix86}:
#   bloaty, ceph, credentials-fetcher, CuraEngine_grpc_definitions, dnsdist,
#   libarrow, mtxclient, nheko, onnx, onnxruntime, parlaylib,
#   perl-re-engine-RE2, python-torchtext
#
# The following are not (yet):
# - grpc:
#   Not blocked by: CuraEngine_grpc_definitions, bear, buildbox, buildstream,
#                   ceph, credentials-fetcher, frr, libarrow, libphonenumber,
#                   syslog-ng
#     Note that syslog-ng does depend on grpc *and* builds on i686, but grpc
#     support is disabled on i686, so all is well.
#   Blocked by:
#   - duplicity (indirect, via noarch intermediate packages:
#     grpc <- python-google-api-core <- google-api-python-client <- duplicity)
#     - Not blocked by: duply
#     - Blocked by:
#       - deja-dup
#   - fastnetmon: https://src.fedoraproject.org/rpms/fastnetmon/pull-request/2
#   - matrix-synapse (indirect, via noarch intermediate package:
#     grpc <- python-sentry-sdk <- matrix-synapse)
#   - nanopb
#   - perl-grpc-xs
#   - qt6-qtgrpc
#   TBD:
#     There are many more packages that depend directly or indirectly on
#     python3-grpcio in particular at install time, but not at build time. We
#     must explore the entire tree looking for arched packages that build on
#     i686.
# Run the tests from the top-level directory to make sure we don’t accidentally
# import the “un-built” package instead of the one in the buildroot.
ln -s python/re2_test.py
LD_LIBRARY_PATH='%{buildroot}%{_libdir}' %pytest re2_test.py
%endif


%files
%license LICENSE
%doc README.md
%{_libdir}/libre2.so.%{so_version}{,.*}


%files          devel
%doc doc/syntax.{html,txt}
%{_includedir}/re2/
%{_libdir}/libre2.so
%{_libdir}/pkgconfig/re2.pc
%{_libdir}/cmake/re2/


%if %{with python}
%files -n       python3-google-re2 -f %{pyproject_files}
%endif


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2:20251105-2
- test: add initial lock files

* Thu Nov 06 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2:20251105-1
- Update to 20251105

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2:20250812-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Sep 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2:20250812-3
- Rebuilt for abseil-cpp 20250814.0

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2:20250812-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Aug 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2:20250812-1
- Update to 2025-08-12

* Wed Aug 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2:20250805-1
- Update to 2025-08-05

* Tue Aug 05 2025 František Zatloukal <fzatlouk@redhat.com> - 2:20250722-2
- Rebuilt for icu 77.1

* Sun Aug 03 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 2:20250722-1
- Update to 20250722
- Adjust the version of python3-google-re2 to match the version on PyPI and
  in its metadata; bump Epoch to preserve the upgrade path

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:20240702-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 15 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-34
- Do not build and run benchmarks

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1:20240702-33
- Rebuilt for Python 3.14

* Mon May 26 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-32
- Rebuilt for abseil-cpp 20250512.0

* Sat May 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-31
- Remove conditionals for F41, which is reaching end-of-life

* Tue Feb 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-30
- Rebuilt for abseil-cpp-20250127.0

* Tue Jan 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-28
- Update spec-file notes about i686 reverse dependencies

* Tue Jan 21 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-27
- Starting in F42, don’t build the Python extension on i686

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:20240702-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-23
- Work around segfault in Python tests on i686

* Sun Dec 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-22
- Add a SourceLicense field

* Sun Dec 08 2024 Pete Walter <pwalter@fedoraproject.org> - 1:20240702-21
- Rebuild for ICU 76

* Sat Nov 02 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-20
- Invoke %%cmake in %%conf rather than in %%build

* Mon Aug 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-19
- Build the Python extension, replacing python-fb-re2

* Sun Aug 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-18
- Rebuilt for abseil-cpp-20240722.0

* Fri Aug 16 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-17
- Enable full Unicode properties support by linking ICU

* Thu Aug 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-16
- Include HTML and text syntax references as devel package documentation

* Thu Aug 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-14
- Improve the source URL

* Thu Aug 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-13
- Switch the URL from HTTP to HTTPS

* Thu Aug 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-12
- Convert License to SPDX

* Thu Aug 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-10
- Use a simplified description from upstream.

* Thu Aug 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-9
- Build with ninja instead of make
- This is modestly faster and has no disadvantages

* Thu Aug 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-8
- Fix unowned directory %%{_libdir}/cmake/re2/

* Thu Aug 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1:20240702-5
- Use CMake to build and run tests; this results in more thorough testing

* Tue Aug 13 2024 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1:20240702-1
- Upgrade to 2024-07-02

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:20220601-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:20220601-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:20220601-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:20220601-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:20220601-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 30 2022 Denis Arnaud <denis.arnaud_fedora@m4x.org>  - 1:20220601-1
- Upgrade to 2022-06-01

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:20211101-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:20211101-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Adam Williamson <awilliam@redhat.com> - 1:20211101-2
- Backport patch to fix thread dependency discovery
- Substitute the pkgconfig file before installing it (#2038572)
- Drop soname patches as upstream seems to be doing it properly now

* Fri Jan 07 2022 Denis Arnaud <denis.arnaud_fedora@m4x.org>  - 1:20211101-1
- Upgrade to 2021-11-01

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 1:20190801-8
- Rebuilt for removed libstdc++ symbol (#1937698)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:20190801-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 26 2020 Jeff Law <law@redhat.com> - 1:20190801-6
- No longer force C++11

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:20190801-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:20190801-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 14 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:20190801-3
- -devel: use epoch in versioned dep

* Wed Aug 14 2019 Rex Dieter <rdieter@fedoraproject.org> - 1:20190801-2
- bump soname
- tighten %%files, track soname explicitly
- use %%make_build %%make_install macros
- Epoch:1 for upgrade path (from f29)

* Sat Aug 03 2019 Lukas Vrabec <lvrabec@redhat.com> - 20190801-1
- update to 20190801

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20160401-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20160401-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20160401-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20160401-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160401-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160401-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160401-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 29 2016 Tom Callaway <spot@fedoraproject.org> - 20160401-2
- hardcode -std=c++11 for older compilers

* Fri Apr 29 2016 Tom Callaway <spot@fedoraproject.org> - 20160401-1
- update to 20160401

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20131024-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20131024-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 15 2015 Petr Pisar <ppisar@redhat.com> - 20131024-4
- Rebuild owing to C++ ABI change in GCC-5 (bug #1195351)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20131024-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20131024-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 11 2013 Tom Callaway <spot@fedoraproject.org> - 20131024-1
- update to 20131024
- fix symbols export to stop test from failing

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130115-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Feb 17 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> 20130115-2
- Took into account the feedback from review request (#868578).

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> 20130115-1
- The download source comes now directly from the project.

* Thu Oct 25 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.0.0-2
- Took into account review request (#868578) feedback.

* Sat Oct 20 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> 0.0.0-1
- RPM release for Fedora 18

## END: Generated by rpmautospec
