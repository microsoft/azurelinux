Summary:        Test for warnings and the lack of them in Perl
Name:           perl-Test-Warnings
Version:        0.032
Release:        1%{?dist}
URL:            https://metacpan.org/release/Test-Warnings
License:        GPL+ or Artistic
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source:         https://cpan.metacpan.org/authors/id/E/ET/ETHER/Test-Warnings-%{version}.tar.gz

BuildArch:      noarch
Requires:       perl-libs
Requires:       perl(Carp)
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
%if %{with_check}
BuildRequires:  perl(Test::More)
%endif

Provides:       perl(Test::Warnings) = %{version}-%{release}

%description
Test::Warnings tests for warnings and the lack of them

%prep
%setup -q -n Test-Warnings-%{version}

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
* Mon Nov 27 2023 Andrew Phelps <anphel@microsoft.com> - 0.032-1
- Upgrade to version 0.032

* Mon Aug 01 2022 Muhammad Falak <mwani@microsoft.com> - 0.031-2
- Add BR on `perl(Test::More)` to enable ptest

*   Thu Apr 14 2022 Mateusz Malisz <mateusz.malisz@microsoft.com> - 0.031-1
-   Updated to 0.031

*   Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.028-5
-   Adding 'BuildRequires: perl-generators'.

*   Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 0.028-4
-   Use new perl package names.
-   Build with NO_PACKLIST option.
-   Provide perl(Test::Warnings).

*   Tue May 26 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.028-3
-   Adding the "%%license" macro.

*   Thu Apr 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.028-2
-   License verified.

*   Tue Mar 03 2020 Paul Monson <paulmon@microsoft.com> 0.028-1
-   Original version for CBL-Mariner.
