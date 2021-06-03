Summary:        File-HomeDir
Name:           perl-File-HomeDir
Version:        1.004
Release:        3%{?dist}
License:        The Perl 5 License (Artistic 1 & GPL 1)
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/File-HomeDir/
Source0:        https://cpan.metacpan.org/authors/id/R/RE/REHSACK/File-HomeDir-%{version}.tar.gz
%define sha1 File-HomeDir=7d2ceddfd2f331cc1ac0dc160b0d4a91302ee418
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch
BuildRequires:	perl >= 5.28.0
%if %{with_check}
BuildRequires:  perl-File-Which
%endif
Requires:	perl >= 5.28.0
Requires:   perl-File-Which

%description
File::HomeDir is a module for locating the directories that are "owned" by a user (typicaly your user) and to solve the various issues that arise trying to find them consistently across a wide variety of platforms.

%prep
%setup -q -n File-HomeDir-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
make test

%files
%license LICENSE
%{perl_vendorlib}/File/HomeDir.pm
%{perl_vendorlib}/File/HomeDir/Darwin.pm
%{perl_vendorlib}/File/HomeDir/Darwin/Carbon.pm
%{perl_vendorlib}/File/HomeDir/Darwin/Cocoa.pm
%{perl_vendorlib}/File/HomeDir/Driver.pm
%{perl_vendorlib}/File/HomeDir/FreeDesktop.pm
%{perl_vendorlib}/File/HomeDir/MacOS9.pm
%{perl_vendorlib}/File/HomeDir/Test.pm
%{perl_vendorlib}/File/HomeDir/Unix.pm
%{perl_vendorlib}/File/HomeDir/Windows.pm
%{_mandir}/man3
%{_mandir}/man3/File::HomeDir.3.gz
%{_mandir}/man3/File::HomeDir::Darwin.3.gz
%{_mandir}/man3/File::HomeDir::Darwin::Carbon.3.gz
%{_mandir}/man3/File::HomeDir::Darwin::Cocoa.3.gz
%{_mandir}/man3/File::HomeDir::Driver.3.gz
%{_mandir}/man3/File::HomeDir::FreeDesktop.3.gz
%{_mandir}/man3/File::HomeDir::MacOS9.3.gz
%{_mandir}/man3/File::HomeDir::Test.3.gz
%{_mandir}/man3/File::HomeDir::Unix.3.gz
%{_mandir}/man3/File::HomeDir::Windows.3.gz

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.004-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.004-1
-   Update to version 1.004
*   Tue Aug 08 2017 Chang Lee <changlee@vmware.com> 1.00-3
-   Add perl-File-Which for make check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.00-2
-   GA - Bump release of all rpms
*   Thu Mar 3 2016 Xiaolin Li <xiaolinl@vmware.com> 1.00-1
-   Initial version.
