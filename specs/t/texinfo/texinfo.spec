# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global tex_texinfo %{_datadir}/texlive/texmf-dist/tex/texinfo

Summary: Tools needed to create Texinfo format documentation files
Name: texinfo
Version: 7.2
Release: 8%{?dist}
License: GPL-3.0-or-later
Url: http://www.gnu.org/software/texinfo/
Source0: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz
Source1: ftp://ftp.gnu.org/gnu/texinfo/texinfo-%{version}.tar.xz.sig
Source2: fix-info-dir
# Patch0: we need to fix template fix-info-dir generates
Patch0: info-6.5-sync-fix-info-dir.patch
# Patch1: rhbz#1592433, bug in fix-info-dir --delete
Patch1: texinfo-6.5-fix-info-dir.patch
# Patch3: fixes issues detected by static analysis
Patch3: texinfo-7.1-various-sast-fixes.patch
# Patch4: fixes issues detected by static analysis
Patch4: texinfo-7.1-make-tainted-data-safe.patch
# Patch5: fixes Perl precedence warnings (already upstream)
Patch5: texinfo-7.2-fix-perl-precedence-warnings.patch

BuildRequires: make
BuildRequires: gcc
BuildRequires: perl-generators
BuildRequires: ncurses-devel, help2man, perl(Data::Dumper)
BuildRequires: perl(Locale::Messages), perl(Unicode::EastAsianWidth), perl(Text::Unidecode)
BuildRequires: perl(Storable), perl(Unicode::Normalize), perl(File::Copy)

# Texinfo perl packages are not installed in default perl library dirs
%global __provides_exclude ^perl\\(.*Texinfo.*\\)$
%global __requires_exclude ^perl\\(.*Texinfo.*\\)$

%description
Texinfo is a documentation system that can produce both online
information and printed output from a single source file. The GNU
Project uses the Texinfo file format for most of its documentation.

Install texinfo if you want a documentation system for producing both
online and print documentation from the same source file and/or if you
are going to write documentation for the GNU Project.

%package -n info
Summary: A stand-alone TTY-based reader for GNU texinfo documentation
Provides: /sbin/install-info

%description -n info
The GNU project uses the texinfo file format for much of its
documentation. The info package provides a standalone TTY-based
browser program for viewing texinfo files.

%package tex
Summary: Tools for formatting Texinfo documentation files using TeX
Requires: texinfo = %{version}-%{release}
Requires: tex(tex) tex(epsf.tex)
Requires: /usr/bin/cmp
Requires: /usr/bin/diff
Requires(post): %{_bindir}/texconfig-sys
Requires(postun): %{_bindir}/texconfig-sys
Provides: tex-texinfo
Provides: texlive-texinfo
Obsoletes: texlive-texinfo <= 9:2019-15

%description tex
Texinfo is a documentation system that can produce both online
information and printed output from a single source file. The GNU
Project uses the Texinfo file format for most of its documentation.

The texinfo-tex package provides tools to format Texinfo documents
for printing using TeX.

%prep
%setup -q
mkdir contrib
install -Dpm0755 -t contrib %{SOURCE2}
%autopatch -p1

%build
%configure --with-external-Text-Unidecode \
           --with-external-libintl-perl \
           --with-external-Unicode-EastAsianWidth \
           --disable-perl-xs
%make_build

%install
%make_install

mkdir -p %{buildroot}%{tex_texinfo}
install -p -m644 doc/texinfo.tex doc/txi-??.tex %{buildroot}%{tex_texinfo}

install -Dpm0755 -t %{buildroot}%{_sbindir} contrib/fix-info-dir

%find_lang %{name}
%find_lang %{name}_document

%check
export ALL_TESTS=yes
%make_build check

%post tex
%{_bindir}/texconfig-sys rehash 2> /dev/null || :

%postun tex
%{_bindir}/texconfig-sys rehash 2> /dev/null || :

%transfiletriggerin -n info -- %{_infodir}
[ -f %{_infodir}/dir ] && create_arg="" || create_arg="--create"
%{_sbindir}/fix-info-dir $create_arg %{_infodir}/dir &>/dev/null || :

%transfiletriggerpostun -n info -- %{_infodir}
[ -f %{_infodir}/dir ] && %{_sbindir}/fix-info-dir --delete %{_infodir}/dir &>/dev/null || :

%files -f %{name}.lang -f %{name}_document.lang
%doc AUTHORS ChangeLog NEWS README TODO
%license COPYING
%{_bindir}/makeinfo
%{_bindir}/texi2any
%{_bindir}/pod2texi
%{_datadir}/texinfo
%{_datadir}/texi2any
%{_infodir}/texinfo*
%{_infodir}/texi2any_api.info*
%{_infodir}/texi2any_internals.info*
%{_mandir}/man1/makeinfo.1*
%{_mandir}/man5/texinfo.5*
%{_mandir}/man1/texi2any.1*
%{_mandir}/man1/pod2texi.1*

%files -n info
%license COPYING
%{_bindir}/info
%{_infodir}/info-stnd.info*
%{_sbindir}/install-info
%{_sbindir}/fix-info-dir
%{_mandir}/man1/info.1*
%{_mandir}/man1/install-info.1*
%{_mandir}/man5/info.5*
%ghost %{_infodir}/dir
%ghost %attr(644, root, root) %{_infodir}/dir.old

%files tex
%{_bindir}/texindex
%{_bindir}/texi2dvi
%{_bindir}/texi2pdf
%{_bindir}/pdftexi2dvi
%{tex_texinfo}/
%{_mandir}/man1/texindex.1*
%{_mandir}/man1/texi2dvi.1*
%{_mandir}/man1/texi2pdf.1*
%{_mandir}/man1/pdftexi2dvi.1*

%changelog
* Thu Feb 12 2026 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.2-7
- Use || : so scriptlets do not fail when devfs is unavailable
  Resolves: #2422085

* Fri Aug 01 2025 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.2-6
- Fix FTBFS (Perl precedence warnings)
  Resolves: #2385687

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 25 2025 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.2-4
- Fix texi2dvi missing dependencies
  Resolves: #2374602

* Tue Jan 21 2025 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.2-3
- Changes related to bin and sbin unify

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.2-1
- Update to texinfo-7.2
  Resolves: #2333829

* Tue Oct 15 2024 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.1.1-2
- Another batch of fixes for issues detected by static analysis

* Mon Sep 09 2024 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.1.1-1
- Update to texinfo-7.1.1
  Resolves: #2310652

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 24 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.1-1
- Update to texinfo-7.1
  Resolves: #2244846

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 31 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.0.3-2
- SPDX migration

* Thu Mar 30 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.0.3-1
- Update to texinfo-7.0.3
  Resolves: #2181837

* Wed Feb 22 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.0.2-2
- Fix possible use of an undefined value as an ARRAY reference in ParserNonXS.pm
  (causes FTBFS of a2ps)
  Resolves: #2171433

* Mon Jan 23 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.0.2-1
- Update to texinfo-7.0.2
  Resolves: #2162979

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 01 2022 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.0.1-1
- Update to texinfo-7.0.1
  Resolves: #2149772

* Fri Nov 18 2022 Vitezslav Crhonek <vcrhonek@redhat.com> - 7.0-1
- Update to texinfo-7.0
  Resolves: #2140872

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.8-1
- Update to texinfo-6.8
  Resolves: #1978903

* Mon Jun 14 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.7-11
- Fix install path of install-info

* Tue Feb 02 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.7-10
- Fix problem in shell code found by ShellCheck in test script

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 16 2020 Jitka Plesnikova <jplesnik@redhat.com> - 6.7-7
- Add BR: perl(Unicode::Normalize)

* Thu Mar  5 2020 Tom Callaway <spot@fedoraproject.org> - 6.7-6
- add additional Provides: tex-texinfo ("it's an older code sir, but it checks out")

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.7-4
- Move texlive-tex files to more approriate location again, this
  time in sync with dropping texlive-texinfo from texlive
  Resolves: #1719379

* Thu Jan 09 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.7-3
- Fix mode of dir.old

* Tue Oct 08 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.7-2
- Revert move of texinfo-tex files
  Resolves: #1758817

* Thu Sep 26 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.7-1
- Update to texinfo-6.7
  Resolves: #1754648
- Move texlive-tex files to more approriate location
  Resolves: #1719379

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 18 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.6-1
- Update to texinfo-6.6
  Resolves: #1677911

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 04 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 6.5-11
- Fix another issue in fix-info-dir which could lead to an infinite loop in odd
  circumstances.
  Resolves: #1614162

* Thu Aug 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6.5-10
- Drop macros.info

* Wed Aug 08 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.5-9
- Fix issues detected by static analysis

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 6.5-7
- Perl 5.28 rebuild

* Thu Jun 21 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.5-6
- Fix fail of test because of unescaped left brace with Perl 5.28
  (patch by Jitka Plesnikova)
  Resolves: #1590308

* Tue Jun 19 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 6.5-5
- Fix bug in fix-info-dir which prevented the transfiletriggerpostun script
  from working properly.

* Fri Mar 30 2018 Tom Callaway <spot@fedoraproject.org> - 6.5-4
- update texinfo.tex

* Tue Feb 13 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 6.5-3
- Implement transaction filetriggers for crating info/dir

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Sep 13 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.5-1
- Update to texinfo-6.5
  Resolves: #1491075

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 6.4-3
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Mon Jul 10 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.4-2
- Fix broken reference following when the reference is split to
  more than one line
- Fix possible incorrect selection of already loaded file when
  following cross reference
  Resolves: #1383057

* Tue Jun 27 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.4-1
- Update to texinfo-6.4
  Resolves: #1464624

* Mon Mar 13 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.3-3
- Fix path to install-info in macros.info
  Resolves: #1419246

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 19 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.3-1
- Update to texinfo-6.3
  Resolves: #1374962

* Wed Jun 22 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.1-3
- install-info: use create-tmp-then-rename pattern because of OSTree
  (patch by Colin Walters)
  Resolves: #1348671

* Wed Feb 24 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.1-2
- Fix texi2dvi exits without completing the task
  Resolves: #1309702

* Thu Feb 11 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.1-1
- Update to texinfo-6.1
  Resolves: #1305316

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Aug 9 2015 Orion Poplawski <orion@cora.nwra.com> - 6.0-2
- Add BR on perl(Storable), fix perl requires (bug #1251766)

* Tue Jul 14 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 6.0-1
- Update to texinfo-6.0
  Resolves: #1236254

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 5.2-9
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Feb 02 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.2-8
- Add macros.info
  Resolves: #948735

* Thu Oct 30 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.2-7
- Filter bogus perl requires/provides
- Enable upstream test suite

* Tue Oct 14 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.2-6
- Use perl-Unicode-EastAsianWidth

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug  6 2014 Tom Callaway <spot@fedoraproject.org> - 5.2-4
- fix license handling

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 16 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.2-2
- Fix info segfaults on non existing info page when used with -o

* Tue Oct 01 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.2-1
- Update to texinfo-5.2

* Tue Aug 13 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.1-4
- Fix \b[...\b] tag processing
  Resolves: #928975

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 5.1-2
- Perl 5.18 rebuild

* Mon Mar 18 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.1-1
- Update to texinfo-5.1

* Tue Mar 05 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.0-3
- Fix bug in parser
  Resolves: #917974

* Wed Feb 20 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.0-2
- Fix configure arguments, remove ChangeLog conversion,
  move texi2any/pod2texi to main package

* Tue Feb 19 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.0-1
- Update to texinfo-5.0

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13a-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Jindrich Novy <jnovy@redhat.com> - 4.13a-19
- require epsf.tex (#868011)

* Mon Sep 10 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.13a-18
- Fix issues found by fedora-review utility in the spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13a-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13a-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13a-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.13a-14
- Fix missing Texinfo manual in the Directory node
  Resolves: #662382

* Wed Nov 10 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.13a-13
- Fix get_sectioning_number function problem
  Resolves: #651314

* Tue Nov  9 2010 Jindrich Novy <jnovy@redhat.com> - 4.13a-12
- require tex(tex) instead of tetex in texinfo-tex

* Mon Oct 11 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.13a-11
- Fix incopatible regexp with the lates version of egrep in texi2dvi script
  Resolves: #641534

* Tue Aug 31 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.13a-10
- Fix info crash when using index in help window
  Resolves: #579263

* Mon Jan 11 2010 Jan Gorig <jgorig@redhat.com> - 4.13a-9
- Fix PowerPC return code bug #531349

* Mon Dec 14 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.13a-8
- Fix memory allocation bug when using old-style --section "Foo" arguments

* Wed Sep  2 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.13a-7
- Fix errors installing texinfo/info with --excludedocs
  Resolves: #515909
  Resolves: #515938

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 4.13a-6
- Use lzma compressed upstream tarball.

* Wed Aug  5 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.13a-5
- Fix changelog entry and rebuild

* Tue Aug  4 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.13a-4
- Fix data types (fix by Ralf Corsepius)
  Resolves: #515402

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.13-1
- Update to texinfo-4.13a
  Resolves: #471194
  Resolves: #208511

* Wed Jun  4 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.12-4
- Remove sed Requires (dependency loop)
  Resolves: #449705

* Mon Jun  2 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.12-3
- Fix install-info crashes on some info files
  Resolves: #449292

* Thu May 29 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.12-2
- Fix Requires and info post script

* Wed May 14 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.12-1
- Update to texinfo-4.12
- Remove description ("This is...") from /usr/share/info/dir in info
  post install section
  Resolves: #433535

* Mon Feb  4 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.11-5
- Merge Review
  Resolves: #226488

* Mon Dec 10 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.11-4
- Don't insert description ("This is...") into the direntry section
  of some generated files
  Resolves: #394191

* Tue Nov 13 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.11-3
- Fix info crashes when resizing window
  Resolves: #243971

* Wed Nov  7 2007 Stepan Kasal <skasal@redhat.com> - 4.11-2
- fix a typo in texinfo-tex summary
  Resolves: #239216

* Wed Sep 19 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.11-1
- Rebase to upstream texinfo-4.11 (update zlib.patch, drop
  texindex.patch and 0xA0.patch -- both included in upstream)
  Resolves: #295441

* Tue Aug 28 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.9-2
- Fix license
- Rebuild

* Tue Jul 31 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 4.9-1
- Rebase to upstream texinfo-4.9, fix typo in summary
  Resolves: #250119, #248883

* Mon Dec  4 2006 Miloslav Trmac <mitr@redhat.com> - 4.8-15
- Don't replace 0xA0 by a space in makeinfo
  Related: #208511
- Fix some rpmlint warnings

* Sun Nov  5 2006 Miloslav Trmac <mitr@redhat.com> - 4.8-14
- Remove off-line sorting from texindex (fixes CVE 2006-4810)

* Mon Oct  9 2006 Miloslav Trmac <mitr@redhat.com> - 4.8-13
- Don't use mode 0666 for the texindex temporary files

* Mon Oct  9 2006 Miloslav Trmac <mitr@redhat.com> - 4.8-12
- Don't leave around temporary files used by texindex
- Add missing error handling to texinfo-CAN-2005-3011.patch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.8-11.1
- rebuild

* Sat Mar 25 2006 Miloslav Trmac <mitr@redhat.com> - 4.8-11
- Split texinfo-tex from the texinfo package (#178406)
- Ship COPYING, don't ship INSTALL

* Sun Mar 19 2006 Miloslav Trmac <mitr@redhat.com> - 4.8-10
- Remove incorrect Prefix:
- Drop info/README
- Convert change log to UTF-8

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.8-9.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.8-9.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 16 2006 Miloslav Trmac <mitr@redhat.com> - 4.8-9
- Fix handling of bzip2'ed files (#128637)

* Mon Jan 16 2006 Miloslav Trmac <mitr@redhat.com> - 4.8-8
- Ignore scriptlet failures with --excludedocs (#166958)
- Don't link texindex to zlib, don't pretend to link to zlib statically

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Oct 14 2005 Tim Waugh <twaugh@redhat.com> 4.8-7
- Apply patch to fix CAN-2005-3011 (bug #169585).

* Thu Jun  9 2005 Tim Waugh <twaugh@redhat.com> 4.8-6
- Ship texi2pdf man page, taken from tetex-2.0.2 RPM.

* Tue Jun  7 2005 Tim Waugh <twaugh@redhat.com> 4.8-5
- Ship texi2pdf (bug #147271).

* Mon Mar 14 2005 Tim Waugh <twaugh@redhat.com> 4.8-4
- Requires tetex (bug #151075).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 4.8-3
- Rebuild for new GCC.

* Mon Feb  7 2005 Tim Waugh <twaugh@redhat.com> 4.8-2
- Don't ship texi2pdf (bug #147271).

* Thu Feb  3 2005 Tim Waugh <twaugh@redhat.com> 4.8-1
- 4.8.

* Thu Dec 30 2004 Tim Waugh <twaugh@redhat.com> 4.7-6
- Fixed URL (bug #143729).

* Thu Aug 12 2004 Tim Waugh <twaugh@redhat.com> 4.7-5
- Rebuilt.

* Wed Jul  7 2004 Tim Waugh <twaugh@redhat.com> 4.7-4
- Build for FC2.

* Tue Jun 29 2004 Tim Waugh <twaugh@redhat.com> 4.7-3
- Fix grouping in user-defined macros.

* Mon Jun 28 2004 Tim Waugh <twaugh@redhat.com> 4.7-2
- Build requires ncurses-devel (bug #126600).

* Fri Jun 25 2004 Tim Waugh <twaugh@redhat.com> 4.7-1
- 4.7.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar  2 2004 Tim Waugh <twaugh@redhat.com>
- Fixed compiler warning (bug #117097).

* Sat Feb 21 2004 Tim Waugh <twaugh@redhat.com> 4.6-3
- Build requires zlib-devel (bug #116436).

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Dec  2 2003 Tim Waugh <twaugh@redhat.com> 4.6-1
- Fixed compiler warning (bug #111279).
- 4.6.

* Tue Jun 17 2003 Tim Waugh <twaugh@redhat.com> 4.5-3
- Rebuilt.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May  6 2003 Tim Waugh <twaugh@redhat.com>
- No longer need 3.12h-fix patch.

* Tue Apr 29 2003 Tim Waugh <twaugh@redhat.com> 4.5-1
- 4.5 (bug #88428).  Update zlib patch.
- Add URL tag (bug #54613).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 4.3-5
- rebuilt

* Tue Jan  7 2003 Tim Waugh <twaugh@redhat.com> 4.3-4
- Fix up spec_install_post to strip debug info out to separate package
  (bug #81226).

* Thu Dec 26 2002 Florian La Roche <Florian.LaRoche@redhat.de> 4.3-3
- Make /usr/share/info/dir a real file and remove /etc/info-dir, that
  file should be unused for a long time.

* Thu Nov 21 2002 Elliot Lee <sopwith@redhat.com> 4.3-2
- Don't strip files here (rpm takes care of it)
- Use pushd/popd instead of enclosing things in (), to make
  error detection easier
- Use _smp_mflags

* Tue Nov 19 2002 Tim Waugh <twaugh@redhat.com> 4.3-1
- 4.3.
- No longer need fileextension or malloccheck patches.
- Update zlib patch.

* Wed Oct 23 2002 Tim Waugh <twaugh@redhat.com> 4.2-6
- Don't install files not packaged.
- Fix file list (bug #55816).

* Mon Sep  2 2002 Bernhard Rosenkraenzer <bero@redhat.com> 4.2-5
- Fix crash w/ MALLOC_CHECK_ == 2 (#72831)

* Tue Jul  2 2002 Bernhard Rosenkraenzer <bero@redhat.com> 4.2-4
- Add infokey (#67728)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr 23 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- 4.2

* Tue Mar  5 2002 Bernhard Rosenkraenzer <bero@redhat.com> 4.1-1
- 4.1 (#60714)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Aug  7 2001 Bernhard Rosenkraenzer <bero@redhat.com> 4.0b-3
- Don't create the desktop file - we don't install it anyway.

* Sat Jul 21 2001 Tim Powers <timp@redhat.com>
- remove the info viewer from the menus, it's cluttering things

* Wed May 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- 4.0b

* Tue Apr 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 4.0a-1
- Update to 4.0a, the patch looks sane

* Fri Feb 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- langify
- don't create desktop file in spec file

* Tue Jan 23 2001 Preston Brown <pbrown@redhat.com>
- danish translation added

* Tue Dec 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild to get rid of 0777 dirs

* Wed Nov  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix recognition of .?o extensions in texi2dvi, Bug #20498

* Thu Sep  7 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging (64bit systems need to use %%_libdir not /usr/lib).

* Sat Aug 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- really do it - #16120

* Mon Aug 14 2000 Helge Deller <hdeller@redhat.com>
- gzip man-pages, #16120

* Mon Aug  7 2000 Tim Waugh <twaugh@redhat.com>
- List man-pages in %%files.

* Fri Aug  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add Swedish and German translations to desktop file, Bug #15366

* Thu Aug  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- mark /etc/info-dir %%verify(not md5 size mime), Bug #14826

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jun 28 2000 Bill Nottingham <notting@redhat.com>
- fix build wackiness with info page compressing

* Fri Jun 16 2000 Bill Nottingham <notting@redhat.com>
- fix info-dir symlink

* Thu May 18 2000 Preston Brown <pbrown@redhat.com>
- use FHS paths for info.

* Fri Mar 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with current ncurses

* Wed Feb 09 2000 Preston Brown <pbrown@redhat.com>
- wmconfig -> desktop

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix descriptions

* Wed Jan 26 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- move info-stnd.info* to the info package, /sbin/install-info it
  in %%post (Bug #6632)

* Thu Jan 13 2000 Jeff Johnson <jbj@redhat.com>
- recompile to eliminate ncurses foul-up.

* Tue Nov  9 1999 Bernhard Rosenkränzer <bero@redhat.com>
- 4.0
- handle RPM_OPT_FLAGS

* Tue Sep 07 1999 Cristian Gafton <gafton@redhat.com>
- import version 3.12h into 6.1 tree from HJLu

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Wed Mar 17 1999 Erik Troan <ewt@redhat.com>
- hacked to use zlib to get rid of the requirement on gzip

* Wed Mar 17 1999 Matt Wilson <msw@redhat.com>
- install-info prerequires gzip

* Thu Mar 11 1999 Cristian Gafton <gafton@redhat.com>
- version 3.12f
- make /usr/info/dir to be a %%config(noreplace)

* Wed Nov 25 1998 Jeff Johnson <jbj@redhat.com>
- rebuild to fix docdir perms.

* Thu Sep 24 1998 Cristian Gafton <gafton@redhat.com>
- fix allocation problems in install-info

* Wed Sep 23 1998 Jeff Johnson <jbj@redhat.com>
- /sbin/install-info should not depend on /usr/lib/libz.so.1 -- statically
  link with /usr/lib/libz.a.

* Fri Aug 07 1998 Erik Troan <ewt@redhat.com>
- added a prereq of bash to the info package -- see the comment for a
  description of why that was done

* Tue Jun 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Tue Jun  9 1998 Jeff Johnson <jbj@redhat.com>
- add %%attr to permit non-root build.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun Apr 12 1998 Cristian Gafton <gafton@redhat.com>
- added %%clean
- manhattan build

* Wed Mar 04 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to version 3.12
- added buildroot

* Sun Nov 09 1997 Donnie Barnes <djb@redhat.com>
- moved /usr/info/dir to /etc/info-dir and made /usr/info/dir a
  symlink to /etc/info-dir.

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- added wmconfig entry for info

* Wed Oct 01 1997 Donnie Barnes <djb@redhat.com>
- stripped /sbin/install-info

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- added info-dir to filelist

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- added patch from sopwith to let install-info understand gzip'ed info files
- use skeletal dir file from texinfo tarball (w/ bash entry to reduce
  dependency chain) instead (and install-info command everywhere else)
- patches install-info to handle .gz names correctly

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Feb 25 1997 Erik Troan <ewt@redhat.com>
- patched install-info.c for glibc.
- added /usr/bin/install-info to the filelist

* Tue Feb 18 1997 Michael Fulbright <msf@redhat.com>
- upgraded to version 3.9.
