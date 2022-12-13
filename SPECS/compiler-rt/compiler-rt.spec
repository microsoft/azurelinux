%global compiler_rt_srcdir %{name}-%{version}.src

Summary:        LLVM compiler support routines
Name:           compiler-rt
Version:        12.0.1
Release:        1%{?dist}
License:        Apache 2.0 WITH exceptions
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://compiler-rt.llvm.org
Source0:        https://github.com/llvm/llvm-project/releases/download/llvmorg-%{version}/%{compiler_rt_srcdir}.tar.xz
BuildRequires:  cmake
BuildRequires:  llvm-devel = %{version}
Requires:       llvm

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
       -Wno-dev ..

%make_build

%install
cd build
%make_install

mkdir -p %{buildroot}%{_libdir}/clang/%{version}/share
mv -v %{buildroot}%{_datadir}/*list.txt  %{buildroot}%{_libdir}/clang/%{version}/share/

mkdir -p %{buildroot}%{_libdir}/clang/%{version}/lib/linux
mv -v %{buildroot}%{_prefix}/lib/linux/*clang_rt* %{buildroot}%{_libdir}/clang/%{version}/lib/linux

%files
%defattr(-,root,root)
%license LICENSE.TXT

%{_includedir}/fuzzer
%{_includedir}/profile
%{_includedir}/sanitizer
%{_includedir}/xray
%{_libdir}/clang/%{version}/lib/linux/*
%{_libdir}/clang/%{version}/share/*
%{_bindir}/hwasan_symbolize

%changelog
* Tue Dec 06 2022 Adam Schwab <adschwab@microsoft.com> - 12.0.1-1
- Initial CBL-Mariner import from Fedora 35 (license: MIT). License verified.
