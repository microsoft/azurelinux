%define debug_package %{nil}
Summary:        A core cryptographic library written by Microsoft
Name:           symcrypt
Version:        100.20
Release:        1%{?dist}
License:        MIT License
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Libraries
URL:            https://github.com/microsoft/SymCrypt
Source0:        %{name}-%{version}-with-submodules.tar.gz
Patch0:         build-only-generic.patch
Patch1:         tests-build-only-generic.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  python3-pyelftools

%description
A core cryptographic library written by Microsoft

%prep
%setup -n SymCrypt

%patch0
%patch1

%build
mkdir bin
cd bin
%ifarch aarch64
cmake .. -DCMAKE_TOOLCHAIN_FILE="../cmake-toolchain/LinuxUserMode-ARM64.cmake" -DCMAKE_BUILD_TYPE=Release
%else
cmake .. -DCMAKE_TOOLCHAIN_FILE="../cmake-toolchain/LinuxUserMode-AMD64.cmake" -DCMAKE_BUILD_TYPE=Release
%endif
cmake --build .

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
%ifarch aarch64
install bin/module/ARM64/LinuxUserMode/generic_linux/libsymcrypt.so %{buildroot}%{_libdir}/
%else
install bin/module/AMD64/LinuxUserMode/generic_linux/libsymcrypt.so %{buildroot}%{_libdir}/
%endif
install inc/* %{buildroot}%{_includedir}

%files
%license LICENSE
%{_libdir}/libsymcrypt.so
%{_includedir}/*

%changelog
* Mon Jan 01 2022 Spencer Nofzinger <spnofzin@microsoft.com> - 100.20-1
- Initial CBL-Mariner import
