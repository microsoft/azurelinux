# Got the intial spec from Fedora and modified it
Summary:        Read/Write YAML files with as little code as possible
Name:           perl-YAML-Tiny
Version:        1.74
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/YAML-Tiny/
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/YAML-Tiny-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
%if %{with_check}
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(Test::More)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(Exporter)
Requires:       perl(Fcntl)
Requires:       perl(Scalar::Util)
Provides:       perl(YAML::Tiny) = %{version}-%{release}

%description
YAML::Tiny is a Perl class for reading and writing YAML-style files,
written with as little code as possible, reducing load time and
memory overhead.

%prep
%setup -q -n YAML-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%license LICENSE
%{perl_vendorlib}/YAML/
%{_mandir}/man3/YAML::Tiny.3*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.74-1
- Auto-upgrade to 1.74 - Azure Linux 3.0 - package upgrades

* Mon Aug 01 2022 Muhammad Falak <mwani@microsoft.com> - 1.73-6
- Add BR on `perl(JSON::PP)` & `perl(Test::More)` to fix ptest

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.73-5
- Adding 'BuildRequires: perl-generators'.
- License verified.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.73-4
- Use new perl package names.
- Provide perl(YAML::Tiny).

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.73-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.73-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.73-1
- Update to version 1.73

* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 1.70-1
- Update version to 1.70

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.69-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.69-1
- Upgraded to version 1.69

* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.66-1
- Initial version.
