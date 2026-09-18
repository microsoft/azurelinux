# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-autobox
Version:        3.0.2
Release:        4%{?dist}
Summary:        Call methods on native types
License:        Artistic-2.0
URL:            https://metacpan.org/release/autobox
Source0:        https://cpan.metacpan.org/modules/by-module/autobox/autobox-v%{version}.tar.gz
# Build:
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Scope::Guard) >= 0.21
BuildRequires:  perl(Storable)
BuildRequires:  perl(strict)
BuildRequires:  perl(version) >= 0.77
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl-debugger
BuildRequires:  perl(blib)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IPC::System::Simple) >= 1.30
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::Fatal) >= 0.017
BuildRequires:  perl(Test::More)
BuildRequires:  perl(vars)
# Optional Tests:
BuildRequires:  perl(Test::Pod) >= 1.00
# Dependencies:
Requires:       perl(Scope::Guard) >= 0.21

%{?perl_default_filter}

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Scope::Guard\\)$

%description
The autobox pragma allows methods to be called on integers, floats,
strings, arrays, hashes, and code references in exactly the same manner as
blessed references.

%prep
%setup -q -n autobox-v%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE.md
%doc Changes README
%{perl_vendorarch}/auto/autobox/
%{perl_vendorarch}/autobox/
%{perl_vendorarch}/autobox.pm
%doc %{perl_vendorarch}/autobox.pod
%{_mandir}/man3/autobox.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.2-3
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep  4 2024 Paul Howarth <paul@city-fan.org> - 3.0.2-1
- Update to 3.0.2 (rhbz#2309576)
  - Fix debugger test (GH#15)
  - Upgrade ppport.h from 3.42 to 3.68
  - Fix doc typo (GH#12)
  - Fix changelog typo (GH#14)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.1-23
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.1-19
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 31 2022 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.1-16
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.1-13
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.1-10
- Perl 5.32 rebuild

* Tue Mar 10 2020 Petr Pisar <ppisar@redhat.com> - 3.0.1-9
- Build-require perl-debugger for tests

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov  6 2019 Paul Howarth <paul@city-fan.org> - 3.0.1-7
- Spec tidy-up
  - Use author-independent source URL
  - Use %%{make_build} and %%{make_install}

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.1-5
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.1-2
- Perl 5.28 rebuild

* Mon May  7 2018 Paul Howarth <paul@city-fan.org> - 3.0.1-1
- Update to 3.0.1
  - Breaking change:
    - The behaviour of UNIVERSAL methods like $native->can and $native->isa is
      now defined as being the same as when autobox is not enabled rather than
      "undefined" (technically, this still falls under the rubric of
      "undefined", but the switch from "don't know" to "don't" could break
      buggy code, so bump for safety)
    - Add DOES to the list of non-autoboxed methods
  - Switch to semantic versioning scheme
  - Upgrade ppport.h from 3.35 → 3.42
  - Fix version declaration on 5.8 (GH#11)

* Mon Apr 23 2018 Paul Howarth <paul@city-fan.org> - 2.86-1
- Update to 2.86
  - Fix bug that prevented autoboxing working under the debugger on perl 5.22+
    (GH#9); added t/debugger.t
  - Fix bug that prevented bareword method-calls being exempted when the method
    is a variable e.g. Foo->$bar (GH#8)
  - Add operator-overloading note to the gotchas section (GH#7)
- License changed to Artistic 2.0
- Drop legacy Group: tag

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.85-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.85-2
- Perl 5.26 rebuild

* Tue Feb 28 2017 Paul Howarth <paul@city-fan.org> - 2.85-1
- Update to 2.85
  - Fix failing test under 5.25.10 with -Ddefault_inc_excludes_dot

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.84-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 30 2016 Paul Howarth <paul@city-fan.org> - 2.84-1
- Update to 2.84
  - Compatibility fix for perl ≥ 5.25
  - Upgrade ppport.h from 3.20 to 3.35
  - Add .travis.yml

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.83-6
- Perl 5.24 rebuild

* Tue Apr 19 2016 Paul Howarth <paul@city-fan.org> - 2.83-5
- Fix FTBFS due to missing buildreq perl-devel
- Simplify find command using -empty and -delete
- Make %%files list more explicit

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.83-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.83-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.83-2
- Perl 5.22 rebuild

* Wed Feb 04 2015 Petr Šabata <contyk@redhat.com> - 2.83-1
- 2.83 bump

* Fri Dec 05 2014 Petr Pisar <ppisar@redhat.com> - 2.82-1
- 2.82 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.77-7
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.77-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.77-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.77-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 2.77-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Iain Arnell <iarnell@gmail.com> 2.77-1
- update to latest upstream version

* Fri Dec 07 2012 Iain Arnell <iarnell@gmail.com> 2.76-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.75-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 2.75-3
- Perl 5.16 rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Aug 14 2011 Iain Arnell <iarnell@gmail.com> 2.75-1
- update to latest upstream version

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> 2.73-3
- update filters for rpm 4.9

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.73-2
- Perl mass rebuild

* Sat May 07 2011 Iain Arnell <iarnell@gmail.com> 2.73-1
- update to latest upstream version

* Sat Feb 19 2011 Iain Arnell <iarnell@gmail.com> 2.71-3
- update requires filtering to use standard macros

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Iain Arnell <iarnell@gmail.com> 2.71-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.55-6
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.55-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.55-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.55-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Allisson Azevedo <allisson@gmail.com> 2.55-1
- Initial rpm release.
