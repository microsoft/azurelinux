Summary:        Library for low-level netlink programming interface to the in-kernel nf_tables subsystem
Name:           libnftnl
Version:        1.2.6
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://netfilter.org/projects/libnftnl/
Source0:        https://netfilter.org/projects/libnftnl/files/%{name}-%{version}.tar.xz
BuildRequires:  jansson-devel
BuildRequires:  libmnl-devel

%description
libnftnl is a userspace library providing a low-level netlink programming interface (API) to the in-kernel nf_tables subsystem.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
Development files for %{name}

%prep
%autosetup -p1

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
find %{buildroot} -type f -name "*.la" -delete -print

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}

%changelog
* Fri Dec 15 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 1.2.6-1
- Update to v1.2.6

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.2.1-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Jan 11 2022 Henry Li <lihl@microsoft.com> - 1.2.1-1
- Upgrade to version 1.2.1
- Verified License

* Wed Mar 03 2021 Henry Li <lihl@microsoft.com> - 1.1.9-1
- Update to version 1.1.9
- Remove sha1 macro

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.1.1-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.1.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Ankit Jain <ankitja@vmware.com> 1.1.1-1
- Initial version
