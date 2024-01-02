Summary:        Text file viewer
Name:           less
Version:        643
Release:        1%{?dist}
License:        GPLv3+ OR BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/File
URL:            https://www.greenwoodsoftware.com/less
Source0:        https://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
BuildRequires:  ncurses-devel
Requires:       ncurses

%description
The Less package contains a text file viewer

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%files
%defattr(-,root,root)
%license LICENSE COPYING
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 643-1
- Auto-upgrade to 643 - Azure Linux 3.0 - package upgrades

* Fri Feb 17 2023 Suresh Thelkar <sthelkar@microsoft.com> - 590-2
- Patch CVE-2022-46663

* Wed Dec 08 2021 Mateusz Malisz <mamalisz@microsoft.com> - 590-1
- Update to version 590
- License verified.
- Fix changelog versions and formatting

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 530-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 530-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 530-1
- Upgrade version to 530

* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 487-1
- Upgrade version to 487

* Tue Oct 18 2016 Anish Swaminathan <anishs@vmware.com>  481-1
- Upgrade version to 481

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 458-2
- GA - Bump release of all rpms

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 458-1
- Initial build. First version
