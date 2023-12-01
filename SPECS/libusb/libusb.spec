Summary:        A library which allows userspace access to USB devices
Name:           libusb
Version:        1.0.24
Release:        2%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://libusb.info/
Source:         https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.bz2
BuildRequires:  systemd-devel
Requires:       systemd
# libusbx is a fork that was merged back into libusb.
# Some distros still use the name of the fork
Provides:       %{name}x = %{version}-%{release}
Provides:       %{name}1 = %{version}-%{release}

%description
This package provides a way for applications to access USB devices.

%package        devel
Summary:        Development files for libusb
Group:          Development/Libraries
Requires:       %{name} = %{version}
Provides:       %{name}x-devel = %{version}-%{release}
Provides:       %{name}1-devel = %{version}-%{release}

%description    devel
This package contains the header files, libraries and documentation needed to
develop applications that use libusb.

%prep
%autosetup

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
pushd tests
%make_build -k check
./stress
popd

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libusb*.so.*

%files devel
%{_includedir}/*
%{_libdir}/libusb*.so
%{_libdir}/pkgconfig/*

%changelog
* Fri Sep 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.0.24-2
- Remove libtool archive files from final packaging

* Tue Jun 29 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.0.24-1
- Upgrade to latest upstream version
- Provide libusbx, libusb1 names to match other distros
- Utilize make, ldconfig macros
- Update URLs
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0.22-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.0.22-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> - 1.0.22-1
- Update to version 1.0.22

* Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> - 1.0.21-1
- Upgrading version to 1.0.21

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com> - 1.0.20-4
- Change systemd dependency

* Tue Jul 12 2016 Xiaolin Li <xiaolinl@vmware.com> - 1.0.20-3
- Build libusb single threaded.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.0.20-2
- GA - Bump release of all rpms

* Thu May 05 2016 Nick Shi <nshi@vmware.com> - 1.0.20-1
- Initial version
