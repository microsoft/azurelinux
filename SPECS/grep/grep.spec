# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Pattern matching utilities
Name: grep
Version: 3.12
Release: 2%{?dist}
License: GPL-3.0-or-later AND LGPL-3.0-or-later AND LGPL-2.1-or-later AND GPL-2.0-or-later AND LGPL-2.0-or-later AND GFDL-1.3-no-invariants-or-later
URL: https://www.gnu.org/software/grep/

Source0: https://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.xz
Source1: https://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz.sig
Source2: https://savannah.gnu.org/project/release-gpgkeys.php?group=grep&download=1'#/grep-keyring.gpg
Source3: colorgrep.sh
Source4: colorgrep.csh
Source5: GREP_COLORS
Source6: grepconf.sh

# upstream ticket 39445
Patch: grep-3.5-help-align.patch
# upstream ticket 77800
Patch: grep-3.12-test-write-error-msg-drop.patch

BuildRequires: gcc
BuildRequires: pcre2-devel
BuildRequires: texinfo
BuildRequires: gettext
BuildRequires: autoconf
BuildRequires: automake

# temporal for the gnulib patch
BuildRequires: gettext-devel

Buildrequires: glibc-all-langpacks
BuildRequires: perl(FileHandle)
BuildRequires: make
BuildRequires: gnupg2
# https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib)
# for backward compatibility (rhbz#1540485)
Provides: /bin/grep
Provides: /bin/fgrep
Provides: /bin/egrep

%description
The GNU versions of commonly used grep utilities. Grep searches through
textual input for lines which contain a match to a specified pattern and then
prints the matching lines. GNU's grep utilities include grep, egrep and fgrep.

GNU grep is needed by many scripts, so it shall be installed on every system.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
%global BUILD_FLAGS $RPM_OPT_FLAGS

# Currently gcc on ppc uses double-double arithmetic for long double and it
# does not conform to the IEEE floating-point standard. Thus force
# long double to be double and conformant.
%ifarch ppc ppc64
%global BUILD_FLAGS %{BUILD_FLAGS} -mlong-double-64
%endif

%configure --without-included-regex --disable-silent-rules CFLAGS="%{BUILD_FLAGS}"
%make_build

%install
%make_install
gzip $RPM_BUILD_ROOT%{_infodir}/grep*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}
install -Dpm 755 %{SOURCE6} $RPM_BUILD_ROOT%{_libexecdir}/grepconf.sh

%find_lang %name

%check
make check

%files -f %{name}.lang
%doc AUTHORS THANKS TODO NEWS README
%license COPYING

%{_bindir}/*
%config(noreplace) %{_sysconfdir}/profile.d/colorgrep.*sh
%config(noreplace) %{_sysconfdir}/GREP_COLORS
%{_infodir}/*.info*.gz
%{_mandir}/*/*
%{_libexecdir}/grepconf.sh

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Apr 14 2025 Jaroslav Škarvada <jskarvad@redhat.com> - 3.12-1
- New version
  Resolves: rhbz#2358901

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 29 2024 Lukáš Zaoral <lzaoral@redhat.com> - 3.11-8
- remove redundant dependency on libsigsegv (RHEL-34664)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 10 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 3.11-5
- Updated SPDX license expression

* Wed Aug  9 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 3.11-4
- Converted license to SPDX

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 3.11-2
- Fixed egrep/fgrep aliases
  Resolves: rhbz#2215713

* Tue Jun  6 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 3.11-1
- New version
  Resolves: rhbz#2181063

* Thu Mar 23 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 3.10-1
- New version
  Resolves: rhbz#2181063

* Tue Mar  7 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 3.9-1
- New version
  Resolves: rhbz#2175526
- Added sources verification

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan  3 2023 Florian Weimer <fweimer@redhat.com> - 3.8-2
- Fix C99 compatibility issue in the configure script

* Mon Sep  5 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 3.8-1
- New version
  Resolves: rhbz#2123935
- Switchd to pcre2
  Resolves: rhbz#1755491

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr  8 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 3.7-3
- Gate perl-FileHandle dependency to f33 onwards

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 16 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 3.7-1
- New version
  Resolves: rhbz#1993631
- Temporarily switch to the included regex until glibc bug (glibc#11053)
  is fixed

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6-3
- Fixed stack overflow detection

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov  9 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 3.6-1
- New version
  Resolves: rhbz#1895797

* Wed Sep 30 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 3.5-1
- New version
  Resolves: rhbz#1883086

* Wed Aug 26 2020 Adam Williamson <awilliam@redhat.com> - 3.4-5
- Backport fix for upstream #28105 to fix zgrep
  Resolves: rhbz#1872913
- Remove some non-portable tests that fail on armv7hl (Paul Eggert)
  Resolves: rhbz#1863830

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 3.4-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Apr  1 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 3.4-1
- New version
  Resolves: rhbz#1818417
- Added all glibc langpacks to allow more locale sensitive tests to run
- Added perl-FileHandle requirement for the filename-lineno.pl test

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 24 2019 Björn Esser <besser82@fedoraproject.org> - 3.3-2
- Remove hardcoded gzip suffix from GNU info pages

* Wed Apr 10 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 3.3-1
- New version
  Resolves: rhbz#1698044
- Updated patches
- Dropped glibc-2.28-fix patch (not needed)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug  9 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.1-8
- Fixed FTBFS with glibc-2.28
  Resolves: rhbz#1604263

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.1-6
- Dropped install-info

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb  2 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.1-4
- Moved binaries to /usr/bin
  Resolves: rhbz#1540485

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul  3 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 3.1-1
- New version
  Related: rhbz#1421129
- Updated patches

* Fri Feb 10 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0-1
- New version
  Resolves: rhbz#1421129

* Wed Feb  8 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2.28-1
- New version
  Resolves: rhbz#1419921
- De-fuzzified patches

* Wed Dec  7 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.27-1
- New version
  Resolves: rhbz#1402379
- De-fuzzified patches

* Wed Oct  5 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.26-2
- Re-enabled 'make check', glibc seems fixed

* Mon Oct  3 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.26-1
- New version
  Resolves: rhbz#1381203
- Disabled 'make check' due to glibc bug rhbz#1381582

* Fri Apr 22 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.25-1
- New version
  Resolves: rhbz#1329627
- De-fuzzified patches

* Fri Mar 11 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.24-1
- New version
  Resolves: rhbz#1316890

* Fri Feb  5 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.23-1
- New version
  Resolves: rhbz#1305035
- Dropped disable-performance-related-tests, better-encoding-errors-handling,
  Pc-consistent-results, and test-pcre-count-fix patches (all upstreamed)
- De-fuzzified man-fx-gs, and help-align patches

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.22-6
- Fixed pcre-count test on secondary architectures
  (byt test-pcre-count-fix patch)
  Resolves: rhbz#1296842

* Wed Jan  6 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.22-5
- Used latest upstream patch for bug 1269014 to fix regression,
  fixed order of patches
  Resolves: rhbz#1269014

* Tue Jan  5 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.22-4
- Improved encoding errors handling (by better-encoding-errors-handling patch)
  Resolves: rhbz#1219141
- kwset-abuse test no longer needs to be explicitly set executable

* Tue Dec  1 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.22-3
- Fixed grep to be consistent in 'grep -Pc' and 'grep -P | wc -l'
  Resolves: rhbz#1269014

* Thu Nov  5 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.22-2
- Disabled performance related tests
  (by disable-performance-related-tests patch), patch backported from upstream
- Dropped disable-long-pattern-perf-test patch (not needed, covered by
  previous patch)
  Resolves: rhbz#1278428

* Mon Nov  2 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.22-1
- New version
  Resolves: rhbz#1277113
- Dropped buf-overrun-fix, recurse-behaviour-change-doc, gnulib
  patches (all upstreamed)
- Minor spec cleanup to be consistent with whitespaces

* Sun Aug  2 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.21-7
- Minor spec cleanups and modifications
- Drop Changelog, details in NEWS
- Add gnulib patch to fix FTBFS with perl 5.22

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr  7 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.21-5
- Documented change in behaviour of recurse option
  Resolves: rhbz#1178305

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.21-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Jan 20 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.21-3
- Fixed buffer overrun for grep -F
  Resolves: rhbz#1183653

* Tue Dec  9 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.21-2
- Disable silent rules to make the build process more verbose

* Tue Nov 25 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.21-1
- New version
  Resolves: rhbz#1167657
- De-fuzzified patches
- Dropped pcre-backported-fixes patch (not needed)

* Fri Nov 14 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.20-7
- Backported more PCRE fixes (by pcre-backported-fixes patch)
- Dropped pcre-invalid-utf8-fix patch, handled by pcre-backported-fixes patch

* Tue Nov 11 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.20-6
- Fixed invalid UTF-8 byte sequence error in PCRE mode
  (by pcre-invalid-utf8-fix patch)
  Resolves: rhbz#1161832

* Wed Aug 20 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.20-5
- Added script to check whether grep is coloured
  Resolves: rhbz#1034631

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 2.20-3
- fix license handling .

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun  4 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.20-1
- New version
  Resolves: rhbz#1104508
- De-fuzzified patches

* Fri May 23 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.19-1
- New version
  Resolves: rhbz#1100653

* Wed Feb 26 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.18-1
- New version
  Resolves: rhbz#1070127
- De-fuzzified patches

* Tue Feb 18 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.17-1
- New version
  Resolves: rhbz#1066310
- De-fuzzified patches

* Thu Jan  2 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.16-1
- New version
  Resolves: rhbz#1047813
- De-fuzzified patches

* Tue Nov 26 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.15-2
- Removed coloring restriction for interactive shells
  Resolves: rhbz#1034631

* Tue Oct 29 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.15-1
- New version
  Resolves: rhbz#1023698
- Fixed bogus date in the changelog
- Dropped gnulib-tests-rm-f patch, rejected upstream and not
  needed for Fedora build system
- Dropped man-fix-R patch, upstreamed
- De-fuzzified other patches

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul  9 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.14-4
- Added group-separator, no-group-separator options decription
- Aligned output of built-in help
- Defuzzified gnulib-tests-rm-f patch

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct  3 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.14-2
- Fixed -R option placement
  Resolves: rhbz#861937

* Mon Aug 20 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.14-1
- New version
  Resolves: rhbz#849594

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.13-1
- New version
  Resolves: rhbz#837749
- Fixed -i option
  Resolves: rhbz#828844
- Added virtual provide and FPC ticket link for bundled gnulib
  Resolves: rhbz#821759

* Tue Apr 24 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.12-1
- New version
  Resolves: rhbz#815705

* Fri Mar  2 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.11-1
- New version

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.10-3
- Rebuild against PCRE 8.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.10-1
- New version

* Mon Jul 11 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9-3
- Use rm -f in gnulib-tests (gnulib-tests-rm-f patch)
  Resolves: rhbz#716330

* Mon Jul 04 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9-2
- Fixed build failure on ppc - long double forced to double on ppc

* Wed Jun 22 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9-1
- New version: grep-2.9
- Removed dfa-buffer-overrun-fix patch

* Mon Jun 20 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8-4
- dfa: don't overrun a malloc'd buffer for certain regexps
  (patch dfa-buffer-overrun-fix)
  Resolves: rhbz#713328

* Mon May 16 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8-3
- Added coloring aliases to csh script as well

* Mon May 16 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8-2
- Added coloring to egrep and fgrep
  Resolves: rhbz#697895

* Mon May 16 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8-1
- New version: grep-2.8
  Resolves: rhbz#704710
- Removed const-range-exp patch (upstreamed)

* Mon Apr 04 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7-5
- colorgrep scripts no longer overwrites COLORS envvar (#693058),
  thanks to Ville Skyttä

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 01 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7-3
- Fixed inconsistency with range expressions, const-range-exp patch (#583011)

* Wed Sep 29 2010 jkeating - 2.7-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7-1
- New version: grep-2.7
- Removed patches (already in upstream): dfa-optimize-period,
  glibc-matcher-fallback, mmap-option-fix, dfa-convert-to-wide-char,
  dfa-speedup-digit-xdigit

* Fri Jun 11 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.3-4
- Colors can be globally disabled via /etc/GREP_COLORS (#602867)
- Fixed indentation in spec
- Fixed defattr in spec

* Mon Jun 07 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.3-3
- Added auto-color profile.d scripts (thanks to Ville Skyttä #600832)
- Removed description macro from changelog

* Thu May 06 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.3-2
- Added dfa-optimize-period patch (speedup for . patterns in UTF-8)
- Added glibc-matcher-fallback patch (speedup for [a-z] patterns in UTF-8)
- Added mmap-option-fix patch
- Added dfa-convert-to-wide-char patch (speedup for -m and remove quadratic
  complexity when going to glibc)
- Added dfa-speedup-digit-xdigit patch (speedup for [[:digit:]] [:xdigit:]])

* Sun Apr 04 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.3-1
- New version: grep-2.6.3
- make check is not silent now

* Fri Mar 26 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.1-1
- New version: grep-2.6.1
- Dropped sigsegv patch (integrated upstream)

* Tue Mar 23 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6-1
- New version: grep-2.6
- Added sigsegv patch (after release patch from upstream)
- Dropped obsoleted patches: fedora-tests, pcrewrap, case, egf-speedup,
  bz460641, utf8, dfa-optional, w

* Fri Mar 05 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.5.4-2
- Added w patch to fix -w switch behaviour broken by dfa-optional patch

* Wed Feb 10 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 2.5.4-1
- New version: grep-2.5.4
- Fixed typos in description
- Updated utf-8 patch
- Added dfa-optional patch (#538423)

* Tue Aug 11 2009 Lubomir Rintel <lkundrak@v3.sk> 2.5.3-6
- Silence possible scriptlets errors

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Stepan Kasal <skasal@redhat.com> 2.5.3-3
- remove grep-mem-exhausted.patch (#481765, #198165)

* Thu Jan  8 2009 Stepan Kasal <skasal@redhat.com> 2.5.3-2
- fix bug #460641 (a.k.a. 479152)

* Thu Nov 20 2008 Lubomir Rintel <lkundrak@v3.sk> 2.5.3-1
- Update to latest upstream version
- Drop upstreamed patches
- Add a couple of regression tests
- Temporarily disable tests
- Minor cleanup

* Wed Oct 1 2008 Lubomir Rintel <lkundrak@v3.sk> 2.5.1a-61
- Fix pcre-mode (-P) line wrapping (bug #324781)
- Match the version with upstream
- Recode AUTHORS to utf8

* Fri Jul 25 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.5.1-60
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.5.1-59
- Autorebuild for GCC 4.3

* Fri Apr 20 2007 Stepan Kasal <skasal@redhat.com> - 2.5.1-58
- Adhere to packaging guidelines.
- Resolves: #225857
- Use CPPFLAGS= argument to configure to add an -I option.
- Do not set LDFLAGS=-s for "make install".

* Mon Jan 22 2007 Tim Waugh <twaugh@redhat.com> 2.5.1-57
- Make preun scriptlet unconditionally succeed (bug #223697).

* Wed Nov 22 2006 Tim Waugh <twaugh@redhat.com> 2.5.1-56
- Fixed count of patterns when the last is an empty string (bug #204255).

* Wed Nov 22 2006 Tim Waugh <twaugh@redhat.com> 2.5.1-55
- Fix 'memory exhausted' errors by limiting in-memory buffer (bug #198165).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.5.1-54.1
- rebuild

* Wed May 31 2006 Tim Waugh <twaugh@redhat.com> 2.5.1-54
- Applied upstream patch to fix '-D skip' (bug #189580).

* Mon Feb 20 2006 Tim Waugh <twaugh@redhat.com> 2.5.1-53
- Applied Tim Robbins' patch for 'grep -w' (bug #179698).

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.5.1-52.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.5.1-52.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb  3 2006 Tim Waugh <twaugh@redhat.com> 2.5.1-52
- Prevent 'grep -P' from segfaulting (bug #171379).

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Sep 29 2005 Tim Waugh <twaugh@redhat.com> 2.5.1-51
- Prevent 'grep -Fw ""' from busy-looping (bug #169524).

* Tue Jun 28 2005 Tim Waugh <twaugh@redhat.com> 2.5.1-50
- Further fixing for bug #161700.

* Mon Jun 27 2005 Tim Waugh <twaugh@redhat.com> 2.5.1-49
- Fix 'grep -Fw' for encodings other than UTF-8 (bug #161700).

* Wed Apr 13 2005 Tim Waugh <twaugh@redhat.com>
- Build requires recent pcre-devel (bug #154626).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 2.5.1-48
- Rebuild for new GCC.

* Fri Jan  7 2005 Tim Waugh <twaugh@redhat.com> 2.5.1-47
- Run 'make check'.
- Fixed -w handling for EGexecute.  Now 'make check' passes.
- Cache MB_CUR_MAX value in egf-speedup patch.
- Fixed variable shadowing in egf-speedup patch.
- Removed redundant (and incorrect) code in prline.

* Fri Jan  7 2005 Tim Waugh <twaugh@redhat.com> 2.5.1-46
- More -w tests from Jakub Jelinek.
- Rebased on 2.5.1a.

* Fri Dec 31 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-45
- More tests (Jakub Jelinek).
- Jakub Jelinek's much improved -Fi algorithm.
- Removed bogus part of grep-2.5.1-fgrep patch.

* Tue Dec 21 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-44
- Fixed -Fi for multibyte input (bug #143079).

* Thu Dec 16 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-43
- Bypass kwset matching when ignoring case and processing multibyte input
  (bug #143079).

* Tue Dec 14 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-42
- Further UTF-8 processing avoided since a '\n' byte is always an
  end-of-line character in that encoding.

* Fri Dec  3 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-41
- Fixed a busy loop in the egf-speedup patch (bug #140781).

* Thu Nov 18 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-40
- Fixed a bug in the fgrep patch, exposed by the dfa-optional patch
  (bug #138558).

* Tue Nov 16 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-39
- Fixed last patch.

* Tue Nov 16 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-38
- Applied patch from Karsten Hopp to fix background colour problems with
  --color output (bug #138913).

* Wed Nov 10 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-37
- Prevent false matches when DFA is disabled (bug #138558).

* Mon Nov  8 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-36
- Automatically disable DFA when processing multibyte input.  GREP_USE_DFA
  environment variable overrides.

* Fri Nov  5 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-35
- Fixes to egf-speedup patch: now it does not change any functionality,
  as intended.
- GREP_NO_DFA now turns off the DFA engine, for performance testing.

* Thu Nov  4 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-34
- More improvements to egf-speedup patch (bug #138076).

* Thu Nov  4 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-33
- Small improvements to egf-speedup patch.

* Wed Nov  3 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-32
- Remove mb-caching hack.
- Better multibyte handling in EGexecute() and Fexecute().
- Don't need regex.c changes in grep-2.5-i18n.patch.

* Wed Oct 13 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-31
- Make 'grep -F' avoid UTF-8 processing if the pattern contains no
  multibyte characters (bug #133932).

* Mon Oct 11 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-30
- Applied patch from Robert Scheck to tidy spec file and add a URL
  tag (bug #135185).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com>
- More build requirements (bug #125323).

* Tue May 18 2004 Jeremy Katz <katzj@redhat.com> 2.5.1-28
- rebuild

* Tue May 18 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-27
- Fix dfa multibyte character class matching when -i is used (bug #123363).
- Use bracket patch before i18n patch to make it clear that the bug exists
  upstream.

* Thu Feb 26 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-26
- Fix fgrep (bug #116909).

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan  5 2004 Tim Waugh <twaugh@redhat.com> 2.5.1-24
- Work around glibc bug #112869 (segfault in re_compile_pattern).
- Avoid patching Makefile.am, to avoid automake/autoconf weirdness.

* Wed Dec 10 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-23
- Another multibyte efficiency bug-fix (bug #111800).

* Mon Dec  8 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-22
- Fixed [:alpha:]-type character classes (bug #108484).
- Fixed -o -i properly (bug #111489).

* Sat Dec  6 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-21
- Fixed 'fgrep -i' (bug #111614).

* Fri Nov 21 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-20
- Another two multibyte efficiency bug-fixes (bug #110524).

* Thu Nov  6 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-19
- Fixed a multibyte efficiency bug.

* Thu Nov  6 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-18
- Turn on multibyte efficiency patch again to shake out bugs.

* Wed Oct  8 2003 Tim Waugh <twaugh@redhat.com>
- Fixed man page bug (bug #106267).

* Thu Sep 18 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-17
- Use symlinks for egrep/fgrep, rather than shell script wrappers.

* Fri Jun 27 2003 Tim Waugh <twaugh@redhat.com>
- Fix debuginfo package.

* Fri Jun 27 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-16.1
- Rebuilt.

* Fri Jun 27 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-16
- Finally give up on making grep go fast. :-(

* Thu Jun 26 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-15.1
- Rebuilt.

* Thu Jun 26 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-15
- Fixed grep -i bug introduced by cache.

* Mon Jun 23 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-14.1
- Rebuilt.

* Mon Jun 23 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-14
- Redo the gofast patch (bug #97785).

* Thu Jun 12 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-13.1
- Rebuilt.

* Thu Jun 12 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-13
- Fixed a bug in the gofast patch (bug #97266).

* Tue Jun 10 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-12.1
- Rebuilt.

* Tue Jun 10 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-12
- Go faster (bug #69900).
- Fix man page.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 29 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-10.1
- Rebuilt.

* Thu May 29 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-10
- Use system regex again.

* Thu May 29 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-9
- Fixed bug in go-fast patch.

* Wed May 28 2003 Tim Waugh <twaugh@redhat.com> 2.5.1-8
- Go fast (bug #69900).
- Run test suite.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 2.5.1-7
- rebuilt

* Tue Nov 19 2002 Tim Waugh <twaugh@redhat.com> 2.5.1-6
- i18n patch.

* Mon Oct 21 2002 Tim Waugh <twaugh@redhat.com> 2.5.1-5
- Don't install /usr/share/info/dir.
- Fix -o -i (bug #72641).

* Sat Jul 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- install all info files #69204

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Mar 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.5.1-1
- 2.5.1

* Wed Mar 13 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.5-1
- 2.5 final

* Wed Jan 23 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.5-0.g.1
- 2.5g

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Nov 19 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5-0.f.4
- Update CVS to reduce bloat

* Thu Nov  8 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5-0.f.3
- Don't fail %%post with --excludedocs

* Wed Sep 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5-0.f.2
- Fix up echo A |grep '[A-Z0-9]' in locales other than C

* Tue Sep 25 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5-0.f.1
- 2.5f, fixes #53603

* Wed Jul 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.4.2-7
- Fix up the i18n patch - it used to break "grep '[]a]'" (#49003)
- revert to 2.4.2 (latest official release) for now

* Mon May 28 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5e-4
- Fix "echo Linux forever |grep -D skip Linux"

* Mon May 21 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5e-3
- Add new -D, --devices option
- Fix a bug with "directories" being uninitialized

* Sun May 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5e-2
- Fix up the --color option to behave like the one from ls (--color=auto)
  Sooner or later, some people will alias grep="grep --color" and wonder why
  their scripts break.
- Update docs accordingly
- Get rid of the annoying blinking in grep --color

* Sun May 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.5e-1
- 2.5e

* Tue Feb 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}
- langify

* Sun Aug 20 2000 Jakub Jelinek <jakub@redhat.com>
- i18n character ranges patch from Ulrich Drepper

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify

* Tue Mar 21 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 2.4.2
- fix download URL

* Thu Feb 03 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- gzip info pages (Bug #9035)

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Wed Dec 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.4.

* Wed Oct 20 1999 Bill Nottingham <notting@redhat.com>
- prereq install-info

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- upgraded to grep 2.3, added install-info %%post/%%preun for info

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Sat May 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.2

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- updated from 2.0 to 2.1
- spec file cleanups
- added BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
