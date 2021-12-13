Vendor:         Microsoft Corporation
Distribution:   Mariner
# Globals and defines to control package behavior (configure these as desired)

## User and group to use for nonprivileged services
%global uname hacluster
%global gname haclient
%global hacluster_id 189

## Where to install Pacemaker documentation
%if 0%{?rhel}
%global pcmk_docdir %{_docdir}/%{name}-doc
%else
%global pcmk_docdir %{_docdir}/%{name}
%endif

## GitHub entity that distributes source (for ease of using a fork)
%global github_owner ClusterLabs

## Upstream pacemaker version, and its package version (specversion
## can be incremented to build packages reliably considered "newer"
## than previously built packages with the same pcmkversion)
%global pcmkversion 2.0.5
%global specversion 10

## Upstream commit (or git tag, such as "Pacemaker-" plus the
## {pcmkversion} macro for an official release) to use for this package
%global commit Pacemaker-2.0.5
## Since git v2.11, the extent of abbreviation is autoscaled by default
## (used to be constant of 7), so we need to convey it for non-tags, too.
%global commit_abbrev 9

# Define conditionals so that "rpmbuild --with <feature>" and
# "rpmbuild --without <feature>" can enable and disable specific features

## NOTE: skip --with stonithd

## Add option to enable support for storing sensitive information outside CIB
%bcond_with cibsecrets

## Add option to create binaries suitable for use with profiling tools
%bcond_with profiling

## Add option to create binaries with coverage analysis
%bcond_with coverage

## Add option to skip/enable generating documentation
## (the build tools aren't available everywhere)
%if 0%{?rhel}
  %bcond_with doc
%else
  %bcond_without doc
%endif

## Add option to prefix package version with "0."
## (so later "official" packages will be considered updates)
%bcond_with pre_release

## NOTE: skip --with upstart_job

## Add option to turn off hardening of libraries and daemon executables
%bcond_without hardening

## Add option to disable links for legacy daemon names
%bcond_without legacy_links


## Nagios source control identifiers
%global nagios_name nagios-agents-metadata
%global nagios_hash 105ab8a7b2c16b9a29cf1c1596b80136eeef332b
%global nagios_archive_github_url %{nagios_hash}#/%{nagios_name}-%{nagios_hash}.tar.gz

# Define globals for convenient use later

## Workaround to use parentheses in other globals
%global lparen (
%global rparen )

## Whether this is a tagged release (final or release candidate)
%define tag_release %(c=%{commit}; case ${c} in Pacemaker-*%{rparen} echo 1 ;;
                      *%{rparen} echo 0 ;; esac)

## Portion of export/dist tarball name after "pacemaker-", and release version
%if 0%{tag_release}
%define archive_version %{commit}
%define archive_github_url %{commit}#/%{name}-%{archive_version}.tar.gz
%else
%define archive_version %(c=%{commit}; echo ${c:0:%{commit_abbrev}})
%define archive_github_url %{archive_version}#/%{name}-%{archive_version}.tar.gz
%endif

%define bleeding 1

## Base GnuTLS cipher priorities (presumably only the initial, required keyword)
## overridable with "rpmbuild --define 'pcmk_gnutls_priorities PRIORITY-SPEC'"
%define gnutls_priorities %{?pcmk_gnutls_priorities}%{!?pcmk_gnutls_priorities:@SYSTEM}

# Python-related definitions

## Turn off auto-compilation of Python files outside Python specific paths,
## so there's no risk that unexpected "__python" macro gets picked to do the
## RPM-native byte-compiling there (only "{_datadir}/pacemaker/tests" affected)
## -- distro-dependent tricks or automake's fallback to be applied there
%if %{defined _python_bytecompile_extra}
%global _python_bytecompile_extra 0
%else
### the statement effectively means no RPM-native byte-compiling will occur at
### all, so distro-dependent tricks for Python-specific packages to be applied
%global __os_install_post %(echo '%{__os_install_post}' | {
                            sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g'; })
%endif

## Values that differ by Python major version
%global python_name python3
%global python_path %{?__python3}%{!?__python3:/usr/bin/python%{?python3_pkgversion}%{!?python3_pkgversion:3}}
%define python_site %{?python3_sitelib}%{!?python3_sitelib:%(
  %{python_path} -c 'from distutils.sysconfig import get_python_lib as gpl; print(gpl(1))' 2>/dev/null)}
%global python_min 3.2
# python_min still required?

# Keep sane profiling data if requested
%if %{with profiling}

## Disable -debuginfo package and stripping binaries/libraries
%define debug_package %{nil}

%endif


Name:          pacemaker
Summary:       Scalable High-Availability cluster resource manager
Version:       %{pcmkversion}
Release:       11%{?dist}
License:       GPLv2+ and LGPLv2+
Url:           https://www.clusterlabs.org

# Hint: use "spectool -s 0 pacemaker.spec" (rpmdevtools) to check the final URL
Source0:       https://codeload.github.com/%{github_owner}/%{name}/tar.gz/%{archive_github_url}
Source1:       https://codeload.github.com/%{github_owner}/%{nagios_name}/tar.gz/%{nagios_archive_github_url}
# ---

Requires:      resource-agents
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}
Requires:      %{name}-cluster-libs%{?_isa} = %{version}-%{release}
Requires:      %{name}-cli = %{version}-%{release}
%{?systemd_requires}

# Pacemaker requires a minimum Python functionality
Requires:      %{python_name} >= %{python_min}
BuildRequires: %{python_name}-devel >= %{python_min}

# Pacemaker requires a minimum libqb functionality
Requires:      libqb >= 0.13.0
BuildRequires: libqb-devel >= 0.13.0

# Basics required for the build (even if usually satisfied through other BRs)
BuildRequires: coreutils findutils grep sed

# Required for core functionality
BuildRequires: automake autoconf gcc libtool pkgconfig libtool-ltdl-devel
BuildRequires: pkgconfig(glib-2.0) >= 2.16
BuildRequires: libxml2-devel libxslt-devel libuuid-devel
BuildRequires: bzip2-devel

# Enables optional functionality
BuildRequires: ncurses-devel docbook-style-xsl
BuildRequires: help2man gnutls-devel pam-devel pkgconfig(dbus-1)

BuildRequires: pkgconfig(systemd)

Requires:      corosync >= 2.0.0
BuildRequires: corosync-devel >= 2.0.0
#XXX
#BuildRequires: pkgconfig(libcpg)
#BuildRequires: pkgconfig(libcfg)

## (note no avoiding effect when building through non-customized mock)
%if !%{bleeding}
%if %{with doc}
BuildRequires: asciidoc inkscape publican
%endif
%endif

# git-style patch application
#BuildRequires: git

Provides:      pcmk-cluster-manager = %{version}-%{release}
Provides:      pcmk-cluster-manager%{?_isa} = %{version}-%{release}

# Pacemaker uses the crypto/md5 module from gnulib
Provides:      bundled(gnulib)

%description
Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

It supports more than 16 node clusters with significant capabilities
for managing resources and dependencies.

It will run scripts at initialization, when machines go up or down,
when related resources fail and can be configured to periodically check
resource health.

Available rpmbuild rebuild options:
  --with(out) : cibsecrets coverage doc hardening pre_release profiling

%package cli
License:       GPLv2+ and LGPLv2+
Summary:       Command line tools for controlling Pacemaker clusters
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}
Recommends:    pcmk-cluster-manager = %{version}-%{release}
# For crm_report
Recommends:    tar
Recommends:    bzip2
Requires:      perl-TimeDate
Requires:      procps-ng
Requires:      psmisc
Requires(post):coreutils

%description cli
Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

The %{name}-cli package contains command line tools that can be used
to query and control the cluster from machines that may, or may not,
be part of the cluster.

%package libs
License:       GPLv2+ and LGPLv2+
Summary:       Core Pacemaker libraries
Requires(pre): shadow-utils
Requires:      %{name}-schemas = %{version}-%{release}
# sbd 1.4.0+ supports the libpe_status API for pe_working_set_t
Conflicts:     sbd < 1.4.0

%description libs
Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

The %{name}-libs package contains shared libraries needed for cluster
nodes and those just running the CLI tools.

%package cluster-libs
License:       GPLv2+ and LGPLv2+
Summary:       Cluster Libraries used by Pacemaker
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}

%description cluster-libs
Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

The %{name}-cluster-libs package contains cluster-aware shared
libraries needed for nodes that will form part of the cluster nodes.

%package remote
License:       GPLv2+ and LGPLv2+
Summary:       Pacemaker remote daemon for non-cluster nodes
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}
Requires:      %{name}-cli = %{version}-%{release}
Requires:      resource-agents
# -remote can be fully independent of systemd
%{?systemd_ordering}%{!?systemd_ordering:%{?systemd_requires}}
Provides:      pcmk-cluster-manager = %{version}-%{release}
Provides:      pcmk-cluster-manager%{?_isa} = %{version}-%{release}

%description remote
Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

The %{name}-remote package contains the Pacemaker Remote daemon
which is capable of extending pacemaker functionality to remote
nodes not running the full corosync/cluster stack.

%package libs-devel
License:       GPLv2+ and LGPLv2+
Summary:       Pacemaker development package
Requires:      %{name}-libs%{?_isa} = %{version}-%{release}
Requires:      %{name}-cluster-libs%{?_isa} = %{version}-%{release}
Requires:      libtool-ltdl-devel%{?_isa} libuuid-devel%{?_isa}
Requires:      libxml2-devel%{?_isa} libxslt-devel%{?_isa}
Requires:      bzip2-devel%{?_isa} glib2-devel%{?_isa}
Requires:      libqb-devel%{?_isa}
Requires:      corosync-devel%{?_isa} >= 2.0.0

%description libs-devel
Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

The %{name}-libs-devel package contains headers and shared libraries
for developing tools for Pacemaker.

%package       cts
License:       GPLv2+ and LGPLv2+
Summary:       Test framework for cluster-related technologies like Pacemaker
Requires:      %{python_path}
Requires:      %{python_name} >= %{python_min}
Requires:      %{name}-libs = %{version}-%{release}
Requires:      procps-ng
Requires:      psmisc
BuildArch:     noarch

Requires:      %{python_name}-systemd

%description   cts
Test framework for cluster-related technologies like Pacemaker

%package       doc
License:       CC-BY-SA-4.0
Summary:       Documentation for Pacemaker
BuildArch:     noarch
Conflicts:     %{name}-libs > %{version}-%{release}
Conflicts:     %{name}-libs < %{version}-%{release}

%description   doc
Documentation for Pacemaker.

Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

%package       schemas
License:       GPLv2+
Summary:       Schemas and upgrade stylesheets for Pacemaker
BuildArch:     noarch

%description   schemas
Schemas and upgrade stylesheets for Pacemaker

Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

%package       nagios-plugins-metadata
License:       GPLv3
Summary:       Pacemaker Nagios Metadata
BuildArch:     noarch
# NOTE below are the plugins this metadata uses.
# Requires:      nagios-plugins-http
# Requires:      nagios-plugins-ldap
# Requires:      nagios-plugins-mysql
# Requires:      nagios-plugins-pgsql
# Requires:      nagios-plugins-tcp
Requires:      pcmk-cluster-manager

%description  nagios-plugins-metadata
The metadata files required for Pacemaker to execute the nagios plugin
monitor resources.

%prep
%setup -q -a 1 -n %{name}-%{archive_version}

%build

export systemdsystemunitdir=%{?_unitdir}%{!?_unitdir:no}

%if %{with hardening}
# prefer distro-provided hardening flags in case they are defined
# through _hardening_{c,ld}flags macros, configure script will
# use its own defaults otherwise; if such hardenings are completely
# undesired, rpmbuild using "--without hardening"
# (or "--define '_without_hardening 1'")
export CFLAGS_HARDENED_EXE="%{?_hardening_cflags}"
export CFLAGS_HARDENED_LIB="%{?_hardening_cflags}"
export LDFLAGS_HARDENED_EXE="%{?_hardening_ldflags}"
export LDFLAGS_HARDENED_LIB="%{?_hardening_ldflags}"
%endif

./autogen.sh

# Rawhide glibc doesn't like ftime at all
export CPPFLAGS="-UPCMK_TIME_EMERGENCY_CGT $CPPFLAGS"

%{configure}                                                                    \
        PYTHON=%{python_path}                                                   \
        %{!?with_hardening:    --disable-hardening}                             \
        %{!?with_legacy_links: --disable-legacy-links}                          \
        %{?with_profiling:     --with-profiling}                                \
        %{?with_coverage:      --with-coverage}                                 \
        %{?with_cibsecrets:    --with-cibsecrets}                               \
        %{!?with_doc:          --with-brand=}                                   \
        %{?gnutls_priorities:  --with-gnutls-priorities="%{gnutls_priorities}"} \
        --disable-static                                                        \
        --with-initdir=%{_initrddir}                                            \
        --with-runstatedir=%{_rundir}                                           \
        --localstatedir=%{_var}                                                 \
        --with-version=%{version}-%{release}                                    \
        --with-bug-url=https://bugz.fedoraproject.org/%{name}                   \
        --with-nagios                                                           \
        --with-nagios-metadata-dir=%{_datadir}/pacemaker/nagios/plugins-metadata/  \
        --with-nagios-plugin-dir=%{_libdir}/nagios/plugins/

make %{_smp_mflags} V=1

%check
make %{_smp_mflags} check
{ cts/cts-scheduler --run load-stopped-loop \
  && cts/cts-cli \
  && touch .CHECKED
} 2>&1 | sed 's/[fF]ail/faiil/g'  # prevent false positives in rpmlint
[ -f .CHECKED ] && rm -f -- .CHECKED

%install
# skip automake-native Python byte-compilation, since RPM-native one (possibly
# distro-confined to Python-specific directories, which is currently the only
# relevant place, anyway) assures proper intrinsic alignment with wider system
# (such as with py_byte_compile macro, which is concurrent Fedora/EL specific)
make install \
  DESTDIR=%{buildroot} V=1 docdir=%{pcmk_docdir} \
  %{?_python_bytecompile_extra:%{?py_byte_compile:am__py_compile=true}}

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
install -m 644 daemons/pacemakerd/pacemaker.sysconfig ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/pacemaker
install -m 644 tools/crm_mon.sysconfig ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/crm_mon

mkdir -p %{buildroot}%{_datadir}/pacemaker/nagios/plugins-metadata
for file in $(find %{nagios_name}-%{nagios_hash}/metadata -type f); do
    install -m 644 $file %{buildroot}%{_datadir}/pacemaker/nagios/plugins-metadata
done


mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/rpm-state/%{name}

# These are not actually scripts
find %{buildroot} -name '*.xml' -type f -print0 | xargs -0 chmod a-x

# Don't package static libs
find %{buildroot} -name '*.a' -type f -print0 | xargs -0 rm -f
find %{buildroot} -name '*.la' -type f -print0 | xargs -0 rm -f

# Do not package these either
rm -f %{buildroot}/%{_sbindir}/fence_legacy
rm -f %{buildroot}/%{_mandir}/man8/fence_legacy.*

# For now, don't package the servicelog-related binaries built only for
# ppc64le when certain dependencies are installed. If they get more exercise by
# advanced users, we can reconsider.
rm -f %{buildroot}/%{_sbindir}/notifyServicelogEvent
rm -f %{buildroot}/%{_sbindir}/ipmiservicelogd

# Don't ship init scripts for systemd based platforms
rm -f %{buildroot}/%{_initrddir}/pacemaker
rm -f %{buildroot}/%{_initrddir}/pacemaker_remote

# Byte-compile Python sources where suitable and the distro procedures known
%if %{defined py_byte_compile} && %{defined python_path}
%{py_byte_compile %{python_path} %{buildroot}%{_datadir}/pacemaker/tests}
%if !%{defined _python_bytecompile_extra}
%{py_byte_compile %{python_path} %{buildroot}%{python_site}/cts}
%endif
%endif

%if %{with coverage}
GCOV_BASE=%{buildroot}/%{_var}/lib/pacemaker/gcov
mkdir -p $GCOV_BASE
find . -name '*.gcno' -type f | while read F ; do
        D=`dirname $F`
        mkdir -p ${GCOV_BASE}/$D
        cp $F ${GCOV_BASE}/$D
done
%endif

%post
%systemd_post pacemaker.service

%preun
%systemd_preun pacemaker.service

%postun
%systemd_postun_with_restart pacemaker.service

%pre remote
# Stop the service before anything is touched, and remember to restart
# it as one of the last actions (compared to using systemd_postun_with_restart,
# this avoids suicide when sbd is in use)
systemctl --quiet is-active pacemaker_remote
if [ $? -eq 0 ] ; then
    mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
    touch %{_localstatedir}/lib/rpm-state/%{name}/restart_pacemaker_remote
    systemctl stop pacemaker_remote >/dev/null 2>&1
else
    rm -f %{_localstatedir}/lib/rpm-state/%{name}/restart_pacemaker_remote
fi

%post remote
%systemd_post pacemaker_remote.service

%preun remote
%systemd_preun pacemaker_remote.service

%postun remote
# This next line is a no-op, because we stopped the service earlier, but
# we leave it here because it allows us to revert to the standard behavior
# in the future if desired
%systemd_postun_with_restart pacemaker_remote.service
# Explicitly take care of removing the flag-file(s) upon final removal
if [ "$1" -eq 0 ] ; then
    rm -f %{_localstatedir}/lib/rpm-state/%{name}/restart_pacemaker_remote
fi

%posttrans remote
if [ -e %{_localstatedir}/lib/rpm-state/%{name}/restart_pacemaker_remote ] ; then
    systemctl start pacemaker_remote >/dev/null 2>&1
    rm -f %{_localstatedir}/lib/rpm-state/%{name}/restart_pacemaker_remote
fi

%post cli
%systemd_post crm_mon.service
if [ "$1" -eq 2 ]; then
    # Package upgrade, not initial install:
    # Move any pre-2.0 logs to new location to ensure they get rotated
    { mv -fbS.rpmsave %{_var}/log/pacemaker.log* %{_var}/log/pacemaker \
      || mv -f %{_var}/log/pacemaker.log* %{_var}/log/pacemaker
    } >/dev/null 2>/dev/null || :
fi

%preun cli
%systemd_preun crm_mon.service

%postun cli
%systemd_postun_with_restart crm_mon.service

%pre libs
# XXX keep an eye on https://fedoraproject.org/wiki/Changes/SystemdSysusers
#     reopened recently:
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/AETGESYR4IEQJMA6SKL7OERSDZFWFNEU/
getent group %{gname} >/dev/null || groupadd -r %{gname} -g %{hacluster_id}
getent passwd %{uname} >/dev/null || useradd -r -g %{gname} -u %{hacluster_id} -s /usr/sbin/nologin -c "cluster user" %{uname}
exit 0

%ldconfig_scriptlets libs
%ldconfig_scriptlets cluster-libs

%files
###########################################################
%config(noreplace) %{_sysconfdir}/sysconfig/pacemaker
%{_sbindir}/pacemakerd

%{_unitdir}/pacemaker.service

%exclude %{_datadir}/pacemaker/nagios/plugins-metadata/*

%exclude %{_libexecdir}/pacemaker/cts-log-watcher
%exclude %{_libexecdir}/pacemaker/cts-support
%exclude %{_sbindir}/pacemaker-remoted
%if %{with legacy_links}
%exclude %{_sbindir}/pacemaker_remoted
%endif
%{_libexecdir}/pacemaker/*

%{_sbindir}/crm_attribute
%{_sbindir}/crm_master

%doc %{_mandir}/man7/pacemaker-controld.*
%doc %{_mandir}/man7/pacemaker-schedulerd.*
%doc %{_mandir}/man7/pacemaker-fenced.*
%doc %{_mandir}/man7/ocf_pacemaker_controld.*
%doc %{_mandir}/man7/ocf_pacemaker_remote.*
%doc %{_mandir}/man8/crm_attribute.*
%doc %{_mandir}/man8/crm_master.*
%doc %{_mandir}/man8/pacemakerd.*

%doc %{_datadir}/pacemaker/alerts

%license licenses/GPLv2
%doc COPYING
%doc ChangeLog

%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/cib
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/pengine
/usr/lib/ocf/resource.d/pacemaker/controld
/usr/lib/ocf/resource.d/pacemaker/remote

%files cli
%dir %attr (750, root, %{gname}) %{_sysconfdir}/pacemaker
%config(noreplace) %{_sysconfdir}/logrotate.d/pacemaker
%config(noreplace) %{_sysconfdir}/sysconfig/crm_mon

%{_unitdir}/crm_mon.service

%{_sbindir}/attrd_updater
%{_sbindir}/cibadmin
%if %{with cibsecrets}
%{_sbindir}/cibsecret
%endif
%{_sbindir}/crm_diff
%{_sbindir}/crm_error
%{_sbindir}/crm_failcount
%{_sbindir}/crm_mon
%{_sbindir}/crm_node
%{_sbindir}/crm_resource
%{_sbindir}/crm_rule
%{_sbindir}/crm_standby
%{_sbindir}/crm_verify
%{_sbindir}/crmadmin
%{_sbindir}/iso8601
%{_sbindir}/crm_shadow
%{_sbindir}/crm_simulate
%{_sbindir}/crm_report
%{_sbindir}/crm_ticket
%{_sbindir}/stonith_admin
# "dirname" is owned by -schemas, which is a prerequisite
%{_datadir}/pacemaker/report.collector
%{_datadir}/pacemaker/report.common
# XXX "dirname" is not owned by any prerequisite
%{_datadir}/snmp/mibs/PCMK-MIB.txt

%exclude /usr/lib/ocf/resource.d/pacemaker/controld
%exclude /usr/lib/ocf/resource.d/pacemaker/o2cb
%exclude /usr/lib/ocf/resource.d/pacemaker/remote

%dir /usr/lib/ocf
%dir /usr/lib/ocf/resource.d
/usr/lib/ocf/resource.d/pacemaker

%doc %{_mandir}/man7/*
%exclude %{_mandir}/man7/pacemaker-controld.*
%exclude %{_mandir}/man7/pacemaker-schedulerd.*
%exclude %{_mandir}/man7/pacemaker-fenced.*
%exclude %{_mandir}/man7/ocf_pacemaker_controld.*
%exclude %{_mandir}/man7/ocf_pacemaker_o2cb.*
%exclude %{_mandir}/man7/ocf_pacemaker_remote.*
%doc %{_mandir}/man8/*
%exclude %{_mandir}/man8/crm_attribute.*
%exclude %{_mandir}/man8/crm_master.*
%exclude %{_mandir}/man8/fence_legacy.*
%exclude %{_mandir}/man8/pacemakerd.*
%exclude %{_mandir}/man8/pacemaker-remoted.*

%license licenses/GPLv2
%doc COPYING
%doc ChangeLog

%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/blackbox
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/cores
%dir %attr (770, %{uname}, %{gname}) %{_var}/log/pacemaker
%dir %attr (770, %{uname}, %{gname}) %{_var}/log/pacemaker/bundles

%files libs
%{_libdir}/libcib.so.*
%{_libdir}/liblrmd.so.*
%{_libdir}/libcrmservice.so.*
%{_libdir}/libcrmcommon.so.*
%{_libdir}/libpe_status.so.*
%{_libdir}/libpe_rules.so.*
%{_libdir}/libpacemaker.so.*
%{_libdir}/libstonithd.so.*
%license licenses/LGPLv2.1
%doc COPYING
%doc ChangeLog

%files cluster-libs
%{_libdir}/libcrmcluster.so.*
%license licenses/LGPLv2.1
%doc COPYING
%doc ChangeLog

%files remote
%config(noreplace) %{_sysconfdir}/sysconfig/pacemaker
# state directory is shared between the subpackets
# let rpm take care of removing it once it isn't
# referenced anymore and empty
%ghost %dir %{_localstatedir}/lib/rpm-state/%{name}
%{_unitdir}/pacemaker_remote.service

%{_sbindir}/pacemaker-remoted
%if %{with legacy_links}
%{_sbindir}/pacemaker_remoted
%endif
%{_mandir}/man8/pacemaker-remoted.*
%license licenses/GPLv2
%doc COPYING
%doc ChangeLog

%files doc
%doc %{pcmk_docdir}
%license licenses/CC-BY-SA-4.0

%files cts
%{python_site}/cts
%{_datadir}/pacemaker/tests

%{_libexecdir}/pacemaker/cts-log-watcher
%{_libexecdir}/pacemaker/cts-support

%license licenses/GPLv2
%doc COPYING
%doc ChangeLog

%files libs-devel
%{_includedir}/pacemaker
%{_libdir}/*.so
%if %{with coverage}
%{_var}/lib/pacemaker/gcov
%endif
%{_libdir}/pkgconfig/*.pc
%license licenses/LGPLv2.1
%doc COPYING
%doc ChangeLog

%files schemas
%license licenses/GPLv2
%dir %{_datadir}/pacemaker
%{_datadir}/pacemaker/*.rng
%{_datadir}/pacemaker/*.xsl
%{_datadir}/pacemaker/api
%{_datadir}/pkgconfig/pacemaker-schemas.pc

%files nagios-plugins-metadata
%dir %{_datadir}/pacemaker/nagios
%dir %{_datadir}/pacemaker/nagios/plugins-metadata
%attr(0644,root,root) %{_datadir}/pacemaker/nagios/plugins-metadata/*
%license %{nagios_name}-%{nagios_hash}/COPYING

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.5-11
- Switching to using full number for the 'Release' tag.

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.5-10.2
- Making binaries paths compatible with CBL-Mariner's paths.

* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 2.0.5-10.1
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Turn on bleeding to avoid inkscape dependency

* Mon Dec 7 2020 Klaus Wenninger <kwenning@redhat.com> - 2.0.5-10
- Conflicts of doc package introduced to fix upgrade/downgrade
  issues needs to be independent from arch

* Fri Dec 4 2020 Klaus Wenninger <kwenning@redhat.com> - 2.0.5-9
- Make doc-package conflict with wrong version of libs
  to fix upgrade/downgrade issues

* Fri Dec 4 2020 Klaus Wenninger <kwenning@redhat.com> - 2.0.5-8
- Update for new upstream release tarball: Pacemaker-2.0.5
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.5

* Wed Nov 18 2020 Klaus Wenninger <kwenning@redhat.com> - 2.0.5-0.7.rc3
- a little more syncing with upstream spec-file

* Tue Nov 17 2020 Klaus Wenninger <kwenning@redhat.com> - 2.0.5-0.6.rc3
- Update for new upstream tarball for release candidate: Pacemaker-2.0.5-rc3
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.5-rc3
- Corosync in Fedora now provides corosync-devel as well in isa-flavor

* Sun Nov 1 2020 Klaus Wenninger <kwenning@redhat.com> - 2.0.5-0.5.rc2
- Update for new upstream tarball for release candidate: Pacemaker-2.0.5-rc2,
  includes fix for CVE-2020-25654
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.5-rc2
- Remove dependencies to nagios-plugins from metadata-package
- some sync with structure of upstream spec-file
- removed some legacy conditionals
- added with-cibsecrets
- enable some basic gating-tests
- remove building documentation using publican from ELN
- rename doc-dir for ELN

* Tue Jun 16 2020 Chris Lumens <clumens@redhat.com> - 2.0.4-1
- Update for new upstream tarball: Pacemaker-2.0.4
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.4

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 26 2019 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.3-1
- Update for new upstream tarball: Pacemaker-2.0.3,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.3
  (functionally identical to 2.0.3-rc3, new build mostly to fix a memory
  leak & allow for easy glibc ~2.31+ friendly switch away from ftime(3))
- Fix unability to build with Inkscape 1.0 beta (and possibly beyond)

* Thu Nov 14 2019 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.3-0.1.rc3
- Update for new upstream tarball for release candidate: Pacemaker-2.0.3-rc3,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.3-rc3
- Fix failure to build due to using obsolete ftime(3)

* Wed Nov 06 2019 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.3-0.1.rc2
- Update for new upstream tarball for release candidate: Pacemaker-2.0.3-rc2,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.3-rc2

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.2-1.3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.2-1.2
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 07 2019 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.2-1
- Update for new upstream tarball: Pacemaker-2.0.2,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.2
  (functionally identical to 2.0.2-rc3, new build mostly to match expectations)

* Fri May 31 2019 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.2-0.1.rc3
- Update for new upstream tarball for release candidate: Pacemaker-2.0.2-rc3,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.2-rc3
- Adapt spec file more akin to upstream version including:
  . /usr/share/pacemaker now owned by -schemas, its "api" subdirectory
    is not carried redundantly in -cli anymore (f05eb7eec)

* Tue May 28 2019 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.2-0.1.rc2
- Update for new upstream tarball for release candidate: Pacemaker-2.0.2-rc2,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.2-rc2

* Thu Apr 25 2019 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.2-0.1.rc1
- Update for new upstream tarball for release candidate: Pacemaker-2.0.2-rc1,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.2-rc1
- Customize (as allowed now) exhibited downstream-specific bug reporting URL
- Adapt spec file more akin to upstream version including:
  . sbd ABI compatible version enforcement (37ad2bea1)

* Wed Apr 17 2019 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.1-2
- Apply fixes for security issues:
  . CVE-2019-3885 (use-after-free with potential information disclosure)
  . CVE-2018-16877 (insufficient local IPC client-server authentication)
  . CVE-2018-16878 (insufficient verification inflicted preference of
                    uncontrolled processes)

* Tue Mar 05 2019 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.1-1
- Update for new upstream tarball: Pacemaker-2.0.1,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.1

* Thu Feb 28 2019 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.1-0.4.rc5
- Update for new upstream tarball for release candidate: Pacemaker-2.0.1-rc5,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.1-rc5
- Reflect that cts-scheduler tests are fully compatible with whatever recent
  glib version that gets to be used in run-time (incl. buildroot tests) again

* Mon Feb 04 2019 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.1-0.3.rc4
- Update for new upstream tarball for release candidate: Pacemaker-2.0.1-rc4,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.1-rc4
- Conditionally disable "hash affected tests" in cts-scheduler (-cts package),
  since it is unlikely glib v2.59.0+ present in the buildroot will be
  artificially downgraded post-deployment

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-0.2.rc3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.1-0.2.rc3
- Fix buildability with GCC 9 (PR #1681)
- Apply minor crm_mon XML output fix (PR #1678)

* Sun Jan 20 2019 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.1-0.1.rc3
- Update for new upstream tarball for release candidate: Pacemaker-2.0.1-rc3,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.1-rc3
- Adapt spec file more akin to upstream version including:
  . split a dedicated, noarch -schemas package (c6a87bd86)
  . make static dependencies on inner libraries arch-specific (14bfff68e)
  . weak co-dependence of -cli with -remote & pacemaker proper (73e2c94a3)
  . declare bundled gnulib (d57aa84c1)
- Move stonith_admin to -cli where it belongs, since it doesn't require
  -cluster-libs (considered by upstream)
- Apply patches to restore basic buildability (still without much run-time
  reproducibility guarantees compared to what's been customary prior to glib
  v2.59.0+ that may now get run-time linked upon its fresh installation/update,
  but this applies also to whatever older version of pacemaker, and wasn't
  discovered until now; cf. https://github.com/ClusterLabs/pacemaker/pull/1677)

* Thu Aug 23 2018 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.0-4
- Sanitize/generalize approach to Python byte-compilation, so that also
  out-of-Python-path *.py files (%%{_datadir}/pacemaker/tests/cts/CTSlab.py
  in particular) get the expected treatment now

* Wed Aug 15 2018 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.0-3
- Fix Python 3.7 incompatibility (otherwise missed in bytecompilation phase,
  see rhbz#1616219)

* Thu Aug 09 2018 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.0-2
- Include fix for "cibadmin --upgrade" related issues (rhbz#1611631)
- Adapt spec file more akin to upstream version including:
  . assuredly skip servicelog-related binaries even when build-time
    prerequisites are present on suitable systems (9f24448d8)

* Mon Jul 09 2018 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.0-1
- Update for new upstream tarball: Pacemaker-2.0.0,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.0

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-0.1.rc6.1
- Rebuilt for Python 3.7

* Thu Jun 28 2018 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.0-0.1.rc6
- Update for new upstream tarball for release candidate: Pacemaker-2.0.0-rc6,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.0-rc6
- Adapt spec file more akin to upstream version including:
  . new procps-ng and psmisc dependencies with -cli and -cts, for e.g.
    "ps/sysctl/uptime" and "killall" invocations, respectively (a4ad8183a)
  . move crm_node to -cli (a94a1ed58)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-0.1.rc5.1
- Rebuilt for Python 3.7

* Fri Jun 01 2018 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.0-0.1.rc5
- Update for new upstream tarball for release candidate: Pacemaker-2.0.0-rc5,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.0-rc5
- Adapt spec file more akin to upstream version including:
  . new coreutils dependency for "post" scriptlet of -cli,
    for "mv" invocation (c2b16165d)

* Wed May 16 2018 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.0-0.1.rc4
- Update for new upstream tarball for release candidate: Pacemaker-2.0.0-rc4,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.0-rc4
  . as a special note, previous release candidate, rc3, had rolling upgrades
    broken, and if that is required, that particular release shall be
    skipped in the upgrade path altogether
- Adapt spec file more akin to upstream version including:
  . as part of the update process, possibly move old log files as implicitly
    used prior to 2.0 so there's a (limited) continuity with the new implicit
    location, preventing clutter and confusion (ce2e74c99, c2b16165d)
  . move cts-exec-helper from -cli under main package (a2dc2a67e)
  . -cts backed with new helpers and, tangentially, dummy systemd service
    file transiently generated on-demand again (fa2d43445, d52b001b1)

* Wed May 02 2018 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.0-0.1.rc3
- Update for new upstream tarball for release candidate: Pacemaker-2.0.0-rc3,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.0-rc3
  . IMPORTANT: this release candidate, rc3, has rolling upgrades broken,
               and if that is required, this particular release shall be
               skipped in the upgrade path altogether
- Adapt spec file more akin to upstream version including:
  . new --without legacy_links conditional (c8a7e5225)
  . reflect name change of the auxiliary daemons
    (e4f4a0d64, db5536e40, e2fdc2bac + 9ecbfea1c, 038c465e2 + ed8ce4055a)
  . new dummy systemd service for -cts (bf0a22812)
  . honor system-wide crypto policies once for all, via package-build-time
    configurable "pcmk_gnutls_priorities" defaulting to @SYSTEM as prescribed
    in https://fedoraproject.org/wiki/Packaging:CryptoPolicies
    (based on b3dfce1d3)
- Adapt spec file akin to current packaging guidelines including:
  . make -nagios-plugins-metadata package noarch

* Mon Apr 09 2018 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.0-0.1.rc2
- Update for new upstream tarball for release candidate: Pacemaker-2.0.0-rc2,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.0-rc2
- Adapt spec file more akin to upstream version including:
  . out-of-tree change from 1.1.18-2 build got subsumed (508ad52e7)
  . %%{_sysconfdir}/pacemaker path got properly owned
    (-cli package; f6e3ab98d)
  . -libs package started to properly declare Requires(pre): shadow-utils
    (293fcc1e8 + b3d49d210)
  . some build conditionals and dependencies dropped for no longer
    (snmp, esmtp; f24bdc6f2 and 1f7374884, respectively) or never
    being relevant (~bison, byacc, flex; 61aef8af4)
  . some dependencies were constrained with new or higher lower bounds:
    corosync needs to be of version 2+ unconditionally (ccd58fe29),
    ditto some others components (~GLib, 1ac2e7cbb), plus both 2 and 3
    versions of Python are now (comprehensively for the auxiliary
    functionality where used) supported upstream with the latter being
    a better fit (453355f8f)
  . package descriptions got to reflect the drop of legacy low-level
    cluster infrastructures (55ab749bf)
- Adapt spec file akin to current packaging guidelines including:
  . drop some redundant/futile expressions (defattr, "-n %%{name}-libs"
    instead of plain "libs", "timezone hack"), add some notes for future
  . make -cts and -doc packages noarch (former enabled with 088a5e7d4)
  . simplify "systemd_requires" macro invocation, and relax it to
    "systemd_ordering" for -remote package where possible so as not
    to drag systemd into a lightweight system setup (e.g. container)
    needlessly
  . adjust, in a compatible way, common ldconfig invocation with
    post{,un} scriptlets
    (https://fedoraproject.org/wiki/Changes/Removing_ldconfig_scriptlets)
  . drop some more unuseful conditionals (upstart_job)
- Apply some regression fixes on top as patches (PR #1457, #1459)

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.1.18-2.2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.18-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 16 2017 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.18-2
- Make sure neither of pacemaker{,_remoted} is process-limited

* Wed Nov 15 2017 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.18-1
- Update for new upstream tarball: Pacemaker-1.1.18,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.18
- Make -libs-devel package dependencies arch-qualified
  (-cts hasn't been switched at this time, pending further cleanup)

* Fri Nov 03 2017 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.18-0.1.rc4
- Update for new upstream tarball for release candidate: Pacemaker-1.1.18-rc4,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.18-rc4

* Thu Oct 26 2017 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.18-0.1.rc3
- Update for new upstream tarball for release candidate: Pacemaker-1.1.18-rc3,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.18-rc3

* Mon Oct 16 2017 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.18-0.1.rc2
- Update for new upstream tarball for release candidate: Pacemaker-1.1.18-rc2,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.18-rc2
- Fix check scriptlet so as to work properly also with rpm<4.14 (not strictly
  required since: https://github.com/rpm-software-management/rpm/pull/249,
  but pragmatically follow the upstream)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.17-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.17-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.17-1
- Update for new upstream tarball: Pacemaker-1.1.17,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.17

* Thu Jun 22 2017 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.17-0.1.rc4
- Update for new upstream tarball for release candidate: Pacemaker-1.1.17-rc4,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.17-rc4
- Add an imposed lower bound for glib2 BuildRequires

* Thu Jun 01 2017 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.17-0.1.rc3
- Update for new upstream tarball for release candidate: Pacemaker-1.1.17-rc3,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.17-rc3

* Wed May 24 2017 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.17-0.1.rc2
- Update for new upstream tarball for release candidate: Pacemaker-1.1.17-rc2,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.17-rc2

* Tue May 09 2017 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.17-0.1.rc1
- Update for new upstream tarball for release candidate: Pacemaker-1.1.17-rc1,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.17-rc1

* Mon Feb 06 2017 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.16-2.a39ea6491.git
- Update for (slightly stabilized) snapshot beyond Pacemaker-1.1.16
  (commit a39ea6491), including:
  . prevent FTBFS with new GCC 7 (a7476dd96)
- Adapt spec file more akin to upstream version including:
  . better pre-release vs. tags logic (4581d4366)

* Fri Dec 02 2016 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.16-1
- Update for new upstream tarball: Pacemaker-1.1.16,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.16
- Adapt spec file more akin to upstream version including:
  . clarify licensing, especially for -doc (f01f734)
  . fix pacemaker-remote upgrade (779e0e3)
  . require python >= 2.6 (31ef7f0)
  . older libqb is sufficient (based on 30fe1ce)
  . remove openssl-devel and libselinux-devel as BRs (2e05c17)
  . make systemd BR pkgconfig-driven (6285924)
  . defines instead of some globals + error suppression (625d427)
- Rectify -nagios-plugins-metadata declared license and install
  also respective license text

* Thu Nov 03 2016 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.15-3
- Apply fix for CVE-2016-7035 (improper IPC guarding)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.15-2.1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jul 07 2016 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.15-2
- Stop building with -fstack-protector-all using the upstream patches
  overhauling toolchain hardening (Fedora natively uses
  -fstack-protector-strong so this effectively relaxed stack protection
  is the only effect as hardened flags are already used by default:
  https://fedoraproject.org/wiki/Changes/Harden_All_Packages)

* Wed Jun 22 2016 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.15-1
- Update for new upstream tarball: Pacemaker-1.1.15,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.15
- Adapt spec file more akin to upstream version:
  . move xml schema files + PCMK-MIB.txt (81ef956), logrotate configuration
    file (ce576cf; drop it from -remote package as well), attrd_updater
    (aff80ae), the normal resource agents (1fc7287), and common directories
    under /var/lib/pacemaker (3492794) from main package under -cli
  . simplify docdir build parameter passing and drop as of now
    redundant chmod invocations (e91769e)

* Fri May 27 2016 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.15-0.1.rc3
- Update for new upstream tarball for release candidate: Pacemaker-1.1.15-rc3,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.15-rc3
- Drop fence_pcmk (incl. man page) from the package (no use where no CMAN)
- Drop license macro emulation for cases when not supported natively
  (several recent Fedora releases do not need that)

* Mon May 16 2016 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.15-0.1.rc2
- Update for new upstream tarball for release candidate: Pacemaker-1.1.15-rc2,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.15-rc2

* Tue Apr 26 2016 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.15-0.1.rc1
- Update for new upstream tarball for release candidate: Pacemaker-1.1.15-rc1,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.15-rc1
- Adapt spec file more akin to upstream version (also to reflect recent
  changes like ability to built explicitly without Publican-based docs)

* Thu Mar 31 2016 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.14-2.5a6cdd1.git
- Update for currently stabilized snapshot beyond Pacemaker-1.1.14
  (commit 5a6cdd1), but restore old-style notifications to the state at
  Pacemaker-1.1.14 point release (disabled)
- Definitely get rid of Corosync v1 (Flatiron) hypothetical support
- Remove some of the spec file cruft, not required for years
  (BuildRoot, AutoReqProv, "clean" scriptlet, etc.) and adapt the file
  per https://github.com/ClusterLabs/pacemaker/pull/965

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.14-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.14-1
- Update for new upstream tarball: Pacemaker-1.1.14,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-1.1.14
- Disable Fedora crypto policies conformance patch for now (rhbz#1179335)
- Better align specfile with the upstream version (also fix issue with
  crm_mon sysconfig file not being installed)
- Further specfile modifications:
  - drop unused gcc-c++ and repeatedly mentioned pkgconfig packages
    from BuildRequires
  - refer to python_sitearch macro first, if defined
  - tolerate license macro not being defined (e.g., for EPEL rebuilds)
- Prevent console mode not available in crm_mon due to curses library test
  fragility of configure script in hardened build environment (rhbz#1297985)

* Tue Oct 20 2015 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.13-4
- Adapt to follow Fedora crypto policies (rhbz#1179335)

* Wed Oct 14 2015 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 1.1.13-3
- Update to Pacemaker-1.1.13 post-release + patches (sync)
- Add nagios-plugins-metadata subpackage enabling support of selected
  Nagios plugins as resources recognized by Pacemaker
- Several specfile improvements: drop irrelevant stuff, rehash the
  included/excluded files + dependencies, add check scriptlet,
  reflect current packaging practice, do minor cleanups
  (mostly adopted from another spec)

* Thu Aug 20 2015 Andrew Beekhof <abeekhof@redhat.com> - 1.1.13-2
- Update for new upstream tarball: Pacemaker-1.1.13
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for full details

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.12-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Nov 05 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-2
- Address incorrect use of the dbus API for interacting with systemd

* Tue Oct 28 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-1
- Update for new upstream tarball: Pacemaker-1.1.12+ (a9c8177)
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for full details

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.11-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.11-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 18 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.11-1
- Update for new upstream tarball: Pacemaker-1.1.11 (9d39a6b)
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for full details

* Thu Jun 20 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.9-3
- Update to upstream 7d8acec
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for full details

  + Feature: Turn off auto-respawning of systemd services when the cluster starts them
  + Fix: crmd: Ensure operations for cleaned up resources don't block recovery
  + Fix: logging: If SIGTRAP is sent before tracing is turned on, turn it on instead of crashing

* Mon Jun 17 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.9-2
- Update for new upstream tarball: 781a388
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for full details

* Wed May 12 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.2-1
- Update the tarball from the upstream 1.1.2 release
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for full details

* Tue Jul 14 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.4-1
- Initial checkin
