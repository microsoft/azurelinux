Name:           buildsys-build-azurelinux-kerneldevpkgs
Version:        4.0
Release:        7%{?dist}
Summary:        Kernel dev package list for kmod builds on Azure Linux
License:        MIT
BuildArch:      noarch

# The Azure Linux kernel version to build kernel modules against.
# Update these macros when the kernel component version changes.
%define azl_kernel_version 6.18.5.1
%define azl_kernel_release 3%{?dist}

Provides:       buildsys-build-azurelinux-kerneldevpkgs-current-x86_64
Provides:       buildsys-build-azurelinux-kerneldevpkgs-current-aarch64
Provides:       buildsys-build-azurelinux-kerneldevpkgs-akmod-x86_64
Provides:       buildsys-build-azurelinux-kerneldevpkgs-akmod-aarch64

Requires:       kernel-devel = %{azl_kernel_version}-%{azl_kernel_release}

%description
Meta-package that provides the kerneldevpkgs-current data file and
helper script used by kmodtool to discover which kernel version to
build kernel modules against on Azure Linux.

The kernel version is explicitly set to the Azure Linux kernel version
rather than queried from the build chroot, which would resolve to the
upstream Fedora kernel.

%install
# Install the Azure Linux kerneldevpkgs-current file (version WITHOUT arch,
# the helper script appends arch at runtime based on build host)
install -d %{buildroot}%{_datadir}/buildsys-build-azurelinux
echo "%{azl_kernel_version}-%{azl_kernel_release}" > %{buildroot}%{_datadir}/buildsys-build-azurelinux/kerneldevpkgs-current

# Create a compat symlink so kmodtool (which hardcodes the
# buildsys-build-rpmfusion path) can find the kerneldevpkgs-current file
install -d %{buildroot}%{_datadir}/buildsys-build-rpmfusion
ln -s ../buildsys-build-azurelinux/kerneldevpkgs-current %{buildroot}%{_datadir}/buildsys-build-rpmfusion/kerneldevpkgs-current

# kmodtool (RPM Fusion version) does:
#   1. `which buildsys-build-<repo>-kerneldevpkgs` to verify package exists
#   2. `buildsys-build-<repo>-kerneldevpkgs --current` to get kernel version list
#   3. Uses the output as kernel_uname_r to generate:
#      BuildRequires: kernel-devel-uname-r = <output>
#
# The output MUST include the arch suffix (e.g., 6.18.5.1-3.azl4.x86_64)
# to match the kernel-devel RPM's "Provides: kernel-devel-uname-r = ..."
install -d %{buildroot}%{_bindir}

cat > %{buildroot}%{_bindir}/buildsys-build-azurelinux-kerneldevpkgs << 'EOFSCRIPT'
#!/bin/bash
# Helper script called by kmodtool to list kernel versions for kmod builds.
# Output format must be VERSION-RELEASE.ARCH (e.g., 6.18.5.1-3.azl4.x86_64)
# because kmodtool uses it to generate:
#   BuildRequires: kernel-devel-uname-r = <output>

datadir="/usr/share"
arch="$(uname -m)"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --current|--akmod|--newest)
            shift
            ;;
        --prefix)
            shift
            datadir="$1"
            shift
            ;;
        *)
            shift
            ;;
    esac
done

kerneldevpkgs="${datadir}/buildsys-build-azurelinux/kerneldevpkgs-current"
if [[ ! -f "${kerneldevpkgs}" ]]; then
    kerneldevpkgs="${datadir}/buildsys-build-rpmfusion/kerneldevpkgs-current"
fi

if [[ -f "${kerneldevpkgs}" ]]; then
    kver="$(cat "${kerneldevpkgs}")"
    # Append arch suffix — kmodtool expects VERSION-RELEASE.ARCH format
    echo "${kver}.${arch}"
else
    echo "Error: kerneldevpkgs-current not found" >&2
    exit 1
fi
EOFSCRIPT
chmod 0755 %{buildroot}%{_bindir}/buildsys-build-azurelinux-kerneldevpkgs

# Compat symlink for unpatched kmodtool which uses --repo rpmfusion
ln -s buildsys-build-azurelinux-kerneldevpkgs %{buildroot}%{_bindir}/buildsys-build-rpmfusion-kerneldevpkgs

%files
%{_bindir}/buildsys-build-azurelinux-kerneldevpkgs
%{_bindir}/buildsys-build-rpmfusion-kerneldevpkgs
%dir %{_datadir}/buildsys-build-azurelinux
%{_datadir}/buildsys-build-azurelinux/kerneldevpkgs-current
%dir %{_datadir}/buildsys-build-rpmfusion
%{_datadir}/buildsys-build-rpmfusion/kerneldevpkgs-current

%changelog
* Thu Mar 13 2026 Elaheh Dehghani <edehghani@microsoft.com> - 4.0-7
- Initial Azure Linux package
