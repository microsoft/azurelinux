Summary:        sdbus-cpp
Name:           sdbus-cpp
Version:        1.3.0
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          SystemUtilities
URL:            https://github.com/Kistler-Group/sdbus-cpp
Source0:        https://github.com/Kistler-Group/sdbus-cpp/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  systemd-devel

%description
This is a high level C++ D-Bus library for Linux designed to provide easy-to-use yet powerful API in modern C++.

%package        devel
Summary:        Development libraries and headers for sdbus-cpp
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The sdbus-cpp-devel package contains libraries, header files and documentation
for developing applications that use sdbus-cpp.

%prep
%autosetup -p1

%build
mkdir build
cd build
cmake \
   -D CMAKE_INSTALL_LIBDIR=%{buildroot}%{_libdir} \
   -D CMAKE_INSTALL_BINDIR=%{buildroot}%{_bindir} \
   -D CMAKE_INSTALL_SBINDIR=%{buildroot}%{_sbindir} \
   -D CMAKE_INSTALL_MANDIR=%{buildroot}%{_mandir} \
   -D CMAKE_INSTALL_DOCDIR=%{buildroot}%{_docdir} \
   -D CMAKE_INSTALL_INCLUDEDIR=%{buildroot}%{_includedir} \
   -DCMAKE_BUILD_TYPE=Release        \
   ..
cmake --build .

%install
cd build
cmake --build . --target install
rm -rf %{buildroot}%{_docdir}

%post
-p /sbin/ldconfig

%postun
-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/sdbus-c++/*.h
%{_includedir}/sdbus-c++/*.inl
%{_libdir}/cmake/sdbus-c++/*.cmake
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.0-1
- Auto-upgrade to 1.3.0 - Azure Linux 3.0 - package upgrades

* Mon May 16 2022 Sriram Nambakam <snambakam@microsoft.com> - 1.1.0-1
- Original version for CBL-Mariner.
- Verified license
