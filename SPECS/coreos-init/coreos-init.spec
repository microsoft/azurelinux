Name:           coreos-init
Version:        0.0.1
Release:        2%{?dist}
Summary:        Init scripts for Flatcar (systemd units, scripts, configs)

License:        BSD-3-Clause
URL:            https://github.com/flatcar/init
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
BuildArch:      noarch

%global commit 8bd8a82fb22bc46ea2cf7da94d58655e102ca26d
%global shortcommit %(echo %{commit} | cut -c1-7)

# tarball matches the ebuild SRC_URI pattern:
Source0:        https://github.com/flatcar/init/archive/%{commit}/init-%{commit}.tar.gz#/%{name}-%{version}-%{shortcommit}.tar.gz
Patch0:         support-UKI-mode-by-restoring-firstboot-addon.patch
Patch1:         Add-noop-sysupdate-transfer-config.patch
# optional tests, analogous to IUSE=test
%bcond_without tests

# The upstream repo contains systemd units/scripts/configs for Flatcar init. [1](https://github.com/flatcar/init)
BuildRequires:  make
BuildRequires:  systemd-rpm-macros

# DEPEND/RDEPEND mapping from ebuild:
# DEPEND: openssh, rpcbind
# RDEPEND adds: logrotate, parted, gptfdisk, systemd >= 207, coreos-cloudinit >= 0.1.2-r5
#
# NOTE: package names can differ in Azure Linux; adjust if your repo uses split names
# (e.g., openssh-server instead of openssh).
BuildRequires:       openssh
BuildRequires:       rpcbind
Requires:       logrotate
Requires:       parted
Requires:       gptfdisk
Requires:       systemd >= 207
Requires:       coreos-cloudinit

%if %{with tests}
BuildRequires:  python3
%endif

%description
System initialization content for Flatcar-style images: systemd unit files, helper scripts,
and configuration files used during early boot and provisioning. The upstream project
organizes content under configs/, scripts/, systemd/, udev/, etc. [1](https://github.com/flatcar/init)

%prep
%autosetup -p1 -n init-%{commit}

%install
rm -rf %{buildroot}

# ebuild: emake DESTDIR="${D}" install
%{__make} DESTDIR=%{buildroot} install

# ebuild: systemd_enable_service rpcbind.target rpcbind.service
# In systemd, enabling a unit is implemented by creating symlinks in a target’s .wants dir. [3](https://www.flatcar.org/docs/latest/setup/systemd/getting-started/)
install -d %{buildroot}%{_sysconfdir}/systemd/system/rpcbind.target.wants
ln -sf %{_unitdir}/rpcbind.service %{buildroot}%{_sysconfdir}/systemd/system/rpcbind.target.wants/rpcbind.service
# removing files which in conflict with other flatcar packages while installation.
rm %{buildroot}/usr/lib/systemd/system/ignition-delete-config.service
rm %{buildroot}/usr/lib/systemd/system/sshd-keygen.service
rm -rf  %{buildroot}/etc/issue

# Removing unwanted files that cause failures in Azure Linux image compliance checks
rm -f %{buildroot}%{_unitdir}/sysinit.target.wants/ignition-delete-config.service

# Generate file manifest automatically (avoids missing files when upstream changes)
# This will list all files installed under %{buildroot} as absolute paths.
find %{buildroot} -type f -o -type l \
  | sed "s|^%{buildroot}||" \
  | sort -u > %{name}.files

%check
%if %{with tests}
# Upstream includes a tests/ directory; if tests are wired via Makefile, run them.
# If this fails in Azure Linux, replace with the repo’s actual test invocation.
%{__make} test
%endif

%post
# Standard systemd scriptlets for packages shipping unit files
%systemd_post rpcbind.target 
%systemd_post rpcbind.service

%preun
%systemd_preun rpcbind.target
%systemd_preun rpcbind.service

%postun
%systemd_postun rpcbind.target
%systemd_postun rpcbind.service

%files -f %{name}.files
%license LICENSE NOTICE
%doc README.md

%changelog
* Mon Feb 02 2026 Sandeep Karambelkar <skarambelkar@microsoft.com> - 0.0.1-2
- Cleanup unwanted files

* Mon Feb 02 2026 Sumit Jena (HCL Technologies Ltd) - 0.0.1-1
- Initial Azure Linux import from the source project (license: same as "License" tag).
- Add patch from Flatcar upstream with noop systemd-sysupdate transfer config to prevent service failure.
- Change .transfer to .conf, since .transfer is only introduced in systemd 257 (.conf stays supported for compatibility)
- If we bump to more recent upstream commit, we should keep .conf while systemd on < 257.
- License verified.
