%bcond_with perl_Unicode_UTF8_enables_Module_Install_ReadmeFromPod

# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Unicode_UTF8_enables_optional_test
%else
%bcond_with perl_Unicode_UTF8_enables_optional_test
%endif

Summary:	Encoding and decoding of UTF-8 encoding form
Name:		perl-Unicode-UTF8
Version:	0.62
Release:	13%{?dist}
License:	GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Unicode-UTF8
Source0:	https://cpan.metacpan.org/authors/id/C/CH/CHANSEN/Unicode-UTF8-%{version}.tar.gz#/perl-Unicode-UTF8-%{version}.tar.gz
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	perl-interpreter
BuildRequires:	perl-devel
BuildRequires:	perl-generators
BuildRequires:	perl(FindBin)
%if %{with perl_Unicode_UTF8_enables_Module_Install_ReadmeFromPod}
BuildRequires:	perl(inc::Module::Install)
BuildRequires:	perl(Module::Install::ReadmeFromPod)
%else
BuildRequires:	perl(base)
BuildRequires:	perl(Config)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(Pod::Text)
BuildRequires:	perl(vars)
%endif
# Module Runtime
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
BuildRequires:	perl(XSLoader)
# Test Suite
BuildRequires:	perl(Encode) >= 1.9801
BuildRequires:	perl(IO::File)
BuildRequires:	perl(lib)
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(Test::Builder)
BuildRequires:	perl(Test::Fatal) >= 0.006
BuildRequires:	perl(Test::More) >= 0.47
%if %{with perl_Unicode_UTF8_enables_optional_test}
# Optional Tests
BuildRequires:	perl(Taint::Runtime) >= 0.03
BuildRequires:	perl(Test::LeakTrace) >= 0.10
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:	perl(Variable::Magic)
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Exporter)
Requires:	perl(XSLoader)

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
This module provides functions to encode and decode UTF-8 encoding form as
specified by Unicode and ISO/IEC 10646:2011.

%prep
%setup -q -n Unicode-UTF8-%{version}

# Unbundle inc::Module::Install, we'll use system version instead
# unless we're on EL-6, where there's no Module::Install::ReadmeFromPod
%if %{with perl_Unicode_UTF8_enables_Module_Install_ReadmeFromPod}
rm -rf inc/
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%license README
%doc Changes
%{perl_vendorarch}/Unicode/
%{perl_vendorarch}/auto/Unicode/
%{_mandir}/man3/Unicode::UTF8.3*

%changelog
* Thu Jan 13 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.62-13
- License verified.

* Mon Nov 02 2020 Joe Schmitt <joschmit@microsoft.com> - 0.62-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Explicitly turn off perl_Unicode_UTF8_enables_Module_Install_ReadmeFromPod.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.62-9
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.62-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.62-2
- Perl 5.26 rebuild

* Wed Apr 12 2017 Paul Howarth <paul@city-fan.org> - 0.62-1
- Update to 0.62
  - Only check for missing Module::Install related modules in Makefile.PL

* Mon Apr 10 2017 Paul Howarth <paul@city-fan.org> - 0.61-1
- Update to 0.61
  - Avoid relying on current working directory being in @INC
  - Documentation typo fixes
- Drop redundant Group: tag
- Simplify find commands using -empty and -delete

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.60-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.60-8
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.60-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.60-5
- Perl 5.22 rebuild

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.60-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep 25 2013 Paul Howarth <paul@city-fan.org> - 0.60-1
- Update to 0.60
  - Added valid_utf8()
  - Skip copy-on-write tests on Perl 5.19

* Mon Sep  2 2013 Paul Howarth <paul@city-fan.org> - 0.59-3
- BR: perl(Scalar::Util) for the test suite (#1003650)
- Add buildreqs for deps of bundled inc::Module::Install for EL-6 build

* Mon Sep  2 2013 Paul Howarth <paul@city-fan.org> - 0.59-2
- Sanitize for Fedora submission

* Mon Sep  2 2013 Paul Howarth <paul@city-fan.org> - 0.59-1
- Initial RPM build
