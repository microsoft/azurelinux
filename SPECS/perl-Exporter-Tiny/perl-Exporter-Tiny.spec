# Got the intial spec from Fedora and modified it
Summary:        An exporter with the features of Sub::Exporter but only core dependencies
Name:           perl-Exporter-Tiny
Version:        1.006002
Release:        1%{?dist}
License:        (GPL+ or Artistic) and Public Domain and (GPL+ or Artistic or CC-BY-SA)
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Exporter-Tiny/
Source0:        https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Exporter-Tiny-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
%if %{with_check}
BuildRequires:  perl(Test::More)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)

Provides:       perl(Exporter::Shiny) = %{version}-%{release}
Provides:       perl(Exporter::Tiny) = %{version}-%{release}

%description
Exporter::Tiny supports many of Sub::Exporter's external-facing features
including renaming imported functions with the -as, -prefix and -suffix
options; explicit destinations with the into option; and alternative
installers with the installer option. But it's written in only about 40%%
as many lines of code and with zero non-core dependencies.

Its internal-facing interface is closer to Exporter.pm, with configuration
done through the @EXPORT, @EXPORT_OK and %%EXPORT_TAGS package variables.

Exporter::Tiny performs most of its internal duties (including resolution of
tag names to sub names, resolution of sub names to coderefs, and installation
of coderefs into the target package) as method calls, which means they can be
overridden to provide interesting behavior.

%prep
%setup -q -n Exporter-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test

%files
%license LICENSE
%{perl_vendorlib}/Exporter/
%{_mandir}/man3/Exporter::Tiny.3*
%{_mandir}/man3/Exporter::Shiny.3*
%{_mandir}/man3/Exporter::Tiny::Manual*

%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.006002-1
- Auto-upgrade to 1.006002 - Azure Linux 3.0 - package upgrades

* Mon Aug 01 2022 Muhammad Falak <mwani@microsoft.com> - 1.002002-2
- Add BR on `perl(Test::More)` to fix ptest build

* Tue Apr 26 2022 Mateusz Malisz <mamalisz@microsoft.com> - 1.002002-1
- Update to 1.002002

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.002001-6
- Adding 'BuildRequires: perl-generators'.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.002001-5
- Removing the explicit %%clean stage.
- License verified.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.002001-4
- Use new perl package names.
- Provide perl(Exporter::*).

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.002001-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.002001-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.002001-1
- Update to version 1.002001

* Wed Mar 29 2017 Robert Qi <qij@vmware.com> 0.044-1
- Upgraded to 0.044.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.042-2
- GA - Bump release of all rpms

* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 0.042-1
- Initial version.
