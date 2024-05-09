Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           paps
Version:        0.6.8
Release:        46%{?dist}

License:        LGPLv2+
URL:            https://paps.sourceforge.net/
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        paps.convs
Source2:	29-paps.conf
BuildRequires:  pango-devel automake autoconf libtool doxygen cups-devel
## https://sourceforge.net/tracker/index.php?func=detail&aid=1832897&group_id=153049&atid=786241
Patch0:         paps-0.6.8-shared.patch
## https://sourceforge.net/tracker/index.php?func=detail&aid=1832924&group_id=153049&atid=786241
Patch1:         paps-0.6.8-wordwrap.patch
## https://sourceforge.net/tracker/index.php?func=detail&aid=1832926&group_id=153049&atid=786241
Patch2:         paps-langinfo.patch
## https://sourceforge.net/tracker/index.php?func=detail&aid=1832929&group_id=153049&atid=786241
Patch3:         paps-0.6.6-lcnumeric.patch
## https://sourceforge.net/tracker/index.php?func=detail&aid=1832935&group_id=153049&atid=786241
Patch4:         paps-exitcode.patch
## rhbz#854897
Patch5:         paps-854897-manpage.patch
## Fedora specific patch to integrate with CUPS
Patch50:        paps-cups.patch
Patch51:        paps-cpilpi.patch
## rhbz#424951
Patch52:        paps-dsc-compliant.patch
Patch53:        paps-autoconf262.patch
## rhbz#524883
Patch54:        paps-fix-cpi.patch
## rhbz#618483
Patch55:        paps-fix-loop-in-split.patch
## rhbz#857592
Patch56:        paps-fix-tab-width.patch
Patch57:        paps-fix-non-weak-symbol.patch
Patch58:        paps-correct-fsf-address.patch
## rhbz#1078519
Patch59:        %{name}-ft-header.patch
## rhbz#1196997
Patch60:        %{name}-a3.patch
## rhbz#1214939
Patch61:	%{name}-fix-paper-size-truncate.patch

Summary:        Plain Text to PostScript converter
Requires:       %{name}-libs = %{version}-%{release}
Requires:       cups-filesystem fontpackages-filesystem
%description
paps is a PostScript converter from plain text file using Pango.

%package libs
Summary:        Libraries for paps
%description libs
paps is a PostScript converter from plain text file using Pango.

This package contains the library for paps.

%package devel
Summary:        Development files for paps
Requires:       %{name}-libs = %{version}-%{release}
%description devel
paps is a PostScript converter from plain text file using Pango.

This package contains the development files that is necessary to develop
applications using paps API.

%prep
%setup -q
%patch 0 -p1 -b .shared
%patch 1 -p1 -b .wordwrap
%patch 2 -p1 -b .langinfo
%patch 3 -p1 -b .lcnumeric
%patch 4 -p1 -b .exitcode
%patch 5 -p1 -b .manpage
%patch 50 -p1 -b .cups
%patch 51 -p1 -b .cpilpi
%patch 52 -p1 -b .dsc
%patch 53 -p1 -b .autoconf262
%patch 54 -p1 -b .fixcpi
%patch 55 -p1 -b .loop
%patch 56 -p1 -b .tab
%patch 57 -p1 -b .weak-symbol
%patch 58 -p1 -b .fsf
%patch 59 -p1 -b .ft-header
%patch 60 -p1 -b .a3
%patch 61 -p1 -b .paper-size
libtoolize -f -c
autoreconf -f -i


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="/usr/bin/install -p"

# remove unnecessary files
rm $RPM_BUILD_ROOT%{_libdir}/libpaps.la

# make a symlink for CUPS filter
install -d $RPM_BUILD_ROOT%{_cups_serverbin}/filter # Not libdir
ln -s %{_bindir}/paps $RPM_BUILD_ROOT%{_cups_serverbin}/filter/texttopaps

install -d $RPM_BUILD_ROOT%{_datadir}/cups/mime
install -p -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/cups/mime/

install -d $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
install -p -m0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d/


%ldconfig_scriptlets libs

%files
%doc AUTHORS COPYING.LIB README TODO
%{_bindir}/paps
%{_mandir}/man1/paps.1*
%{_cups_serverbin}/filter/texttopaps
%{_datadir}/cups/mime/paps.convs
%{_sysconfdir}/fonts/conf.d/29-paps.conf

%files libs
%doc COPYING.LIB
%{_libdir}/libpaps.so.*

%files devel
%doc COPYING.LIB
%{_includedir}/libpaps.h
%{_libdir}/libpaps.so

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.8-46
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 0.6.8-40
- Rebuilt for switch to libxcrypt

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.8-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Akira TAGOH <tagoh@redhat.com> - 0.6.8-34
- Fix wrong paper size due to the integer cast.

* Mon Mar  2 2015 Akira TAGOH <tagoh@redhat.com> - 0.6.8-33
- Support A3 paper size.

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.6.8-32
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Oct 31 2014 Akira TAGOH <tagoh@redhat.com> - 0.6.8-31
- Add a fontconfig config to force the scalable font.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Akira TAGOH <tagoh@redhat.com> - 0.6.8-28
- Fix FTBFS against freetype's header files location change. (#1078519)

* Mon Dec 16 2013 Akira TAGOH <tagoh@redhat.com> - 0.6.8-27
- Move the place of paps.convs to %%{_datadir}/cups/mime. (#1042984)

* Wed Jul 31 2013 Akira TAGOH <tagoh@redhat.com> - 0.6.8-26
- Fix the width calculation with CPI enabled. (#990228)

* Thu Apr 18 2013 Akira TAGOH <tagoh@redhat.com> - 0.6.8-25
- Rebuilt for aarch64 support. (#926309)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Akira TAGOH <tagoh@redhat.com> - 0.6.8-23
- the spec file cleanup
- Fix the undefined symbol issue in libpaps.so.0
- Correct FSF address in the COPYING.LIB

* Mon Sep 24 2012 Akira TAGOH <tagoh@redhat.com> - 0.6.8-22
- Ensure the latest version of paps-libs are installed.

* Fri Sep 21 2012 Akira TAGOH <tagoh@redhat.com> - 0.6.8-21
- Fix wrong width for whitespaces when enabling CPI feature. (#857592)

* Thu Sep  6 2012 Akira TAGOH <tagoh@redhat.com> - 0.6.8-20
- Add a missing description of --encoding in manpage. (#854897)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 11 2012 Akira TAGOH <tagoh@redhat.com> - 0.6.8-18
- Use %%{_cups_serverbin} instead of the hardcoded path. (#772240)

* Mon Dec  5 2011 Akira TAGOH <tagoh@redhat.com> - 0.6.8-17
- Add ldconfig in %%post/%%postun for paps-libs (#759880)

* Fri Jun 24 2011 Akira TAGOH <tagoh@redhat.com> - 0.6.8-16
- Fix FTBFS issue. (#716211)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 27 2010 Akira TAGOH <tagoh@redhat.com> - 0.6.8-14
- Fix the infinite loop in splitting paragraphs (#618483)

* Fri Mar 12 2010 Akira TAGOH <tagoh@redhat.com> - 0.6.8-13
- Fix the directory's group ownership. (#572733)

* Tue Dec  8 2009 Akira TAGOH <tagoh@redhat.com> - 0.6.8-12
- Add paps.convs to behaves the cups filter without the hardcoded thing
  in cups. (#545031)

* Wed Oct 14 2009 Akira TAGOH <tagoh@redhat.com> - 0.6.8-11
- Fix code that deal with CPI parameter to be accurate. (#524883)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 17 2008 Akira TAGOH <tagoh@redhat.com> - 0.6.8-8
- Courier font to be a default font for texttopaps. (#469325)

* Mon Sep  1 2008 Akira TAGOH <tagoh@redhat.com> - 0.6.8-7
- paps-langinfo.patch: Updated.
- paps-exitcode.patch: Updated.

* Fri May 16 2008 Akira TAGOH <tagoh@redhat.com> - 0.6.8-6
- paps-cups.patch: Fix printing with -o landscape in CUPS. (#222137)
- paps-autoconf262.patch: Fix an error on autoreconf.

* Tue Feb 12 2008 Akira TAGOH <tagoh@redhat.com> - 0.6.8-5
- Rebuild for gcc-4.3.

* Wed Jan 23 2008 Akira TAGOH <tagoh@redhat.com> - 0.6.8-4
- Fix an exception on ghostscript. (#429275)

* Tue Jan 15 2008 Akira TAGOH <tagoh@redhat.com> - 0.6.8-3
- Put %%%%Pages: after %%%%Trailer. (#424951)

* Thu Jan 10 2008 Akira TAGOH <tagoh@redhat.com> - 0.6.8-2
- paps-0.6.8-dsc-compliant.patch: Patch out to be DSC compliant. (#424951)

* Fri Nov 30 2007 Akira TAGOH <tagoh@redhat.com> - 0.6.8-1
- New upstream release.
  - Remove patches merged and unnecessary anymore:
    - paps-makefile.patch
    - paps-formfeed.patch
    - paps-0.6.6-encoding.patch
    - paps-typo-font-scale.patch
    - paps-0.6.6-segfault.patch
    - paps-0.6.6-font-option.patch
    - paps-0.6.6-lcctype.patch
- paps-0.6.8-shared.patch: Enable building shared library.
- paps-0.6.8-wordwrap.patch: Update a bit to get it working without an wordwrap
  mode.
- Add paps-libs and paps-devel package.
- paps-cups.patch: Update.
- paps-cpilpi.patch: Update.
- Fix the wrong rendering with CPI option. (#237202)
- Fix the unnecessary rotation with the landscape option when paps is running
  as CUPS filter. (#222137)

* Thu Aug 23 2007 Akira TAGOH <tagoh@redhat.com> - 0.6.6-21
- Rebuild

* Fri Aug 10 2007 Akira TAGOH <tagoh@redhat.com>
- Update License tag.

* Wed May 30 2007 Akira TAGOH <tagoh@redhat.com> - 0.6.6-20
- Fix to not do wordwrap when 'wrap=false' is given. (#240588)

* Tue Mar 27 2007 Akira TAGOH <tagoh@redhat.com> - 0.6.6-19
- Fix PostScript breakage following the non-monetary numeric format from
  current locale. (#231916)

* Wed Mar  7 2007 Akira TAGOH <tagoh@redhat.com> - 0.6.6-18
- default to lpi=6 and cpi=10 if paps is bringing up as cups filter. (#223862)

* Tue Jan 23 2007 Akira TAGOH <tagoh@redhat.com>
- Better the encoding guess by looking at current locale. (#212154)

* Mon Dec  4 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-17
- Fix a segfault on non-printable character. (#216296)

* Sat Sep 30 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-16
- paps-0.6.6-exitcode.patch: exit immediately with proper exit code
  when unrecoverable error occurs. (#208592)

* Fri Sep 29 2006 Tim Waugh <twaugh@redhat.com> - 0.6.6-15
- Avoid using iconv when not needed (bug #206259).

* Thu Sep 14 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-14
- paps-cups.patch: try to parse input even if any invalid character appears.
  (#206259)

* Thu Aug 31 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-13
- paps-formfeed.patch: fixed to not insert an extra line in next page.
  (#202731)

* Thu Aug 17 2006 Tim Waugh <twaugh@redhat.com> - 0.6.6-12
- Map CUPS charset names to real ones (bug #197577).

* Mon Jul 17 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-11
- add an owner info to PS.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.6.6-10.2
- rebuild

* Tue Jul  4 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-10
- paps-0.6.6-cpilpi.patch: add --cpi and --lpi option to support the characters
  per inch and the lines per inch.
- paps-cups.patch: add cpi and lpi support.

* Thu Jun 29 2006 Tim Waugh <twaugh@redhat.com> - 0.6.6-9
- Fixed font-option patch.
- Adjusted CUPS patch: CUPS invokes the filter with the destination
  printer name in argv[0], not the binary name.
- CUPS filter lives in CUPS_SERVERBIN, which is /usr/lib/cups on all
  architectures -- not %%{_libdir}/cups.

* Thu Jun 29 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-8
- use dist tag.
- paps-cups.patch: applied to work paps as CUPS filter.
- paps-0.6.6-encoding.patch: null-terminates the output.

* Tue Jun 27 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-7
- rebuilt to import into Core.

* Wed Jun 21 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-6
- paps-0.6.6-wordwrap.patch: applied to do a wordwrap.

* Tue Jun 20 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-5
- paps-typo-font-scale.patch: backported from CVS.
- paps-0.6.6-font-option.patch: integrated --font-family and --font-scale
  options to --font.
- paps-0.6.6-lcctype.patch: follow LC_CTYPE to determine the default language.

* Fri Jun 16 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-4
- added libtool and doxygen to BuildReq.
- removed NEWS file which is empty.

* Mon Jun 12 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-3
- use make install DESTDIR=... instead of %%makeinstall
- add automake and autoconf to BuildReq.

* Thu May 25 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-2
- paps-0.6.6-encoding.patch: support --encoding option to be able to convert
  the input file to UTF-8.
- paps-0.6.6-segfault.patch: fixed a possible segfault issue when reading is
  failed.

* Fri May 19 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.6-1
- New upstream release.

* Mon Apr 17 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.5-1
- New upstream release.
  - paps-0.6.3-fix-pagesize.patch: removed. it has been merged in upstream.
  - paps-0.6.3-goption.patch: removed. it has been merged in upstream.
  - paps-0.6.3-header.patch: removed. it has been merged in upstream.
- paps-makefile.patch: rework to be applied.

* Fri Mar 31 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.3-4
- paps-0.6.3-formfeed.patch: applied to deal with the formfeed mark properly.
- paps-0.6.3-goption.patch: rewritten option parser using GOption. and segfault
  gone as well. (#187205)
- paps-0.6.3-header.patch: applied to support the output of the page header.

* Fri Mar 24 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.3-3
- paps-0.6.3-fix-pagesize.patch: fixed displaying the beginning of line at out of page. (#176207)

* Thu Mar  2 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.3-2
- rebuilt.

* Wed Jan 11 2006 Akira TAGOH <tagoh@redhat.com> - 0.6.3-1
- New upstream release.
- paps-0.6.2-fix-bufferoverflow.patch: removed.

* Wed Dec 21 2005 Akira TAGOH <tagoh@redhat.com> - 0.6.2-1
- New upstream release.
  - the bitmap font is now ignored. (#176206)
- paps-0.6.2-fix-bufferoverflow.patch: applied to fix the buffer overflow.

* Tue Dec 13 2005 Akira TAGOH <tagoh@redhat.com> - 0.6.1-1
- New upstream release.
- paps-0.6.1-makefile.patch: applied to install docs on the proper dir.

* Fri Nov  4 2005 Akira TAGOH <tagoh@redhat.com> - 0.5-1
- New upstream release.

* Tue Oct 18 2005 Akira TAGOH <tagoh@redhat.com> - 0.3-1
- Initial package.

