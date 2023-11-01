Summary:        Converts markdown into roff (man pages)
Name:           go-md2man
Version:        2.0.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Tools/Container
URL:            https://github.com/cpuguy83/go-md2man
Source0:        https://github.com/cpuguy83/go-md2man/archive/v%{version}.tar.gz#/go-md2man-%{version}.tar.gz
BuildRequires:  golang
BuildRequires:  which
# required packages on install
Requires:       /bin/sh
Provides:       golang-github-cpuguy83-md2man
Provides:       go-go-md2man = %{version}-%{release}

%description
Converts markdown into roff (man pages)

%define OUR_GOPATH %{_topdir}/.gopath
Vendor:         Microsoft Corporation
Distribution:   Mariner

%prep
%setup -q -n %{name}-%{version} -c

%build
export GOPATH=%{OUR_GOPATH}
export GOCACHE=%{OUR_GOPATH}/.cache
export CGO_ENABLED=0
export GO111MODULE=on

cd %{_topdir}/BUILD/%{name}-%{version}/go-md2man-%{version}
go build -mod vendor -o go-md2man

%install
mkdir -p "%{buildroot}%{_bindir}"
cp -aT go-md2man-%{version}/go-md2man %{buildroot}%{_bindir}/go-md2man

# copy legal files
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
cp go-md2man-%{version}/LICENSE.md %{buildroot}%{_docdir}/%{name}-%{version}/LICENSE.md

%files
%license %{_docdir}/%{name}-%{version}/LICENSE.md
%{_bindir}/go-md2man

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.2-1
- Auto-upgrade to 2.0.2 - Azure Linux 3.0 - package upgrades

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.1-21
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 2.0.1-20
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.1-19
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.1-18
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.1-17
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.1-16
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.1-15
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.1-14
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.1-13
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.1-12
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 2.0.1-11
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.0.1-10
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.0.1-9
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 2.0.1-8
- Bump release to rebuild with golang 1.18.3

* Fri Mar 04 2022 Andrew Phelps <anphel@microsoft.com> 2.0.1-1
- Update to version 2.0.1
- License verified

* Fri Jun 18 2021 Henry Li <lihl@microsoft.com> 2.0.0-7
- Provides go-go-md2man.
- Fix linting errors.

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 2.0.0-6
- Increment release to force republishing using golang 1.15.13.

* Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 2.0.0-5
- Increment release to force republishing using golang 1.15.

* Wed May 20 2020 Joe Schmitt <joschmit@microsoft.com> 2.0.0-4
- Remove reliance on existing GOPATH environment variable.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.0.0-3
- Added %%license line automatically

* Fri May 01 2020 Emre Girgin <mrgirgin@microsoft.com> 2.0.0-2
- Renaming go to golang

* Fri Apr 03 2020 Mohan Datla <mdatla@microsoft.com> 2.0.0-1
- Original version for CBL-Mariner.
