## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 6;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond cpp_tests 1
# Disabled for now because protobuf-devel does not provide CMake files
%bcond cpp_grpc_test 0
%bcond py_tests 1

%bcond mingw 1

Name:           flatbuffers
Version:        25.2.10
# The .so version is equal to the project version since upstream offers no ABI
# stability guarantees. We manually repeat it here and and use the macro in the
# file lists as a reminder to avoid undetected .so version bumps. See
# https://github.com/google/flatbuffers/issues/7759.
%global so_version 25.2.10
Release:        %autorelease
Summary:        Memory efficient serialization library

# The entire source code is Apache-2.0. Even code from grpc, which is
# BSD-3-Clause in its upstream, is intended to be Apache-2.0 in this project.
# (Google is the copyright holder for both projects, so it can relicense at
# will.) See https://github.com/google/flatbuffers/pull/7073.
License:        Apache-2.0
URL:            https://google.github.io/flatbuffers
%global forgeurl https://github.com/google/flatbuffers
Source0:        %{forgeurl}/archive/v%{version}/%{name}-%{version}.tar.gz
# Hand-written for Fedora in groff_man(7) format based on docs/source/flatc.md
Source1:        flatc.1

# Adjust library installation under mingw
# https://github.com/google/flatbuffers/pull/8365
Patch:          flatbuffers_mingw-lib.patch

# NumPy 2.x fix
# https://github.com/google/flatbuffers/issues/8332
Patch:          %{forgeurl}/pull/8346.patch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  gcc-c++
BuildRequires:  cmake
# The ninja backend should be slightly faster than make, with no disadvantages.
BuildRequires:  ninja-build
%if %{with cpp_tests} && %{with cpp_grpc_test}
BuildRequires:  cmake(absl)
BuildRequires:  cmake(protobuf)
BuildRequires:  grpc-devel
%endif

BuildRequires:  python3-devel
# Enables numpy integration tests
BuildRequires:  python3dist(numpy)

%if %{with mingw}
BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-python3
BuildRequires:  mingw32-python3-build
BuildRequires:  mingw32-python3-numpy

BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-python3
BuildRequires:  mingw64-python3-build
BuildRequires:  mingw64-python3-numpy
%endif

# From grpc/README.md:
#
#   NOTE: files in `src/` are shared with the GRPC project, and maintained
#   there (any changes should be submitted to GRPC instead). These files are
#   copied from GRPC, and work with both the Protobuf and FlatBuffers code
#   generator.
#
# It’s not clearly documented which GPRC version is excerpted, but see
# https://github.com/google/flatbuffers/pull/4305 for more details. We use
# _GRPC_VERSION from the WORKSPACE file as the bundled GRPC version, but we are
# not 100% certain that this is entirely correct.
#
# It is not possible to unbundle this because private/internal APIs are used.
Provides:       bundled(grpc) = 1.49.0

%global common_description %{expand:
FlatBuffers is a cross platform serialization library architected for maximum
memory efficiency. It allows you to directly access serialized data without
parsing/unpacking it first, while still having great forwards/backwards
compatibility.}

%description %{common_description}


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel %{common_description}

This package contains libraries and header files for developing applications
that use FlatBuffers.


%package        compiler
Summary:        FlatBuffers compiler (flatc)
# The flatc compiler does not link against the shared library, so this could
# possibly be removed; we leave it for now to ensure there is no version skew
# across subpackages.
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    compiler %{common_description}

This package contains flatc, the FlatBuffers compiler.


%package        doc
Summary:        Documentation and examples for FlatBuffers

BuildArch:      noarch

%description    doc %{common_description}

This package contains documentation and examples for FlatBuffers.


%package -n     python3-flatbuffers
Summary:        FlatBuffers serialization format for Python

BuildArch:      noarch

Recommends:     python3dist(numpy)

Provides:       flatbuffers-python3 = %{version}-%{release}
Obsoletes:      flatbuffers-python3 < 2.0.0-6

%description -n python3-flatbuffers %{common_description}

This package contains the Python runtime library for use with the Flatbuffers
serialization format.


%if %{with mingw}
# Win32
%package -n mingw32-%{name}
Summary:        MinGW Windows %{name} library

BuildArch:      noarch

%description -n mingw32-%{name}
%{summary}


%package -n mingw32-python3-%{name}
Summary:        MinGW Windows %{name} Python 3 bindings

BuildArch:      noarch

%description -n mingw32-python3-%{name}
%{summary}


# Win64
%package -n mingw64-%{name}
Summary:        MinGW Windows %{name} library

BuildArch:      noarch

%description -n mingw64-%{name}
%{summary}


%package -n mingw64-python3-%{name}
Summary:        MinGW Windows %{name} Python 3 bindings

BuildArch:      noarch

%description -n mingw64-python3-%{name}
%{summary}


%{?mingw_debug_package}
%endif


%prep
%autosetup -p1
# Remove unused directories that contain pre-compiled .jar files:
rm -rvf android/ kotlin/

%py3_shebang_fix samples
# Fix paths in the Python test script to match how our build is organized:
#   - Use flatc from the buildroot, not the root of the extracted sources
#   - Use the proper python3 interpreter path from the RPM macro
#   - Don’t attempt to run tests with interpreters other than python3
#   - Add the buildroot python3_sitelib to PYTHONPATH so the flatbuffers
#     package can be found; the appropriate PYTHONPATH is supplied by could be
#     handled by %%{py3_test_envvars}, but the test script overrides it
#   - Make sure we don’t do coverage analysis even if python3-coverage is
#     somehow installed as an indirect dependency
sed -r -i.upstream \
    -e 's|[^[:blank:]]*(/flatc)|%{buildroot}%{_bindir}\1|' \
    -e 's| python3 | %{python3} |' \
    -e 's|run_tests [^/]|# &|' \
    -e 's|PYTHONPATH=|&%{buildroot}%{python3_sitelib}:|' \
    -e 's|which coverage|/bin/false|' \
    tests/PythonTest.sh


%generate_buildrequires
pushd python >/dev/null
%pyproject_buildrequires
popd >/dev/null


%conf
# Needed for correct Python wheel version
export VERSION='%{version}'
%cmake -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
%if %{with cpp_tests}
    -DFLATBUFFERS_BUILD_TESTS:BOOL=ON \
%if %{with cpp_grpc_test}
    -DFLATBUFFERS_BUILD_GRPCTEST:BOOL=ON \
    -DGRPC_INSTALL_PATH:PATH=%{_prefix} \
%endif
%else
    -DFLATBUFFERS_BUILD_TESTS:BOOL=OFF \
    -DFLATBUFFERS_BUILD_GRPCTEST:BOOL=OFF \
%endif
    -DFLATBUFFERS_BUILD_SHAREDLIB=ON \
    -DFLATBUFFERS_BUILD_FLATLIB=OFF \
    -DFLATBUFFERS_BUILD_FLATC=ON

%if %{with mingw}
(
%mingw_cmake \
    -DFLATBUFFERS_BUILD_TESTS:BOOL=OFF \
    -DFLATBUFFERS_BUILD_GRPCTEST:BOOL=OFF \
    -DFLATBUFFERS_BUILD_SHAREDLIB=ON \
    -DFLATBUFFERS_BUILD_FLATLIB=OFF \
    -DFLATBUFFERS_BUILD_FLATC=ON
)
%endif


%build
%cmake_build

pushd python
%pyproject_wheel
popd

%if %{with mingw}
(
%mingw_make_build

pushd python
%mingw32_py3_build_wheel
%mingw64_py3_build_wheel
popd
)
%endif


%install
%cmake_install
pushd python
%pyproject_install
%pyproject_save_files flatbuffers
popd
install -t '%{buildroot}%{_mandir}/man1' -D -p -m 0644 '%{SOURCE1}'

%if %{with mingw}
(
%mingw_make_install

pushd python
%mingw32_py3_install_wheel
%mingw64_py3_install_wheel
popd
%mingw_debug_install_post
)
%endif


%check
%if %{with cpp_tests}
%ctest
%endif
%if %{with py_tests}
# The test script overrides PYTHONPATH and PYTHONDONTWRITEBYTECODE, but we’d
# like to pass through any other environment variables that are set by
# %%{py3_test_envvars}.
%{py3_test_envvars} ./tests/PythonTest.sh
%endif
# Do an import-only “smoke test” even if we ran the Python tests; we are not
# convinced that they cover all modules in the package.
%pyproject_check_import


%files
%license LICENSE
%{_libdir}/libflatbuffers.so.%{so_version}


%files devel
%{_includedir}/flatbuffers/

%{_libdir}/libflatbuffers.so

%{_libdir}/cmake/flatbuffers/
%{_libdir}/pkgconfig/flatbuffers.pc


%files compiler
%{_bindir}/flatc
%{_mandir}/man1/flatc.1*


%files doc
%license LICENSE
%doc CHANGELOG.md
%doc SECURITY.md
%doc README.md

%doc examples/
%doc samples/


%files -n python3-flatbuffers -f %{pyproject_files}
%license LICENSE


%if %{with mingw}
%files -n mingw32-%{name}
%license LICENSE
%{mingw32_bindir}/flatc.exe
%{mingw32_bindir}/libflatbuffers-%{so_version}.dll
%{mingw32_libdir}/libflatbuffers.dll.a
%{mingw32_libdir}/pkgconfig/flatbuffers.pc
%{mingw32_libdir}/cmake/flatbuffers/
%{mingw32_includedir}/flatbuffers/

%files -n mingw32-python3-%{name}
%{mingw32_python3_sitearch}/flatbuffers/
%{mingw32_python3_sitearch}/flatbuffers-%{version}.dist-info/


%files -n mingw64-%{name}
%license LICENSE
%{mingw64_bindir}/flatc.exe
%{mingw64_bindir}/libflatbuffers-%{so_version}.dll
%{mingw64_libdir}/libflatbuffers.dll.a
%{mingw64_libdir}/pkgconfig/flatbuffers.pc
%{mingw64_libdir}/cmake/flatbuffers/
%{mingw64_includedir}/flatbuffers/

%files -n mingw64-python3-%{name}
%{mingw64_python3_sitearch}/flatbuffers/
%{mingw64_python3_sitearch}/flatbuffers-%{version}.dist-info/
%endif


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 25.2.10-6
- test: add initial lock files

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 25.2.10-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 25.2.10-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 25.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 25.2.10-2
- Rebuilt for Python 3.14

* Tue Feb 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.2.10-1
- Update to 25.2.10 (close RHBZ#2344831)

* Sat Jan 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.24-2
- Rewrite the man page based on upstream docs/source/flatc.md

* Sat Jan 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 25.1.24-1
- Update to 25.1.24 (close RHBZ#2339399)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.12.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 24.12.23-4
- Make MinGW subpackages noarch

* Mon Jan 13 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 24.12.23-3
- Fix defective descriptions in MinGW subpackages

* Wed Dec 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 24.12.23-1
- Update to 24.12.23 (close RHBZ#2333905)
- Update the man page

* Tue Dec 17 2024 Sandro <devel@penguinpee.nl> - 24.3.25-9
- Apply patch for NumPy 2.x

* Mon Nov 04 2024 Sandro Mani <manisandro@gmail.com> - 24.3.25-8
- Prevent env-pollution from mingw build

* Fri Nov 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 24.3.25-7
- Invoke %%cmake in %%conf rather than in %%build

* Sat Jul 27 2024 Sandro Mani <manisandro@gmail.com> - 24.3.25-5
- Add upstream link for proposed flatbuffers_mingw-lib.patch

* Sat Jul 27 2024 Sandro Mani <manisandro@gmail.com> - 24.3.25-4
- Add mingw build

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.3.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 24.3.25-2
- Rebuilt for Python 3.13

* Thu Mar 28 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 24.3.25-1
- Update to 24.3.25 (close RHBZ#2271730)

* Fri Mar 08 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 24.3.7-1
- Update to 24.3.7 (close RHBZ#2268502)

* Fri Mar 08 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 23.5.26-8
- Improve the Summary

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.5.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.5.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 11 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.5.26-4
- F38+: Run the tests with %%{py3_test_envvars}

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.5.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.5.26-2
- Use new (rpm 4.17.1+) bcond style (missed one)

* Sun Jun 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.5.26-1
- Update to 23.5.26 (close RHBZ#2196940)

* Sun Jun 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.5.9-3
- Use new (rpm 4.17.1+) bcond style

* Sat Jun 17 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.5.9-2
- Fix and re-enable Python tests

* Sat Jun 17 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.5.9-1
- Update to 23.5.9

* Sat Jun 17 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.5.8-1
- Update to 23.5.8
- Disable Python tests due to upstream issue #7944

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 23.3.3-4
- Rebuilt for Python 3.12

* Sat Jun 03 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.3.3-3
- Remove explicit %%set_build_flags, not needed since F36

* Sat Mar 04 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.3.3-1
- Update to 23.3.3 (close RHBZ#2175405)

* Mon Jan 23 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.1.21-1
- Update to 23.1.21 (close RHBZ#2159100)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 23.1.4-1
- Update to 23.1.4 (close RHBZ#2159100)

* Mon Jan 09 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 22.12.06-6
- Fix Python big-endian (s390x) issues

* Sun Jan 08 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 22.12.06-5
- Enable Python tests

* Sun Jan 08 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 22.12.06-4
- Minor spec file tidying

* Sun Jan 08 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 22.12.06-3
- Add CHANGELOG.md and examples/ to -doc subpackage

* Tue Dec 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 22.12.06-2
- Leaf package: remove i686 support

* Wed Dec 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 22.12.06-1
- Update to 22.12.06 (close RHBZ#2151541)

* Tue Dec 06 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 22.11.23-2
- Apply upstream PR#7681 for s390x failures

* Fri Nov 25 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 22.11.23-1
- Update to 22.11.23 (close RHBZ#2130864)

* Sat Oct 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 22.10.26-3
- Fix some minor errors in flatc help output

* Sat Oct 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 22.10.26-2
- Update flatc.1 man page

* Sat Oct 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 22.10.26-1
- Update to 22.10.26 (close RHBZ#2130864)

* Sat Oct 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 22.10.25-1
- Update to 22.10.25

* Sat Oct 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 22.9.29-1
- Update to 22.9.29

* Sat Oct 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 22.9.24-1
- Update to 22.9.24 (.so version 2→22)

* Sat Oct 29 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.0.8-3
- Drop a skipped test that is now upstream

* Tue Aug 30 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.0.8-2
- Out-of-source build fix

* Tue Aug 30 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.0.8-1
- Update to 2.0.8 (close RHBZ#2122466, fix RHBZ#2122528)

* Wed Aug 24 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.0.7-1
- Update to 2.0.7 (close RHBZ#2120889)

* Mon Aug 01 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.0.6-4
- Update License field to SPDX
- Treat grpc-derived code as Apache-licensed, too; see
  https://github.com/google/flatbuffers/pull/7073

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.0.6-2
- Fix extra newline in description

* Thu Jun 23 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.0.6-1
- Update to 2.0.6 (close RHBZ#2099837)

* Tue Jun 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.0.0-24
- Fix Python wheel versioning

* Tue Jun 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.0.0-23
- Work around error building tests on s390x

* Sat Jun 18 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 2.0.0-6
- Fix cmake invocation (fix RHBZ#2045385)
- Re-enable the tests
- Move the unversioned .so file link to the devel package
- Fix unowned %%{_libdir}/cmake/flatbuffers directory
- Move flatc to a new flatbuffers-compiler subpackage
- Fix the Python library subpackage: rename it to python3-flatbuffers, make it
  noarch, build it with pyproject-rpm-macros, add an import-only “smoke test”,
  and add a weak dependency on numpy
- Stop maintaining a flatbuffers.7 man page
- Update flatc.1 man page
- Add a -doc subpackage with samples (no reference manual for now)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.0-5
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.0-2
- Rebuilt for Python 3.10

* Mon May 17 2021 Benjamin Lowry <ben@ben.gmbh - 2.0.0-1
- flatbuffers 2.0.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 10 2020 Cristian Balint <cristian.balint@gmail.com> - 1.12.0-5
- Enable python module

* Sat Aug 01 2020 Benjamin lowry <ben@ben.gmbh> - 1.12.0-4
- Update to new cmake macros, fix build error

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 12 2020 Benjamin Lowry <ben@ben.gmbh> - 1.12.0-1
- Upgrade to 1.12.0, fix compilation on F32

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 15 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.11.0-1
- Update to 1.11.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.10.0-3
- Add explicit curdir on CMake invocation

* Thu Jan 10 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.10.0-2
- Fix generator (and generated tests) for gcc9 (ignore -Wclass-memaccess)

* Thu Oct 04 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.10.0-1
- Update to 1.10.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Apr 06 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.9.0-1
- Update to 1.9.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.8.0-3
- Fix build errors.

* Wed Nov 22 2017 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.8.0-2
- Update manpages for 1.8.0

* Wed Nov 22 2017 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.8.0-1
- Update to 1.8.0

* Thu Nov 2 2017 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.7.1-1
- Initial version

* Mon Mar 30 2015 Daniel Vrátil <dvratil@redhat.com> - 1.0.3-1
- Initial version (abandoned at #1207208)

## END: Generated by rpmautospec
