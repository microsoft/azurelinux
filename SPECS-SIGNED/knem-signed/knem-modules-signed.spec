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

%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_azurelinux_build_kernel_version %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_kernel_release %(/bin/rpm -q --queryformat '%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers) | /bin/cut -d . -f 1)

%global KVERSION %{target_kernel_version_full}

# set package name
%{!?_name: %global _name knem}
%global non_kmp_pname %{_name}-modules

# knem-modules is a sub-package in SPECS/knem. We are making that into a
# main package for signing.

Summary:	 KNEM: High-Performance Intra-Node MPI Communication
Name:		 %{_name}-modules
Version:	 1.1.4.90mlnx3
Release:	 1%{?dist}
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

Source0:         %{name}-%{version}-%{release}.%{_arch}.rpm
Source1:         knem.ko
BuildRoot:       /var/tmp/%{name}-%{version}-build

Requires:       kernel = %{target_kernel_version_full}
Requires:       kmod

%description
KNEM is a Linux kernel module enabling high-performance intra-node MPI communication for large messages. KNEM offers support for asynchronous and vectorial data transfers as well as offloading memory copies on to Intel I/OAT hardware.
See http://knem.gitlabpages.inria.fr for details.

%global debug_package %{nil}

%prep

%build
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

%install
cp -r %{SOURCE1} %{buildroot}/lib/modules/%{KVERSION}/extra/knem/knem.ko

%clean
rm -rf %{buildroot}

%post
depmod %{KVERSION} -a

%postun
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
    depmod %{KVERSION} -a
fi

%files
%license COPYING COPYING.BSD-3 COPYING.GPL-2
/lib/modules/
%if %{IS_RHEL_VENDOR}
%if ! 0%{?fedora}
%config(noreplace) %{_sysconfdir}/depmod.d/%{_name}.conf
%endif
%endif


%changelog
* Tue Dec  16 2024 Binu Jose Philip <bphilip@microsoft.com> - 1.1.4.90mlnx3
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
