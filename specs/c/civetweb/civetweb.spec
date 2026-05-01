# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


#%%global dev rc1

Name:           civetweb
Summary:        Embedded C/C++ web server
Version:        1.16
Release:        10%{?dev:%{dev}}%{?dist}
License:        MIT
Url:            https://github.com/civetweb/civetweb
Source:         https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch:		0001-CMakeLists.txt.patch
Patch:		0002-src-civetweb.c.patch
Patch:		0003-src-civetweb.c.patch
BuildRequires:  cmake make gcc-c++

%description
Civetweb is an easy to use, powerful, C (C/C++) embeddable web server
with optional CGI, SSL and Lua support.

CivetWeb can be used by developers as a library, to add web server
functionality to an existing application. It can also be used by end
users as a stand-alone web server running on a Windows or Linux PC.
It is available as single executable, no installation is required.

%package devel
Summary:        Civetweb Client Library C and C++ header files
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Civetweb shared libs and associated header files

%prep
%autosetup -p1

%build
%{cmake} . \
    -G "Unix Makefiles" \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DBUILD_CONFIG=rpmbuild \
    -DCIVETWEB_ENABLE_CXX:BOOL=ON \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DCIVETWEB_BUILD_TESTING:BOOL=OFF

export GCC_COLORS=
export VERBOSE=1
%cmake_build %{?_smp_mflags}

%install
%cmake_install
mkdir -p %{buildroot}%{_docdir}/civetweb

%files
%{_bindir}/civetweb
%{_libdir}/libcivetweb.so.*
%{_libdir}/libcivetweb-cpp.so.*
%license LICENSE.md
%doc README.md RELEASE_NOTES.md SECURITY.md

%files devel
%{_includedir}/*.h
%{_libdir}/libcivetweb.so
%{_libdir}/libcivetweb-cpp.so
%{_libdir}/cmake/civetweb/*
%{_datadir}/pkgconfig/*

%changelog
* Mon Sep 29 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 1.16-10
- civetweb 1.16, rhbz 2400162-2400166

* Wed Sep 3 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 1.16-9
- civetweb 1.16

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 1.16-7
- civetweb 1.16, rhbz#2380496

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 11 2023 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 1.16-1
- civetweb 1.16 GA

* Tue Mar 7 2023 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 1.15-1
- civetweb 1.15 GA, initial build

