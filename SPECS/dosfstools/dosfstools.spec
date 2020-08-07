Summary:	Dos Filesystem tools
Name:		dosfstools
Version:	4.1
Release:        4%{?dist}
License:	GPLv3+
URL:		http://github.com/dosfstools/dosfstools
Group:		Filesystem Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	http://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha1 dosfstools=db39f667c3cb51bdf321f07f9cf17c726ca50323
%description
dosfstools contains utilities for making and checking MS-DOS FAT filesystems.
%prep
%setup -q
%build
./configure --prefix=%{_prefix} --enable-compat-symlinks
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} PREFIX="/usr" install
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/*
%{_mandir}/man8/*
%{_docdir}/dosfstools/*
%changelog
* Sat May 09 00:21:25 PST 2020 Nick Samson <nisamson@microsoft.com> - 4.1-4
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
