Summary:        C++ wrapper around minizip compression library
Name:           zipper
Version:        1.0.3
Release:        1%{?dist}
# zlib licenses comes from minizip/ source code
License:        MIT AND zlib
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/File
URL:            https://github.com/sebastiandev/zipper
#Source0:       https://github.com/sebastiandev/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# The 1.0.1 version requires the 'minizip' sources from the following commit: https://github.com/sebastiandev/minizip/tree/0b46a2b4ca317b80bc53594688883f7188ac4d08
Source1:        minizip.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  zlib-devel
Provides:       bundled(minizip) = 1.2.8

%description
Zipper's goal is to bring the power and simplicity of minizip to a more
object oriented/c++ user friendly library.
It was born out of the necessiyty of a compression library that would be
reliable, simple and flexible.
By flexibility I mean supporting all kinds of inputs and outputs,
but specifically been able to compress into memory instead of being
restricted to file compression only, and using data from memory instead
of just files as well.

Features:
- Create zip in memory
- Allow files, vector and generic streams as input to zip
- File mappings for replacing strategies (overwrite if exists or use alternative name from mapping)
- Password protected zip
- Multi platform

%package devel
Summary:        Development files of %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides header files, shared and static library files of %{name}.

%prep
%setup -q

# Fix library destination
sed -e 's|DESTINATION lib|DESTINATION %{_lib}|g' -i CMakeLists.txt

# Extract 'minizip' sources dependency
tar -xf %{SOURCE1}

# Fix permissions
find minizip -name '*.c' -exec chmod 0644 '{}' \;

%build
mkdir build && cd build
export CXXFLAGS="%{optflags} -Wl,--as-needed"
%cmake .. \
  -Wno-cpp \
  -DBUILD_SHARED_VERSION:BOOL=ON \
  -DBUILD_STATIC_VERSION:BOOL=ON \
  -DBUILD_TEST:BOOL=ON
%make_build

%install
%make_install -C build
# Tests still want the static library, but we're not going to package it.
rm %{buildroot}%{_libdir}/libZipper-static.a

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
make test -C build

%files
%defattr(-,root,root)
%doc README.md VERSION.txt
%license LICENSE.md minizip/LICENSE
%{_bindir}/Zipper-test
%{_libdir}/libZipper.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/cmake/*.cmake
%{_libdir}/libZipper.so
%{_libdir}/libZipper.a
%{_datadir}/pkgconfig/zipper.pc
%{_includedir}/zipper/

%changelog
* Thu Jan 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.0.3-1
- Update to version 1.0.3.

* Wed Oct 14 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.0.1-2
- Added source URL.
- Switching to published GitHub source from the custom-made one.
- Added a separate minizip.tar.gz source.
- License verified.

* Fri Feb 14 2020 Nick Bopp <nichbop@microsoft.com> - 1.0.1-1
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Update to 1.0.1

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-6.20170831giteee877a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-5.20170831giteee877a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-4.20170831giteee877a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 03 2018 Antonio Trande <sagitter@fedoraproject.org> - 0.9.1-3.20170831giteee877a
- Rebuild for batched updates

* Sun Apr 29 2018 Antonio Trande <sagitter@fedoraproject.org> - 0.9.1-2.20170831giteee877a
- Specify bundled code's license and version

* Thu Apr 19 2018 Antonio Trande <sagitter@fedoraproject.org> - 0.9.1-1.20170831giteee877a
- First package
