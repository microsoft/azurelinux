# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# Copyright Fedora Project Authors.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
%global rocm_release 6.4
%global rocm_patch 2
%global rocm_version %{rocm_release}.%{rocm_patch}
%global upstreamname amdsmi

# Downloads its own googletest
# Testing also depends on having AMD hardware cpu and/or gpu installed.
# Not suitable for a general check
#
# Non root result for gfx1100 and this kernel 6.13.0-0.rc0.20241126git7eef7e306d3c.10.fc42.x86_64
# 25 pass, 5 fail
# No oops
%bcond_with test
%if %{with test}
%global build_test ON
%else
%global build_test OFF
%endif

Name:       amdsmi
Version:    %{rocm_version}
Release: 8%{?dist}
Summary:    AMD System Management Interface

License:    NCSA AND MIT AND BSD-3-Clause
URL:        https://github.com/RadeonOpenCompute/%{upstreamname}
Source0:    %{url}/archive/rocm-%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz
# esmi_ib_library is not suitable for packaging
# https://github.com/amd/esmi_ib_library/issues/13
# This tag was choosen by the amdsmi project because 4.0+ introduced variables not
# found in the upstream kernel.
%global esmi_ver 4.1.2
Source1:    https://github.com/amd/esmi_ib_library/archive/refs/tags/esmi_pkg_ver-%{esmi_ver}.tar.gz
Patch2:     0001-Include-cstdint-for-gcc-15.patch
Patch3:     0002-option-use-system-gtest.patch
Patch4:     0003-test-client-includes-for-gcc-15.patch
# https://github.com/ROCm/amdsmi/pull/165
Patch:      0001-Fix-compilation-with-libdrm-2.4.130.patch

ExclusiveArch: x86_64

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: kernel-devel
BuildRequires: libdrm-devel
BuildRequires: python3-devel

%if %{with test}
%if 0%{?suse_version}
BuildRequires: gtest
%else
BuildRequires: gtest-devel
%endif
%endif

Requires:      python3dist(pyyaml)

# University of Illinois/NCSA Open Source License
Provides: bundled(esmi_ib_library) = %{esmi_ver}

%description
The AMD System Management Interface Library, or AMD SMI library, is a C
library for Linux that provides a user space interface for applications
to monitor and control AMD devices.

%package devel
Summary: Libraries and headers for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}

%if %{with test}
%package test
Summary:        Tests for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libdrm-devel

%description test
%{summary}
%endif

%prep
%autosetup -n %{upstreamname}-rocm-%{version} -p1
tar xf %{SOURCE1}
mv esmi_ib_library-* esmi_ib_library
# So we can pick up this license
mv esmi_ib_library/License.txt esmi_ib_library_License.txt 
# The esmi version check uses git tags, but we use tar's without git files.
# Just inject in the tag that we've pulled into the version check:
sed -i 's/NOT latest_esmi_tag/NOT "esmi_pkg_ver-%{esmi_ver}"/' CMakeLists.txt

# W: spurious-executable-perm /usr/share/doc/amdsmi/README.md
chmod a-x README.md

# /usr/libexec/amdsmi_cli/BDF.py:126: SyntaxWarning: invalid escape sequence '\.'
#   bdf_regex = "(?:[0-6]?[0-9a-fA-F]{1,4}:)?[0-2]?[0-9a-fA-F]{1,2}:[0-9a-fA-F]{1,2}\.[0-7]"
sed -i -e 's@bdf_regex = "@bdf_regex = r"@' amdsmi_cli/BDF.py

# Fix script shebang
sed -i -e 's@env python3@python3@' amdsmi_cli/*.py

# Install local gtests in same dir as tests
sed -i -e 's@${CPACK_PACKAGING_INSTALL_PREFIX}/lib@${SHARE_INSTALL_PREFIX}/tests@' tests/amd_smi_test/CMakeLists.txt

%build
%cmake \
    -DBUILD_KERNEL_ASM_DIR=/usr/include/asm \
    -DCMAKE_SKIP_INSTALL_RPATH=TRUE \
%if %{with test}
    -DUSE_SYSTEM_GTEST=On \
%endif
    -DBUILD_TESTS=%build_test

%cmake_build

%install
%cmake_install

mkdir -p %{buildroot}/%{python3_sitelib}
if [ -d %{buildroot}/usr/share/amd_smi/amdsmi ]; then
    mv %{buildroot}/usr/share/amd_smi/amdsmi %{buildroot}/%{python3_sitelib}
    mv %{buildroot}/usr/share/amd_smi/pyproject.toml %{buildroot}/%{python3_sitelib}/amdsmi/
else
    mv %{buildroot}/usr/share/amdsmi %{buildroot}/%{python3_sitelib}
    mv %{buildroot}/usr/share/pyproject.toml %{buildroot}/%{python3_sitelib}/amdsmi/
fi

# Remove some things
rm -rf %{buildroot}/usr/share/example
rm -rf %{buildroot}/usr/share/amd_smi/example
rm -rf %{buildroot}/usr/share/doc/amd_smi-asan/LICENSE.txt
rm -f %{buildroot}/usr/share/doc/amd_smi/LICENSE.txt
rm -f %{buildroot}/usr/share/doc/amd_smi/README.md
rm -rf %{buildroot}/usr/share/doc/amd_smi/copyright
rm -f %{buildroot}%{_datadir}/_version.py
rm -f %{buildroot}%{_datadir}/amd_smi/_version.py
rm -f %{buildroot}%{_datadir}/setup.py
rm -f %{buildroot}%{_datadir}/amd_smi/setup.py

# W: unstripped-binary-or-object /usr/lib/python3.13/site-packages/amdsmi/libamd_smi.so
# Does an explict open, so can not just rm it
# let's just strip it
strip %{buildroot}/%{python3_sitelib}/amdsmi/*.so
# E: non-executable-script .../amdsmi_cli/amdsmi_cli_exceptions.py 644 /usr/bin/env python3
chmod a+x %{buildroot}/%{_libexecdir}/amdsmi_cli/amdsmi_*.py

%if %{with test}
# put the test files in a reasonable place
mkdir %{buildroot}%{_datadir}/amdsmi
mv %{buildroot}%{_datadir}/tests %{buildroot}%{_datadir}/amdsmi/.
%endif

%if 0%{?suse_version}
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%endif

%files
%doc README.md
%license LICENSE
%license esmi_ib_library_License.txt 
%{_libdir}/libamd_smi.so.*
%{_libdir}/libgoamdsmi_shim64.so.*
%{_bindir}/amd-smi
%{_libexecdir}/amdsmi_cli
%{python3_sitelib}/amdsmi

%files devel
%dir %{_includedir}/amd_smi
%dir %{_libdir}/cmake/amd_smi
%{_includedir}/amd_smi/*.h
%{_includedir}/*.h
%{_libdir}/libamd_smi.so
%{_libdir}/libgoamdsmi_shim64.so
%{_libdir}/cmake/amd_smi/*.cmake

%if %{with test}
%files test
%{_datadir}/amdsmi
%{_datadir}/amdsmi/tests
%endif

%changelog
* Fri Mar 13 2026 Tom Rix <Tom.Rix@amd.com> - 6.4.2-7
- Fix break from kernel update

* Wed Aug 27 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-6
- Add Fedora copyright

* Mon Aug 25 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-5
- Simplify file removal

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 6.4.2-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Aug 13 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-3
- Build -test on SUSE

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.2-1
- Update to 6.4.2

* Wed Jun 18 2025 Tim Flink <tflink@fedoraproject.org> - 6.4.1-4
- update so that test subpackage builds cleanly in mock and runs outside of build environment

* Mon Jun 2 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-3
- handle movement of copyright file on suse

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 6.4.1-2
- Rebuilt for Python 3.14

* Thu May 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.1-1
- Update to 6.4.1

* Wed Apr 16 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.0-1
- Update to 6.4.0

* Tue Mar 11 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.3-3
- Adjust install of python for fedora

* Thu Feb 27 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.3-2
- Install amd_smi-config.cmake

* Wed Feb 19 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.3-1
- Update to 6.3.3

* Wed Jan 29 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.2-1
- Update to 6.3.2

* Fri Jan 17 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-6
- Cleanup for suse

* Thu Jan 16 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-5
- Improve empty return patch
- Fix shebangs

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 8 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-3
- Include cstdint for gcc 15

* Tue Dec 31 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.1-2
- Require pyyaml

* Sun Dec 22 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.1-1
- Update to 6.3.1

* Sat Dec 7 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3

* Sun Nov 3 2024 Tom Rix <Tom.Rix@amd.com> - 6.2.1-1
- Stub for tumbleweed


