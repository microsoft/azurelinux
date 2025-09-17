%global debug_package %{nil}
%global buildarch aarch64
%define uname_r %{version}-%{release}
Summary:        Signed Linux Kernel for %{buildarch} systems
Name:           kernel-hwe-signed-%{buildarch}
Version:        6.12.40.1
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
# This package's "version" and "release" must reflect the unsigned version that
# was signed.
# An important consequence is that when making a change to this package, the
# unsigned version/release must be increased to keep the two versions consistent.
# Ideally though, this spec will not change much or at all, so the version will
# just track the unsigned package's version/release.
#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec
Source0:        kernel-hwe-%{version}-%{release}.%{buildarch}.rpm
Source1:        vmlinuz-%{uname_r}
ExclusiveArch:  aarch64
BuildRequires:  cpio
BuildRequires:  grub2-rpm-macros
BuildRequires:  openssl
BuildRequires:  sed
%{?grub2_configuration_requires}

%description
This package contains the Linux kernel package with kernel signed with the production key

%package -n     kernel-hwe
Summary:        Linux Kernel
Group:          System Environment/Kernel
Requires:       filesystem
Requires:       kmod
Requires(post): coreutils
Requires(postun): coreutils

%description -n kernel-hwe
The kernel package contains the signed Linux kernel.

%prep

%build
mkdir rpm_contents
pushd rpm_contents

# This spec's whole purpose is to inject the signed kernel binary
rpm2cpio %{SOURCE0} | cpio -idmv
cp %{SOURCE1} ./boot/vmlinuz-%{uname_r}

popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

popd

%triggerin -n kernel-hwe -- initramfs
mkdir -p %{_localstatedir}/lib/rpm-state/initramfs/pending
touch %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
echo "initrd generation of kernel %{uname_r} will be triggered later" >&2

%triggerun -n kernel-hwe -- initramfs
rm -rf %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
rm -rf /boot/initramfs-%{uname_r}.img
echo "initrd of kernel %{uname_r} removed" >&2

%postun -n kernel-hwe
%grub2_postun

%post -n kernel-hwe
/sbin/depmod -a %{uname_r}
%grub2_post

%files -n kernel-hwe
%defattr(-,root,root)
%license COPYING
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
%exclude /lib/modules/%{uname_r}/build
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound
%exclude /module_info.ld

%changelog
* Fri Aug 15 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 6.12.40.1-1
- Original version for Azure Linux
- License verified
