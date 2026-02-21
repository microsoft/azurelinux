# Copyright © INRIA 2009-2010
# Brice Goglin <Brice.Goglin@inria.fr>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

%global debug_package %{nil}
# The default %%__os_install_post macro ends up stripping the signatures off of the kernel module.
%define __os_install_post %{__os_install_post_leave_signatures} %{nil}

%global target_azl_build_kernel_version %azl_kernel_hwe_version
%global target_kernel_release %azl_kernel_hwe_release
%global target_kernel_version_full %{target_azl_build_kernel_version}-%{target_kernel_release}%{?dist}
%global release_suffix _%{target_azl_build_kernel_version}.%{target_kernel_release}

%global KVERSION %{target_kernel_version_full}

# set package name
%{!?_name: %global _name knem-modules}

# knem-modules is a sub-package in SPECS/knem. We are making that into a
# main package for signing.

Summary:	 KNEM: High-Performance Intra-Node MPI Communication
Name:		 %{_name}-signed
Version:	 1.1.4.90mlnx3
Release:	 23%{release_suffix}%{?dist}
Provides:	 knem-mlnx = %{version}-%{release}
Obsoletes:	 knem-mlnx < %{version}-%{release}
License:	 BSD and GPLv2
Group:		 System Environment/Libraries
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
ExclusiveArch:   x86_64

#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:         %{_name}-%{version}-%{release}.%{_arch}.rpm
Source1:         knem.ko
BuildRoot:       /var/tmp/%{_name}-%{version}-build

%description
KNEM is a Linux kernel module enabling high-performance intra-node MPI communication for large messages. KNEM offers support for asynchronous and vectorial data transfers as well as offloading memory copies on to Intel I/OAT hardware.
See http://knem.gitlabpages.inria.fr for details.

%package -n %{_name}
Summary:        KNEM: High-Performance Intra-Node MPI Communication
Requires:       kernel = %{target_kernel_version_full}
Requires:       kmod

%description -n %{_name}
%{description}

%prep

%build
mkdir rpm_contents
pushd rpm_contents

# This spec's whole purpose is to inject the signed modules
rpm2cpio %{SOURCE0} | cpio -idmv
cp -rf %{SOURCE1} ./lib/modules/%{KVERSION}/extra/knem/knem.ko
popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

popd


%post -n %{_name}
depmod %{KVERSION} -a

%postun -n %{_name}
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
    depmod %{KVERSION} -a
fi

%files -n %{_name}
%{_datadir}/licenses
/lib/modules/

%changelog
* Mon Feb 10 2026 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.1.4.90mlnx3-23
- Tweak specs to use dynamic versioning for kernel

* Tue Nov 04 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.1.4.90mlnx3-22
- Bump release to rebuild for new release.

* Fri Oct 10 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.4.90mlnx3-21
- Bump release to rebuild for new release

* Thu May 29 2025 Nicolas Guibourge <nicolasg@microsoft.com> - 1.1.4.90mlnx3-20
- Add kernel version and release nb into release nb

* Fri May 23 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.4.90mlnx3-19
- Bump release to rebuild for new kernel release

* Tue May 13 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 1.1.4.90mlnx3-18
- Bump release to rebuild for new kernel release

* Tue Apr 29 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 1.1.4.90mlnx3-17
- Bump release to rebuild for new kernel release

* Fri Apr 25 2025 Chris Co <chrco@microsoft.com> - 1.1.4.90mlnx3-16
- Bump release to rebuild for new kernel release

* Wed Apr 09 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.4.90mlnx3-15
- Bump release to match updates from 'unsigned' spec
- Re-name the package to knem-modules-signed.

* Sat Apr 05 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.4.90mlnx3-14
- Bump release to rebuild for new kernel release

* Fri Mar 14 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.4.90mlnx3-13
- Bump release to rebuild for new kernel release

* Tue Mar 11 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.4.90mlnx3-12
- Bump release to rebuild for new kernel release

* Mon Mar 10 2025 Chris Co <chrco@microsoft.com> - 1.1.4.90mlnx3-11
- Bump release to rebuild for new kernel release

* Wed Mar 05 2025 Rachel Menge <rachelmenge@microsoft.com> - 1.1.4.90mlnx3-10
- Bump release to rebuild for new kernel release

* Tue Mar 04 2025 Rachel Menge <rachelmenge@microsoft.com> - 1.1.4.90mlnx3-9
- Bump release to rebuild for new kernel release

* Wed Feb 19 2025 Chris Co <chrco@microsoft.com> - 1.1.4.90mlnx3-8
- Bump release to rebuild for new kernel release

* Tue Feb 11 2025 Rachel Menge <rachelmenge@microsoft.com> - 1.1.4.90mlnx3-7
- Bump release to rebuild for new kernel release

* Wed Feb 05 2025 Tobias Brick <tobiasb@microsoft.com> - 1.1.4.90mlnx3-6
- Bump release to rebuild for new kernel release

* Tue Feb 04 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 1.1.4.90mlnx3-5
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 1.1.4.90mlnx3-4
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 1.1.4.90mlnx3-3
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 1.1.4.90mlnx3-2
- Bump release to match kernel

* Sat Jan 18 2025 Binu Jose Philip <bphilip@microsoft.com> - 1.1.4.90mlnx3-1
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
