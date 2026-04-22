# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: A utility for retrieving files using the HTTP or FTP protocols
Name: wget1
Version: 1.25.0
Release: 3%{?dist}
# Generally wget is distributed under GPLv3 or later but there are files in lib/ directory
# which are under LGPLv2.1 or later and are actually built into the resulting rpm.
# This version of wget is built with gnutls so I believe that the 'with openssl'
# part in some files is not applicable here.
License: GPL-3.0-or-later AND LGPL-2.1-or-later
Url: http://www.gnu.org/software/wget/
Source: https://ftp.gnu.org/gnu/wget/wget-%{version}.tar.gz

Patch1: wget-1.17-path.patch

Provides: bundled(gnulib) 
# needed for test suite
BuildRequires: make
BuildRequires: perl(lib)
BuildRequires: perl(English)
BuildRequires: perl(HTTP::Daemon)
BuildRequires: python3
BuildRequires: gnutls-devel
BuildRequires: pkgconfig
BuildRequires: texinfo
BuildRequires: gettext
BuildRequires: autoconf
BuildRequires: libidn2-devel
BuildRequires: libuuid-devel
BuildRequires: perl-podlators
BuildRequires: libpsl-devel
BuildRequires: gpgme-devel
BuildRequires: gcc
BuildRequires: zlib-devel
BuildRequires: git-core

%description
GNU Wget is a file retrieval utility which can use either the HTTP or
FTP protocols. Wget features include the ability to work in the
background while you are logged out, recursive retrieval of
directories, file name wildcard matching, remote file timestamp
storage and comparison, use of Rest with FTP servers and Range with
HTTP servers to retrieve files over slow or unstable connections,
support for Proxy servers, and configurability.

%package wget
Summary: %{name} shim to provide wget
Requires: wget1%{?_isa} = %{version}-%{release}
# Replace wget2
Conflicts: wget >= 2.0
Provides: wget = %{version}-%{release}
Provides: wget%{?_isa} = %{version}-%{release}
# From original wget package
Provides: webclient

%description wget
This package provides the shim links for %{name} to be automatically
used in place of wget. This ensures that %{name} is used as
the system provider of wget.

%prep
%autosetup -S git -n wget-%{version}

# modify the package string
sed -i "s|\(PACKAGE_STRING='wget .*\)'|\1 (Red Hat modified)'|" configure
grep "PACKAGE_STRING='wget .* (Red Hat modified)'" configure || exit 1

%build
%configure \
    --with-ssl=gnutls \
    --with-libpsl \
    --enable-largefile \
    --enable-opie \
    --enable-digest \
    --enable-ntlm \
    --enable-nls \
    --enable-ipv6 \
    --disable-rpath \
    --without-metalink \
    --disable-year2038

%{make_build}

%install
%{make_install} CFLAGS="%{build_cflags}"
rm -f %{buildroot}%{_infodir}/dir

# Rename the binary and docs
mv %{buildroot}%{_bindir}/wget %{buildroot}%{_bindir}/%{name}
mv %{buildroot}%{_mandir}/man1/wget.1 %{buildroot}%{_mandir}/man1/%{name}.1

# Create links for the wget1-wget
ln -sr %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/wget
# Link wget(1) to wget1(1)
echo ".so man1/%{name}.1" > %{buildroot}%{_mandir}/man1/wget.1

%find_lang wget
%find_lang wget-gnulib

##%check
##make check

%files -f wget.lang -f wget-gnulib.lang
%license AUTHORS COPYING
%doc MAILING-LIST NEWS README doc/sample.wgetrc
%{_mandir}/man1/%{name}.*
%{_bindir}/%{name}
%{_infodir}/wget.info.*

%files wget
%{_mandir}/man1/wget.*
%{_bindir}/wget
%config(noreplace) %{_sysconfdir}/wgetrc

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 05 2025 Michal Ruprich <mruprich@redhat.com> - 1.25.0-1
- Update to 1.25.0
- Rename package from wget to wget1
- Add wget1-wget subpackage to allow usage as wget

* Tue Mar 05 2024 Michal Ruprich <mruprich@redhat.com> - 1.21.4-1
- New version 1.21.4

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 21 2023 Michal Ruprich <mruprich@redhat.com> - 1.21.3-6
- SPDX migration
- Disable metalink in RHEL builds

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 21 2022 Michal Ruprich <mruprich@redhat.com> - 1.21.3-3
- Changing previous 32b fix to a proper one

* Tue Mar 15 2022 Michal Ruprich <mruprich@redhat.com> - 1.21.3-2
- Removing some forgotten lines from the spec

* Tue Mar 15 2022 Michal Ruprich <mruprich@redhat.com> - 1.21.3-1
- New version 1.21.3

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 19 2021 Michal Ruprich <mruprich@redhat.com> - 1.21.2-2
- Fix for #2014743 - wget regression SSL_INIT output even with --quiet enabled

* Mon Oct 11 2021 Michal Ruprich <mruprich@redhat.com> - 1.21.2-1
- New version 1.21.2
- Fix for #2010039 - [abrt] wget: find_cell(): wget killed by SIGSEGV

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 12 2021 Michal Ruprich <mruprich@redhat.com> - 1.21.1-3
- Resolves bug #1944262 - wget in F33 arm is unable to download files larger than 2GiB

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Michal Ruprich <mruprich@redhat.com> - 1.21.1-1
- Update to 1.21.1

* Thu Nov 19 2020 Michal Ruprich <mruprich@redhat.com> - 1.20.3-9
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Thu Jul 30 2020 Tomas Hozza <thozza@redhat.com> - 1.20.3-8
- Fix too verbose output even with --no-verbose

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Artem Egorenkov <aegorenk@redhat.com> - 1.20.3-6
- Fix Perl module build dependencies

* Wed Jun 24 2020 Artem Egorenkov <aegorenk@redhat.com> - 1.20.3-5
- Fix FTP VERIFCERTERR handling (#1475861)

* Tue Feb 25 2020 Tomas Hozza <thozza@redhat.com> - 1.20.3-4
- Fix FTBFS with new gcc (#1800250)

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr 05 2019 Tomas Hozza <thozza@redhat.com> - 1.20.3-1
- Update to 1.20.3
- Fix CVE-2019-5953

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 02 2019 Tomas Hozza <thozza@redhat.com> - 1.20.1-1
- Update to 1.20.1
- Fix CVE-2018-20483

* Thu Dec 06 2018 Tomas Hozza <thozza@redhat.com> - 1.20-1
- Update to 1.20
- --secure-protocol=TLSv1_3 now works (#1623994)

* Thu Aug 29 2018 Tomas Hozza <thozza@redhat.com> - 1.19.5-5
- Avoid creating empty wget-log when using -O and -q in background (#1484411)

* Tue Aug 28 2018 Tomas Korbar <tkorbar@redhat.com> - 1.19.5-4
- Add zlib-devel to buildrequires (#1612891)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Tomas Hozza <thozza@redhat.com> - 1.19.5-2
- Don't install info files in scriptlets

* Wed May 09 2018 Tomas Hozza <thozza@redhat.com> - 1.19.5-1
- Update to 1.19.5 fixing CVE-2018-0494

* Thu Apr 26 2018 Tomas Hozza <thozza@redhat.com> - 1.19.4-3
- Added gcc as an explicit BuildRequires

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Tomas Hozza <thozza@redhat.com> - 1.19.4-1
- Update to the latest upstream version
- Fix issue with decompressing with broken web servers (#1532233)

* Fri Dec 08 2017 Tomas Hozza <thozza@redhat.com> - 1.19.2-2
- Fix segfault when calling strchr in http.c (#1511562)

* Fri Oct 27 2017 Tomas Hozza <thozza@redhat.com> - 1.19.2-1
- Update to latest upstream version due to CVE-2017-13089 CVE-2017-13090

* Mon Oct 09 2017 Troy Dawson <tdawson@redhat.com> - 1.19.1-6
- Fix FTBFS (#1499876)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 31 2017 Tomas Hozza <thozza@redhat.com> - 1.19.1-3
- Fixed use of .netrc (#1425097)

* Fri May 12 2017 Tomas Hozza <thozza@redhat.com> - 1.19.1-2
- Fix CVE-2017-6508 (#1429986)

* Thu Feb 16 2017 Tomas Hozza <thozza@redhat.com> - 1.19.1-1
- New upstream version 1.19.1 (#1421398)

* Fri Feb 10 2017 Tomas Hozza <thozza@redhat.com> - 1.19-1
- New upstream version 1.19 (#1419013)
- Use libidn2 instead of libidn (new upstream default)

* Tue Jul 26 2016 Tomas Hozza <thozza@redhat.com> - 1.18-2
- Switched openssl to gnutls for crypto

* Tue Jun 14 2016 Tomas Hozza <thozza@redhat.com> - 1.18-1
- Update to 1.18

* Wed May 18 2016 Filip Čáp <cap.filip.dev@gmail.com> - 1.17.1-4
- Added metalink support (#1321334)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Adam Williamson <awilliam@redhat.com> - 1.17.1-2
- rebuild for new libpsl

* Mon Dec 14 2015 Tomas Hozza <thozza@redhat.com> - 1.17.1-1
- Update to 1.17.1

* Fri Nov 27 2015 Tomas Hozza <thozza@redhat.com> - 1.17-1
- Updated to 1.17 + added some additional upstream fixes
- Fixed hardening of wget executable (#1281829)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 10 2015 Tomas Hozza <thozza@redhat.com> - 1.16.3-1
- update to 1.16.3

* Wed Mar 04 2015 Tomas Hozza <thozza@redhat.com> - 1.16.2-1
- update to 1.16.2

* Mon Jan 12 2015 Tomas Hozza <thozza@redhat.com> - 1.16.1-3
- Fix wget to accept 5 digit port numbers in epsv responses over ipv6 (#1180777)

* Tue Dec 16 2014 Tomas Hozza <thozza@redhat.com> - 1.16.1-2
- build wget with libpsl support (#1123616)
- Fix NULL pointer dereference in FTP code (#1169022)

* Thu Dec 11 2014 Tomas Hozza <thozza@redhat.com> - 1.16.1-1
- update to 1.16.1

* Tue Nov 18 2014 Tomas Hozza <thozza@redhat.com> - 1.16-3
- Fix the progress bar issue (#1159643)

* Mon Nov 03 2014 Jakub Čajka <jcajka@redhat.com> - 1.16-2
- fix failing tests idn-cmd-utf8 and idn-robots-utf8
- re-enabled tests

* Fri Oct 31 2014 Tomas Hozza <thozza@redhat.com> - 1.16-1
- update to 1.16
- fixes CVE-2014-4877

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 22 2014 Tomas Hozza <thozza@redhat.com> - 1.15-1
- Update to 1.15
- Drop merged patches

* Mon Oct 21 2013 Tomas Hozza <thozza@redhat.com> - 1.14-11
- run test suite during the build

* Thu Oct 10 2013 Tomas Hozza <thozza@redhat.com> - 1.14-10
- remove excessive line for '-nv' option in the manpage (#1017106)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Tomas Hozza <thozza@redhat.com> - 1.14-8
- Fix deadcode and possible use of NULL in vprintf (#913153)
- Add documentation for --regex-type and --preserve-permissions
- Fix --preserve-permissions to work as documented (and expected)
- Fix bug when authenticating using user:password@url syntax (#912358)
- Document and fix --backups option

* Wed Jul 10 2013 Tomas Hozza <thozza@redhat.com> - 1.14-7
- Fix double free of iri->orig_url (#981778)

* Mon Jun 24 2013 Tomas Hozza <thozza@redhat.com> - 1.14-6
- add missing options accept-regex and reject-regex to man page
- fix errors in texi2pod introduced in Perl-5.18

* Fri Feb 22 2013 Tomas Hozza <thozza@redhat.com> - 1.14-5
- Added BuildRequires: perl-podlators for pod2man
- Patched manpage to silent new Tex errors
- Resolves: (#914571) 

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Tomas Hozza <thozza@redhat.com> 1.14-3
- Added libuuid-devel to BuildRequires to use libuuid functions
  in "src/warc.c" functions (#865421)

* Wed Oct 10 2012 Tomas Hozza <thozza@redhat.com> 1.14-2
- Added libidn-devel to BuildRequires to support IDN domains (#680394)

* Thu Aug 09 2012 Karsten Hopp <karsten@redhat.com> 1.14-1
- Update to wget-1.14

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 29 2012 Karsten Hopp <karsten@redhat.com> 1.13.4-4
- fix timeout if http server doesn't answer to SSL handshake (#860727)

* Tue May 15 2012 Karsten Hopp <karsten@redhat.com> 1.13.4-3
- add virtual provides per https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Jon Ciesla <limburgher@gmail.com> - 1.13.4-1
- New upstream, BZ 730286.
- Modified path patch.
- subjectAltNames patch upstreamed.
- Specified openssl at config time.

* Thu Jun 23 2011 Volker Fröhlich <volker27@gmx.at> - 1.12-4
- Applied patch to accept subjectAltNames in X509 certificates (#674186)
- New URL (#658969)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 18 2009 Karsten Hopp <karsten@redhat.com> 1.12-2
- don't provide /usr/share/info/dir

* Tue Nov 17 2009 Karsten Hopp <karsten@redhat.com> 1.12-1
- update to wget-1.12
- fixes CVE-2009-3490 wget: incorrect verification of SSL certificate
  with NUL in name

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.11.4-5
- rebuilt with new openssl

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> 1.11.4-2
- rebuild with new openssl

* Wed Aug 13 2008 Karsten Hopp <karsten@redhat.com> 1.11.4-1
- update

* Wed Jun 04 2008 Karsten Hopp <karsten@redhat.com> 1.11.3-1
- wget-1.11.3, downgrades the combination of the -N and -O options
  to a warning instead of an error

* Fri May 09 2008 Karsten Hopp <karsten@redhat.com> 1.11.2-1
- wget-1.11.2, fixes #179962

* Mon Mar 31 2008 Karsten Hopp <karsten@redhat.com> 1.11.1-1
- update to bugfix release 1.11.1, fixes p.e. #433606

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.11-2
- Autorebuild for GCC 4.3

* Tue Dec 04 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-17
- rebuild to pick up new openssl SONAME

* Mon Aug 27 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-16
- fix license tag
- rebuild

* Mon Feb 12 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-15
- fix discarding of expired cookies
- escape non-printable characters
- drop to11 patch for now (#223754, #227853, #227498)

* Mon Feb 05 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-14
- shut up rpmlint, even though xx isn't a macro

* Mon Feb 05 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-13
- merge review changes (#226538)
  - use version/release/... in buildroot tag
  - remove BR perl
  - use SMP flags
  - use make install instead of %%makeinstall
  - include copy of license
  - use Requires(post)/Requires(preun)
  - use optflags
  - remove trailing dot from summary
  - change tabs to spaces

* Thu Jan 18 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-12
- don't abort (un)install scriptlets when _excludedocs is set (Ville Skyttä)

* Wed Jan 10 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-11
- add fix for CVE-2006-6719

* Fri Dec 08 2006 Karsten Hopp <karsten@redhat.com> 1.10.2-10
- fix repeated downloads (Tomas Heinrich, #186195)

* Thu Dec 07 2006 Karsten Hopp <karsten@redhat.com> 1.10.2-9
- add distflag, rebuild

* Thu Dec 07 2006 Karsten Hopp <karsten@redhat.com> 1.10.2-8
- Resolves: #218211
  fix double free corruption

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.10.2-7
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Karsten Hopp <karsten@redhat.de> 1.10.2-6
- fix resumed downloads (#205723)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.10.2-5.1
- rebuild

* Thu Jun 29 2006 Karsten Hopp <karsten@redhat.de> 1.10.2-5
- updated german translations from Robert Scheck

* Tue Jun 27 2006 Karsten Hopp <karsten@redhat.de> 1.10.2-4
- upstream patches

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.10.2-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.10.2-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 1.10.2-3
- rebuilt against new openssl

* Tue Oct 25 2005 Karsten Hopp <karsten@redhat.de> 1.10.2-2
- use %%{_sysconfdir} (#171555)

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- 1.10.2

* Thu Sep 08 2005 Karsten Hopp <karsten@redhat.de> 1.10.1-7
- fix builtin help of --load-cookies / --save-cookies (#165408)

* Wed Sep 07 2005 Karsten Hopp <karsten@redhat.de> 1.10.1-6
- convert changelog to UTF-8 (#159585)

* Mon Sep 05 2005 Karsten Hopp <karsten@redhat.de> 1.10.1-5
- update
- drop patches which are already in the upstream sources

* Wed Jul 13 2005 Karsten Hopp <karsten@redhat.de> 1.10-5
- update german translation

* Mon Jul 11 2005 Karsten Hopp <karsten@redhat.de> 1.10-4
- update german translation (Robert Scheck)

* Tue Jul 05 2005 Karsten Hopp <karsten@redhat.de> 1.10-3
- fix minor documentation bug
- fix --no-cookies crash

* Mon Jul 04 2005 Karsten Hopp <karsten@redhat.de> 1.10-2
- update to wget-1.10
  - drop passive-ftp patch, already in 1.10
  - drop CVS patch
  - drop LFS patch, similar fix in 1.10
  - drop protdir patch, similar fix in 1.10
  - drop actime patch, already in 1.10

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-22
- build with gcc-4

* Wed Feb 02 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-21 
- remove old copy of the manpage (#146875, #135597)
- fix garbage in manpage (#117519)

* Tue Feb 01 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-20 
- texi2pod doesn't handle texinfo xref's. rewrite some lines so that
  the man page doesn't have incomplete sentences anymore (#140470)

* Mon Jan 31 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-19 
- Don't set actime to access time of the remote file or tmpwatch might 
  remove the file again (#146440).  Set it to the current time instead.
  timestamping checks only modtime, so this should be ok.

* Thu Jan 20 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-18
- add support for --protocol-directories option as documented
  in the man page (Ville Skyttä, #145571)

* Wed Sep 29 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-17 
- additional LFS patch from Leonid Petrov to fix file lengths in 
  http downloads

* Thu Sep 16 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-16 
- more fixes

* Tue Sep 14 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-15 
- added strtol fix from Leonid Petrov, reenable LFS

* Tue Sep 14 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-14
- buildrequires gettext (#132519)

* Wed Sep 01 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-13
- disable LFS patch for now, it breaks normal downloads (123524#c15)

* Tue Aug 31 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-12 
- move largefile stuff inside the configure script, it didn't
  get appended to CFLAGS

* Tue Aug 31 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-11
- rebuild

* Tue Aug 31 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-10 
- fix patch

* Sun Aug 29 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-9
- more cleanups of the manpage (#117519)

* Fri Aug 27 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-8
- rebuild

* Fri Aug 27 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-7 
- clean up manpage (#117519)
- buildrequire texinfo (#123780)
- LFS patch, based on wget-LFS-20040630.patch from Leonid Petrov
  (#123524, #124628, #115348)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Mar 11 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-3 
- fix documentation (#117517)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Nov 28 2003 Karsten Hopp <karsten@redhat.de> 1.9.1-3
- update to -stable CVS
- document the passive ftp default

* Fri Nov 28 2003 Karsten Hopp <karsten@redhat.de> 1.9.1-2
- add patch from -stable CVS

* Fri Nov 28 2003 Karsten Hopp <karsten@redhat.de> 1.9.1-1
- update to 1.9.1
- remove obsolete patches

* Mon Aug 04 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-15.3
- fix variable usage

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 1.8.2-15.2
- rebuild

* Wed Jun 25 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-15.1
- rebuilt

* Wed Jun 25 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-15
- default to passive-ftp (#97996)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-13
- rebuild

* Wed Jun 04 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-12
- merge debian patch for long URLs
- cleanup filename patch

* Sun May 11 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-11
- rebuild

* Sun May 11 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-10
- upstream fix off-by-one error

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 1.8.2-8
- rebuild

* Fri Dec 13 2002 Nalin Dahyabhai <nalin@redhat.com>
- use openssl pkg-config data, if present
- don't bomb out when building with newer openssl

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 1.8.2-7
- rebuild on all arches

* Tue Nov 19 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Fri Oct 4 2002 Karsten Hopp <karsten@redhat.de> 1.8.2-5
- fix directory traversal bug

* Wed Jul 24 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.8.2-3
- Don't segfault when downloading URLs A-B-A (A-A-B worked) #49859

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.8.2 (bug-fix release)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- remove s390 patch, not needed anymore

* Wed Feb 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.8.1-4
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add hack to not link against libmd5, even if available

* Fri Dec 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.8.1

* Thu Dec 13 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.8
- also include md5global to get it compile

* Sun Nov 18 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.7.1

* Wed Sep  5 2001 Phil Knirsch <phil@redhat.de> 1.7-3
- Added va_args patch required for S390.

* Mon Sep  3 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.7-2
- Configure with ssl support (duh - #53116)
- s/Copyright/License/

* Wed Jun  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.7
- Require perl for building (to get man pages)
- Don't include the Japanese po file, it's now included
- Use %%{_tmppath}
- no patches necessary
- Make /etc/wgetrc noreplace
- More docs

* Tue Jan 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Norwegian isn't a iso-8859-2 locale, neither is Danish.
  This fixes #15025.
- langify

* Sat Jan  6 2001 Bill Nottingham <notting@redhat.com>
- escape %%xx characters before fnmatch (#23475, patch from alane@geeksrus.net)

* Fri Jan  5 2001 Bill Nottingham <notting@redhat.com>
- update to 1.6, fix patches accordingly (#23412)
- fix symlink patch (#23411)

* Mon Dec 18 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese and Korean Resources

* Tue Aug  1 2000 Bill Nottingham <notting@redhat.com>
- setlocale for LC_CTYPE too, or else all the translations think their
  characters are unprintable.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 11 2000 Bill Nottingham <notting@redhat.com>
- build in new environment

* Mon Jun  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHS compliance

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Thu Aug 26 1999 Jeff Johnson <jbj@redhat.com>
- don't permit chmod 777 on symlinks (#4725).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0 tree
- add Provides

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries
- version 1.5.3

* Sat Jun 27 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.5.2

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- modified group to Applications/Networking

* Wed Apr 22 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.5.0
- they removed the man page from the distribution (Duh!) and I added it back
  from 1.4.5. Hey, removing the man page is DUMB!

* Fri Nov 14 1997 Cristian Gafton <gafton@redhat.com>
- first build against glibc
