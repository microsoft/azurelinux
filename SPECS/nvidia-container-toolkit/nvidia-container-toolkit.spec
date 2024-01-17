%global debug_package %{nil}
Summary:        NVIDIA container runtime hook
Name:           nvidia-container-toolkit
Version:        1.13.5
Release:        3%{?dist}
License:        ALS2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/NVIDIA/nvidia-container-toolkit
#Source0:       https://github.com/NVIDIA/%%{name}/archive/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/NVIDIA/%%{name}/archive/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
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
BuildRequires:  golang >= 1.20.7
Obsoletes: nvidia-container-runtime <= 3.5.0-1, nvidia-container-runtime-hook <= 1.4.0-2
Provides: nvidia-container-runtime
Provides: nvidia-container-runtime-hook
Requires: libnvidia-container-tools >= 1.13.5, libnvidia-container-tools < 2.0.0

%description
Provides a OCI hook to enable GPU support in containers.

# The BASE package consists of the NVIDIA Container Runtime and the NVIDIA Container Toolkit CLI.
# This allows the package to be installed on systems where no NVIDIA Container CLI is available.
%package base
Summary: NVIDIA Container Toolkit Base
Obsoletes: nvidia-container-runtime <= 3.5.0-1, nvidia-container-runtime-hook <= 1.4.0-2
Provides: nvidia-container-runtime
# Since this package allows certain components of the NVIDIA Container Toolkit to be installed separately
# it conflicts with older versions of the nvidia-container-toolkit package that also provide these files.
Conflicts: nvidia-container-toolkit <= 1.10.0-1

%description base
Provides tools such as the NVIDIA Container Runtime and NVIDIA Container Toolkit CLI to enable GPU support in containers.

%prep
%autosetup -p1
tar -xvf %{SOURCE1}

%build
go build -ldflags "-s -w " -o "nvidia-container-runtime-hook" ./cmd/nvidia-container-runtime-hook
go build -ldflags "-s -w " -o "nvidia-container-runtime" ./cmd/nvidia-container-runtime
go build -ldflags "-s -w " -o "nvidia-ctk" ./cmd/nvidia-ctk

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 -t %{buildroot}%{_bindir} nvidia-container-runtime-hook
install -m 755 -t %{buildroot}%{_bindir} nvidia-container-runtime
install -m 755 -t %{buildroot}%{_bindir} nvidia-ctk

cp config/config.toml.rpm-yum config.toml
mkdir -p %{buildroot}%{_sysconfdir}/nvidia-container-runtime
install -m 644 -t %{buildroot}%{_sysconfdir}/nvidia-container-runtime config.toml

mkdir -p %{buildroot}%{_libexecdir}/oci/hooks.d
install -m 755 -t %{buildroot}%{_libexecdir}/oci/hooks.d oci-nvidia-hook

mkdir -p %{buildroot}%{_datadir}/containers/oci/hooks.d
install -m 644 -t %{buildroot}%{_datadir}/containers/oci/hooks.d oci-nvidia-hook.json

%posttrans
ln -sf %{_bindir}/nvidia-container-runtime-hook %{_bindir}/nvidia-container-toolkit

%postun
rm -f %{_bindir}/nvidia-container-toolkit

%files
%license LICENSE
%{_bindir}/nvidia-container-runtime-hook
%{_libexecdir}/oci/hooks.d/oci-nvidia-hook
%{_datadir}/containers/oci/hooks.d/oci-nvidia-hook.json

%files base
%license LICENSE
%config %{_sysconfdir}/nvidia-container-runtime/config.toml
%{_bindir}/nvidia-container-runtime
%{_bindir}/nvidia-ctk

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.13.5-3
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.13.5-2
- Bump release to rebuild with updated version of Go.

* Thu Aug 24 2023 Henry Li <lihl@microsoft.com> - 1.13.5-1
- Upgrade to version 1.13.5
- Enforce golang to be equal to or greater than v1.20.7

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-11
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-10
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-9
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-8
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-7
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-6
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-5
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-4
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.11.0-3
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.11.0-2
- Bump release to rebuild with go 1.18.8

* Wed Sep 21 2022 Henry Li <lihl@microsoft.com> - 1.11.0-1
- Upgrade to version 1.11.0
- Remove patch that no longer applies to v1.11.0
- Replace nvidia-container-toolkit with nvidia-container-runtime-hook
- Build and install nvidia-ctk binary
- Use config.toml.rpm-yum, which replaces config.toml.centos
- Add nlibnvidia-container-tools minimum version 1.11.0 dependency
- Add the nvidia-container-runtime-toolkit-base package

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.9.0-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.9.0-2
- Bump release to rebuild with golang 1.18.3

* Wed Mar 30 2022 Adithya Jayachandran <adjayach@microsoft.com> - 1.9.0-1
- Update toolkit version to 1.9.0
- NVIDIA unified release package

* Tue Sep 28 2021 Adithya Jayachandran <adjayach@microsoft.com> - 1.5.1-1
- Update toolkit version to 1.5.1

* Fri Aug 06 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.4.2-4
- Increment release to force republishing using golang 1.16.7.

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 1.4.2-3
- Increment release to force republishing using golang 1.15.13.

* Mon Apr 26 2021 Joseph Knierman <joknierm@microsoft.com> - 1.4.2-2
- License verified
- Initial CBL-Mariner import from NVIDIA (license: ASL 2.0).

* Fri Feb 05 2021 NVIDIA CORPORATION <cudatools@nvidia.com> 1.4.2-1
- Add dependence on libnvidia-container-tools >= 1.3.3

* Mon Jan 25 2021 NVIDIA CORPORATION <cudatools@nvidia.com> 1.4.1-1
- Ignore NVIDIA_VISIBLE_DEVICES for containers with insufficent privileges
- Add dependence on libnvidia-container-tools >= 1.3.2

* Fri Dec 11 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.4.0-1
- Add 'compute' capability to list of defaults
- Add dependence on libnvidia-container-tools >= 1.3.1

* Wed Sep 16 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.3.0-1
- Promote 1.3.0-0.1.rc.2 to 1.3.0-1
- Add dependence on libnvidia-container-tools >= 1.3.0

* Mon Aug 10 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.3.0-0.1.rc.2
- 2c180947 Add more tests for new semantics with device list from volume mounts
- 7c003857 Refactor accepting device lists from volume mounts as a boolean

* Fri Jul 24 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.3.0-0.1.rc.1
- b50d86c1 Update build system to accept a TAG variable for things like rc.x
- fe65573b Add common CI tests for things like golint, gofmt, unit tests, etc.
- da6fbb34 Revert "Add ability to merge envars of the form NVIDIA_VISIBLE_DEVICES_*"
- a7fb3330 Flip build-all targets to run automatically on merge requests
- 8b248b66 Rename github.com/NVIDIA/container-toolkit to nvidia-container-toolkit
- da36874e Add new config options to pull device list from mounted files instead of ENVVAR

* Wed Jul 22 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.2.1-1
- 4e6e0ed4 Add 'ngx' to list of *all* driver capabilities
- 2f4af743 List config.toml as a config file in the RPM SPEC

* Wed Jul 08 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.2.0-1
- 8e0aab46 Fix repo listed in changelog for debian distributions
- 320bb6e4 Update dependence on libnvidia-container to 1.2.0
- 6cfc8097 Update package license to match source license
- e7dc3cbb Fix debian copyright file
- d3aee3e0 Add the 'ngx' driver capability

* Wed Jun 03 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.1.2-1
- c32237f3 Add support for parsing Linux Capabilities for older OCI specs

* Tue May 19 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.1.1-1
- d202aded Update dependence to libnvidia-container 1.1.1

* Fri May 15 2020 NVIDIA CORPORATION <cudatools@nvidia.com> 1.1.0-1
- 4e4de762 Update build system to support multi-arch builds
- fcc1d116 Add support for MIG (Multi-Instance GPUs)
- d4ff0416 Add ability to merge envars of the form NVIDIA_VISIBLE_DEVICES_* 
- 60f165ad Add no-pivot option to toolkit
