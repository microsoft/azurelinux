# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Params_ValidationCompiler_enables_optional_test
%else
%bcond_with perl_Params_ValidationCompiler_enables_optional_test
%endif

Name:		perl-Params-ValidationCompiler
Version:	0.31
Release:	6%{?dist}
Summary:	Build an optimized subroutine parameter validator once, use it forever
License:	Artistic-2.0
URL:		https://metacpan.org/release/Params-ValidationCompiler
Source0:	https://cpan.metacpan.org/modules/by-module/Params/Params-ValidationCompiler-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) > 6.75
# Module
BuildRequires:	perl(B)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Class::XSAccessor) >= 1.17
BuildRequires:	perl(Eval::Closure)
BuildRequires:	perl(Exception::Class)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(List::Util) >= 1.29
BuildRequires:	perl(overload)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Optional Functionality
BuildRequires:	perl(Sub::Util) >= 1.40
# Test Suite
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(Specio) >= 0.14
BuildRequires:	perl(Specio::Declare)
BuildRequires:	perl(Specio::Library::Builtins)
BuildRequires:	perl(Test2::Plugin::NoWarnings)
BuildRequires:	perl(Test2::Require::Module)
BuildRequires:	perl(Test2::V0)
BuildRequires:	perl(Test::More) >= 1.302015
BuildRequires:	perl(Test::Without::Module)
%if %{with perl_Params_ValidationCompiler_enables_optional_test}
# Optional Tests
BuildRequires:	perl(Const::Fast)
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Prereqs)
BuildRequires:	perl(Hash::Util)
%if !%{defined perl_bootstrap}
# Avoid build dependency cycles via Moose and DateTime
BuildRequires:	perl(Moose::Util::TypeConstraints)
BuildRequires:	perl(Types::Standard)
%endif
%endif
# Dependencies
Recommends:	perl(Class::XSAccessor) >= 1.17
Recommends:	perl(Sub::Util) >= 1.40

%description
Create a customized, optimized, non-lobotomized, uncompromised, and thoroughly
specialized parameter checking subroutine.

%prep
%setup -q -n Params-ValidationCompiler-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PERLLOCAL=1 NO_PACKLIST=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license LICENSE
%doc Changes CODE_OF_CONDUCT.md CONTRIBUTING.md eg/ README.md
%{perl_vendorlib}/Params/
%{_mandir}/man3/Params::ValidationCompiler.3*
%{_mandir}/man3/Params::ValidationCompiler::Compiler.3*
%{_mandir}/man3/Params::ValidationCompiler::Exceptions.3*

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan  8 2023 Paul Howarth <paul@city-fan.org> - 0.31-1
- Update to 0.31
  - Require Class::XSAccessor 1.17+ when trying to load it; earlier versions
    cause test failures (GH#27)
- Use SPDX-format license tag

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-16
- Perl 5.36 re-rebuild of bootstrapped packages

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-15
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-12
- Perl 5.34 re-rebuild of bootstrapped packages

* Sat May 22 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-11
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-8
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-7
- Perl 5.32 rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-4
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.30-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug  1 2018 Paul Howarth <paul@city-fan.org> - 0.30-1
- Update to 0.30
  - Added a new option for named params, "return_object", which causes the
    validation sub to return an object with methods for each param rather than
    a hashref; this is a great way to avoid typos in hash keys (idea
    shamelessly stolen from Toby Inkster's Type::Params module)
  - Tweaked the POD formatting so that the table of contents generated by
    MetaCPAN is more useful
  - Optionally use Class::XSAccessor

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-3
- Perl 5.28 re-rebuild of bootstrapped packages

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.27-2
- Perl 5.28 rebuild

* Mon Feb 12 2018 Paul Howarth <paul@city-fan.org> - 0.27-1
- Update to 0.27
  - Fixed a bug with inlining Moose types: if a type's parent needed
    environment variables, those would not get closed over (GH#22)
  - Added a debug option to dump the source of the subroutine before it is
    eval'd

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 28 2017 Paul Howarth <paul@city-fan.org> - 0.26-1
- Update to 0.26
  - The exceptions.t test would fail if Sub::Util was not installed (GH#19)
  - Fix test failures on Windows (GH#20)

* Fri Nov 24 2017 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25
  - All exceptions now include a stack trace by default when treated as a
    string; this makes finding where validation failed a lot easier (GH#18)
  - The name for a subroutine is now used in some exception messages, even if
    Sub::Util cannot be installed

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-2
- Perl 5.26 rebuild

* Sun Apr  9 2017 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24
  - The source_for() exported by Params::ValidationCompiler did not work at all
    (GH#16)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Paul Howarth <paul@city-fan.org> - 0.23-1
- Update to 0.23
  - Trying to create a validator for positional parameters where a required
    param came after one with a default did not throw an exception
  - A positional params validator with a slurpy type that had coercions did not
    return the coerced values; it returned the original values instead

* Sat Dec 31 2016 Paul Howarth <paul@city-fan.org> - 0.22-1
- Update to 0.22
  - Explicitly load the B module; previously, the code relied on this already
    being loaded by something else (GH#11)
  - Removed the alpha warning from the docs

* Wed Dec  7 2016 Paul Howarth <paul@city-fan.org> - 0.21-1
- Update to 0.21
  - Switched to using GitHub issues

* Tue Dec  6 2016 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20
  - The keys for parameter specifications are now validated, and if an unknown
    key is seen then an exception will be thrown; this will help you catch
    typos in your parameter specification (GH#8)

* Tue Nov 22 2016 Paul Howarth <paul@city-fan.org> - 0.19-1
- Update to 0.19
  - Non-inlinable Specio types caused a syntax error when used with positional
    params
  - Positional params with coercions and defaults did not work properly; the
    coerced value and the default would simply not be returned in any case

* Mon Nov 14 2016 Paul Howarth <paul@city-fan.org> - 0.18-1
- Update to 0.18
  - Using coercions with positional parameters could cause a "Modification of a
    read-only value attempted" exception when the generated code tried to
    assign to elements of @_; this is now fixed by making a copy if any of the
    types have a coercion
  - Using Moose types with coercions in a positional params check would cause
    invalid code to be generated; this could also happen with Type::Tiny if
    either the type or a coercion could not be inlined

* Mon Nov  7 2016 Paul Howarth <paul@city-fan.org> - 0.17-1
- Update to 0.17
  - When using positional parameters, parameters with a default are now
    optional; for named parameters, this was already the case

* Fri Nov  4 2016 Paul Howarth <paul@city-fan.org> - 0.16-1
- Update to 0.16
  - Previously, using a default with a positional parameter would result in an
    error when compiling the validator subroutine; defaults now work with
    positional parameters (GH#5)
  - Moose and Specio types (and coercions) that provide variables to close over
    when being inlined did not always compile properly; most notably, this was
    not being handled at all for Moose types, and not completely handled for
    Specio coercions

* Thu Nov  3 2016 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Added a "named_to_list" option to support returning only the parameter
    values from a named parameter validator rather than the key-value pairs
    (GH#4)
  - Errors from calls to validation_for() now use croak so as to show up at the
    call site, rather than in the internals

* Wed Oct 26 2016 Petr Pisar <ppisar@redhat.com> - 0.13-4
- Break build cycle: perl-Moose → perl-DateTime → perl-Params-ValidationCompiler

* Mon Sep 19 2016 Paul Howarth <paul@city-fan.org> - 0.13-3
- Drop unused BR: findutils (#1377252)

* Mon Sep 19 2016 Paul Howarth <paul@city-fan.org> - 0.13-2
- Sanitize for Fedora submission

* Sun Sep 18 2016 Paul Howarth <paul@city-fan.org> - 0.13-1
- Initial RPM version
