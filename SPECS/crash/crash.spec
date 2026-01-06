%global gdb_version 16.2
Name:          crash
Version:       9.0.0
Release:       1%{?dist}
Summary:       kernel crash analysis utility for live systems, netdump, diskdump, kdump, LKCD or mcore dumpfiles
Group:         Development/Tools
Vendor:        Microsoft Corporation
Distribution:  Azure Linux
URL:           https://github.com/crash-utility/crash
Source0:       https://github.com/crash-utility/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# crash requires gdb tarball for the build. There is no option to use the host gdb. For crash 9.0.0, the minimum required gdb version is 16.2.
Source1:       gdb-%{gdb_version}.tar.gz
# lzo patch sourced from https://src.fedoraproject.org/rpms/crash/blob/rawhide/f/lzo_snappy_zstd.patch

# Since we have two source tarballs to patch, we use separate patch numbering
# to indicate where patches are applied where during the prep section.
# Patch 0-99 will automatically apply to Source0 (crash)
# Patch 100+ will automatically apply to Source1 (gdb)

# Patches for crash sources
Patch0:        lzo_snappy_zstd.patch
# Patches for gdb sources
Patch100:      CVE-2022-37434.patch
Patch101:      CVE-2025-11082.patch

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

%ifarch x86_64
%package target-arm64
Summary:       Crash executable for analyzing arm64 crash dumps on x86_64 host machines
Group:         Development/Libraries

%description target-arm64
This package contains the "crash-target-arm64" binary for analyzing arm64 crash dumps on x86_64 host machines.
%endif

%prep
# -N skips automatic patch application
%autosetup -n %{name}-%{version} -N

# Apply only patches 0-99 to original crash source
%autopatch -p1 -M 99

# Extract and patch secondary gdb sources, re-tar and gzip them, and clean up the working directory.
# Note: crash's make expects the gdb tarball to be named with its version only, gdb-[version].tar.gz, e.g.: gdb-10.2.tar.gz
tar -xzf %{SOURCE1}
pushd gdb-%{gdb_version}
%autopatch -p1 -m 100
popd
# Re-tar with consistent timestamps for reproducibility
tar --sort=name \
    --mtime="2021-04-26 00:00Z" \
    --owner=0 --group=0 --numeric-owner \
    -czf gdb-%{gdb_version}.tar.gz gdb-%{gdb_version}
rm -rf gdb-%{gdb_version}/

%build
%ifarch x86_64
# For x86_64 only, build a separate crash binary for target=ARM64
# After creating the "crash-target-arm64" binary, clean everything and rebuild for native target
make RPMPKG=%{version}-%{release} target=ARM64
cp -v crash crash-target-arm64
rm -rf ./gdb-%{gdb_version}
make clean
# Need to specify target=X86_64 here, since this parameter is "sticky" from the previous build
make RPMPKG=%{version}-%{release} target=X86_64
%else
make RPMPKG=%{version}-%{release}
%endif

%install
mkdir -p %{buildroot}%{_bindir}
%make_install
%ifarch x86_64
cp -v crash-target-arm64 %{buildroot}%{_bindir}/crash-target-arm64
%endif

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
%doc README

%files devel
%defattr(-,root,root)
%dir %{_includedir}/crash
%{_includedir}/crash/*.h

%ifarch x86_64
%files target-arm64
%defattr(-,root,root)
%{_bindir}/crash-target-arm64
%endif

%changelog
* Thu Nov 20 2025 Chris Co <chrco@microsoft.com> - 9.0.0-1
- Update to 9.0.0

* Fri Oct 03 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 8.0.4-5
- Update gdb-10.2-4.tar.gz to address CVE-2025-11082

* Mon Apr 21 2025 Kanishk Bansal <kanbansal@microsoft.com> - 8.0.4-4
- Update gdb-10.2-3.tar.gz to address CVE-2021-20197, CVE-2022-47673, CVE-2022-47696

* Tue Jun 18 2024 Andrew Phelps <anphel@microsoft.com> - 8.0.4-3
- Add crash-target-arm64 binary to analyze aarch64 dumps on x86_64 machine

* Mon Jun 03 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 8.0.4-2
- Update gdb-10.2-2.tar.gz to address CVE-2022-37434

* Thu Dec 07 2023 Andrew Phelps <anphel@microsoft.com> - 8.0.4-1
- Upgrade to 8.0.4

* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.3-1
- Auto-upgrade to 8.0.3 - Azure Linux 3.0 - package upgrades

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
