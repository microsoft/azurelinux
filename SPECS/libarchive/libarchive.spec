Summary:        Multi-format archive and compression library
Name:           libarchive
Version:        3.7.7
Release:        4%{?dist}
# Certain files have individual licenses. For more details see contents of "COPYING".
License:        BSD AND Public Domain AND (ASL 2.0 OR CC0 1.0 OR OpenSSL)
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.libarchive.org/
Source0:        https://github.com/libarchive/libarchive/releases/download/v%{version}/%{name}-%{version}.tar.gz
Patch0:         CVE-2025-1632.patch
Patch1:         CVE-2025-25724.patch
Patch2:         CVE-2025-5914.patch
Patch3:         CVE-2025-5915.patch
Patch4:         CVE-2025-5916.patch
Patch5:         CVE-2025-5917.patch
Patch6:         CVE-2025-5918.patch
Patch7:         CVE-2025-60753.patch
Provides:       bsdtar = %{version}-%{release}

BuildRequires:  xz-libs
BuildRequires:  xz-devel
BuildRequires:  xz-libs
Requires:       xz-libs

%description
Multi-format archive and compression library

%package	devel
Summary:        Header and development files
Requires:       %{name} = %{version}

%description	devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
export CFLAGS="%{optflags}"
./configure  --prefix=%{_prefix} --disable-static

make %{?_smp_mflags}

%install
rm -rf %{buildroot}%{_infodir}
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print
mv %{buildroot}%{_mandir}/man1/* .

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%license bsdcat.1
%license bsdtar.1
%license bsdcpio.1
%license bsdunzip.1
%{_libdir}/*.so.*
%{_bindir}
%exclude %{_libdir}/debug/

%files devel
%defattr(-,root,root)
%{_includedir}
%doc %{_mandir}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Jan 19 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.7.7-4
- Patch for CVE-2025-60753

* Thu Jun 26 2025 Sumit Jena <v-sumitjena@microsoft.com> - 3.7.7-3
- Patch CVE-2025-5914, CVE-2025-5915, CVE-2025-5916, CVE-2025-5917, CVE-2025-5918

* Tue Mar 11 2025 Kanishk Bansal <kanbansal@microsoft.com> - 3.7.7-2
- Patch CVE-2025-1632, CVE-2025-25724

* Tue Oct 15 2024 Nan Liu <liunan@microsoft.com> - 3.7.7-1
- Upgrade to 3.7.7 - Fix CVE-2024-48957, CVE-2024-48958, CVE-2024-20696
- Remove unused patches

* Tue Jun 25 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 3.7.1-2
- Patch CVE-2024-26256 and CVE-2024-37407

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.7.1-1
- Auto-upgrade to 3.7.1 - Azure Linux 3.0 - package upgrades

* Thu Dec 01 2022 Muhammad Falak <mwani@microsoft.com> - 3.6.1-2
- Patch CVE-2022-36227

* Mon Jun 13 2022 Muhammad Falak <mwani@microsoft.com> - 3.6.1-1
- Bump version to 3.6.1 to address CVE-2022-26280

* Tue Mar 15 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 3.6.0-1
- Upgrading to v3.6.0

* Thu Feb 03 2022 Muhammad Falak <mwani@microsoft.com> - 3.4.2-5
- Backport patch from upstream to fix 'test_write_disk_secure'

* Fri Apr 02 2021 Thomas Crain <thcrain@microsoft.com> - 3.4.2-4
- Merge the following releases from 1.0 to dev branch
- henry.beberman@microsoft.com, 3.4.2-3: Update Source URL to GitHub instead of libarchive.org

*   Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 3.4.2-3
-   Provide bsdtar for base package
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.4.2-2
-   Added %%license line automatically
*   Fri May 01 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.4.2-1
-   Bumping version up to 3.4.2 to fix following CVEs:
-       CVE-2018-1000877,
-       CVE-2018-1000878,
-       CVE-2018-1000879,
-       CVE-2018-1000880,
-       CVE-2019-1000019,
-       CVE-2019-1000020,
-       CVE-2019-18408, and
-       CVE-2020-9308.
-   Fixed "Source0" and "URL" tags.
-   License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.3.3-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 3.3.3-1
-   Updated to latest version

*   Fri Sep 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.3.1-2
-   Add xz-libs and xz-devel to BuildRequires and Requires

*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 3.3.1-1
-   Upgrade version to 3.3.1

*   Tue Sep 27 2016 Alexey Makhalov <amakhalov@vmware.com> 3.2.1-1
-   Update version to 3.2.1

*   Thu Sep 22 2016 Anish Swaminathan <anishs@vmware.com> 3.1.2-7
-   Adding patch for security fix CVE-2016-6250

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.2-6
-   GA - Bump release of all rpms

*   Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-5
-   Moving static lib files to devel package.

*   Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-4
-   Removing la files from packages.

*   Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 3.1.2-3
-   Adding patches for security fixes CVE-2013-2011 and CVE-2015-2304.

*   Wed Jul 8 2015 Alexey Makhalov <amakhalov@vmware.com> 3.1.2-2
-   Added devel package, dist tag. Use macroses part.

*   Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 3.1.2-1
-   Initial build.  First version
