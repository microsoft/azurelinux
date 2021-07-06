Summary:        Vendor Package Management for Goland
Name:           glide
Version:        0.13.3
Release:        2%{?dist}
License:        MIT
URL:            https://github.com/Masterminds/glide
#Source0:       https://github.com/Masterminds/%{name}/archive/v%{version}.tar.gz
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

%setup -q

%build
export GOPATH=%{OUR_GOPATH}
mkdir -p ${GOPATH}/src/github.com/Masterminds/glide
cp -r * ${GOPATH}/src/github.com/Masterminds/glide/.
pushd ${GOPATH}/src/github.com/Masterminds/glide
make VERSION=%{version} build
popd

%check
export GOPATH=%{OUR_GOPATH}
pushd ${GOPATH}/src/github.com/Masterminds/glide
make test
popd

%install
export GOPATH=%{OUR_GOPATH}
pushd ${GOPATH}/src/github.com/Masterminds/glide
make install
install -vdm 755 %{buildroot}%{_bindir}
install -vpm 0755 -t %{buildroot}%{_bindir}/ ./glide
popd

%files
%defattr(-,root,root)
%{_bindir}/glide

%changelog
*   Tue Jun 02 2020 Paul Monson <paulmon@microsoft.com> 0.13.3-2
-   Rename go to golang
-   Add ca-certificates temporarily
-   Update GOPATH handling
*   Thu May 21 2020 Mateusz Malisz <mamalisz@microsoft.com> 0.13.3-1
-   Update to version 0.13.3
-   Remove dependency on go 1.9
-   Add quiet option to setup
*   Tue Apr 07 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.13.1-6
-   Adding a "#Source0" comment pointing to the online sources.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.13.1-5
-   Initial Mariner version.
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
