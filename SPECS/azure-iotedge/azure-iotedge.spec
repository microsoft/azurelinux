
%define iotedge_user iotedge
%define iotedge_group %{iotedge_user}
%define iotedge_home %{_localstatedir}/lib/iotedge
%define iotedge_logdir %{_localstatedir}/log/aziot/edged
%define iotedge_datadir %{_datadir}/iotedge
%define iotedge_socketdir %{_localstatedir}/lib/iotedge
%define aziot_confdir %{_sysconfdir}/aziot
%define iotedge_confdir %{aziot_confdir}/edged

# Needs to be kept in-sync with the current version of 'rust' provided by Mariner.
%global rust_build_version 1.59.0

Summary:        Azure IoT Edge Security Daemon
Name:           azure-iotedge
Version:        1.2.8
Release:        1%{?dist}

# A buildable azure-iotedge environments needs functioning submodules that do not work from the archive download
# To recreate the tar.gz run the following
#  sudo git clone https://github.com/Azure/iotedge.git -b %%{version}
#  pushd iotedge
#  sudo git submodule update --init --recursive
#  popd
#  sudo mv iotedge azure-iotedge-%%{version}
#  sudo tar --sort=name --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime
#           -cvf azure-iotedge-%%{version}.tar.gz azure-iotedge-%%{version}
Source0:        https://github.com/Azure/iotedge/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-cargo.tar.gz
Patch0:         rust-1.59.0-fix.patch
License:        MIT
Group:          Applications/File
URL:            https://github.com/azure/iotedge
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  rust = %{rust_build_version}
BuildRequires:  cmake
BuildRequires:  curl
BuildRequires:  git
BuildRequires:  shadow-utils
BuildRequires:  systemd

Requires(pre):  shadow-utils

Requires:       libiothsm-std
Requires:       openssl
Requires:       moby-engine
Requires:       moby-cli

%description
Azure IoT Edge Security Daemon
Azure IoT Edge is a fully managed service that delivers cloud intelligence
locally by deploying and running artificial intelligence (AI), Azure services,
and custom logic directly on cross-platform IoT devices. Run your IoT solution
securely and at scale whether in the cloud or offline.

This package contains the IoT Edge daemon and CLI tool

%global debug_package %{nil}

%prep
# Setup .cargo directory
mkdir -p $HOME
pushd $HOME
tar xf %{SOURCE1} --no-same-owner
popd
%setup -q -n %{_topdir}/BUILD/azure-iotedge-%{version}/edgelet
%patch0 -p1

%build
echo "%{rust_build_version}" > rust-toolchain

# Remove FORTIFY_SOURCE from CFLAGS to fix compilation error
CFLAGS="`echo " %{build_cflags} " | sed 's/ -Wp,-D_FORTIFY_SOURCE=2//'`"
export CFLAGS

%make_build \
    CONNECT_MANAGEMENT_URI=unix://%{iotedge_socketdir}/mgmt.sock \
    CONNECT_WORKLOAD_URI=unix://%{iotedge_socketdir}/workload.sock \
    LISTEN_MANAGEMENT_URI=unix://%{iotedge_socketdir}/mgmt.sock \
    LISTEN_WORKLOAD_URI=unix://%{iotedge_socketdir}/workload.sock \
    release

%install
IOTEDGE_HOST=unix:///var/lib/iotedge/mgmt.sock
export IOTEDGE_HOST

export PATH=$PATH:/root/.cargo/bin/
make %{?_smp_mflags} \
    CONNECT_MANAGEMENT_URI=unix://%{iotedge_socketdir}/mgmt.sock \
    CONNECT_WORKLOAD_URI=unix://%{iotedge_socketdir}/workload.sock \
    LISTEN_MANAGEMENT_URI=unix://%{iotedge_socketdir}/mgmt.sock \
    LISTEN_WORKLOAD_URI=unix://%{iotedge_socketdir}/workload.sock \
    DESTDIR=$RPM_BUILD_ROOT \
    unitdir=%{_unitdir} \
    docdir=%{_docdir}/%{name} \
    install

install -D contrib/centos/00-aziot-edged.preset %{buildroot}%{_presetdir}/00-aziot-edged.preset

%pre
# Check for container runtime
if ! /usr/bin/getent group docker >/dev/null; then
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo ""
    echo " ERROR: No container runtime detected."
    echo ""
    echo " Please install a container runtime and run this install again."
    echo ""
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

    exit 1
fi

# Create iotedge group
if ! /usr/bin/getent group iotedge >/dev/null; then
    %{_sbindir}/groupadd -r %{iotedge_group}
fi

# Create iotedge user
if ! /usr/bin/getent passwd iotedge >/dev/null; then
    %{_sbindir}/useradd -r -g %{iotedge_group} -c "iotedge user" -s /bin/nologin -d %{iotedge_home} %{iotedge_user}
fi

# Add iotedge user to moby-engine group
if /usr/bin/getent group docker >/dev/null; then
    %{_sbindir}/usermod -aG docker %{iotedge_user}
fi

# Add iotedge user to systemd-journal group so it can get system logs
if /usr/bin/getent group systemd-journal >/dev/null; then
    %{_sbindir}/usermod -aG systemd-journal %{iotedge_user}
fi

# Add iotedge user to aziot-identity-service groups
if /usr/bin/getent group aziotcs >/dev/null; then
    %{_sbindir}/usermod -aG aziotcs %{iotedge_user}
fi
if /usr/bin/getent group aziotks >/dev/null; then
    %{_sbindir}/usermod -aG aziotks %{iotedge_user}
fi
if /usr/bin/getent group aziotid >/dev/null; then
    %{_sbindir}/usermod -aG aziotid %{iotedge_user}
fi
exit 0

%post
if [ ! -f '/etc/aziot/config.toml' ]; then
    echo "==============================================================================="
    echo ""
    echo "                              Azure IoT Edge"
    echo ""
    echo "  IMPORTANT: Please configure the device with provisioning information."
    echo ""

    if [ -f '/etc/iotedge/config.yaml' ]; then
        echo "  Detected /etc/iotedge/config.yaml from a previously installed version of IoT Edge."
        echo "  You can import the previous configuration using:"
        echo ""
        echo "    iotedge config import"
        echo ""
        echo "Alternatively, copy the configuration file at /etc/aziot/config.toml.edge.template to /etc/aziot/config.toml,"
    else
        echo "Copy the configuration file at /etc/aziot/config.toml.edge.template to /etc/aziot/config.toml,"
    fi

    echo "  update it with your device information, then apply your configuration changes with:"
    echo ""
    echo "    iotedge config apply"
    echo ""
    echo "  You may need to run iotedge config commands with sudo, depending on your environment."
    echo ""
    echo "==============================================================================="
fi
%systemd_post aziot-edged.service

%preun
%systemd_preun aziot-edged.service

%postun
%systemd_postun_with_restart aziot-edged.service

%files
%defattr(-, root, root, -)
%license ../LICENSE

# bins
%{_bindir}/iotedge
%{_libexecdir}/aziot/aziot-edged

# config
%attr(600, root, root) %{aziot_confdir}/config.toml.edge.template
%attr(400, %{iotedge_user}, %{iotedge_group}) %{iotedge_confdir}/config.toml.default
%attr(700, %{iotedge_user}, %{iotedge_group}) %dir %{iotedge_confdir}/config.d
%config(noreplace) %{_sysconfdir}/logrotate.d/aziot-edge

# man
%{_mandir}/man1/iotedge.1.gz
%{_mandir}/man8/aziot-edged.8.gz

# systemd
%{_unitdir}/aziot-edged.service
/usr/lib/systemd/system-preset/00-aziot-edged.preset

# sockets
%attr(660, %{iotedge_user}, %{iotedge_group}) %{iotedge_socketdir}/mgmt.sock
%attr(666, %{iotedge_user}, %{iotedge_group}) %{iotedge_socketdir}/workload.sock

# dirs
%attr(-, %{iotedge_user}, %{iotedge_group}) %dir %{iotedge_home}
%attr(-, %{iotedge_user}, %{iotedge_group}) %dir %{iotedge_logdir}
%attr(-, %{iotedge_user}, %{iotedge_group}) %dir %{iotedge_socketdir}

%doc %{_docdir}/%{name}/LICENSE.gz
%doc %{_docdir}/%{name}/ThirdPartyNotices.gz
%doc %{_docdir}/%{name}/trademark

%changelog
* Tue Mar 08 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.8-1
- Updating to version 1.2.8.
- Using 'rust' version 1.59.0

* Fri Nov 19 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.2-2
- Adding a fix to work with newer version of cmake.

* Fri May 14 2021 Andrew Phelps <anphel@microsoft.com> - 1.1.2-1
- Update to version 1.1.2

* Mon Apr 26 2021 Thomas Crain <thcrain@microsoft.com> - 1.1.0-4
- Bump release to rebuild with rust 1.47.0-3 (security update)

* Tue Apr 20 2021 Thomas Crain <thcrain@microsoft.com> - 1.1.0-3
- Bump release to rebuild with rust 1.47.0-2 (security update)

* Fri Apr 09 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.0-2
- Fixing a 'BuildRequires' typo from "==" to "=".

* Tue Feb 23 2021 Andrew Phelps <anphel@microsoft.com> - 1.1.0-1
- Update to version 1.1.0

* Sun May 31 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0.9.1-2
- Disable FORTIFY_SOURCE=2 to fix compilation error with hardened defaults.

* Wed May 27 2020 Andrew Phelps <anphel@microsoft.com> - 1.0.9.1-1
- Update to version 1.0.9.1. Fix tarball build notes.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0.9-8
- Added %%license line automatically

* Thu May 07 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 1.0.9-7
- Fix docker based build issue.

* Wed May 06 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.0.9-6
- Rename shadow to shadow-utils.

* Tue May 05 2020 Mohan Datla <mdatla@microsoft.com> - 1.0.9-5
- Add moby-engine and moby-cli dependencies

* Wed Apr 29 2020 Mohan Datla <mdatla@microsoft.com> - 1.0.9-4
- Removed dependency on docker.

* Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.9-3
- Fixed 'Source0' tag.

* Mon Apr 20 2020 Andrew Phelps <anphel@microsoft.com> - 1.0.9-2
- Support building offline with prepopulated .cargo directory.

* Thu Mar 19 2020 Henry Beberman <henry.beberman@microsoft.com> - 1.0.9-1
- Update to 1.0.9. License verified.

* Tue Dec 3 2019 Henry Beberman <hebeberm@microsoft.com> - 1.0.8.4-1
- Original version for CBL-Mariner.
