# Got the intial spec from Fedora and modified it
Summary:        JSON serializing/deserializing, done correctly and fast
Name:           perl-JSON-XS
Version:        4.03
Release:        2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            https://search.cpan.org/dist/JSON-XS/
Source0:        https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/JSON-XS-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-Canary-Stability
BuildRequires:  perl-common-sense
BuildRequires:  perl-generators
BuildRequires:  perl-Types-Serialiser
BuildRequires:  perl(ExtUtils::MakeMaker)
%if 0%{?with_check}
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Array)
%endif

Requires:  perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:  perl-Canary-Stability
Requires:  perl-Types-Serialiser
Requires:  perl-common-sense

Provides:       perl(JSON::XS) = %{version}-%{release}

%description
This module converts Perl data structures to JSON and vice versa. Its
primary goal is to be correct and its secondary goal is to be fast. To
reach the latter goal it was written in C.

%prep
%setup -q -n JSON-XS-%{version}

sed -i 's/\r//' t/*
perl -pi -e 's|^#!/opt/bin/perl|#!%{__perl}|' eg/*
chmod -c -x eg/*

%build
export PERL_CANARY_STABILITY_NOPROMPT=1
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license COPYING
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto
%{_bindir}/*
%{_mandir}/man[13]/*

%changelog
* Fri Jul 29 2022 Muhammad Falak <mwani@microsoft.com> - 4.03-2
- Add BR on `perl(ExtUtils::MakeMaker)` & `perl(Test::*)` to enable ptest

* Mon Apr 25 2022 Mateusz Malisz <mamalisz@microsoft.com> - 4.03-1
- Update to version 4.03

* Fri Feb 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.04-6
- Removing epoch.

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:3.04-5
- Adding 'BuildRequires: perl-generators'.
- License verified.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1:3.04-4
- Use new perl package names.
- Provide perl(JSON::XS).

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1:3.04-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.04-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 3.04-1
- Update to version 3.04

* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 3.03-1
- Add build requires for perl-Canary-Stability, and pass NO_PACKLIST to Makefile.PL.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.01-2
- GA - Bump release of all rpms

* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 3.01-1
- Initial version.
