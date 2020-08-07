Summary:        Text file viewer
Name:           less
Version:        530
Release:        2%{?dist}
License:        GPLv3+
URL:            http://www.greenwoodsoftware.com/less
Group:          Applications/File
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://www.greenwoodsoftware.com/less/%{name}-%{version}.tar.gz
%define sha1 %{name}=d8ba1f43e88b706ef701f978cd3262b5b44dffd6
BuildRequires:  ncurses-devel
Requires:       ncurses

%description
The Less package contains a text file viewer

%prep
%setup -q

%build
./configure \
        --prefix=%{_prefix} \
        --sysconfdir=%{_sysconfdir}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Sat May 09 00:20:49 PST 2020 Nick Samson <nisamson@microsoft.com> - 530-2
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 530-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 530-1
-   Upgrade version to 530
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 487-1
-   Upgrade version to 487
*   Tue Oct 18 2016 Anish Swaminathan <anishs@vmware.com>  481-1
-   Upgrade version to 481
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 458-2
-   GA - Bump release of all rpms
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 458-1
-   Initial build. First version
