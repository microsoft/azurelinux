Summary:        YANG data modeling language library
Name:           libyang
Version:        2.1.111
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/CESNET/libyang
Source:         https://github.com/CESNET/libyang/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  libcmocka-devel
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  valgrind
BuildRequires:  pkgconfig(libpcre2-8) >= 10.21

%package devel
Summary:        Development files for libyang
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pcre2-devel

%package devel-doc
Summary:        Documentation of libyang API
Requires:       %{name}%{?_isa} = %{version}-%{release}

%package tools
Summary:        YANG validator tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers of libyang library.

%description devel-doc
Documentation of libyang API.

%description tools
YANG validator tools.

%description
Libyang is YANG data modeling language parser and toolkit
written (and providing API) in C.

%prep
%autosetup -p1

%build
mkdir build
pushd build
%cmake \
   -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
   -DCMAKE_BUILD_TYPE=RELWITHDEBINFO \
   -DENABLE_LYD_PRIV=ON \
   -DENABLE_VALGRIND_TESTS=ON ..
%make_build
make doc

%check
ctest --output-on-failure -V %{?_smp_mflags}

%install
pushd build
%make_install
popd
mkdir -m0755 -p %{buildroot}/%{_docdir}/libyang
cp -a doc/html %{buildroot}/%{_docdir}/libyang/html

%files
%license LICENSE
%{_libdir}/libyang.so.2
%{_libdir}/libyang.so.2.*
%{_datadir}/yang/modules/libyang/*.yang
%dir %{_datadir}/yang/
%dir %{_datadir}/yang/modules/
%dir %{_datadir}/yang/modules/libyang/

%files tools
%{_bindir}/yanglint
%{_bindir}/yangre
%{_mandir}/man1/yanglint.1.gz
%{_mandir}/man1/yangre.1.gz

%files devel
%{_libdir}/libyang.so
%{_libdir}/pkgconfig/libyang.pc
%{_includedir}/libyang/*.h
%dir %{_includedir}/libyang/

%files devel-doc
%{_docdir}/libyang

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.1.111-1
- Auto-upgrade to 2.1.111 - Azure Linux 3.0 - package upgrades

* Mon Apr 10 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.1.55-1
- Auto-upgrade to 2.1.55 - to fix CVE-2023-26916

* Thu Oct 06 2022 Tom Fay <tomfay@microsoft.com> - 2.0.231-1
- Initial CBL-Mariner import from Fedora 35 (license: MIT).
- License verified
