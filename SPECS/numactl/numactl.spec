Summary:        NUMA support for Linux
Name:           numactl
Version:        2.0.16
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/numactl/numactl
Source0:        https://github.com/numactl/numactl/releases/download/v%{version}/%{name}-%{version}.tar.gz

%description
Simple NUMA policy support. It consists of a numactl program to run other programs with a specific NUMA policy.

%package -n libnuma
Summary:        Development libraries and header files for numactl
License:        LGPLv2.1
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-libs = %{version}-%{release}

%description -n libnuma
libnuma shared library ("NUMA API") to set NUMA policy in applications.

%package -n libnuma-devel
Summary:        Development libraries and header files for libnuma
License:        GPLv2
Requires:       libnuma = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description -n libnuma-devel
The package contains libraries and header files for
developing applications that use libnuma.

%prep
%autosetup

%build
autoreconf -fiv
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

# Rename conflicting docs (also packaged in man-pages)
mv %{buildroot}%{_mandir}/man2/move_pages.2 %{buildroot}%{_mandir}/man2/numa-move_pages.2

%check
%make_build check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE.GPL2
%{_bindir}/*
%{_mandir}/man8/*

%files -n libnuma
%defattr(-,root,root)
%license LICENSE.LGPL2.1
%{_libdir}/*.so.*

%files -n libnuma-devel
%defattr(-,root,root)
%license LICENSE.GPL2
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/numa.pc
%{_mandir}/man2/*
%{_mandir}/man3/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.0.16-1
- Auto-upgrade to 2.0.16 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.0.14-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Feb 1 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 2.0.14-1
- Upgrading to 2.0.14

* Thu Sep 30 2021 Thomas Crain <thcrain@microsoft.com> - 2.0.13-6
- Rename conflicting move_pages.2 man pages
- Require libnuma from libnuma-devel
- Fix license packaging
- Lint spec
- License verified

* Fri Sep 10 2021 Thomas Crain <thcrain@microsoft.com> - 2.0.13-5
- Remove libtool archive files from final packaging

* Thu Dec 10 2020 Joe Schmitt <joschmit@microsoft.com> - 2.0.13-4
- Provide numactl-libs and numactl-devel.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.0.13-3
- Added %%license line automatically

*  Mon Jan 20 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 2.0.13-2
-  Initial CBL-Mariner import from Photon (license: Apache2).

*  Mon Nov 18 2019 Alexey Makhalov <amakhalov@vmware.com> 2.0.13-1
-  Initial build. First version
