Name: libiscsi
Summary: iSCSI client library
Version: 1.19.0
Release: 1%{?dist}
License: LGPL-2.1-or-later
URL: https://github.com/sahlberg/%{name}
%global commit 7577ec589cb34900f83a95797ef473f79603ad61
#Source: https://github.com/sahlberg/libiscsi/archive/{version}.tar.gz
#Source: https://github.com/sahlberg/libiscsi/archive/%{commit}.tar.gz#/%{name}-%{version}.tar.gz
Source: https://github.com/sahlberg/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires: make
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: popt-devel
BuildRequires: CUnit-devel
BuildRequires: libgcrypt-devel
%ifnarch %{arm}
BuildRequires: rdma-core-devel
%endif

%description
libiscsi is a library for attaching to iSCSI resources across
a network.


#######################################################################

# Conflict with iscsi-initiator-utils.

%global libiscsi_includedir %{_includedir}/iscsi
%global libiscsi_libdir %{_libdir}/iscsi

%prep
%autosetup -n libiscsi-%{commit}
%autopatch -p1

%build
sh autogen.sh
%configure --libdir=%{libiscsi_libdir} --disable-werror
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install pkgconfigdir=%{_libdir}/pkgconfig %{?_smp_mflags}
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo %{libiscsi_libdir} > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf
rm $RPM_BUILD_ROOT/%{libiscsi_libdir}/libiscsi.a
rm $RPM_BUILD_ROOT/%{libiscsi_libdir}/libiscsi.la


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING LICENCE-LGPL-2.1.txt
%doc README.md TODO
%dir %{libiscsi_libdir}
%{libiscsi_libdir}/libiscsi.so.9*
%config /etc/ld.so.conf.d/*

%package utils
Summary: iSCSI Client Utilities
License: GPL-2.0-or-later
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
The libiscsi-utils package provides a set of assorted utilities to connect
to iSCSI servers without having to set up the Linux iSCSI initiator.

%files utils
%license LICENCE-GPL-2.txt
%{_bindir}/iscsi-ls
%{_bindir}/iscsi-inq
%{_bindir}/iscsi-readcapacity16
%{_bindir}/iscsi-swp
%{_bindir}/iscsi-perf
%{_bindir}/iscsi-test-cu
%{_bindir}/iscsi-pr
%{_bindir}/iscsi-discard
%{_bindir}/iscsi-md5sum
%{_mandir}/man1/iscsi-ls.1.gz
%{_mandir}/man1/iscsi-inq.1.gz
%{_mandir}/man1/iscsi-swp.1.gz
%{_mandir}/man1/iscsi-test-cu.1.gz

%package devel
Summary: iSCSI client development libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The libiscsi-devel package includes the header files for libiscsi.

%files devel
%dir %{libiscsi_includedir}
%{libiscsi_includedir}/iscsi.h
%{libiscsi_includedir}/scsi-lowlevel.h
%{libiscsi_libdir}/libiscsi.so
%{_libdir}/pkgconfig/libiscsi.pc

%changelog
* Fri Jan 19 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 1.19.0-1
- Upgrade to 1.19 from Fedora

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.18.0-11
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.18.0-10
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- License verified.

* Mon Dec  2 2019 Daniel P. Berrangé <berrange@redhat.com> - 1.18.0-9
- Disable RDMA on arm 32-bit (rhbz #1778517)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 30 2018 Paolo Bonzini <pbonzini@redhat.com> - 1.18.0-6
- Backport upstream fix for IPv6 connections
- Backport upstream fix for issues reported by coverity

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 30 2018 Cole Robinson <crobinso@redhat.com> - 1.18.0-4
- Fix build with newer rdma-core

* Fri Mar 23 2018 Cole Robinson <crobinso@redhat.com> - 1.18.0-3
- Fix rdma deps and don't restrict archs
- Add --disable-werror to fix gcc8 build (bz #1556044)
- Spec file cleanups (bz #1483290)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 03 2017 Paolo Bonzini <pbonzini@redhat.com> - 1.18.0-1
- Rebased to version 1.18.0
- Added patch to fix gcc7 warnings

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 26 2015 Neal Gompa <ngompa13@gmail.com> - 1.15.0-1
- Rebased to version 1.15.0
- Removed patch 20 as it has been upstreamed
- Disabled patch 12 as need for revised one is in question
- Updated patch 13 to current tree
- New tool iscsi-perf

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 12 2014 Paolo Bonzini <pbonzini@redhat.com> - 1.11.0-1
- Rebased to version 1.11.0
- Most patches removed
- New tool iscsi-swp + manpages

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Tomáš Mráz <tmraz@redhat.com> - 1.9.0-5
- Rebuild for new libgcrypt

* Mon Aug 26 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.9.0-4
- Cleaned up patches 18/19 to match upstream more closely

* Mon Aug 26 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.9.0-3
- Improved patch 18 to cover write side too

* Mon Aug 26 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.9.0-2
- Add patch 18 to fix QEMU's scsi-generic mode

* Fri Aug 2 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.9.0-1
- Rebase to 1.9.0
- Cherry-pick selected patches from upstream

* Mon Jul 1 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-6
- Add patch 5 to silence strict aliasing warnings

* Wed Jun 26 2013 Andy Grover <agrover@redhat.com> - 1.7.0-5
- Add patch 4 to enable installing of iscsi-test binary

* Fri May 3 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-4
- Add patch 2 for FIPS mode
- Add patch 3 to avoid segmentation fault on iscsi-tools

* Thu Mar 7 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-3
- Correct license for libiscsi-utils, prefer %%global to %%define
- Add Requires
- Remove percent-clean section

* Fri Feb 22 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-2
- Use percent-config for ld.so.conf.d file.

* Fri Feb 22 2013 Paolo Bonzini <pbonzini@redhat.com> - 1.7.0-1
- Initial version (bug 914752)
