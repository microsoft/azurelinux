# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

################################################################################
Name:             dogtag-pki
################################################################################

# Don't use macros in these params since they need to be parsed by build.sh
%global           vendor_id dogtag
%global           product_name Dogtag PKI
%global           product_id dogtag-pki
%global           theme dogtag

# Upstream version number:
%global           major_version 11
%global           minor_version 8
%global           update_version 0

# Downstream release number:
# - development/stabilization (unsupported): 0.<n> where n >= 1
# - GA/update (supported): <n> where n >= 1
%global           release_number 1

# Development phase:
# - development (unsupported): alpha<n> where n >= 1
# - stabilization (unsupported): beta<n> where n >= 1
# - GA/update (supported): <none>
#global           phase

%undefine         timestamp
%undefine         commit_id

Summary:          %{product_name} Package
URL:              https://www.dogtagpki.org
# The entire source code is GPLv2 except for 'pki-tps' which is LGPLv2
License:          GPL-2.0-only AND LGPL-2.0-only
Version:          %{major_version}.%{minor_version}.%{update_version}
Release:          %{release_number}%{?phase:.}%{?phase}%{?timestamp:.}%{?timestamp}%{?commit_id:.}%{?commit_id}%{?dist}


# To create a tarball from a version tag:
# $ git archive \
#     --format=tar.gz \
#     --prefix pki-<version>/ \
#     -o pki-<version>.tar.gz \
#     <version tag>
Source: https://github.com/dogtagpki/pki/archive/v%{version}%{?phase:-}%{?phase}/pki-%{version}%{?phase:-}%{?phase}.tar.gz

# To create a patch for all changes since a version tag:
# $ git format-patch \
#     --stdout \
#     <version tag> \
#     > pki-VERSION-RELEASE.patch
# Patch: pki-VERSION-RELEASE.patch

%if 0%{?java_arches:1}
ExclusiveArch: %{java_arches}
%else
ExcludeArch: i686
%endif

################################################################################
# PKCS #11 Kit Trust
################################################################################

%global p11_kit_trust /usr/lib64/pkcs11/p11-kit-trust.so

################################################################################
# Java
################################################################################

# use Java 17 on Fedora 39 or older and RHEL 9 or older
# otherwise, use Java 21

# maven-local is a subpackage of javapackages-tools

%if 0%{?fedora} && 0%{?fedora} >= 43 || 0%{?rhel} >= 11

%define java_runtime java-25-openjdk
%define java_devel java-25-openjdk-devel
%define java_headless java-25-openjdk-headless
%define java_home %{_jvmdir}/jre-25-openjdk
%define maven_local maven-local-openjdk25

%else

%define java_runtime java-21-openjdk
%define java_devel java-21-openjdk-devel
%define java_headless java-21-openjdk-headless
%define java_home %{_jvmdir}/jre-21-openjdk
%define maven_local maven-local-openjdk21

%endif

################################################################################
# Application Server
################################################################################

%global app_server tomcat-10.1

################################################################################
# PKI
################################################################################

# Use external build dependencies unless --without build_deps is specified.
%bcond_without build_deps

# Use bundled runtime dependencies unless --with runtime_deps is specified.
%bcond_with runtime_deps

# Build with Maven unless --without maven is specified.
%bcond_without maven

# Execute unit tests unless --without test is specified.
%bcond_without test

# Build the package unless --without <package> is specified.

%bcond_without base
%bcond_without server
%bcond_without acme
%bcond_without ca
%bcond_without esc
%bcond_without est
%bcond_without kra
%bcond_without ocsp
%bcond_without tks
%bcond_without tps
%bcond_without javadoc
%bcond_without theme
%bcond_without meta
%bcond_without tests
%bcond_without debug

# Don't build console unless --with console is specified.
%bcond_with console

%if ! %{with debug}
%define debug_package %{nil}
%endif

# ignore unpackaged files from native 'tpsclient'
# REMINDER:  Remove this '%%define' once 'tpsclient' is rewritten as a Java app
%define _unpackaged_files_terminate_build 0

# The PKI UID and GID are preallocated, see:
# https://bugzilla.redhat.com/show_bug.cgi?id=476316
# https://bugzilla.redhat.com/show_bug.cgi?id=476782
# https://pagure.io/setup/blob/master/f/uidgid
# /usr/share/doc/setup/uidgid
%define pki_username pkiuser
%define pki_uid 17
%define pki_groupname pkiuser
%define pki_gid 17

# Create a home directory for PKI user at /home/pkiuser
# to store rootless Podman container.
%define pki_homedir /home/%{pki_username}

%global saveFileContext() \
if [ -s /etc/selinux/config ]; then \
     . %{_sysconfdir}/selinux/config; \
     FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
     if [ "${SELINUXTYPE}" == %1 -a -f ${FILE_CONTEXT} ]; then \
          cp -f ${FILE_CONTEXT} ${FILE_CONTEXT}.%{name}; \
     fi \
fi;

%global relabel() \
. %{_sysconfdir}/selinux/config; \
FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
selinuxenabled; \
if [ $? == 0  -a "${SELINUXTYPE}" == %1 -a -f ${FILE_CONTEXT}.%{name} ]; then \
     fixfiles -C ${FILE_CONTEXT}.%{name} restore; \
     rm -f ${FILE_CONTEXT}.%name; \
fi;

################################################################################
# Build Dependencies
################################################################################

BuildRequires:    make
BuildRequires:    cmake
BuildRequires:    gcc-c++
BuildRequires:    zip

BuildRequires:    nspr-devel
BuildRequires:    nss-devel >= 3.101

BuildRequires:    openldap-devel
BuildRequires:    pkgconfig
BuildRequires:    policycoreutils

# Java build dependencies
BuildRequires:    %{java_devel}
BuildRequires:    %{maven_local}
%if 0%{?fedora}
BuildRequires:    xmvn-tools
%endif
BuildRequires:    javapackages-tools

%if %{without runtime_deps}
BuildRequires:    xmlstarlet
%endif

BuildRequires:    tomcat-lib >= 1:10.1.36
BuildRequires:    tomcat-jakartaee-migration

BuildRequires:    pki-resteasy-core                 >= 3.0.26
BuildRequires:    pki-resteasy-client               >= 3.0.26
BuildRequires:    pki-resteasy-servlet-initializer  >= 3.0.26
BuildRequires:    pki-resteasy-jackson2-provider    >= 3.0.26
BuildRequires:    pki-resteasy                      >= 3.0.26


BuildRequires:    mvn(commons-cli:commons-cli)
BuildRequires:    mvn(commons-codec:commons-codec)
BuildRequires:    mvn(commons-io:commons-io)
BuildRequires:    mvn(commons-logging:commons-logging)
BuildRequires:    mvn(commons-net:commons-net)
BuildRequires:    mvn(org.apache.commons:commons-lang3)
BuildRequires:    mvn(org.apache.httpcomponents:httpclient)
BuildRequires:    mvn(org.slf4j:slf4j-api)
BuildRequires:    mvn(xml-apis:xml-apis)
BuildRequires:    mvn(xml-resolver:xml-resolver)
BuildRequires:    mvn(org.junit.jupiter:junit-jupiter-api)

%if %{with build_deps}
BuildRequires:    mvn(jakarta.activation:jakarta.activation-api)
BuildRequires:    mvn(jakarta.annotation:jakarta.annotation-api)
BuildRequires:    mvn(jakarta.xml.bind:jakarta.xml.bind-api)

BuildRequires:    mvn(com.fasterxml.jackson.core:jackson-annotations)
BuildRequires:    mvn(com.fasterxml.jackson.core:jackson-core)
BuildRequires:    mvn(com.fasterxml.jackson.core:jackson-databind)
BuildRequires:    mvn(com.fasterxml.jackson.module:jackson-module-jaxb-annotations)
BuildRequires:    mvn(com.fasterxml.jackson.jaxrs:jackson-jaxrs-base)
BuildRequires:    mvn(com.fasterxml.jackson.jaxrs:jackson-jaxrs-json-provider)

BuildRequires:    mvn(org.jboss.spec.javax.ws.rs:jboss-jaxrs-api_2.0_spec)
BuildRequires:    mvn(org.jboss.logging:jboss-logging)

BuildRequires:    mvn(org.jboss.resteasy:resteasy-jaxrs)
BuildRequires:    mvn(org.jboss.resteasy:resteasy-client)
BuildRequires:    mvn(org.jboss.resteasy:resteasy-jackson2-provider)
BuildRequires:    mvn(org.jboss.resteasy:resteasy-servlet-initializer)
%endif

BuildRequires:    mvn(org.apache.tomcat:tomcat-catalina) >= 10.1.36
BuildRequires:    mvn(org.apache.tomcat:tomcat-servlet-api) >= 10.1.36
BuildRequires:    mvn(org.apache.tomcat:tomcat-jaspic-api) >= 10.1.36
BuildRequires:    mvn(org.apache.tomcat:tomcat-util-scan) >= 10.0.36

BuildRequires:    mvn(org.dogtagpki.jss:jss-base) >= 5.8
BuildRequires:    mvn(org.dogtagpki.jss:jss-tomcat) >= 5.8
BuildRequires:    mvn(org.dogtagpki.ldap-sdk:ldapjdk) >= 5.6.0

# Python build dependencies
BuildRequires:    python3 >= 3.6
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-cryptography
BuildRequires:    python3-lxml
BuildRequires:    python3-ldap
BuildRequires:    python3-libselinux
BuildRequires:    python3-requests >= 2.6.0
BuildRequires:    python3-six
BuildRequires:    python3-sphinx

BuildRequires:    systemd-units

# additional build requirements needed to build native 'tpsclient'
# REMINDER:  Revisit these once 'tpsclient' is rewritten as a Java app
BuildRequires:    apr-devel
BuildRequires:    apr-util-devel
BuildRequires:    cyrus-sasl-devel
BuildRequires:    httpd-devel >= 2.4.2
BuildRequires:    systemd

# build dependency to build man pages
BuildRequires:    golang-github-cpuguy83-md2man

# pki-healthcheck depends on the following library
%if 0%{?rhel}
BuildRequires:    ipa-healthcheck-core
%else
BuildRequires:    freeipa-healthcheck-core
%endif

# PKICertImport depends on certutil and openssl
BuildRequires:    nss-tools
BuildRequires:    openssl

# description for top-level package (if there is a separate meta package)
%if "%{name}" != "%{product_id}"
%description

%{product_name} is an enterprise software system designed
to manage enterprise Public Key Infrastructure deployments.

%{product_name} consists of the following components:

  * Certificate Authority (CA)
  * Key Recovery Authority (KRA)
  * Online Certificate Status Protocol (OCSP) Manager
  * Token Key Service (TKS)
  * Token Processing Service (TPS)
  * Automatic Certificate Management Environment (ACME) Responder
  * Enrollment over Secure Transport (EST) Responder

%endif

%if %{with meta}
%if "%{name}" != "%{product_id}"
################################################################################
%package -n       %{product_id}
################################################################################

Summary:          %{product_name} Package
%endif

Obsoletes:        pki-symkey < %{version}
Obsoletes:        %{product_id}-symkey < %{version}
Obsoletes:        pki-console < %{version}
Obsoletes:        pki-console-theme < %{version}

%if %{with base}
Requires:         %{product_id}-base = %{version}-%{release}
Requires:         python3-%{product_id} = %{version}-%{release}
Requires:         %{product_id}-java = %{version}-%{release}
Requires:         %{product_id}-tools = %{version}-%{release}
%endif

%if %{with server}
Requires:         %{product_id}-server = %{version}-%{release}
%endif

%if %{with acme}
Requires:         %{product_id}-acme = %{version}-%{release}
%else
Obsoletes:        pki-acme < %{version}
Conflicts:        pki-acme < %{version}

Obsoletes:        %{product_id}-acme < %{version}
Conflicts:        %{product_id}-acme < %{version}
%endif

%if %{with ca}
Requires:         %{product_id}-ca = %{version}-%{release}
%else
Obsoletes:        pki-ca < %{version}
Conflicts:        pki-ca < %{version}

Obsoletes:        %{product_id}-ca < %{version}
Conflicts:        %{product_id}-ca < %{version}
%endif

%if %{with est}
Requires:         %{product_id}-est = %{version}-%{release}
%else
Obsoletes:        pki-est < %{version}
Conflicts:        pki-est < %{version}

Obsoletes:        %{product_id}-est < %{version}
Conflicts:        %{product_id}-est < %{version}
%endif

%if %{with kra}
Requires:         %{product_id}-kra = %{version}-%{release}
%else
Obsoletes:        pki-kra < %{version}
Conflicts:        pki-kra < %{version}

Obsoletes:        %{product_id}-kra < %{version}
Conflicts:        %{product_id}-kra < %{version}
%endif

%if %{with ocsp}
Requires:         %{product_id}-ocsp = %{version}-%{release}
%else
Obsoletes:        pki-ocsp < %{version}
Conflicts:        pki-ocsp < %{version}

Obsoletes:        %{product_id}-ocsp < %{version}
Conflicts:        %{product_id}-ocsp < %{version}
%endif

%if %{with tks}
Requires:         %{product_id}-tks = %{version}-%{release}
%else
Obsoletes:        pki-tks < %{version}
Conflicts:        pki-tks < %{version}

Obsoletes:        %{product_id}-tks < %{version}
Conflicts:        %{product_id}-tks < %{version}
%endif

%if %{with tps}
Requires:         %{product_id}-tps = %{version}-%{release}
%else
Obsoletes:        pki-tps < %{version}
Conflicts:        pki-tps < %{version}

Obsoletes:        %{product_id}-tps < %{version}
Conflicts:        %{product_id}-tps < %{version}
%endif

%if %{with javadoc}
Requires:         %{product_id}-javadoc = %{version}-%{release}
%else
Obsoletes:        pki-javadoc < %{version}
Conflicts:        pki-javadoc < %{version}

Obsoletes:        %{product_id}-javadoc < %{version}
Conflicts:        %{product_id}-javadoc < %{version}
%endif

%if %{with console}
Requires:         %{product_id}-console = %{version}-%{release}
%else
Obsoletes:        pki-console < %{version}
Conflicts:        pki-console < %{version}

Obsoletes:        %{product_id}-console < %{version}
Conflicts:        %{product_id}-console < %{version}
%endif

%if %{with theme}
Requires:         %{product_id}-theme = %{version}-%{release}
%if %{with console}
Requires:         %{product_id}-console-theme = %{version}-%{release}
%endif
%else
Obsoletes:        pki-theme < %{version}
Conflicts:        pki-theme < %{version}

Obsoletes:        %{product_id}-theme < %{version}
Conflicts:        %{product_id}-theme < %{version}

Obsoletes:        pki-console-theme < %{version}
Conflicts:        pki-console-theme < %{version}

Obsoletes:        %{product_id}-console-theme < %{version}
Conflicts:        %{product_id}-console-theme < %{version}
%endif

%if %{with tests}
Requires:         %{product_id}-tests = %{version}-%{release}
%endif

%if %{with esc}
# Make certain that this 'meta' package requires the latest version(s)
# of ALL PKI clients -- except for s390/s390x where 'esc' is not built
%ifnarch s390 s390x
Requires:         esc >= 1.1.2
%endif
%else
Obsoletes:        esc <= 1.1.2
Conflicts:        esc <= 1.1.2
%endif

# description for top-level package (unless there is a separate meta package)
%if "%{name}" == "%{product_id}"
%description
%else
%description -n   %{product_id}
%endif

%{product_name} is an enterprise software system designed
to manage enterprise Public Key Infrastructure deployments.

%{product_name} consists of the following components:

  * Certificate Authority (CA)
  * Key Recovery Authority (KRA)
  * Online Certificate Status Protocol (OCSP) Manager
  * Token Key Service (TKS)
  * Token Processing Service (TPS)
  * Automatic Certificate Management Environment (ACME) Responder
  * Enrollment over Secure Transport (EST) Responder

# with meta
%endif

%if %{with base}
################################################################################
%package -n       %{product_id}-base
################################################################################

Summary:          %{product_name} Base Package
BuildArch:        noarch

Obsoletes:        pki-base < %{version}-%{release}
Provides:         pki-base = %{version}-%{release}

Requires:         nss >= 3.101

Requires:         python3-pki = %{version}-%{release}
Requires(post):   python3-pki = %{version}-%{release}

# Ensure we end up with a useful installation
Conflicts:        pki-javadoc < %{version}
Conflicts:        pki-server-theme < %{version}
Conflicts:        %{product_id}-theme < %{version}

%description -n   %{product_id}-base
This package provides default configuration files for %{product_name} client.

################################################################################
%package -n       python3-%{product_id}
################################################################################

Summary:          %{product_name} Python 3 Package
BuildArch:        noarch

Obsoletes:        python3-pki < %{version}-%{release}
Provides:         python3-pki = %{version}-%{release}

Obsoletes:        pki-base-python3 < %{version}-%{release}
Provides:         pki-base-python3 = %{version}-%{release}

%{?python_provide:%python_provide python3-pki}

Requires:         %{product_id}-base = %{version}-%{release}
Requires:         python3 >= 3.6
Requires:         python3-cryptography
Requires:         python3-ldap
Requires:         python3-lxml
Requires:         python3-requests >= 2.6.0
Requires:         python3-six

%description -n   python3-%{product_id}
This package provides common and client library for Python 3.

################################################################################
%package -n       %{product_id}-java
################################################################################

Summary:          %{product_name} Base Java Package
BuildArch:        noarch

Obsoletes:        pki-base-java < %{version}-%{release}
Provides:         pki-base-java = %{version}-%{release}

Obsoletes:        %{product_id}-base-java < %{version}-%{release}
Provides:         %{product_id}-base-java = %{version}-%{release}

Requires:         %{java_headless}
Requires:         mvn(commons-cli:commons-cli)
Requires:         mvn(commons-codec:commons-codec)
Requires:         mvn(commons-io:commons-io)
Requires:         mvn(commons-logging:commons-logging)
Requires:         mvn(commons-net:commons-net)
Requires:         mvn(org.apache.commons:commons-lang3)
Requires:         mvn(org.apache.httpcomponents:httpclient)
Requires:         mvn(org.slf4j:slf4j-api)
Requires:         mvn(org.slf4j:slf4j-jdk14)

%if %{with runtime_deps}
Requires:         mvn(jakarta.activation:jakarta.activation-api)
Requires:         mvn(jakarta.annotation:jakarta.annotation-api)
Requires:         mvn(jakarta.xml.bind:jakarta.xml.bind-api)

Requires:         mvn(com.fasterxml.jackson.core:jackson-annotations)
Requires:         mvn(com.fasterxml.jackson.core:jackson-core)
Requires:         mvn(com.fasterxml.jackson.core:jackson-databind)
Requires:         mvn(com.fasterxml.jackson.jaxrs:jackson-jaxrs-base)
Requires:         mvn(com.fasterxml.jackson.jaxrs:jackson-jaxrs-json-provider)

Requires:         mvn(org.jboss.spec.javax.ws.rs:jboss-jaxrs-api_2.0_spec)
Requires:         mvn(org.jboss.logging:jboss-logging)

Requires:         mvn(org.jboss.resteasy:resteasy-jaxrs)
Requires:         mvn(org.jboss.resteasy:resteasy-client)
Requires:         mvn(org.jboss.resteasy:resteasy-jackson2-provider)
%else
Provides:         bundled(jakarta-activation)
Provides:         bundled(jakarta-annotations)
Provides:         bundled(jaxb-api)

Provides:         bundled(jackson-annotations)
Provides:         bundled(jackson-core)
Provides:         bundled(jackson-databind)
Provides:         bundled(jackson-modules-base)
Provides:         bundled(jackson-jaxrs-providers)
Provides:         bundled(jackson-jaxrs-json-provider)

Provides:         bundled(jboss-jaxrs-2.0-api)
Provides:         bundled(jboss-logging)

Provides:         bundled(resteasy-jaxrs)
Provides:         bundled(resteasy-client)
Provides:         bundled(resteasy-jackson2-provider)
%endif

Requires:         mvn(org.dogtagpki.jss:jss-base) >= 5.8
Requires:         mvn(org.dogtagpki.ldap-sdk:ldapjdk) >= 5.6.0
Requires:         %{product_id}-base = %{version}-%{release}

%description -n   %{product_id}-java
This package provides common and client libraries for Java.

################################################################################
%package -n       %{product_id}-tools
################################################################################

Summary:          %{product_name} Tools Package

Obsoletes:        pki-tools < %{version}-%{release}
Provides:         pki-tools = %{version}-%{release}

Requires:         openldap-clients
Requires:         nss-tools >= 3.101
Requires:         %{product_id}-java = %{version}-%{release}
Requires:         p11-kit-trust
Requires:         file

# PKICertImport depends on certutil and openssl
Requires:         nss-tools
Requires:         openssl

%description -n   %{product_id}-tools
This package provides tools that can be used to help make
%{product_name} into a more complete and robust PKI solution.

The utility "tpsclient" is a test tool that interacts with TPS.
This tool is useful to test TPS server without risking an actual smart card.

# with base
%endif

%if %{with server}
################################################################################
%package -n       %{product_id}-server
################################################################################

Summary:          %{product_name} Server Package
BuildArch:        noarch

Obsoletes:        pki-server < %{version}-%{release}
Provides:         pki-server = %{version}-%{release}

Requires:         hostname

Requires:         policycoreutils
Requires:         procps-ng
Requires:         openldap-clients
Requires:         openssl
Requires:         %{product_id}-tools = %{version}-%{release}

Requires:         %{java_devel}

Requires:         keyutils

Requires:         policycoreutils-python-utils

Requires:         python3-lxml
Requires:         python3-libselinux
Requires:         python3-policycoreutils

Requires:         selinux-policy-targeted >= 3.13.1-159

%if %{with runtime_deps}
Requires:         mvn(org.jboss.resteasy:resteasy-servlet-initializer)
%else
Provides:         bundled(resteasy-servlet-initializer)
%endif

Requires:         tomcat >= 1:10.1.36

Requires:         mvn(org.dogtagpki.jss:jss-tomcat) >= 5.8

Requires:         systemd
Requires(post):   systemd-units
Requires(postun): systemd-units
Requires(pre):    shadow-utils

# pki-healthcheck depends on the following library
%if 0%{?rhel}
Requires:         ipa-healthcheck-core
%else
Requires:         freeipa-healthcheck-core
%endif

# https://pagure.io/freeipa/issue/7742
%if 0%{?rhel}
Conflicts:        ipa-server < 4.7.1
%else
Conflicts:        freeipa-server < 4.7.1
%endif

Provides:         bundled(js-backbone) = 1.6.0
Provides:         bundled(js-bootstrap) = 3.4.1
Provides:         bundled(js-jquery) = 3.7.1
Provides:         bundled(js-jquery-i18n-properties) = 1.2.7
Provides:         bundled(js-patternfly) = 3.59.2
Provides:         bundled(js-underscore) = 1.13.7

%description -n   %{product_id}-server
This package provides libraries and utilities needed by %{product_name} services.

# with server
%endif

%if %{with acme}
################################################################################
%package -n       %{product_id}-acme
################################################################################

Summary:          %{product_name} ACME Package
BuildArch:        noarch

Obsoletes:        pki-acme < %{version}-%{release}
Provides:         pki-acme = %{version}-%{release}

Requires:         %{product_id}-server = %{version}-%{release}

%description -n   %{product_id}-acme
%{product_name} ACME responder is a service that provides an automatic certificate
management via ACME v2 protocol defined in RFC 8555.

# with acme
%endif

%if %{with ca}
################################################################################
%package -n       %{product_id}-ca
################################################################################

Summary:          %{product_name} CA Package
BuildArch:        noarch

Obsoletes:        pki-ca < %{version}-%{release}
Provides:         pki-ca = %{version}-%{release}

Requires:         %{product_id}-server = %{version}-%{release}
Requires(post):   systemd-units
Requires(postun): systemd-units

%description -n   %{product_id}-ca
%{product_name} Certificate Authority (CA) is a required subsystem which issues,
renews, revokes, and publishes certificates as well as compiling and
publishing Certificate Revocation Lists (CRLs).

The Certificate Authority can be configured as a self-signing Certificate
Authority, where it is the root CA, or it can act as a subordinate CA,
where it obtains its own signing certificate from a public CA.

# with ca
%endif

%if %{with est}
################################################################################
%package -n       %{product_id}-est
################################################################################

Summary:          %{product_name} EST Package
BuildArch:        noarch

Obsoletes:        pki-est < %{version}-%{release}
Provides:         pki-est = %{version}-%{release}

Requires:         %{product_id}-server = %{version}-%{release}

%description -n   %{product_id}-est
%{product_name} EST subsystem provides an Enrollment over
Secure Transport (RFC 7030) service.

# with est
%endif

%if %{with kra}
################################################################################
%package -n       %{product_id}-kra
################################################################################

Summary:          %{product_name} KRA Package
BuildArch:        noarch

Obsoletes:        pki-kra < %{version}-%{release}
Provides:         pki-kra = %{version}-%{release}

Requires:         %{product_id}-server = %{version}-%{release}
Requires(post):   systemd-units
Requires(postun): systemd-units

%description -n   %{product_id}-kra
%{product_name} Key Recovery Authority (KRA) is an optional subsystem that can act
as a key archival facility.  When configured in conjunction with the
Certificate Authority (CA), the KRA stores private encryption keys as part of
the certificate enrollment process.  The key archival mechanism is triggered
when a user enrolls in the PKI and creates the certificate request.  Using the
Certificate Request Message Format (CRMF) request format, a request is
generated for the user's private encryption key.  This key is then stored in
the KRA which is configured to store keys in an encrypted format that can only
be decrypted by several agents requesting the key at one time, providing for
protection of the public encryption keys for the users in the PKI deployment.

Note that the KRA archives encryption keys; it does NOT archive signing keys,
since such archival would undermine non-repudiation properties of signing keys.

# with kra
%endif

%if %{with ocsp}
################################################################################
%package -n       %{product_id}-ocsp
################################################################################

Summary:          %{product_name} OCSP Package
BuildArch:        noarch

Obsoletes:        pki-ocsp < %{version}-%{release}
Provides:         pki-ocsp = %{version}-%{release}

Requires:         %{product_id}-server = %{version}-%{release}
Requires(post):   systemd-units
Requires(postun): systemd-units

%description -n   %{product_id}-ocsp
%{product_name} Online Certificate Status Protocol (OCSP) Manager is an optional
subsystem that can act as a stand-alone OCSP service.  The OCSP Manager
performs the task of an online certificate validation authority by enabling
OCSP-compliant clients to do real-time verification of certificates.  Note
that an online certificate-validation authority is often referred to as an
OCSP Responder.

Although the Certificate Authority (CA) is already configured with an
internal OCSP service.  An external OCSP Responder is offered as a separate
subsystem in case the user wants the OCSP service provided outside of a
firewall while the CA resides inside of a firewall, or to take the load of
requests off of the CA.

The OCSP Manager can receive Certificate Revocation Lists (CRLs) from
multiple CA servers, and clients can query the OCSP Manager for the
revocation status of certificates issued by all of these CA servers.

When an instance of OCSP Manager is set up with an instance of CA, and
publishing is set up to this OCSP Manager, CRLs are published to it
whenever they are issued or updated.

# with ocsp
%endif

%if %{with tks}
################################################################################
%package -n       %{product_id}-tks
################################################################################

Summary:          %{product_name} TKS Package
BuildArch:        noarch

Obsoletes:        pki-tks < %{version}-%{release}
Provides:         pki-tks = %{version}-%{release}

Requires:         %{product_id}-server = %{version}-%{release}
Requires(post):   systemd-units
Requires(postun): systemd-units

%description -n   %{product_id}-tks
%{product_name} Token Key Service (TKS) is an optional subsystem that manages the
master key(s) and the transport key(s) required to generate and distribute
keys for hardware tokens.  TKS provides the security between tokens and an
instance of Token Processing System (TPS), where the security relies upon the
relationship between the master key and the token keys.  A TPS communicates
with a TKS over SSL using client authentication.

TKS helps establish a secure channel (signed and encrypted) between the token
and the TPS, provides proof of presence of the security token during
enrollment, and supports key changeover when the master key changes on the
TKS.  Tokens with older keys will get new token keys.

Because of the sensitivity of the data that TKS manages, TKS should be set up
behind the firewall with restricted access.

# with tks
%endif

%if %{with tps}
################################################################################
%package -n       %{product_id}-tps
################################################################################

Summary:          %{product_name} TPS Package
BuildArch:        noarch

Obsoletes:        pki-tps < %{version}-%{release}
Provides:         pki-tps = %{version}-%{release}

Requires:         %{product_id}-server = %{version}-%{release}
Requires(post):   systemd-units
Requires(postun): systemd-units

# additional runtime requirements needed to run native 'tpsclient'
# REMINDER:  Revisit these once 'tpsclient' is rewritten as a Java app

Requires:         nss-tools >= 3.101
Requires:         openldap-clients

%description -n   %{product_id}-tps
%{product_name} Token Processing System (TPS) is an optional subsystem that acts
as a Registration Authority (RA) for authenticating and processing
enrollment requests, PIN reset requests, and formatting requests from
the Enterprise Security Client (ESC).

TPS is designed to communicate with tokens that conform to
Global Platform's Open Platform Specification.

TPS communicates over SSL with various PKI backend subsystems (including
the Certificate Authority (CA), the Key Recovery Authority (KRA), and the
Token Key Service (TKS)) to fulfill the user's requests.

TPS also interacts with the token database, an LDAP server that stores
information about individual tokens.

# with tps
%endif

%if %{with javadoc}
################################################################################
%package -n       %{product_id}-javadoc
################################################################################

Summary:          %{product_name} Javadoc Package
BuildArch:        noarch

Obsoletes:        pki-javadoc < %{version}-%{release}
Provides:         pki-javadoc = %{version}-%{release}

# Ensure we end up with a useful installation
Conflicts:        pki-base < %{version}
Conflicts:        pki-server-theme < %{version}
Conflicts:        %{product_id}-theme < %{version}

%description -n   %{product_id}-javadoc
This package provides %{product_name} API documentation.

# with javadoc
%endif

%if %{with console}
################################################################################
%package -n       %{product_id}-console
################################################################################

Summary:          %{product_name} Console Package
BuildArch:        noarch

Obsoletes:        pki-console < %{version}-%{release}
Provides:         pki-console = %{version}-%{release}

Requires:         %{java_runtime}
Requires:         %{product_id}-java = %{version}-%{release}
Requires:         %{product_id}-console-theme = %{version}-%{release}

# IDM Console Framework has been merged into PKI Console.
# This will remove installed IDM Console Framework packages.
Obsoletes:        idm-console-framework <= 2.1
Conflicts:        idm-console-framework <= 2.1

%description -n   %{product_id}-console
%{product_name} Console is a Java application used to administer %{product_name} Server.

# with console
%endif

%if %{with theme}
################################################################################
%package -n       %{product_id}-theme
################################################################################

Summary:          %{product_name} Server Theme Package
BuildArch:        noarch

Obsoletes:        pki-server-theme < %{version}-%{release}
Provides:         pki-server-theme = %{version}-%{release}

Obsoletes:        %{product_id}-server-theme < %{version}-%{release}
Provides:         %{product_id}-server-theme = %{version}-%{release}

%if 0%{?fedora} > 38 || 0%{?rhel} > 9
BuildRequires:    fontawesome4-fonts-web
Requires:         fontawesome4-fonts-web
%else
BuildRequires:    fontawesome-fonts-web
Requires:         fontawesome-fonts-web
%endif

# Ensure we end up with a useful installation
Conflicts:        pki-base < %{version}
Conflicts:        pki-javadoc < %{version}

%description -n   %{product_id}-theme
This package provides theme files for %{product_name}.

%if %{with console}
################################################################################
%package -n       %{product_id}-console-theme
################################################################################

Summary:          %{product_name} Console Theme Package
BuildArch:        noarch

Obsoletes:        pki-console-theme < %{version}-%{release}
Provides:         pki-console-theme = %{version}-%{release}

# Ensure we end up with a useful installation
Conflicts:        pki-base < %{version}
Conflicts:        pki-server-theme < %{version}
Conflicts:        pki-javadoc < %{version}
Conflicts:        %{product_id}-theme < %{version}

%description -n   %{product_id}-console-theme
This package provides theme files for %{product_name} Console.

# with console
%endif

# with theme
%endif

%if %{with tests}
################################################################################
%package -n       %{product_id}-tests
################################################################################

Summary:          %{product_name} Tests
BuildArch:        noarch

Obsoletes:        pki-tests < %{version}-%{release}
Provides:         pki-tests = %{version}-%{release}


%if 0%{?fedora} && 0%{?fedora} < 43
Requires:         python3-pylint
%endif

Requires:         python3-flake8

%description -n   %{product_id}-tests
This package provides test suite for %{product_name}.

# with tests
%endif

################################################################################
%prep
################################################################################

%autosetup -n pki-%{version}%{?phase:-}%{?phase} -p 1

%if %{without runtime_deps}

if [ ! -d base/common/lib ]
then
    # import common libraries from RPMs

    mkdir -p base/common/lib
    pushd base/common/lib

    JAKARTA_ACTIVATION_API_VERSION=$(rpm -q jakarta-activation | sed -n 's/^jakarta-activation-\([^-]*\)-.*$/\1/p')
    echo "JAKARTA_ACTIVATION_API_VERSION: $JAKARTA_ACTIVATION_API_VERSION"

    cp /usr/share/java/jakarta-activation/jakarta.activation-api.jar \
        jakarta.activation-api-$JAKARTA_ACTIVATION_API_VERSION.jar

    JAKARTA_ANNOTATION_API_VERSION=$(rpm -q jakarta-annotations | sed -n 's/^jakarta-annotations-\([^-]*\)-.*$/\1/p')
    echo "JAKARTA_ANNOTATION_API_VERSION: $JAKARTA_ANNOTATION_API_VERSION"

    cp /usr/share/java/jakarta-annotations/jakarta.annotation-api.jar \
        jakarta.annotation-api-$JAKARTA_ANNOTATION_API_VERSION.jar

    JAXB_API_VERSION=$(rpm -q jaxb-api | sed -n 's/^jaxb-api-\([^-]*\)-.*$/\1/p')
    echo "JAXB_API_VERSION: $JAXB_API_VERSION"

    if [ -f /usr/share/java/jaxb-api.jar ]
    then
        cp /usr/share/java/jaxb-api.jar \
            jakarta.xml.bind-api-$JAXB_API_VERSION.jar
    elif [ -f /usr/share/java/jaxb-api/jakarta.xml.bind-api.jar ]
    then
        cp /usr/share/java/jaxb-api/jakarta.xml.bind-api.jar \
            jakarta.xml.bind-api-$JAXB_API_VERSION.jar
    fi

    JACKSON_VERSION=$(rpm -q jackson-annotations | sed -n 's/^jackson-annotations-\([^-]*\)-.*$/\1/p')
    echo "JACKSON_VERSION: $JACKSON_VERSION"

    cp /usr/share/java/jackson-annotations.jar \
        jackson-annotations-$JACKSON_VERSION.jar
    cp /usr/share/java/jackson-core.jar \
        jackson-core-$JACKSON_VERSION.jar
    cp /usr/share/java/jackson-databind.jar \
        jackson-databind-$JACKSON_VERSION.jar
    cp /usr/share/java/jackson-jaxrs-providers/jackson-jaxrs-base.jar \
        jackson-jaxrs-base-$JACKSON_VERSION.jar
    cp /usr/share/java/jackson-jaxrs-providers/jackson-jaxrs-json-provider.jar \
        jackson-jaxrs-json-provider-$JACKSON_VERSION.jar
    cp /usr/share/java/jackson-modules/jackson-module-jaxb-annotations.jar \
        jackson-module-jaxb-annotations-$JACKSON_VERSION.jar

    JAXRS_VERSION=$(rpm -q jboss-jaxrs-2.0-api | sed -n 's/^jboss-jaxrs-2.0-api-\([^-]*\)-.*$/\1.Final/p')
    echo "JAXRS_VERSION: $JAXRS_VERSION"

    cp /usr/share/java/jboss-jaxrs-2.0-api.jar \
        jboss-jaxrs-api_2.0_spec-$JAXRS_VERSION.jar

    JBOSS_LOGGING_VERSION=$(rpm -q jboss-logging | sed -n 's/^jboss-logging-\([^-]*\)-.*$/\1.Final/p')
    echo "JBOSS_LOGGING_VERSION: $JBOSS_LOGGING_VERSION"

    cp /usr/share/java/jboss-logging/jboss-logging.jar \
        jboss-logging-$JBOSS_LOGGING_VERSION.jar

    RESTEASY_VERSION=$(rpm -q pki-resteasy-core | sed -n 's/^pki-resteasy-core-\([^-]*\)-.*$/\1.Final/p')
    echo "RESTEASY_VERSION: $RESTEASY_VERSION"

    cp /usr/share/java/resteasy/resteasy-jaxrs.jar \
        resteasy-jaxrs-$RESTEASY_VERSION.jar
    cp /usr/share/java/resteasy/resteasy-client.jar \
        resteasy-client-$RESTEASY_VERSION.jar
    cp /usr/share/java/resteasy/resteasy-jackson2-provider.jar \
        resteasy-jackson2-provider-$RESTEASY_VERSION.jar

    #migrate necessary files being copied around to jakarta 9.0 ee

    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE  jboss-jaxrs-api_2.0_spec-$JAXRS_VERSION.jar  jboss-jaxrs-api_2.0_spec-$JAXRS_VERSION.jar 

    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE  jackson-jaxrs-json-provider-$JACKSON_VERSION.jar jackson-jaxrs-json-provider-$JACKSON_VERSION.jar

    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE  jackson-annotations-$JACKSON_VERSION.jar jackson-annotations-$JACKSON_VERSION.jar
    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE  jackson-core-$JACKSON_VERSION.jar  jackson-core-$JACKSON_VERSION.jar
    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE  jackson-databind-$JACKSON_VERSION.jar jackson-databind-$JACKSON_VERSION.jar
    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE  jackson-jaxrs-base-$JACKSON_VERSION.jar  jackson-jaxrs-base-$JACKSON_VERSION.jar
    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE  jackson-jaxrs-json-provider-$JACKSON_VERSION.jar jackson-jaxrs-json-provider-$JACKSON_VERSION.jar 
    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE  jackson-module-jaxb-annotations-$JACKSON_VERSION.jar jackson-module-jaxb-annotations-$JACKSON_VERSION.jar

    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE   jakarta.activation-api-$JAKARTA_ACTIVATION_API_VERSION.jar  jakarta.activation-api-$JAKARTA_ACTIVATION_API_VERSION.jar
    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE   jakarta.annotation-api-$JAKARTA_ANNOTATION_API_VERSION.jar jakarta.annotation-api-$JAKARTA_ANNOTATION_API_VERSION.jar  
    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE   jakarta.xml.bind-api-$JAXB_API_VERSION.jar jakarta.xml.bind-api-$JAXB_API_VERSION.jar 

    # Now migrate the required resteasy jars, in case we are using an existing resteasy version.

    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE resteasy-client-$RESTEASY_VERSION.jar  resteasy-client-$RESTEASY_VERSION.jar
    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE resteasy-jackson2-provider-$RESTEASY_VERSION.jar resteasy-jackson2-provider-$RESTEASY_VERSION.jar
    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE resteasy-jaxrs-$RESTEASY_VERSION.jar  resteasy-jaxrs-$RESTEASY_VERSION.jar

    # Add local artifact so we can compile against the migrated jboss-jaxrs-api_2.0_spec-$JAXRS_VERSION.jar
    # We could have used the maven install plugin but it's not available with standard rpms.

    # Create the local artifact structure
    mkdir -p ~/.m2/repository/pki-local/jboss-jaxrs-api_2.0_spec/$JAXRS_VERSION
    # Copy over the jaxrs api so we can compile
    cp jboss-jaxrs-api_2.0_spec-$JAXRS_VERSION.jar  ~/.m2/repository/pki-local/jboss-jaxrs-api_2.0_spec/$JAXRS_VERSION/jboss-jaxrs-api_2.0_spec-$JAXRS_VERSION.jar

    popd
fi

if [ ! -d base/server/lib ]
then
    # import server libraries from RPMs

    mkdir -p base/server/lib
    pushd base/server/lib

    RESTEASY_VERSION=$(rpm -q pki-resteasy-servlet-initializer | sed -n 's/^pki-resteasy-servlet-initializer-\([^-]*\)-.*$/\1.Final/p')
    echo "RESTEASY_VERSION: $RESTEASY_VERSION"

    cp /usr/share/java/resteasy/resteasy-servlet-initializer.jar \
        resteasy-servlet-initializer-$RESTEASY_VERSION.jar

    # Migrate the resteasy servlet initializer, in case we are using an existing resteasy version.
    /usr/bin/javax2jakarta -logLevel=ALL -profile=EE resteasy-servlet-initializer-$RESTEASY_VERSION.jar resteasy-servlet-initializer-$RESTEASY_VERSION.jar
    ls -l
    popd
fi
%endif

%if ! %{with base}
%pom_disable_module common base
%pom_disable_module tools base
%endif

%if ! %{with server}
%pom_disable_module tomcat base
%pom_disable_module tomcat-9.0 base
%pom_disable_module server base
%pom_disable_module server-webapp base
%endif

%if ! %{with ca}
%pom_disable_module ca base
%endif

%if ! %{with kra}
%pom_disable_module kra base
%endif

%if ! %{with ocsp}
%pom_disable_module ocsp base
%endif

%if ! %{with tks}
%pom_disable_module tks base
%endif

%if ! %{with tps}
%pom_disable_module tps base
%endif

%if ! %{with acme}
%pom_disable_module acme base
%endif

%if ! %{with est}
%pom_disable_module est base
%endif

%if ! %{with console}
%pom_disable_module console base
%endif

# remove plugins not needed to build RPM
%pom_remove_plugin org.codehaus.mojo:flatten-maven-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-deploy-plugin
%pom_remove_plugin com.github.github:site-maven-plugin

# specify Maven artifact locations
%mvn_file org.dogtagpki.pki:pki-common            pki/pki-common
%mvn_file org.dogtagpki.pki:pki-tools             pki/pki-tools
%mvn_file org.dogtagpki.pki:pki-server            pki/pki-server
%mvn_file org.dogtagpki.pki:pki-server-webapp     pki/pki-server-webapp
%mvn_file org.dogtagpki.pki:pki-tomcat            pki/pki-tomcat
#%mvn_file org.dogtagpki.pki:pki-tomcat-9.0        pki/pki-tomcat-9.0
%mvn_file org.dogtagpki.pki:pki-tomcat-10.1       pki/pki-tomcat-10.1
%mvn_file org.dogtagpki.pki:pki-ca                pki/pki-ca
%mvn_file org.dogtagpki.pki:pki-kra               pki/pki-kra
%mvn_file org.dogtagpki.pki:pki-ocsp              pki/pki-ocsp
%mvn_file org.dogtagpki.pki:pki-tks               pki/pki-tks
%mvn_file org.dogtagpki.pki:pki-tps               pki/pki-tps
%mvn_file org.dogtagpki.pki:pki-acme              pki/pki-acme
%mvn_file org.dogtagpki.pki:pki-est               pki/pki-est

%if %{with console}
%mvn_file org.dogtagpki.pki:pki-console           pki/pki-console
%endif

# specify Maven artifact packages
%mvn_package org.dogtagpki.pki:pki-common         pki-java
%mvn_package org.dogtagpki.pki:pki-tools          pki-tools
%mvn_package org.dogtagpki.pki:pki-server         pki-server
%mvn_package org.dogtagpki.pki:pki-server-webapp  pki-server
%mvn_package org.dogtagpki.pki:pki-tomcat         pki-server
%mvn_package org.dogtagpki.pki:pki-tomcat-10.1     pki-server
%mvn_package org.dogtagpki.pki:pki-ca             pki-ca
%mvn_package org.dogtagpki.pki:pki-kra            pki-kra
%mvn_package org.dogtagpki.pki:pki-ocsp           pki-ocsp
%mvn_package org.dogtagpki.pki:pki-tks            pki-tks
%mvn_package org.dogtagpki.pki:pki-tps            pki-tps
%mvn_package org.dogtagpki.pki:pki-acme           pki-acme
%mvn_package org.dogtagpki.pki:pki-est            pki-est

%if %{with console}
%mvn_package org.dogtagpki.pki:pki-console        pki-console
%endif

%if 0%{?fedora} || 0%{?rhel} >= 11
# Create a sysusers.d config file

cat > %{product_id}.sysusers.conf <<EOF
g %{pki_username} %{pki_gid}
u %{pki_groupname} %{pki_uid} 'Certificate System' %{pki_homedir} -
EOF

%endif

################################################################################
%build
################################################################################

# Set build flags for CMake
# (see /usr/lib/rpm/macros.d/macros.cmake)
%set_build_flags

export JAVA_HOME=%{java_home}

%if %{with maven}
# build Java binaries and run unit tests with Maven
%mvn_build %{!?with_test:-f} -j

# create links to Maven-built JAR files for CMake
mkdir -p %{_vpath_builddir}/dist
pushd %{_vpath_builddir}/dist

%if %{with base}
ln -sf ../../base/common/target/pki-common.jar
ln -sf ../../base/tools/target/pki-tools.jar
%endif

%if %{with server}
ln -sf ../../base/tomcat/target/pki-tomcat.jar
ln -sf ../../base/tomcat-10.1/target/pki-tomcat-10.1.jar
ln -sf ../../base/server/target/pki-server.jar
ln -sf ../../base/server-webapp/target/pki-server-webapp.jar
%endif

%if %{with ca}
ln -sf ../../base/ca/target/pki-ca.jar
%endif

%if %{with kra}
ln -sf ../../base/kra/target/pki-kra.jar
%endif

%if %{with ocsp}
ln -sf ../../base/ocsp/target/pki-ocsp.jar
%endif

%if %{with tks}
ln -sf ../../base/tks/target/pki-tks.jar
%endif

%if %{with tps}
ln -sf ../../base/tps/target/pki-tps.jar
%endif

%if %{with acme}
ln -sf ../../base/acme/target/pki-acme.jar
%endif

%if %{with est}
ln -sf ../../base/est/target/pki-est.jar
%endif

%if %{with console}
ln -sf ../../base/console/target/pki-console.jar
%endif

popd

# with maven
%endif

# Remove all symbol table and relocation information from the executable.
C_FLAGS="%{optflags}"
CXX_FLAGS="%{optflags}"

pkgs=base\
%{?with_server:,server}\
%{?with_ca:,ca}\
%{?with_est:,est}\
%{?with_kra:,kra}\
%{?with_ocsp:,ocsp}\
%{?with_tks:,tks}\
%{?with_tps:,tps}\
%{?with_acme:,acme}\
%{?with_javadoc:,javadoc}\
%{?with_theme:,theme}\
%{?with_meta:,meta}\
%{?with_tests:,tests}\
%{?with_debug:,debug}

# build PKI console, Javadoc, and native binaries with CMake
./build.sh \
    %{?_verbose:-v} \
    --product-name="%{product_name}" \
    --product-id=%{product_id} \
%if %{with theme}
    --theme=%{theme} \
%endif
    --work-dir=%{_vpath_builddir} \
    --prefix-dir=%{_prefix} \
    --include-dir=%{_includedir} \
    --lib-dir=%{_libdir} \
    --sbin-dir=%{_sbindir} \
    --sysconf-dir=%{_sysconfdir} \
    --share-dir=%{_datadir} \
    --cmake=%{__cmake} \
    --c-flags="$C_FLAGS" \
    --cxx-flags="$CXX_FLAGS" \
    --java-home=%{java_home} \
    --jni-dir=%{_jnidir} \
    --unit-dir=%{_unitdir} \
    --python=%{python3} \
    --python-dir=%{python3_sitelib} \
    %{?with_maven:--without-java} \
    --with-pkgs=$pkgs \
    %{?with_console:--with-console} \
    --without-test \
    dist

################################################################################
%install
################################################################################

%if %{with maven}
# install Java binaries
%mvn_install

# Normally JAR files are installed in /usr/share/java/pki.
# Since pki-tools.jar uses JNI Maven might install it in
# /usr/lib/java/pki or /usr/share/java/pki depending on the
# build environment.
find %{buildroot} -name "*.jar"

# Create link to ensure pki-tools.jar is available at both locations.
if [ -e %{buildroot}%{_jnidir}/pki/pki-tools.jar ]; then
   ln -sf ../../../..%{_jnidir}/pki/pki-tools.jar %{buildroot}%{_javadir}/pki
else
   mkdir -p %{buildroot}%{_jnidir}/pki
   ln -sf ../../../..%{_javadir}/pki/pki-tools.jar %{buildroot}%{_jnidir}/pki
fi

# with maven
%endif

# install PKI console, Javadoc, and native binaries
./build.sh \
    %{?_verbose:-v} \
    --work-dir=%{_vpath_builddir} \
    --install-dir=%{buildroot} \
    install

%if %{without runtime_deps}

%if %{with maven}

%if %{with meta}
echo "Removing RPM deps from %{buildroot}%{_datadir}/maven-metadata/pki.xml"
xmlstarlet edit --inplace \
    -d "//_:dependency[_:groupId='jakarta.activation']" \
    -d "//_:dependency[_:groupId='jakarta.annotation']" \
    -d "//_:dependency[_:groupId='jakarta.xml.bind']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.core']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.module']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.jaxrs']" \
    -d "//_:dependency[_:groupId='org.jboss.spec.javax.ws.rs']" \
    -d "//_:dependency[_:groupId='org.jboss.logging']" \
    -d "//_:dependency[_:groupId='org.jboss.resteasy']" \
    %{buildroot}%{_datadir}/maven-metadata/%{name}.xml
%endif

%if %{with base}
echo "Removing RPM deps from %{buildroot}%{_datadir}/maven-metadata/pki-pki-java.xml"
xmlstarlet edit --inplace \
    -d "//_:dependency[_:groupId='jakarta.activation']" \
    -d "//_:dependency[_:groupId='jakarta.annotation']" \
    -d "//_:dependency[_:groupId='jakarta.xml.bind']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.core']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.module']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.jaxrs']" \
    -d "//_:dependency[_:groupId='org.jboss.spec.javax.ws.rs']" \
    -d "//_:dependency[_:groupId='pki-local']" \
    -d "//_:dependency[_:groupId='org.jboss.logging']" \
    -d "//_:dependency[_:groupId='org.jboss.resteasy']" \
    %{buildroot}%{_datadir}/maven-metadata/%{name}-pki-java.xml

echo "Removing RPM deps from %{buildroot}%{_datadir}/maven-metadata/pki-pki-tools.xml"
xmlstarlet edit --inplace \
    -d "//_:dependency[_:groupId='jakarta.activation']" \
    -d "//_:dependency[_:groupId='jakarta.annotation']" \
    -d "//_:dependency[_:groupId='jakarta.xml.bind']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.core']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.module']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.jaxrs']" \
    -d "//_:dependency[_:groupId='org.jboss.spec.javax.ws.rs']" \
    -d "//_:dependency[_:groupId='org.jboss.logging']" \
    -d "//_:dependency[_:groupId='org.jboss.resteasy']" \
    %{buildroot}%{_datadir}/maven-metadata/%{name}-pki-tools.xml
%endif

%if %{with server}
echo "Removing RPM deps from %{buildroot}%{_datadir}/maven-metadata/pki-pki-server.xml"
xmlstarlet edit --inplace \
    -d "//_:dependency[_:groupId='jakarta.activation']" \
    -d "//_:dependency[_:groupId='jakarta.annotation']" \
    -d "//_:dependency[_:groupId='jakarta.xml.bind']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.core']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.module']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.jaxrs']" \
    -d "//_:dependency[_:groupId='org.jboss.spec.javax.ws.rs']" \
    -d "//_:dependency[_:groupId='org.jboss.logging']" \
    -d "//_:dependency[_:groupId='org.jboss.resteasy']" \
    %{buildroot}%{_datadir}/maven-metadata/%{name}-pki-server.xml
%endif

%if %{with ca}
echo "Removing RPM deps from %{buildroot}%{_datadir}/maven-metadata/pki-pki-ca.xml"
xmlstarlet edit --inplace \
    -d "//_:dependency[_:groupId='jakarta.activation']" \
    -d "//_:dependency[_:groupId='jakarta.annotation']" \
    -d "//_:dependency[_:groupId='jakarta.xml.bind']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.core']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.module']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.jaxrs']" \
    -d "//_:dependency[_:groupId='org.jboss.spec.javax.ws.rs']" \
    -d "//_:dependency[_:groupId='org.jboss.logging']" \
    -d "//_:dependency[_:groupId='org.jboss.resteasy']" \
    %{buildroot}%{_datadir}/maven-metadata/%{name}-pki-ca.xml
%endif

%if %{with kra}
echo "Removing RPM deps from %{buildroot}%{_datadir}/maven-metadata/pki-pki-kra.xml"
xmlstarlet edit --inplace \
    -d "//_:dependency[_:groupId='jakarta.activation']" \
    -d "//_:dependency[_:groupId='jakarta.annotation']" \
    -d "//_:dependency[_:groupId='jakarta.xml.bind']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.core']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.module']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.jaxrs']" \
    -d "//_:dependency[_:groupId='org.jboss.spec.javax.ws.rs']" \
    -d "//_:dependency[_:groupId='org.jboss.logging']" \
    -d "//_:dependency[_:groupId='org.jboss.resteasy']" \
    %{buildroot}%{_datadir}/maven-metadata/%{name}-pki-kra.xml
%endif

%if %{with ocsp}
echo "Removing RPM deps from %{buildroot}%{_datadir}/maven-metadata/pki-pki-ocsp.xml"
xmlstarlet edit --inplace \
    -d "//_:dependency[_:groupId='jakarta.activation']" \
    -d "//_:dependency[_:groupId='jakarta.annotation']" \
    -d "//_:dependency[_:groupId='jakarta.xml.bind']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.core']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.module']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.jaxrs']" \
    -d "//_:dependency[_:groupId='org.jboss.spec.javax.ws.rs']" \
    -d "//_:dependency[_:groupId='org.jboss.logging']" \
    -d "//_:dependency[_:groupId='org.jboss.resteasy']" \
    %{buildroot}%{_datadir}/maven-metadata/%{name}-pki-ocsp.xml
%endif

%if %{with tks}
echo "Removing RPM deps from %{buildroot}%{_datadir}/maven-metadata/pki-pki-tks.xml"
xmlstarlet edit --inplace \
    -d "//_:dependency[_:groupId='jakarta.activation']" \
    -d "//_:dependency[_:groupId='jakarta.annotation']" \
    -d "//_:dependency[_:groupId='jakarta.xml.bind']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.core']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.module']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.jaxrs']" \
    -d "//_:dependency[_:groupId='org.jboss.spec.javax.ws.rs']" \
    -d "//_:dependency[_:groupId='org.jboss.logging']" \
    -d "//_:dependency[_:groupId='org.jboss.resteasy']" \
    %{buildroot}%{_datadir}/maven-metadata/%{name}-pki-tks.xml
%endif

%if %{with tps}
echo "Removing RPM deps from %{buildroot}%{_datadir}/maven-metadata/pki-pki-tps.xml"
xmlstarlet edit --inplace \
    -d "//_:dependency[_:groupId='jakarta.activation']" \
    -d "//_:dependency[_:groupId='jakarta.annotation']" \
    -d "//_:dependency[_:groupId='jakarta.xml.bind']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.core']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.module']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.jaxrs']" \
    -d "//_:dependency[_:groupId='org.jboss.spec.javax.ws.rs']" \
    -d "//_:dependency[_:groupId='org.jboss.logging']" \
    -d "//_:dependency[_:groupId='org.jboss.resteasy']" \
    %{buildroot}%{_datadir}/maven-metadata/%{name}-pki-tps.xml
%endif

%if %{with acme}
echo "Removing RPM deps from %{buildroot}%{_datadir}/maven-metadata/pki-pki-acme.xml"
xmlstarlet edit --inplace \
    -d "//_:dependency[_:groupId='jakarta.activation']" \
    -d "//_:dependency[_:groupId='jakarta.annotation']" \
    -d "//_:dependency[_:groupId='jakarta.xml.bind']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.core']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.module']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.jaxrs']" \
    -d "//_:dependency[_:groupId='org.jboss.spec.javax.ws.rs']" \
    -d "//_:dependency[_:groupId='org.jboss.logging']" \
    -d "//_:dependency[_:groupId='org.jboss.resteasy']" \
    %{buildroot}%{_datadir}/maven-metadata/%{name}-pki-acme.xml
%endif

%if %{with est}
echo "Removing RPM deps from %{buildroot}%{_datadir}/maven-metadata/pki-pki-est.xml"
xmlstarlet edit --inplace \
    -d "//_:dependency[_:groupId='jakarta.activation']" \
    -d "//_:dependency[_:groupId='jakarta.annotation']" \
    -d "//_:dependency[_:groupId='jakarta.xml.bind']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.core']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.module']" \
    -d "//_:dependency[_:groupId='com.fasterxml.jackson.jaxrs']" \
    -d "//_:dependency[_:groupId='org.jboss.spec.javax.ws.rs']" \
    -d "//_:dependency[_:groupId='org.jboss.logging']" \
    -d "//_:dependency[_:groupId='org.jboss.resteasy']" \
    %{buildroot}%{_datadir}/maven-metadata/%{name}-pki-est.xml
%endif

# with maven
%endif

# without runtime_deps
%endif

%if %{with server}

%if 0%{?fedora} || 0%{?rhel} >= 11

install -m0644 -D %{product_id}.sysusers.conf %{buildroot}%{_sysusersdir}/%{product_id}.conf
%pre -n %{product_id}-server

%else

%pre -n %{product_id}-server

# create PKI group if it doesn't exist
getent group %{pki_groupname} >/dev/null || groupadd -f -g %{pki_gid} -r %{pki_groupname}

# create PKI user if it doesn't exist
if ! getent passwd %{pki_username} >/dev/null ; then
    useradd -r -u %{pki_uid} -g %{pki_groupname} -d %{pki_homedir} -s /sbin/nologin -c "Certificate System" %{pki_username}
fi

%endif

# create PKI home directory if it doesn't exist
if [ ! -d %{pki_homedir} ] ; then
    cp -ar /etc/skel %{pki_homedir}
    chown -R %{pki_username}:%{pki_groupname} %{pki_homedir}
    chmod 700 %{pki_homedir}
    usermod -d %{pki_homedir} %{pki_username}
fi

exit 0

# with server
%endif

%if %{with base}

%post -n %{product_id}-base

if [ $1 -eq 1 ]
then
    # On RPM installation create system upgrade tracker
    echo "Configuration-Version: %{version}" > %{_sysconfdir}/pki/pki.version

else
    # On RPM upgrade run system upgrade
    echo "Upgrading PKI system configuration at `/bin/date`." >> /var/log/pki/pki-upgrade-%{version}.log
    /sbin/pki-upgrade 2>&1 | tee -a /var/log/pki/pki-upgrade-%{version}.log
    echo >> /var/log/pki/pki-upgrade-%{version}.log
fi

%postun -n %{product_id}-base

if [ $1 -eq 0 ]
then
    # On RPM uninstallation remove system upgrade tracker
    rm -f %{_sysconfdir}/pki/pki.version
fi

# with base
%endif

%if %{with server}

%post -n %{product_id}-server
# CVE-2021-3551
# Remove world access from existing installation logs
find /var/log/pki -maxdepth 1 -type f -exec chmod o-rwx {} \;

# Reload systemd daemons on upgrade only
if [ "$1" == "2" ]
then
    systemctl daemon-reload
fi

# Update the fapolicy rules for each PKI server instance
for instance in $(ls /var/lib/pki)
do
    target="/etc/fapolicyd/rules.d/61-pki-$instance.rules"

    sed -e "s/\[WORK_DIR\]/\/var\/lib\/pki\/$instance\/work/g" \
        /usr/share/pki/server/etc/fapolicy.rules \
        > $target

    chown root:fapolicyd $target
    chmod 644 $target
done

# Restart fapolicy daemon if it's active
status=$(systemctl is-active fapolicyd)
if [ "$status" = "active" ]
then
    systemctl restart fapolicyd
fi

# with server
%endif

%if %{with meta}
%if "%{name}" != "%{product_id}"
################################################################################
%files -n %{product_id} %{?with_maven:-f .mfiles}
################################################################################
%else
%files %{?with_maven:-f .mfiles}
%endif

%doc %{_datadir}/doc/pki/README

# with meta
%endif

%if %{with base}
################################################################################
%files -n %{product_id}-base
################################################################################

%license base/common/LICENSE
%license base/common/LICENSE.LESSER
%doc %{_datadir}/doc/pki-base/html
%dir %{_datadir}/pki
%{_datadir}/pki/VERSION
%{_datadir}/pki/pom.xml
%dir %{_datadir}/pki/etc
%{_datadir}/pki/etc/pki.conf
%{_datadir}/pki/etc/logging.properties
%dir %{_datadir}/pki/lib
%dir %{_datadir}/pki/scripts
%{_datadir}/pki/scripts/config
%{_datadir}/pki/upgrade/
%{_datadir}/pki/key/templates
%dir %{_sysconfdir}/pki
%config(noreplace) %{_sysconfdir}/pki/pki.conf
%dir %{_localstatedir}/log/pki
%{_sbindir}/pki-upgrade
%{_mandir}/man1/pki-python-client.1.gz
%{_mandir}/man5/pki-logging.5.gz
%{_mandir}/man8/pki-upgrade.8.gz

################################################################################
%files -n %{product_id}-java %{?with_maven:-f .mfiles-pki-java}
################################################################################

%license base/common/LICENSE
%license base/common/LICENSE.LESSER
%{_datadir}/pki/examples/java/
%{_datadir}/pki/lib/*.jar

%if %{without maven}
%{_datadir}/java/pki/pki-common.jar
%endif

################################################################################
%files -n python3-%{product_id}
################################################################################

%license base/common/LICENSE
%license base/common/LICENSE.LESSER
%if %{with server}
%exclude %{python3_sitelib}/pki/server
%endif
%{python3_sitelib}/pki

################################################################################
%files -n %{product_id}-tools %{?with_maven:-f .mfiles-pki-tools}
################################################################################

%license base/tools/LICENSE
%doc base/tools/doc/README
%{_bindir}/pistool
%{_bindir}/pki
%{_bindir}/revoker
%{_bindir}/setpin
%{_bindir}/tkstool
%{_bindir}/tpsclient
%{_bindir}/AtoB
%{_bindir}/AuditVerify
%{_bindir}/BtoA
%{_bindir}/CMCEnroll
%{_bindir}/CMCRequest
%{_bindir}/CMCResponse
%{_bindir}/CMCRevoke
%{_bindir}/CMCSharedToken
%{_bindir}/CRMFPopClient
%{_bindir}/ExtJoiner
%{_bindir}/GenExtKeyUsage
%{_bindir}/GenIssuerAltNameExt
%{_bindir}/GenSubjectAltNameExt
%{_bindir}/HttpClient
%{_bindir}/KRATool
%{_bindir}/OCSPClient
%{_bindir}/PKCS10Client
%{_bindir}/PKCS12Export
%{_bindir}/PKICertImport
%{_bindir}/PrettyPrintCert
%{_bindir}/PrettyPrintCrl
%{_bindir}/TokenInfo
%{_datadir}/pki/tools/
%{_datadir}/pki/lib/p11-kit-trust.so
%{_libdir}/libpki-tps.so
%{_mandir}/man1/AtoB.1.gz
%{_mandir}/man1/AuditVerify.1.gz
%{_mandir}/man1/BtoA.1.gz
%{_mandir}/man1/CMCEnroll.1.gz
%{_mandir}/man1/CMCRequest.1.gz
%{_mandir}/man1/CMCSharedToken.1.gz
%{_mandir}/man1/CMCResponse.1.gz
%{_mandir}/man1/KRATool.1.gz
%{_mandir}/man1/PrettyPrintCert.1.gz
%{_mandir}/man1/PrettyPrintCrl.1.gz
%{_mandir}/man1/pki.1.gz
%{_mandir}/man1/pki-audit.1.gz
%{_mandir}/man1/pki-ca-cert.1.gz
%{_mandir}/man1/pki-ca-kraconnector.1.gz
%{_mandir}/man1/pki-ca-profile.1.gz
%{_mandir}/man1/pki-client.1.gz
%{_mandir}/man1/pki-group.1.gz
%{_mandir}/man1/pki-group-member.1.gz
%{_mandir}/man1/pki-kra-key.1.gz
%{_mandir}/man1/pki-pkcs12-cert.1.gz
%{_mandir}/man1/pki-pkcs12-key.1.gz
%{_mandir}/man1/pki-pkcs12.1.gz
%{_mandir}/man1/pki-securitydomain.1.gz
%{_mandir}/man1/pki-tps-profile.1.gz
%{_mandir}/man1/pki-user.1.gz
%{_mandir}/man1/pki-user-cert.1.gz
%{_mandir}/man1/pki-user-membership.1.gz
%{_mandir}/man1/PKCS10Client.1.gz
%{_mandir}/man1/PKICertImport.1.gz
%{_mandir}/man1/tpsclient.1.gz
%{_javadir}/pki/pki-tools.jar
%{_jnidir}/pki/pki-tools.jar

# with base
%endif

%if %{with server}
################################################################################
%files -n %{product_id}-server %{?with_maven:-f .mfiles-pki-server}
################################################################################

%license base/common/THIRD_PARTY_LICENSES
%license base/server/LICENSE
%doc base/server/README
%attr(755,-,-) %dir %{_sysconfdir}/sysconfig/pki
%attr(755,-,-) %dir %{_sysconfdir}/sysconfig/pki/tomcat
%{_sbindir}/pkispawn
%{_sbindir}/pkidestroy
%{_sbindir}/pki-server
%{_sbindir}/pki-healthcheck
%{python3_sitelib}/pki/server/
%{python3_sitelib}/pkihealthcheck-*.egg-info/
%config(noreplace) %{_sysconfdir}/pki/healthcheck.conf

%{_datadir}/pki/etc/tomcat.conf
%dir %{_datadir}/pki/deployment
%{_datadir}/pki/deployment/config/
%{_datadir}/pki/scripts/operations
%{_bindir}/pkidaemon
%{_bindir}/pki-server-nuxwdog
%dir %{_sysconfdir}/systemd/system/pki-tomcatd.target.wants
%attr(644,-,-) %{_unitdir}/pki-tomcatd@.service
%attr(644,-,-) %{_unitdir}/pki-tomcatd.target
%dir %{_sysconfdir}/systemd/system/pki-tomcatd-nuxwdog.target.wants
%attr(644,-,-) %{_unitdir}/pki-tomcatd-nuxwdog@.service
%attr(644,-,-) %{_unitdir}/pki-tomcatd-nuxwdog.target
%dir %{_sharedstatedir}/pki
%{_mandir}/man1/pkidaemon.1.gz
%{_mandir}/man5/pki_default.cfg.5.gz
%{_mandir}/man5/pki_healthcheck.conf.5.gz
%{_mandir}/man5/pki-server-logging.5.gz
%{_mandir}/man8/pki-server-upgrade.8.gz
%{_mandir}/man8/pkidestroy.8.gz
%{_mandir}/man8/pkispawn.8.gz
%{_mandir}/man8/pki-server.8.gz
%{_mandir}/man8/pki-server-acme.8.gz
%{_mandir}/man8/pki-server-est.8.gz
%{_mandir}/man8/pki-server-instance.8.gz
%{_mandir}/man8/pki-server-subsystem.8.gz
%{_mandir}/man8/pki-server-nuxwdog.8.gz
%{_mandir}/man8/pki-server-migrate.8.gz
%{_mandir}/man8/pki-server-cert.8.gz
%{_mandir}/man8/pki-server-ca.8.gz
%{_mandir}/man8/pki-server-kra.8.gz
%{_mandir}/man8/pki-server-ocsp.8.gz
%{_mandir}/man8/pki-server-tks.8.gz
%{_mandir}/man8/pki-server-tps.8.gz
%{_mandir}/man8/pki-healthcheck.8.gz
%{_datadir}/pki/setup/
%{_datadir}/pki/server/
%if 0%{?fedora} || 0%{?rhel} >= 11
%{_sysusersdir}/%{product_id}.conf
%endif
%if %{without maven}
%{_datadir}/java/pki/pki-server.jar
%{_datadir}/java/pki/pki-server-webapp.jar
%{_datadir}/java/pki/pki-tomcat.jar
#%{_datadir}/java/pki/pki-tomcat-9.0.jar
%{_datadir}/java/pki/pki-tomcat-10.1.jar
%endif

# with server
%endif

%if %{with acme}
################################################################################
%files -n %{product_id}-acme %{?with_maven:-f .mfiles-pki-acme}
################################################################################

%{_datadir}/pki/acme/

%if %{without maven}
%{_datadir}/java/pki/pki-acme.jar
%endif

# with acme
%endif

%if %{with ca}
################################################################################
%files -n %{product_id}-ca %{?with_maven:-f .mfiles-pki-ca}
################################################################################

%license base/ca/LICENSE
%{_datadir}/pki/ca/

%if %{without maven}
%{_datadir}/java/pki/pki-ca.jar
%endif

# with ca
%endif

%if %{with est}
################################################################################
%files -n %{product_id}-est %{?with_maven:-f .mfiles-pki-est}
################################################################################

%{_datadir}/pki/est/

%if %{without maven}
%{_datadir}/java/pki/pki-est.jar
%endif

# with est
%endif

%if %{with kra}
################################################################################
%files -n %{product_id}-kra %{?with_maven:-f .mfiles-pki-kra}
################################################################################

%license base/kra/LICENSE
%{_datadir}/pki/kra/

%if %{without maven}
%{_datadir}/java/pki/pki-kra.jar
%endif

# with kra
%endif

%if %{with ocsp}
################################################################################
%files -n %{product_id}-ocsp %{?with_maven:-f .mfiles-pki-ocsp}
################################################################################

%license base/ocsp/LICENSE
%{_datadir}/pki/ocsp/

%if %{without maven}
%{_datadir}/java/pki/pki-ocsp.jar
%endif

# with ocsp
%endif

%if %{with tks}
################################################################################
%files -n %{product_id}-tks %{?with_maven:-f .mfiles-pki-tks}
################################################################################

%license base/tks/LICENSE
%{_datadir}/pki/tks/

%if %{without maven}
%{_datadir}/java/pki/pki-tks.jar
%endif

# with tks
%endif

%if %{with tps}
################################################################################
%files -n %{product_id}-tps %{?with_maven:-f .mfiles-pki-tps}
################################################################################

%license base/tps/LICENSE
%{_datadir}/pki/tps/
%{_mandir}/man5/pki-tps-connector.5.gz
%{_mandir}/man5/pki-tps-profile.5.gz

%if %{without maven}
%{_datadir}/java/pki/pki-tps.jar
%endif

# with tps
%endif

%if %{with javadoc}
################################################################################
%files -n %{product_id}-javadoc
################################################################################

%{_javadocdir}/pki/

# with javadoc
%endif

%if %{with console}
################################################################################
%files -n %{product_id}-console %{?with_maven:-f .mfiles-pki-console}
################################################################################

%license base/console/LICENSE
%{_bindir}/pkiconsole

%if %{without maven}
%{_datadir}/java/pki/pki-console.jar
%endif

# with console
%endif

%if %{with theme}
################################################################################
%files -n %{product_id}-theme
################################################################################

%license themes/%{theme}/common-ui/LICENSE
%dir %{_datadir}/pki

%if %{with server}
%{_datadir}/pki/CS_SERVER_VERSION
%{_datadir}/pki/common-ui/
%{_datadir}/pki/server/webapps/pki/ca
%{_datadir}/pki/server/webapps/pki/css
%{_datadir}/pki/server/webapps/pki/esc
%{_datadir}/pki/server/webapps/pki/fonts
%{_datadir}/pki/server/webapps/pki/images
%{_datadir}/pki/server/webapps/pki/kra
%{_datadir}/pki/server/webapps/pki/ocsp
%{_datadir}/pki/server/webapps/pki/pki.properties
%{_datadir}/pki/server/webapps/pki/tks

# with server
%endif

%if %{with console}
################################################################################
%files -n %{product_id}-console-theme
################################################################################

%license themes/%{theme}/console-ui/LICENSE
%{_javadir}/pki/pki-console-theme.jar

# with console
%endif

# with theme
%endif

%if %{with tests}
################################################################################
%files -n %{product_id}-tests
################################################################################

%{_datadir}/pki/tests/

# with tests
%endif

################################################################################
%changelog
* Tue Nov 04 2025 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.8.0-1
- Rebase to PKI 11.8.0

* Fri Sep 26 2025 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.8.0-0.5.beta6
- Rebase to PKI 11.8.0-beta6

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 11.8.0-0.6.beta5.1
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 22 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 11.8.0-0.6.beta5
- Build with Java 25 for ELN
- Enable sysusers.d for ELN

* Tue Aug 19 2025 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.8.0-0.5.beta5
- Rebase to PKI 11.8.0-beta5

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 11.8.0-0.4.beta4.4
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Aug 11 2025 jmagne@redhat.com              - 11.8.0-0.4.beta4.3
- Rebase to PKI v11.8.0-beta4

* Wed Jul 30 2025 jiri vanek <jvanek@redhat.com> - 11.8.0-0.2.beta2.3
- Rrevert to jdk21

* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 11.8.0-0.2.beta2.2
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.0-0.2.beta2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.8.0-0.2.beta2
- Rebase to PKI 11.8.0-beta2

* Wed Jul 09 2025 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.8.0-0.1.beta1
- Rebase to PKI 11.8.0-beta1

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 11.6.0-0.3.alpha1.2
- Rebuilt for Python 3.14

* Thu Jan 23 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 11.6.0-0.3.alpha1.1
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Thu Jan 16 2025 Adam Williamson <awilliam@redhat.com> - 11.6.0-0.3.alpha1
- Rebuild on mass rebuild tag to make that process happy

* Thu Jan 16 2025 Adam Williamson <awilliam@redhat.com> - 11.6.0-0.2.alpha1
- Add pkiuser user and group provides

* Wed Nov 20 2024 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.6.0-0.1.alpha1
- Rebase to PKI 11.6.0-alpha1

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11.5.0-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Python Maint <python-maint@redhat.com> - 11.5.0-3.1
- Rebuilt for Python 3.13

* Mon Mar 04 2024 Jiri Vanek <jvanek@redhat.com> - 11.5.0-3
- properly, dynamically follow system jdk
-- requiring version-less, thus sytem jdk, as in:
--- https://docs.fedoraproject.org/en-US/packaging-guidelines/Java/
-- detecting java home it via javapackages-tools
--- https://fedoraproject.org/wiki/Changes/Decouple_system_java_setting_from_java_command_setting

* Thu Feb 29 2024 Adam Williamson <awilliam@redhat.com> - 11.5.0-2.fc41
- Really build against java-21-openjdk

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 11.5.0-1.1
- Rebuilt for java-21-openjdk as system jdk

* Wed Feb 21 2024 Dogtag PKI Team <devel@lists.dogtagpki.org> 11.5.0-1
- Rebase to PKI 11.5.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11.4.3-2.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11.4.3-2.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 29 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 11.4.3-2.2
- Disable unwanted components in RHEL builds
- Update conditionals for RHEL 10

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11.4.3-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Adam Williamson <awilliam@redhat.com> - 11.4.3-2.fc39
- Backport PR #4494 to fix pkiparser.py with Python 3.12

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 11.4.3-1.fc39.1
- Rebuilt for Python 3.12

* Mon Feb 27 2023 Jerry James <loganjerry@gmail.com> - 11.3.1-2
- Unbundle the FontAwesome font

* Tue Feb 07 2023 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.3.1-1
- Rebase to PKI 11.3.1

* Fri Jan 20 2023 Marian Koncek <mkoncek@redhat.com> - 11.2.0-3
- Resolve jar paths using xmvn

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11.2.0-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 29 2022 Adam Williamson <awilliam@redhat.com> - 11.2.0-2
- Backport fix to work with python-ldap 3.4.2 (#2112243)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11.2.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 01 2022 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.2.0-1
- Rebase to PKI 11.2.0

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 11.2.0-0.3.beta2.1
- Rebuilt for Python 3.11

* Mon May 02 2022 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.2.0-0.3.beta2
- Rebase to PKI 11.2.0-beta2

* Tue Apr 12 2022 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.2.0-0.2.beta1
- Rebase to PKI 11.2.0-beta1

* Mon Feb 14 2022 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.1.0-1
- Rebase to PKI 11.1.0

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 11.1.0-0.3.alpha2
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11.1.0-0.2.alpha2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 26 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.1.0-0.1.alpha2
- Rebase to PKI 11.1.0-alpha2

* Thu Sep 30 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.0.0-1
- Rebase to PKI 11.0.0
- Bug #1999052 - pki instance creation fails for IPA server

* Fri Sep 03 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.0.0-0.4.beta1
- Rebase to PKI 11.0.0-beta1

* Thu Aug 12 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.0.0-0.3.alpha2
- Rebase to PKI 11.0.0-alpha2

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.0-0.2.alpha1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Dogtag PKI Team <devel@lists.dogtagpki.org> - 11.0.0-0.1.alpha1
- Rebase to PKI 11.0.0-alpha1
