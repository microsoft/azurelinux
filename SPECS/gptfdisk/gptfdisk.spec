Summary:	gptfdisk-1.0.4
Name:		gptfdisk
Version:	1.0.4
Release:        4%{?dist}
License:	GPLv2+
URL:		http://sourceforge.net/projects/gptfdisk/
Group:		System Environment/Filesystem and Disk management
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	http://downloads.sourceforge.net/project/gptfdisk/%{name}/%{version}/%{name}-%{version}.tar.gz

Patch0:	    gptfdisk-1.0.4-convenience-1.patch
Requires: 	popt >= 1.16
BuildRequires:	popt-devel
BuildRequires:	ncurses-devel
Requires:	ncurses
Requires:	libstdc++

%description
The gptfdisk package is a set of programs for creation and maintenance of GUID Partition
Table (GPT) disk drives. A GPT partitioned disk is required for drives greater than 2 TB
and is a modern replacement for legacy PC-BIOS partitioned disk drives that use a
Master Boot Record (MBR). The main program, gdisk, has an inteface similar to the
classic fdisk program.

%prep
%setup -q
%patch0 -p1

%build
make %{?_smp_mflags} POPT=1

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install POPT=1
%{_fixperms} %{buildroot}/*

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
/sbin/*
%{_mandir}/man8/*

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-4
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0.4-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0.4-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Sep 11 2018 Anish Swaminathan <anishs@vmware.com> 1.0.4-1
-   Update version to 1.0.4
*   Mon Jun 05 2017 Bo Gan <ganb@vmware.com> 1.0.1-4
-   Fix dependency
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.0.1-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-2
-   GA - Bump release of all rpms
*   Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.1-1
-   Updated Version.
*   Thu Oct 30 2014 Divya Thaluru <dthaluru@vmware.com> 0.8.10-1
-   Initial build.	First version
