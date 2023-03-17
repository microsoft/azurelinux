%global _hardened_build 1
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name: fstrm
Summary: Frame Streams implementation in C
Version: 0.6.1
Release: 1%{?dist}
License: MIT
URL: https://github.com/farsightsec/fstrm
Source0: https://dl.farsightsecurity.com/dist/fstrm/fstrm-%{version}.tar.gz
BuildRequires: autoconf automake libtool
BuildRequires: libevent-devel

%description
Frame Streams is a light weight, binary clean protocol that allows for the
transport of arbitrarily encoded data payload sequences with minimal framing
overhead -- just four bytes per data frame. Frame Streams does not specify
an encoding format for data frames and can be used with any data serialization
format that produces byte sequences, such as Protocol Buffers, XML, JSON,
MessagePack, YAML, etc.

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
Requires: %{name} = %{version}-%{release}

%description doc
The fstrm-doc package contains Doxygen generated API documentation for
fstrm library.

%prep
%setup -q
# regenerated build scripts to:
# - remove RPATHs
# - allow dynamic linking and execution of 'make check'
autoreconf -fi

%build
%configure --disable-static --prefix=/tmp/
make %{?_smp_mflags}
make html

%install
# install the library
make install DESTDIR=%{buildroot}
rm %{buildroot}%{_libdir}/libfstrm.la

# install documentation
mkdir -p %{buildroot}%{_pkgdocdir}/
cp -ar html %{buildroot}%{_pkgdocdir}/html

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%define _unpackaged_files_terminate_build 0

%files
%doc COPYRIGHT LICENSE
%exclude %{_pkgdocdir}/html
%{_libdir}/libfstrm.so.*

%files devel
%doc README.md
%{_bindir}/fstrm_capture
%{_bindir}/fstrm_dump
%{_includedir}/fstrm.h
%{_includedir}/fstrm/
%{_libdir}/pkgconfig/libfstrm.pc
%{_libdir}/libfstrm.so

%files doc
%doc %{_pkgdocdir}/html

%changelog
* Thu Feb 23 2023 Andy Zaugg <azaugg@linkedin.com> - 0.6.1-1
- Initial CBL-Mariner import from CentOS 8 (license: MIT).
- License verified

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
