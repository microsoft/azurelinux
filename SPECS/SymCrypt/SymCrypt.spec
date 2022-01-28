%define debug_package %{nil}
Summary:        A core cryptographic library written by Microsoft
Name:           SymCrypt
Version:        101.0.0
Release:        1%{?dist}
License:        MIT License
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Libraries
URL:            https://github.com/microsoft/SymCrypt
#Source0:       https://github.com/microsoft/SymCrypt/archive/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
#Source1        https://github.com/smuellerDD/jitterentropy-library/archive/v3.3.1.tar.gz
Source1:        jitterentropy-library-3.3.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  python3-pyelftools

%description
A core cryptographic library written by Microsoft

%prep
%setup
%setup -a 1
# Create a symbolic link as if jitterentropy-library has been pulled in as git submodule
rm -rf jitterentropy-library
ln -s jitterentropy-library-3.3.1 jitterentropy-library

%build
mkdir bin; cd bin

cmake   .. \
%ifarch x86_64
        -DCMAKE_TOOLCHAIN_FILE="../cmake-toolchain/LinuxUserMode-AMD64.cmake" \
%endif
%ifarch aarch64
        -DCMAKE_TOOLCHAIN_FILE="../cmake-toolchain/LinuxUserMode-ARM64.cmake" \
%endif
        -DCMAKE_BUILD_TYPE=Release

cmake --build .

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
install inc/* %{buildroot}%{_includedir}
%ifarch x86_64
install bin/module/AMD64/LinuxUserMode/generic/libsymcrypt.so %{buildroot}%{_libdir}/
%endif
%ifarch aarch64
install bin/module/ARM64/LinuxUserMode/generic/libsymcrypt.so %{buildroot}%{_libdir}/
%endif
# Other architectures will currently break here because we are not creating the expected
# libsymcrypt.so output. Equally, other architectures currently should not include SymCrypt in their
# package list!

%files
%license LICENSE
%{_libdir}/libsymcrypt.so
%{_includedir}/*

%changelog
* Fri Jan 28 2022 Samuel Lee <saml@microsoft.com> - 101.0.0-1
- Initial CBL-Mariner import
