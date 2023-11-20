###############################################################################
###############################################################################
##
##  Copyright (C) 2004-2018 Red Hat, Inc.  All rights reserved.
##
##  This copyrighted material is made available to anyone wishing to use,
##  modify, copy, or redistribute it subject to the terms and conditions
##  of the GNU General Public License v.2.
##
###############################################################################
###############################################################################
Summary:        Utilities for managing the global file system (GFS2)
Name:           gfs2-utils
Version:        3.2.0
Release:        12%{?dist}
License:        GPLv2+ AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pagure.io/gfs2-utils
Source:         https://releases.pagure.org/gfs2-utils/gfs2-utils-%{version}.tar.gz
Patch0:         0-Fix_libuuid_linking.patch
Patch1:         1-Fix_more_linking_errors.patch
Patch2:         fix-format-security.patch

BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  check-devel
BuildRequires:  flex
BuildRequires:  gettext-devel
BuildRequires:  kernel-headers
BuildRequires:  libblkid-devel
BuildRequires:  libtool
BuildRequires:  libuuid-devel
BuildRequires:  ncurses-devel
BuildRequires:  zlib-devel

Recommends:     kmod(dlm.ko)
Recommends:     kmod(gfs2.ko)

%prep
%autosetup -p1

%build
./autogen.sh
%configure
make %{_smp_mflags} V=1

%check
make check || { cat tests/testsuite.log; false; }

%install
make -C gfs2 install DESTDIR=%{buildroot}
# Don't ship gfs2_{trace,lockcapture} in this package
rm -f %{buildroot}%{_sbindir}/gfs2_trace
rm -f %{buildroot}%{_sbindir}/gfs2_lockcapture
rm -f %{buildroot}%{_mandir}/man8/gfs2_trace.8
rm -f %{buildroot}%{_mandir}/man8/gfs2_lockcapture.8

%description
The gfs2-utils package contains a number of utilities for creating, checking,
modifying, and correcting inconsistencies in GFS2 file systems.

%files
%license doc/COPYING.* doc/README.licence doc/COPYRIGHT
%doc doc/README.contributing doc/*.txt
%{_sbindir}/fsck.gfs2
%{_sbindir}/gfs2_grow
%{_sbindir}/gfs2_jadd
%{_sbindir}/mkfs.gfs2
%{_sbindir}/gfs2_convert
%{_sbindir}/gfs2_edit
%{_sbindir}/tunegfs2
%{_sbindir}/gfs2_withdraw_helper
%{_sbindir}/glocktop
%{_mandir}/man8/*gfs2*
%{_mandir}/man8/glocktop*
%{_mandir}/man5/*
%{_libdir}/udev/rules.d/82-gfs2-withdraw.rules

%changelog
* Tue Sep 26 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.2.0-12
- Removing 'exit' calls from the '%%check' section.

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.2.0-11
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Jun 17 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.2.0-10
- Add upstream patch to fix -Werror=format-security errors after ncurses 6.3 upgrade

* Fri Apr 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.2.0-9
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.2.0-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Andrew Price <anprice@redhat.com> - 3.2.0-5
- Fix libuuid linking

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 21 2018 Andrew Price <anprice@redhat.com> - 3.2.0-2
- Recommend the gfs2 and dlm kmods instead of requiring them
  Resolves: bz#1593411

* Thu May 24 2018 Andrew Price <anprice@redhat.com> - 3.2.0-1
- New upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 13 2017 Andrew Price <anprice@redhat.com> - 3.1.10-4
- Update URL in spec file

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 28 2017 Andrew Price <anprice@redhat.com> - 3.1.10-1
- New upstream release
- Make dependency on libuuid explicit

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 07 2016 Andrew Price <anprice@redhat.com> - 3.1.9-1
- New upstream release
- Drop all patches
- Add glocktop to the package

* Mon Feb 15 2016 Andrew Price <anprice@redhat.com> - 3.1.8-7
- libgfs2: Add support for dirent.de_rahead
- gfs2_edit: Include dirent.de_rahead in directory listings
- gfs2-utils: Add a check for the de_rahead field
- libgfs2: Support the new dirent de_cookie field
  Resolves: bz#1307532

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 20 2015 Andrew Price <anprice@redhat.com> - 3.1.8-5
- Add patches to install the withdraw helper script properly:
  scripts_rename_gfs2_wd_udev_sh_to_gfs2_withdraw_helper.patch
  scripts_install_the_withdraw_helper_script.patch
  scripts_install_the_withdraw_udev_rules_script.patch
- Remove the obsolete udev script installation bits

* Tue Aug 11 2015 Andrew Price <anprice@redhat.com> - 3.1.8-4
- gfs2-utils: Fix hang on withdraw
- Install udev withdraw handler scripts

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 18 2015 Andrew Price <anprice@redhat.com> - 3.1.8-2
- fsck.gfs2: replace recent i_goal fixes with simple logic

* Tue Apr 07 2015 Andrew Price <anprice@redhat.com> - 3.1.8-1
- New upstream release
- Remove perl dependency
- Update spec per the latest packaging guidelines

* Mon Sep 08 2014 Andrew Price <anprice@redhat.com> - 3.1.7-1
- New upstream release
- Drop all patches
- gfs2-utils tests: Build unit tests with consistent cpp flags

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Josh Boyer <jwboyer@fedoraproject.org> - 3.1.6-7
- Switch to using Requires on individual kernel modules
  Resolves: bz#1056191

* Fri Mar 21 2014 Andrew Price <anprice@redhat.com> - 3.1.6-6
- gfs2_grow: Don't try to open an empty string
- libgfs2: Add lgfs2 open mnt functions
- Switch is pathname mounted callers to lgfs2 open mnt
- libgfs2 Remove is pathname mounted
  Resolves: bz#1079286

* Fri Oct 04 2013 Andrew Price <anprice@redhat.com> - 3.1.6-5
- Suppress req on kernel-modules-extra for ARM arches.

* Tue Sep 17 2013 Andrew Price <anprice@redhat.com> - 3.1.6-4
- Don't use README.* for docs (it can pick up some patch files)

* Wed Aug 21 2013 Andrew Price <anprice@redhat.com> - 3.1.6-3
- Install utils into /usr/sbin instead of /sbin
  Resolves: rhbz#996539

* Mon Jul 29 2013 Andrew Price <anprice@redhat.com> - 3.1.6-2
- Don't install gfs2_lockcapture and gfs2_trace
  Resolves: rhbz#987019
- Run test suite after build (requires check-devel build req)
- Install both of the READMEs into doc/

* Wed Jul 24 2013 Andrew Price <anprice@redhat.com> - 3.1.6-1
- New upstream release
- Drop 'file' requirement - mkfs.gfs2 now uses libblkid instead
- Drop 'ncurses' requirement - dependency is added automatically
- Drop requires chkconfig and initscripts - no longer installs daemons
- Drop fix_build_on_rawhide.patch - upstream
- Add build req on libblkid-devel

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild
