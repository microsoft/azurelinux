%global debug_package %{nil}
%global sha512hmac bash %{_sourcedir}/sha512hmac-openssl.sh
%ifarch x86_64
%global buildarch x86_64
%endif
%define uname_r %{version}-%{release}
Summary:        Signed MSHV-enabled Linux Kernel for %{buildarch} systems
Name:           kernel-mshv-signed-%{buildarch}
Version:        5.15.126.mshv9
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
# This spec purpose is to take an input kernel rpm and input secure-boot-signed
# kernel binary from the same build and generate a new "kernel" rpm with the
# signed kernel binary + all of the other original kernel files, triggers,
# scriptlets, requires, provides, etc.
#
# We need to ensure the kernel modules and kernel binary used are from the exact
# same build because at build time the kernel modules are signed with an
# ephemeral key that the kernel enrolls in its keyring. We enforce kernel
# module signature checking when we enable security features like kernel
# lockdown so our kernel can only load those specific kernel modules at runtime.
#
# Additionally, to complete the UEFI Secure Boot chain, we must PE-sign the
# kernel binary. Ideally we would enable secure-boot signing tools like pesign
# or sbsign to be callable from inside the rpmbuild environment, that way we can
# secure-boot sign the kernel binary during the kernel's rpmbuild. It is best
# practice to sign as soon as possible. However there are issues getting that
# secure boot signing infrastructure in place today. Hence we sign the
# resulting kernel binary and "repackage" the kernel RPM (something rpm itself
# actively tries to make sure you never do...generally for good reasons).
#
# To achive this repackaging, this spec creates a new subpackage named
# "kernel-mshv". To retain all of the initial kernel-mshv package behaviors, we make sure
# the subpackage has the same requires, provides, triggers, post steps, and
# files as the original kernel package.
#
# This specific repackaging implementation leaves room for us to enable the
# more ideal secure-boot signing flow in the future without introducing any
# sort of breaking change or new packaging. Users still install a "kernel-mshv"
# package like they normally would.
#
# Maintenance Notes:
# - This spec's "version" and "release" must reflect the unsigned version that
# was signed. An important consequence is that when making a change to this
# spec or the normal kernel spec, the other spec's version version/release must
# be increased to keep the two versions consistent.
#
# - Make sure the kernel subpackage's Requires, Provides, triggers, post/postun
# scriptlets, and files match the normal kernel-mshv spec's. The kernel subpackage
# should contain the same content as the input kernel package but replace the
# kernel binary with our signed kernel binary. Since all the requires, provides,
# etc are the same, this new kernel package can be a direct replacement for the
# normal kernel package and RPM will resolve packages with kernel dependencies
# correctly.
#
# To populate the input sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec
Source0:        kernel-mshv-%{version}-%{release}.%{buildarch}.rpm
Source1:        vmlinuz-%{uname_r}
Source2:        sha512hmac-openssl.sh
BuildRequires:  cpio
BuildRequires:  openssl
BuildRequires:  sed

%description
This package contains the MSHV-enabled Linux kernel package with kernel-mshv signed with the production key

%package -n     kernel-mshv
Summary:        MSHV-enabled Linux Kernel
Group:          System Environment/Kernel
Requires:       filesystem
Requires:       kmod
Requires(post): coreutils
Requires(postun): coreutils
%{?grub2_configuration_requires}
ExclusiveArch:  x86_64

%description -n kernel-mshv
The kernel package contains the signed MSHV-enabled Linux kernel.

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

%triggerin -n kernel-mshv -- initramfs
mkdir -p %{_localstatedir}/lib/rpm-state/initramfs/pending
touch %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
echo "initrd generation of kernel %{uname_r} will be triggered later" >&2

%triggerun -n kernel-mshv -- initramfs
rm -rf %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
rm -rf /boot/efi/initrd.img-%{uname_r}
echo "initrd of kernel %{uname_r} removed" >&2

%postun -n kernel-mshv
if [ ! -e /boot/mariner-mshv.cfg ]
then
     ls /boot/linux-*.cfg 1> /dev/null 2>&1
     if [ $? -eq 0 ]
     then
          list=`ls -tu /boot/linux-*.cfg | head -n1`
          test -n "$list" && ln -sf "$list" /boot/mariner-mshv.cfg
     fi
fi
%grub2_postun

%post -n kernel-mshv
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/mariner-mshv.cfg
%grub2_post

%files -n kernel-mshv
%defattr(-,root,root)
%license COPYING
%exclude %dir /usr/lib/debug
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
/boot/efi/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
%config(noreplace) %{_sysconfdir}/default/grub.d/50_mariner_mshv.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
%exclude /lib/modules/%{uname_r}/build

%changelog
* Thu Jan 04 2024 Cameron Baird <cameronbaird@microsoft.com> - 5.15.126.mshv9-2
- Introduced
- License verified
