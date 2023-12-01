Summary:        FUSE adapter - Azure Storage Blobs
Name:           blobfuse
Version:        1.4.5
Release:        13%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/Azure/azure-storage-fuse/
Source0:        https://github.com/Azure/azure-storage-fuse/archive/%{name}-%{version}.tar.gz
BuildRequires:  boost-devel
BuildRequires:  boost-static
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  fuse-devel
BuildRequires:  gcc
BuildRequires:  gnutls
BuildRequires:  gnutls-devel
BuildRequires:  golang
BuildRequires:  libgcrypt-devel
BuildRequires:  make
BuildRequires:  pkg-config
BuildRequires:  util-linux-devel
Requires:       fuse

%description
FUSE adapter - Azure Storage Blobs

%prep
%autosetup -n azure-storage-fuse-blobfuse-%{version}

%build
CFLAGS="`echo " %{build_cflags} -Wno-error=type-limits "`"
CXXFLAGS="`echo " %{build_cflags} -Wno-error=type-limits "`"
export CFLAGS
export CXXFLAGS
./build.sh

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 build/blobfuse %{buildroot}%{_bindir}/

%files
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/blobfuse

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.5-13
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.4.5-12
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.5-11
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.5-10
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.5-9
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.5-8
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.5-7
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.5-6
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.5-5
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.5-4
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.4.5-3
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.4.5-2
- Bump release to rebuild with go 1.18.8

* Sat Sep 17 2022 Muhammad Falak <mwani@microsoft.com> - 1.4.5-1
- Bump version to 1.4.5

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.4.4-2
- Bump release to rebuild against Go 1.18.5

* Mon Jul 25 2022 Betty Lakes <bettylakes@microsoft.com> - 1.4.4-1
- Upgrade to latest upstream version

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.4.2-3
- Bump release to rebuild with golang 1.18.3

* Wed Dec 01 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.4.2-2
- Add back in gcc11 compilation error mitigation

* Mon Nov 29 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.4.2-1
- Upgrade to latest upstream version
- Remove %%clean section

* Fri Nov 13 2021 Andrew Phelps <anphel@microsoft.com> - 1.3.6-5
- Fix gcc11 compilation errors

* Tue Sep 21 2021 Henry Li <lihl@microsoft.com> - 1.3.6-4
- Remove util-linux-libs from BR 

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> - 1.3.6-3
- Increment release to force republishing using golang 1.15.13.

* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.3.6-2
- Increment release to force republishing using golang 1.15.11.

* Tue Feb 02 2021 Henry Beberman <henry.beberman@microsoft.com> - 1.3.6-1
- Add blobfuse spec
- License verified
- Original version for CBL-Mariner
