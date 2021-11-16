Summary:        Google's C++ gtest framework
Name:           gtest
Version:        1.11.0
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/google/googletest
Source0:        https://github.com/google/googletest/archive/release-%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Google's C++ test framework that combines the GoogleTest and GoogleMock projects. This package provides gtest shared libraries.

%package devel
Summary:        libgtest headers
Group:          Development/Tools

%description devel
This contains libgtest header files.

%package -n gmock
Summary:        Google's C++ gmock framework
Group:          Development/Tools

%description -n gmock
Google's C++ test framework that combines the GoogleTest and GoogleMock projects. This package provides gmock shared libraries.

%package -n gmock-devel
Summary:        libgmock headers
Group:          Development/Tools

%description -n gmock-devel
This contains libgmock header files.

%prep
%setup -q -n googletest-release-%{version}

%build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DBUILD_SHARED_LIBS=OFF .
make
cmake -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DBUILD_SHARED_LIBS=ON .
make

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_prefix}/src/gtest/src/
install -vdm 755 %{buildroot}%{_prefix}/src/gmock/src/
cp googletest/src/* %{buildroot}%{_prefix}/src/gtest/src/
cp googlemock/src/* %{buildroot}%{_prefix}/src/gmock/src/
find %{buildroot} -type f -name "*.la" -delete -print

%files
%defattr(-,root,root)
%license LICENSE
%{_lib64dir}/libgtest.so.1.*
%{_lib64dir}/libgtest_main.so.1.*

%files -n gmock
%{_lib64dir}/libgmock.so.1.*
%{_lib64dir}/libgmock_main.so.1.*

%files devel
%defattr(-,root,root)
%{_includedir}/gtest/*
%{_lib64dir}/cmake/GTest/*.cmake
%{_lib64dir}/libgtest.so
%{_lib64dir}/libgtest_main.so
%{_lib64dir}/pkgconfig/*.pc
%{_prefix}/src/gtest/

%files -n gmock-devel
%{_includedir}/gmock/*
%{_lib64dir}/libgmock.so
%{_lib64dir}/libgmock_main.so
%{_prefix}/src/gmock/

%changelog
* Tue Nov 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.11.0-1
- Update to version 1.11.0.
- Removing "*-static" subpackages.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.8.1-5
- Added %%license line automatically

* Thu Apr 23 2020 Andrew Phelps <anphel@microsoft.com> - 1.8.1-4
- Update source0.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.8.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 23 2018 Sharath George <anishs@vmware.com> - 1.8.1-2
- Add gmock subpackage

* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> - 1.8.1-1
- Update version to 1.8.1

* Thu May 04 2017 Anish Swaminathan <anishs@vmware.com> - 1.8.0-2
- Add gtest sources in devel package

* Mon Apr 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 1.8.0-1
- Initial version of libgtest package for Photon.
