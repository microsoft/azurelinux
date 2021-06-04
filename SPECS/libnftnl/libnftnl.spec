Summary:        Library for low-level netlink programming interface to the in-kernel nf_tables subsystem
Name:           libnftnl
Version:        1.1.1
Release:        3%{?dist}
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
License:        GPLv2+
URL:            http://netfilter.org/projects/libnftnl/
Source0:        https://netfilter.org/projects/libnftnl/files/%{name}-%{version}.tar.bz2
%define sha1 %{name}-%{version}=d2be642a54e0f105cb5564471ae4aaaed8b97ca6
Distribution:   Mariner
BuildRequires:  libmnl-devel
BuildRequires:  jansson-devel

%description
libnftnl is a userspace library providing a low-level netlink programming interface (API) to the in-kernel nf_tables subsystem.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description    devel
Development files for %{name}

%prep
%setup -q

%build
./configure \
         --prefix=%{_prefix} \
         --disable-static \
         --disable-silent-rules \
         --with-json-parsing
make %{?_smp_mflags}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%doc COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.1.1-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.1.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
* Mon Sep 10 2018 Ankit Jain <ankitja@vmware.com> 1.1.1-1
- Initial version
