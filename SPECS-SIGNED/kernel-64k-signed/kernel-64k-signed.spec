%global debug_package %{nil}
%global sha512hmac bash %{_sourcedir}/sha512hmac-openssl.sh
%ifarch aarch64
%global buildarch aarch64
%endif
%define uname_r %{version}-%{release}
Summary:        Signed Linux Kernel for %{buildarch} systems
Name:           kernel-64k-signed-%{buildarch}
Version:        6.6.119.3
Release:        3%{?dist}
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
Source0:        kernel-64k-%{version}-%{release}.%{buildarch}.rpm
Source1:        vmlinuz-%{uname_r}
Source2:        sha512hmac-openssl.sh
BuildRequires:  cpio
BuildRequires:  grub2-rpm-macros
BuildRequires:  openssl
BuildRequires:  sed
%{?grub2_configuration_requires}

%description
This package contains the Linux kernel package with kernel signed with the production key

%package -n     kernel-64k
Summary:        Linux Kernel
Group:          System Environment/Kernel
Requires:       filesystem
Requires:       kmod
Requires(post): coreutils
Requires(postun): coreutils

%description -n kernel-64k
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

# Recalculate sha512hmac for FIPS
%{sha512hmac} %{buildroot}/boot/vmlinuz-%{uname_r} | sed -e "s,$RPM_BUILD_ROOT,," > %{buildroot}/boot/.vmlinuz-%{uname_r}.hmac
cp %{buildroot}/boot/.vmlinuz-%{uname_r}.hmac %{buildroot}/lib/modules/%{uname_r}/.vmlinuz.hmac

%triggerin -n kernel-64k -- initramfs
mkdir -p %{_localstatedir}/lib/rpm-state/initramfs/pending
touch %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
echo "initrd generation of kernel %{uname_r} will be triggered later" >&2

%triggerun -n kernel-64k -- initramfs
rm -rf %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
rm -rf /boot/initramfs-%{uname_r}.img
echo "initrd of kernel %{uname_r} removed" >&2

%postun -n kernel-64k
%grub2_postun

%post -n kernel-64k
/sbin/depmod -a %{uname_r}
%grub2_post

%files -n kernel-64k
%defattr(-,root,root)
%license COPYING
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
/boot/.vmlinuz-%{uname_r}.hmac
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
/lib/modules/%{uname_r}/.vmlinuz.hmac
%exclude /lib/modules/%{uname_r}/build
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound
%exclude /module_info.ld

%changelog
* Fri Jan 16 2026 Rachel Menge <rachelmenge@microsoft.com> - 6.6.119.3-3
- Bump release to match kernel,kernel-ipe

* Thu Jan 08 2026 Rachel Menge <rachelmenge@microsoft.com> - 6.6.119.3-2
- Bump release to match kernel,kernel-ipe,kernel-64k

* Tue Jan 06 2026 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.119.3-1
- Auto-upgrade to 6.6.119.3

* Wed Nov 26 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.117.1-1
- Auto-upgrade to 6.6.117.1

* Tue Nov 18 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.116.1-2
- Bump release to match kernel,kernel-ipe,kernel-64k

* Mon Nov 10 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.116.1-1
- Auto-upgrade to 6.6.116.1

* Mon Oct 27 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.112.1-2
- Bump release to match kernel

* Wed Oct 15 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.112.1-1
- Auto-upgrade to 6.6.112.1

* Tue Sep 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.104.2-4
- Bump release to match kernel

* Tue Sep 23 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 6.6.104.2-3
- Bump release to match kernel

* Tue Sep 23 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.104.2-2
- Bump release to match kernel

* Wed Sep 17 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.104.2-1
- Auto-upgrade to 6.6.104.2

* Fri Aug 22 2025 Siddharth Chintamaneni <siddharthc@microsoft.com> - 6.6.96.2-2
- Bump release to match kernel

* Fri Aug 15 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.96.2-1
- Auto-upgrade to 6.6.96.2

* Thu Jul 17 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.96.1-2
- Bump release to match kernel

* Mon Jul 07 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.96.1-1
- Auto-upgrade to 6.6.96.1

* Mon Jun 16 2025 Harshit Gupta <guptaharshit@microsoft.com> - 6.6.92.2-3
- Bump release to match kernel-64k

* Mon Jun 09 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.92.2-2
- Bump release to match kernel

* Fri May 30 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.92.2-1
- Auto-upgrade to 6.6.92.2

* Fri May 23 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.90.1-1
- Auto-upgrade to 6.6.90.1

* Tue May 13 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 6.6.85.1-4
- Bump release to match kernel

* Tue Apr 29 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 6.6.85.1-3
- Bump release to match kernel

* Fri Apr 25 2025 Chris Co <chrco@microsoft.com> - 6.6.85.1-2
- Bump release to rebuild for new kernel release

* Sat Apr 05 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.85.1-1
- Auto-upgrade to 6.6.85.1

* Fri Mar 14 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.82.1-1
- Auto-upgrade to 6.6.82.1

* Tue Mar 11 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.79.1-1
- Auto-upgrade to 6.6.79.1

* Mon Mar 10 2025 Chris Co <chrco@microsoft.com> - 6.6.78.1-3
- Bump release to match kernel

* Wed Mar 05 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.78.1-2
- Bump release to match kernel

* Mon Mar 03 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.78.1-1
- Auto-upgrade to 6.6.78.1

* Wed Feb 19 2025 Chris Co <chrco@microsoft.com> - 6.6.76.1-2
- Bump release to match kernel

* Mon Feb 10 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.76.1-1
- Auto-upgrade to 6.6.76.1

* Wed Feb 05 2025 Tobias Brick <tobiasb@microsoft.com> - 6.6.64.2-9
- Bump release to match kernel

* Tue Feb 04 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 6.6.64.2-8
- Bump release to match kernel

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 6.6.64.2-7
- Bump release to match kernel

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 6.6.64.2-6
- Bump to match kernel-64k

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.64.2-5
- Bump to match kernel-64k

* Sat Jan 18 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.64.2-4
- Bump release to match kernel-64k

* Thu Jan 16 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.64.2-3
- Bump release to match kernel

* Fri Jan 10 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.64.2-2
- Bump release to match kernel-64k

* Thu Jan 09 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.64.2-1
- Auto-upgrade to 6.6.64.2

* Wed Jan 08 2025 Tobias Brick <tobiasb@microsoft.com> - 6.6.57.1-8
- Bump release to match kernel

* Sun Dec 22 2024 Ankita Pareek <ankitapareek@microsoft.com> - 6.6.57.1-7
- Bump release to match kernel

* Wed Dec 18 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.57.1-6
- Bump release to match kernel-64k

* Thu Nov 07 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.57.1-5
- Original version for Azure Linux
- Starting with release 5 to align with kernel release.
- License verified
