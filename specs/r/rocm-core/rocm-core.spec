# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?suse_version}
# 15.6
# rocm-core.x86_64: E: shlib-policy-name-error (Badness: 10000) librocm-core1
# Your package contains a single shared library but is not named after its SONAME.
%global core_name librocm-core1
%else
%global core_name rocm-core
%endif

%global upstreamname rocm-core
%global rocm_release 6.4
%global rocm_patch 4
%global rocm_version %{rocm_release}.%{rocm_patch}

Name:           %{core_name}
Version:        %{rocm_version}
Release: 2%{?dist}
Summary:        A utility to get the ROCm release version
Url:            https://github.com/ROCm/%{upstreamname}
License:        MIT

Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++

Provides:       rocm-core = %{version}-%{release}

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
%{summary}

%if 0%{?suse_version}
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%endif

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       rocm-core-devel = %{version}-%{release}

%description devel
%{summary}

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

%build
%cmake -DROCM_VERSION=%{rocm_version}
%cmake_build

%install
%cmake_install

rm -rf %{buildroot}/%{_prefix}/.info
rm -rf %{buildroot}/%{_libdir}/rocmmod
rm -rf %{buildroot}/%{_docdir}/*/LICENSE.txt
rm -rf %{buildroot}/%{_libexecdir}/%{name}

mv  %{buildroot}/%{_includedir}/rocm-core/*.h %{buildroot}/%{_includedir}/
rm -rf %{buildroot}/%{_includedir}/rocm-core

find %{buildroot} -type f -name 'runpath_to_rpath.py' -exec rm {} \;

%files
%license copyright
%{_libdir}/librocm-core.so.*

%files devel
%dir %{_libdir}/cmake/rocm-core
%{_includedir}/*.h
%{_libdir}/librocm-core.so
%{_libdir}/cmake/rocm-core/*.cmake

%changelog
* Wed Oct 8 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.4-1
- Update to 6.4.4

* Thu Aug 7 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.3-1
- Update to 6.4.3

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.2-1
- Update to 6.4.2

* Thu May 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.1-1
- Update to 6.4.1

* Wed Apr 16 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.0-1
- Update to 6.4.0

* Wed Feb 19 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.3-1
- Update to 6.3.3

* Mon Feb 10 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.2-2
- Fix SLE 15.6

* Wed Jan 29 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.2-1
- Update to 6.3.2

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 26 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.1-1
- Update to 6.3.1

* Tue Dec 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3

