# Got the intial spec from Fedora and modified it
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((ExtUtils::Install|File::Spec|Module::Build|Module::Metadata|Perl::OSType)\\)$
%global __requires_exclude %__requires_exclude|^perl\\(CPAN::Meta::YAML\\) >= 0.002$

Summary:        Build and install Perl modules
Name:           perl-Module-Build
Version:        0.4224
Release:        4%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-Build/
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEONT/Module-Build-%{version}.tar.gz
%define sha1 Module-Build=4f78f28187d6525a59cc2e1887e4788964c8029c
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch

BuildRequires:  perl-interpreter
BuildRequires:  perl-devel
BuildRequires:  perl(Archive::Tar)
BuildRequires:  perl(AutoSplit)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(CPAN::Meta) >= 2.142060
BuildRequires:  perl(CPAN::Meta::Converter) >= 2.141170
BuildRequires:  perl(CPAN::Meta::Merge)
BuildRequires:  perl(CPAN::Meta::YAML) >= 0.003
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::CBuilder) >= 0.27
BuildRequires:  perl(ExtUtils::Install) >= 0.3
BuildRequires:  perl(ExtUtils::Installed)
BuildRequires:  perl(ExtUtils::Manifest) >= 1.54
BuildRequires:  perl(ExtUtils::Mkbootstrap)
BuildRequires:  perl(ExtUtils::Packlist)
BuildRequires:  perl(ExtUtils::ParseXS) >= 2.21
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 0.82
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp) >= 0.15
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::Metadata) >= 1.000002
BuildRequires:  perl(Parse::CPAN::Meta) >= 1.4401
BuildRequires:  perl(Perl::OSType) >= 1
BuildRequires:  perl(strict)
BuildRequires:  perl(TAP::Harness)
BuildRequires:  perl(TAP::Harness::Env)
BuildRequires:  perl(Test::Harness) >= 3.29
BuildRequires:  perl(Test::More) >= 0.49
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(version) >= 0.87
BuildRequires:  perl(warnings)

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

%check
rm t/signature.t
LANG=C TEST_SIGNATURE=1 MB_TEST_EXPERIMENTAL=1 ./Build test

%files
%license LICENSE
%doc Changes contrib LICENSE README
%{_bindir}/config_data
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
*   Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 0.4224-4
-   Use new perl package names.
* Sat May 09 00:20:53 PST 2020 Nick Samson <nisamson@microsoft.com> - 0.4224-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.4224-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.4224-1
-   Update to version 0.4224
*   Wed Apr 05 2017 Robert Qi <qij@vmware.com> 0.4222-1
-   Update version to 0.4222.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.4216-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.4216-1
-   Upgraded to version 0.4216
*   Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 0.4214-1
-   Initial version.
