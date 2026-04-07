# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: gfs2-utils
Version: 3.6.1
Release: 2%{?dist}
# Refer to doc/README.licence in the upstream tarball
License: GPL-2.0-or-later AND LGPL-2.1-or-later
Summary: Utilities for managing the global file system (GFS2)
%ifnarch %{arm}
%{?fedora:Recommends: kmod(gfs2.ko) kmod(dlm.ko)}
%endif
# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}
BuildRequires: ncurses-devel
BuildRequires: kernel-headers
BuildRequires: automake
BuildRequires: libtool
BuildRequires: zlib-devel
BuildRequires: gettext-devel
BuildRequires: bison
BuildRequires: flex
BuildRequires: libblkid-devel
BuildRequires: libuuid-devel
BuildRequires: check-devel
BuildRequires: bzip2-devel
BuildRequires: make
Source: https://releases.pagure.org/gfs2-utils/gfs2-utils-%{version}.tar.gz
URL: https://pagure.io/gfs2-utils

%prep
%autosetup -p1

%build
./autogen.sh
%configure
%make_build

%check
make check || { cat tests/testsuite.log; exit 1; }

%install
%make_install
# Don't ship gfs2_{trace,lockcapture} in this package
rm -f %{buildroot}%{_sbindir}/gfs2_trace
rm -f %{buildroot}%{_sbindir}/gfs2_lockcapture
rm -f %{buildroot}%{_mandir}/man8/gfs2_trace.8
rm -f %{buildroot}%{_mandir}/man8/gfs2_lockcapture.8

%description
The gfs2-utils package contains a number of utilities for creating, checking,
modifying, and correcting inconsistencies in GFS2 file systems.

%files
%doc doc/COPYING.* doc/COPYRIGHT doc/*.txt
%doc doc/README.contributing doc/README.licence
%{_sbindir}/fsck.gfs2
%{_sbindir}/gfs2_grow
%{_sbindir}/gfs2_jadd
%{_sbindir}/mkfs.gfs2
%{_sbindir}/gfs2_edit
%{_sbindir}/tunegfs2
%{_sbindir}/glocktop
%{_libexecdir}/gfs2_withdraw_helper
%{_mandir}/man8/*gfs2*
%{_mandir}/man8/glocktop*
%{_mandir}/man5/*
%{_prefix}/lib/udev/rules.d/82-gfs2-withdraw.rules

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Feb 27 2025 Andrew Price <anprice@redhat.com> - 3.6.1-1
- New upstream release

* Mon Jan 20 2025 Andrew Price <anprice@redhat.com> - 3.5.1-7
- Don't hardcode /usr/sbin in the spec

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 11 2023 Andrew Price <anprice@redhat.com> - 3.5.1-1
- New upstream release

* Thu Feb 09 2023 Andrew Price <anprice@redhat.com> - 3.5.0-1
- New upstream release
- Drop all patches
- Exclude i686 for https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
- Migrate to SPDX license identifier

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 23 2022 Andrew Price <anprice@redhat.com> - 3.4.1-4
- gfs2/edit: always use "%s"-style format for printf()-style functions
- Custom patch to fix a printw() call missed by the above
  Fixes a build failure due to format-security warnings being treated as errors

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar 15 2021 Andrew Price <anprice@redhat.com> - 3.4.1-1
- New upstream version

* Mon Mar 08 2021 Andrew Price <anprice@redhat.com> - 3.4.0-1
- New upstream version
- Update testsuite script

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 03 2020 Andrew Price <anprice@redhat.com> - 3.3.0-2
- Version bump to enable gating tests

* Tue Sep 01 2020 Andrew Price <anprice@redhat.com> - 3.3.0-1
- New upstream version
- Add dependency on bzip2
- Drop all patches
- gfs2_withdraw_helper is now in /usr/libexec/

* Wed Jul 29 2020 Andrew Price <anprice@redhat.com> - 3.2.0-10
- tests: Don't use fail_unless in unit tests
  Fixes build failures due to a regression in check-devel

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Andrew Price <anprice@redhat.com> - 3.2.0-8
- Use make_build and make_install macros
  https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro
- Remove -C gfs2 - it's a remnant from the cluster.git days
- Remove unnecessary header notice from spec file

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
