Summary:        XML-Parser perl module
Name:           perl-XML-Parser
Version:        2.44
Release:        10%{?dist}
License:        GPL+ or Artistic
URL:            https://metacpan.org/pod/XML::Parser
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TODDR/XML-Parser-%{version}.tar.gz
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  expat-devel
BuildRequires:  perl >= 5.28.0
Requires:       expat
Requires:       perl >= 5.28.0

%description
The XML::Parser module is a Perl extension interface to James Clark's XML parser, expat
%prep
%setup -q -n XML-Parser-%{version}
%build
perl Makefile.PL --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

find %{buildroot}/%{_libdir}/perl5/ -name "perllocal.pod" | xargs rm -v

%check
make %{?_smp_mflags} test

%files
%defattr(-,root,root)
%license README
%{_libdir}/perl5/*
%{_mandir}/man3/*

%changelog
*   Wed May 27 2020 Nick Samson <nisamson@microsoft.com> 2.44-10
-   Added %%license invocation
*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 2.44-9
-   Renaming XML-Parser to perl-XML-Parser
*   Wed Apr 22 2020 Emre Girgin <mrgirgin@microsoft.com> 2.44-8
-   Decouple perl version from the build.
*   Tue Mar 07 2020 Paul Monson <paulmon@microsoft.com> 2.44-7
-   Update URL. Update Source0. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.44-6
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 2.44-5
-   Consuming perl version upgrade of 5.28.0
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.44-4
-   Aarch64 support
*   Tue Apr 4 2017 Robert Qi <qij@vmware.com> 2.44-3
-   Update to version 2.44-3 since perl version updated.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.44-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.44-1
-   Upgraded to version 2.44
*   Mon Feb 01 2016 Anish Swaminathan <anishs@vmware.com> 2.41-3
-   Fix for multithreaded perl
*   Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 2.41-2
-   Fix for new perl
*   Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 2.41-1
-   Initial build. First version
