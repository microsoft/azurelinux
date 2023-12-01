Summary:        gptfdisk
Name:           gptfdisk
Version:        1.0.8
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Filesystem and Disk management
URL:            https://sourceforge.net/projects/gptfdisk/
Source0:        https://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.gz
Patch0:         fix-format-security.patch
BuildRequires:  gcc
BuildRequires:  libuuid-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  popt-devel
Provides:       gdisk = %{version}-%{release}

%description
The gptfdisk package is a set of programs for creation and maintenance of GUID Partition
Table (GPT) disk drives. A GPT partitioned disk is required for drives greater than 2 TB
and is a modern replacement for legacy PC-BIOS partitioned disk drives that use a
Master Boot Record (MBR). The main program, gdisk, has an inteface similar to the
classic fdisk program.

%prep
%autosetup -p1

%build
export CXXFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64"
%make_build

%install
install -dm 755 %{buildroot}%{_sbindir} %{buildroot}%{_mandir}/man8
install -m755 gdisk cgdisk sgdisk fixparts %{buildroot}%{_sbindir}
install -m644 *.8 %{buildroot}%{_mandir}/man8

%check
%make_build test

%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Fri Jun 17 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.0.8-2
- Add upstream patch to fix -Werror=format-security errors after ncurses 6.3 upgrade

* Wed Feb 16 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.0.8-1
- Upgrade to latest upstream version
- Translate Makefile patch to %%install section instructions for easier maintenance
- Add provides for gdisk package for Fedora compatibility
- Add %%check section
- Lint spec
- License verified

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-4
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0.4-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.0.4-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Sep 11 2018 Anish Swaminathan <anishs@vmware.com> - 1.0.4-1
- Update version to 1.0.4

* Mon Jun 05 2017 Bo Gan <ganb@vmware.com> - 1.0.1-4
- Fix dependency

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> - 1.0.1-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.1-2
- GA - Bump release of all rpms

* Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> - 1.0.1-1
- Updated Version.

* Thu Oct 30 2014 Divya Thaluru <dthaluru@vmware.com> - 0.8.10-1
- Initial build.	First version
