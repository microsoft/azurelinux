Vendor:         Microsoft Corporation
Distribution:   Mariner
%{?!PEGASUS_BUILD_TEST_RPM:     %global PEGASUS_BUILD_TEST_RPM        1}
# do "rpmbuild --define 'PEGASUS_BUILD_TEST_RPM 1'" to build test RPM.

%global srcname pegasus
%global major_ver 2.14
%global pegasus_gid 65
%global pegasus_uid 66

Name:           tog-pegasus
Version:        %{major_ver}.1
Release:        52%{?dist}
Summary:        OpenPegasus WBEM Services for Linux

License:        MIT
URL:            http://www.openpegasus.org
Source0:        https://collaboration.opengroup.org/pegasus/documents/27211/pegasus-%{version}.tar.gz
#  1: Description of security enhacements
Source1:        README.RedHat.Security
#  3: Description of SSL settings
Source3:        README.RedHat.SSL
#  4: /etc/tmpfiles.d configuration file
Source4:        tog-pegasus.tmpfiles
#  5: systemd service file
Source5:        tog-pegasus.service
#  6: This file controls access to the Pegasus services by users with the PAM pam_access module
Source6:        access.conf
#  7: Simple wrapper for Pegasus's cimprovagt - because of confining providers in SELinux
Source7:        cimprovagt-wrapper.sh
#  8: Example wrapper confining Operating System Provider from sblim-cmpi-base package
Source8:        cmpiOSBase_OperatingSystemProvider-cimprovagt.example
#  9: DMTF CIM schema
Source9:        cim_schema_2.38.0Experimental-MOFs.zip
# 10: Fedora/RHEL script for adding self-signed certificates to the local CA
#     trust store
Source10:       generate-certs
# 11: Configuration file for snmp tests in -test rpm
Source11:       snmptrapd.conf
# 12: repupgrade man page based on pegasus/src/Clients/repupgrade/doc/repupgrade.html
Source12:       repupgrade.1.gz

#  1: http://cvs.rdg.opengroup.org/bugzilla/show_bug.cgi?id=5011
#     Removing insecure -rpath
Patch1:         pegasus-2.9.0-no-rpath.patch
#  2: Adding -fPIE
Patch2:         pegasus-2.7.0-PIE.patch
#  3: http://cvs.rdg.opengroup.org/bugzilla/show_bug.cgi?id=5016
#     Configuration variables
Patch3:         pegasus-2.9.0-redhat-config.patch
#  4: don't see how http://cvs.rdg.opengroup.org/bugzilla/show_bug.cgi?id=5099 fixed it
#     Changing provider dir to the directory we use
Patch4:         pegasus-2.9.0-cmpi-provider-lib.patch
#  5: http://cvs.rdg.opengroup.org/bugzilla/show_bug.cgi?id=5010
#     We distinguish between local and remote user and behave adequately (will be upstream once)
Patch5:         pegasus-2.9.0-local-or-remote-auth.patch
#  6: http://cvs.rdg.opengroup.org/bugzilla/show_bug.cgi?id=5012
#     Modifies pam rules to use access cofiguration file and local/remote differences
Patch6:         pegasus-2.5.1-pam-wbem.patch
# 12: Adds snmp tests to the -test rpm, configures snmptrapd
Patch12:        pegasus-2.7.0-snmp-tests.patch
# 13: Changes to make package compile on sparc
Patch13:        pegasus-2.9.0-sparc.patch
# 16: Fixes "getpagesize" build error
Patch16:        pegasus-2.9.1-getpagesize.patch
# 19: Don't strip binaries, add -g flag
Patch19:        pegasus-2.10.0-dont-strip.patch
# 20: use posix locks on sparc arches
Patch20:        pegasus-2.10.0-sparc-posix-lock.patch
# 22: Fix CMPI enumGetNext function to change CMPI Data state from default CMPI_nullValue
#     to CMPI_goodValue when it finds and returns next instance correctly
Patch22:        pegasus-2.12.0-null_value.patch
# 24: bz#883030, getPropertyAt() returns Null instead of empty array
Patch24:        pegasus-2.12.0-empty_arrays.patch
# 25: allow experimental schema registration with cimmofl during build
Patch25:        pegasus-2.12.0-cimmofl-allow-experimental.patch
# 26: use external schema and add missing includes there
Patch26:        pegasus-2.12.0-schema-version-and-includes.patch
# 29: bz#1049314, allow unprivileged users to subscribe to indications by default
Patch29:        pegasus-2.13.0-enable-subscriptions-for-nonprivileged-users.patch
# 33: fixes build with gcc5
Patch33:        pegasus-2.13.0-gcc5-build.patch
# 34: fixes various build problemss
Patch34:        pegasus-2.14.1-build-fixes.patch
# 35: add missing ssl.h include
Patch35:        pegasus-2.14.1-ssl-include.patch
# 36: fixes sending of SNMPv3 traps in cimserver
Patch36:        pegasus-2.14.1-snmpv3-trap.patch
# 37: fixes setupSDK in -devel
Patch37:        pegasus-2.14.1-fix-setup-sdk.patch
# 38: cimconfig man page fixes
Patch38:        pegasus-2.14.1-cimconfig-man-page-fixes.patch
# 39: fixes setupSDK in -devel for ppc64le
Patch39:        pegasus-2.14.1-fix-setup-sdk-ppc64le.patch
# 40: removes Beaker conflicting env variable
Patch40:        pegasus-2.14.1-tesid.patch
# 41: moves SSL certificates to /etc/pki/Pegasus
Patch41:        pegasus-2.14.1-ssl-cert-path.patch
# 42: port to openssl-1.1
Patch42:        pegasus-2.14.1-openssl-1.1-fix.patch

BuildRequires:  procps, libstdc++, pam-devel
BuildRequires:  openssl, openssl-devel
BuildRequires:  bash, sed, grep, coreutils, procps, gcc, gcc-c++
BuildRequires:  libstdc++, make, pam-devel
BuildRequires:  openssl-devel
BuildRequires:  net-snmp-devel, openslp-devel
BuildRequires:  systemd-units
Requires:       net-snmp-libs
Requires:       %{name}-libs = %{version}-%{release}
Requires:       openssl
Requires:       ca-certificates
Provides:       cim-server = 1
Requires(post): /sbin/ldconfig
Requires(post): /sbin/restorecon

%description
OpenPegasus WBEM Services for Linux enables management solutions that deliver
increased control of enterprise resources. WBEM is a platform and resource
independent DMTF standard that defines a common information model and
communication protocol for monitoring and controlling resources from diverse
sources.

%package devel
Summary:        The OpenPegasus Software Development Kit
Requires:       tog-pegasus >= %{version}-%{release}
Obsoletes:      tog-pegasus-sdk

%description devel
The OpenPegasus WBEM Services for Linux SDK is the developer's kit for the
OpenPegasus WBEM Services for Linux release. It provides Linux C++ developers
with the WBEM files required to build WBEM Clients and Providers. It also
supports C provider developers via the CMPI interface.

%package libs
Summary:        The OpenPegasus Libraries
Conflicts:      libcmpiCppImpl0
Requires(pre):  /usr/sbin/useradd
Requires(pre):  /usr/sbin/groupadd
Requires(post): /sbin/ldconfig

%description libs
The OpenPegasus libraries.

%if %{PEGASUS_BUILD_TEST_RPM}
%package test
Summary:        The OpenPegasus Tests
Requires:       tog-pegasus >= %{version}-%{release}, make
Requires:       %{name}-libs = %{version}-%{release}

%description test
The OpenPegasus WBEM tests for the OpenPegasus %{version} Linux rpm.
%endif


%ifarch ia64
%global PEGASUS_HARDWARE_PLATFORM LINUX_IA64_GNU
%endif
%ifarch x86_64
%global PEGASUS_HARDWARE_PLATFORM LINUX_X86_64_GNU
%endif
%ifarch ppc
%global PEGASUS_HARDWARE_PLATFORM LINUX_PPC_GNU
%endif
%ifarch ppc64
%global PEGASUS_HARDWARE_PLATFORM LINUX_PPC64_GNU
%endif
%ifarch ppc64le
%global PEGASUS_HARDWARE_PLATFORM LINUX_PPC64_GNU
%endif
%ifarch s390
%global PEGASUS_HARDWARE_PLATFORM LINUX_ZSERIES_GNU
%endif
%ifarch s390x
%global PEGASUS_HARDWARE_PLATFORM LINUX_ZSERIES64_GNU
%endif
%ifarch sparcv9
%global PEGASUS_HARDWARE_PLATFORM LINUX_SPARCV9_GNU
%endif
%ifarch sparc64
%global PEGASUS_HARDWARE_PLATFORM LINUX_SPARC64_GNU
%endif
%ifarch %{ix86}
%global PEGASUS_HARDWARE_PLATFORM LINUX_IX86_GNU
%endif
%ifarch %{arm}
%global PEGASUS_HARDWARE_PLATFORM LINUX_XSCALE_GNU
%endif
%ifarch aarch64
%global PEGASUS_HARDWARE_PLATFORM LINUX_AARCH64_GNU
%endif

%global PEGASUS_ARCH_LIB %{_lib}
%global OPENSSL_HOME /usr
%global OPENSSL_BIN /usr/bin
%global PEGASUS_PEM_DIR /etc/pki/Pegasus
%global PEGASUS_SSL_CERT_FILE server.pem
%global PEGASUS_SSL_KEY_FILE file.pem
%global PEGASUS_SSL_TRUSTSTORE client.pem
%global PAM_CONFIG_DIR /etc/pam.d
%global PEGASUS_CONFIG_DIR /etc/Pegasus
%global PEGASUS_VARDATA_DIR /var/lib/Pegasus
%global PEGASUS_VARDATA_CACHE_DIR /var/lib/Pegasus/cache
%global PEGASUS_LOCAL_DOMAIN_SOCKET_PATH  /var/run/tog-pegasus/socket/cimxml.socket
%global PEGASUS_CIMSERVER_START_FILE /var/run/tog-pegasus/cimserver.pid
%global PEGASUS_TRACE_FILE_PATH /var/lib/Pegasus/cache/trace/cimserver.trc
%global PEGASUS_CIMSERVER_START_LOCK_FILE /var/run/tog-pegasus/cimserver_start.lock
%global PEGASUS_REPOSITORY_DIR /var/lib/Pegasus/repository
%global PEGASUS_PREV_REPOSITORY_DIR_NAME prev_repository
%global PEGASUS_REPOSITORY_PARENT_DIR /var/lib/Pegasus
%global PEGASUS_PREV_REPOSITORY_DIR /var/lib/PegasusXXX/prev_repository
%global PEGASUS_SBIN_DIR /usr/sbin
%global PEGASUS_DOC_DIR /usr/share/doc/%{name}-%{version}

%global PEGASUS_RPM_ROOT $RPM_BUILD_DIR/%{srcname}
%global PEGASUS_RPM_HOME %PEGASUS_RPM_ROOT/build
%global PEGASUS_INSTALL_LOG /var/lib/Pegasus/log/install.log


%prep
%setup -q -n %{srcname}
# convert DMTF schema for Pegasus
export PEGASUS_ROOT=%PEGASUS_RPM_ROOT
yes | mak/CreateDmtfSchema 238 %{SOURCE9} cim_schema_2.38.0
%patch1 -p1 -b .no-rpath
%patch2 -p1 -b .PIE
%patch3 -p1 -b .redhat-config
%patch4 -p1 -b .cmpi-provider-lib
%patch6 -p1 -b .pam-wbem
%patch12 -p1 -b .snmp-tests
%patch5 -p1 -b .local-or-remote-auth
%patch13 -p1 -b .sparc
%patch16 -p1 -b .getpagesize
%patch19 -p1 -b .dont-strip
%patch20 -p1 -b .sparc-locks
%patch22 -p1 -b .null_value
%patch24 -p1 -b .empty_arrays
%patch25 -p1 -b .cimmofl-allow-experimental
%patch26 -p1 -b .schema-version-and-includes
%patch29 -p1 -b .enable-subscriptions-for-nonprivileged-users
%patch33 -p1 -b .gcc5-build
%patch34 -p1 -b .build-fixes
%patch35 -p1 -b .ssl-include
%patch36 -p1 -b .snmpv3-trap
%patch37 -p1 -b .fix-setup-sdk
%patch38 -p1 -b .cimconfig-man-page-fixes
%patch39 -p1 -b .fix-setup-sdk-ppc64le
%patch40 -p1 -b .testid
%patch41 -p1 -b .ssl-cert-path
%patch42 -p1 -b .openssl-1.1-fix


%build
cp -fp %SOURCE1 doc
cp -fp %SOURCE3 doc
cp -fp %SOURCE6 rpm
cp -fp %SOURCE8 doc

export PEGASUS_ROOT=%PEGASUS_RPM_ROOT
export PEGASUS_HOME=%PEGASUS_RPM_HOME
export PEGASUS_PLATFORM=%PEGASUS_HARDWARE_PLATFORM
export PEGASUS_ARCH_LIB=%PEGASUS_ARCH_LIB
export PEGASUS_ENVVAR_FILE=$PEGASUS_ROOT/env_var_Linux.status

export OPENSSL_HOME=%OPENSSL_HOME
export OPENSSL_BIN=%OPENSSL_BIN
export LD_LIBRARY_PATH=$PEGASUS_HOME/lib
export PATH=$PEGASUS_HOME/bin:$PATH

export PEGASUS_EXTRA_C_FLAGS="$RPM_OPT_FLAGS -fPIC -g -Wall -Wno-unused -fno-strict-aliasing"
export PEGASUS_EXTRA_CXX_FLAGS="$PEGASUS_EXTRA_C_FLAGS"
export PEGASUS_EXTRA_LINK_FLAGS="$RPM_OPT_FLAGS"
export PEGASUS_EXTRA_PROGRAM_LINK_FLAGS="-g -pie -Wl,-z,relro,-z,now,-z,nodlopen,-z,noexecstack"
export SYS_INCLUDES=-I/usr/kerberos/include

make %{?_smp_mflags} -f ${PEGASUS_ROOT}/Makefile.Release create_ProductVersionFile
make %{?_smp_mflags} -f ${PEGASUS_ROOT}/Makefile.Release create_CommonProductDirectoriesInclude
make %{?_smp_mflags} -f ${PEGASUS_ROOT}/Makefile.Release create_ConfigProductDirectoriesInclude
make %{?_smp_mflags} -f ${PEGASUS_ROOT}/Makefile.Release all
make %{?_smp_mflags} -f ${PEGASUS_ROOT}/Makefile.Release repository


%install
# Create directory for SSL certificates
mkdir -p $RPM_BUILD_ROOT/etc/pki/Pegasus

export PEGASUS_ROOT=%PEGASUS_RPM_ROOT
export PEGASUS_HOME=%PEGASUS_RPM_HOME
export PEGASUS_PLATFORM=%PEGASUS_HARDWARE_PLATFORM
export PEGASUS_ARCH_LIB=%PEGASUS_ARCH_LIB
export PEGASUS_ENVVAR_FILE=$PEGASUS_ROOT/env_var_Linux.status

export OPENSSL_BIN=%OPENSSL_BIN
export LD_LIBRARY_PATH=$PEGASUS_HOME/lib
export PATH=$PEGASUS_HOME/bin:$PATH

export PEGASUS_STAGING_DIR=$RPM_BUILD_ROOT
%if %{PEGASUS_BUILD_TEST_RPM}
make -f $PEGASUS_ROOT/Makefile.Release stage \
    PEGASUS_STAGING_DIR=$PEGASUS_STAGING_DIR \
    PEGASUS_BUILD_TEST_RPM=%{PEGASUS_BUILD_TEST_RPM}
%else
make -f $PEGASUS_ROOT/Makefile.Release stage \
    PEGASUS_STAGING_DIR=$PEGASUS_STAGING_DIR
%endif

mkdir -p $RPM_BUILD_ROOT/%{_tmpfilesdir}
install -p -D -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_tmpfilesdir}/tog-pegasus.conf

# Install script to generate SSL certificates at startup
mkdir -p $RPM_BUILD_ROOT/usr/share/Pegasus/scripts
install -p -m 755 %{SOURCE10} $RPM_BUILD_ROOT/usr/share/Pegasus/scripts/generate-certs
# Remove unused ssl.cnf file
rm -f $RPM_BUILD_ROOT/etc/Pegasus/ssl.cnf
# Create certificate revocation list dir (see bz#1032046)
mkdir -p $RPM_BUILD_ROOT/etc/pki/Pegasus/crl

# remove SysV initscript, install .service file
rm -f $RPM_BUILD_ROOT/etc/init.d/tog-pegasus
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_unitdir}/tog-pegasus.service
# cimserver_planned.conf is on the right place since 2.9.2 (update - not in 2.10.0)
#mv $RPM_BUILD_ROOT/var/lib/Pegasus/cimserver_planned.conf $RPM_BUILD_ROOT/etc/Pegasus/cimserver_planned.conf
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}
mv $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{major_ver}/* $RPM_BUILD_ROOT/%{_docdir}/%{name}
rm -rf $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{major_ver}
# create symlink for libcmpiCppImpl
pushd $RPM_BUILD_ROOT/usr/%{_lib}
ln -s libcmpiCppImpl.so.1 libcmpiCppImpl.so
# and libpeglistener
ln -s libpeglistener.so.1 libpeglistener.so
popd
mkdir -p $RPM_BUILD_ROOT/%{_libexecdir}/pegasus
mv $RPM_BUILD_ROOT/%{_sbindir}/cimprovagt $RPM_BUILD_ROOT/%{_libexecdir}/pegasus
install -p -m 0755 %{SOURCE7} $RPM_BUILD_ROOT/%{_sbindir}/cimprovagt
# install Platform_LINUX_XSCALE_GNU.h because of lmiwbem on arm
install -m 644 src/Pegasus/Common/Platform_LINUX_XSCALE_GNU.h $RPM_BUILD_ROOT/%{_includedir}/Pegasus/Common
# install Linkage.h and CIMListener.h because of lmiwbem (CIMListener class)
mkdir -p $RPM_BUILD_ROOT/%{_includedir}/Pegasus/Listener
install -m 644 src/Pegasus/Listener/Linkage.h $RPM_BUILD_ROOT/%{_includedir}/Pegasus/Listener
install -m 644 src/Pegasus/Listener/CIMListener.h $RPM_BUILD_ROOT/%{_includedir}/Pegasus/Listener
install -m 644 src/Pegasus/Client/CIMEnumerationContext.h $RPM_BUILD_ROOT/%{_includedir}/Pegasus/Client
install -m 644 src/Pegasus/Common/UintArgs.h $RPM_BUILD_ROOT/%{_includedir}/Pegasus/Common

# Install snptrapd.conf used for net-snmp tests
%if %{PEGASUS_BUILD_TEST_RPM}
install -p %{SOURCE11} $RPM_BUILD_ROOT/usr/share/Pegasus/test/snmptrapd.conf
%endif

# Install missing mof file for makeSDK
install -p Schemas/CIM238/DMTF/Core/CIM_AbstractComponent.mof $RPM_BUILD_ROOT/usr/share/Pegasus/samples/Providers/Load/CIM238/DMTF/Core/

# install man page
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man1/
cp %SOURCE12 ${RPM_BUILD_ROOT}/%{_mandir}/man1/

%check
# run unit tests
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT/usr/%{_lib}
cd $RPM_BUILD_ROOT/usr/share/Pegasus/test
make prestarttests
# remove files created during the test
rm $RPM_BUILD_ROOT/usr/share/Pegasus/test/log.trace.0
rm $RPM_BUILD_ROOT/usr/share/Pegasus/test/testtracer4.trace.0


%files
%defattr(0640, root, pegasus, 0750)
%verify(not md5 size mtime mode group) /var/lib/Pegasus/repository
%defattr(0644, root, pegasus, 0755)
/usr/share/Pegasus/mof
%dir /usr/share/Pegasus
%defattr(0755, root, pegasus, 0750)
/usr/share/Pegasus/scripts
%defattr(0640, root, pegasus, 0750)
%dir /var/lib/Pegasus
/var/lib/Pegasus/cache
%dir /var/lib/Pegasus/log
%defattr(0640, root, pegasus, 0750)
%dir /etc/Pegasus
%dir /etc/pki/Pegasus
%{_tmpfilesdir}/tog-pegasus.conf
%defattr(0640, root, pegasus, 1750)
%ghost /var/run/tog-pegasus
%ghost %attr(0600, root, root) /var/run/tog-pegasus/cimserver.pid
%ghost %attr(0600, root, root) /var/run/tog-pegasus/cimserver_start.lock
%ghost %attr(0777 ,root, root) /var/run/tog-pegasus/cimxml.socket
%attr(0644, root, pegasus) %{_unitdir}/tog-pegasus.service
%defattr(0640, root, pegasus, 0750)
%ghost %attr(0644, root, root) %config(noreplace) /etc/Pegasus/cimserver_current.conf
%ghost %attr(0644, root, root) %config(noreplace) /etc/Pegasus/cimserver_planned.conf
%config(noreplace) /etc/Pegasus/access.conf
%config(noreplace) /etc/pam.d/wbem
%defattr(0444, root, root)
%ghost /etc/pki/Pegasus/client.pem
%ghost /etc/pki/Pegasus/server.pem
%defattr(0400, root, root)
%ghost /etc/pki/Pegasus/file.pem
%defattr(0644, root, root)
%ghost /etc/pki/Pegasus/ca.crt
%ghost /etc/pki/Pegasus/ca.srl
%ghost /etc/pki/Pegasus/client.srl
%defattr(0400, root, root)
%ghost /etc/Pegasus/ssl-ca.cnf
%ghost /etc/Pegasus/ssl-service.cnf
%defattr(0644, root, root)
%ghost /etc/pki/ca-trust/source/anchors/localhost-pegasus.pem
%ghost %attr(0640, root, pegasus) /etc/pki/Pegasus/cimserver_trust
%ghost %attr(0640, root, pegasus) /etc/pki/Pegasus/indication_trust
%dir %attr(0640, root, pegasus) /etc/pki/Pegasus/crl
%ghost %attr(0644, root, root) %verify(not md5 size mtime) /var/lib/Pegasus/log/install.log
%ghost %attr(0640, root, pegasus) %verify(not md5 size mtime) /var/lib/Pegasus/cache/trace/cimserver.trc
%defattr(0755, root, pegasus, 0755)
/usr/sbin/*
/usr/bin/*
%{_libexecdir}/pegasus/
%defattr(0644, root, pegasus, 0755)
/usr/share/man/man8/*
/usr/share/man/man1/*
%doc doc/license.txt doc/Admin_Guide_Release.pdf doc/PegasusSSLGuidelines.htm doc/SecurityGuidelinesForDevelopers.html doc/README.RedHat.Security src/Clients/repupgrade/doc/repupgrade.html doc/README.RedHat.SSL doc/cmpiOSBase_OperatingSystemProvider-cimprovagt.example OpenPegasusNOTICE.txt

%files devel
%defattr(0644,root,pegasus,0755)
/usr/share/Pegasus/samples
/usr/include/Pegasus
/usr/share/Pegasus/html

%files libs
%defattr(0755, root, pegasus, 0755)
%{_libdir}/*
%exclude /usr/lib/debug
%exclude /usr/lib/systemd
%exclude %{_tmpfilesdir}

%if %{PEGASUS_BUILD_TEST_RPM}
%files test
%defattr(0644,root,pegasus,0755)
%dir /usr/share/Pegasus/test
/usr/share/Pegasus/test/Makefile
%attr(0600, root, root) /usr/share/Pegasus/test/snmptrapd.conf
/usr/share/Pegasus/test/mak
%dir /usr/share/Pegasus/test/tmp
%ghost /usr/share/Pegasus/test/tmp/procIdFile
%ghost /usr/share/Pegasus/test/tmp/trapLogFile
%ghost /usr/share/Pegasus/test/tmp/IndicationStressTestLog
%ghost /usr/share/Pegasus/test/tmp/oldIndicationStressTestLog
%verify(not md5 size mtime) /var/lib/Pegasus/testrepository
%defattr(0750,root,pegasus,0755)
/usr/share/Pegasus/test/bin
/usr/share/Pegasus/test/%PEGASUS_ARCH_LIB
%endif


%pre
if [ $1 -gt 1 ]; then
   if [ -d /var/lib/Pegasus/repository ]; then
        if [ -d /var/lib/Pegasus/prev_repository ]; then
           rm -rf /var/lib/Pegasus/prev_repository
        fi;
        cp -r /var/lib/Pegasus/repository /var/lib/Pegasus/prev_repository;
   fi
fi
:;

%post
install -d -m 1750 -o root -g pegasus /var/run/tog-pegasus
restorecon /var/run/tog-pegasus
/sbin/ldconfig;
%systemd_post tog-pegasus.service
if [ $1 -ge 1 ]; then
   echo `date` >>  /var/lib/Pegasus/log/install.log 2>&1 || :;
   if [ $1 -gt 1 ]; then
      if [ -d /var/lib/Pegasus/prev_repository ]; then
      #  The user's old repository was moved to /var/lib/Pegasus/prev_repository, which 
      #  now must be upgraded to the new repository in /var/lib/Pegasus/repository:
         /usr/sbin/repupgrade 2>> /var/lib/Pegasus/log/install.log || :;
      fi;
      /bin/systemctl try-restart tog-pegasus.service >/dev/null 2>&1 || :;
   fi;
fi
:;

%preun
%systemd_preun stop tog-pegasus.service
if [ $1 -eq 0 ]; then                  
   # Package removal, not upgrade     
   rm -rf /var/run/tog-pegasus
fi
:;

%postun
/sbin/ldconfig
%systemd_postun_with_restart tog-pegasus.service

%preun devel
if [ $1 -eq 0 ] ; then
   make --directory /usr/share/Pegasus/samples -s clean >/dev/null 2>&1 || :;
fi
:;

%pre libs
if [ $1 -eq 1 ]; then
#  first install: create the 'pegasus' user and group:
   /usr/sbin/groupadd -g %{pegasus_gid} -f -r pegasus >/dev/null 2>&1 || :; 
   /usr/sbin/useradd -u %{pegasus_uid} -r -N -M -g pegasus -s /usr/sbin/nologin -d /var/lib/Pegasus \
     -c "tog-pegasus OpenPegasus WBEM/CIM services" pegasus >/dev/null 2>&1 || :;
fi
:;

%post libs
if [ $1 -eq 1 ]; then
   # Create Symbolic Links for SDK Libraries
   #
   ln -sf libpegclient.so.1 /usr/%PEGASUS_ARCH_LIB/libpegclient.so
   ln -sf libpegcommon.so.1 /usr/%PEGASUS_ARCH_LIB/libpegcommon.so
   ln -sf libpegprovider.so.1 /usr/%PEGASUS_ARCH_LIB/libpegprovider.so
   ln -sf libDefaultProviderManager.so.1 /usr/%PEGASUS_ARCH_LIB/libDefaultProviderManager.so
   ln -sf libCIMxmlIndicationHandler.so.1 /usr/%PEGASUS_ARCH_LIB/libCIMxmlIndicationHandler.so
   ln -sf libsnmpIndicationHandler.so.1 /usr/%PEGASUS_ARCH_LIB/libsnmpIndicationHandler.so

   # Create Symbolic Links for Packaged Provider Libraries
   #
   ln -sf libComputerSystemProvider.so.1 /usr/%PEGASUS_ARCH_LIB/Pegasus/providers/libComputerSystemProvider.so
   ln -sf libOSProvider.so.1 /usr/%PEGASUS_ARCH_LIB/Pegasus/providers/libOSProvider.so
   ln -sf libProcessProvider.so.1 /usr/%PEGASUS_ARCH_LIB/Pegasus/providers/libProcessProvider.so

   # Create Symbolic Links for Packaged Provider Managers
   #
   ln -sf libCMPIProviderManager.so.1 /usr/%PEGASUS_ARCH_LIB/Pegasus/providerManagers/libCMPIProviderManager.so

   # Change ownership of Symbolic Links to the 'pegasus' group
   #
   /bin/chgrp -h pegasus /usr/%{_lib}/libpegclient.so
   /bin/chgrp -h pegasus /usr/%{_lib}/libpegcommon.so 
   /bin/chgrp -h pegasus /usr/%{_lib}/libpegprovider.so
   /bin/chgrp -h pegasus /usr/%{_lib}/libDefaultProviderManager.so
   /bin/chgrp -h pegasus /usr/%{_lib}/libCIMxmlIndicationHandler.so
   /bin/chgrp -h pegasus /usr/%{_lib}/libsnmpIndicationHandler.so
   /bin/chgrp -h pegasus /usr/%{_lib}/Pegasus/providers/libComputerSystemProvider.so
   /bin/chgrp -h pegasus /usr/%{_lib}/Pegasus/providers/libOSProvider.so
   /bin/chgrp -h pegasus /usr/%{_lib}/Pegasus/providers/libProcessProvider.so
   /bin/chgrp -h pegasus /usr/%{_lib}/Pegasus/providerManagers/libCMPIProviderManager.so
fi
:;
/sbin/ldconfig

%postun libs
/sbin/ldconfig


%changelog
* Thu Oct 28 2021 Muhammad Falak <mwani@microsft.com> - 2.14.1-52
- Remove epoch

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2:2.14.1-51
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.14.1-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.14.1-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.14.1-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 2:2.14.1-47
- Rebuilt for libcrypt.so.2 (#1666033)

* Wed Aug 01 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-46
- Review and fix %%files section because of failing rpm -V

* Tue Jul 24 2018 Adam Williamson <awilliam@redhat.com> - 2:2.14.1-45
- Rebuild for new net-snmp

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.14.1-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.14.1-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2:2.14.1-42
- Rebuilt for switch to libxcrypt

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.14.1-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.14.1-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 01 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-39
- Fix FTBFS because of openssl-1.1
  Resolves: #1424141

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.14.1-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 31 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-37
- Release permissions for files %%{_libdir}/Pegasus, there's no reason
  to hide them for others

* Thu Mar 17 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-36
- Move SSL certificates to more convenient place, update related scripts
  and README.RedHat.SSL
  Related: #1308809

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.14.1-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 12 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-34
- Remove Beaker conflicting env variable from benchmark tests

* Tue Oct 06 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-33
- Fix setupSDK in -devel for ppc64le

* Mon Sep 21 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-32
- Add manpage for repupgrade, fixes in cimconfig manapage

* Tue Sep 15 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-31
- Add missing dependency for -test subpackage
- Fix enumerating instances of PG_SSLCertificateRevocationList returns error
  Resolves: #1032046

* Mon Aug 31 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-30
- Fix possible cleanup warning during package upgrade

* Thu Aug 13 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-29
- Require restorecon because of %%post
  Resolves: #1253127

* Tue Jun 23 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-28
- Add install CIMEnumerationContext.h and UintArgs.h to -devel because of lmiwbem

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.14.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-26
- Fix setupSDK in -devel
- Use Experimental DMTF CIM schema version 2.38.0

* Tue May 26 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-25
- Fix sending of SNMPv3 traps

* Tue May 19 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-24
- Add snmp tests to the -test rpm and enable them, configure snmptrapd
  in test setup phase
- Add missing ssl.h include

* Wed Apr 08 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.14.1-23
- Update to upstream version 2.14.1

* Tue Feb 10 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-23
- Fix tog-pegasus.service is marked world-inaccessible
  Resolves: #1191026
- Fix build fail with gcc5

* Mon Feb 02 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-22
- Backup only latest repository when upgrading the package
  Resolves: #1069620

* Mon Jan 26 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-21
- Exclude accidentaly packed tmpfiles dir from -libs subpackage on i686
  Resolves: #1185133

* Mon Jan 19 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-20
- Fix packaging of tmpfiles

* Mon Sep 22 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-19
- Fix missing space in generate-certs

* Mon Sep 01 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-18
- Increase security of generating SSL certificates

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.13.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-16
- Fix Pegasus service regenerates SSL certificates on every start
  Resolves: #1126871

* Tue Aug 05 2014 Michal Minar <miminar@redhat.com> - 2:2.13.0-15
- Fixed wrong instances from CIMOM callback
  Resolves: #1038013

* Tue Jul 01 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-14
- Fix cmpi: CMGetKey() returns wrong data type for some data types
  Resolves: #1111571

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.13.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-12
- Add symlink to libpeglistener.so.1

* Wed Apr 23 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-11
- Add install Linkage.h and CIMListener.h to -devel because of lmiwbem
  (CIMListener class)

* Tue Mar 18 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-10
- Port to ppc64le architecture (patch by Michel Normand)
  Resolves: #1075923

* Wed Mar 12 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-9
- Wait for the slpd.service in the systemd unit file (patch by Tomas Smetana)

* Thu Mar 06 2014 Stephen Gallagher <sgallagh@redhat.com> - 2:2.13.0-8
- Generate SSL certificates with x509v3 and CA:FALSE
- Automatically import self-signed certificates into local trust-store
- Move SSL certificate generation into the systemd service file

* Thu Jan 30 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-7
- Add Platform_LINUX_XSCALE_GNU.h to -devel because of lmiwbem on arm

* Wed Jan 08 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-6
- Allow unprivileged users to subscribe to indications
  Resolves: #1049314
- Remove packages which are part of the minimum build environment from BR

* Mon Nov 04 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-5
- Fix missing openssl dependency
  Resolves: #1022056

* Thu Oct 24 2013 Tomas Bzatek <tbzatek@redhat.com> - 2:2.13.0-4
- Fix PG_ComputerSystem to have correct CreationClassName value

* Wed Oct 09 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-3
- Add version to cim-server virtual provides

* Thu Sep 05 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-2
- Use Experimental DMTF CIM schema version 2.38.0

* Tue Sep 03 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.13.0-1
- Update to upstream version 2.13.0

* Tue Aug 27 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.1-9
- Fix package FTBFS, unversioned docdir change
  Resolves: #992795

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.12.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.1-7
- Require net-snmp-libs instead of net-snmp

* Mon Jul 22 2013 D.Marlin <dmarlin@redhat.com> - 2:2.12.1-6
- Add initial 64-bit ARM (Aarch64) support.
  See http://bugzilla.openpegasus.org/show_bug.cgi?id=9663

* Thu Jul 18 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.1-5
- Change root/PG_InterOp to root/interop

* Mon Jun 03 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.1-4
- Workaround for Python reinitializion issue
  Resolves: #958273

* Tue May 07 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.1-3
- Fix atomic operations on ARM (patch by D. Marlin)
  Resolves: #922770

* Thu Apr 25 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.1-2
- Add -fno-strict-aliasing

* Sun Mar 31 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2:2.12.1-1
- Update to upstream version 2.12.1

* Mon Mar 18 2013 Jon Ciesla <limburgher@gmail.com> - 2:2.12.0-16
- Fix dates in changelog, BZ 922770.

* Tue Mar 12 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-15
- Fix source link 
  Resolves: #905992

* Mon Feb 18 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-14
- Fix /usr/lib/systemd* unintentionally included in -libs subpackage 

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.12.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-12
- Fix schema-version-and-includes patch

* Wed Jan 16 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-11
- Use Experimental DMTF CIM schema version 2.33.0

* Tue Jan 08 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-10
- Fix getPropertyAt() returns Null instead of empty array (patch by Jan Safranek)

* Tue Dec 18 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-9
- Add cimprovagt wrapper for possibility of confining providers in SELinux,
  update README.RedHat.Security accordingly, add provider specific wrapper
  example

* Thu Dec 06 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-8
- Fix tracing of CMPI messages with CMPI_DEV_DEBUG severity
  Resolves: #883395

* Mon Dec 03 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-7
- Add %%check section and run unit tests
- Enable -test subpackage

* Tue Nov 20 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-6
- Set PEGASUS_ENABLE_INTEROP_PROVIDER=true (fixes registration of CMPI providers)
- Move .so links back to main package (they are necessary to be present for a user
  to use or execute the functionality in the base package properly)

* Tue Nov 13 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-5
- Call ldconfig in %%post/%%postun of -libs subpackage
- Move .so links to -devel subpackage

* Wed Oct 24 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-4
- Fix CMPI enumGetNext function to change CMPI Data state from default CMPI_nullValue
  to CMPI_goodValue when it finds and returns next instance correctly
- Enable processing of ExecQuery operations

* Thu Oct 18 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-3
- Fix permissions for executables

* Tue Oct 16 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-2
- Fix local-or-remote-auth patch to work with IPv6
- Distribute modified access.conf file to conform README.RedHat.Security

* Tue Oct 09 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.12.0-1
- Update to upstream version 2.12.0

* Wed Aug 22 2012 Lukáš Nykrýn <lnykryn@redhat.com> - 2:2.11.1-10
- Scriptlets replaced with new systemd macros (#850411)

* Tue Jul 31 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.11.1-9
- Fix security context of /var/run/tog-pegasus in post install scriptlet

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.11.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2:2.11.1-7
- Add options for ARM arch, cleanup ARCH directives
- Add openssl base package

* Mon May 21 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.11.1-6
- Add systemd support

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.11.1-5
- Rebuilt for c++ ABI breakage

* Mon Feb 06 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.11.1-4
- Add missing useradd/groupadd dependency to tog-pegasus-libs
  Resolves: #786888

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.11.1-2
- Fix post created symlinks group owner to 'pegasus'

* Tue Sep 27 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.11.1-1
- Update to upstream version 2.11.1
- Add explicit file attributes where RPM requires it
- Disable privilege separation feature

* Mon Jul 18 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.11.0-2
- Rebuild

* Thu May 19 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.11.0-1
- Update to upstream version 2.11.0

* Tue Apr 05 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.10.0-6
- Add -g flag for compiler

* Wed Mar 30 2011 Dennis Gilmore <dennis@ausil.us> - 2:2.10.0-5
- use posix locks on sparc linux arches

* Tue Mar 22 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.10.0-4
- Use %%ghost for /var/run/tog-pegasus
  Resolves: #656705

* Tue Mar 01 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.10.0-3
- Don't strip binaries

* Thu Feb 17 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.10.0-2
- Remove dubuginfo files from -libs subpackage

* Wed Feb 16 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.10.0-1
- Update to upstream version 2.10.0
- Move creating of the 'pegasus' user and group to the 'libs' %%pre
- Use %%global instead of %%define and some minor spec file cleaning

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.2-2
- Fix provides

* Wed Nov  3 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.2-1
- Update to upstream version 2.9.2
- Mark files in /var/lib/Pegasus as noverify in spec file
- Fix initscript permissions
- Add patch/source descriptions to the spec file
- Cleanup the spec file, use upstream Makefile

* Thu Apr 22 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.0-11
- Fix initscript permissions

* Thu Jan 21 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.0-10
- Add cimsub to the pegasus_arch_alternatives script
  Resolves: #543956

* Mon Nov  2 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.0-9
- Fix wrong multilib flag for ix86 arch

* Wed Sep 30 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.0-8
- Rebuilt with new net-snmp

* Wed Sep 23 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.0-7
- Fix initscript
  Resolves: #523370

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 2:2.9.0-6
- Use password-auth common PAM configuration instead of system-auth

* Tue Aug 25 2009 Tomas Mraz <tmraz@redhat.com> - 2:2.9.0-5
- rebuilt with new openssl

* Wed Aug 19 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.0-4
- Fix Source (but I'm afraid it's not very persistent and it will
  not work again after some time)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.0-2
- Fix Group

* Tue Jun 16 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.9.0-1
- Update to upstream version 2.9.0
- Remove redhat-lsb requires
- Add README.RedHat.SSL

* Thu Apr 16 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.2-8
- Replace useradd '-n' option by '-N' ('-n' is obsolete)
  Resolves: #495729

* Tue Mar  3 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.2-7
- Add noreplace to config files

* Sat Feb 28 2009 Caolán McNamara <caolanm@redhat.com> - 2:2.7.2-6
- fix elif

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Dennis Gilmore < dennis@ausil.us> - 2:2.7.2-4
- apply sparc fixes

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 2:2.7.2-3
- rebuild with new openssl

* Tue Nov 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.2-2
- Fix local or remote auth patch to work correctly with new code base
  Related: #459217

* Thu Nov  6 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.2-1
- Update to upstream version 2.7.2
  (remove patches added in 2.7.1-1 - they're upstream now)
- Enable out-of-process providers
  Resolves: #455109

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2.7.1-2
- fix license tag

* Tue Jul 15 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.1-1
- Update to upstream version 2.7.1
- Fix setElementAt() doesn't copy value of CMPI_char parameter
  Resolves: #454589
- Fix CMPI MI factories that return errors are unsupported
  Resolves: #454590
- Fix HTTP 401 responses lack Content-Length headers
  Resolves: #454591

* Tue Jul  1 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-9
- Add SNMP indication handler to package
  Resolves: #452930

* Tue Jun  3 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-8
- Add cimsub to package
  Resolves: #447823

* Thu May 15 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-7
- Rebuild

* Mon Feb 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-6
- Rebuild

* Mon Jan 21 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-5
- No snmp tests in Test RPM

* Thu Jan 10 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-4
- Fix Test RPM

* Wed Dec  5 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-3
- Rebuild

* Fri Nov 23 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-2
- Fix OpenPegasus SRPM fails to build Test RPM
  Resolves: #391961

* Mon Nov 19 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.7.0-1
- Update to upstream version 2.7.0
- Unhide some cmpi classes, package cmpi C++ headers
- Fix multiarch conflicts
  Resolves: #343311
- Add libcmpiCppImpl.so (symlink to libcmpiCppImpl.so.1)
  Resolves: #366871

* Tue Oct  9 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.6.1-2
- Fix files permissions
  Resolves: #200906

* Thu Aug 30 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.6.1-1
- Update to 2.6.1
- Fix wrong init script (#245339)

* Wed Mar 28 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2:2.6.0-2
- Update changelog
- Build with Open Pegasus' Makefiles, istall with Red Hats (Mark Hamzy)

* Mon Feb 26 2007 Mark Hamzy <hamzy@us.ibm.com> - 2:2.6.0-1
- Upgrade to upstream version 2.6.0

* Mon Dec  4 2006 Nalin Dahyabhai <nalin@redhat.com> - 2:2.5.2-3
- change requires: tog-pegasus to prereq: tog-pegasus so that the pegasus
  user and group will exist when we go to lay down files for tog-pegasus-devel
  (#218305)
- prereq the current version of openssl so that the right versions of
  libssl and libcrypto will be available in %%post (possible for #208949)

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 2:2.5.2-2
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Thu Jul 27 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.2-1.fc6
- Upgrade to upstream version 2.5.2
- fix bug 198185
- fix bug 200246

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:2.5.1-10.FC6.1
- rebuild

* Fri Jul 07 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.4.1-10
- More upstream 2.5.2_APPROVED bug fixes:
  o 4629: Pegasus freezes when it is unable to send out completely, the results of a request
  o 5073: Class Names on Reference, ReferenceNames, Assoc, AssocNames returned lower case
  o 5090: cimserver crash on a request after attempting to unload idle CMPI providers
  o 5180: OperationAggregate deleted in _enqueueResponse while member mutex held

* Fri Jun 09 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.1-8
- Fix bug 192754: remove multilib conflicts
- More upstream 2.5.2_APPROVED bug fixes:
  o 5119: memory leak in CMPI implementation
  o 5115: fix SetConfig_EnvVar comments

* Wed May 31 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.1-6
- Apply upstream patches for latest 2.5.2_APPROVED bugs:
  o 5046: cimprovider timeout needs to be increased
  o 5047: cimmof timeout needs to be increased
  o 5048: Invalid Pointer in CIMOperationRequestEncoder code
  o 5049: Unnecessary dependency on experimental headers
  o 5051: Improved handling of OOP indication provide module failures
  o 5053: reserveCapacity method may cause size overflow
  o 5059: XMLWriter does not escape '>' in strings
  o 5072: Potential race condition with OOP response chunks
  o 5083: CIMRequestMessage buildResponse() should be const
- Fix bug 193121: restore world read access to libraries

* Tue May 02 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.1-4
- fix bug 190432: %%exclude /usr/lib/debug from RPM
- fix upstream OpenPegasus '2.5.2_APPROVED' bugs, applying upstream patches:
  o 4955 : Bogus Description property for OperatingSystem provider
  o 4956 : reserveCapacity method may cause size overflow on invalid input
  o 4968 : CMPI provider up-calls cause failure with out-of-process
  o 4978 : snmpDeliverTrap_netsnmp::_createSession function is not thread safe
  o 4983 : Memory leak in OOP indication generation
  o 4984 : Forked process hangs in system call
  o 4986 : Adding automated test for snmpIndication Handler
  (  http://cvs.opengroup.org/bugzilla/show_bug.cgi?id=? )
- apply upstream update to 'pegasus-2.5.1-warnings.patch'

* Mon Apr 17 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.1-3
- Fix repupgrade (make it use correct paths)

* Fri Apr 14 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.1-2
- Apply patches for the two '2.5.2_APPROVED' upstream bugzillas
  4934(4943) and 4945 :
  (http://cvs.opengroup.org/bugzilla/buglist.cgi?bug_id=4943%%2C4945)
- Fix the PATH_MAX and MAXHOSTNAMELEN issues (again)

* Thu Apr 06 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5.1-1
- Upgrade to version 2.5.1 (including new upstream .spec file).

* Tue Mar  7 2006 Bill Nottingham <notting@redhat.com> - 2:2.5-9
- use an assigned uid/gid, do not loop over user ids looking for a free one

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2:2.5-6.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-6
- restore SSLv23_method SSL support now that bug 173399 is fixed
- rebuild for new gcc, glibc, glibc-kernheaders
- PAMBasicAuthenticatorUnix.cpp includes no longer include syslog.h: add
- /usr/bin/install now decides to fail if chown fails - set $INSTALL_USER, $INSTALL_GROUP

* Thu Dec 15 2005 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-5
- fix bug 175434 : deal with pegasus uid/gid already existing
  on first install

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 2:2.5-4.1
- rebuilt

* Wed Nov 16 2005 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-4
- fix bug 173401: SSL support broken by openssl-0.9.7g -> 0.9.8a upgrade

* Wed Nov 09 2005 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-3
- Rebuild for new openssl dependencies
- Enable CMPI support for sblim-cmpi-base with ENABLE_CQL=true

* Mon Oct 31 2005 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-2
- Add /usr/lib/cmpi alternate providerLibDir for sblim-cmpi-base Fedora Extras pkg
- Fix bug 171124: use numeric ids for pegasus user/group
- guidelines: do not remove pegasus user/group in %%postun.

* Fri Oct 14 2005 Tomas Mraz <tmraz@redhat.com>
- use include instead of pam_stack in pam config

* Fri Sep 30 2005 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-1
- Implemented new 'make install' target.
- Re-wrote tog-pegasus.spec file from scratch.
- Ported BZ 167986 authentication code and BZ 167164 + BZ 167165 fixes from RHEL-4

* Wed Sep 28 2005 Jason Vas Dias <jvdias@redhat.com> - 2:2.5-0
- Initial build.
