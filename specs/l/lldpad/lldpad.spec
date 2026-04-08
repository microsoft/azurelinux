# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _default_patch_fuzz 2

# https://fedoraproject.org/wiki/Packaging:Guidelines#Compiler_flags
%global _hardened_build 1

%global checkout 85e5583

Name:               lldpad
Version:            1.1.0
Release:            14.git%{checkout}%{?dist}
Summary:            Intel LLDP Agent
License:            GPL-2.0-only
URL:                http://open-lldp.org/
Source0:            %{name}-%{version}.tar.gz

BuildRequires:      automake autoconf libtool
BuildRequires:      flex >= 2.5.33
BuildRequires:      kernel-headers >= 2.6.32
BuildRequires:      libconfig-devel >= 1.3.2
BuildRequires:      libnl3-devel
BuildRequires:      readline-devel
BuildRequires:      systemd
BuildRequires: make
Requires:           readline

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
This package contains the Linux user space daemon and configuration tool for
Intel LLDP Agent with Enhanced Ethernet support for the Data Center.

%package            devel
Summary:            Development files for %{name}
Requires:           %{name}%{?_isa} = %{version}-%{release}
Provides:           dcbd-devel = %{version}-%{release}
Obsoletes:          dcbd-devel < 0.9.26

%description devel
The %{name}-devel package contains header files for developing applications
that use %{name}.

%prep
%autosetup -p1

%build
./bootstrap.sh
CFLAGS=${CFLAGS:-%optflags -Wno-error -fcommon}; export CFLAGS;
%configure --disable-static
# fix the hardened build flags
sed -i -e 's! \\\$compiler_flags !&\\\$CFLAGS \\\$LDFLAGS !' libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
rm -f %{buildroot}%{_libdir}/liblldp_clif.la

%post
%systemd_post %{name}.service %{name}.socket

%preun
%systemd_preun %{name}.service %{name}.socket

%postun
%systemd_postun_with_restart %{name}.service %{name}.socket

%files
%doc COPYING README ChangeLog
%{_sbindir}/*
%{_libdir}/liblldp_clif.so.*
%dir %{_sharedstatedir}/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
%{_sysconfdir}/bash_completion.d/*
%{_mandir}/man3/*
%{_mandir}/man8/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/liblldp_clif.so

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-14.git85e5583
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-13.git85e5583
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12.git85e5583
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb 22 2024 Aaron Conole <aconole@redhat.com> - 1.1.0-11.git85e5583
- Convert the license tag to SPDX format

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10.git85e5583
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9.git85e5583
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-8.git85e5583
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7.git85e5583
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6.git85e5583
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5.git85e5583
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4.git85e5583
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.1.0-3.git85e5583
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2.git85e5583
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 02 2020 Aaron Conole <aconole@redhat.com> - 1.1.0-1.git85e5583
- Update to 1.1.0

* Fri Aug 07 2020 Jeff Law <law@redhat.com> - 1.0.1-20.git036e314
- Enable _legacy_common_support

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-19.git036e314
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-18.git036e314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-17.git036e314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Sep 14 2019 Ido Schimmel <idosch@mellanox.com> - 1.0.1-16.git036e314
- Add open-lldp-v1.0.1-30-lldpad-Do-not-enable-port-if-already-enabled.patch
  (BZ 1752207)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-15.git036e314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.1-14.git036e314
- Remove obsolete scriptlets

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-13.git036e314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 23 2018 Petr Machata <pmachata@gmail.com> - 1.0.1-12.git036e314
- Add open-lldp-v1.0.1-29-basman_clif-print-the-OID-properly.patch (BZ 1614932,
  1614896 (CVE-2018-10932)
- Add open-lldp-v1.0.1-28-support-DSCP-selectors.patch (BZ 1618377)

* Tue Jul 24 2018 Adam Williamson <awilliam@redhat.com> - 1.0.1-11.git036e314
- Rebuild for new libconfig

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-10.git036e314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-9.git036e314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-8.git036e314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7.git036e314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Feb 12 2017 Chris Leech <cleech@redhat.com> - 1.0.1-6.git036e314
- disable -Werror from upstream to rebuild with newer compiler warnings

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-5.git036e314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4.git036e314
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Chris Leech <cleech@redhat.com> - 1.0.1-3.git986eb2e
- 1303439 package should not attempt to own /etc/bash_completion.d
- fix more build warning in rawhide

* Tue Nov 03 2015 Chris Leech <cleech@redhat.com> - 1.0.1-2.git986eb2e
- convert from sysv shm to posix, to allow selinux restorecon 

* Wed Jun 17 2015 Chris Leech <cleech@redhat.com> - 1.0.1-1.git986eb2e
- rebased to upstream v1.0.1-23-g986eb2e

* Thu Oct 23 2014 Chris Leech <cleech@redhat.com> - 0.9.46-8.git48a5f38
- sync to upstream v0.9.46-123-g48a5f38

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.46-6
- Add upstream patch to build against libnl3
- Drop legacy dcbd packaging support, we've not shipped it since F-13

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.46-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 11 2014 Petr Šabata <contyk@redhat.com> - 0.9.46-4
- Drop the explicit kernel runtime dependency
- Patch configure.ac to build in rawhide

* Wed Jul 31 2013 Petr Šabata <contyk@redhat.com> - 0.9.46-3
- Require 'systemd' instead of 'systemd-units'

* Tue Jul 02 2013 Petr Šabata <contyk@redhat.com> - 0.9.46-2
- Fix the hardened build flags

* Tue Jun 04 2013 Petr Šabata <contyk@redhat.com> - 0.9.46-1
- 0.9.46 bump
- 802.1Qaz fixes to enable support on not CEE DCBX-enabled hardware
- 802.1Qbg EVB module support
- lldpad now supports bonded interfaces

* Tue Mar 05 2013 Petr Šabata <contyk@redhat.com> - 0.9.45-5
- Fix build by patching the sizeof() call in lldp_8021qaz_cmds.c

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.45-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Petr Šabata <contyk@redhat.com> - 0.9.45-3
- Migrate to systemd scriptlets (#850192)

* Thu Aug 23 2012 Petr Šabata <contyk@redhat.com> - 0.9.45-2
- Fix displaying of the Management Address TLV (327ef662)

* Wed Aug 15 2012 Petr Šabata <contyk@redhat.com> - 0.9.45-1
- 0.9.45 bump
- Provide bash-completion and the new clif library

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Petr Šabata <contyk@redhat.com> - 0.9.44-1
- 0.9.44 bump, patches cleanup
- Correct dependencies a bit
- Require dlopen()'d readline

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.43-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 06 2011 Petr Sabata <contyk@redhat.com> - 0.9.43-5
- Do not enable lldpad by default (#701999)

* Fri Sep 23 2011 Petr Sabata <contyk@redhat.com> - 0.9.43-4
- Enable hardened build

* Tue Sep 13 2011 Petr Sabata <contyk@redhat.com> - 0.9.43-3
- Mute systemd output (#737897)

* Tue Aug 30 2011 Petr Sabata <contyk@redhat.com> - 0.9.43-2
- Apply various upstream 0.9.43 bugfixes
- Include not yet accepted Jens Osterkamp's patch to fix bug #720080
- Whitespace cleanup, phew

* Thu Jul 07 2011 Petr Sabata <contyk@redhat.com> - 0.9.43-1
- 0.9.43 bump
- Drop the the clean exit patch and our unit file, both are now included upstream

* Tue Jun 21 2011 Petr Sabata <contyk@redhat.com> - 0.9.42-2
- Introduce systemd unit file, drop SysV support
- Call systemctl instead of service and chkconfig
- Enable the service only on new installation (post)
- Clean exit patch

* Mon Jun 13 2011 Petr Sabata <contyk@redhat.com> - 0.9.42-1
- 0.9.42 bump (massive patches cleanup)
- Remove obsolete defattr
- Remove COPYING and README from devel subpackage

* Wed May  4 2011 Petr Sabata <psabata@redhat.com> - 0.9.41-3
- Fix the frequent, power consuming lldpad wake-ups (rhbz#701943)

* Thu Apr 21 2011 Petr Sabata <psabata@redhat.com> - 0.9.41-2
- Bring in upstream 802.1Qbg bugfixes

* Thu Feb 10 2011 Petr Sabata <psabata@redhat.com> - 0.9.41-1
- 0.9.41 bump
- New BR: autotools, flex
- Buildroot garbage removed
- Devel post and preun scriptlets sanitized

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jun 28 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.38-1
- rebased to 0.9.38 (various enhancements and bugfixes, see 
  lldpad-0.9.38-relnotes.txt on http://e1000.sf.net for complete list)

* Mon May 10 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.32-2
- rebuild to match new libconfig

* Mon Apr 12 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.32-1
- rebased to 0.9.32 (various enhancements and bugfixes, see 
  lldpad-0.9.32-relnotes.txt on http://e1000.sf.net for complete list)

* Thu Mar 25 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.29-2
- added Provides and Obsoletes tags to devel subpackage

* Mon Mar 15 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.29-1
- updated package to 0.9.29, improved compatibility with fcoe-utils

* Fri Feb 26 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.26-2
- updated spec file and LSB init script patch for re-review
  (#568641)

* Thu Feb 25 2010 Jan Zeleny <jzeleny@redhat.com> - 0.9.26-1
- rebased to 0.9.26
- package renamed to lldpad
- enahanced functionality (LLDP supported as well as DCBX)

* Fri Nov 13 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.19-2
- init script patch adding LSB compliance

* Thu Oct 08 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.19-1
- update to new upstream version

* Mon Oct 05 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.15-5
- replaced the last patch, which was not fully functional, with
  the new one

* Wed Sep 09 2009 Karsten Hopp <karsten@redhat.com> 0.9.15-4
- buildrequire libconfig-devel >= 1.3.2, it doesn't build with 1.3.1 due to
  the different config_lookup_string api

* Thu Aug 20 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.15-3
- update of config_lookup_string() function calls

* Thu Aug 20 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.15-2
- rebuild in order to match new libconfig

* Mon Aug 17 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.15-1
- rebase to 0.9.15

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 20 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.7-4
- updated scriptlets in spec file to follow the rules

* Wed Mar 11 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.7-3
- added devel files again to support fcoe-utils package
- added kernel >= 2.6.29 to Requires, deleted dcbnl.h, since it is
  aviable in kernel 2.6.29-rc7
- changed config dir from /etc/sysconfig/dcbd to /etc/dcbd
- updated init script: added mandatory Short description tag,
  deleted default runlevels, which should start the script

* Tue Mar 10 2009 Jan Zeleny <jzeleny@redhat.com> - 0.9.7-2
- added patch to enable usage of libconfig shared in system
- removed devel part of package

* Mon Mar 2 2009 Chris Leech <christopher.leech@intel.com> - 0.9.7-1
- Updated to 0.9.7
- Added a private copy of dcbnl.h until kernel-headers includes it.
  Export patch is making it's way to the upstream kernel via net-2.6,
  expected in 2.6.29-rc7

* Thu Feb 26 2009 Chris Leech <christopher.leech@intel.com> - 0.9.5-1
- initial RPM packaging
