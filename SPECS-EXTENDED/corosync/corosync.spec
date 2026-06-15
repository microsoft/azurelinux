Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Conditionals
# Invoke "rpmbuild --without <feature>" or "rpmbuild --with <feature>"
# to disable or enable specific features
%bcond_with watchdog
%bcond_with monitoring
%bcond_without snmp
%bcond_without dbus
%bcond_without systemd
%bcond_without xmlconf
%bcond_without nozzle
%bcond_without vqsim
%bcond_without runautogen
%bcond_without userflags

%global gittarver %{?numcomm:.%{numcomm}}%{?alphatag:-%{alphatag}}%{?dirty:-%{dirty}}

Name: corosync
Summary: The Corosync Cluster Engine and Application Programming Interfaces
Version: 3.0.4
Release: 4%{?dist}
License: BSD
URL: http://corosync.github.io/corosync/
Source0: http://build.clusterlabs.org/corosync/releases/%{name}-%{version}%{?gittarver}.tar.gz

# Runtime bits
# The automatic dependency overridden in favor of explicit version lock
Requires: corosynclib%{?_isa} = %{version}-%{release}

# NSS crypto plugin should be always installed
Requires: libknet1-crypto-nss-plugin

# Build bits
BuildRequires: gcc
BuildRequires: groff
BuildRequires: libqb-devel
BuildRequires: libknet1-devel
BuildRequires: zlib-devel
%if %{with runautogen}
BuildRequires: autoconf automake libtool
%endif
%if %{with monitoring}
BuildRequires: libstatgrab-devel
%endif
%if %{with snmp}
BuildRequires: net-snmp-devel
%endif
%if %{with dbus}
BuildRequires: dbus-devel
%endif
%if %{with nozzle}
BuildRequires: libnozzle1-devel
%endif
%if %{with systemd}
%{?systemd_requires}
BuildRequires: systemd
BuildRequires: systemd-devel
%else
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
%endif
%if %{with xmlconf}
Requires: libxslt
%endif
%if %{with vqsim}
BuildRequires: readline-devel
%endif

%prep
%setup -q -n %{name}-%{version}%{?gittarver}

%build
%if %{with runautogen}
./autogen.sh
%endif

%{configure} \
%if %{with watchdog}
	--enable-watchdog \
%endif
%if %{with monitoring}
	--enable-monitoring \
%endif
%if %{with snmp}
	--enable-snmp \
%endif
%if %{with dbus}
	--enable-dbus \
%endif
%if %{with systemd}
	--enable-systemd \
%endif
%if %{with xmlconf}
	--enable-xmlconf \
%endif
%if %{with nozzle}
	--enable-nozzle \
%endif
%if %{with vqsim}
	--enable-vqsim \
%endif
%if %{with userflags}
	--enable-user-flags \
%endif
	--with-initddir=%{_initrddir} \
	--with-systemddir=%{_unitdir} \
	--docdir=%{_docdir}

make %{_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%if %{with dbus}
mkdir -p -m 0700 %{buildroot}/%{_sysconfdir}/dbus-1/system.d
install -m 644 %{_builddir}/%{name}-%{version}%{?gittarver}/conf/corosync-signals.conf %{buildroot}/%{_sysconfdir}/dbus-1/system.d/corosync-signals.conf
%endif

## tree fixup
# drop static libs
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
# drop docs and html docs for now
rm -rf %{buildroot}%{_docdir}/*
# /etc/sysconfig/corosync-notifyd
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 tools/corosync-notifyd.sysconfig.example \
   %{buildroot}%{_sysconfdir}/sysconfig/corosync-notifyd
# /etc/sysconfig/corosync
install -m 644 init/corosync.sysconfig.example \
   %{buildroot}%{_sysconfdir}/sysconfig/corosync

%description
This package contains the Corosync Cluster Engine Executive, several default
APIs and libraries, default configuration files, and an init script.

%post
%if %{with systemd} && 0%{?systemd_post:1}
%systemd_post corosync.service
%else
if [ $1 -eq 1 ]; then
	/sbin/chkconfig --add corosync || :
fi
%endif

%preun
%if %{with systemd} && 0%{?systemd_preun:1}
%systemd_preun corosync.service
%else
if [ $1 -eq 0 ]; then
	/sbin/service corosync stop &>/dev/null || :
	/sbin/chkconfig --del corosync || :
fi
%endif

%postun
%if %{with systemd} && 0%{?systemd_postun:1}
%systemd_postun corosync.service
%endif

%files
%license LICENSE
%{_sbindir}/corosync
%{_sbindir}/corosync-keygen
%{_sbindir}/corosync-cmapctl
%{_sbindir}/corosync-cfgtool
%{_sbindir}/corosync-cpgtool
%{_sbindir}/corosync-quorumtool
%{_sbindir}/corosync-notifyd
%{_bindir}/corosync-blackbox
%if %{with xmlconf}
%{_bindir}/corosync-xmlproc
%dir %{_datadir}/corosync
%{_datadir}/corosync/xml2conf.xsl
%{_mandir}/man8/corosync-xmlproc.8*
%{_mandir}/man5/corosync.xml.5*
%endif
%dir %{_sysconfdir}/corosync
%dir %{_sysconfdir}/corosync/uidgid.d
%config(noreplace) %{_sysconfdir}/corosync/corosync.conf.example
%config(noreplace) %{_sysconfdir}/sysconfig/corosync-notifyd
%config(noreplace) %{_sysconfdir}/sysconfig/corosync
%config(noreplace) %{_sysconfdir}/logrotate.d/corosync
%if %{with dbus}
%{_sysconfdir}/dbus-1/system.d/corosync-signals.conf
%endif
%if %{with snmp}
%{_datadir}/snmp/mibs/COROSYNC-MIB.txt
%endif
%if %{with systemd}
%{_unitdir}/corosync.service
%{_unitdir}/corosync-notifyd.service
%else
%{_initrddir}/corosync
%{_initrddir}/corosync-notifyd
%endif
%dir %{_localstatedir}/lib/corosync
%dir %{_localstatedir}/log/cluster
%{_mandir}/man7/corosync_overview.7*
%{_mandir}/man8/corosync.8*
%{_mandir}/man8/corosync-blackbox.8*
%{_mandir}/man8/corosync-cmapctl.8*
%{_mandir}/man8/corosync-keygen.8*
%{_mandir}/man8/corosync-cfgtool.8*
%{_mandir}/man8/corosync-cpgtool.8*
%{_mandir}/man8/corosync-notifyd.8*
%{_mandir}/man8/corosync-quorumtool.8*
%{_mandir}/man5/corosync.conf.5*
%{_mandir}/man5/votequorum.5*
%{_mandir}/man7/cmap_keys.7*

# library
#
%package -n corosynclib
Summary: The Corosync Cluster Engine Libraries

%description -n corosynclib
This package contains corosync libraries.

%files -n corosynclib
%license LICENSE
%{_libdir}/libcfg.so.*
%{_libdir}/libcpg.so.*
%{_libdir}/libcmap.so.*
%{_libdir}/libquorum.so.*
%{_libdir}/libvotequorum.so.*
%{_libdir}/libsam.so.*
%{_libdir}/libcorosync_common.so.*

%ldconfig_scriptlets -n corosynclib

%package -n corosynclib-devel
Summary: The Corosync Cluster Engine Development Kit
Requires: corosynclib%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Provides: corosync-devel = %{version}-%{release}
Provides: corosync-devel%{?_isa} = %{version}-%{release}

%description -n corosynclib-devel
This package contains include files and man pages used to develop using
The Corosync Cluster Engine APIs.

%files -n corosynclib-devel
%dir %{_includedir}/corosync/
%{_includedir}/corosync/corodefs.h
%{_includedir}/corosync/cfg.h
%{_includedir}/corosync/cmap.h
%{_includedir}/corosync/corotypes.h
%{_includedir}/corosync/cpg.h
%{_includedir}/corosync/hdb.h
%{_includedir}/corosync/sam.h
%{_includedir}/corosync/quorum.h
%{_includedir}/corosync/votequorum.h
%{_libdir}/libcfg.so
%{_libdir}/libcpg.so
%{_libdir}/libcmap.so
%{_libdir}/libquorum.so
%{_libdir}/libvotequorum.so
%{_libdir}/libsam.so
%{_libdir}/libcorosync_common.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/cpg_*3*
%{_mandir}/man3/quorum_*3*
%{_mandir}/man3/votequorum_*3*
%{_mandir}/man3/sam_*3*
%{_mandir}/man3/cmap_*3*

%if %{with vqsim}
%package -n corosync-vqsim
Summary: The Corosync Cluster Engine - Votequorum Simulator
Requires: corosynclib%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n corosync-vqsim
A command-line simulator for the corosync votequorum subsystem.
It uses the same code as the corosync quorum system but forks
them into subprocesses to simulate nodes.
Nodes can be added and removed as well as partitioned (to simulate
network splits)

%files -n corosync-vqsim
%{_bindir}/corosync-vqsim
%{_mandir}/man8/corosync-vqsim.8*
%endif

%changelog
* Tue Jan 06 2026 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.4-4
- Bumping release to rebuild with new 'net-snmp' libs.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.4-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 02 2020 Jan Friesse <jfriesse@redhat.com> - 3.0.4-2
- Add isa version of corosync-devel
- Add release to corosync-devel version to match autogenerated
  corosynclib-devel provides

* Thu Apr 23 2020 Jan Friesse <jfriesse@redhat.com> - 3.0.4-1
- New upstream release

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Jan Friesse <jfriesse@redhat.com> - 3.0.3-1
- New upstream release

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 12 2019 Jan Friesse <jfriesse@redhat.com> - 3.0.2-1
- New upstream release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Jan Friesse <jfriesse@redhat.com> - 3.0.1-1
- New upstream release

* Fri Dec 14 2018 Jan Friesse <jfriesse@redhat.com> - 3.0.0-1
- New upstream release

* Fri Dec  7 2018 Jan Friesse <jfriesse@redhat.com> - 2.99.5-1
- New upstream release

* Tue Dec  4 2018 Jan Friesse <jfriesse@redhat.com> - 2.99.4-2
- Add libknet1-crypto-nss-plugin dependency

* Tue Nov 20 2018 Jan Friesse <jfriesse@redhat.com> - 2.99.4-1
- New upstream release

* Thu Aug 16 2018 Jan Pokorný <jpokorny+rpm-corosync@redhat.com> - 2.99.3-3
- Rebuild again, since the previous one was so unfortunate it got affected
  with binutils (2.31.1-3.fc29) producing non-monotonically increasing
  section offsets causing unprepared eu-strip to damage the binary
  (related: rhbz#1609577)
- Apply patch to prevent redundancy in systemd journal

* Tue Jul 24 2018 Adam Williamson <awilliam@redhat.com> - 2.99.3-2
- Rebuild for new net-snmp

* Fri Jul 13 2018 Jan Friesse <jfriesse@redhat.com> - 2.99.3-1
- New upstream release

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.99.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 30 2018 Jan Friesse <jfriesse@redhat.com> - 2.99.2-1
- New upstream release

* Fri Mar 16 2018 Jan Friesse <jfriesse@redhat.com> - 2.99.1-1
- New upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.3-2
- Rebuild to fix upgradepath

* Fri Oct 20 2017 Jan Friesse <jfriesse@redhat.com> - 2.4.3-1
- New upstream release

* Mon Oct 09 2017 Troy Dawson <tdawson@redhat.com> - 2.4.2-7
- Cleanup spec file conditionals

* Mon Oct 02 2017 Troy Dawson <tdawson@redhat.com> - 2.4.2-6
- Bump to rebuild on newer binutils

* Wed Aug 23 2017 Adam Williamson <awilliam@redhat.com> - 2.4.2-5
- Disable RDMA on 32-bit ARM (#1484155)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov  7 2016 Jan Friesse <jfriesse@redhat.com> - 2.4.2-1
- New upstream release

* Thu Aug  4 2016 Jan Friesse <jfriesse@redhat.com> - 2.4.1-1
- New upstream release

* Thu Jun 30 2016 Jan Friesse <jfriesse@redhat.com> - 2.4.0-1
- New upstream release

* Thu Jun 16 2016 Jan Friesse <jfriesse@redhat.com> - 2.3.6-1
- New upstream release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 01 2015 Jan Friesse <jfriesse@redhat.com> - 2.3.5-1
- New upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Aug 26 2014 Jan Friesse <jfriesse@redhat.com> - 2.3.4-1
- New upstream release

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 14 2014 Jan Friesse <jfriesse@redhat.com> - 2.3.3-1
- New upstream release

* Mon Sep 16 2013 Jan Friesse <jfriesse@redhat.com> - 2.3.2-1
- New upstream release

* Mon Aug 19 2013 Jan Friesse <jfriesse@redhat.com> 2.3.1-3
- Resolves: rhbz#998362

- Fix scheduler pause-detection timeout (rhbz#998362)
- merge upstream commit 2740cfd1eac60714601c74df2137fe588b607866 (rhbz#998362)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Jan Friesse <jfriesse@redhat.com> - 2.3.1-1
- New upstream release
- Fix incorrect dates in specfile changelog section

* Mon Mar 25 2013 Jan Friesse <jfriesse@redhat.com> - 2.3.0-3
- Resolves: rhbz#925185

- Run autogen by default

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Jan Friesse <jfriesse@redhat.com> - 2.3.0-1
- New upstream release

* Wed Dec 12 2012 Jan Friesse <jfriesse@redhat.com> - 2.2.0-1
- New upstream release

* Thu Oct 11 2012 Jan Friesse <jfriesse@redhat.com> - 2.1.0-1
- New upstream release

* Fri Aug 3 2012 Steven Dake <sdake@redhat.com> - 2.0.1-3
- add groff as a BuildRequires as it is no longer installed in the buildroot

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Jan Friesse <jfriesse@redhat.com> - 2.0.1-1
- New upstream release

* Tue Apr 17 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.0.0-2
- Backport IPCS fix from master (ack by Steven)

* Tue Apr 10 2012 Jan Friesse <jfriesse@redhat.com> - 2.0.0-1
- New upstream release

* Thu Apr 05 2012 Karsten Hopp <karsten@redhat.com> 1.99.9-1.1
- bump release and rebuild on PPC

* Tue Mar 27 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.9-1
- New upstream release

* Fri Mar 16 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.8-1
- New upstream release

* Tue Mar  6 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.7-1
- New upstream release

* Tue Feb 28 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.6-1
- New upstream release

* Wed Feb 22 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.5-1
- New upstream release

* Tue Feb 14 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.4-1
- New upstream release

* Tue Feb 14 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.3-1
- New upstream release

* Tue Feb  7 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.99.2-1
- New upstream release
- Re-enable xmlconfig bits
- Ship cmap man pages
- Add workaround to usrmove breakage!!

* Thu Feb  2 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.99.1-2
- Add proper Obsoltes on openais/cman/clusterlib

* Wed Feb  1 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.99.1-1
- New upstream release
- Temporary disable xml config (broken upstream tarball)

* Tue Jan 24 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.0-1
- New upstream release

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 06 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.2-1
- New upstream release

* Thu Sep 08 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.1-2
- Add upstream fixes

* Tue Jul 26 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.1-1
- New upstream release

* Wed Jul 20 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.0-2
- Change attributes of cluster log directory

* Tue Jul 19 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.0-1
- New upstream release
- Resync spec file with upstream changes

* Fri Jul 08 2011 Jan Friesse <jfriesse@redhat.com> - 1.3.2-1
- New upstream release

* Tue May 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.3.1-1
- New upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.3.0-1
- New upstream release
- drop upstream patch revision-2770.patch now included in release
- update spec file to ship corosync-blackbox

* Thu Sep  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.8-1
- New upstream release

* Thu Jul 29 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.7-1
- New upstream release

* Fri Jul  9 2010 Dan Horák <dan[at]danny.cz> - 1.2.6-2
- no InfiniBand stack on s390(x)

* Mon Jul  5 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.6-1
- New upstream release
- Resync spec file with upstream changes

* Tue May 25 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.3-1
- New upstream release
- Rediff revision 2770 patch

* Mon May 17 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.2-1
- New upstream release
- Add upstream trunk revision 2770 to add cpg_model_initialize api.
- Fix URL and Source0 entries.
- Add workaround to broken 1.2.2 Makefile with make -j.

* Wed Mar 24 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.1-1
- New upstream release

* Tue Dec  8 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.0-1
- New upstream release
- Use global instead of define
- Update Source0 url
- Use more name macro around
- Cleanup install section. Init script is now installed by upstream
- Cleanup whitespace
- Don't deadlock between package upgrade and corosync condrestart
- Ship service.d config directory
- Fix Conflicts vs Requires
- Ship new sam library and man pages

* Fri Oct 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.2-1
- New upstream release fixes major regression on specific loads

* Wed Oct 21 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.1-1
- New upstream release

* Fri Sep 25 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.0-1
- New upstream release
- spec file updates:
  * enable IB support
  * explicitly define built-in features at configure time

* Tue Sep 22 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.1-1
- New upstream release
- spec file updates:
  * use proper configure macro

* Tue Jul 28 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.0-3
- spec file updates:
  * more consistent use of macros across the board
  * fix directory ownership

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  8 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.0-1
- New upstream release

* Thu Jul  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.100-1
- New upstream release

* Sat Jun 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.98-1
- New upstream release
- spec file updates:
  * Drop corosync-trunk patch and alpha tag.
  * Fix alphatag vs buildtrunk handling.
  * Drop requirement on ais user/group and stop creating them.
  * New config file locations from upstream: /etc/corosync/corosync.conf.

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.97-1.svn2233
- spec file updates:
  * Update to svn version 2233 to include library linking fixes

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.97-1.svn2232
- New upstream release
- spec file updates:
  * Drop pkgconfig fix that's now upstream
  * Update to svn version 2232
  * Define buildtrunk if we are using svn snapshots
  * BuildRequires: nss-devel to enable nss crypto for network communication
  * Force autogen invokation if buildtrunk is defined
  * Whitespace cleanup
  * Stop shipping corosync.conf in favour of a generic example
  * Update file list

* Mon Mar 30 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.95-2
- Backport svn commit 1913 to fix pkgconfig files generation
  and unbreak lvm2 build.

* Tue Mar 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.95-1
- New upstream release
- spec file updates:
  * Drop alpha tag
  * Drop local patches (no longer required)
  * Allow to build from svn trunk by supporting rpmbuild --with buildtrunk 
  * BuildRequires autoconf automake if building from trunk
  * Execute autogen.sh if building from trunk and if no configure is available
  * Switch to use rpm configure macro and set standard install paths
  * Build invokation now supports _smp_mflags
  * Remove install section for docs and use proper doc macro instead
  * Add tree fixup bits to drop static libs and html docs (only for now)
  * Add LICENSE file to all subpackages
  * libraries have moved to libdir. Drop ld.so.conf.d corosync file
  * Update BuildRoot usage to preferred versions/names

* Tue Mar 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-5.svn1797
- Update the corosync-trunk patch for real this time.

* Tue Mar 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-4.svn1797
- Import fixes from upstream:
  * Cleanup logsys format init around to use default settings (1795)
  * logsys_format_set should use its own internal copy of format_buffer (1796)
  * Add logsys_format_get to logsys API (1797)
- Cherry pick svn1807 to unbreak CPG.

* Mon Mar  9 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-3.svn1794
- Import fixes from upstream:
  * Add reserve/release feature to totem message queue space (1793)
  * Fix CG shutdown (1794)

* Fri Mar  6 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-2.svn1792
- Import fixes from upstream:
  * Fix uninitialized memory. Spotted by valgrind (1788)
  * Fix logsys_set_format by updating the right bits (1789)
  * logsys: re-add support for timestamp  (1790)
  * Fix cpg crash (1791)
  * Allow logsys_format_set to reset to default (1792)

* Tue Mar  3 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-1
- New upstream release.
- Drop obsolete patches.
- Add soname bump patch that was missing from upstream.

* Wed Feb 25 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.93-4
- Add Makefile fix to install all corosync tools (commit r1780)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.93-2
- Rename gcc-4.4 patch to match svn commit (r1767).
- Backport patch from trunk (commit r1774) to fix quorum engine.

* Thu Feb 19 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.93-1
- New upstream release.
- Drop alphatag from spec file.
- Drop trunk patch.
- Update Provides for corosynclib-devel.
- Backport gcc-4.4 build fix from trunk.

* Mon Feb  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-7.svn1756
- Update to svn trunk at revision 1756 from upstream.
- Add support pkgconfig to devel package.
- Tidy up spec files by re-organazing sections according to packages.
- Split libraries from corosync to corosynclib.
- Rename corosync-devel to corosynclib-devel.
- Comply with multiarch requirements (libraries).

* Tue Jan 27 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-6.svn1750
- Update to svn trunk at revision 1750 from upstream.
- Include new quorum service in the packaging.

* Mon Dec 15 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-5.svn1709
- Update to svn trunk at revision 1709 from upstream.
- Update spec file to include new include files.

* Wed Dec 10 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-4.svn1707
- Update to svn trunk at revision 1707 from upstream.
- Update spec file to include new lcrso services and include file.

* Mon Oct 13 2008 Dennis Gilmore <dennis@ausil.us> - 0.92-3
- remove ExclusiveArch line

* Wed Sep 24 2008 Steven Dake <sdake@redhat.com> - 0.92-2
- Add conflicts for openais and openais-devel packages older then 0.90.

* Wed Sep 24 2008 Steven Dake <sdake@redhat.com> - 0.92-1
- New upstream release corosync-0.92.

* Sun Aug 24 2008 Steven Dake <sdake@redhat.com> - 0.91-3
- move logsys_overview.8.* to devel package.
- move shared libs to main package.

* Wed Aug 20 2008 Steven Dake <sdake@redhat.com> - 0.91-2
- use /sbin/service instead of calling init script directly.
- put corosync-objctl man page in the main package.
- change all initrddir to initddir for fedora 10 guidelines.

* Thu Aug 14 2008 Steven Dake <sdake@redhat.com> - 0.91-1
- First upstream packaged version of corosync for rawhide review.
