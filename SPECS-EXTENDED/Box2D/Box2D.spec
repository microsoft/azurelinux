%global __cmake_in_source_build 1

Summary:        A 2D Physics Engine for Games
Name:           Box2D
Version:        2.4.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries
URL:            http://box2d.org/
Source0:        https://github.com/erincatto/box2d/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make

%description
Box2D is an open source C++ engine for simulating rigid bodies in 2D.
Box2D is developed by Erin Catto and has the MIT license.
While the MIT license does not require acknowledgement,
we encourage you to give credit to Box2D in your product.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
Box2D is an open source C++ engine for simulating rigid bodies in 2D.
Box2D is developed by Erin Catto and has the MIT license.
While the MIT license does not require acknowledgement,
we encourage you to give credit to Box2D in your product.

These are the development files.

%prep
%autosetup -n box2d-%{version}
rm -r extern

%build
%cmake -DBOX2D_INSTALL=ON -DBOX2D_BUILD_SHARED=ON -DBOX2D_BUILD_TESTBED=OFF -DBOX2D_BUILD_UNIT_TESTS=OFF .
%cmake_build

%install
%cmake_install

%ldconfig_scriptlets

%files
%license LICENSE
%{_libdir}/*.so.2*

%files devel
%doc README.md docs/
%{_libdir}/*.so
%{_includedir}/box2d
%{_libdir}/cmake/box2d/*.cmake

%changelog
* Tue Aug 13 2024 Azure Linux Team <azurelinux@microsoft.com> - 2.4.2-1
- Original version for Azure Linux
- License Verified
