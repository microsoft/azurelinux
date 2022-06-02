Summary:        Kpatch tooling
Name:           kpatch
Version:        0.9.6
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/dynup/kpatch
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

Requires:       binutils
Requires:       dnf-utils
Requires:       gcc
Requires:       glibc-devel
Requires:       elfutils
Requires:       elfutils-devel
Requires:       kernel-debuginfo
Requires:       kernel-headers
Requires:       numactl-devel
Requires:       openssl
# Requires:       pesign
Requires:       wget

%description
Kpatch is a Linux dynamic kernel patching infrastructure which allows you to patch
a running kernel without rebooting or restarting any processes.
It enables sysadmins to apply critical security patches to the kernel immediately,
without having to wait for long-running tasks to complete, for users to log off, or
for scheduled reboot windows.
It gives more control over uptime without sacrificing security or stability.

%package devel
Summary:        Tools for building livepatches with kpatch.
Group:          Development/Tools

%description devel
%{summary}

%prep
%autosetup

%build
%make_build

%install
%make_install PREFIX=%{_prefix}

# We don't need to install manuals.
rm -rf %{buildroot}/usr/share/man

%post
%systemd_post kpatch.service

%preun
%systemd_preun kpatch.service

%files
%license COPYING
%defattr(-,root,root)
%config(noreplace) /etc/init/kpatch.conf
/usr/sbin/kpatch
/usr/lib/systemd/system/kpatch.service

%files devel
%license COPYING
/usr/libexec/kpatch/*
/usr/share/kpatch/patch/*
/usr/bin/kpatch-build

%changelog
* Wed Jun 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.6-1
- Original version for CBL-Mariner.
- License verified.
