# Got the intial spec from Fedora and modified it

Summary:        Handle Common Gateway Interface requests and responses
Name:           perl-CGI
Version:        4.60
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEEJO/CGI-%{version}.tar.gz
URL:            http://search.cpan.org/dist/CGI
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  sed
BuildRequires:  perl(ExtUtils::MakeMaker)
%if %{with_check}
BuildRequires:  perl(CPAN)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(local::lib)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(blib)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(File::Spec) >= 0.82
Requires:       perl(File::Temp) >= 0.17
Requires:       perl(Text::ParseWords)

Provides:       perl(CGI) = %{version}-%{release}
Provides:       perl(CGI::Carp) = %{version}-%{release}
Provides:       perl(CGI::Cookie) = %{version}-%{release}
Provides:       perl(CGI::File::Temp) = %{version}-%{release}
Provides:       perl(CGI::HTML::Functions) = %{version}-%{release}
Provides:       perl(CGI::MultipartBuffer) = %{version}-%{release}
Provides:       perl(CGI::Pretty) = %{version}-%{release}
Provides:       perl(CGI::Push) = %{version}-%{release}
Provides:       perl(CGI::Util) = %{version}-%{release}


%{?perl_default_filter}
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((File::Spec)\\)$
# Remove false dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Fh)\\)
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(MultipartBuffer\\)$
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Fh\\)

%description
CGI.pm is a stable, complete and mature solution for processing and preparing
HTTP requests and responses. Major features including processing form
submissions, file uploads, reading and writing cookies, query string
generation and manipulation, and processing and preparing HTTP headers. Some
HTML generation utilities are included as well.

CGI.pm performs very well in in a vanilla CGI.pm environment and also comes
with built-in support for mod_perl and mod_perl2 as well as FastCGI.

%prep
%setup -q -n CGI-%{version}
iconv -f iso8859-1 -t utf-8 < Changes > Changes.1
mv Changes.1 Changes
sed -i 's?usr/bin perl?usr/bin/perl?' t/init.t
chmod -c -x examples/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}/*

%check
PERL_MM_USE_DEFAULT=1 cpan Test::Warn
# Setting 'PERL5LIB' because otherwise tests can't find modules installed by cpan.
PERL5LIB=/root/perl5/lib/perl5 make %{?_smp_mflags} test

%files
%license LICENSE
%doc Changes README.md examples/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.60-1
- Auto-upgrade to 4.60 - Azure Linux 3.0 - package upgrades

* Thu Oct 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.54-3
- Switched to using Mariner packages instead of external test dependencies.

* Mon Aug 01 2022 Muhammad Falak <mwani@microsoft.com> - 4.54-2
- Add BR on `cpan` & `perl(Test::*)` to enable ptest

*   Tue Apr 26 2022 Mateusz Malisz <mamalisz@microsoft.com> - 4.54-1
-   Update to 4.54

*   Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.40-4
-   Adding 'BuildRequires: perl-generators'.
-   License verified.
*   Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 4.40-3
-   Use new perl package names.
-   Provide perl(CGI::*).
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.40-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 4.40-1
-   Update to version 4.40
*   Mon Apr 3 2017 Robert Qi <qij@vmware.com> 4.35-1
-   Upgraded to 4.35
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 4.26-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.26-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.26-1
-   Updated to version 4.26
*   Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 4.25-1
-   Initial version.
