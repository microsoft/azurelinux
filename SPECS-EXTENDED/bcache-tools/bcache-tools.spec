Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Tools for Linux kernel block layer cache
Name: bcache-tools
Version: 1.1
Release: 3%{?dist}
License: GPLv2
URL: https://bcache.evilpiepirate.org/
VCS: git://git.kernel.org/pub/scm/linux/kernel/git/colyli/bcache-tools.git
# git clone git://git.kernel.org/pub/scm/linux/kernel/git/colyli/bcache-tools.git
# cd bcache-tools/
# git archive --format=tar --prefix=bcache-tools-1.1/ bcache-tools-1.1 | gzip > ../bcache-tools-1.1.tar.gz
Source0: %{_distro_sources_url}/%{name}-%{version}.tar.gz
# This part is a prerelease version obtained by https://gist.github.com/djwong/6343451:
# git clone https://gist.github.com/6343451.git
# cd 6343451/
# git archive --format=tar --prefix=bcache-status-20140220/ 6d278f9886ab5f64bd896080b1b543ba7ef6c7a6 | gzip > ../bcache-status-20140220.tar.gz
# see also https://article.gmane.org/gmane.linux.kernel.bcache.devel/1951
Source1: %{_distro_sources_url}/bcache-status-20140220.tar.gz
# bcache status not provided as a true package, so this is a self maintained
# man page for it
# https://article.gmane.org/gmane.linux.kernel.bcache.devel/1946
Patch0: %{name}-status-20160804-man.patch
# Process commandline arguments
Patch1: %{name}-1.1-cmdline.patch
# configure is not "Fedora compliant", do a small step in the
# right direction
Patch2: %{name}-20131018-fedconf.patch
# util-linux takes care of bcache superblock identification so we remove
# the probe-cache call (which is Fedora specific):
Patch3: %{name}-1.0.8-noprobe.2.patch
# proper include util-linux headers
Patch4: %{name}-1.1-util-linux-hdr.patch
# Fedora 23 uses python3 by default
Patch5: bcache-status-python3.patch
# Fix BZ#1360951 - this fix is python 3 only
Patch6: bcache-status-rootgc.patch
# Fedora packaging guidelines require man pages, none was provided for bcache. Add a placeholder
Patch7: bcache-tools-1.1-man.pach
# This is a kind of soft dependency: because we don't include probe-bcache
# we have to make sure that libblkid is able to identify bcache. So this
# is why it requires recent libblkid.
Requires: libblkid >= 2.24
Conflicts: dracut < 034
BuildRequires: libuuid-devel libblkid-devel libsmartcols-devel systemd gcc

%description
Bcache is a Linux kernel block layer cache. It allows one or more fast disk
drives such as flash-based solid state drives (SSDs) to act as a cache for
one or more slower hard disk drives.
This package contains the utilities for manipulating bcache.

%global _udevlibdir %{_prefix}/lib/udev
%global dracutlibdir %{_prefix}/lib/dracut

%prep
%setup -q -n bcache-tools-%{version}
tar xzf %{SOURCE1} --strip-components=1
%patch 0 -p1 -b .man
%patch 1 -p1 -b .cmdline
%patch 2 -p1 -b .fedconfmake
chmod +x configure
%patch 3 -p1 -b .noprobe
%patch 4 -p1 -b .util-linux-hdr

%patch 5 -p1 -b .python3
%patch 6 -p1 -b .rootgc
%patch 7 -p1 -b .man

%build
%configure
make %{?_smp_mflags}

%install
mkdir -p \
    %{buildroot}%{_sbindir} \
    %{buildroot}%{_mandir}/man8 \
    %{buildroot}%{_udevlibdir} \
    %{buildroot}%{_udevrulesdir} \
    %{buildroot}%{dracutlibdir}/modules.d

%make_install \
    INSTALL="install -p" \
    UDEVLIBDIR=%{_udevlibdir} \
    DRACUTLIBDIR=%{dracutlibdir} \
    MANDIR=%{_mandir}

# prevent complaints when checking for unpackaged files
rm %{buildroot}%{_udevlibdir}/probe-bcache
rm %{buildroot}%{_mandir}/man8/probe-bcache.8
rm %{buildroot}%{_prefix}/lib/initcpio/install/bcache
rm %{buildroot}%{_datarootdir}/initramfs-tools/hooks/bcache


install -p  -m 755 bcache-status %{buildroot}%{_sbindir}/bcache-status

%files
%license COPYING
%doc README
%{_udevrulesdir}/*
%{_mandir}/man8/*
%{_udevlibdir}/bcache-register
%{_udevlibdir}/bcache-params
%{_sbindir}/bcache
%{_sbindir}/bcache-super-show
%{_sbindir}/bcache-status
%{_sbindir}/make-bcache
%{dracutlibdir}/modules.d/90bcache

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1-3
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1-2
- Updating source URLs.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1-1
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Sat Jan 30 2021 Rolf Fokkens <rolf@rolffokkens.nl> - 1.1-0
- Changed upstream to git://git.kernel.org/pub/scm/linux/kernel/git/colyli/bcache-tools.git
- Updated to 1.1

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 21 2019 Rolf Fokkens <rolf@rolffokkens.nl> - 1.0.8-17
- Fix build with gcc-10 reported by Jeff Law <law@redhat.com>

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Rolf Fokkens <rolf@rolffokkens.nl> - 1.0.8-14
- Added Buildrequires gcc

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.8-12
- Use python3 always

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.8-7
- Rebuild for Python 3.6

* Sat Jul 09 2016 Rolf Fokkens <rolf@rolffokkens.nl> - 1.0.8-6
- Added experimental kernel cmdline parameter processing for bcache
- fixed bad non-root permission handling for --gc option (#1360951)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jun 20 2015 Rolf Fokkens <rolf@rolffokkens.nl> - 1.0.8-4
- bcache-status now explicitly uses python3 not python on Fedora 23 and up

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 Rolf Fokkens <rolf@rolffokkens.nl> - 1.0.8-2
- (#1224384) Now compiles on Fedora 22 / gcc 5.1.1

* Fri Dec 05 2014 Rolf Fokkens <rolf@rolffokkens.nl> - 1.0.8-1
- Sourced now from https://github.com/g2p/bcache-tools.git

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 10 2014 Rolf Fokkens <rolf@rolffokkens.nl> - 0.9-1
- Using the v0.9 git tag instead of the commit#
- Removed obsolete SOURCE2 (bcache-tools-dracut-module.tgz) way too late...

* Thu Feb 20 2014 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.16.20131018git
- (#1066555) updated bcache-status to latest upstream gist

* Fri Oct 18 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.15.20131018git
- updated bcache-tools to latest upstream git
- dracut module is now included upstream
- bcache-register no longer needs patching
- Makefile no longer needs patching

* Wed Oct 02 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.14.20130909git
- dropped pre F20 support; no use since deps on util-linux and dracut
- (#1004693) removed execute blkid in 61-bcache.rules
- (#1004693) moved 61-bcache.rules to 69-bcache.rules
- (#1004693) now inluding /usr/lib/dracut/modules.d/90bcache/...

* Mon Sep 30 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.13.20130909git
- (#1004693) add execute blkid in 61-bcache.rules

* Fri Sep 27 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.12.20130909git
- remove obsoleted probe-bcache in F20 using use_blkid macro

* Mon Sep 09 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.11.20130909git
- updated to new bcache-status
- updated to new bcache-tools
- added libblkid-devel to BuildRequires

* Fri Sep 06 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.10.20130827git
- fixed some udev related issues (#1004693)

* Mon Sep 02 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.9.20130827git
- fedconfmake.spec file renamed to fedconfmake.patch
- removed libuuid as dependency
- removed trailing white-spaces in patch lines
- removed CFLAGS= from configure section
- removed (empty) check section
- replaced "make install" with make_install macro
- updated summary

* Sat Aug 31 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.8.20130827git
- updated bcache-tools to commit 8327108eeaf3e0491b17d803da164c0827aae622
- corrected URL/VCS tag
- moved towards more RPM compliancy by using configure macro
- used "make install" to do most of the work
- added (empty) check section

* Mon Aug 26 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.7.20130820git
- updated bcache-status to latest upstream gist
- removed the -rules patch

* Mon Aug 26 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.6.20130820git
- removed tar and gcc from BuildRequires
- removed defattr from files section
- added upstream references to patches in comments 

* Sun Aug 25 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.5.20130820git
- moved bcache-register to /usr/lib/udev
- suppress bcache-register error output (caused by registering device twice)
- removed man page for bcache-register
- added bcache-status
- added tar and gcc to BuildRequires
- added python to Requires

* Sat Aug 24 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.4.20130820git
- Fixed the udev rules for Fedora

* Thu Aug 22 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.3.20130820git
- Added systemd to BuildRequires

* Thu Aug 22 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.2.20130820git
- Fixed initial review feedback

* Tue Aug 20 2013 Rolf Fokkens <rolf@rolffokkens.nl> - 0-0.1.20130820git
- Initial build
