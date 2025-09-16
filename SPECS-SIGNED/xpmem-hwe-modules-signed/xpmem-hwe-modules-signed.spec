%{!?KMP: %global KMP 0}

%global debug_package %{nil}
# The default %%__os_install_post macro ends up stripping the signatures off of the kernel module.
%define __os_install_post %{__os_install_post_leave_signatures} %{nil}

# hard code versions due to ADO bug:58993948
%global target_azl_build_kernel_version 6.12.40.1
%global target_kernel_release 1
%global target_kernel_version_full %{target_azl_build_kernel_version}-%{target_kernel_release}%{?dist}
%global release_suffix _%{target_azl_build_kernel_version}.%{target_kernel_release}

%global KVERSION %{target_kernel_version_full}

%define _name xpmem-hwe-modules
%{!?_mofed_full_version: %define _mofed_full_version 24.10-20%{release_suffix}%{?dist}}

# xpmem-modules is a sub-package in SPECS/xpmem.
# We are making that into a main package for signing.

Summary:	 Cross-partition memory
Name:		 %{_name}-signed
Version:	 2.7.4
Release:	 20%{release_suffix}%{?dist}
License:	 GPLv2 and LGPLv2.1
Group:		 System Environment/Libraries
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
BuildRequires:	 automake autoconf
URL:		 https://github.com/openucx/xpmem
ExclusiveArch:   aarch64

#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:        %{_name}-%{version}-%{release}.%{_arch}.rpm
Source1:        xpmem.ko

%description
XPMEM is a Linux kernel module that enables a process to map the
memory of another process into its virtual address space. Source code
can be obtained by cloning the Git repository, original Mercurial
repository or by downloading a tarball from the link above.

This package includes the kernel module.

%package -n %{_name}
Summary:        %{summary}
Requires:       mlnx-ofa_kernel-hwe = %{_mofed_full_version}
Requires:       mlnx-ofa_kernel-hwe-modules = %{_mofed_full_version}
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

cp -rf %{SOURCE1} ./lib/modules/%{KVERSION}/updates/xpmem.ko

popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

popd

%files -n %{_name}
/lib/modules/%{KVERSION}/updates/xpmem.ko
%{_datadir}/licenses

%post -n %{_name}
depmod %{KVERSION} -a
/sbin/modprobe -r xpmem > /dev/null 2>&1
/sbin/modprobe xpmem > /dev/null 2>&1

%postun -n %{_name}
if [ "$1" = 0 ]; then
	if lsmod | grep -qw xpmem; then
		# If the module fails to unload, give an error,
		# but don't fail uninstall. User should handle this
		# Maybe the module is in use
		rmmod xpmem || :
	fi
fi

%changelog
* Mon Sep 08 2025 Elaheh Dehghani <edehghani@microsoft.com> - 2.7.4-20
- Build using kernel-hwe for aarch64 architecture

* Fri May 23 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.7.4-19
- Bump release to rebuild for new kernel release

* Tue May 13 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 2.7.4-18
- Bump release to rebuild for new kernel release

* Tue Apr 29 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 2.7.4-17
- Bump release to rebuild for new kernel release

* Fri Apr 25 2025 Chris Co <chrco@microsoft.com> - 2.7.4-16
- Bump release to rebuild for new kernel release

* Wed Apr 09 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.4-15
- Bump release to match updates from 'unsigned' spec
- Re-name the package to xpmem-modules-signed.

* Sat Apr 05 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.7.4-14
- Bump release to rebuild for new kernel release

* Fri Mar 14 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.7.4-13
- Bump release to rebuild for new kernel release

* Tue Mar 11 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.7.4-12
- Bump release to rebuild for new kernel release

* Mon Mar 10 2025 Chris Co <chrco@microsoft.com> - 2.7.4-11
- Bump release to rebuild for new kernel release

* Wed Mar 05 2025 Rachel Menge <rachelmenge@microsoft.com> - 2.7.4-10
- Bump release to rebuild for new kernel release

* Tue Mar 04 2025 Rachel Menge <rachelmenge@microsoft.com> - 2.7.4-9
- Bump release to rebuild for new kernel release

* Wed Feb 19 2025 Chris Co <chrco@microsoft.com> - 2.7.4-8
- Bump release to rebuild for new kernel release

* Tue Feb 11 2025 Rachel Menge <rachelmenge@microsoft.com> - 2.7.4-7
- Bump release to rebuild for new kernel release

* Wed Feb 05 2025 Tobias Brick <tobiasb@microsoft.com> - 2.7.4-6
- Bump release to rebuild for new kernel release

* Tue Feb 04 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 2.7.4-5
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 2.7.4-4
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 2.7.4-3
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 2.7.4-2
- Bump release to match kernel

* Sat Jan 18 2025 Binu Jose Philip <bphilip@microsoft.com> - 2.7.4-1
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
