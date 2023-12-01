Summary:        WPA client
Name:           wpa_supplicant
Version:        2.10
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Communications
URL:            https://w1.fi
Source0:        https://w1.fi/releases/%{name}-%{version}.tar.gz
BuildRequires:  libnl3-devel
BuildRequires:  openssl-devel
Requires:       libnl3
Requires:       openssl

%description
WPA Supplicant is a Wi-Fi Protected Access (WPA) client and IEEE 802.1X supplicant

%prep
%autosetup -p1

%build
cat > wpa_supplicant/.config << "EOF"
CONFIG_BACKEND=file
CONFIG_CTRL_IFACE=y
CONFIG_DEBUG_FILE=y
CONFIG_DEBUG_SYSLOG=y
CONFIG_DEBUG_SYSLOG_FACILITY=LOG_DAEMON
CONFIG_DRIVER_NL80211=y
CONFIG_DRIVER_WEXT=y
CONFIG_DRIVER_WIRED=y
CONFIG_EAP_GTC=y
CONFIG_EAP_LEAP=y
CONFIG_EAP_MD5=y
CONFIG_EAP_MSCHAPV2=y
CONFIG_EAP_OTP=y
CONFIG_EAP_PEAP=y
CONFIG_EAP_TLS=y
CONFIG_EAP_TTLS=y
CONFIG_IEEE8021X_EAPOL=y
CONFIG_IPV6=y
CONFIG_LIBNL32=y
CONFIG_PEERKEY=y
CONFIG_PKCS12=y
CONFIG_READLINE=y
CFLAGS += -I/usr/include/libnl3
EOF

cd wpa_supplicant
make BINDIR=%{_sbindir} LIBDIR=%{_libdir} %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man5
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_libdir}/systemd/system
mkdir -p %{buildroot}%{_sysconfdir}/wpa_supplicant
cd wpa_supplicant
install -v -m755 wpa_{cli,passphrase,supplicant} %{buildroot}%{_sbindir}/
install -v -m644 doc/docbook/wpa_supplicant.conf.5 %{buildroot}%{_mandir}/man5/
install -v -m644 doc/docbook/wpa_{cli,passphrase,supplicant}.8 %{buildroot}%{_mandir}/man8/

cat > %{buildroot}%{_libdir}/systemd/system/wpa_supplicant@.service << "EOF"
[Unit]
Description=WPA supplicant (%{I})
BindsTo=sys-subsystem-net-devices-%{i}.device
After=sys-subsystem-net-devices-%{i}.device

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=%{_sbindir}/ip link set dev %{I} up
ExecStart=%{_sbindir}/wpa_supplicant -c %{_sysconfdir}/wpa_supplicant/wpa_supplicant-%{I}.conf -B -i %{I}
ExecStop=%{_sbindir}/ip link set dev %{I} down

[Install]
WantedBy=multi-user.target
EOF

cat > %{buildroot}%{_sysconfdir}/wpa_supplicant/wpa_supplicant-wlan0.conf << "EOF"
ctrl_interface=/run/wpa_supplicant
update_config=1

# Add network= entry below
EOF

%files
%defattr(-,root,root)
%license COPYING
%{_sbindir}/wpa_cli
%{_sbindir}/wpa_passphrase
%{_sbindir}/wpa_supplicant
%{_mandir}/*
%{_libdir}/systemd/system/wpa_supplicant@.service
%{_sysconfdir}/wpa_supplicant/wpa_supplicant-wlan0.conf

%changelog
* Wed Jan 26 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.10-1
- Upgrade to v2.10 to resolve CVE-2022-23303 and CVE-2022-23304.
- License verified.

* Fri Apr 09 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.9-4
- Add patch for CVE-2021-30004

* Mon Mar 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.9-3
- Add patch for CVE-2021-0326 and CVE-2021-27803

* Mon Nov 16 2020 Nicolas Guibourge <nicolasg@microsoft.com> - 2.9-2
- Change name of CVE-2019-16275 patch.

* Thu May 14 2020 Henry Beberman <hebeberm@microsoft.com> - 2.9-1
- Update version to 2.9.
- Add patch for CVE-2019-16275.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.7-4
- Added %%license line automatically

* Fri Apr 17 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.7-3
- Rename libnl to libnl3.
- Remove sha1 macro.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.7-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Jan 3 2019 Michelle Wang <michellew@vmware.com> - 2.7-1
- Update version to 2.7.

* Fri Aug 17 2018 Alexey Makhalov <amakhalov@vmware.com> - 2.6-2
- Improve .service file: wait wlanX to appear, run daemon in background.
- Added skeleton for wlan0 conf file.

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.6-1
- Initial build. First version.
