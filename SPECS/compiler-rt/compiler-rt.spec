%global compiler_rt_srcdir llvm-project-llvmorg-%{version}

Summary:        LLVM compiler support routines
Name:           compiler-rt
Version:        17.0.6
Release:        1%{?dist}
License:        Apache 2.0 WITH exceptions
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://compiler-rt.llvm.org
Source0:        https://github.com/llvm/llvm-project/archive/refs/tags/llvmorg-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  llvm-devel = %{version}
Requires:       llvm = %{version}

%description
The compiler-rt project consists of several related runtime libraries for interfacing
with the clang compiler infrastructure. Builtins is a library for providing low-level
target-specific hooks required by code generation and other runtime components. Sanitizer
consists of several sanitizers such as the AddressSanitizer that can include instrumentation
into compiled binaries. Profile is a library used to collect coverage information and
BlocksRuntime is an implementation of Apple "blocks" interface.

%prep
%setup -q -n %{compiler_rt_srcdir}

%build
mkdir -p build
cd build
%cmake -DCMAKE_BUILD_TYPE=Release  \
	-DCOMPILER_RT_INSTALL_PATH=%{_prefix}/lib/clang/%{version} \
       -Wno-dev ../compiler-rt

%make_build

%install
cd build
%make_install

%files
%defattr(-,root,root)
%license LICENSE.TXT

%{_libdir}/clang/%{version}/bin/*
%{_libdir}/clang/%{version}/include/*
%{_libdir}/clang/%{version}/lib/*
%{_libdir}/clang/%{version}/share/*

%changelog
* Tue Jan 16 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 17.0.6-1
- Upgrade to 17.0.6

* Tue Dec 06 2022 Adam Schwab <adschwab@microsoft.com> - 12.0.1-1
- Initial CBL-Mariner import from Fedora 35 (license: MIT). License verified.
