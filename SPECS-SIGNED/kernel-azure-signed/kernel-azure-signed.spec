%global debug_package %{nil}
%global sha512hmac bash %{_sourcedir}/sha512hmac-openssl.sh
%ifarch x86_64
%global buildarch x86_64
%endif
%ifarch aarch64
%global buildarch aarch64
%endif
%define uname_r %{version}-%{release}
Summary:        Signed Linux Kernel for Azure
Name:           kernel-azure-signed-%{buildarch}
Version:        5.15.145.2
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
# This spec purpose is to take an input kernel-azure rpm and input secure-boot-signed
# kernel binary from the same build and generate a new "kernel-azure" rpm with the
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
# resulting kernel binary and "repackage" the kernel-azure RPM (something rpm itself
# actively tries to make sure you never do...generally for good reasons).
#
# To achive this repackaging, this spec creates a new subpackage named
# "kernel-azure". To retain all of the initial kernel-azure package behaviors, we make sure
# the subpackage has the same requires, provides, triggers, post steps, and
# files as the original kernel package.
#
# This specific repackaging implementation leaves room for us to enable the
# more ideal secure-boot signing flow in the future without introducing any
# sort of breaking change or new packaging. Users still install a "kernel-azure"
# package like they normally would.
#
# Maintenance Notes:
# - This spec's "version" and "release" must reflect the unsigned version that
# was signed. An important consequence is that when making a change to this
# spec or the normal kernel-azure spec, the other spec's version version/release must
# be increased to keep the two versions consistent.
#
# - Make sure the kernel-azure subpackage's Requires, Provides, triggers, post/postun
# scriptlets, and files match the normal kernel-azure spec's. The kernel-azure subpackage
# should contain the same content as the input kernel-azure package but replace the
# kernel binary with our signed kernel binary. Since all the requires, provides,
# etc are the same, this new kernel-azure package can be a direct replacement for the
# normal kernel-azure package and RPM will resolve packages with kernel-azure dependencies
# correctly.
#
# To populate the input sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec
Source0:        kernel-azure-%{version}-%{release}.%{buildarch}.rpm
Source1:        vmlinuz-%{uname_r}
Source2:        sha512hmac-openssl.sh
BuildRequires:  cpio
BuildRequires:  openssl
BuildRequires:  sed

%description
This package contains the Linux kernel package with kernel signed with the production key

%package -n     kernel-azure
Summary:        Linux Kernel for Azure
Group:          System Environment/Kernel
Requires:       filesystem
Requires:       kmod
Requires(post): coreutils
Requires(postun): coreutils

%description -n kernel-azure
The kernel-azure package contains the signed Linux kernel for Azure.

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

# Recalculate sha512hmac for FIPS
%{sha512hmac} %{buildroot}/boot/vmlinuz-%{uname_r} | sed -e "s,$RPM_BUILD_ROOT,," > %{buildroot}/boot/.vmlinuz-%{uname_r}.hmac
cp %{buildroot}/boot/.vmlinuz-%{uname_r}.hmac %{buildroot}/lib/modules/%{uname_r}/.vmlinuz.hmac

%triggerin -n kernel-azure -- initramfs
mkdir -p %{_localstatedir}/lib/rpm-state/initramfs/pending
touch %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
echo "initrd generation of kernel %{uname_r} will be triggered later" >&2

%triggerun -n kernel-azure -- initramfs
rm -rf %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
rm -rf /boot/initrd.img-%{uname_r}
echo "initrd of kernel %{uname_r} removed" >&2

%postun -n kernel-azure
if [ ! -e /boot/mariner.cfg ]
then
     ls /boot/linux-*.cfg 1> /dev/null 2>&1
     if [ $? -eq 0 ]
     then
          list=`ls -tu /boot/linux-*.cfg | head -n1`
          test -n "$list" && ln -sf "$list" /boot/mariner.cfg
     fi
fi

%post -n kernel-azure
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/mariner.cfg

%files -n kernel-azure
%defattr(-,root,root)
%license COPYING
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
/boot/.vmlinuz-%{uname_r}.hmac
%config(noreplace) /boot/linux-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
/lib/modules/%{uname_r}/.vmlinuz.hmac
%exclude /lib/modules/%{uname_r}/build
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound
%exclude /module_info.ld

%changelog
* Tue Jan 16 2024 Gary Swalling <gaswal@microsoft.com> - 5.15.145.2-1
- Update to 5.15.145.2

* Tue Dec 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.139.1-1
- Auto-upgrade to 5.15.139.1

* Tue Nov 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.138.1-1
- Auto-upgrade to 5.15.138.1

* Mon Nov 20 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.137.1-2
- Bump release to match kernel

* Mon Nov 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.137.1-1
- Auto-upgrade to 5.15.137.1

* Tue Oct 17 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.135.1-1
- Auto-upgrade to 5.15.135.1

* Tue Sep 26 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.133.1-1
- Auto-upgrade to 5.15.133.1

* Tue Sep 22 2023 Cameron Baird <cameronbaird@microsoft.com> - 5.15.131.1-3
- Bump release to match kernel

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.15.131.1-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Sep 08 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.131.1-1
- Auto-upgrade to 5.15.131.1

* Mon Aug 14 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.126.1-1
- Auto-upgrade to 5.15.126.1

* Wed Aug 09 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.125.1-1
- Auto-upgrade to 5.15.125.1

* Tue Aug 01 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.123.1-1
- Auto-upgrade to 5.15.123.1

* Wed Jul 26 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.122.1-1
- Auto-upgrade to 5.15.122.1

* Wed Jun 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.118.1-1
- Auto-upgrade to 5.15.118.1

* Tue Jun 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.116.1-1
- Auto-upgrade to 5.15.116.1

* Tue May 23 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.112.1-1
- Auto-upgrade to 5.15.112.1

* Mon May 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.111.1-1
- Auto-upgrade to 5.15.111.1

* Mon May 01 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.110.1-1
- Auto-upgrade to 5.15.110.1

* Wed Apr 19 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.107.1-2
- Bump release to match kernel-azure

* Tue Apr 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.107.1-1
- Auto-upgrade to 5.15.107.1

* Tue Mar 14 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.102.1-1
- Auto-upgrade to 5.15.102.1

* Mon Mar 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.98.1-1
- Auto-upgrade to 5.15.98.1

* Sat Feb 25 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.95.1-1
- Auto-upgrade to 5.15.95.1

* Wed Feb 22 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.94.1-1
- Auto-upgrade to 5.15.94.1

* Wed Feb 15 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.92.1-2
- Bump to match kernel-azure release

* Mon Feb 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.15.92.1-1
- Auto-upgrade to 5.15.92.1

* Thu Jan 05 2023 Rachel Menge <rachelmenge@microsoft.com> - 5.15.86.1-1
- Original version for CBL-Mariner.
- License verified
