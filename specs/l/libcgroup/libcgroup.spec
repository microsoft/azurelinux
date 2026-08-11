# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with tests

%global tests_commit 7c998caddcd8236fe4191841e361b401697fb777

Summary: Library to control and monitor control groups
Name: libcgroup
Version: 3.0
Release: 11%{?dist}
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License: LicenseRef-Callaway-LGPLv2+
URL: http://libcg.sourceforge.net/
Source0: https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-v%{version}.tar.gz
Source1: https://github.com/%{name}/%{name}-tests/archive/%{tests_commit}.tar.gz
Source2: cgconfig.service

Patch0: fedora-config.patch
Patch1: libcgroup-0.37-chmod.patch
Patch2: libcgroup-0.40.rc1-coverity.patch
Patch3: libcgroup-0.40.rc1-fread.patch
Patch4: libcgroup-0.40.rc1-templates-fix.patch

Patch100: libcgroup-tests-unbundle-gtest.patch

BuildRequires: autoconf, automake, libtool
BuildRequires: gcc, gcc-c++
BuildRequires: byacc, coreutils, flex, pam-devel, systemd-units
BuildRequires: make
%if %{with tests}
BuildRequires: gtest-devel
%endif
Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Control groups infrastructure. The library helps manipulate, control,
administrate and monitor control groups and the associated controllers.

%package tools
Summary: Command-line utility programs, services and daemons for libcgroup
Requires: %{name}%{?_isa} = %{version}-%{release}
# needed for Delegate property in cgconfig.service
Requires: systemd >= 217-0.2

%description tools
This package contains command-line programs, services and a daemon for
manipulating control groups using the libcgroup library.

%package pam
Summary: A Pluggable Authentication Module for libcgroup
Requires: %{name}%{?_isa} = %{version}-%{release}

%description pam
Linux-PAM module, which allows administrators to classify the user's login
processes to pre-configured control group.

%package devel
Summary: Development libraries to develop applications that utilize control groups
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
It provides API to create/delete and modify cgroup nodes. It will also in the
future allow creation of persistent configuration for control groups and
provide scripts to manage that configuration.

%prep
%setup  -q  -n %{name}-%{version}
%patch -P0 -p1 -b .config-patch
%patch -P1 -p1 -b .chmod
%patch -P2 -p1 -b .coverity
%patch -P3 -p1 -b .fread
%patch -P4 -p1 -b .templates-fix

%setup -D -T -a 1
mv -T %{name}-tests-%{tests_commit} tests
%patch -P100 -p1 -b .tests-unbundle-gtest

%build
autoreconf -vif
%configure --enable-pam-module-dir=%{_libdir}/security \
           --enable-opaque-hierarchy="name=systemd" \
           --disable-daemon
%make_build

%install
%make_install

# install config files
install -d ${RPM_BUILD_ROOT}%{_sysconfdir}
install -m 644 samples/config/cgconfig.conf $RPM_BUILD_ROOT/%{_sysconfdir}/cgconfig.conf
install -m 644 samples/config/cgsnapshot_blacklist.conf $RPM_BUILD_ROOT/%{_sysconfdir}/cgsnapshot_blacklist.conf

# sanitize pam module, we need only pam_cgroup.so
rm -f $RPM_BUILD_ROOT%{_libdir}/security/pam_cgroup.{,l}a

rm -f $RPM_BUILD_ROOT/%{_libdir}/*.{,l}a

rm -f $RPM_BUILD_ROOT/%{_libdir}/libcgroupfortesting.*

rm -f $RPM_BUILD_ROOT/%{_mandir}/man5/cgred.conf.5*
rm -f $RPM_BUILD_ROOT/%{_mandir}/man5/cgrules.conf.5*
rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/cgrulesengd.8*

# install unit and sysconfig files
install -d ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %SOURCE2 ${RPM_BUILD_ROOT}%{_unitdir}/
install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig

%check
%if %{with tests}
make -C tests/gunit check
%endif

%post tools
%systemd_post cgconfig.service

%preun tools
%systemd_preun cgconfig.service

%postun tools
%systemd_postun_with_restart cgconfig.service

%triggerun -- libcgroup < 0.38
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply cgconfig
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save cgconfig >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del cgconfig >/dev/null 2>&1 || :
/bin/systemctl try-restart cgconfig.service >/dev/null 2>&1 || :

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README
%{_libdir}/libcgroup.so.3*

%files tools
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README README_systemd
%config(noreplace) %{_sysconfdir}/cgconfig.conf
%config(noreplace) %{_sysconfdir}/cgsnapshot_blacklist.conf
%{_bindir}/cgcreate
%{_bindir}/cgget
%{_bindir}/cgset
%{_bindir}/cgxget
%{_bindir}/cgxset
%{_bindir}/cgdelete
%{_bindir}/lscgroup
%{_bindir}/lssubsys
%{_sbindir}/cgconfigparser
%{_bindir}/cgsnapshot
%{_bindir}/cgclassify
%attr(0755, root, root) %{_bindir}/cgexec
%attr(0644, root, root) %{_mandir}/man1/*
%attr(0644, root, root) %{_mandir}/man5/*
%attr(0644, root, root) %{_mandir}/man8/*
%{_unitdir}/cgconfig.service

%files pam
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README
%attr(0755,root,root) %{_libdir}/security/pam_cgroup.so

%files devel
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README
%{_includedir}/libcgroup.h
%{_includedir}/libcgroup/*.h
%{_libdir}/libcgroup.so
%{_libdir}/pkgconfig/libcgroup.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 3.0-7
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Aug 06 2022 Nikola Forró <nforro@redhat.com> - 3.0-1
- New upstream release 3.0
  resolves: #2115990

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 25 2022 Nikola Forró <nforro@redhat.com> - 2.0.2-1
- New upstream release 2.0.2
  resolves: #2085318

* Sat Mar 12 2022 Nikola Forró <nforro@redhat.com> - 2.0.1-1
- New upstream release 2.0.1
  resolves: #2063319

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 18 2021 Nikola Forró <nforro@redhat.com> - 2.0-2
- remove unnecessary cgred group and setgid on binaries

* Sun May 16 2021 Nikola Forró <nforro@redhat.com> - 2.0-1
- resolves: #1953968
  new upstream release 2.0

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.42.2-5
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.42.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.42.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 0.42.2-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Thu Feb 06 2020 Nikola Forró <nforro@redhat.com> - 0.42.2-1
- resolves: #1798286
  new upstream release 0.42.2

* Mon Feb 03 2020 Nikola Forró <nforro@redhat.com> - 0.42.1-1
- resolves: #1792190
  new upstream release 0.42.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 02 2018 Nikola Forró <nforro@redhat.com> - 0.41-20
- resolves: #1611121
  fix CVE-2018-14348

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Nikola Forró <nforro@redhat.com> - 0.41-18
- remove ldconfig scriptlets

* Tue Apr 17 2018 Nikola Forró <nforro@redhat.com> - 0.41-17
- backport several upstream fixes
- set Delegate property for cgconfig service to make sure complete
  cgroup hierarchy is always created by systemd

* Tue Feb 20 2018 Nikola Forró <nforro@redhat.com> - 0.41-16
- add missing gcc-c++ build dependency

* Tue Feb 20 2018 Nikola Forró <nforro@redhat.com> - 0.41-15
- add missing gcc build dependency

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 13 2016 Nikola Forró <nforro@redhat.com> - 0.41-10
- resolves: #1384504
  api.c: preserve dirty flag when copying controller values

* Fri Jul 01 2016 Nikola Forró <nforro@redhat.com> - 0.41-9
- resolves: #1348874
  api.c: fix order of memory subsystem parameters generated by cgsnapshot

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 23 2014 jchaloup <jchaloup@redhat.com> - 0.41-6
- resolves: #647107
  api.c: support for setting multiline values in control files

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Tom Callaway <spot@fedoraproject.org> - 0.41-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 03 2014 jchaloup <jchaloup@redhat.com> - 0.41-2
- lex.l update: add \ character into regexp for ID token

* Tue Jan 14 2014 Peter Schiffer <pschiffe@redhat.com> 0.41-1
- resolves: #966008
  updated to 0.41
- removed deprecated cgred service
  please use Control Group Interface in Systemd instead

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Karsten Hopp <karsten@redhat.com> 0.38-6
- add BR: systemd-units

* Tue Jul 09 2013 Karsten Hopp <karsten@redhat.com> 0.38-5
- bump release and rebuild to fix some dependencies on PPC

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Peter Schiffer <pschiffe@redhat.com> - 0.38-3
- resolves: #850183
  scriptlets replaced with new systemd macros (thanks to vpavlin)
- cleaned .spec file

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 20 2012 Jan Safranek <jsafrane@redhat.com> 0.38-1
- updated to 0.38

* Fri Feb  3 2012 Jan Safranek <jsafrane@redhat.com> 0.38-0.rc1
- updated to 0.38.rc1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 30 2011 Jan Safranek <jsafrane@redhat.com> 0.37.1-4
- fixed cgconfig service not to unmount stuff it did not mount
- added better sample cgconfig.conf file to reflect systemd
  mounting all controllers during boot (#702111)

* Wed May 25 2011 Ivana Hutarova Varekova <varekova@redhat.com> 0.37.1-3
- split tools part from libcgroup package

* Fri Apr  8 2011 Jan Safranek <jsafrane@redhat.com> 0.37.1-2
- Remove /cgroup directory, groups are created in /sys/fs/cgroup
  (#694687)

* Thu Mar  3 2011 Jan Safranek <jsafrane@redhat.com> 0.37.1-1
- Update to 0.37.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Jan Safranek <jsafrane@redhat.com> 0.37-2
- Create the 'cgred' group as system group, not as user
- Fix cgclassify exit code

* Mon Dec 13 2010 Jan Safranek <jsafrane@redhat.com> 0.37-1
- Update to 0.37
- use /sys/fs/cgroup as default directory to mount control groups (and rely on
  systemd mounting tmpfs there)

* Fri Nov 12 2010 Jan Safranek <jsafrane@redhat.com> 0.36.2-3
- Ignore systemd hierarchy - it's now invisible to libcgroup (#627378)

* Mon Aug  2 2010 Jan Safranek <jsafrane@redhat.com> 0.36.2-2
- Fix initscripts to report stopped cgconfig service as not running
  (#619091)

* Tue Jun 22 2010 Jan Safranek <jsafrane@redhat.com> 0.36.2-1
- Update to 0.36.2, fixing packaging the libraries (#605434)
- Remove the dependency on redhat-lsb (#603578)

* Fri May 21 2010 Jan Safranek <jsafrane@redhat.com> 0.36-1
- Update to 0.36.1

* Tue Mar  9 2010 Jan Safranek <jsafrane@redhat.com> 0.35-1
- Update to 0.35.1
- Separate pam module to its own subpackage

* Mon Jan 18 2010 Jan Safranek <jsafrane@redhat.com> 0.34-4
- Added README.Fedora to describe initscript integration

* Mon Oct 19 2009 Jan Safranek <jsafrane@redhat.com> 0.34-3
- Change the default configuration to mount everything to /cgroup

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul  7 2009 Jan Safranek <jsafrane@redhat.com> 0.34-1
- Update to 0.34
* Mon Mar 09 2009 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.33-3
- Add a workaround for rt cgroup controller.
* Mon Mar 09 2009 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.33-2
- Change the cgconfig script to start earlier
- Move the binaries to /bin and /sbin
* Mon Mar 02 2009 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.33-1
- Update to latest upstream
* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.32.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 05 2009 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.32.2-3
- Fix redhat-lsb dependency
* Mon Dec 29 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.32.2-2
- Fix build dependencies
* Mon Dec 29 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.32.2-1
- Update to latest upstream
* Thu Oct 23 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.32.1-1
* Tue Feb 24 2009 Balbir Singh <balbir@linux.vnet.ibm.com> 0.33-1
- Update to 0.33, spec file changes to add Makefiles and pam_cgroup module
* Fri Oct 10 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.32-1
- Update to latest upstream
* Thu Sep 11 2008 Dhaval Giani <dhaval@linux-vnet.ibm.com> 0.31-1
- Update to latest upstream
* Sat Aug 2 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.1c-3
- Change release to fix broken upgrade path
* Wed Jun 11 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.1c-1
- Update to latest upstream version
* Tue Jun 3 2008 Balbir Singh <balbir@linux.vnet.ibm.com> 0.1b-3
- Add post and postun. Also fix Requires for devel to depend on base n-v-r
* Sat May 31 2008 Balbir Singh <balbir@linux.vnet.ibm.com> 0.1b-2
- Fix makeinstall, Source0 and URL (review comments from Tom)
* Mon May 26 2008 Balbir Singh <balbir@linux.vnet.ibm.com> 0.1b-1
- Add a generatable spec file
* Tue May 20 2008 Balbir Singh <balbir@linux.vnet.ibm.com> 0.1-1
- Get the spec file to work
* Tue May 20 2008 Dhaval Giani <dhaval@linux.vnet.ibm.com> 0.01-1
- The first version of libcg
