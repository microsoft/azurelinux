# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Eval_Closure_enables_optional_test
%else
%bcond_with perl_Eval_Closure_enables_optional_test
%endif

Name:           perl-Eval-Closure
Version:        0.14
Release:        12%{?dist}
Summary:        Safely and cleanly create closures via string eval
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Eval-Closure
Source0:        https://cpan.metacpan.org/authors/id/D/DO/DOY/Eval-Closure-%{version}.tar.gz#/perl-Eval-Closure-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
# Module Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Devel::LexAlias) >= 0.05
BuildRequires:  perl(Exporter)
BuildRequires:  perl(overload)
BuildRequires:  perl(Perl::Tidy)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(strict)
# Test Suite
BuildRequires:  perl(B)
BuildRequires:  perl(blib)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(PadWalker)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Requires)
BuildRequires:  perl(warnings)
%if %{with perl_Eval_Closure_enables_optional_test}
# Optional Tests
BuildRequires:  perl(Test::Output)
%endif
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Devel::LexAlias) >= 0.05
Requires:       perl(Perl::Tidy)

%description
String eval is often used for dynamic code generation. For instance, Moose uses
it heavily, to generate inlined versions of accessors and constructors, which
speeds code up at runtime by a significant amount. String eval is not without
its issues however - it's difficult to control the scope it's used in (which
determines which variables are in scope inside the eval), and it can be quite
slow, especially if doing a large number of evals.
 
This module attempts to solve both of those problems. It provides an
eval_closure function, which evals a string in a clean environment, other than
a fixed list of specified variables. It also caches the result of the eval, so
that doing repeated evals of the same source, even with a different
environment, will be much faster (but note that the description is part of the
string to be evaled, so it must also be the same (or non-existent) if caching
is to work properly).

%prep
%setup -q -n Eval-Closure-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Eval/
%{_mandir}/man3/Eval::Closure.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-9
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.14-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 29 2016 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - A couple of minor optimizations (GH#8)
- BR: perl-generators
- Simplify find command using -delete

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-2
- Perl 5.22 rebuild

* Tue May 12 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.13-1
- Update to 0.13
  - Fix tests under blead (GH#6)

* Mon Jan 19 2015 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - Fix tests under blead (GH#4)

* Wed Nov 12 2014 Paul Howarth <paul@city-fan.org> - 0.11-1
- Update to 0.11
  - Support lexical subs on 5.18+
  - Fix pod links
  - Add "alias => 1" option for making closure variables actually alias the
    closed over variables (so the variable referenced in the environment
    hashref will actually be updated by changes made in the closure)
- Classify buildreqs by usage
- Use %%license
- Make %%files list more explicit
- Update %%description
- Don't need to remove empty directories from the buildroot

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.08-8
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.08-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.08-2
- Perl 5.16 rebuild

* Fri Feb 10 2012 Iain Arnell <iarnell@gmail.com> 0.08-1
- update to latest upstream version

* Sat Feb 04 2012 Iain Arnell <iarnell@gmail.com> 0.07-1
- update to latest upstream version
- update description

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-2
- Perl mass rebuild

* Tue Jun 07 2011 Iain Arnell <iarnell@gmail.com> 0.06-1
- update to latest upstream version

* Wed May 04 2011 Iain Arnell <iarnell@gmail.com> 0.05-1
- update to latest upstream version

* Wed Apr 20 2011 Iain Arnell <iarnell@gmail.com> 0.04-1
- update to latest upstream version

* Thu Mar 03 2011 Iain Arnell <iarnell@gmail.com> 0.03-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Iain Arnell <iarnell@gmail.com> 0.02-1
- update to latest upstream version

* Sun Jan 23 2011 Iain Arnell <iarnell@gmail.com> 0.01-1
- Specfile autogenerated by cpanspec 1.78.
