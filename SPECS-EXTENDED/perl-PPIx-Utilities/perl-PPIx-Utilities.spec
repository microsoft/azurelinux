# Run extra test
%if ! (0%{?rhel})
%bcond_without perl_PPIx_Utilities_enables_extra_test
%else
%bcond_with perl_PPIx_Utilities_enables_extra_test
%endif

Name:		perl-PPIx-Utilities
Version:	1.001000
Release:	37%{?dist}
Summary:	Extensions to PPI
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/PPIx-Utilities
Source0:	https://cpan.metacpan.org/authors/id/E/EL/ELLIOTJS/PPIx-Utilities-%{version}.tar.gz#/perl-PPIx-Utilities-%{version}.tar.gz
BuildArch:	noarch
# Build:
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	sed
# Run-time:
BuildRequires:	perl(base)
BuildRequires:	perl(Exception::Class)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(PPI) >= 1.208
BuildRequires:	perl(PPI::Document::Fragment) >= 1.208
BuildRequires:	perl(Readonly)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Tests:
BuildRequires:	perl(Data::Dumper)
BuildRequires:	perl(PPI::Document) >= 1.208
BuildRequires:	perl(PPI::Dumper) >= 1.208
BuildRequires:	perl(Task::Weaken)
BuildRequires:	perl(Test::Deep)
BuildRequires:	perl(Test::More)
# Extra tests:
# PPI needed by Perl::Critic, so don't run extra tests when bootstrapping
%if 0%{!?perl_bootstrap:1} && %{with perl_PPIx_Utilities_enables_extra_test}
BuildRequires:	aspell-en
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Slurp)
BuildRequires:	perl(Perl::Critic::Policy::Miscellanea::RequireRcsKeywords)
BuildRequires:	perl(Test::Perl::Critic)
BuildRequires:	perl(Test::Distribution)
BuildRequires:	perl(Test::Kwalitee)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
%endif
# Run-time:
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This is a collection of functions for dealing with PPI objects, many of
which originated in Perl::Critic. They are organized into modules by the
kind of PPI class they relate to, by replacing the "PPI" at the front of
the module name with "PPIx::Utilities", e.g. functionality related to
PPI::Nodes is in PPIx::Utilities::Node.

%prep
%setup -q -n PPIx-Utilities-%{version}

# Remove date-sensitive copyright.t, which also upsets Perl::Critic
# (#1139503)
rm xt/author/copyright.t
sed -i -e '/copyright\.t/d' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test
%if 0%{!?perl_bootstrap:1} && %{with perl_PPIx_Utilities_enables_extra_test}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%endif

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes README
%{perl_vendorlib}/PPIx/
%{_mandir}/man3/PPIx::Utilities.3*
%{_mandir}/man3/PPIx::Utilities::Exception::Bug.3*
%{_mandir}/man3/PPIx::Utilities::Node.3*
%{_mandir}/man3/PPIx::Utilities::Statement.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.001000-37
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.001000-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep  5 2019 Paul Howarth <paul@city-fan.org> - 1.001000-35
- Specify all build requirements
- Don't assume manpages have ".3pm" extension
- Simplify find command using -delete

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.001000-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.001000-33
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 1.001000-32
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.001000-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.001000-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.001000-29
- Perl 5.28 re-rebuild of bootstrapped packages

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.001000-28
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.001000-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.001000-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.001000-25
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 1.001000-24
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.001000-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.001000-22
- Perl 5.24 re-rebuild of bootstrapped packages

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.001000-21
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.001000-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001000-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.001000-18
- Perl 5.22 re-rebuild of bootstrapped packages

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.001000-17
- Perl 5.22 rebuild

* Tue Sep  9 2014 Paul Howarth <paul@city-fan.org> - 1.001000-16
- Avoid copyright.t more forcefully, as it is now upsetting Perl::Critic too
- Use %%license where possible

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.001000-15
- Perl 5.20 re-rebuild of bootstrapped packages

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.001000-14
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001000-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.001000-12
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001000-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 29 2013 Petr Pisar <ppisar@redhat.com> - 1.001000-10
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001000-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 26 2012 Paul Howarth <paul@city-fan.org> - 1.001000-8
- Drop redundant %%perl_default_filter
- Run extra tests (and include necessary buildreqs) except when bootstrapping

* Thu Oct 25 2012 Petr Pisar <ppisar@redhat.com> - 1.001000-7
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001000-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 1.001000-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.001000-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.001000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Paul Howarth <paul@city-fan.org> - 1.001000-1
- Update to 1.001000
  - Add support for Const::Fast to PPIx::Utilities::Statement

* Thu Jul 29 2010 Paul Howarth <paul@city-fan.org> - 1.000001-2
- Re-jig for Fedora submission

* Wed Jun 23 2010 Paul Howarth <paul@city-fan.org> - 1.000001-1
- Initial RPM version
