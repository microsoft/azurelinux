# Temporarily disabled dependencies:
%bcond_with freeipa
%bcond_with selinux_policy_targeted

Vendor:         Microsoft Corporation
Distribution:   Mariner
################################################################################
Name:             pki-core
################################################################################

%global           vendor_id dogtag
%global           brand Dogtag

Summary:          %{brand} PKI Core Package
URL:              https://www.dogtagpki.org
# The entire source code is GPLv2 except for 'pki-tps' which is LGPLv2+, "base/common" which is LGPLv3, and "base/tps-client/apache" which is ASL 2.0.
License:          ASL 2.0 and GPLv2 and LGPLv2+ and LGPLv3

# For development (i.e. unsupported) releases, use x.y.z-0.n.<phase>.
# For official (i.e. supported) releases, use x.y.z-r where r >=1.
Version:          10.10.3
Release:          10%{?dist}
#global           _phase -beta1

# To create a tarball from a version tag:
# $ git archive \
#     --format=tar.gz \
#     --prefix pki-<version>/ \
#     -o pki-<version>.tar.gz \
#     <version tag>
Source: https://github.com/dogtagpki/pki/archive/v%{version}%{?_phase}/pki-%{version}%{?_phase}.tar.gz

# To create a patch for all changes since a version tag:
# $ git format-patch \
#     --stdout \
#     <version tag> \
#     > pki-VERSION-RELEASE.patch
# Patch: pki-VERSION-RELEASE.patch
Patch1: 0001-remove-jakarta-commons-httpclient.patch

################################################################################
# NSS
################################################################################

%global nss_default_db_type sql

################################################################################
# Python
################################################################################

%if 0%{?rhel}
%global python_executable /usr/libexec/platform-python
%else
%global python_executable /usr/bin/python3
%endif

################################################################################
# Java
################################################################################

%define java_devel java-devel
%define java_headless java-headless
%define min_java_version 1.8.0

################################################################################
# RESTEasy
################################################################################

%define jaxrs_api_jar /usr/share/java/jboss-jaxrs-2.0-api.jar
%define resteasy_lib /usr/share/java/resteasy

################################################################################
# PKI
################################################################################

# By default all packages will be built except the ones specified with
# --without <package> option (exclusion method).

# If --with pkgs option is specified, only packages specified with
# --with <package> will be built (inclusion method).

# bcond_with pkgs
%global with_pkgs 1

# Define package_option macro to wrap bcond_with or bcond_without macro
# depending on package selection method.

%if %{with pkgs}
%define package_option() %bcond_with %1
%else
%define package_option() %bcond_without %1
%endif

# Define --with <package> or --without <package> options depending on
# package selection method.

%global with_base 1
%global with_server 1
%global with_ca 1
%global with_kra 1
%global without_theme 1
%global without_meta 1
%global without_tests 1
%global with_debug 1

# Not required by Mariner:
%bcond_with acme
%bcond_with console
%bcond_with javadoc
%bcond_with ocsp
%bcond_with tks
%bcond_with tps

%if ! %{with debug}
%define debug_package %{nil}
%endif

%bcond_without sdnotify

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
%define pki_homedir /usr/share/pki

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

# autosetup
BuildRequires:    git
BuildRequires:    make

BuildRequires:    cmake >= 3.0.2
BuildRequires:    gcc-c++
BuildRequires:    zip
BuildRequires:    %java_devel >= %{min_java_version}
BuildRequires:    javapackages-tools
BuildRequires:    redhat-rpm-config
BuildRequires:    ldapjdk >= 4.22.0
BuildRequires:    apache-commons-cli
BuildRequires:    apache-commons-codec
BuildRequires:    apache-commons-io
BuildRequires:    apache-commons-lang3 >= 3.2
BuildRequires:    apache-commons-net
BuildRequires:    glassfish-jaxb-api
BuildRequires:    slf4j
BuildRequires:    slf4j-jdk14
BuildRequires:    nspr-devel
BuildRequires:    nss-devel >= 3.36.1

BuildRequires:    openldap-devel
BuildRequires:    pkgconfig
BuildRequires:    policycoreutils

BuildRequires:    python3-lxml
BuildRequires:    python3-sphinx

BuildRequires:    velocity
BuildRequires:    xalan-j2
BuildRequires:    xerces-j2

%if 0%{?rhel}
BuildRequires:    resteasy >= 3.0.26
%else
BuildRequires:    jboss-annotations-1.2-api
BuildRequires:    jboss-jaxrs-2.0-api
BuildRequires:    jboss-logging
BuildRequires:    resteasy-atom-provider >= 3.0.17-1
BuildRequires:    resteasy-client >= 3.0.17-1
BuildRequires:    resteasy-jaxb-provider >= 3.0.17-1
BuildRequires:    resteasy-core >= 3.0.17-1
BuildRequires:    resteasy-jackson2-provider >= 3.0.17-1
%endif

BuildRequires:    python3 >= 3.5
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-cryptography
BuildRequires:    python3-lxml
BuildRequires:    python3-ldap
BuildRequires:    python3-libselinux
BuildRequires:    python3-nss
BuildRequires:    python3-requests >= 2.6.0
BuildRequires:    python3-six

%if 0%{?rhel}
# no python3-pytest-runner
%else
BuildRequires:    python3-pytest-runner
%endif

BuildRequires:    junit
BuildRequires:    jpackage-utils >= 1.7.5-10
BuildRequires:    jss >= 4.8.1
BuildRequires:    tomcatjss >= 7.6.1

# JNA is used to bind to libsystemd
%if %{with sdnotify}
BuildRequires:    jna
%endif
BuildRequires:    systemd-units

%if 0%{?rhel}
BuildRequires:    pki-servlet-engine
%else
BuildRequires:    tomcat >= 9.0.7
%endif

# additional build requirements needed to build native 'tpsclient'
# REMINDER:  Revisit these once 'tpsclient' is rewritten as a Java app
BuildRequires:    apr-devel
BuildRequires:    apr-util-devel
BuildRequires:    cyrus-sasl-devel
BuildRequires:    httpd-devel >= 2.4.2
BuildRequires:    pcre-devel
BuildRequires:    systemd
BuildRequires:    zlib
BuildRequires:    zlib-devel

# build dependency to build man pages

BuildRequires:    golang-github-cpuguy83-md2man

# pki-healthcheck depends on the following library
%if 0%{?rhel}
BuildRequires:    ipa-healthcheck-core
%else
%if %{with freeipa}
BuildRequires:    freeipa-healthcheck-core
%endif
%endif

# PKICertImport depends on certutil and openssl
BuildRequires:    nss-tools
BuildRequires:    openssl

# description for top-level package (if there is a separate meta package)
%if "%{name}" != "%{vendor_id}-pki"
%description

%{brand} PKI is an enterprise software system designed
to manage enterprise Public Key Infrastructure deployments.

PKI consists of the following components:

  * Automatic Certificate Management Environment (ACME) Responder
  * Certificate Authority (CA)
  * Key Recovery Authority (KRA)
  * Online Certificate Status Protocol (OCSP) Manager
  * Token Key Service (TKS)
  * Token Processing Service (TPS)

%endif

%if %{with meta}
%if "%{name}" != "%{vendor_id}-pki"
################################################################################
%package -n       %{vendor_id}-pki
################################################################################

Summary:          %{brand} PKI Package
%endif

# Make certain that this 'meta' package requires the latest version(s)
# of ALL PKI theme packages
Requires:         %{vendor_id}-pki-server-theme = %{version}
Requires:         %{vendor_id}-pki-console-theme = %{version}

# Make certain that this 'meta' package requires the latest version(s)
# of ALL PKI core packages
Requires:         pki-acme = %{version}
Requires:         pki-ca = %{version}
Requires:         pki-kra = %{version}
Requires:         pki-ocsp = %{version}
Requires:         pki-tks = %{version}
Requires:         pki-tps = %{version}

# Make certain that this 'meta' package requires the latest version(s)
# of PKI console
Requires:         pki-console = %{version}
Requires:         pki-javadoc = %{version}

# Make certain that this 'meta' package requires the latest version(s)
# of ALL PKI clients
Requires:         esc >= 1.1.1

# description for top-level package (unless there is a separate meta package)
%if "%{name}" == "%{vendor_id}-pki"
%description
%else
%description -n   %{vendor_id}-pki
%endif

%{brand} PKI is an enterprise software system designed
to manage enterprise Public Key Infrastructure deployments.

PKI consists of the following components:

  * Automatic Certificate Management Environment (ACME) Responder
  * Certificate Authority (CA)
  * Key Recovery Authority (KRA)
  * Online Certificate Status Protocol (OCSP) Manager
  * Token Key Service (TKS)
  * Token Processing Service (TPS)

# with meta
%endif

%if %{with base}
################################################################################
%package -n       pki-symkey
################################################################################

Summary:          PKI Symmetric Key Package

Requires:         %java_headless >= %{min_java_version}
Requires:         jpackage-utils >= 1.7.5-10
Requires:         jss >= 4.8.0
Requires:         nss >= 3.38.0

# Ensure we end up with a useful installation
Conflicts:        pki-symkey < %{version}
Conflicts:        pki-javadoc < %{version}
Conflicts:        pki-server-theme < %{version}
Conflicts:        pki-console-theme < %{version}

%description -n   pki-symkey
The PKI Symmetric Key Java Package supplies various native
symmetric key operations to Java programs.

################################################################################
%package -n       pki-base
################################################################################

Summary:          PKI Base Package
BuildArch:        noarch

Requires:         nss >= 3.36.1

Requires:         python3-pki = %{version}-%{release}
Requires(post):   python3-pki = %{version}-%{release}

# Ensure we end up with a useful installation
Conflicts:        pki-symkey < %{version}
Conflicts:        pki-javadoc < %{version}
Conflicts:        pki-server-theme < %{version}
Conflicts:        pki-console-theme < %{version}

%description -n   pki-base
The PKI Base Package contains the common and client libraries and utilities
written in Python.

################################################################################
%package -n       python3-pki
################################################################################

Summary:          PKI Python 3 Package
BuildArch:        noarch

Obsoletes:        pki-base-python3 < %{version}
Provides:         pki-base-python3 = %{version}

%{?python_provide:%python_provide python3-pki}


Requires:         pki-base = %{version}-%{release}
Requires:         python3 >= 3.5
Requires:         python3-cryptography
Requires:         python3-ldap
Requires:         python3-lxml
Requires:         python3-nss
Requires:         python3-requests >= 2.6.0
Requires:         python3-six

%description -n   python3-pki
This package contains PKI client library for Python 3.

################################################################################
%package -n       pki-base-java
################################################################################

Summary:          PKI Base Java Package
BuildArch:        noarch

Requires:         %java_headless >= %{min_java_version}
Requires:         apache-commons-cli
Requires:         apache-commons-codec
Requires:         apache-commons-io
Requires:         apache-commons-lang3 >= 3.2
Requires:         apache-commons-logging
Requires:         apache-commons-net
Requires:         glassfish-jaxb-api
Requires:         slf4j
Requires:         slf4j-jdk14
Requires:         jpackage-utils >= 1.7.5-10
Requires:         jss >= 4.7.0
Requires:         ldapjdk >= 4.22.0
Requires:         pki-base = %{version}-%{release}

%if 0%{?rhel}
Requires:         resteasy >= 3.0.26
%else
Requires:         resteasy-atom-provider >= 3.0.17-1
Requires:         resteasy-client >= 3.0.17-1
Requires:         resteasy-jaxb-provider >= 3.0.17-1
Requires:         resteasy-core >= 3.0.17-1
Requires:         resteasy-jackson2-provider >= 3.0.17-1
%endif


Requires:         xalan-j2
Requires:         xerces-j2
Requires:         xml-commons-apis
Requires:         xml-commons-resolver

%description -n   pki-base-java
The PKI Base Java Package contains the common and client libraries and utilities
written in Java.

################################################################################
%package -n       pki-tools
################################################################################

Summary:          PKI Tools Package

Requires:         openldap-clients
Requires:         nss-tools >= 3.36.1
Requires:         pki-base-java = %{version}-%{release}
Requires:         p11-kit-trust

# PKICertImport depends on certutil and openssl
Requires:         nss-tools
Requires:         openssl

%description -n   pki-tools
This package contains PKI executables that can be used to help make
Certificate System into a more complete and robust PKI solution.

# with base
%endif

%if %{with server}
################################################################################
%package -n       pki-server
################################################################################

Summary:          PKI Server Package
BuildArch:        noarch

Requires:         hostname

Requires:         policycoreutils
Requires:         policycoreutils-python-utils
Requires:         policycoreutils-python3

Requires:         procps-ng
Requires:         openldap-clients
Requires:         openssl
Requires:         pki-symkey = %{version}-%{release}
Requires:         pki-tools = %{version}-%{release}

Requires:         keyutils

Requires:         python3-lxml
Requires:         python3-libselinux

%if %{with selinux_policy_targeted}
Requires:         selinux-policy-targeted >= 3.13.1-159
%endif

%if 0%{?rhel}
Requires:         pki-servlet-engine >= 9.0.7
%else
Requires:         tomcat >= 9.0.7
%endif

Requires:         velocity
Requires:         sudo
Requires:         systemd
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
Requires(pre):    shadow-utils
Requires:         tomcatjss >= 7.6.1

# JNA is used to bind to libsystemd
%if %{with sdnotify}
Requires:         jna
%endif

# pki-healthcheck depends on the following library
%if 0%{?rhel}
Requires:         ipa-healthcheck-core
%else
%if %{with freeipa}
Requires:         freeipa-healthcheck-core
%endif
%endif

# https://pagure.io/freeipa/issue/7742
%if 0%{?rhel}
Conflicts:        ipa-server < 4.7.1
%else
%if %{with freeipa}
Conflicts:        freeipa-server < 4.7.1
%endif
%endif

Provides:         bundled(js-backbone) = 1.4.0
Provides:         bundled(js-bootstrap) = 3.4.1
Provides:         bundled(js-jquery) = 3.5.1
Provides:         bundled(js-jquery-i18n-properties) = 1.2.7
Provides:         bundled(js-patternfly) = 3.59.2
Provides:         bundled(js-underscore) = 1.9.2

%description -n   pki-server
The PKI Server Package contains libraries and utilities needed by other
PKI subsystems.

# with server
%endif

%if %{with acme}
################################################################################
%package -n       pki-acme
################################################################################

Summary:          PKI ACME Package
BuildArch:        noarch

Requires:         pki-server = %{version}-%{release}

%description -n   pki-acme
The PKI ACME responder is a service that provides an automatic certificate
management via ACME v2 protocol defined in RFC 8555.

# with acme
%endif

%if %{with ca}
################################################################################
%package -n       pki-ca
################################################################################

Summary:          PKI CA Package
BuildArch:        noarch

Requires:         pki-server = %{version}-%{release}
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

%description -n   pki-ca
The Certificate Authority (CA) is a required PKI subsystem which issues,
renews, revokes, and publishes certificates as well as compiling and
publishing Certificate Revocation Lists (CRLs).

The Certificate Authority can be configured as a self-signing Certificate
Authority, where it is the root CA, or it can act as a subordinate CA,
where it obtains its own signing certificate from a public CA.

# with ca
%endif

%if %{with kra}
################################################################################
%package -n       pki-kra
################################################################################

Summary:          PKI KRA Package
BuildArch:        noarch

Requires:         pki-server = %{version}-%{release}
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

%description -n   pki-kra
The Key Recovery Authority (KRA) is an optional PKI subsystem that can act
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
%package -n       pki-ocsp
################################################################################

Summary:          PKI OCSP Package
BuildArch:        noarch

Requires:         pki-server = %{version}
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

%description -n   pki-ocsp
The Online Certificate Status Protocol (OCSP) Manager is an optional PKI
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
%package -n       pki-tks
################################################################################

Summary:          PKI TKS Package
BuildArch:        noarch

Requires:         pki-server = %{version}
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

%description -n   pki-tks
The Token Key Service (TKS) is an optional PKI subsystem that manages the
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
%package -n       pki-tps
################################################################################

Summary:          PKI TPS Package

Requires:         pki-server = %{version}
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

# additional runtime requirements needed to run native 'tpsclient'
# REMINDER:  Revisit these once 'tpsclient' is rewritten as a Java app

Requires:         nss-tools >= 3.36.1
Requires:         openldap-clients

%description -n   pki-tps
The Token Processing System (TPS) is an optional PKI subsystem that acts
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

The utility "tpsclient" is a test tool that interacts with TPS.  This
tool is useful to test TPS server configs without risking an actual
smart card.

# with tps
%endif

%if %{with javadoc}
################################################################################
%package -n       pki-javadoc
################################################################################

Summary:          PKI Javadoc Package
BuildArch:        noarch

# Ensure we end up with a useful installation
Conflicts:        pki-base < %{version}
Conflicts:        pki-symkey < %{version}
Conflicts:        pki-server-theme < %{version}
Conflicts:        pki-console-theme < %{version}

%description -n   pki-javadoc
This package contains PKI API documentation.

# with javadoc
%endif

%if %{with console}
################################################################################
%package -n       pki-console
################################################################################

Summary:          PKI Console Package
BuildArch:        noarch

BuildRequires:    idm-console-framework >= 1.2.0

Requires:         idm-console-framework >= 1.2.0
Requires:         pki-base-java = %{version}
Requires:         pki-console-theme = %{version}

%description -n   pki-console
The PKI Console is a Java application used to administer PKI server.

# with console
%endif

%if %{with theme}
################################################################################
%package -n       %{vendor_id}-pki-server-theme
################################################################################

Summary:          %{brand} PKI Server Theme Package
BuildArch:        noarch

Provides:         pki-server-theme = %{version}

# Ensure we end up with a useful installation
Conflicts:        pki-base < %{version}
Conflicts:        pki-symkey < %{version}
Conflicts:        pki-console-theme < %{version}
Conflicts:        pki-javadoc < %{version}

%description -n   %{vendor_id}-pki-server-theme
This PKI Server Theme Package contains
%{brand} textual and graphical user interface for PKI Server.

################################################################################
%package -n       %{vendor_id}-pki-console-theme
################################################################################

Summary:          %{brand} PKI Console Theme Package
BuildArch:        noarch

Provides:         pki-console-theme = %{version}

# Ensure we end up with a useful installation
Conflicts:        pki-base < %{version}
Conflicts:        pki-symkey < %{version}
Conflicts:        pki-server-theme < %{version}
Conflicts:        pki-javadoc < %{version}

%description -n   %{vendor_id}-pki-console-theme
This PKI Console Theme Package contains
%{brand} textual and graphical user interface for PKI Console.

# with theme
%endif

%if %{with tests}
################################################################################
%package -n       pki-tests
################################################################################

Summary:          PKI Tests
BuildArch:        noarch

%description -n   pki-tests
This package contains PKI test suite.

# with tests
%endif

################################################################################
%prep
################################################################################

%autosetup -n pki-%{version}%{?_phase} -p 1 -S git

################################################################################
%build
################################################################################

export JAVA_HOME="%{java_home}"

# get Java <major>.<minor> version number
java_version=`${JAVA_HOME}/bin/java -XshowSettings:properties -version 2>&1 | sed -n 's/ *java.version *= *\([0-9]\+\.[0-9]\+\).*/\1/p'`

# if <major> == 1, get <minor> version number
# otherwise get <major> version number
java_version=`echo $java_version | sed -e 's/^1\.//' -e 's/\..*$//'`

# get Tomcat <major>.<minor> version number
tomcat_version=`/usr/sbin/tomcat version | sed -n 's/Server number: *\([0-9]\+\.[0-9]\+\).*/\1/p'`

if [ $tomcat_version == "9.0" ]; then
    app_server=tomcat-8.5
else
    app_server=tomcat-$tomcat_version
fi

%if 0%{?rhel}
%{__mkdir_p} build
cd build
%endif

# Disable looking for JAVA_AWT_LIBRARY to fix build.
sed -i -E "/.*JNI REQUIRED.*/i set(JAVA_AWT_LIBRARY NotNeeded)" CMakeLists.txt

%cmake \
    --no-warn-unused-cli \
    -DVERSION=%{version}-%{release} \
    -DVAR_INSTALL_DIR:PATH=/var \
    -DP11_KIT_TRUST=/etc/alternatives/libnssckbi.so.%{_arch} \
    -DJAVA_VERSION=${java_version} \
    -DPKI_JAVA_PATH=${JAVA_HOME}/bin/java \
    -DJAVA_LIB_INSTALL_DIR=%{_jnidir} \
    -DSYSTEMD_LIB_INSTALL_DIR=%{_unitdir} \
    -DAPP_SERVER=$app_server \
    -DJAXRS_API_JAR=%{jaxrs_api_jar} \
    -DRESTEASY_LIB=%{resteasy_lib} \
    -DNSS_DEFAULT_DB_TYPE=%{nss_default_db_type} \
    -DBUILD_PKI_CORE:BOOL=ON \
    -DPYTHON_EXECUTABLE=%{python_executable} \
%if ! %{with server} && ! %{with acme} && ! %{with ca} && ! %{with kra} && ! %{with ocsp} && ! %{with tks} && ! %{with tps}
    -DWITH_SERVER:BOOL=OFF \
%endif
    -DWITH_CA:BOOL=%{?with_ca:ON}%{!?with_ca:OFF} \
    -DWITH_KRA:BOOL=%{?with_kra:ON}%{!?with_kra:OFF} \
    -DWITH_OCSP:BOOL=%{?with_ocsp:ON}%{!?with_ocsp:OFF} \
    -DWITH_TKS:BOOL=%{?with_tks:ON}%{!?with_tks:OFF} \
    -DWITH_TPS:BOOL=%{?with_tps:ON}%{!?with_tps:OFF} \
    -DWITH_ACME:BOOL=%{?with_acme:ON}%{!?with_acme:OFF} \
    -DWITH_SYSTEMD_NOTIFICATION:BOOL=%{?with_sdnotify:ON}%{!?with_sdnotify:OFF} \
    -DWITH_JAVADOC:BOOL=%{?with_javadoc:ON}%{!?with_javadoc:OFF} \
%if %{with_check}
    -DWITH_TEST:BOOL=ON \
%else
    -DWITH_TEST:BOOL=OFF \
%endif
    -DBUILD_PKI_CONSOLE:BOOL=%{?with_console:ON}%{!?with_console:OFF} \
    -DTHEME=%{?with_theme:%{vendor_id}} \
%if 0%{?rhel}
    ..
%else
    -B %{_vpath_builddir}
%endif


cd %{_vpath_builddir}


# Do not use _smp_mflags to preserve build order
%{__make} \
    VERBOSE=%{?_verbose} \
    CMAKE_NO_VERBOSE=1 \
    DESTDIR=%{buildroot} \
    INSTALL="install -p" \
    --no-print-directory \
    all

################################################################################
%install
################################################################################

%if 0%{?rhel}
cd build
%else
cd %{_vpath_builddir}
%endif

%{__make} \
    VERBOSE=%{?_verbose} \
    CMAKE_NO_VERBOSE=1 \
    DESTDIR=%{buildroot} \
    INSTALL="install -p" \
    --no-print-directory \
    install

%if %{with meta}
%{__mkdir_p} %{buildroot}%{_datadir}/doc/pki

cat > %{buildroot}%{_datadir}/doc/pki/README << EOF
This package is a "meta-package" whose dependencies pull in all of the
packages comprising the %{brand} Public Key Infrastructure (PKI) Suite.
EOF

# with meta
%endif

# Customize client library links in /usr/share/pki/lib
ln -sf /usr/share/java/jboss-logging/jboss-logging.jar %{buildroot}%{_datadir}/pki/lib/jboss-logging.jar
ln -sf /usr/share/java/jboss-annotations-1.2-api/jboss-annotations-api_1.2_spec.jar %{buildroot}%{_datadir}/pki/lib/jboss-annotations-api_1.2_spec.jar

%if %{with server}

# Customize server common library links in /usr/share/pki/server/common/lib
ln -sf %{jaxrs_api_jar} %{buildroot}%{_datadir}/pki/server/common/lib/jboss-jaxrs-2.0-api.jar
ln -sf /usr/share/java/jboss-logging/jboss-logging.jar %{buildroot}%{_datadir}/pki/server/common/lib/jboss-logging.jar
ln -sf /usr/share/java/jboss-annotations-1.2-api/jboss-annotations-api_1.2_spec.jar %{buildroot}%{_datadir}/pki/server/common/lib/jboss-annotations-api_1.2_spec.jar

# with server
%endif

%check
cd %{_vpath_builddir}
ctest --output-on-failure

%if %{with server}

%pre -n pki-server
getent group %{pki_groupname} >/dev/null || groupadd -f -g %{pki_gid} -r %{pki_groupname}
if ! getent passwd %{pki_username} >/dev/null ; then
    useradd -r -u %{pki_uid} -g %{pki_groupname} -d %{pki_homedir} -s /usr/sbin/nologin -c "Certificate System" %{pki_username}
fi
exit 0

# with server
%endif

%if %{with base}

%post -n pki-base

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

%postun -n pki-base

if [ $1 -eq 0 ]
then
    # On RPM uninstallation remove system upgrade tracker
    rm -f %{_sysconfdir}/pki/pki.version
fi

# with base
%endif

%if %{with server}

%post -n pki-server
## NOTE:  At this time, NO attempt has been made to update ANY PKI subsystem
##        from EITHER 'sysVinit' OR previous 'systemd' processes to the new
##        PKI deployment process

# Reload systemd daemons on upgrade only
if [ "$1" == "2" ]
then
    systemctl daemon-reload
fi

## preun -n pki-server
## NOTE:  At this time, NO attempt has been made to update ANY PKI subsystem
##        from EITHER 'sysVinit' OR previous 'systemd' processes to the new
##        PKI deployment process


## postun -n pki-server
## NOTE:  At this time, NO attempt has been made to update ANY PKI subsystem
##        from EITHER 'sysVinit' OR previous 'systemd' processes to the new
##        PKI deployment process

# with server
%endif

%if %{with meta}
%if "%{name}" != "%{vendor_id}-pki"
################################################################################
%files -n %{vendor_id}-pki
################################################################################
%else
%files
%endif

%doc %{_datadir}/doc/pki/README

# with meta
%endif

%if %{with base}
################################################################################
%files -n pki-symkey
################################################################################

%license base/symkey/LICENSE
%{_jnidir}/symkey.jar
%{_libdir}/symkey/

################################################################################
%files -n pki-base
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
%files -n pki-base-java
################################################################################

%license base/common/LICENSE
%license base/common/LICENSE.LESSER
%{_datadir}/pki/examples/java/
%{_datadir}/pki/lib/*.jar
%dir %{_javadir}/pki
%{_javadir}/pki/pki-cmsutil.jar
%{_javadir}/pki/pki-certsrv.jar

################################################################################
%files -n python3-pki
################################################################################

%license base/common/LICENSE
%license base/common/LICENSE.LESSER
%if %{with server}
%exclude %{python3_sitelib}/pki/server
%endif
%{python3_sitelib}/pki

################################################################################
%files -n pki-tools
################################################################################

%license base/tools/LICENSE
%doc base/tools/doc/README
%{_bindir}/p7tool
%{_bindir}/pistool
%{_bindir}/pki
%{_bindir}/revoker
%{_bindir}/setpin
%{_bindir}/sslget
%{_bindir}/tkstool
%{_bindir}/AtoB
%{_bindir}/AuditVerify
%{_bindir}/BtoA
%{_bindir}/CMCEnroll
%{_bindir}/CMCRequest
%{_bindir}/CMCResponse
%{_bindir}/CMCRevoke
%{_bindir}/CMCSharedToken
%{_bindir}/CRMFPopClient
%{_bindir}/DRMTool
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
%{_javadir}/pki/pki-tools.jar
%{_datadir}/pki/tools/
%{_datadir}/pki/lib/p11-kit-trust.so
%{_mandir}/man1/AtoB.1.gz
%{_mandir}/man1/AuditVerify.1.gz
%{_mandir}/man1/BtoA.1.gz
%{_mandir}/man1/CMCEnroll.1.gz
%{_mandir}/man1/CMCRequest.1.gz
%{_mandir}/man1/CMCSharedToken.1.gz
%{_mandir}/man1/CMCResponse.1.gz
%{_mandir}/man1/DRMTool.1.gz
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

# with base
%endif

%if %{with server}
################################################################################
%files -n pki-server
################################################################################

%license base/common/THIRD_PARTY_LICENSES
%license base/server/LICENSE
%doc base/server/README
%attr(755,-,-) %dir %{_sysconfdir}/sysconfig/pki
%attr(755,-,-) %dir %{_sysconfdir}/sysconfig/pki/tomcat
%{_sbindir}/pkispawn
%{_sbindir}/pkidestroy
%{_sbindir}/pki-server
%{_sbindir}/pki-server-upgrade
%{python3_sitelib}/pki/server/
%{_sbindir}/pki-healthcheck
%{python3_sitelib}/pki/server/healthcheck/
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
%{_javadir}/pki/pki-cms.jar
%{_javadir}/pki/pki-cmsbundle.jar
%{_javadir}/pki/pki-tomcat.jar
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

%if %{with sdnotify}
%{_javadir}/pki/pki-systemd.jar
%endif

# with server
%endif

%if %{with acme}
################################################################################
%files -n pki-acme
################################################################################

%{_javadir}/pki/pki-acme.jar
%dir %{_datadir}/pki/acme
%{_datadir}/pki/acme/

# with acme
%endif

%if %{with ca}
################################################################################
%files -n pki-ca
################################################################################

%license base/ca/LICENSE
%{_javadir}/pki/pki-ca.jar
%dir %{_datadir}/pki/ca
%{_datadir}/pki/ca/

# with ca
%endif

%if %{with kra}
################################################################################
%files -n pki-kra
################################################################################

%license base/kra/LICENSE
%{_javadir}/pki/pki-kra.jar
%dir %{_datadir}/pki/kra
%{_datadir}/pki/kra/

# with kra
%endif

%if %{with ocsp}
################################################################################
%files -n pki-ocsp
################################################################################

%license base/ocsp/LICENSE
%{_javadir}/pki/pki-ocsp.jar
%dir %{_datadir}/pki/ocsp
%{_datadir}/pki/ocsp/

# with ocsp
%endif

%if %{with tks}
################################################################################
%files -n pki-tks
################################################################################

%license base/tks/LICENSE
%{_javadir}/pki/pki-tks.jar
%dir %{_datadir}/pki/tks
%{_datadir}/pki/tks/

# with tks
%endif

%if %{with tps}
################################################################################
%files -n pki-tps
################################################################################

%license base/tps/LICENSE
%{_javadir}/pki/pki-tps.jar
%dir %{_datadir}/pki/tps
%{_datadir}/pki/tps/
%{_mandir}/man5/pki-tps-connector.5.gz
%{_mandir}/man5/pki-tps-profile.5.gz
%{_mandir}/man1/tpsclient.1.gz

# files for native 'tpsclient'
# REMINDER:  Remove this comment once 'tpsclient' is rewritten as a Java app

%{_bindir}/tpsclient
%{_libdir}/tps/libtps.so
%{_libdir}/tps/libtokendb.so

# with tps
%endif

%if %{with javadoc}
################################################################################
%files -n pki-javadoc
################################################################################

%{_javadocdir}/pki-%{version}/

# with javadoc
%endif

%if %{with console}
################################################################################
%files -n pki-console
################################################################################

%license base/console/LICENSE
%{_bindir}/pkiconsole
%{_javadir}/pki/pki-console.jar

# with console
%endif

%if %{with theme}
################################################################################
%files -n %{vendor_id}-pki-server-theme
################################################################################

%license themes/%{vendor_id}/common-ui/LICENSE
%dir %{_datadir}/pki
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

################################################################################
%files -n %{vendor_id}-pki-console-theme
################################################################################

%license themes/%{vendor_id}/console-ui/LICENSE
%{_javadir}/pki/pki-console-theme.jar

# with theme
%endif

%if %{with tests}
################################################################################
%files -n pki-tests
################################################################################

%{_datadir}/pki/tests/

# with tests
%endif

################################################################################
%changelog
* Wed Jan 12 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.10.3-10
- License verified.

* Thu Oct 28 2021 Muhammad Falak <mwani@microsft.com> - 10.10.3-9
- Drop epoch from tomcat

* Mon Oct 18 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.10.3-8
- Re-enabling 'policycoreutils' dependencies.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.10.3-7
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Sep 01 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.10.3-6
- Fixing minimal Java version dependency - removed epoch number.

* Wed Aug 18 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.10.3-5
- Manually setting 'JAVA_HOME' to work with CBL-Mariner's path.
- Moved tests to the '%%check' section.
- Disabling components not needed for CBL-Mariner:
    - acme;
    - console;
    - javadoc;
    - ocsp;
    - tks;
    - tps.
- Temporarily disabled following dependencies (see: bconds at the very top):
    - freeipa;
    - policycoreutils;
    - selinux-policy-targeted.

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 10.10.3-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Tue Jan 19 2021 Alexander Scheel <ascheel@redhat.com> - 10.10.3-3
- Sync spec between upstream and Fedora

* Tue Jan 19 2021 Alexander Scheel <ascheel@redhat.com> - 10.10.3-2
- Remove dependency on jakarta-commons-httpclient

* Thu Jan 14 2021 Dogtag PKI Team <pki-devel@redhat.com> - 10.10.3-1
- Rebase to upstream stable v10.10.3-1 release

* Thu Nov 05 2020 Dogtag PKI Team <pki-devel@redhat.com> - 10.10.0-2
- Add missing pki-acme package
- Add workaround for missing capture_output in Python 3.6
- Fix JSS initialization in pki-server <subsystem>-user-cert-add
- Fix NPE in UGSubsystem.findUsersByKeyword()

* Wed Oct 28 2020 Dogtag PKI Team <pki-devel@redhat.com> - 10.10.0-1
- Rebase to upstream stable v10.10.0-1 release

* Fri Sep 11 2020 Dogtag PKI Team <pki-devel@redhat.com> - 10.9.4-1
- Rebase to stable upstream v10.9.4 release

* Tue Aug 18 2020 Dogtag PKI Team <pki-devel@redhat.com> - 10.9.2-2
- Fix permission issue during clone installation; reported by FreeIPA
- Rebase to final release v10.9.2

* Tue Jun 30 2020 Dogtag PKI Team <pki-devel@redhat.com> - 10.9.0-0.4
- Rebase to match upstream beta version v10.9.0-b2
- pki password fix for FIPS

* Wed Jun 10 2020 Dogtag PKI Team <pki-devel@redhat.com> - 10.9.0-0.2
- Rebase to match upstream alpha version 10.9.0-a2

* Mon Apr 27 2020 Dinesh Prasanth M K <dmoluguw@redhat.com> - 10.8.3-2
- Fix bz#1814242 / dogtag issue #3168: Fix EC admin certificate profile upgrade

* Thu Mar 05 2020 Dinesh Prasanth M K <dmoluguw@redhat.com> - 10.8.3-1
- Rebase to latest upstream version
- Spec cleanup to match with upstream spec

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.7.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 10.7.3-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 10.7.3-4
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Dogtag PKI Team <pki-devel@redhat.com> - 10.7.3-3
- Rebuild with patches applied

* Wed Aug 14 2019 Dogtag PKI Team <pki-devel@redhat.com> - 10.7.3-2
- Fix URL redirection for KRA and OCSP web UI

* Thu Aug 08 2019 Dogtag PKI Team <pki-devel@redhat.com> - 10.7.3-1
- Rebased to PKI 10.7.3

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 10.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 06 2019 Dogtag PKI Team <pki-devel@redhat.com> - 10.7.0-1
- Rebased to PKI 10.7.0


