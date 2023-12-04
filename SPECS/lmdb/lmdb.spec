Summary:        Lightning memory-mapped database
Name:           lmdb
Version:        0.9.31
Release:        1%{?dist}
License:        OpenLDAP
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Libraries
URL:            https://symas.com/lmdb
Source0:        https://github.com/LMDB/lmdb/archive/LMDB_%{version}.tar.gz
Source1:        %{name}.pc
Requires:       lmdb-libs = %{version}-%{release}

%description
An ultra-fast, ultra-compact, crash-proof key-value
embedded data store.

%package devel
Summary:        Development files for lmdb
Group:          Development/Libraries
Requires:       lmdb = %{version}-%{release}

%description devel
Development files for lmdb

%package libs
Summary:        Shared libraries for lmdb
Group:          Development/Libraries

%description libs
Shared libraries for lmdb

%prep
%setup -q -n lmdb-LMDB_%{version}

%build
cd libraries/liblmdb
make %{?_smp_mflags}

%install
cd libraries/liblmdb
make prefix=%{_prefix} DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_docdir}/%{name}
mkdir -p %{buildroot}%{_defaultlicensedir}/%{name}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -m0644 COPYRIGHT %{buildroot}%{_docdir}/%{name}
install -m0644 LICENSE %{buildroot}%{_defaultlicensedir}/%{name}
install -m0755 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig

%post

    /sbin/ldconfig

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

%files
%license libraries/liblmdb/LICENSE
%{_mandir}/*
%{_bindir}/*

%files devel
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/%{name}.pc

%files libs
%{_docdir}/%{name}/COPYRIGHT
%{_defaultlicensedir}/%{name}/LICENSE
%{_libdir}/*.so

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.9.31-1
- Auto-upgrade to 0.9.31 - Azure Linux 3.0 - package upgrades

* Mon Feb 07 2022 Henry Li <lihl@microsoft.com> - 0.9.29-1
- Upgrade to version 0.9.29

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.23-3
- Removing the explicit %%clean stage.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.9.23-2
- Added %%license line automatically

*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 0.9.23-1
-   Update to 0.9.23. License verified.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.9.22-3
-   Initial CBL-Mariner import from Photon (license: Apache2).

*  Tue Jan 22 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.22-2
-  add libs package for library. tools and man in main package.

*  Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.9.22-1
-  Update to version 0.9.22

*  Wed Dec 13 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.21-1
-  Initial
