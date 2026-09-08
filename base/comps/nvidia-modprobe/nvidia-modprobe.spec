Name:           nvidia-modprobe
Version:        610.57.04
Release:        1%{?dist}
Summary:        NVIDIA kernel module loader
License:        GPLv2+
URL:            http://www.nvidia.com/object/unix.html
Vendor:         NVIDIA
Packager:       NVIDIA

ExclusiveArch:  %{ix86} x86_64 aarch64

Source0:        https://download.nvidia.com/XFree86/%{name}/%{name}-%{version}.tar.bz2
Patch0:         %{name}-man-page-permissions.patch

BuildRequires:  gcc
BuildRequires:  m4
BuildRequires:  make

%description
This utility is used by user-space NVIDIA driver components to make sure the
NVIDIA kernel modules are loaded and that the NVIDIA character device files are
present.

%prep
%autosetup -p1
# Remove additional CFLAGS added when enabling DEBUG
sed -i '/+= -O0 -g/d' utils.mk

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{?__global_ldflags}"
make %{?_smp_mflags} \
    DEBUG=1 \
    NV_VERBOSE=1 \
    PREFIX=%{_prefix} \
    STRIP_CMD=true

%install
%make_install \
    NV_VERBOSE=1 \
    PREFIX=%{_prefix} \
    STRIP_CMD=true

%files
%license COPYING
%attr(4755, root, root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*

%changelog
