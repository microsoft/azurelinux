Summary:        Netfilter conntrack userspace library
Name:           libnetfilter_conntrack
Version:        1.0.9
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://www.netfilter.org/projects/libnetfilter_conntrack/index.html
Source0:        http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
BuildRequires:  kernel-headers
BuildRequires:  libmnl-devel
BuildRequires:  libnfnetlink-devel

%description
libnetfilter_conntrack is a userspace library providing a programming interface (API) to the in-kernel connection tracking state table. The library libnetfilter_conntrack has been previously known as libnfnetlink_conntrack and libctnetlink.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       kernel-headers
Requires:       libnfnetlink-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%doc COPYING README
%{_libdir}/*.so.*

%files devel
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Mon Jan 29 2024 Sharath Srikanth Chellappa <sharathsr@microsoft.com> - 1.0.9-1
- Bump version to 1.0.9

* Tue Jan 11 2022 Henry Li <lihl@microsoft.com> - 1.0.8-1
- Upgrade to version 1.0.8
- Verified License
- Remove sha1 macro

* Fri Sep 10 2021 Thomas Crain <thcrain@microsoft.com> - 1.0.7-5
- Remove libtool archive files from final packaging

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0.7-4
- Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.0.7-3
-   Renaming linux-api-headers to kernel-headers

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0.7-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 1.0.7-1
-   Update to 1.0.7

*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 1.0.6-1
-   Initial packaging
