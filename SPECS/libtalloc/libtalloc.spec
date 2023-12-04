%define LICENSE_PATH LICENSE.PTR
Summary:        Talloc is a hierarchical, reference counted memory pool system
Name:           libtalloc
Version:        2.4.1
Release:        1%{?dist}
# Some files are GPL, others LGPL. Info in source.
License:        GPLv3+ AND LGPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://talloc.samba.org
Source0:        https://www.samba.org/ftp/talloc/talloc-%{version}.tar.gz
Source1:        %{LICENSE_PATH}
BuildRequires:  docbook-style-xsl
BuildRequires:  libxslt
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  which

%description
Libtalloc alloc is a hierarchical, reference counted memory pool system with destructors. It is the core memory allocator used in Samba.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The libtalloc-devel package contains libraries and header files for libtalloc

%package -n python-talloc
Summary:        Python bindings for the Talloc library
Group:          Development/Libraries
Requires:       libtalloc = %{version}-%{release}
Provides:       python3-talloc = %{version}-%{release}

%description -n python-talloc
Python 3 libraries for creating bindings using talloc

%package -n python-talloc-devel
Summary:        Development libraries for python-talloc
Group:          Development/Libraries
Requires:       python-talloc = %{version}-%{release}
Provides:       python3-talloc-devel = %{version}-%{release}

%description -n python-talloc-devel
Development libraries for python-talloc

%prep
%setup -q -n talloc-%{version}
cp %{SOURCE1} ./

%build
%configure --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules
make %{?_smp_mflags} V=1

%install
%make_install
rm -f %{buildroot}%{_datadir}/swig/*/talloc.i

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license %{LICENSE_PATH}
%{_libdir}/libtalloc.so.*

%files devel
%{_includedir}/talloc.h
%{_libdir}/libtalloc.so
%{_libdir}/pkgconfig/talloc.pc
%{_mandir}/man3/talloc*.3.gz

%files -n python-talloc
%{_libdir}/libpytalloc-util.cpython*.so.*
%{python3_sitelib}/*

%files -n python-talloc-devel
%{_includedir}/pytalloc.h
%{_libdir}/pkgconfig/pytalloc-util.cpython-*.pc
%{_libdir}/libpytalloc-util.cpython*.so

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.1-1
- Auto-upgrade to 2.4.1 - Azure Linux 3.0 - package upgrades

* Tue Jan 25 2022 Henry Li <lihl@microsoft.com> - 2.3.3-1
- Upgrade to version 2.3.3

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 2.3.1-2
- Use %%{python3_sitelib} macro to enable building with Python 3.9

* Mon Jan 11 2021 Joe Schmitt <joschmit@microsoft.com> - 2.3.1-1
- Upgrade to v2.3.1.
- Provide python3-talloc and python3-talloc-devel.

* Thu Jun 06 2020 Joe Schmitt <joschmit@microsoft.com> - 2.1.16-4
- Added %%license macro.

* Tue May 05 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.1.16-3
- Renaming docbook-xsl to docbook-style-xsl

* Thu Apr 23 2020 Nick Samson <nisamson@microsoft.com> - 2.1.16-2
- Updated Source0, License. License verified.

* Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.1.16-1
- Update to 2.1.16. Move to python3. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.1.14-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> - 2.1.14-2
- Added BuildRequires python2-devel

* Tue Sep 11 2018 Bo Gan <ganb@vmware.com> - 2.1.14-1
- Update to 2.1.14

* Thu Aug 03 2017 Chang Lee <changlee@vmware.com> - 2.1.9-2
- Copy libraries and add a patch for path regarding %check

* Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> - 2.1.9-1
- Initial packaging
