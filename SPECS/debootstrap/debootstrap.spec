# Mariner does not use the %%__brp_mangle_shebangs buildroot policy, but may in the future
# Mangling shebang in /usr/sbin/debootstrap from /bin/sh to /usr/bin/sh
%undefine __brp_mangle_shebangs

Summary:        Debian GNU/Linux bootstrapper
Name:           debootstrap
Version:        1.0.134
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://wiki.debian.org/Debootstrap
Source0:        https://deb.debian.org/debian/pool/main/d/%{name}/%{name}_%{version}.tar.gz
BuildRequires:  fakeroot
BuildRequires:  make
Requires:       binutils
Requires:       gettext
Requires:       gpg
Requires:       perl-interpreter
Requires:       wget
Requires:       tar
Requires:       gzip
Requires:       xz
Requires:       zstd
BuildArch:      noarch

%description
debootstrap is used to create a Debian base system from scratch, without
requiring the availability of dpkg or apt.  It does this by downloading
.deb files from a mirror site, and carefully unpacking them into a
directory which can eventually be chrooted into.

This might be often useful coupled with virtualization techniques to run
Debian GNU/Linux guest system.


%prep
%autosetup -n %{name}

%build
# nothing to do

%install
fakeroot %make_install VERSION="%{version}-%{release}"

# install manual page
mkdir -p %{buildroot}%{_mandir}/man8
install -p -m 0644 debootstrap.8 %{buildroot}%{_mandir}/man8

%files
%license debian/copyright
%doc README
%{_datadir}/debootstrap
%{_datadir}/debootstrap/scripts/*
%{_sbindir}/debootstrap
%{_mandir}/man8/debootstrap.8*

%changelog
* Tue Jun 18 2024 Adeel Mujahid <adeelbm@outlook.com> - 1.0.134-1
- Upgrade to version 1.0.134 to support RISC-V architecture

* Tue Jun 06 2023 Olivia Crain <oliviacrain@microsoft.com> - 1.0.128+nmu2-1
- Upgrade to latest upstream version and promote to base repo
- Remove requirement on dpkg- ar (from binutils) is sufficient to unpack debs
- Verified license
- Verified license tag uses SPDX expression

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.123-2
- Initial CBL-Mariner import from Fedora 20 (license: MIT).

* Fri May 22 2020 Sérgio Basto <sergio@serjux.com> - 1.0.123-1
- Update to 1.0.123
- Undefine mangle_shebangs (#1654765)
- Remove old scriplets, %%{_datadir} and /usr/share is the same
  and %%{_sbindir} and /usr/sbin is also the same

* Sat Feb 29 2020 Sérgio Basto <sergio@serjux.com> - 1.0.119-1
- Update to 1.0.119 (#1807970)

* Fri Feb 21 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1.0.118-1
- Update to 1.0.118 (#1805812)

* Fri Feb 21 2020 Sérgio Basto <sergio@serjux.com> - 1.0.117-1
- Update to 1.0.117

* Tue Oct 08 2019 Sérgio Basto <sergio@serjux.com> - 1.0.116-1
- Update to 1.0.116 (#1727618)

* Tue Oct 08 2019 Sérgio Basto <sergio@serjux.com> - 1.0.114-1
- Update to 1.0.114 (#1708159)

* Sat Dec 01 2018 Sérgio Basto <sergio@serjux.com> - 1.0.109-3
- Don't mangling shebang in /usr/sbin/debootstrap from /bin/sh to /usr/bin/sh
  (#1654765), thanks to Laurent Vivier

* Fri Sep 21 2018 Sérgio Basto <sergio@serjux.com> - 1.0.109-2
- dpkg was fixed in el6 and el7 we may use dpkg again.

* Fri Sep 21 2018 Sérgio Basto <sergio@serjux.com> - 1.0.109-1
- Update to 1.0.109 (#1594470)

* Thu Jun 14 2018 Sérgio Basto <sergio@serjux.com> - 1.0.102-1
- Update to 1.0.102 (#1585520)

* Wed May 23 2018 Sérgio Basto <sergio@serjux.com> - 1.0.100-1
- New upstream release (#1578167)
- Do not use dpkg on el, dpkg cause broken deps with man-pages-it in el6 and el7

* Thu Apr 19 2018 Sérgio Basto <sergio@serjux.com> - 1.0.97-1
- Update to 1.0.97 (#1557586)
- Require perl-interpreter (#1566045)
- From the mentioned bug report, 2 patches was applied upstream cleaned, the
  other 2 don't but I assume the bug is fixed.

* Tue Feb 27 2018 Lubomir Rintel <lkundrak@v3.sk> - 1.0.93-3
- Fix boostrapping libvirt LXC containers
- Don't let host PATH leak into the target commands

* Tue Feb 13 2018 Lubomir Rintel <lkundrak@v3.sk> - 1.0.93-2
- Require dpkg instead of ar as the unpacker

* Fri Dec 08 2017 Fedora Release Monitoring  <release-monitoring@fedoraproject.org> - 1.0.93-1
- Update to 1.0.93 (#1523424)

* Wed Nov 01 2017 Fedora Release Monitoring  <release-monitoring@fedoraproject.org> - 1.0.92-1
- Update to 1.0.92 (#1508179)

* Wed Jul 26 2017 Fedora Release Monitoring  <release-monitoring@fedoraproject.org> - 1.0.91-1
- Update to 1.0.91 (#1475301)

* Wed Apr 26 2017 Sérgio Basto <sergio@serjux.com> - 1.0.90-1
- Update debootstrap to 1.0.90

* Sat Nov 19 2016 Jan Vcelak <jvcelak@fedoraproject.org> - 1.0.87-1
- new upstream release:
  + rework split_inline_sig with shell built-ins for Debian Installer (Debian #842591)
  + default to split /usr again, as merged-/usr breaks dpkg-shlibdeps (Debian #844221)
  * remove scratchbox2 support (Debian #796189)

* Sun Oct 23 2016 Jan Vcelak <jvcelak@fedoraproject.org> - 1.0.85-1
- new upstream release:
  + add support for xz-compressed Package indicies (Debian #837649)
  + add support for downloading and validating InRelease files
  + switch default mirror to deb.debian.org
  + add Ubuntu zesty as a symlink to gutsy
  + enable merged /usr by default (Debian #839046)
  + blacklist merged /usr for jessie-kfreebsd
  + error out when seeing short options (Debian #548880)
  + add oldoldstable, buster, bullseye as symlinks to sid (Debian #792734)
  + fix failure when installing just minbase (Debian #825034)
  + do not use `tar -k` for older releases which might have file
    conflicts between the packages to be installed (Debian #838388)
  + man page: use stretch instead of wheezy in examples

* Thu Sep 22 2016 Jan Vcelak <jvcelak@fedoraproject.org> - 1.0.83-1
- new upstream release:
  + validate installed suite against Release file (Debian #837075)
  + support for merged /usr with --merged-usr option (Debian #810301)
  + fix installation with tar from busybox (Debian #837185)
  + remove devices.tar.gz code (Debian #830869)

* Fri Jun 24 2016 Jan Vcelak <jvcelak@fedoraproject.org> - 1.0.81-1
- new upstream release (RHBZ #1332736)
  + add Ubuntu yakkety as a symlink to gutsy
- add missing dependency on xz (RHBZ #1347734)

* Sun Mar 27 2016 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.80-1
- new upstream release
  + support kfreebsd & hurd arches on Ubuntu targets
- recommend installation of debian-keyring and ubu-keyring

* Wed Feb 24 2016 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.79-1
- new upstream release
  + generate deburis files
  + add Ubuntu xenial as a symlink to gutsy
  + stop cleaning KEEP_DEBOOTSTRAP_DIR twice
  + add Tanglu distribution support
  + use HTTPS for VCS URLs

* Fri Aug 14 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.72-1
- new upstream release
  + add Ubuntu wily as a symlink to gutsy
  + fix resolve_deps and setup_available in --foreign case

* Thu Jun 04 2015 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.70-1
- new upstream release:
  + support for jessie-kfreebsd
  + deduplicate package list when counting downloaded packages
  + add support for '--force-check-gpg'
  + switch default FTP to official redirector
  + make it possible to override the MAKEDEV variable
  + use tr instead of xargs

* Mon Apr 27 2015 Lubomir Rintel <lkundrak@v3.sk> 1.0.67-1
- new upstream release
- Fix upstream URL
- Depend on Ubuntu keyring

* Tue Nov 25 2014 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.66-1
- new upstream release:
  + add support for 'stretch'
  + specify gzip for deboostrap, xz for debootstrap-udeb
  + better portability on non-Debian platforms

* Wed Oct 22 2014 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.64-1
- new upstream release:
  + Ubuntu vivid as a symlink to gutsy
  + move set -e out of shebang line (Debian: #762713)

* Wed Sep 17 2014 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.62-1
- new upstream release:
  + fix warnings caused by change in output of dpkg 1.17.2
  + fix reporting of package versions with epoch

* Sat Aug 02 2014 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.60-1
- new upstream release:
  + Ubuntu utopic as a symlink to gutsy
  + Compression support in fallback method for deb archives extraction

* Tue Apr 29 2014 Lubomir Rintel <lkundrak@v3.sk> 1.0.59-1.2
- Fix chrooting
- Fix architecture detection
- Drop unneded MAKEDEV patch, as we don't use it anymore

* Tue Apr 29 2014 Lubomir Rintel <lkundrak@v3.sk> 1.0.59-1.1
- RHEL 7 does not ship MAKEDEV anymore

* Fri Feb 14 2014 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.59-1
- new upstream release:
  + install ca-certificates as well as apt-transport-https for https installations

* Wed Feb 12 2014 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.58-1
- new upstream release:
  + install apt-transport-https when installing over HTTPS

* Sun Feb 09 2014 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.57-1
- new upstream release:
  + Ubuntu trusty as a symlink to gutsy
  + when debian-archive-keyring is not available, use the main mirror with https
  + separate installation of base-passwd and base-files
  + pkgdetails_perl: fix percentage sign interpretation

* Mon Sep 02 2013 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.53-1
- new upstream release:
  + add saucy (Ubuntu) as a symlink to gutsy
  + clarify location of pkgdetails.c in error message
  + resolve mount points symlinks relative to target chroot before unmounting them
  + gutsy: detect if running under Upstart
  + sid, gutsy: add policy-rc.d
  + set Debian source format to '3.0 (native)'
  + bump debhelper compat level to 9
  + set Vcs-* to canonical format
  + update Standards to 3.9.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 18 2013 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.50-1
- new upstream release:
  + add support for 'jessie' release
  + print version and revision information when retrieving the packages

* Fri Apr 05 2013 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.48-1
- new upstream release:
  + Disable InRelease support.  gpgv won't give us back the signed data, and
    full gpg is not available inside d-i (Debian: #703889).
  + Move extract_release_components to after signature verification.

* Sun Mar 31 2013 Jan Vcelak <jvcelak@fedoraproject.org> 1.0.47-1
- new upstream release:
  + properly decrypt InRelease file if available
  + add dependency on gnupg

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 01 2013 Jan Vcelak <jvcelak@redhat.com> 1.0.46-1
- new upstream release:
  + better support use on Android
  + use which to locate sh if /bin/sh not found

* Thu Nov 22 2012 Jan Vcelak <jvcelak@redhat.com> 1.0.44-1
- new upstream release:
  + remove double quotes to fix for loop on GNU/kFreeBSD

* Wed Nov 07 2012 Jan Vcelak <jvcelak@redhat.com> 1.0.43-1
- new upstream release:
  + add (Ubuntu) raring as a symlink to gutsy.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jan Vcelak <jvcelak@redhat.com> 1.0.42-1
- new upstream release:
  + downgrade missing InRelease file warning to info message

* Tue Jun 26 2012 Jan Vcelak <jvcelak@redhat.com> 1.0.41-1
- new upstream release:
  + support for InRelease repository files

* Wed May 02 2012 Jan Vcelak <jvcelak@redhat.com> 1.0.40-1
- new upstream release:
  + better error reporting when installation or configuration fails
  + add quantal as a symlink to gutsy

* Wed Mar 14 2012 Jan Vcelak <jvcelak@redhat.com> 1.0.39-1
- new upstream release:
  + retry corrupted downloads rather than carrying on almost regardless
  + stop at the end of the retrieval phase if any packages failed to download

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Jan Vcelak <jvcelak@redhat.com> 1.0.38-1
- new upstream release:
  + a few bugfixes, no new features

* Mon Oct 24 2011 Jan Vcelak <jvcelak@redhat.com> 1.0.37-1
- new upstream release:
  + add Ubuntu 'precise' as a symlink to 'gutsy'

* Mon Aug 22 2011 Jan Vcelak <jvcelak@redhat.com> 1.0.36-1
- new upstream release:
  + use md5sum for 'sarge'
  + improve error message when decompressing command is not available
  + add more information regarding the version and architecture in case a download fails
  + do not use --arch when we specifically care about the host architecture
  + guess host OS based on uname for non-Debian systems
  + clarify "target" in usage message
  + search PATH for programs, rather than checking hardcoded locations
  + various fixes for installing kFreeBSD

* Mon Jun 20 2011 Jan Vcelak <jvcelak@redhat.com> 1.0.32-1
- new upstream release:
  + use md5sums for 'woody' and 'potato'

* Mon May 23 2011 Jan Vcelak <jvcelak@redhat.com> 1.0.31-1
- bootstrapping Ubuntu systems:
  + recommend ubuntu-keyring instead of debian-archive-keyring
  + check signatures when ubuntu-keyring package is installed

* Fri May 20 2011 Jan Vcelak <jvcelak@redhat.com> 1.0.30-1
- new upstream release:
  + support bootstraping Debian oldstable
  + Ubuntu Oneiric symlink to Gutsy
  + removed --boot-floppies switch and mode
  + various fixes in package GPG signatures checking

* Tue Mar 08 2011 Jan Vcelak <jvcelak@redhat.com> 1.0.28-1
- new upstream release:
  + fix: bug in the ar extractor for non-gz data.tar in .debs (Debian #598729)
  + remove 5 second sleeps when debootstrap finds additional required dependencies
  + use SHA checksums instead of MD5
  + avoid new warning from dpkg about missing Maintainer field

* Wed Feb 09 2011 Jan Vcelak <jvcelak@redhat.com> 1.0.27-1
- new upstream release (typo in --private-key, improve Hurd support)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Jan Vcelak <jvcelak@redhat.com> 1.0.26-1
- new upstream release (fix typos and remove old workaround for md5sum)

* Mon Oct 25 2010 Jan Vcelak <jvcelak@redhat.com> 1.0.25-1
- new upstream release (support for HTTPS, added Ubuntu Nanty, added Debian Wheezy)

* Wed May 26 2010 Jan Zeleny <jzeleny@redhat.com> - 1.0.23-1
- rebased to 1.0.23 (Add ${misc:Depends}, Add (Ubuntu) maverick as symlink to gutsy)

* Fri Mar 05 2010 Jan Zeleny <jzeleny@redhat.com> - 1.0.22-1
- rebased to 1.0.22

* Wed Sep 30 2009 Adam Goode <adam@spicenitz.org> - 1.0.19-2
- Make sure to create /dev/console in devices.tar.gz

* Wed Sep 30 2009 Adam Goode <adam@spicenitz.org> - 1.0.19-1
- New upstream release
   + Many bugfixes
   + Support for new distributions
- Arch patch no longer needed
- Rebase other patches

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Lubomir Rintel <lkundrak@v3.sk> - 1.0.10-1
- New upstream version

* Sun Jun 15 2008 Adam Goode <adam@spicenitz.org> - 1.0.9-1
- 1.0.9

* Fri Feb 22 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1.0.8-1
- 1.0.8

* Sun Nov 18 2007 Patrice Dumas <pertusus@free.fr> 1.0.7-2
- keep timestamps
- use rpm macros instead of hardcoded paths

* Sat Nov 17 2007 Lubomir Kundrak <lkundrak@redhat.com> 1.0.7-1
- Version bump

* Thu Nov 15 2007 Lubomir Kundrak <lkundrak@redhat.com> 1.0.3-2
- Some more fixes, thanks to Patrice Dumas (#329291)

* Fri Oct 12 2007 Lubomir Kundrak <lkundrak@redhat.com> 1.0.3-1
- Incorporating advises from Patrice Dumas (#329291) in account

* Fri Oct 12 2007 Lubomir Kundrak <lkundrak@redhat.com> 0.3.3.2etch1-1
- Initial package
