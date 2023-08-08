Summary:        LLD is a linker from the LLVM project that is a drop-in replacement for system linkers and runs much faster than them
Name:           lld16
Version:        16.0.0
Release:        1%{?dist}
License:        NCSA
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://clang.llvm.org
Source0:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/lld-%{version}.src.tar.xz
# The `lld` build needs access to `mach-o/compact_unwind_encoding.h` which LLVM
# packages with the `libunwind` source.  We fetch and unpack both sources then
# pass an additional `-I` to `CMAKE` to allow the build to find the header.
Source1:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/libunwind-%{version}.src.tar.xz
Source2:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/cmake-%{version}.src.tar.xz#/llvm-cmake-%{version}.src.tar.xz
# The additional cmake tarball includes files that were previously included in 
# the standalone release but started to be a requirement starting in version 
# 15. The tarball was renamed to reduce possible collisions in the future with
# cmake itself
BuildRequires:  build-essential
BuildRequires:  cmake
BuildRequires:  file
BuildRequires:  llvm16-devel
BuildRequires:  ncurses-devel
BuildRequires:  zlib-devel
BuildRequires:  ninja-build
BuildRequires:  python3
Requires:       %{name}-libs = %{version}-%{release}

%package devel
Summary:        Libraries and header files for LLD
Requires:       %{name} = %{version}-%{release}

%package libs
Summary:        LLD shared libraries

%description
The LLVM project linker.

%description devel
This package contains library and header files needed to develop new native
programs that use the LLD infrastructure.

%description libs
Shared libraries for LLD.

%prep
tar -xf %{SOURCE2}
mv cmake-16.0.0.src cmake
%setup -q -b 1 -n lld-%{version}.src

%build
mkdir -p build
cd build
%cmake ..                                                         \
       -G Ninja                                                   \
       -DCMAKE_BUILD_TYPE=Release                                 \
       -DCMAKE_SKIP_RPATH:BOOL=on                                 \
       -DCMAKE_C_FLAGS=-I../../libunwind-%{version}.src/include   \
       -DCMAKE_CXX_FLAGS=-I../../libunwind-%{version}.src/include \
       -DLLVM_LINK_LLVM_DYLIB:BOOL=on                             \
       -DLLVM_DYLIB_COMPONENTS="all"                              \
       -Wno-dev
%ninja_build

%install
cd build
%ninja_install

%files
%{_bindir}/*

%files devel
%{_includedir}/lld/
%{_libdir}/cmake/lld/*.cmake
%{_libdir}/*.so

%files libs
%license LICENSE.TXT
%{_libdir}/*.so.16*

%changelog
* Wed Jul 12 2023 Sam Meluch <sammeluch@microsoft.com> 16.0.0-1
- Add lld16 for llvm16/clang16
- Update spec from lld12 for use with lld16

* Thu Aug 12 2021 Andy Caldwell <andycaldwell@microsoft.com>  12.0.1-1
- Original version for CBL-Mariner.
- License verified
