%global debug_package %{nil}
Summary:        NVIDIA container runtime
Name:           nvidia-container-runtime
Version:        3.13.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/NVIDIA/nvidia-container-runtime
#Source0:       https://github.com/NVIDIA/%%{name}/archive/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Obsoletes: nvidia-container-runtime < 2.0.0
Requires: nvidia-container-toolkit >= 1.13.5, nvidia-container-toolkit < 2.0.0
Requires:       libseccomp
# NVIDIA now includes the runtime within the toolkit installs itself.
# Previously there were independent installs of the runtime and the toolkit
# but with v3.9.0 and beyond the nvidia-container-runtime package no longer builds.
#
# The package is now a meta package that only forces the toolkit installation.

%description
Provides a modified version of runc allowing users to run GPU enabled
containers.

%prep
%setup -q

%install

%files
%license LICENSE


%changelog
* Mon Jul 10 2023 Henry Li <lihl@microsoft.com> - 3.13.0-1
- Upgrade to version 3.13.0
- Add nvidia-container-toolkit minimum version 1.13.5 dependency

* Wed Sep 21 2022 Henry Li <lihl@microsoft.com> - 3.11.0-1
- Upgrade to version 3.11.0
- Add nvidia-container-toolkit minimum version 1.11.0 dependency

* Wed Mar 30 2022 Adithya Jayachandran <adjayach@microsoft.com> - 3.9.0-1
- Bumped version to 3.9.0
- Package is officially included in toolkit install, this is a meta package
- Added nvidia-container-toolkit minimum version 1.9.0 dependence

* Tue Mar 29 2022 Adithya Jayachandran <adjayach@microsoft.com> - 3.5.0-1
- Ported nvidia container runtime update v3.5.0 to 2.0
- Added dependence on nvidia-container-toolkit >= 1.5.0
- Change directory structure for build output

* Wed Nov 17 2021 Mateusz Malisz <mateusz.malisz@microsoft.com> 3.4.2-5
- Move buildroot directory tree creation to install step
- Use make macros.

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
