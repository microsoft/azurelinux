# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _hardened_build 1
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name: fstrm
Summary: Frame Streams implementation in C
Version: 0.6.1
Release: 13%{?dist}
License: MIT AND NTP
URL: https://github.com/farsightsec/fstrm
Source0: https://dl.farsightsecurity.com/dist/%{name}/%{name}-%{version}.tar.gz
# Patches to libmy library
# https://github.com/farsightsec/libmy/pull/4
Patch1: fstrm-0.6.1-Fix-deadcode-and-check-return-code.patch
Patch2: fstrm-0.6.1-Invalid-dereference.patch
Patch3: fstrm-0.6.1-Possible-resource-leak-fix.patch
Patch4: fstrm-0.6.1-Fix-CLANG_WARNING.patch
BuildRequires: autoconf automake libtool
BuildRequires: libevent-devel
# Upstream repository without a single release
# https://github.com/farsightsec/libmy
# Always included as sources copy in farsightsec projects
Provides: bundled(libmy)

%description
Frame Streams is a light weight, binary clean protocol that allows for the
transport of arbitrarily encoded data payload sequences with minimal framing
overhead -- just four bytes per data frame. Frame Streams does not specify
an encoding format for data frames and can be used with any data serialization
format that produces byte sequences, such as Protocol Buffers, XML, JSON,
MessagePack, YAML, etc.

%package utils
Summary: Frame Streams (fstrm) utilities
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
Frame Streams is a light weight, binary clean protocol that allows for the
transport of arbitrarily encoded data payload sequences with minimal framing
overhead -- just four bytes per data frame. Frame Streams does not specify
an encoding format for data frames and can be used with any data serialization
format that produces byte sequences, such as Protocol Buffers, XML, JSON,
MessagePack, YAML, etc.

The fstrm-utils package contains command line utilities.

%package devel
Summary: Development Files for fstrm library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The fstrm-devel package contains header files required to build an application
using fstrm library.

%package doc
Summary: API documentation for fstrm library
BuildArch: noarch
BuildRequires: doxygen
BuildRequires: make
Requires: %{name} = %{version}-%{release}

%description doc
The fstrm-doc package contains Doxygen generated API documentation for
fstrm library.

%prep
%autosetup -p1
# regenerated build scripts to:
# - remove RPATHs
# - allow dynamic linking and execution of 'make check'
autoreconf -fi

%build
%configure --disable-static
%make_build
make html

%install
# install the library
%make_install
rm %{buildroot}%{_libdir}/libfstrm.la

# install documentation
mkdir -p %{buildroot}%{_pkgdocdir}/
cp -ar html %{buildroot}%{_pkgdocdir}/html

%check
make check

%if 0%{?fedora} || 0%{?rhel} > 7
# https://fedoraproject.org/wiki/Changes/Removing_ldconfig_scriptlets
%else
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%endif

%files
%doc COPYRIGHT LICENSE
%exclude %{_pkgdocdir}/html
%{_libdir}/libfstrm.so.*

%files utils
%{_bindir}/fstrm_capture
%{_bindir}/fstrm_dump
%{_bindir}/fstrm_replay
%{_mandir}/man1/fstrm_*

%files devel
%doc README.md
%{_includedir}/fstrm.h
%{_includedir}/fstrm/
%{_libdir}/pkgconfig/libfstrm.pc
%{_libdir}/libfstrm.so

%files doc
%doc %{_pkgdocdir}/html

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Petr Menšík <pemensik@redhat.com> - 0.6.1-7
- Expand licenses to SPDX identifiers

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 09 2021 Petr Menšík <pemensik@redhat.com> - 0.6.1-2
- Apply coverity fixes also to bundled libmy

* Thu Apr 08 2021 Petr Menšík <pemensik@redhat.com> - 0.6.1-1
- Update to 0.6.1 (#1946415)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 15 2020 Petr Menšík <pemensik@redhat.com> - 0.6.0-3
- Move command line tools to utils subpackage

* Tue Sep 15 2020 Petr Menšík <pemensik@redhat.com> - 0.6.0-2
- Rebuilt for libevent rebase

* Tue Aug 11 2020 Michał Kępień <michal@isc.org> - 0.6.0-1
- Update to new upstream version 0.6.0

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 10 2019 Tomas Krizek <tomas.krizek@nic.cz> - 0.5.0-1
- Update to new upstream version 0.5.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 17 2018 Tomas Krizek <tomas.krizek@nic.cz> - 0.4.0-1
- Update to new upstream version 0.4.0 BZ#1577420

* Thu Apr 05 2018 Tomas Krizek <tomas.krizek@nic.cz> - 0.3.2-1
- Update to new upstream version 0.3.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct 23 2016 Jan Vcelak <jvcelak@fedoraproject.org> - 0.3.0-1
- new upstream release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec 15 2014 Jan Vcelak <jvcelak@fedoraproject.org> 0.2.0-1
- initial package
