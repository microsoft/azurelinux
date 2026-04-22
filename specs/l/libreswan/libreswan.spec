## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _hardened_build 1
# These are rpm macros and are 0 or 1
%global with_efence 0
%global with_development 0
%global with_cavstests 1
%global nss_version 3.52
%global unbound_version 1.6.6
# Libreswan config options
%global libreswan_config \\\
    LIBEXECDIR=%{_libexecdir}/ipsec \\\
    MANDIR=%{_mandir} \\\
    PREFIX=%{_prefix} \\\
    INITSYSTEM=systemd \\\
    SBINDIR=%{_sbindir} \\\
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

#global prever dr1

Name: libreswan
Summary: Internet Key Exchange (IKEv1 and IKEv2) implementation for IPsec
# version is generated in the release script
Version: 5.3
Release: %autorelease
# The code in lib/libswan/nss_copies.c is under MPL-2.0, while the
# rest is under GPL-2.0-or-later
License: GPL-2.0-or-later AND MPL-2.0
Url: https://libreswan.org/
Source0: https://download.libreswan.org/%{?prever:development/}%{name}-%{version}%{?prever}.tar.gz
Source1: https://download.libreswan.org/%{?prever:development/}%{name}-%{version}%{?prever}.tar.gz.asc
Source2: https://download.libreswan.org/LIBRESWAN-OpenPGP-KEY.txt
%if 0%{with_cavstests}
Source3: https://download.libreswan.org/cavs/ikev1_dsa.fax.bz2
Source4: https://download.libreswan.org/cavs/ikev1_psk.fax.bz2
Source5: https://download.libreswan.org/cavs/ikev2.fax.bz2
%endif

Patch1: libreswan-4.15-ipsec_import.patch

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
BuildRequires: libxcrypt-devel
BuildRequires: make
BuildRequires: nspr-devel
BuildRequires: nss-devel >= %{nss_version}
BuildRequires: nss-tools >= %{nss_version}
BuildRequires: openldap-devel
BuildRequires: pam-devel
BuildRequires: pkgconfig
BuildRequires: systemd
BuildRequires: systemd-devel
BuildRequires: systemd-rpm-macros
BuildRequires: unbound-devel >= %{unbound_version}
BuildRequires: xmlto
%if 0%{with_efence}
BuildRequires: ElectricFence
%endif
Requires: iproute >= 2.6.8
Requires: nss >= %{nss_version}
Requires: nss-softokn
Requires: logrotate
# for pidof
Requires: procps-ng

Requires: %{name}-minimal%{?_isa} = %{version}-%{release}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/ipsec
%endif

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

%package minimal
Summary: Internet Key Exchange (IKEv1 and IKEv2) implementation for IPsec (minimal version)
Requires(post): bash
Requires(post): coreutils
Requires: nss-tools
Requires: unbound-libs >= %{unbound_version}

%description minimal
Libreswan is a free implementation of IPsec & IKE for Linux.  IPsec is
the Internet Protocol Security and uses strong cryptography to provide
both authentication and encryption services.  These services allow you
to build secure tunnels through untrusted networks.  Everything passing
through the untrusted net is encrypted by the ipsec gateway machine and
decrypted by the gateway at the other end of the tunnel.  The resulting
tunnel is a virtual private network or VPN.

This package contains the minimal set of daemons and userland tools
for setting up Libreswan.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q -n libreswan-%{version}%{?prever}
# enable crypto-policies support
sed -i "s:#[ ]*include \(.*\)\(/crypto-policies/back-ends/libreswan.config\)$:include \1\2:" configs/ipsec.conf.in
%ifarch s390x
# throws error on s390x
sed -i "s/SUBDIRS += hunkcheck/#SUBDIRS += hunkcheck/" testing/programs/Makefile
%endif
%autopatch -p1

%build
%make_build \
%if 0%{with_development}
    OPTIMIZE_CFLAGS="%{?_hardened_cflags}" \
%else
    OPTIMIZE_CFLAGS="%{optflags}" \
%endif
    WERROR_CFLAGS="-Werror -Wno-missing-field-initializers -Wno-lto-type-mismatch -Wno-maybe-uninitialized" \
%if 0%{with_efence}
    USE_EFENCE=true \
%endif
    USERLINK="%{?__global_ldflags} -Wl,-z,relro -Wl,--as-needed  -Wl,-z,now -flto --no-lto" \
    %{libreswan_config} \
    programs
FS=$(pwd)


%install
%make_install \
    %{libreswan_config} \
FS=$(pwd)
rm -rf %{buildroot}/usr/share/doc/libreswan
rm -rf %{buildroot}%{_libexecdir}/ipsec/*check
# avoids python depency and are old / aging tools that are not very useful
rm -rf %{buildroot}%{_libexecdir}/ipsec/show
rm -rf %{buildroot}%{_libexecdir}/ipsec/verify

install -d -m 0755 %{buildroot}%{_rundir}/pluto
install -d %{buildroot}%{_sbindir}

install -d %{buildroot}%{_sysctldir}
install -m 0644 packaging/fedora/libreswan-sysctl.conf \
    %{buildroot}%{_sysctldir}/50-libreswan.conf

echo "include %{_sysconfdir}/ipsec.d/*.secrets" \
    > %{buildroot}%{_sysconfdir}/ipsec.secrets
rm -fr %{buildroot}%{_sysconfdir}/rc.d/rc*

%if 0%{with_cavstests}
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
%endif

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

%post minimal
%sysctl_apply 50-libreswan.conf

%preun
%systemd_preun ipsec.service

%postun
%systemd_postun_with_restart ipsec.service

%files
%doc CHANGES COPYING CREDITS README* LICENSE
%doc docs/*.* docs/examples
%attr(0644,root,root) %{_unitdir}/ipsec.service
%doc %{_mandir}/*/*

%files minimal
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
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/pluto
%config(noreplace) %{_sysconfdir}/logrotate.d/libreswan
%{_sbindir}/ipsec
%{_libexecdir}/ipsec

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 5.3-4
- Latest state for libreswan

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Stephen Kitt <skitt@redhat.com> - 5.3-2
- Move the nss-tools requirement to libreswan-minimal for certutils. The
  unbound-libs requirement is also carried by the Libreswan binaries; since
  those are in -minimal, this moves the unbound-libs versioned requirement
  there as well.

* Fri Jul 04 2025 Paul Wouters <paul.wouters@aiven.io> - 5.3-1
- Update to libreswan-5.3

* Thu Apr 17 2025 Paul Wouters <pwouters@fedoraproject.org> - 5.2-2
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
