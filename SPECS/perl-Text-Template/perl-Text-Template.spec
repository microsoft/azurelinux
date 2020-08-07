Summary:        Cross-platform path specification manipulation for Perl
Name:           perl-Text-Template
Version:        1.51
Release:        2%{?dist}
URL:            https://metacpan.org/pod/Text::Template
License:        The Perl 5 License (Artistic 1 & GPL 1)
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source:         https://cpan.metacpan.org/authors/id/M/MS/MSCHOUT/Text-Template-%{version}.tar.gz
%define sha1    Text-Template=423945fbe09c31f341d51afafcf635d2fbe6850b

BuildArch:      noarch
Requires:       perl >= 5.28.0
Requires:       perl-Test-Warnings
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-Test-Warnings

%description
Text::Template is a library for generating form letters, building HTML pages, or filling in templates generally.  A template is a piece of text that has little Perl programs embedded in it here and there.  When you fill in a template, you evaluate the little programs and replace them with their values.

%prep
%setup -q -n Text-Template-%{version}

%build
env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
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
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.51-2
-   Added %%license line automatically

*   Tue Mar 03 2020 Paul Monson <paulmon@microsoft.com> 1.51-1
-   Original version for CBL-Mariner.