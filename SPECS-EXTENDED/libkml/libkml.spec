%bcond_with java
%global _smp_mflags -j1
%global __requires_exclude_from ^%{_docdir}/.*$
%global __provides_exclude_from ^%{python3_sitearch}/.*\\.so$

Summary:        Reference implementation of OGC KML 2.2
Name:           libkml
Version:        1.3.0
Release:        41%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/libkml/libkml
Source0:        https://github.com/libkml/libkml/archive/%{version}/libkml-%{version}.tar.gz
# TODO: Port to minizip-2.x, meanwhile bundle version 1.3.0
# wget -O minizip-1.3.0.tar.gz http://sourceforge.net/projects/libkml-files/files/1.3.0/minizip.tar.gz/download
Source1:        minizip-1.3.0.tar.gz
## See https://github.com/libkml/libkml/pull/239
Patch0:         0001-Fix-build-failure-due-to-failure-to-convert-pointer-.patch
Patch1:         0002-Fix-mistaken-use-of-std-cerr-instead-of-std-endl.patch
Patch2:         0003-Fix-python-tests.patch
Patch3:         0004-Correctly-build-and-run-java-test.patch
# Fix a fragile test failing on i686
Patch4:         fragile_test.patch
# Don't bytecompile python sources as part of build process, leave it to rpmbuild
Patch5:         libkml_dont-bytecompile.patch
# Add crypt.h which was removed from Fedora minizip package (see #1424609)
Patch6:         libkml_crypth.patch
# Use local file for bundled minizip
Patch7:         libkml-bundle-minizip.patch
# Fix possible OOB array access in strcmp due to undersized array
Patch8:         libkml_test_strcmp.patch
# MinGW build fixes
Patch9:         libkml_mingw.patch

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  expat-devel
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  swig
BuildRequires:  uriparser-devel
BuildRequires:  zlib-devel
Provides:       bundled(minizip) = 1.3.0
%if %{with java}
BuildRequires:  java-devel
BuildRequires:  junit
%endif

%description
Reference implementation of OGC KML 2.2.
It also includes implementations of Google's gx: extensions used by Google
Earth, as well as several utility libraries for working with other formats.

%package -n python3-%{name}
Summary:        Python 3 bindings for %{name}
%{?python_provide:%python_provide python3-%{name}}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
The python3-%{name} package contains Python 3 bindings for %{name}.

%if %{with java}
%package java
Summary:        Java bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description java
The %{name}-java package contains Java bindings for %{name}.
%endif


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       boost-devel
Requires:       expat-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -a1


%build
# Build bundled minizip
pushd minizip
(
%cmake -DBUILD_SHARED_LIBS=OFF
%cmake_build
)
popd
ls -la minizip

# Native build
%cmake -DWITH_SWIG=ON -DWITH_PYTHON=ON \
%if %{with java}
  -DWITH_JAVA=ON -DJNI_INSTALL_DIR=%{_libdir}/%{name} \
%endif
  -DCMAKE_INSTALL_DIR=%{_libdir}/cmake/%{name} \
  -DINCLUDE_INSTALL_DIR=%{_includedir}/kml \
  -DPYTHON_LIBRARY=%{_libdir}/libpython%{python3_version}$(python3-config --abiflags).so \
  -DPYTHON_INCLUDE_DIR=%{_includedir}/python%{python3_version}$(python3-config --abiflags)/ \
  -DPYTHON_INSTALL_DIR=%{python3_sitearch} \
  -DMINIZIP_INCLUDE_DIR=$PWD -DMINIZIP_LIBRARY=$PWD/minizip/libminizip.a \
  -DBUILD_TESTING=ON \
%cmake_build


%install
%cmake_install


%check
%ctest


%files
%license LICENSE
%doc AUTHORS README.md
%{_libdir}/libkml*.so.*

%files -n python3-%{name}
%{python3_sitearch}/*.so
%{python3_sitearch}/*.py
%{python3_sitearch}/__pycache__/*.pyc

%if %{with java}
%files java
%{_javadir}/LibKML.jar
%{_libdir}/%{name}/
%endif

%files devel
%doc examples
%{_includedir}/kml/
%{_libdir}/libkml*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/

%changelog
* Wed Aug 16 2023 Archana Choudhary <archana1@microsoft.com> - 1.3.0-41
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified.
- Remove examples from build

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.3.0-39
- Rebuilt for Python 3.11

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.3.0-38
- Rebuild with mingw-gcc-12

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 1.3.0-37
- Make mingw subpackages noarch

* Mon Feb 21 2022 Sandro Mani <manisandro@gmail.com> - 1.3.0-36
- Add mingw subpackages

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.3.0-35
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 12 2021 Sandro Mani <manisandro@gmail.com> - 1.3.0-31
- Disable java build for now

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.3.0-31
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1.3.0-27
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-26
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 30 2019 Sandro Mani <manisandro@gmail.com> - 1.3.0-24
- Fix possible OOB array access in strcmp due to undersized array

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-23
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-22
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 03 2019 Sandro Mani <manisandro@gmail.com> - 1.3.0-20
- Don't hard-code abi flags

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Björn Esser <besser82@fedoraproject.org> - 1.3.0-18
- Append curdir to CMake invokation. (#1668512)

* Fri Oct 05 2018 Sandro Mani <manisandro@gmail.com> - 1.3.0-17
- Statically link against bundled minizip

* Thu Oct 04 2018 Sandro Mani <manisandro@gmail.com> - 1.3.0-16
- Drop python2 subpackage (#1634846)
- Bundle minizip (#1632186)
- Remove obsolete scriptlets

* Tue Aug 28 2018 Patrik Novotný <panovotn@redhat.com> - 1.3.0-15
- change requires to minizip-compat(-devel), rhbz#1609830, rhbz#1615381

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-13
- Rebuilt for Python 3.7

* Tue Jun 19 2018 Sandro Mani <manisandro@gmail.com> - 1.3.0-12
- Locally add crypt.h from minizip, which was removed in minizip-devel (see #1424609)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-11
- Rebuilt for Python 3.7

* Sun Feb 18 2018 Sandro Mani <manisandro@gmail.com> - 1.3.0-10
- Add missing BR: gcc-c++, make

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 07 2017 Sandro Mani <manisandro@gmail.com> - 1.3.0-8
- Workaround armv7hl FTBFS
- Add python3 bindings

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Jonathan Wakely <jwakely@redhat.com> - 1.3.0-5
- Rebuilt for Boost 1.64

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Apr 08 2016 Sandro Mani <manisandro@gmail.com> - 1.3.0-2
- Don't call it Google's reference implementation in Summary/Description
- Update Source URL
- Add python_provide macro
- Enable tests

* Thu Mar 31 2016 Sandro Mani <manisandro@gmail.com> - 1.3.0-1
- Update to 1.3.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 02 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6.1-7
- Fix gcc warning that lead to failure due to -Werror flag

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-4
- Included *pyc and pyo files in %%files and added BuildRequires libgcj-devel.

* Sun Apr 12 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-3
- libkml-0.6.1.configure_ac.patch patch for swig > 1.3.35

* Sat Mar 07 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-2
- updated to 0.6.1
- libkml-third_party_removal.diff Removes third part dependency
- (provided by Peter Lemenkov)

* Fri Jan 16 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.6.1-1
- Updated to 0.6.1

* Mon Oct 06 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.4.0-2
- Added >= 1.3.35 for swing

* Sat Aug 09 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.4.0-1
- Initial package
