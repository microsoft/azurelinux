Summary:        A simplified, portable interface to several low-level networking routines
Name:           libdnet
Version:        1.17.0
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/System
URL:            https://github.com/ofalk/%{name}
Source0:        https://github.com/ofalk/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz
	
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: check-devel
BuildRequires: python3-Cython
BuildRequires: python3-setuptools

%description
libdnet provides a simplified, portable interface to several
low-level networking routines, including network address
manipulation, kernel arp(4) cache and route(4) table lookup and
manipulation, network firewalling (IP filter, ipfw, ipchains,
pf, ...), network interface lookup and manipulation, raw IP
packet and Ethernet frame, and data transmission.

%package        devel
Summary:        Header files for libdnet library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
%{summary}.

%package progs
Summary:       Sample applications to use with libdnet
Requires:      %{name}%{?_isa} = %{version}-%{release}
 
%description progs
%{summary}.

%package -n python%{python3_pkgversion}-libdnet
%{?python_provide:%python_provide python%{python3_pkgversion}-libdnet}
# Remove before F30
Provides:      %{name}-python = %{version}-%{release}
Provides:      %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes:     %{name}-python < %{version}-%{release}
Summary:       Python bindings for libdnet
Requires:      %{name}%{?_isa} = %{version}-%{release}
BuildRequires: python%{python3_pkgversion}-devel

%description -n python%{python3_pkgversion}-libdnet
%{summary}.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
autoreconf -i
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build
	
%install
%make_install
find %{buildroot}/usr/lib/ -name '*.la' -delete

pushd python
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
 
%ldconfig_scriptlets

%files
%license LICENSE
%doc THANKS TODO
%{_libdir}/*.so.*
 
%files devel
%{_bindir}/*
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*.3*
 
%files progs
%{_sbindir}/*
%{_mandir}/man8/*.8*
 
%files -n python%{python3_pkgversion}-libdnet
%{python3_sitearch}/*

%changelog
* Mon Feb 05 2024 Dallas Delaney <dadelan@microsoft.com> - 1.17.0-1
- Upgrade to 1.17.0
- Add subpackages libdnet-progs, python3-libdnet

* Wed Mar 16 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 1.14-1
- Upgrading to v1.14

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.12-2
- Added %%license line automatically

*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 1.12-1
-   Update to 1.12. URL Fixed. Source0 URL Fixed. License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.11-7
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.11-6
-   Aarch64 support

*   Thu Aug 03 2017 Kumar Kaushik <kaushikk@vmware.com> 1.11-5
-   Applying patch for makecheck bug #1633615.

*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.11-4
-   Move man files to /usr/share, add devel package

*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 1.11-3
-   Modified %check

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11-2
-   GA - Bump release of all rpms

*   Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 1.11-1
    Initial version
