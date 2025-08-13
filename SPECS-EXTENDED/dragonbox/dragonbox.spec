# Header-only package
%global debug_package %{nil}

Summary:        Reference implementation of Dragonbox in C++
Name:           dragonbox
Version:        1.1.3
Release:        1%{?dist}
License:        Apache-2.0 WITH LLVM-exception OR BSL-1.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries
URL:            https://github.com/jk-jeon/dragonbox
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  gcc-c++
BuildRequires:  cmake

%description
Dragonbox is a float-to-string conversion algorithm based on a beautiful
algorithm Schubfach, developed by Raffaello Giulietti in 2017-2018.
Dragonbox is further inspired by Grisu and Grisu-Exact.

Dragonbox generates a pair of integers from a floating-point number: the decimal
significand and the decimal exponent of the input floating-point number. These
integers can then be used for string generation of decimal representation of the
input floating-point number, the procedure commonly called ftoa or dtoa.

%package devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}

%description devel
Development files for %{name}. This is a header-only C++ library for
high-performance float-to-string conversion.

%prep
%autosetup

%build
%cmake -DDRAGONBOX_INSTALL_TO_CHARS=OFF
%cmake_build

%check
# No tests provided by upstream

%install
%cmake_install

%files devel
%license LICENSE-Apache2-LLVM LICENSE-Boost
%doc README.md
%{_includedir}/%{name}-%{version}/
%{_libdir}/cmake/%{name}-%{version}/

%changelog
* Mon Aug 13 2025 Microsoft Corporation <azurelinux@microsoft.com> - 1.1.3-1
- Original version for Azure Linux
- License Verified
