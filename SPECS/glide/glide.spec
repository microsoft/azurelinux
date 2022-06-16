Summary:        Vendor Package Management for Golang
Name:           glide
Version:        0.13.3
Release:        11%{?dist}
License:        MIT
URL:            https://github.com/Masterminds/glide
# Source0:      https://github.com/Masterminds/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  git
BuildRequires:  golang
BuildRequires:  perl
BuildRequires:  ca-certificates

%description
Glide is a tool for managing the vendor directory within a Go package.

%define OUR_GOPATH %{_topdir}/.gopath

%prep
%autosetup -p1

%build
export GO111MODULE=auto
export GOPATH=%{OUR_GOPATH}
mkdir -p ${GOPATH}/src/github.com/Masterminds/glide
cp -r * ${GOPATH}/src/github.com/Masterminds/glide/.
pushd ${GOPATH}/src/github.com/Masterminds/glide
make VERSION=%{version} build %{?_smp_mflags}
popd

%check
export GO111MODULE=auto
export GOPATH=%{OUR_GOPATH}
pushd ${GOPATH}/src/github.com/Masterminds/glide
make test %{?_smp_mflags}
popd

%install
export GO111MODULE=auto
export GOPATH=%{OUR_GOPATH}
pushd ${GOPATH}/src/github.com/Masterminds/glide
make install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ ./glide
popd

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/glide

%changelog
*   Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 0.13.3-11
-   Bump release to rebuild with golang 1.18.3

*   Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 0.13.3-10
-   Bump release to force rebuild with golang 1.16.15

*   Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 0.13.3-9
-   Bump release to force rebuild with golang 1.16.14

*   Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 0.13.3-8
-   Increment release for force republishing using golang 1.16.12

*   Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 0.13.3-7
-   Increment release for force republishing using golang 1.16.9

*   Fri Sep 17 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.13.3-6
-   Initial CBL-Mariner import from Photon (license: Apache2)
-   License verified

*   Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 0.13.3-5
-   Bump up version to compile with new go

*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 0.13.3-4
-   Bump up version to compile with new go

*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 0.13.3-3
-   Bump up version to compile with new go

*   Tue Oct 06 2020 Ashwin H <ashwinh@vmware.com> 0.13.3-2
-   Build using go 1.14

*   Tue Jun 30 2020 Gerrit Photon <photon-checkins@vmware.com> 0.13.3-1
-   Automatic Version Bump

*   Mon Jan 21 2019 Bo Gan <ganb@vmware.com> 0.13.1-4
-   Build using go 1.9.7

*   Fri Nov 23 2018 Ashwin H <ashwinh@vmware.com> 0.13.1-3
-   Fix %check

*   Mon Sep 24 2018 Tapas Kundu <tkundu@vmware.com> 0.13.1-2
-   Build using go version 1.9

*   Thu Sep 13 2018 Michelle Wang <michellew@vmware.com> 0.13.1-1
-   Update version to 0.13.1.

*   Mon Aug 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.12.3-1
-   glide for PhotonOS.
