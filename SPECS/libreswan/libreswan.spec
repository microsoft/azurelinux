%global _hardened_build 1
# These are rpm macros and are 0 or 1
%global with_development 0
%global nss_version 3.52
%global unbound_version 1.6.6
# Libreswan config options
%global libreswan_config \\\
    FINALLIBEXECDIR=%{_libexecdir}/ipsec \\\
    FINALMANDIR=%{_mandir} \\\
    PREFIX=%{_prefix} \\\
    INITSYSTEM=systemd \\\
    PYTHON_BINARY=%{__python3} \\\
    SHELL_BINARY=%{_bindir}/sh \\\
    USE_DNSSEC=true \\\
    USE_LABELED_IPSEC=true \\\
    USE_LDAP=true \\\
    USE_LIBCAP_NG=true \\\
    USE_LIBCURL=true \\\
    USE_LINUX_AUDIT=true \\\
    USE_NM=true \\\
    USE_NSS_IPSEC_PROFILE=true \\\
    USE_SECCOMP=true \\\
    USE_AUTHPAM=true \\\
%{nil}

Summary:        Internet Key Exchange (IKEv1 and IKEv2) implementation for IPsec
Name:           libreswan
Version:        4.7
Release:        5%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
Url:            https://libreswan.org/
Source0:        https://github.com/libreswan/libreswan/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source3:        https://download.libreswan.org/cavs/ikev1_dsa.fax.bz2
Source4:        https://download.libreswan.org/cavs/ikev1_psk.fax.bz2
Source5:        https://download.libreswan.org/cavs/ikev2.fax.bz2
Patch0:         CVE-2023-38710.patch
Patch1:         CVE-2023-38711.patch
Patch2:         CVE-2023-38712.patch

BuildRequires: audit-libs-devel
BuildRequires: bison
BuildRequires: curl-devel
BuildRequires: flex
BuildRequires: gcc
BuildRequires: gnupg2
BuildRequires: hostname
BuildRequires: ldns-devel
BuildRequires: libcap-ng-devel
BuildRequires: libevent-devel
BuildRequires: libseccomp-devel
BuildRequires: libselinux-devel
BuildRequires: make
BuildRequires: nspr-devel
BuildRequires: nss-devel >= %{nss_version}
BuildRequires: nss-tools >= %{nss_version}
BuildRequires: openldap-devel
BuildRequires: azurelinux-release
BuildRequires: pam-devel
BuildRequires: pkgconfig
BuildRequires: systemd-devel
BuildRequires: unbound-devel >= %{unbound_version}
BuildRequires: xmlto
Requires: iproute >= 2.6.8
Requires: nss >= %{nss_version}
Requires: nss-softokn
Requires: nss-tools
Requires: unbound-libs >= %{unbound_version}
Requires: logrotate
# for pidof
Requires: procps-ng

Requires(post): bash
Requires(post): coreutils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Libreswan is a free implementation of IPsec & IKE for Linux.  IPsec is
the Internet Protocol Security and uses strong cryptography to provide
both authentication and encryption services.  These services allow you
to build secure tunnels through untrusted networks.  Everything passing
through the untrusted net is encrypted by the ipsec gateway machine and
decrypted by the gateway at the other end of the tunnel.  The resulting
tunnel is a virtual private network or VPN.

This package contains the daemons and userland tools for setting up
Libreswan.

Libreswan also supports IKEv2 (RFC7296) and Secure Labeling

Libreswan is based on Openswan-2.6.38 which in turn is based on FreeS/WAN-2.04

%prep
%setup -q -n libreswan-%{version}
# enable crypto-policies support
sed -i "s:#[ ]*include \(.*\)\(/crypto-policies/back-ends/libreswan.config\)$:include \1\2:" configs/ipsec.conf.in
sed -i "s/SUBDIRS += ipcheck/#SUBDIRS += ipchec/" testing/programs/Makefile
%autopatch -p1

%build
make %{?_smp_mflags} \
%if 0%{with_development}
    OPTIMIZE_CFLAGS="%{?_hardened_cflags}" \
%else
    OPTIMIZE_CFLAGS="%{optflags}" \
%endif
    WERROR_CFLAGS="-Werror -Wno-missing-field-initializers -Wno-lto-type-mismatch -Wno-maybe-uninitialized" \
    USERLINK="%{?__global_ldflags} -Wl,-z,relro -Wl,--as-needed  -Wl,-z,now -flto --no-lto" \
    %{libreswan_config} \
    programs
FS=$(pwd)


%install
make \
    DESTDIR=%{buildroot} \
    %{libreswan_config} \
    install
FS=$(pwd)
rm -rf %{buildroot}/usr/share/doc/libreswan
rm -rf %{buildroot}%{_libexecdir}/ipsec/*check

install -d -m 0755 %{buildroot}%{_rundir}/pluto
install -d %{buildroot}%{_sbindir}

install -d %{buildroot}%{_sysctldir}
install -m 0644 packaging/fedora/libreswan-sysctl.conf \
    %{buildroot}%{_sysctldir}/50-libreswan.conf

echo "include %{_sysconfdir}/ipsec.d/*.secrets" \
    > %{buildroot}%{_sysconfdir}/ipsec.secrets
rm -fr %{buildroot}%{_sysconfdir}/rc.d/rc*

%check
# There is an elaborate upstream testing infrastructure which we do not
# run here - it takes hours and uses kvm
# We only run the CAVS tests and startup selftest
cp %{SOURCE3} %{SOURCE4} %{SOURCE5} .
bunzip2 *.fax.bz2

: starting CAVS test for IKEv2
%{buildroot}%{_libexecdir}/ipsec/cavp -v2 ikev2.fax | \
    diff -u ikev2.fax - > /dev/null
: starting CAVS test for IKEv1 RSASIG
%{buildroot}%{_libexecdir}/ipsec/cavp -v1dsa ikev1_dsa.fax | \
    diff -u ikev1_dsa.fax - > /dev/null
: starting CAVS test for IKEv1 PSK
%{buildroot}%{_libexecdir}/ipsec/cavp -v1psk ikev1_psk.fax | \
    diff -u ikev1_psk.fax - > /dev/null
: CAVS tests passed

# Some of these tests will show ERROR for negative testing - it will exit on real errors
%{buildroot}%{_libexecdir}/ipsec/algparse -tp || { echo prooposal test failed; exit 1; }
%{buildroot}%{_libexecdir}/ipsec/algparse -ta || { echo algorithm test failed; exit 1; }
: Algorithm parser tests passed

# self test for pluto daemon - this also shows which algorithms it allows in FIPS mode
tmpdir=$(mktemp -d /tmp/libreswan-XXXXX)
certutil -N -d sql:$tmpdir --empty-password
%{buildroot}%{_libexecdir}/ipsec/pluto --selftest --nssdir $tmpdir --rundir $tmpdir
: pluto self-test passed - verify FIPS algorithms allowed is still compliant with NIST

%post
%systemd_post ipsec.service
%sysctl_apply 50-libreswan.conf

%preun
%systemd_preun ipsec.service

%postun
%systemd_postun_with_restart ipsec.service

%files
%license CREDITS COPYING LICENSE
%doc CHANGES README* 
%doc docs/*.* docs/examples
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ipsec.conf
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ipsec.secrets
%attr(0700,root,root) %dir %{_sysconfdir}/ipsec.d
%attr(0700,root,root) %dir %{_sysconfdir}/ipsec.d/policies
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ipsec.d/policies/*
%attr(0644,root,root) %config(noreplace) %{_sysctldir}/50-libreswan.conf
%attr(0755,root,root) %dir %{_rundir}/pluto
%attr(0700,root,root) %dir %{_sharedstatedir}/ipsec
%attr(0700,root,root) %dir %{_sharedstatedir}/ipsec/nss
%attr(0644,root,root) %{_tmpfilesdir}/libreswan.conf
%attr(0644,root,root) %{_unitdir}/ipsec.service
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/pluto
%config(noreplace) %{_sysconfdir}/logrotate.d/libreswan
%{_sbindir}/ipsec
%{_libexecdir}/ipsec
%doc %{_mandir}/*/*

%changelog
* Mon Aug 28 2023 Henry Beberman <henry.beberman@microsoft.com> - 4.7-5
- Backport patches for CVE-2023-38710, CVE-2023-38711, CVE-2023-38712

* Tue Oct 11 2022 Osama Esmail <osamaesmail@microsoft.com> - 4.7-4
- Removed with_check macro

* Mon Jul 25 2022 Rachel Menge <rachelmenge@microsoft.com> - 4.7-3
- Move from SPECS-EXTENDED to SPECS

* Fri Jun 10 2022 Rachel Menge <rachelmenge@microsoft.com> - 4.7-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified

* Tue May 24 2022 Paul Wouters <paul.wouters@aiven.io> - 4.7-1
- Updated to 4.7 (EAPTLS support, bugfixes)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.6-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Paul Wouters <paul.wouters@aiven.io> - 4.6-2
- Re-enable USE_DNSSEC again with patch to resolve header conflicts

* Wed Jan 12 2022 Paul Wouters <paul.wouters@aiven.io> - 4.6-1
- Resolves: CVE-2022-23094
- Resolves: rhbz#2039604 libreswan-4.6 is available
- Add gpg key and signature check for build
- Temporarilly disable USE_DNSSEC in rawhide while we figure out openssl vs nss include clash

* Thu Aug 26 2021 Paul Wouters <paul.wouters@aiven.io> - 4.5-1
- Resolves rhbz#1996250 libreswan-4.5 is available

* Tue Aug 03 2021 Paul Wouters <paul.wouters@aiven.io> - 4.4-3
- Resolves rhbz#1989198 libreswan should depend on procps-ng or pidof

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 07 2021 Paul Wouters <paul.wouters@aiven.io> - 4.4-2
- Properly handle rpm sysctl config

* Wed May 12 2021 Paul Wouters <paul.wouters@aiven.io> - 4.4-1
- Resolves: rhbz#1952602 libreswan-4.4 is available

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.3-1.1
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Sun Feb 21 2021 Paul Wouters <pwouters@redhat.com> - 4.3-1
- update to 4.3 (minor bugfix release)

* Wed Feb 03 2021 Paul Wouters <pwouters@redhat.com> - 4.2-1
- Update to 4.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-0.1.rc1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 19 19:59:55 EST 2020 Paul Wouters <pwouters@redhat.com> - 4.2-0.1.rc1
- Resolves: rhbz#1867580 pluto process frequently dumps core
  (disable USE_NSS_KDF until nss fixes have propagated)

* Sat Dec 19 2020 Adam Williamson <awilliam@redhat.com> - 4.1-4
- Rebuild for ldns soname bump

* Mon Nov 23 11:50:41 EST 2020 Paul Wouters <pwouters@redhat.com> - 4.1-3
- Resolves: rhbz#1894381 Libreswan 4.1-2 breaks l2tp connection to Windows VPN server

* Mon Oct 26 10:21:57 EDT 2020 Paul Wouters <pwouters@redhat.com> - 4.1-2
- Resolves: rhbz#1889538 libreswan's /var/lib/ipsec/nss missing

* Sun Oct 18 21:49:39 EDT 2020 Paul Wouters <pwouters@redhat.com> - 4.1-1
- Updated to 4.1 - interop fix for Cisco

* Thu Oct 15 10:27:14 EDT 2020 Paul Wouters <pwouters@redhat.com> - 4.0-1
- Resolves: rhbz#1888448 libreswan-4.0 is available

* Wed Sep 30 14:05:58 EDT 2020 Paul Wouters <pwouters@redhat.com> - 4.0-0.2.rc1
- Rebuild for libevent 2.1.12 with a soname bump

* Sun Sep 27 22:49:40 EDT 2020 Paul Wouters <pwouters@redhat.com> - 4.0-0.1.rc1
- Updated to 4.0rc1

* Thu Aug 27 2020 Paul Wouters <pwouters@redhat.com> - 3.32-4
- Resolves: rhbz#1864043 libreswan: FTBFS in Fedora rawhide/f33

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.32-3.2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.32-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 3.32-3
- Initialize ppk_id_p in ikev2_parent_inR1outI2_tail to avoid uninitialized
  object

* Tue May 26 2020 Paul Wouters <pwouters@redhat.com> - 3.32-2
- Backport NSS guarding fix for unannounced changed api in NSS causing segfault

* Mon May 11 2020 Paul Wouters <pwouters@redhat.com> - 3.32-1
- Resolves: rhbz#1809770 libreswan-3.32 is available

* Tue Apr 14 2020 Paul Wouters <pwouters@redhat.com> - 3.31-2
- Resolves: rhbz#1823823 Please drop the dependency on fipscheck

* Tue Mar 03 2020 Paul Wouters <pwouters@redhat.com> - 3.31-1
- Resolves: rhbz#1809770 libreswan-3.31 is available (fixes rekey regression)

* Fri Feb 14 2020 Paul Wouters <pwouters@redhat.com> - 3.30-1
- Resolves: rhbz#1802896 libreswan-3.30 is available
- Resolves: rhbz#1799598 libreswan: FTBFS in Fedora rawhide/f32
- Resolves: rhbz#1760571 [abrt] libreswan: configsetupcheck(): verify:366:configsetupcheck:TypeError:

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.29-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Paul Wouters <pwouters@redhat.com> - 3.29-2
- _updown.netkey: fix syntax error in checking routes

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.29-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 2019 Paul Wouters <pwouters@redhat.com> - 3.29-1
- Resolves: rhbz#1718986 Updated to 3.29 for CVE-2019-10155

* Tue May 21 2019 Paul Wouters <pwouters@redhat.com> - 3.28-1
- Updated to 3.28 (many imported bugfixes, including CVE-2019-12312)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.27-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 3.27-1.1
- Rebuilt for libcrypt.so.2 (#1666033)

* Mon Oct 08 2018 Paul Wouters <pwouters@redhat.com> - 3.27-1
- Updated to 3.27 (various bugfixes)

* Thu Sep 27 2018 Paul Wouters <pwouters@redhat.com> - 3.26-3
- Add fedora python fixup for _unbound-hook

* Mon Sep 17 2018 Paul Wouters <pwouters@redhat.com> - 3.26-2
- linking against freebl is no longer needed (and wasn't done in 3.25)

* Mon Sep 17 2018 Paul Wouters <pwouters@redhat.com> - 3.26-1
- Updated to 3.26 (CHACHA20POLY1305, ECDSA and RSA-PSS support)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.25-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Paul Wouters <pwouters@redhat.com> - 3.25-3
- Fix Opportunistic IPsec _unbound-hook argument parsing
- Make rundir readable for all (so we can hand out permissions later)

* Mon Jul 02 2018 Paul Wouters <pwouters@redhat.com> - 3.25-2
- Relax deleting IKE SA's and IPsec SA's to avoid interop issues with third party VPN vendors

* Wed Jun 27 2018 Paul Wouters <pwouters@redhat.com> - 3.25-1
- Updated to 3.25

* Mon Feb 19 2018 Paul Wouters <pwouters@redhat.com> - 3.23-2
- Support crypto-policies package
- Pull in some patches from upstream and IANA registry updates
- gcc7 format-truncate fixes and workarounds

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.23-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Paul Wouters <pwouters@redhat.com> - 3.23-1
- Updated to 3.23 - support for MOBIKE, PPK, CMAC, nic offload and performance improvements

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 3.22-1.1
- Rebuilt for switch to libxcrypt

* Mon Oct 23 2017 Paul Wouters <pwouters@redhat.com> - 3.22-1
- Updated to 3.22 - many bugfixes, and unbound ipsecmod support

* Wed Aug  9 2017 Paul Wouters <pwouters@redhat.com> - 3.21-1
- Updated to 3.21

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.20-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 14 2017 Paul Wouters <pwouters@redhat.com> - 3.20-1
- Updated to 3.20

* Fri Mar 03 2017 Paul Wouters <pwouters@redhat.com> - 3.20-0.1.dr4
- Update to 3.20dr4 to test mozbz#1336487 export CERT_CompareAVA

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.19-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 03 2017 Paul Wouters <pwouters@redhat.com> - 3.19-2
- Resolves: rhbz#1392191 libreswan: crash when OSX client connects
- Improved uniqueid and session replacing support
- Test Buffer warning fix on size_t
- Re-introduce --configdir for backwards compatibility

* Sun Jan 15 2017 Paul Wouters <pwouters@redhat.com> - 3.19-1
- Updated to 3.19 (see download.libreswan.org/CHANGES)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.18-1.1
- Rebuild for Python 3.6

* Fri Jul 29 2016 Paul Wouters <pwouters@redhat.com> - 3.18-1
- Updated to 3.18 for CVE-2016-5391 rhbz#1361164 and VTI support
- Remove support for /etc/sysconfig/pluto (use native systemd instead)

* Thu May 05 2016 Paul Wouters <pwouters@redhat.com> - 3.17-2
- Resolves: rhbz#1324956 prelink is gone, /etc/prelink.conf.d/* is no longer used

* Thu Apr 07 2016 Paul Wouters <pwouters@redhat.com> - 3.17-1
- Updated to 3.17 for CVE-2016-3071
- Disable LIBCAP_NG as it prevents unbound-control from working properly
- Temporarilly disable WERROR due to a few minor known issues

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.16-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 18 2015 Paul Wouters <pwouters@redhat.com> - 3.16-1
- Updated to 3.16 (see https://download.libreswan.org/CHANGES)

* Tue Aug 11 2015 Paul Wouters <pwouters@redhat.com> - 3.15-1
- Updated to 3.15 (see http://download.libreswan.org/CHANGES)
- Resolves: rhbz#CVE-2015-3240 IKE daemon restart when receiving a bad DH gx
- NSS database creation moved from spec file to service file
- Run CAVS tests on package build
- Added BuildRequire systemd-units and xmlto
- Bumped minimum required nss to 3.16.1
- Install tmpfiles
- Install sysctl file
- Update doc files to include

* Mon Jul 13 2015 Paul Wouters <pwouters@redhat.com> - 3.13-2
- Resolves: rhbz#1238967 Switch libreswan to use python3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 01 2015 Paul Wouters <pwouters@redhat.com> - 3.13-1
- Updated to 3.13 for CVE-2015-3204

* Fri Nov 07 2014 Paul Wouters <pwouters@redhat.com> - 3.12-1
- Updated to 3.12 Various IKEv2 fixes

* Wed Oct 22 2014 Paul Wouters <pwouters@redhat.com> - 3.11-1
- Updated to 3.11 (many fixes, including startup fixes)
- Resolves: rhbz#1144941 libreswan 3.10 upgrade breaks old ipsec.secrets configs
- Resolves: rhbz#1147072 ikev1 aggr mode connection fails after libreswan upgrade
- Resolves: rhbz#1144831 Libreswan appears to start with systemd before all the NICs are up and running

* Tue Sep 09 2014 Paul Wouters <pwouters@redhat.com> - 3.10-3
- Fix some coverity issues, auto=route on bootup and snprintf on 32bit machines

* Mon Sep 01 2014 Paul Wouters <pwouters@redhat.com> - 3.10-1
- Updated to 3.10, major bugfix release, new xauth status options

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 10 2014 Paul Wouters <pwouters@redhat.com> - 3.9-1
- Updated to 3.9. IKEv2 enhancements, ESP/IKE algo enhancements
- Mark libreswan-fips.conf as config file
- attr modifier for man pages no longer needed
- BUGS file no longer exists upstream

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jan 18 2014 Paul Wouters <pwouters@redhat.com> - 3.8-1
- Updated to 3.8, fixes rhbz#CVE-2013-6467 (rhbz#1054102)

* Wed Dec 11 2013 Paul Wouters <pwouters@redhat.com> - 3.7-1
- Updated to 3.7, fixes CVE-2013-4564
- Fixes creating a bogus NSS db on startup (rhbz#1005410)

* Thu Oct 31 2013 Paul Wouters <pwouters@redhat.com> - 3.6-1
- Updated to 3.6 (IKEv2, MODECFG, Cisco interop fixes)
- Generate empty NSS db if none exists

* Mon Aug 19 2013 Paul Wouters <pwouters@redhat.com> - 3.5-3
- Add a Provides: for openswan-doc

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Paul Wouters <pwouters@redhat.com> - 3.5-2
- Added interop patch for (some?) Cisco VPN clients sending 16 zero
  bytes of extraneous IKE data
- Removed fipscheck_version

* Sat Jul 13 2013 Paul Wouters <pwouters@redhat.com> - 3.5-1
- Updated to 3.5

* Thu Jun 06 2013 Paul Wouters <pwouters@redhat.com> - 3.4-1
- Updated to 3.4, which only contains style changes to kernel coding style
- IN MEMORIAM: June 3rd, 2013 Hugh Daniel

* Mon May 13 2013 Paul Wouters <pwouters@redhat.com> - 3.3-1
- Updated to 3.3, which resolves CVE-2013-2052

* Sat Apr 13 2013 Paul Wouters <pwouters@redhat.com> - 3.2-1
- Initial package for Fedora