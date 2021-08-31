Summary:        LLD is a linker from the LLVM project that is a drop-in replacement for system linkers and runs much faster than them
Name:           lld
Version:        8.0.1
Release:        1%{?dist}
License:        NCSA
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://clang.llvm.org
Source0:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/lld-%{version}.src.tar.xz
BuildRequires:  build-essential
BuildRequires:  cmake
BuildRequires:  libxml2
BuildRequires:  llvm-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  python3
Requires:       libxml2
Requires:       ncurses

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
%setup -q -n lld-%{version}.src

%build
mkdir -p build
cd build
%cmake .. \
       -DCMAKE_SKIP_RPATH:BOOL=on     \
       -DLLVM_LINK_LLVM_DYLIB:BOOL=on \
       -DLLVM_DYLIB_COMPONENTS="all"  \
       -DLLVM_MAIN_SRC_DIR=%{_datadir}/llvm/src
%make_build

%install
cd build
%make_install

%files
%license LICENSE.TXT
%{_bindir}

%files devel
%{_includedir}/lld
%{_libdir}/*.so

%files libs
%{_libdir}/*.so.8*

%changelog
*   Thu Aug 12 2021 Andy Caldwell <andycaldwell@microsoft.com>  8.0.1-1
-   Original version for CBL-Mariner.
-   License verified
