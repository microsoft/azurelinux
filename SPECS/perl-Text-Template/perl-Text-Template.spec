Summary:        Cross-platform path specification manipulation for Perl
Name:           perl-Text-Template
Version:        1.61
Release:        1%{?dist}
URL:            https://metacpan.org/pod/Text::Template
License:        GPL+ or Artistic
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source:         https://cpan.metacpan.org/authors/id/M/MS/MSCHOUT/Text-Template-%{version}.tar.gz

BuildArch:      noarch
Requires:       perl-libs
Requires:       perl(Carp)
Requires:       perl-Test-Warnings
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl-Test-Warnings

Provides:       perl(Text::Template) = %{version}-%{release}
Provides:       perl(Text::Template::Preprocess) = %{version}-%{release}

%description
Text::Template is a library for generating form letters, building HTML pages, or filling in templates generally.  A template is a piece of text that has little Perl programs embedded in it here and there.  When you fill in a template, you evaluate the little programs and replace them with their values.

%prep
%setup -q -n Text-Template-%{version}

%build
env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
make test

%files
%license LICENSE
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
* Tue Nov 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.61-1
- Auto-upgrade to 1.61 - Azure Linux 3.0 - package upgrades

*   Fri Apr 22 2022 Mateusz Malisz <mamalisz@microsoft.com> - 1.60-1
-   Update to 1.60

*   Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.51-4
-   Adding 'BuildRequires: perl-generators'.
-   License verified.

*   Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.51-3
-   Use new perl package names.
-   Disable PACK_LIST for packaging.
-   Provide perl(Text::Template*).

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.51-2
-   Added %%license line automatically

*   Tue Mar 03 2020 Paul Monson <paulmon@microsoft.com> 1.51-1
-   Original version for CBL-Mariner.
