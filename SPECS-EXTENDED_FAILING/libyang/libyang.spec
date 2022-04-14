Vendor:         Microsoft Corporation
Distribution:   Mariner
# valgrind finds invalid writes in libcmocka on arm
# see bug #1699304 for more information
%ifarch %arm
%global run_valgrind_tests OFF
%else
%global run_valgrind_tests ON
%endif

%global rsuffixver 1.0-r5

Name: libyang
Version: 1.0.101
Release: 3%{?dist}
Summary: YANG data modeling language library
Url: https://github.com/CESNET/libyang
Source: %{url}/archive/v%{rsuffixver}.tar.gz#/%{name}-%{version}.tar.gz
License: BSD

Requires:  pcre
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  pcre-devel
BuildRequires:  gcc
BuildRequires:  valgrind
BuildRequires:  gcc-c++
BuildRequires:  swig >= 3.0.12
BuildRequires:  libcmocka-devel
BuildRequires:  python3-devel
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  graphviz

%package devel
Summary:    Development files for libyang
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pcre-devel

%package devel-doc
Summary:    Documentation of libyang API
Requires:   %{name} = %{version}-%{release}
BuildArch:  noarch

%package -n libyang-cpp
Summary:    C++ bindings for libyang
Requires:   %{name}%{?_isa} = %{version}-%{release}

%package -n libyang-cpp-devel
Summary:    Development files for libyang-cpp
Requires:   libyang-cpp%{?_isa} = %{version}-%{release}
Requires:   pcre-devel

%package -n python3-libyang
Summary:    Python3 bindings for libyang
Requires:   libyang-cpp%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python3-libyang}

%description -n libyang-cpp
Bindings of libyang library to C++ language.

%description -n libyang-cpp-devel
Headers of bindings to c++ language.

%description -n python3-libyang
Bindings of libyang library to python language.

%description devel
Headers of libyang library.

%description devel-doc
Documentation of libyang API.

%description
Libyang is YANG data modeling language parser and toolkit
written (and providing API) in C.

%prep
%setup -q -n libyang-%{rsuffixver}
mkdir build

%build
cd build
%cmake \
   %{?_smp_mflags} \
   -DCMAKE_INSTALL_PREFIX:PATH=/usr \
   -DCMAKE_BUILD_TYPE:String="Package" \
   -DENABLE_LYD_PRIV=ON \
   -DGEN_JAVA_BINDINGS=OFF \
   -DGEN_JAVASCRIPT_BINDINGS=OFF \
   -DGEN_LANGUAGE_BINDINGS=ON \
   -DENABLE_VALGRIND_TESTS=%{run_valgrind_tests} ..
%make_build
make doc

%check
cd build
ctest --output-on-failure -V %{?_smp_mflags}

%install
pushd build
%make_install DESTDIR=%{buildroot}
popd
mkdir -m0755 -p %{buildroot}/%{_docdir}/libyang
cp -r doc/html %{buildroot}/%{_docdir}/libyang/html

%files
%license LICENSE
%{_bindir}/yanglint
%{_bindir}/yangre
%{_datadir}/man/man1/yanglint.1.gz
%{_datadir}/man/man1/yangre.1.gz
%{_libdir}/libyang
%{_libdir}/libyang.so.1*
%{_libdir}/libyang/extensions
%{_libdir}/libyang/user_types/*
%dir %{_libdir}/libyang/

%files devel
%{_libdir}/libyang.so
%{_libdir}/pkgconfig/libyang.pc
%{_includedir}/libyang/*.h
%dir %{_includedir}/libyang/

%files devel-doc
%{_docdir}/libyang

%files -n libyang-cpp
%{_libdir}/libyang-cpp.so.*

%files -n libyang-cpp-devel
%{_libdir}/libyang-cpp.so
%{_includedir}/libyang/*.hpp
%{_libdir}/pkgconfig/libyang-cpp.pc
%dir %{_includedir}/libyang/

%files -n python3-libyang
%{python3_sitearch}/yang.py
%{python3_sitearch}/_yang.so
%{python3_sitearch}/__pycache__/yang*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.101-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Tomas Korbar <tkorbar@redhat.com> - 1.0.101-1
- Rebase to version 1.0.101
- Fix CVE-2019-19333 (#1780495)
- Fix CVE-2019-19334 (#1780494)

* Fri Oct 25 2019 Tomas Korbar <tkorbar@redhat.com> - 1.0.73-1
- Rebase to version 1.0.73 (#1758512)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.16.105-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.16.105-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.105-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 07 2019 Tomas Korbar <tkorbar@redhat.com> - 0.16.105-1
- Initial import (#1699846).

* Fri Apr 26 2019 Tomas Korbar <tkorbar@redhat.com> - 0.16.105-1
- Change specfile accordingly to mosvald's review
- Remove obsolete ldconfig scriptlets
- libyang-devel-doc changed to noarch package
- Add python_provide macro to python3-libyang subpackage
- Remove obsolete Requires from libyang-cpp-devel
- Start using cmake with smp_mflags macro

* Wed Apr 03 2019 Tomas Korbar <tkorbar@redhat.com> - 0.16.105-1
- Initial commit of package after editation of specfile
