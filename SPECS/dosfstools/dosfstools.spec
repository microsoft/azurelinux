Summary:	Dos Filesystem tools
Name:		dosfstools
Version:	4.2
Release:    1%{?dist}
License:	GPLv3+
URL:		https://github.com/dosfstools/dosfstools
Group:		Filesystem Tools
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:	https://github.com/dosfstools/dosfstools/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires: acl
BuildRequires: autoconf
BuildRequires: automake

%description
dosfstools contains utilities for making and checking MS-DOS FAT filesystems.

%prep
%setup -q

%build
./autogen.sh
./configure --prefix=%{_prefix} --enable-compat-symlinks
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} PREFIX="/usr" install

%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/*
%{_mandir}/man8/*
%{_docdir}/dosfstools/*

%changelog
* Fri Jan 21 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 4.2-1
- Upgrade to 4.2.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.1-5
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.1-4
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.1-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*	Thu May 04 2017 Chang Lee <changlee@vmware.com> 4.1-2
-	Add .vfat and .msdos symlinks back.
*	Fri Mar 31 2017 Chang Lee <changlee@vmware.com> 4.1-1
-	Updated package version
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.26-2
-	GA - Bump release of all rpms
*	Wed Jul 1 2014 Sharath George <sharathg@vmware.com> 3.0.26-1
-	Initial build.	First version
