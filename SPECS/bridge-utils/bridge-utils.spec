Summary:      Utilities for configuring and managing bridge devices
Name:         bridge-utils
Version:      1.7.1
Release:      2%{?dist}
License:      GPLv2+
URL:          https://wiki.linuxfoundation.org/networking/bridge
Group:        System Environment/Base
Vendor:       Microsoft Corporation
Distribution: Mariner
Source0:      https://kernel.org/pub/linux/utils/net/%{name}/%{name}-%{version}.tar.xz

%description
The bridge-utils package contains a utility needed to create and manage bridge devices. This is useful in setting up networks for a hosted virtual machine (VM).
%prep
%setup -q
%build
autoconf
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/brctl
%{_mandir}/man8/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.7.1-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Jan 10 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.7.1-1
- Upgrade to 1.7.1

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.6-4
- Added %%license line automatically

*   Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> 1.6-3
-   Update URL.
-   Update Source0 with valid URL.
-   Remove sha1 macro.
-   Fix changelog styling.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.6-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 1.6-1
-   Upgraded to version 1.6
*   Mon Sep 12 2016 Alexey Makhalov <amakhalov@vmware.com> 1.5-3
-   Update patch to fix-2.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5-2
-   GA - Bump release of all rpms
*   Tue May 19 2015 Divya Thaluru <dthaluru@vmware.com> 1.5-1
-   Initial build.	First version
