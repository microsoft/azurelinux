# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Specio_enables_optional_test
%else
%bcond_with perl_Specio_enables_optional_test
%endif

Name:		perl-Specio
Version:	0.48
Release:	7%{?dist}
Summary:	Type constraints and coercions for Perl
# lib/Specio/PartialDump.pm:	GPL-1.0-or-later OR Artistic-1.0-Perl
#				<https://github.com/houseabsolute/Specio/issues/17>
# other files:			Artistic-2.0
License:	Artistic-2.0 AND (GPL-1.0-or-later OR Artistic-1.0-Perl)
URL:		https://metacpan.org/release/Specio
Source0:	https://cpan.metacpan.org/modules/by-module/Test/Specio-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker) >= 6.76
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Devel::StackTrace)
BuildRequires:	perl(Eval::Closure)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(List::Util) >= 1.33
BuildRequires:	perl(Module::Runtime)
BuildRequires:	perl(MRO::Compat)
BuildRequires:	perl(overload)
BuildRequires:	perl(parent)
BuildRequires:	perl(re)
BuildRequires:	perl(Ref::Util) >= 0.112
BuildRequires:	perl(Role::Tiny) >= 1.003003
BuildRequires:	perl(Role::Tiny::With)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Storable)
BuildRequires:	perl(strict)
BuildRequires:	perl(Sub::Quote)
BuildRequires:	perl(Sub::Util) >= 1.40
BuildRequires:	perl(Test::Fatal)
BuildRequires:	perl(Test::More) >= 0.96
BuildRequires:	perl(Try::Tiny)
BuildRequires:	perl(version) >= 0.83
BuildRequires:	perl(warnings)
BuildRequires:	perl(XString)
# Test Suite
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(FindBin)
BuildRequires:	perl(lib)
BuildRequires:	perl(open)
BuildRequires:	perl(Test::Needs)
BuildRequires:	perl(utf8)
%if %{with perl_Specio_enables_optional_test}
# Optional Tests
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(CPAN::Meta::Prereqs)
BuildRequires:	perl(Moo)
%if !%{defined perl_bootstrap}
# Break cycle: perl-Moose → perl-DateTime → perl-Specio
BuildRequires:	perl(Moose) >= 2.1207
# Break cycle: perl-Mouse → perl-Moose → perl-DateTime → perl-Specio
BuildRequires:	perl(Mouse)
%endif
BuildRequires:	perl(namespace::autoclean)
%endif
# Dependencies
Requires:	perl(Ref::Util) >= 0.112
Requires:	perl(Sub::Util) >= 1.40
Requires:	perl(XString)

# Avoid provides for private packages
%global __provides_exclude ^perl\\(_T::.*\\)

%description
The Specio distribution provides classes for representing type constraints
and coercion, along with syntax sugar for declaring them.

Note that this is not a proper type system for Perl. Nothing in this
distribution will magically make the Perl interpreter start checking a value's
type on assignment to a variable. In fact, there's no built-in way to apply a
type to a variable at all.

Instead, you can explicitly check a value against a type, and optionally coerce
values to that type.

%package -n perl-Test-Specio
Summary:	Test helpers for Specio
License:	Artistic-2.0
Requires:	%{name} = %{version}-%{release}

%description -n perl-Test-Specio
This package provides some helper functions and variables for testing Specio
types.

%prep
%setup -q -n Specio-%{version}

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
%doc Changes CODE_OF_CONDUCT.md CONTRIBUTING.md README.md TODO.md
%{perl_vendorlib}/Specio.pm
%{perl_vendorlib}/Specio/
%{_mandir}/man3/Specio.3*
%{_mandir}/man3/Specio::Coercion.3*
%{_mandir}/man3/Specio::Constraint::AnyCan.3*
%{_mandir}/man3/Specio::Constraint::AnyDoes.3*
%{_mandir}/man3/Specio::Constraint::AnyIsa.3*
%{_mandir}/man3/Specio::Constraint::Enum.3*
%{_mandir}/man3/Specio::Constraint::Intersection.3*
%{_mandir}/man3/Specio::Constraint::ObjectCan.3*
%{_mandir}/man3/Specio::Constraint::ObjectDoes.3*
%{_mandir}/man3/Specio::Constraint::ObjectIsa.3*
%{_mandir}/man3/Specio::Constraint::Parameterizable.3*
%{_mandir}/man3/Specio::Constraint::Parameterized.3*
%{_mandir}/man3/Specio::Constraint::Role::CanType.3*
%{_mandir}/man3/Specio::Constraint::Role::DoesType.3*
%{_mandir}/man3/Specio::Constraint::Role::Interface.3*
%{_mandir}/man3/Specio::Constraint::Role::IsaType.3*
%{_mandir}/man3/Specio::Constraint::Simple.3*
%{_mandir}/man3/Specio::Constraint::Structurable.3*
%{_mandir}/man3/Specio::Constraint::Structured.3*
%{_mandir}/man3/Specio::Constraint::Union.3*
%{_mandir}/man3/Specio::Declare.3*
%{_mandir}/man3/Specio::DeclaredAt.3*
%{_mandir}/man3/Specio::Exception.3*
%{_mandir}/man3/Specio::Exporter.3*
%{_mandir}/man3/Specio::Helpers.3*
%{_mandir}/man3/Specio::Library::Builtins.3*
%{_mandir}/man3/Specio::Library::Numeric.3*
%{_mandir}/man3/Specio::Library::Perl.3*
%{_mandir}/man3/Specio::Library::String.3*
%{_mandir}/man3/Specio::Library::Structured.3*
%{_mandir}/man3/Specio::Library::Structured::Dict.3*
%{_mandir}/man3/Specio::Library::Structured::Map.3*
%{_mandir}/man3/Specio::Library::Structured::Tuple.3*
%{_mandir}/man3/Specio::OO.3*
%{_mandir}/man3/Specio::PartialDump.3*
%{_mandir}/man3/Specio::Registry.3*
%{_mandir}/man3/Specio::Role::Inlinable.3*
%{_mandir}/man3/Specio::Subs.3*
%{_mandir}/man3/Specio::TypeChecks.3*

%files -n perl-Test-Specio
%{perl_vendorlib}/Test/
%{_mandir}/man3/Test::Specio.3*

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jun 12 2022 Paul Howarth <paul@city-fan.org> - 0.48-1
- Update to 0.48
  - Importing types into a class that inherited from another class that had
    imported types wouldn't work, leaving the child class with no 't()' sub

* Fri Jun 03 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.47-7
- Perl 5.36 re-rebuild of bootstrapped packages

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.47-6
- Perl 5.36 rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 24 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.47-3
- Perl 5.34 re-rebuild of bootstrapped packages

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.47-2
- Perl 5.34 rebuild

* Sun Jan 31 2021 Paul Howarth <paul@city-fan.org> - 0.47-1
- Update to 0.47
  - Change Specio constraint object's stringification overloading to return the
    type name rather than the default Perl object stringification, which gives
    you something like
    "Specio::Constraint::Parameterized=HASH(0x564d258efb48)"; anonymous types
    are special cased to return something you can print
  - All types now overload the 'eq' comparison operator: Moose expects types to
    be comparable in this manner when doing role summation (GH#18)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.46-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-3
- Perl 5.32 re-rebuild of bootstrapped packages

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.46-2
- Perl 5.32 rebuild

* Sat Mar 14 2020 Paul Howarth <paul@city-fan.org> - 0.46-1
- Update to 0.46
  - Correct license of Specio::PartialDump (GH#17)

* Tue Feb 18 2020 Petr Pisar <ppisar@redhat.com> - 0.45-3
- Correct a perl-Specio license to "Artistic 2.0 and (GPL+ or Artistic)"

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Paul Howarth <paul@city-fan.org> - 0.45-1
- Update to 0.45
  - Made XString a prereq if installing with Perl 5.10+

* Thu Aug 15 2019 Paul Howarth <paul@city-fan.org> - 0.44-1
- Update to 0.44
  - Replaced the use of B with XString if it is installed; the latter is much
    smaller and provides the one subroutine from B we cared about (based on
    GH#15)
- Use %%{make_build} and %%{make_install}

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 02 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-4
- Perl 5.30 re-rebuild of bootstrapped packages

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.43-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 28 2018 Paul Howarth <paul@city-fan.org> - 0.43-1
- Update to 0.43
  - Optimized compile-time operations to make Specio itself quicker to load;
    Specio's load time is a non-trivial part of the load time of DateTime (and
    presumably other things that use it)
  - Based on https://github.com/houseabsolute/DateTime.pm/issues/85
- Package new CODE_OF_CONDUCT.md file

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-4
- Perl 5.28 re-rebuild of bootstrapped packages

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.42-3
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov  6 2017 Paul Howarth <paul@city-fan.org> - 0.42-1
- Update to 0.42
  - Fixed checks for whether a class is loaded in light of upcoming
    optimization in Perl 5.28 (GH#12)
  - The Perl library claimed it provided types named LaxVersionStr and
    StrictVersionStr but they were really named LaxVersion and StrictVersion;
    the names have now been fixed to match the documentation, so they are
    LaxVersionStr and StrictVersionStr

* Fri Aug  4 2017 Paul Howarth <paul@city-fan.org> - 0.40-1
- Update to 0.40
  - Fixed more bugs with {any,object}_{can,does,isa}_type
    - When passed a glob (not a globref) they would die in their type check
    - On Perl 5.16 or earlier, passing a number to an any_* type would also die
  - Fixed subification overloading: if Sub::Quote was loaded, this would be
    used, but any environment variables needed for the closure would not be
    included, which broke enums, among other things

* Thu Aug  3 2017 Paul Howarth <paul@city-fan.org> - 0.39-1
- Update to 0.39
  - Many bug fixes and improvements to the types created by
    {any,object}_{can,does,isa}_type; in some cases, an invalid value could
    cause an exception in type check itself, and in other cases, a value that
    failed a type check would cause an exception when generating a message
    describing the failure
  - The messages describing a failure for all of these types have been improved
  - You can now create anonymous *_does and *_isa types using the exports from
    Specio::Declare

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul  1 2017 Paul Howarth <paul@city-fan.org> - 0.38-1
- Update to 0.38
  - Simplify checks for overloading to not call overload::Overloaded(); just
    checking the return value of overload::Method() is sufficient

* Wed Jun 07 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-3
- Perl 5.26 re-rebuild of bootstrapped packages

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.37-2
- Perl 5.26 rebuild

* Tue May  9 2017 Paul Howarth <paul@city-fan.org> - 0.37-1
- Update to 0.37
  - Possible fix for very weird failures seen under threaded Perls with some
    modules that use Specio

* Mon Feb 20 2017 Paul Howarth <paul@city-fan.org> - 0.36-1
- Update to 0.36
  - Inlined coercions would attempt to coerce for every type that matched the
    value given, instead of stopping after the first type (GH#11)
  - Inlined coercions did not include the inline environment variables needed
    by the type from which the coercion was being performed (GH#8)
  - When you use the same type repeatedly as coderef (for example, as a
    constraint with Moo), it will only generate its subified form once, rather
    than regenerating it each time it is de-referenced
  - Added an API to Specio::Subs to allow you to combine type libraries and
    helper subs in one package for exporting; see the Specio::Exporter docs for
    more detail

* Mon Feb 13 2017 Paul Howarth <paul@city-fan.org> - 0.35-1
- Update to 0.35
  - Added Specio::Subs, a module that allows you to turn one or more library's
    types into subroutines like is_Int() and to_Int()
  - Added an inline_coercion method to Specio constraints

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 30 2017 Paul Howarth <paul@city-fan.org> - 0.34-1
- Update to 0.34
  - Packages with Specio::Exporter can now specify additional arbitrary subs to
    exporter; see the Specio::Exporter docs for details
  - Importing the same library twice in a given package would throw an
    exception; the second attempt to import is now ignored

* Wed Jan 25 2017 Paul Howarth <paul@city-fan.org> - 0.33-1
- Update to 0.33
  - Fixed a mistake in the SYNOPSIS for Specio::Declare; the example for the
    *_isa_type helpers was not correct
  - Removed the alpha warning from the docs; this is being used by enough of my
    modules on CPAN that I don't plan on doing any big breaking changes without
    a deprecation first

* Fri Jan 13 2017 Paul Howarth <paul@city-fan.org> - 0.32-1
- Update to 0.32
  - Fixed a bug in the inlining for types create by any_can_type() and
    object_can_type(); this inlining mostly worked by accident because of some
    List::Util XS magic, but this broke under the debugger (GH#6,
    https://github.com/houseabsolute/DateTime.pm/issues/49)

* Mon Nov  7 2016 Paul Howarth <paul@city-fan.org> - 0.31-1
- Update to 0.31
  - The stack trace contained by Specio::Exception objects no longer includes
    stack frames for the Specio::Exception package
  - Made the inline_environment() and description() methods public on type and
    coercion objects

* Thu Oct 20 2016 Petr Pisar <ppisar@redhat.com> - 0.30-2
- Break build cycle: perl-Moose → perl-DateTime → perl-Specio

* Sun Oct 16 2016 Paul Howarth <paul@city-fan.org> - 0.30-1
- Update to 0.30
  - Fix a bug with the Sub::Quoted sub returned by $type->coercion_sub; if a
    type had more than one coercion, the generated sub could end up coercing
    the value to undef some of the time and, depending on hash key ordering,
    this could end up being a heisenbug that only occurred some of the time

* Mon Oct 10 2016 Paul Howarth <paul@city-fan.org> - 0.29-1
- Update to 0.29
  - Document Specio::PartialDump because you may want to use it as part of the
    failure message generation code for a type

* Mon Oct  3 2016 Paul Howarth <paul@city-fan.org> - 0.28-1
- Update to 0.28
  - Added a Test::Specio module to provide helpers for testing Specio libraries
  - Fixed another bug with a subtype of special types and inlining
- Introduce sub-package perl-Test-Specio to avoid dependencies on Test::Fatal
  and Test::More in main package

* Sun Oct  2 2016 Paul Howarth <paul@city-fan.org> - 0.27-1
- Update to 0.27
  - Cloning a type with coercions defined on it would cause an exception
  - Creating a subtype of a special type created by *_isa_type, *_can_type, or
    *_does_type, or enum would die when trying to inline type constraint
  - Removed the never-documented Any type
  - Added documentation for each type in Specio::Library::Builtins

* Mon Sep 26 2016 Paul Howarth <paul@city-fan.org> - 0.26-1
- Update to 0.26
  - Require Role::Tiny 1.003003, which should fix some test failures

* Mon Sep  5 2016 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25
  - Calling {any,object}_{isa,does}_type repeatedly in a package with the same
    class or role name would die; these subs are now special-cased to simply
    return an existing type for the given name when they receive a single
    argument (the name of the class or role)

* Fri Jul  1 2016 Paul Howarth <paul@city-fan.org> - 0.24-2
- Sanitize for Fedora submission

* Fri Jul  1 2016 Paul Howarth <paul@city-fan.org> - 0.24-1
- Initial RPM version
