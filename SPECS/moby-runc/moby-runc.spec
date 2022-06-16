%define         upstream_name runc
%define         commit_hash a916309fff0f838eb94e928713dbc3c0d0ac7aa4

Summary:        CLI tool for spawning and running containers per OCI spec.
Name:           moby-%{upstream_name}
# update "commit_hash" above when upgrading version
Version:        1.1.2
Release:        2%{?dist}
License:        ASL 2.0
URL:            https://github.com/opencontainers/runc
Group:          Virtualization/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner

Source0:        https://github.com/opencontainers/runc/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

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
%setup -q -n %{upstream_name}-%{version}

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
