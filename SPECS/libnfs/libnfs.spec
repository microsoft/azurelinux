# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		libnfs
Version:	6.0.2
Release:	6%{?dist}
Summary:	Client library for accessing NFS shares over a network
# The library is licensed as LGPL-2.1-or-later
# The protocol definition is BSD-2-Clause
# The utility and examples are GPL-3.0-or-later
License:	LGPL-2.1-or-later AND BSD-2-Clause AND GPL-3.0-or-later
URL:		https://github.com/sahlberg/libnfs
Source0:	%{url}/archive/%{name}-%{version}/%{name}-%{version}.tar.gz

# https://github.com/sahlberg/libnfs/pull/518
Patch0:         libnfs-6.0.2-fix_gnutls_undefined_symbols.patch
# https://github.com/sahlberg/libnfs/commit/2cdfedaba379cbb512d3c203a1b9eae795f4fb23
Patch1:         libnfs-6.0.2-fix_missing_include.patch

BuildRequires:	automake
BuildRequires:	gcc
BuildRequires:	gnutls-devel
BuildRequires:	krb5-devel
BuildRequires:	libtool
BuildRequires:	make

%description
The libnfs package contains a library of functions for accessing NFSv2
and NFSv3 servers from user space. It provides a low-level, asynchronous
RPC library for accessing NFS protocols, an asynchronous library with
POSIX-like VFS functions, and a synchronous library with POSIX-like VFS
functions.


%package devel
Summary:	Development files for libnfs
# The library is licensed as LGPLv2+, the protocol definition is BSD
# and the example source code is GPLv3+.
License:	LGPL-2.1-or-later AND BSD-2-Clause AND GPL-3.0-or-later

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The libnfs-devel package contains libraries and header files for
developing applications that use libnfs.


%package utils
Summary:	Utilities for accessing NFS servers
License:	GPL-3.0-or-later

Requires:	%{name}%{?_isa} = %{version}-%{release}

%description utils
The libnfs-utils package contains simple client programs for accessing
NFS servers using libnfs.


%prep
%setup -q -n %{name}-%{name}-%{version}
%patch -P0 -p1
%patch -P1 -p1
autoreconf -vif

%build
%configure --disable-static --disable-examples --disable-werror \
           --enable-pthread
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build V=1

%install
%make_install

rm -f %{buildroot}%{_libdir}/*.la


%ldconfig_scriptlets

%files
%{_libdir}/libnfs.so.16*
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
* Mon Jul 28 2025 Xavier Bachelot <xavier@bachelot.org> - 6.0.2-6
- Add upstream patch to fix missing include

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri May 23 2025 Xavier Bachelot <xavier@bachelot.org> - 6.0.2-4
- Add upstream patch to fix undefined symbols (RHBZ#2368146)

* Tue Apr 08 2025 Richard W.M. Jones <rjones@redhat.com> - 6.0.2-3
- Enable the multithreading API
  (https://github.com/sahlberg/libnfs/blob/master/README.multithreading)

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 16 2024 Xavier Bachelot <xavier@bachelot.org> - 6.0.2-1
- Update to 6.0.2 (RHBZ#2331668)

* Fri Dec 13 2024 Xavier Bachelot <xavier@bachelot.org> - 6.0.1-1
- Update to 6.0.1 (RHBZ#2331668)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 11 2024 Xavier Bachelot <xavier@bachelot.org> - 5.0.3-1
- Update to 5.0.3 (RHBZ#2263724)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 01 2023 Xavier Bachelot <xavier@bachelot.org> - 5.0.2-2
- Convert License: to SPDX

* Mon Jan 30 2023 Xavier Bachelot <xavier@bachelot.org> - 5.0.2-1
- Update to 5.0.2 (RHBZ#2047688)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

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
