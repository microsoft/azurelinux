Summary:        Interface to create per object accessors
Name:           perl-Object-Accessor
Version:        0.48
Release:        10%{?dist}
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Object-Accessor
Source0:        https://cpan.metacpan.org/authors/id/B/BI/BINGOS/Object-Accessor-%{version}.tar.gz
Source1:        LICENSE.PTR
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
BuildArch:      noarch

BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
%if 0%{?with_check}
BuildRequires:  perl(Params::Check)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Scalar)
BuildRequires:  perl(deprecate)
%endif

Requires:       perl-libs
Requires:       perl(deprecate)

Provides:       perl(Object::Accessor) = %{version}-%{release}

%description
Object::Accessor provides an interface to create per object accessors (as
opposed to per Class accessors, as, for example, Class::Accessor provides).

%prep
%setup -q -n Object-Accessor-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*
cp %{SOURCE1} ./

%check
make test

%files
%license LICENSE.PTR
%doc CHANGES README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri May 24 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.48-10
- Release bump to regenerate package's requires and provides.

* Fri Jul 29 2022 Muhammad Falak <mwani@microsoft.com> - 0.48-9
- Add BR on `perl(ExtUtils::MakeMaker)` & other check deps to enable ptest

*   Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.48-8
-   Adding 'BuildRequires: perl-generators'.

*   Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 0.48-7
-   Use new perl package names.
-   Provide perl(Object::Accessor).
*   Wed May 27 2020 Nick Samson <nisamson@microsoft.com> 0.48-6
-   Added LICENSE file and %%license invocation
*   Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.48-5
-   Fixed "Source0" and "URL" tags.
-   License verified.
-   Removed "%%define sha1".
-   Removed unnecessary comment.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.48-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.48-3
-   Consuming perl version upgrade of 5.28.0
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.48-2
-   GA - Bump release of all rpms
*   Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 0.48-1
-   Initial version.
