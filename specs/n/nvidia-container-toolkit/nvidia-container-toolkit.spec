## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           nvidia-container-toolkit
Version:        1.20.0
Release:        %autorelease
Summary:        NVIDIA Container Toolkit
License:        Apache-2.0
URL:            https://github.com/NVIDIA/nvidia-container-toolkit
Vendor:         NVIDIA CORPORATION
Packager:       NVIDIA CORPORATION <cudatools@nvidia.com>

ExclusiveArch:  x86_64 aarch64

# Binaries are built with -s -w (no DWARF/symbol table), so there's no debug
# info for rpmbuild's automatic debuginfo/debugsource extraction to package.
%global debug_package %{nil}

# GitHub tag archives don't include a .git directory, so vendor/ (checked into
# upstream's repo) is what makes this buildable without network access.
Source0:        https://github.com/NVIDIA/nvidia-container-toolkit/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  golang >= 1.26
BuildRequires:  gcc
BuildRequires:  systemd-devel

Obsoletes:      nvidia-container-runtime <= 3.5.0-1
Obsoletes:      nvidia-container-runtime-hook <= 1.4.0-2
Provides:       nvidia-container-runtime
Provides:       nvidia-container-runtime-hook
# TODO: libnvidia-container isn't yet packaged in Azure Linux. Until it is,
# this package's runtime dependency on libnvidia-container-tools cannot be
# satisfied and nvidia-container-runtime-hook will fail to dlopen it.
Requires:       libnvidia-container-tools == %{version}-%{release}
Requires:       libnvidia-container-tools < 2.0.0
Requires:       %{name}-base = %{version}-%{release}

%description
Provides tools and utilities to enable GPU support in containers.

# The BASE package consists of the NVIDIA Container Runtime and the NVIDIA
# Container Toolkit CLI. This allows the package to be installed on systems
# where no NVIDIA Container CLI is available.
%package base
Summary:        NVIDIA Container Toolkit Base
Obsoletes:      nvidia-container-runtime <= 3.5.0-1
Obsoletes:      nvidia-container-runtime-hook <= 1.4.0-2
Provides:       nvidia-container-runtime
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# Since this package allows certain components of the NVIDIA Container
# Toolkit to be installed separately, it conflicts with older versions of the
# nvidia-container-toolkit package that also provide these files.
Conflicts:      nvidia-container-toolkit <= 1.10.0-1

%description base
Provides tools such as the NVIDIA Container Runtime and NVIDIA Container
Toolkit CLI to enable GPU support in containers.

# The OPERATOR EXTENSIONS package consists of components that are required to
# enable GPU support in Kubernetes. This package is not distributed as part
# of the upstream NVIDIA Container Toolkit RPMs, but is kept as its own
# subpackage here to mirror upstream's packaging split.
%package operator-extensions
Summary:        NVIDIA Container Toolkit Operator Extensions
Requires:       %{name}-base = %{version}-%{release}

%description operator-extensions
Provides tools for using the NVIDIA Container Toolkit with the GPU Operator.

%prep
%autosetup -p1

%build
%global cli_version_pkg github.com/NVIDIA/nvidia-container-toolkit/internal/info
%global extldflags -Wl,--export-dynamic -Wl,--unresolved-symbols=ignore-in-object-files -Wl,-z,lazy

export GOFLAGS=-mod=vendor
export GO111MODULE=on
for cmd in \
    nvidia-container-runtime-hook \
    nvidia-ctk \
    nvidia-container-runtime \
    nvidia-container-runtime.cdi \
    nvidia-container-runtime.legacy \
    nvidia-cdi-hook \
; do
    go build -ldflags "-s -w '-extldflags=%{extldflags}' -X %{cli_version_pkg}.gitCommit=v%{version} -X %{cli_version_pkg}.version=%{version}" \
        -o "${cmd}" "./cmd/${cmd}"
done

%install
install -d %{buildroot}%{_bindir}
install -m 0755 -t %{buildroot}%{_bindir} \
    nvidia-container-runtime-hook \
    nvidia-container-runtime \
    nvidia-container-runtime.cdi \
    nvidia-container-runtime.legacy \
    nvidia-ctk \
    nvidia-cdi-hook

install -d %{buildroot}%{_unitdir}
install -m 0644 -t %{buildroot}%{_unitdir} \
    deployments/systemd/nvidia-cdi-refresh.service \
    deployments/systemd/nvidia-cdi-refresh.path

install -d %{buildroot}%{_presetdir}
install -m 0644 -t %{buildroot}%{_presetdir} \
    deployments/systemd/90-nvidia-container-toolkit.preset

install -d %{buildroot}%{_sysconfdir}/nvidia-container-toolkit
install -m 0644 -t %{buildroot}%{_sysconfdir}/nvidia-container-toolkit \
    deployments/systemd/nvidia-cdi-refresh.env

%post
if [ $1 -gt 1 ]; then  # only on package upgrade
  mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
  cp -af %{_bindir}/nvidia-container-runtime-hook %{_localstatedir}/lib/rpm-state/%{name}
fi

%posttrans
if [ ! -e %{_bindir}/nvidia-container-runtime-hook ]; then
  # repairing lost file nvidia-container-runtime-hook
  cp -avf %{_localstatedir}/lib/rpm-state/%{name}/nvidia-container-runtime-hook %{_bindir}
fi
rm -rf %{_localstatedir}/lib/rpm-state/%{name}
ln -sf %{_bindir}/nvidia-container-runtime-hook %{_bindir}/%{name}

%postun
if [ "$1" = 0 ]; then  # package is uninstalled, not upgraded
  if [ -L %{_bindir}/%{name} ]; then rm -f %{_bindir}/%{name}; fi
fi

%files
%license LICENSE
%{_bindir}/nvidia-container-runtime-hook

%post base
# Generate the default config; if this file already exists, no changes are made.
%{_bindir}/nvidia-ctk --quiet config --config-file=%{_sysconfdir}/nvidia-container-runtime/config.toml --in-place
%systemd_post nvidia-cdi-refresh.path nvidia-cdi-refresh.service

%preun base
%systemd_preun nvidia-cdi-refresh.path nvidia-cdi-refresh.service

%postun base
%systemd_postun nvidia-cdi-refresh.path nvidia-cdi-refresh.service

%files base
%license LICENSE
%{_bindir}/nvidia-container-runtime
%{_bindir}/nvidia-ctk
%{_bindir}/nvidia-cdi-hook
%{_unitdir}/nvidia-cdi-refresh.service
%{_unitdir}/nvidia-cdi-refresh.path
%{_presetdir}/90-nvidia-container-toolkit.preset
%config(noreplace) %{_sysconfdir}/nvidia-container-toolkit/nvidia-cdi-refresh.env

%files operator-extensions
%license LICENSE
%{_bindir}/nvidia-container-runtime.cdi
%{_bindir}/nvidia-container-runtime.legacy

%changelog
## START: Generated by rpmautospec
* Wed Sep 09 2026 John Doe <packager@example.com> - 1.20.0-1
- Uncommitted changes
## END: Generated by rpmautospec
