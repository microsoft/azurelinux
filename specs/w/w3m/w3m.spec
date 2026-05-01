# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# These are the build option passed to ./configure command
%global build_options  --enable-m17n --enable-unicode --enable-nls --with-editor=/bin/vi --with-mailer="gnome-open mailto:%s" --with-browser=gnome-open --with-charset=UTF-8 --with-gc --with-termlib=ncurses --enable-nntp --enable-gopher --enable-image=x11,fb --with-imagelib=gtk2 --enable-keymap=w3m

%global gitdate 20230121

%{?perl_default_filter}
%global __requires_exclude perl\\(w3mhelp-

Name:     w3m
Version:  0.5.3
Release:  66.git%{gitdate}%{?dist}
# Unicode-DFS-2015 is added for EastAsianWidth.txt source
License:  MIT AND Unicode-DFS-2015
URL:      http://w3m.sourceforge.net/
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  perl-generators
BuildRequires:  pkgconfig
BuildRequires:  gettext-devel
%ifnarch s390 s390x
BuildRequires:  gpm-devel
%endif
BuildRequires:  gc-devel
BuildRequires:  nkf
BuildRequires:  lynx
BuildRequires:  gcc-c++
BuildRequires:  make

# This is needed for perl files
Requires: perl(NKF)

Source0: https://github.com/tats/%{name}/archive/v%{version}+git%{gitdate}/%{name}-%{version}+git%{gitdate}.tar.gz
Source1: w3mconfig

Patch0: https://github.com/tats/w3m/pull/273/commits/edc602651c506aeeb60544b55534dd1722a340d3.patch#/w3m-0.5.3-fix-oob-access.patch

Summary:  Pager with Web browsing abilities
Provides: webclient
Provides: text-www-browser

%description
The w3m program is a pager (or text file viewer) that can also be used
as a text-mode Web browser. W3m features include the following: when
reading an HTML document, you can follow links and view images using
an external image viewer; its internet message mode determines the
type of document from the header; if the Content-Type field of the
document is text/html, the document is displayed as an HTML document;
you can change a URL description like 'http://hogege.net' in plain
text into a link to that URL.
If you want to display the inline images on w3m, you need to install
w3m-img package as well.

%package img
Summary: Helper program to display the inline images for w3m
BuildRequires:  gtk2-devel
BuildRequires:  gdk-pixbuf2-xlib-devel
Requires: ImageMagick
Requires: %{name}%{?_isa} = %{version}-%{release}

%description img
w3m-img package provides a helper program for w3m to display the inline
images on the terminal emulator in X Window System environments and the
linux framebuffer.

%prep
%autosetup -n %{name}-%{version}-git%{gitdate} -p1

%build
export CFLAGS="$CFLAGS -std=gnu17"
%configure %{build_options}
%make_build

%install
%make_install

install -D -p -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/w3m/config

rm -f doc*/w3m.1

%find_lang w3m

%files -f w3m.lang
%doc doc NEWS README ChangeLog
%lang(ja) %doc doc-jp
%lang(de) %doc doc-de
%{_datadir}/w3m/
%config(noreplace) %{_sysconfdir}/w3m/
%{_bindir}/w3m*
%lang(ja) %{_mandir}/ja/man1/w3m.1*
%lang(de) %{_mandir}/de/man1/w3m.1*
%lang(de) %{_mandir}/de/man1/w3mman.1*
%{_mandir}/man1/w3m.1*
%{_mandir}/man1/w3mman.1*
%{_libexecdir}/w3m/
%exclude %{_libexecdir}/w3m/w3mimgdisplay

%files img
%{_libexecdir}/w3m/w3mimgdisplay

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-66.git20230121
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-65.git20230121
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-64.git20230121
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Mar 18 2024 Robert Scheck <robert@fedoraproject.org> - 0.5.3-63.git20230121
- Added upstream patch to fix out-of-bounds access due to multiple backspaces
  to address incomplete fix for CVE-2022-38223 (#2222775, #2222780, #2255207)

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-62.git20230121
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-61.git20230121
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jan 22 2023 Robert Scheck <robert@fedoraproject.org> - 0.5.3-60.git20230121
- Rebase to latest upstream gitrev 20230121 (#2163003)

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-59.git20220429
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 23 2022 Robert Scheck <robert@fedoraproject.org> - 0.5.3-58.git20220429
- Added upstream patch to address CVE-2022-38223 (#2126270)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-57.git20220429
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.5.3-56.git20220429
- Perl 5.36 rebuild

* Sun May 01 2022 Robert Scheck <robert@fedoraproject.org> - 0.5.3-55.git20220429
- Rebase to latest upstream gitrev 20220429 (#2080136)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-54.git20210102
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 0.5.3-53.git20210102
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-52.git20210102
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.5.3-51.git20210102
- Perl 5.34 rebuild

* Wed Mar 03 2021 Robert Scheck <robert@fedoraproject.org> - 0.5.3-50.git20210102
- Rebase to latest upstream gitrev 20210102

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-49.git20200502
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Oct 06 2020 Robert Scheck <robert@fedoraproject.org> - 0.5.3-48.git20200502
- Rebase to latest upstream gitrev 20200502

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-47.git20190105
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.5.3-46.git20190105
- Perl 5.32 rebuild

* Sat Mar 14 2020 Robert Scheck <robert@fedoraproject.org> - 0.5.3-45.git20190105
- Rebase to latest upstream gitrev 20190105

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-44.git20180125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-43.git20180125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.5.3-42.git20180125
- Perl 5.30 rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-41.git20180125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-40.git20180125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.5.3-39.git20180125
- Perl 5.28 rebuild

* Mon Feb 19 2018 Parag Nemade <pnemade AT redhat DOT com> - 0.5.3-38.git20180125
- Add BuildRequires: gcc-c++ as per packaging guidelines

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-37.git20180125
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Parag <pnemade AT redhat DOT com> - 0.5.3-36.git20180125
- Rebase to latest upstream gitrev 20180125

* Tue Jan 16 2018 Karsten Hopp <karsten@redhat.com> - 0.5.3-35.git20170102
- fix some conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-34.git20170102
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-33.git20170102
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.5.3-32.git20170102
- Perl 5.26 rebuild

* Mon Apr 03 2017 Parag <pnemade AT redhat DOT com> - 0.5.3-31.git20170102
- Add conditional for epel build (Resolves:rh#1437730 - can't access https sites)

* Sun Mar 05 2017 Parag <pnemade AT redhat DOT com> - 0.5.3-30.git20170102
- Add conditional for epel7 build

* Thu Mar 02 2017 Parag <pnemade AT redhat DOT com> - 0.5.3-29.git20170102
- Update to latest upstream gitrev 20170102

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-28.git20161120
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Dec 04 2016 Parag <pnemade AT redhat DOT com> - 0.5.3-27.git20161120
- Rebase to latest upstream gitrev 20161120
- All existing patches was already upstream so removed it

* Mon Nov 21 2016 Parag <pnemade AT redhat DOT com> - 0.5.3-26
- Rebuild against compat-openssl10-devel

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.5.3-25
- Perl 5.24 rebuild

* Mon Apr 11 2016 Parag <pnemade AT redhat DOT com> - 0.5.3-24
- Resolves:rh#1324349 - denial of service with crafted html files
- patch from debian bug 820162

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.5.3-21
- Perl 5.22 rebuild

* Fri Mar 20 2015 Richard Hughes <richard@hughsie.com> - 0.5.3-20
- Rebuilt for gdk-pixbuf2-xlib split

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.5.3-19
- Perl 5.20 rebuild

* Tue Aug 26 2014 Parag <pnemade AT redhat DOT com> - 0.5.3-18
- Resolves:rh#1133668 - Fix broken deps for perl requires

* Wed Aug 20 2014 Parag <pnemade AT redhat DOT com> - 0.5.3-17
- Don't need external dependency generator now

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 04 2013 Parag <pnemade AT redhat DOT com> - 0.5.3-14
- Fix build with -Werror=format-security (rh#1037380)
- Fix another FTBFS due to above flag (rh#1038009)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.5.3-12
- Perl 5.18 rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 03 2013 Parag <pnemade AT redhat DOT com> - 0.5.3-10
- Resolves:rh#885590 - w3mhelp-funcdesc.ja.pl contains broken Japanese
- Fix the parallel make support patch

* Thu Dec 27 2012 Parag <pnemade AT redhat DOT com> - 0.5.3-9
- Add patch for parallel make support

* Tue Dec 11 2012 Parag <pnemade AT redhat DOT com> - 0.5.3-8
- Resolves:rh#885940 - suggestions for further improvements
- Drop w3m-0.4.1-helpcharset.patch as default encoding works fine
- Drop w3m-0.5.1-gcc4.patch as compilation works fine without it

* Fri Dec 07 2012 Parag <pnemade AT redhat DOT com> - 0.5.3-7
- Resolves:rh#885091 - update license tag to include UCD also

* Wed Nov 21 2012 Parag <pnemade AT redhat DOT com> - 0.5.3-6
- Resolves:rh#878803 - some spec cleanups

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.5.3-3
- Rebuild for new libpng

* Mon Sep 05 2011 Parag <pnemade AT redhat DOT com> - 0.5.3-2
- Resolves: rh#707994-[abrt] openSocket: Process /usr/bin/w3m was killed by signal 11 (SIGSEGV) 

* Mon Aug 08 2011 Parag <pnemade AT redhat DOT com> - 0.5.3-1
- update to 0.5.3 upstream release 

* Mon Jun 27 2011 Parag <pnemade AT redhat DOT com> - 0.5.2-21
- Resolves:rh#716155-FTBFS w3m-0.5.2-20.fc15

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 28 2010 Parag <pnemade AT redhat.com> - 0.5.1-19
- Resolves:rh#638026 - Man w3m is stating incorrect program version

* Thu Jun 17 2010 Parag <pnemade AT redhat.com> - 0.5.2-18
- Resolves:rh#604864-CVE-2010-2074 w3m: doesn't handle NULL in Common Name properly 

* Wed Feb 17 2010 Parag <pnemade AT redhat.com> - 0.5.2-17
- Resolves:rh#566101-FTBFS w3m-0.5.2-16.fc13: ImplicitDSOLinking 

* Tue Feb 16 2010 Parag <pnemade AT redhat.com> - 0.5.2-16
- Resolves:rh#555467-FTBFS

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.5.2-15
- rebuilt with new openssl

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 0.5.2-12
- rebuild with new openssl

* Fri Jul 18 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.2-11
- Add BR: lynx which provides "text-www-browser" virtual Provides
  to avoid BR dependency loop between gtk2-devel and w3m (shorter name wins
  the game with yum)
  Proposed by drago01 <drago01@gmail.com> rh#455734

* Wed Apr 23 2008 Parag <pnemade@redhat.com> - 0.5.2-10
- Rebuilt for new rpm package
- Resolves:rh#443115: needs rebuild

* Fri Apr 18 2008 Parag <pnemade@redhat.com> - 0.5.2-9
- Re-enable BR:gtk2-devel 
- Resolves:rh#442950: Images aren't displayed in any type of terminal

* Mon Feb 11 2008 Parag <pnemade@redhat.com> - 0.5.2-8
- Rebuild for gcc 4.3

* Tue Dec 04 2007 Jesse Keating <jkeating@redhat.com> - 0.5.2-7
- Temporarily disable gtk to bootstrap build for openssl

* Tue Dec 04 2007 Parag Nemade <pnemade@redhat.com> - 0.5.2-6
- build against new openssl

* Fri Oct 12 2007 Parag Nemade <pnemade@redhat.com> - 0.5.2-5
- Added Provides: text-www-browser as part of rh#174566

* Wed Aug 22 2007 Parag Nemade <pnemade@redhat.com> - 0.5.2-4
- rebuild against new rpm package

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 0.5.2-3
- rebuild for toolchain bug

* Tue Jul 24 2007 Parag Nemade <pnemade@redhat.com> - 0.5.2-2
- Build against new gc-7.0 release.

* Tue Jun 26 2007 Parag Nemade <pnemade@redhat.com> - 0.5.2-1
- Update to 0.5.2 and remove merged patches.
- Build against system gc library.
- Add BR: nkf for multipart.cgi.
- Don't call unneeded autotool

* Tue Mar 27 2007 Parag Nemade <pnemade@redhat.com> - 0.5.1-19
- and more cleanup.

* Tue Mar 27 2007 Parag Nemade <pnemade@redhat.com> - 0.5.1-18.2
- more cleanup.

* Mon Mar 26 2007 Parag Nemade <pnemade@redhat.com> - 0.5.1-18
- spec file cleanup.

* Mon Feb 26 2007 Parag Nemade <pnemade@redhat.com> - 0.5.1-17
- Resolves #229799

* Wed Feb 21 2007 Parag Nemade <pnemade@redhat.com> - 0.5.1-16
- Modified SPEC file to add new patchfile to resolve rh#222914.

* Fri Feb 02 2007 Parag Nemade <pnemade@redhat.com> - 0.5.1-15.1
- Resolves: rh#226535 Review Merge 
- Modified SPEC file.

* Mon Jan 15 2007 Parag Nemade <pnemade@redhat.com> - 0.5.1-15
- Resolves: rh#221484

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.5.1-14.1
- rebuild

* Sat Jun 24 2006 Jesse Keating <jkeating@redhat.com> - 0.5.1-14
- Fix missing br gettext-devel, automake

* Mon Mar  6 2006 Akira TAGOH <tagoh@redhat.com> - 0.5.1-13
- w3m-multilib.patch: fixed to link 64bit version of libnsl.so. (#182408)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.5.1-12.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.5.1-12.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Akira TAGOH <tagoh@redhat.com> 0.5.1-12
- rebuilt against the latest openssl.
- gc6.2-fix-prelink.patch: removed.
- w3m-fix-vi-prec-num.patch: applied to get the vi-like prefix working.

* Tue May 10 2005 Joe Orton <jorton@redhat.com> 0.5.1-11
- point at certs directory in /etc/pki

* Mon Apr 18 2005 Akira TAGOH <tagoh@redhat.com> - 0.5.1-10
- fixed the unnecessary owned directory. (#154600)

* Thu Apr  7 2005 Akira TAGOH <tagoh@redhat.com> - 0.5.1-9
- removed imlib-devel build-dependency. (#153773)

* Mon Mar 28 2005 Akira TAGOH <tagoh@redhat.com> - 0.5.1-8
- w3m-cvs-20050328.patch: updated to CVS snapshot to support gtk2.

* Thu Mar 17 2005 Akira TAGOH <tagoh@redhat.com> - 0.5.1-7
- rebuilt
- w3m-0.5.1-gcc4.patch: applied to fix the build fails with gcc4.
  (#151136: Robert Scheck)

* Thu Jan 13 2005 Akira TAGOH <tagoh@redhat.com> - 0.5.1-6
- fixed a duplicated w3mimgdisplay.

* Mon Dec 20 2004 Akira TAGOH <tagoh@redhat.com> - 0.5.1-5
- updates to gc6.3. (#143361)
  - w3m-0.3.1-fixptr_t.patch: removed. it's no longer needed.
- fixed the permission to get working of the helper scripts.

* Thu Aug 05 2004 Akira TAGOH <tagoh@redhat.com> 0.5.1-4
- rebuilt

* Wed Aug 04 2004 Akira TAGOH <tagoh@redhat.com> 0.5.1-3
- converted Japanese man page to UTF-8. (#129028)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 06 2004 Akira TAGOH <tagoh@redhat.com> 0.5.1-1
- New upstream release.

* Tue Apr 20 2004 Akira TAGOH <tagoh@redhat.com> 0.5-3
- build with --with-termlib=ncurses to fix segfault. (#120240)

* Mon Apr 12 2004 Akira TAGOH <tagoh@redhat.com> 0.5-2
- separated w3mimgdisplay to w3m-img package. (#120600)
- removed indexhtml, which is no longer refered.

* Tue Mar 23 2004 Akira TAGOH <tagoh@redhat.com> 0.5-1
- New upstream release.
- w3m-0.2.3.1-ipv6.patch: removed.
- w3m-0.4.1-stable-m17n-20030308.patch.gz: removed, because it has been marged to the upstream.
- w3mconfig: updated.
- w3mbookmark: removed, use one, which the upstream disbributed.
- w3mhelperpanel: likewise.
- libwc-latest.tar.gz: likewise.
- w3m-wrapper: removed.
- w3m-0.5-guess_display_locale.patch: updated.
- w3m-0.5-staic-libgc.patch: applied to build static library of libgc.
- w3m-0.3.2-lib64path.patch: removed.

* Tue Mar 09 2004 Akira TAGOH <tagoh@redhat.com> 0.4.1-12
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 10 2004 Akira TAGOH <tagoh@redhat.com> 0.4.1-10
- gc6.2alpha5-ppc64.patch: removed because no need to apply.
- gc6.2.tar.gz: update to the stable version.
- gc6.2-fix-prelink.patch: applied to fix prelink issue. (#115201: Jakub Jelinek)

* Mon Dec 15 2003 Akira TAGOH <tagoh@redhat.com> 0.4.1-9
- w3m-0.4.1-guess_display_locale.patch: applied to guess the display encoding
  from the current locale. (#111217)

* Wed Oct 01 2003 Akira TAGOH <tagoh@redhat.com> 0.4.1-8
- converted Japanese manpage to UTF-8.

* Tue Jun 17 2003 Akira TAGOH <tagoh@redhat.com> 0.4.1-7
- rebuild.

* Thu Jun 12 2003 Akira TAGOH <tagoh@redhat.com> 0.4.1-6
- applied m17n patch to allow UTF-8 encoding.
- specify the charset for w3m-help.cgi.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 21 2003 Akira TAGOH <tagoh@redhat.com> 0.4.1-4
- rebuild
- use gc6.2alpha5.
- gc6.2alpha5-ppc64.patch: applied to fix the build issue on ppc64.

* Wed May 21 2003 Akira TAGOH <tagoh@redhat.com> 0.4.1-3
- rebuild.

* Thu May 1 2003 Elliot Lee <sopwith@redhat.com> 0.4.1-2
- Genericize multilib
- _smp_mflags

* Mon Mar 17 2003 Akira TAGOH <tagoh@redhat.com> 0.4.1-1
- New upstream release.
- w3m-0.3.2.2-fixhttpssegv.patch: removed.
- w3m-0.3.2-fix64arch.patch: removed.

* Mon Feb  3 2003 Akira TAGOH <tagoh@redhat.com> 0.3.2.2-5
- w3m-0.3.2.2-fixhttpssegv.patch: applied to fix a segfault with https. (#83263)
- gc6.2alpha3.tar.gz: use it to be built on s390x.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 0.3.2.2-3
- rebuild

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- buildreq openssl-devel instead of openssl
- use openssl's pkg-config configuration if it exists
- pass cflags and ldflags in to configure instead of letting them get pulled
  in from the environment

* Tue Dec 24 2002 Akira TAGOH <tagoh@redhat.com> 0.3.2.2-2
- add indexhtml to BuildRequires.
- fix the wrong path to the local CGI.
- don't use rpms internal dep generator.
- w3m-wrapper: go through the options.

* Fri Dec  6 2002 Akira TAGOH <tagoh@redhat.com> 0.3.2.2-1
- New upstream release.
- this release contains yet another security fix.

* Wed Nov 27 2002 Akira TAGOH <tagoh@redhat.com> 0.3.2.1-1
- New upstream release.

* Mon Nov 11 2002 Akira TAGOH <tagoh@redhat.com> 0.3.2-1
- New upstream release.
- removed some packages, because this release contains it.
  - w3m-0.3.1-fixanchor.patch
  - w3m-0.3.1-multipartimg.patch
  - w3m-0.3.1-fixwarning-03276.patch
- w3mimgsize is obsolete.
- gc6.1.tar.gz: update to the latest gc library.
- w3m-0.3.2-fix64arch.patch: applied to fix the build issue for ia64 and x86_64.
- w3m-0.3.2-lib64path.patch: applied to add lib64 path for x86_64.

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- rebuild for new imlib soname

* Mon Jul 22 2002 Akira TAGOH <tagoh@redhat.com> 0.3.1-3
- use 'display' to show the image when nothing is described in mailcap.
- w3m-0.3.1-fixanchor.patch: applied to fix an anchor issue on plain text.
- w3m-0.3.1-multipartimg.patch: applied to fix a rendering issue on multipart.
- w3m-0.3.1-fixwarning-03276.patch: applied to fix a warning message at buld
  time.

* Thu Jul 18 2002 Akira TAGOH <tagoh@redhat.com> 0.3.1-2
- add the owned directory.

* Tue Jul 16 2002 Akira TAGOH <tagoh@redhat.com> 0.3.1-1
- New upstream release.
- w3m-0.3.1-fixprivsym.patch: disabled. it works without this patch.
- w3m-0.3.1-fixptr_t.patch: applied to fix the build issue for alpha.
- gc6.1alpha2.tar.bz2: use an old version to avoid the build issue for IA64.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 18 2002 Akira TAGOH <tagoh@redhat.com> 0.3-4
- fix the missing files. (Bug#66865)

* Thu May 30 2002 Chip Turner <cturner@redhat.com>
- add dependency filter for bogus perl dependencies

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Mar  6 2002 Akira TAGOH <tagoh@redhat.com> 0.3-1
- New upstream release.
- w3m-0.3-config.param-{en,ja}: update.
- w3m-0.3-fixprivsym.patch: Fixed unresolved dependencies. (Bug#60725)
  Thanks Jakub.
- fix the missing files.

* Fri Feb 22 2002 Akira TAGOH <tagoh@redhat.com> 0.2.5.1-2
- Build against new environment.

* Tue Feb  5 2002 Akira TAGOH <tagoh@redhat.com> 0.2.5.1-1
- New upstream release.

* Fri Feb  1 2002 Akira TAGOH <tagoh@redhat.com> 0.2.5-1
- New upstream release.
- Update build config files for 0.2.5
- Update default config.

* Wed Jan  9 2002 Akira TAGOH <tagoh@redhat.com> 0.2.4-2
- Fixed use a wrong build config for en. (Bug#58093)
- Update build config files for 0.2.4
- Added cert path to default config.

* Tue Jan  8 2002 Akira TAGOH <tagoh@redhat.com> 0.2.4-1
- New upstream release.
- Remove old GC library from srpm because no longer need it.

* Thu Dec 27 2001 Akira TAGOH <tagoh@redhat.com> 0.2.3.2-2
- Fixed the wrong default settings.

* Tue Dec 25 2001 Akira TAGOH <tagoh@redhat.com> 0.2.3.2-1
- New upstream release.

* Fri Dec 21 2001 Akira TAGOH <tagoh@redhat.com> 0.2.3.1-1
- New upstream release.

* Wed Dec  5 2001 Akira TAGOH <tagoh@redhat.com> 0.2.2-2
- Added config file for alpha from James Antill.

* Mon Nov 19 2001 Akira TAGOH <tagoh@redhat.com> 0.2.2-1
- New upstream release.

* Wed Aug 29 2001 SATO Satoru <ssato@redhat.com> - 0.2.1-11
- made the relative link to HTML_HOME instead of the absolute one
- fixed the permission of sources (to shut up rpmlint)

* Wed Aug 29 2001 SATO Satoru <ssato@redhat.com> - 0.2.1-10
- fixed the wrapper script (#52759)

* Thu Aug  9 2001 SATO Satoru <ssato@redhat.com> - 0.2.1-9
- corrected the help files' path (#51197)
- removed /etc/profile.d/*
- fixed and update the wrapper
- removed imlib-devel (BuildRequires:)

* Sat Aug  4 2001 SATO Satoru <ssato@redhat.com> - 0.2.1-8
- disabled the inline image rendering patch by default (#50786)

* Tue Jul 24 2001 SATO Satoru <ssato@redhat.com>
- s/Copyright/License/
- %%files: add '/etc/profile.d/w3m.*'
- enable IPv6 support by default (#35649)

* Fri Jul 20 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- do not require gpm for s390,s390x

* Tue Jul 17 2001 SATO Satoru <ssato@redhat.com>
- apply inline image support patch.
- BuildRequires: imlib-devel
- add %%dir lines

* Thu Jun 28 2001 Than Ngo <than@redhat.com>
- fix to build on s390x s390
- fix to use RPM_OPT_FLAGS

* Mon Jun 25 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- disable mouse/gpm on s390 s390x

* Thu Jun 21 2001 Yukihiro Nakai <ynakai@redhat.com>
- Add ia64 support.

* Wed Jun 20 2001 SATO Satoru <ssato@redhat.com>
- 0.2.1
- clean up SPEC
- apply security bug fix
- w3m-el is removed (moved into w3m-el package)

* Fri Mar  2 2001 Tim Powers <timp@redhat.com>
- rebuilt against openssl-0.9.6-1

* Fri Feb  9 2001 SATO Satoru <ssato@redhat.com>
- not to use upstream configure script (it looks corrupted)
- separated w3m-ja/w3m-en (#26443)
- apply many security bug fix patch
- ExludeArch alpha
- use bzip2 instead of gzip for src/patches

* Thu Feb  8 2001 SATO Satoru <ssato@redhat.com>
- changed configure option ( --lang=ja -> --lang=en)

* Thu Jan 18 2001 Tim Powers <timp@redhat.com>
- ExludeArch ia64

* Sun Jan 14 2001 SATO Satoru <ssato@redhat.com>
- fix the error while building on IA64

* Fri Jan 12 2001 SATO Satoru <ssato@redhat.com>
- fix the error while building on Sparc
- clean up SPEC

* Thu Dec 28 2000 SATO Satoru <ssato@redhat.com>
- new upstream pre release
- added w3m.el
- clean up SPEC

* Wed Sep  6 2000 Satoru Sato <ssato@redhat.com>
- ported from vine
- remove w3m.wmconfig
- build with openssl library

* Sun Jul 09 2000 Lisa Sagami <czs14350@nifty.ne.jp>
- w3m-0.1.10-0vl3
- provide default HTTP_HOME in /etc/profile.d

* Fri Jul 07 2000 Lisa Sagami <czs14350@nifty.ne.jp>
- Provides: webclient, Requires: indexhtml (capability of lynx)
- added w3m.wmconfig
- give them(who?) RPM_OPT_FLAGS(what?)
- dont include duplicated man pages and CVS directory in doc

* Wed Jun 21 2000 Jun Nishii <jun@vinelinux.org>
- 0.1.10-0vl1

* Sat Jan 22 2000 Yoichi Imai <yoichi@silver-forest.com>
- fix spec file

* Sat Jan 22 2000 Yoichi Imai <yoichi@silver-forest.com>
- updated from 0.1.4 to 0.1.6

* Thu Jan 13 2000 Yoichi Imai <yoichi@silver-forest.com>
- updated from 991203 to 0.1.4

* Fri Dec 03 1999 Yoichi Imai <yoichi@silver-forest.com>
- updated from 991028 to 991203

* Sat Oct 30 1999 Yoichi Imai <bonaim@mutt.freemail.ne.jp>
- updated from 990820 to 991028

* Thu Aug 26 1999 Ryo Hattori <ryoh@vs01.vaio.ne.jp>
- updated from 990716 to 990820

* Wed Aug 11 1999 Ryo Hattori <ryoh@vs01.vaio.ne.jp>
- initial Release to VinePlus
