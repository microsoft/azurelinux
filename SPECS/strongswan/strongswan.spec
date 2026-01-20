%global _hardened_build 1
#%%define prerelease dr1

%bcond_without python3
%bcond_without perl
%bcond_without check

%bcond_with    network_man
%bcond_with tss_trousers

%global forgeurl0 https://github.com/strongswan/strongswan

Name:           strongswan
Version:        5.9.14
Release:        8%{?dist}
Summary:        An OpenSource IPsec-based VPN and TNC solution
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.strongswan.org/
VCS:            git:%{forgeurl0}
Source0:        https://download.strongswan.org/strongswan-%{version}%{?prerelease}.tar.bz2
Source3:        tmpfiles-strongswan.conf
Patch0:         strongswan-5.6.0-uintptr_t.patch
# https://github.com/strongswan/strongswan/issues/1198
Patch1:         strongswan-5.9.7-error-no-format.patch
# C23 fixes included in 6.0.1
Patch2:         strongswan-6.0.0-gcc15.patch
# C23 fixed merged but not yet released
Patch3:         strongswan-6.0.1-gcc15.patch
Patch4:         strongswan-fix-make-check.patch
Patch5:         0001-Extending-timeout-for-test-cases-with-multiple-read-.patch
Patch6:         CVE-2025-62291.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gnupg2
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  systemd
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  gmp-devel
BuildRequires:  libcurl-devel
BuildRequires:  openldap-devel
BuildRequires:  openssl-devel

BuildRequires:  sqlite-devel
BuildRequires:  gettext-devel
BuildRequires:  libxml2-devel
BuildRequires:  pam-devel
BuildRequires:  json-c-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  iptables-devel
BuildRequires:  libcap-devel
BuildRequires:  tpm2-tss-devel
BuildRequires:  pkgconfig(gthread-2.0)
Recommends:     tpm2-tools

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
%endif

%if %{with perl}
BuildRequires:  perl-devel perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
%endif

%if %{with tss_trousers}
BuildRequires:  trousers-devel
%endif

%if %{with network_man}
#BuildRequires:  NetworkManager-libnm-devel
%endif
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
The strongSwan IPsec implementation supports both the IKEv1 and IKEv2 key
exchange protocols in conjunction with the native NETKEY IPsec stack of the
Linux kernel.

%package libipsec
Summary: Strongswan's libipsec backend
%description libipsec
The kernel-libipsec plugin provides an IPsec backend that works entirely
in userland, using TUN devices and its own IPsec implementation libipsec.

%if %{with network_man}
%package charon-nm
Summary:        NetworkManager plugin for Strongswan
Requires:       dbus
Obsoletes:      strongswan-NetworkManager < 0:5.0.4-5
Conflicts:      strongswan-NetworkManager < 0:5.0.4-5
Conflicts:      NetworkManager-strongswan < 1.4.2-1
%description charon-nm
NetworkManager plugin integrates a subset of Strongswan capabilities
to NetworkManager.
%endif

%package sqlite
Summary: SQLite support for strongSwan
Requires: strongswan = %{version}-%{release}
%description sqlite
The sqlite plugin adds an SQLite database backend to strongSwan.

%package tnc-imcvs
Summary: Trusted network connect (TNC)'s IMC/IMV functionality
Requires: strongswan = %{version}-%{release}
Requires: strongswan-sqlite = %{version}-%{release}
%description tnc-imcvs
This package provides Trusted Network Connect's (TNC) architecture support.
It includes support for TNC client and server (IF-TNCCS), IMC and IMV message
exchange (IF-M), interface between IMC/IMV and TNC client/server (IF-IMC
and IF-IMV). It also includes PTS based IMC/IMV for TPM based remote
attestation, SWID IMC/IMV, and OS IMC/IMV. It's IMC/IMV dynamic libraries
modules can be used by any third party TNC Client/Server implementation
possessing a standard IF-IMC/IMV interface. In addition, it implements
PT-TLS to support TNC over TLS.

%if %{with python3}
%package -n python3-vici
Summary: Strongswan Versatile IKE Configuration Interface python bindings
BuildArch: noarch
%description -n python3-vici
VICI is an attempt to improve the situation for system integrators by providing
a stable IPC interface, allowing external tools to query, configure
and control the IKE daemon.

The Versatile IKE Configuration Interface (VICI) python bindings provides module
for Strongswan runtime configuration from python applications.

%endif

%if %{with perl}
%package -n perl-vici
Summary: Strongswan Versatile IKE Configuration Interface perl bindings
BuildArch: noarch
%description -n perl-vici
VICI is an attempt to improve the situation for system integrators by providing
a stable IPC interface, allowing external tools to query, configure
and control the IKE daemon.

The Versatile IKE Configuration Interface (VICI) perl bindings provides module
for Strongswan runtime configuration from perl applications.
%endif

# TODO: make also ruby-vici


%prep
%autosetup -n %{name}-%{version}%{?prerelease} -p1

%build
# only for snapshots
autoreconf -fiv

# --with-ipsecdir moves internal commands to /usr/libexec/strongswan
# --bindir moves 'pki' command to /usr/libexec/strongswan
# See: http://wiki.strongswan.org/issues/552
# too broken to enable:    --enable-sha3 --enable-rdrand --enable-connmark --enable-forecast
%configure --disable-static \
    --with-ipsec-script=strongswan \
    --sysconfdir=%{_sysconfdir}/strongswan \
    --with-ipsecdir=%{_libexecdir}/strongswan \
    --bindir=%{_libexecdir}/strongswan \
    --with-ipseclibdir=%{_libdir}/strongswan \
    --with-piddir=%{_rundir}/strongswan \
    --with-nm-ca-dir=%{_sysconfdir}/strongswan/ipsec.d/cacerts/ \
    --enable-bypass-lan \
    --enable-tss-tss2 \
    --enable-systemd \
    --enable-openssl \
    --enable-unity \
    --enable-ctr \
    --enable-ccm \
    --enable-gcm \
    --enable-chapoly \
    --enable-md4 \
    --enable-gcrypt \
    --enable-newhope \
    --enable-xauth-eap \
    --enable-xauth-pam \
    --enable-xauth-noauth \
    --enable-eap-identity \
    --enable-eap-md5 \
    --enable-eap-gtc \
    --enable-eap-tls \
    --enable-eap-ttls \
    --enable-eap-peap \
    --enable-eap-mschapv2 \
    --enable-eap-tnc \
    --enable-eap-sim \
    --enable-eap-sim-file \
    --enable-eap-aka \
    --enable-eap-aka-3gpp \
    --enable-eap-aka-3gpp2 \
    --enable-eap-dynamic \
    --enable-eap-radius \
    --enable-ext-auth \
    --enable-ipseckey \
    --enable-pkcs11 \
    --enable-tpm \
    --enable-farp \
    --enable-dhcp \
    --enable-ha \
    --enable-led \
    --enable-sql \
    --enable-sqlite \
    --enable-tnc-ifmap \
    --enable-tnc-pdp \
    --enable-tnc-imc \
    --enable-tnc-imv \
    --enable-tnccs-20 \
    --enable-tnccs-11 \
    --enable-tnccs-dynamic \
    --enable-imc-test \
    --enable-imv-test \
    --enable-imc-scanner \
    --enable-imv-scanner  \
    --enable-imc-attestation \
    --enable-imv-attestation \
    --enable-imv-os \
    --enable-imc-os \
    --enable-imc-swima \
    --enable-imv-swima \
    --enable-imc-hcd \
    --enable-imv-hcd \
    --enable-curl \
    --enable-cmd \
    --enable-acert \
    --enable-vici \
    --enable-swanctl \
    --enable-duplicheck \
%ifarch x86_64 %{ix86}
    --enable-aesni \
%endif
%if %{with python3}
    PYTHON=%{python3} --enable-python-eggs \
%endif
%if %{with perl}
    --enable-perl-cpan \
%endif
%if %{with check}
    --enable-test-vectors \
%endif
%if %{with tss_trousers}
    --enable-tss-trousers \
    --enable-aikgen \
%endif
    --enable-kernel-libipsec \
    --with-capabilities=libcap \
    CPPFLAGS="-DSTARTER_ALLOW_NON_ROOT"
# TODO: --enable-python-eggs-install not python3 ready

# disable certain plugins in the daemon configuration by default
for p in bypass-lan; do
    echo -e "\ncharon.plugins.${p}.load := no" >> conf/plugins/${p}.opt
done

# ensure manual page is regenerated with local configuration
rm -f src/ipsec/_ipsec.8

%make_build

pushd src/libcharon/plugins/vici

%if %{with python3}
  pushd python
    %make_build
    sed -e "s,/var/run/charon.vici,%{_rundir}/strongswan/charon.vici," -i vici/session.py
    #py3_build
  popd
%endif

%if %{with perl}
  pushd perl/Vici-Session/
    perl Makefile.PL INSTALLDIRS=vendor
    %make_build
  popd
%endif

popd

%install
%make_install


pushd src/libcharon/plugins/vici
%if %{with python3}
  pushd python
    # TODO: --enable-python-eggs breaks our previous build. Do it now
    # propose better way to upstream
    %py3_build
    %py3_install
  popd
%endif
%if %{with perl}
  %make_install -C perl/Vici-Session
  rm -f %{buildroot}{%{perl_archlib}/perllocal.pod,%{perl_vendorarch}/auto/Vici/Session/.packlist}
%endif
popd
# prefix man pages
for i in %{buildroot}%{_mandir}/*/*; do
    if echo "$i" | grep -vq '/strongswan[^\/]*$'; then
        mv "$i" "`echo "$i" | sed -re 's|/([^/]+)$|/strongswan_\1|'`"
    fi
done
find %{buildroot} -type f -name '*.la' -delete
# delete unwanted library files - no consumers, so no -devel package
rm %{buildroot}%{_libdir}/strongswan/*.so
# fix config permissions
chmod 644 %{buildroot}%{_sysconfdir}/strongswan/strongswan.conf

# Create ipsec.d directory tree.
install -d -m 700 %{buildroot}%{_sysconfdir}/strongswan/ipsec.d
for i in aacerts acerts certs cacerts crls ocspcerts private reqs; do
    install -d -m 700 %{buildroot}%{_sysconfdir}/strongswan/ipsec.d/${i}
done
install -d -m 0700 %{buildroot}%{_rundir}/strongswan
install -D -m 0644 %{SOURCE3} %{buildroot}/%{_tmpfilesdir}/strongswan.conf
install -D -m 0644 %{SOURCE3} %{buildroot}/%{_tmpfilesdir}/strongswan-starter.conf


%check
%if %{with check}
  # Seen some tests hang. Ensure we do not block builder forever
  #export TESTS_VERBOSITY=1
  timeout 600 %make_build check
%endif
%if %{with python}
  pushd src/libcharon/plugins/vici
    %pytest
  popd
%endif
:

%post
%systemd_post strongswan.service strongswan-starter.service

%preun
%systemd_preun strongswan.service strongswan-starter.service

%postun
%systemd_postun_with_restart strongswan.service strongswan-starter.service

%files
%doc README NEWS TODO ChangeLog
%license COPYING
%dir %attr(0755,root,root) %{_sysconfdir}/strongswan
%config(noreplace) %{_sysconfdir}/strongswan/*
%dir %{_libdir}/strongswan
%exclude %{_libdir}/strongswan/imcvs
%dir %{_libdir}/strongswan/plugins
%dir %{_libexecdir}/strongswan
%{_unitdir}/strongswan.service
%{_unitdir}/strongswan-starter.service
%{_sbindir}/charon-cmd
%{_sbindir}/charon-systemd
%{_sbindir}/strongswan
%{_sbindir}/swanctl
%{_libdir}/strongswan/*.so.*
%exclude %{_libdir}/strongswan/libimcv.so.*
%exclude %{_libdir}/strongswan/libtnccs.so.*
%exclude %{_libdir}/strongswan/libipsec.so.*
%{_libdir}/strongswan/plugins/*.so
%exclude %{_libdir}/strongswan/plugins/libstrongswan-sqlite.so
%exclude %{_libdir}/strongswan/plugins/libstrongswan-*tnc*.so
%exclude %{_libdir}/strongswan/plugins/libstrongswan-kernel-libipsec.so
%{_libexecdir}/strongswan/*
%exclude %{_libexecdir}/strongswan/attest
%exclude %{_libexecdir}/strongswan/pt-tls-client
%exclude %dir %{_datadir}/strongswan/swidtag
%{_mandir}/man?/*.gz
%{_datadir}/strongswan/templates/config/
%{_datadir}/strongswan/templates/database/
%attr(0755,root,root) %dir %{_rundir}/strongswan
%attr(0644,root,root) %{_tmpfilesdir}/strongswan.conf
%attr(0644,root,root) %{_tmpfilesdir}/strongswan-starter.conf

%files sqlite
%{_libdir}/strongswan/plugins/libstrongswan-sqlite.so

%files tnc-imcvs
%{_sbindir}/sw-collector
%{_sbindir}/sec-updater
%dir %{_libdir}/strongswan/imcvs
%dir %{_libdir}/strongswan/plugins
%{_libdir}/strongswan/libimcv.so.*
%{_libdir}/strongswan/libtnccs.so.*
%{_libdir}/strongswan/plugins/libstrongswan-*tnc*.so
%{_libexecdir}/strongswan/attest
%{_libexecdir}/strongswan/pt-tls-client
%dir %{_datadir}/strongswan/swidtag
%{_datadir}/strongswan/swidtag/*.swidtag

%files libipsec
%{_libdir}/strongswan/libipsec.so.*
%{_libdir}/strongswan/plugins/libstrongswan-kernel-libipsec.so

%if %{with network_man}
%files charon-nm
%doc COPYING
%{_datadir}/dbus-1/system.d/nm-strongswan-service.conf
%{_libexecdir}/strongswan/charon-nm
%endif

%if %{with python3}
%files -n python3-vici
%license COPYING
%doc src/libcharon/plugins/vici/python/README.rst
%{python3_sitelib}/vici
%{python3_sitelib}/vici-%{version}-py*.egg-info
%endif

%if %{with perl}
%license COPYING
%files -n perl-vici
%{perl_vendorlib}/Vici
%endif

%changelog
* Mon Jan 19 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 5.9.14-8
- Patch for CVE-2025-62291

* Fri May 23 2025 Mayank Singh <mayansingh@microsoft.com> - 5.9.14-7
- Initial Azure Linux import from Fedora 42 (license: MIT).
- License verified

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 27 2024 Michel Lind <salimma@fedoraproject.org> - 5.9.14-5
- Depend on openssl-devel-engine since we still use this deprecated feature (rhbz#2295335)

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 5.9.14-4
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 5.9.14-2
- Rebuilt for Python 3.13

* Fri May 31 2024 Paul Wouters <paul.wouters@aiven.io> - 5.9.14-1
- Resolves: rhbz#2254560 CVE-2023-41913 buffer overflow and possible RCE
- Resolved: rhbz#2250666 Update to 5.9.14 (IKEv2 OCSP extensions, seqno/regno overflow handling
- Update to 5.9.13 (OCSP nonce set regression configuration option charon.ocsp_nonce_len)
- Update to 5.9.12 (CVE-2023-41913 fix, various IKEv2 fixes)

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Paul Wouters <paul.wouters@aiven.io - 5.9.11-1
- Resolves: rhbz#2214186 strongswan-5.9.11 is available

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 5.9.10-2
- Rebuilt for Python 3.12

* Thu Mar 02 2023 Paul Wouters <paul.wouters@aiven.io - 5.9.10-1
- Update to 5.9.10

* Tue Feb 28 2023 Paul Wouters <paul.wouters@aiven.io - 5.9.9-3
- Resolves: CVE-2023-26463 authorization bypass in TLS-based EAP methods

* Mon Jan 16 2023 Petr Menšík <pemensik@redhat.com> - 5.9.9-2
- Use configure paths in manual pages (#2106120)

* Sun Jan 15 2023 Petr Menšík <pemensik@redhat.com> - 5.9.9-1
- Update to 5.9.9 (#2157850)

* Thu Dec 08 2022 Jitka Plesnikova <jplesnik@redhat.com> - 5.9.8-2
- Add BR perl-generators to automatically generates run-time dependencies
  for installed Perl files

* Sun Oct 16 2022 Arne Reiter <redhat@arnereiter.de> - 5.9.8-1
- Resolves rhbz#2112274 strongswan-5.9.8 is available
- Patch1 removes CFLAGS -Wno-format which interferes with -Werror=format-security
- Add BuildRequire for autoconf and automake, now required for release
- Remove obsolete patches

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 22 2022 Arne Reiter <redhat@arnereiter.de> - 5.9.6-1
- Resolves rhbz#2080070 strongswan-5.9.6 is available
- Fixed missing format string in enum_flags_to_string()

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 5.9.5-4
- Rebuilt for Python 3.11

* Fri Feb 25 2022 Arne Reiter <redhat@arnereiter.de> - 5.9.5-3
- Resolves: rhbz#2048108 - segfault at 18 ip 00007f4c7c0d841c sp 00007ffe49f61b70 error 4 in libc.so.6

* Tue Jan 25 2022 Paul Wouters <paul.wouters@aiven.io> - 5.9.5-2
- Use newly published/cleaned strongswan gpg key

* Mon Jan 24 2022 Paul Wouters <paul.wouters@aiven.io> - 5.9.5-1
- Resolves rhbz#2044361 strongswan-5.9.5 is available (CVE-2021-45079)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 16 2021 Neal Gompa <ngompa@datto.com> - 5.9.4-4
- Disable TPM/TSS 1.2 support for F36+ / RHEL9+
- Resolves: rhbz#2033299 Drop TPM/TSS 1.2 support (trousers)

* Thu Nov 11 2021 Petr Menšík <pemensik@redhat.com> - 5.9.4-3
- Resolves rhbz#1419441 Add python and perl vici bindings
- Adds optional tests run

* Tue Nov 09 2021 Paul Wouters <paul.wouters@aiven.io> - 5.9.4-2
- Resolves rhbz#2018547 'strongswan restart' breaks ipsec started with strongswan-starter
- Return to using tmpfiles, but extend to cover strongswan-starter service too
- Cleanup old patches

* Wed Oct 20 2021 Paul Wouters <paul.wouters@aiven.io> - 5.9.4-1
- Resolves: rhbz#2015165 strongswan-5.9.4 is available
- Resolves: rhbz#2015611 CVE-2021-41990 strongswan: gmp plugin: integer overflow via a crafted certificate with an RSASSA-PSS signature
- Resolves: rhbz#2015614 CVE-2021-41991 strongswan: integer overflow when replacing certificates in cache
- Add BuildRequire for tpm2-tss-devel and weak dependency for tpm2-tools

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 5.9.3-4
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Björn Esser <besser82@fedoraproject.org> - 5.9.3-2
- Rebuild for versioned symbols in json-c

* Tue Jul 06 2021 Paul Wouters <paul.wouters@aiven.io> - 5.9.3-1
- Resolves: rhbz#1979574 strongswan-5.9.3 is available
- Make strongswan main dir world readable so apps can find strongswan.conf

* Thu Jun 03 2021 Paul Wouters <paul.wouters@aiven.io> - 5.9.2-1
- Resolves: rhbz#1896545 strongswan-5.9.2 is available

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.9.1-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Fri Feb 12 2021 Paul Wouters <pwouters@redhat.com> - 5.9.1-1
- Resolves: rhbz#1896545 strongswan-5.9.1 is available

* Thu Feb 11 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 5.9.0-4
- Build with with capabilities support
- Resolves: rhbz#1911572 StrongSwan not configured with libcap support

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 22 12:43:48 EDT 2020 Paul Wouters <pwouters@redhat.com> - 5.9.0-2
- Resolves: rhbz#1886759 charon looking for certificates in the wrong place

* Mon Sep 28 12:36:45 EDT 2020 Paul Wouters <pwouters@redhat.com> - 5.9.0-1
- Resolves: rhbz#1861747 strongswan-5.9.0 is available
- Remove --enable-fips-mode=2, which defaults strongswan to FIPS only.
  (use fips_mode = 2 in plugins {} openssl {} in strongswan.conf to enable FIPS)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.4-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Apr 21 2020 Björn Esser <besser82@fedoraproject.org> - 5.8.4-3
- Rebuild (json-c)

* Sun Apr 12 2020 Mikhail Zabaluev <mikhail.zabaluev@gmail.com> - 5.8.4-2
- Patch0: Add RuntimeDirectory options to service files (#1789263)

* Sun Apr 12 2020 Mikhail Zabaluev <mikhail.zabaluev@gmail.com> - 5.8.4-1
- Updated to 5.8.4
- Patch4 has been applied upstream

* Sat Feb 22 2020 Mikhail Zabaluev <mikhail.zabaluev@gmail.com> - 5.8.2-5
- Patch to declare a global variable with extern (#1800117)

* Mon Feb 10 2020 Paul Wouters <pwouters@redhat.com> - 5.8.2-4
- use tmpfile to ensure rundir is present

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 28 2019 Paul Wouters <pwouters@redhat.com> - 5.8.2-2
- Use /run/strongswan as rundir to support strongswans in namespaces

* Tue Dec 17 2019 Mikhail Zabaluev <mikhail.zabaluev@gmail.com> - 5.8.2-1
- Update to 5.8.2 (#1784457)
- The D-Bus config file moved under datadir

* Mon Sep 02 2019 Mikhail Zabaluev <mikhail.zabaluev@gmail.com> - 5.8.1-1
- Update to 5.8.1 (#1711920)
- No more separate strongswan-swanctl.service to start out of order (#1775548)
- Added strongswan-starter.service

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Paul Wouters <pwouters@redhat.com> - 5.7.2-1
- Updated to 5.7.2

* Thu Oct 04 2018 Mikhail Zabaluev <mikhail.zabaluev@gmail.com> - 5.7.1-1
- Updated to 5.7.1
- Resolves rhbz#1635872 CVE-2018-16152
- Resolves rhbz#1635875 CVE-2018-16151

* Thu Aug 23 2018 Mikhail Zabaluev <mikhail.zabaluev@gmail.com> - 5.6.3-3
- Add plugin bypass-lan, disabled by default
- Resolves rhbz#1554479 Update to strongswan-charon-nm fails

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 29 2018 Mikhail Zabaluev <mikhail.zabaluev@gmail.com> - 5.6.3-1
- New version 5.6.3

* Thu May 24 2018 Paul Wouters <pwouters@redhat.com> - 5.6.2-6
- Resolves rhbz#1581868 CVE-2018-5388 strongswan: buffer underflow in stroke_socket.c

* Thu May 24 2018 Paul Wouters <pwouters@redhat.com> - 5.6.2-5
- Resolves rhbz#1574939 IKEv2 VPN connections fail to use DNS servers provided by the server
- Resolves rhbz#1449875 Strongswan on epel built without the sql plugin but with the sqlite plugin

* Sun May 20 2018 Mikhail Zabaluev <mikhail.zabaluev@gmail.com> - 5.6.2-3
- Move eap-radius, sqlite, and pkcs7 plugins out of tnc-imcvs, added package
  sqlite (#1579945)

* Tue Mar 06 2018 Björn Esser <besser82@fedoraproject.org> - 5.6.2-2
- Rebuilt for libjson-c.so.4 (json-c v0.13.1)

* Wed Feb 21 2018 Lubomir Rintel <lkundrak@v3.sk> - 5.6.2-1
- Updated to 5.6.2 (Dropped libnm-glib use in charon-nm)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 22 2017 Paul Wouters <pwouters@redhat.com> - 5.6.1-1
- Updated to 5.6.1 (RSA-PSS support)

* Sun Dec 10 2017 Björn Esser <besser82@fedoraproject.org> - 5.6.0-3
- Rebuilt for libjson-c.so.3

* Fri Dec 01 2017 Lubomir Rintel <lkundrak@v3.sk> - 5.6.0-2
- Fix the placement of charon-nm D-Bus policy

* Sat Sep 09 2017 Paul Wouters <pwouters@redhat.com> - 5.6.0-1
- Updated to 5.6.0
- Fixup configure arguments, enabled a bunch of new features
- Added new BuildRequires:
- Fixup Obsolete/Conflicts, use license macro
- Don't require autoconf/autotools for non-snapshots
- Remove macro overuse, remove fedora/rhel checks and sysvinit support
- Make listings/grouping of all plugins/libs to reduce file listing

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Paul Wouters <pwouters@redhat.com> - 5.5.3-1
- Updated to 5.5.3

* Sat May 27 2017 Paul Wouters <pwouters@redhat.com> - 5.5.2-1
- Updated to 5.5.2

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 15 2016 Pavel Šimerda <psimerda@redhat.com> - 5.5.0-2
- Resolves: #1367796 - Enable the unity plugin

* Mon Aug 08 2016 Pavel Šimerda <psimerda@redhat.com> - 5.5.0-1
- New version 5.5.0

* Wed Jun 22 2016 Pavel Šimerda <psimerda@redhat.com>
- Enable IKEv2 GCM (requires gcrypt module as well) - merged from f22 by Paul Wouters

* Wed Jun 22 2016 Pavel Šimerda <psimerda@redhat.com> - 5.4.0-1
- New version 5.4.0

* Thu Mar 03 2016 Pavel Šimerda <psimerda@redhat.com> - 5.3.5-1
- New version 5.3.5

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Paul Wouters <pwouters@redhat.com> - 5.3.3-2
- Enable IKEv2 GCM (requires gcrypt module as well)

* Tue Sep 29 2015 Pavel Šimerda <psimerda@redhat.com> - 5.3.3-1
- new version 5.3.3

* Thu Sep 24 2015 Pavel Šimerda <psimerda@redhat.com> - 5.3.2-3
- Resolves: #1264598 - strongswan: many configuration files are not protected

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Pavel Šimerda <psimerda@redhat.com>
- new version 5.3.2

* Fri Jun 05 2015 Pavel Šimerda <psimerda@redhat.com> - 5.3.1-1
- new version 5.3.1

* Tue Mar 31 2015 Pavel Šimerda <psimerda@redhat.com> - 5.3.0-1
- new version 5.3.0

* Fri Feb 20 2015 Avesh Agarwal <avagarwa@redhat.com> - 5.2.2-2
- Fixes strongswan swanctl service issue rhbz#1193106

* Tue Jan 06 2015 Pavel Šimerda <psimerda@redhat.com> - 5.2.2-1
- new version 5.2.2

* Thu Dec 18 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.2.2-0.2.dr1
- Enabled ccm, and ctr plugins as it seems enabling just openssl does
  not work for using ccm and ctr algos.

* Mon Dec 8 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.2.2-0.1.dr1
- New strongswan developer release 5.2.2dr1

* Mon Nov 24 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.2.1-2
- 1167331: Enabled native systemd support.
- Does not disable old systemd, starter, ipsec.conf support yet.

* Thu Oct 30 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.2.1-1
- New upstream release 5.2.1

* Thu Oct 16 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.2.1-0.2.rc1
- New upstream release candidate 5.2.1rc1

* Fri Oct 10 2014 Pavel Šimerda <psimerda@redhat.com> - 5.2.1-1
- new version 5.2.1dr1

* Thu Sep 25 2014 Pavel Šimerda <psimerda@redhat.com> - 5.2.0-7
- use upstream patch for json/json-c dependency

* Thu Sep 25 2014 Pavel Šimerda <psimerda@redhat.com> - 5.2.0-6
- Resolves: #1146145 - Strongswan is compiled without xauth-noauth plugin

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Pavel Šimerda <psimerda@redhat.com> - 5.2.0-4
- Resolves: #1081804 - enable Kernel IPSec support

* Wed Jul 30 2014 Pavel Šimerda <psimerda@redhat.com> - 5.2.0-3
- rebuilt

* Tue Jul 29 2014 Pavel Šimerda <psimerda@redhat.com> - 5.2.0-2
- fix json-c dependency

* Tue Jul 15 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.2.0-1
- New upstream release 5.2.0
- The Attestation IMC/IMV pair supports the IMA-NG
  measurement format
- Aikgen tool to generate an Attestation Identity Key bound
  to a TPM
- Swanctl tool to provide a portable, complete IKE
  configuration and control interface for the command
  line using vici interface with libvici library
- PT-EAP transport protocol (RFC 7171) for TNC
- Enabled support for acert for checking X509 attribute certificate
- Updated patches, removed selinux patch as upstream has fixed it
  in this release.
- Updated spec file with minor cleanups

* Thu Jun 26 2014 Pavel Šimerda <psimerda@redhat.com> - 5.2.0-0.4.dr6
- improve prerelease macro

* Thu Jun 26 2014 Pavel Šimerda <psimerda@redhat.com> - 5.2.0-0.3
- Resolves: #1111895 - bump to 5.2.0dr6

* Thu Jun 12 2014 Pavel Šimerda <psimerda@redhat.com> - 5.2.0-0.2
- Related: #1087437 - remove or upstream all patches not specific to fedora/epel

* Thu Jun 12 2014 Pavel Šimerda <psimerda@redhat.com> - 5.2.0-0.1.dr5
- fix the pre-release version according to guidelines before it gets branched

* Fri Jun 06 2014 Pavel Šimerda <psimerda@redhat.com> - 5.2.0dr5-1
- new version 5.2.0dr5
- add json-c-devel to build deps

* Mon May 26 2014 Pavel Šimerda <psimerda@redhat.com> - 5.2.0dr4-3
- merge two related patches

* Mon May 26 2014 Pavel Šimerda <psimerda@redhat.com> - 5.2.0dr4-2
- clean up the patches a bit

* Thu May 22 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.2.0dr4-1
- New upstream developer release 5.2.0dr4
- Attestation IMV/IMC supports IMA-NG measurement format now
- Aikgen tool to generate an Attestation Identity Key bound
  to a TPM
- PT-EAP transport protocol (RFC 7171) for TNC
- vici plugin provides IKE Configuration Interface for charon
- Enabled support for acert for checking X509 attribute certificate
- Updated patches
- Updated spec file with minor cleanups

* Tue Apr 15 2014 Pavel Šimerda <psimerda@redhat.com> - 5.1.3-1
- new version 5.1.3

* Mon Apr 14 2014 Pavel Šimerda <psimerda@redhat.com> - 5.1.3rc1-1
- new version 5.1.3rc1

* Mon Mar 24 2014 Pavel Šimerda <psimerda@redhat.com> - 5.1.2-4
- #1069928 - updated libexec patch.

* Tue Mar 18 2014 Pavel Šimerda <psimerda@redhat.com> - 5.1.2-3
- fixed el6 initscript
- fixed pki directory location

* Fri Mar 14 2014 Pavel Šimerda <psimerda@redhat.com> - 5.1.2-2
- clean up the specfile a bit
- replace the initscript patch with an individual initscript
- patch to build for epel6

* Mon Mar 03 2014 Pavel Šimerda <psimerda@redhat.com> - 5.1.2-1
- #1071353 - bump to 5.1.2
- #1071338 - strongswan is compiled without xauth-pam plugin
- remove obsolete patches
- sent all patches upstream
- added comments to all patches
- don't touch the config with sed

* Thu Feb 20 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.1.1-6
- Fixed full hardening for strongswan (full relro and PIE).
  The previous macros had a typo and did not work
  (see bz#1067119).
- Fixed tnc package description to reflect the current state of
  the package.
- Fixed pki binary and moved it to /usr/libexece/strongswan as
  others binaries are there too.

* Wed Feb 19 2014 Pavel Šimerda <psimerda@redhat.com> - 5.1.1-5
- #903638 - SELinux is preventing /usr/sbin/xtables-multi from 'read' accesses on the chr_file /dev/random

* Thu Jan 09 2014 Pavel Šimerda <psimerda@redhat.com> - 5.1.1-4
- Removed redundant patches and *.spec commands caused by branch merging

* Wed Jan 08 2014 Pavel Šimerda <psimerda@redhat.com> - 5.1.1-3
- rebuilt

* Mon Dec 2 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.1.1-2
- Resolves: 973315
- Resolves: 1036844

* Fri Nov 1 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.1.1-1
- Support for PT-TLS  (RFC 6876)
- Support for SWID IMC/IMV
- Support for command line IKE client charon-cmd
- Changed location of pki to /usr/bin
- Added swid tags files
- Added man pages for pki and charon-cmd
- Renamed pki to strongswan-pki to avoid conflict with
  pki-core/pki-tools package.
- Update local patches
- Fixes CVE-2013-6075
- Fixes CVE-2013-6076
- Fixed autoconf/automake issue as configure.ac got changed
  and it required running autoreconf during the build process.
- added strongswan signature file to the sources.

* Thu Sep 12 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.1.0-3
- Fixed initialization crash of IMV and IMC particularly
  attestation imv/imc as libstrongswas was not getting
  initialized.

* Fri Aug 30 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.1.0-2
- Enabled fips support
- Enabled TNC's ifmap support
- Enabled TNC's pdp support
- Fixed hardocded package name in this spec file

* Wed Aug 7 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.1.0-1
- rhbz#981429: New upstream release
- Fixes CVE-2013-5018: rhbz#991216, rhbz#991215
- Fixes rhbz#991859 failed to build in rawhide
- Updated local patches and removed which are not needed
- Fixed errors around charon-nm
- Added plugins libstrongswan-pkcs12.so, libstrongswan-rc2.so,
  libstrongswan-sshkey.so
- Added utility imv_policy_manager

* Thu Jul 25 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 5.0.4-5
- rename strongswan-NetworkManager to strongswan-charon-nm
- fix enable_nm macro

* Mon Jul 15 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 5.0.4-4
- %%files tries to package some of the shared objects as directories (#984437)
- fix broken systemd unit file (#984300)
- fix rpmlint error: description-line-too-long
- fix rpmlint error: macro-in-comment
- fix rpmlint error: spelling-error Summary(en_US) fuctionality
- depend on 'systemd' instead of 'systemd-units'
- use new systemd scriptlet macros
- NetworkManager subpackage should have a copy of the license (#984490)
- enable hardened_build as this package meets the PIE criteria (#984429)
- invocation of "ipsec _updown iptables" is broken as ipsec is renamed
  to strongswan in this package (#948306)
- invocation of "ipsec scepclient" is broken as ipsec is renamed
  to strongswan in this package
- add /etc/strongswan/ipsec.d and missing subdirectories
- conditionalize building of strongswan-NetworkManager subpackage as the
  version of NetworkManager in EL6 is too old (#984497)

* Fri Jun 28 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.0.4-3
- Patch to fix a major crash issue when Freeradius loads
  attestatiom-imv and does not initialize libstrongswan which
  causes crash due to calls to PTS algorithms probing APIs.
  So this patch fixes the order of initialization. This issues
  does not occur with charon because libstrongswan gets
  initialized earlier.
- Patch that allows to outputs errors when there are permission
  issues when accessing strongswan.conf.
- Patch to make loading of modules configurable when libimcv
  is used in stand alone mode without charon with freeradius
  and wpa_supplicant.

* Tue Jun 11 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.0.4-2
- Enabled TNCCS 1.1 protocol
- Fixed libxm2-devel build dependency
- Patch to fix the issue with loading of plugins

* Wed May 1 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.0.4-1
- New upstream release
- Fixes for CVE-2013-2944
- Enabled support for OS IMV/IMC
- Created and applied a patch to disable ECP in fedora, because
  Openssl in Fedora does not allow ECP_256 and ECP_384. It makes
  it non-compliant to TCG's PTS standard, but there is no choice
  right now. see redhat bz # 319901.
- Enabled Trousers support for TPM based operations.

* Sat Apr 20 2013 Pavel Šimerda <psimerda@redhat.com> - 5.0.3-2
- Rebuilt for a single specfile for rawhide/f19/f18/el6

* Fri Apr 19 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.0.3-1
- New upstream release
- Enabled curl and eap-identity plugins
- Enabled support for eap-radius plugin.

* Thu Apr 18 2013 Pavel Šimerda <psimerda@redhat.com> - 5.0.2-3
- Add gettext-devel to BuildRequires because of epel6
- Remove unnecessary comments

* Tue Mar 19 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.0.2-2
- Enabled support for eap-radius plugin.

* Mon Mar 11 2013 Avesh Agarwal <avagarwa@redhat.com> - 5.0.2-1
- Update to upstream release 5.0.2
- Created sub package strongswan-tnc-imcvs that provides trusted network
  connect's IMC and IMV funtionality. Specifically it includes PTS
  based IMC/IMV for TPM based remote attestation and scanner and test
  IMCs and IMVs. The Strongswan's IMC/IMV dynamic libraries can be used
  by any third party TNC Client/Server implementation possessing a
  standard IF-IMC/IMV interface.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 04 2012 Pavel Šimerda <psimerda@redhat.com> - 5.0.1-1
- Update to release 5.0.1

* Thu Oct 04 2012 Pavel Šimerda <psimerda@redhat.com> - 5.0.0-4.git20120619
- Add plugins to interoperate with Windows 7 and Android (#862472)
  (contributed by Haim Gelfenbeyn)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.0-3.git20120619
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 08 2012 Pavel Šimerda <pavlix@pavlix.net> - 5.0.0-2.git20120619
- Fix configure substitutions in initscripts

* Wed Jul 04 2012 Pavel Šimerda <psimerda@redhat.com> - 5.0.0-1.git20120619
- Update to current upstream release
- Comment out all stuff that is only needed for git builds
- Remove renaming patch from git
- Improve init patch used for EPEL

* Thu Jun 21 2012 Pavel Šimerda <psimerda@redhat.com> - 5.0.0-0.3.git20120619
- Build with openssl plugin enabled

* Wed Jun 20 2012 Pavel Šimerda <psimerda@redhat.com> - 5.0.0-0.2.git20120619
- Add README.Fedora with link to 4.6 to 5.0 migration information

* Tue Jun 19 2012 Pavel Šimerda - 5.0.0-0.1.git20120619
- Snapshot of upcoming major release
- Move patches and renaming upstream
  http://wiki.strongswan.org/issues/194
  http://wiki.strongswan.org/issues/195
- Notified upstream about manpage issues

* Tue Jun 19 2012 Pavel Šimerda - 4.6.4-2
- Make initscript patch more distro-neutral
- Add links to bugreports for patches

* Fri Jun 01 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.4-1
- New upstream version (CVE-2012-2388)

* Sat May 26 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.3-2
- Add --enable-nm to configure
- Add NetworkManager-devel to BuildRequires
- Add NetworkManager-glib-devel to BuildRequires
- Add strongswan-NetworkManager package

* Sat May 26 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.3-1
- New version of Strongswan
- Support for RFC 3110 DNSKEY (see upstream changelog)
- Fix corrupt scriptlets

* Fri Mar 30 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.2-2
- #808612 - strongswan binary renaming side-effect

* Sun Feb 26 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.2-1
- New upstream version
- Changed from .tar.gz to .tar.bz2
- Added libstrongswan-pkcs8.so

* Wed Feb 15 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-8
- Fix initscript's status function

* Wed Feb 15 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-7
- Expand tabs in config files for better readability
- Add sysvinit script for epel6

* Wed Feb 15 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-6
- Fix program name in systemd unit file

* Tue Feb 14 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-5
- Improve fedora/epel conditionals

* Sat Jan 21 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-4
- Protect configuration directory from ordinary users
- Add still missing directory /etc/strongswan

* Fri Jan 20 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-3
- Change directory structure to avoid clashes with Openswan
- Prefixed all manpages with 'strongswan_'
- Every file now includes 'strongswan' somewhere in its path
- Removed conflict with Openswan
- Finally fix permissions on strongswan.conf

* Fri Jan 20 2012 Pavel Šimerda <pavlix@pavlix.net> - 4.6.1-2
- Change license tag from GPL to GPLv2+
- Change permissions on /etc/strongswan.conf to 644
- Rename ipsec.8 manpage to strongswan.8
- Fix empty scriptlets for non-fedora builds
- Add ldconfig scriptlet
- Add missing directories and files

* Sun Jan 01 2012 Pavel Šimerda <pavlix@pavlix.net - 4.6.1-1
- Bump to version 4.6.1

* Sun Jan 01 2012 Pavel Šimerda <pavlix@pavlix.net - 4.6.0-3
- Add systemd scriptlets
- Add conditions to also support EPEL6

* Sat Dec 10 2011 Pavel Šimerda <pavlix@pavlix.net> - 4.6.0-2
- Experimental build for development
