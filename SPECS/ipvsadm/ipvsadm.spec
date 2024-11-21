Summary:       Linux Virtual Server administration
Name:          ipvsadm
Version:       1.31
Release:       1%{?dist}
License:       GPLv2
URL:           http://www.kernel.org/
Group:         System Environment/tools
Vendor:        Microsoft Corporation
Distribution:   Azure Linux
Source0:       https://www.kernel.org/pub/linux/utils/kernel/ipvsadm/%{name}-%{version}.tar.xz
BuildRequires: libnl3-devel
BuildRequires: popt-devel
BuildRequires: which 
Requires:      libnl3
Requires:      popt
%description
Ipvsadm is  used  to set up, maintain or inspect the virtual server table in
the Linux kernel.

%prep
%autosetup -p1

%build
make

%install
make install BUILD_ROOT=%{buildroot} MANDIR=%{_mandir}

%files
%defattr(-,root,root)
%license debian/copyright
%{_sysconfdir}/*
/sbin/*
%{_mandir}/*

%changelog
* Thu Jan 20 2022 Rachel Menge <rachelmenge@microsoft.com> - 1.31-1
- Update to 1.31

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.29-6
- Removing the explicit %%clean stage.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.29-5
- Added %%license line automatically

* Thu Apr 30 2020 Nicolas Ontiveros <niontive@microsoft.com> 1.29-4
- Rename libnl to libnl3.

* Thu Apr 23 2020 Jon Slobodzian < joslobo@microsot.com>  1.29-3
- Verified license. Removed sha1. Fixed some formatting.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.29-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Mar 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.29-1
- Upgrading to version 1.29

* Fri Nov 11 2016 Alexey Makhalov <amakhalov@vmware.com> 1.28-1
- Initial build. First version
