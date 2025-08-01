%global debug_package %{nil}
%ifarch x86_64
%global buildarch x86_64
%endif
%define kernelver %{version}-%{release}
Summary:        Signed Unified Kernel Image for %{buildarch} systems
Name:           kernel-uki-signed-%{buildarch}
Version:        6.6.96.1
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
Source0:        kernel-uki-%{kernelver}.%{buildarch}.rpm
Source1:        vmlinuz-uki-%{kernelver}.efi
ExclusiveArch:  x86_64

%description
This package contains the Unified Kernel Image (UKI) EFI binary signed for secure boot.
The package is specifically created for installing on %{buildarch} systems.

%package -n     kernel-uki
Summary:        Unified Kernel Image
Group:          System Environment/Kernel

%description -n kernel-uki
The kernel-uki package contains the Linux kernel packaged as a Unified
Kernel Image (UKI).

%prep

%build
mkdir rpm_contents
pushd rpm_contents

# This spec's whole purpose is to inject the signed kernel-uki binary
rpm2cpio %{SOURCE0} | cpio -idmv
cp %{SOURCE1} ./boot/vmlinuz-uki-%{kernelver}.efi

popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

cp %{buildroot}/boot/vmlinuz-uki-%{kernelver}.efi %{buildroot}/boot/efi/EFI/Linux/vmlinuz-uki-%{kernelver}.efi

popd

%files -n kernel-uki
/boot/vmlinuz-uki-%{kernelver}.efi
/lib/modules/%{kernelver}/vmlinuz-uki.efi
/boot/efi/EFI/Linux/vmlinuz-uki-%{kernelver}.efi

%changelog
* Mon Jul 07 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.96.1-1
- Auto-upgrade to 6.6.96.1

* Mon Jun 16 2025 Harshit Gupta <guptaharshit@microsoft.com> - 6.6.92.2-3
- Bump release to match kernel

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
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.64.2-5
- Bump release to match kernel

* Sat Jan 18 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.64.2-4
- Bump release to match kernel

* Thu Jan 16 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.64.2-3
- Bump release to match kernel

* Fri Jan 10 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.64.2-2
- Bump release to match kernel

* Thu Jan 09 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.64.2-1
- Auto-upgrade to 6.6.64.2

* Wed Jan 08 2025 Tobias Brick <tobiasb@microsoft.com> - 6.6.57.1-8
- Bump release to match kernel

* Sun Dec 22 2024 Ankita Pareek <ankitapareek@microsoft.com> - 6.6.57.1-7
- Bump release to match kernel

* Wed Dec 18 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.57.1-6
- Bump release to match kernel-64k

* Mon Nov 25 2024 Chris Co <chrco@microsoft.com> - 6.6.57.1-5
- Bump release to match kernel

* Wed Nov 06 2024 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 6.6.57.1-4
- Bump release to match kernel

* Tue Nov 05 2024 Chris Co <chrco@microsoft.com> - 6.6.57.1-3
- Bump release to match kernel

* Wed Oct 30 2024 Thien Trung Vuong <tvuong@microsoft.com> - 6.6.57.1-2
- Bump release to match kernel

* Tue Oct 29 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.57.1-1
- Auto-upgrade to 6.6.57.1

* Thu Oct 24 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.56.1-5
- Bump release to match kernel

* Wed Oct 23 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.56.1-4
- Bump release to match kernel

* Wed Oct 23 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.56.1-3
- Bump release to match kernel

* Tue Oct 22 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.56.1-2
- Bump release to match kernel

* Thu Oct 17 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.56.1-1
- Auto-upgrade to 6.6.56.1

* Thu Oct 03 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.51.1-5
- Bump release to match kernel

* Wed Oct 02 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.51.1-4
- Bump release to match kernel

* Tue Sep 24 2024 Jo Zzsi <jozzsicsataban@gmail.com> - 6.6.51.1-3
- Bump release to match kernel

* Fri Sep 20 2024 Chris Co <chrco@microsoft.com> - 6.6.51.1-2
- Bump release to match kernel

* Wed Sep 18 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.51.1-1
- Auto-upgrade to 6.6.51.1

* Fri Sep 13 2024 Thien Trung Vuong <tvuong@microsoft.com> - 6.6.47.1-7
- Bump release to match kernel

* Fri Sep 13 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.47.1-6
- Bump release to match kernel

* Thu Sep 12 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.47.1-5
- Bump release to match kernel

* Thu Sep 12 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.47.1-4
- Bump release to match kernel

* Wed Sep 04 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.47.1-3
- Bump release to match kernel

* Thu Aug 29 2024 Jo Zzsi <jozzsicsataban@gmail.com> - 6.6.47.1-2
- Bump release to match kernel

* Thu Aug 22 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.47.1-1
- Auto-upgrade to 6.6.47.1

* Wed Aug 14 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.44.1-1
- Auto-upgrade to 6.6.44.1

* Sat Aug 10 2024 Thien Trung Vuong <tvuong@microsoft.com> - 6.6.43.1-7
- Bump release to match kernel

* Wed Aug 07 2024 Thien Trung Vuong <tvuong@microsoft.com> - 6.6.43.1-6
- Bump release to match kernel

* Tue Aug 06 2024 Chris Co <chrco@microsoft.com> - 6.6.43.1-5
- Bump release to match kernel

* Sat Aug 03 2024 Chris Co <chrco@microsoft.com> - 6.6.43.1-4
- Bump release to match kernel

* Thu Aug 01 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.43.1-3
- Bump release to match kernel

* Wed Jul 31 2024 Chris Co <chrco@microsoft.com> - 6.6.43.1-2
- Bump release to match kernel

* Tue Jul 30 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.43.1-1
- Auto-upgrade to 6.6.43.1

* Tue Jul 30 2024 Chris Co <chrco@microsoft.com> - 6.6.39.1-2
- Bump release to match kernel

* Fri Jul 26 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.39.1-1
- Auto-upgrade to 6.6.39.1

* Tue Jul 16 2024 Kelsey Steele <kelseysteele@microsoft.com> - 6.6.35.1-6
- Bump release to match kernel

* Wed Jul 10 2024 Thien Trung Vuong <tvuong@microsoft.com> - 6.6.35.1-5
- Bump release to match kernel

* Fri Jul 05 2024 Gary Swalling <gaswal@microsoft.com> - 6.6.35.1-4
- Bump release to match kernel

* Mon Jul 01 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.35.1-3
- Bump release to match kernel

* Tue Jun 25 2024 Thien Trung Vuong <tvuong@microsoft.com> - 6.6.35.1-2
- Original version for Azure Linux.
- License verified.
