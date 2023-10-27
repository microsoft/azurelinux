Summary:    User-space infrastructure for connection tracking timeout
Name:       libnetfilter_cttimeout
Version:    1.0.1
Release:        1%{?dist}
License:    GPLv2+
URL:        http://www.netfilter.org/projects/libnetfilter_cttimeout/index.html
Group:      System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:    http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2

BuildRequires:  libmnl-devel
BuildRequires:  kernel-headers

%description
libnetfilter_cttimeout is the userspace library that provides the programming interface to the fine-grain connection tracking timeout infrastructure. With this library, you can create, update and delete timeout policies that can be attached to traffic flows.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libmnl-devel
Requires:       kernel-headers

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
find %{buildroot} -type f -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%doc COPYING README
%{_libdir}/*.so.*

%files devel
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libnetfilter_cttimeout
%{_includedir}/libnetfilter_cttimeout/*.h
%{_libdir}/*.so

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.1-1
- Auto-upgrade to 1.0.1 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.0.0-6
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Feb 08 2022 Thomas Crain <thcrain@microsoft.com> - 1.0.0-5
- Remove unused `%%define sha1` lines
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0.0-4
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.0.0-3
- Renaming linux-api-headers to kernel-headers

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.0.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> - 1.0.0-1
- Initial packaging
