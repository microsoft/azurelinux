# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define ipa_requires_gt()  %(LC_ALL="C" echo '%*' | xargs -r rpm -q --qf 'Requires: %%{name} >= %%{epoch}:%%{version}-%%{release}\\n' | sed -e 's/ (none):/ /' -e 's/ 0:/ /' | grep -v "is not")

# ipatests enabled by default, can be disabled with --without ipatests
%bcond_without ipatests
# default to not use XML-RPC in Rawhide, can be turned around with --with ipa_join_xml
# On RHEL 8 we should use --with ipa_join_xml
%bcond_with ipa_join_xml

# Linting is disabled by default, needed for upstream testing
%bcond_with lint

# Build documentation with sphinx
%bcond_with doc

# Build Python wheels
%bcond_with wheels

# 389-ds-base 1.4 no longer supports i686 platform, build only client
# packages, https://bugzilla.redhat.com/show_bug.cgi?id=1544386
%ifarch %{ix86}
    %{!?ONLY_CLIENT:%global ONLY_CLIENT 1}
%endif

# Define ONLY_CLIENT to only make the ipa-client and ipa-python
# subpackages
%{!?ONLY_CLIENT:%global ONLY_CLIENT 0}
%if %{ONLY_CLIENT}
    %global enable_server_option --disable-server
%else
    %global enable_server_option --enable-server
%endif

%if %{ONLY_CLIENT}
    %global with_ipatests 0
%endif

# Whether to build ipatests
%if %{with ipatests}
    %global with_ipatests_option --with-ipatests
%else
    %global with_ipatests_option --without-ipatests
%endif

# Whether to use XML-RPC with ipa-join
%if %{with ipa_join_xml}
    %global with_ipa_join_xml_option --with-ipa-join-xml
%else
    %global with_ipa_join_xml_option --without-ipa-join-xml
%endif

# lint is not executed during rpmbuild
# %%global with_lint 1
%if %{with lint}
    %global linter_options --enable-pylint --without-jslint --enable-rpmlint
%else
    %global linter_options --disable-pylint --without-jslint --disable-rpmlint
%endif

# Include SELinux subpackage
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 8
    %global with_selinux 1
    %global selinuxtype targeted
    %global modulename ipa
%endif

%if 0%{?rhel}
%global package_name ipa
%global alt_name freeipa
%global krb5_version 1.20.1-1
%global krb5_kdb_version 9.0
# 0.7.16: https://github.com/drkjam/netaddr/issues/71
%global python_netaddr_version 0.7.19
%global samba_version 4.17.4-101
%global slapi_nis_version 0.56.4
%global python_ldap_version 3.1.0-1
%if 0%{?rhel} < 9
# Bug 1929067 - PKI instance creation failed with new 389-ds-base build
%global ds_version 1.4.3.16-12
%global selinux_policy_version 3.14.3-107
%else
# version supporting LMDB and lib389.cli_ctl.dblib.run_dbscan utility
%global ds_version 2.1.0
%global selinux_policy_version 38.1.1-1
%endif

# Fix for TLS 1.3 PHA, RHBZ#1775158
%global httpd_version 2.4.37-21

# DNSSEC support with OpenSSL provider API in RHEL 10
%if 0%{?rhel} < 10
%global bind_version 9.11.20-6
%else
%global bind_version 9.18.33-3
%endif

# support for passkey
%global sssd_version 2.9.0

%else
# Fedora
%global package_name freeipa
%global alt_name ipa
# 0.7.16: https://github.com/drkjam/netaddr/issues/71
%global python_netaddr_version 0.7.16
# Require 4.23 for passdb ABI bump
%global samba_version 2:4.23.0

# 38.28 or later includes passkey-related fixes
%global selinux_policy_version 38.28-1

%global slapi_nis_version 0.70.0

# Require new KDB ABI
%global krb5_version 1.21.2
%global krb5_kdb_version 9.0

# fix for segfault in python3-ldap, https://pagure.io/freeipa/issue/7324
%global python_ldap_version 3.1.0-1

# 389-ds-base version that fixes uniqueness plugin
# https://bodhi.fedoraproject.org/updates/FEDORA-2025-db214a095a
%global ds_version 3.1.3-7

# Fix for TLS 1.3 PHA, RHBZ#1775146
%global httpd_version 2.4.41-9

# Support for Encrypted DNS and OpenSSL Provider API
%if 0%{?fedora} < 42
%global bind_version 32:9.18.33-1
%else
# BIND version with backport of DNSSEC support over OpenSSL provider API
%global bind_version 32:9.18.35-2
%endif

# Don't use Fedora's Python dependency generator on Fedora 30/rawhide yet.
# Some packages don't provide new dist aliases.
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/
%{?python_disable_dependency_generator}

# Support for passkey
%global sssd_version 2.9.5

# Fedora
%endif

# BIND employs 'pkcs11' OpenSSL engine instead of native PKCS11
# Fedora 31+ uses OpenSSL engine, as well as RHEL9
# Howevever, Fedora 42+ and RHEL10+ use OpenSSL provider
%global openssl_pkcs11_version 1.0-1
%global openssl_pkcs11_name pkcs11-provider
%global softhsm_version 2.6.1

%if 0%{?rhel} == 8
# Make sure to use PKI versions that work with 389-ds fix for https://github.com/389ds/389-ds-base/issues/4609
%global pki_version 10.10.5
%else
# Make sure to use PKI versions that work with 389-ds fix for https://github.com/389ds/389-ds-base/issues/4609
%global pki_version 11.7.0
%endif

# for PKI-API to function
%global certmonger_version 0.79.21-1

# RHEL 8.2+, F32+ has 3.58
%global nss_version 3.44.0-4

%define krb5_base_version %(LC_ALL=C /usr/bin/pkgconf --modversion krb5 2>/dev/null | grep -Eo '^[^.]+\.[^.]+' || echo %krb5_version)
%global kdcproxy_version 0.4-3

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
# systemd with resolved enabled
# see https://pagure.io/freeipa/issue/8275
%global systemd_version 246.6-3
%else
%global systemd_version 239
%endif

# augeas support for new chrony options
# see https://pagure.io/freeipa/issue/8676
# https://bugzilla.redhat.com/show_bug.cgi?id=1931787
%if 0%{?fedora} >= 33
%global augeas_version 1.12.0-6
%else
%if 0%{?rhel} >= 9
%global augeas_version 1.12.1-0
%else
%global augeas_version 1.12.0-3
%endif
%endif

%global plugin_dir %{_libdir}/dirsrv/plugins
%global etc_systemd_dir %{_sysconfdir}/systemd/system
%global gettext_domain ipa

%define _hardened_build 1

# Work-around fact that RPM SPEC parser does not accept
# "Version: @VERSION@" in freeipa.spec.in used for Autoconf string replacement
%define IPA_VERSION 4.13.1
%global TARBALL_IPA_VERSION 4.13.1
# Release candidate version -- uncomment with one percent for RC versions
#%%global rc_version rc1
%define AT_SIGN @
# redefine IPA_VERSION only if its value matches the Autoconf placeholder
%if "%{IPA_VERSION}" == "%{AT_SIGN}VERSION%{AT_SIGN}"
    %define IPA_VERSION nonsense.to.please.RPM.SPEC.parser
%endif

%define NON_DEVELOPER_BUILD ("%{lua: print(rpm.expand('%{suffix:%IPA_VERSION}'):find('^dev'))}" == "nil")

Name:           %{package_name}
Version:        %{IPA_VERSION}
Release:        5%{?rc_version:.%rc_version}%{?dist}
Summary:        The Identity, Policy and Audit system

License:        GPL-3.0-or-later
URL:            http://www.freeipa.org/
Source0:        https://releases.pagure.org/freeipa/freeipa-%{TARBALL_IPA_VERSION}%{?rc_version}.tar.gz
# Only use detached signature for the distribution builds. If it is a developer build, skip it
%if %{NON_DEVELOPER_BUILD}
Source1:        https://releases.pagure.org/freeipa/freeipa-%{TARBALL_IPA_VERSION}%{?rc_version}.tar.gz.asc
# https://www.freeipa.org/page/Verify_Release_Signature
#
# The following commands can be used to fetch the signing key via fingerprint
# and extract it:
#   fpr=0E63D716D76AC080A4A33513F40800B6298EB963
#   gpg --keyserver keys.openpgp.org --receive-keys $fpr
#   gpg --armor --export-options export-minimal --export $fpr >gpgkey-$fpr.asc
Source2:        gpgkey-0E63D716D76AC080A4A33513F40800B6298EB963.asc
%endif
Patch0001:      0001-SELinux-expand-policy-coverage-for-Kerberos-usage.patch
Patch0002:      0002-ipa-sam-use-internal-Samba-method-to-populate-in-mem.patch

# RHEL spec file only: START: Change branding to IPA and Identity Management
# Moved branding logos and background to redhat-logos-ipa-80.4:
# header-logo.png, login-screen-background.jpg, login-screen-logo.png,
# product-name.png
# RHEL spec file only: END: Change branding to IPA and Identity Management

# RHEL spec file only: START
%if %{NON_DEVELOPER_BUILD}
%if 0%{?rhel} == 8
Patch1001:      1001-Change-branding-to-IPA-and-Identity-Management.patch
Patch1002:      1002-Revert-freeipa.spec-depend-on-bind-dnssec-utils.patch
%endif
%if 0%{?rhel} == 9
Patch1001:      1001-Change-branding-to-IPA-and-Identity-Management.patch
%endif
%endif
# RHEL spec file only: END

BuildRequires:  openldap-devel
# For KDB DAL version, make explicit dependency so that increase of version
# will cause the build to fail due to unsatisfied dependencies.
# DAL version change may cause code crash or memory leaks, it is better to fail early.
BuildRequires:  krb5-kdb-version = %{krb5_kdb_version}
BuildRequires:  krb5-kdb-devel-version = %{krb5_kdb_version}
BuildRequires:  krb5-devel >= %{krb5_version}
BuildRequires:  pkgconfig(krb5)
%if %{with ipa_join_xml}
# 1.27.4: xmlrpc_curl_xportparms.gssapi_delegation
BuildRequires:  xmlrpc-c-devel >= 1.27.4
%else
BuildRequires:  libcurl-devel
BuildRequires:  jansson-devel
%endif
BuildRequires:  popt-devel
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  pkgconf
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  libtool
BuildRequires:  gettext
BuildRequires:  gettext-devel
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-argcomplete
BuildRequires:  systemd >= %{systemd_version}
# systemd-tmpfiles which is executed from make install requires apache user
BuildRequires:  httpd
BuildRequires:  nspr-devel
BuildRequires:  openssl-devel
BuildRequires:  libini_config-devel
BuildRequires:  cyrus-sasl-devel
%if ! %{ONLY_CLIENT}
BuildRequires:  389-ds-base-devel >= %{ds_version}
BuildRequires:  samba-devel >= %{samba_version}
BuildRequires:  libtalloc-devel
BuildRequires:  libtevent-devel
BuildRequires:  libuuid-devel
BuildRequires:  libpwquality-devel
BuildRequires:  libsss_idmap-devel
BuildRequires:  libsss_certmap-devel
BuildRequires:  libsss_nss_idmap-devel >= %{sssd_version}
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 10
# Do not use nodejs22 on fedora < 41, https://pagure.io/freeipa/issue/9643
BuildRequires: nodejs(abi) == 127, /usr/bin/node, /usr/bin/npm
%elif 0%{?fedora} >= 39
# Do not use nodejs20 on fedora < 39, https://pagure.io/freeipa/issue/9374
BuildRequires:  nodejs(abi) < 127
%else
BuildRequires:  nodejs(abi) < 111
%endif
# Copr explicitely says no weak refs, so this has to be included
BuildRequires:  nodejs-npm
# use old dependency on RHEL 8 for now
%if 0%{?fedora} >= 31 || 0%{?rhel} >= 9
BuildRequires:  python3-rjsmin
%else
BuildRequires:  uglify-js
%endif
BuildRequires:  libverto-devel
BuildRequires:  libunistring-devel
# 0.13.0: https://bugzilla.redhat.com/show_bug.cgi?id=1584773
# 0.13.0-2: fix for missing dependency on python-six
BuildRequires:  python3-lesscpy >= 0.13.0-2
BuildRequires:  cracklib-dicts
# ONLY_CLIENT
%endif

#
# Build dependencies for makeapi/makeaci
#
BuildRequires:  python3-cffi
BuildRequires:  python3-dns
BuildRequires:  python3-ldap >= %{python_ldap_version}
BuildRequires:  python3-libsss_nss_idmap
BuildRequires:  python3-netaddr >= %{python_netaddr_version}
BuildRequires:  python3-pyasn1
BuildRequires:  python3-pyasn1-modules
BuildRequires:  python3-six
BuildRequires:  python3-psutil

#
# Build dependencies for wheel packaging and PyPI upload
#
%if %{with wheels}
BuildRequires:  dbus-glib-devel
BuildRequires:  libffi-devel
BuildRequires:  python3-tox
%if 0%{?fedora} <= 28
BuildRequires:  python3-twine
%else
BuildRequires:  twine
%endif
BuildRequires:  python3-wheel
# with_wheels
%endif

%if %{with doc}
BuildRequires: python3-sphinx
BuildRequires: plantuml
BuildRequires: fontconfig
BuildRequires: google-noto-sans-vf-fonts
%endif

#
# Build dependencies for lint and fastcheck
#
%if %{with lint}

# python3-pexpect might not be available in RHEL9
%if 0%{?fedora} || 0%{?rhel} < 9
BuildRequires:  python3-pexpect
%endif

# jsl is orphaned in Fedora 34+
%if 0%{?fedora} < 34
BuildRequires:  jsl
%endif

BuildRequires:  git
BuildRequires:  nss-tools
BuildRequires:  rpmlint
BuildRequires:  softhsm

BuildRequires:  keyutils
BuildRequires:  python3-augeas
BuildRequires:  python3-cffi
BuildRequires:  python3-cryptography >= 1.6
BuildRequires:  python3-dateutil
BuildRequires:  python3-dbus
BuildRequires:  python3-dns >= 1.15
BuildRequires:  python3-docker
BuildRequires:  python3-gssapi >= 1.2.0
BuildRequires:  python3-jinja2
BuildRequires:  python3-jwcrypto >= 0.4.2
BuildRequires:  python3-ldap >= %{python_ldap_version}
BuildRequires:  python3-ldap >= %{python_ldap_version}
BuildRequires:  python3-lib389 >= %{ds_version}
BuildRequires:  python3-libipa_hbac
BuildRequires:  python3-libsss_nss_idmap
BuildRequires:  python3-lxml
BuildRequires:  python3-netaddr >= %{python_netaddr_version}
BuildRequires:  python3-ifaddr
BuildRequires:  python3-pki >= %{pki_version}
BuildRequires:  python3-polib
BuildRequires:  python3-pyasn1
BuildRequires:  python3-pyasn1-modules
BuildRequires:  python3-pycodestyle
# .wheelconstraints.in limits pylint version in Azure and tox tests
BuildRequires:  python3-pylint
BuildRequires:  python3-pytest-multihost
BuildRequires:  python3-pytest-sourceorder
BuildRequires:  python3-qrcode-core >= 5.0.0
BuildRequires:  python3-samba
BuildRequires:  python3-six
BuildRequires:  python3-sss
BuildRequires:  python3-sss-murmur
BuildRequires:  python3-sssdconfig >= %{sssd_version}
BuildRequires:  python3-systemd
BuildRequires:  python3-yaml
BuildRequires:  python3-yubico
# with_lint
%endif

#
# Build dependencies for unit tests
#
%if ! %{ONLY_CLIENT}
BuildRequires:  libcmocka-devel
# Required by ipa_kdb_tests
BuildRequires:  krb5-server >= %{krb5_version}
# ONLY_CLIENT
%endif

# Build dependencies for SELinux policy
%if %{with selinux}
BuildRequires:  selinux-policy-devel >= %{selinux_policy_version}
%endif

%description
IPA is an integrated solution to provide centrally managed Identity (users,
hosts, services), Authentication (SSO, 2FA), and Authorization
(host access control, SELinux user roles, services). The solution provides
features for further integration with Linux based clients (SUDO, automount)
and integration with Active Directory based infrastructures (Trusts).


%if ! %{ONLY_CLIENT}

%package server
Summary: The IPA authentication server
Requires: %{name}-server-common = %{version}-%{release}
Requires: %{name}-client = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Requires: python3-ipaserver = %{version}-%{release}
Requires: python3-ldap >= %{python_ldap_version}
Requires: 389-ds-base >= %{ds_version}
Requires: openldap-clients > 2.4.35-4
Requires: nss-tools >= %{nss_version}
Requires(post): krb5-server >= %{krb5_version}
Requires(post): krb5-server >= %{krb5_base_version}
Requires: krb5-kdb-version = %{krb5_kdb_version}
Requires: cyrus-sasl-gssapi%{?_isa}
Requires: chrony
Requires: httpd >= %{httpd_version}
Requires(preun): python3
Requires(postun): python3
Requires: python3-gssapi >= 1.2.0-5
Requires: python3-systemd
Requires: python3-mod_wsgi
Requires: mod_auth_gssapi >= 1.5.0
Requires: mod_ssl >= %{httpd_version}
Requires: mod_session >= %{httpd_version}
# 0.9.9: https://github.com/adelton/mod_lookup_identity/pull/3
Requires: mod_lookup_identity >= 0.9.9
Requires: acl
Requires: systemd-units >= %{systemd_version}
Requires(pre): systemd-units >= %{systemd_version}
Requires(post): systemd-units >= %{systemd_version}
Requires(preun): systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}
Requires(pre): shadow-utils
Requires: selinux-policy >= %{selinux_policy_version}
Requires(post): selinux-policy-base >= %{selinux_policy_version}
Requires: slapi-nis >= %{slapi_nis_version}
Requires: pki-ca >= %{pki_version}
Requires: pki-kra >= %{pki_version}
# pki-acme package was split out in pki-10.10.0
Requires: (pki-acme >= %{pki_version} if pki-ca >= 10.10.0)
Requires: policycoreutils >= 2.1.12-5
Requires: tar
Requires(pre): certmonger >= %{certmonger_version}
Requires(pre): 389-ds-base >= %{ds_version}
Requires: font(fontawesome)
Requires: open-sans-fonts
%if 0%{?fedora} >= 32 || 0%{?rhel} >= 9
# https://pagure.io/freeipa/issue/8632
Requires: openssl > 1.1.1i
%else
Requires: openssl
%endif
Requires: softhsm >= 2.0.0rc1-1
Requires: p11-kit
Requires: %{etc_systemd_dir}
Requires: gzip
Requires: oddjob
# 0.7.0-2: https://pagure.io/gssproxy/pull-request/172
Requires: gssproxy >= 0.7.0-2
Requires: sssd-dbus >= %{sssd_version}
Requires: libpwquality
Requires: cracklib-dicts
# NDR libraries are internal in Samba and change with version without changing SONAME
%ipa_requires_gt samba-client-libs

Provides: %{alt_name}-server = %{version}
Conflicts: %{alt_name}-server
Obsoletes: %{alt_name}-server < %{version}

# With FreeIPA 3.3, package freeipa-server-selinux was obsoleted as the
# entire SELinux policy is stored in the system policy
Obsoletes: freeipa-server-selinux < 3.3.0

# upgrade path from monolithic -server to -server + -server-dns
Obsoletes: %{name}-server <= 4.2.0

# Versions of nss-pam-ldapd < 0.8.4 require a mapping from uniqueMember to
# member.
Conflicts: nss-pam-ldapd < 0.8.4

# RHEL spec file only: START: Do not build tests
%if 0%{?rhel} == 8
# ipa-tests subpackage was moved to separate srpm
Conflicts: ipa-tests < 3.3.3-9
%endif
# RHEL spec file only: END: Do not build tests

%description server
IPA is an integrated solution to provide centrally managed Identity (users,
hosts, services), Authentication (SSO, 2FA), and Authorization
(host access control, SELinux user roles, services). The solution provides
features for further integration with Linux based clients (SUDO, automount)
and integration with Active Directory based infrastructures (Trusts).
If you are installing an IPA server, you need to install this package.


%package -n python3-ipaserver
Summary: Python libraries used by IPA server
BuildArch: noarch
%{?python_provide:%python_provide python3-ipaserver}
Requires: %{name}-server-common = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
# we need pre-requires since earlier versions may break upgrade
Requires(pre): python3-ldap >= %{python_ldap_version}
Requires: python3-augeas
Requires: augeas-libs >= %{augeas_version}
Requires: python3-dbus
Requires: python3-dns >= 1.15
Requires: python3-gssapi >= 1.2.0
Requires: python3-ipaclient = %{version}-%{release}
Requires: python3-kdcproxy >= %{kdcproxy_version}
Requires: python3-lxml
Requires: python3-pki >= %{pki_version}
Requires: python3-pyasn1 >= 0.3.2-2
Requires: python3-sssdconfig >= %{sssd_version}
Requires: python3-psutil
Requires: rpm-libs
%if 0%{?rhel}
Requires: python3-urllib3 >= 1.24.2-3
%else
# For urllib3.util.ssl_match_hostname
Requires: python3-urllib3 >= 1.25.8
%endif

%description -n python3-ipaserver
IPA is an integrated solution to provide centrally managed Identity (users,
hosts, services), Authentication (SSO, 2FA), and Authorization
(host access control, SELinux user roles, services). The solution provides
features for further integration with Linux based clients (SUDO, automount)
and integration with Active Directory based infrastructures (Trusts).
If you are installing an IPA server, you need to install this package.


%package server-common
Summary: Common files used by IPA server
BuildArch: noarch
Requires: %{name}-client-common = %{version}-%{release}
Requires: httpd >= %{httpd_version}
Requires: systemd-units >= %{systemd_version}
%if 0%{?rhel} >= 8 && ! 0%{?eln}
Requires: system-logos-ipa >= 80.4
%endif

# The list below is automatically generated by `fix-spec.sh -i` 
# from the install/freeipa-webui
Provides: bundled(npm(attr-accept)) = 2.2.5
Provides: bundled(npm(cookie)) = 1.0.2
Provides: bundled(npm(csstype)) = 3.1.3
Provides: bundled(npm(file-selector)) = 2.1.2
Provides: bundled(npm(focus-trap)) = 7.6.4
Provides: bundled(npm(freeipa-webui)) = 0.1.9
Provides: bundled(npm(immer)) = 10.1.1
Provides: bundled(npm(js-tokens)) = 4.0.0
Provides: bundled(npm(lodash)) = 4.17.21
Provides: bundled(npm(loose-envify)) = 1.4.0
Provides: bundled(npm(object-assign)) = 4.1.1
Provides: bundled(npm(@patternfly/patternfly)) = 6.3.1
Provides: bundled(npm(@patternfly/react-core)) = 6.3.1
Provides: bundled(npm(@patternfly/react-icons)) = 6.3.1
Provides: bundled(npm(@patternfly/react-styles)) = 6.3.1
Provides: bundled(npm(@patternfly/react-table)) = 6.3.1
Provides: bundled(npm(@patternfly/react-tokens)) = 6.3.1
Provides: bundled(npm(prop-types)) = 15.8.1
Provides: bundled(npm(qrcode.react)) = 4.2.0
Provides: bundled(npm(react)) = 18.3.1
Provides: bundled(npm(react-dom)) = 18.3.1
Provides: bundled(npm(react-dropzone)) = 14.3.8
Provides: bundled(npm(react-is)) = 16.13.1
Provides: bundled(npm(react-redux)) = 9.2.0
Provides: bundled(npm(react-router)) = 7.12.0
Provides: bundled(npm(redux)) = 5.0.1
Provides: bundled(npm(@reduxjs/toolkit)) = 2.6.1
Provides: bundled(npm(redux-thunk)) = 3.1.0
Provides: bundled(npm(reselect)) = 5.1.1
Provides: bundled(npm(scheduler)) = 0.23.2
Provides: bundled(npm(set-cookie-parser)) = 2.7.1
Provides: bundled(npm(tabbable)) = 6.2.0
Provides: bundled(npm(tiny-invariant)) = 1.3.3
Provides: bundled(npm(tslib)) = 2.8.1
Provides: bundled(npm(@types/prop-types)) = 15.7.14
Provides: bundled(npm(@types/react)) = 18.3.20
Provides: bundled(npm(@types/use-sync-external-store)) = 0.0.6
Provides: bundled(npm(use-sync-external-store)) = 1.5.0
# end of generated list

Provides: %{alt_name}-server-common = %{version}
Conflicts: %{alt_name}-server-common
Obsoletes: %{alt_name}-server-common < %{version}

%description server-common
IPA is an integrated solution to provide centrally managed Identity (users,
hosts, services), Authentication (SSO, 2FA), and Authorization
(host access control, SELinux user roles, services). The solution provides
features for further integration with Linux based clients (SUDO, automount)
and integration with Active Directory based infrastructures (Trusts).
If you are installing an IPA server, you need to install this package.


%package server-dns
Summary: IPA integrated DNS server with support for automatic DNSSEC signing
BuildArch: noarch
Requires: %{name}-server = %{version}-%{release}
Requires: bind-dyndb-ldap >= 11.11-3
Requires: bind >= %{bind_version}
Requires: bind-utils >= %{bind_version}
# bind-dnssec-utils is required by the OpenDNSSec integration
# https://pagure.io/freeipa/issue/9026
Requires: bind-dnssec-utils >= %{bind_version}
%if %{with bind_pkcs11}
Requires: bind-pkcs11 >= %{bind_version}
%else
Requires: softhsm >= %{softhsm_version}
Requires: %{openssl_pkcs11_name} >= %{openssl_pkcs11_version}
%endif
# See https://bugzilla.redhat.com/show_bug.cgi?id=1825812
# RHEL 8.3+ and Fedora 32+ have 2.1
Requires: opendnssec >= 2.1.6-5
%if 0%{?fedora} >= 42 || 0%{?rhel} > 9
Recommends: %{name}-server-encrypted-dns
%endif
%{?systemd_requires}

Provides: %{alt_name}-server-dns = %{version}
Conflicts: %{alt_name}-server-dns
Obsoletes: %{alt_name}-server-dns < %{version}

# upgrade path from monolithic -server to -server + -server-dns
Obsoletes: %{name}-server <= 4.2.0

%description server-dns
IPA integrated DNS server with support for automatic DNSSEC signing.
Integrated DNS server is BIND 9. OpenDNSSEC provides key management.


%package server-encrypted-dns
Summary: support for encrypted DNS in IPA integrated DNS server
Requires: %{name}-client-encrypted-dns
# Will need newer bind-dyndb-ldap to allow use of OpenSSL provider API
Requires: bind-dyndb-ldap >= 11.11

%description server-encrypted-dns
Provides support for enabling DNS over TLS in the IPA integrated DNS
server.


%package server-trust-ad
Summary: Virtual package to install packages required for Active Directory trusts
Requires: %{name}-server = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}

Requires: samba >= %{samba_version}
Requires: samba-winbind
Requires: sssd-winbind-idmap
Requires: libsss_idmap
%if 0%{?rhel}
Obsoletes: ipa-idoverride-memberof-plugin <= 0.1
%endif
Requires(post): python3
Requires: python3-samba
Requires: python3-libsss_nss_idmap
Requires: python3-sss

# We use alternatives to divert winbind_krb5_locator.so plugin to libkrb5
# on the installes where server-trust-ad subpackage is installed because
# IPA AD trusts cannot be used at the same time with the locator plugin
# since Winbindd will be configured in a different mode
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Requires(preun): %{_sbindir}/update-alternatives

Provides: %{alt_name}-server-trust-ad = %{version}
Conflicts: %{alt_name}-server-trust-ad
Obsoletes: %{alt_name}-server-trust-ad < %{version}

%description server-trust-ad
Cross-realm trusts with Active Directory in IPA require working Samba 4
installation. This package is provided for convenience to install all required
dependencies at once.

# ONLY_CLIENT
%endif


%package client
Summary: IPA authentication for use on clients
Requires: %{name}-client-common = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Requires: python3-gssapi >= 1.2.0-5
Requires: python3-ipaclient = %{version}-%{release}
Requires: python3-ldap >= %{python_ldap_version}
Requires: python3-sssdconfig >= %{sssd_version}
Requires: cyrus-sasl-gssapi%{?_isa}
Requires: chrony
Requires: krb5-workstation >= %{krb5_version}
# support pkinit with client install
Requires: krb5-pkinit-openssl >= %{krb5_version}
# authselect: sssd profile with-subid
%if 0%{?fedora} >= 36
Requires: authselect >= 1.4.0
%else
Requires: authselect >= 1.2.5
%endif
Requires: curl
# NIS domain name config: /usr/lib/systemd/system/*-domainname.service
# All Fedora 28+ and RHEL8+ contain the service in hostname package
Requires: hostname
Requires: libcurl >= 7.21.7-2
%if %{with ipa_join_xml}
Requires: xmlrpc-c >= 1.27.4
%else
Requires: jansson
%endif
Requires: sssd-ipa >= %{sssd_version}
Requires: sssd-idp >= %{sssd_version}
Requires: sssd-krb5 >= %{sssd_version}
Requires: certmonger >= %{certmonger_version}
Requires: nss-tools >= %{nss_version}
Requires: bind-utils
Requires: oddjob-mkhomedir
Requires: libsss_autofs
Requires: autofs
Requires: libnfsidmap
Requires: (nfs-utils or nfsv4-client-utils)
Requires: sssd-tools >= %{sssd_version}
Requires(post): policycoreutils
Recommends: %{name}-client-encrypted-dns

# https://pagure.io/freeipa/issue/8530
Recommends: libsss_sudo
Recommends: sudo
Requires: (libsss_sudo if sudo)

# Passkey support
Recommends: sssd-passkey

Provides: %{alt_name}-client = %{version}
Conflicts: %{alt_name}-client
Obsoletes: %{alt_name}-client < %{version}

Provides: %{alt_name}-admintools = %{version}
Conflicts: %{alt_name}-admintools
Obsoletes: %{alt_name}-admintools < 4.4.1

Obsoletes: %{name}-admintools < 4.4.1
Provides: %{name}-admintools = %{version}-%{release}

%if 0%{?rhel} == 8
# Conflict with crypto-policies < 20200629-1 to get AD-SUPPORT policy module
Conflicts: crypto-policies < 20200629-1
%endif

%if 0%{?rhel} == 9
# Conflict with crypto-policies < 20220223-1 to get upgraded AD-SUPPORT and
# AD-SUPPORT-LEGACY policy modules
Conflicts: crypto-policies < 20220223-1
%endif

%description client
IPA is an integrated solution to provide centrally managed Identity (users,
hosts, services), Authentication (SSO, 2FA), and Authorization
(host access control, SELinux user roles, services). The solution provides
features for further integration with Linux based clients (SUDO, automount)
and integration with Active Directory based infrastructures (Trusts).
If your network uses IPA for authentication, this package should be
installed on every client machine.
This package provides command-line tools for IPA administrators.

%package client-encrypted-dns
Summary: Enable encrypted DNS support for clients
Requires: unbound

%description client-encrypted-dns
This package enables support for installing clients with encrypted DNS
via DNS over TLS.

%package client-samba
Summary: Tools to configure Samba on IPA client
Group: System Environment/Base
Requires: %{name}-client = %{version}-%{release}
Requires: python3-samba
Requires: samba-client
Requires: samba-winbind
Requires: samba-common-tools
Requires: samba
Requires: sssd-winbind-idmap
Requires: tdb-tools
Requires: cifs-utils

%description client-samba
This package provides command-line tools to deploy Samba domain member
on the machine enrolled into a FreeIPA environment

%package client-epn
Summary: Tools to configure Expiring Password Notification in IPA
Group: System Environment/Base
Requires: %{name}-client = %{version}-%{release}
Requires: systemd-units >= %{systemd_version}
Requires(post): systemd-units >= %{systemd_version}
Requires(preun): systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}

%description client-epn
This package provides a service to collect and send expiring password
notifications via email (SMTP).

%package -n python3-ipaclient
Summary: Python libraries used by IPA client
BuildArch: noarch
%{?python_provide:%python_provide python3-ipaclient}
Requires: %{name}-client-common = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Requires: python3-ipalib = %{version}-%{release}
Requires: python3-augeas
Requires: augeas-libs >= %{augeas_version}
Requires: python3-dns >= 1.15
Requires: python3-jinja2

%description -n python3-ipaclient
IPA is an integrated solution to provide centrally managed Identity (users,
hosts, services), Authentication (SSO, 2FA), and Authorization
(host access control, SELinux user roles, services). The solution provides
features for further integration with Linux based clients (SUDO, automount)
and integration with Active Directory based infrastructures (Trusts).
If your network uses IPA for authentication, this package should be
installed on every client machine.

%package client-common
Summary: Common files used by IPA client
BuildArch: noarch

Provides: %{alt_name}-client-common = %{version}
Conflicts: %{alt_name}-client-common
Obsoletes: %{alt_name}-client-common < %{version}
# python2-ipa* packages are no longer available in 4.8.
Obsoletes: python2-ipaclient < 4.8.0-1
Obsoletes: python2-ipalib < 4.8.0-1
Obsoletes: python2-ipaserver < 4.8.0-1
Obsoletes: python2-ipatests < 4.8.0-1


%description client-common
IPA is an integrated solution to provide centrally managed Identity (users,
hosts, services), Authentication (SSO, 2FA), and Authorization
(host access control, SELinux user roles, services). The solution provides
features for further integration with Linux based clients (SUDO, automount)
and integration with Active Directory based infrastructures (Trusts).
If your network uses IPA for authentication, this package should be
installed on every client machine.


%package python-compat
Summary: Compatiblity package for Python libraries used by IPA
BuildArch: noarch
Obsoletes: %{name}-python < 4.2.91
Provides: %{name}-python = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Requires: python3-ipalib = %{version}-%{release}

Provides: %{alt_name}-python-compat = %{version}
Conflicts: %{alt_name}-python-compat
Obsoletes: %{alt_name}-python-compat < %{version}

Obsoletes: %{alt_name}-python < 4.2.91
Provides: %{alt_name}-python = %{version}

%description python-compat
IPA is an integrated solution to provide centrally managed Identity (users,
hosts, services), Authentication (SSO, 2FA), and Authorization
(host access control, SELinux user roles, services). The solution provides
features for further integration with Linux based clients (SUDO, automount)
and integration with Active Directory based infrastructures (Trusts).
This is a compatibility package to accommodate %{name}-python split into
python3-ipalib and %{name}-common. Packages still depending on
%{name}-python should be fixed to depend on python2-ipaclient or
%{name}-common instead.


%package -n python3-ipalib
Summary: Python3 libraries used by IPA
BuildArch: noarch
%{?python_provide:%python_provide python3-ipalib}
Provides: python3-ipapython = %{version}-%{release}
%{?python_provide:%python_provide python3-ipapython}
Provides: python3-ipaplatform = %{version}-%{release}
%{?python_provide:%python_provide python3-ipaplatform}
Requires: %{name}-common = %{version}-%{release}
# we need pre-requires since earlier versions may break upgrade
Requires(pre): python3-ldap >= %{python_ldap_version}
Requires: gnupg2
Requires: keyutils
Requires: python3-argcomplete
Requires: python3-cffi
Requires: python3-cryptography >= 1.6
Requires: python3-dateutil
Requires: python3-dbus
Requires: python3-dns >= 1.15
Requires: python3-gssapi >= 1.2.0
Requires: python3-jwcrypto >= 0.4.2
Requires: python3-libipa_hbac
Requires: python3-netaddr >= %{python_netaddr_version}
Requires: python3-ifaddr
Requires: python3-packaging
Requires: python3-pyasn1 >= 0.3.2-2
Requires: python3-pyasn1-modules >= 0.3.2-2
Requires: python3-pyusb
Requires: python3-qrcode-core >= 5.0.0
Requires: python3-requests
Requires: python3-six
Requires: python3-sss-murmur
Requires: python3-yubico >= 1.3.2-7
%if 0%{?rhel}
Requires: python3-urllib3 >= 1.24.2-3
%else
# For urllib3.util.ssl_match_hostname
Requires: python3-urllib3 >= 1.25.8
%endif
Requires: python3-systemd

%description -n python3-ipalib
IPA is an integrated solution to provide centrally managed Identity (users,
hosts, services), Authentication (SSO, 2FA), and Authorization
(host access control, SELinux user roles, services). The solution provides
features for further integration with Linux based clients (SUDO, automount)
and integration with Active Directory based infrastructures (Trusts).
If you are using IPA with Python 3, you need to install this package.


%package common
Summary: Common files used by IPA
BuildArch: noarch
Conflicts: %{name}-python < 4.2.91

Provides: %{alt_name}-common = %{version}
Conflicts: %{alt_name}-common
Obsoletes: %{alt_name}-common < %{version}

Conflicts: %{alt_name}-python < %{version}

%if %{with selinux}
# This ensures that the *-selinux package and all it’s dependencies are not
# pulled into containers and other systems that do not use SELinux. The
# policy defines types and file contexts for client and server.
Requires:       (%{name}-selinux if selinux-policy-%{selinuxtype})
%endif

%description common
IPA is an integrated solution to provide centrally managed Identity (users,
hosts, services), Authentication (SSO, 2FA), and Authorization
(host access control, SELinux user roles, services). The solution provides
features for further integration with Linux based clients (SUDO, automount)
and integration with Active Directory based infrastructures (Trusts).
If you are using IPA, you need to install this package.


%if %{with ipatests}

%package -n python3-ipatests
Summary: IPA tests and test tools
BuildArch: noarch
%{?python_provide:%python_provide python3-ipatests}
Requires: python3-ipaclient = %{version}-%{release}
Requires: python3-ipaserver = %{version}-%{release}
Requires: iptables
Requires: python3-cryptography >= 1.6
%if 0%{?fedora}
# These packages do not exist on RHEL and for ipatests use
# they are installed on the controller through other means
Requires: ldns-utils
Requires: python3-pexpect
# update-crypto-policies
Requires: crypto-policies-scripts
Requires: python3-polib
Requires: python3-pytest >= 3.9.1
Requires: python3-pytest-multihost >= 0.5
Requires: python3-pytest-sourceorder
Requires: sshpass
%endif
Requires: python3-sssdconfig >= %{sssd_version}
Requires: tar
Requires: xz
Requires: openssh-clients
%if 0%{?rhel}
AutoReqProv: no
%endif

%description -n python3-ipatests
IPA is an integrated solution to provide centrally managed Identity (users,
hosts, services), Authentication (SSO, 2FA), and Authorization
(host access control, SELinux user roles, services). The solution provides
features for further integration with Linux based clients (SUDO, automount)
and integration with Active Directory based infrastructures (Trusts).
This package contains tests that verify IPA functionality under Python 3.

# with ipatests
%endif


%if %{with selinux}
# SELinux subpackage
%package selinux
Summary:             FreeIPA SELinux policy
BuildArch:           noarch
Requires:            selinux-policy-%{selinuxtype}
Requires(post):      selinux-policy-%{selinuxtype}
%{?selinux_requires}

%description selinux
Custom SELinux policy module for FreeIPA

%package selinux-nfast
Summary:             FreeIPA SELinux policy for nCipher nfast HSMs
BuildArch:           noarch
Requires:            selinux-policy-%{selinuxtype}
Requires(post):      selinux-policy-%{selinuxtype}
%{?selinux_requires}

%description selinux-nfast
Custom SELinux policy module for nCipher nfast HSMs

%package selinux-luna
Summary:             FreeIPA SELinux policy for Thales Luna HSMs
BuildArch:           noarch
Requires:            selinux-policy-%{selinuxtype}
Requires(post):      selinux-policy-%{selinuxtype}
%{?selinux_requires}

%description selinux-luna
Custom SELinux policy module for Thales Luna HSMs
# with selinux
%endif


%prep
# Verify release signature
%if %{NON_DEVELOPER_BUILD}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%endif

%autosetup -n freeipa-%{TARBALL_IPA_VERSION}%{?rc_version} -N -p1

# To allow proper application patches to the stripped po files, strip originals
pushd po
for i in *.po ; do
    msgattrib --translated --no-fuzzy --no-location -s $i > $i.tmp || exit 1
    mv $i.tmp $i || exit 1
done
popd

%if 0%{?fedora}>=41
    %global autopatch_options -q -p1
%else
    %global autopatch_options -p1
%endif
%autopatch %{autopatch_options}

%build
# PATH is workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1005235
export PATH=/usr/bin:/usr/sbin:$PATH

export PYTHON=%{__python3}

# Adjust minor release version because we actually applied all patches post 4.12.2
sed -i 's@IPA_VERSION_RELEASE, 2@IPA_VERSION_RELEASE, 5@' VERSION.m4

autoreconf -ivf
%configure --with-vendor-suffix=-%{release} \
           %{enable_server_option} \
           %{with_ipatests_option} \
           %{with_ipa_join_xml_option} \
           %{linter_options}

# run build in default dir
# -Onone is workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1398405
%make_build -Onone


%check
make %{?_smp_mflags} check VERBOSE=yes LIBDIR=%{_libdir}


%install
# Please put as much logic as possible into make install. It allows:
# - easier porting to other distributions
# - rapid devel & install cycle using make install
#   (instead of full RPM build and installation each time)
#
# All files and directories created by spec install should be marked as ghost.
# (These are typically configuration files created by IPA installer.)
# All other artifacts should be created by make install.

%make_install PACKAGE_NAME=%{package_name}

# don't package ipasphinx for now
rm -rf %{buildroot}%{python3_sitelib}/ipasphinx*

%if %{with ipatests}
mv %{buildroot}%{_bindir}/ipa-run-tests %{buildroot}%{_bindir}/ipa-run-tests-%{python3_version}
mv %{buildroot}%{_bindir}/ipa-test-config %{buildroot}%{_bindir}/ipa-test-config-%{python3_version}
mv %{buildroot}%{_bindir}/ipa-test-task %{buildroot}%{_bindir}/ipa-test-task-%{python3_version}
ln -rs %{buildroot}%{_bindir}/ipa-run-tests-%{python3_version} %{buildroot}%{_bindir}/ipa-run-tests-3
ln -rs %{buildroot}%{_bindir}/ipa-test-config-%{python3_version} %{buildroot}%{_bindir}/ipa-test-config-3
ln -rs %{buildroot}%{_bindir}/ipa-test-task-%{python3_version} %{buildroot}%{_bindir}/ipa-test-task-3
ln -frs %{buildroot}%{_bindir}/ipa-run-tests-%{python3_version} %{buildroot}%{_bindir}/ipa-run-tests
ln -frs %{buildroot}%{_bindir}/ipa-test-config-%{python3_version} %{buildroot}%{_bindir}/ipa-test-config
ln -frs %{buildroot}%{_bindir}/ipa-test-task-%{python3_version} %{buildroot}%{_bindir}/ipa-test-task
# with_ipatests
%endif

# remove files which are useful only for make uninstall
find %{buildroot} -wholename '*/site-packages/*/install_files.txt' -exec rm {} \;

%if 0%{?rhel}
# RHEL spec file only: START
# Moved branding logos and background to redhat-logos-ipa-80.4:
# header-logo.png, login-screen-background.jpg, login-screen-logo.png,
# product-name.png
rm -f %{buildroot}%{_usr}/share/ipa/ui/images/header-logo.png
rm -f %{buildroot}%{_usr}/share/ipa/ui/images/login-screen-background.jpg
rm -f %{buildroot}%{_usr}/share/ipa/ui/images/login-screen-logo.png
rm -f %{buildroot}%{_usr}/share/ipa/ui/images/product-name.png
%endif
# RHEL spec file only: END

%if ! %{ONLY_CLIENT}
%if 0%{?fedora}
# Register CLI tools for bash completion (fedora only)
for clitool in ipa-migrate
do
    register-python-argcomplete "${clitool}" > "${clitool}"
    install -p -m 0644 -D -t '%{buildroot}%{bash_completions_dir}' "${clitool}"
done
%endif
%endif

%find_lang %{gettext_domain}

%if ! %{ONLY_CLIENT}
# Remove .la files from libtool - we don't want to package
# these files
rm %{buildroot}/%{plugin_dir}/libipa_pwd_extop.la
rm %{buildroot}/%{plugin_dir}/libipa_enrollment_extop.la
rm %{buildroot}/%{plugin_dir}/libipa_winsync.la
rm %{buildroot}/%{plugin_dir}/libipa_repl_version.la
rm %{buildroot}/%{plugin_dir}/libipa_uuid.la
rm %{buildroot}/%{plugin_dir}/libipa_modrdn.la
rm %{buildroot}/%{plugin_dir}/libipa_lockout.la
rm %{buildroot}/%{plugin_dir}/libipa_cldap.la
rm %{buildroot}/%{plugin_dir}/libipa_dns.la
rm %{buildroot}/%{plugin_dir}/libipa_sidgen.la
rm %{buildroot}/%{plugin_dir}/libipa_sidgen_task.la
rm %{buildroot}/%{plugin_dir}/libipa_extdom_extop.la
rm %{buildroot}/%{plugin_dir}/libipa_range_check.la
rm %{buildroot}/%{plugin_dir}/libipa_otp_counter.la
rm %{buildroot}/%{plugin_dir}/libipa_otp_lasttoken.la
rm %{buildroot}/%{plugin_dir}/libipa_graceperiod.la
rm %{buildroot}/%{plugin_dir}/libtopology.la
rm %{buildroot}/%{_libdir}/krb5/plugins/kdb/ipadb.la
rm %{buildroot}/%{_libdir}/samba/pdb/ipasam.la

# So we can own our Apache configuration
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d/
/bin/touch %{buildroot}%{_sysconfdir}/httpd/conf.d/ipa.conf
/bin/touch %{buildroot}%{_sysconfdir}/httpd/conf.d/ipa-kdc-proxy.conf
/bin/touch %{buildroot}%{_sysconfdir}/httpd/conf.d/ipa-pki-proxy.conf
/bin/touch %{buildroot}%{_sysconfdir}/httpd/conf.d/ipa-rewrite.conf
/bin/touch %{buildroot}%{_usr}/share/ipa/html/ca.crt

mkdir -p %{buildroot}%{_libdir}/krb5/plugins/libkrb5
touch %{buildroot}%{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so

# ONLY_CLIENT
%endif

/bin/touch %{buildroot}%{_sysconfdir}/ipa/default.conf
/bin/touch %{buildroot}%{_sysconfdir}/ipa/ca.crt

%if ! %{ONLY_CLIENT}
mkdir -p %{buildroot}%{_sysconfdir}/cron.d
# ONLY_CLIENT
%endif

%if ! %{ONLY_CLIENT}

%post server
# NOTE: systemd specific section
    /bin/systemctl --system daemon-reload 2>&1 || :
# END
if [ $1 -gt 1 ] ; then
    /bin/systemctl condrestart certmonger.service 2>&1 || :
fi
/bin/systemctl reload-or-try-restart dbus
/bin/systemctl reload-or-try-restart oddjobd

%tmpfiles_create ipa.conf
%journal_catalog_update

%postun server
%journal_catalog_update

%posttrans server
# don't execute upgrade and restart of IPA when server is not installed
%{__python3} -c "import sys; from ipalib import facts; sys.exit(0 if facts.is_ipa_configured() else 1);" > /dev/null 2>&1

if [  $? -eq 0 ]; then
    # This is necessary for Fedora system upgrades which by default
    # work with the network being offline
    /bin/systemctl start network-online.target

    # Restart IPA processes. This must be also run in postrans so that plugins
    # and software is in consistent state. This will also perform the
    # system upgrade.
    # NOTE: systemd specific section

    /bin/systemctl is-enabled ipa.service >/dev/null 2>&1
    if [  $? -eq 0 ]; then
        /bin/systemctl restart ipa.service >/dev/null
    fi

    /bin/systemctl is-enabled ipa-ccache-sweep.timer >/dev/null 2>&1
    if [  $? -eq 1 ]; then
        /bin/systemctl enable ipa-ccache-sweep.timer>/dev/null
    fi
fi
# END


%preun server
if [ $1 = 0 ]; then
# NOTE: systemd specific section
    /bin/systemctl --quiet stop ipa.service || :
    /bin/systemctl --quiet disable ipa.service || :
    # Skip systemctl calls when leapp upgrade is in progress
    if [ -z "$LEAPP_IPU_IN_PROGRESS" ] ; then
        /bin/systemctl reload-or-try-restart dbus
        /bin/systemctl reload-or-try-restart oddjobd
    fi
# END
fi


%pre server
# Stop ipa_kpasswd if it exists before upgrading so we don't have a
# zombie process when we're done.
if [ -e /usr/sbin/ipa_kpasswd ]; then
# NOTE: systemd specific section
    /bin/systemctl stop ipa_kpasswd.service >/dev/null 2>&1 || :
# END
fi


%pre server-common
# create users and groups
# create kdcproxy group and user
getent group kdcproxy >/dev/null || groupadd -f -r kdcproxy
getent passwd kdcproxy >/dev/null || useradd -r -g kdcproxy -s /sbin/nologin -d / -c "IPA KDC Proxy User" kdcproxy
# create ipaapi group and user
getent group ipaapi >/dev/null || groupadd -f -r ipaapi
getent passwd ipaapi >/dev/null || useradd -r -g ipaapi -s /sbin/nologin -d / -c "IPA Framework User" ipaapi
# add apache to ipaaapi group
id -Gn apache | grep '\bipaapi\b' >/dev/null || usermod apache -a -G ipaapi


%post server-dns
%systemd_post ipa-dnskeysyncd.service ipa-ods-exporter.socket ipa-ods-exporter.service

%preun server-dns
%systemd_preun ipa-dnskeysyncd.service ipa-ods-exporter.socket ipa-ods-exporter.service

%postun server-dns
%systemd_postun ipa-dnskeysyncd.service ipa-ods-exporter.socket ipa-ods-exporter.service


%postun server-trust-ad
if [ "$1" -ge "1" ]; then
    if [ "`readlink %{_sysconfdir}/alternatives/winbind_krb5_locator.so`" == "/dev/null" ]; then
        %{_sbindir}/alternatives --set winbind_krb5_locator.so /dev/null
    fi
fi


%post server-trust-ad
%{_sbindir}/update-alternatives --install %{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so \
        winbind_krb5_locator.so /dev/null 90
/bin/systemctl reload-or-try-restart dbus >/dev/null 2>&1 || :
/bin/systemctl reload-or-try-restart oddjobd >/dev/null 2>&1 || :

%posttrans server-trust-ad
%{__python3} -c "import sys; from ipalib import facts; sys.exit(0 if facts.is_ipa_configured() else 1);" > /dev/null 2>&1
if [  $? -eq 0 ]; then
# NOTE: systemd specific section
    /bin/systemctl try-restart httpd.service >/dev/null 2>&1 || :
# END
fi


%preun server-trust-ad
if [ $1 -eq 0 ]; then
    %{_sbindir}/update-alternatives --remove winbind_krb5_locator.so /dev/null
    # Skip systemctl calls when leapp upgrade is in progress
    if [ -z "$LEAPP_IPU_IN_PROGRESS" ] ; then
        /bin/systemctl reload-or-try-restart dbus >/dev/null 2>&1 || :
        /bin/systemctl reload-or-try-restart oddjobd >/dev/null 2>&1 || :
    fi
fi

# ONLY_CLIENT
%endif

%preun client-epn
%systemd_preun ipa-epn.service
%systemd_preun ipa-epn.timer

%postun client-epn
%systemd_postun ipa-epn.service
%systemd_postun ipa-epn.timer

%post client-epn
%systemd_post ipa-epn.service
%systemd_post ipa-epn.timer

%post client
if [ $1 -gt 1 ] ; then
    # Has the client been configured?
    restore=0
    test -f '/var/lib/ipa-client/sysrestore/sysrestore.index' && restore=$(wc -l '/var/lib/ipa-client/sysrestore/sysrestore.index' | awk '{print $1}')

    if [ -f '/etc/sssd/sssd.conf' -a $restore -ge 2 ]; then
        if grep -E -q '/var/lib/sss/pubconf/krb5.include.d/' /etc/krb5.conf  2>/dev/null ; then
            sed -i '\;includedir /var/lib/sss/pubconf/krb5.include.d;d' /etc/krb5.conf
        fi
    fi

    if [ $restore -ge 2 ]; then
        if grep -E -q '\s*pkinit_anchors = FILE:/etc/ipa/ca.crt$' /etc/krb5.conf 2>/dev/null; then
            sed -E 's|(\s*)pkinit_anchors = FILE:/etc/ipa/ca.crt$|\1pkinit_anchors = FILE:/var/lib/ipa-client/pki/kdc-ca-bundle.pem\n\1pkinit_pool = FILE:/var/lib/ipa-client/pki/ca-bundle.pem|' /etc/krb5.conf >/etc/krb5.conf.ipanew
            mv -Z /etc/krb5.conf.ipanew /etc/krb5.conf
            cp /etc/ipa/ca.crt /var/lib/ipa-client/pki/kdc-ca-bundle.pem
            cp /etc/ipa/ca.crt /var/lib/ipa-client/pki/ca-bundle.pem
        fi
        %{__python3} -c 'from ipaclient.install.client import configure_krb5_snippet; configure_krb5_snippet()' >>/var/log/ipaupgrade.log 2>&1
        %{__python3} -c 'from ipaclient.install.client import update_ipa_nssdb; update_ipa_nssdb()' >>/var/log/ipaupgrade.log 2>&1
        chmod 0600 /var/log/ipaupgrade.log
        SSH_CLIENT_SYSTEM_CONF="/etc/ssh/ssh_config"
        if [ -f "$SSH_CLIENT_SYSTEM_CONF" ]; then
            if grep -E -q '^HostKeyAlgorithms ssh-rsa,ssh-dss' $SSH_CLIENT_SYSTEM_CONF 2>/dev/null; then
                sed -E --in-place=.orig 's/^(HostKeyAlgorithms ssh-rsa,ssh-dss)$/# disabled by ipa-client update\n# \1/' "$SSH_CLIENT_SYSTEM_CONF"
            fi
            # https://pagure.io/freeipa/issue/9536
            # replace sss_ssh_knownhostsproxy with sss_ssh_knownhosts
            if [ -f '/usr/bin/sss_ssh_knownhosts' ]; then
                if grep -E -q 'Include' $SSH_CLIENT_SYSTEM_CONF  2>/dev/null ; then
                    SSH_CLIENT_SYSTEM_CONF="/etc/ssh/ssh_config.d/04-ipa.conf"
                fi
                sed -E --in-place=.orig 's/^(GlobalKnownHostsFile \/var\/lib\/sss\/pubconf\/known_hosts)$/# disabled by ipa-client update\n# \1/' $SSH_CLIENT_SYSTEM_CONF || :
                sed -E --in-place=.orig 's/(ProxyCommand \/usr\/bin\/sss_ssh_knownhostsproxy -p \%p \%h)/# replaced by ipa-client update\n    KnownHostsCommand \/usr\/bin\/sss_ssh_knownhosts \%H/' $SSH_CLIENT_SYSTEM_CONF || :
            fi
        fi

        UNBOUND_CFG=/etc/unbound/conf.d/zzz-ipa.conf
        if [ -f "$UNBOUND_CFG" ]; then
            # The client has been configured for Dot
            # replace the line tls-cert-bundle: /etc/pki/tls/certs/ca-bundle.crt
            # with tls-system-cert: yes
            # See https://fedoraproject.org/wiki/Changes/droppingOfCertPemFile
            if grep -E -q 'tls-cert-bundle: \/etc\/pki\/tls\/certs\/ca-bundle.crt'  $UNBOUND_CFG 2>/dev/null; then
                sed -E --in-place=.orig 's/tls-cert-bundle: \/etc\/pki\/tls\/certs\/ca-bundle.crt/tls-system-cert: yes/' $UNBOUND_CFG
            fi
        fi
    fi
fi

%if %{with selinux}
# SELinux contexts are saved so that only affected files can be
# relabeled after the policy module installation
%pre selinux
%selinux_relabel_pre -s %{selinuxtype}

%post selinux
semodule -d ipa_custodia &> /dev/null || true;
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%post selinux-nfast
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}-nfast.pp.bz2

%post selinux-luna
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}-luna.pp.bz2

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
    semodule -e ipa_custodia &> /dev/null || true;
fi

%postun selinux-nfast
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}-nfast
fi

%postun selinux-luna
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}-luna
fi

%posttrans selinux
%selinux_relabel_post -s %{selinuxtype}
# with_selinux
%endif

%triggerin client -- sssd-common < 2.10
# Has the client been configured?
restore=0
test -f '/var/lib/ipa-client/sysrestore/sysrestore.index' && restore=$(wc -l '/var/lib/ipa-client/sysrestore/sysrestore.index' | awk '{print $1}')

if [ -f '/etc/ssh/sshd_config' -a $restore -ge 2 ]; then
    SSH_CLIENT_SYSTEM_CONF="/etc/ssh/ssh_config"
    if [ -f "$SSH_CLIENT_SYSTEM_CONF" ]; then
        # https://pagure.io/freeipa/issue/9536
        # downgrade sss_ssh_knownhosts with sss_ssh_knownhostsproxy
        if [ -f '/usr/bin/sss_ssh_knownhosts' ]; then
            if grep -E -q 'Include' $SSH_CLIENT_SYSTEM_CONF  2>/dev/null ; then
                SSH_CLIENT_SYSTEM_CONF="/etc/ssh/ssh_config.d/04-ipa.conf"
            fi
            GLOBALKNOWNHOSTFILE="GlobalKnownHostsFile /var/lib/sss/pubconf/known_hosts/"
            grep -qF '$GLOBALKNOWNHOSTFILE' $SSH_CLIENT_SYSTEM_CONF
            if [ $? -ne 0 ]; then
                sed -E --in-place=.orig '/(# IPA-related configuration changes to ssh_config)/a # added by ipa-client update\n'"$GLOBALKNOWNHOSTFILE"'' $SSH_CLIENT_SYSTEM_CONF
            fi
            sed -E --in-place=.orig 's/(KnownHostsCommand \/usr\/bin\/sss_ssh_knownhosts \%H)/ProxyCommand \/usr\/bin\/sss_ssh_knownhostsproxy -p \%p \%h/' $SSH_CLIENT_SYSTEM_CONF
        fi
    fi
fi

%triggerin client -- sssd-common >= 2.10
# Has the client been configured?
restore=0
test -f '/var/lib/ipa-client/sysrestore/sysrestore.index' && restore=$(wc -l '/var/lib/ipa-client/sysrestore/sysrestore.index' | awk '{print $1}')

if [ -f '/etc/ssh/sshd_config' -a $restore -ge 2 ]; then
    SSH_CLIENT_SYSTEM_CONF="/etc/ssh/ssh_config"
    if [ -f "$SSH_CLIENT_SYSTEM_CONF" ]; then
        # https://pagure.io/freeipa/issue/9536
        # upgrade sss_ssh_knownhostsproxy with sss_ssh_knownhosts
        if [ -f '/usr/bin/sss_ssh_knownhosts' ]; then
            if grep -E -q 'Include' $SSH_CLIENT_SYSTEM_CONF  2>/dev/null ; then
                SSH_CLIENT_SYSTEM_CONF="/etc/ssh/ssh_config.d/04-ipa.conf"
            fi
            sed -E --in-place=.orig 's/^(GlobalKnownHostsFile \/var\/lib\/sss\/pubconf\/known_hosts)$/# disabled by ipa-client update\n# \1/' $SSH_CLIENT_SYSTEM_CONF
            sed -E --in-place=.orig 's/(ProxyCommand \/usr\/bin\/sss_ssh_knownhostsproxy -p \%p \%h)/# replaced by ipa-client update\n    KnownHostsCommand \/usr\/bin\/sss_ssh_knownhosts \%H/' $SSH_CLIENT_SYSTEM_CONF
        fi
    fi
fi

%triggerin client -- openssh-server < 8.2
# Has the client been configured?
restore=0
test -f '/var/lib/ipa-client/sysrestore/sysrestore.index' && restore=$(wc -l '/var/lib/ipa-client/sysrestore/sysrestore.index' | awk '{print $1}')

if [ -f '/etc/ssh/sshd_config' -a $restore -ge 2 ]; then
    if grep -E -q '^(AuthorizedKeysCommand /usr/bin/sss_ssh_authorizedkeys|PubKeyAgent /usr/bin/sss_ssh_authorizedkeys %u)$' /etc/ssh/sshd_config 2>/dev/null; then
        sed -r '
            /^(AuthorizedKeysCommand(User|RunAs)|PubKeyAgentRunAs)[ \t]/ d
        ' /etc/ssh/sshd_config >/etc/ssh/sshd_config.ipanew

        if /usr/sbin/sshd -t -f /dev/null -o 'AuthorizedKeysCommand=/usr/bin/sss_ssh_authorizedkeys' -o 'AuthorizedKeysCommandUser=nobody' 2>/dev/null; then
            sed -ri '
                s/^PubKeyAgent (.+) %u$/AuthorizedKeysCommand \1/
                s/^AuthorizedKeysCommand .*$/\0\nAuthorizedKeysCommandUser nobody/
            ' /etc/ssh/sshd_config.ipanew
        elif /usr/sbin/sshd -t -f /dev/null -o 'AuthorizedKeysCommand=/usr/bin/sss_ssh_authorizedkeys' -o 'AuthorizedKeysCommandRunAs=nobody' 2>/dev/null; then
            sed -ri '
                s/^PubKeyAgent (.+) %u$/AuthorizedKeysCommand \1/
                s/^AuthorizedKeysCommand .*$/\0\nAuthorizedKeysCommandRunAs nobody/
            ' /etc/ssh/sshd_config.ipanew
        elif /usr/sbin/sshd -t -f /dev/null -o 'PubKeyAgent=/usr/bin/sss_ssh_authorizedkeys %u' -o 'PubKeyAgentRunAs=nobody' 2>/dev/null; then
            sed -ri '
                s/^AuthorizedKeysCommand (.+)$/PubKeyAgent \1 %u/
                s/^PubKeyAgent .*$/\0\nPubKeyAgentRunAs nobody/
            ' /etc/ssh/sshd_config.ipanew
        fi

        mv -Z /etc/ssh/sshd_config.ipanew /etc/ssh/sshd_config
        chmod 600 /etc/ssh/sshd_config

        /bin/systemctl condrestart sshd.service 2>&1 || :
    fi
fi


%triggerin client -- openssh-server >= 8.2
# Has the client been configured?
restore=0
test -f '/var/lib/ipa-client/sysrestore/sysrestore.index' && restore=$(wc -l '/var/lib/ipa-client/sysrestore/sysrestore.index' | awk '{print $1}')

if [ -f '/etc/ssh/sshd_config' -a $restore -ge 2 ]; then
    # If the snippet already exists, skip
    if [ ! -f '/etc/ssh/sshd_config.d/04-ipa.conf' ]; then
        # Take the values from /etc/ssh/sshd_config and put them in 04-ipa.conf
        grep -E '^(PubkeyAuthentication|KerberosAuthentication|GSSAPIAuthentication|UsePAM|ChallengeResponseAuthentication|AuthorizedKeysCommand|AuthorizedKeysCommandUser)' /etc/ssh/sshd_config 2>/dev/null > /etc/ssh/sshd_config.d/04-ipa.conf
        # Remove the values from sshd_conf
        sed -ri '
            /^(PubkeyAuthentication|KerberosAuthentication|GSSAPIAuthentication|UsePAM|ChallengeResponseAuthentication|AuthorizedKeysCommand|AuthorizedKeysCommandUser)[ \t]/ d
        ' /etc/ssh/sshd_config

        /bin/systemctl condrestart sshd.service 2>&1 || :
    fi
    # If the snippet has been created, ensure that it is included
    # either by /etc/ssh/sshd_config.d/*.conf or directly
    if [ -f '/etc/ssh/sshd_config.d/04-ipa.conf' ]; then
        if ! grep -E -q  '^\s*Include\s*/etc/ssh/sshd_config.d/\*\.conf' /etc/ssh/sshd_config 2> /dev/null ; then
            if ! grep -E -q '^\s*Include\s*/etc/ssh/sshd_config.d/04-ipa\.conf' /etc/ssh/sshd_config 2> /dev/null ; then
                # Include the snippet
                echo "Include /etc/ssh/sshd_config.d/04-ipa.conf" > /etc/ssh/sshd_config.ipanew
                cat /etc/ssh/sshd_config >> /etc/ssh/sshd_config.ipanew
                mv -fZ --backup=existing --suffix .ipaold /etc/ssh/sshd_config.ipanew /etc/ssh/sshd_config
            fi
        fi
    fi
fi


%if ! %{ONLY_CLIENT}

%files server
%doc README.md Contributors.txt
%license COPYING
%{_sbindir}/ipa-backup
%{_sbindir}/ipa-restore
%{_sbindir}/ipa-ca-install
%{_sbindir}/ipa-kra-install
%{_sbindir}/ipa-server-install
%{_sbindir}/ipa-replica-conncheck
%{_sbindir}/ipa-replica-install
%{_sbindir}/ipa-replica-manage
%{_sbindir}/ipa-csreplica-manage
%{_sbindir}/ipa-server-certinstall
%{_sbindir}/ipa-server-upgrade
%{_sbindir}/ipa-ldap-updater
%{_sbindir}/ipa-otptoken-import
%{_sbindir}/ipa-compat-manage
%{_sbindir}/ipa-managed-entries
%{_sbindir}/ipactl
%{_sbindir}/ipa-advise
%{_sbindir}/ipa-cacert-manage
%{_sbindir}/ipa-winsync-migrate
%{_sbindir}/ipa-pkinit-manage
%{_sbindir}/ipa-crlgen-manage
%{_sbindir}/ipa-cert-fix
%{_sbindir}/ipa-idrange-fix
%{_sbindir}/ipa-acme-manage
%{_sbindir}/ipa-migrate
%if 0%{?fedora} >= 38
%{bash_completions_dir}/ipa-migrate
%endif
%{_libexecdir}/certmonger/dogtag-ipa-ca-renew-agent-submit
%{_libexecdir}/certmonger/ipa-server-guard
%dir %{_libexecdir}/ipa
%{_libexecdir}/ipa/ipa-ccache-sweeper
%{_libexecdir}/ipa/ipa-custodia
%{_libexecdir}/ipa/ipa-custodia-check
%{_libexecdir}/ipa/ipa-httpd-kdcproxy
%{_libexecdir}/ipa/ipa-httpd-pwdreader
%{_libexecdir}/ipa/ipa-pki-retrieve-key
%{_libexecdir}/ipa/ipa-pki-wait-running
%{_libexecdir}/ipa/ipa-otpd
%{_libexecdir}/ipa/ipa-print-pac
%{_libexecdir}/ipa/ipa-subids
%dir %{_libexecdir}/ipa/custodia
%attr(755,root,root) %{_libexecdir}/ipa/custodia/ipa-custodia-dmldap
%attr(755,root,root) %{_libexecdir}/ipa/custodia/ipa-custodia-pki-tomcat
%attr(755,root,root) %{_libexecdir}/ipa/custodia/ipa-custodia-pki-tomcat-wrapped
%attr(755,root,root) %{_libexecdir}/ipa/custodia/ipa-custodia-ra-agent
%dir %{_libexecdir}/ipa/oddjob
%attr(0755,root,root) %{_libexecdir}/ipa/oddjob/org.freeipa.server.conncheck
%attr(0755,root,root) %{_libexecdir}/ipa/oddjob/org.freeipa.server.trust-enable-agent
%attr(0755,root,root) %{_libexecdir}/ipa/oddjob/org.freeipa.server.config-enable-sid
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freeipa.server.conf
%config(noreplace) %{_sysconfdir}/oddjobd.conf.d/ipa-server.conf
%dir %{_libexecdir}/ipa/certmonger
%attr(755,root,root) %{_libexecdir}/ipa/certmonger/*
# NOTE: systemd specific section
%attr(644,root,root) %{_unitdir}/ipa.service
%attr(644,root,root) %{_unitdir}/ipa-otpd.socket
%attr(644,root,root) %{_unitdir}/ipa-otpd@.service
%attr(644,root,root) %{_unitdir}/ipa-ccache-sweep.service
%attr(644,root,root) %{_unitdir}/ipa-ccache-sweep.timer
%attr(644,root,root) %{_journalcatalogdir}/ipa.catalog
# END
%attr(755,root,root) %{plugin_dir}/libipa_pwd_extop.so
%attr(755,root,root) %{plugin_dir}/libipa_enrollment_extop.so
%attr(755,root,root) %{plugin_dir}/libipa_winsync.so
%attr(755,root,root) %{plugin_dir}/libipa_repl_version.so
%attr(755,root,root) %{plugin_dir}/libipa_uuid.so
%attr(755,root,root) %{plugin_dir}/libipa_modrdn.so
%attr(755,root,root) %{plugin_dir}/libipa_lockout.so
%attr(755,root,root) %{plugin_dir}/libipa_dns.so
%attr(755,root,root) %{plugin_dir}/libipa_range_check.so
%attr(755,root,root) %{plugin_dir}/libipa_otp_counter.so
%attr(755,root,root) %{plugin_dir}/libipa_otp_lasttoken.so
%attr(755,root,root) %{plugin_dir}/libtopology.so
%attr(755,root,root) %{plugin_dir}/libipa_sidgen.so
%attr(755,root,root) %{plugin_dir}/libipa_sidgen_task.so
%attr(755,root,root) %{plugin_dir}/libipa_extdom_extop.so
%attr(755,root,root) %{plugin_dir}/libipa_graceperiod.so
%attr(755,root,root) %{_libdir}/krb5/plugins/kdb/ipadb.so
%{_mandir}/man1/ipa-replica-conncheck.1*
%{_mandir}/man1/ipa-replica-install.1*
%{_mandir}/man1/ipa-replica-manage.1*
%{_mandir}/man1/ipa-csreplica-manage.1*
%{_mandir}/man1/ipa-server-certinstall.1*
%{_mandir}/man1/ipa-server-install.1*
%{_mandir}/man1/ipa-server-upgrade.1*
%{_mandir}/man1/ipa-ca-install.1*
%{_mandir}/man1/ipa-kra-install.1*
%{_mandir}/man1/ipa-compat-manage.1*
%{_mandir}/man1/ipa-managed-entries.1*
%{_mandir}/man1/ipa-ldap-updater.1*
%{_mandir}/man8/ipactl.8*
%{_mandir}/man1/ipa-backup.1*
%{_mandir}/man1/ipa-restore.1*
%{_mandir}/man1/ipa-advise.1*
%{_mandir}/man1/ipa-otptoken-import.1*
%{_mandir}/man1/ipa-cacert-manage.1*
%{_mandir}/man1/ipa-winsync-migrate.1*
%{_mandir}/man1/ipa-pkinit-manage.1*
%{_mandir}/man1/ipa-crlgen-manage.1*
%{_mandir}/man1/ipa-cert-fix.1*
%{_mandir}/man1/ipa-idrange-fix.1*
%{_mandir}/man1/ipa-acme-manage.1*
%{_mandir}/man1/ipa-migrate.1*


%files -n python3-ipaserver
%doc README.md Contributors.txt
%license COPYING
%{python3_sitelib}/ipaserver
%{python3_sitelib}/ipaserver-*.egg-info


%files server-common
%doc README.md Contributors.txt
%license COPYING
%license %{_defaultlicensedir}/%{package_name}-server-common/modern-ui/COPYING
%ghost %verify(not owner group) %dir %{_sharedstatedir}/kdcproxy
%dir %attr(0755,root,root) %{_sysconfdir}/ipa/kdcproxy
%config(noreplace) %{_sysconfdir}/ipa/kdcproxy/kdcproxy.conf
# NOTE: systemd specific section
%{_tmpfilesdir}/ipa.conf
%attr(644,root,root) %{_unitdir}/ipa-custodia.service
%ghost %attr(644,root,root) %{etc_systemd_dir}/httpd.d/ipa.conf
# END
%dir %{_usr}/share/ipa
%{_usr}/share/ipa/wsgi.py*
%{_usr}/share/ipa/kdcproxy.wsgi
%{_usr}/share/ipa/ipaca*.ini
%{_usr}/share/ipa/*.ldif
%exclude %{_datadir}/ipa/ipa-cldap-conf.ldif
%{_usr}/share/ipa/*.uldif
%{_usr}/share/ipa/*.template
%dir %{_usr}/share/ipa/advise
%dir %{_usr}/share/ipa/advise/legacy
%{_usr}/share/ipa/advise/legacy/*.template
%dir %{_usr}/share/ipa/profiles
%{_usr}/share/ipa/profiles/README
%{_usr}/share/ipa/profiles/*.cfg
%dir %{_usr}/share/ipa/html
%{_usr}/share/ipa/html/ssbrowser.html
%{_usr}/share/ipa/html/unauthorized.html
%dir %{_usr}/share/ipa/migration
%{_usr}/share/ipa/migration/index.html
%{_usr}/share/ipa/migration/migration.py*
%{_usr}/share/ipa/modern-ui
%dir %{_usr}/share/ipa/ui
%{_usr}/share/ipa/ui/index.html
%{_usr}/share/ipa/ui/reset_password.html
%{_usr}/share/ipa/ui/sync_otp.html
%{_usr}/share/ipa/ui/*.ico
%{_usr}/share/ipa/ui/*.css
%dir %{_usr}/share/ipa/ui/css
%{_usr}/share/ipa/ui/css/*.css
%dir %{_usr}/share/ipa/ui/js
%dir %{_usr}/share/ipa/ui/js/dojo
%{_usr}/share/ipa/ui/js/dojo/dojo.js
%dir %{_usr}/share/ipa/ui/js/libs
%{_usr}/share/ipa/ui/js/libs/*.js
%dir %{_usr}/share/ipa/ui/js/freeipa
%{_usr}/share/ipa/ui/js/freeipa/app.js
%{_usr}/share/ipa/ui/js/freeipa/core.js
%dir %{_usr}/share/ipa/ui/js/plugins
%dir %{_usr}/share/ipa/ui/images
%if 0%{?rhel}
%{_usr}/share/ipa/ui/images/facet-*.png
# Moved branding logos and background to redhat-logos-ipa-80.4:
# header-logo.png, login-screen-background.jpg, login-screen-logo.png,
# product-name.png
%else
%{_usr}/share/ipa/ui/images/*.jpg
%{_usr}/share/ipa/ui/images/*.png
%endif
%dir %{_usr}/share/ipa/wsgi
%{_usr}/share/ipa/wsgi/plugins.py*
%dir %{_sysconfdir}/ipa
%dir %{_sysconfdir}/ipa/html
%config(noreplace) %{_sysconfdir}/ipa/html/ssbrowser.html
%config(noreplace) %{_sysconfdir}/ipa/html/unauthorized.html
%ghost %attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/ipa-rewrite.conf
%ghost %attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/ipa.conf
%ghost %attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/ipa-kdc-proxy.conf
%ghost %attr(0640,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/ipa-pki-proxy.conf
%ghost %attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ipa/kdcproxy/ipa-kdc-proxy.conf
%ghost %attr(0644,root,root) %config(noreplace) %{_usr}/share/ipa/html/ca.crt
%ghost %attr(0640,root,named) %config(noreplace) %{_sysconfdir}/named/ipa-ext.conf
%ghost %attr(0640,root,named) %config(noreplace) %{_sysconfdir}/named/ipa-options-ext.conf
%dir %{_usr}/share/ipa/updates/
%{_usr}/share/ipa/updates/*
%dir %{_localstatedir}/lib/ipa
%attr(700,root,root) %dir %{_localstatedir}/lib/ipa/backup
%attr(700,root,root) %dir %{_localstatedir}/lib/ipa/gssproxy
%attr(711,root,root) %dir %{_localstatedir}/lib/ipa/sysrestore
%attr(700,root,root) %dir %{_localstatedir}/lib/ipa/sysupgrade
%attr(755,root,root) %dir %{_localstatedir}/lib/ipa/pki-ca
%attr(755,root,root) %dir %{_localstatedir}/lib/ipa/certs
%attr(700,root,root) %dir %{_localstatedir}/lib/ipa/private
%attr(700,root,root) %dir %{_localstatedir}/lib/ipa/passwds
%ghost %attr(775,root,pkiuser) %{_localstatedir}/lib/ipa/pki-ca/publish
%ghost %attr(770,named,named) %{_localstatedir}/named/dyndb-ldap/ipa
%dir %attr(0700,root,root) %{_sysconfdir}/ipa/custodia
%dir %{_usr}/share/ipa/schema.d
%attr(0644,root,root) %{_usr}/share/ipa/schema.d/README
%attr(0644,root,root) %{_usr}/share/ipa/gssapi.login
%{_usr}/share/ipa/ipakrb5.aug

%files server-dns
%doc README.md Contributors.txt
%license COPYING
%config(noreplace) %{_sysconfdir}/sysconfig/ipa-dnskeysyncd
%config(noreplace) %{_sysconfdir}/sysconfig/ipa-ods-exporter
%dir %attr(0755,root,root) %{_sysconfdir}/ipa/dnssec
%{_libexecdir}/ipa/ipa-dnskeysyncd
%{_libexecdir}/ipa/ipa-dnskeysync-replica
%{_libexecdir}/ipa/ipa-ods-exporter
%{_sbindir}/ipa-dns-install
%{_mandir}/man1/ipa-dns-install.1*
%{_usr}/share/ipa/ipa-dnssec.conf
%attr(644,root,root) %{_unitdir}/ipa-dnskeysyncd.service
%attr(644,root,root) %{_unitdir}/ipa-ods-exporter.socket
%attr(644,root,root) %{_unitdir}/ipa-ods-exporter.service

%files server-encrypted-dns
%doc README.md Contributors.txt
%license COPYING

%files server-trust-ad
%doc README.md Contributors.txt
%license COPYING
%{_sbindir}/ipa-adtrust-install
%{_usr}/share/ipa/smb.conf.empty
%attr(755,root,root) %{_libdir}/samba/pdb/ipasam.so
%attr(755,root,root) %{plugin_dir}/libipa_cldap.so
%{_datadir}/ipa/ipa-cldap-conf.ldif
%{_mandir}/man1/ipa-adtrust-install.1*
%ghost %{_libdir}/krb5/plugins/libkrb5/winbind_krb5_locator.so
%{_sysconfdir}/dbus-1/system.d/oddjob-ipa-trust.conf
%{_sysconfdir}/oddjobd.conf.d/oddjobd-ipa-trust.conf
%attr(755,root,root) %{_libexecdir}/ipa/oddjob/com.redhat.idm.trust-fetch-domains

# ONLY_CLIENT
%endif


%files client
%doc README.md Contributors.txt
%license COPYING
%{_sbindir}/ipa-client-install
%{_sbindir}/ipa-client-automount
%{_sbindir}/ipa-certupdate
%{_sbindir}/ipa-getkeytab
%{_sbindir}/ipa-rmkeytab
%{_sbindir}/ipa-join
%{_bindir}/ipa
%config %{_sysconfdir}/bash_completion.d
%config %{_sysconfdir}/sysconfig/certmonger
%{_mandir}/man1/ipa.1*
%{_mandir}/man1/ipa-getkeytab.1*
%{_mandir}/man1/ipa-rmkeytab.1*
%{_mandir}/man1/ipa-client-install.1*
%{_mandir}/man1/ipa-client-automount.1*
%{_mandir}/man1/ipa-certupdate.1*
%{_mandir}/man1/ipa-join.1*
%dir %{_libexecdir}/ipa/acme
%{_libexecdir}/ipa/acme/certbot-dns-ipa

%files client-samba
%doc README.md Contributors.txt
%license COPYING
%{_sbindir}/ipa-client-samba
%{_mandir}/man1/ipa-client-samba.1*


%files client-epn
%doc README.md Contributors.txt
%dir %{_sysconfdir}/ipa/epn
%license COPYING
%{_sbindir}/ipa-epn
%{_mandir}/man1/ipa-epn.1*
%{_mandir}/man5/epn.conf.5*
%attr(644,root,root) %{_unitdir}/ipa-epn.service
%attr(644,root,root) %{_unitdir}/ipa-epn.timer
%attr(600,root,root) %config(noreplace) %{_sysconfdir}/ipa/epn.conf
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/ipa/epn/expire_msg.template

%files client-encrypted-dns
%doc README.md Contributors.txt
%license COPYING

%files -n python3-ipaclient
%doc README.md Contributors.txt
%license COPYING
%dir %{python3_sitelib}/ipaclient
%{python3_sitelib}/ipaclient/*.py
%{python3_sitelib}/ipaclient/__pycache__/*.py*
%dir %{python3_sitelib}/ipaclient/install
%{python3_sitelib}/ipaclient/install/*.py
%{python3_sitelib}/ipaclient/install/__pycache__/*.py*
%dir %{python3_sitelib}/ipaclient/plugins
%{python3_sitelib}/ipaclient/plugins/*.py
%{python3_sitelib}/ipaclient/plugins/__pycache__/*.py*
%dir %{python3_sitelib}/ipaclient/remote_plugins
%{python3_sitelib}/ipaclient/remote_plugins/*.py
%{python3_sitelib}/ipaclient/remote_plugins/__pycache__/*.py*
%dir %{python3_sitelib}/ipaclient/remote_plugins/2_*
%{python3_sitelib}/ipaclient/remote_plugins/2_*/*.py
%{python3_sitelib}/ipaclient/remote_plugins/2_*/__pycache__/*.py*
%{python3_sitelib}/ipaclient-*.egg-info


%files client-common
%doc README.md Contributors.txt
%license COPYING
%dir %attr(0755,root,root) %{_sysconfdir}/ipa/
%ghost %attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ipa/default.conf
%ghost %attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ipa/ca.crt
%dir %attr(0755,root,root) %{_sysconfdir}/ipa/nssdb
# old dbm format
%ghost %attr(644,root,root) %config(noreplace) %{_sysconfdir}/ipa/nssdb/cert8.db
%ghost %attr(644,root,root) %config(noreplace) %{_sysconfdir}/ipa/nssdb/key3.db
%ghost %attr(644,root,root) %config(noreplace) %{_sysconfdir}/ipa/nssdb/secmod.db
# new sql format
%ghost %attr(644,root,root) %config(noreplace) %{_sysconfdir}/ipa/nssdb/cert9.db
%ghost %attr(644,root,root) %config(noreplace) %{_sysconfdir}/ipa/nssdb/key4.db
%ghost %attr(644,root,root) %config(noreplace) %{_sysconfdir}/ipa/nssdb/pkcs11.txt
%ghost %attr(600,root,root) %config(noreplace) %{_sysconfdir}/ipa/nssdb/pwdfile.txt
%ghost %attr(644,root,root) %config(noreplace) %{_sysconfdir}/pki/ca-trust/source/ipa.p11-kit
%dir %{_localstatedir}/lib/ipa-client
%dir %{_localstatedir}/lib/ipa-client/pki
%dir %{_localstatedir}/lib/ipa-client/sysrestore
%{_mandir}/man5/default.conf.5*
%dir %{_usr}/share/ipa/client
%{_usr}/share/ipa/client/*.template


%files python-compat
%doc README.md Contributors.txt
%license COPYING


%files common -f %{gettext_domain}.lang
%doc README.md Contributors.txt
%license COPYING
%dir %{_usr}/share/ipa
%dir %{_libexecdir}/ipa

%files -n python3-ipalib
%doc README.md Contributors.txt
%license COPYING

%{python3_sitelib}/ipapython/
%{python3_sitelib}/ipalib/
%{python3_sitelib}/ipaplatform/
%{python3_sitelib}/ipapython-*.egg-info
%{python3_sitelib}/ipalib-*.egg-info
%{python3_sitelib}/ipaplatform-*.egg-info


%if %{with ipatests}


%files -n python3-ipatests
%doc README.md Contributors.txt
%license COPYING
%{python3_sitelib}/ipatests
%{python3_sitelib}/ipatests-*.egg-info
%{_bindir}/ipa-run-tests-3
%{_bindir}/ipa-test-config-3
%{_bindir}/ipa-test-task-3
%{_bindir}/ipa-run-tests-%{python3_version}
%{_bindir}/ipa-test-config-%{python3_version}
%{_bindir}/ipa-test-task-%{python3_version}
%{_bindir}/ipa-run-tests
%{_bindir}/ipa-test-config
%{_bindir}/ipa-test-task
%{_mandir}/man1/ipa-run-tests.1*
%{_mandir}/man1/ipa-test-config.1*
%{_mandir}/man1/ipa-test-task.1*

# with ipatests
%endif


%if %{with selinux}
%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}

%files selinux-nfast
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}-nfast.pp.*
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}-nfast

%files selinux-luna
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}-luna.pp.*
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}-luna
# with selinux
%endif

%changelog
* Wed Feb 18 2026 Alexander Bokovoy <abokovoy@redhat.com> - 4.13.1-5
- More changes to SELinux policy to help upgrade SSSD helpers' contexts

* Tue Feb 17 2026 Alexander Bokovoy <abokovoy@redhat.com> - 4.13.1-4
- Update SELinux policy to allow relabel SSSD helpers during install (rpm_t)

* Tue Feb 17 2026 Alexander Bokovoy <abokovoy@redhat.com> - 4.13.1-3
- Update SELinux policy to allow relabel SSSD helpers during install

* Tue Feb 17 2026 Alexander Bokovoy <abokovoy@redhat.com> - 4.13.1-2
- Rebuild against MIT Kerberos 1.22.2
- Fix build against NodeJS in F44/45
- Allow SELinux policy for ipa-otpd in non-IPA environment (standalone SSSD)
- Fix freeipa-client package scriptlet to not fail when config is missing
- Resolves: rhbz#2439482

* Fri Jan 16 2026 Rob Crittenden <rcritten@redhat.com> - 4.13.1-0.1
- Upstream release 4.13.1
- Release notes: https://www.freeipa.org/release-notes/4-13-1.html

* Fri Dec 05 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.13.0-2
- Fix upgrade to Samba 4.23 when there is already established trust
- Upstream PR: https://github.com/freeipa/freeipa/pull/8046

* Thu Dec 04 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.13.0-1
- Upstream release 4.13.0
- Release notes: https://www.freeipa.org/release-notes/4-13-0.html

* Fri Oct 03 2025 Adam Williamson <awilliam@redhat.com> - 4.12.5-3
- Rebuild with no changes to keep version ahead of F41

* Tue Sep 30 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.5-2
- Update minor version metadata to alow IPA data upgrade

* Tue Sep 30 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.5-1
- CVE-2025-7493: host to admin escalation prevention

* Tue Sep 23 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-19
- Rebuild for Python 3.14.0rc3
- Resolves: rhbz#2396699
- Update fixes from ipa-4-12 branch

* Tue Sep 09 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-18
- Fix forest trust information handling to support Samba 4.23
- resolves: rhbz#2393890

* Mon Aug 25 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-17
- Update samba dependency
- Resolves: rhbz#2390262
- Protect against failures on restart of dbus/oddjob in container build environment
- Resolves: rhbz#2379490

* Sat Aug 23 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-16
- Rebuild against new Samba passdb ABI (with no changes at the moment)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.12.2-15.2
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 30 2025 Rob Crittenden <rcritten@redhat.com> - 4.12.2-15.1
- Revert new location of the tomcat scripts

* Thu Jul 24 2025 Rob Crittenden <rcritten@redhat.com> - 4.12.2-15
- Support Tomcat 10

* Tue Jun 17 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-14
- CVE-2025-4404
- Include encrypted DNS support subpackages
- various fixes from ipa-4-12 branch upstream

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 4.12.2-13.1
- Rebuilt for Python 3.14

* Tue Apr 01 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-13
- Upgrade from OpenSSL Engine use to OpenSSL provider API

* Tue Apr 01 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-12
- Actually include OpenSSL provider API support

* Tue Apr 01 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-11
- Synchronize patchset with C10S
- Enable Encrypted DNS support

* Mon Feb 10 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-10
- Rebuild for Samba 4.22.0 RC1

* Mon Jan 27 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-9
- Do not pass OAuth2 client secret for public clients (freeipa#9734)
- Fix upgrade for two-way trust to Active Directory (freeipa#9471 post-fix)
- Allow extending certmonger request timeouts to accomodate for slow HSMs (freeipa#9725)

* Wed Jan 15 2025 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-8
- CVE-2024-11029
- Release notes: https://www.freeipa.org/release-notes/4-12-3.html

* Wed Dec 04 2024 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-7
- Apply upstream fixes since 4.12.2
- Fix OTP LDAP bind regression
- Resolves: rhbz#2321307
- add ipa-idrange-fix tool
- Support PyCA 44.0.0

* Thu Nov 21 2024 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-6
- Adjust to Samba 4.21

* Tue Oct 22 2024 Richard W.M. Jones <rjones@redhat.com> - 4.12.2-5
- Rebuild for Jansson 2.14
  (https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/3PYINSQGKQ4BB25NQUI2A2UCGGLAG5ND/)

* Fri Oct  4 2024 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-4
- Bump release to handle F41 updates which went out of sync due to rebuilds
- Fix CA uninstall in case ACME instance is available
- Bump SSSD requirement to 2.9.5 to ensure sssd-idp can handle Entra ID
- Make sure to use correct nodejs version for build

* Thu Aug 22 2024 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.2-1
- Upstream release 4.12.2
- Rebuild against Samba 4.21.0-RC3

* Mon Aug 19 2024 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.1-3
- Few more fixes, including tests and python-cryptography 43.0 compatibility

* Mon Aug 19 2024 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.1-2
- Post-4.12.1 fixes:
  - ipa-migrate tool fixes
  - HSM support fixes including SELinux policy changes
  - ipa-backup/ipa-restore uniqueness fix
  - improvements in replication topology access controls
  - allow PKINIT cert renewal on hidden replica
  - cleanup more files during uninstall
  - support for python-cryptography 43.0+
- Remove support for NIS server emulation. Requires slapi-nis 0.70.0

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Julien Rische <jrische@redhat.com> - 4.12.1-1
- Upstream release 4.12.1
- Release notes: https://www.freeipa.org/release-notes/4-12-1.html
- Security release: CVE-2024-2698 CVE-2024-3183

* Mon Jun 10 2024 Python Maint <python-maint@redhat.com> - 4.12.0-1.1
- Rebuilt for Python 3.13

* Wed May 29 2024 Alexander Bokovoy <abokovoy@redhat.com> - 4.12.0-1
- Upstream release 4.12
- Release notes: https://www.freeipa.org/release-notes/4-12-0.html

* Wed Feb 21 2024 Rob Crittenden <rcritten@redhat.com> - 4.11.1-4
- Security release: CVE-2024-1481
- Resolves: rhbz#2265129

* Thu Feb 08 2024 Alexander Bokovoy <abokovoy@redhat.com> - 4.11.1-3
- Support 389-ds with lmdb backend

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.1-2
- Rebuild against Samba 4.20rc1
- Fix memory leak in Kerberos KDC driver
- Fix possible crash in IPA command line tool when accessing Kerberos credentials
- Compatibility fix for Python Cryptography 42.0.0
- NetBIOS defaults fix
- Fix default host keytab retrieval permissions

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.1-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Alexander Bokovoy <abokovoy@redhat.com> - 4.11.1-1
- Security release: CVE-2023-5455
- Resolves: rhbz#2257646

* Wed Nov 08 2023 Alexander Bokovoy <abokovoy@redhat.com> - 4.11.0-7
- ipalib: fix the IPACertificate validity dates (python 3.12 compatibility)
- Handle PKI revocation response differences in JSON API
- Allow removal of minimal length from a custom password policy

* Mon Oct 23 2023 Alexander Bokovoy <abokovoy@redhat.com> - 4.11.0-6
- Adopt trust to AD code to Samba changes in case SIDs are malformed

* Tue Oct 03 2023 Alexander Bokovoy <abokovoy@redhat.com> - 4.11.0-5
- FreeIPA 4.11.0 release
- Simplify Fedora spec file
- Release notes: https://www.freeipa.org/release-notes/4-11-0.html

* Mon Sep 18 2023 Alexander Bokovoy <abokovoy@redhat.com> - 4.11.0-4.beta1
- Depend on selinux-policy-38.28-1.fc39
- Add SELinux policy for passkey_child to be used without ipa-otpd
- Related: rhbz#2238474

* Tue Sep 12 2023 Alexander Bokovoy <abokovoy@redhat.com> - 4.11.0-3.beta1
- Restore properly SELinux context during IPA client uninstallation
- Related: rhbz#2238474

* Tue Sep 12 2023 Alexander Bokovoy <abokovoy@redhat.com> - 4.11.0-2.beta1
- Set 'sssd_use_usb' SELinux boolean when enrolling IPA client
- Resolves: rhbz#2238474

* Mon Aug 21 2023 Alexander Bokovoy <abokovoy@redhat.com> - 4.11.0-1.beta1
- FreeIPA 4.11.0 beta 1
- Release notes: https://www.freeipa.org/release-notes/4-11-0-beta.html

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.2-1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 05 2023 Miro Hrončok <mhroncok@redhat.com> - 4.10.2-1.2
- Use ssl.match_hostname from urllib3 as it was removed from Python 3.12

* Tue Jun 27 2023 Python Maint <python-maint@redhat.com> - 4.10.2-1.1
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Alexander Bokovoy <abokovoy@redhat.com> - 4.10.2-1
- Upstream release FreeIPA 4.10.2
- Synchronize patches with CentOS 9 Stream

* Mon May 15 2023 Alexander Bokovoy <abokovoy@redhat.com> - 4.10.1-5
- Support python-cryptography 40.0

* Thu Mar 30 2023 Jerry James <loganjerry@gmail.com> - 4.10.1-4
- Change fontawesome-fonts R to match fontawesome 4.x

* Fri Jan 20 2023 Alexander Bokovoy <abokovoy@redhat.com> - 4.10.1-3
- Rebuild against Samba 4.18.0RC1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec  1 2022 Alexander Bokovoy <abokovoy@redhat.com> - 4.10.1-2
- Rebuild against krb5-1.20.1-1

* Sun Nov 27 2022 Alexander Bokovoy <abokovoy@redhat.com> - 4.10.1-1
- Upstream release FreeIPA 4.10.1

* Wed Sep 14 2022 Alexander Bokovoy <abokovoy@redhat.com> - 4.10.0-6
- Rebuild against final samba 4.17.0 release

* Wed Aug 24 2022 Adam Williamson <awilliam@redhat.com> - 4.10.0-5
- Rebuild against new samba-client-libs (for F37)

* Wed Aug 24 2022 Thomas Woerner <twoerner@redhat.com> - 4.10.0-4
- Disabling gracelimit does not prevent LDAP binds
- webui: Allow grace login limit
- Fix dns resolver for nameservers with ports
- Set passwordgracelimit to match global policy on group pw policies

* Tue Aug 09 2022 Adam Williamson <awilliam@redhat.com> - 4.10.0-3
- Rebuild against new libndr

* Tue Jul 26 2022 Alexander Bokovoy <abokovoy@redhat.com> - 4.10.0-2
- Rebuild against samba-4.16.3-2.fc37
- Resolves: rhbz#2110746

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 30 2022 Rob Crittenden <rcritten@redhat.com> - 4.10.0-1
- Upstream release FreeIPA 4.10.0

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 4.9.10-1.1
- Rebuilt for Python 3.11

* Thu Jun 16 2022 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.10-1
- Upstream release FreeIPA 4.9.10

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 4.9.9-1.1
- Rebuilt for Python 3.11

* Wed Apr 27 2022 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.9-1
- Upstream release FreeIPA 4.9.9

* Mon Feb 07 2022 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.8-3
- Use -H option for OpenLDAP client tools as -h and -p are deprecated now
- Resolves: rhbz#2050921

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.8-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.8-2
- Make possible to compile FreeIPA against OpenLDAP 2.6
- Resolves: rhbz#2032701

* Fri Nov 26 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.8-1
- Upstream release FreeIPA 4.9.8

* Thu Nov 11 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.7-4
- Hardening for CVE-2020-25717 part 2
- Handle S4U for users from trusted domains

* Wed Nov 10 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.7-3
- Hardening for CVE-2020-25717
- Generate SIDs for IPA users and groups by default
- Verify MS-PAC consistency when it is generated or validated
- Rebuild against samba-4.15.2
- Resolves: rhbz#2021720

* Fri Oct 15 2021 Rob Crittenden <rcritten@redhat.com> - 4.9.7-2
- Make Dogtag return XML for ipa cert-find (#2014658)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 4.9.7-1.1
- Rebuilt with OpenSSL 3.0.0

* Thu Aug 19 2021 François Cami <fcami@redhat.com> - 4.9.7-1
- Upstream release 4.9.7
- Resolves: rhbz#1994739

* Fri Aug 6 2021 François Cami <fcami@redhat.com> - 4.9.6-4
- Remove dependency on python3-pexpect on RHEL9.
- Resolves: rhbz#1980734

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.6-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 16 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.6-3
- Add dependency on sssd-winbind-idmap for freeipa-server-trust-ad
- Resolves: rhbz#1970168
- Rebuild against Samba 4.15.0 RC1 (libndr soname bump)

* Fri Jul 02 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.6-2
- Remove custodia dependencies as the code merged into FreeIPA now
- Resolves: rhbz#1978632

* Tue Jun 29 2021 François Cami <fcami@redhat.com> - 4.9.6-1
- Upstream release FreeIPA 4.9.6

* Mon Jun 14 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.4-2
- Rebuilt for Python 3.10, second part

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.9.4-1.1
- Rebuilt for Python 3.10

* Fri Jun 04 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.4-1
- Upstream release FreeIPA 4.9.4

* Tue Jun 01 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.3-4
- Handle upgrade of 389-ds replication plugin rename (part 2)

* Tue Jun 01 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.3-3
- Handle upgrade of 389-ds replication plugin rename

* Mon Apr 12 2021  Alexander Bokovoy <abokovoy@redhat.com> - 4.9.3-2
- Handle failures to resolve non-existing reverse zones during deployment with systemd-resolved
- Resolves: rhbz#1948034

* Wed Mar 31 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.3-1
- Upstream release FreeIPA 4.9.3

* Fri Feb 26 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.2-4
- Rebuild against 389-ds and PKI to fix https://github.com/389ds/389-ds-base/issues/4609

* Tue Feb 23 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.2-3
- Only use python-platform on RHEL 8

* Mon Feb 15 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.2-2
- Fix ipatests dependency to python3-pexpect

* Mon Feb 15 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.2-1
- Upstream release FreeIPA 4.9.2

* Wed Jan 27 2021 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.1-1
- Upstream release FreeIPA 4.9.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Rob Crittenden <rcritten@redhat.com> - 4.9.0-2
- Set client keytab location for 389ds (RHBZ#1918075)

* Wed Dec 23 17:05:00 EET 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.0-1
- FreeIPA 4.9.0 final release

* Wed Dec 16 07:52:00 EET 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.0-0.6.rc3
- Refactor DNSSEC paths creation code (upstream PR#5340)

* Thu Dec 10 20:06:03 EET 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.0-0.5.rc3
- FreeIPA 4.9.0 release candidate 3
- Enforce C.UTF-8 locale in systemd service units
- Fold up fixes from Rawhide and RHEL 8.4 testing

* Wed Dec  9 20:06:03 EET 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.0-0.4.rc2
- Fix upgrade script for CA rule rewrites
- Fix permissions for /run/ipa/ccaches

* Fri Dec  4 22:17:00 EET 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.0-0.3.rc2
- Correct SELinux policy requirements

* Fri Dec  4 13:41:28 EET 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.0-0.2.rc2
- FreeIPA 4.9.0 release candidate 2

* Thu Nov 19 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.0-0.1.rc1
- Use correct bind PKCS11 engine dependencies
- Fix SELinux build requirement
- Fix linting requirements

* Wed Nov 18 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.9.0-0.rc1
- FreeIPA 4.9.0 release candidate 1
- Synchronize spec file with upstream and RHEL

* Wed Oct 28 2020 Adam Williamson <awilliam@redhat.com> - 4.8.10-7
- Backport #5212 for deployment failures with 389-ds-base 1.4.4.6+

* Tue Oct 13 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.10-6
- Handle sshd_config upgrade properly
  Fixes: rhbz#1887928

* Tue Sep 29 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.10-5
- Properly handle upgrade case when systemd-resolved is enabled

* Mon Sep 28 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.10-4
- Fix permissions for /etc/systemd/resolved.conf.d/zzz-ipa.conf
- Add NetworkManager and systemd-resolved configuration files to backup

* Sun Sep 27 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.10-3
- Fix dependency between freeipa-selinux and freeipa-common
- Resolves: rhbz#1883005

* Sat Sep 26 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.10-2
- Support upgrade F32 -> F33 with systemd-resolved

* Sat Sep 26 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.10-1
- Upstream release FreeIPA 4.8.10

* Fri Aug 21 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.9-2
- Backport fix for detecting older installations on upgrade

* Thu Aug 20 2020 François Cami <fcami@redhat.com> - 4.8.9-1
- Upstream release FreeIPA 4.8.9

* Mon Aug 03 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.7-5
- Make use of unshare+chroot in ipa-extdom-extop unittests to work against glibc 2.32

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.7-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 30 2020 Merlin Mathesius <mmathesi@redhat.com> - 4.8.7-3
- Conditional fixes for ELN to set krb5-kdb version appropriately

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 10 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.7-1
- Upstream release FreeIPA 4.8.7

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.8.6-2
- Rebuilt for Python 3.9

* Fri Mar 27 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.6-1
- Upstream release FreeIPA 4.8.6

* Sat Mar 21 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.5-2
- Roll up post-release fixes from upstream
- Move freeipa-selinux to be a dependency of freeipa-common

* Wed Mar 18 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.5-1
- Upstream release FreeIPA 4.8.5
- Depend on selinux-policy-devel 3.14.6-9 for build due to a makefile issue in
  SELinux external policy support

* Tue Mar 03 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.4-8
- Support opendnssec 2.1
- Resolves: #1809492

* Mon Feb 17 2020 François Cami <fcami@redhat.com> - 4.8.4-7
- Fix audit_as_req() callback usage
- Resolves: #1803786

* Sat Feb 01 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.4-6
- Fix constraint delegation for krb5 1.18 update
- Resolves: #1797096

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 28 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.4-4
- Rebuild against krb5 1.18 beta

* Sun Jan 26 2020 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.4-3
- Rebuild against Samba 4.12RC1

* Mon Dec 16 2019 Adam Williamson <awilliam@redhat.com> - 4.8.4-2
- Backport PR #4045 to fix overlapping DNS zone check bugs

* Sat Dec 14 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.4-1
- New upstream release 4.8.4

* Tue Nov 26 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.3-1
- New upstream release 4.8.3
- CVE-2019-14867: Denial of service in IPA server due to wrong use of ber_scanf()
- CVE-2019-10195: Don't log passwords embedded in commands in calls using batch

* Tue Nov 12 2019 Rob Crittenden <rcritten@redhat.com> - 4.8.2-1
- New upstream release 4.8.2
- Replace %%{_libdir} macro in BuildRequires (#1746882)
- Restore user-nsswitch.conf before calling authselect (#1746557)
- ipa service-find does not list cifs service created by
  ipa-client-samba (#1731433)
- Occasional 'whoami.data is undefined' error in FreeIPA web UI
  (#1699109)
- ipa-kra-install fails due to fs.protected_regular=1 (#1698384)

* Sun Oct 20 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.1-5
- Don't create log files from helper scripts
- Fixes: rhbz#1754189

* Tue Oct 08 2019 Christian Heimes <cheimes@redhat.com> - 4.8.1-4
- Fix compatibility issue with preexec_fn in Python 3.8
- Fixes: rhbz#1759290

* Tue Oct  1 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.1-3
- Fix ipasam for compatibility with Samba 4.11
- Fixes: rhbz#1757089

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.8.1-2
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.1-1
- New upstream release 4.8.1
- Fixes: rhbz#1732528
- Fixes: rhbz#1732524

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.8.0-1
- New upstream release 4.8.0
- New subpackage: freeipa-client-samba

* Sat May 11 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.90.pre1-6
- Upgrade: handle situation when trusts were configured but not established yet
  Fixed: rhbz#1708808

* Fri May  3 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.90.pre1-5
- Add krb5-kdb-server dependency provided by krb5-server >= 1.17-17

* Fri May  3 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.90.pre1-4
- Rebuild to drop upper limit for Kerberos package
  After krb5-server will provide krb5-kdb-version, we'll switch to it

* Wed May  1 2019 Adam Williamson <awilliam@redhat.com> - 4.7.90.pre1-3
- Backport PR #3104 to fix a font path error

* Wed May  1 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.90.pre1-2
- Revert MINSSF defaults because realmd cannot join FreeIPA right now
  as it uses anonymous LDAP connection for the discovery and validation

* Mon Apr 29 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.90.pre1-1
- First release candidate for FreeIPA 4.8.0

* Sat Apr 06 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.2-8
- Fixed: rhbz#1696963 (Failed to install replica)
  
* Sat Apr 06 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.2-7
- Support Samba 4.10
- Support 389-ds 1.4.1.2-2.fc30 or later

* Thu Feb 28 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.2-6
- Support new nfs-utils behavior (#1668836)
- ipa-client-automount now works without /etc/sysconfig/nfs

* Tue Feb 19 2019 François Cami <fcami@redhat.com> - 4.7.2-5
- Fix FTBS due to Samba having removed talloc_strackframe.h
  and memory.h (#1678670)
- Fix CA setup when fs.protected_regular=1 (#1677027)

* Mon Feb 11 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.2-4
- Disable python dependency generator in Rawhide as not all required packages support it yet
- Require python-kdcproxy 0.4.1 or later on Rawhide

* Fri Feb 8 2019 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.2-3
- Fix compile issues after a mass rebuild using upstream patches

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.2-1
- Upstream release FreeIPA 4.7.2

* Wed Nov 28 2018 Adam Williamson <awilliam@redhat.com> - 4.7.1-4
- Update PR #2610 patch to tiran's modified version

* Tue Nov 27 2018 Adam Williamson <awilliam@redhat.com> - 4.7.1-3
- Backport PR #2610 to fix for authselect 1.0.2+ (see #1645708)

* Sun Nov 11 2018 Alexander Bokovoy <abokovoy@redhat.com> - 4.7.1-2
- Rebuild for krb5-1.17 (#1648673)
- Bump required SSSD version to 2.0.0-4 to get back pysss.getgrouplist() API

* Fri Oct  5 2018 Rob Crittenden <rcritten@redhat.com> - 4.7.1-1
- Update to upstream 4.7.1

* Tue Sep 25 2018 Christian Heimes <cheimes@redhat.com> - 4.7.0-5
- Remove Python 2 support from Fedora 30
- https://fedoraproject.org/wiki/Changes/FreeIPA_Python_2_Removal

* Tue Sep  4 2018 Thomas Woerner <twoerner@redhat.com> - 4.7.0-4
- Enable python2 client packages for f30 for now again

* Tue Sep  4 2018 Thomas Woerner <twoerner@redhat.com> - 4.7.0-3
- Force generation of aclocal.m4 and configuration scripts
- Fix only client build for Fedora>=28 and RHEL>7
- Bring back special patch handling for Fedora

* Mon Sep  3 2018 Thomas Woerner <twoerner@redhat.com> - 4.7.0-2
- Restore SELinux context of session_dir /etc/httpd/alias (pagure#7662)
- Restore SELinux context of template_dir /var/log/dirsrv/slapd-X (pagure#7662)
- Add "389-ds-base-legacy-tools" to requires
- Refactor os-release and platform information (#1609475)
- Don't check for systemd service (#1609475)
- Switched to upstream spec file with small adaptions

* Thu Jul 26 2018 Thomas Woerner <twoerner@redhat.com> - 4.7.0-1
- Update to upstream 4.7.0
- New BuildRequires for nodejs and uglify-js
- New Requires for 389-ds-base-legacy-tools in server (RHBZ#1606541)
- Do not build python2-ipaserver and python2-ipatests for Fedora 29 and up
- Do not build any python2 packages for Fedora 30
- Added ipatest man pages to python3-ipatests packages also
- Added ipatest bindir links to python3-ipatests for Fedora up to 28
- Dropped explicit copy of freeipa.template, install is doing this now
- Added upstream fix: (f3faecb) Fix $-style format string in ipa_ldap_init
- Added upstream fix: (4b592fe,1a7baa2) Added reason to raise of errors.NotFound

* Mon Jul 16 2018 Alexander Bokovoy <abokovoy@redhat.com> - 4.6.90.pre2-11
- Use version-aware macros for Python

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.90.pre2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 4.6.90.pre2-9
- Rebuilt for Python 3.7

* Wed Jun 27 2018 Rob Crittenden <rcritten@redhat.com> - 4.6.90.pre2-8
- Build UI using py3-lesscpy

* Tue Jun 19 2018 Rob Crittenden <rcritten@redhat.com> - 4.6.90.pre2-7
- *-domainname.service moved to the hostname package in F29 (#1592355)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.6.90.pre2-6
- Rebuilt for Python 3.7

* Fri Jun 15 2018 Rob Crittenden <rcritten@redhat.com> - 4.6.90.pre2-5
- Change BuildRequires from python-lesscpy to python3-lesscpy

* Fri Jun 15 2018 Rob Crittenden <rcritten@redhat.com> - 4.6.90.pre2-4.1
- Rename service fedora-domainname.service to nis-domainname.service
  (#1588192)
- Fix bad date in changelog

* Wed May 16 2018 Alexander Bokovoy <abokovoy@redhat.com> - 4.6.90.pre2-3
- Fine tune packaging of server templates so that it doesn't include
  freeipa.template which always go to freeipa-client-common

* Tue May 15 2018 Rob Crittenden <rcritten@redhat.com> - 4.6.90.pre2-2
- Exclude /usr/share from client-only builds

* Tue May 15 2018 Rob Crittenden <rcritten@redhat.com> - 4.6.90.pre2-1
- Update to upstream 4.6.90.pre2

* Wed May 02 2018 Alexander Bokovoy <abokovoy@redhat.com> - 4.6.90.pre1-7
- Fix upgrade when named.conf does not exist
- Resolves rhbz#1573671
- Requires newer slapi-nis to avoid hitting rhbz#1573636

* Wed Mar 21 2018 Alexander Bokovoy <abokovoy@redhat.com> - 4.6.90.pre1-6.1
- Change upgrade code to use DIR-based ccache and no kinit (#1558818)
- Require pki-symkey until pki-core has proper dependencies

* Wed Mar 21 2018 Alexander Bokovoy <abokovoy@redhat.com> - 4.6.90.pre1-6
- Change upgrade code to use DIR-based ccache and no kinit (#1558818)

* Tue Mar 20 2018 Alexander Bokovoy <abokovoy@redhat.com> - 4.6.90.pre1-5
- Apply upstream fix for #1558354
- Run upgrade under file-based ccache (#1558818)
- Fix OTP token issuance due to regression in https://pagure.io/389-ds-base/issue/49617

* Tue Mar 20 2018 Adam Williamson <awilliam@redhat.com> - 4.6.90.pre1-4
- Fix upgrades harder (extension of -3 patch) (#1558354)

* Tue Mar 20 2018 Alexander Bokovoy <abokovoy@redhat.com> - 4.6.90.pre1-3
- Fix upgrade from F27 to F28 (#1558354)

* Mon Mar 19 2018 Rob Crittenden <rcritten@redhat.com> - 4.6.90.pre1-2
- Patch to fix GUI login for non-admin users (#1557609)

* Fri Mar 16 2018 Rob Crittenden <rcritten@redhat.com> - 4.6.90.pre1-1
- Update to upstream 4.6.90.pre1

* Tue Feb 20 2018 Rob Crittenden <rcritten@redhat.com> - 4.6.3-5
- Disable i686 server builds because 389-ds no longer provides
  builds on that arch. (#1544386)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.6.3-4
- Escape macros in %%changelog

* Thu Feb  8 2018 Rob Crittenden <rcritten@redhat.com> - 4.6.3-3
- Don't fail on upgrades if KRA is not installed
- Remove Conflicts between mod_wsgi and python3-mod_wsgi

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Rob Crittenden <rcritten@redhat.com> - 4.6.3-1
- Update to upstream 4.6.3

* Wed Jan 03 2018 Lumír Balhar <lbalhar@redhat.com> - 4.6.1-5
- Fix directory ownership in python3 subpackage

* Tue Oct 17 2017 Rob Crittenden <rcritten@redhat.com> - 4.6.1-4
- Update workaround patch to prevent SELinux execmem AVC (#1491508)

* Mon Oct 16 2017 Alexander Bokovoy <abokovoy@redhat.com> - 4.6.1-3
- Another attempt at fix for bug #1491053

* Fri Oct 06 2017 Tomas Krizek <tkrizek@redhat.com> - 4.6.1-2
- Rebuild against krb5-1.16

* Fri Sep 22 2017 Tomas Krizek <tkrizek@redhat.com> - 4.6.1-1
- Fixes #1491053  Firefox reports insecure TLS configuration when visiting
  FreeIPA web UI after standard server deployment

* Wed Sep 13 2017 Adam Williamson <awilliam@redhat.com> - 4.6.0-3
- Fixes #1490762 Ipa-server-install update dse.ldif with wrong SELinux context
- Fixes #1491056 FreeIPA enrolment via kickstart fails

* Wed Sep 06 2017 Adam Williamson <awilliam@redhat.com> - 4.6.0-2
- Fixes #1488640 "unknown command 'undefined'" error when changing password in web UI
- BuildRequires diffstat (for the use in patch application)

* Mon Sep 04 2017 Tomas Krizek <tkrizek@redhat.com> - 4.6.0-1
- Rebase to upstream 4.6.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Tomas Krizek <tkrizek@redhat.com> - 4.5.3-1
- Update to upstream 4.5.3 - see https://www.freeipa.org/page/Releases/4.5.3

* Thu Jul 13 2017 Alexander Bokovoy <abokovoy@redhat.com> - 4.5.2-4
- Make sure tmpfiles.d snippet for replica is in place after install

* Mon Jul 10 2017 Alexander Bokovoy <abokovoy@redhat.com> - 4.5.2-3
- Fix build with Samba 4.7.0-RC1
- Increase java stack for rhino calls to get around crashes on ppc64-le

* Tue Jun 20 2017 Tomas Krizek <tkrizek@redhat.com> - 4.5.2-2
- Patch: Fix IP address checks
- Patch: python-netifaces fix

* Sun Jun 18 2017 Tomas Krizek <tkrizek@redhat.com> - 4.5.2-1
- Update to upstream 4.5.2 - see https://www.freeipa.org/page/Releases/4.5.2

* Thu May 25 2017 Tomas Krizek <tkrizek@redhat.com> - 4.5.1-1
- Update to upstream 4.5.1 - see https://www.freeipa.org/page/Releases/4.5.1
- Fixes #1168266 UI drops "Enknown Error" when the ipa record in /etc/hosts changes

* Tue May 23 2017 Tomas Krizek <tkrizek@redhat.com> - 4.4.4-2
- Fixes #1448049 Subpackage freeipa-server-common has unmet dependencies on Rawhide
- Fixes #1430247 FreeIPA server deployment runs ipa-custodia on Python 3, should use Python 2
- Fixes #1446744 python2-ipaclient subpackage does not own %%{python_sitelib}/ipaclient/plugins
- Fixes #1440525 surplus 'the' in output of `ipa-adtrust-install`
- Fixes #1411810 ipa-replica-install fails with 406 Client Error
- Fixes #1405814 ipa plugins: ERROR an internal error occured

* Fri Mar 24 2017 Tomas Krizek <tkrizek@redhat.com> - 4.4.4-1
- Update to upstream 4.4.4 - see https://www.freeipa.org/page/Releases/4.4.4
- Add upstream signature file for tarball

* Wed Mar  1 2017 Alexander Bokovoy <abokovoy@redhat.com> - 4.4.3-8
- Use different method to keep /usr/bin/ipa on Python 2
- Fixes #1426847

* Mon Feb 27 2017 Tomas Krizek <tkrizek@redhat.com> - 4.4.3-7
- Fixes #1413137 CVE-2017-2590 ipa: Insufficient permission check for
  ca-del, ca-disable and ca-enable commands

* Mon Feb 27 2017 Alexander Bokovoy <abokovoy@redhat.com> - 4.4.3-6
- Rebuild to pick up system-python dependency change
- Fixes #1426847 - Cannot upgrade freeipa-client on rawhide

* Wed Feb 15 2017 Tomas Krizek <tkrizek@redhat.com> - 4.4.3-5
- Fixes #1403352 - bind-dyndb-ldap: support new named.conf API in BIND 9.11
- Fixes #1412739 - ipa-kdb: support DAL version 6.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 21 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.4.3-3
- Rebuild for xmlrpc-c

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 4.4.3-2
- Rebuild for Python 3.6

* Fri Dec 16 2016 Pavel Vomacka <pvomacka@redhat.com> - 4.4.3-1
- Update to upstream 4.4.3 - see http://www.freeipa.org/page/Releases/4.4.3

* Wed Dec 14 2016 Pavel Vomacka <pvomacka@redhat.com> - 4.4.2-4
- Fixes 1395311 - CVE-2016-9575 ipa: Insufficient permission check in certprofile-mod
- Fixes 1370493 - CVE-2016-7030 ipa: DoS attack against kerberized services
  by abusing password policy

* Tue Nov 29 2016 Petr Vobornik <pvoborni@redhat.com> - 4.4.2-3
- Fixes 1389866  krb5-server: ipadb_change_pwd(): kdb5_util killed by SIGSEGV

* Fri Oct 21 2016 Petr Vobornik <pvoborni@redhat.com> - 4.4.2-2
- Rebuild against krb5-1.15

* Thu Oct 13 2016 Petr Vobornik <pvoborni@redhat.com> - 4.4.2-1
- Update to upstream 4.4.2 - see http://www.freeipa.org/page/Releases/4.4.2

* Thu Sep 01 2016 Alexander Bokovoy <abokovoy@redhat.com> - 4.4.1-1
- Update to upstream 4.4.1 - see http://www.freeipa.org/page/Releases/4.4.1

* Fri Aug 19 2016 Petr Vobornik <pvoborni@redhat.com> - 4.3.2-2
- Fixes 1365669 - The ipa-server-upgrade command failed when named-pkcs11 does
  not happen to run during dnf upgrade
- Fixes 1367883 - CVE-2016-5404 freeipa: ipa: Insufficient privileges check
  in certificate revocation
- Fixes 1364338 - Freeipa cannot be build on fedora 25

* Fri Jul 22 2016 Petr Vobornik <pvoborni@redhat.com> - 4.3.2-1
- Update to upstream 4.3.2 - see http://www.freeipa.org/page/Releases/4.3.2

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Mar 24 2016 Petr Vobornik <pvoborni@redhat.com> - 4.3.1-1
- Update to upstream 4.3.1 - see http://www.freeipa.org/page/Releases/4.3.1

* Thu Feb 04 2016 Petr Vobornik <pvoborni@redhat.com> - 4.3.0-3
- Fix build with Samba 4.4
- Update SELinux requires to fix connection check during installation

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 18 2015 Petr Vobornik <pvoborni@redhat.com> - 4.3.0-1
- Update to upstream 4.3.0 - see http://www.freeipa.org/page/Releases/4.3.0

* Mon Dec 07 2015 Petr Vobornik <pvoborni@redhat.com> - 4.2.3-2
- Workarounds for SELinux execmem violations in cryptography

* Mon Nov 02 2015 Petr Vobornik <pvoborni@redhat.com> - 4.2.3-1
- Update to upstream 4.2.3 - see http://www.freeipa.org/page/Releases/4.2.3
- fix #1274905

* Wed Oct 21 2015 Alexander Bokovoy <abokovoy@redhat.com> - 4.2.2-2
- Depend on samba-common-tools for the trust-ad subpackage after
  samba package split
- Rebuild against krb5 1.14 to fix bug #1273957

* Thu Oct 8 2015 Petr Vobornik <pvoborni@redhat.com> - 4.2.2-1
- Update to upstream 4.2.2 - see http://www.freeipa.org/page/Releases/4.2.2

* Mon Sep 7 2015 Petr Vobornik <pvoborni@redhat.com> - 4.2.1-1
- Update to upstream 4.2.1 - see http://www.freeipa.org/page/Releases/4.2.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Alexander Bokovoy <abokovoy@redhat.com> - 4.1.4-4
- Fix typo in the patch to fix bug #1219834

* Mon May 11 2015 Alexander Bokovoy <abokovoy@redhat.com> - 4.1.4-3
- Fix FreeIPA trusts to AD feature with Samba 4.2 (#1219834)

* Mon Mar 30 2015 Petr Vobornik <pvoborni@redhat.com> - 4.1.4-2
- Replace mod_auth_kerb usage with mod_auth_gssapi

* Thu Mar 26 2015 Alexander Bokovoy <abokovoy@redhat.com> - 4.1.4-1
- Update to upstream 4.1.4 - see http://www.freeipa.org/page/Releases/4.1.4
- fix CVE-2015-1827 (#1206047)
- Require slapi-nis 0.54.2 and newer for CVE-2015-0283 fixes

* Tue Mar 17 2015 Petr Vobornik <pvoborni@redhat.com> - 4.1.3-3
- Timeout ipa-client install if ntp server is unreachable #4842
- Skip time sync during client install when using --no-ntp #4842

* Wed Mar 04 2015 Petr Vobornik <pvoborni@redhat.com> - 4.1.3-2
- Add missing sssd python dependencies
- https://bugzilla.redhat.com/show_bug.cgi?id=1197218

* Wed Feb 18 2015 Petr Vobornik <pvoborni@redhat.com> - 4.1.3-1
- Update to upstream 4.1.3 - see http://www.freeipa.org/page/Releases/4.1.3

* Mon Jan 19 2015 Alexander Bokovoy <abokovoy@redhat.com> - 4.1.2-2
- Fix broken build after Samba ABI change and rename of libpdb to libsamba-passdb
- Use python-dateutil15 until we validate python-dateutil 2.x

* Tue Nov 25 2014 Petr Vobornik <pvoborni@redhat.com> - 4.1.2-1
- Update to upstream 4.1.2 - see http://www.freeipa.org/page/Releases/4.1.2
- fix CVE-2014-7850

* Thu Nov 20 2014 Simo Sorce <simo@redhat.com> - 4.1.1-2
- Patch blokers and feature freze exceptions
- Resolves: bz1165674
- Resolves: bz1165856 (CVE-2014-7850)
- Fixes DNS install issue that prevents the server from working

* Thu Nov 06 2014 Petr Vobornik <pvoborni@redhat.com> - 4.1.1-1
- Update to upstream 4.1.1 - see http://www.freeipa.org/page/Releases/4.1.1
- fix CVE-2014-7828

* Wed Oct 22 2014 Petr Vobornik <pvoborni@redhat.com> - 4.1.0-2
- fix armv7hl stack oversize build failure
- fix https://fedorahosted.org/freeipa/ticket/4660

* Tue Oct 21 2014 Petr Vobornik <pvoborni@redhat.com> - 4.1.0-1
- Update to upstream 4.1.0 - see http://www.freeipa.org/page/Releases/4.1.0

* Fri Sep 12 2014 Petr Viktorin <pviktori@redhat.com> - 4.0.3-1
- Update to upstream 4.0.3 - see http://www.freeipa.org/page/Releases/4.0.3

* Fri Sep 05 2014 Petr Viktorin <pviktori@redhat.com> - 4.0.2-1
- Update to upstream 4.0.1 - see http://www.freeipa.org/page/Releases/4.0.2

* Tue Sep 02 2014 Pádraig Brady <pbrady@redhat.com> - 4.0.1-3
- rebuild for libunistring soname bump

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 25 2014 Martin Kosek <mkosek@redhat.com> 4.0.1-1
- Update to upstream 4.0.1

* Mon Jul 07 2014 Petr Viktorin <pviktori@redhat.com> 4.0.0-1
- Update to upstream 4.0.0
- Remove the server-strict package

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Petr Vobornik <pvoborni@redhat.com> 3.3.5-3
- Increase Java stack size for Web UI build on aarch64

* Wed Apr 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.3.5-2
- Add rhino as dependency to fix FTBFS

* Fri Mar 28 2014 Martin Kosek <mkosek@redhat.com> - 3.3.5-1
- Update to upstream 3.3.5

* Tue Feb 11 2014 Martin Kosek <mkosek@redhat.com> - 3.3.4-3
- Move ipa-otpd socket directory to /var/run/krb5kdc
- Require krb5-server 1.11.5-3 supporting the new directory
- ipa_lockout plugin did not work with users's without krbPwdPolicyReference

* Wed Jan 29 2014 Martin Kosek <mkosek@redhat.com> - 3.3.4-2
- Fix hardened build

* Tue Jan 28 2014 Martin Kosek <mkosek@redhat.com> - 3.3.4-1
- Update to upstream 3.3.4
- Install CA anchor into standard location (#928478)
- ipa-client-install part of ipa-server-install fails on reinstall (#1044994)
- Remove mod_ssl workaround (RHEL bug #1029046)
- Enable syncrepl plugin to support bind-dyndb-ldap 4.0

* Fri Jan 3 2014 Martin Kosek <mkosek@redhat.com> - 3.3.3-5
- Build crashed with rhino exception on s390 architectures (#1040576)

* Thu Dec 12 2013 Martin Kosek <mkosek@redhat.com> - 3.3.3-4
- Build crashed with rhino exception on PPC architectures (#1040576)

* Tue Dec 3 2013 Martin Kosek <mkosek@redhat.com> - 3.3.3-3
- Fix -Werror=format-security errors (#1037070)

* Mon Nov 4 2013 Martin Kosek <mkosek@redhat.com> - 3.3.3-2
- ipa-server-install crashed when freeipa-server-trust-ad subpackage was not
  installed

* Fri Nov 1 2013 Martin Kosek <mkosek@redhat.com> - 3.3.3-1
- Update to upstream 3.3.3

* Fri Oct 4 2013 Martin Kosek <mkosek@redhat.com> - 3.3.2-1
- Update to upstream 3.3.2

* Thu Aug 29 2013 Petr Viktorin <pviktori@redhat.com> - 3.3.1-1
- Bring back Fedora-only changes

* Thu Aug 29 2013 Petr Viktorin <pviktori@redhat.com> - 3.3.1-0
- Update to upstream 3.3.1

* Wed Aug 14 2013 Alexander Bokovoy <abokovoy@redhat.com> - 3.3.0-2
- Remove freeipa-systemd-upgrade as non-systemd installs are not supported
  anymore by Fedora project

* Wed Aug 7 2013 Martin Kosek <mkosek@redhat.com> - 3.3.0-1
- Update to upstream 3.3.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Martin Kosek <mkosek@redhat.com> - 3.2.2-1
- Update to upstream 3.2.2
- Drop freeipa-server-selinux subpackage
- Drop redundant directory /var/cache/ipa/sessions
- Do not create /var/lib/ipa/pki-ca/publish, retain reference as ghost
- Run ipa-upgradeconfig and server restart in posttrans to avoid inconsistency
  issues when there are still old parts of software (like entitlements plugin)

* Fri Jun  7 2013 Martin Kosek <mkosek@redhat.com> - 3.2.1-1
- Update to upstream 3.2.1

* Tue May 14 2013 Rob Crittenden <rcritten@redhat.com> - 3.2.0-2
- Add OTP patches
- Add patch to set KRB5CCNAME for 389-ds-base

* Fri May 10 2013 Rob Crittenden <rcritten@redhat.com> - 3.2.0-1
- Update to upstream 3.2.0 GA
- ipa-client-install fails if /etc/ipa does not exist (#961483)
- Certificate status is not visible in Service and Host page (#956718)
- ipa-client-install removes needed options from ldap.conf (#953991)
- Handle socket.gethostbyaddr() exceptions when verifying hostnames (#953957)
- Add triggerin scriptlet to support OpenSSH 6.2 (#953617)
- Require nss 3.14.3-12.0 to address certutil certificate import
  errors (#953485)
- Require pki-ca 10.0.2-3 to pull in fix for sslget and mixed IPv4/6
  environments. (#953464)
- ipa-client-install removes 'sss' from /etc/nsswitch.conf (#953453)
- ipa-server-install --uninstall doesn't stop dirsrv instances (#953432)
- Add requires for openldap-2.4.35-4 to pickup fixed SASL_NOCANON behavior for
  socket based connections (#960222)
- Require libsss_nss_idmap-python
- Add Conflicts on nss-pam-ldapd < 0.8.4. The mapping from uniqueMember to
  member is now done automatically and having it in the config file raises
  an error.
- Add backup and restore tools, directory.
- require at least systemd 38 which provides the journal (we no longer
  need to require syslog.target)
- Update Requires on policycoreutils to 2.1.14-37
- Update Requires on selinux-policy to 3.12.1-42
- Update Requires on 389-ds-base to 1.3.1.0
- Remove a Requires for java-atk-wrapper

* Tue Apr 23 2013 Rob Crittenden <rcritten@redhat.com> - 3.2.0-0.4.beta1
- Remove release from krb5-server in strict sub-package to allow for rebuilds.

* Mon Apr 22 2013 Rob Crittenden <rcritten@redhat.com> - 3.2.0-0.3.beta1
- Add a Requires for java-atk-wrapper until we can determine which package
  should be pulling it in, dogtag or tomcat.

* Tue Apr 16 2013 Rob Crittenden <rcritten@redhat.com> - 3.2.0-0.2.beta1
- Update to upstream 3.2.0 Beta 1

* Tue Apr  2 2013 Martin Kosek <mkosek@redhat.com> - 3.2.0-0.1.pre1
- Update to upstream 3.2.0 Prerelease 1
- Use upstream reference spec file as a base for Fedora spec file

* Sat Mar 30 2013 Kevin Fenzi <kevin@scrye.com> 3.1.2-4
- Rebuild for broken deps
- Fix 389-ds-base strict dep to be 1.3.0.5 and krb5-server 1.11.1

* Sat Feb 23 2013 Kevin Fenzi <kevin@scrye.com> - 3.1.2-3
- Rebuild for broken deps in rawhide
- Fix 389-ds-base strict dep to be 1.3.0.3

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Rob Crittenden <rcritten@redhat.com> - 3.1.2-1
- Update to upstream 3.1.2
- CVE-2012-4546: Incorrect CRLs publishing
- CVE-2012-5484: MITM Attack during Join process
- CVE-2013-0199: Cross-Realm Trust key leak
- Updated strict dependencies to 389-ds-base = 1.3.0.2 and
  pki-ca = 10.0.1

* Thu Dec 20 2012 Martin Kosek <mkosek@redhat.com> - 3.1.0-2
- Remove redundat Requires versions that are already in Fedora 17
- Replace python-crypto Requires with m2crypto
- Add missing Requires(post) for client and server-trust-ad subpackages
- Restart httpd service when server-trust-ad subpackage is installed
- Bump selinux-policy Requires to pick up PKI/LDAP port labeling fixes

* Mon Dec 10 2012 Rob Crittenden <rcritten@redhat.com> - 3.1.0-1
- Updated to upstream 3.1.0 GA
- Set minimum for sssd to 1.9.2
- Set minimum for pki-ca to 10.0.0-1
- Set minimum for 389-ds-base to 1.3.0
- Set minimum for selinux-policy to 3.11.1-60
- Remove unneeded dogtag package requires

* Tue Oct 23 2012 Martin Kosek <mkosek@redhat.com> - 3.0.0-3
- Update Requires on krb5-server to 1.11

* Fri Oct 12 2012 Rob Crittenden <rcritten@redhat.com> - 3.0.0-2
- Configure CA replication to use TLS instead of SSL

* Fri Oct 12 2012 Rob Crittenden <rcritten@redhat.com> - 3.0.0-1
- Updated to upstream 3.0.0 GA
- Set minimum for samba to 4.0.0-153.
- Make sure server-trust-ad subpackage alternates winbind_krb5_locator.so
  plugin to /dev/null since they cannot be used when trusts are configured
- Restrict krb5-server to 1.10.
- Update BR for 389-ds-base to 1.3.0
- Add directory /var/lib/ipa/pki-ca/publish for CRL published by pki-ca
- Add Requires on zip for generating FF browser extension

* Fri Oct  5 2012 Rob Crittenden <rcritten@redhat.com> - 3.0.0-0.10
- Updated to upstream 3.0.0 rc 2
- Include new FF configuration extension
- Set minimum Requires of selinux-policy to 3.11.1-33
- Set minimum Requires dogtag to 10.0.0-0.43.b1
- Add new optional strict sub-package to allow users to limit other
  package upgrades.

* Tue Oct  2 2012 Martin Kosek <mkosek@redhat.com> - 3.0.0-0.9
- Require samba packages instead of obsoleted samba4 packages

* Fri Sep 21 2012 Rob Crittenden <rcritten@redhat.com> - 3.0.0-0.8
- Updated to upstream 3.0.0 rc 1
- Update BR for 389-ds-base to 1.2.11.14
- Update BR for krb5 to 1.10
- Update BR for samba4-devel to 4.0.0-139 (rc1)
- Add BR for python-polib
- Update BR and Requires on sssd to 1.9.0
- Update Requires on policycoreutils to 2.1.12-5
- Update Requires on 389-ds-base to 1.2.11.14
- Update Requires on selinux-policy to 3.11.1-21
- Update Requires on dogtag to 10.0.0-0.33.a1
- Update Requires on certmonger to 0.60
- Update Requires on tomcat to 7.0.29
- Update minimum version of bind to 9.9.1-10.P3
- Update minimum version of bind-dyndb-ldap to 1.1.0-0.16.rc1
- Remove Requires on authconfig from python sub-package

* Wed Sep  5 2012 Rob Crittenden <rcritten@redhat.com> - 3.0.0-0.7
- Rebuild against samba4 beta8

* Fri Aug 31 2012 Rob Crittenden <rcritten@redhat.com> - 3.0.0-0.6
- Rebuild against samba4 beta7

* Wed Aug 22 2012 Alexander Bokovoy <abokovoy@redhat.com> - 3.0.0-0.5
- Adopt to samba4 beta6 (libsecurity -> libsamba-security)
- Add dependency to samba4-winbind

* Fri Aug 17 2012 Rob Crittenden <rcritten@redhat.com> - 3.0.0-0.4
- Updated to upstream 3.0.0 beta 2

* Mon Aug  6 2012 Martin Kosek <mkosek@redhat.com> - 3.0.0-0.3
- Updated to current upstream state of 3.0.0 beta 2 development

* Mon Jul 23 2012 Alexander Bokovoy <abokovy@redhat.com> - 3.0.0-0.2
- Rebuild against samba4 beta4

* Mon Jul  2 2012 Rob Crittenden <rcritten@redhat.com> - 3.0.0-0.1
- Updated to upstream 3.0.0 beta 1

* Thu May  3 2012 Rob Crittenden <rcritten@redhat.com> - 2.2.0-1
- Updated to upstream 2.2.0 GA
- Update minimum n-v-r of certmonger to 0.53
- Update minimum n-v-r of slapi-nis to 0.40
- Add Requires in client to oddjob-mkhomedir and python-krbV
- Update minimum selinux-policy to 3.10.0-110

* Mon Mar 19 2012 Rob Crittenden <rcritten@redhat.com> - 2.1.90-0.2
- Update to upstream 2.2.0 beta 1 (2.1.90.rc1)
- Set minimum n-v-r for pki-ca and pki-silent to 9.0.18.
- Add Conflicts on mod_ssl
- Update minimum n-v-r of 389-ds-base to 1.2.10.4
- Update minimum n-v-r of sssd to 1.8.0
- Update minimum n-v-r of slapi-nis to 0.38
- Update minimum n-v-r of pki-* to 9.0.18
- Update conflicts on bind-dyndb-ldap to < 1.1.0-0.9.b1
- Update conflicts on bind to < 9.9.0-1
- Drop requires on krb5-server-ldap
- Add patch to remove escaping arguments to pkisilent

* Mon Feb 06 2012 Rob Crittenden <rcritten@redhat.com> - 2.1.90-0.1
- Update to upstream 2.2.0 alpha 1 (2.1.90.pre1)

* Wed Feb 01 2012 Alexander Bokovoy <abokovoy@redhat.com> - 2.1.4-5
- Force to use 389-ds 1.2.10-0.8.a7 or above
- Improve upgrade script to handle systemd 389-ds change
- Fix freeipa to work with python-ldap 2.4.6

* Wed Jan 11 2012 Martin Kosek <mkosek@redhat.com> - 2.1.4-4
- Fix ipa-replica-install crashes
- Fix ipa-server-install and ipa-dns-install logging
- Set minimum version of pki-ca to 9.0.17 to fix sslget problem
  caused by FEDORA-2011-17400 update (#771357)

* Wed Dec 21 2011 Alexander Bokovoy <abokovoy@redhat.com> - 2.1.4-3
- Allow Web-based migration to work with tightened SE Linux policy (#769440)
- Rebuild slapi plugins against re-enterant version of libldap

* Sun Dec 11 2011 Alexander Bokovoy <abokovoy@redhat.com> - 2.1.4-2
- Allow longer dirsrv startup with systemd:
  - IPAdmin class will wait until dirsrv instance is available up to 10 seconds
  - Helps with restarts during upgrade for ipa-ldap-updater
- Fix pylint warnings from F16 and Rawhide

* Tue Dec  6 2011 Rob Crittenden <rcritten@redhat.com> - 2.1.4-1
- Update to upstream 2.1.4 (CVE-2011-3636)

* Mon Dec  5 2011 Rob Crittenden <rcritten@redhat.com> - 2.1.3-8
- Update SELinux policy to allow ipa_kpasswd to connect ldap and
  read /dev/urandom. (#759679)

* Wed Nov 30 2011 Alexander Bokovoy <abokovoy@redhat.com> - 2.1.3-7
- Fix wrong path in packaging freeipa-systemd-upgrade

* Wed Nov 30 2011 Alexander Bokovoy <abokovoy@redhat.com> - 2.1.3-6
- Introduce upgrade script to recover existing configuration after systemd migration
  as user has no means to recover FreeIPA from systemd migration
- Upgrade script:
  - recovers symlinks in Dogtag instance install
  - recovers systemd configuration for FreeIPA's directory server instances
  - recovers freeipa.service
  - migrates directory server and KDC configs to use proper keytabs for systemd services

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-5
- Rebuilt for glibc bug#747377

* Wed Oct 19 2011 Alexander Bokovoy <abokovoy@redhat.com> - 2.1.3-4
- clean up spec
- Depend on sssd >= 1.6.2 for better user experience

* Tue Oct 18 2011 Alexander Bokovoy <abokovoy@redhat.com> - 2.1.3-3
- Fix Fedora package changelog after merging systemd changes

* Tue Oct 18 2011 Alexander Bokovoy <abokovoy@redhat.com> - 2.1.3-2
- Fix postin scriplet for F-15/F-16

* Tue Oct 18 2011 Alexander Bokovoy <abokovoy@redhat.com> - 2.1.3-1
- 2.1.3

* Mon Oct 17 2011 Alexander Bokovoy <abokovoy@redhat.com> - 2.1.2-1
- Default to systemd for Fedora 16 and onwards

* Tue Aug 16 2011 Rob Crittenden <rcritten@redhat.com> - 2.1.0-1
- Update to upstream 2.1.0

* Fri May  6 2011 Simo Sorce <ssorce@redhat.com> - 2.0.1-2
- Fix bug #702633

* Mon May  2 2011 Rob Crittenden <rcritten@redhat.com> - 2.0.1-1
- Update minimum selinux-policy to 3.9.16-18
- Update minimum pki-ca and pki-selinux to 9.0.7
- Update minimum 389-ds-base to 1.2.8.0-1
- Update to upstream 2.0.1

* Thu Mar 24 2011 Rob Crittenden <rcritten@redhat.com> - 2.0.0-1
- Update to upstream GA release
- Automatically apply updates when the package is upgraded

* Fri Feb 25 2011 Rob Crittenden <rcritten@redhat.com> - 2.0.0-0.4.rc2
- Update to upstream freeipa-2.0.0.rc2
- Set minimum version of python-nss to 0.11 to make sure IPv6 support is in
- Set minimum version of sssd to 1.5.1
- Patch to include SuiteSpotGroup when setting up 389-ds instances
- Move a lot of BuildRequires so this will build with ONLY_CLIENT enabled

* Tue Feb 15 2011 Rob Crittenden <rcritten@redhat.com> - 2.0.0-0.3.rc1
- Set the N-V-R so rc1 is an update to beta2.

* Mon Feb 14 2011 Rob Crittenden <rcritten@redhat.com> - 2.0.0-0.1.rc1
- Set minimum version of sssd to 1.5.1
- Update to upstream freeipa-2.0.0.rc1
- Move server-only binaries from admintools subpackage to server

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.2.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Rob Crittenden <rcritten@redhat.com> - 2.0.0-0.1.beta2
- Set min version of 389-ds-base to 1.2.8
- Set min version of mod_nss 1.0.8-10
- Set min version of selinux-policy to 3.9.7-27
- Add dogtag themes to Requires
- Update to upstream freeipa-2.0.0.pre2

* Thu Jan 27 2011 Rob Crittenden <rcritten@redhat.com> - 2.0.0-0.2.beta.git80e87e7
- Remove unnecessary moving of v1 CA serial number file in post script
- Add Obsoletes for server-selinxu subpackage
- Using git snapshot 442d6ad30ce1156914e6245aa7502499e50ec0da

* Wed Jan 26 2011 Rob Crittenden <rcritten@redhat.com> - 2.0.0-0.1.beta.git80e87e7
- Prepare spec file for release
- Using git snapshot 80e87e75bd6ab56e3e20c49ece55bd4d52f1a503

* Tue Jan 25 2011 Rob Crittenden <rcritten@redhat.com> - 1.99-41
- Re-arrange doc and defattr to clean up rpmlint warnings
- Remove conditionals on older releases
- Move some man pages into admintools subpackage
- Remove some explicit Requires in client that aren't needed
- Consistent use of buildroot vs RPM_BUILD_ROOT

* Wed Jan 19 2011 Adam Young <ayoung@redhat.com> - 1.99-40
- Moved directory install/static to install/ui

* Thu Jan 13 2011 Simo Sorce <ssorce@redhat.com> - 1.99-39
- Remove dependency on nss_ldap/nss-pam-ldapd
- The official client is sssd and that's what we use by default.

* Thu Jan 13 2011 Simo Sorce <ssorce@redhat.com> - 1.99-38
- Remove radius subpackages

* Thu Jan 13 2011 Rob Crittenden <rcritten@redhat.com> - 1.99-37
- Set minimum pki-ca and pki-silent versions to 9.0.0

* Wed Jan 12 2011 Rob Crittenden <rcritten@redhat.com> - 1.99-36
- Drop BuildRequires on mozldap-devel

* Mon Dec 13 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-35
- Add Requires on krb5-pkinit-openssl

* Fri Dec 10 2010 Jr Aquino <jr.aquino@citrix.com> - 1.99-34
- Add ipa-host-net-manage script

* Tue Dec  7 2010 Simo Sorce <ssorce@redhat.com> - 1.99-33
- Add ipa init script

* Fri Nov 19 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-32
- Set minimum level of 389-ds-base to 1.2.7 for enhanced memberof plugin

* Wed Nov  3 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-31
- remove ipa-fix-CVE-2008-3274

* Wed Oct  6 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-30
- Remove duplicate %%files entries on share/ipa/static
- Add python default encoding shared library

* Mon Sep 20 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-29
- Drop requires on python-configobj (not used any more)
- Drop ipa-ldap-updater message, upgrades are done differently now

* Wed Sep  8 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-28
- Drop conflicts on mod_nss
- Require nss-pam-ldapd on F-14 or higher instead of nss_ldap (#606847)
- Drop a slew of conditionals on older Fedora releases (< 12)
- Add a few conditionals against RHEL 6
- Add Requires of nss-tools on ipa-client

* Fri Aug 13 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-27
- Set minimum version of certmonger to 0.26 (to pck up #621670)
- Set minimum version of pki-silent to 1.3.4 (adds -key_algorithm)
- Set minimum version of pki-ca to 1.3.6
- Set minimum version of sssd to 1.2.1

* Tue Aug 10 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-26
- Add BuildRequires for authconfig

* Mon Jul 19 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-25
- Bump up minimum version of python-nss to pick up nss_is_initialize() API

* Thu Jun 24 2010 Adam Young <ayoung@redhat.com> - 1.99-24
- Removed python-asset based webui

* Thu Jun 24 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-23
- Change Requires from fedora-ds-base to 389-ds-base
- Set minimum level of 389-ds-base to 1.2.6 for the replication
  version plugin.

* Tue Jun  1 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-22
- Drop Requires of python-krbV on ipa-client

* Mon May 17 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-21
- Load ipa_dogtag.pp in post install

* Mon Apr 26 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-20
- Set minimum level of sssd to 1.1.1 to pull in required hbac fixes.

* Thu Mar  4 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-19
- No need to create /var/log/ipa_error.log since we aren't using
  TurboGears any more.

* Mon Mar 1 2010 Jason Gerard DeRose <jderose@redhat.com> - 1.99-18
- Fixed share/ipa/wsgi.py so .pyc, .pyo files are included

* Wed Feb 24 2010 Jason Gerard DeRose <jderose@redhat.com> - 1.99-17
- Added Require mod_wsgi, added share/ipa/wsgi.py

* Thu Feb 11 2010 Jason Gerard DeRose <jderose@redhat.com> - 1.99-16
- Require python-wehjit >= 0.2.2

* Wed Feb  3 2010 Rob Crittenden <rcritten@redhat.com> - 1.99-15
- Add sssd and certmonger as a Requires on ipa-client

* Wed Jan 27 2010 Jason Gerard DeRose <jderose@redhat.com> - 1.99-14
- Require python-wehjit >= 0.2.0

* Fri Dec  4 2009 Rob Crittenden <rcritten@redhat.com> - 1.99-13
- Add ipa-rmkeytab tool

* Tue Dec  1 2009 Rob Crittenden <rcritten@redhat.com> - 1.99-12
- Set minimum of python-pyasn1 to 0.0.9a so we have support for the ASN.1
  Any type

* Wed Nov 25 2009 Rob Crittenden <rcritten@redhat.com> - 1.99-11
- Remove v1-style /etc/ipa/ipa.conf, replacing with /etc/ipa/default.conf

* Fri Nov 13 2009 Rob Crittenden <rcritten@redhat.com> - 1.99-10
- Add bash completion script and own /etc/bash_completion.d in case it
  doesn't already exist

* Tue Nov  3 2009 Rob Crittenden <rcritten@redhat.com> - 1.99-9
- Remove ipa_webgui, its functions rolled into ipa_httpd

* Mon Oct 12 2009 Jason Gerard DeRose <jderose@redhat.com> - 1.99-8
- Removed python-cherrypy from BuildRequires and Requires
- Added Requires python-assets, python-wehjit

* Mon Aug 24 2009 Rob Crittenden <rcritten@redhat.com> - 1.99-7
- Added httpd SELinux policy so CRLs can be read

* Thu May 21 2009 Rob Crittenden <rcritten@redhat.com> - 1.99-6
- Move ipalib to ipa-python subpackage
- Bump minimum version of slapi-nis to 0.15

* Wed May  6 2009 Rob Crittenden <rcritten@redhat.com> - 1.99-5
- Set 0.14 as minimum version for slapi-nis

* Wed Apr 22 2009 Rob Crittenden <rcritten@redhat.com> - 1.99-4
- Add Requires: python-nss to ipa-python sub-package

* Thu Mar  5 2009 Rob Crittenden <rcritten@redhat.com> - 1.99-3
- Remove the IPA DNA plugin, use the DS one

* Wed Mar  4 2009 Rob Crittenden <rcritten@redhat.com> - 1.99-2
- Build radius separately
- Fix a few minor issues

* Tue Feb  3 2009 Rob Crittenden <rcritten@redhat.com> - 1.99-1
- Replace TurboGears requirement with python-cherrypy

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.1-3
- rebuild with new openssl

* Fri Dec 19 2008 Dan Walsh <dwalsh@redhat.com> - 1.2.1-2
- Fix SELinux code

* Mon Dec 15 2008 Simo Sorce <ssorce@redhat.com> - 1.2.1-1
- Fix breakage caused by python-kerberos update to 1.1

* Fri Dec 5 2008 Simo Sorce <ssorce@redhat.com> - 1.2.1-0
- New upstream release 1.2.1

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.0-4
- Rebuild for Python 2.6

* Fri Nov 14 2008 Simo Sorce <ssorce@redhat.com> - 1.2.0-3
- Respin after the tarball has been re-released upstream
  New hash is 506c9c92dcaf9f227cba5030e999f177

* Thu Nov 13 2008 Simo Sorce <ssorce@redhat.com> - 1.2.0-2
- Conditionally restart also dirsrv and httpd when upgrading

* Wed Oct 29 2008 Rob Crittenden <rcritten@redhat.com> - 1.2.0-1
- Update to upstream version 1.2.0
- Set fedora-ds-base minimum version to 1.1.3 for winsync header
- Set the minimum version for SELinux policy
- Remove references to Fedora 7

* Wed Jul 23 2008 Simo Sorce <ssorce@redhat.com> - 1.1.0-3
- Fix for CVE-2008-3274
- Fix segfault in ipa-kpasswd in case getifaddrs returns a NULL interface
- Add fix for bug #453185
- Rebuild against openldap libraries, mozldap ones do not work properly
- TurboGears is currently broken in rawhide. Added patch to not build
  the UI locales and removed them from the ipa-server files section.

* Wed Jun 18 2008 Rob Crittenden <rcritten@redhat.com> - 1.1.0-2
- Add call to /usr/sbin/upgradeconfig to post install

* Wed Jun 11 2008 Rob Crittenden <rcritten@redhat.com> - 1.1.0-1
- Update to upstream version 1.1.0
- Patch for indexing memberof attribute
- Patch for indexing uidnumber and gidnumber
- Patch to change DNA default values for replicas
- Patch to fix uninitialized variable in ipa-getkeytab

* Fri May 16 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.0-5
- Set fedora-ds-base minimum version to 1.1.0.1-4 and mod_nss minimum
  version to 1.0.7-4 so we pick up the NSS fixes.
- Add selinux-policy-base(post) to Requires (446496)

* Tue Apr 29 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.0-4
- Add missing entry for /var/cache/ipa/kpasswd (444624)
- Added patch to fix permissions problems with the Apache NSS database.
- Added patch to fix problem with DNS querying where the query could be
  returned as the answer.
- Fix spec error where patch1 was in the wrong section

* Fri Apr 25 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.0-3
- Added patch to fix problem reported by ldapmodify

* Fri Apr 25 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.0-2
- Fix Requires for krb5-server that was missing for Fedora versions > 9
- Remove quotes around test for fedora version to package egg-info

* Fri Apr 18 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.0-1
- Update to upstream version 1.0.0

* Tue Mar 18 2008 Rob Crittenden <rcritten@redhat.com> 0.99-12
- Pull upstream changelog 722
- Add Conflicts mod_ssl (435360)

* Fri Feb 29 2008 Rob Crittenden <rcritten@redhat.com> 0.99-11
- Pull upstream changelog 698
- Fix ownership of /var/log/ipa_error.log during install (435119)
- Add pwpolicy command and man page

* Thu Feb 21 2008 Rob Crittenden <rcritten@redhat.com> 0.99-10
- Pull upstream changelog 678
- Add new subpackage, ipa-server-selinux
- Add Requires: authconfig to ipa-python (bz #433747)
- Package i18n files

* Mon Feb 18 2008 Rob Crittenden <rcritten@redhat.com> 0.99-9
- Pull upstream changelog 641
- Require minimum version of krb5-server on F-7 and F-8
- Package some new files

* Thu Jan 31 2008 Rob Crittenden <rcritten@redhat.com> 0.99-8
- Marked with wrong license. IPA is GPLv2.

* Tue Jan 29 2008 Rob Crittenden <rcritten@redhat.com> 0.99-7
- Ensure that /etc/ipa exists before moving user-modifiable html files there
- Put html files into /etc/ipa/html instead of /etc/ipa

* Tue Jan 29 2008 Rob Crittenden <rcritten@redhat.com> 0.99-6
- Pull upstream changelog 608 which renamed several files

* Thu Jan 24 2008 Rob Crittenden <rcritten@redhat.com> 0.99-5
- package the sessions dir /var/cache/ipa/sessions
- Pull upstream changelog 597

* Thu Jan 24 2008 Rob Crittenden <rcritten@redhat.com> 0.99-4
- Updated upstream pull (596) to fix bug in ipa_webgui that was causing the
  UI to not start.

* Thu Jan 24 2008 Rob Crittenden <rcritten@redhat.com> 0.99-3
- Included LICENSE and README in all packages for documentation
- Move user-modifiable content to /etc/ipa and linked back to
  /usr/share/ipa/html
- Changed some references to /usr to the {_usr} macro and /etc
  to {_sysconfdir}
- Added popt-devel to BuildRequires for Fedora 8 and higher and
  popt for Fedora 7
- Package the egg-info for Fedora 9 and higher for ipa-python

* Tue Jan 22 2008 Rob Crittenden <rcritten@redhat.com> 0.99-2
- Added auto* BuildRequires

* Mon Jan 21 2008 Rob Crittenden <rcritten@redhat.com> 0.99-1
- Unified spec file

* Thu Jan 17 2008 Rob Crittenden <rcritten@redhat.com> - 0.6.0-2
- Fixed License in specfile
- Include files from /usr/lib/python*/site-packages/ipaserver

* Fri Dec 21 2007 Karl MacMillan <kmacmill@redhat.com> - 0.6.0-1
- Version bump for release

* Wed Nov 21 2007 Karl MacMillan <kmacmill@mentalrootkit.com> - 0.5.0-1
- Preverse mode on ipa-keytab-util
- Version bump for relase and rpm name change

* Thu Nov 15 2007 Rob Crittenden <rcritten@redhat.com> - 0.4.1-2
- Broke invididual Requires and BuildRequires onto separate lines and
  reordered them
- Added python-tgexpandingformwidget as a dependency
- Require at least fedora-ds-base 1.1

* Thu Nov  1 2007 Karl MacMillan <kmacmill@redhat.com> - 0.4.1-1
- Version bump for release

* Wed Oct 31 2007 Karl MacMillan <kmacmill@redhat.com> - 0.4.0-6
- Add dep for freeipa-admintools and acl

* Wed Oct 24 2007 Rob Crittenden <rcritten@redhat.com> - 0.4.0-5
- Add dependency for python-krbV

* Fri Oct 19 2007 Rob Crittenden <rcritten@redhat.com> - 0.4.0-4
- Require mod_nss-1.0.7-2 for mod_proxy fixes

* Thu Oct 18 2007 Karl MacMillan <kmacmill@redhat.com> - 0.4.0-3
- Convert to autotools-based build

* Tue Sep 25 2007 Karl MacMillan <kmacmill@redhat.com> - 0.4.0-2

* Fri Sep 7 2007 Karl MacMillan <kmacmill@redhat.com> - 0.3.0-1
- Added support for libipa-dna-plugin

* Fri Aug 10 2007 Karl MacMillan <kmacmill@redhat.com> - 0.2.0-1
- Added support for ipa_kpasswd and ipa_pwd_extop

* Sun Aug  5 2007 Rob Crittenden <rcritten@redhat.com> - 0.1.0-3
- Abstracted client class to work directly or over RPC

* Wed Aug  1 2007 Rob Crittenden <rcritten@redhat.com> - 0.1.0-2
- Add mod_auth_kerb and cyrus-sasl-gssapi to Requires
- Remove references to admin server in ipa-server-setupssl
- Generate a client certificate for the XML-RPC server to connect to LDAP with
- Create a keytab for Apache
- Create an ldif with a test user
- Provide a certmap.conf for doing SSL client authentication

* Fri Jul 27 2007 Karl MacMillan <kmacmill@redhat.com> - 0.1.0-1
- Initial rpm version
