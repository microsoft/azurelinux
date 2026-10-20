%global debug_package %{nil}
Summary:        NVIDIA Container Toolkit
Name:           nvidia-container-toolkit
Version:        1.20.1
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
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
BuildRequires:  golang >= 1.26.0
BuildRequires:  systemd-rpm-macros

# Distributions that don't define the udev rules directory macro fall back to
# the default location.
%{!?_udevrulesdir: %global _udevrulesdir %{_prefix}/lib/udev/rules.d}

Obsoletes: nvidia-container-runtime <= 3.5.0-1, nvidia-container-runtime-hook <= 1.4.0-2
Provides: nvidia-container-runtime
Provides: nvidia-container-runtime-hook
Requires: libnvidia-container-tools = %{version}
Requires: nvidia-container-toolkit-base == %{version}-%{release}

%description
Provides tools and utilities to enable GPU support in containers.

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
%autosetup -p1 -a1

%build
go build -ldflags "-s -w -X github.com/NVIDIA/nvidia-container-toolkit/internal/info.version=%{version}" -o "nvidia-container-runtime-hook" ./cmd/nvidia-container-runtime-hook
go build -ldflags "-s -w -X github.com/NVIDIA/nvidia-container-toolkit/internal/info.version=%{version}" -o "nvidia-container-runtime" ./cmd/nvidia-container-runtime
go build -ldflags "-s -w -X github.com/NVIDIA/nvidia-container-toolkit/internal/info.version=%{version}" -o "nvidia-ctk" ./cmd/nvidia-ctk
go build -ldflags "-s -w -X github.com/NVIDIA/nvidia-container-toolkit/internal/info.version=%{version}" -o "nvidia-cdi-hook" ./cmd/nvidia-cdi-hook

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}/nvidia-cdi-refresh.service.d
mkdir -p %{buildroot}%{_presetdir}
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_sysconfdir}/nvidia-container-toolkit
install -m 755 -t %{buildroot}%{_bindir} nvidia-container-runtime-hook
install -m 755 -t %{buildroot}%{_bindir} nvidia-container-runtime
install -m 755 -t %{buildroot}%{_bindir} nvidia-ctk
install -m 755 -t %{buildroot}%{_bindir} nvidia-cdi-hook
install -m 644 -t %{buildroot}%{_unitdir} deployments/systemd/nvidia-cdi-refresh.service
install -m 644 -t %{buildroot}%{_unitdir} deployments/systemd/nvidia-cdi-refresh.path
install -m 644 -t %{buildroot}%{_presetdir} deployments/systemd/90-nvidia-container-toolkit.preset
install -m 644 -t %{buildroot}%{_udevrulesdir} deployments/udev/99-nvidia-cdi-refresh.rules
install -m 644 -t %{buildroot}%{_unitdir}/nvidia-cdi-refresh.service.d deployments/systemd/10-container-engines.conf
install -m 644 -t %{buildroot}%{_sysconfdir}/nvidia-container-toolkit deployments/systemd/nvidia-cdi-refresh.env
cat >> %{buildroot}%{_sysconfdir}/nvidia-container-toolkit/nvidia-cdi-refresh.env << 'EOF'

# Azure Linux: skip libnvidia-sandboxutils when generating the CDI specification.
# Its initialization fails on Azure Linux's 64-bit-only library layout and prints
# "ERROR: init 250 result=11"; discovery falls back to NVML either way.
NVIDIA_CTK_CDI_GENERATE_FEATURE_FLAGS=disable-nvsandboxutils
EOF

%post
if [ $1 -gt 1 ]; then  # only on package upgrade
  mkdir -p %{_localstatedir}/lib/rpm-state/nvidia-container-toolkit
  cp -af %{_bindir}/nvidia-container-runtime-hook %{_localstatedir}/lib/rpm-state/nvidia-container-toolkit
fi

%posttrans
if [ ! -e %{_bindir}/nvidia-container-runtime-hook ]; then
  # repairing lost file nvidia-container-runtime-hook
  cp -avf %{_localstatedir}/lib/rpm-state/nvidia-container-toolkit/nvidia-container-runtime-hook %{_bindir}
fi
rm -rf %{_localstatedir}/lib/rpm-state/nvidia-container-toolkit
ln -sf %{_bindir}/nvidia-container-runtime-hook %{_bindir}/nvidia-container-toolkit

%postun
if [ "$1" = 0 ]; then  # package is uninstalled, not upgraded
  if [ -L %{_bindir}/nvidia-container-toolkit ]; then rm -f %{_bindir}/nvidia-container-toolkit; fi
fi

%post base
# Generate the default config; If this file already exists no changes are made,
# except for the Azure Linux default below.
#
# Azure Linux: skip libnvidia-sandboxutils for JIT-CDI unless nvcdi-feature-flags
# is already set in [nvidia-container-runtime.modes.jit-cdi]. Its initialization
# fails on Azure Linux's 64-bit-only library layout and writes
# "ERROR: init 250 result=11" into GPU containers' output; discovery falls back
# to NVML either way. To opt out, set nvcdi-feature-flags = [] in that table.
config_file=%{_sysconfdir}/nvidia-container-runtime/config.toml
# Reads nvidia-ctk's normalized TOML from stdin, so quoted keys, dotted keys, and
# inline tables are recognized the same way the runtime parses them.
jit_cdi_feature_flags_set() {
  table=
  while read -r line; do
    case "${line}" in
      "["*) table="${line}" ;;
      "nvcdi-feature-flags ="*|"nvcdi-feature-flags="*)
        [ "${table}" = "[nvidia-container-runtime.modes.jit-cdi]" ] && return 0 ;;
    esac
  done
  return 1
}
jit_cdi_default=
if ! %{_bindir}/nvidia-ctk --quiet config --config-file="${config_file}" 2>/dev/null | jit_cdi_feature_flags_set; then
  jit_cdi_default="--set nvidia-container-runtime.modes.jit-cdi.nvcdi-feature-flags=disable-nvsandboxutils"
fi
%{_bindir}/nvidia-ctk --quiet config --config-file="${config_file}" --in-place ${jit_cdi_default}

%systemd_post nvidia-cdi-refresh.path nvidia-cdi-refresh.service

%preun base
%systemd_preun nvidia-cdi-refresh.path nvidia-cdi-refresh.service

%postun base
%systemd_postun nvidia-cdi-refresh.path nvidia-cdi-refresh.service

%posttrans base
# Remove enablement links left by older packages that installed these units in
# /etc so systemd can re-enable them from the current unit directory.
stale_enabled_units_to_reenable=
for unit in nvidia-cdi-refresh.path nvidia-cdi-refresh.service; do
	old_unit="%{_sysconfdir}/systemd/system/${unit}"
	wants_link="%{_sysconfdir}/systemd/system/multi-user.target.wants/${unit}"
	if [ -L "${wants_link}" ]; then
		case "$(readlink "${wants_link}")" in
			"${old_unit}"|"../${unit}")
				rm -f "${wants_link}"
				stale_enabled_units_to_reenable="${stale_enabled_units_to_reenable} ${unit}"
				;;
		esac
	fi
done

# Reload udev rules and generate a CDI specification without requiring the
# NVIDIA driver or systemd to be active during package installation.
if command -v udevadm >/dev/null 2>&1; then
	udevadm control --reload-rules >/dev/null 2>&1 || :
fi
if command -v systemctl >/dev/null 2>&1; then
	systemctl daemon-reload >/dev/null 2>&1 || :
	if [ -n "${stale_enabled_units_to_reenable}" ]; then
		systemctl enable ${stale_enabled_units_to_reenable} >/dev/null 2>&1 || :
	fi
	systemctl start nvidia-cdi-refresh.path >/dev/null 2>&1 || :
	systemctl start nvidia-cdi-refresh.service >/dev/null 2>&1 || :
fi

%files
%license LICENSE
%{_bindir}/nvidia-container-runtime-hook

%files base
%license LICENSE
%{_bindir}/nvidia-container-runtime
%{_bindir}/nvidia-ctk
%{_bindir}/nvidia-cdi-hook
%{_unitdir}/nvidia-cdi-refresh.service
%{_unitdir}/nvidia-cdi-refresh.path
%{_presetdir}/90-nvidia-container-toolkit.preset
%{_udevrulesdir}/99-nvidia-cdi-refresh.rules
%{_unitdir}/nvidia-cdi-refresh.service.d/10-container-engines.conf
%config(noreplace) %{_sysconfdir}/nvidia-container-toolkit/nvidia-cdi-refresh.env

%changelog
* Mon Oct 19 2026 Henry Li <lihl@microsoft.com> - 1.20.1-1
- Upgrade to version 1.20.1
- Add upstream CDI refresh service, triggers, and configuration
- Disable libnvidia-sandboxutils by default for JIT-CDI and the CDI refresh service
- Require libnvidia-container-tools of the same version
- Remove security patches included upstream

* Fri Jul 10 2026 Henry Li <lihl@microsoft.com> - 1.17.8-4
- Remove golang version cap

* Wed May 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.17.8-3
- Patch for CVE-2026-39834, CVE-2026-39830

* Mon Jul 28 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.17.8-2
- Patch for CVE-2025-22872

* Thu Jul 24 2025 Sam Meluch <sammeluch@microsoft.com> - 1.17.8-1
- Upgrade to 1.17.8 to resolve CVE-2025-23266

* Thu Apr 10 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.17.4-3
- Removed extraction command from prep

* Fri Mar 07 2025 Jon Slobodzian <joslobo@microsoft.com> - 1.17.4-2
- Changing nvidia-container-toolkit to use latest golang before 1.24 as this will not compile without it.

* Thu Feb 13 2025 Mitch Zhu <mitchzhu@microsoft.com> - 1.17.4-1
- Upgrade to v1.17.4 to resolve CVE-2025-23359

* Thu Dec 05 2024 Henry Li <lihl@microsoft.com> - 1.17.3-1
- Upgrade to v1.17.3
- Add nvidia-cdi-hook binary to nvidia-container-toolkit-base package
- Add nvidia-container-toolkit-base as runtime requirement for nvidia-container-toolkit

* Mon Nov 11 2024 Henry Li <lihl@microsoft.com> - 1.17.1-1
- Upgrade to v1.17.1 to resolve CVE‑2024-0134

* Sat Oct 05 2024 Mandeep Plaha <mandeepplaha@microsoft.com> - 1.16.2-1
- Auto-upgrade to 1.16.2 - Critical vulnerability CVE-2024-0132, Medium vulnerability CVE-2024-0133

* Fri Jun 07 2024 Henry Li <lihl@microsoft.com> - 1.15.0-1
- Upgrade to version 1.15.0
- Generate config.toml file during %posttrans

* Mon Feb 05 2024 Bala <balakumaran.kannan@microsoft.com> - 1.14.4-1
- Upgrade to version 1.14.4
- Remove config and oci hooks from files as they are handled in post-install from v1.14.0

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.13.5-3
- Bump release to rebuild with go 1.20.10

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
