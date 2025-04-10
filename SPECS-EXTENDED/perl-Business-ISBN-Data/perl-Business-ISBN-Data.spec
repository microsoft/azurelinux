Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           perl-Business-ISBN-Data
Version:        20240930.001
Release:        2%{?dist}
Summary:        The data pack for Business::ISBN
License:        Artistic-2.0
URL:            https://metacpan.org/release/Business-ISBN-Data
Source0:        https://cpan.metacpan.org/modules/by-module/Business/Business-ISBN-Data-%{version}.tar.gz#/perl-Business-ISBN-Data-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Manifest) >= 1.21
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(strict)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test::More) >= 0.95
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Dependencies
# (none)

%description
This is a data pack for Business::ISBN.  You can update
the ISBN data without changing the version of Business::ISBN.
Most of the interesting stuff is in Business::ISBN.

%prep
%setup -q -n Business-ISBN-Data-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README.pod examples/ t/
%{perl_vendorlib}/Business/
%{_mandir}/man3/Business::ISBN::Data.3*

%changelog
* Thu Dec 12 2024 Jyoti Kanase <v-jykanase@microsoft.com> - 20240930.001-2
- Initial CBL-Mariner import from Fedora 41 (license: MIT).
- License verified

* Mon Sep 30 2024 Jitka Plesnikova <jplesnik@redhat.com> - 20240930.001-1
- 20240930.001 bump (rhbz#2315652)

* Thu Sep 19 2024 Paul Howarth <paul@city-fan.org> - 20240918.001-1
- 20240918.001 bump

* Sun Sep 15 2024 Paul Howarth <paul@city-fan.org> - 20240914.001-1
- 20240914.001 bump (rhbz#2312391)

* Fri Sep  6 2024 Paul Howarth <paul@city-fan.org> - 20240906.001-1
- 20240906.001 bump (rhbz#2310418)

* Wed Aug 21 2024 Paul Howarth <paul@city-fan.org> - 20240821.001-1
- 20240821.001 bump (rhbz#2306448)

* Tue Aug 20 2024 Paul Howarth <paul@city-fan.org> - 20240820.001-1
- 20240820.001 bump

* Sat Aug 17 2024 Paul Howarth <paul@city-fan.org> - 20240817.001-1
- 20240817.001 bump

* Thu Aug 15 2024 Paul Howarth <paul@city-fan.org> - 20240815.001-1
- 20240815.001 bump (rhbz#2305174)

* Wed Aug  7 2024 Paul Howarth <paul@city-fan.org> - 20240807.001-1
- 20240807.001 bump (rhbz#2303454)

* Sat Aug  3 2024 Paul Howarth <paul@city-fan.org> - 20240803.001-1
- 20240803.001 bump (rhbz#2302579)

* Thu Jul 25 2024 Paul Howarth <paul@city-fan.org> - 20240725.001-1
- 20240725.001 bump

* Fri Jul 19 2024 Paul Howarth <paul@city-fan.org> - 20240718.001-1
- 20240718.001 bump (rhbz#2298736)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240716.001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Paul Howarth <paul@city-fan.org> - 20240716.001-1
- 20240716.001 bump (rhbz#2298226)

* Wed Jul 10 2024 Paul Howarth <paul@city-fan.org> - 20240710.001-1
- 20240710.001 bump (rhbz#2297072)

* Tue Jul  9 2024 Paul Howarth <paul@city-fan.org> - 20240709.001-1
- 20240709.001 bump (rhbz#2296627)

* Sat Jun 15 2024 Paul Howarth <paul@city-fan.org> - 20240614.001-1
- 20240614.001 bump (rhbz#2292468)

* Sun Jun  2 2024 Paul Howarth <paul@city-fan.org> - 20240601.001-1
- 20240601.001 bump (rhbz#2284202)

* Fri May 24 2024 Paul Howarth <paul@city-fan.org> - 20240523.001-1
- 20240523.001 bump (rhbz#2283021)

* Fri May 10 2024 Paul Howarth <paul@city-fan.org> - 20240509.001-1
- 20240509.001 bump

* Mon Apr 29 2024 Jitka Plesnikova <jplesnik@redhat.com> - 20240426.001-1
- 20240426.001 bump (rhbz#2277396)

* Sat Apr 20 2024 Paul Howarth <paul@city-fan.org> - 20240420.001-1
- 20240420.001 bump (rhbz#2276198)

* Sun Apr 14 2024 Paul Howarth <paul@city-fan.org> - 20240413.001-1
- 20240413.001 bump (rhbz#2274936)

* Sun Mar 24 2024 Paul Howarth <paul@city-fan.org> - 20240323.001-1
- 20240323.001 bump (rhbz#2271173)

* Thu Mar 21 2024 Paul Howarth <paul@city-fan.org> - 20240321.001-1
- 20240321.001 bump

* Wed Mar 13 2024 Paul Howarth <paul@city-fan.org> - 20240313.001-1
- 20240313.001 bump (rhbz#2269338)

* Fri Mar  8 2024 Paul Howarth <paul@city-fan.org> - 20240308.001-1
- 20240308.001 bump (rhbz#2268556)

* Sun Mar  3 2024 Paul Howarth <paul@city-fan.org> - 20240302.001-1
- 20240302.001 bump (rhbz#2267478)

* Fri Mar  1 2024 Paul Howarth <paul@city-fan.org> - 20240229.001-1
- 20240229.001 bump (rhbz#2267133)

* Sun Feb 11 2024 Paul Howarth <paul@city-fan.org> - 20240209.001-1
- 20240209.001 bump (rhbz#2263590)

* Tue Feb 06 2024 Jitka Plesnikova <jplesnik@redhat.com> - 20240206.001-1
- 20240206.001 bump (rhbz#2262917)

* Fri Jan 26 2024 Jitka Plesnikova <jplesnik@redhat.com> - 20240126.001-1
- 20240126.001 bump (rhbz#2260428)

* Tue Jan 23 2024 Paul Howarth <paul@city-fan.org> - 20240123.001-1
- 20240123.001 bump

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240116.001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Paul Howarth <paul@city-fan.org> - 20240116.001-1
- 20240116.001 bump (rhbz#2258613)

* Fri Jan 12 2024 Paul Howarth <paul@city-fan.org> - 20240111.001-1
- 20240111.001 bump (rhbz#2257961)

* Thu Dec 21 2023 Paul Howarth <paul@city-fan.org> - 20231220.001-1
- 20231220.001 bump (rhbz#2255496)

* Fri Dec 15 2023 Paul Howarth <paul@city-fan.org> - 20231215.001-1
- 20231215.001 bump (rhbz#2254689)

* Thu Nov 30 2023 Paul Howarth <paul@city-fan.org> - 20231130.001-1
- 20231130.001 bump

* Sat Nov 25 2023 Paul Howarth <paul@city-fan.org> - 20231125.001-1
- 20231125.001 bump (rhbz#2251459)

* Sun Nov 19 2023 Paul Howarth <paul@city-fan.org> - 20231118.001-1
- 20231118.001 bump (rhbz#2250416)

* Tue Nov 14 2023 Paul Howarth <paul@city-fan.org> - 20231114.001-1
- 20231114.001 bump (rhbz#2249602)

* Fri Nov 10 2023 Paul Howarth <paul@city-fan.org> - 20231110.001-1
- 20231110.001 bump (rhbz#2249035)

* Thu Nov  2 2023 Paul Howarth <paul@city-fan.org> - 20231102.001-1
- 20231102.001 bump (rhbz#2247582)

* Tue Oct 31 2023 Paul Howarth <paul@city-fan.org> - 20231031.001-1
- 20231031.001 bump (rhbz#2247270)

* Fri Oct 20 2023 Paul Howarth <paul@city-fan.org> - 20231020.001-1
- 20231020.001 bump (rhbz#2245229)

* Fri Oct 13 2023 Paul Howarth <paul@city-fan.org> - 20231013.001-1
- 20231013.001 bump (rhbz#2243835)

* Tue Oct 10 2023 Paul Howarth <paul@city-fan.org> - 20231010.001-1
- 20231010.001 bump (rhbz#2243069)

* Sun Oct  8 2023 Paul Howarth <paul@city-fan.org> - 20231006.001-1
- 20231006.001 bump (rhbz#2242684)

* Tue Sep 26 2023 Paul Howarth <paul@city-fan.org> - 20230926.001-1
- 20230926.001 bump

* Sun Sep 24 2023 Paul Howarth <paul@city-fan.org> - 20230923.001-1
- 20230923.001 bump (rhbz#2240303)

* Thu Sep  7 2023 Paul Howarth <paul@city-fan.org> - 20230907.001-1
- 20230907.001 bump (rhbz#2237858)

* Tue Sep  5 2023 Paul Howarth <paul@city-fan.org> - 20230904.001-1
- 20230904.001 bump (rhbz#2237353)

* Wed Aug 30 2023 Jitka Plesnikova <jplesnik@redhat.com> - 20230830.001-1
- 20230830.001 bump (rhbz#2236151)

* Tue Aug 22 2023 Paul Howarth <paul@city-fan.org> - 20230822.001-1
- 20230822.001 bump (rhbz#2233365)

* Fri Aug 11 2023 Paul Howarth <paul@city-fan.org> - 20230811.001-1
- 20230811.001 bump (rhbz#2231347)

* Sun Jul 30 2023 Paul Howarth <paul@city-fan.org> - 20230729.001-1
- 20230729.001 bump (rhbz#2227461)

* Thu Jul 20 2023 Paul Howarth <paul@city-fan.org> - 20230719.001-1
- 20230719.001 bump (rhbz#2224116)

* Wed Jul 19 2023 Jitka Plesnikova <jplesnik@redhat.com> - 20230718.001-1
- 20230718.001 bump (rhbz#2223772)

* Sun Jul 16 2023 Paul Howarth <paul@city-fan.org> - 20230714.001-1
- 20230714.001 bump (rhbz#2222866)

* Fri Jul  7 2023 Paul Howarth <paul@city-fan.org> - 20230707.001-1
- 20230707.001 bump (rhbz#2221022)

* Mon Jun 26 2023 Paul Howarth <paul@city-fan.org> - 20230626.001-1
- 20230626.001 bump (rhbz#2217555)

* Mon May 29 2023 Jitka Plesnikova <jplesnik@redhat.com> - 20230528.001-1
- 20230528.001 bump

* Wed May 17 2023 Jitka Plesnikova <jplesnik@redhat.com> - 20230516.001-1
- 20230516.001 bump

* Thu May  4 2023 Paul Howarth <paul@city-fan.org> - 20230426.002-1
- 20230426.002 bump

* Thu Apr 27 2023 Jitka Plesnikova <jplesnik@redhat.com> - 20230426.001-1
- 20230426.001 bump (rhbz#2190042)

* Mon Apr 10 2023 Paul Howarth <paul@city-fan.org> - 20230410.001-1
- 20230410.001 bump (rhbz#2185525)

* Mon Apr 03 2023 Jitka Plesnikova <jplesnik@redhat.com> - 20230331.001-1
- 20230331.001 bump

* Thu Mar 23 2023 Jitka Plesnikova <jplesnik@redhat.com> - 20230322.001-1
- 20230322.001 bump

* Fri Mar 17 2023 Paul Howarth <paul@city-fan.org> - 20230316.001-1
- 20230316.001 bump (rhbz#2179198)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20210112.006-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210112.006-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 20210112.006-5
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210112.006-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210112.006-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 20210112.006-2
- Perl 5.34 rebuild

* Tue Feb 16 2021 Jitka Plesnikova <jplesnik@redhat.com> - 20210112.006-1
- 20210112.006 bump

* Sat Feb 13 2021 Paul Howarth <paul@city-fan.org> - 20210112.005-1
- 20210112.005 bump

* Wed Feb 10 2021 Jitka Plesnikova <jplesnik@redhat.com> - 20210112.004-1
- 20210112.004 bump

* Sun Feb  7 2021 Paul Howarth <paul@city-fan.org> - 20210112.002-1
- 20210112.002 bump

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210112.001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Jitka Plesnikova <jplesnik@redhat.com> - 20210112.001-1
- 20210112.001 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20191107-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 20191107-3
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20191107-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 12 2019 Jitka Plesnikova <jplesnik@redhat.com> - 20191107-1
- 20191107 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 20140910.003-11
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 20140910.003-8
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 20140910.003-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 20140910.003-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20140910.003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 16 2015 Paul Howarth <paul@city-fan.org> - 20140910.003-1
- Update to 20140910.003
  - Hide the Business::ISBN namespace
- Drop now-redundant provides filter

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140910.002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 20140910.002-2
- Perl 5.22 rebuild

* Tue Sep 23 2014 Paul Howarth <paul@city-fan.org> - 20140910.002-1
- Update to 20140910.002
  - Look in the current directory for RangeMessage.xml if it's not in other
    locations; this can help with various Perl app packagers (also try
    ISBN_RANGE_MESSAGE env var)

* Fri Sep 19 2014 Paul Howarth <paul@city-fan.org> - 20140910.001-1
- Update to 20140910.001
  - Update to the latest data (2014-09-10)
- Use %%license
- Classify buildreqs by usage
- Drop redundant LWP::Simple requires filter

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 20120719.001-6
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120719.001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120719.001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 20120719.001-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120719.001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 26 2012 Paul Howarth <paul@city-fan.org> - 20120719.001-1
- Update to 20120719.001:
  - Require Test::More ≥ 0.95 for subtest support
  - No code or feature changes
- Bump Test::Manifest version requirement to 1.21
- Bump Test::More version requirement to 0.95
- Drop redundant buildreq perl(Test::Prereq)

* Tue Jul 24 2012 Paul Howarth <paul@city-fan.org> - 20120719-1
- Update to 20120719:
  - Support using data from RangeMessage.xml, so you can use the latest data
    from ISBN without updating this module
- Fix shellbang and permissions of make_data.pl script to placate rpmlint
- Filter dependency on perl(LWP::Simple), required only by make_data.pl script,
  not in normal operation
- Don't need to remove empty directories from the buildroot
- BR: perl(Carp), perl(File::Spec::Functions) and perl(Test::Manifest) ≥ 1.14
- BR: at least version 1.00 of perl(Test::Pod)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081208-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 20081208-9
- Perl 5.16 rebuild

* Fri Jan 20 2012 Paul Howarth <paul@city-fan.org> - 20081208-8
- Clean up for modern rpmbuild:
  - Drop BuildRoot specification
  - Drop %%clean section
  - Don't bother cleaning buildroot in %%install section
  - Make %%files list more explicit
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Use %%{_fixperms} macro rather than our own chmod incantation
  - Replace provides filter with version that works with rpm ≥ 4.9
- Include tests as %%doc since they're referred to by examples/README

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081208-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 20081208-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081208-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 20081208-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 20081208-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 20081208-2
- rebuild against perl 5.10.1

* Mon Oct  5 2009 Stepan Kasal <skasal@redhat.com> - 20081208-1
- new upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081020-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081020-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Stepan Kasal <skasal@redhat.com> - 20081020-1
- new upstream version

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.15-4
- rebuild for new perl

* Thu Nov 15 2007 Robin Norwood <rnorwood@redhat.com> - 1.15-3
- Should not provide perl(Business::ISBN)

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 1.15-2
- Fix BuildRequires

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 1.15-1
- Initial build
