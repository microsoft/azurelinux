# Run optional test
%if ! (0%{?rhel})
%bcond_without perl_Ref_Util_enables_optional_test
%else
%bcond_with perl_Ref_Util_enables_optional_test
%endif

Name:		perl-Ref-Util
Version:	0.204
Release:	8%{?dist}
Summary:	Utility functions for checking references
License:	MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://metacpan.org/release/Ref-Util
Source0:	https://cpan.metacpan.org/authors/id/A/AR/ARC/Ref-Util-%{version}.tar.gz#/perl-Ref-Util-%{version}.tar.gz
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	perl-generators
BuildRequires:	perl-interpreter
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(lib)
BuildRequires:	perl(Text::ParseWords)
# Dependencies of bundled ExtUtils::HasCompiler
BuildRequires:	gcc
BuildRequires:	perl-devel
BuildRequires:	perl(base)
BuildRequires:	perl(Config)
BuildRequires:	perl(DynaLoader)
BuildRequires:	perl(File::Basename)
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(File::Temp)
# Module
BuildRequires:	perl(Carp)
BuildRequires:	perl(constant)
BuildRequires:	perl(Exporter) >= 5.57
BuildRequires:	perl(Scalar::Util)
BuildRequires:	perl(strict)
BuildRequires:	perl(warnings)
# Test Suite
BuildRequires:	perl(File::Find)
BuildRequires:	perl(File::Spec)
BuildRequires:	perl(IPC::Open2)
BuildRequires:	perl(Ref::Util::XS)
BuildRequires:	perl(Test::More) >= 0.96
%if %{with perl_Ref_Util_enables_optional_test}
# Optional Tests
BuildRequires:	perl(B::Concise)
BuildRequires:	perl(CPAN::Meta) >= 2.120900
BuildRequires:	perl(Readonly)
%endif
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(Ref::Util::XS)

%description
Ref::Util introduces several functions to help identify references in a faster
and smarter way.

%prep
%setup -q -n Ref-Util-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} -c %{buildroot}

%check
make test

%files
%if 0%{?_licensedir:1}
%license LICENSE
%else
%doc LICENSE
%endif
%doc Changes README
%{perl_vendorlib}/Ref/
%{_mandir}/man3/Ref::Util.3*
%{_mandir}/man3/Ref::Util::PP.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.204-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.204-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.204-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.204-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.204-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.204-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.204-2
- Perl 5.28 rebuild

* Thu Apr 19 2018 Paul Howarth <paul@city-fan.org> - 0.204-1
- Update to 0.204
  - Fix Makefile.PL so that the 'install' sub is patched before WriteMakefile()
    is called (GH#41)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.203-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.203-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.203-2
- Perl 5.26 rebuild

* Mon May 15 2017 Paul Howarth <paul@city-fan.org> - 0.203-1
- Update to 0.203
  - Fix space/tab issue in Makefile
  - Don't use DynamicPrereqs for unrelated Makefile.PL snippet
  - Use of the Pure-Perl implementation can now be forced at runtime by setting
    either $Ref::Util::IMPLEMENTATION or $ENV{PERL_REF_UTIL_IMPLEMENTATION} to
    "XS"
  - Fix is_*_formatref() error messages (GH#38)
  - Speed enhancements for is_*_formatref() on 5.8+
  - Restore 5.6 and 5.8 compatibility
  - PP behaviour now matches XS for \v1.2.3 and \sub {}
  - Updated documentation to reflect the PP/XS split

* Fri May 12 2017 Paul Howarth <paul@city-fan.org> - 0.200-1
- Update to 0.200
  - Reimplement in pure Perl, with a dynamic dependency on a new Ref::Util::XS
    module that contains the fast XS implementation
- This release by ARC → update source URL
- Package is now noarch

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.113-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Paul Howarth <paul@city-fan.org> - 0.113-1
- Update to 0.113
  - Fix bugtracker link

* Sun Jan 15 2017 Paul Howarth <paul@city-fan.org> - 0.112-1
- Update to 0.112
  - Fix compilation on Sun (Oracle) and some MSVC compilers (GH#35)

* Fri Dec 30 2016 Paul Howarth <paul@city-fan.org> - 0.111-1
- Update to 0.111
  - Fix test failure on 5.8.5 and under
  - Moved to Dist::Zilla

* Thu Dec 29 2016 Paul Howarth <paul@city-fan.org> - 0.110-1
- Update to 0.110
  - Fix support of 5.8 (GH#29, GH#34)
  - Additional optimizations
  - More extensive test suite

* Mon Aug 29 2016 Paul Howarth <paul@city-fan.org> - 0.101-1
- Update to 0.101
  - A test accidentally added a dependency on Readonly.pm - fixed! (GH#30)
  - Update README

* Sat Aug 27 2016 Paul Howarth <paul@city-fan.org> - 0.100-1
- Update to 0.100
  - Support situations in op-code implementation where the parameters do not
    come as a list
  - Fix memory leak in dangling op
  - Support magic (tied variables)
  - Rework op implementation
  - Speed up by changing the top of the stack instead of POPing and PUSHing
  - Update ppport.h file from Devel::PPPort and remove the copy of SVRXOK since
    it's now available
  - Add license in Pod
  - Specify minimum version of perl (5.6.2)

* Thu Jul 28 2016 Paul Howarth <paul@city-fan.org> - 0.020-2
- Sanitize for Fedora submission

* Thu Jul 28 2016 Paul Howarth <paul@city-fan.org> - 0.020-1
- Initial RPM version
