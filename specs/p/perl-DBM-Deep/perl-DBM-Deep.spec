# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-DBM-Deep
Version:        2.0019
Release: 7%{?dist}
Summary:        A pure perl multi-level hash/array DBM
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/DBM-Deep
Source0:        https://cpan.metacpan.org/modules/by-module/DBM/DBM-Deep-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Module::Build) >= 0.42
# Module Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DBI) >= 1.5
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(Hash::Util::FieldHash)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Test Suite
BuildRequires:  perl(blib)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Warn)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
# Optional Tests
BuildRequires:  perl(DBD::SQLite) >= 1.25
BuildRequires:  perl(FileHandle::Fmode)
BuildRequires:  perl(Pod::Simple)
BuildRequires:  perl(Pod::Usage) >= 1.3
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
# Dependencies
Requires:       perl(Carp)
Requires:       perl(Data::Dumper)
Requires:       perl(Digest::MD5)
Requires:       perl(Hash::Util::FieldHash)

%description
A unique flat-file database module, written in pure perl. True multi-level
hash/array support (unlike MLDBM, which is faked), hybrid OO / tie()
interface, cross-platform FTPable files, and quite fast. Can handle
millions of keys and unlimited hash levels without significant slow-down.
Written from the ground-up in pure perl - this is NOT a wrapper around a
C-based DBM. Out-of-the-box compatibility with Unix, Mac OS X and Windows.

%prep
%setup -q -n DBM-Deep-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
%{_fixperms} -c %{buildroot}

%check
LONG_TESTS=1 TEST_SQLITE=1 ./Build test

%files
%doc Changes README
%{perl_vendorlib}/DBM/
%{_mandir}/man3/DBM::Deep.3*
%{_mandir}/man3/DBM::Deep::ConfigData.3*
%{_mandir}/man3/DBM::Deep::Cookbook.3*
%{_mandir}/man3/DBM::Deep::Engine.3*
%{_mandir}/man3/DBM::Deep::Engine::File.3*
%{_mandir}/man3/DBM::Deep::Internals.3*
%{_mandir}/man3/DBM::Deep::Iterator.3*
%{_mandir}/man3/DBM::Deep::Iterator::File::BucketList.3*
%{_mandir}/man3/DBM::Deep::Iterator::File::Index.3*
%{_mandir}/man3/DBM::Deep::Null.3*
%{_mandir}/man3/DBM::Deep::Storage.3*
%{_mandir}/man3/DBM::Deep::Storage::File.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0019-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0019-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0019-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0019-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0019-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 13 2023 Paul Howarth <paul@city-fan.org> - 2.0019-1
- Update to 2.0019 (rhbz#2249377)
  - Improvement so that when you try to put too much data in you get a useful
    error, and don't corrupt the database
- Use author-independent source URL
- Drop support for building with Module::Build < 0.42

* Thu Nov  9 2023 Paul Howarth <paul@city-fan.org> - 2.0018-1
- Update to 2.0018 (rhbz#2248772)
  - Tiny documentation and metadata fixes to make sure people go to the correct
    issue tracker

* Sun Sep  3 2023 Paul Howarth <paul@city-fan.org> - 2.0017-1
- Update to 2.0017 (rhbz#2236875)
  - Get rid of old perl4-style ' package separator and use :: instead for
    compatibility with perl 5.38 (CPAN RT#148417)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0016-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 23 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.0016-18
- Fix test 01_basic.t to pass with Perl 5.38

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0016-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0016-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.0016-15
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0016-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Dec 19 2021 Paul Howarth <paul@city-fan.org> - 2.0016-13
- Additional test deps: perl(blib) and perl(FileHandle::Fmode) for EPEL

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0016-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.0016-11
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0016-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0016-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.0016-8
- Perl 5.32 rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0016-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0016-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.0016-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0016-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0016-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.0016-2
- Perl 5.28 rebuild

* Mon May 21 2018 Paul Howarth <paul@city-fan.org> - 2.0016-1
- Update to 2.0016
  - Fix for tests failing on 5.28
- Switch upstream from search.cpan.org to metacpan.org

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0014-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jul 28 2017 Paul Howarth <paul@city-fan.org> - 2.0014-1
- Update to 2.0014
  - Fix for tests failing on 5.26
- Drop explicit buildroot cleaning in %%install section
- BR: perl-interpreter rather than perl

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0013-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.0013-5
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0013-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.0013-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0013-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan  2 2016 Paul Howarth <paul@city-fan.org> - 2.0013-1
- Update to 2.0013
  - Documentation updates (GH#14, GH#15, GH#16)

* Wed Jun 17 2015 Paul Howarth <paul@city-fan.org> - 2.0012-1
- Update to 2.0012
  - Improved transaction validation and warnings (GH#12)
- Classify buildreqs by usage
- Use Hash::Util::FieldHash
- Enumerate manpages in %%files list

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.0011-4.1
- Perl 5.22 rebuild

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.0011-3.1
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0011-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 14 2014 Lubomir Rintel <lkundrak@v3.sk> - 2.0011-1.1
- Fix epel7 build

* Mon Jan 13 2014 Paul Howarth <paul@city-fan.org> - 2.0011-1
- Update to 2.0011
  - Pod fixes

* Tue Nov 12 2013 Paul Howarth <paul@city-fan.org> - 2.0010-1
- Update to 2.0010
  - Can push undefined values onto arrays
- Drop upstreamed POD patch

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0009-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 2.0009-2
- Perl 5.18 rebuild

* Mon Jul  1 2013 Paul Howarth <paul@city-fan.org> - 2.0009-1
- Update to 2.0009
  - Fix for pushing non-true values in DBM::Deep::Array (CPAN RT#85414)
- This release by RKINYON -> update source URL
- Add patch to fix broken POD (CPAN RT#85252)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0008-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 2.0008-2
- Perl 5.16 rebuild

* Mon Jun 18 2012 Paul Howarth <paul@city-fan.org> - 2.0008-1
- Update to 2.0008 (#832921)
  - Arrays and hashes retrieved from a database no longer create circular
    references (CPAN RT#77746)
- Don't use macros for commands

* Sun Jun 17 2012 Petr Pisar <ppisar@redhat.com> - 2.0007-2
- Perl 5.16 rebuild

* Mon May 28 2012 Paul Howarth <paul@city-fan.org> - 2.0007-1
- Update to 2.0007
  - Include one-line descriptions of each POD page after the name
    (CPAN RT#76378)
  - t/98_pod.t: skip tests if Pod::Simple 3.21 is installed (CPAN RT#77419)
- BR: perl(Pod::Simple)

* Fri May 18 2012 Petr Pisar <ppisar@redhat.com> - 2.0006-2
- Do not build-require FileHandle::Fmode on RHEL ≥ 7 (#822885)

* Mon Apr  2 2012 Paul Howarth <paul@city-fan.org> - 2.0006-1
- Update to 2.0006
  - Try harder to get t/27_filehandle.t to work under TB2; the extra
    'TAP version 13' line was causing a TAP parse error

* Mon Mar 26 2012 Paul Howarth <paul@city-fan.org> - 2.0005-1
- Update to 2.0005 (t/27_filehandle.t has been fixed again; it no longer
  violates Test::Builder's encapsulation)
- BR/R: perl(Carp) and perl(Data::Dumper)
- Add buildreqs for module and support utilities: perl ≥ 5.8.4, perl(base),
  perl(constant), perl(DBI), perl(FileHandle::Fmode) and perl(Pod::Usage) ≥ 1.3
- Add buildreqs for additional test coverage: perl(DBD::SQLite),
  perl(Exporter), perl(Test::Pod) and perl(Test::Pod::Coverage)
- Run LONG_TESTS and SQLite tests too
- Don't need to remove empty directories from the buildroot
- Make %%files list more explicit
- Use %%{_fixperms} macro rather than our own chmod incantation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 09 2011 Iain Arnell <iarnell@gmail.com> 2.0004-2
- R/BR perl(Digest::MD5)

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.0004-1
- update to 2.004
- clean spec, add BR Test::Deep, Test::Warn

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.983-12
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.983-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.983-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.983-9
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.983-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.983-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.983-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.983-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.983-3
- rebuild for new perl

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 0.983-2
- FE6 Rebuild

* Thu Apr 27 2006 Andreas Thienemann <andreas@bawue.net> 0.983-1
- Specfile autogenerated by cpanspec 1.64.
- Cleaned up for FE
