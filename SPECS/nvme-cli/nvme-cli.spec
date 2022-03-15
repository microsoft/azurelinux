Name:           nvme-cli
Summary:        NVM-Express user space tooling for Linux
Version:        1.16
Release:        1%{?dist}
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
License:        GPLv2
URL:            https://github.com/linux-nvme/nvme-cli
Source0:        https://github.com/linux-nvme/%{name}/archive/%{name}-%{version}.tar.gz
#Source0:       https://github.com/linux-nvme/%{name}/archive/v%{version}.tar.gz

%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
NVM-Express user space tooling for Linux

%prep
%setup -q

%build
make CFLAGS="%{build_cflags} -std=gnu99 -I."

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}

%check
pip3 install nose nose2 pep8 flake8 pylint epydoc
make test

%files
%defattr(-,root,root)
%license LICENSE
%{_sbindir}/nvme
%{_datadir}/*
%{_mandir}/man1/*
%{_sysconfdir}/nvme/*
%{_sysconfdir}/udev/rules.d/*
%{_libdir}/dracut/dracut.conf.d/*
%{_libdir}/systemd/system/*

%changelog
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
