Summary:        C, C++, Objective C and Objective C++ front-end for the LLVM compiler.
Name:           clang
Version:        8.0.1
Release:        4%{?dist}
License:        NCSA
URL:            https://clang.llvm.org
Source0:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/cfe-%{version}.src.tar.xz
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  cmake
BuildRequires:  llvm-devel = %{version}
BuildRequires:  ncurses-devel
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
BuildRequires:  python2-devel
Requires:       libstdc++-devel
Requires:       ncurses
Requires:       llvm
Requires:       zlib
Requires:       libxml2
Requires:       python2

%description
The goal of the Clang project is to create a new C based language front-end: C, C++, Objective C/C++, OpenCL C and others for the LLVM compiler. You can get and build the source today.

%package devel
Summary:        Development headers for clang
Requires:       %{name} = %{version}-%{release}

%description devel
The clang-devel package contains libraries, header files and documentation
for developing applications that use clang.

%prep
%setup -q -n cfe-%{version}.src

%build
# Disable symbol generation
export CFLAGS="`echo " %{build_cflags} " | sed 's/ -g//'`"
export CXXFLAGS="`echo " %{build_cxxflags} " | sed 's/ -g//'`"

mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr   \
      -DCMAKE_BUILD_TYPE=Release    \
      -DLLVM_ENABLE_RTTI=ON         \
      -Wno-dev ..

make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
cd build
make DESTDIR=%{buildroot} install

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
cd build
make clang-check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE.TXT
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/*.so.*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/cmake/*
%{_libdir}/clang/*
%{_includedir}/*

%changelog
*   Tue Feb 09 2021 Henry Beberman <henry.beberman@microsoft.com> 8.0.1-4
-   Enable RTTI (runtime type information) so other packages can depend on it.
*   Fri Jun 12 2020 Henry Beberman <henry.beberman@microsoft.com> 8.0.1-3
-   Temporarily disable generation of debug symbols.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 8.0.1-2
-   Added %%license line automatically
*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 8.0.1-1
-   Update to 8.0.1. Fix Source0 URL. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 6.0.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Aug 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 6.0.1-1
-   Update to version 6.0.1 to get it to build with gcc 7.3
*   Wed Jun 28 2017 Chang Lee <changlee@vmware.com> 4.0.0-2
-   Updated %check
*   Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.0-1
-   Version update
*   Wed Jan 11 2017 Xiaolin Li <xiaolinl@vmware.com>  3.9.1-1
-   Initial build.
