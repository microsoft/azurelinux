Name:          nvme-cli
Summary:       NVM-Express user space tooling for Linux
Version:       1.8.1
Release:       3%{?dist}
Group:         Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
License:       GPLv2
URL:           https://github.com/linux-nvme/nvme-cli
Source0:       https://github.com/linux-nvme/%{name}/archive/%{name}-%{version}.tar.gz
#Source0:       https://github.com/linux-nvme/%{name}/archive/v%{version}.tar.gz

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
%{_datadir}/*
%{_mandir}/man1/*

%changelog
* Sat May 09 00:20:54 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.8.1-3
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
