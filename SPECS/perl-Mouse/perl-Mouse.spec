# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           perl-Mouse
Summary:        Moose minus the antlers
Version:        2.5.11
Release:        5%{?dist}
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Mouse
Source0:        https://cpan.metacpan.org/modules/by-module/Test/Mouse-v%{version}.tar.gz
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Devel::PPPort) >= 3.59
BuildRequires:  perl(ExtUtils::ParseXS) >= 3.22
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Build::XSUtil) >= 0.19
BuildRequires:  perl(utf8)
BuildRequires:  sed
# Module Runtime
BuildRequires:  perl(B)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Filter::Simple)
BuildRequires:  perl(mro)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util) >= 1.14
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(version) >= 0.9913
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader) >= 0.02
# Test Suite
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(if)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::String)
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::LeakTrace) >= 0.10
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(Tie::Array)
BuildRequires:  perl(Tie::Hash)
BuildRequires:  perl(Tie::Scalar)
# Optional Tests
BuildRequires:  perl(Data::Dump::Streamer)
BuildRequires:  perl(Declare::Constraints::Simple)
BuildRequires:  perl(HTTP::Headers)
BuildRequires:  perl(Locale::US)
BuildRequires:  perl(Moose)
%if !%{defined perl_bootstrap}
BuildRequires:  perl(MouseX::Foreign)
%endif
BuildRequires:  perl(Params::Coerce)
BuildRequires:  perl(Path::Class)
%if !%{defined perl_bootstrap}
# Break build cycle: perl-Mouse → perl-Pod-Coverage-Moose
# → perl-namespace-autoclean → perl-Mouse
BuildRequires:  perl(Pod::Coverage::Moose)
%endif
BuildRequires:  perl(Regexp::Common)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::Output)
BuildRequires:  perl(URI)
# Dependencies
Requires:       perl(Scalar::Util) >= 1.14
Requires:       perl(Data::Dumper)
Requires:       perl(mro)
Requires:       perl(XSLoader) >= 0.02

# Virtual provides for perl-Any-Moose
Provides:       perl(Any-Moose) = %{version}

%{?perl_default_filter}
# filter unversioned Mouse::Util provide from Mouse/PurePerl.pm
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(Mouse::Util\\)$

%description
Moose, a powerful metaobject-fueled extension of the Perl 5 object system,
is wonderful.  (For more information on Moose, please see 'perldoc Moose'
after installing the perl-Moose package.)

Unfortunately, it's a little slow. Though significant progress has been
made over the years, the compile time penalty is a non-starter for some
applications.  Mouse aims to alleviate this by providing a subset of Moose's
functionality, faster.

%package -n perl-Test-Mouse
License:    GPL-1.0-or-later OR Artistic-1.0-Perl
Summary:    Test functions for Mouse specific features
Requires:   %{name} = %{version}-%{release}

%description -n perl-Test-Mouse
This module provides some useful test functions for Mouse based classes. It is
an experimental first release, so comments and suggestions are very welcome.

%prep
%setup -q -n Mouse-v%{version}

# Fix permissions
find . -type f -exec chmod -c -x {} ';'

# Fix shellbangs
find benchmarks/ example/ t/ tool/ -type f -print0 |
  xargs -0 sed -i '1s|^#!.*perl|#!%{__perl}|'

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
./Build test

%files
%doc Changes benchmarks/ example/ tool/ t/
%{perl_vendorarch}/auto/Mouse/
%{perl_vendorarch}/Mouse.pm
%{perl_vendorarch}/Mouse/
%{perl_vendorarch}/ouse.pm
%{perl_vendorarch}/Squirrel.pm
%{perl_vendorarch}/Squirrel/
%{_mandir}/man3/Mouse.3*
%{_mandir}/man3/Mouse::Exporter.3*
%{_mandir}/man3/Mouse::Meta::Attribute.3*
%{_mandir}/man3/Mouse::Meta::Class.3*
%{_mandir}/man3/Mouse::Meta::Method.3*
%{_mandir}/man3/Mouse::Meta::Method::Accessor.3*
%{_mandir}/man3/Mouse::Meta::Method::Constructor.3*
%{_mandir}/man3/Mouse::Meta::Method::Delegation.3*
%{_mandir}/man3/Mouse::Meta::Method::Destructor.3*
%{_mandir}/man3/Mouse::Meta::Module.3*
%{_mandir}/man3/Mouse::Meta::Role.3*
%{_mandir}/man3/Mouse::Meta::Role::Application.3*
%{_mandir}/man3/Mouse::Meta::Role::Composite.3*
%{_mandir}/man3/Mouse::Meta::Role::Method.3*
%{_mandir}/man3/Mouse::Meta::TypeConstraint.3*
%{_mandir}/man3/Mouse::Object.3*
%{_mandir}/man3/Mouse::PurePerl.3*
%{_mandir}/man3/Mouse::Role.3*
%{_mandir}/man3/Mouse::Spec.3*
%{_mandir}/man3/Mouse::Tiny.3*
%{_mandir}/man3/Mouse::TypeRegistry.3*
%{_mandir}/man3/Mouse::Util.3*
%{_mandir}/man3/Mouse::Util::MetaRole.3*
%{_mandir}/man3/Mouse::Util::TypeConstraints.3*
%{_mandir}/man3/Mouse::XS.3*
%{_mandir}/man3/ouse.3*
%{_mandir}/man3/Squirrel.3*
%{_mandir}/man3/Squirrel::Role.3*

%files -n perl-Test-Mouse
%{perl_vendorarch}/Test/
%{_mandir}/man3/Test::Mouse.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.11-4
- Perl 5.42 re-rebuild of bootstrapped packages

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.11-3
- Perl 5.42 rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Aug  4 2024 Paul Howarth <paul@city-fan.org> - 2.5.11-1
- Update to 2.5.11 (rhbz#2302715)
  - Use Devel-PPPort 3.59 (GH#113)
  - Mark "builtin" as foreign (GH#123)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.10-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.10-21
- Perl 5.40 re-rebuild of bootstrapped packages

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.10-20
- Perl 5.40 rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.10-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.10-16
- Perl 5.38 re-rebuild of bootstrapped packages

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.10-15
- Perl 5.38 rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.10-12
- Perl 5.36 re-rebuild of bootstrapped packages

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.10-11
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 28 2021 Paul Howarth <paul@city-fan.org> - 2.5.10-9
- Post EPEL-9 bootstrap rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.10-7
- Perl 5.34 re-rebuild of bootstrapped packages

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.10-6
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.10-3
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.10-2
- Perl 5.32 rebuild

* Sun Mar 29 2020 Emmanuel Seyman <emmanuel@seyman.fr> - 2.5.10-1
- Update to 2.5.10

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 18 2019 Paul Howarth <paul@city-fan.org> - 2.5.9-2
- Post EPEL-8 bootstrap rebuild

* Mon Aug 26 2019 Paul Howarth <paul@city-fan.org> - 2.5.9-1
- Update to 2.5.9
  - Fix segmentation fault that occurs when using MouseX::Foreign and
    role->apply at the same time (GH#100, GH#101)

* Tue Aug 13 2019 Paul Howarth <paul@city-fan.org> - 2.5.7-1
- Update to 2.5.7
  - Bump Module::Build::XSUtil prereq (GH#99)
  - Fix typo (GH#98)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.6-4
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.6-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 14 2018 aul Howarth <paul@city-fan.org> - 2.5.6-1
- Update to 2.5.6
  - Fix for threads and XS; use newSVpvs instead of newSVpvs_share (GH#92)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.4-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.5.4-2
- Perl 5.28 rebuild

* Sun May 06 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 2.5.4-1
- Update to 2.5.4

* Sun Feb 18 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 2.5.2-1
- Update to 2.5.2

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan  8 2018 Paul Howarth <paul@city-fan.org> - 2.5.1-1
- Update to 2.5.1
  - Use PERL_UNUSED_RESULT (GH#83)
  - Apply several minor patches, especially for packaging (GH#84)

* Mon Nov 27 2017 Paul Howarth <paul@city-fan.org> - 2.5.0-1
- Update to 2.5.0
  - Fix build under perl 5.8 (GH#63, GH#76, GH#79)
  - Use version->declare() to declare $VERSION (GH#55, GH#80)
  - Make 'prove -br t' work with dot-not-in-INC perls (GH#81)
- This release by SKAJI → update source URL

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Paul Howarth <paul@city-fan.org> - 2.4.10-1
- Update to 2.4.10
  - Support Moose-like oneliners (GH#51)
  - Various minor fixes (GH#58)
- This release by GFUJI → update source URL
- BR: perl-interpreter rather than perl
- Drop legacy Group: tags

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.9-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.9-2
- Perl 5.26 rebuild

* Wed Feb 22 2017 Paul Howarth <paul@city-fan.org> - 2.4.9-1
- Update to 2.4.9
  - Fix build issue on newer Perl without '.' in @INC

* Thu Feb 16 2017 Paul Howarth <paul@city-fan.org> - 2.4.8-1
- Update to 2.4.8
  - Fix stack collapse (GH#71)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 15 2017 Paul Howarth <paul@city-fan.org> - 2.4.7-1
- Update to 2.4.7
  - Workaround for GH#64 (GH#67); in some case stack is corrupted at more than
    23 attributes (this change may make things a bit slow in that case)

* Fri Jan  6 2017 Paul Howarth <paul@city-fan.org> - 2.4.6-1
- Update to 2.4.6
  - Fix test for older Perls (GH#68)
  - Define macros for older Visual Studio compiler (GH#66)
- Simplify find command using -empty and -delete

* Fri Sep 02 2016 Petr Pisar <ppisar@redhat.com> - 2.4.5-7
- Enable optional test with Data::Dump::Steamer (bug #1231204)

* Fri Jul 22 2016 Petr Pisar <ppisar@redhat.com> - 2.4.5-6
- Disable Data::Dumper::streamer everywhere

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.5-5
- Perl 5.24 re-rebuild of bootstrapped packages

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.5-4
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 01 2015 Petr Pisar <ppisar@redhat.com> - 2.4.5-2
- Break build cycle: perl-Mouse → perl-Pod-Coverage-Moose
  → perl-namespace-autoclean → perl-Mouse

* Sun Aug 16 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 2.4.5-1
- Update to 2.4.5
- Drop upstreamed patches

* Fri Jun 26 2015 Petr Pisar <ppisar@redhat.com> - 2.4.2-5
- Fix interaction with threads in perl-5.22 (bug #1235938)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.2-3
- Perl 5.22 rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.2-2
- Disable using of Data::Dump::Streamer with Perl 5.22

* Sun Apr 12 2015 Emmanuel Seyman <emmanuel@seyman.fr> - 2.4.2-1
- Update to 2.4.2

* Tue Oct  7 2014 Paul Howarth <paul@city-fan.org> - 2.4.1-1
- Update to 2.4.1
  - Merged the pull-request #13, which fixed an issue where the behavior of
    role method confliction was different from Moose; this change might affect
    your existing code so the major version has incremented (see
    t/030_roles/role_conflict_and_inheritance.t for details)
  - Dropped 5.6.2 support
  - Migrated to Minilla
  - Fixed #16 (Inconsistent coercion/validation of Bool type)
  - Fixed #17 (Memory leak in applying roles to instances)
- Classify buildreqs by usage
- Switch to Module::Build flow
- Make %%files list more explicit

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-3
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.13-1
- 1.13 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 16 2013 Iain Arnell <iarnell@gmail.com> 1.11-1
- update to latest upstream version

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1.06-2
- Perl 5.18 rebuild

* Fri Apr 19 2013 Iain Arnell <iarnell@gmail.com> 1.06-1
- update to latest upstream version

* Fri Feb 15 2013 Iain Arnell <iarnell@gmail.com> 1.05-1
- update to latest upstream version
- drop old tests sub-package obsoletes/provides

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Iain Arnell <iarnell@gmail.com> 1.04-1
- update to latest upstream version

* Fri Sep 07 2012 Iain Arnell <iarnell@gmail.com> 1.02-1
- update to latest upstream version

* Sun Aug 26 2012 Iain Arnell <iarnell@gmail.com> 1.01-1
- update to latest upstream version

* Sat Jul 21 2012 Iain Arnell <iarnell@gmail.com> 0.99-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.97-4
- Perl 5.16 rebuild

* Wed Apr 18 2012 Iain Arnell <iarnell@gmail.com> 0.97-3
- sub-package Test::Mouse (rhbz#813698)
- drop tests sub-package; move tests to main package documentation
- filter unversioned Mouse::Util from provides

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 15 2011 Iain Arnell <iarnell@gmail.com> 0.97-1
- update to latest upstream version

* Sun Oct 09 2011 Iain Arnell <iarnell@gmail.com> 0.95-1
- update to latest upstream version
- add virtual provides for perl-Any-Moose
- clean up some rpmlint warnings

* Thu Jul 21 2011 Iain Arnell <iarnell@gmail.com> 0.93-3
- Perl mass rebuild

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> 0.93-2
- Perl mass rebuild

* Sun Jun 26 2011 Iain Arnell <iarnell@gmail.com> 0.93-1
- update to latest upstream version

* Thu May 12 2011 Iain Arnell <iarnell@gmail.com> 0.92-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- additional BRs for improved test coverage

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.58-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 18 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.58-2
- bump

* Mon May 17 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.58-1
- include .proverc in tests subpackage
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.58)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.53-2
- Mass rebuild with perl-5.12.0 & update

* Fri Apr 16 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.53-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.53)
- altered br on perl(Devel::PPPort) (0 => 3.19)
- altered br on perl(ExtUtils::ParseXS) (0 => 2.21)
- altered br on perl(Test::Exception) (0 => 0.29)
- added a new br on perl(Test::Requires) (version 0.03)
- added manual BR on perl(Class::Method::Modifiers) (or override to 0)
- added manual BR on perl(Test::Deep) (or override to 0)
- added manual BR on perl(Test::Output) (or override to 0)
- added manual BR on perl(Path::Class) (or override to 0)
- added manual BR on perl(IO::File) (or override to 0)
- added manual BR on perl(IO::String) (or override to 0)

* Sun Feb 28 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.50-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.47-1
- add perl_default_filter
- we're no longer noarch
- auto-update to 0.47 (by cpan-spec-update 0.01)
- added a new br on perl(Devel::PPPort)
- added a new br on perl(ExtUtils::ParseXS)
- added a new br on perl(XSLoader) (version 0.1)
- added a new req on perl(Scalar::Util) (version 1.14)
- added a new req on perl(XSLoader) (version 0.1)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.35-2
- rebuild against perl 5.10.1

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.35-1
- update filtering
- drop our soft-requires (except 1).  Anything using Mouse by this point
  should know to require them if their bits are needed.
- add benchmarks/ to doc
- auto-update to 0.35 (by cpan-spec-update 0.01)
- altered br on perl(Test::Exception) (0.21 => 0.27)
- altered br on perl(Test::More) (0.8 => 0.88)

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.28-1
- auto-update to 0.28 (by cpan-spec-update 0.01)

* Fri Jul 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.27-1
- auto-update to 0.27 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.25-1
- auto-update to 0.25 (by cpan-spec-update 0.01)
- altered req on perl(Scalar::Util) (1.19 => 1.14)

* Tue Jun 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.23-1
- auto-update to 0.23 (by cpan-spec-update 0.01)
- altered br on perl(Test::Exception) (0 => 0.21)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- altered br on perl(Test::More) (0 => 0.8)

* Sun May 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.22-1
- update to 0.22

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.19-1
- update to 0.19

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- update to 0.17

* Tue Feb 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.16-1
- update to 0.16

* Tue Dec 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.14-1
- update to 0.14

* Tue Dec 16 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- update to 0.13

* Mon Oct 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-2
- bump

* Wed Oct 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- update to 0.09
- add manual requires on the "soft" dependencies

* Mon Sep 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.06-2
- update description a touch.

* Sat Sep 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.06-1
- initial Fedora packaging
- generated with cpan2dist (CPANPLUS::Dist::Fedora version 0.0.1)
