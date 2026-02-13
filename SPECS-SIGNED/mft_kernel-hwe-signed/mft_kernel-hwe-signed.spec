
%global debug_package %{nil}
# The default %%__os_install_post macro ends up stripping the signatures off of the kernel module.
%define __os_install_post %{__os_install_post_leave_signatures} %{nil}


%global target_azl_build_kernel_version %azl_kernel_hwe_version
%global target_kernel_release %azl_kernel_hwe_release
%global target_kernel_version_full %{target_azl_build_kernel_version}-%{target_kernel_release}%{?dist}
%global release_suffix _%{target_azl_build_kernel_version}.%{target_kernel_release}

%global KVERSION %{target_kernel_version_full}
%define _name mft_kernel-hwe

Name:            %{_name}-signed
Summary:         %{_name} Kernel Module for the %{KVERSION} kernel
Version:         4.33.0
Release:         5%{release_suffix}%{?dist}
License:         Dual BSD/GPLv2
Group:           System Environment/Kernel

#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:        %{_name}-%{version}-%{release}.%{_arch}.rpm
Source1:        mst_pci.ko
Source2:        mst_pciconf.ko
%ifarch aarch64
Source3:        bf3_livefish.ko
%endif

Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Conflicts:      mft_kernel
Conflicts:      kernel-mft

# Azure Linux attempts to match the spec file name and the "Name" tag.
# Upstream's mft_kernel spec set rpm name as kernel-mft. To comply, we
# set "Name" as mft_kernel but add a "Provides" for kernel-mft.
Provides:       kernel-hwe-mft = %{version}-%{release}

%description
mft kernel module(s)

%package -n %{_name}
Summary:        %{summary}
Requires:       kernel-hwe = %{target_kernel_version_full}
Requires:       kmod

%description -n %{_name}
%{description}

%prep

%build
mkdir rpm_contents
pushd rpm_contents

# This spec's whole purpose is to inject the signed modules
rpm2cpio %{SOURCE0} | cpio -idmv
cp -rf %{SOURCE1} ./lib/modules/%{KVERSION}/updates/mst_pci.ko
cp -rf %{SOURCE2} ./lib/modules/%{KVERSION}/updates/mst_pciconf.ko
%ifarch aarch64
cp -rf %{SOURCE3} ./lib/modules/%{KVERSION}/updates/bf3_livefish.ko
%endif

popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

popd

%post -n %{_name}
/sbin/depmod %{KVERSION}

%postun -n %{_name}
/sbin/depmod %{KVERSION}

%files -n %{_name}
%defattr(-,root,root,-)
%license %{_defaultlicensedir}/%{_name}/COPYING
/lib/modules/%{KVERSION}/updates/

%changelog
* Mon Feb 10 2026 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 4.33.0-5_6.12.57.1.2
- Tweak specs to use dynamic versioning for kernel

* Fri Feb 06 2026 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.33.0-4_6.12.57.1.4
- Bump to match kernel-hwe.

* Mon Feb 02 2026 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.33.0-3_6.12.57.1.3
- Bump to match kernel-hwe.

* Mon Jan 19 2026 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.33.0-2_6.12.57.1.2
- Bump to match kernel-hwe.

* Tue Nov 18 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.33.0-1_6.12.57.1.1
- Upgrade version to 4.33.0.
- Enable build on x86_64 kernel hwe.

* Wed Nov 05 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 4.30.0-24_6.12.57.1.1
- Bump to match kernel-hwe

* Fri Oct 10 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.30.0-23_6.12.50.2-1
- Bump release to rebuild for new release

* Fri Oct 06 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 4.30.0-22_6.12.50.2-1
- Bump to match kernel-hwe
- Fix signed spec for -hwe variant

* Fri Sep 12 2025 Rachel Menge <rachelmenge@microsoft.com> - 4.30.0-21
- Bump to match kernel-hwe

* Mon Sep 08 2025 Elaheh Dehghani <edehghani@microsoft.com> - 4.30.0-20
- Build using kernel-hwe for aarch64 architecture

* Fri May 23 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.30.0-19
- Bump release to rebuild for new kernel release

* Tue May 13 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 4.30.0-18
- Bump release to rebuild for new kernel release

* Tue Apr 29 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 4.30.0-17
- Bump release to rebuild for new kernel release

* Fri Apr 25 2025 Chris Co <chrco@microsoft.com> - 4.30.0-16
- Bump release to rebuild for new kernel release

* Tue Apr 08 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.30.0-15
- Bump release to rebuild for new kernel release

* Sat Apr 05 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.30.0-14
- Bump release to rebuild for new kernel release

* Fri Mar 14 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.30.0-13
- Bump release to rebuild for new kernel release

* Tue Mar 11 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.30.0-12
- Bump release to rebuild for new kernel release

* Mon Mar 10 2025 Chris Co <chrco@microsoft.com> - 4.30.0-11
- Bump release to rebuild for new kernel release

* Wed Mar 05 2025 Rachel Menge <rachelmenge@microsoft.com> - 4.30.0-10
- Bump release to rebuild for new kernel release

* Tue Mar 04 2025 Rachel Menge <rachelmenge@microsoft.com> - 4.30.0-9
- Bump release to rebuild for new kernel release

* Wed Feb 19 2025 Chris Co <chrco@microsoft.com> - 4.30.0-8
- Bump release to rebuild for new kernel release

* Tue Feb 11 2025 Rachel Menge <rachelmenge@microsoft.com> - 4.30.0-7
- Bump release to rebuild for new kernel release

* Wed Feb 05 2025 Tobias Brick <tobiasb@microsoft.com> - 4.30.0-6
- Bump release to rebuild for new kernel release

* Tue Feb 04 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 4.30.0-5
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 4.30.0-4
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 4.30.0-3
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 4.30.0-2
- Bump release to match kernel

* Tue Dec 17 2024 Binu Jose Philip <bphilip@microsoft.com> - 4.30.0-1
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
