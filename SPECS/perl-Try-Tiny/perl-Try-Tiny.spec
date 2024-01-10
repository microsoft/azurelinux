Summary:        Minimal try/catch with proper preservation of $@
Name:           perl-Try-Tiny
Version:        0.31
Release:        1%{?dist}
URL:            https://metacpan.org/release/Try-Tiny
License:        MIT
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source:         https://cpan.metacpan.org/authors/id/E/ET/ETHER/Try-Tiny-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
%if %{with_check}
BuildRequires:  perl(Test::More)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Sub::Util)
Provides:       perl(Try::Tiny) = %{version}-%{release}

%description
This module provides bare bones try/catch/finally statements that are designed to minimize common mistakes with eval blocks, and NOTHING else.

This is unlike TryCatch which provides a nice syntax and avoids adding another call stack layer, and supports calling return from the try block to return from the parent subroutine. These extra features come at a cost of a few dependencies, namely Devel::Declare and Scope::Upper which are occasionally problematic, and the additional catch filtering uses Moose type constraints which may not be desirable either.

%prep
%setup -q -n Try-Tiny-%{version}

%build
env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
make test

%files
%license LICENCE
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.31-1
- Auto-upgrade to 0.31 - Azure Linux 3.0 - package upgrades

* Mon Aug 01 2022 Muhammad Falak <mwani@microsoft.com> - 0.30-8
- Add BR on `perl(Test::More)` to fix ptest build

*   Wed Apr 27 2022 Mateusz Malisz <mamalisz@microsoft.com> - 0.30-7
-   Add missing BuildRequires for ExtUtils::MakeMaker

*   Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.30-6
-   Adding 'BuildRequires: perl-generators'.

*   Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 0.30-5
-   Use new perl package names.
-   Build with NO_PACKLIST option.
-   Provide perl(Try::Tiny).

*   Tue May 26 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.30-4
-   Adding the "%%license" macro.

*   Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> 0.30-3
-   Update URL.
-   Update License.
-   License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.30-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.30-1
-   Update to version 0.30

*   Wed Apr 26 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.28-2
-   Fix arch

*   Wed Apr 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.28-1
-   Initial version.
