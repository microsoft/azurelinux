# Got the intial spec from Fedora and modified it
Summary:        Read/Write YAML files with as little code as possible
Name:           perl-YAML-Tiny
Version:        1.73
Release:        3%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/YAML-Tiny/
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/YAML-Tiny-%{version}.tar.gz
%define sha1 YAML-Tiny=32ee7a7d499c7d8c2b4672f9735901fb4de1ab88
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildArch:      noarch
BuildRequires:  perl >= 5.28.0
Requires:	perl >= 5.28.0
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
* Sat May 09 00:21:15 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.73-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.73-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.73-1
-   Update to version 1.73
*   Wed Apr 05 2017 Robert Qi <qij@vmware.com> 1.70-1
-   Update version to 1.70
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.69-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.69-1
-   Upgraded to version 1.69
*   Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.66-1
-   Initial version.
