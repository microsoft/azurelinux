## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libnvidia-container
Version:        1.20.0
Release:        %autorelease
Summary:        NVIDIA container runtime library
License:        Apache-2.0 AND GPL-3.0-or-later AND LGPL-3.0-or-later AND MIT AND GPL-2.0-only
URL:            https://github.com/NVIDIA/libnvidia-container
Vendor:         NVIDIA CORPORATION
Packager:       NVIDIA CORPORATION <cudatools@nvidia.com>

ExclusiveArch:  x86_64 aarch64

%global major %(echo %{version} | cut -d. -f1)

# Upstream's own Makefile always builds this statically from source (no
# system-libtirpc option), and modern glibc dropped <rpc/rpc.h> entirely, so
# this must be vendored regardless of distro.
Source0:        https://github.com/NVIDIA/libnvidia-container/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/NVIDIA/nvidia-modprobe/archive/550.54.14.tar.gz#/nvidia-modprobe-550.54.14.tar.gz
Source2:        https://downloads.sourceforge.net/project/libtirpc/libtirpc/1.3.2/libtirpc-1.3.2.tar.bz2

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  m4
BuildRequires:  rpcgen
BuildRequires:  libcap-devel
BuildRequires:  libseccomp-devel
BuildRequires:  elfutils-libelf-devel

%description
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

%prep
%autosetup

# Pre-stage the vendored deps that upstream's mk/*.mk normally curl at build
# time, so `make deps` finds its .download_stamp already satisfied and never
# touches the network.
mkdir -p deps/src/nvidia-modprobe-550.54.14
tar -C deps/src/nvidia-modprobe-550.54.14 --strip-components=1 \
    -xzf %{SOURCE1} nvidia-modprobe-550.54.14/modprobe-utils
patch -d deps/src/nvidia-modprobe-550.54.14 -p1 < mk/nvidia-modprobe.patch
touch deps/src/nvidia-modprobe-550.54.14/.download_stamp

mkdir -p deps/src/libtirpc-1.3.2
tar -C deps/src/libtirpc-1.3.2 --strip-components=1 -xjf %{SOURCE2}
touch deps/src/libtirpc-1.3.2/.download_stamp

# libtirpc 1.3.2 predates GCC 14 defaulting to C23, where an empty "()"
# parameter list means "no arguments" instead of "unspecified"; its stale
# K&R-style forward declarations then conflict with the real prototypes.
sed -i '/^export CFLAGS/s/$/ -std=gnu17/' mk/libtirpc.mk

%build
# WITH_LIBELF=yes: link system elfutils-libelf instead of vendoring elftoolchain.
# WITH_NVCGO=no: use the legacy C cgroup path instead of the Go/cgo shim.
%{__make} all \
    LIB_VERSION=%{version} \
    REVISION=v%{version} \
    WITH_NVCGO=no \
    WITH_LIBELF=yes \
    WITH_TIRPC=yes \
    WITH_SECCOMP=yes

%install
DESTDIR=%{buildroot} %{__make} install \
    prefix=%{_prefix} exec_prefix=%{_exec_prefix} bindir=%{_bindir} \
    libdir=%{_libdir} includedir=%{_includedir} docdir=%{_licensedir} \
    LIB_VERSION=%{version} \
    REVISION=v%{version} \
    WITH_NVCGO=no \
    WITH_LIBELF=yes \
    WITH_TIRPC=yes \
    WITH_SECCOMP=yes

%package -n %{name}%{major}
Summary:        NVIDIA container runtime library
%description -n %{name}%{major}
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

This package requires the NVIDIA driver (>= 340.29) to be installed separately.

%post -n %{name}%{major} -p /sbin/ldconfig
%postun -n %{name}%{major} -p /sbin/ldconfig

%files -n %{name}%{major}
%license %{_licensedir}/*
%{_libdir}/lib*.so.*

%package devel
Summary:        NVIDIA container runtime library (development files)
Requires:       %{name}%{major}%{?_isa} = %{version}-%{release}

%description devel
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

This package contains the files required to compile programs with the library.

%files devel
%license %{_licensedir}/*
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%package static
Summary:        NVIDIA container runtime library (static library)
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

This package requires the NVIDIA driver (>= 340.29) to be installed separately.

%files static
%license %{_licensedir}/*
%{_libdir}/lib*.a

# Debug symbols are extracted manually by the upstream Makefile (objcopy
# --only-keep-debug) rather than rpmbuild's automatic find-debuginfo.
%define debug_package %{nil}

%package -n %{name}%{major}-debuginfo
Summary:        NVIDIA container runtime library (debugging symbols)
Requires:       %{name}%{major}%{?_isa} = %{version}-%{release}

%description -n %{name}%{major}-debuginfo
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

This package contains the debugging symbols for the library.

%files -n %{name}%{major}-debuginfo
%license %{_licensedir}/*
%{_prefix}/lib/debug%{_libdir}/lib*.so.*

%package tools
Summary:        NVIDIA container runtime library (command-line tools)
Requires:       %{name}%{major}%{?_isa} = %{version}-%{release}

%description tools
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

This package contains command-line tools that facilitate using the library.

%files tools
%license %{_licensedir}/*
%{_bindir}/*

%changelog
## START: Generated by rpmautospec
* Tue Sep 22 2026 John Doe <packager@example.com> - 1.20.0-1
- Uncommitted changes
## END: Generated by rpmautospec
