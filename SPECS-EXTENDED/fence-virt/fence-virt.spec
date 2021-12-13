Vendor:         Microsoft Corporation
Distribution:   Mariner
###############################################################################
###############################################################################
##
##  Copyright (C) 2019 Red Hat, Inc.  All rights reserved.
##
##  This copyrighted material is made available to anyone wishing to use,
##  modify, copy, or redistribute it subject to the terms and conditions
##  of the GNU General Public License v.2.
##
###############################################################################
###############################################################################

Name:    fence-virt
Summary: A pluggable fencing framework for virtual machines
Version: 1.0.0
Release: 2%{?dist}
License: GPLv2+
URL:     https://github.com/ClusterLabs/fence-virt
Source0: %{name}-%{version}%{?rcver:%{rcver}}%{?numcomm:.%{numcomm}}%{?alphatag:-%{alphatag}}%{?dirty:-%{dirty}}.tar.bz2

%if 0%{?suse_version}
%define nss_devel mozilla-nss-devel
%define nspr_devel mozilla-nspr-devel
%define systemd_units systemd
%else
%define nss_devel nss-devel
%define nspr_devel nspr-devel
%define systemd_units systemd-units
%endif

BuildRequires: gcc
BuildRequires: corosynclib-devel libvirt-devel
BuildRequires: automake autoconf libtool libxml2-devel %{nss_devel} %{nspr_devel}
BuildRequires: flex bison libuuid-devel

BuildRequires:    systemd-units
Requires(post):   systemd-sysv systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

Conflicts:	fence-agents < 3.0.5-2

%prep
%autosetup -p1

%build
./autogen.sh
%{configure} --disable-libvirt-qmf-plugin --enable-cpg-plugin
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Systemd unit file
mkdir -p %{buildroot}/%{_unitdir}/
install -m 0644 fence_virtd.service %{buildroot}/%{_unitdir}/

rm -f %{buildroot}/%{_libdir}/%{name}/*.*a

%post
ccs_update_schema > /dev/null 2>&1 ||:
# https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Systemd
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun
# https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Systemd
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable fence_virtd.service &> /dev/null || :
    /bin/systemctl stop fence_virtd.service &> /dev/null || :
fi

%postun
# https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Systemd
/bin/systemctl daemon-reload &> /dev/null || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart fence_virtd.service &> /dev/null || :
fi

%triggerun -- fence_virtd < 0.3.0-1
# https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Packages_migrating_to_a_systemd_unit_file_from_a_SysV_initscript
/usr/bin/systemd-sysv-convert --save fence_virtd &> /dev/null || :
/sbin/chkconfig --del fence_virtd &> /dev/null || :
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
/bin/systemctl try-restart fence_virtd.service &> /dev/null || :

%description
Fencing agent for virtual machines.

%files
%doc COPYING TODO README
%{_sbindir}/fence_virt
%{_sbindir}/fence_xvm
%{_mandir}/man8/fence_virt.*
%{_mandir}/man8/fence_xvm.*

%package -n fence-virtd
Summary: Daemon which handles requests from fence-virt
%description -n fence-virtd
This package provides the host server framework, fence_virtd,
for fence_virt.  The fence_virtd host daemon is resposible for
processing fencing requests from virtual machines and routing
the requests to the appropriate physical machine for action.
%files -n fence-virtd
%{_sbindir}/fence_virtd
%{_unitdir}/fence_virtd.service
%config(noreplace) %{_sysconfdir}/fence_virt.conf
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/vsock.so
%{_mandir}/man5/fence_virt.conf.*
%{_mandir}/man8/fence_virtd.*

%package -n fence-virtd-multicast
Summary:  Multicast listener for fence-virtd
Requires: fence-virtd
%description -n fence-virtd-multicast
Provides multicast listener capability for fence-virtd.
%files -n fence-virtd-multicast
%{_libdir}/%{name}/multicast.so

%package -n fence-virtd-serial
Summary:  Serial VMChannel listener for fence-virtd
Requires: libvirt >= 0.6.2
Requires: fence-virtd
%description -n fence-virtd-serial
Provides serial VMChannel listener capability for fence-virtd.
%files -n fence-virtd-serial
%{_libdir}/%{name}/serial.so

%package -n fence-virtd-tcp
Summary:  TCP listener for fence-virtd
Requires: fence-virtd
%description -n fence-virtd-tcp
Provides TCP listener capability for fence-virtd.
%files -n fence-virtd-tcp
%{_libdir}/%{name}/tcp.so

%package -n fence-virtd-libvirt
Summary:  Libvirt backend for fence-virtd
Requires: libvirt >= 0.6.0
Requires: fence-virtd
%description -n fence-virtd-libvirt
Provides fence_virtd with a connection to libvirt to fence
virtual machines.  Useful for running a cluster of virtual
machines on a desktop.
%files -n fence-virtd-libvirt
%{_libdir}/%{name}/virt.so

%package -n fence-virtd-cpg
Summary:  CPG/libvirt backend for fence-virtd
Requires: corosynclib
Requires: fence-virtd
%description -n fence-virtd-cpg
Provides fence_virtd with a connection to libvirt to fence
virtual machines. Uses corosync CPG to keep track of VM
locations to allow for non-local VMs to be fenced when VMs
are located on corosync cluster nodes.
%files -n fence-virtd-cpg
%{_libdir}/%{name}/cpg.so

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Mar 10 2020 Oyvind Albrigtsen <oalbrigt@redhat.com> - 1.0.0-1
- Rebase to fence-virt-1.0.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 21 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 0.9.0-1
- Rebase to fence-virt-0.9.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Ryan McCabe <rmccabe@redhat.com> - 0.4.0-9
- Add gcc-c++ to build deps.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 31 2018 Ryan McCabe <rmccabe@redhat.com> - 0.4.0-7
- Return control to the dispatch loop if select is interrupted by a signal.

* Tue May 29 2018 Rafael dos Santos <rdossant@redhat.com> - 0.4.0-5
- Use Fedora standard build/linker flags (rhbz#1548424)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Ryan McCabe <rmccabe@redhat.com> - 0.4.0-1
- Rebase to fence-virt-0.4.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.3.2-4
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 04 2013 Ryan McCabe <rmccabe@redhat.com> - 0.3.2-1
- New upstream version 0.3.2

* Sun Nov 03 2013 Ryan McCabe <rmccabe@redhat.com> - 0.3.1-1
- Drop executable flags of manual pages
- Fix for missed libvirtd events
- Fix for broken systemd service file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-14
- Fail properly when unable to bind the TCP listener socket.
- Resolves: rhbz#814515

* Tue May 07 2013 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-13
- Rebuild

* Tue May 07 2013 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-12
- Drop libvirt-qmf-plugin

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-10
- bswap fix for big endian

* Fri Nov 02 2012 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-9
- Return success if a domain exists but is already off.

* Thu Oct 25 2012 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-8
- Version bump

* Thu Oct 25 2012 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-7
- Fix uninitialized variable for the -w option.

* Mon Oct 15 2012 Ryan McCabe <rmccabe@redhat.com> - 0.3.0-6
- Add a -w (delay) option.
- Return failure when attempting to fence a nonexistent domain
- Improve man pages

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Ryan McCabe <rmccabe@fedoraproject.org> 0.3.0-4
- Add QPid build fix patch from upstream.

* Fri Feb 10 2012 Lon Hohberger <lon@fedoraproject.org> 0.3.0-2
- Fix URL / Source0 lines
  Resolves: Fedora#706560

* Tue Feb 07 2012 Lon Hohberger <lhh@redhat.com> 0.3.0-1
- Rebase from upstream to 0.3.0
- Systemd unit file integration
- Pacemaker backend
- Various fixes for startup
- Rename libvirt-qpid to libvirt-qmf backend
- Updated default configuration for easier deployment on
  Fedora systems

* Tue Feb 07 2012 Lon Hohberger <lhh@redhat.com> - 0.2.3-6
- Bump and rebuild

* Tue Feb 07 2012 Lon Hohberger <lhh@redhat.com> - 0.2.3-5
- Fixup changelog

* Mon Feb 06 2012 Lon Hohberger <lhh@redhat.com> - 0.2.3-4
- Drop checkpoint backend since cman and openais are gone

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul  8 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.2.3-2
- add post call to fence-virt to integrate with cluster 3.1.4

* Wed Jun 29 2011 Fabio M. Di Nitto <fdinitto@redhat.com> 0.2.3-1
- new upstream release fix compat regression

* Mon Jun 27 2011 Fabio M. Di Nitto <fdinitto@redhat.com> 0.2.2-1
- new upstream release

* Mon May 09 2011 Fabio M. Di Nitto <fdinitto@redhat.com> 0.2.1-5
- Rebuilt for libqmfconsole soname change

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 01 2010 Lon Hohberger <lhh@redhat.com> 0.2.1-3
- Update specfile to require correct qpid/qmf libraries
- Resolves: bz#565111

* Tue Feb 23 2010 Fabio M. Di Nitto <fdinitto@redhat.com> 0.2.1-2
- Update spec file to handle correctly versioned Requires

* Fri Jan 15 2010 Lon Hohberger <lhh@redhat.com> 0.2.1-1
- Update to latest upstream version
- Fix bug around status return codes for VMs which are 'off'

* Thu Jan 14 2010 Lon Hohberger <lhh@redhat.com> 0.2-1
- Update to latest upstream version
- Serial & VMChannel listener support
- Static permission map support
- Man pages
- Init script
- Various bugfixes

* Mon Sep 21 2009 Lon Hohberger <lhh@redhat.com> 0.1.3-1
- Update to latest upstream version
- Adds libvirt-qpid backend support
- Fixes UUID operation with libvirt backend
- Adds man page for fence_xvm and fence_virt
- Provides fence_xvm compatibility for cluster 3.0.6

* Mon Sep 21 2009 Lon Hohberger <lhh@redhat.com> 0.1.2-1
- Update to latest upstream version
- Fix build issue on i686

* Mon Sep 21 2009 Lon Hohberger <lhh@redhat.com> 0.1.1-1
- Update to latest upstream version
- Clean up spec file

* Mon Sep 21 2009 Lon Hohberger <lhh@redhat.com> 0.1-2
- Spec file cleanup

* Thu Sep 17 2009 Lon Hohberger <lhh@redhat.com> 0.1-1
- Initial build for rawhide
