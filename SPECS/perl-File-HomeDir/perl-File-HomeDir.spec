Summary:        File-HomeDir
Name:           perl-File-HomeDir
Version:        1.006
Release:        2%{?dist}
License:        GPL+ OR Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/File-HomeDir/
Source0:        https://cpan.metacpan.org/authors/id/R/RE/REHSACK/File-HomeDir-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
%if %{with_check}
BuildRequires:  perl(File::Which)
BuildRequires:  perl(Test::More)
%endif

Requires:   perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:   perl(Cwd) >= 3.12
Requires:   perl(File::Path) >= 2.01
Requires:   perl(File::Spec) >= 3.12
Requires:   perl(File::Temp) >= 0.19
Requires:   perl-File-Which

Provides:       perl(File::HomeDir) = %{version}-%{release}
Provides:       perl(File::HomeDir::Darwin) = %{version}-%{release}
Provides:       perl(File::HomeDir::Darwin::Carbon) = %{version}-%{release}
Provides:       perl(File::HomeDir::Darwin::Cocoa) = %{version}-%{release}
Provides:       perl(File::HomeDir::Driver) = %{version}-%{release}
Provides:       perl(File::HomeDir::FreeDesktop) = %{version}-%{release}
Provides:       perl(File::HomeDir::MacOS9) = %{version}-%{release}
Provides:       perl(File::HomeDir::Test) = %{version}-%{release}
Provides:       perl(File::HomeDir::Unix) = %{version}-%{release}
Provides:       perl(File::HomeDir::Windows) = %{version}-%{release}

%description
File::HomeDir is a module for locating the directories that are "owned" by a user (typicaly your user) and to solve the various issues that arise trying to find them consistently across a wide variety of platforms.

%prep
%autosetup -n File-HomeDir-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
%make_install
find %{buildroot} -name 'perllocal.pod' -delete

%check
%make_build test

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
%{_mandir}/man3/File::HomeDir.3pm.gz
%{_mandir}/man3/File::HomeDir::Darwin.3pm.gz
%{_mandir}/man3/File::HomeDir::Darwin::Carbon.3pm.gz
%{_mandir}/man3/File::HomeDir::Darwin::Cocoa.3pm.gz
%{_mandir}/man3/File::HomeDir::Driver.3pm.gz
%{_mandir}/man3/File::HomeDir::FreeDesktop.3pm.gz
%{_mandir}/man3/File::HomeDir::MacOS9.3pm.gz
%{_mandir}/man3/File::HomeDir::Test.3pm.gz
%{_mandir}/man3/File::HomeDir::Unix.3pm.gz
%{_mandir}/man3/File::HomeDir::Windows.3pm.gz

%changelog
* Fri Jul 29 2022 Muhammad Falak <mwani@microsoft.com> - 1.006-2
- Add BR on `perl(ExtUtils::MakeMaker)` & `perl(Test::More)` to enable ptest

* Tue Apr 26 2022 Mateusz Malisz <mamalisz@microsoft.com> - 1.006-1
- Update to 1.006

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.004-7
- Adding 'BuildRequires: perl-generators'.

* Mon Aug 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.004-6
- Bump release to represent package's move to toolchain
- Lint spec
- License verified

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.004-5
- Use new perl package names.
- Provide perl(File::HomeDir*).

* Thu Sep 10 2020 Joe Schmitt <joschmit@microsoft.com> 1.004-4
- Switch to new perl man page extension.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.004-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.004-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.004-1
- Update to version 1.004

* Tue Aug 08 2017 Chang Lee <changlee@vmware.com> 1.00-3
- Add perl-File-Which for make check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.00-2
- GA - Bump release of all rpms

* Thu Mar 3 2016 Xiaolin Li <xiaolinl@vmware.com> 1.00-1
- Initial version.
