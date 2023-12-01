%define sover_major 11

Summary:        C/C++ configuration file library
Name:           libconfig
Version:        1.7.3
Release:        2%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://hyperrealm.github.io/libconfig/
Source0:        https://github.com/hyperrealm/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  texinfo

%description
Libconfig is a simple library for processing structured configuration files. This file format is more compact and more readable than XML. And unlike XML, it is type-aware, so it is not necessary to do string parsing in application code.

%package        devel
Summary:        Development libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Development libraries and headers for %{name}

%prep
%autosetup

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
rm -rf %{buildroot}%{_infodir}/dir

%check
cd ./tests
./libconfig_tests # This HAS to be run in the tests directory due to use of relative paths.
cd ..

%ldconfig_scriptlets

%files
%license COPYING.LIB
%doc AUTHORS ChangeLog README
%{_libdir}/libconfig*.so.%{sover_major}
%{_libdir}/libconfig*.so.%{sover_major}.*

%files devel
%{_includedir}/libconfig*
%{_infodir}/libconfig.info*
%{_libdir}/cmake/libconfig*/*.cmake
%{_libdir}/libconfig*.so
%{_libdir}/pkgconfig/libconfig*.pc

%changelog
* Tue Jul 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7.3-2
- Removing minor version number from the %%files section.

* Tue Jun 29 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.7.3-1
- Upgrade to latest release and update license location
- Use release version of the source tarball
- Add a devel subpackage
- Lint spec, modernize with macros

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.7.2-2
- Added %%license line automatically

* Mon Apr 20 2020 Nick Samson <nisamson@microsoft.com> - 1.7.2-1
- Updated for bug-fixes, changed Source0 to current official sources. URL updated. License verified.
- Fixes to build script to compile latest version.
- Added BuildRequires.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.5-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.5-2
- GA - Bump release of all rpms

* Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> - 0.7.2-1
- Initial build.  First version
