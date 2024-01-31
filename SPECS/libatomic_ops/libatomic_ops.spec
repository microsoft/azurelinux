Summary:        Atomic memory update operations portable implementation
Name:           libatomic_ops
Version:        7.8.2
Release:        1%{?dist}
License:        GPLv2 and MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://github.com/ivmai/libatomic_ops
Source0:        https://github.com/ivmai/libatomic_ops/releases/download/v%{version}/%{name}-%{version}.tar.gz

%description
This package provides semi-portable access to hardware-provided atomic memory update operations on a number of architectures.

%package        devel
Summary:        Development files for the libatomic_ops library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Libraries and header files for the libatomic_ops library.

%prep
%autosetup

%build
%configure \
    --bindir=%{_sbindir} \
    --enable-shared \
    --disable-silent-rules
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -type f -name "*.a" -delete -print
# We will package these files manually using the %%license macro
rm -rf %{buildroot}%{_docdir}/%{name}/{COPYING,LICENSING.txt}

%check
%make_build check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license COPYING doc/LICENSING.txt
%{_libdir}/libatomic_ops.so.1*
%{_libdir}/libatomic_ops_gpl.so.1*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_docdir}/libatomic_ops/README*
%{_libdir}/libatomic_ops.so
%{_libdir}/libatomic_ops_gpl.so
%{_libdir}/pkgconfig/atomic_ops.pc

%changelog
* Wed Jan 31 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 7.8.2-1
- Auto-upgrade to 7.8.2 - Azure Linux 3.0

* Wed Jan 12 2022 Thomas Crain <thcrain@microsoft.com> - 7.6.12-1
- Upgrade to latest upstream version
- Remove static libraries
- Install licenses using just the %%license macro

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.6.6-4
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 7.6.6-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 7.6.6-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> - 7.6.6-1
- Updated to latest version

* Tue Jul 26 2016 Xiaolin Li <xiaolinl@vmware.com> - 7.4.4-1
- Initial build. First version
