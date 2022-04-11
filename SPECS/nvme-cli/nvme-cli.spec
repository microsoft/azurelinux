Summary:        NVM-Express user space tooling for Linux
Name:           nvme-cli
Version:        1.16
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/linux-nvme/nvme-cli
Source0:        https://github.com/linux-nvme/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
Requires(post): systemd
Requires(post): systemd-udev
Requires(post): util-linux

%description
NVM-Express user space tooling for Linux

%prep
%setup -q

%build
make CFLAGS="%{build_cflags} -std=gnu99 -I."

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}

%files
%defattr(-,root,root)
%license LICENSE
%{_sbindir}/nvme
%{_datadir}/bash-completion/completions/nvme
%{_datadir}/zsh/site-functions/_nvme
%{_mandir}/man1/nvme*.1*
%dir %{_sysconfdir}/nvme
%{_sysconfdir}/nvme/hostnqn
%{_sysconfdir}/nvme/hostid
%{_sysconfdir}/nvme/discovery.conf
%{_sysconfdir}/udev/rules.d/70-nvmf-autoconnect.rules
%{_sysconfdir}/udev/rules.d/71-nvmf-iopolicy-netapp.rules
%{_libdir}/dracut/dracut.conf.d/*
%{_libdir}/systemd/system/nvmf-connect@.service
%{_libdir}/systemd/system/nvmefc-boot-connections.service
%{_libdir}/systemd/system/nvmf-connect.target
%{_libdir}/systemd/system/nvmf-autoconnect.service

%post
if [ $1 -eq 1 ]; then # 1 : This package is being installed for the first time
	if [ ! -s %{_sysconfdir}/nvme/hostnqn ]; then
		echo $(%{_sbindir}/nvme gen-hostnqn) > %{_sysconfdir}/nvme/hostnqn
        fi
        if [ ! -s %{_sysconfdir}/nvme/hostid ]; then
                uuidgen > %{_sysconfdir}/nvme/hostid
        fi

	# apply udev and systemd changes that we did
	systemctl daemon-reload
	udevadm control --reload-rules && udevadm trigger
fi

%changelog
* Fri Mar 25 2022 Andrew Phelps <anphel@microsoft.com> - 1.16-2
- Remove check tests which fail to run properly on daily build machines
- Update spec with changes based on upstream github project's nvme.spec.in

* Wed Mar 09 2022 Andrew Phelps <anphel@microsoft.com> - 1.16-1
- Upgrade to version 1.16
- Enable check tests

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.8.1-3
- Added %%license line automatically

* Tue Mar 24 2020 Paul Monson <paulmon@microsoft.com> 1.8.1-2
- Add CFLAGS

* Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 1.8.1-1
- Update to 1.8.1. Source0 URL fixed. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.6-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.6-1
- Upgrade to 1.6

* Thu Jul 26 2018 Ajay Kaher <akaher@vmware.com> 1.5-2
- Resolved compilation error for aarch64

* Thu Jun 14 2018 Anish Swaminathan <anishs@vmware.com> 1.5-1
- Initial build
