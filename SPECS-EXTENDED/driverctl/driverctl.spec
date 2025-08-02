Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global commit	2ba60536eb20ca0a6a751bd8b6501dba84ec45d3

Name:		driverctl
Version:	0.115
Release:	1%{?dist}
Summary:	Device driver control utility

License:	LGPLv2
URL:		https://gitlab.com/driverctl/driverctl
BuildArch:	noarch

# rpm doesn't grok the gitlab url but spectool understands this monster
Source0:	https://gitlab.com/driverctl/%{name}/repository/archive.tar.gz?ref=%{version}#/%{name}-%{version}-%{commit}.tar.gz

# for udev macros
BuildRequires: systemd
Requires(post,postun): %{_bindir}/udevadm
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
%make_install UDEVDIR=/usr/lib/udev/ UNITDIR=%{_unitdir}

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
* Thu Oct 24 2024 Sumit Jena <v-sumitjena@microsoft.com> - 0.115-1
- Update to version 0.115
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.111-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sun Jun 6 2021 Jon Slobodzian- 0.111-1
- Upgraded to 0.111
- Fixed build issues for Mariner

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
