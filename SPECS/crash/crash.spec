Name:          crash
Version:       8.0.1
Release:       3%{?dist}
Summary:       kernel crash analysis utility for live systems, netdump, diskdump, kdump, LKCD or mcore dumpfiles
Group:         Development/Tools
Vendor:        Microsoft Corporation
Distribution:  Mariner
URL:           https://github.com/crash-utility/crash
Source0:       https://github.com/crash-utility/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# crash requires gdb tarball for the build. There is no option to use the host gdb. For crash 8.0.1 the newest supported gdb version is 10.2.
Source1:       https://ftp.gnu.org/gnu/gdb/gdb-10.2.tar.gz
# lzo patch sourced from https://src.fedoraproject.org/rpms/crash/blob/rawhide/f/lzo_snappy_zstd.patch
Patch0:        lzo_snappy_zstd.patch
License:       GPLv3+
BuildRequires: binutils
BuildRequires: glibc-devel
BuildRequires: lzo-devel
BuildRequires: ncurses-devel
BuildRequires: snappy-devel
BuildRequires: zlib-devel
BuildRequires: zstd-devel
Requires:      binutils

%description
The core analysis suite is a self-contained tool that can be used to investigate either live systems, kernel core dumps created from the netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch offered by Mission Critical Linux, or the LKCD kernel patch.

%package devel
Group:         Development/Libraries
Summary:       Libraries and headers for %{name}
Requires:      %{name} = %{version}-%{release}

%description devel
The core analysis suite is a self-contained tool that can be used to investigate either live systems, kernel core dumps created from the netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch offered by Mission Critical Linux, or the LKCD kernel patch.

This package contains libraries and header files need for development.

%prep
%autosetup -n %{name}-%{version}
cp %{SOURCE1} .

%build
make RPMPKG=%{version}-%{release}

%install
mkdir -p %{buildroot}%{_bindir}
%make_install
mkdir -p %{buildroot}%{_mandir}/man8
install -pm 644 crash.8 %{buildroot}%{_mandir}/man8/crash.8
mkdir -p %{buildroot}%{_includedir}/crash
chmod 0644 defs.h
cp -p defs.h %{buildroot}%{_includedir}/crash

%files
%defattr(-,root,root)
%license COPYING3
%{_bindir}/crash
%{_mandir}/man8/crash.8.gz
%doc COPYING3 README

%files devel
%defattr(-,root,root)
%dir %{_includedir}/crash
%{_includedir}/crash/*.h

%changelog
* Mon Oct 09 2023 Chris Co <chrco@microsoft.com> - 8.0.1-3
- Add patch from Fedora to enable lzo, snappy, zstd compression support
- Remove unused crash printk fix patch

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 8.0.1-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Apr 27 2022 Mateusz Malisz <mamalisz@microsoft.com> - 8.0.1-1
- Update to 8.0.1

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.2.9-3
- Removing the explicit %%clean stage.

* Wed Oct 27 2021 Muhammad Falak <mwani@microsft.com> - 7.2.9-2
- Remove epoch

* Tue Feb 23 2021 Andrew Phelps <anphel@microsoft.com> 7.2.9-1
- Update version to 7.2.9.
- Add patches to support new printk in 5.10 kernel

* Sat Jun 20 2020 Andrew Phelps <anphel@microsoft.com> 7.2.8-2
- Add Source1 with gdb source tarball to support offline build.

* Wed Jun 17 2020 Joe Schmitt <joschmit@microsoft.com> 7.2.8-1
- Update version to 7.2.8.
- Update URL.
- Update Source0.
- Fix license.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 7.2.7-2
- Added %%license line automatically

* Wed Mar 25 2020 Emre Girgin <mrgirgin@microsoft.com> 7.2.7-1
- Split the package into two 'crash' and 'crash-gcore-command'.
- Update version to 7.2.7. Updated URL and Source0 links.Verified License.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 7.2.3-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 7.2.3-1
- Upgrading to version 7.2.3

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 7.1.8-2
- Aarch64 support

* Wed Mar 22 2017 Alexey Makhalov <amakhalov@vmware.com> 7.1.8-1
- Update version to 7.1.8 (it supports linux-4.9)
- Disable a patch - it requires a verification.

* Fri Oct 07 2016 Alexey Makhalov <amakhalov@vmware.com> 7.1.5-2
- gcore-support-linux-4.4.patch

* Fri Sep 30 2016 Alexey Makhalov <amakhalov@vmware.com> 7.1.5-1
- Update version to 7.1.5 (it supports linux-4.4)
- Added gcore plugin
- Remove zlib-devel requirement from -devel subpackage

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.1.4-2
- GA - Bump release of all rpms

* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 7.1.4-1
- Updated to version 7.1.4

* Wed Nov 18 2015 Anish Swaminathan <anishs@vmware.com> 7.1.3-1
- Initial build. First version
