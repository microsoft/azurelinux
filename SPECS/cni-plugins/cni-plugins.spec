Summary:        Container Network Interface (CNI) plugins
Name:           cni-plugins
Version:        1.3.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
# cni moved to https://github.com/containernetworking/cni/issues/667#issuecomment-491693752
URL:            https://github.com/containernetworking/plugins
#Source0:       https://github.com/containernetworking/plugins/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define _default_cni_plugins_dir /opt/cni/bin
BuildRequires:  golang >= 1.5
Provides:       kubernetes-cni

%description
The CNI (Container Network Interface) project consists of a specification and libraries for writing plugins to configure network interfaces in Linux containers, along with a number of supported plugins.

%prep
%setup -q -n plugins-%{version}

%build
./build_linux.sh -ldflags "-X github.com/containernetworking/plugins/pkg/utils/buildversion.BuildVersion=v%{version}"

%install
install -vdm 755 %{buildroot}%{_default_cni_plugins_dir}
install -vpm 0755 -t %{buildroot}%{_default_cni_plugins_dir} bin/*

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post
%postun

%files
%defattr(-,root,root)
%license LICENSE
%{_default_cni_plugins_dir}/*

%changelog
* Wed Oct 18 2023 Mateusz Gozdek <mgozdek@microsoft.com> - 1.3.0-1
- Make plugin binaries correctly print version
- Upgrade to version 1.3.0

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.9.1-16
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 0.9.1-15
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.9.1-14
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.9.1-13
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.9.1-12
- Bump release to rebuild with go 1.19.10

* Mon May 22 2023 Betty Lakes <bettylakes@microsoft.com> - 0.9.1-11
- Added Provides for kubernetes-cni

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.9.1-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.9.1-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.9.1-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.9.1-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.9.1-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 0.9.1-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.9.1-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.9.1-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 0.9.1-2
- Bump release to rebuild with golang 1.18.3

* Tue Aug 17 2021 Henry Li <lihl@microsoft.com> - 0.8.1-1
- Rename package name from cni to cni-plugins
- Upgrade to version 0.9.1

*   Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 0.7.5-5
-   Increment release to force republishing using golang 1.15.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.7.5-4
-   Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 0.7.5-3
-   Renaming go to golang

*   Tue Mar 07 2020 Paul Monson <paulmon@microsoft.com> 0.7.5-3
-   Fix Source0. License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.7.5-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Apr 02 2019 Ashwin H <ashwinh@vmware.com> 0.7.5-1
-   Update cni to v0.7.5

*   Tue Dec 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.6.0-1
-   cni v0.6.0.

*   Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 0.5.1-1
-   Version update

*   Thu Feb 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.4.0-1
-   Add CNI plugins package to PhotonOS.
