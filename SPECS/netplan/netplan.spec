# Ubuntu calls their own software netplan.io in the archive due to name conflicts
%global ubuntu_name netplan.io

# If the definition isn't available for python3_pkgversion, define it
%global python3_pkgversion 3

# If this isn't defined, define it
%{?!_systemdgeneratordir:%global _systemdgeneratordir /usr/lib/systemd/system-generators}

# Netplan library soversion major
%global libsomajor 0.0

# Force auto-byte-compilation to Python 3
%global __python %{__python3}


Name:           netplan
Version:        0.107.1
Release:        1%{?dist}
Summary:        Network configuration tool using YAML
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        GPLv3
URL:            https://netplan.io/
# Source0:      https://github.com/canonical/%{name}/archive/%{version}/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:         remove-flakes-check.patch

BuildRequires:  gcc
# BuildRequires:  make
BuildRequires:  meson >= 0.61
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  bash-completion-devel
BuildRequires:  libgcc-devel
BuildRequires:  bash-devel
BuildRequires:  systemd
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  glib-devel
BuildRequires:  libyaml-devel
BuildRequires:  util-linux-devel
BuildRequires:  python%{python3_pkgversion}-devel
# For tests
BuildRequires:  iproute
BuildRequires:  libcmocka-devel
BuildRequires:  python%{python3_pkgversion}-cffi
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-coverage
BuildRequires:  python%{python3_pkgversion}-netifaces
BuildRequires:  python%{python3_pkgversion}-pycodestyle
BuildRequires:  python%{python3_pkgversion}-PyYAML

# /usr/sbin/netplan is a Python 3 script that requires netifaces and PyYAML
Requires:       python%{python3_pkgversion}-netifaces
Requires:       python%{python3_pkgversion}-PyYAML
# Requires:       python3dist(rich) # TBD!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 'ip' command is used in netplan apply subcommand
Requires:       iproute
# netplan ships dbus files
Requires:       dbus

# Netplan requires a backend for configuration
Requires:       %{name}-default-backend

# Netplan requires its core libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

# Provide the package name that Ubuntu uses for it too...
Provides:       %{ubuntu_name} = %{version}-%{release}
Provides:       %{ubuntu_name}%{?_isa} = %{version}-%{release}

%description
netplan reads network configuration from /etc/netplan/*.yaml which are written by administrators,
installers, cloud image instantiations, or other OS deployments. During early boot, it generates
backend specific configuration files in /run to hand off control of devices to a particular
networking daemon.

Currently supported backends are systemd-networkd and NetworkManager.

%files
%license COPYING
%doc %{_docdir}/%{name}/
%{_sbindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/dbus-1/system-services/io.netplan.Netplan.service
%{_datadir}/dbus-1/system.d/io.netplan.Netplan.conf
%{_systemdgeneratordir}/%{name}
# %{_mandir}/man5/%{name}.5*
# %{_mandir}/man8/%{name}*.8*
%dir %{_sysconfdir}/%{name}
%dir %{_prefix}/lib/%{name}
%{_libexecdir}/%{name}/
%{_datadir}/bash-completion/completions/%{name}
%{python3_sitelib}/%{name}/
%{python3_sitearch}/%{name}/

# ------------------------------------------------------------------------------------------------

%package libs
Summary:        Network configuration tool using YAML (core library)
Group:          System Environment/Libraries

%description libs
netplan reads network configuration from /etc/netplan/*.yaml which are written by administrators,
installers, cloud image instantiations, or other OS deployments. During early boot, it generates
backend specific configuration files in /run to hand off control of devices to a particular
networking daemon.

This package provides Netplan's core libraries.

%files libs
%license COPYING
%{_libdir}/libnetplan.so.%{libsomajor}{,.*}

# ------------------------------------------------------------------------------------------------

%package devel
Summary:        Network configuration tool using YAML (development files)
Group:          Development/Libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
netplan reads network configuration from /etc/netplan/*.yaml which are written by administrators,
installers, cloud image instantiations, or other OS deployments. During early boot, it generates
backend specific configuration files in /run to hand off control of devices to a particular
networking daemon.

This package provides development headers and libraries for building applications using Netplan.

%files devel
%{_includedir}/%{name}/
%{_libdir}/libnetplan.so
%{_libdir}/pkgconfig/%{name}.pc

# ------------------------------------------------------------------------------------------------

%package default-backend-networkd
Summary:        Network configuration tool using YAML (systemd-networkd backend)
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}
# Netplan requires systemd-networkd for configuration
Requires:       systemd-networkd

# Generally, if linux-firmware is installed, we want Wi-Fi capabilities
Recommends:     (wpa_supplicant if linux-firmware)
Suggests:       wpa_supplicant

# One and only one default backend permitted
Conflicts:      %{name}-default-backend
Provides:       %{name}-default-backend

BuildArch:      noarch

%description default-backend-networkd
netplan reads network configuration from /etc/netplan/*.yaml which are written by administrators,
installers, cloud image instantiations, or other OS deployments. During early boot, it generates
backend specific configuration files in /run to hand off control of devices to a particular
networking daemon.

This package configures Netplan to use systemd-networkd as its backend.

%files default-backend-networkd
%{_prefix}/lib/%{name}/00-netplan-default-renderer-networkd.yaml

# ------------------------------------------------------------------------------------------------

%prep

%autosetup -p1

# Drop -Werror to avoid the following error:
# /usr/include/glib-2.0/glib/glib-autocleanups.h:28:3: error: 'ip_str' may be used uninitialized in this function [-Werror=maybe-uninitialized]
sed -e "s/werror=true/werror=false/g" -i meson.build

# # Do not use Pandoc to format documentation
# sed -e "s/pandoc/echo pandoc/g" -i Makefile
cp doc/netplan.md doc/netplan.5
cp doc/netplan.md doc/netplan.html
# # No man8 files only man5 files are generated 
# sed -e "s/*.8/*.5/g" -i Makefile
# sed -e "s/man8/man5/g" -i Makefile

%build

# python3-coverage provides /usr/bin/coverage3, but the meson config expects it to be called coverage-3
if [ ! -e /usr/bin/coverage-3 ]; then
    ln -s /usr/bin/coverage3 /usr/bin/coverage-3
fi

%meson
%meson_build


%install

%meson_install

# Remove useless "compat" symlink and path
rm -f %{buildroot}/lib/netplan/generate
rmdir %{buildroot}/lib/netplan
rmdir %{buildroot}/lib

# Remove superfluous __pycache__
rm -rf %{buildroot}/usr/lib/python3.11/site-packages/netplan/__pycache__

# Pre-create the config directories
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_prefix}/lib/%{name}

cat > %{buildroot}%{_prefix}/lib/%{name}/00-netplan-default-renderer-networkd.yaml <<EOF
network:
  renderer: networkd
EOF

%changelog
* Thu Feb 15 2024 Francisco Huelsz prince <frhuelsz@microsoft.com> - 0.107.1-1
- Upgrade to 0.107.1

* Fri Sep 17 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.95-1
- Initial CBL-Mariner import from Netplan source (license: GPLv3)
- License verified
- Update netplan to Netplan

* Fri Dec 14 2018 Mathieu Trudel-Lapierre <mathieu.trudel-lapierre@canonical.com> - 0.95
- Update to 0.95

* Sat Oct 13 2018 Neal Gompa <ngompa13@gmail.com> - 0.40.3-0
- Rebase to 0.40.3

* Tue Mar 13 2018 Neal Gompa <ngompa13@gmail.com> - 0.34-0.1
- Update to 0.34

* Wed Mar  7 2018 Neal Gompa <ngompa13@gmail.com> - 0.33-0.1
- Rebase to 0.33

* Sat Nov  4 2017 Neal Gompa <ngompa13@gmail.com> - 0.30-1
- Rebase to 0.30

* Sun Jul  2 2017 Neal Gompa <ngompa13@gmail.com> - 0.23~17.04.1-1
- Initial packaging
