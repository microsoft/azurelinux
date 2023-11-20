# Got the intial spec from Fedora and modified it
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((VMS|Win32|BSD::|DB\\)$)
# unicore::Name - it's needed by perl, maybe problem of rpm
# FCGI is external dependency after install of perl-CGI, remove it during RC releases
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((VMS|BSD::|Win32|Tk|Mac::|Your::Module::Here|unicore::Name|FCGI)

Summary:        Perl extension interface for libcurl
Name:           perl-WWW-Curl
Version:        4.17
Release:        15%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://search.cpan.org/dist/WWW-Curl/
Source0:        https://search.cpan.org/CPAN/authors/id/S/SZ/SZBALINT/WWW-Curl-%{version}.tar.gz

Patch0:         0001-Curl-macros-fix.patch
Patch1:         WWW-Curl-4.17-Adapt-to-changes-in-cURL-7.69.0.patch
Patch2:         WWW-Curl-4.17-Adapt-to-curl-7.87.0.patch
Patch3:         WWW-Curl-4.17-Work-around-a-macro-bug-in-curl-7.87.0.patch

BuildRequires:  curl-devel
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Module::CoreList)
BuildRequires:  perl-Module-Install
BuildRequires:  perl-YAML-Tiny
BuildRequires:  perl-generators
%if %{with_check}
BuildRequires:  perl(Test::More)
BuildRequires:  perl(File::Temp)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       curl

Provides:       perl(WWW::Curl) = %{version}-%{release}
Provides:       perl(WWW::Curl::Easy) = %{version}-%{release}
Provides:       perl(WWW::Curl::Form) = %{version}-%{release}
Provides:       perl(WWW::Curl::Multi) = %{version}-%{release}
Provides:       perl(WWW::Curl::Share) = %{version}-%{release}

%description
WWW::Curl is a Perl extension interface for libcurl.

%prep
%autosetup -p1 -n WWW-Curl-%{version}
rm -rf inc && sed -i -e '/^inc\//d' MANIFEST
sed -i 's/_LASTENTRY\\z/_LASTENTRY\\z|CURL_DID_MEMORY_FUNC_TYPEDEFS\\z/' Makefile.PL

%build
perl Makefile.PL INSTALLDIRS=vendor
sed -i '/CURL_STRICTER/d' curlopt-constants.c
sed -i 's/CURLAUTH_ANY/(int)CURLAUTH_ANY/' curlopt-constants.c
sed -i 's/CURLAUTH_ANYSAFE/(int)CURLAUTH_ANYSAFE/' curlopt-constants.c
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} %{buildroot}/*

%check
# These tests require network, use "--with network_tests" to execute them
%{?!_with_network_tests: rm t/01basic.t }
%{?!_with_network_tests: rm t/02callbacks.t }
%{?!_with_network_tests: rm t/04abort-test.t }
%{?!_with_network_tests: rm t/05progress.t }
%{?!_with_network_tests: rm t/08ssl.t }
%{?!_with_network_tests: rm t/09times.t }
%{?!_with_network_tests: rm t/14duphandle.t }
%{?!_with_network_tests: rm t/15duphandle-callback.t }
%{?!_with_network_tests: rm t/18twinhandles.t }
%{?!_with_network_tests: rm t/19multi.t }
%{?!_with_network_tests: rm t/21write-to-scalar.t }
make test

%files
%license LICENSE
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/WWW*
%{_mandir}/man3/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 4.17-15
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Apr 27 2023 Olivia Crain <oliviacrain@microsoft.com> - 4.17-14
- Fix package test by adding check-time requirement on perl(Test::More), perl(File::Temp)

* Fri Mar 17 2023 Muhammad Falak <mwani@microsoft.com> - 4.17-13
- Introduce patches to workaround macro bug which breaks build
- Add BR on perl(FindBin) & perl(Module::CoreList)

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.17-12
- Adding 'BuildRequires: perl-generators'.

* Fri Apr 02 2021 Thomas Crain <thcrain@microsoft.com> - 4.17-11
- Merge the following releases from 1.0 to dev branch
- pawelwi@microsoft.com, 4.17-10: Adapting Fedora 32 patch (license: MIT) for "curl" versions >= 7.69.0.
- JOSLOBO 7/26/21: Bump dash version due to merge.

* Tue Dec 29 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.17-10  (from 1.0 branch)
- Adapting Fedora 32 patch (license: MIT) for "curl" versions >= 7.69.0.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 4.17-9 (from dev branch)
- Use new perl package names.
- Provide perl(WWW::Curl*).

* Tue Aug 11 2020 Andrew Phelps <anphel@microsoft.com> - 4.17-9 (from 1.0 branch)
- Add provides for perl(WWW::Curl::Easy)

* Tue May 19 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.17-8
- Adding a patch to build with "curl" version >= 7.66.0.
- License verified.
- Updated the 'Source0' and 'URL' tags.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.17-7
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.17-6
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> - 4.17-5
- Consuming perl version upgrade of 5.28.0

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.17-4
- BuildRequires curl-devel.

* Thu Sep 15 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.17-3
- Build WWW-Curl with curl 7.50.3

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.17-2
- GA - Bump release of all rpms

* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> - 4.17-1
- Initial version.
