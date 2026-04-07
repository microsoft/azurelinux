# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           xeus-zmq
Version:        3.1.0
Release:        4%{?dist}
Summary:        ZeroMQ based middleware for xeus

License:        BSD-3-Clause
URL:            https://github.com/jupyter-xeus/xeus-zmq
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# Xeus is not available for i686
# https://src.fedoraproject.org/rpms/xeus/blob/rawhide/f/xeus.spec
ExcludeArch: %{ix86}

BuildRequires:  cmake
BuildRequires:  cppzmq-devel
BuildRequires:  gcc-c++
BuildRequires:  json-devel
BuildRequires:  libuuid-devel
BuildRequires:  openssl-devel
BuildRequires:  xeus-devel
BuildRequires:  xtl-devel
BuildRequires:  zeromq-devel
# Needed for tests
BuildRequires:  doctest-devel
BuildRequires:  python3-jupyter-kernel-test
BuildRequires:  python3-pytest

%description
xeus-zmq provides various implementations of the xserver API from
xeus, based on the ZeroMQ library. These implementations all
conform to the Jupyter Kernel Protocol specification.

%package devel
Summary:   ZeroMQ based middleware for xeus
Requires:  %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for xeus-zmq

%prep
%autosetup


%build
%cmake -DXEUS_ZMQ_BUILD_STATIC_LIBS=OFF \
       -DXEUS_ZMQ_BUILD_SHARED_LIBS=ON \
       -DXEUS_ZMQ_STATIC_DEPENDENCIES=OFF \
       -DXEUS_ZMQ_BUILD_TESTS=ON
%cmake_build


%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md
%{_libdir}/libxeus-zmq.so.6*

%files devel
%dir %{_includedir}/xeus-zmq
%{_includedir}/xeus-zmq/*.hpp
%dir %{_libdir}/cmake/xeus-zmq
%{_libdir}/cmake/xeus-zmq/*.cmake
%{_libdir}/libxeus-zmq.so

%changelog
* Sun Sep 21 2025 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 3.1.0-4
- Rebuild for xeus SONAME bump

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Sep 29 2024 Benson Muite <benson_muite@emailplus.org> - 3.1.0-1
- Update to latest release 3.1.0

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 29 2024 Benson Muite <benson_muite@emailplus.org> - 1.2.0-1
- Update to latest release 1.2.0

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Oct 07 2023 Benson Muite <benson_muite@emailplus.org> - 1.1.1-1
- Initial package 
