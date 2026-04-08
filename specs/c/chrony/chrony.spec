# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _hardened_build 1
%global clknetsim_ver 6ee99f50dec8
%bcond_without debug
%bcond_without nts

%ifarch %{ix86} x86_64 %{arm} aarch64 mipsel mips64el ppc64 ppc64le s390 s390x
%bcond_without seccomp
%endif

Name:           chrony
Version:        4.8
Release:        3%{?dist}
Summary:        An NTP client/server

License:        GPL-2.0-only
URL:            https://chrony-project.org
Source0:        https://chrony-project.org/releases/chrony-%{version}%{?prerelease}.tar.gz
Source1:        https://chrony-project.org/releases/chrony-%{version}%{?prerelease}-tar-gz-asc.txt
Source2:        https://chrony-project.org/gpgkey-8F375C7E8D0EE125A3D3BD51537E2B76F7680DAC.asc
Source3:        chrony.dhclient
Source4:        chrony.sysusers
# simulator for test suite
Source10:       https://gitlab.com/chrony/clknetsim/-/archive/master/clknetsim-%{clknetsim_ver}.tar.gz
%{?gitpatch:Patch0: chrony-%{version}%{?prerelease}-%{gitpatch}.patch.gz}

# add distribution-specific bits to DHCP dispatcher
Patch1:         chrony-nm-dispatcher-dhcp.patch
# let systemd create /var/lib/chrony and /var/log/chrony
Patch2:         chrony-servicedirs.patch
# update seccomp filter for new glibc
Patch3:         chrony-seccomp.patch

BuildRequires:  libcap-devel libedit-devel nettle-devel pps-tools-devel
BuildRequires:  gcc gcc-c++ make bison systemd gnupg2
%{?with_nts:BuildRequires: gnutls-devel gnutls-utils}
%{?with_seccomp:BuildRequires: libseccomp-devel}

%{?systemd_requires}
%{?sysusers_requires_compat}

# Needed by the leapseclist directive in default chrony.conf
Requires:       tzdata

# suggest drivers for hardware reference clocks
Suggests:       ntp-refclock

%description
chrony is a versatile implementation of the Network Time Protocol (NTP).
It can synchronise the system clock with NTP servers, reference clocks
(e.g. GPS receiver), and manual input using wristwatch and keyboard. It
can also operate as an NTPv4 (RFC 5905) server and peer to provide a time
service to other computers in the network.

%if 0%{!?vendorzone:1}
%global vendorzone %(source /etc/os-release && echo ${ID}.)
%endif

%prep
%{gpgverify} --keyring=%{SOURCE2} --signature=%{SOURCE1} --data=%{SOURCE0}
%setup -q -n %{name}-%{version}%{?prerelease} -a 10
%{?gitpatch:%patch -P 0 -p1}
%patch -P 1 -p1 -b .nm-dispatcher-dhcp
%patch -P 2 -p1 -b .servicedirs
%patch -P 3 -p1 -b .seccomp

%{?gitpatch: echo %{version}-%{gitpatch} > version.txt}

# review changes in packaged configuration files and scripts
md5sum -c <<-EOF | (! grep -v 'OK$')
        5530d6e60f84b76c27495485d2510bac  examples/chrony-wait.service
        3f2ddca6065c3e8f4565d7422739795a  examples/chrony.conf.example2
        6a3178c4670de7de393d9365e2793740  examples/chrony.logrotate
        c3992e2f985550739cd1cd95f98c9548  examples/chrony.nm-dispatcher.dhcp
        4e85d36595727318535af3387411070c  examples/chrony.nm-dispatcher.onoffline
        607c82f56639486f52c31105632909eb  examples/chronyd.service
        5ddbb8a8055f587cb6b0b462ca73ea46  examples/chronyd-restricted.service
EOF

# don't allow packaging without vendor zone
test -n "%{vendorzone}"

# use example chrony.conf as the default config with some modifications:
# - use our vendor zone (2.*pool.ntp.org names include IPv6 addresses)
# - enable leapseclist to get TAI-UTC offset and leap seconds
# - use NTP servers from DHCP
sed -e 's|^\(pool \)\(pool.ntp.org\)|\12.%{vendorzone}\2|' \
    -e 's|#\(leapseclist\)|\1|' \
    -e 's|^pool.*pool.ntp.org.*|&\n\n# Use NTP servers from DHCP.\nsourcedir /run/chrony-dhcp|' \
        < examples/chrony.conf.example2 > chrony.conf

touch -r examples/chrony.conf.example2 chrony.conf

# set selinux context in chronyd-restricted service
sed -i '/^ExecStart/a SELinuxContext=system_u:system_r:chronyd_restricted_t:s0' \
	examples/chronyd-restricted.service

# regenerate the file from getdate.y
rm -f getdate.c

mv clknetsim-*-%{clknetsim_ver}* test/simulation/clknetsim

%build
%configure \
%{?with_debug: --enable-debug} \
        --enable-ntp-signd \
%{?with_seccomp: --enable-scfilter} \
%{!?with_nts: --disable-nts} \
        --chronyrundir=/run/chrony \
        --docdir=%{_docdir} \
        --with-ntp-era=$(date -d '1970-01-01 00:00:00+00:00' +'%s') \
        --with-chronyc-user=chrony \
        --with-user=chrony \
        --with-hwclockfile=%{_sysconfdir}/adjtime \
        --with-pidfile=/run/chrony/chronyd.pid \
        --with-sendmail=%{_sbindir}/sendmail
%make_build

%install
%make_install

rm -rf $RPM_BUILD_ROOT%{_docdir}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,logrotate.d}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/{lib,log}/chrony
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dhcp/dhclient.d
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
mkdir -p $RPM_BUILD_ROOT%{_sysusersdir}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/NetworkManager/dispatcher.d
mkdir -p $RPM_BUILD_ROOT{%{_unitdir},%{_prefix}/lib/systemd/ntp-units.d}

install -m 644 -p chrony.conf $RPM_BUILD_ROOT%{_sysconfdir}/chrony.conf

install -m 755 -p %{SOURCE3} \
        $RPM_BUILD_ROOT%{_sysconfdir}/dhcp/dhclient.d/chrony.sh
install -m 644 -p examples/chrony.logrotate \
        $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/chrony

install -m 644 -p examples/chronyd.service \
        $RPM_BUILD_ROOT%{_unitdir}/chronyd.service
install -m 644 -p examples/chronyd-restricted.service \
        $RPM_BUILD_ROOT%{_unitdir}/chronyd-restricted.service
install -m 755 -p examples/chrony.nm-dispatcher.onoffline \
        $RPM_BUILD_ROOT%{_prefix}/lib/NetworkManager/dispatcher.d/20-chrony-onoffline
install -m 755 -p examples/chrony.nm-dispatcher.dhcp \
        $RPM_BUILD_ROOT%{_prefix}/lib/NetworkManager/dispatcher.d/20-chrony-dhcp
install -m 644 -p examples/chrony-wait.service \
        $RPM_BUILD_ROOT%{_unitdir}/chrony-wait.service
install -m 644 -p %{SOURCE4} \
        $RPM_BUILD_ROOT%{_sysusersdir}/chrony.conf

cat > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/chronyd <<EOF
# Command-line options for chronyd
OPTIONS="%{?with_seccomp:-F 2}"
EOF

touch $RPM_BUILD_ROOT%{_sysconfdir}/chrony.keys
touch $RPM_BUILD_ROOT%{_localstatedir}/lib/chrony/{drift,rtc}

echo 'chronyd.service' > \
        $RPM_BUILD_ROOT%{_prefix}/lib/systemd/ntp-units.d/50-chronyd.list

%check
# set random seed to get deterministic results
export CLKNETSIM_RANDOM_SEED=24508
%make_build -C test/simulation/clknetsim
make quickcheck

%pre
%sysusers_create_compat %{SOURCE4}

%post
# migrate from chrony-helper to sourcedir directive
if test -a %{_libexecdir}/chrony-helper; then
        grep -qi 'sourcedir /run/chrony-dhcp$' %{_sysconfdir}/chrony.conf 2> /dev/null || \
                echo -e '\n# Use NTP servers from DHCP.\nsourcedir /run/chrony-dhcp' >> \
                        %{_sysconfdir}/chrony.conf
        mkdir -p /run/chrony-dhcp
        for f in %{_localstatedir}/lib/dhclient/chrony.servers.*; do
                sed 's|.*|server &|' < $f > /run/chrony-dhcp/"${f##*servers.}.sources"
        done 2> /dev/null
fi
%systemd_post chronyd.service chronyd-restricted.service chrony-wait.service

%preun
%systemd_preun chronyd.service chronyd-restricted.service chrony-wait.service

%postun
%systemd_postun_with_restart chronyd.service chronyd-restricted.service

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc FAQ NEWS README examples/chrony.keys.example
%config(noreplace) %{_sysconfdir}/chrony.conf
%ghost %config %attr(640,root,chrony) %{_sysconfdir}/chrony.keys
%config(noreplace) %{_sysconfdir}/logrotate.d/chrony
%config(noreplace) %{_sysconfdir}/sysconfig/chronyd
%{_sysconfdir}/dhcp/dhclient.d/chrony.sh
%{_bindir}/chronyc
%{_sbindir}/chronyd
%{_prefix}/lib/NetworkManager
%{_prefix}/lib/systemd/ntp-units.d/*.list
%{_unitdir}/chrony*.service
%{_sysusersdir}/chrony.conf
%{_mandir}/man[158]/%{name}*.[158]*
%ghost %dir %attr(750,chrony,chrony) %{_localstatedir}/lib/chrony
%ghost %attr(-,chrony,chrony) %{_localstatedir}/lib/chrony/drift
%ghost %attr(-,chrony,chrony) %{_localstatedir}/lib/chrony/rtc
%ghost %dir %attr(750,chrony,chrony) %{_localstatedir}/log/chrony

%changelog
* Tue Oct 21 2025 Miroslav Lichvar <mlichvar@redhat.com> 4.8-3
- update seccomp filter for new glibc (#2405310)

* Mon Sep 08 2025 Miroslav Lichvar <mlichvar@redhat.com> 4.8-2
- drop root privileges in chronyc by default

* Wed Aug 27 2025 Miroslav Lichvar <mlichvar@redhat.com> 4.8-1
- update to 4.8

* Thu Aug 14 2025 Miroslav Lichvar <mlichvar@redhat.com> 4.8-0.1.pre1
- update to 4.8-pre1

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Miroslav Lichvar <mlichvar@redhat.com> 4.7-2
- let systemd create /var/lib/chrony and /var/log/chrony (#2372944)
- drop workaround for broken build on aarch64
- drop old conflict with NetworkManager

* Wed Jun 11 2025 Miroslav Lichvar <mlichvar@redhat.com> 4.7-1
- update to 4.7

* Thu May 22 2025 Miroslav Lichvar <mlichvar@redhat.com> 4.7-0.2.pre1
- add workaround for broken build on aarch64

* Wed May 21 2025 Miroslav Lichvar <mlichvar@redhat.com> 4.7-0.1.pre1
- update to 4.7-pre1

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 08 2024 Miroslav Lichvar <mlichvar@redhat.com> 4.6.1-1
- update to 4.6.1

* Mon Sep 02 2024 Miroslav Lichvar <mlichvar@redhat.com> 4.6-1
- update to 4.6

* Tue Jul 30 2024 Miroslav Lichvar <mlichvar@redhat.com> 4.6-0.1.pre1
- update to 4.6-pre1

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 05 2023 Miroslav Lichvar <mlichvar@redhat.com> 4.5-1
- update to 4.5

* Wed Nov 22 2023 Miroslav Lichvar <mlichvar@redhat.com> 4.5-0.1.pre1
- update to 4.5-pre1

* Wed Aug 09 2023 Miroslav Lichvar <mlichvar@redhat.com> 4.4-1
- update to 4.4
- require tzdata (#2218368)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4-0.4.pre2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 21 2023 Miroslav Lichvar <mlichvar@redhat.com> 4.4-0.3.pre2
- update to 4.4-pre2
- set selinux context in chronyd-restricted service (#2169949)

* Tue Jun 06 2023 Miroslav Lichvar <mlichvar@redhat.com> 4.4-0.2.pre1
- rebuild for AES-GCM-SIV in new nettle

* Wed May 10 2023 Miroslav Lichvar <mlichvar@redhat.com> 4.4-0.1.pre1
- update to 4.4-pre1
- switch from patchX to patch -P X

* Wed Jan 25 2023 Miroslav Lichvar <mlichvar@redhat.com> 4.3-3
- drop default chrony.keys config (#2104918)
- add chronyd-restricted service for minimal NTP client configurations
- convert license tag to SPDX

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 31 2022 Miroslav Lichvar <mlichvar@redhat.com> 4.3-1
- update to 4.3

* Thu Aug 11 2022 Miroslav Lichvar <mlichvar@redhat.com> 4.3-0.1.pre1
- update to 4.3-pre1

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 24 2022 Luca BRUNO <lucab@lucabruno.net> - 4.2-6
- Add a sysusers.d fragment for chrony user/group

* Wed Feb 16 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.2-5
- Drop obsolete workaround in scriptlet

* Wed Feb 09 2022 Miroslav Lichvar <mlichvar@redhat.com> 4.2-4
- update seccomp filter for latest glibc

* Tue Feb 08 2022 Miroslav Lichvar <mlichvar@redhat.com> 4.2-3
- use NTP servers passed by NetworkManager from DHCPv6 NTP server option

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 16 2021 Miroslav Lichvar <mlichvar@redhat.com> 4.2-1
- update to 4.2

* Thu Dec 02 2021 Miroslav Lichvar <mlichvar@redhat.com> 4.2-0.1.pre1
- update to 4.2-pre1

* Tue Nov 16 2021 Miroslav Lichvar <mlichvar@redhat.com> 4.1-5
- fix hardened chronyd service to allow writing log files

* Wed Sep 29 2021 Miroslav Lichvar <mlichvar@redhat.com> 4.1-4
- harden chronyd and chrony-wait services

* Mon Aug 09 2021 Miroslav Lichvar <mlichvar@redhat.com> 4.1-3
- update seccomp filter for new glibc
- remove unnecessary build requirement

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 13 2021 Miroslav Lichvar <mlichvar@redhat.com> 4.1-1
- update to 4.1
- enable seccomp filter by default (incompatible with mailonchange directive)

* Thu Apr 22 2021 Miroslav Lichvar <mlichvar@redhat.com> 4.1-0.1.pre1
- update to 4.1-pre1
- rework NM-dispatcher/dhclient detection
- enable LTO on s390x

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.0-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Feb 02 2021 Miroslav Lichvar <mlichvar@redhat.com> 4.0-3
- update NM DHCP dispatcher script

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
- Add BuildRequires: make
- drop dnssrv service and timer

* Wed Oct 07 2020 Miroslav Lichvar <mlichvar@redhat.com> 4.0-1
- update to 4.0
- update directory permissions to follow upstream

* Wed Sep 16 2020 Miroslav Lichvar <mlichvar@redhat.com> 4.0-0.9.pre4
- update to 4.0-pre4

* Wed Aug 26 2020 Miroslav Lichvar <mlichvar@redhat.com> 4.0-0.8.pre3
- update to 4.0-pre3
- switch to sourcedir directive for loading servers from DHCP
- add NetworkManager dispatcher script to save servers from DHCP when
  dhclient is not installed (Robert Fairley)
- drop old migration code from scriptlet
- move default paths in /var/run to /run

* Mon Aug 10 2020 Jeff Law <law@redhat.com> - 4.0-0.7.pre2
- Disable LTO on s390x

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-0.6.pre2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-0.5.pre2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> 4.0-0.4.pre2
- use make macros

* Mon May 04 2020 Miroslav Lichvar <mlichvar@redhat.com> 4.0-0.3.pre2
- rebuild for new nettle

* Mon Apr 20 2020 Miroslav Lichvar <mlichvar@redhat.com> 4.0-0.2.pre2
- update to 4.0-pre2

* Tue Mar 17 2020 Miroslav Lichvar <mlichvar@redhat.com> 4.0-0.1.pre1
- update to 4.0-pre1
- add net-tools to build requirements for testing
- add missing dependency on coreutils

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Miroslav Lichvar <mlichvar@redhat.com> 3.5-7
- fix testing with new glibc (#1792854)

* Wed Oct 09 2019 Miroslav Lichvar <mlichvar@redhat.com> 3.5-6
- drop timedatex recommendation
- verify upstream signatures

* Thu Aug 22 2019 Lubomir Rintel <lkundrak@v3.sk> - 3.5-5
- Move the NetworkManager dispatcher script out of /etc

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Miroslav Lichvar <mlichvar@redhat.com> 3.5-3
- rebuild for new nettle

* Thu May 23 2019 Miroslav Lichvar <mlichvar@redhat.com> 3.5-2
- fix shellcheck warnings in helper scripts

* Tue May 14 2019 Miroslav Lichvar <mlichvar@redhat.com> 3.5-1
- update to 3.5

* Thu May 02 2019 Miroslav Lichvar <mlichvar@redhat.com> 3.5-0.1.pre1
- update to 3.5-pre1

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 19 2018 Miroslav Lichvar <mlichvar@redhat.com> 3.4-1
- update to 3.4

* Fri Aug 31 2018 Miroslav Lichvar <mlichvar@redhat.com> 3.4-0.1.pre1
- update to 3.4-pre1

* Mon Aug 13 2018 Miroslav Lichvar <mlichvar@redhat.com> 3.3-5
- fix PIDFile in local chronyd.service on upgrades from chrony < 3.3-2
- add workaround for late reload of unit file (#1614751)

* Mon Jul 16 2018 Miroslav Lichvar <mlichvar@redhat.com> 3.3-4
- add gcc-c++ to build requirements

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miroslav Lichvar <mlichvar@redhat.com> 3.3-2
- move pidfile to /var/run/chrony to allow chronyd to remove it on exit
- avoid blocking in getrandom system call

* Wed Apr 04 2018 Miroslav Lichvar <mlichvar@redhat.com> 3.3-1
- update to 3.3
- enable keyfile by default again

* Thu Mar 15 2018 Miroslav Lichvar <mlichvar@redhat.com> 3.3-0.1.pre1
- update to 3.3-pre1
- switch to nettle for crypto hashing
- add gcc to build requirements

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Miroslav Lichvar <mlichvar@redhat.com> 3.2-3
- use systemd macro for scriptlet dependencies

* Thu Jan 25 2018 Miroslav Lichvar <mlichvar@redhat.com> 3.2-2
- fix chronyc getting stuck in infinite loop after clock step
- don't allow packaging without vendor zone
- suggest ntp-refclock
- remove obsolete dependency
- update description

* Fri Sep 15 2017 Miroslav Lichvar <mlichvar@redhat.com> 3.2-1
- update to 3.2
- get TAI-UTC offset and leap seconds from tzdata by default

* Tue Aug 29 2017 Miroslav Lichvar <mlichvar@redhat.com> 3.2-0.4.pre2
- update to 3.2-pre2

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-0.3.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-0.2.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Miroslav Lichvar <mlichvar@redhat.com> 3.2-0.1.pre1
- update to 3.2-pre1

* Thu May 04 2017 Miroslav Lichvar <mlichvar@redhat.com> 3.1-5
- check PEERNTP variable before loading existing dhclient files

* Thu Apr 20 2017 Miroslav Lichvar <mlichvar@redhat.com> 3.1-4
- use ID from /etc/os-release to set pool.ntp.org vendor zone (#1443599)
- fix seccomp filter for new glibc once again
- don't drop PHC samples with zero delay

* Mon Mar 13 2017 Miroslav Lichvar <mlichvar@redhat.com> 3.1-3
- fix seccomp filter for new glibc

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Miroslav Lichvar <mlichvar@redhat.com> 3.1-1
- update to 3.1
- enable seccomp support on more archs
- package chronyd sysconfig file

* Tue Jan 24 2017 Miroslav Lichvar <mlichvar@redhat.com> 3.1-0.1.pre1
- update to 3.1-pre1

* Mon Jan 16 2017 Miroslav Lichvar <mlichvar@redhat.com> 3.0-1
- update to 3.0

* Fri Jan 06 2017 Miroslav Lichvar <mlichvar@redhat.com> 3.0-0.3.pre3
- update to 3.0-pre3

* Thu Dec 15 2016 Miroslav Lichvar <mlichvar@redhat.com> 3.0-0.2.pre2
- update to 3.0-pre2
- enable support for MS-SNTP authentication in Samba

* Fri Dec 09 2016 Miroslav Lichvar <mlichvar@redhat.com> 3.0-0.1.pre1
- update to 3.0-pre1

* Mon Nov 21 2016 Miroslav Lichvar <mlichvar@redhat.com> 2.4.1-1
- update to 2.4.1

* Thu Oct 27 2016 Miroslav Lichvar <mlichvar@redhat.com> 2.4-4
- avoid AVC denials in chrony-wait service (#1350815)

* Tue Sep 13 2016 Miroslav Lichvar <mlichvar@redhat.com> 2.4-3
- fix chrony-helper to escape names of systemd units (#1374767)

* Tue Jun 28 2016 Miroslav Lichvar <mlichvar@redhat.com> 2.4-2
- fix chrony-helper to exit with correct status (#1350531)

* Tue Jun 07 2016 Miroslav Lichvar <mlichvar@redhat.com> 2.4-1
- update to 2.4
- don't require info

* Mon May 16 2016 Miroslav Lichvar <mlichvar@redhat.com> 2.4-0.1.pre1
- update to 2.4-pre1
- extend chrony-helper to allow management of static sources (#1331655)

* Tue Feb 16 2016 Miroslav Lichvar <mlichvar@redhat.com> 2.3-1
- update to 2.3

* Tue Feb 02 2016 Miroslav Lichvar <mlichvar@redhat.com> 2.3-0.1.pre1
- update to 2.3-pre1

* Thu Jan 21 2016 Miroslav Lichvar <mlichvar@redhat.com> 2.2.1-1
- update to 2.2.1 (CVE-2016-1567)
- set NTP era split explicitly

* Mon Oct 19 2015 Miroslav Lichvar <mlichvar@redhat.com> 2.2-1
- update to 2.2

* Fri Oct 09 2015 Miroslav Lichvar <mlichvar@redhat.com> 2.2-0.2.pre2
- update to 2.2-pre2
- require libseccomp-devel on supported archs only

* Fri Oct 02 2015 Miroslav Lichvar <mlichvar@redhat.com> 2.2-0.1.pre1
- update to 2.2-pre1
- enable seccomp support
- use weak dependency for timedatex on Fedora 24 and later

* Tue Jun 23 2015 Miroslav Lichvar <mlichvar@redhat.com> 2.1.1-1
- update to 2.1.1
- add -n option to gzip command to not save timestamp

* Mon Jun 22 2015 Miroslav Lichvar <mlichvar@redhat.com> 2.1-1
- update to 2.1
- extend chrony-helper to allow using servers from DNS SRV records (#1234406)
- set random seed in testing to get deterministic results

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-0.2.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Miroslav Lichvar <mlichvar@redhat.com> 2.1-0.1.pre1
- update to 2.1-pre1

* Mon Apr 27 2015 Miroslav Lichvar <mlichvar@redhat.com> 2.0-1
- update to 2.0

* Wed Apr 08 2015 Miroslav Lichvar <mlichvar@redhat.com> 2.0-0.3.pre2
- update to 2.0-pre2 (CVE-2015-1853 CVE-2015-1821 CVE-2015-1822)

* Thu Jan 29 2015 Miroslav Lichvar <mlichvar@redhat.com> 2.0-0.2.pre1
- require timedatex (#1136905)

* Tue Jan 27 2015 Miroslav Lichvar <mlichvar@redhat.com> 2.0-0.1.pre1
- update to 2.0-pre1

* Thu Sep 11 2014 Miroslav Lichvar <mlichvar@redhat.com> 1.31-1
- update to 1.31
- add servers from DHCP with iburst option by default
- use upstream configuration files and scripts
- don't package configuration examples
- compress chrony.txt

* Thu Aug 21 2014 Miroslav Lichvar <mlichvar@redhat.com> 1.31-0.1.pre1
- update to 1.31-pre1
- use license macro if available

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Miroslav Lichvar <mlichvar@redhat.com> 1.30-2
- reconnect client sockets (#1124059)

* Tue Jul 01 2014 Miroslav Lichvar <mlichvar@redhat.com> 1.30-1
- update to 1.30
- enable debug messages

* Mon Jun 09 2014 Miroslav Lichvar <mlichvar@redhat.com> 1.30-0.1.pre1
- update to 1.30-pre1
- execute test suite
- avoid calling systemctl in helper script
- call chronyc directly from logrotate and NM dispatcher scripts
- add conflict with systemd-timesyncd service

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.29.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 31 2014 Miroslav Lichvar <mlichvar@redhat.com> 1.29.1-1
- update to 1.29.1 (CVE-2014-0021)
- replace hardening build flags with _hardened_build

* Tue Nov 19 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.29-3
- let systemd remove pid file (#974305)

* Thu Oct 03 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.29-2
- add ordering dependency to not start chronyd before ntpd stopped

* Thu Aug 08 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.29-1
- update to 1.29 (CVE-2012-4502, CVE-2012-4503)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.28-1
- update to 1.28
- change default makestep limit to 10 seconds

* Mon Jun 24 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.28-0.2.pre1
- buildrequire systemd-units

* Fri Jun 21 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.28-0.1.pre1
- update to 1.28-pre1
- listen for commands only on localhost by default

* Thu May 09 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.27-3
- disable chrony-wait service by default (#961047)
- drop old systemd scriptlets
- don't own ntp-units.d directory
- move files from /lib
- remove unncessary dependency on syslog target

* Tue Mar 12 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.27-2
- suppress error messages from tr when generating key (#907914)
- fix delta calculation with extreme frequency offsets

* Fri Feb 01 2013 Miroslav Lichvar <mlichvar@redhat.com> 1.27-1
- update to 1.27
- start chrony-wait service with chronyd
- start chronyd service after sntp
- remove obsolete macros

* Tue Sep 11 2012 Miroslav Lichvar <mlichvar@redhat.com> 1.27-0.5.pre1.git1ca844
- update to git snapshot 1ca844
- update systemd integration (#846303)
- use systemd macros if available (#850151)
- use correct vendor pool.ntp.org zone on RHEL (#845981)
- don't log output of chrony-wait service

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-0.4.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 Miroslav Lichvar <mlichvar@redhat.com> 1.27-0.3.pre1
- update service file for systemd-timedated-ntp target (#816493)

* Fri Apr 06 2012 Miroslav Lichvar <mlichvar@redhat.com> 1.27-0.2.pre1
  use systemctl is-active instead of status in chrony-helper (#794771)

* Tue Feb 28 2012 Miroslav Lichvar <mlichvar@redhat.com> 1.27-0.1.pre1
- update to 1.27-pre1
- generate SHA1 command key instead of MD5

* Wed Feb 15 2012 Miroslav Lichvar <mlichvar@redhat.com> 1.26-6.20110831gitb088b7
- remove old servers on DHCP update (#787042)

* Fri Feb 10 2012 Miroslav Lichvar <mlichvar@redhat.com> 1.26-5.20110831gitb088b7
- improve chrony-helper to keep track of servers added from DHCP (#787042)
- fix dhclient script to always return with zero exit code (#767859)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-4.20110831gitb088b7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 06 2011 Miroslav Lichvar <mlichvar@redhat.com> 1.26-3.20110831gitb088b7
- update to git snapshot 20110831gitb088b7
- on first start generate password with 16 chars
- change systemd service type to forking
- add forced-command to chrony-helper (#735821)

* Mon Aug 15 2011 Miroslav Lichvar <mlichvar@redhat.com> 1.26-2
- fix iburst with very high jitters and long delays
- use timepps header from pps-tools-devel

* Wed Jul 13 2011 Miroslav Lichvar <mlichvar@redhat.com> 1.26-1
- update to 1.26
- read options from sysconfig file if it exists

* Fri Jun 24 2011 Miroslav Lichvar <mlichvar@redhat.com> 1.26-0.1.pre1
- update to 1.26-pre1
- fix service name in %%triggerun
- drop SysV init script
- add chrony-wait service

* Fri May 06 2011 Bill Nottingham <notting@redhat.com> 1.25-2
- fix systemd scriptlets for the upgrade case

* Wed May 04 2011 Miroslav Lichvar <mlichvar@redhat.com> 1.25-1
- update to 1.25

* Wed Apr 20 2011 Miroslav Lichvar <mlichvar@redhat.com> 1.25-0.3.pre2
- update to 1.25-pre2
- link with -Wl,-z,relro,-z,now options

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-0.2.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Miroslav Lichvar <mlichvar@redhat.com> 1.25-0.1.pre1
- update to 1.25-pre1
- use iburst, four pool servers, rtcsync, stratumweight in default config
- add systemd support
- drop sysconfig file 
- suppress install-info errors

* Thu Apr 29 2010 Miroslav Lichvar <mlichvar@redhat.com> 1.24-4.20100428git73d775
- update to 20100428git73d775
- replace initstepslew directive with makestep in default config
- add NetworkManager dispatcher script
- add dhclient script
- retry server/peer name resolution at least once to workaround
  NetworkManager race condition on boot
- don't verify chrony.keys

* Fri Mar 12 2010 Miroslav Lichvar <mlichvar@redhat.com> 1.24-3.20100302git5fb555
- update to snapshot 20100302git5fb555
- compile with PPS API support

* Thu Feb 04 2010 Miroslav Lichvar <mlichvar@redhat.com> 1.24-1
- update to 1.24 (#555367, CVE-2010-0292 CVE-2010-0293 CVE-2010-0294)
- modify default config
  - step clock on start if it is off by more than 100 seconds
  - disable client log
- build with -fPIE on sparc

* Tue Dec 15 2009 Miroslav Lichvar <mlichvar@redhat.com> 1.24-0.1.pre1
- update to 1.24-pre1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-7.20081106gitbe42b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Miroslav Lichvar <mlichvar@redhat.com> 1.23-6.20081106gitbe42b4
- switch to editline
- support arbitrary chronyc commands in init script

* Mon Jun 08 2009 Dan Horak <dan[at]danny.cz> 1.23-5.20081106gitbe42b4
- add patch with support for s390/s390x

* Mon Mar 09 2009 Miroslav Lichvar <mlichvar@redhat.com> 1.23-4.20081106gitbe42b4
- fix building with broken libcap header (#483548)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-3.20081106gitbe42b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 19 2008 Miroslav Lichvar <mlichvar@redhat.com> 1.23-2.20081106gitbe42b4
- fix info uninstall
- generate random command key in init script
- support cyclelogs, online, offline commands in init script
- add logrotate script

* Tue Nov 11 2008 Miroslav Lichvar <mlichvar@redhat.com> 1.23-1.20081106gitbe42b4
- initial release
