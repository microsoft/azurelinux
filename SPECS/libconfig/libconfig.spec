Summary:        C/C++ configuration file library
Name:           libconfig
Version:        1.7.2
Release:        2%{?dist}
License:        LGPLv2+
URL:            https://hyperrealm.github.io/libconfig/
#Source0:       https://github.com/hyperrealm/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  autoconf
BuildRequires:  texinfo

%description
Libconfig is a simple library for processing structured configuration files, like this one: test.cfg. This file format is more compact and more readable than XML. And unlike XML, it is type-aware, so it is not necessary to do string parsing in application code.

%prep
%setup -q

%build
autoreconf
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_infodir}/dir

%check
cd ./tests
./libconfig_tests # This HAS to be run in the tests directory due to use of relative paths.
cd ..

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc AUTHORS ChangeLog COPYING.LIB README
%{_libdir}/libconfig*.so.*
%{_includedir}/libconfig*
%{_libdir}/libconfig*.so
%{_libdir}/pkgconfig/libconfig*.pc
%{_infodir}/libconfig.info*
%{_libdir}/cmake/libconfig*/*.cmake

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.7.2-2
- Added %%license line automatically

*   Mon Apr 20 2020 Nick Samson <nisamson@microsoft.com> 1.7.2-1
-   Updated for bug-fixes, changed Source0 to current official sources. URL updated. License verified.
-   Fixes to build script to compile latest version.
-   Added BuildRequires.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.5-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5-2
-   GA - Bump release of all rpms
*   Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 0.7.2-1
-   Initial build.  First version
