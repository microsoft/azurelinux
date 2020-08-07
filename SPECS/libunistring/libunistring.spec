Summary:	GNU Unicode string library
Name:		libunistring
Version:	0.9.10
Release:        3%{?dist}
License:	LGPLv3+
Url:		http://www.gnu.org/software/libunistring/
Source0:	http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.xz
%define sha1 libunistring=16dc423d3ebd23f365b0ffe7d584428b427f4bde
Group:		System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
%description
libunistring is a library that provides functions for manipulating Unicode strings and for manipulating C strings according to the Unicode standard.

%package devel
Summary:	Development libraries and header files for libunistring
Requires:	libunistring

%description devel
The package contains libraries and header files for
developing applications that use libunistring.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_infodir}/*

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*
%{_docdir}/%{name}/*
%{_libdir}/*.a
%{_libdir}/*.la
%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/unistring/*.h
%{_libdir}/*.so
%changelog
* Sat May 09 00:21:20 PST 2020 Nick Samson <nisamson@microsoft.com> - 0.9.10-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.9.10-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
* Mon Sep 10 2018 Alexey Makhalov <amakhalov@vmware.com> 0.9.10-1
- Version update to fix compilation issue againts glibc-2.28
* Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 0.9.7-1
- Updating Version to 0.9.7
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.6-2
- GA - Bump release of all rpms
* Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 0.9.6-1
- Updated to version 0.9.6
* Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 0.9.5-1
- Initial build. First version
