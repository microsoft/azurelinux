%define         upstream_name runc
%define         commit_hash ccaecfcbc907d70a7aa870a6650887b901b25b82

Summary:        CLI tool for spawning and running containers per OCI spec.
Name:           moby-%{upstream_name}
# update "commit_hash" above when upgrading version
Version:        1.1.9
Release:        4%{?dist}
License:        ASL 2.0
URL:            https://github.com/opencontainers/runc
Group:          Virtualization/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner

Source0:        https://github.com/opencontainers/runc/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         CVE-2024-21626.patch

BuildRequires:  git
BuildRequires:  golang => 1.16
BuildRequires:  go-md2man
BuildRequires:  libseccomp-devel
BuildRequires:  make

Requires:       glibc
Requires:       libgcc
Requires:       libseccomp

# conflicting packages
Conflicts: runc
Conflicts: runc-io

Obsoletes: runc
Obsoletes: runc-io

%description
runC is a CLI tool for spawning and running containers according to the OCI specification. Containers are started as a child process of runC and can be embedded into various other systems without having to run a daemon.

%prep
%autosetup -n %{upstream_name}-%{version} -p1

%build
export CGO_ENABLED=1
# note that "apparmor" and "selinux" feature are by default enabled since version 1.0.0-rc93
make %{?_smp_mflags} BUILDTAGS="seccomp" COMMIT="%{commit_hash}" man runc

%check
# only run local unit tests
make %{?_smp_mflags} COMMIT="%{commit_hash}" localunittest

%install
# must set BINDIR to force install to '/usr/bin' instead of '/usr/sbin'
make install DESTDIR="%{buildroot}" PREFIX="%{_prefix}" BINDIR="%{_bindir}" 
make install-man DESTDIR="%{buildroot}" PREFIX="%{_prefix}"

%files
%license LICENSE NOTICE
%{_bindir}/runc
%{_mandir}/*

%changelog
* Tue Jan 23 2024 Muhammad Falak <mwani@microsoft.com> - 1.1.9-4
- Address CVE-2024-21626
- Switch to autosetup

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.9-3
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.1.9-2
- Bump release to rebuild with updated version of Go.

* Tue Aug 15 2023 Muhammad Falak <mwani@microsoft.com> - 1.1.9-1
- Bump version to 1.1.9

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.5-4
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.5-3
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.5-2
- Bump release to rebuild with go 1.19.10

* Mon Apr 10 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.5-1
- Auto-upgrade to 1.1.5 - to fix CVE-2023-28642, CVE-2023-27561, CVE-2023-25809

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.2-11
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.2-10
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.2-9
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 Vince Perri <viperri@microsoft.com> - 1.1.2-8
- Add 0001-cgroups-cpuset-fix-byte-order-while-parsing-cpuset-r.patch

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.2-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.2-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.1.2-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.1.2-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.1.2-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.1.2-2
- Bump release to rebuild with golang 1.18.3

* Thu Jun 02 2022 Nicolas Guibourge <nicolasg@microsoft.com> 1.1.2-1
- Upgrade to 1.1.2 to fix CVE-2022-29162.
* Fri Jan 28 2022 Nicolas Guibourge <nicolasg@microsoft.com> 1.1.0-1
- Upgrade to 1.1.0.
- Use code from upstream instead of Azure fork.
- License verified.
* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 1.0.0~rc95+azure-2
- Increment release to force republishing using golang 1.15.13.
* Wed May 19 2021 Andrew Phelps <anphel@microsoft.com> 1.0.0~rc95+azure-1
- Update to version 1.0.0~rc95+azure to fix CVE-2021-30465
* Thu May 13 2021 Andrew Phelps <anphel@microsoft.com> 1.0.0~rc94+azure-1
- Update to version 1.0.0~rc94+azure
* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.0.0~rc10+azure-6
- Increment release to force republishing using golang 1.15.11.
* Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 1.0.0~rc10+azure-5
- Increment release to force republishing using golang 1.15.
* Wed May 20 2020 Joe Schmitt <joschmit@microsoft.com> 1.0.0~rc10+azure-4
- Remove reliance on existing GOPATH environment variable.
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.0.0~rc10+azure-3
- Added %%license line automatically
* Fri May 01 2020 Emre Girgin <mrgirgin@microsoft.com> 1.0.0~rc10+azure-2
- Renaming go to golang
* Fri Apr 03 2020 Mohan Datla <mdatla@microsoft.com> 1.0.0~rc10+azure-1
- Initial CBL-Mariner import from Azure.
* Thu Jan 23 2020 Brian Goff <brgoff@microsoft.com>
- Initial version
