%global debug_package %{nil}

Summary:        Container Network Interface (CNI) plugins
Name:           cni
Version:        0.9.1
Release:        5%{?dist}
License:        ASL 2.0
URL:            https://github.com/containernetworking/plugins
#Source0:       https://github.com/containernetworking/plugins/archive/refs/tags/v0.9.1.tar.gz
Source0:        %{name}-v%{version}.tar.gz
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  golang >= 1.5
%define _default_cni_plugins_dir /opt/cni/bin

%description
The CNI (Container Network Interface) project consists of a specification and libraries for writing plugins to configure network interfaces in Linux containers, along with a number of supported plugins.

%prep
%setup -n plugins-%{version}

%build
./build_linux.sh

%install
install -vdm 755 %{buildroot}%{_default_cni_plugins_dir}
install -vpm 0755 -t %{buildroot}%{_default_cni_plugins_dir} bin/*

# running this requires sudo and some debugging 
# (miss cnitools which are not part of the src tarball)
# %check
# ./test_linux.sh

%post

%postun

%files
%defattr(-,root,root)
%license LICENSE
%{_default_cni_plugins_dir}/*

%changelog
* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 0.9.1-5
- Bump release to force rebuild with golang 1.16.15

* Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 0.9.1-4
- Bump release to force rebuild with golang 1.16.14

* Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 0.9.1-3
- Increment release for force republishing using golang 1.16.12

* Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 0.9.1-2
- Increment release for force republishing using golang 1.16.9

*   Fri Aug 06 2021 Nicolas Guibourge <nicolasg@microsoft.com> 0.9.1-1
-   Move to version 0.9.1 and build using golang 1.16.7.
*   Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 0.7.5-7
-   Increment release to force republishing using golang 1.15.13.
*   Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 0.7.5-6
-   Increment release to force republishing using golang 1.15.11.
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
