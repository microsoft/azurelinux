# Ubuntu calls their own software netplan.io in the archive due to name conflicts
%global ubuntu_name netplan.io

# If the definition isn't available for python3_pkgversion, define it
%global python3_pkgversion 3

# If this isn't defined, define it
%{?!_systemdgeneratordir:%global _systemdgeneratordir /usr/lib/systemd/system-generators}

# Force auto-byte-compilation to Python 3
%global __python %{__python3}


Name:           netplan
Version:        0.105
Release:        1%{?dist}
Summary:        Network configuration tool using YAML
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
License:        GPLv3
URL:            https://netplan.io/
# Source0:      https://github.com/canonical/%{name}/archive/%{version}/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(yaml-0.1)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  systemd-rpm-macros
# For tests
BuildRequires:  python%{python3_pkgversion}-coverage
BuildRequires:  python%{python3_pkgversion}-netifaces
BuildRequires:  python%{python3_pkgversion}-pycodestyle
BuildRequires:  python%{python3_pkgversion}-PyYAML

# /usr/sbin/netplan is a Python 3 script that requires netifaces and PyYAML
Requires:       python%{python3_pkgversion}-netifaces
Requires:       python%{python3_pkgversion}-PyYAML
# 'ip' command is used in netplan apply subcommand
Requires:       iproute

# Provide the package name that Ubuntu uses for it too...
Provides:       %{ubuntu_name} = %{version}-%{release}
Provides:       %{ubuntu_name}%{?_isa} = %{version}-%{release}

%description
netplan reads network configuration from /etc/netplan/*.yaml which are written by administrators,
installers, cloud image instantiations, or other OS deployments. During early boot, it generates
backend specific configuration files in /run to hand off control of devices to a particular
networking daemon.

Currently supported backends are systemd-networkd and NetworkManager.


%prep
%autosetup -p1

# Drop -Werror to avoid the following error:
# /usr/include/glib-2.0/glib/glib-autocleanups.h:28:3: error: 'ip_str' may be used uninitialized in this function [-Werror=maybe-uninitialized]
sed -e "s/-Werror//g" -i Makefile
# Do not use Pandoc to format documentation
sed -e "s/pandoc/echo pandoc/g" -i Makefile
cp doc/netplan.md doc/netplan.5
cp doc/netplan.md doc/netplan.html
# No man8 files only man5 files are generated 
sed -e "s/*.8/*.5/g" -i Makefile
sed -e "s/man8/man5/g" -i Makefile

%build
%make_build CFLAGS="%{optflags}"

%install
%make_install ROOTPREFIX=%{_prefix} LIBDIR=%{_libdir} LIBEXECDIR=%{_libexecdir}

# Pre-create the config directory
mkdir -p %{buildroot}%{_sysconfdir}/%{name}

# Generate Netplan default renderer configuration
cat > %{buildroot}%{_prefix}/lib/%{name}/00-netplan-default-renderer-networkd.yaml <<EOF
network:
  renderer: networkd
EOF

%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%check
make check

%files
%license COPYING
%doc %{_docdir}/%{name}/
%{_sbindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/dbus-1/system-services/io.netplan.Netplan.service
%{_datadir}/dbus-1/system.d/io.netplan.Netplan.conf
%{_systemdgeneratordir}/%{name}
%{_mandir}/man5/%{name}.5*
%dir %{_sysconfdir}/%{name}
%{_prefix}/lib/%{name}/
%{_datadir}/bash-completion/completions/%{name}
%{_includedir}/%{name}/
%{_libdir}/libnetplan.so
%{_libdir}/libnetplan.so.*


%changelog
* Thu Aug 18 2022 Lukas Märdian <slyon@ubuntu.com> - 0.105-0
- Update to 0.105

* Sun Feb 20 2022 Neal Gompa <ngompa13@gmail.com> - 0.104-0
- Update to 0.104
- Resync with Fedora spec

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