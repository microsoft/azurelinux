# This package doesn't contain any binaries, thus no debuginfo package is needed.
%global debug_package %{nil}

%if "%{_arch}" == "x86_64"
    %global build_cross 1
    %define cross_archs arm64
%else
    %global build_cross 0
    %define cross_archs %{nil}
%endif

Summary:        Linux API header files
Name:           kernel-headers
Version:        6.12.40.1
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
Source0:        https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/hwe-%{hwe}/%{version}.tar.gz#/kernel-%{version}.tar.gz
# Historical name shipped by other distros
Provides:       glibc-kernheaders = %{version}-%{release}
BuildArch:      noarch
%description
The Linux API Headers expose the kernel's API for use by Glibc.

%if %{build_cross}
%package -n kernel-cross-headers
Summary: Header files for the Linux kernel for use by cross-glibc.

%description -n kernel-cross-headers
Kernel-cross-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
cross-glibc package.
%endif

%prep
%setup -q -n CBL-Mariner-Linux-Kernel-rolling-lts-hwe-%{version}

%build
make mrproper
make headers

for cross_arch in %{cross_archs}; do
    make ARCH=$cross_arch O=usr/include-$cross_arch headers
done

%install
find usr/include* \( -name ".*" -o -name "Makefile" \) -delete

mkdir -p /%{buildroot}%{_includedir}
cp -rv usr/include/* /%{buildroot}%{_includedir}

for cross_arch in %{cross_archs}; do
    cross_arch_includedir=/%{buildroot}%{_prefix}/${cross_arch}-linux-gnu/include
    mkdir -p $cross_arch_includedir
    cp -rv usr/include-$cross_arch/usr/include/* $cross_arch_includedir
done

%files
%defattr(-,root,root)
%license COPYING
%{_includedir}/*

%if %{build_cross}
%files -n kernel-cross-headers
%defattr(-,root,root)
%{_prefix}/*-linux-gnu/*
%endif

%changelog
