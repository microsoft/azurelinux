Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:        Hardware Platform Interface library and tools
Name:           openhpi
Version:        3.8.0
Release:        11%{?dist}
License:        BSD
URL:            http://www.openhpi.org
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# convert from initscript to systemd unit
Patch0:         %{name}-3.4.0-systemd.patch
Patch1:         %{name}-3.6.1-ssl.patch
Patch2:         %{name}-3.7.0-multilib.patch
Patch3:         %{name}-3.8.0-manpage-scan.patch
Patch4:         %{name}-3.8.0-ipv6-ipmidirect.patch
Patch5:         %{name}-3.8.0-link-libopenhpi.patch
Patch6:         %{name}-3.8.0-new_ssl.patch
BuildRequires:  gcc-c++
BuildRequires:  libsysfs-devel
BuildRequires:  net-snmp-devel
BuildRequires:  OpenIPMI-devel
BuildRequires:  glib2-devel
BuildRequires:  libtool-ltdl-devel
BuildRequires:  openssl-devel
BuildRequires:  ncurses-devel
BuildRequires:  libxml2-devel
BuildRequires:  docbook-utils
BuildRequires:  libuuid-devel
BuildRequires:  librabbitmq-devel
BuildRequires:  json-c-devel
BuildRequires:  libcurl-devel
BuildRequires:  systemd
BuildRequires:  autoconf automake libtool
BuildRequires:  libgcrypt-devel
BuildRequires:  net-snmp
Requires(post):         systemd
Requires(preun):        systemd
Requires(postun):       systemd
Requires: %{name}-libs%{?_isa} = %{version}-%{release}


%description
OpenHPI is an open source project created with the intent of providing an
implementation of the SA Forum's Hardware Platform Interface (HPI). HPI
provides an abstracted interface to managing computer hardware, typically for
chassis and rack based servers. HPI includes resource modeling; access to and
control over sensor, control, watchdog, and inventory data associated with
resources; abstracted System Event Log interfaces; hardware events and alerts;
and a managed hot swap interface.

OpenHPI provides a modular mechanism for adding new hardware and device support
easily. Many plug-ins exist in the OpenHPI source tree to provide access to
various types of hardware. This includes, but is not limited to, IPMI based
servers, Blade Center, and machines which export data via sysfs.


%package libs
Summary: The system libraries for the OpenHPI project

%description libs
The system libraries for the OpenHPI project.


%package devel
Summary: The development environment for the OpenHPI project
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description devel
The development libraries and header files for the OpenHPI project.


%prep
%autosetup -p1

autoreconf -vif

# fix permissions
chmod a-x plugins/simulator/*.[ch]
chmod a-x clients/hpipower.c

# Fix ownership of config files and dirs for building/running tests as root
# Due to security check the daemon breaks with error if the config file
# does not belong to the current user.
# https://bugzilla.redhat.com/show_bug.cgi?id=1267928
if [ $UID -eq 0 ]; then
    find . -name openhpi.conf -exec chown root:root {} \;
    find . -name openhpi.conf -execdir chown root:root . \;
fi


%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure --disable-static --with-systemdsystemunitdir=%{_unitdir} --docdir=%{_docdir}/%{name}-%{version}

# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p -m1755 $RPM_BUILD_ROOT%{_var}/lib/%{name}
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT/%{_libdir}/%{name}/*.la

cp plugins/dynamic_simulator/README $RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version}/README-dynamic_simulator

%check
make check


%post
%systemd_post openhpid.service

%preun
%systemd_preun openhpid.service

%postun
%systemd_postun_with_restart openhpid.service


%files
%license %{_docdir}/%{name}-%{version}/COPYING
%doc %{_docdir}/%{name}-%{version}/ChangeLog
%doc %{_docdir}/%{name}-%{version}/README*
%doc openhpi.conf.example plugins/*/*.pdf
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}client.conf
%config(noreplace) %{_sysconfdir}/%{name}/simulation.data
%{_unitdir}/openhpid.service
%attr(1755,root,root) %{_var}/lib/%{name}
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/%{name}
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%files libs
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/%{name}
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue Aug 10 2021 Thomas Crain <thcrain@microsoft.com> - 3.8.0-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add upstream patch to fix openssl 1.1 incompatibility

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 05 2018 Than Ngo <than@redhat.com> - 3.8.0-7
- add ipv6 support for ipmidirect
- fix #1654725, testcases failed due to undefined symbol: saHpiSessionOpen

* Tue Aug 07 2018 Than Ngo <than@redhat.com> - 3.8.0-6
- install README-dynamic_simulator

* Tue Aug 07 2018 Than Ngo <than@redhat.com> - 3.8.0-5
- fixed bz#1612210, manpage scan issues

* Tue Jul 24 2018 Adam Williamson <awilliam@redhat.com> - 3.8.0-4
- Rebuild for new net-snmp

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Than Ngo <than@redhat.com> - 3.8.0-2
- fix file list in docdir 

* Tue Mar 13 2018 Dan Horák <dan[at]danny.cz> - 3.8.0-1
- updated to 3.8.0

* Tue Mar 06 2018 Björn Esser <besser82@fedoraproject.org> - 3.7.0-5
- Rebuilt for libjson-c.so.4 (json-c v0.13.1)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Than Ngo <than@redhat.com> - 3.7.0-3
- fixed multilib issue
- enable file encryption (missing hpicrypt)
- add BR on net-snmp in order to fix the undefined reference issue

* Sun Dec 10 2017 Björn Esser <besser82@fedoraproject.org> - 3.7.0-2
- Rebuilt for libjson-c.so.3

* Wed Nov 01 2017 Dan Horák <dan[at]danny.cz> - 3.7.0-1
- updated to 3.7.0
- enabled ov_rest plugin

* Thu Aug 03 2017 Than Ngo <than@redhat.com> - 3.6.1-8
- Resolves bz#1267928, the testsuite failure when build as root

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 21 2017 Than Ngo <than@redhat.com> - 3.6.1-5
- FTBFS for gcc 7
- fixed build with openssl-1.1.x
- use %%autosetup

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Rafael Fonseca <rdossant@redhat.com> - 3.6.1-3
- Fix #1414802 - double free or corruption on sysfs plugin.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 07 2015 Rafael Fonseca <rdossant@redhat.com> - 3.6.1-1
- update to 3.6.1

* Fri Aug 28 2015 Rafael Fonseca <rdossant@redhat.com> - 3.6.0-1
- Update to upstream version 3.6.0
- Mark COPYING as %%license
- Add ChangeLog to %%doc

* Tue Jul 07 2015 Rafael Fonseca <rdossant@redhat.com> - 3.4.0-5
- fix missing header (#1239746)

* Thu Jun 25 2015 Rafael Fonseca <rdossant@redhat.com> - 3.4.0-4
- fix /var/lib/openhpi permissions (#1233521)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.4.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 25 2014 Dan Horák <dan[at]danny.cz> - 3.4.0-1
- update to 3.4.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 23 2013 Dan Horák <dan[at]danny.cz> - 3.2.1-4
- enable hardened build (#955180)
- backport IPv6 support for OA SOAP plugin

* Tue Aug 20 2013 Dan Horák <dan[at]danny.cz> - 3.2.1-3
- fix build with unversioned docdir (#992402)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Dan Horák <dan[at]danny.cz> - 3.2.1-1
- update to 3.2.1
- switch to systemd macros

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Dan Horák <dan[at]danny.cz> - 3.2.0-1
- update to 3.2.0

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 Dan Horák <dan[at]danny.cz> - 3.0.0-1
- update to 3.0.0
- convert from initscript to systemd unit

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 11 2011 Dan Horák <dan[at]danny.cz> - 2.17.0-1
- update to 2.17.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  8 2010 Dan Horák <dan[at]danny.cz> - 2.15.0-1
- update to 2.15.0

* Thu Jul  8 2010 Dan Horák <dan[at]danny.cz> - 2.14.1-4
- moved license text into -libs subpackage

* Wed Feb 24 2010 Dan Horák <dan[at]danny.cz> - 2.14.1-3
- update initscript (#521648, #521830)

* Fri Jan 15 2010 Dan Horák <dan[at]danny.cz> - 2.14.1-2
- added fix for inconsistent SaHpi.h

* Wed Nov 25 2009 Dan Horák <dan[at]danny.cz> - 2.14.1-1
- updated to bug fix release 2.14.1

* Fri Oct  9 2009 Dan Horák <dan[at]danny.cz> - 2.14.0-6
- rebuilt with net-snmp 5.5

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.14.0-5
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Dan Horak <dan[at]danny.cz> - 2.14.0-3
- add BR: libuuid-devel

* Fri Apr 17 2009 Dan Horak <dan[at]danny.cz> - 2.14.0-2
- use upstream default config
- libtoolize/autoreconf is not needed

* Fri Apr 17 2009 Dan Horak <dan[at]danny.cz> - 2.14.0-1
- update to 2.14.0

* Wed Feb 25 2009 Dan Horak <dan[at]danny.cz> - 2.13.3-2
- fix ppc/ppc64 builds

* Wed Feb 25 2009 Dan Horak <dan[at]danny.cz> - 2.13.3-1
- update to 2.13.3

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 2.13.1-3
- rebuild with new openssl

* Tue Nov 25 2008 Dan Horak <dan[at]danny.cz> - 2.13.1-2
- shorten Summary

* Thu Nov 20 2008 Dan Horak <dan[at]danny.cz> - 2.13.1-1
- update to 2.13.1

* Mon Nov 17 2008 Dan Horak <dan[at]danny.cz> - 2.12.0-2
- rebuild for new libtool

* Sat Jul 26 2008 Dan Horak <dan[at]danny.cz> - 2.12.0-1
- update to 2.12.0

* Thu Jun 26 2008 Dan Horak <dan[at]danny.cz> - 2.11.3-1
- update to 2.11.3

* Fri Apr 18 2008 Dan Horak <dan[at]danny.cz> - 2.10.2-2
- enable the sysfs plugin
- add missing R: for -devel subpackage

* Thu Mar 13 2008 Dan Horak <dan[at]danny.cz> - 2.10.2-1
- update to 2.10.2
- spec file and patch cleanup

* Thu Feb 28 2008 Phil Knirsch <pknirsch@redhat.com> - 2.10.1-3
- Removed incorrect patch for IBM BC snmp_bc plugin
- Fixed GCC 4.3 rebuild problems

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.10.1-2
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Phil Knirsch <pknirsch@redhat.com> - 2.10.1-1
- Updated to openhpi-2.10.1
- Bump release and rebuild due to new openssl

* Thu Aug 23 2007 Phil Knirsch <pknirsch@redhat.com> - 2.8.1-5
- Bump release and rebuild because of PPC issues
- Fix rebuild problems due to new glibc open macro

* Fri Jul 20 2007 Phil Knirsch <pknirsch@redhat.com> - 2.8.1-4
- Fix for hpipower segfaulting when using -b option out of range (#247279)

* Tue Jul 17 2007 Phil Knirsch <pknirsch@redhat.com> - 2.8.1-3
- Fixed a bug where the snmp_bc plugin didn't work in IBM BC (#247280)

* Mon Jun 04 2007 Phil Knirsch <pknirsch@redhat.com> - 2.8.1-2.fc7
- Fixed missing e2fsprogs-devel and openssl-devel build requires

* Fri Mar 30 2007 Phil Knirsch <pknirsch@redhat.com> - 2.8.1-1.fc7
- Update to openhpi-2.8.1

* Thu Feb 08 2007 Phil Knirsch <pknirsch@redhat.com> - 2.8.0-3.fc7
- Fixed some silly bugs in the specfile

* Wed Feb 07 2007 Phil Knirsch <pknirsch@redhat.com> - 2.8.0-2.fc7
- Bump and rebuild.

* Tue Feb 06 2007 Phil Knirsch <pknirsch@redhat.com> - 2.8.0-1.fc7
- Update to openhpi-2.8.0

* Tue Nov 28 2006 Phil Knirsch <pknirsch@redhat.com> - 2.4.1-7.fc7
- Rebuilt due to new net-snmp-5.4
- Small specfile updates

* Fri Sep 29 2006 Phil Knirsch <pknirsch@redhat.com> - 2.4.1-6
- Fixed file conflicts for openhpi-switcher (#205226)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.4.1-5.1
- rebuild

* Mon Jul 10 2006 Phil Knirsch <pknirsch@redhat.com> - 2.4.1-5
- Had to disable sysfs support due to new libsysfs and incompatible API.
- Added missing ncurses-devel buildrequires

* Wed Jun 07 2006 Phil Knirsch <pknirsch@redhat.com> - 2.4.1-4
- Rebuilt with final memset patch
- Added missing pkgconfig buildprereq (#191935)

* Fri May 26 2006 Radek Vokal <rvokal@redhat.com> - 2.4.1-2
- rebuilt for new libnetsnmp and net-snmp-config changes

* Wed May 24 2006 Phil Knirsch <pknirsch@redhat.com> - 2.4.1-1
- Fixed buggy use of memset throughout the code
- Made the package build and install properly

* Fri May 19 2006 Phil Knirsch <pknirsch@redhat.com>
- Added missing glib2-devel build prereq (#191935)
- Update to latest stable version openhpi-2.4.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2.1-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2.1-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan  9 2006 Peter Jones <pjones@redhat.com> 2.2.1-4
- Don't use -Werror, it doesn't build with that on ppc64 currently.

* Mon Jan 09 2006 Jesse Keating <jkeating@redhat.com> 2.2.1-3
- Fix to not use stict-aliasing.

* Wed Jan 04 2006 Radek Vokal <rvokal@redhat.com> 2.2.1-2
- Rebuilt against new libnetsnmp

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Phil Knirsch <pknirsch@redhat.com> 2.2.1-1
- Update to stable openhpi-2.2.1

* Wed Nov 09 2005 Phil Knirsch <pknirsch@redhat.com> 2.0.3-5
- Rebuilt to link against latest openssl lib.

* Mon Nov 07 2005 Phil Knirsch <pknirsch@redhat.com> 2.0.3-4
- Added the openhpi config file
- Added missing /var/lib/openhpi dir with proper rights
- Added a few missing BuildPreReqs

* Thu Nov 03 2005 Phil Knirsch <pknirsch@redhat.com> 2.0.3-3
- Rebuild against new net-snmp libs

* Wed Mar 30 2005 Phil Knirsch <pknirsch@redhat.com> 2.0.3-1
- Moved the pkgconfig files to the devel package (#152507)
- Update to openhpi-2.0.3
- Had to manually disable ipmi support for now until openhpi builds correctly
  against it again
- Dropped net-snmp-config patch, not needed anymore

* Thu Mar 17 2005 Phil Knirsch <pknirsch@redhat.com> 1.9.2-5
- Fixed gcc4 rebuild problems

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 1.9.2-4
- bump release and rebuild with gcc 4

* Mon Feb 14 2005 Phil Knirsch <pknirsch@redhat.com> 1.9.2-3
- Rebuilt for new rpm-4.4

* Mon Dec 20 2004 Phil Knirsch <pknirsch@redhat.com> 1.9.2-2
- Fixed overflow in plugins/sysfs/sysfs2hpi.c
- Fixed rebuild problem with latest net-snmp
- Removed is_simulator patch, not needed anymore

* Fri Nov 26 2004 Florian La Roche <laroche@redhat.com> 1.9.2-1
- update to 1.9.2

* Tue Nov 02 2004 Phil Knirsch <pknirsch@redhat.com> 1.9.1-1
- Added proper BuildRequires
- Drop ia64 for first build, something fishy with the compiler and warning.

* Tue Oct 26 2004 Phil Knirsch <pknirsch@redhat.com>
- Initial version
- Disable dummy plugin, doesn't compile
- Fix missing () in snmp_bc_session.c
