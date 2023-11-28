%global debug_package %{nil}
Summary:       Git extension for versioning large files
Name:          git-lfs
Version:       3.1.4
Release:       15%{?dist}
Group:         System Environment/Programming
Vendor:        Microsoft Corporation
Distribution:  Mariner
License:       MIT
URL:           https://github.com/git-lfs/git-lfs
Source0:       https://github.com/git-lfs/git-lfs/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/git-lfs/git-lfs/archive/v%{version}.tar.gz -O git-lfs-%%{version}.tar.gz
#   2. tar -xf git-lfs-%%{version}.tar.gz
#   3. cd git-lfs-%%{version}
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
Source1:       %{name}-%{version}-vendor.tar.gz

BuildRequires: golang
BuildRequires: which
BuildRequires: rubygem-ronn
BuildRequires: tar
BuildRequires: git
Requires:      git
%define our_gopath %{_topdir}/.gopath

%description
Git LFS is a command line extension and specification for managing large files with Git

%prep
%autosetup

%build
tar --no-same-owner -xf %{SOURCE1}
export GOPATH=%{our_gopath}
export GOFLAGS="-buildmode=pie -trimpath -mod=vendor -modcacherw -ldflags=-linkmode=external"
go generate ./commands
go build .
export PATH=$PATH:%{gem_dir}/bin
make man %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -D git-lfs %{buildroot}%{_bindir}/git-lfs
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man5
install -D man/*.1 %{buildroot}%{_mandir}/man1
install -D man/*.5 %{buildroot}%{_mandir}/man5

%check
go test -mod=vendor ./...

%post
git lfs install --system

%preun
git lfs uninstall

%files
%defattr(-,root,root,-)
%doc LICENSE.md README.md
%{_bindir}/git-lfs
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.4-15
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 3.1.4-14
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.4-13
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.4-12
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.4-11
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.4-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.4-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.4-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.4-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.1.4-6
- Bump release to rebuild with go 1.19.4

*   Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 3.1.4-5
-   Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717.

*   Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.1.4-4
-   Bump release to rebuild with go 1.18.8

*   Wed Sep 28 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> 3.1.4-3
-   Initial CBL-Mariner import from Photon (license: Apache2)
-   License verified
-   Add git-lfs vendor cache check setion and update build section commands as needed.

*   Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 3.1.4-2
-   Bump up version to compile with new go

*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.1.4-1
-   Automatic Version Bump

*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 2.13.3-2
-   Bump up version to compile with new go

*   Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 2.13.3-1
-   Automatic Version Bump

*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 2.12.0-3
-   Bump up version to compile with new go

*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 2.12.0-2
-   Bump up version to compile with new go

*   Fri Sep 18 2020 Him Kalyan Bordoloi <bordoloih@vmware.com>  2.12.0-1
-   Initial release.
