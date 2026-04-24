# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#%%global devrel dev.12
%global devrel %{nil}

Summary: A text-based Web browser
Name: lynx
Version: 2.9.2
#Release: %%{devrel}.1%%{?dist}
Release: 5%{?dist}
License: GPL-2.0-only

Source0: https://invisible-island.net/archives/lynx/tarballs/lynx%{version}%{devrel}.tar.bz2
Source1: https://invisible-island.net/archives/lynx/tarballs/lynx%{version}%{devrel}.tar.bz2.asc
Source2: https://invisible-island.net/public/dickey@invisible-island.net-rsa3072.asc

URL: https://lynx.invisible-island.net/

# RH specific tweaks - directory layout, utf-8 by default, misc. configuration
Patch0: lynx-2.8.9-redhat.patch

# patch preparing upstream sources for rpmbuild, in particular for parallel make
Patch1: lynx-2.8.9-build.patch

# prompt user before executing command via a lynxcgi link even in advanced mode,
# as the actual URL may not be shown but hidden behind an HTTP redirect and set
# TRUSTED_LYNXCGI:none in lynx.cfg to disable all lynxcgi URLs by default
# [CVE-2008-4690]
Patch2: lynx-CVE-2008-4690.patch

Provides: webclient
Provides: text-www-browser
BuildRequires: brotli-devel
BuildRequires: bzip2-devel
BuildRequires: dos2unix
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: gnupg2
BuildRequires: libidn2-devel
BuildRequires: make
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: telnet
BuildRequires: unzip
BuildRequires: zip
BuildRequires: zlib-devel

# provides /usr/share/doc/HTML/en-US/index.html used as STARTFILE on RHEL
%if 0%{?rhel} && !0%{?eln}
Requires: redhat-indexhtml
%endif

%description
Lynx is a text-based Web browser. Lynx does not display any images,
but it does support frames, tables, and most other HTML tags. One
advantage Lynx has over graphical browsers is speed; Lynx starts and
exits quickly and swiftly displays web pages.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1 -n lynx%{version}%{devrel}

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
sed -e "s,^HELPFILE:.*,HELPFILE:file://localhost%{_pkgdocdir}/lynx_help/lynx_help_main.html,g" -i lynx.cfg
%if 0%{?rhel} && !0%{?eln}
sed -e 's,^STARTFILE:.*,STARTFILE:file:/usr/share/doc/HTML/en-US/index.html,' -i lynx.cfg
%endif

%build
# These options are specified explicitly below but are also defaults in 2.9.0:
#   --enable-addrlist-page
#   --enable-cjk
#   --enable-file-upload
#   --enable-japanese-utf8
#   --enable-justify-elts
#   --enable-locale-charset
#   --enable-persistent-cookies
#   --enable-prettysrc
#   --enable-read-eta
#   --enable-scrollbar
#   --enable-source-cache
#   --with-brotli
#   --with-bzlib
#   --with-zlib
%configure --libdir=/etc            \
    --disable-font-switch           \
    --disable-rpath-hack            \
    --enable-addrlist-page          \
    --enable-charset-choice         \
    --enable-cgi-links              \
    --enable-cjk                    \
    --enable-debug                  \
    --enable-default-colors         \
    --enable-externs                \
    --enable-file-upload            \
    --enable-gzip-help              \
    --enable-internal-links         \
    --enable-ipv6                   \
    --enable-japanese-utf8          \
    --enable-justify-elts           \
    --enable-locale-charset         \
    --enable-kbd-layout             \
    --enable-libjs                  \
    --enable-nls                    \
    --enable-nsl-fork               \
    --enable-persistent-cookies     \
    --enable-prettysrc              \
    --enable-read-eta               \
    --enable-scrollbar              \
    --enable-source-cache           \
    --enable-warnings               \
    --with-screen=ncursesw          \
    --with-ssl=%{_libdir}           \
    --with-brotli                   \
    --with-bzlib                    \
    --with-zlib                     \
    ac_cv_path_RLOGIN=/usr/bin/rlogin

%make_build

%install
chmod -x samples/mailto-form.pl
%make_install

# remove unneeded files
rm -f docs/{OS-390.announce,README.jp}
rm -f samples/*.bat

# convert line endings
dos2unix samples/lynx-demo.cfg
dos2unix samples/midnight.lss

cat >$RPM_BUILD_ROOT%{_sysconfdir}/lynx-site.cfg <<EOF
# Place any local lynx configuration options (proxies etc.) here.
EOF

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc docs README samples
%doc test lynx.hlp lynx_help
%{_bindir}/lynx
%{_mandir}/man1/lynx.1.*
%config(noreplace) %{_sysconfdir}/lynx.cfg
%config(noreplace) %{_sysconfdir}/lynx.lss
%config(noreplace,missingok) %{_sysconfdir}/lynx-site.cfg

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 03 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.9.2-1
- rebase to latest upstream version (rhbz#2284168)

* Fri Apr 26 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.9.1-1
- rebase to latest upstream version (rhbz#2277307)

* Tue Jan 23 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.9.0-4
- enable bzip2 support

* Mon Jan 22 2024 Thomas E. Dickey <dickey@invisible-island.net> - 2.9.0-3
- add brotli build-dependency
- restore formerly-empty sample files
- remove a couple of obsolete workarounds for installing

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.9.0-1
- rebase to latest upstream version

* Fri Oct 13 2023 Lukáš Zaoral <lzaoral@redhat.com> - 2.9.0-dev.12.2
- fix FTBFS in Fedora Rawhide (rhbz#2243829)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-dev.12.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 03 2023 Lukáš Zaoral <lzaoral@redhat.com> - 2.9.0-dev.12.1
- %%{gpgverify} sources
- remove upstreamed patches
- update to new upstream release
- use compressed man pages

* Wed May 03 2023 Lukáš Zaoral <lzaoral@redhat.com> - 2.9.0-dev.10.2.5
- fix SIGABRT after start (rhbz#2185402)

* Tue Apr 11 2023 Lukáš Zaoral <lzaoral@redhat.com> - 2.9.0-dev.10.2.4
- migrate to SPDX license format

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-dev.10.2.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec  2 2022 Florian Weimer <fweimer@redhat.com> - 2.9.0-dev.10.2.2
- Port the configure script to C99

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-dev.10.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Kamil Dudka <kdudka@redhat.com> - 2.9.0dev.10.2
- add presentation type for xhtml

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-dev.10.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Kamil Dudka <kdudka@redhat.com> - 2.9.0dev.10.1
- add BR for libidn2-devel (#1910971)

* Fri Jan 07 2022 Thomas E. Dickey - 2.9.0dev.10
- Correct homepage URL.
- Update to lynx 2.9.0dev.10, removing obsolete patches.

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.8.9-14
- Rebuilt with OpenSSL 3.0.0

* Tue Aug 31 2021 Kamil Dudka <kdudka@redhat.com> - 2.8.9-13
- fix disclosure of HTTP auth credentials via SNI data (CVE-2021-38165)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 30 2020 Kamil Dudka <kdudka@redhat.com> - 2.8.9-10
- remove unused build-time dependency on slang-devel (#1910966)

* Thu Aug 06 2020 Merlin Mathesius <mmathesi@redhat.com> - 2.8.9-9
- Skip RHEL-specific Requires and STARTFILE edit when building for ELN

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 11 2019 Kamil Dudka <kdudka@redhat.com> - 2.8.9-5
- include license file in the package (#1686886)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 08 2018 Kamil Dudka <kdudka@redhat.com> - 2.8.9-3
- fix bugs detected by static analysis

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Kamil Dudka <kdudka@redhat.com> - 2.8.9-1
- update to the latest upstream release

* Wed May 23 2018 Kamil Dudka <kdudka@redhat.com> - 2.8.9-0.23.dev19
- do not require 'rsh' installed at build time (#1581747)
- update to the latest upstream pre-release

* Mon Feb 19 2018 Kamil Dudka <kdudka@redhat.com> - 2.8.9-0.22.dev16
- add explicit BR for the gcc compiler

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-0.21.dev16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-0.20.dev16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Florian Weimer <fweimer@redhat.com> - 2.8.9-0.19.dev16
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-0.18.dev16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.9-0.17.dev16
- fix rpmlint warnings
- do not depend on perl
- update upstream project URL
- update to the latest upstream pre-release

* Wed May 17 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.9-0.16.dev14
- update to the latest upstream pre-release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-0.15.dev11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Kamil Dudka <kdudka@redhat.com> - 2.8.9-0.14.dev11
- update to the latest upstream pre-release (fixes CVE-2016-9179)

* Thu Oct 20 2016 Kamil Dudka <kdudka@redhat.com> - 2.8.9-0.13.dev9
- fix compatibility with OpenSSL 1.1

* Wed Oct 12 2016 Kamil Dudka <kdudka@redhat.com> - 2.8.9-0.12.dev9
- update to the latest upstream pre-release

* Sat Feb 06 2016 Kamil Dudka <kdudka@redhat.com> - 2.8.9-0.11.dev6
- avoid using rpath for the lynx executable
- remove zero-length tests files to silence rpmlint

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.9-0.10.dev6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 09 2015 Kamil Dudka <kdudka@redhat.com> - 2.8.9-0.9.dev6
- update to the latest upstream pre-release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.9-0.8.dev5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 28 2015 Kamil Dudka <kdudka@redhat.com> - 2.8.9-0.7.dev5
- update to the latest upstream pre-release

* Wed Feb 11 2015 Ville Skyttä <ville.skytta@iki.fi> - 2.8.9-0.6.dev4
- do not remove -g from our CFLAGS (#1191706)

* Wed Jan 28 2015 Kamil Dudka <kdudka@redhat.com> - 2.8.9-0.5.dev4
- update to the latest upstream pre-release
- drop a compiler wrapper no longer needed
- do not override compiler/linker flags given by the build system

* Mon Jan 05 2015 Kamil Dudka <kdudka@redhat.com> - 2.8.9-0.4.dev2
- update to the latest upstream pre-release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.9-0.3.dev1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.9-0.2.dev1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Kamil Dudka <kdudka@redhat.com> - 2.8.9-0.1.dev1
- update to the latest upstream pre-release

* Fri Aug 09 2013 Kamil Dudka <kdudka@redhat.com> - 2.8.8-0.3.dev16
- update to the latest upstream pre-release
- make the help working with unversioned docdir (#993909)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.8-0.2.dev15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Kamil Dudka <kdudka@redhat.com> - 2.8.8-0.1.dev15
- update to the latest upstream pre-release
- drop applied patches
- drop lynx-2.8.6-backgrcolor.patch (#908449)

* Tue Sep 11 2012 Kamil Dudka <kdudka@redhat.com> - 2.8.7-12
- set STARTFILE to a local file when building for RHEL

* Fri Sep 07 2012 Kamil Dudka <kdudka@redhat.com> - 2.8.7-11
- fix typo in the man page (#854574)

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 2.8.7-10
- sync the upstream tarball with the current upstream version
- fix specfile issues reported by the fedora-review script

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 27 2011 Kamil Dudka <kdudka@redhat.com> - 2.8.7-7
- include read-only text fields on form submission (#679266)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 07 2010 Kamil Dudka <kdudka@redhat.com> - 2.8.7-5
- upstream patch that limits length of parsed URIs (#605286)

* Thu Apr 08 2010 Kamil Dudka <kdudka@redhat.com> - 2.8.7-4
- allow IPv6 addresses without http:// prefix (#425879)

* Wed Apr 07 2010 Kamil Dudka <kdudka@redhat.com> - 2.8.7-3
- avoid build failure caused by mistakenly excluded <locale.h>

* Wed Jan 13 2010 Kamil Dudka <kdudka@redhat.com> - 2.8.7-2
- make it possible to delete a bookmark when ~/lynx_bookmarks.html is writable
  by group (#486070)

* Tue Jan 05 2010 Kamil Dudka <kdudka@redhat.com> - 2.8.7-1
- new upstream release
- dropped applied patches
- fixed regression from #533004
- cleanup in BuildRequires

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.8.6-22
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 2.8.6-19
- rebuild with new openssl

* Fri Nov  7 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 2.8.6-18
- Fixed CVE-2008-4690 lynx: remote arbitrary command execution.
  via a crafted lynxcgi: URL (thoger)

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.8.6-17
- fix license tag

* Thu May 29 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 2.8.6-16
- updated to latest stable version 2.8.6rel5
- Resolves: #214205
- added build patches from Dennis Gilmore
- skipped 2 releases to correct the NVR path

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.8.6-13
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 2.8.6-12
- added telnet, rsh, zip and unzip to BuildRequires
- Resolves: #430508

* Tue Jan  8 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 2.8.6-11
- fixed crash when using formatting character '$' in translation
- Resolves: #426449

* Tue Dec 11 2007 Ivana Varekova <varekova@redhat.com> - 2.8.6-10
- add default-colors option, change default setting (#409211)

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 2.8.6-9
- Rebuild for openssl bump

* Wed Dec  5 2007 Ivana Varekova <varekova@redhat.com> - 2.8.6-8
- rebuild

* Fri Oct 12 2007 Ivana Varekova <varekova@redhat.com> - 2.8.6-7
- add provides:text-www-browser flag

* Tue Oct  2 2007 Ivana Varekova <varekova@redhat.com> - 2.8.6-6
- fix 311031 - fix argument parsing

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.8.6-5
- Rebuild for selinux ppc32 issue.

* Tue Jul 17 2007 Ivana Varekova <varekova@redhat.com> - 2.8.6-4
- remove default-colors option

* Fri Feb 23 2007 Ivana Varekova <varekova@redhat.com> - 2.8.6-3
- incorporate package review feedback (#226113)

* Wed Oct 25 2006 Ivana Varekova <varekova@redhat.com> - 2.8.6-2
- add japanese unicode support (#143787)

* Tue Oct 24 2006 Ivana Varekova <varekova@redhat.com> - 2.8.6-1
- update to 2.8.6

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.8.5-28.1
- rebuild

* Tue May 30 2006 Ivana Varekova <varekova@redhat.com> - 2.8.5-28
- add buildreq gettext (#193515)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.8.5-27.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.8.5-27.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Nov 13 2005 Tim Waugh <twaugh@redhat.com> 2.8.5-27
- Apply patch to fix CVE-2005-2929 (bug #172973).

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 2.8.5-26
- rebuilt against new openssl

* Wed Nov  9 2005 Tim Waugh <twaugh@redhat.com> 2.8.5-25
- Rebuild for new openssl.

* Mon Oct 17 2005 Tim Waugh <twaugh@redhat.com> 2.8.5-24
- Apply patch to fix CAN-2005-3120 (bug #170253).

* Tue Mar 29 2005 Tim Waugh <twaugh@redhat.com> 2.8.5-23
- Fixed fix for bug #90302 (bug #152146).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 2.8.5-22
- Rebuild for new GCC.

* Thu Jan  6 2005 Tim Waugh <twaugh@redhat.com> 2.8.5-21
- Fixed <option> handling (bug #90302).

* Thu Dec 30 2004 Tim Waugh <twaugh@redhat.com> 2.8.5-20
- Added --enable-locale-charset compilation option, set LOCALE_CHARSET
  on in the config file and removed i18ncfg patch (bug #124849).

* Fri Nov 19 2004 Tim Waugh <twaugh@redhat.com> 2.8.5-19
- 2.8.5rel1.  Fixes bug #139783.

* Thu Jul  8 2004 Tim Waugh <twaugh@redhat.com> 2.8.5-18
- Removed perl dependencies (bug #127423).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 25 2004 Tim Waugh <twaugh@redhat.com> 2.8.5-16
- No longer need lynx-284-ipv6-salen.patch.
- No longer need lynx2-8-2-telnet.patch.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 2.8.5-15
- rebuilt

* Mon Dec  1 2003 Tim Waugh <twaugh@redhat.com> 2.8.5-14
- Updated to dev16, fixing bug #110196.
- No longer need crlf patch.
- Use shipped ja translations.
- Use %%find_lang.
- Default config file now sets UTF-8 (bug #110986).

* Fri Jun 06 2003 Adrian Havill <havill@redhat.com> 2.8.5-13
- use wide version of ncurses for UTF-8

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Waugh <twaugh@redhat.com> 2.8.5-10
- Fix CRLF issue.

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.8.5-9
- rebuild

* Fri Dec 20 2002 Elliot Lee <sopwith@redhat.com> 2.8.5-8
- _smp_mflags

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- use openssl pkg-config data, if available

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Thu Aug 08 2002 Karsten Hopp <karsten@redhat.de>
- remove menu entry (#69457)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 13 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.5-3
- Fix build with current toolchain

* Thu Nov 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.5-2
- Update (dev5)

* Wed Oct 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.5-1
- Update (dev3)
- Use "display" as image viewer (#54184)

* Tue Jul 31 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.4-17
- 2.8.4 release - no need to ship prerelease code...

* Thu Jul 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.4-16
- update to 2.8.4p5 (bugfix release)

* Tue Jul 10 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.4-15
- Add site-cfg file (#43841)

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.4-14
- 2.8.4p2

* Thu Jun 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- support newer gettext version

* Thu May  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.4-12
- --with-display=ncurses, fixes #37481

* Wed May  2 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.8.4-11
- Add Czech/Slovak patches from milan.kerslager@spsselib.hiedu.cz (RFE#38334)

* Sun Apr 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- dev20
- Add ipv6 patches from Pekka Savola <pekkas@netcore.fi>:
  - enable ipv6, patch for missing sockaddr sa_len
  - buildrequires: slang-devel, zlib-devel
  (Bug #35644)

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Jan  4 2001 Nalin Dahyabhai <nalin@redhat.com>
- Fix up more of the i18ncfg patch

* Wed Jan  3 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.8.4dev16
- Fix up the i18ncfg patch - segfaulting on startup is not exactly
  a nice feature.
- Mark locale related files as such
- Mark /etc/lynx.cfg.ja as %%lang(ja)
- Add BuildRequires

* Thu Dec 21 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add -enable-nls --with-included-gettext
- Add i18ncfg patch
- Add Japanese resources

* Thu Oct  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update build URL
- Fix help (Bug #18394)
- Replace the "index page link" (pointing to a Mosaic site with thousands
  of dead links) with a link to Google

* Sat Sep 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add https:// support (#17554)
- Update to dev10

* Fri Aug  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add Swedish and German translations to desktop file, Bug 15322

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.8.4.dev.4

* Mon Jul 10 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up location of standard page and help page in lynx.cfg (still
  pointed at /usr/doc instead of /usr/share/doc, Bug #13227)

* Thu Jun 8 2000 Tim Powers <timp@redhat.com>
- fixed man page lolcation to be FHS compliant
- use predefined RPM macros wherever possible
- use %%makeinstall
- cleaned up files list

* Wed Apr 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- 2.8.3rel.1

* Tue Mar 28 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.8.3dev23
- add URL header

* Mon Feb 07 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Sat Feb 05 2000 Cristian Gafton <gafton@redhat.com>
- version 2.8.3dev18
- drop the RFC compliance patch - they seemed to have done theiir own
- pray that ported patches are okay

* Mon Jan 31 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add "passive mode ftp" option, activated by PASSIVE:TRUE in /etc/lynx.cfg
- turn on "PASSIVE:TRUE" by default
- deal with the fact that RPM compresses man pages.

* Sun Jan 16 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add "view with less" download option

* Wed Nov  3 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix compliance with RFCs describing FTP.
  We can now connect to wu-ftpd >= 2.6.0 based servers.

* Wed Aug 25 1999 Bill Nottingham <notting@redhat.com>
- fix path to help file.
- turn off font switching
- disable args to telnet.

* Tue Jun 15 1999 Bill Nottingham <notting@redhat.com>
- update to 2.8.2

* Mon Mar 29 1999 Bill Nottingham <notting@redhat.com>
- apply some update patches from the lynx folks
- set user's TEMP dir to their home dir to avoid /tmp races

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 10)

* Wed Feb 24 1999 Bill Nottingham <notting@redhat.com>
- return of wmconfig

* Mon Nov 30 1998 Bill Nottingham <notting@redhat.com>
- create cookie file 0600

* Fri Nov  6 1998 Bill Nottingham <notting@redhat.com>
- update to 2.8.1rel2

* Thu Oct 29 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide (slang-1.2.2)

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- 2.8.1pre9
- strip binaries

* Mon Oct 05 1998 Cristian Gafton <gafton@redhat.com>
- updated to lynx2.8.1pre.7.tar.gz

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon May 04 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 2.8rel3
- fixed mailto: buffer overflow (used Alan's patch)

* Fri Mar 20 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.8
- added buildroot

* Tue Jan 13 1998 Erik Troan <ewt@redhat.com>
- updated to 2.7.2
- enabled lynxcgi

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 2.6 to 2.7.1
- moved /usr/lib/lynx.cfg to /etc/lynx.cfg
- build with slang instead of ncurses
- made default startup file be file:/usr/doc/HTML/index.html

