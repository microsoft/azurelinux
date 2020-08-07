Summary:        TCP/IP daemon wrapper package
Name:           tcp_wrappers
Version:        7.6
Release:        9%{?dist}
License:        BSD
Group:          System Environment/Networking
# URL doesn't work in the browser but can be downloaded with wget
URL:            ftp://ftp.porcupine.org/pub/security/index.html
Source0:        ftp://ftp.porcupine.org/pub/security/%{name}_%{version}.tar.gz
Source1:        ftp://ftp.porcupine.org/pub/security/tcp_wrappers_license
Patch0:         http://www.linuxfromscratch.org/patches/blfs/6.3/tcp_wrappers-7.6-shared_lib_plus_plus-1.patch
Requires:       finger
BuildRequires:  libnsl2-devel
Requires:       libnsl2

%description
The TCP Wrapper package provides daemon wrapper programs that report the name of the client requesting network services and the requested service.

%package devel
Summary:	The libraries and header files needed for tcp_wrappers development.
Requires: 	%{name} = %{version}-%{release}
Requires:	libnsl2-devel

%description devel
The libraries and header files needed for tcp_wrappers development.

%prep
%setup -qn %{name}_%{version}
%patch0 -p1

%build
sed -i -e "s,^extern char \*malloc();,/* & */," scaffold.c &&
sed -i 's/-O2/-O2 -DUSE_GETDOMAIN/g' Makefile &&
make REAL_DAEMON_DIR=%{_sbindir} STYLE=-DPROCESS_OPTIONS linux

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man{3,5,8}
mkdir -p %{buildroot}%{_includedir}
make DESTDIR=%{buildroot} install

cp %{SOURCE1} .

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-, root, root)
%license tcp_wrappers_license
%{_libdir}/*.so.*
%{_libdir}/*.a
%{_sbindir}/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%defattr(-, root, root)
%license tcp_wrappers_license
%{_libdir}/*.so
%{_includedir}/*.h

%changelog
* Mon Jun 01 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 7.6-9
- Adding a license reference.
* Fri Apr 17 2020 Nicolas Ontiveros <niontive@microsoft.com> 7.6-8
- Change libnsl to libnsl2.
* Tue Apr 07 2020 Paul Monson <paulmon@microsoft.com> 7.6-7
- Verified License. Verified URL.
* Thu Aug 08 2019 Mateusz Malisz <mamalisz@microsoft.com> 7.6-6
- Initial CBL-Mariner import from Photon (license: Apache2).
* Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 7.6-5
- Use libnsl
* Mon Sep 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 7.6-4
- Add finger to Requires
* Wed Aug 23 2017 Alexey Makhalov <amakhalov@vmware.com> 7.6-3
- Fix compilation issue for glibc-2.26
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.6-2
- GA - Bump release of all rpms
* Fri Aug 28 2015 Divya Thaluru <dthaluru@vmware.com> 7.6-1
- Initial version

