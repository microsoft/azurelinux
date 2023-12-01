Summary:        Multi-format archive and compression library
Name:           libarchive
Version:        3.7.1
Release:        1%{?dist}
# Certain files have individual licenses. For more details see contents of "COPYING".
License:        BSD AND Public Domain AND (ASL 2.0 OR CC0 1.0 OR OpenSSL)
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.libarchive.org/
Source0:        https://github.com/libarchive/libarchive/releases/download/v%{version}/%{name}-%{version}.tar.gz
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

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*
%{_bindir}
%exclude %{_libdir}/debug/

%files devel
%defattr(-,root,root)
%{_includedir}
%{_mandir}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
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

* Fri Apr 02 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.4.2-4
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
