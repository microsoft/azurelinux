Name:           libnvidia-container
Version:        1.20.0
Release:        %autorelease
Summary:        NVIDIA container runtime library
License:        BSD-3-Clause AND Apache-2.0 AND GPL-3.0-or-later AND LGPL-3.0-or-later AND MIT AND GPL-2.0-only
URL:            https://github.com/NVIDIA/libnvidia-container
Vendor:         NVIDIA CORPORATION
Packager:       NVIDIA CORPORATION <cudatools@nvidia.com>

ExclusiveArch:  x86_64 aarch64

%global major %(echo %{version} | cut -d. -f1)

# modprobe-utils helper sources, pinned by upstream's mk/nvidia-modprobe.mk.
%global nvidia_modprobe_version 550.54.14

Source0:        https://github.com/NVIDIA/libnvidia-container/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/NVIDIA/nvidia-modprobe/archive/%{nvidia_modprobe_version}.tar.gz#/nvidia-modprobe-%{nvidia_modprobe_version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  m4
BuildRequires:  rpcgen
BuildRequires:  pkgconfig(libtirpc)
BuildRequires:  libcap-devel
BuildRequires:  libseccomp-devel
BuildRequires:  elfutils-libelf-devel
# nvcgo (the Go/cgo cgroup shim, built from src/nvcgo's vendored modules) handles
# device cgroups on cgroup v2 hosts.
BuildRequires:  golang >= 1.25
%description
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

%prep
%autosetup

mkdir -p deps/src/nvidia-modprobe-%{nvidia_modprobe_version}
tar -C deps/src/nvidia-modprobe-%{nvidia_modprobe_version} --strip-components=1 \
    -xzf %{SOURCE1} nvidia-modprobe-%{nvidia_modprobe_version}/modprobe-utils
patch -d deps/src/nvidia-modprobe-%{nvidia_modprobe_version} -p1 < mk/nvidia-modprobe.patch
touch deps/src/nvidia-modprobe-%{nvidia_modprobe_version}/.download_stamp

%build
export GOFLAGS=-mod=vendor
export CPPFLAGS="${CPPFLAGS:-} $(pkg-config --cflags libtirpc)"
export LDLIBS="$(pkg-config --libs libtirpc)"
%{__make} all \
    LIB_VERSION=%{version} \
    REVISION=v%{version} \
    WITH_LIBELF=yes

%install
export GOFLAGS=-mod=vendor
export CPPFLAGS="${CPPFLAGS:-} $(pkg-config --cflags libtirpc)"
export LDLIBS="$(pkg-config --libs libtirpc)"
DESTDIR=%{buildroot} %{__make} install \
    prefix=%{_prefix} exec_prefix=%{_exec_prefix} bindir=%{_bindir} \
    libdir=%{_libdir} includedir=%{_includedir} docdir=%{_licensedir} \
    LIB_VERSION=%{version} \
    REVISION=v%{version} \
    WITH_LIBELF=yes

vendor_dir=src/nvcgo/vendor
(cd "${vendor_dir}" && find . -type f \( -name 'LICENSE*' -o -name 'COPYING*' -o -name 'NOTICE*' -o -name 'PATENTS' \)) | while read -r f; do
    install -Dpm 0644 "${vendor_dir}/${f#./}" "%{buildroot}%{_licensedir}/%{name}%{major}/vendor/${f#./}"
done

# modprobe-utils is linked into both the shared and static library; its license
# lives only in each file's header, so extract those notices.
modprobe_utils=deps/src/nvidia-modprobe-%{nvidia_modprobe_version}/modprobe-utils
install -d %{buildroot}%{_licensedir}/%{name}%{major}/modprobe-utils
for f in nvidia-modprobe-utils.c nvidia-modprobe-utils.h pci-enum.h pci-sysfs.c pci-sysfs.h; do
    sed '/\*\//q' "${modprobe_utils}/${f}" > "%{buildroot}%{_licensedir}/%{name}%{major}/modprobe-utils/${f}.notice"
done

%package -n %{name}%{major}
Summary:        NVIDIA container runtime library
Provides:       bundled(nvidia-modprobe) = %{nvidia_modprobe_version}
%description -n %{name}%{major}
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

This package requires the NVIDIA driver (>= 340.29) to be installed separately.

%post -n %{name}%{major} -p /sbin/ldconfig
%postun -n %{name}%{major} -p /sbin/ldconfig

%files -n %{name}%{major}
%license %{_licensedir}/%{name}-%{version}
%license %{_licensedir}/%{name}%{major}
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
%license %{_licensedir}/%{name}-%{version}
%{_includedir}/*.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc

%package static
Summary:        NVIDIA container runtime library (static library)
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       libcap-devel%{?_isa}
Requires:       elfutils-libelf-devel%{?_isa}
Requires:       libseccomp-devel%{?_isa}
Requires:       libtirpc-devel%{?_isa}

%description static
The nvidia-container library provides an interface to configure GNU/Linux
containers leveraging NVIDIA hardware. The implementation relies on several
kernel subsystems and is designed to be agnostic of the container runtime.

This package requires the NVIDIA driver (>= 340.29) to be installed separately.

%files static
%license %{_licensedir}/%{name}-%{version}
%license %{_licensedir}/%{name}%{major}/modprobe-utils
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
%license %{_licensedir}/%{name}-%{version}
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
%license %{_licensedir}/%{name}-%{version}
%{_bindir}/*

%changelog
%autochangelog
