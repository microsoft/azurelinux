# User-configurable globals and defines to control package behavior
# (these should not test {with X} values, which are declared later)

## User and group to use for nonprivileged services
%global uname hacluster
%global gname haclient

## Where to install Pacemaker documentation
%global pcmk_docdir %{_docdir}/%{name}

## Where bug reports should be submitted
## Leave bug_url undefined to use ClusterLabs default, others define it here

## What to use as the OCF resource agent root directory
%global ocf_root %{_prefix}/lib/ocf

## Add option to enable support for stonith/external fencing agents
%bcond_with stonithd

## Add option for whether to support storing sensitive information outside CIB
%bcond_without cibsecrets

## Add option to enable Native Language Support (experimental)
%bcond_with nls

## Add option to create binaries suitable for use with profiling tools
%bcond_with profiling

## Allow deprecated option to skip (or enable, on RHEL) documentation
%bcond_with doc

## Add option to default to start-up synchronization with SBD.
##
## If enabled, SBD *MUST* be built to default similarly, otherwise data
## corruption could occur. Building both Pacemaker and SBD to default
## to synchronization improves safety, without requiring higher-level tools
## to be aware of the setting or requiring users to modify configurations
## after upgrading to versions that support synchronization.
%bcond_without sbd_sync

## NOTE: skip --with upstart_job

## Add option to turn off hardening of libraries and daemon executables
%bcond_with hardening

## Add option to enable (or disable) links for legacy daemon names
%bcond_with legacy_links

# Define globals for convenient use later

## Base GnuTLS cipher priorities (presumably only the initial, required keyword)
## overridable with "rpmbuild --define 'pcmk_gnutls_priorities PRIORITY-SPEC'"
%define gnutls_priorities %{?pcmk_gnutls_priorities}%{!?pcmk_gnutls_priorities:@SYSTEM}

## Different distros name certain packages differently
## (note: corosync libraries also differ, but all provide corosync-devel)
%global pkgname_libtool_devel libtool-ltdl-devel
%global pkgname_libtool_devel_arch libtool-ltdl-devel%{?_isa}
%global pkgname_bzip2_devel bzip2-devel
%global pkgname_docbook_xsl docbook-style-xsl
%global pkgname_gettext gettext-devel
%global pkgname_gnutls_devel gnutls-devel
%global pkgname_shadow_utils shadow-utils
%global pkgname_procps procps-ng
%global pkgname_glue_libs cluster-glue-libs
%global pkgname_pcmk_libs %{name}-libs
%global hacluster_id 189

## Distro-specific configuration choices

### Use 2.0-style output when other distro packages don't support current output
%global compat20 --enable-compat-2.0

### Default concurrent-fencing to true when distro prefers that
%global concurrent_fencing --with-concurrent-fencing-default=true

### Default resource-stickiness to 1 when distro prefers that
%global resource_stickiness --with-resource-stickiness-default=1

## Prefer Python 3 definitions explicitly, in case 2 is also available
%global python_name python3
%global python_path %{__python3}
%define python_site %{?python3_sitelib}%{!?python3_sitelib:%(
  %{python_path} -c 'from distutils.sysconfig import get_python_lib as gpl; print(gpl(1))' 2>/dev/null)}

# Keep sane profiling data if requested
%if %{with profiling}
## Disable -debuginfo package and stripping binaries/libraries
%define debug_package %{nil}
%endif

Summary:        Scalable High-Availability cluster resource manager
Name:           pacemaker
Version:        2.1.5
Release:        5%{?dist}
License:        GPLv2+ and LGPLv2+
Url:            https://www.clusterlabs.org/
Source0:        https://github.com/ClusterLabs/pacemaker/archive/refs/tags/Pacemaker-2.1.5.tar.gz#/%{name}-%{version}.tar.gz
Requires:       resource-agents
Requires:       %{pkgname_pcmk_libs}%{?_isa} = %{version}-%{release}
Requires:       %{name}-cluster-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-cli = %{version}-%{release}
%{?systemd_requires}
Requires:       %{python_path}
BuildRequires:  %{python_name}-devel
# Pacemaker requires a minimum libqb functionality
Requires:       libqb >= 0.17.0
#BuildRequires: libqb-devel >= 0.17.0
BuildRequires:  pkgconfig(libqb) >= 0.17.0
# Required basic build tools
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  grep
BuildRequires:  libtool
%if %{defined pkgname_libtool_devel}
BuildRequires:  %{?pkgname_libtool_devel}
%endif
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  sed
# Required for core functionality
BuildRequires:  pkgconfig(glib-2.0) >= 2.42
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  libuuid-devel
BuildRequires:  %{pkgname_bzip2_devel}
# Enables optional functionality
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  %{pkgname_docbook_xsl}
BuildRequires:  %{pkgname_gnutls_devel}
BuildRequires:  help2man
BuildRequires:  ncurses-devel
BuildRequires:  pam-devel
BuildRequires:  %{pkgname_gettext} >= 0.18
# Required for "make check"
%if %{with_check}
BuildRequires:  libcmocka-devel
%endif
BuildRequires:  corosync-devel >= 2.0.0
%if %{with stonithd}
BuildRequires:  %{pkgname_glue_libs}-devel
%endif
%if %{with doc}
BuildRequires:  asciidoc
BuildRequires:  inkscape
BuildRequires:  %{python_name}-sphinx
%endif
BuildRequires:  systemd
Requires:       corosync >= 2.0.0
# Booth requires this
Provides:       pacemaker-ticket-support = 2.0
Provides:       pcmk-cluster-manager = %{version}-%{release}
Provides:       pcmk-cluster-manager%{?_isa} = %{version}-%{release}

%description
Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

It supports more than 16 node clusters with significant capabilities
for managing resources and dependencies.

It will run scripts at initialization, when machines go up or down,
when related resources fail and can be configured to periodically check
resource health.

Available rpmbuild rebuild options:
  --with(out) : cibsecrets hardening nls pre_release profiling stonithd

%package cli
License:        GPLv2+ and LGPLv2+
Summary:        Command line tools for controlling Pacemaker clusters
Requires:       %{pkgname_pcmk_libs}%{?_isa} = %{version}-%{release}
Recommends:     pcmk-cluster-manager = %{version}-%{release}
# For crm_report
Recommends:     tar
Recommends:     bzip2
Requires:       perl-TimeDate
Requires:       %{pkgname_procps}
Requires:       psmisc
Requires:       %{python_name}-psutil
Requires(post): coreutils

%description cli
Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

The %{name}-cli package contains command line tools that can be used
to query and control the cluster from machines that may, or may not,
be part of the cluster.

%package -n %{pkgname_pcmk_libs}
License:        GPLv2+ and LGPLv2+
Summary:        Core Pacemaker libraries
Requires(pre):  %{pkgname_shadow_utils}
Requires:       %{name}-schemas = %{version}-%{release}
# sbd 1.4.0+ supports the libpe_status API for pe_working_set_t
# sbd 1.4.2+ supports startup/shutdown handshake via pacemakerd-api
#            and handshake defaults to enabled for rhel builds
# sbd 1.5.0+ handshake defaults to enabled with upstream sbd-release
#            implicitly supports handshake defaults to enabled in this spec
Conflicts:      sbd < 1.5.0

%description -n %{pkgname_pcmk_libs}
Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

The %{pkgname_pcmk_libs} package contains shared libraries needed for cluster
nodes and those just running the CLI tools.

%package cluster-libs
License:        GPLv2+ and LGPLv2+
Summary:        Cluster Libraries used by Pacemaker
Requires:       %{pkgname_pcmk_libs}%{?_isa} = %{version}-%{release}

%description cluster-libs
Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

The %{name}-cluster-libs package contains cluster-aware shared
libraries needed for nodes that will form part of the cluster nodes.

%package remote
License:        GPLv2+ and LGPLv2+
Summary:        Pacemaker remote executor daemon for non-cluster nodes
Requires:       %{pkgname_pcmk_libs}%{?_isa} = %{version}-%{release}
Requires:       %{name}-cli = %{version}-%{release}
Requires:       resource-agents
# -remote can be fully independent of systemd
%{?systemd_ordering}%{!?systemd_ordering:%{?systemd_requires}}
Provides:       pcmk-cluster-manager = %{version}-%{release}
Provides:       pcmk-cluster-manager%{?_isa} = %{version}-%{release}

%description remote
Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

The %{name}-remote package contains the Pacemaker Remote daemon
which is capable of extending pacemaker functionality to remote
nodes not running the full corosync/cluster stack.

%package -n %{pkgname_pcmk_libs}-devel
License:        GPLv2+ and LGPLv2+
Summary:        Pacemaker development package
Requires:       %{pkgname_pcmk_libs}%{?_isa} = %{version}-%{release}
Requires:       %{name}-cluster-libs%{?_isa} = %{version}-%{release}
Requires:       %{pkgname_bzip2_devel}%{?_isa}
Requires:       corosync-devel >= 2.0.0
Requires:       glib2-devel%{?_isa}
Requires:       libqb-devel%{?_isa}
%if %{defined pkgname_libtool_devel_arch}
Requires:       %{?pkgname_libtool_devel_arch}
%endif
Requires:       libuuid-devel%{?_isa}
Requires:       libxml2-devel%{?_isa}
Requires:       libxslt-devel%{?_isa}

%description -n %{pkgname_pcmk_libs}-devel
Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

The %{pkgname_pcmk_libs}-devel package contains headers and shared libraries
for developing tools for Pacemaker.

%package       cts
License:        GPLv2+ and LGPLv2+
Summary:        Test framework for cluster-related technologies like Pacemaker
Requires:       %{python_path}
Requires:       %{pkgname_pcmk_libs} = %{version}-%{release}
Requires:       %{name}-cli = %{version}-%{release}
Requires:       %{pkgname_procps}
Requires:       psmisc
BuildArch:      noarch


%description   cts
Test framework for cluster-related technologies like Pacemaker

%package       doc
License:        CC-BY-SA-4.0
Summary:        Documentation for Pacemaker
BuildArch:      noarch
Conflicts:      %{name}-libs > %{version}-%{release}
Conflicts:      %{name}-libs < %{version}-%{release}

%description   doc
Documentation for Pacemaker.

Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

%package       schemas
License:        GPLv2+
Summary:        Schemas and upgrade stylesheets for Pacemaker
BuildArch:      noarch

%description   schemas
Schemas and upgrade stylesheets for Pacemaker

Pacemaker is an advanced, scalable High-Availability cluster resource
manager.

%prep
%autosetup -p1 -n %{name}-Pacemaker-%{version}

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

CFLAGS="%{optflags} -DQB_KILL_ATTRIBUTE_SECTION"

%configure \
        PYTHON=%{python_path}                                                   \
        %{!?with_hardening:    --disable-hardening}                             \
        %{?with_legacy_links:  --enable-legacy-links}                           \
        %{?with_profiling:     --with-profiling}                                \
        %{?with_cibsecrets:    --with-cibsecrets}                               \
        %{?with_nls:           --enable-nls}                                    \
        %{?with_sbd_sync:      --with-sbd-sync-default="true"}                  \
        %{?gnutls_priorities:  --with-gnutls-priorities="%{gnutls_priorities}"} \
        %{?bug_url:            --with-bug-url=%{bug_url}}                       \
        %{?ocf_root:           --with-ocfdir=%{ocf_root}}                       \
        %{?concurrent_fencing}                                                  \
        %{?resource_stickiness}                                                 \
        %{?compat20}                                                            \
        --disable-static                                                        \
        --with-initdir=%{_initrddir}                                            \
        --with-runstatedir=%{_rundir}                                           \
        --localstatedir=%{_var}                                                 \
        --with-nagios=true                                                      \
        --with-version=%{version}-%{release}

%make_build

%install
%make_install

mkdir -p %{buildroot}%{_localstatedir}/lib/rpm-state/%{name}

# Don't package libtool archives
find %{buildroot} -type f -name "*.la" -delete -print

# Do not package these either
rm -f %{buildroot}/%{_sbindir}/fence_legacy
rm -f %{buildroot}/%{_mandir}/man8/fence_legacy.*

%{py_byte_compile %{python_path} %{buildroot}%{_datadir}/pacemaker/tests}
%{py_byte_compile %{python_path} %{buildroot}%{python_site}/cts}

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
    { mv -fbS.rpmsave %{_}//pacemaker.log* %{_var}/log/pacemaker \
      || mv -f %{_var}/log/pacemaker.log* %{_var}/log/pacemaker
    } >/dev/null 2>/dev/null || :
fi

%preun cli
%systemd_preun crm_mon.service

%postun cli
%systemd_postun_with_restart crm_mon.service

%pre -n %{pkgname_pcmk_libs}
# @TODO Use sysusers.d:
# https://fedoraproject.org/wiki/Changes/Adopting_sysusers.d_format
getent group %{gname} >/dev/null || groupadd -r %{gname} -g %{hacluster_id}
getent passwd %{uname} >/dev/null || useradd -r -g %{gname} -u %{hacluster_id} -s /sbin/nologin -c "cluster user" %{uname}
exit 0

%ldconfig_scriptlets -n %{pkgname_pcmk_libs}
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
%exclude %{_sbindir}/pacemaker_remoted
%{_libexecdir}/pacemaker/*

%{_sbindir}/crm_master
%{_sbindir}/fence_watchdog

%doc %{_mandir}/man7/pacemaker-controld.*
%doc %{_mandir}/man7/pacemaker-schedulerd.*
%doc %{_mandir}/man7/pacemaker-fenced.*
%doc %{_mandir}/man7/ocf_pacemaker_controld.*
%doc %{_mandir}/man7/ocf_pacemaker_remote.*
%doc %{_mandir}/man8/crm_master.*
%doc %{_mandir}/man8/fence_watchdog.*
%doc %{_mandir}/man8/pacemakerd.*

%doc %{_datadir}/pacemaker/alerts

%license licenses/GPLv2
%license COPYING
%doc ChangeLog

%dir %attr (750, %{uname}, %{gname}) %{_sharedstatedir}/pacemaker/cib
%dir %attr (750, %{uname}, %{gname}) %{_sharedstatedir}/pacemaker/pengine
%{ocf_root}/resource.d/pacemaker/controld
%{ocf_root}/resource.d/pacemaker/remote

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
%{_sbindir}/crm_attribute
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

%exclude %{ocf_root}/resource.d/pacemaker/controld
%exclude %{ocf_root}/resource.d/pacemaker/o2cb
%exclude %{ocf_root}/resource.d/pacemaker/remote

%dir %{ocf_root}
%dir %{ocf_root}/resource.d
%{ocf_root}/resource.d/pacemaker

%doc %{_mandir}/man7/*
%exclude %{_mandir}/man7/pacemaker-controld.*
%exclude %{_mandir}/man7/pacemaker-schedulerd.*
%exclude %{_mandir}/man7/pacemaker-fenced.*
%exclude %{_mandir}/man7/ocf_pacemaker_controld.*
%exclude %{_mandir}/man7/ocf_pacemaker_o2cb.*
%exclude %{_mandir}/man7/ocf_pacemaker_remote.*
%doc %{_mandir}/man8/*
%exclude %{_mandir}/man8/crm_master.*
%exclude %{_mandir}/man8/fence_watchdog.*
%exclude %{_mandir}/man8/pacemakerd.*
%exclude %{_mandir}/man8/pacemaker-remoted.*

%license licenses/GPLv2
%license COPYING
%doc ChangeLog

%dir %attr (750, %{uname}, %{gname}) %{_sharedstatedir}/pacemaker
%dir %attr (750, %{uname}, %{gname}) %{_sharedstatedir}/pacemaker/blackbox
%dir %attr (750, %{uname}, %{gname}) %{_sharedstatedir}/pacemaker/cores
%dir %attr (770, %{uname}, %{gname}) %{_var}/log/pacemaker
%dir %attr (770, %{uname}, %{gname}) %{_var}/log/pacemaker/bundles

%files -n %{pkgname_pcmk_libs} %{?with_nls:-f %{name}.lang}
%{_libdir}/libcib.so.*
%{_libdir}/liblrmd.so.*
%{_libdir}/libcrmservice.so.*
%{_libdir}/libcrmcommon.so.*
%{_libdir}/libpe_status.so.*
%{_libdir}/libpe_rules.so.*
%{_libdir}/libpacemaker.so.*
%{_libdir}/libstonithd.so.*
%license licenses/LGPLv2.1
%license COPYING
%doc ChangeLog

%files cluster-libs
%{_libdir}/libcrmcluster.so.*
%license licenses/LGPLv2.1
%license COPYING
%doc ChangeLog

%files remote
%config(noreplace) %{_sysconfdir}/sysconfig/pacemaker
# state directory is shared between the subpackets
# let rpm take care of removing it once it isn't
# referenced anymore and empty
%ghost %dir %{_localstatedir}/lib/rpm-state/%{name}
%{_unitdir}/pacemaker_remote.service

%{_sbindir}/pacemaker-remoted
%{_sbindir}/pacemaker_remoted
%{_mandir}/man8/pacemaker-remoted.*
%license licenses/GPLv2
%license COPYING
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
%license COPYING
%doc ChangeLog

%files -n %{pkgname_pcmk_libs}-devel
%{_includedir}/pacemaker
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%license licenses/LGPLv2.1
%license COPYING
%doc ChangeLog

%files schemas
%license licenses/GPLv2
%dir %{_datadir}/pacemaker
%{_datadir}/pacemaker/*.rng
%{_datadir}/pacemaker/*.xsl
%{_datadir}/pacemaker/api
%{_datadir}/pacemaker/base
%{_datadir}/pkgconfig/pacemaker-schemas.pc

%changelog
* Tue Sep 19 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.1.5-5
- Fix build issue for systemd/systemd-bootstrap confusion

* Wed Mar 08 2023 Sumedh Sharma <sumsharma@microsoft.com> - 2.1.5-4
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Disable nagios-plugins-metadata
- license verified

* Thu Dec 08 2022 Klaus Wenninger <kwenning@redhat.com> - 2.1.5-3
- Update for new upstream release tarball: Pacemaker-2.1.5,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.5

* Thu Nov 24 2022 Klaus Wenninger <kwenning@redhat.com> - 2.1.5-0.3.rc3
- Update for new upstream tarball for release candidate: Pacemaker-2.1.5-rc3,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.5-rc3
- remove unused parts of upstream release-magic

* Wed Nov 16 2022 Klaus Wenninger <kwenning@redhat.com> - 2.1.5-0.2.rc2
- Update for new upstream tarball for release candidate: Pacemaker-2.1.5-rc2,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.5-rc2

* Wed Oct 26 2022 Klaus Wenninger <kwenning@redhat.com> - 2.1.5-0.1.rc1
- Update for new upstream tarball for release candidate: Pacemaker-2.1.5-rc1,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.5-rc1
- add patch to fix 32 bit issue with cmocka

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 30 2022 Klaus Wenninger <kwenning@redhat.com> - 2.1.4-4
- Fix 2.1.3 regression: Don't output "(null)" in crm_attribute's
  quiet mode (rhbz#2099331)

* Mon Jun 20 2022 Klaus Wenninger <kwenning@redhat.com> - 2.1.4-3
- Update for new upstream release tarball: Pacemaker-2.1.4,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.4

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.1.4-0.2.rc1.1
- Rebuilt for Python 3.11

* Wed Jun 8 2022 Klaus Wenninger <kwenning@redhat.com> - 2.1.4-0.2.rc1
- re-add accidentially deleted nagios tar-ball

* Wed Jun 8 2022 Klaus Wenninger <kwenning@redhat.com> - 2.1.4-0.1.rc1
- Update for new upstream tarball for release candidate: Pacemaker-2.1.4-rc1,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.4-rc1

* Tue Jun 7 2022 Klaus Wenninger <kwenning@redhat.com> - 2.1.3-3
- Update for new upstream release tarball: Pacemaker-2.1.3
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.3
- get target-by-attribute working again
- avoid use-after-free with self-fencing and topology

* Mon May 23 2022 Klaus Wenninger <kwenning@redhat.com> - 2.1.3-0.2.rc2
- Update for new upstream tarball for release candidate: Pacemaker-2.1.3-rc2,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.3-rc2
- merged in upstream spec-changes - move crm_attribute to cli-package

* Mon Apr 25 2022 Klaus Wenninger <kwenning@redhat.com> - 2.1.3-0.1.rc1
- Update for new upstream tarball for release candidate: Pacemaker-2.1.3-rc1,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.3-rc1
- merged in upstream spec-changes - add nsl-support, remove gnu-coverage
- removed explicit BuildRequires for glibc-headers again

* Thu Jan 27 2022 Klaus Wenninger <kwenning@redhat.com> - 2.1.2-4
- add explicit BuildRequires for glibc-headers to make
  rawhide build again

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 26 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.2-3
- Update for new upstream release tarball: Pacemaker-2.1.2
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.2

* Wed Nov 17 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.2-0.2.rc2
- Update for new upstream tarball for release candidate: Pacemaker-2.1.2-rc2,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.2-rc2

* Mon Nov 8 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.2-0.1.rc1
- Update for new upstream tarball for release candidate: Pacemaker-2.1.2-rc1,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.2-rc1

* Wed Sep 15 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.1-9
- allow xml-testing without rng in cts-fencing
- merged in upstream spec-changes

* Mon Sep 13 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.1-8
- added test for getting metadata via stonith_admin

* Mon Sep 13 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.1-7
- added test for metadata of fence_watchdog & fence_dummy

* Mon Sep 13 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.1-6
- Update for new upstream release tarball: Pacemaker-2.1.1
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.1
- Add fencing regression-test to gating

* Thu Aug 19 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.1-0.5.rc3
- Fix malformed xml in fence_watchdog metadata

* Tue Aug 17 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.1-0.4.rc3
- Update for new upstream tarball for release candidate: Pacemaker-2.1.1-rc3,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.1-rc3
- Make tools exit-codes consistent for --version
- Check exit-codes of tools prior to manpage-generation

* Wed Aug 11 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.1-0.3.rc2
- package fence_watchdog in base-package instead if cli-subpackage
- fix version output of fence_watchdog as needed for help2man
- ensure transient attributes of lost nodes are cleared reliably

* Mon Aug 9 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.1-0.2.rc2
- Update for new upstream tarball for release candidate: Pacemaker-2.1.1-rc2,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.1-rc2
- Added feature patch that allows to explicitly specify nodes that
  should do watchdog-fencing

* Wed Jul 28 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.1-0.1.rc1
- Update for new upstream tarball for release candidate: Pacemaker-2.1.1-rc1,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.1-rc1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 5 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.0-6
- synced/merged with CS9 spec-file for current 2.1.0-release build

* Tue Jun 8 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.0-0.5.rc3
- silence f33 s390x build complaining about possible format-trucation

* Mon Jun 07 2021 Python Maint <python-maint@redhat.com> - 2.1.0-0.4.rc3.1
- Rebuilt for Python 3.10

* Mon Jun 07 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.0-0.4.rc3
- Update for new upstream tarball for release candidate: Pacemaker-2.1.0-rc3,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.0-rc3

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.1.0-0.3.rc2.1
- Rebuilt for Python 3.10

* Mon May 31 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.0-0.3.rc2
- Update for new upstream tarball for release candidate: Pacemaker-2.1.0-rc2,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.0-rc2
- merge changes in upstream specfile sind Pacemaker-2.1.0-rc1
    add configurable ocf_root
    enable cibsecrets for > f33
    require libqb >= 0.17.0 instead of 0.13.0
    default to syncing with sbd
    conflict all sbd < 1.4.3 to enforce sbd-build has the same default

* Wed May 5 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.0-0.2.rc1
- remove PCMK_TIME_EMERGENCY_CGT not present in pacemaker codebase anymore
- enable Pacemaker-2.0-compatibility for a fedora versions

* Tue May 4 2021 Klaus Wenninger <kwenning@redhat.com> - 2.1.0-0.1.rc1
- Update for new upstream tarball for release candidate: Pacemaker-2.1.0-rc1,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.1.0-rc1
- merge changes in upstream spec-file since Pacemaker-2.0.5
- disable legacy-links

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.5-10.2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-10.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

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
- remove no more working dist.rpmdeplint from gating

* Fri Oct 30 2020 Klaus Wenninger <kwenning@redhat.com> - 2.0.5-0.4.rc2
- never use spec-variables in changelog
- replace dist.depcheck by dist.rpmdeplint
- do gate stable as well to be effective on rawhide

* Fri Oct 30 2020 Klaus Wenninger <kwenning@redhat.com> - 2.0.5-0.3.rc2
- revert dependency corosync-devel back to corosynclib-devel as long
  as corosynclib-devel-package doesn't provide corosync-devel(isa)
  we would need for pacemaker-libs-devel to require
- enable some basic gating-tests
- re-add building documentation using publican to everything but ELN
- rename doc-dir for ELN

* Wed Oct 28 2020 Klaus Wenninger <kwenning@redhat.com> - 2.0.5-0.2.rc2
- Update for new upstream tarball for release candidate: Pacemaker-2.0.5-rc2,
  includes fix for CVE-2020-25654
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.5-rc2

* Thu Oct 22 2020 Klaus Wenninger <kwenning@redhat.com> - 2.0.5-0.1.rc1
- Update for new upstream tarball for release candidate: Pacemaker-2.0.5-rc1,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.5-rc1
- Disable building of documentation - as not to pull in publican
- Remove dependencies to nagios-plugins from metadata-package
- some sync with structure of upstream spec-file
- removed some legacy conditionals
- added with-cibsecrets

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 16 2020 Chris Lumens <clumens@redhat.com> - 2.0.4-1
- Update for new upstream tarball: Pacemaker-2.0.4
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.4

* Thu Jun 04 2020 Chris Lumens <clumens@redhat.com> - 2.0.4-0.1.rc3
- Update for new upstream tarball for release candidate: Pacemaker-2.0.4-rc3,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.4-rc3

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.4-0.2.rc1.1
- Rebuilt for Python 3.9

* Wed May 13 2020 Chris Lumens <clumens@redhat.com> - 2.0.4-0.2.rc1
- Rebuilt for libqb 2.0.

* Mon May 04 2020 Chris Lumens <clumens@redhat.com> - 2.0.4-0.1.rc1
- Update for new upstream tarball for release candidate: Pacemaker-2.0.4-rc1,
  for full details, see included ChangeLog file or
  https://github.com/ClusterLabs/pacemaker/releases/tag/Pacemaker-2.0.4-rc1

* Fri Mar 06 2020 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.3-4
- return back to building also for s390x architecture, previous obstacle
  was identified and interim fix (way to build along with one actual bugfix
  as raised along) applied (RHBZ#1799842)

* Wed Mar 04 2020 Jan Pokorný <jpokorny+rpm-pacemaker@redhat.com> - 2.0.3-3
- include upstream fix for buildability with GCC 10 (PR #1968)
- omit s390x architecture for now, compilation would fail at this time

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
