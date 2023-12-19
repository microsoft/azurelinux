Summary:        Wrapper Class for the various JSON classes
Name:           perl-JSON-Any
Version:        1.40
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/~ether/JSON-Any-1.39/lib/JSON/Any.pm
Source:         http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/JSON-Any-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
%if %{with_check}
BuildRequires:  perl(CPAN)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(Test::More)
%endif

Requires:       perl(Carp)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

Provides:       perl(JSON::Any) = %{version}-%{release}

%description
This module tries to provide a coherent API to bring together the various JSON modules currently on CPAN. This module will allow you to code to any JSON API and have it work regardless of which JSON module is actually installed.

%prep
%setup -q -n JSON-Any-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
            -name '*.bs' -size 0 \) -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%check
export PERL_MM_USE_DEFAULT=1
cpan local::lib
cpan Test::Fatal Test::Requires Test::Warnings Test::Without::Module
make test

%files
%license LICENCE
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.40-1
- Auto-upgrade to 1.40 - Azure Linux 3.0 - package upgrades

* Fri Jul 29 2022 Muhammad Falak <mwani@microsoft.com> - 1.39-10
- Add BR on `perl(ExtUtils::MakeMaker)` & `cpan` to enable ptest

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.39-9
- Adding 'BuildRequires: perl-generators'.
- License verified.

* Fri Apr 02 2021 Thomas Crain <thcrain@microsoft.com> - 1.39-8
- Merge the following releases from 1.0 to dev branch
- pawelwi@microsoft.com, 1.39-7: Adding 'local::lib' perl5 library to fix test dependencies.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.39-7
- Use new perl package names.
- Provide perl(JSON::Any).

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.39-6
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.39-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> - 1.39-4
- Consuming perl version upgrade of 5.28.0

* Tue Aug 08 2017 Chang Lee <Chang Lee@vmware.com> - 1.39-3
- Adding dependencies for %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.39-2
- GA - Bump release of all rpms

* Mon Mar 28 2016 Mahmoud Bassiouny <mbassiounu@vmware.com> - 1.39-1
- Initial version.
