Summary:        Shell script to auto detect free size on disk and grow partition.
Name:           cloud-utils-growpart
Version:        0.32
Release:        2%{?dist}
License:        GPLv3
Group:          System Environment
Source0:        https://launchpad.net/cloud-utils/trunk/%{version}/+download/cloud-utils-%{version}.tar.gz
URL:            https://launchpad.net/cloud-utils
Vendor:         Microsoft Corporation
Distribution:   Mariner
Requires:       gptfdisk
Requires:       gawk
Requires:       util-linux
BuildArch:      noarch
Patch0:         growpart-remove-flock-disk-locking.patch

%description
Cloud-utils brings in growpart script. This script is very useful for
detecting available disk size and grow the partition.
This is generally used by cloud-init for disk space manangement on cloud images.

%prep
%setup -q -n cloud-utils-%{version}
%patch0 -p1

%build
%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
cp bin/growpart $RPM_BUILD_ROOT/%{_bindir}/
cp man/growpart.* $RPM_BUILD_ROOT/%{_mandir}/man1/

%files
%license LICENSE
%{_bindir}/growpart
%doc %{_mandir}/man1/growpart.*

%changelog
*   Tue Apr 27 2021 Chris Co <chrco@microsoft.com> - 0.32-2
-   Add patch to handle unexpected timeout
*   Sat Mar 13 2021 Henry Beberman <henry.beberman@microsoft.com> 0.32-1
-   Update to version 0.32 for more robust parsing of kernel version in growpart
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.30-6
-   Added %%license line automatically
*   Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> 0.30-5
-   Renaming cloud-utils to cloud-utils-growpart
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.30-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
-   License verified.
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 0.30-3
-   Requires util-linux or toybox
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.30-2
-   Fix arch
*   Wed Mar 29 2017 Kumar Kaushik <kaushikk@vmware.com> 0.30-1
-   Initial build.  First version
