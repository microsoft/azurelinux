Summary:        The NIS (Network Information Service) server
Name:           ypserv
Version:        4.2
Release:        12%{?dist}
License:        GPL-2.0-only
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.thkukuk.de/nis/nis/ypserv/

Source0: https://github.com/thkukuk/ypserv/archive/refs/tags/v4.2.tar.gz#/%{name}-%{version}.tar.gz
Source1: ypserv.service
Source2: yppasswdd.service
Source3: ypxfrd.service
Source4: rpc.yppasswdd.env
Source5: yppasswdd-pre-setdomain

Requires: gawk, make, portmap, bash >= 2.0
Requires: tokyocabinet
# requirement for domainname
Requires(pre): hostname
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Patch0: ypserv-2.5-redhat.patch
Patch2: ypserv-2.5-nfsnobody2.patch
Patch3: ypserv-2.13-ypxfr-zeroresp.patch
Patch4: ypserv-2.13-nonedomain.patch
Patch5: ypserv-2.19-slp-warning.patch
Patch6: ypserv-4.0-manfix.patch
Patch7: ypserv-2.24-aliases.patch
Patch8: ypserv-2.27-confpost.patch
Patch10: ypserv-2.31-netgrprecur.patch
Patch12: ypserv-4.0-headers.patch
Patch14: ypserv-4.0-selinux-context.patch
Patch15: ypserv-4.2-implicit-int.patch

BuildRequires: make
BuildRequires:  gcc
BuildRequires: tokyocabinet-devel
BuildRequires: systemd
BuildRequires: autoconf, automake
BuildRequires: systemd-devel
BuildRequires: libnsl2-devel
BuildRequires: libtirpc-devel
BuildRequires: docbook-style-xsl
BuildRequires: libxslt
BuildRequires: libselinux-devel

%description
The Network Information Service (NIS) is a system that provides
network information (login names, passwords, home directories, group
information) to all of the machines on a network. NIS can allow users
to log in on any machine on the network, as long as the machine has
the NIS client programs running and the user's password is recorded in
the NIS passwd database. NIS was formerly known as Sun Yellow Pages
(YP).

This package provides the NIS server, which will need to be running on
your network. NIS clients do not need to be running the server.

Install ypserv if you need an NIS server for your network. You also
need to install the yp-tools and ypbind packages on any NIS client
machines.

%prep
%autosetup -n %{name}-%{version} -p1

# Delete generated man pages. They will be generated later from source.
rm makedbm/makedbm.8
rm mknetid/mknetid.8
rm etc/netgroup.5
rm etc/ypserv.conf.5

autoreconf -i

%build
cp etc/README etc/README.etc
%ifarch s390 s390x
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%else
export CFLAGS="$RPM_OPT_FLAGS -fpic"
%endif

# Fix gcc12 issues (#2047138)
export CFLAGS="$CFLAGS -Wno-format-overflow"

%configure \
    --enable-checkroot \
    --enable-fqdn \
    --libexecdir=%{_libdir}/yp \
    --with-dbmliborder=tokyocabinet \
    --localstatedir=%{_localstatedir} \
    --with-selinux

make

%install
%make_install
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
install -m 644 etc/ypserv.conf $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/ypserv.service
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_unitdir}/yppasswdd.service
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/ypxfrd.service
install -m 755 %{SOURCE5} $RPM_BUILD_ROOT%{_libexecdir}/yppasswdd-pre-setdomain

mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
cat >$RPM_BUILD_ROOT/etc/sysconfig/yppasswdd <<EOF
# The passwd and shadow files are located under the specified
# directory path. rpc.yppasswdd will use these files, not /etc/passwd
# and /etc/shadow.
#ETCDIR=/etc

# This option tells rpc.yppasswdd to use a different source file
# instead of /etc/passwd
# You can't mix usage of this with ETCDIR
#PASSWDFILE=/etc/passwd

# This option tells rpc.yppasswdd to use a different source file
# instead of /etc/passwd.
# You can't mix usage of this with ETCDIR
#SHADOWFILE=/etc/shadow

# Additional arguments passed to yppasswd
YPPASSWDD_ARGS=
EOF

# We need to pass all environment variables set in /etc/sysconfig/yppasswdd
# only if they are not empty. However, this simple logic is not supported
# by systemd. The script rpc.yppasswdd.env wraps the main binary and
# prepares YPPASSWDD_ARGS variable to include all necessary variables
# (ETCDIR, PASSWDFILE and SHADOWFILE). The script ensures, that the
# rpc.yppasswdd arguments are not used when the appropriate environment
# variables are empty.
install -m 755 %{SOURCE4} $RPM_BUILD_ROOT%{_libexecdir}/rpc.yppasswdd.env

%post
%systemd_post ypserv.service
%systemd_post ypxfrd.service
%systemd_post yppasswdd.service

%preun
%systemd_preun ypserv.service
%systemd_preun ypxfrd.service
%systemd_preun yppasswdd.service

%postun
%systemd_postun_with_restart ypserv.service
%systemd_postun_with_restart ypxfrd.service
%systemd_postun_with_restart yppasswdd.service

%files
%doc AUTHORS README INSTALL ChangeLog TODO NEWS COPYING
%doc etc/ypserv.conf etc/securenets etc/README.etc
%doc etc/netgroup etc/locale etc/netmasks etc/timezone
%config(noreplace) %{_sysconfdir}/ypserv.conf
%config(noreplace) %{_sysconfdir}/sysconfig/yppasswdd
%config(noreplace) /var/yp/*
%{_unitdir}/*
%{_libexecdir}/*
%{_libdir}/yp/*
%{_sbindir}/*
%{_mandir}/*/*
%{_includedir}/rpcsvc

%changelog
* Fri Mar 14 2025 Jyoti kanase <v-jykanase@microsoft.com> - 4.2-12
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 30 2024 Ondrej Sloup <osloup@redhat.com> - 4.2-10
- Don't hard code _FORTIFY_SOURCE=2
- Update license tag to the SPDX format (GPL-2.0-only)

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 01 2022 Timm Bäder <tbaeder@redhat.com> - 4.2-6
- Get rid of an implicit int during configure time
- See https://fedoraproject.org/wiki/Changes/PortingToModernC

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Feb 01 2022 Marek Kulik <mkulik@redhat.com> - 4.2-4
- Fix gcc12 compilation issues
- Resolves: #2047138

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 Björn Esser <besser82@fedoraproject.org> - 4.2-2
- Rebuild(libnsl2)

* Tue Sep 28 2021 Marek Kulik <mkulik@redhat.com> - 4.2-1
- Update to new upstream version 4.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.1-6
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 19 2019 Matej Mužila <mmuzila@redhat.com> - 4.1-1
- Update to new upstream version 4.1

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-15.20180831git326857e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 4.0-14.20180831git326857e
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Aug 31 2018 Petr Kubat <pkubat@redhat.com> - 4.0-13.20180831git326857e
- Rebase ypserv to latest upstream commit

* Fri Jul 20 2018 Matej Mužila <mmuzila@redhat.com> - 4.0-12.20170331git5bfba76
- rpc.yppasswd: presserve selinux context of shadow and passwd
- Resolves: #1255583

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-11.20170331git5bfba76
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Matej Mužila <mmuzila@redhat.com> - 4.0-10.20170331git5bfba76
- Remove trailing whitespaces from spec

* Tue Jun 12 2018 Matej Mužila <mmuzila@redhat.com> - 4.0-9.20170331git5bfba76
- Drop map rebuild (gdbm -> tokyocabinet) support

* Mon Jun 11 2018 Matej Mužila <mmuzila@redhat.com> - 4.0-8.20170331git5bfba76
- Clean spec

* Mon Jun 11 2018 Matej Mužila <mmuzila@redhat.com> - 4.0-7.20170331git5bfba76
- Remove no longer needed relro patch
- Fix man pages

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-6.20170331git5bfba76
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 4.0-5.20170331git5bfba76
- Rebuilt for switch to libxcrypt

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-4.20170331git5bfba76
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-3.20170331git5bfba76
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 6 2017 Matej Mužila <mmuzila@redhat.com> - 4.0-2.20170331git5bfba76
- Rebase to ypserv 4.0
- Added IPv6 support

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.32.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Sep 05 2014 Honza Horak <hhorak@redhat.com> - 2.32.1-5
- Require hostname for domainname in pre
  Do not crash in pre if /etc/sysconfig/network is missing

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 2.32.1-4
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Honza Horak <hhorak@redhat.com> - 2.32.1-2
- Link with systemd.so

* Tue Aug 12 2014 Honza Horak <hhorak@redhat.com> - 2.32.1-1
- New upstream release 2.32.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.32-2
- Own %%{_includedir}/rpcsvc (RHBZ #1100354).

* Mon Nov 18 2013 Honza Horak <hhorak@redhat.com> - 2.32-1
- Update to new upstream version 2.32

* Wed Sep  4 2013 Honza Horak <hhorak@redhat.com> - 2.31-5
- Return proper error code when map file opening did not succeeded
  RHBZ#1004110
- Read MINUID and MINGID values from /etc/login.defs
  RHBZ#1004090

* Mon Jul 29 2013 Honza Horak <hhorak@redhat.com> - 2.31-4
- Remove systemd-units and systemd-sysv requirements
- Clean-up SysV init conversion code
- Clean-up systemd preset macros compatibility code

* Mon May 27 2013 Honza Horak <hhorak@redhat.com> - 2.31-3
- Fix crash when netgroups include recursive dependency

* Thu May 09 2013 Honza Horak <hhorak@redhat.com> - 2.31-2
- Enable PrivateTmp feature, just for the case

* Mon May 06 2013 Honza Horak <hhorak@redhat.com> - 2.31-1
- Update to new upstream version

* Mon Feb 04 2013 Honza Horak <hhorak@redhat.com> - 2.29-8
- Stop ypserv daemon temporary when reading info about maps

* Mon Jan 28 2013 Honza Horak <hhorak@redhat.com> - 2.29-7
- Open maps with no blocking for reading

* Mon Jan 21 2013 Honza Horak <hhorak@redhat.com> - 2.29-6
- Open database files with correct mode
- Make rebuilding maps during upgrade a bit more clever

* Fri Nov 30 2012 Honza Horak <hhorak@redhat.com> - 2.29-5
- Build daemons and yppush with full relro
- Move rpc.yppasswdd.env into /usr/libexec

* Fri Nov 09 2012 Honza Horak <hhorak@redhat.com> - 2.29-4
- Add missing break in switch

* Thu Oct 04 2012 Honza Horak <hhorak@redhat.com> - 2.29-3
- Run %%triggerun regardless of systemd_post variable definition

* Mon Sep 24 2012 Honza Horak <hhorak@redhat.com> - 2.29-2
- Use new systemd macros
  Resolves: #850376

* Mon Sep 03 2012 Honza Horak <hhorak@redhat.com> - 2.29-1
- Update to new upstream version that fix memory leaks (Related: #845283)
- Use sdnotify to inform systemd that daemons are ready
- Some minor spec file clean up
- Added systemd-devel as a build requirement

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Honza Horak <hhorak@redhat.com> - 2.28-2
- Minor spec file fixes
- Helper scripts moved to /usr/libexec

* Mon Jun 04 2012 Honza Horak <hhorak@redhat.com> - 2.28-1
- Update to new upstream version, which fixes several bugs
- Use Tokyo Cabinet as DBM and rebuild maps after updating
- Consider NISDOMAIN variable from /etc/sysconfig/network

* Mon May 14 2012 Honza Horak <hhorak@redhat.com> - 2.27-5
- Checking if domainname is set moved from ypserv.service
  to yppasswdd.service
  Related: #456249

* Thu Apr 26 2012 Honza Horak <hhorak@redhat.com> - 2.27-4
- Build against qdbm and rebuild maps after updating

* Thu Apr 26 2012 Honza Horak <hhorak@redhat.com> - 2.27-3
- Added patch to handle crypt() returning NULL

* Fri Apr 13 2012 Honza Horak <hhorak@redhat.com> - 2.27-2
- Use O_CLOEXEC when opening pid file to avoid SELinux issues
  Resolves: #809120

* Wed Feb 01 2012 Honza Horak <hhorak@redhat.com> - 2.27-1
- Update to new upstream version, which fixes several bugs
  (removing patches that aren't needed any more)

* Thu Jan 12 2012 Honza Horak <hhorak@redhat.com> - 2.26-10
- Added ypserv-pre-setdomain to respect NISDOMAIN environment variable
  and set domainname if empty
- Added autoreconf call (thus .path patch modified to keep impact)
- Patch .aliases fixed
  Resolves: #699826

* Mon Dec 12 2011 Honza Horak <hhorak@redhat.com> - 2.26-9
- Rebuild against compat_gdbm, because gdbm has changed license
  to GPLv3+ and it is not compatible with ypserv GPLv2

* Mon Nov 28 2011 Honza Horak <hhorak@redhat.com> - 2.26-8
- Fixed returning success when shadow file is not writable
  Resolves: #747335

* Fri Nov 25 2011 Honza Horak <hhorak@redhat.com> - 2.26-7
- Fixed empty domain handling in ypinit script
  Resolves: #751427
- Added a wrapper script to use all variables correctly in the unit file
  Resolves: #755775

* Mon Oct 10 2011 Honza Horak <hhorak@redhat.com> - 2.26-6
- Made error messages in yppasswdd more accurate
  Resolves: #695754

* Fri Sep 30 2011 Honza Horak <hhorak@redhat.com> - 2.26-5
- Rebuild with new gdbm-1.9.1

* Fri Sep 30 2011 Honza Horak <hhorak@redhat.com> - 2.26-4
- Added passwd.adjunct support in yppasswdd to recognize
  password format correctly when changing password using yppasswd
  Resolves: #699667

* Wed Aug 31 2011 Honza Horak <hhorak@redhat.com> - 2.26-3
- fixed hiding the change request when external script is used
  in rpc.yppasswdd

* Wed Aug 03 2011 Honza Horak <hhorak@redhat.com> - 2.26-2
- fixed systemd unit files requires and description

* Tue Aug 02 2011 Honza Horak <hhorak@redhat.com> - 2.26-1
- Update to new upstream version
  Simplified systemd snippets in spec file

* Tue Jun 14 2011 Honza Horak <hhorak@redhat.com> - 2.25-3
- Adjust yppush man page and add a comment how to assign options
  to yppush (#712239)

* Tue May 10 2011 Honza Horak <hhorak@redhat.com> - 2.25-2
- Add systemd native services files for ypserv, ypxfrd and yppasswdd
  (#696903)

* Tue May 10 2011 Honza Horak <hhorak@redhat.com> - 2.25-1
- Update to new upstream version, which contains .staticanal patch

* Fri May 06 2011 Honza Horak <hhorak@redhat.com> - 2.24-4
- Change default aliases file location to /etc/aliases to correspond
  with default MTAs' config (#699826)

* Tue Apr 26 2011 Honza Horak <hhorak@redhat.com> - 2.24-3
- Fix problems found by static analysis
- Added man page info about passing arguments to daemons

* Tue Oct 19 2010 Karel Klic <kklic@redhat.com> - 2.24-2
- Removed Buildroot tag
- Removed %%clean section
- Replace custom %%initdir macro with systemwide %%_initrddir

* Tue Oct 19 2010 Karel Klic <kklic@redhat.com> - 2.24-1
- New upstream version.

* Thu Mar 11 2010 Karel Klic <kklic@redhat.com> - 2.23-4
- Rebuilt for gdbm upgrade

* Mon Mar 01 2010 Karel Klic <kklic@redhat.com> - 2.23-3
- /var/yp is owned by filesystem (#569382)

* Mon Mar 01 2010 Karel Klic <kklic@redhat.com> - 2.23-2
- Added COPYING file to the package
- Removed Obsoletes: yppasswd
- Spec file cleanup

* Wed Feb 24 2010 Karel Klic <kklic@redhat.com> - 2.23-1
- Updated to new upstream version
- Removed pidfile and nodbclose patches, as those were
  merged by the upstream

* Thu Jan 28 2010 Karel Klic <kklic@redhat.com> - 2.21-4
- Removed ypserv-2.21-iface.patch, because upstream refused to
  merge it three times over 7 years. "Since this is
  not supported by RPC (means portmapper still shows ypserv
  for the other subnets and portmapper can forward requests
  from other subnets via loopback), this will give quite some
  unexpected behaviors and makes it pretty difficult to debug
  such scenarios."

* Wed Jan 27 2010 Karel Klic <kklic@redhat.com> - 2.21-3
- Added patch removing invalid ypdb_close call (#403621, #430902)

* Thu Jan 21 2010 Karel Klic <kklic@redhat.com> - 2.21-2
- Added patch for rpc.ypxfrd to create a pid file
- Rewrote initscripts to become closer to Packaging:SysVInitScript
  Fedora guildeline
- Fixed initscript for ypserv (rhbz#523438)
- Fixed initscript for yppasswdd (rhbz#523394)
- Fixed initscript for ypxfrd (rhbz#523397)

* Wed Jan 13 2010 Karel Klic <kklic@redhat.com> - 2.21-1
- Updated to new upstream version
- Removed ypserv-2.11-nomap.patch, it has been applied by upstream
- Removed ypserv-2.19-quieter.patch, it has been applied by upstream
- Removed ypserv-2.13-yplib-memleak.patch, upstream version fixes the problem
- Removed ypserv-2.19-debuginfo.patch, upstream version no longer needs it
- Ported -path, -iface patches to the new version

* Thu Jan  7 2010 Karel Klic <kklic@redhat.com> - 2.19-15
- Removed Prereq use in the spec file
- Removed usage of RPM_SOURCE_DIR from the spec file

* Tue Jan  5 2010 Karel Klic <kklic@redhat.com> - 2.19-14
- Removed --enable-yppasswd from configure, as this option is
  ignored

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar  3 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.19-12
- Mark apropriate config files as noreplace

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 25 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.19-10
- Rediff all patches to work with patch --fuzz=0

* Wed Feb 13 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.19-9
- Mark /var/yp/Makefile as %%config(noreplace)
  Resolves: #432582
- Comment "slp" part of ypserv.conf to avoid ypserv warnings
  Resolves: #154806
- Spec file cleanup - remove period from end of Summary,
  fix license, remove macros from Changelog

* Mon Feb  4 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.19-8
- Fix Buildroot
- Fix /var/yp/Makefile
  Resolves: #431008

* Tue Jan  8 2008 Steve Dickson <steved@redhat.com> 2.19-7
- Changed Makefiles.in so binaries are not stripped.

* Sat Sep 15 2007 Steve Dickson <steved@redhat.com> 2.19-6
- Fixed init scripts to return correct exit code on
 'service status' (bz 248097)

* Tue Jul 31 2007 Steve Dickson <steved@redhat.com> 2.19-5
- Changed install process to create an useful debuginfo package (bz 249961)

* Fri Dec 22 2006 Steve Dickson <steved@redhat.com> - 2.19-4
- Made ypserver less verbose on common errors (bz #199236)
- Don't allow a make for empty domainname's or domainname's set to (none)
  (bz #197646)

* Wed Sep 13 2006 Steve Dickson <steved@redhat.com> - 2.19-3
- Added range checks to port values given on command line
  (bz 205354)

* Tue Jul 25 2006 Steve Dickson <steved@redhat.com> - 2.19-2
- fixed typo in ypxfrd initscript (bz 185403)

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 2.19-1
- rebuild

* Mon Feb 13 2006 Chris Feist <cfeist@redhat.com> - 2.19-0
- Rebuilt against latest upstream sources (2.19).

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13-10.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13-10.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan  9 2006 Chris Feist <cfeist@redhat.com> - 2.13-10
- Fix crash with ypxfr caused by failing to zero out data (bz #161217)

* Wed Jan  4 2006 Jesse Keating <jkeating@redhat.com> - 2.13-6.2
- rebuilt for new gcc

* Thu Oct 14 2004 Miloslav Trmac <mitr@redhat.com> - 2.13-5
- Fix crash with -p (#134910, #129676)

* Tue Aug 31 2004 Steve Dickson <SteveD@RedHat.com>
- Zeroed out the ypxfr response buffer so allocated memory
  is not freed with the transfer fails

* Sat Jun 19 2004 Steve Dickson <SteveD@RedHat.com>
- Closed a memory leak in GDBM database routines (bz 120980)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 17 2004 Thomas Woerner <twoerner@redhat.com> 2.13-1
- compiling rpc.yppasswdd, rpc.ypxfrd, yppush and ypserv PIE

* Fri Apr 16 2004 Steve Dickson <SteveD@RedHat.com>
- Updated to 2.13

* Fri Apr  2 2004 Steve Dickson <SteveD@RedHat.com>
- Change ypMakefile to create services.byservicename
  maps correctly

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Phil Knirsch <pknirsch@redhat.com> 2.12.1-1
- Updated to latest upstream version.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 19 2004 Phil Knirsch <pknirsch@redhat.com> 2.11-1
- Updated to latest upstream version.
- Dropped ypserv-2.8-echild.patch (not needed anymore).
- Fixed several other patches for new version.

* Mon Sep 15 2003 Steve Dickson <SteveD@RedHat.com>
- updated Release number for QU1

* Mon Sep 15 2003 Steve Dickson <SteveD@RedHat.com>
- Recompiled for AS2.1

* Wed Sep 10 2003 Steve Dickson <SteveD@RedHat.com>
- Added the --iface flag.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr 24 2003 Steve Dickson <SteveD@RedHat.com>
- Update to 2.8

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Nov  5 2002 Alexander Larsson <alexl@redhat.com> 2.6-1
- Updated to 2.6, allows you to disable db caching, bug #76618

* Mon Oct  7 2002 Alexander Larsson <alexl@redhat.com> 2.5-2
- Added comments to nfsnobody patch
- Corrected URL
- fixed missing %%doc file, bug #74060

* Thu Aug 15 2002 Alexander Larsson <alexl@redhat.com> 2.5-1
- Update to 2.5, fixes memleak
- remove manpage patch since it was already fixed upstream

* Thu Aug 15 2002 Alexander Larsson <alexl@redhat.com>
- Fix ypserv.conf manpage, bug #69785
- Don't leak nfsnobody into nfs maps, bug #71515

* Thu Aug  8 2002 Alexander Larsson <alexl@redhat.com> 2.3-3
- Remove old broken triggers that are not needed anymore. Fixes #70612

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 2.3-2
- automated rebuild

* Tue Jun 11 2002 Alex Larsson <alexl@redhat.com> 2.3-1
- Updated to 2.3 from upstream.
- Removed patches that went in upstream.

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 16 2002 Alex Larsson <alexl@redhat.com> 2.2-9
- Removed my ypserv-2.2-services patch. According to thorsten
  (yp maintainer) the key in services.byname actually
  SHOULD be port/protocol.

* Mon Apr  8 2002 Alex Larsson <alexl@redhat.com> 2.2-8
- Change the yppush patch to the patch from thorsten.

* Fri Apr  5 2002 Alex Larsson <alexl@redhat.com> 2.2-7
- Added patch to fix yppush timeout errors (#62429)

* Wed Mar 27 2002 Alex Larsson <alexl@redhat.com> 2.2-6
- Make yppasswdd source /etc/sysconf/yppasswd for options (#52253)

* Mon Mar 25 2002 Alex Larsson <alexl@redhat.com> 2.2-5
- Add patch that fixes generation of services.byname. (#41851)
- Actually apply patch #5, seems like it got left out by misstake

* Fri Mar 22 2002 Alex Larsson <alexl@redhat.com> 2.2-4
- Changed Copyright from GNU to GPL

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat Dec 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix restart initscript option #57129
- add a "gawk" requires #57002
- fix printcap bug #56993
- fix ypxfrd init script #55234

* Wed Dec 05 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.2 plus first official bug-fix

* Sat Nov 17 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to version 2.1, adjust all patches

* Mon Aug 27 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- set domainname if it is not yet set #52514

* Tue Jul 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add gdbm-devel BuildReq #49767
- add ypxfrd init script #44845
- fix #44805
- fix #20042, adding option to yppasswdd startup
- own /var/yp

* Mon Jul  9 2001 Tim Powers <timp@redhat.com>
- added reload entry to initscript (same as restart)

* Fri Jun 29 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.3.12

* Wed Mar 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- do not require tcp_wrappers anymore

* Thu Mar 15 2001 Philipp Knirsch <pknirsch@redhat.com>
- Added missing make requirement

* Tue Feb 27 2001 Preston Brown <pbrown@redhat.com>
- don't own dir /var/yp

* Wed Jan 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- prepare for startup script translation

* Thu Jan 11 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Start after netfs (#23527)

* Wed Aug 16 2000 Than Ngo <than@redhat.com>
- fix typo in startup script (Bug #15999)

* Wed Jul 19 2000 Than Ngo <than@redhat.de>
- inits back to rc.d/init.d, using service
- fix initscript again

* Mon Jul 17 2000 Bill Nottingham <notting@redhat.com>
- move initscript back
- fix format syslog bug

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul  7 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- prereq /etc/init.d

* Tue Jun 27 2000 Than Ngo <than@redhat.de>
- /etc/rc.d/init.d -> /etc/init.d
- fix initscript

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- FHS fixes,
- fix docdir

* Fri May 19 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- disable "netgrp" target in default all: (/var/yp/Makefile)

* Thu May 18 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 1.3.11

* Mon Mar 06 2000 Cristian Gafton <gafton@redhat.com>
- add patch to avoid potential deadlock on the server (fix #9968)

* Wed Feb  2 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- fix typo in %%triggerpostun

* Mon Oct 25 1999 Bill Nottingham <notting@redhat.com>
- update to 1.3.9
- use gdbm, move back to /usr/sbin

* Tue Aug 17 1999 Bill Nottingham <notting@redhat.com>
- initscript munging
- ypserv goes on root partition

* Fri Aug 13 1999 Cristian Gafton <gafton@redhat.com>
- version 1.3.7

* Thu Jul  1 1999 Bill Nottingham <notting@redhat.com>
- start after network FS

* Tue Jun  1 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.6.94.

* Sun May 30 1999 Jeff Johnson <jbj@redhat.com>
- improved daemonization.

* Sat May 29 1999 Jeff Johnson <jbj@redhat.com>
- fix buffer overflow in rpc.yppasswd (#3126).

* Fri May 28 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.3.6.92.

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- version 1.3.6.91

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 4)

* Mon Feb  8 1999 Bill Nottingham <notting@redhat.com>
- move to start before ypbind

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1
- upgraded to 1.3.5

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- yppasswd.init: lock file must have same name as init.d script, not daemon

* Sat Jul 11 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.3.4
- fixed the fubared Makefile
- link against gdbm instead of ndbm (it seems to work better)

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.3.1
- enhanced init scripts

* Fri May 01 1998 Jeff Johnson <jbj@redhat.com>
- added triggerpostun
- Use libdb fro dbp_*().

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Apr 13 1998 Cristian Gafton <gafton@redhat.com>
- updated to 1.3.0

* Wed Dec 03 1997 Cristian Gafton <gafton@redhat.com>
- updated to 1.2.5
- added buildroot; updated spec file
- added yppasswdd init file

* Tue Nov 04 1997 Erik Troan <ewt@redhat.com>
- init script shouldn't set the domain name

* Tue Oct 14 1997 Erik Troan <ewt@redhat.com>
- supports chkconfig
- updated initscript for status and restart
- turned off in all runlevels, by default
- removed postinstall script which didn't do anything

* Thu Oct 09 1997 Erik Troan <ewt@redhat.com>
- added patch to build against later glibc

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Wed Apr 23 1997 Erik Troan <ewt@redhat.com>
- updated to 1.1.7.

* Fri Mar 14 1997 Erik Troan <ewt@redhat.com>
- Updated to ypserv 1.1.5, ported to Alpha (glibc).

* Fri Mar 07 1997 Erik Troan <ewt@redhat.com>
- Removed -pedantic which confuses the SPARC :-(
