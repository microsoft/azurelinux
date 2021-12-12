# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Params_Classify_enables_optional_test
%else
%bcond_with perl_Params_Classify_enables_optional_test
%endif

Name:           perl-Params-Classify
Version:        0.015
Release:        10%{?dist}
Summary:        Argument type classification
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://metacpan.org/release/Params-Classify
Source0:        https://cpan.metacpan.org/authors/id/Z/ZE/ZEFRAM/Params-Classify-%{version}.tar.gz#/perl-Params-Classify-%{version}.tar.gz
# Module Build
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::CBuilder) >= 0.15
BuildRequires:  perl(ExtUtils::ParseXS) >= 3.30
BuildRequires:  perl(Module::Build)
# Module Runtime
BuildRequires:  perl(Devel::CallChecker) >= 0.003
BuildRequires:  perl(Exporter)
BuildRequires:  perl(parent)
BuildRequires:  perl(Scalar::Util) >= 1.01
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
# Test Suite
BuildRequires:  perl(Test::More)
%if %{with perl_Params_Classify_enables_optional_test}
# Optional Tests
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
%endif
# Dependencies
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Devel::CallChecker) >= 0.003
Requires:       perl(Exporter)
Requires:       perl(Scalar::Util) >= 1.01
Requires:       perl(XSLoader)

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module provides various type-testing functions. These are intended
for functions that, unlike most Perl code, care what type of data they
are operating on. For example, some functions wish to behave
differently depending on the type of their arguments (like overloaded
functions in C++).

%prep
%setup -q -n Params-Classify-%{version}

%build
perl Build.PL --installdirs=vendor --optimize="%{optflags}"
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
./Build test

%files
%doc Changes README
%{perl_vendorarch}/auto/Params/
%{perl_vendorarch}/Params/
%{_mandir}/man3/Params::Classify.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.015-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.015-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.015-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.015-7
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.015-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.015-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.015-4
- Perl 5.28 rebuild

* Fri Mar  2 2018 Paul Howarth <paul@city-fan.org> - 0.015-3
- Arch-specific package using Module::Build needs to use ExtUtils::CBuilder
  (https://bugzilla.redhat.com/show_bug.cgi?id=1547165#c7)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.015-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug  7 2017 Paul Howarth <paul@city-fan.org> - 0.015-1
- Update to 0.015
  - Port to Perl 5.19.4, where the C type of array indices has changed
  - Update to accommodate PERL_OP_PARENT builds of Perl 5.21.11 or later
    (which is the default from Perl 5.25.1)
  - Trigger custom op generation via Devel::CallChecker rather than by hooking
    the underlying op checker
  - Update test suite not to rely on . in @INC, which is no longer necessarily
    there from Perl 5.25.7
  - No longer include a Makefile.PL in the distribution
  - Correct dynamic_config setting to 0
  - Use boolSV() where appropriate in XS code
  - Use cBOOL() where appropriate
  - Consistently use THX_ prefix on internal function names
  - Include META.json in distribution
  - Add MYMETA.json to .cvsignore
  - Convert .cvsignore to .gitignore
  - Update for changed S_croak_xs_usage() prototype in ExtUtils::ParseXS 3.30,
    requiring the new version of that module in order to build the XS
    implementation
  - In documentation, use four-column indentation for all verbatim material
  - In META.{yml,json}, point to public bug tracker
  - Correctly classify ExtUtils::ParseXS dependency as a recommendation rather
    than a requirement
  - Avoid some compiler warnings
- Classify buildreqs by usage
- Drop legacy spec file elements: %%defattr and Group: tag
- Make %%files list more explicit

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-19
- Perl 5.26 rebuild

* Mon May 22 2017 Petr Pisar <ppisar@redhat.com> - 0.013-18
- Restore compatibility with Perl 5.26.0 (CPAN RT#114490)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-16
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.013-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-13
- Perl 5.22 rebuild

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.013-12
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.013-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.013-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.013-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.013-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 19 2010 Iain Arnell <iarnell@gmail.com> 0.013-1
- update to latest upstream version

* Tue Nov 09 2010 Iain Arnell <iarnell@gmail.com> 0.012-3
- BR perl(ExtUtils::ParseXS) >= 2.2006 now that it's available

* Sat Nov 06 2010 Iain Arnell <iarnell@gmail.com> 0.012-2
- clarify ExtUtils::ParseXS build requirement version

* Thu Nov 04 2010 Iain Arnell <iarnell@gmail.com> 0.012-1
- update to latest upstream version
- use correct optflags macro

* Sun Sep 26 2010 Iain Arnell <iarnell@gmail.com> 0.011-1
- Specfile autogenerated by cpanspec 1.78.
