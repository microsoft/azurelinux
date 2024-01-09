# Got the intial spec from Fedora and modified it
Summary:        Recursively scan Perl code for dependencies
Name:           perl-Module-ScanDeps
Version:        1.35
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        https://cpan.metacpan.org/authors/id/R/RS/RSCHUPP/Module-ScanDeps-%{version}.tar.gz
URL:            http://search.cpan.org/dist/Module-ScanDeps/
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl-generators
%if %{with_check}
BuildRequires:  perl(CPAN)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Test::More)
%endif

Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(B)
Requires:       perl(DynaLoader)
Requires:       perl(Data::Dumper)
Requires:       perl(Encode)
Requires:       perl(File::Find)
Requires:       perl(Text::ParseWords)
Requires:       perl(Digest::MD5)
Requires:       perl(Storable)

Provides:       perl(Module::ScanDeps) = %{version}-%{release}
Provides:       perl(Module::ScanDeps::Cache) = %{version}-%{release}

%description
This module scans potential modules used by perl programs and returns a
hash reference.  Its keys are the module names as they appear in %%INC (e.g.
Test/More.pm).  The values are hash references.

%prep
%setup -q -n Module-ScanDeps-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
%{_fixperms} %{buildroot}

%check
export PERL_MM_USE_DEFAULT=1
cpan local::lib
cpan Test::Requires
make %{?_smp_mflags} test

%files
%license LICENSE
%{_bindir}/scandeps.pl
%{perl_vendorlib}/Module/
%{_mandir}/man1/scandeps.pl.1*
%{_mandir}/man3/*

%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.35-1
- Auto-upgrade to 1.35 - Azure Linux 3.0 - package upgrades

* Tue Aug 23 2020 Muhammad Falak <mwani@microsoft.com> - 1.31-2
- Add BR on `perl-{(CPAN::*),(FindBin),(Test::More)}` to enable ptest

* Fri Apr 22 2022 Mateusz Malisz <mamalisz@microsoft.com> - 1.31-1
- Update to 1.31

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.25-5
- Adding 'BuildRequires: perl-generators'.
- License verified.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.25-4
- Use new perl package names.
- Provide perl(Module::ScanDeps*).

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.25-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.25-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.25-1
- Update to version 1.25

* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 1.23-1
- Update version to 1.23

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.18-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.18-2
- GA - Bump release of all rpms

* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.18-1
- Initial version.
