Summary:	The New GNU Portable Threads Library.
Name:		npth
Version:	1.6
Release:        3%{?dist}
License:	GPLv2+ and LGPLv3+
URL:		https://github.com/gpg/npth
Group:		System Environment/Libraries.
Source0:        https://github.com/gpg/%{name}/archive/%{name}-%{version}.tar.gz
%define sha1 npth=3f3c68d439c2f8a798423de38b9a6eb32c0c417e
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description
This is a library to provide the GNU Pth API and thus a non-preemptive threads implementation.
In contrast to GNU Pth, it is based on the system's standard threads implementation.
This allows the use of libraries which are not compatible to GNU Pth.
Experience with a Windows Pth emulation showed that this is a solid way to provide
a co-routine based framework.

%package devel
Summary:       GNU npth development header and libraries.
Group:         Development/Libraries.
Requires:      npth = %{version}

%description devel
Development package for npth.

%prep
%setup -qn npth-%{name}-%{version}

%build
./autogen.sh
./configure --disable-static \
           --prefix=%{_prefix}
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING.LIB
%{_bindir}/*
%{_libdir}/*.so*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/aclocal/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.6-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.6-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*       Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.6-1
-       Upgrade to 1.6.
*       Tue Apr 11 2017 Danut Moraru <dmoraru@vmware.com> 1.3-1
-       Initial Build.
