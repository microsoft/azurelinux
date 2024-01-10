# Got the intial spec from Fedora and modified it
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Devel::PPPort|ExtUtils::MakeMaker|File::Remove|File::Spec|YAML::Tiny)\\)$

Summary:        Standalone, extensible Perl module installer
Name:           perl-Module-Install
Version:        1.21
Release:        1%{?dist}
License:        GPL+ or Artistic
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-Install/
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/Module-Install-%{version}.tar.gz
Source1:        LICENSE.PTR
BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
BuildRequires:  perl-generators
BuildRequires:  perl-YAML-Tiny
Requires:       perl-YAML-Tiny
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Archive::Zip) >= 1.37
Requires:       perl(Carp)
Requires:       perl(CPAN)

Provides:       perl(Module::AutoInstall) = %{version}-%{release}
Provides:       perl(Module::Install) = %{version}-%{release}
Provides:       perl(Module::Install::Admin) = %{version}-%{release}
Provides:       perl(Module::Install::Admin::Bundle) = %{version}-%{release}
Provides:       perl(Module::Install::Admin::Compiler) = %{version}-%{release}
Provides:       perl(Module::Install::Admin::Find) = %{version}-%{release}
Provides:       perl(Module::Install::Admin::Include) = %{version}-%{release}
Provides:       perl(Module::Install::Admin::Makefile) = %{version}-%{release}
Provides:       perl(Module::Install::Admin::Manifest) = %{version}-%{release}
Provides:       perl(Module::Install::Admin::Metadata) = %{version}-%{release}
Provides:       perl(Module::Install::Admin::ScanDeps) = %{version}-%{release}
Provides:       perl(Module::Install::Admin::WriteAll) = %{version}-%{release}
Provides:       perl(Module::Install::AutoInstall) = %{version}-%{release}
Provides:       perl(Module::Install::Base) = %{version}-%{release}
Provides:       perl(Module::Install::Base::FakeAdmin) = %{version}-%{release}
Provides:       perl(Module::Install::Bundle) = %{version}-%{release}
Provides:       perl(Module::Install::Can) = %{version}-%{release}
Provides:       perl(Module::Install::Compiler) = %{version}-%{release}
Provides:       perl(Module::Install::DSL) = %{version}-%{release}
Provides:       perl(Module::Install::Deprecated) = %{version}-%{release}
Provides:       perl(Module::Install::External) = %{version}-%{release}
Provides:       perl(Module::Install::Fetch) = %{version}-%{release}
Provides:       perl(Module::Install::Include) = %{version}-%{release}
Provides:       perl(Module::Install::Inline) = %{version}-%{release}
Provides:       perl(Module::Install::MakeMaker) = %{version}-%{release}
Provides:       perl(Module::Install::Makefile) = %{version}-%{release}
Provides:       perl(Module::Install::Metadata) = %{version}-%{release}
Provides:       perl(Module::Install::PAR) = %{version}-%{release}
Provides:       perl(Module::Install::Run) = %{version}-%{release}
Provides:       perl(Module::Install::Scripts) = %{version}-%{release}
Provides:       perl(Module::Install::Share) = %{version}-%{release}
Provides:       perl(Module::Install::Win32) = %{version}-%{release}
Provides:       perl(Module::Install::With) = %{version}-%{release}
Provides:       perl(Module::Install::WriteAll) = %{version}-%{release}
Provides:       perl(inc::Module::Install) = %{version}-%{release}
Provides:       perl(inc::Module::Install::DSL) = %{version}-%{release}

%description
Module::Install is a package for writing installers for CPAN (or CPAN-like)
distributions that are clean, simple, minimalist, act in a strictly correct
manner with ExtUtils::MakeMaker, and will run on any Perl installation
version 5.005 or newer.

%prep
%setup -q -n Module-Install-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
rm -rf %{buildroot}/blib/lib/auto/share/dist/Module-Install/dist_file.txt
%{_fixperms} %{buildroot}/*

cp %{SOURCE1} .

%check
export PERL_MM_USE_DEFAULT=1
cpan local::lib
cpan File::Remove
make %{?_smp_mflags} test AUTOMATED_TESTING=1

%files
%license LICENSE.PTR
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Dec 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.21-1
- Auto-upgrade to 1.21 - Azure Linux 3.0 - package upgrades

* Wed Jan 19 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.19-5
- Adding 'BuildRequires: perl-generators'.
- License verified.

* Mon Oct 12 2020 Joe Schmitt <joschmit@microsoft.com> 1.19-4
- Use new perl package names.
- Provide perl(Module::*).

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.19-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.19-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.19-1
- Update to version 1.19

* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 1.18-1
- Update version to 1.18.

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.16-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.16-2
- GA - Bump release of all rpms

* Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com> 1.16-1
- Upgrade version to 1.16

* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.14-1
- Initial version.
