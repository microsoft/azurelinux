%global debug_package %{nil}

# This should be a subpackage of the kernel package, but due to
# "circular dependencies" that is not possible, so this is instead a
# separate source package

# Note - while Fedora's kernel version includes the %%_target_cpu as a
# suffix, our kernel version does not.
%define kernelver %{version}-%{release}

%define cmdline console=ttyS0

Summary:        Linux Kernel
Name:           kernel-uki
Version:        6.6.22.1
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
Source0:        kernel-uki-dracut.conf

BuildRequires:  kernel = %{version}-%{release}
BuildRequires:  systemd-ukify
BuildRequires:  dracut
BuildRequires:  binutils
BuildRequires:  systemd-boot-unsigned
BuildRequires:  systemd-udev
BuildRequires:  system-release
BuildRequires:  tpm2-tools
BuildRequires:  cryptsetup
BuildRequires:  device-mapper

%description
The kernel-uki package contains the Linux kernel packaged as a Unified
Kernel Image (UKI).

%prep
%setup -c -T

%build
dracut --conf=%{SOURCE0} --confdir=$(mktemp -d) --logfile=$(mktemp) \
       --verbose \
       --kver %{kernelver} \
       --kernel-image /lib/modules/%{kernelver}/vmlinuz \
       --kernel-cmdline "%{cmdline}" initrd
ukify build \
      --uname %{kernelver} \
      --linux /lib/modules/%{kernelver}/vmlinuz \
      --initrd initrd \
      --cmdline "%{cmdline}" \
      --output vmlinuz-uki.efi

%install
install -D -t %{buildroot}/lib/modules/%{kernelver} vmlinuz-uki.efi

%files
/lib/modules/%{kernelver}/vmlinuz-uki.efi

%changelog
* Thu Apr 25 2024 Dan Streetman <ddstreet@microsoft.com> - 6.6.22.1-2
- initial package
- The following lines are here solely to satisfy tooling.
- Initial CBL-Mariner import from Photon (license: Apache2).
- License verified
