Name:           nvidia-persistenced
Version:        610.57.04
Release:        1%{?dist}
Summary:        A daemon to maintain persistent software state in the NVIDIA driver
License:        MIT
URL:            http://www.nvidia.com/object/unix.html
Vendor:         NVIDIA
Packager:       NVIDIA

ExclusiveArch:  %{ix86} x86_64 aarch64

Source0:        https://download.nvidia.com/XFree86/%{name}/%{name}-%{version}.tar.bz2
Source1:        %{name}.service

BuildRequires:  gcc
BuildRequires:  libtirpc-devel
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  systemd-devel

Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
# dlopened: libnvidia-cfg
Requires:           nvidia-driver-common%{?_isa} >= %{version}

%description
The %{name} utility is used to enable persistent software state in the NVIDIA
driver. When persistence mode is enabled, the daemon prevents the driver from
releasing device state when the device is not in use. This can improve the
startup time of new clients in this scenario.

%prep
%autosetup
# Remove additional CFLAGS added when enabling DEBUG
sed -i -e '/+= -O0 -g/d' utils.mk

%build
export CFLAGS="%{optflags} -I%{_includedir}/tirpc"
%make_build \
    DEBUG=1 \
    LIBS="-ldl -ltirpc" \
    NV_VERBOSE=1 \
    PREFIX=%{_prefix} \
    STRIP_CMD=true

%install
%make_install \
    NV_VERBOSE=1 \
    PREFIX=%{_prefix} \
    STRIP_CMD=true

# Systemd unit files
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d /var/run/%{name} -s /sbin/nologin \
    -c "NVIDIA Persistence Daemon" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{_unitdir}/%{name}.service

%changelog
