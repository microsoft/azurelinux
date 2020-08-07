%undefine _ld_as_needed

Name:			ebtables
Version:		2.0.11
Release:		6%{?dist}
Summary:		Ethernet Bridge frame table administration tool
License:		GPLv2+
URL:			http://ebtables.sourceforge.net/

Source0:		https://netfilter.org/pub/ebtables/%{name}-%{version}.tar.gz
Source1:		ebtables-legacy-save
Source2:		ebtables-helper
Source3:		ebtables.service
Source4:		ebtables-config

BuildRequires:		autogen
BuildRequires:		autoconf
BuildRequires:		automake
BuildRequires:		libtool
BuildRequires:		gcc
BuildRequires:		systemd

%description
Ethernet bridge tables is a firewalling tool to transparently filter network
traffic passing a bridge. The filtering possibilities are limited to link
layer filtering and some basic filtering on higher network layers.

This tool is the userspace control for the bridge and ebtables kernel
components (built by default in Fedora kernels).

The ebtables tool can be used together with the other Linux filtering tools,
like iptables. There are no known incompatibility issues.

%package legacy
Summary: Legacy user space tool to configure bridge netfilter rules in kernel
Provides: ebtables

%description legacy
Ethernet bridge tables is a firewalling tool to transparently filter network
traffic passing a bridge. The filtering possibilities are limited to link
layer filtering and some basic filtering on higher network layers.

This tool is the userspace control for the bridge and ebtables kernel
components (built by default in Fedora kernels).

The ebtables tool can be used together with the other Linux filtering tools,
like iptables. There are no known incompatibility issues.

Note that it is considered legacy upstream since nftables provides the same
functionality in a much newer code-base. To aid in migration, there is
ebtables-nft utility, a drop-in replacement for the legacy one which uses
nftables internally. It is provided by iptables-nft package.

%package services
Summary: ebtables systemd services
%{?systemd_ordering}
Obsoletes:	ebtables-compat < 2.0.10-39

%description services
ebtables systemd services

This package provides the systemd ebtables service that has been split
out of the base package for better integration with alternatives.

%prep
%autosetup -p1 -n ebtables-%{version}
# Convert to UTF-8
f=THANKS; iconv -f iso-8859-1 -t utf-8 $f -o $f.utf8 ; mv $f.utf8 $f

%build
./autogen.sh
%configure --disable-silent-rules LOCKFILE=/run/ebtables.lock
%make_build

%install
%make_install
install -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/ebtables.service
install -D -m 755 %{SOURCE2} %{buildroot}%{_libexecdir}/ebtables-helper
install -D -m 600 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/ebtables-config
touch %{buildroot}%{_sysconfdir}/sysconfig/ebtables

# install ebtables-legacy-save bash script
install -m 755 %{SOURCE1} %{buildroot}%{_sbindir}/ebtables-legacy-save

# No use for libtool archive files
rm %{buildroot}/%{_libdir}/libebtc.la

# Drop these binaries (for now at least)
rm %{buildroot}/%{_sbindir}/ebtables{d,u}

# Symlink ebtables-legacy to ebtables
ln -sf ebtables-legacy %{buildroot}%{_sbindir}/ebtables
ln -sf ebtables-legacy-save %{buildroot}%{_sbindir}/ebtables-save
ln -sf ebtables-legacy-restore %{buildroot}%{_sbindir}/ebtables-restore

%post services
%systemd_post ebtables.service

%preun services
%systemd_preun ebtables.service

%postun services
%systemd_postun ebtables.service

%files legacy
%license COPYING
%doc ChangeLog THANKS
%{_sbindir}/ebtables-legacy*
%{_sbindir}/ebtables*
%{_mandir}/*/ebtables-legacy*
%{_libdir}/libebtc.so*
%{_sysconfdir}/ethertypes

%files services
%{_unitdir}/ebtables.service
%{_libexecdir}/ebtables-helper
%config(noreplace) %{_sysconfdir}/sysconfig/ebtables-config
%ghost %{_sysconfdir}/sysconfig/ebtables

%changelog
* Fri Jul 31 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.0.11-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Modified to remove update-alternatives dependency

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Tom Callaway <spot@fedoraproject.org> - 2.0.11-4
- add Requires(post): %%{_bindir}/readlink (bz1792805)

* Mon Dec 16 2019 Phil Sutter <psutter@redhat.com> - 2.0.11-3
- Fix nft-variant reference in package description

* Mon Dec 16 2019 Phil Sutter <psutter@redhat.com> - 2.0.11-2
- Eliminate implicit dependency on initscripts package

* Mon Dec  2 2019 Tom Callaway <spot@fedoraproject.org> - 2.0.11-1
- update to 2.0.11 (all of Phil's awesome patches merged)

* Wed Oct 30 2019 Phil Sutter <psutter@redhat.com> - 2.0.10-39
- Make services sub-package obsolete compat to fix upgrade path

* Tue Oct 22 2019 Phil Sutter <psutter@redhat.com> - 2.0.10-38
- Drop compat sub-package again

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 26 2019 Phil Sutter <psutter@redhat.com> - 2.0.10-36
- Fix segfault with non-existing lock directory

* Wed Apr 24 2019 Phil Sutter <psutter@redhat.com> - 2.0.10-35
- Workaround missing broute table support in ebtables-nft

* Tue Apr 09 2019 Phil Sutter <psutter@redhat.com> - 2.0.10-34
- Fix lockfile location

* Thu Apr 04 2019 Phil Sutter <psutter@redhat.com> - 2.0.10-33
- Fix date in previous changelog entry
- Use systemd_ordering macro

* Thu Apr 04 2019 Phil Sutter <psutter@redhat.com> - 2.0.10-32
- Add upstream changes since last release
- Rename package to ebtables-legacy
- Split systemd service into services sub-package
- Rewrite systemd unit helper script for compatibility with ebtables-nft
- Drop module unloading on service stop, this causes more harm than good
- Remove save format settings, they are not effective anymore
- Remove save on restart setting, restart is merely stop && start
- Complete integration into alternatives
- Remove needless ldconfig calls

* Thu Feb  7 2019 Tom Callaway <spot@fedoraproject.org> - 2.0.10-31
- build without as-needed everywhere (stop using Ubuntu patch)
  Resolves BZ:1672683

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 David Abdurachmanov <david.abdurachmanov@gmail.com> 2.0.10-29
- Disable --as-needed to resolve segfaults

* Sun Jul 22 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.0.10-28
- Add gcc dep, spec cleanups

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Phil Sutter <psutter@redhat.com> - 2.0.10-26
- Replace calls to ldconfig with newly introduced macro.
- Install binaries in /usr/sbin instead of /sbin.
- Make use of Alternatives system.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 22 2016 Thomas Woerner <twoerner@redhat.com> - 2.0.10-21
- /etc/ethertypes has been moved into the setup package for F-25+.
  (RHBZ#1329256)

* Mon May  9 2016 Thomas Woerner <twoerner@redhat.com> - 2.0.10-20
- add upstream --noflush option patch for ebtables-restore

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.10-18
- Move lock file to /run/ebtables.lock (bz 1290327)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 24 2014 Tom Callaway <spot@fedoraproject.org> - 2.0.10-15
- create and own /var/lib/ebtables (bz 1093361)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Tom Callaway <spot@fedoraproject.org> - 2.0.10-13
- use standard optflags and ldflags (bz 1071993)

* Wed Feb 19 2014 Tom Callaway <spot@fedoraproject.org> - 2.0.10-12
- remove executable bit from systemd service file
- add RARP type to ethertypes (bz 1060537)

* Wed Aug 21 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.10-11
- convert to systemd

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 21 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.10-8
- add audit module

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr  5 2012 Tom Callaway <spot@fedoraproject.org> - 2.0.10-5
- update to 2.0.10-4 (upstream numbering is goofy)
- fix missing symbol issue with extension modules (bz810006)

* Thu Feb 16 2012 Thomas Woerner <twoerner@redhat.com> - 2.0.10-4
- replaced ebtables-save perl script by bash script to get rid of the perl 
  requirement

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 11 2011 Tom Callaway <spot@fedoraproject.org> - 2.0.10-2
- update to 2.0.10-2

* Mon Jul 11 2011 Tom Callaway <spot@fedoraproject.org> - 2.0.10-1
- update to 2.0.10-1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 15 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.9-5
- update to 2.0.9-2

* Fri Jan 29 2010 Thomas Woerner <twoerner@redhat.com> - 2.0.9-4
- moved ebtables modules to /lib[64]/ebtables (rhbz#558886)

* Fri Jan 15 2010 Thomas Woerner <twoerner@redhat.com> - 2.0.9-3
- fixed init script to be lsb conform (rhbz#536828)
- fixed download link according to package review

* Wed Aug 19 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.9-2
- fix source0 url

* Mon Jul 27 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.9-1
- update to 2.0.9

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.8-5
- Autorebuild for GCC 4.3

* Sun Oct 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-4
- bump to 2.0.8-2 from upstream
- keep _libdir/ebtables, even though upstream just moved away from it.

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-3
- use _libdir/ebtables to match upstream RPATH (bugzilla 248865)
- correct license tag
- use upstream init script
- enable build-id
- use cflags for all compiles
- be sane with DESTDIR

* Mon Jul  9 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-2
- remove "Fedora Core" reference in spec

* Mon Jul  2 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-1
- final 2.0.8 release

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.8.rc3
- fix release order

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.1.rc3
- bump to rc3

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 2.0.8-0.7.rc2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.6.rc2
- fix versioning

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.3.rc2
- fix bugzilla 206257

* Tue Sep 12 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.2.rc2
- fix for FC-6

* Mon Apr 24 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.1.rc2
- bump to rc2

* Sun Apr  2 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.5.rc1
- learn to use "install" correctly. :/

* Sun Apr  2 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.4.rc1
- package up the shared libs too

* Wed Mar 29 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.3.rc1
- use -fPIC

* Wed Mar 29 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.2.rc1
- broken tagging

* Tue Jan 10 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.8-0.1.rc1
- bump to 2.0.8-rc1

* Mon Jul  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-7
- buildsystem error requires artificial release bump

* Mon Jul  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-6
- actually touch ghosted files

* Fri Jul  1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-5
- fix sysv file

* Fri Jul  1 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-4
- remove INSTALL file
- add some text to description, correct typos
- fix %%postun
- add PreReqs
- add %%ghost config files

* Tue May 31 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.6-3
- reworked for Fedora Extras
- add gcc4 fix
- move init file into SOURCE1

* Thu Dec 02 2004 Dag Wieers <dag@wieers.com> - 2.0.6-2
- Added patch for gcc 3.4. (Nigel Smith)

* Tue Apr 27 2004 Dag Wieers <dag@wieers.com> - 2.0.6-2
- Cosmetic changes.

* Tue Apr 27 2004 Dag Wieers <dag@wieers.com> - 2.0.6-1
- Initial package. (using DAR)
