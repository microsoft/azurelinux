# Got the intial spec from Fedora and modified it
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((ExtUtils::Install|File::Spec|Module::Build|Module::Metadata|Perl::OSType)\\)$
%global __requires_exclude %__requires_exclude|^perl\\(CPAN::Meta::YAML\\) >= 0.002$

Summary:        Build and install Perl modules
Name:           perl-Module-Build
Version:        0.4234
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-Build/
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-%{version}.tar.gz
Source1:        LICENSE.PTR
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch

BuildRequires:  perl >= 5.28.0
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(ExtUtils::Install)
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(blib)
BuildRequires:  perl(lib)
BuildRequires:  perl-generators
%if %{with_check}
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(CPAN::Meta::YAML)
BuildRequires:  perl(Module::Metadata)
BuildRequires:  perl(Perl::OSType)
BuildRequires:  perl(Test::More)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(CPAN::Meta) >= 2.142060
Requires:       perl(CPAN::Meta::Converter) >= 2.141170
Requires:       perl(CPAN::Meta::Merge)
Requires:       perl(ExtUtils::CBuilder) >= 0.27
Requires:       perl(ExtUtils::Install) >= 0.3
Requires:       perl(ExtUtils::Manifest) >= 1.54
Requires:       perl(ExtUtils::Mkbootstrap)
Requires:       perl(ExtUtils::ParseXS) >= 2.21
Requires:       perl(Module::Metadata) >= 1.000002

Provides:       perl(Module::Build) = %{version}-%{release}
Provides:       perl(Module::Build::Base) = %{version}-%{release}
Provides:       perl(Module::Build::Compat) = %{version}-%{release}
Provides:       perl(Module::Build::Config) = %{version}-%{release}
Provides:       perl(Module::Build::ConfigData) = %{version}-%{release}
Provides:       perl(Module::Build::Cookbook) = %{version}-%{release}
Provides:       perl(Module::Build::Dumper) = %{version}-%{release}
Provides:       perl(Module::Build::Notes) = %{version}-%{release}
Provides:       perl(Module::Build::PPMMaker) = %{version}-%{release}
Provides:       perl(Module::Build::Platform::Default) = %{version}-%{release}
Provides:       perl(Module::Build::Platform::MacOS) = %{version}-%{release}
Provides:       perl(Module::Build::Platform::Unix) = %{version}-%{release}
Provides:       perl(Module::Build::Platform::VMS) = %{version}-%{release}
Provides:       perl(Module::Build::Platform::VOS) = %{version}-%{release}
Provides:       perl(Module::Build::Platform::Windows) = %{version}-%{release}
Provides:       perl(Module::Build::Platform::aix) = %{version}-%{release}
Provides:       perl(Module::Build::Platform::cygwin) = %{version}-%{release}
Provides:       perl(Module::Build::Platform::darwin) = %{version}-%{release}
Provides:       perl(Module::Build::Platform::os2) = %{version}-%{release}
Provides:       perl(Module::Build::PodParser) = %{version}-%{release}


%description
Module::Build is a system for building, testing, and installing Perl
modules. It is meant to be an alternative to ExtUtils::MakeMaker.

%prep
%setup -q -n Module-Build-%{version}

%build
perl Build.PL installdirs=vendor
./Build

%install
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}/*

cp %{SOURCE1} .

%check
rm t/signature.t
LANG=C TEST_SIGNATURE=1 MB_TEST_EXPERIMENTAL=1 ./Build test

%files
%license LICENSE.PTR
%doc Changes contrib README
%{_bindir}/config_data
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4234-1
- Auto-upgrade to 0.4234 - Azure Linux 3.0 - package upgrades

* Tue Aug 23 2022 Muhammad Falak <mwani@microsoft.com> - 0.4231-2
- Add BR on `perl(ExtUtils::*)` & `perl(CPAN::*)` to enable ptest

* Fri Apr 22 2022 Mateusz Malisz <mamalisz@microsoft.com> - 0.4231-1
- Update to 0.4231

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4224-5
- Adding 'BuildRequires: perl-generators'.
- License verified.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 0.4224-4
- Use new perl package names.
- Provide perl(Module::Build*)

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.4224-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.4224-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.4224-1
- Update to version 0.4224

* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 0.4222-1
- Update version to 0.4222.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.4216-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.4216-1
- Upgraded to version 0.4216

* Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 0.4214-1
- Initial version.
