# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit	06ae09c8d09ff62a8b69e45af67fc31974c30244

Name:		driverctl
Version:	0.101
Release: 19%{?dist}
Summary:	Device driver control utility

# Automatically converted from old format: LGPLv2 - review is highly recommended.
License:	LicenseRef-Callaway-LGPLv2
URL:		https://gitlab.com/driverctl/driverctl
BuildArch:	noarch

# rpm doesn't grok the gitlab url but spectool understands this monster
Source0:	https://gitlab.com/driverctl/%{name}/repository/archive.tar.gz?ref=%{version}#/%{name}-%{version}-%{commit}.tar.gz

# for udev macros
BuildRequires: systemd
BuildRequires: make
Requires(post,postun): %{_sbindir}/udevadm
Requires: coreutils udev

%description
driverctl is a tool for manipulating and inspecting the system
device driver choices.

Devices are normally assigned to their sole designated kernel driver
by default. However in some situations it may be desireable to
override that default, for example to try an older driver to
work around a regression in a driver or to try an experimental alternative
driver. Another common use-case is pass-through drivers and driver
stubs to allow userspace to drive the device, such as in case of
virtualization.

driverctl integrates with udev to support overriding
driver selection for both cold- and hotplugged devices from the
moment of discovery, but can also change already assigned drivers,
assuming they are not in use by the system. The driver overrides
created by driverctl are persistent across system reboots
by default.

%prep
%setup -q -n %{name}-%{version}-%{commit}

%install
%make_install PREFIX=%{_prefix} SBINDIR=%{_sbindir}

%files
%license COPYING
%doc README TODO
%{_sbindir}/driverctl
%{_udevrulesdir}/*.rules
%{_udevrulesdir}/../vfio_name
%{_unitdir}/driverctl@.service
%dir %{_sysconfdir}/driverctl.d
%{_datadir}/bash-completion/
%{_mandir}/man8/driverctl.8*

%post
%udev_rules_update

%postun
%udev_rules_update

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 0.101-16
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 20 2018 Timothy Redaelli <tredaelli@redhat.com> - 0.101-1
- Fix shellcheck warnings
- Install bash-completion as driverctl instead of driverctl-bash-completion.sh
- fix load_override for non-PCI bus
- Make sure driverctl had loaded all the overrides before basic.target

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.95-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.95-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.95-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.95-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Timothy Redaelli <tredaelli@redhat.com> - 0.95-1
- Update to 0.95
- update URLs to new group-based location

* Fri Sep 16 2016 Panu Matilainen <pmatilai@redhat.com> - 0.91-1
- Use a relative path from udevrulesdir
- Use fedorable source url which spectool actually understands
- Move bash completions to newer standard in %%{_datadir}/bash-completion
- Use %%make_install macro
- Require /usr/sbin/udevadm for %%post and %%postun

* Fri Sep 2 2016 Panu Matilainen <pmatilai@redhat.com> - 0.74-1
- Initial package
