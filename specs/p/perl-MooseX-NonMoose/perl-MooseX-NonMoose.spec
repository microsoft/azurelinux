# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Run extra test
%if ! (0%{?rhel})
%bcond_without perl_MooseX_NonMoose_enables_extra_test
%else
%bcond_with perl_MooseX_NonMoose_enables_extra_test
%endif

Name:           perl-MooseX-NonMoose
Version:        0.27
Release:        3%{?dist}
Summary:        Easy subclassing of non-Moose classes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/MooseX-NonMoose
Source0:        https://cpan.metacpan.org/modules/by-module/MooseX/MooseX-NonMoose-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(List::Util) >= 1.33
BuildRequires:  perl(Module::Runtime)
BuildRequires:  perl(Moose::Exporter)
BuildRequires:  perl(Moose::Role) >= 2.0000
BuildRequires:  perl(Moose::Util)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Try::Tiny)
# Test
BuildRequires:  perl(base)
BuildRequires:  perl(Config)
BuildRequires:  perl(Moose)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::Moose)
BuildRequires:  perl(Test::More) >= 0.98
BuildRequires:  perl(Test2::Require::Module) >= 0.000121
# Optional tests
%if %{with perl_MooseX_NonMoose_enables_extra_test}
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(MooseX::GlobRef)
BuildRequires:  perl(MooseX::InsideOut) >= 0.100
%endif
# Dependencies
# (none)

%description
MooseX::NonMoose allows for easily subclassing non-Moose classes with
Moose, taking care of the annoying details connected with doing this, such
as setting up proper inheritance from Moose::Object and installing (and
inlining, at make_immutable time) a constructor that makes sure things like
BUILD methods are called. It tries to be as non-intrusive as possible -
when this module is used, inheriting from non-Moose classes and inheriting
from Moose classes should work identically, aside from the few caveats
mentioned below. One of the goals of this module is that including it in a
Moose::Exporter-based package used across an entire application should be
possible, without interfering with classes that only inherit from Moose
modules, or even classes that don't inherit from anything at all.

%prep
%setup -q -n MooseX-NonMoose-%{version}

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
%doc Changes README
%{perl_vendorlib}/MooseX/
%{_mandir}/man3/MooseX::NonMoose.3*
%{_mandir}/man3/MooseX::NonMoose::InsideOut.3*
%{_mandir}/man3/MooseX::NonMoose::Meta::Role::Class.3*
%{_mandir}/man3/MooseX::NonMoose::Meta::Role::Constructor.3*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan  3 2025 Paul Howarth <paul@city-fan.org> - 0.27-1
- Update to 0.27 (rhbz#2335385)
- Use %%{make_build} and %%{make_install}

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-24
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 23 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-21
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-18
- Perl 5.32 rebuild

* Tue Mar 10 2020 Paul Howarth <paul@city-fan.org> - 0.26-17
- BR: perl(blib) for t/00-compile.t

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-14
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-11
- Perl 5.28 rebuild

* Tue Apr 17 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-10
- Specify all dependencies; Modernize spec file

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-7
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.26-2
- Perl 5.22 rebuild

* Tue Nov 11 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.26-1
- Update to 0.26
- Use the %%license tag

* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-9
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.22-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 0.22-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.22-2
- Perl mass rebuild

* Thu May 12 2011 Iain Arnell <iarnell@gmail.com> 0.22-1
- update to latest upstream version

* Wed May 04 2011 Iain Arnell <iarnell@gmail.com> 0.21-1
- update to latest upstream version

* Wed Mar 23 2011 Iain Arnell <iarnell@gmail.com> 0.20-1
- update to latest upstream version

* Fri Mar 04 2011 Iain Arnell <iarnell@gmail.com> 0.19-1
- update to latest upstream version

* Wed Feb 16 2011 Iain Arnell <iarnell@gmail.com> 0.18-1
- update to latest upstream version
- BR perl(MooseX::GlobRef) for additional test coverage

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 19 2010 Iain Arnell <iarnell@gmail.com> 0.17-1
- update to latest upstream version

* Wed Nov 03 2010 Iain Arnell <iarnell@gmail.com> 0.16-2
- requires Moose >= 1.15

* Wed Oct 27 2010 Iain Arnell <iarnell@gmail.com> 0.16-1
- update to latest upstream version

* Tue Oct 05 2010 Iain Arnell <iarnell@gmail.com> 0.15-1
- Specfile autogenerated by cpanspec 1.78.
