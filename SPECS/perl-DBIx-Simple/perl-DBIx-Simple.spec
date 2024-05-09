# Got the intial spec from Fedora and modified it
Summary:        Easy-to-use OO interface to DBI
Name:           perl-DBIx-Simple
Version:        1.37
Release:        6%{?dist}
# License not mentioned in any of the source files and CPAN web page explicitly says it's unknown.
License:        Unknown
Group:          Development/Libraries
Source0:        https://cpan.metacpan.org/authors/id/J/JU/JUERD/DBIx-Simple-%{version}.tar.gz
URL:            https://search.cpan.org/dist/DBIx-Simple/
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
BuildArch:      noarch
BuildRequires:  perl-DBI >= 1.21
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
%if 0%{?with_check}
BuildRequires:  perl(Test::More)
%endif

Requires:       perl-libs
Requires:       perl-Object-Accessor
Requires:       perl-DBI >= 1.21

Provides:       perl(DBIx::Simple) = %{version}-%{release}
Provides:       perl(DBIx::Simple::DeadObject) = %{version}-%{release}
Provides:       perl(DBIx::Simple::Dummy) = %{version}-%{release}
Provides:       perl(DBIx::Simple::Result) = %{version}-%{release}
Provides:       perl(DBIx::Simple::Result::RowObject) = %{version}-%{release}
Provides:       perl(DBIx::Simple::Statement) = %{version}-%{release}

%description
DBIx::Simple provides a simplified interface to DBI, Perl's powerful
database module.

%prep
%setup -q -n DBIx-Simple-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
make test

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Aug 01 2022 Muhammad Falak <mwani@microsoft.com> - 1.37-6
- Add BR on `perl(Test::More)` to fix ptest

*   Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.37-5
-   Adding 'BuildRequires: perl-generators'.

*   Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.37-4
-   Removing the explicit %%clean stage.
-   License verified.

*   Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.37-3
-   Use new perl package names.
-   Provide perl(DBIx::*).
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.37-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.37-1
-   Update to version 1.37
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.35-2
-   GA - Bump release of all rpms
*   Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.35-1
-   Initial version.
