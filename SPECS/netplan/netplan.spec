# Ubuntu calls their own software netplan.io in the archive due to name conflicts
%global ubuntu_name netplan.io

# If the definition isn't available for python3_pkgversion, define it
%global python3_pkgversion 3

# If this isn't defined, define it
%{?!_systemdgeneratordir:%global _systemdgeneratordir /usr/lib/systemd/system-generators}

# Netplan library soversion major
%global libsomajor 1


Name:           netplan
Version:        1.0
Release:        1%{?dist}
Summary:        Network configuration tool using YAML
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        GPLv3
URL:            https://netplan.io/
Source0:        https://github.com/canonical/%{name}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Fix bug in netplan when python3-rich is not present.
Patch2:         rich-import-failure-no-log.patch

# Temporarily disabling broken test suite due to version mismatches between
# pytest-cov and python3-coverage in 3.0.
Patch3:         disable-broken-tests.patch

BuildRequires:  bash-completion-devel
BuildRequires:  bash-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  libgcc-devel
BuildRequires:  libyaml-devel
BuildRequires:  meson >= 0.61
BuildRequires:  ninja-build
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  systemd
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  util-linux-devel
BuildRequires:  python%{python3_pkgversion}-pyflakes

# BuildRequires below are only required for %check:
BuildRequires:  iproute
BuildRequires:  libcmocka-devel
BuildRequires:  openvswitch
BuildRequires:  python%{python3_pkgversion}-cffi
BuildRequires:  python%{python3_pkgversion}-coverage
BuildRequires:  python%{python3_pkgversion}-netifaces
BuildRequires:  python%{python3_pkgversion}-pycodestyle
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pytest-cov
BuildRequires:  python%{python3_pkgversion}-PyYAML

# netplan ships dbus files and imports the dbus python module
Requires:       dbus
Requires:       python%{python3_pkgversion}-dbus

# 'ip' command is used in netplan apply subcommand
Requires:       iproute

# /usr/sbin/netplan is a Python 3 script that imports the following:
Requires:       python%{python3_pkgversion}-netifaces
Requires:       python%{python3_pkgversion}-PyYAML
Requires:       python%{python3_pkgversion}-cffi
# Disabled: python-rich is not available on 3.0 yet. This is an optional
# dependency used to improve the CLI output, but is not required for core
# functionality. Should be enabled once the dependency is satisfied.
# Requires:       python%{python3_pkgversion}-rich

# Netplan requires a backend for configuration
Requires:       %{name}-default-backend

# Netplan requires its core libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

# Provide the package name that Ubuntu uses for it too...
Provides:       %{ubuntu_name} = %{version}-%{release}
Provides:       %{ubuntu_name}%{?_isa} = %{version}-%{release}

%description
netplan reads network configuration from /etc/netplan/*.yaml which are written
by administrators, installers, cloud image instantiations, or other OS deployments.
During early boot, it generates backend specific configuration files in /run to
hand off control of devices to a particular networking daemon.

Currently supported backends are systemd-networkd and NetworkManager.

%files
%license COPYING
%doc %{_docdir}/%{name}/
%{_sbindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/dbus-1/system-services/io.netplan.Netplan.service
%{_datadir}/dbus-1/system.d/io.netplan.Netplan.conf
%{_systemdgeneratordir}/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_prefix}/lib/%{name}
%{_libexecdir}/%{name}/
%{_datadir}/bash-completion/completions/%{name}

# Check if sitearch and archlib are different to avoid "File listed twice"
# warning.
%if "%{python3_sitelib}" == "%{python3_sitearch}"
%{python3_sitelib}/%{name}/
%else
%{python3_sitelib}/%{name}/
%{python3_sitearch}/%{name}/
%endif

# ------------------------------------------------------------------------------------------------

%package libs
Summary:        Network configuration tool using YAML (core library)
Group:          System Environment/Libraries

%description libs
netplan reads network configuration from /etc/netplan/*.yaml which are written
by administrators, installers, cloud image instantiations, or other OS deployments.
During early boot, it generates backend specific configuration files in /run to
hand off control of devices to a particular networking daemon.

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
netplan reads network configuration from /etc/netplan/*.yaml which are written
by administrators, installers, cloud image instantiations, or other OS deployments.
During early boot, it generates backend specific configuration files in /run to
hand off control of devices to a particular networking daemon.

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

# Wireless configuration through netplan requires using wpa_supplicant
Suggests:       wpa_supplicant

# One and only one default backend permitted
Conflicts:      %{name}-default-backend
Provides:       %{name}-default-backend

BuildArch:      noarch

%description default-backend-networkd
netplan reads network configuration from /etc/netplan/*.yaml which are written
by administrators, installers, cloud image instantiations, or other OS deployments.
During early boot, it generates backend specific configuration files in /run to
hand off control of devices to a particular networking daemon.

This package configures Netplan to use systemd-networkd as its backend.

%files default-backend-networkd
%{_prefix}/lib/%{name}/00-netplan-default-renderer-networkd.yaml

# ------------------------------------------------------------------------------------------------

%prep

%autosetup -p1

# Drop -Werror to avoid the following error:
# /usr/include/glib-2.0/glib/glib-autocleanups.h:28:3: error: 'ip_str' may be used uninitialized in this function [-Werror=maybe-uninitialized]
sed -e "s/werror=true/werror=false/g" -i meson.build

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

# Remove __pycache__
rm -rf %{buildroot}%{python3_sitelib}/%{name}/__pycache__

# Pre-create the config directories
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_prefix}/lib/%{name}

# Create the default renderer configuration for networkd
cat > %{buildroot}%{_prefix}/lib/%{name}/00-netplan-default-renderer-networkd.yaml <<EOF
network:
  renderer: networkd
EOF

# Make netplan configuration only accessible by root.
chmod 600 %{buildroot}%{_prefix}/lib/%{name}/00-netplan-default-renderer-networkd.yaml

%check
%meson_test

%changelog
* Fri Mar 29 2024 Francisco Huelsz prince <frhuelsz@microsoft.com> - 1.0-1
- Upgrade to 1.0

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
