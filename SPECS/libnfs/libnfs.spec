Summary:        Client library for accessing NFS shares over a network
Name:           libnfs
Version:        4.0.0
Release:        6%{?dist}
# The library is licensed as LGPLv2+, the protocol definition is BSD
License:        LGPLv2+ AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/sahlberg/libnfs
Source0:        %{url}/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
The libnfs package contains a library of functions for accessing NFSv2
and NFSv3 servers from user space. It provides a low-level, asynchronous
RPC library for accessing NFS protocols, an asynchronous library with
POSIX-like VFS functions, and a synchronous library with POSIX-like VFS
functions.

%package devel
Summary:        Development files for libnfs
# The library is licensed as LGPLv2+, the protocol definition is BSD
# and the example source code is GPLv3+.
License:        LGPLv2+ AND BSD AND GPLv3+
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The libnfs-devel package contains libraries and header files for
developing applications that use libnfs.

%package utils
Summary:        Utilities for accessing NFS servers
License:        GPLv3+
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
The libnfs-utils package contains simple client programs for accessing
NFS servers using libnfs.

%prep
%setup -q -n %{name}-%{name}-%{version}
autoreconf -vif

%build
%configure --disable-static --disable-examples --disable-werror
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build V=1

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%ldconfig_scriptlets

%files
%{_libdir}/libnfs.so.13*
%doc README
%license COPYING
%license LICENCE-*.txt

%files devel
%{_libdir}/libnfs.so
%{_includedir}/nfsc/
%{_libdir}/pkgconfig/libnfs.pc
%doc examples/*.c

%files utils
%{_bindir}/nfs-*
%{_mandir}/man1/nfs-*.1*

%changelog
* Wed Sep 22 2021 Olivia Crain <oliviacrain@microsoft.com> - 4.0.0-6
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.0-1
- Update to 4.0.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Mar 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.11.0-1
- Update to 1.11.0 (version 2.0.0 is also available)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.8-6
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 06 2015 Ross Lagerwall <rosslagerwall@gmail.com> 1.9.8-1
- Bump to 1.9.8.
- Include examples and licence terms.

* Sun Mar 29 2015 Ross Lagerwall <rosslagerwall@gmail.com> 1.9.7-2
- Update packaging after review.

* Sun Mar 01 2015 Ross Lagerwall <rosslagerwall@gmail.com> 1.9.7-1
- Initial packaging
