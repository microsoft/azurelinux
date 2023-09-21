Summary:        The OpenSource IPsec-based VPN Solution
Name:           strongswan
Version:        5.9.10
Release:        2%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.strongswan.org/
Source0:        https://download.strongswan.org/%{name}-%{version}.tar.bz2
Patch0:         strongswan-fix-make-check.patch
Patch1:         0001-Extending-timeout-for-test-cases-with-multiple-read-.patch
BuildRequires:  autoconf
BuildRequires:  gmp-devel

%description
strongSwan is a complete IPsec implementation for Linux 2.6, 3.x, and 4.x kernels.

%prep
%autosetup -p1

%build
# Disabling "format-security" warning, not compatible with strongswan custom printf specifiers
export CCFLAGS="%{optflags}"
export CFLAGS="$CFLAGS -Wno-format-security"
%configure
sed -i '/stdlib.h/a #include <stdint.h>' src/libstrongswan/utils/utils.h &&
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%check
make check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_sysconfdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/ipsec/*
%{_libexecdir}/*
%{_mandir}/man[158]/*
%{_datadir}/strongswan/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.9.10-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Apr 26 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.9.10-1
- Auto-upgrade to 5.9.10 - Fix: Upgrade strongswan to fix CVE-2023-26463

* Thu Dec 08 2022 Henry Beberman <henry.beberman@microsoft.com> - 5.9.8-1
- Updated to version 5.9.8 to fix CVE-2022-40617

* Tue Apr 12 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 5.9.5-1
- Updated to version 5.9.5 to fix CVE-2021-45079.

* Mon Jan 03 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 5.9.3-1
- Updated to version 5.9.3.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.7.2-4
- Removing the explicit %%clean stage.

* Mon Oct 05 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 5.7.2-3
- Adding a patch to extend the timeout for the ''valid/invalid data' test case.
- Switching to %%autosetup.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 5.7.2-2
- Added %%license line automatically

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 5.7.2-1
- Update to 5.7.2. Remove CVE patch fixed in 5.7.0. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 5.6.3-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Dec 21 2018 Keerthana K <keerthanak@vmware.com> 5.6.3-3
- Fix for CVE-2018-16151 and CVE-2018-16152.

* Thu Dec 06 2018 Keerthana K <keerthanak@vmware.com> 5.6.3-2
- Fixed make check failures.

* Mon Sep 17 2018 Tapas Kundu <tkundu@vmware.com> 5.6.3-1
- Updated to 5.6.3 release

* Thu Aug 16 2018 Tapas Kundu <tkundu@vmware.com> 5.5.2-5
- Fix for CVE-2018-10811

* Mon Jul 23 2018 Ajay Kaher <akaher@vmware.com> 5.5.2-4
- Fix CVE-2018-5388

* Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 5.5.2-3
- Fix CVE-2017-11185 CVE-2017-9022 and CVE-2017-9023

* Thu Aug 24 2017 Alexey Makhalov <amakhalov@vmware.com> 5.5.2-2
- Fix compilation issue for glibc-2.26

* Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 5.5.2-1
- Update to version 5.5.2

* Wed Dec 21 2016 Xiaolin Li <xiaolinl@vmware.com>  5.5.1-1
- Initial build.
