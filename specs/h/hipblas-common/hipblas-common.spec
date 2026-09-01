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

%bcond_with gitcommit
%if %{with gitcommit}
%global commit0 2584e35062ad9c2edb68d93c464cf157bc57e3b0
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20250926
%endif

%global upstreamname hipBLAS-common
%global rocm_release 7.1
%global rocm_patch 0
%global rocm_version %{rocm_release}.%{rocm_patch}

%bcond_with compat
%if %{with compat}
%global pkg_libdir lib
%global pkg_prefix %{_prefix}/lib64/rocm/rocm-%{rocm_release}
%global pkg_suffix -%{rocm_release}
%global pkg_module rocm%{pkg_suffix}
%else
%global pkg_libdir %{_lib}
%global pkg_prefix %{_prefix}
%global pkg_suffix %{nil}
%global pkg_module default
%endif

Name:           hipblas-common%{pkg_suffix}
%if %{with gitcommit}
Version:        git%{date0}.%{shortcommit0}
Release:        2%{?dist}
%else
Version:        %{rocm_version}
Release:        3%{?dist}
%endif
Summary:        Common files shared by hipBLAS and hipBLASLt
License:        MIT

%if %{with gitcommit}
Url:            https://github.com/ROCm/rocm-libraries
Source0:        %{url}/archive/%{commit0}/rocm-libraries-%{shortcommit0}.tar.gz
%else
Url:            https://github.com/ROCm/%{upstreamname}
Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  rocm-cmake%{pkg_suffix}

# Only headers, cmake infra
BuildArch: noarch
# Only x86_64 works right now:
ExclusiveArch:  x86_64

# Problem on SUSE, nothing really to compile so turn jobs off
%global _smp_mflags %{nil}

%description
%summary

%package devel
Summary:        Libraries and headers for %{name}
Provides:       %{name}-static = %{version}-%{release}

%description devel
%{summary}

%prep
%if %{with gitcommit}
%setup -q -n rocm-libraries-%{commit0}
cd projects/hipblas-common
%else
%autosetup -p1 -n %{upstreamname}-rocm-%{version}
%endif

%build
%if %{with gitcommit}
cd projects/hipblas-common
%endif

%cmake \
    -DCMAKE_INSTALL_LIBDIR=share \
    -DCMAKE_INSTALL_PREFIX=%{pkg_prefix}

%cmake_build

%install
%if %{with gitcommit}
cd projects/hipblas-common
%endif

%cmake_install

rm -f %{buildroot}%{pkg_prefix}/share/doc/hipblas-common/LICENSE.md

%files devel
%if %{with gitcommit}
%license projects/hipblas-common/LICENSE.md
%else
%license LICENSE.md
%endif

%{pkg_prefix}/include/hipblas-common/
%{pkg_prefix}/share/cmake/hipblas-common/

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Dec 22 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-2
- Add --with compat

* Fri Oct 31 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-1
- Update to 7.1.0

* Fri Oct 10 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.0-2
- Remove stray backlash

* Fri Sep 19 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.0-1
- Update to 7.0.1

* Wed Aug 27 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-4
- Add Fedora copyright

* Mon Aug 25 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-3
- Simplify file removal

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Apr 19 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Initial package

