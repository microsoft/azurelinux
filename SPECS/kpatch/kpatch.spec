Summary:        Kpatch tooling
Name:           kpatch
Version:        0.9.6
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/dynup/kpatch
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  binutils
BuildRequires:  dnf-utils
BuildRequires:  elfutils
BuildRequires:  elfutils-devel
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  kernel-headers

ExclusiveArch:  x86_64

%description
Kpatch is a Linux dynamic kernel patching infrastructure which allows you to patch
a running kernel without rebooting or restarting any processes.
It enables sysadmins to apply critical security patches to the kernel immediately,
without having to wait for long-running tasks to complete, for users to log off, or
for scheduled reboot windows.
It gives more control over uptime without sacrificing security or stability.

%package build
Summary:        Tools for building livepatches with kpatch.
Group:          Development/Tools

Requires:       numactl-devel
Requires:       openssl
Requires:       patch
Requires:       rpm-build
Requires:       wget

%description build
%{summary}

%prep
%autosetup

%build
%make_build

%install
%make_install PREFIX=%{_prefix}

# We don't need to install manuals.
rm -rf %{buildroot}%{_mandir}

%post
%systemd_post kpatch.service

%preun
%systemd_preun kpatch.service

%files
%defattr(-,root,root)
%license COPYING
%config(noreplace) %{_sysconfdir}/init/kpatch.conf
%{_sbindir}/kpatch
%{_libdir}/systemd/system/kpatch.service

%files build
%license COPYING
%{_libexecdir}/kpatch/*
%{_datadir}/kpatch/patch/*
%{_bindir}/kpatch-build

%changelog
* Fri Jun 17 2022 Jon Slobodzian <joslobo@microsoft.com> - 0.9.6-2
- Fix ARM64 build break (exclusive to AMD64)

* Wed Jun 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.6-1
- Original version for CBL-Mariner.
- License verified.
