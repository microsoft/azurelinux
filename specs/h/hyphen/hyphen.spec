# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:      hyphen
Summary:   A text hyphenation library
Version:   2.8.8
Release: 28%{?dist}
Source:    http://downloads.sourceforge.net/hunspell/hyphen-%{version}.tar.gz
URL:       http://hunspell.sf.net
License:   GPL-2.0-only OR LGPL-2.1-or-later OR MPL-1.1
BuildRequires: perl-interpreter, patch, autoconf, automake, libtool
%ifarch %{valgrind_arches}
BuildRequires: valgrind
%endif
BuildRequires: make

%description
Hyphen is a library for high quality hyphenation and justification.

%package devel
Requires: hyphen = %{version}-%{release}
Summary: Files for developing with hyphen

%description devel
Includes and definitions for developing with hyphen

%package en
Requires: hyphen
Summary: English hyphenation rules
BuildArch: noarch

%description en
English hyphenation rules.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%check
make check
%ifarch %{valgrind_arches}
VALGRIND=memcheck make check
%endif

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

pushd $RPM_BUILD_ROOT/%{_datadir}/hyphen/
en_US_aliases="en_AG en_AU en_BS en_BW en_BZ en_CA en_DK en_GB en_GH en_HK en_IE en_IN en_JM en_MW en_NA en_NZ en_PH en_SG en_TT en_ZA en_ZM en_ZW"
for lang in $en_US_aliases; do
        ln -s hyph_en_US.dic hyph_$lang.dic
done
popd


%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog README README.hyphen README.nonstandard TODO
%{_libdir}/*.so.*
%dir %{_datadir}/hyphen

%files en
%{_datadir}/hyphen/hyph_en*.dic

%files devel
%{_includedir}/hyphen.h
%{_libdir}/*.so
%{_bindir}/substrings.pl

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 06 2024 David Abdurachmanov <davidlt@rivosinc.com> - 2.8.8-24
- Properly check valgrind arches

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Feb 23 2023 Caolán McNamara <caolanm@redhat.com> - 2.8.8-20
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 12 2016 Michal Toman <mtoman@fedoraproject.org> - 2.8.8-5
- Resolves: rhbz#1366680 No valgrind on MIPS

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2.8.8-3
- Valgrind is not available only on s/390
- tests with Valgrind fail only on arm

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Sep 18 2014 Caolán McNamara <caolanm@redhat.com> - 2.8.8-1
- latest version

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 03 2014 David Tardon <dtardon@redhat.com> - 2.8.7-2
- fix hyphen.h

* Fri Jun 27 2014 Caolán McNamara <caolanm@redhat.com> - 2.8.7-1
- latest version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 04 2013 Caolán McNamara <caolanm@redhat.com> - 2.8.6-3
- Resolves: rhbz#925563 support aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Caolán McNamara <caolanm@redhat.com> - 2.8.6-1
- latest version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Caolán McNamara <caolanm@redhat.com> - 2.8.5-1
- latest version

* Fri Jun 29 2012 Caolán McNamara <caolanm@redhat.com> - 2.8.4-1
- latest version

* Wed Apr 18 2012 Caolán McNamara <caolanm@redhat.com> - 2.8.3-4
- Resolves: rhbz#813481 x86_64 valgrind spews, see rhbz#813780
- Related: rhbz#813481 dump valgrind failure log

* Thu Apr 12 2012 Caolán McNamara <caolanm@redhat.com> - 2.8.3-3
- add Malawian alias
- add Zambian alias

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 24 2011 Caolán McNamara <caolanm@redhat.com> - 2.8.3-1
- latest version

* Mon Oct 17 2011 Caolán McNamara <caolanm@redhat.com> - 2.8-1
- latest version

* Fri Jun 24 2011 Caolán McNamara <caolanm@redhat.com> - 2.7-3
- Resolves: rhbz#715995 FTBFS

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Caolán McNamara <caolanm@redhat.com> - 2.7-1
- latest version

* Mon Jul 19 2010 Caolán McNamara <caolanm@redhat.com> - 2.6-1
- latest version
- run make check

* Thu Feb 25 2010 Caolán McNamara <caolanm@redhat.com> - 2.5-1
- latest version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Caolán McNamara <caolanm@redhat.com> - 2.4-4
- make hyphen-en a noarch subpackage

* Fri Jun 12 2009 Caolán McNamara <caolanm@redhat.com> - 2.4-3
- extend coverage

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri May 02 2008 Caolán McNamara <caolanm@redhat.com> - 2.4-1
- latest version

* Tue Feb 19 2008 Caolán McNamara <caolanm@redhat.com> - 2.3.1-1
- latest version

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3-2
- Autorebuild for GCC 4.3

* Mon Nov 12 2007 Caolán McNamara <caolanm@redhat.com> - 2.3-1
- initial version
