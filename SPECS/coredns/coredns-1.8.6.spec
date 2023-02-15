%global debug_package %{nil}

Summary:        Fast and flexible DNS server
Name:           coredns
Version:        1.8.6
Release:        7%{?dist}
License:        Apache License 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/coredns/coredns
#Source0:       https://github.com/coredns/coredns/archive/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/coredns/coredns/archive/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         makefile-buildoption-commitnb.patch

BuildRequires:  golang >= 1.12

%description
CoreDNS is a fast and flexible DNS server.

%prep
%autosetup -p1

%build
# create vendor folder from the vendor tarball and set vendor mode
tar -xf %{SOURCE1} --no-same-owner
export BUILDOPTS="-mod=vendor -v"
# set commit number that correspond to the github tag for that version
export GITCOMMIT="13a9191efb0574cc92ed5ffd55a1f144b840d668"
make

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} %{name}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}

%changelog
* Wed Feb 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.6-7
- Bump release to rebuild with go 1.19.6

* Tue Dec 13 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.8.6-6
- Bump release to rebuild with go 1.18.8-2

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.8.6-5
- Bump release to rebuild with go 1.18.8

* Wed Aug 17 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.8.6-4
- Bump to rebuild with golang 1.18.5-1

* Tue Jun 07 2022 Andrew Phelps <anphel@microsoft.com> - 1.8.6-3
- Bumping release to rebuild with golang 1.18.3

* Fri Apr 29 2022 chalamalasetty <chalamalasetty@live.com> - 1.8.6-2
- Bumping 'Release' to rebuild with updated Golang version 1.16.15-2.

* Wed Apr 20 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.8.6-1
- Update to version  "1.8.6".

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 1.8.4-4
- Bump release to force rebuild with golang 1.16.15

* Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 1.8.4-3
- Bump release to force rebuild with golang 1.16.14

* Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 1.8.4-2
- Increment release for force republishing using golang 1.16.12

* Tue Dec 28 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.8.4-1
- Update to version  "1.8.4".

* Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 1.8.0-2
- Increment release for force republishing using golang 1.16.9

* Fri Aug 20 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.8.0-1
- Update to version  "1.8.0".

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 1.7.0-3
- Increment release to force republishing using golang 1.15.13.
* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.7.0-2
- Increment release to force republishing using golang 1.15.11.
* Wed Jan 20 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.7.0-1
- Original version for CBL-Mariner.
