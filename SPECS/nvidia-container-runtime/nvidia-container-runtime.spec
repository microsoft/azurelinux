%global debug_package %{nil}
Summary:        NVIDIA container runtime
Name:           nvidia-container-runtime
Version:        3.5.0
Release:        5%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/NVIDIA/nvidia-container-runtime
#Source0:       https://github.com/NVIDIA/%%{name}/archive/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  golang
Requires:       libseccomp

%description
Provides a modified version of runc allowing users to run GPU enabled
containers.

%prep
%setup -q

%build
make build
mkdir -p %{buildroot}%{_bindir}
cp %{name} %{buildroot}%{_bindir}

%install
install -m 755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%{_bindir}/%{name}

%changelog
* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 3.5.0-5
- Bump release to force rebuild with golang 1.16.15

* Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 3.5.0-4
- Bump release to force rebuild with golang 1.16.14

* Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 3.5.0-3
- Increment release for force republishing using golang 1.16.12

* Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 3.5.0-2
- Increment release for force republishing using golang 1.16.9

* Thu Sep 30 2021 Adithya Jayachandran <adjayach@microsoft.com> - 3.5.0-1
- Updated nvidia container runtime to v3.5.0.
- Added dependence on nvidia-container-toolkit >= 1.5.0
- Change directory structure for build output

* Fri Aug 06 2021 Nicolas Guibourge <nicolasg@microsoft.com> 3.4.2-5
- Increment release to force republishing using golang 1.16.7.

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 3.4.2-4
- Increment release to force republishing using golang 1.15.13.

* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 3.4.2-3
- Increment release to force republishing using golang 1.15.11.

* Wed Apr 21 2021 Joseph Knierman <jknierman@microsoft.com> - 3.4.2-2
- License verified
- Initial CBL-Mariner import from NVIDIA (license: ASL 2.0).

* Fri Feb 05 2021 NVIDIA CORPORATION <cudatools@nvidia.com> 3.4.2-1
- Add dependence on nvidia-container-toolkit >= 1.4.2

* Mon Jan 25 2021 NVIDIA CORPORATION <cudatools@nvidia.com> 3.4.1-1
- Update README to list 'compute' as part of the default capabilities
- Switch to gomod for vendoring
- Update to Go 1.15.6 for builds
- Add dependence on nvidia-container-toolkit >= 1.4.1

* Wed Sep 16 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 3.4.0-1
- Bump version to v3.4.0
- Add dependence on nvidia-container-toolkit >= 1.3.0

* Wed Jul 08 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 3.3.0-1
- e550cb15 Update package license to match source license
- f02eef53 Update project License
- c0fe8aae Update dependence on nvidia-container-toolkit to 1.2.0

* Fri May 15 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 3.2.0-1
- e486a70e Update build system to support multi-arch builds
- 854f4c48 Require new MIG changes
