Vendor:         Microsoft Corporation
Distribution:   Mariner
%global upstream_version 0.54_05
Name:           perl-TestML
Version:        %(echo '%{upstream_version}' | tr _ .)
Release:        6%{?dist}
Summary:        Generic software Testing Meta Language
# src/perl5/pkg/doc/TestML.pod: GPL+ or Artistic
# src/perl5/pkg/dist.ini:       GPL+ or Artistic
## unused and not packaged
# src/testml-compiler-coffee/pkg/package.json:              MIT
# src/testml-compiler-perl5/pkg/doc/TestML/Compiler.pod:    GPL+ or Artistic
# src/python/pkg/setup.py:      MIT
# src/python/pkg/LICENSE:       MIT text
# src/python/pkg/ReadMe.md:     MIT
# src/node/pkg/package.json:    MIT
License:        GPL+ or Artistic
URL:            https://github.com/testml-lang/testml/
Source0:        %{url}archive/pkg-perl5-%{upstream_version}.tar.gz
# Upstream build script requires checking out various git trees and
# executing sripts dowloaded from the Internet. Use a trivial Makefile.PL
# instead.
Source1:        Makefile.PL
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
# Run-time:
# No tests executed, no modules used at build time
# base
# Carp
# Exporter
# JSON::PP
# List::Util
# overload
# Scalar::Util
# strict
# Test::Builder
# Text::Diff
# utf8
# warnings
# XXX
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(List::Util)
Requires:       perl(Text::Diff)
Requires:       perl(warnings)
Requires:       perl(XXX)

%description
TestML <http://www.testml.org/> is a generic, programming language agnostic,
meta language for writing unit tests. The idea is that you can use the same
test files in multiple implementations of a given programming idea. Then you
can be more certain that your application written in, say, Python matches your
Perl implementation.

In a nutshell you write a bunch of data tests that have inputs and expected
results. Using a simple syntax, you specify what functions the data must pass
through to produce the expected results. You use a bridge class to write the
data functions that pass the data through your application.

In Perl 5, TestML module is the evolution of the Test::Base module. It has
a superset of Test:Base's goals. The data markup syntax is currently exactly
the same as Test::Base.

Currently, TestML is being redesigned. This package contains the new unstable
implementation. The original, production-ready, implementation is available
under TestML1 name in perl-TestML1 package.


%prep
%setup -q -n testml-pkg-perl5-%{upstream_version}
cd src/perl5
cp %{SOURCE1} .
mv pkg/doc/TestML.pod lib/
mv pkg/Changes .

%build
cd src/perl5
perl Makefile.PL VERSION=%{upstream_version} INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
cd src/perl5
make pure_install DESTDIR=$RPM_BUILD_ROOT
%{_fixperms} $RPM_BUILD_ROOT/*

%check
cd src/perl5
make test

%files
%doc src/perl5/Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.54.05-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.54.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.54.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.54.05-3
- Perl 5.30 rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.54.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 15 2018 Petr Pisar <ppisar@redhat.com> - 0.54.05-1
- 0.54_05 bump
- Upstream moved from CPAN to GitHub
- TestML is now unstable, old TestML Perl modules are now available as TestML1
  Perl modules (install "perl(TestML1)")

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.54-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.54-6
- Perl 5.28 rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.54-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.54-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.54-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Petr Pisar <ppisar@redhat.com> - 0.54-1
- 0.54 bump

* Mon Jan 09 2017 Petr Pisar <ppisar@redhat.com> - 0.53-1
- 0.53 bump

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-5
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.52-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.52-2
- Perl 5.22 rebuild

* Mon Jan 05 2015 Petr Pisar <ppisar@redhat.com> - 0.52-1
- 0.52 bump

* Thu Dec 18 2014 Petr Šabata <contyk@redhat.com> - 0.51-1
- 0.51 bump

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.49-2
- Perl 5.20 rebuild

* Mon Aug 18 2014 Petr Pisar <ppisar@redhat.com> - 0.49-1
- 0.49 bump

* Thu Aug 14 2014 Petr Pisar <ppisar@redhat.com> - 0.44-1
- 0.44 bump

* Tue Aug 12 2014 Petr Pisar <ppisar@redhat.com> - 0.43-1
- 0.43 bump

* Thu Aug 07 2014 Petr Pisar <ppisar@redhat.com> - 0.42-1
- 0.42 bump

* Wed Jul 30 2014 Petr Pisar <ppisar@redhat.com> 0.37-1
- Specfile autogenerated by cpanspec 1.78.
