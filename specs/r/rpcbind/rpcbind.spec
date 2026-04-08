# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# These are macros to be usable outside of the build section
%global rpcbind_user_group rpc
%global rpcbind_state_dir %{_rundir}/rpcbind

Name:           rpcbind
Version:        1.2.8
Release:        0%{?dist}
Summary:        Universal Addresses to RPC Program Number Mapper
License:        BSD-3-Clause
URL:            http://nfsv4.bullopensource.org

Source0:        http://downloads.sourceforge.net/rpcbind/%{name}-%{version}.tar.bz2
Source1: %{name}.sysconfig

Requires: glibc-common setup
Requires: libtirpc >= 1.3.5
Conflicts: man-pages < 2.43-12
BuildRequires: make
BuildRequires: automake, autoconf, libtool, systemd, systemd-devel
BuildRequires: libtirpc-devel, quota-devel
Requires(pre): coreutils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd coreutils

Patch100: rpcbind-0.2.3-systemd-tmpfiles.patch
Patch101: rpcbind-0.2.4-systemd-rundir.patch

Provides: portmap = %{version}-%{release}
Obsoletes: portmap <= 4.0-65.3

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires: filesystem(unmerged-sbin-symlinks)
Provides: /usr/sbin/rpcbind
Provides: /usr/sbin/rpcinfo
%endif

%description
The rpcbind utility is a server that converts RPC program numbers into
universal addresses.  It must be running on the host to be able to make
RPC calls on a server on that machine.

%prep
%autosetup -p1

# Create a sysusers.d config file
cat >rpcbind.sysusers.conf <<EOF
u rpc 32 'Rpcbind Daemon' /var/lib/rpcbind -
EOF

%build
autoreconf -fisv
%configure \
    --enable-warmstarts \
    --with-statedir="%rpcbind_state_dir" \
    --with-rpcuser="%rpcbind_user_group" \
    --with-nss-modules="files altfiles" \
    --sbindir=%{_bindir} \
    --enable-rmtcalls \
    --enable-debug

make all

%install
mkdir -p %{buildroot}{%{_sbindir},%{_bindir},/etc/sysconfig}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_tmpfilesdir}
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{rpcbind_state_dir}
make DESTDIR=$RPM_BUILD_ROOT install

install -m644 %{SOURCE1} %{buildroot}/etc/sysconfig/rpcbind

%if "%{_sbindir}" != "%{_bindir}"
# The binaries now live in /usr/bin, moving from /usr/sbin
# For compatibility create a couple symlinks. 
cd ${RPM_BUILD_ROOT}%{_sbindir}
ln -sf ../bin/rpcbind
ln -sf ../bin/rpcinfo
%endif

install -m0644 -D rpcbind.sysusers.conf %{buildroot}%{_sysusersdir}/rpcbind.conf

%post
%systemd_post rpcbind.service rpcbind.socket

%preun
%systemd_preun rpcbind.service rpcbind.socket

# NOTE: We only restart rpcbind.socket in the %postun scriptlet in order to
# avoid the race described in:
#
# https://github.com/systemd/systemd/issues/13271
# https://github.com/systemd/systemd/issues/8102
#
# Restarting rpcbind.socket causes rpcbind.service to be restarted automatically
# due to "Requires=rpcbind.socket" in the rpcbind.service unit file.
%postun
%systemd_postun_with_restart rpcbind.socket

%files
%license COPYING
%config(noreplace) /etc/sysconfig/rpcbind
%doc AUTHORS ChangeLog README
%{_bindir}/rpcbind
%{_bindir}/rpcinfo
%if "%{_sbindir}" != "%{_bindir}"
%{_sbindir}/rpcbind
%{_sbindir}/rpcinfo
%endif
%{_mandir}/man8/*
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
%{_tmpfilesdir}/%{name}.conf
%attr(0700, %{rpcbind_user_group}, %{rpcbind_user_group}) %dir %{rpcbind_state_dir}
%{_sysusersdir}/rpcbind.conf

%changelog
* Sat Jul 26 2025 Steve Dickson <steved@redhat.com> 1.2.8-0
- Updated to latest upstream release: rpcbind-1_2_8 (bz 2300081)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-2.rc1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed May  7 2025 Scott Mayhew <smayhew@redhat.com> - 1.2.7-2.rc1
- Fix rpm scriptlets to remove excessive restarts during upgrade

* Wed Jan 29 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.7-1.rc1.4
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-1.rc1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Panu Matilainen <pmatilai@redhat.com> - 1.2.7-1.rc1.2
- Add provides for the manually created rpc user and group

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.7-1.rc1.1
- Rebuilt for the bin-sbin merge (2nd attempt)

* Mon Sep 9 2024 Steve Dickson <steved@redhat.com> 1.2.8-rc1
- Updated to latest upstream RC release: rpcbind-1_2_8-rc1

* Tue Aug 13 2024 Steve Dickson <steved@redhat.com> 1.2.7-1
- Added Requirement for libtirpc (bz 2304327)

* Thu Jul 25 2024 Steve Dickson <steved@redhat.com> 1.2.7-0
- Updated to latest upstream release: rpcbind-1_2_7

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-5.rc3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Apr 11 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.6-5.rc3
- Prepare for bin-sbin merge
  (https://fedoraproject.org/wiki/Changes/Unify_bin_and_sbin)

* Mon Mar 18 2024 Steve Dickson <steved@redhat.com> 1.2.6-4.rc3
- Updated to latest upstream RC release: rpcbind-1_2_7-rc3

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-4.rc2.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-4.rc2.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 16 2023 Pavel Reichl <preichl@redhat.com> - 1.2.6-4.rc2.2
- Convert License tag to SPDX format

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-4.rc2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 28 2023 Steve Dickson <steved@redhat.com> 1.2.6-4.rc2
- Updated to latest upstream RC release: rpcbind-1_2_7-rc2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Steve Dickson <steved@redhat.com> 1.2.6-0
- Updated to latest upstream release: rpcbind-1_2_6 (bz 1959127)

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.5-5.rc1.5
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-5.rc1.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-5.rc1.3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-5.rc1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-5.rc1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 11 2019 Steve Dickson <steved@redhat.com> - 1.2.5-5.rc1
- Updated to latest upstream RC release: rpcbind-1_2_5-rc1 (bz 1431574)

* Thu Sep 19 2019 Steve Dickson <steved@redhat.com> - 1.2.5-5
- Enable remote calls which are used by NIS and other packages (bz 1630672)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.5-2
- Drop old sys-v migration bits
- Ship the license file, minor spec cleanups

* Tue Oct  9 2018 Steve Dickson <steved@redhat.com> - 1.2.5-1
- Fixed stack buffer overflow in rpcinfo (bz 1637562)

* Wed Aug 15 2018 Steve Dickson <steved@redhat.com> - 1.2.5-0
- Updated to latest upstream release: 1_2_5

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-10.rc3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Feb 24 2018 Florian Weimer <fweimer@redhat.com> - 0.2.4-10.rc3
- Use default build flags from redhat-rpm-config

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-9.rc3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 18 2017 Steve Dickson <steved@redhat.com> - 0.2.4-9.rc3
- Removed tcp_wrappers dependency (bz 1518780)

* Sat Dec 16 2017 Steve Dickson <steved@redhat.com> - 0.2.4-8.rc3
- Updated to latest upstream RC release: rpcbind-0_2_5-rc3 (bz 1431574)

* Wed Sep 06 2017 Nils Philippsen <nils@redhat.com> - 0.2.4-8.rc2
- create and formally own the state directory so it is available from the time
  of first installation until reboot

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-7.rc2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-7.rc2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 30 2017 Steve Dickson <steved@redhat.com> - 0.2.4-7.rc2
- Updated to latest upstream RC release: rpcbind-0_2_5-rc2  (bz 1450765)

* Mon May 15 2017 Steve Dickson <steved@redhat.com> - 0.2.4-7.rc1
- Fixed typo in memory leaks patch (bz 1448128)

* Thu May 11 2017 Steve Dickson <steved@redhat.com> - 0.2.4-6.rc1
- Fixed memory leaks (bz 1448128)

* Tue Mar 21 2017 Steve Dickson <steved@redhat.com> - 0.2.4-6
- Try creating statdir once when opening lock file fails (bz 1401561)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Steve Dickson <steved@redhat.com> - 0.2.4-4
- Corrected boot dependency in systemd files (bz 1401561)

* Mon Jan 23 2017 Steve Dickson <steved@redhat.com> - 0.2.4-3
- Create a systemd dependency for tmpfiles-setup.service (bz 1401561)

* Mon Jan 16 2017 Steve Dickson <steved@redhat.com> - 0.2.4-2
- Document /run/rpcbind is the state directory (bz 1401561)

* Tue Jan  3 2017 Steve Dickson <steved@redhat.com> - 0.2.4-1
- Fix boot dependency in systemd service file (bz 1401561)

* Wed Nov 30 2016 Steve Dickson <steved@redhat.com> - 0.2.4-0
- Update to the latest upstream release: 0.2.4

* Sat Nov 19 2016 Steve Dickson <steved@redhat.com> - 0.2.3-13.rc2
- Create the statedir under /run/rpcbind by systemd-tmpfiles.

* Sat Nov 12 2016 Steve Dickson <steved@redhat.com> - 0.2.3-12.rc2
- Stop enable rpcbind.socket with every update (bz 1393721)

* Mon Nov  7 2016 Steve Dickson <steved@redhat.com> - 0.2.3-11.rc2
- Updated to the latest RC release rpcbind-0_2_4-rc1

* Mon Aug  1 2016 Steve Dickson <steved@redhat.com> - 0.2.3-11.rc1
- Removing the braces from the ${RPCBIND_ARGS} in rpcbind.service (bz 1362201)
- Stop enable rpcbind.socket with every update (bz 1324666)

* Mon Apr  4 2016 Steve Dickson <steved@redhat.com> - 0.2.3-10.rc1
- Restart rpcbind.socket on restarts (bz 1306824)
- Soft static allocate rpc uid/gid (bz 1301288)

* Sat Feb 20 2016 Steve Dickson <steved@redhat.com> - 0.2.3-9.rc1
- Updated to the latest RC release rpcbind-0_2_4-rc1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Steve Dickson <steved@redhat.com> - 0.2.3-7
- Delete the unix socket only if we have created it (bz 1279076)

* Tue Nov  3 2015 Steve Dickson <steved@redhat.com> - 0.2.3-0.6
- handle_reply: Don't use the xp_auth pointer directly

* Mon Nov  2 2015 Steve Dickson <steved@redhat.com> - 0.2.3-0.5
- Support nss-altfiles by adding 'altfiles' to nss lookup path (bz 1159941).

* Mon Nov  2 2015 Steve Dickson <steved@redhat.com> - 0.2.3-0.4
- Fixed Seg fault in PMAP_CALLIT code (bz1264351)

* Sun Nov 01 2015 Kalev Lember <klember@redhat.com> - 0.2.3-0.3
- Rebuilt for libtirpc soname bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Steve Dickson <steved@redhat.com> - 0.2.3-0.0
- Make sure rpcbind.socket always gets enabled (bz 1214496)

* Tue Apr 28 2015 Steve Dickson <steved@redhat.com> - 0.2.3-0.0
- Updated to latest upstream release: 0.2.3
- Change RPCBDIR to be /tmp since that will exist after a 
  reboot and bindings wil be perserved during upgrades
  but not reboots.

* Thu Mar 19 2015 Steve Dickson <steved@redhat.com> - 0.2.2-2.2
- Changed RPCBDIR to be /var/run so bindings are perserved
  during upgrades but not reboots.
- Make sure rpcbind.socket gets enabled

* Thu Feb  5 2015 Steve Dickson <steved@redhat.com> - 0.2.2-2.1
- Added xlogging debugging to rpcbind

* Wed Feb  4 2015 Steve Dickson <steved@redhat.com> - 0.2.2-2.0
- Updated to the latest rc release: rpcbind-0_2_3-rc1 (bz 1095021)

* Wed Dec 17 2014 Steve Dickson <steved@redhat.com> - 0.2.2-1.1
- Fixed NULL fp problem remove error message on warmstart patch

* Tue Dec 16 2014 Steve Dickson <steved@redhat.com> - 0.2.2-1.0
- Updated to the latest rc release: rpcbind-0_2_3-rc1

* Wed Nov 26 2014 Steve Dickson <steved@redhat.com> - 0.2.2-0.0
- Updated to the latest upstream release: 0.2.2 (bz 747363)
- Added BuildRequires systemd-compat-libs

* Mon Nov 10 2014 Steve Dickson <steved@redhat.com> - 0.2.1-4.0
- Updated to the latest rc release: rpcbind-0_2_2-rc3

* Mon Oct 27 2014 Steve Dickson <steved@redhat.com> - 0.2.1-3.0
- Updated to the latest rc release: rpcbind-0_2_2-rc2 (bz 1015283)

* Thu Oct 23 2014 Steve Dickson <steved@redhat.com> - 0.2.1-2.1
- Stop re-enabling with systemd (bz 1087951)

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 0.2.1-2.0
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Steve Dickson <steved@redhat.com> - 0.2.1-1.0
- Updated to the latest rc release: rpcbind-0_2_2-rc1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec  2 2013 Steve Dickson <steved@redhat.com> - 0.2.1-0.2
- Removed unnecessary targets from rpcbind.service (bz 963189)

* Wed Aug 21 2013 Steve Dickson <steved@redhat.com> - 0.2.1-0.1
- Fixed typo in configure.ac file causing rpcuser not to be set.

* Mon Aug 19 2013 Steve Dickson <steved@redhat.com> - 0.2.1-0
- Update to the latest upstream release: 0.2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Steve Dickson <steved@redhat.com> - 0.2.0-20
- Update to the latest upstream release: rpcbind-0_2_1-rc4 (bz 869365)

* Tue Oct 16 2012 Steve Dickson <steved@redhat.com> - 0.2.0-19
- Renamed RPCBINDOPTS to RPCBIND_ARGS for backward compatibility (bz 861025)

* Sun Oct 14 2012 Steve Dickson <steved@redhat.com> - 0.2.0-18
- Fixed typo causing rpcbind to run as root (bz 734598)
- Added /etc/sysconfig/rpcbind config file (bz 861025)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 12 2011 Steve Dickson <steved@redhat.com> - 0.2.0-15
- Bumped up the tigger version to this version, 0.2.0-15 (bz 713574)

* Fri Sep  9 2011 Tom Callaway <spot@fedoraproject.org> - 0.2.0-14
- fix scriptlets to enable service by default

* Fri Jul  8 2011 Steve Dickson <steved@redhat.com> - 0.2.0-13
- Spec file clean up

* Thu Jul  7 2011 Steve Dickson <steved@redhat.com> - 0.2.0-12
- Migrated SysV initscripts to systemd (bz 713574)

* Thu Mar 17 2011 Steve Dickson <steved@redhat.com> - 0.2.0-11
- Updated to the latest upstream release: rpcbind-0_2_1-rc3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Steve Dickson <steved@redhat.com> - 0.2.0-9
- Fixed an incorrect exit code for service rpcbind status (bz 662411)

* Tue Nov 30 2010 Steve Dickson <steved@redhat.com> - 0.2.0-8
- Updated to the latest upstream release: rpcbind-0.2.1-rc2

* Fri Jul 16 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.2.0-7
- correct license tag to BSD

* Tue Jul 13 2010 Steve Dickson <steved@redhat.com> - 0.2.0-6
- Made initscript LSB compliant (bz 614193)
- Added no fork patch

* Tue Jul  6 2010 Steve Dickson <steved@redhat.com> - 0.2.0-5
- Set SO_REUSEADDR on listening sockets (bz 597356)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Adam Jackson <ajax@redhat.com> 0.2.0-3
- Requires(pre): coreutils for cut(1).

* Thu Jun 25 2009 Steve Dickson <steved@redhat.com> - 0.2.0-2
- Fixed pre scriptle failure during upgrades (bz 507364)
- Corrected the usage info to match what the rpcbind man
    page says. (bz 466332)
- Correct package issues (bz 503508)

* Fri May 29 2009 Steve Dickson <steved@redhat.com> - 0.2.0-1
- Updated to latest upstream release: 0.2.0

* Tue May 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.1.7-3
- Replace the Sun RPC license with the BSD license, with the explicit permission of Sun Microsystems

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 19 2008 Steve Dickson <steved@redhat.com>  0.1.7-1
- Update to latest upstream release: 0.1.7

* Tue Sep 30 2008 Steve Dickson <steved@redhat.com>  0.1.6-3
- Fixed a typo in the rpcbind.init script that stop warm starts
  from happening with conrestarts
- Fixed scriptlet failure (bz 462533)

* Tue Sep 16 2008 Steve Dickson <steved@redhat.com> 0.1.6-2
- Added usptream patches 01 thru 03 that do:
    * Introduce helpers for ipprot/netid mapping
    * Change how we decide on the netids to use for portmap
    * Simplify port live check in pmap_svc.c

* Wed Jul  9 2008 Steve Dickson <steved@redhat.com> 0.1.6-1
- Updated to latest upstream release 0.1.6

* Wed Jul  2 2008 Steve Dickson <steved@redhat.com> 0.1.5-5
- Fixed SYNOPSIS section in the rpcinfo man page (bz 453729)

* Fri Jun 27 2008 Steve Dickson <steved@redhat.com> 0.1.5-4
- Removed the documentation about the non-existent 
  '-L' flag (bz 446915)

* Fri Jun 27 2008 Steve Dickson <steved@redhat.com> 0.1.5-3
- Set password and service lookups to be local (bz 447092)

* Mon Jun 23 2008 Steve Dickson <steved@redhat.com> 0.1.5-2
- rpcbind needs to downgrade to non-priviledgied group.

* Mon Jun 23 2008 Steve Dickson <steved@redhat.com> 0.1.5-1
- Updated to latest upstream release 0.1.5

* Mon Feb 11 2008 Steve Dickson <steved@redhat.com> 0.1.4-14
- Fixed a warning in pmap_svc.c
- Cleaned up warmstarts so uid are longer needed, also
  changed condrestarts to use warmstarts. (bz 428496)

* Thu Jan 24 2008 Steve Dickson <steved@redhat.com> 0.1.4-13
- Fixed connectivity with Mac OS clients by making sure handle_reply()
  sets the correct fromlen in its recvfrom() call (bz 244492)

* Mon Dec 17 2007 Steve Dickson <steved@redhat.com> 0.1.4-12
- Changed is_loopback() and check_access() see if the calling
  address is an address on a local interface, just not a loopback
  address (bz 358621).

* Wed Oct 17 2007 Steve Dickson <steved@redhat.com> 0.1.4-11
- Reworked logic in initscript so the correct exit is 
  used when networking does not exist or is set up
  incorrectly.

* Tue Oct 16 2007 Steve Dickson <steved@redhat.com> 0.1.4-10
- Corrected a typo in the initscript from previous 
  commit.

* Mon Oct 15 2007 Steve Dickson <steved@redhat.com> 0.1.4-9
- Fixed typo in Summary (bz 331811)
- Corrected init script (bz 247046)

* Sat Sep 15 2007 Steve Dickson <steved@redhat.com> 0.1.4-8
- Fixed typo in init script (bz 248285)
- Added autoconf rules to turn on secure host checking
  via libwrap. Also turned on host check by default (bz 248284)
- Changed init script to start service in runlevel 2 (bz 251568)
- Added a couple missing Requires(pre) (bz 247134)

* Fri May 25 2007 Steve Dickson <steved@redhat.com> 0.1.4-7
- Fixed condrestarts (bz 241332)

* Tue May 22 2007 Steve Dickson <steved@redhat.com> 0.1.4-6
- Fixed an ipv6 related segfault on startup (bz 240873)

* Wed Apr 18 2007 Steve Dickson <steved@redhat.com> 0.1.4-5
- Added dependency on setup which contains the correct
  rpcbind /etc/service entry which in turns stops 
  rpcbind from haning when NIS is enabled. (bz 236865)

* Wed Apr 11 2007 Jeremy Katz <katzj@redhat.com> - 0.1.4-4
- change man-pages requires into a conflicts as we don't have to have 
  man-pages installed, but if we do, we need the newer version

* Fri Apr  6 2007 Steve Dickson <steved@redhat.com> 0.1.4-3
- Fixed the Provides and Obsoletes statments to correctly
  obsolete the portmap package.
* Tue Apr  3 2007 Steve Dickson <steved@redhat.com> 0.1.4-2
- Added dependency on glibc-common which allows the
  rpcinfo command to be installed in the correct place.
- Added dependency on man-pages so the rpcinfo man 
  pages don't conflict.
- Added the creation of /var/lib/rpcbind which will be
  used to store state files.
- Make rpcbind run with the 'rpc' uid/gid when it exists.

* Wed Feb 21 2007 Steve Dickson <steved@redhat.com> 0.1.4-1
- Initial commit
- Spec reviewed (bz 228894)
- Added the Provides/Obsoletes which should
  cause rpcbind to replace portmapper
