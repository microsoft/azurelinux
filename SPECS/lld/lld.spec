%global lld_srcdir llvm-project-llvmorg-%{version}

Summary:        LLD is a linker from the LLVM project that is a drop-in replacement for system linkers and runs much faster than them
Name:           lld
Version:        18.1.8
Release:        1%{?dist}
License:        NCSA
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Tools
URL:            https://lld.llvm.org/
Source0:        https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  file
BuildRequires:  llvm-devel
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
%autosetup -n %{lld_srcdir}

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
       -DCMAKE_INSTALL_PREFIX=%{_prefix}                          \
       -DLLVM_DIR=%{_libdir}/cmake/llvm                           \
       -DBUILD_SHARED_LIBS:BOOL=ON                                \
       -DLLVM_DYLIB_COMPONENTS="all"                              \
       -Wno-dev                                                   \
       ../lld

%ninja_build

%install
cd build
%ninja_install

%files
%license LICENSE.TXT
%{_bindir}/lld*
%{_bindir}/ld.lld
%{_bindir}/ld64.lld
%{_bindir}/wasm-ld

%files devel
%{_includedir}/lld/
%{_libdir}/cmake/lld/*.cmake
%{_libdir}/liblld*.so

%files libs
%{_libdir}/liblld*.so.*

%changelog
* Tue Jun 03 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 18.1.8-1
- Updated to version 18.1.8.

* Tue Sep 03 2024 Andrew Phelps <anphel@microsoft.com> - 18.1.2-3
- Update file listing with explicit filenames
- Remove unnecessary BR on build-essential

* Wed May 29 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 18.1.2-2
- Bump release to build with new llvm to fix CVE-2024-31852

* Wed Apr 03 2024 Andrew Phelps <anphel@microsoft.com> - 18.1.2-1
- Upgrade to version 18.1.2

* Tue Jan 16 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 17.0.6-1
- Upgrade to 17.0.6

* Thu Aug 12 2021 Andy Caldwell <andycaldwell@microsoft.com>  12.0.1-1
- Original version for CBL-Mariner.
- License verified
