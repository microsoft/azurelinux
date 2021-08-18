Summary:        LLD is a linker from the LLVM project that is a drop-in replacement for system linkers and runs much faster than them
Name:           lld
Version:        8.0.1
Release:        1%{?dist}
License:        NCSA
URL:            https://clang.llvm.org
Source0:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/lld-%{version}.src.tar.xz
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner
Requires:       ncurses
Requires:       libxml2
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  build-essential
BuildRequires:  llvm-devel
BuildRequires:  ncurses-devel
BuildRequires:  libxml2
BuildRequires:  python3

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
%{_libdir}/*.so.*

%changelog
*   Thu Aug 12 2021 Andy Caldwell <andycaldwell@metaswitch.com>  8.0.1-1
-   Initial build.
