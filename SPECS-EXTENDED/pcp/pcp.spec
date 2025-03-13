%global _unpackaged_files_terminate_build 0

Name:    pcp
Version: 6.3.2
Release: 1%{?dist}
Summary: System-level performance monitoring and performance management
License: GPLv2+ and LGPLv2+ and CC-BY
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:     https://pcp.io

Source0: https://github.com/performancecopilot/pcp/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

Patch0: pcp-xsos-fixes.patch
Patch1: pcp-gcc15.patch

ExcludeArch: %{ix86}
# The additional linker flags break out-of-tree PMDAs.
%undefine _package_note_flags
%global __python2 python2

%global _hostname_executable /bin/hostname
%global _ps_executable /bin/ps

# On 32-bit systems time64_t and perl modules do not play well together
%ifarch ix86
%global disable_perl 1
%else
%global disable_perl 0
%endif
%global disable_selinux 1

%global disable_snmp 0

# No libpfm devel packages for s390, armv7hl nor for some rhels, disable
%ifarch s390 s390x armv7hl
%global disable_perfevent 1
%else
%global disable_perfevent 0
%endif

# libvarlink and pmdapodman
%global disable_podman 0

# libchan, libhdr_histogram and pmdastatsd
# Azurelinux does not provide HdrHistogram_c

%global disable_gfs2 0
%global _with_python2 --with-python=no
%global disable_python2 1


# No python3 development environment before el8
%global disable_python3 0
%global default_python 3

%bcond_without libvirt

%global perl_interpreter perl-interpreter

# support for pmdabcc, check bcc.spec for supported architectures of bcc
%ifarch x86_64 %{power64} aarch64 s390x
%global disable_bcc 0
%else
%global disable_bcc 1
%endif

# libbpf-tools are not provided in azurelinux

# support for pmdajson
%if !%{disable_python2} || !%{disable_python3}
%global disable_json 0
%else
%global disable_json 1
%endif

# support for pmdanutcracker (perl deps missing on rhel)
%global disable_nutcracker 0

# support for pmdarpm removed from 5.3.2 from upstream

# GUI components not needed in Azurelinux

# systemd services and pmdasystemd
%global disable_systemd 0

# static probes, missing before el6 and on some architectures
%global disable_sdt 0

# libuv async event library
%global disable_libuv 0

%global disable_openssl 0

# rpm producing "noarch" packages
%global disable_noarch 0

# prevent conflicting binary and man page install for pcp(1)
Conflicts: librapi < 0.16

# KVM PMDA moved into pcp (no longer using Perl, default on)
Obsoletes: pcp-pmda-kvm < 4.1.1
Provides: pcp-pmda-kvm

# RPM PMDA retired completely
Obsoletes: pcp-pmda-rpm < 5.3.2
Obsoletes: pcp-pmda-rpm-debuginfo < 5.3.2
# PCP REST APIs are now provided by pmproxy
Obsoletes: pcp-webapi-debuginfo < 5.0.0
Obsoletes: pcp-webapi < 5.0.0
Provides: pcp-webapi = %{version}-%{release}

# PCP discovery service now provided by pmfind
Obsoletes: pcp-manager-debuginfo < 5.2.0
Obsoletes: pcp-manager < 5.2.0
Obsoletes: pcp-compat < 4.2.0
Obsoletes: pcp-monitor < 4.2.0
Obsoletes: pcp-collector < 4.2.0
Obsoletes: pcp-pmda-nvidia < 3.10.5

# https://fedoraproject.org/wiki/Packaging "C and C++"
BuildRequires: make
BuildRequires: gcc gcc-c++
BuildRequires: procps
BuildRequires: autoconf
BuildRequires: bison
BuildRequires: flex
BuildRequires: avahi-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel
%if !%{disable_python2}
%if 0%{?default_python} != 3
BuildRequires: python%{?default_python}-devel
%else
BuildRequires: %{__python2}-devel
%endif
%endif
%if !%{disable_python3}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%endif
BuildRequires: ncurses-devel
BuildRequires: readline-devel
BuildRequires: cyrus-sasl-devel
%if !%{disable_perfevent}
BuildRequires: libpfm-devel >= 4
%endif
%if !%{disable_sdt}
BuildRequires: systemtap-sdt-devel
%endif
%if !%{disable_libuv}
BuildRequires: libuv-devel >= 1.0
%endif
%if !%{disable_openssl}
BuildRequires: openssl-devel >= 1.1.1
%endif
BuildRequires: perl-generators
BuildRequires: perl-devel
BuildRequires: perl(strict)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(LWP::UserAgent)
BuildRequires: perl(JSON)
BuildRequires: perl(Digest::MD5)
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(File::Slurp)
BuildRequires: perl(XML::LibXML)
BuildRequires: %{_hostname_executable}
BuildRequires: %{_ps_executable}
%if !%{disable_systemd}
BuildRequires: systemd-devel
%endif
# Utilities used indirectly e.g. by scripts we install
Requires: bash
Requires: xz
Requires: gawk
Requires: sed
Requires: grep
Requires: coreutils
Requires: diffutils
Requires: findutils
Requires: which %{_hostname_executable} %{_ps_executable}
Requires: pcp-libs = %{version}-%{release}
%if !%{disable_selinux}
Requires: pcp-selinux = %{version}-%{release}
%endif

%global _confdir        %{_sysconfdir}/pcp
%global _logsdir        %{_localstatedir}/log/pcp
%global _pmnsdir        %{_localstatedir}/lib/pcp/pmns
%global _tempsdir       %{_localstatedir}/lib/pcp/tmp
%global _pmdasdir       %{_localstatedir}/lib/pcp/pmdas
%global _pmdasexecdir   %{_libexecdir}/pcp/pmdas
%global _testsdir       %{_localstatedir}/lib/pcp/testsuite
%global _ieconfigdir    %{_localstatedir}/lib/pcp/config/pmie
%global _logconfdir     %{_localstatedir}/lib/pcp/config/pmlogconf
%global _ieconfdir      %{_localstatedir}/lib/pcp/config/pmieconf
%global _selinuxdir     %{_datadir}/selinux/packages/targeted
%global _hicolordir     %{_datadir}/icons/hicolor
%global _booksdir       %{_datadir}/doc/pcp-doc

%global _with_doc --with-docdir=%{_docdir}/%{name}

%global _with_dstat --with-dstat-symlink=yes
%global disable_dstat 0

%if !%{disable_systemd}
%global _initddir %{_libexecdir}/pcp/lib
%else
%global _initddir %{_sysconfdir}/rc.d/init.d
%global _with_initd --with-rcdir=%{_initddir}
%endif

# we never want Infiniband on s390 and armv7hl platforms
%ifarch s390 s390x armv7hl
%global disable_infiniband 1
%else
%global disable_infiniband 0
%endif

%if !%{disable_infiniband}
%global _with_ib --with-infiniband=yes
%endif

%if %{disable_perfevent}
%global _with_perfevent --with-perfevent=no
%else
%global _with_perfevent --with-perfevent=yes
%endif

%if %{disable_podman}
%global _with_podman --with-podman=no
%else
%global _with_podman --with-podman=yes
%endif

%if %{disable_gfs2}
%global _with_gfs2 --with-pmdagfs2=no
%else
%global _with_gfs2 --with-pmdagfs2=yes
%endif

%global _with_statsd --with-pmdastatsd=no

%if %{disable_bcc}
%global _with_bcc --with-pmdabcc=no
%else
%global _with_bcc --with-pmdabcc=yes
%endif
 
%global _with_bpf --with-pmdabpf=no
%global _with_bpftrace --with-pmdabpftrace=no

%if %{disable_json}
%global _with_json --with-pmdajson=no
%else
%global _with_json --with-pmdajson=yes
%endif
 
%global _with_mongodb --with-pmdamongodb=no
 
%if %{disable_nutcracker}
%global _with_nutcracker --with-pmdanutcracker=no
%else
%global _with_nutcracker --with-pmdanutcracker=yes
%endif

%if %{disable_snmp}
%global _with_snmp --with-pmdasnmp=no
%else
%global _with_snmp --with-pmdasnmp=yes
%endif

%global pmda_remove() %{expand:
if [ %1 -eq 0 ]
then
    PCP_PMDAS_DIR=%{_pmdasdir}
    PCP_PMCDCONF_PATH=%{_confdir}/pmcd/pmcd.conf
    if [ -f "$PCP_PMCDCONF_PATH" -a -f "$PCP_PMDAS_DIR/%2/domain.h" ]
    then
        (cd "$PCP_PMDAS_DIR/%2/" && ./Remove >/dev/null 2>&1)
    fi
fi
}

%global install_file() %{expand:
if [ -w "%1" ]
then
    (cd "%1" && touch "%2" && chmod 644 "%2")
else
    echo "WARNING: Cannot write to %1, skipping %2 creation." >&2
fi
}

%global rebuild_pmns() %{expand:
if [ -w "%1" ]
then
    (cd "%1" && ./Rebuild -s && rm -f "%2")
else
    echo "WARNING: Cannot write to %1, skipping namespace rebuild." >&2
fi
}

%global run_pmieconf() %{expand:
if [ -d "%1" -a -w "%1" -a -w "%1/%2" ]
then
    pmieconf -f "%1/%2" -c enable "%3"
    chown pcp:pcp "%1/%2" 2>/dev/null
else
    echo "WARNING: Cannot write to %1/%2, skipping pmieconf enable of %3." >&2
fi
}

%description
Performance Co-Pilot (PCP) provides a framework and services to support
system-level performance monitoring and performance management.

The PCP open source release provides a unifying abstraction for all of
the interesting performance data in a system, and allows client
applications to easily retrieve and process any subset of that data.

#
# pcp-conf
#
%package conf
License: LGPLv2+
Summary: Performance Co-Pilot run-time configuration
URL: https://pcp.io

# http://fedoraproject.org/wiki/Packaging:Conflicts "Splitting Packages"
Conflicts: pcp-libs < 3.9

%description conf
Performance Co-Pilot (PCP) run-time configuration

#
# pcp-libs
#
%package libs
License: LGPLv2+
Summary: Performance Co-Pilot run-time libraries
URL: https://pcp.io
Requires: pcp-conf = %{version}-%{release}
 
# prevent conflicting library (libpcp.so.N) installation
Conflicts: postgresql-pgpool-II
 
%description libs
Performance Co-Pilot (PCP) run-time libraries

#
# pcp-libs-devel
#
%package libs-devel
License: GPLv2+ and LGPLv2+
Summary: Performance Co-Pilot (PCP) development headers
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
 
# prevent conflicting library (libpcp.so) installation
Conflicts: postgresql-pgpool-II-devel
 
%description libs-devel
Performance Co-Pilot (PCP) headers for development.

#
# pcp-devel
#
%package devel
License: GPLv2+ and LGPLv2+
Summary: Performance Co-Pilot (PCP) development tools and documentation
URL: https://pcp.io
Requires: pcp = %{version}-%{release}
Requires: pcp-libs = %{version}-%{release}
Requires: pcp-libs-devel = %{version}-%{release}

%description devel
Performance Co-Pilot (PCP) documentation and tools for development.

#
# pcp-testsuite
#
%package testsuite
License: GPLv2+
Summary: Performance Co-Pilot (PCP) test suite
URL: https://pcp.io
Requires: pcp = %{version}-%{release}
Requires: pcp-libs = %{version}-%{release}
Requires: pcp-libs-devel = %{version}-%{release}
Requires: pcp-devel = %{version}-%{release}
Obsoletes: pcp-gui-testsuite < 3.9.5
# The following are inherited from pcp-collector and pcp-monitor,
# both of which are now obsoleted by the base pcp package
Requires: pcp-pmda-activemq
Requires: pcp-pmda-bonding
Requires: pcp-pmda-dbping
Requires: pcp-pmda-ds389
Requires: pcp-pmda-ds389log
Requires: pcp-pmda-elasticsearch
Requires: pcp-pmda-gpfs
Requires: pcp-pmda-gpsd
Requires: pcp-pmda-lustre
Requires: pcp-pmda-memcache
Requires: pcp-pmda-mysql
Requires: pcp-pmda-named
Requires: pcp-pmda-netfilter
Requires: pcp-pmda-news
Requires: pcp-pmda-nginx
Requires: pcp-pmda-nfsclient
Requires: pcp-pmda-pdns
Requires: pcp-pmda-postfix
Requires: pcp-pmda-postgresql 
Requires: pcp-pmda-oracle
Requires: pcp-pmda-samba 
Requires: pcp-pmda-slurm
Requires: pcp-pmda-zimbra
Requires: pcp-pmda-dm
Requires: pcp-pmda-apache
Requires: pcp-pmda-bash
Requires: pcp-pmda-cisco
Requires: pcp-pmda-mailq
Requires: pcp-pmda-mounts
Requires: pcp-pmda-nvidia-gpu
Requires: pcp-pmda-roomtemp
Requires: pcp-pmda-sendmail
Requires: pcp-pmda-shping pcp-pmda-smart
Requires: pcp-pmda-lustrecomm
Requires: pcp-pmda-logger
Requires: pcp-pmda-docker
Requires: pcp-pmda-bind2
%if !%{disable_podman}
Requires: pcp-pmda-podman
%endif
%if !%{disable_gfs2}
Requires: pcp-pmda-gfs2
%endif
%if !%{disable_nutcracker}
Requires: pcp-pmda-nutcracker
%endif
%if !%{disable_bcc}
Requires: pcp-pmda-bcc
%endif
%if !%{disable_python2} || !%{disable_python3}
Requires: pcp-export-pcp2json
Requires: pcp-export-pcp2spark
Requires: pcp-export-pcp2xml
Requires: pcp-export-pcp2zabbix
Requires: pcp-pmda-gluster
Requires: pcp-pmda-zswap
Requires: pcp-pmda-unbound
Requires: pcp-pmda-mic
Requires: pcp-pmda-lio
Requires: pcp-pmda-openmetrics
Requires: pcp-pmda-haproxy
Requires: pcp-pmda-lmsensors
Requires: pcp-pmda-netcheck
Requires: pcp-pmda-rabbitmq
Requires: pcp-pmda-openvswitch

%if %{with libvirt}
Requires: pcp-pmda-libvirt
%endif

%endif
%if !%{disable_snmp}
Requires: pcp-pmda-snmp
%endif
%if !%{disable_json}
Requires: pcp-pmda-json
%endif
Requires: pcp-pmda-summary
Requires: pcp-pmda-trace
Requires: pcp-pmda-weblog
%if !%{disable_python2} || !%{disable_python3}
Requires: pcp-system-tools
%endif
Requires: bc
Requires: gcc
Requires: gzip
Requires: bzip2
Requires: redhat-rpm-config
%if !%{disable_selinux}
Requires: selinux-policy-devel
Requires: selinux-policy-targeted
Requires: setools-console
%endif

%description testsuite
Quality assurance test suite for Performance Co-Pilot (PCP).
# end testsuite

#
# perl-PCP-PMDA. This is the PCP agent perl binding.
#
%package -n perl-PCP-PMDA
License: GPLv2+
Summary: Performance Co-Pilot (PCP) Perl bindings and documentation
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: %{perl_interpreter}

%description -n perl-PCP-PMDA
The PCP::PMDA Perl module contains the language bindings for
building Performance Metric Domain Agents (PMDAs) using Perl.
Each PMDA exports performance data for one specific domain, for
example the operating system kernel, Cisco routers, a database,
an application, etc.

#
# perl-PCP-MMV
#
%package -n perl-PCP-MMV
License: GPLv2+
Summary: Performance Co-Pilot (PCP) Perl bindings for PCP Memory Mapped Values
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: %{perl_interpreter}

%description -n perl-PCP-MMV
The PCP::MMV module contains the Perl language bindings for
building scripts instrumented with the Performance Co-Pilot
(PCP) Memory Mapped Value (MMV) mechanism.
This mechanism allows arbitrary values to be exported from an
instrumented script into the PCP infrastructure for monitoring
and analysis with pmchart, pmie, pmlogger and other PCP tools.

#
# perl-PCP-LogImport
#
%package -n perl-PCP-LogImport
License: GPLv2+
Summary: Performance Co-Pilot (PCP) Perl bindings for importing external data into PCP archives
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: %{perl_interpreter}

%description -n perl-PCP-LogImport
The PCP::LogImport module contains the Perl language bindings for
importing data in various 3rd party formats into PCP archives so
they can be replayed with standard PCP monitoring tools.

#
# perl-PCP-LogSummary
#
%package -n perl-PCP-LogSummary
License: GPLv2+
Summary: Performance Co-Pilot (PCP) Perl bindings for post-processing output of pmlogsummary
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: %{perl_interpreter}

%description -n perl-PCP-LogSummary
The PCP::LogSummary module provides a Perl module for using the
statistical summary data produced by the Performance Co-Pilot
pmlogsummary utility.  This utility produces various averages,
minima, maxima, and other calculations based on the performance
data stored in a PCP archive.  The Perl interface is ideal for
exporting this data into third-party tools (e.g. spreadsheets).

#
# pcp-import-sar2pcp
#
%package import-sar2pcp
License: LGPLv2+
Summary: Performance Co-Pilot tools for importing sar data into PCP archive logs
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: perl-PCP-LogImport = %{version}-%{release}
Requires: perl(XML::TokeParser)

%description import-sar2pcp
Performance Co-Pilot (PCP) front-end tools for importing sar data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-import-iostat2pcp
#
%package import-iostat2pcp
License: LGPLv2+
Summary: Performance Co-Pilot tools for importing iostat data into PCP archive logs
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: perl-PCP-LogImport = %{version}-%{release}

%description import-iostat2pcp
Performance Co-Pilot (PCP) front-end tools for importing iostat data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-import-mrtg2pcp
#
%package import-mrtg2pcp
License: LGPLv2+
Summary: Performance Co-Pilot tools for importing MTRG data into PCP archive logs
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: perl-PCP-LogImport = %{version}-%{release}

%description import-mrtg2pcp
Performance Co-Pilot (PCP) front-end tools for importing MTRG data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-import-ganglia2pcp
#
%package import-ganglia2pcp
License: LGPLv2+
Summary: Performance Co-Pilot tools for importing ganglia data into PCP archive logs
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: perl-PCP-LogImport = %{version}-%{release}

%description import-ganglia2pcp
Performance Co-Pilot (PCP) front-end tools for importing ganglia data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-import-collectl2pcp
#
%package import-collectl2pcp
License: LGPLv2+
Summary: Performance Co-Pilot tools for importing collectl log files into PCP archive logs
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}

%description import-collectl2pcp
Performance Co-Pilot (PCP) front-end tools for importing collectl data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-export-zabbix-agent
#
%package export-zabbix-agent
License: GPLv2+
Summary: Module for exporting PCP metrics to Zabbix agent
URL: https://pcp.io
Requires: pcp-libs = %{version}-%{release}

%description export-zabbix-agent
Performance Co-Pilot (PCP) module for exporting metrics from PCP to
Zabbix via the Zabbix agent - see zbxpcp(3) for further details.

%if !%{disable_python2} || !%{disable_python3}
#
# pcp-export-pcp2elasticsearch
#
%package export-pcp2elasticsearch
License: GPLv2+
Summary: Performance Co-Pilot tools for exporting PCP metrics to ElasticSearch
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp = %{version}-%{release}
Requires: python3-requests
BuildRequires: python3-requests
%else
Requires: %{__python2}-pcp = %{version}-%{release}
Requires: %{__python2}-requests
BuildRequires: %{__python2}-requests
%endif

%description export-pcp2elasticsearch
Performance Co-Pilot (PCP) front-end tools for exporting metric values
to Elasticsearch - a distributed, RESTful search and analytics engine.
See https://www.elastic.co/community for further details.

#
# pcp-export-pcp2graphite
#
%package export-pcp2graphite
License: GPLv2+
Summary: Performance Co-Pilot tools for exporting PCP metrics to Graphite
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp = %{version}-%{release}
%else
Requires: %{__python2}-pcp = %{version}-%{release}
%endif

%description export-pcp2graphite
Performance Co-Pilot (PCP) front-end tools for exporting metric values
to graphite (http://graphite.readthedocs.org).

# pcp-export-pcp2influxdb
#
%package export-pcp2influxdb
License: GPLv2+
Summary: Performance Co-Pilot tools for exporting PCP metrics to InfluxDB
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp = %{version}-%{release}
Requires: python3-requests
%else
Requires: %{__python2}-pcp = %{version}-%{release}
Requires: %{__python2}-requests
%endif

%description export-pcp2influxdb
Performance Co-Pilot (PCP) front-end tools for exporting metric values
to InfluxDB (https://influxdata.com/time-series-platform/influxdb).

#
# pcp-export-pcp2json
#
%package export-pcp2json
License: GPLv2+
Summary: Performance Co-Pilot tools for exporting PCP metrics in JSON format
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp = %{version}-%{release}
%else
Requires: %{__python2}-pcp = %{version}-%{release}
%endif

%description export-pcp2json
Performance Co-Pilot (PCP) front-end tools for exporting metric values
in JSON format.
 
#
# pcp-export-pcp2spark
#
%package export-pcp2spark
License: GPLv2+
Summary: Performance Co-Pilot tools for exporting PCP metrics to Apache Spark
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp = %{version}-%{release}
%else
Requires: %{__python2}-pcp = %{version}-%{release}
%endif

%description export-pcp2spark
Performance Co-Pilot (PCP) front-end tools for exporting metric values
in JSON format to Apache Spark. See https://spark.apache.org/ for
further details on Apache Spark.

#
# pcp-export-pcp2xml
#
%package export-pcp2xml
License: GPLv2+
Summary: Performance Co-Pilot tools for exporting PCP metrics in XML format
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp = %{version}-%{release}
%else
Requires: %{__python2}-pcp = %{version}-%{release}
%endif

%description export-pcp2xml
Performance Co-Pilot (PCP) front-end tools for exporting metric values
in XML format.

#
# pcp-export-pcp2zabbix
#
%package export-pcp2zabbix
License: GPLv2+
Summary: Performance Co-Pilot tools for exporting PCP metrics to Zabbix
URL: https://pcp.io
Requires: pcp-libs >= %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp = %{version}-%{release}
%else
Requires: %{__python2}-pcp = %{version}-%{release}
%endif

%description export-pcp2zabbix
Performance Co-Pilot (PCP) front-end tools for exporting metric values
to the Zabbix (https://www.zabbix.org/) monitoring software.
%endif

%if !%{disable_podman}
#
# pcp-pmda-podman
#
%package pmda-podman
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for podman containers
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}

%description pmda-podman
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting podman container and pod statistics via the podman REST API.
%endif

%if !%{disable_perfevent}
#
# pcp-pmda-perfevent
#
%package pmda-perfevent
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for hardware counters
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: libpfm >= 4
BuildRequires: libpfm-devel >= 4
Obsoletes: pcp-pmda-papi < 5.0.0
Obsoletes: pcp-pmda-papi-debuginfo < 5.0.0

%description pmda-perfevent
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting hardware counters statistics through libpfm.
%endif

%if !%{disable_infiniband}
#
# pcp-pmda-infiniband
#
%package pmda-infiniband
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Infiniband HCAs and switches
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: libibmad >= 1.3.7 libibumad >= 1.3.7
BuildRequires: libibmad-devel >= 1.3.7 libibumad-devel >= 1.3.7

%description pmda-infiniband
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting Infiniband statistics.  By default, it monitors the local HCAs
but can also be configured to monitor remote GUIDs such as IB switches.
%endif

#
# pcp-pmda-activemq
#
%package pmda-activemq
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for ActiveMQ
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl(LWP::UserAgent)

%description pmda-activemq
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the ActiveMQ message broker.
#end pcp-pmda-activemq

#
# pcp-pmda-bind2
#
%package pmda-bind2
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for BIND servers
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl(LWP::UserAgent)
Requires: perl(XML::LibXML)
Requires: perl(File::Slurp)
Requires: perl-autodie
Requires: perl-Time-HiRes

%description pmda-bind2
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from BIND (Berkeley Internet Name Domain).
#end pcp-pmda-bind2

#
# pcp-pmda-redis
#
%package pmda-redis
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Redis
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl-autodie
Requires: perl-Time-HiRes
Requires: perl-Data-Dumper

%description pmda-redis
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from Redis servers (redis.io).
#end pcp-pmda-redis

%if !%{disable_nutcracker}
#
# pcp-pmda-nutcracker
#
%package pmda-nutcracker
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for NutCracker (TwemCache)
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl(YAML::XS)
Requires: perl(JSON)

%description pmda-nutcracker
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from NutCracker (TwemCache).
#end pcp-pmda-nutcracker
%endif

#
# pcp-pmda-bonding
#
%package pmda-bonding
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Bonded network interfaces
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-bonding
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about bonded network interfaces.
#end pcp-pmda-bonding

#
# pcp-pmda-dbping
#
%package pmda-dbping
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Database response times and Availablility
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl-DBI

%description pmda-dbping
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Database response times and Availablility.
#end pcp-pmda-dbping

#
# pcp-pmda-ds389
#
%package pmda-ds389
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for 389 Directory Servers
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-ds389
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about a 389 Directory Server.
#end pcp-pmda-ds389

#
# pcp-pmda-ds389log
#
%package pmda-ds389log
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for 389 Directory Server Loggers
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl-Date-Manip

%description pmda-ds389log
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from a 389 Directory Server log.
#end pcp-pmda-ds389log


#
# pcp-pmda-gpfs
#
%package pmda-gpfs
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for GPFS Filesystem
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-gpfs
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the GPFS filesystem.
#end pcp-pmda-gpfs

#
# pcp-pmda-gpsd
#
%package pmda-gpsd
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for a GPS Daemon
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl-Time-HiRes
Requires: perl-JSON

%description pmda-gpsd
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about a GPS Daemon.
#end pcp-pmda-gpsd

#
# pcp-pmda-docker
#
%package pmda-docker
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics from the Docker daemon
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}

%description pmda-docker
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics using the Docker daemon REST API.
#end pcp-pmda-docker

#
# pcp-pmda-lustre
#
%package pmda-lustre
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the Lustre Filesytem
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-lustre
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Lustre Filesystem.
#end pcp-pmda-lustre

#
# pcp-pmda-lustrecomm
#
%package pmda-lustrecomm
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the Lustre Filesytem Comms
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}

%description pmda-lustrecomm
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Lustre Filesystem Comms.
#end pcp-pmda-lustrecomm

#
# pcp-pmda-memcache
#
%package pmda-memcache
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Memcached
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-memcache
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Memcached.
#end pcp-pmda-memcache

#
# pcp-pmda-mysql
#
%package pmda-mysql
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for MySQL
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl(DBI) perl(DBD::mysql)
BuildRequires: perl(DBI) perl(DBD::mysql)

%description pmda-mysql
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the MySQL database.
#end pcp-pmda-mysql

#
# pcp-pmda-named
#
%package pmda-named
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Named
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-named
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Named nameserver.
#end pcp-pmda-named

# pcp-pmda-netfilter
#
%package pmda-netfilter
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Netfilter framework
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-netfilter
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Netfilter packet filtering framework.
#end pcp-pmda-netfilter

#
# pcp-pmda-news
#
%package pmda-news
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Usenet News
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-news
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Usenet News.
#end pcp-pmda-news

#
# pcp-pmda-nginx
#
%package pmda-nginx
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the Nginx Webserver
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl(LWP::UserAgent)
BuildRequires: perl(LWP::UserAgent)

%description pmda-nginx
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Nginx Webserver.
#end pcp-pmda-nginx

#
# pcp-pmda-oracle
#
%package pmda-oracle
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the Oracle database
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl(DBI)
BuildRequires: perl(DBI)

%description pmda-oracle
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Oracle database.
#end pcp-pmda-oracle

#
# pcp-pmda-pdns
#
%package pmda-pdns
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for PowerDNS
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl-Time-HiRes

%description pmda-pdns
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the PowerDNS.
#end pcp-pmda-pdns

#
# pcp-pmda-postfix
#
%package pmda-postfix
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the Postfix (MTA)
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
Requires: perl-Time-HiRes
Requires: postfix-perl-scripts
BuildRequires: postfix-perl-scripts
%if "%{_vendor}" == "suse"
Requires: postfix-doc
BuildRequires: postfix-doc
%endif

%description pmda-postfix
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Postfix (MTA).
#end pcp-pmda-postfix

#
# pcp-pmda-rsyslog
#
%package pmda-rsyslog
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Rsyslog
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-rsyslog
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Rsyslog.
#end pcp-pmda-rsyslog

#
# pcp-pmda-samba
#
%package pmda-samba
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Samba
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-samba
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Samba.
#end pcp-pmda-samba

#
# pcp-pmda-slurm
#
%package pmda-slurm
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the SLURM Workload Manager
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-slurm
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from the SLURM Workload Manager.
#end pcp-pmda-slurm

%if !%{disable_snmp}
#
# pcp-pmda-snmp
#
%package pmda-snmp
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Simple Network Management Protocol
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}
# There are no perl-Net-SNMP packages in rhel, disable unless non-rhel or epel5
Requires: perl(Net::SNMP)

%description pmda-snmp
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about SNMP.
#end pcp-pmda-snmp
%endif

# pcp-pmda-vmware Obsolete from pcp 5.3.5

#
# pcp-pmda-zimbra
#
%package pmda-zimbra
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Zimbra
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: perl-PCP-PMDA = %{version}-%{release}

%description pmda-zimbra
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Zimbra.
#end pcp-pmda-zimbra

#
# pcp-pmda-dm
#
%package pmda-dm
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the Device Mapper Cache and Thin Client
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
BuildRequires: device-mapper-devel
%description pmda-dm
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Device Mapper Cache and Thin Client.
# end pcp-pmda-dm


%if !%{disable_bcc}
#
# pcp-pmda-bcc
#
%package pmda-bcc
License: ASL 2.0 and GPLv2+
Summary: Performance Co-Pilot (PCP) metrics from eBPF/BCC modules
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3-bcc
Requires: python3-pcp
%description pmda-bcc
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
extracting performance metrics from eBPF/BCC Python modules.
# end pcp-pmda-bcc
%endif

%if !%{disable_python2} || !%{disable_python3}
#
# pcp-pmda-gluster
#
%package pmda-gluster
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the Gluster filesystem
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
%else
Requires: %{__python2}-pcp
%endif
%description pmda-gluster
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the gluster filesystem.
# end pcp-pmda-gluster

#
# pcp-pmda-nfsclient
#
%package pmda-nfsclient
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for NFS Clients
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
%else
Requires: %{__python2}-pcp
%endif
%description pmda-nfsclient
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics for NFS Clients.
#end pcp-pmda-nfsclient

#
# pcp-pmda-postgresql
#
%package pmda-postgresql
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for PostgreSQL
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
Requires: python3-psycopg2
BuildRequires: python3-psycopg2
%else
Requires: %{__python2}-pcp
Requires: %{__python2}-psycopg2
BuildRequires: %{__python2}-psycopg2
%endif
%description pmda-postgresql
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the PostgreSQL database.
#end pcp-pmda-postgresql

#
# pcp-pmda-zswap
#
%package pmda-zswap
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for compressed swap
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
%else
Requires: %{__python2}-pcp
%endif
%description pmda-zswap
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about compressed swap.
# end pcp-pmda-zswap

#
# pcp-pmda-unbound
#
%package pmda-unbound
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the Unbound DNS Resolver
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
%else
Requires: %{__python2}-pcp
%endif
%description pmda-unbound
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Unbound DNS Resolver.
# end pcp-pmda-unbound

#
# pcp-pmda-mic
#
%package pmda-mic
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Intel MIC cards
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
%else
Requires: %{__python2}-pcp
%endif
%description pmda-mic
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Intel MIC cards.
# end pcp-pmda-mic

#
# pcp-pmda-haproxy
#
%package pmda-haproxy
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for HAProxy
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
%else
Requires: %{__python2}-pcp
%endif
%description pmda-haproxy
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
extracting performance metrics from HAProxy over the HAProxy stats socket.
# end pcp-pmda-haproxy

#
# pcp-pmda-libvirt
#
%if %{with libvirt}
%package pmda-libvirt
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics from virtual machines
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
Requires: libvirt-python3 python3-lxml
BuildRequires: libvirt-python3 python3-lxml
%else
Requires: %{__python2}-pcp
Requires: %{__python2}-libvirt %{__python2}-lxml
BuildRequires: %{__python2}-libvirt %{__python2}-lxml
%endif
%description pmda-libvirt
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
extracting virtualisation statistics from libvirt about behaviour of guest
and hypervisor machines.
# end pcp-pmda-libvirt
%endif

#
# pcp-pmda-elasticsearch
#
%package pmda-elasticsearch
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Elasticsearch
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
%else
Requires: %{__python2}-pcp
%endif
%description pmda-elasticsearch
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Elasticsearch.
#end pcp-pmda-elasticsearch

#
# pcp-pmda-openvswitch
#
%package pmda-openvswitch
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Open vSwitch
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
%else
Requires: %{__python2}-pcp
%endif
%description pmda-openvswitch
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from Open vSwitch.
#end pcp-pmda-openvswitch

#
# pcp-pmda-rabbitmq
#
%package pmda-rabbitmq
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for RabbitMQ queues
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
%else
Requires: %{__python2}-pcp
%endif
%description pmda-rabbitmq
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about RabbitMQ message queues.
#end pcp-pmda-rabbitmq

#
# pcp-pmda-lio
#
%package pmda-lio
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the LIO subsystem
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
Requires: python3-rtslib
BuildRequires: python3-rtslib
%else
Requires: %{__python2}-pcp
Requires: %{__python2}-rtslib
BuildRequires: %{__python2}-rtslib
%endif
%description pmda-lio
This package provides a PMDA to gather performance metrics from the kernels
iSCSI target interface (LIO). The metrics are stored by LIO within the Linux
kernels configfs filesystem. The PMDA provides per LUN level stats, and a
summary instance per iSCSI target, which aggregates all LUN metrics within the
target.
#end pcp-pmda-lio

#
# pcp-pmda-openmetrics
#
%package pmda-openmetrics
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics from OpenMetrics endpoints
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
Requires: python3-requests
BuildRequires: python3-requests
%else
Requires: %{__python2}-pcp
Requires: %{__python2}-requests
BuildRequires: %{__python2}-requests
%endif
# Obsoletes: pcp-pmda-prometheus < 5.0.0
Provides: pcp-pmda-prometheus

%description pmda-openmetrics
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
extracting metrics from OpenMetrics (https://openmetrics.io/) endpoints.
#end pcp-pmda-openmetrics

#
# pcp-pmda-lmsensors
#
%package pmda-lmsensors
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for hardware sensors
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: lm-sensors
%if !%{disable_python3}
Requires: python3-pcp
%else
Requires: %{__python2}-pcp
%endif
# rewritten in python, so there is no longer a debuginfo package
Obsoletes: pcp-pmda-lmsensors-debuginfo < 4.2.0
%description pmda-lmsensors
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Linux hardware monitoring sensors.
# end pcp-pmda-lmsensors

#
# pcp-pmda-netcheck
#
%package pmda-netcheck
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for simple network checks
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
%else
Requires: %{__python2}-pcp
%endif
%description pmda-netcheck
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from simple network checks.
# end pcp-pmda-netcheck

%endif

%if !%{disable_json}
#
# pcp-pmda-json
#
%package pmda-json
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for JSON data
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%if !%{disable_python3}
Requires: python3-pcp
Requires: python3-jsonpointer python3-six
BuildRequires: python3-jsonpointer python3-six
%else
Requires: %{__python2}-pcp
Requires: %{__python2}-jsonpointer %{__python2}-six
BuildRequires: %{__python2}-jsonpointer %{__python2}-six
%endif
%description pmda-json
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics output in JSON.
# end pcp-pmda-json
%endif

#
# C pmdas
# pcp-pmda-apache
#
%package pmda-apache
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the Apache webserver
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-apache
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Apache webserver.
# end pcp-pmda-apache

#
# pcp-pmda-bash
#
%package pmda-bash
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the Bash shell
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-bash
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Bash shell.
# end pcp-pmda-bash

#
# pcp-pmda-cifs
#
%package pmda-cifs
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the CIFS protocol
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-cifs
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Common Internet Filesytem.
# end pcp-pmda-cifs

#
# pcp-pmda-cisco
#
%package pmda-cisco
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Cisco routers
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-cisco
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Cisco routers.
# end pcp-pmda-cisco

%if !%{disable_gfs2}
#
# pcp-pmda-gfs2
#
%package pmda-gfs2
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the GFS2 filesystem
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-gfs2
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the Global Filesystem v2.
# end pcp-pmda-gfs2
%endif

#
# pcp-pmda-logger
#
%package pmda-logger
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics from arbitrary log files
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-logger
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from a specified set of log files (or pipes).  The PMDA
supports both sampled and event-style metrics.
# end pcp-pmda-logger

#
# pcp-pmda-mailq
#
%package pmda-mailq
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the sendmail queue
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-mailq
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about email queues managed by sendmail.
# end pcp-pmda-mailq

#
# pcp-pmda-mounts
#
%package pmda-mounts
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for filesystem mounts
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-mounts
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about filesystem mounts.
# end pcp-pmda-mounts

#
# pcp-pmda-nvidia-gpu
#
%package pmda-nvidia-gpu
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the Nvidia GPU
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-nvidia-gpu
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Nvidia GPUs.
# end pcp-pmda-nvidia-gpu

#
# pcp-pmda-roomtemp
#
%package pmda-roomtemp
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for the room temperature
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-roomtemp
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about the room temperature.
# end pcp-pmda-roomtemp

#
# pcp-pmda-sendmail
#
%package pmda-sendmail
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for Sendmail
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-sendmail
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about Sendmail traffic.
# end pcp-pmda-sendmail

#
# pcp-pmda-shping
#
%package pmda-shping
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for shell command responses
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-shping
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about quality of service and response time measurements of
arbitrary shell commands.
# end pcp-pmda-shping

#
# pcp-pmda-smart
#
%package pmda-smart
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for S.M.A.R.T values
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: smartmontools
%description pmda-smart
This package contains the PCP Performance Metric Domain Agent (PMDA) for
collecting metrics of disk S.M.A.R.T values making use of data from the
smartmontools package.
#end pcp-pmda-smart

#
# pcp-pmda-summary
#
%package pmda-summary
License: GPLv2+
Summary: Performance Co-Pilot (PCP) summary metrics from pmie
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-summary
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about other installed PMDAs.
# end pcp-pmda-summary

%if !%{disable_systemd}
#
# pcp-pmda-systemd
#
%package pmda-systemd
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics from the Systemd journal
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-systemd
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics from the Systemd journal.
# end pcp-pmda-systemd
%endif

#
# pcp-pmda-trace
#
%package pmda-trace
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics for application tracing
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-trace
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about trace performance data in applications.
# end pcp-pmda-trace

#
# pcp-pmda-weblog
#
%package pmda-weblog
License: GPLv2+
Summary: Performance Co-Pilot (PCP) metrics from web server logs
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
%description pmda-weblog
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting metrics about web server logs.
# end pcp-pmda-weblog
# end C pmdas

%package zeroconf
License: GPLv2+
Summary: Performance Co-Pilot (PCP) Zeroconf Package
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: pcp-system-tools = %{version}-%{release}
Requires: pcp-doc = %{version}-%{release}
Requires: pcp-pmda-dm = %{version}-%{release}
%if !%{disable_python2} || !%{disable_python3}
Requires: pcp-pmda-nfsclient = %{version}-%{release}
Requires: pcp-pmda-openmetrics = %{version}-%{release}
%endif
%description zeroconf
This package contains configuration tweaks and files to increase metrics
gathering frequency, several extended pmlogger configurations, as well as
automated pmie diagnosis, alerting and self-healing for the localhost.

%if !%{disable_python2}
#
# python2-pcp. This is the PCP library bindings for python.
#
%package -n %{__python2}-pcp
License: GPLv2+
Summary: Performance Co-Pilot (PCP) Python bindings and documentation
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
# on these platforms, python2-pcp replaces python-pcp
Obsoletes: python-pcp < %{version}
Requires: %{__python2}

%description -n %{__python2}-pcp
This python PCP module contains the language bindings for
Performance Metric API (PMAPI) monitor tools and Performance
Metric Domain Agent (PMDA) collector tools written in Python.
%endif

%if !%{disable_python3}
#
# python3-pcp. This is the PCP library bindings for python3.
#
%package -n python3-pcp
License: GPLv2+
Summary: Performance Co-Pilot (PCP) Python3 bindings and documentation
URL: https://pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: python3

%description -n python3-pcp
This python PCP module contains the language bindings for
Performance Metric API (PMAPI) monitor tools and Performance
Metric Domain Agent (PMDA) collector tools written in Python3.
%endif

%if !%{disable_python2} || !%{disable_python3}
#
# pcp-system-tools
#
%package system-tools
License: GPLv2+
Summary: Performance Co-Pilot (PCP) System and Monitoring Tools
URL: https://pcp.io
%if !%{disable_python3}
Requires: python3-pcp = %{version}-%{release}
%else
Requires: %{__python2}-pcp = %{version}-%{release}
%endif
%if !%{disable_dstat}
# https://fedoraproject.org/wiki/Packaging:Guidelines "Renaming/Replacing Existing Packages"
Provides: dstat = %{version}-%{release}
Provides: /usr/bin/dstat
Obsoletes: dstat <= 0.8
%endif

%description system-tools
This PCP module contains additional system monitoring tools written
in the Python language.
%endif

#
# pcp-doc package
#
%package doc
License: GPLv2+ and CC-BY
%if !%{disable_noarch}
BuildArch: noarch
%endif
Summary: Documentation and tutorial for the Performance Co-Pilot
URL: https://pcp.io
# http://fedoraproject.org/wiki/Packaging:Conflicts "Splitting Packages"
# (all man pages migrated to pcp-doc during great package split of '15)
Conflicts: pcp-pmda-infiniband < 3.10.5

%description doc
Documentation and tutorial for the Performance Co-Pilot
Performance Co-Pilot (PCP) provides a framework and services to support
system-level performance monitoring and performance management.

The pcp-doc package provides useful information on using and
configuring the Performance Co-Pilot (PCP) toolkit for system
level performance management.  It includes tutorials, HOWTOs,
and other detailed documentation about the internals of core
PCP utilities and daemons, and the PCP graphical tools.

#
# pcp-selinux package
#
%if !%{disable_selinux}
%package selinux
License: GPLv2+ and CC-BY
Summary: Selinux policy package
URL: https://pcp.io
BuildRequires: selinux-policy-devel
BuildRequires: selinux-policy-targeted
BuildRequires: setools-console
Requires: policycoreutils selinux-policy-targeted

%description selinux
This package contains SELinux support for PCP.  The package contains
interface rules, type enforcement and file context adjustments for an
updated policy package.
%endif

%prep
%autosetup -p1

%build
# the buildsubdir macro gets defined in %%setup and is apparently only available in the next step (i.e. the %%build step)
%global __strip %{_builddir}/%{?buildsubdir}/build/rpm/custom-strip

# fix up build version
_build=`echo %{release} | sed -e 's/\..*$//'`
sed -i "/PACKAGE_BUILD/s/=[0-9]*/=$_build/" VERSION.pcp

%if !%{disable_python2} && 0%{?default_python} != 3
export PYTHON=python%{?default_python}
%endif
%configure %{?_with_initd} %{?_with_doc} %{?_with_dstat} %{?_with_ib} %{?_with_gfs2} %{?_with_statsd} %{?_with_perfevent} %{?_with_bcc} %{?_with_bpf} %{?_with_bpftrace} %{?_with_json} %{?_with_mongodb} %{?_with_snmp} %{?_with_nutcracker} %{?_with_python2}
make %{?_smp_mflags} default_pcp

%install
rm -Rf $RPM_BUILD_ROOT
BACKDIR=`pwd`
NO_CHOWN=true
DIST_ROOT=$RPM_BUILD_ROOT
DIST_TMPFILES=$BACKDIR/install.tmpfiles
DIST_MANIFEST=$BACKDIR/install.manifest
export NO_CHOWN DIST_ROOT DIST_MANIFEST DIST_TMPFILES
rm -f $DIST_MANIFEST $DIST_TMPFILES
make install_pcp

### TODO: remove these by incorporating into the actual build

# Fix stuff we do/don't want to ship
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a
sed -i -e '/\.a$/d' $DIST_MANIFEST

# remove sheet2pcp until BZ 830923 and BZ 754678 are resolved.
rm -f $RPM_BUILD_ROOT/%{_bindir}/sheet2pcp $RPM_BUILD_ROOT/%{_mandir}/man1/sheet2pcp.1*
sed -i -e '/sheet2pcp/d' $DIST_MANIFEST

# remove {config,platform}sz.h as these are not multilib friendly.
rm -f $RPM_BUILD_ROOT/%{_includedir}/pcp/configsz.h
sed -i -e '/configsz.h/d' $DIST_MANIFEST
rm -f $RPM_BUILD_ROOT/%{_includedir}/pcp/platformsz.h
sed -i -e '/platformsz.h/d' $DIST_MANIFEST
%if %{disable_infiniband}
# remove pmdainfiniband on platforms lacking IB devel packages.
rm -f $RPM_BUILD_ROOT/%{_pmdasdir}/ib
rm -fr $RPM_BUILD_ROOT/%{_pmdasdir}/infiniband
%endif

%if %{disable_selinux}
rm -fr $RPM_BUILD_ROOT/%{_selinuxdir}
%endif

# Fedora and RHEL default local only access for pmcd and pmlogger
sed -i -e '/^# .*_LOCAL=1/s/^# //' $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/{pmcd,pmlogger}

# default chkconfig off (all RPM platforms)
for f in $RPM_BUILD_ROOT/%{_initddir}/{pcp,pmcd,pmlogger,pmie,pmproxy}; do
    test -f "$f" || continue
    sed -i -e '/^# chkconfig/s/:.*$/: - 95 05/' -e '/^# Default-Start:/s/:.*$/:/' $f
done

### end TODO

PCP_CONF=$BACKDIR/src/include/pcp.conf
export PCP_CONF
. $BACKDIR/src/include/pcp.env
CFGFILELIST=`ls -1 $BACKDIR/debian/pcp-conf.{install,dirs}`
LIBFILELIST=`ls -1 $BACKDIR/debian/lib*.{install,dirs} | grep -F -v -- -dev.`
DEVFILELIST=`ls -1 $BACKDIR/debian/lib*-dev.{install,dirs}`

# Package split: pcp{-conf,-libs,-libs-devel,-testsuite,-import-*,-export-*}...
# The above list is ordered by file selection; files for each package are
# removed from a global set, then the base package catches all remaining.
sed -e 's/^/\//' $CFGFILELIST >pcp-conf-files
sed -e 's/^/\//' $LIBFILELIST >pcp-libs-files
sed -e 's/^/\//' $DEVFILELIST >pcp-devel-files
grep "\.h$" $DEVFILELIST | cut -f2 -d":" >pcp-libs-devel-files
grep "\.pc$" $DEVFILELIST | cut -f2 -d":" >>pcp-libs-devel-files
grep "\.so$" $DEVFILELIST | cut -f2 -d":" >>pcp-libs-devel-files
grep "\.a$" $DEVFILELIST | cut -f2 -d":" >>pcp-libs-devel-files
sed -i -e 's/^/\//' pcp-libs-devel-files
sed -i '/.h$/d' pcp-devel-files
sed -i '/.pc$/d' pcp-devel-files
sed -i '/.so$/d' pcp-devel-files
sed -i '/.a$/d' pcp-devel-files
sed -i '/\/man\//d' pcp-devel-files
sed -i '/\/include\//d' pcp-devel-files

# some special cases for devel
awk '{print $NF}' $DIST_MANIFEST |\
grep -E 'pcp/(examples|demos)|(etc/pcp|pcp/pmdas)/(sample|simple|trivial|txmon)|bin/(pmdbg|pmclient|pmerr|genpmda)' | grep -E -v tutorials >>pcp-devel-files

# Patterns for files to be marked %%config(noreplace).
# Note: /etc/pcp.{conf,env,sh} are %%config but not noreplace
# and are treated specially below.
cat >confpath.list <<EOF
etc/zabbix/zabbix_agentd.d/
etc/sysconfig/
etc/cron.d/
etc/sasl2/
etc/pcp/
EOF

# functions to manipulate the manifest of files - keeping
# or culling given (or common) patterns from the stream.
keep() {
    grep -E $@ || return 0
}
cull() {
    grep -E -v $@ || return 0
}
total_manifest() {
    awk '{print $NF}' $DIST_MANIFEST
}
basic_manifest() {
    total_manifest | cull '/pcp-doc/|/testsuite/|/man/|pcp/examples/'
}

#
# Files for the various subpackages.  We use these subpackages
# to isolate the (somewhat exotic) dependencies for these tools.
# Likewise, for the pcp-pmda and pcp-testsuite subpackages.
#
total_manifest | keep 'tutorials|/html/|pcp-doc|man.*\.[1-9].*' | cull 'out' >pcp-doc-files
total_manifest | keep 'testsuite|pcpqa|etc/systemd/system|libpcp_fault|pcp/fault.h|pmcheck/pmda-sample' >pcp-testsuite-files

%if !%{disable_selinux}
basic_manifest | keep 'selinux' | cull 'tmp|testsuite' >pcp-selinux-files
%endif
basic_manifest | keep 'zeroconf|daily[-_]report|/sa$' | cull 'pmcheck' >pcp-zeroconf-files
basic_manifest | grep -E -e 'pmiostat|pmrep|dstat|htop|pcp2csv' \
   -e 'pcp-atop|pcp-dmcache|pcp-dstat|pcp-free' \
   -e 'pcp-htop|pcp-ipcs|pcp-iostat|pcp-lvmcache|pcp-mpstat' \
   -e 'pcp-numastat|pcp-pidstat|pcp-shping|pcp-ss' \
   -e 'pcp-tapestat|pcp-uptime|pcp-verify|pcp-xsos' | \
   cull 'selinux|pmlogconf|pmieconf|pmrepconf' >pcp-system-tools-files
basic_manifest | keep 'sar2pcp' >pcp-import-sar2pcp-files
basic_manifest | keep 'iostat2pcp' >pcp-import-iostat2pcp-files
basic_manifest | keep 'sheet2pcp' >pcp-import-sheet2pcp-files
basic_manifest | keep 'mrtg2pcp' >pcp-import-mrtg2pcp-files
basic_manifest | keep 'ganglia2pcp' >pcp-import-ganglia2pcp-files
basic_manifest | keep 'collectl2pcp' >pcp-import-collectl2pcp-files
basic_manifest | keep 'pcp2elasticsearch' >pcp-export-pcp2elasticsearch-files
basic_manifest | keep 'pcp2influxdb' >pcp-export-pcp2influxdb-files
basic_manifest | keep 'pcp2graphite' >pcp-export-pcp2graphite-files
basic_manifest | keep 'pcp2json' >pcp-export-pcp2json-files
basic_manifest | keep 'pcp2spark' >pcp-export-pcp2spark-files
basic_manifest | keep 'pcp2xml' >pcp-export-pcp2xml-files
basic_manifest | keep 'pcp2zabbix' >pcp-export-pcp2zabbix-files
basic_manifest | keep 'zabbix|zbxpcp' | cull pcp2zabbix >pcp-export-zabbix-agent-files
basic_manifest | keep '(etc/pcp|pmdas)/activemq(/|$)' >pcp-pmda-activemq-files
basic_manifest | keep '(etc/pcp|pmdas)/apache(/|$)' >pcp-pmda-apache-files
basic_manifest | keep '(etc/pcp|pmdas)/bash(/|$)' >pcp-pmda-bash-files
basic_manifest | keep '(etc/pcp|pmdas)/bcc(/|$)' >pcp-pmda-bcc-files
basic_manifest | keep '(etc/pcp|pmdas)/bind2(/|$)' >pcp-pmda-bind2-files
basic_manifest | keep '(etc/pcp|pmdas)/bonding(/|$)' >pcp-pmda-bonding-files
basic_manifest | keep '(etc/pcp|pmdas)/cifs(/|$)' >pcp-pmda-cifs-files
basic_manifest | keep '(etc/pcp|pmdas)/cisco(/|$)' >pcp-pmda-cisco-files
basic_manifest | keep '(etc/pcp|pmdas)/dbping(/|$)' >pcp-pmda-dbping-files
basic_manifest | keep '(etc/pcp|pmdas|pmieconf)/dm(/|$)' >pcp-pmda-dm-files
basic_manifest | keep '(etc/pcp|pmdas)/docker(/|$)' >pcp-pmda-docker-files
basic_manifest | keep '(etc/pcp|pmdas)/ds389log(/|$)' >pcp-pmda-ds389log-files
basic_manifest | keep '(etc/pcp|pmdas)/ds389(/|$)' >pcp-pmda-ds389-files
basic_manifest | keep '(etc/pcp|pmdas)/elasticsearch(/|$)' >pcp-pmda-elasticsearch-files
basic_manifest | keep '(etc/pcp|pmdas)/gfs2(/|$)' >pcp-pmda-gfs2-files
basic_manifest | keep '(etc/pcp|pmdas)/gluster(/|$)' >pcp-pmda-gluster-files
basic_manifest | keep '(etc/pcp|pmdas)/gpfs(/|$)' >pcp-pmda-gpfs-files
basic_manifest | keep '(etc/pcp|pmdas)/gpsd(/|$)' >pcp-pmda-gpsd-files
basic_manifest | keep '(etc/pcp|pmdas)/haproxy(/|$)' >pcp-pmda-haproxy-files
basic_manifest | keep '(etc/pcp|pmdas)/infiniband(/|$)' >pcp-pmda-infiniband-files
basic_manifest | keep '(etc/pcp|pmdas)/json(/|$)' >pcp-pmda-json-files
%if %{with libvirt}
basic_manifest | keep '(etc/pcp|pmdas)/libvirt(/|$)' >pcp-pmda-libvirt-files
%endif
basic_manifest | keep '(etc/pcp|pmdas)/lio(/|$)' >pcp-pmda-lio-files
basic_manifest | keep '(etc/pcp|pmdas)/lmsensors(/|$)' >pcp-pmda-lmsensors-files
basic_manifest | keep '(etc/pcp|pmdas)/logger(/|$)' >pcp-pmda-logger-files
basic_manifest | keep '(etc/pcp|pmdas)/lustre(/|$)' >pcp-pmda-lustre-files
basic_manifest | keep '(etc/pcp|pmdas)/lustrecomm(/|$)' >pcp-pmda-lustrecomm-files
basic_manifest | keep '(etc/pcp|pmdas)/memcache(/|$)' >pcp-pmda-memcache-files
basic_manifest | keep '(etc/pcp|pmdas)/mailq(/|$)' >pcp-pmda-mailq-files
basic_manifest | keep '(etc/pcp|pmdas)/mic(/|$)' >pcp-pmda-mic-files
basic_manifest | keep '(etc/pcp|pmdas)/mounts(/|$)' >pcp-pmda-mounts-files
basic_manifest | keep '(etc/pcp|pmdas)/mysql(/|$)' >pcp-pmda-mysql-files
basic_manifest | keep '(etc/pcp|pmdas)/named(/|$)' >pcp-pmda-named-files
basic_manifest | keep '(etc/pcp|pmdas)/netfilter(/|$)' >pcp-pmda-netfilter-files
basic_manifest | keep '(etc/pcp|pmdas)/netcheck(/|$)' >pcp-pmda-netcheck-files
basic_manifest | keep '(etc/pcp|pmdas)/news(/|$)' >pcp-pmda-news-files
basic_manifest | keep '(etc/pcp|pmdas)/nfsclient(/|$)' >pcp-pmda-nfsclient-files
basic_manifest | keep '(etc/pcp|pmdas)/nginx(/|$)' >pcp-pmda-nginx-files
basic_manifest | keep '(etc/pcp|pmdas)/nutcracker(/|$)' >pcp-pmda-nutcracker-files
basic_manifest | keep '(etc/pcp|pmdas)/nvidia(/|$)' >pcp-pmda-nvidia-files
basic_manifest | keep '(etc/pcp|pmdas)/openmetrics(/|$)' >pcp-pmda-openmetrics-files
basic_manifest | keep '(etc/pcp|pmdas|pmieconf)/openvswitch(/|$)' >pcp-pmda-openvswitch-files
basic_manifest | keep '(etc/pcp|pmdas)/oracle(/|$)' >pcp-pmda-oracle-files
basic_manifest | keep '(etc/pcp|pmdas)/pdns(/|$)' >pcp-pmda-pdns-files
basic_manifest | keep '(etc/pcp|pmdas)/perfevent(/|$)' >pcp-pmda-perfevent-files
basic_manifest | keep '(etc/pcp|pmdas)/podman(/|$)' >pcp-pmda-podman-files
basic_manifest | keep '(etc/pcp|pmdas)/postfix(/|$)' >pcp-pmda-postfix-files
basic_manifest | keep '(etc/pcp|pmdas)/postgresql(/|$)' >pcp-pmda-postgresql-files
basic_manifest | keep '(etc/pcp|pmdas)/rabbitmq(/|$)' >pcp-pmda-rabbitmq-files
basic_manifest | keep '(etc/pcp|pmdas)/redis(/|$)' >pcp-pmda-redis-files
basic_manifest | keep '(etc/pcp|pmdas)/roomtemp(/|$)' >pcp-pmda-roomtemp-files
basic_manifest | keep '(etc/pcp|pmdas)/rsyslog(/|$)' >pcp-pmda-rsyslog-files
basic_manifest | keep '(etc/pcp|pmdas)/samba(/|$)' >pcp-pmda-samba-files
basic_manifest | keep '(etc/pcp|pmdas)/sendmail(/|$)' >pcp-pmda-sendmail-files
basic_manifest | keep '(etc/pcp|pmdas)/shping(/|$)' >pcp-pmda-shping-files
basic_manifest | keep '(etc/pcp|pmdas)/slurm(/|$)' >pcp-pmda-slurm-files
basic_manifest | keep '(etc/pcp|pmdas)/smart(/|$)' >pcp-pmda-smart-files
basic_manifest | keep '(etc/pcp|pmdas)/snmp(/|$)' >pcp-pmda-snmp-files
basic_manifest | keep '(etc/pcp|pmdas)/summary(/|$)' >pcp-pmda-summary-files
basic_manifest | keep '(etc/pcp|pmdas)/systemd(/|$)' >pcp-pmda-systemd-files
basic_manifest | keep '(etc/pcp|pmdas)/trace(/|$)' >pcp-pmda-trace-files
basic_manifest | keep '(etc/pcp|pmdas)/unbound(/|$)' >pcp-pmda-unbound-files
basic_manifest | keep '(etc/pcp|pmdas)/weblog(/|$)' >pcp-pmda-weblog-files
basic_manifest | keep '(etc/pcp|pmdas)/zimbra(/|$)' >pcp-pmda-zimbra-files
basic_manifest | keep '(etc/pcp|pmdas)/zswap(/|$)' >pcp-pmda-zswap-files

rm -f packages.list
for pmda_package in \
    activemq apache \
    bash bcc bind2 bonding \
    cifs cisco \
    dbping docker dm ds389 ds389log \
    elasticsearch \
    gfs2 gluster gpfs gpsd \
    haproxy \
    infiniband \
    json \
    libvirt lio lmsensors logger lustre lustrecomm \
    mailq memcache mic mounts mysql \
    named netcheck netfilter news nfsclient nginx \
    nutcracker nvidia \
    openmetrics openvswitch oracle \
    pdns perfevent podman postfix postgresql \
    rabbitmq redis roomtemp rpm rsyslog \
    samba sendmail shping slurm smart snmp \
    summary systemd \
    unbound \
    trace \
    weblog \
    zimbra zswap ; \
do \
    pmda_packages="$pmda_packages pcp-pmda-$pmda_package"; \
done

for import_package in \
    collectl2pcp iostat2pcp ganglia2pcp mrtg2pcp sar2pcp sheet2pcp ; \
do \
    import_packages="$import_packages pcp-import-$import_package"; \
done

for export_package in \
    pcp2elasticsearch pcp2graphite pcp2influxdb pcp2json \
    pcp2spark pcp2xml pcp2zabbix zabbix-agent ; \
do \
    export_packages="$export_packages pcp-export-$export_package"; \
done

for subpackage in \
    pcp-conf pcp-doc pcp-libs pcp-devel pcp-libs-devel \
    pcp-selinux pcp-system-tools pcp-testsuite pcp-zeroconf \
    $pmda_packages $import_packages $export_packages ; \
do \
    echo $subpackage >> packages.list; \
done

rm -f *-files.rpm *-tmpfiles.rpm
echo $DIST_MANIFEST
sort -u $DIST_MANIFEST | awk '
function loadfiles(files) {
    system ("touch " files"-files");
    filelist=files"-files";
    while (getline < filelist) {
        if (length(pkg[$0]) > 0 && pkg[$0] != files)
            print "Dup: ", $0, " package: ", pkg[$0], " and ", files;
        if (length(pkg[$0]) == 0)
            pkg[$0] = files;
    }
}
BEGIN {
    while (getline < "packages.list") loadfiles($0);
    while (getline < "confpath.list") conf[nconf++]=$0;
}
{
    if (pkg[$NF]) p=pkg[$NF];
    else p="pcp";
    f=p"-files.rpm";
}
$1 == "d" {
            if (match ($5, "'$PCP_RUN_DIR'")) {
                printf ("%%%%ghost ") >> f;
            }
            if (match ($5, "'$PCP_VAR_DIR'/testsuite")) {
                $3 = $4 = "pcpqa";
            }
            printf ("%%%%dir %%%%attr(%s,%s,%s) %s\n", $2, $3, $4, $5) >> f
          }
$1 == "f" && $6 ~ "etc/pcp\\.conf" { printf ("%%%%config ") >> f; }
$1 == "f" && $6 ~ "etc/pcp\\.env"  { printf ("%%%%config ") >> f; }
$1 == "f" && $6 ~ "etc/pcp\\.sh"   { printf ("%%%%config ") >> f; }
$1 == "f" {
            for (i=0; i < nconf; i++) {
                if ($6 ~ conf[i]) {
                    printf ("%%%%config(noreplace) ") >> f;
                    break;
                }
            }
            if (match ($6, "'$PCP_VAR_DIR'/testsuite")) {
                $3 = $4 = "pcpqa";
            }
            if (match ($6, "'$PCP_MAN_DIR'") || match ($6, "'$PCP_DOC_DIR'")) {
                printf ("%%%%doc ") >> f;
            }
            printf ("%%%%attr(%s,%s,%s) %s\n", $2, $3, $4, $6) >> f
          }
$1 == "l" {
%if !%{disable_systemd}
            if (match ($3, "'$PCP_VAR_DIR'")) {
                print $3 >> p"-tmpfiles";
                if (length(tmpfiles[p]) == 0) {
                    printf ("'$PCP_SYSTEMDTMPFILES_DIR'/%s.conf\n", p) >> f;
                    tmpfiles[p] = p;
                }
            }
%endif
            print $3 >> f;
          }'

%if !%{disable_systemd}
mkdir -p $DIST_ROOT/$PCP_SYSTEMDTMPFILES_DIR
sort -u $DIST_TMPFILES | awk '
function loadtmpfiles(files) {
    system ("touch " files"-tmpfiles");
    filelist=files"-tmpfiles";
    while (getline < filelist) {
        if (pkg[$0] && pkg[$0] != files)
            print "Dup: ", $0, " package: ", pkg[$0], " and ", files;
        pkg[$0] = files;
    }
}
BEGIN {
    while (getline < "packages.list") loadtmpfiles($0);
}
{
    if (pkg[$2]) p=pkg[$2];
    else p="pcp";
    f=p".conf";
    printf ("%s\n", $0) >> f;
}'

for tmpfile in *.conf ; \
do \
    mv $tmpfile $DIST_ROOT/$PCP_SYSTEMDTMPFILES_DIR/$tmpfile; \
done
%endif
%pre testsuite
%if !%{disable_selinux}
%selinux_relabel_pre -s targeted
%endif
getent group pcpqa >/dev/null || groupadd -r pcpqa
getent passwd pcpqa >/dev/null || \
  useradd -c "PCP Quality Assurance" -g pcpqa -d %{_testsdir} -M -r -s /bin/bash pcpqa 2>/dev/null
test -d %{_testsdir} || mkdir -p -m 755 %{_testsdir}
chown -R pcpqa:pcpqa %{_testsdir} 2>/dev/null
exit 0

%post testsuite
%if !%{disable_selinux}
PCP_SELINUX_DIR=%{_selinuxdir}
semodule -r pcpqa >/dev/null 2>&1 || true
%selinux_modules_install -s targeted "$PCP_SELINUX_DIR/pcp-testsuite.pp.bz2"
%selinux_relabel_post -s targeted
%endif
chown -R pcpqa:pcpqa %{_testsdir} 2>/dev/null
%if 0%{?rhel}
%if !%{disable_systemd}
    systemctl restart pcp-reboot-init pmcd pmlogger >/dev/null 2>&1
    systemctl enable pcp-reboot-init pmcd pmlogger >/dev/null 2>&1
%else
    /sbin/chkconfig --add pmcd >/dev/null 2>&1
    /sbin/chkconfig --add pmlogger >/dev/null 2>&1
    /sbin/service pmcd condrestart
    /sbin/service pmlogger condrestart
%endif
%endif
exit 0

%if !%{disable_selinux}
%postun testsuite
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s targeted pcp-testsuite
    %selinux_relabel_post -s targeted
fi
%endif

%pre
getent group pcp >/dev/null || groupadd -r pcp
getent passwd pcp >/dev/null || \
  useradd -c "Performance Co-Pilot" -g pcp -d %{_localstatedir}/lib/pcp -M -r -s /sbin/nologin pcp
exit 0

%if !%{disable_systemd}
%preun pmda-systemd
%{pmda_remove "$1" "systemd"}
%endif

%if !%{disable_infiniband}
%preun pmda-infiniband
%{pmda_remove "$1" "infiniband"}
%endif

%if !%{disable_perfevent}
%preun pmda-perfevent
%{pmda_remove "$1" "perfevent"}
%endif

%if !%{disable_podman}
%preun pmda-podman
%{pmda_remove "$1" "podman"}
%endif

%if !%{disable_json}
%preun pmda-json
%{pmda_remove "$1" "json"}
%endif

%preun pmda-nginx
%{pmda_remove "$1" "nginx"}

%preun pmda-oracle
%{pmda_remove "$1" "oracle"}

%preun pmda-postgresql
%{pmda_remove "$1" "postgresql"}

%preun pmda-postfix
%{pmda_remove "$1" "postfix"}

%preun pmda-elasticsearch
%{pmda_remove "$1" "elasticsearch"}

%preun pmda-openvswitch
%{pmda_remove "$1" "openvswitch"}

%preun pmda-rabbitmq
%{pmda_remove "$1" "rabbitmq"}

%if !%{disable_snmp}
%preun pmda-snmp
%{pmda_remove "$1" "snmp"}
%endif

%preun pmda-mysql
%{pmda_remove "$1" "mysql"}

%preun pmda-activemq
%{pmda_remove "$1" "activemq"}

%preun pmda-bind2
%{pmda_remove "$1" "bind2"}

%preun pmda-bonding
%{pmda_remove "$1" "bonding"}

%preun pmda-dbping
%{pmda_remove "$1" "dbping"}

%preun pmda-docker
%{pmda_remove "$1" "docker"}

%preun pmda-ds389
%{pmda_remove "$1" "ds389"}

%preun pmda-ds389log
%{pmda_remove "$1" "ds389log"}

%preun pmda-gpfs
%{pmda_remove "$1" "gpfs"}

%preun pmda-gpsd
%{pmda_remove "$1" "gpsd"}

%preun pmda-lio
%{pmda_remove "$1" "lio"}

%preun pmda-openmetrics
%{pmda_remove "$1" "openmetrics"}

%preun pmda-lustre
%{pmda_remove "$1" "lustre"}

%preun pmda-lustrecomm
%{pmda_remove "$1" "lustrecomm"}

%preun pmda-memcache
%{pmda_remove "$1" "memcache"}

%preun pmda-named
%{pmda_remove "$1" "named"}

%preun pmda-netfilter
%{pmda_remove "$1" "netfilter"}

%preun pmda-news
%{pmda_remove "$1" "news"}

%preun pmda-nfsclient
%{pmda_remove "$1" "nfsclient"}

%if !%{disable_nutcracker}
%preun pmda-nutcracker
%{pmda_remove "$1" "nutcracker"}
%endif

%preun pmda-pdns
%{pmda_remove "$1" "pdns"}

%preun pmda-rsyslog
%{pmda_remove "$1" "rsyslog"}

%preun pmda-redis
%{pmda_remove "$1" "redis"}

%preun pmda-samba
%{pmda_remove "$1" "samba"}

%preun pmda-zimbra
%{pmda_remove "$1" "zimbra"}

%preun pmda-dm
%{pmda_remove "$1" "dm"}

%if !%{disable_bcc}
%preun pmda-bcc
%{pmda_remove "$1" "bcc"}
%endif

%if !%{disable_python2} || !%{disable_python3}
%preun pmda-gluster
%{pmda_remove "$1" "gluster"}

%preun pmda-zswap
%{pmda_remove "$1" "zswap"}

%preun pmda-unbound
%{pmda_remove "$1" "unbound"}

%preun pmda-mic
%{pmda_remove "$1" "mic"}

%preun pmda-haproxy
%{pmda_remove "$1" "haproxy"}

%if %{with libvirt}
%preun pmda-libvirt
%{pmda_remove "$1" "libvirt"}
%endif

%preun pmda-lmsensors
%{pmda_remove "$1" "lmsensors"}

%preun pmda-netcheck
%{pmda_remove "$1" "netcheck"}

%endif

%preun pmda-apache
%{pmda_remove "$1" "apache"}

%preun pmda-bash
%{pmda_remove "$1" "bash"}

%preun pmda-cifs
%{pmda_remove "$1" "cifs"}

%preun pmda-cisco
%{pmda_remove "$1" "cisco"}

%if !%{disable_gfs2}
%preun pmda-gfs2
%{pmda_remove "$1" "gfs2"}
%endif

%preun pmda-logger
%{pmda_remove "$1" "logger"}

%preun pmda-mailq
%{pmda_remove "$1" "mailq"}

%preun pmda-mounts
%{pmda_remove "$1" "mounts"}

%preun pmda-nvidia-gpu
%{pmda_remove "$1" "nvidia"}

%preun pmda-roomtemp
%{pmda_remove "$1" "roomtemp"}

%preun pmda-sendmail
%{pmda_remove "$1" "sendmail"}

%preun pmda-shping
%{pmda_remove "$1" "shping"}

%preun pmda-smart
%{pmda_remove "$1" "smart"}

%preun pmda-summary
%{pmda_remove "$1" "summary"}

%preun pmda-trace
%{pmda_remove "$1" "trace"}

%preun pmda-weblog
%{pmda_remove "$1" "weblog"}

%preun
if [ "$1" -eq 0 ]
then
    # stop daemons before erasing the package
    %if !%{disable_systemd}
       %systemd_preun pmlogger_check.timer pmlogger_daily.timer pmlogger.service pmie_check.timer pmie_daily.timer pmie.service pmproxy.service pmfind.service pmcd.service pcp-reboot-init.service

       systemctl stop pmlogger.service pmie.service pmproxy.service pmfind.service pmcd.service pcp-reboot-init.service >/dev/null 2>&1
    %else
       /sbin/service pmlogger stop >/dev/null 2>&1
       /sbin/service pmie stop >/dev/null 2>&1
       /sbin/service pmproxy stop >/dev/null 2>&1
       /sbin/service pmcd stop >/dev/null 2>&1

       /sbin/chkconfig --del pcp >/dev/null 2>&1
       /sbin/chkconfig --del pmcd >/dev/null 2>&1
       /sbin/chkconfig --del pmlogger >/dev/null 2>&1
       /sbin/chkconfig --del pmie >/dev/null 2>&1
       /sbin/chkconfig --del pmproxy >/dev/null 2>&1
    %endif
    # cleanup namespace state/flag, may still exist
    PCP_PMNS_DIR=%{_pmnsdir}
    rm -f "$PCP_PMNS_DIR/.NeedRebuild" >/dev/null 2>&1
fi

%post zeroconf
PCP_PMDAS_DIR=%{_pmdasdir}
PCP_SYSCONFIG_DIR=%{_sysconfdir}/sysconfig
PCP_PMCDCONF_PATH=%{_confdir}/pmcd/pmcd.conf
PCP_PMIECONFIG_DIR=%{_ieconfigdir}
# auto-install important PMDAs for RH Support (if not present already)
for PMDA in dm nfsclient openmetrics ; do
    if ! grep -q "$PMDA/pmda$PMDA" "$PCP_PMCDCONF_PATH"
    then
        %{install_file "$PCP_PMDAS_DIR/$PMDA" .NeedInstall}
    fi
done
# auto-enable these usually optional pmie rules
%{run_pmieconf "$PCP_PMIECONFIG_DIR" config.default dmthin}
# managed via /usr/lib/systemd/system-preset/90-default.preset nowadays:
%if 0%{?rhel} > 0 && 0%{?rhel} < 10
%if !%{disable_systemd}
    systemctl restart pmcd pmlogger pmie >/dev/null 2>&1
    systemctl enable pmcd pmlogger pmie >/dev/null 2>&1
%else
    /sbin/chkconfig --add pmcd >/dev/null 2>&1
    /sbin/chkconfig --add pmlogger >/dev/null 2>&1
    /sbin/chkconfig --add pmie >/dev/null 2>&1
    /sbin/service pmcd condrestart
    /sbin/service pmlogger condrestart
    /sbin/service pmie condrestart
%endif
%endif

%post
PCP_PMNS_DIR=%{_pmnsdir}
PCP_LOG_DIR=%{_logsdir}
%{install_file "$PCP_PMNS_DIR" .NeedRebuild}
%{install_file "$PCP_LOG_DIR/pmlogger" .NeedRewrite}
%if !%{disable_systemd}
    # clean up any stale symlinks for deprecated pm*-poll services
    rm -f %{_sysconfdir}/systemd/system/pm*.requires/pm*-poll.* >/dev/null 2>&1 || true
    systemctl restart pcp-reboot-init >/dev/null 2>&1
    systemctl enable pcp-reboot-init >/dev/null 2>&1

    %systemd_postun_with_restart pmcd.service
    %systemd_post pmcd.service
    %systemd_postun_with_restart pmlogger.service
    %systemd_post pmlogger.service
    %systemd_postun_with_restart pmie.service
    %systemd_post pmie.service
    %systemd_postun_with_restart pmproxy.service
    %systemd_post pmproxy.service
    %systemd_post pmfind.service
%else
    /sbin/chkconfig --add pmcd >/dev/null 2>&1
    /sbin/service pmcd condrestart
    /sbin/chkconfig --add pmlogger >/dev/null 2>&1
    /sbin/service pmlogger condrestart
    /sbin/chkconfig --add pmie >/dev/null 2>&1
    /sbin/service pmie condrestart
    /sbin/chkconfig --add pmproxy >/dev/null 2>&1
    /sbin/service pmproxy condrestart
%endif
%{rebuild_pmns "$PCP_PMNS_DIR" .NeedRebuild}

%ldconfig_scriptlets libs

%if !%{disable_selinux}
%pre selinux
%selinux_relabel_pre -s targeted

%post selinux
PCP_SELINUX_DIR=%{_selinuxdir}
semodule -r pcpupstream-container >/dev/null 2>&1 || true
semodule -r pcpupstream-docker >/dev/null 2>&1 || true
semodule -r pcpupstream >/dev/null 2>&1 || true
%selinux_modules_install -s targeted "$PCP_SELINUX_DIR/pcp.pp.bz2"
%selinux_relabel_post -s targeted

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s targeted pcp
    %selinux_relabel_post -s targeted
fi
%endif

%files -f pcp-files.rpm
%doc CHANGELOG COPYING INSTALL.md README.md VERSION.pcp pcp.lsm
%ghost %dir %attr(0775,pcp,pcp) %{_localstatedir}/run/pcp

%files conf -f pcp-conf-files.rpm

%files libs -f pcp-libs-files.rpm

%files libs-devel -f pcp-libs-devel-files.rpm

%files devel -f pcp-devel-files.rpm

%files doc -f pcp-doc-files.rpm

%if !%{disable_selinux}
%files selinux -f pcp-selinux-files.rpm
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/targeted/active/modules/200/pcp
%endif

%files testsuite -f pcp-testsuite-files.rpm

%if !%{disable_infiniband}
%files pmda-infiniband -f pcp-pmda-infiniband-files.rpm
%endif

%if !%{disable_podman}
%files pmda-podman -f pcp-pmda-podman-files.rpm
%endif

%if !%{disable_perfevent}
%files pmda-perfevent -f pcp-pmda-perfevent-files.rpm
%endif

%if !%{disable_perl}
%files pmda-activemq -f pcp-pmda-activemq-files.rpm
%endif

%if !%{disable_perl}
%files pmda-bind2 -f pcp-pmda-bind2-files.rpm
%endif

%if !%{disable_nutcracker}
%files pmda-nutcracker -f pcp-pmda-nutcracker-files.rpm
%endif

%if !%{disable_python2} || !%{disable_python3}
%files pmda-elasticsearch -f pcp-pmda-elasticsearch-files.rpm
%endif

%if !%{disable_perl}
%files pmda-redis -f pcp-pmda-redis-files.rpm

%files pmda-bonding -f pcp-pmda-bonding-files.rpm

%files pmda-dbping -f pcp-pmda-dbping-files.rpm

%files pmda-ds389log -f pcp-pmda-ds389log-files.rpm

%files pmda-ds389 -f pcp-pmda-ds389-files.rpm

%files pmda-gpfs -f pcp-pmda-gpfs-files.rpm

%files pmda-gpsd -f pcp-pmda-gpsd-files.rpm

%files pmda-lustre -f pcp-pmda-lustre-files.rpm

%files pmda-memcache -f pcp-pmda-memcache-files.rpm

%files pmda-named -f pcp-pmda-named-files.rpm

%files pmda-netfilter -f pcp-pmda-netfilter-files.rpm

%files pmda-news -f pcp-pmda-news-files.rpm

%files pmda-pdns -f pcp-pmda-pdns-files.rpm

%files pmda-rsyslog -f pcp-pmda-rsyslog-files.rpm

%files pmda-samba -f pcp-pmda-samba-files.rpm

%files pmda-slurm -f pcp-pmda-slurm-files.rpm

%files pmda-zimbra -f pcp-pmda-zimbra-files.rpm
%endif

%files pmda-docker -f pcp-pmda-docker-files.rpm

%files pmda-lustrecomm -f pcp-pmda-lustrecomm-files.rpm

%if !%{disable_perl}
%files pmda-mysql -f pcp-pmda-mysql-files.rpm
%endif

%files pmda-nginx -f pcp-pmda-nginx-files.rpm

%if !%{disable_perl}
%files pmda-postfix -f pcp-pmda-postfix-files.rpm
%endif

%if !%{disable_python2} || !%{disable_python3}
%files pmda-postgresql -f pcp-pmda-postgresql-files.rpm
%endif

%if !%{disable_perl}
%files pmda-oracle -f pcp-pmda-oracle-files.rpm
%endif

%if !%{disable_perl}
%files pmda-snmp -f pcp-pmda-snmp-files.rpm
%endif

%files pmda-dm -f pcp-pmda-dm-files.rpm

%if !%{disable_bcc}
%files pmda-bcc -f pcp-pmda-bcc-files.rpm
%endif

%if !%{disable_python2} || !%{disable_python3}
%files pmda-gluster -f pcp-pmda-gluster-files.rpm

%files pmda-zswap -f pcp-pmda-zswap-files.rpm

%files pmda-unbound -f pcp-pmda-unbound-files.rpm

%files pmda-mic -f pcp-pmda-mic-files.rpm

%files pmda-haproxy -f pcp-pmda-haproxy-files.rpm

%files pmda-lmsensors -f pcp-pmda-lmsensors-files.rpm

%files pmda-netcheck -f pcp-pmda-netcheck-files.rpm

%files pmda-nfsclient -f pcp-pmda-nfsclient-files.rpm

%files pmda-openvswitch -f pcp-pmda-openvswitch-files.rpm

%files pmda-rabbitmq -f pcp-pmda-rabbitmq-files.rpm

%files export-pcp2graphite -f pcp-export-pcp2graphite-files.rpm

%files export-pcp2json -f pcp-export-pcp2json-files.rpm

%files export-pcp2spark -f pcp-export-pcp2spark-files.rpm

%files export-pcp2xml -f pcp-export-pcp2xml-files.rpm

%files export-pcp2zabbix -f pcp-export-pcp2zabbix-files.rpm
%endif

%if !%{disable_python2} || !%{disable_python3}
%files export-pcp2elasticsearch -f pcp-export-pcp2elasticsearch-files.rpm
%endif

%if !%{disable_python2} || !%{disable_python3}
%files export-pcp2influxdb -f pcp-export-pcp2influxdb-files.rpm
%endif

%files export-zabbix-agent -f pcp-export-zabbix-agent-files.rpm

%if !%{disable_json}
%files pmda-json -f pcp-pmda-json-files.rpm
%endif

%if !%{disable_python2} || !%{disable_python3}

%if %{with libvirt}
%files pmda-libvirt -f pcp-pmda-libvirt-files.rpm
%endif

%files pmda-lio -f pcp-pmda-lio-files.rpm

%files pmda-openmetrics -f pcp-pmda-openmetrics-files.rpm
%endif

%files pmda-apache -f pcp-pmda-apache-files.rpm

%files pmda-bash -f pcp-pmda-bash-files.rpm

%files pmda-cifs -f pcp-pmda-cifs-files.rpm

%files pmda-cisco -f pcp-pmda-cisco-files.rpm

%if !%{disable_gfs2}
%files pmda-gfs2 -f pcp-pmda-gfs2-files.rpm
%endif

%files pmda-logger -f pcp-pmda-logger-files.rpm

%files pmda-mailq -f pcp-pmda-mailq-files.rpm

%files pmda-mounts -f pcp-pmda-mounts-files.rpm

%files pmda-nvidia-gpu -f pcp-pmda-nvidia-files.rpm

%files pmda-roomtemp -f pcp-pmda-roomtemp-files.rpm

%files pmda-sendmail -f pcp-pmda-sendmail-files.rpm

%files pmda-shping -f pcp-pmda-shping-files.rpm

%files pmda-smart -f pcp-pmda-smart-files.rpm

%files pmda-summary -f pcp-pmda-summary-files.rpm

%if !%{disable_systemd}
%files pmda-systemd -f pcp-pmda-systemd-files.rpm
%endif

%files pmda-trace -f pcp-pmda-trace-files.rpm

%files pmda-weblog -f pcp-pmda-weblog-files.rpm

%if !%{disable_perl}
%files import-sar2pcp -f pcp-import-sar2pcp-files.rpm

%files import-iostat2pcp -f pcp-import-iostat2pcp-files.rpm

#TODO:
#%%files import-sheet2pcp -f pcp-import-sheet2pcp-files.rpm

%files import-mrtg2pcp -f pcp-import-mrtg2pcp-files.rpm

%files import-ganglia2pcp -f pcp-import-ganglia2pcp-files.rpm
%endif

%files import-collectl2pcp -f pcp-import-collectl2pcp-files.rpm

%if !%{disable_perl}
%files -n perl-PCP-PMDA -f perl-pcp-pmda.list

%files -n perl-PCP-MMV -f perl-pcp-mmv.list

%files -n perl-PCP-LogImport -f perl-pcp-logimport.list

%files -n perl-PCP-LogSummary -f perl-pcp-logsummary.list
%endif

%if !%{disable_python2}
%files -n %{__python2}-pcp -f python-pcp.list.rpm
%endif

%if !%{disable_python3}
%files -n python3-pcp -f python3-pcp.list.rpm
%endif

%files system-tools -f pcp-system-tools-files.rpm

%files zeroconf -f pcp-zeroconf-files.rpm

%changelog
* Wed Mar 05 2025 Sandeep Karambelkar <skarambelkar@microsoft.com> 6.3.2-1
- Initial Azure Linux import from Fedora 42 (license: MIT).
- Fix the build issues for azurelinux
- License verified

* Wed Jan 29 2025 William Cohen <wcohen@redhat.com> - 6.3.2-5
- Backport GCC15 fixes (BZ #2341011)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 27 2024 Richard W.M. Jones <rjones@redhat.com> - 6.3.2-3
- Rebuild for libarrow 18

* Thu Nov 14 2024 Nathan Scott <nathans@redhat.com> - 6.3.2-2
- Back-port upstream bug fixes for pcp-xsos(1).

* Wed Nov 06 2024 Nathan Scott <nathans@redhat.com> - 6.3.2-1
- Update to latest upstream PCP version.

* Tue Sep 17 2024 Nathan Scott <nathans@redhat.com> - 6.3.1-1
- Update to latest upstream PCP version.

* Tue Jul 30 2024 Nathan Scott <nathans@redhat.com> - 6.3.0-2
- Disable perl components on i386 due to time64_t issues.

* Tue Jul 30 2024 Nathan Scott <nathans@redhat.com> - 6.3.0-1
- Updates to PCP selinux policy (BZ #2278017, #2278049, #2278050)
- Resolved pmcheck.1 man page naming conflict (BZ #2290840)
- Reworked time64_t changes for i386 (BZ #2284431)
- Update to latest upstream PCP version.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 13 2024 Jitka Plesnikova <jplesnik@redhat.com> - 6.2.2-7
- Perl 5.40 re-rebuild updated packages

* Thu Jun 13 2024 Python Maint <python-maint@redhat.com> - 6.2.2-6
- Rebuilt for Python 3.13

* Thu Jun 13 2024 Jitka Plesnikova <jplesnik@redhat.com> - 6.2.2-5
- Perl 5.40 rebuild

* Wed Jun 12 2024 Adam Williamson <awilliam@redhat.com> - 6.2.2-4
- Rebuild for Python 3.13

* Mon Jun 10 2024 Nathan Scott <nathans@redhat.com> - 6.2.2-3
- Revert time64_t related changes breaking i386 (BZ 2284431)
- Try again with rebuild for selinux-policy rpmmacro problem.

* Wed May 15 2024 Nathan Scott <nathans@redhat.com> - 6.2.2-1
- Add tmpfiles.d handling for /var/log directories (BZ #2275408)
- Update to latest PCP sources.

* Wed Apr 10 2024 Nathan Scott <nathans@redhat.com> - 6.2.1-1
- Update to latest PCP sources.

* Mon Feb 12 2024 Nathan Scott <nathans@redhat.com> - 6.2.0-1
- Update to latest PCP sources.

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Nov 17 2023 Nathan Scott <nathans@redhat.com> - 6.1.1-1
- Resolves i686/x86_64 conflicts of PCP packages (BZ 2248841)
- Additional selinux policy updates for pmproxy (BZ 2223568)
- Update to latest PCP sources.

* Tue Sep 05 2023 Nathan Scott <nathans@redhat.com> - 6.1.0-1
- Remove unintended pmie logging to syslog (BZ 2223348)
- Update pcp selinux policy to match core (BZ 2223568)
- Resolve pmlogconf SIGABRT during fsync (BZ 2229441)
- Update to latest PCP sources.

* Mon Aug 07 2023 Sam Feifer <samfeifer@fedoraproject.org> - 6.0.5-6
- Improve on pmieconf integration with Event Driven Ansible

* Thu Aug 03 2023 Sam Feifer <samfeifer@fedoraproject.org> - 6.0.5-5
- Fix path for pmie/conf testing rule

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 6.0.5-3
- Perl 5.38 rebuild

* Fri Jul 07 2023 Python Maint <python-maint@redhat.com> - 6.0.5-2
- Rebuilt for Python 3.12

* Mon Jun 26 2023 Nathan Scott <nathans@redhat.com> - 6.0.5-1
- Ensure rotated pmie log files are pcp:pcp owned (BZ 2217209)
- Update to latest PCP sources.

* Mon May 15 2023 Nathan Scott <nathans@redhat.com> - 6.0.4-1
- Rework LOCALHOSTNAME handling in control files (BZ 2172892)

* Thu Feb 23 2023 Nathan Scott <nathans@redhat.com> - 6.0.3-1
- Update to latest PCP sources.

* Mon Feb 13 2023 Nathan Scott <nathans@redhat.com> - 6.0.2-1
- Resolve a dstat swap plugin related failure (BZ 2168774)
- Update to latest PCP sources.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 12 2022 Florian Weimer <fweimer@redhat.com> - 6.0.1-4
- Port configure script to C99

* Thu Nov 03 2022 Jiri Olsa <jolsa@kernel.org> - 6.0.1-3
- rebuilt for libbpf 1.0

* Thu Oct 27 2022 Nathan Scott <nathans@redhat.com> - 6.0.1-1
- Resolve a BPF module related build failure (BZ 2132998)
- Update to latest PCP sources.

* Wed Aug 31 2022 Nathan Scott <nathans@redhat.com> - 6.0.0-1
- Add libpcp/postgresql-pgpool-II-devel conflict (BZ 2100185)
- Remove an invalid path from pmie unit file (BZ 2079793)
- Update to latest PCP sources.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 20 2022 Python Maint <python-maint@redhat.com> - 5.3.7-5
- Rebuilt for Python 3.11

* Fri Jun 17 2022 Nathan Scott <nathans@redhat.com> - 5.3.7-4
- Fix invalid path in pmie.service unit file (BZ 2079793)

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 5.3.7-3
- Rebuilt for Python 3.11

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 5.3.7-2
- Perl 5.36 rebuild

* Tue Apr 05 2022 Nathan Scott <nathans@redhat.com> - 5.3.7-1
- Add disk.wwid aggregated multipath metrics (BZ 1293444)
- Update to latest PCP sources.

* Thu Feb 03 2022 Nathan Scott <nathans@redhat.com> - 5.3.6-2
- Disable package notes to prevent 3rd PMDA build breakage.

* Wed Feb 02 2022 Nathan Scott <nathans@redhat.com> - 5.3.6-1
- Update to latest PCP sources.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 17 2021 Nathan Scott <nathans@redhat.com> - 5.3.5-2
- pmdabcc: resolve compilation issues of some bcc PMDA modules on
  aarch64, ppc64le and s390x (BZ 2024982)
- pmdabpf: support arm and powerpc architectures (BZ 2024980)
- Further improve pmlogger service startup latency (BZ 1973833)
- Additional improvements to farm systemd services (BZ 2030138)
- PMDA indom cache loading performance improvements (BZ 2030122)
- Resilience improvements for the pmproxy service (BZ 2030141)
- Resolve failure in the Nvidia metrics agent (BZ 2030123)
- Updates to pmlogconf persistance changes (BZ 2017632)

* Wed Nov 10 2021 Nathan Scott <nathans@redhat.com> - 5.3.5-1
- Fix pmlogger services systemd killmode warning (BZ 1897945)
- Fix python PMDA interface for python 3.10 (BZ 2020038)
- Update to latest PCP sources.

* Fri Oct 15 2021 Mark Goodwin <mgoodwin@redhat.com> - 5.3.4-2
- Fix pmlogger manual start failure when service is disabled

* Fri Oct 08 2021 Nathan Scott <nathans@redhat.com> - 5.3.4-1
- Update to latest PCP sources.

* Wed Sep 15 2021 Nathan Scott <nathans@redhat.com> - 5.3.3-1
- Update to latest PCP sources.

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 5.3.2-2
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 30 2021 Mark Goodwin <mgoodwin@redhat.com> - 5.3.2-1
- Update to latest PCP sources.

* Fri Jun 04 2021 Nathan Scott <nathans@redhat.com> - 5.3.1-1
- Fix selinux violations for pmdakvm on debugfs (BZ 1929259)
- Update to latest PCP sources.

* Fri Apr 16 2021 Nathan Scott <nathans@redhat.com> - 5.3.0-1
- Added conditional lockdown policy access by pmdakvm (BZ 1929259)
- Update to latest PCP sources.

* Mon Feb 08 2021 Andreas Gerstmayr <agerstmayr@redhat.com> - 5.2.5-2
- Fixed typo in specfile (pcp-testsuite requires pcp-pmda-hacluster
  and pcp-pmda-sockets instead of pcp-pmdas-hacluster etc.)

* Mon Feb 08 2021 Nathan Scott <nathans@redhat.com> - 5.2.5-1
- Update to latest PCP sources.
- Fix pcp-dstat(1) sample count being off-by-one (BZ 1922768)
- Add dstat(1) symlink to pcp-dstat(1) in pcp-doc (BZ 1922771)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 18 2020 Nathan Scott <nathans@redhat.com> - 5.2.3-1
- Update to latest PCP sources.

* Wed Nov 11 2020 Nathan Scott <nathans@redhat.com> - 5.2.2-1
- Update to latest PCP sources.

* Fri Sep 25 2020 Nathan Scott <nathans@redhat.com> - 5.2.1-1
- Update to latest PCP sources.

* Sat Aug 08 2020 Mark Goodwin <mgoodwin@redhat.com> - 5.2.0-1
- FHS compliance in installed /var file locations (BZ 1827441)
- pmproxy intermittently crashes at uv_timer_stop (BZ 1789312)
- Update to latest PCP sources.
- Re-enabled LTO.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Jeff Law <law@redhat.com> - 5.1.1-3
- Disable LTO

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 5.1.1-2
- Perl 5.32 rebuild

* Fri May 29 2020 Mark Goodwin <mgoodwin@redhat.com> - 5.1.1-1
- Rebuild to pick up changed HdrHistogram_c version (BZ 1831502)
- Existing configure macro in pcp-5.1.0 changelog was expanded (BZ 1833876)
- pmdakvm: handle kernel lockdown in integrity mode (BZ 1824297)
- Update to latest PCP sources.

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 5.1.0-2
- Rebuilt for Python 3.9

* Fri Apr 24 2020 Mark Goodwin <mgoodwin@redhat.com> - 5.1.0-1
- pmdakvm: debugfs access is restricted (BZ 1824297)
- error starting pmlogger; pid file not owned by root (BZ 1761962)
- Update to latest PCP sources.

* Wed Mar 11 2020 Mark Goodwin <mgoodwin@redhat.com> - 5.0.3-3
- Resolve pcp-selinux issues causing services failures - (BZ 1810458)

* Mon Mar 02 2020 Mark Goodwin <mgoodwin@redhat.com> - 5.0.3-2
- fix typo in Requires: perl-Time-HiRes affecting pcp-pmda-bind2

* Thu Feb 27 2020 Mark Goodwin <mgoodwin@redhat.com> - 5.0.3-1
- Avoid python ctypes bitfield struct on-stack (BZ 1800685)
- Add dstat support for DM/MD/part devices (BZ 1794273)
- Fix compilation with gcc version 10 (BZ 1793495)
- Fix dstat sub-sample averaging (BZ 1780039)
- Update to latest PCP sources.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 11 2019 Nathan Scott <nathans@redhat.com> - 5.0.2-1
- Resolve fresh install pmlogger timeout bug (BZ 1721223)
- Fix dstat exception writing to a closed fd (BZ 1768619)
- Fix chan lib dependency of pcp-pmda-statsd (BZ 1770815)
- Update to latest PCP sources.

* Mon Nov 04 2019 Nathan Scott <nathans@redhat.com> - 5.0.1-1
- Resolve selinux policy issues in PCP tools (BZ 1743040)
- Update to latest PCP sources.

* Sun Oct 20 2019 Mark Goodwin <mgoodwin@redhat.com> - 5.0.0-2
- various spec fixes for pmdastatsd
- add patch1 to fix pmdastatsd build on rawhide

* Fri Oct 11 2019 Mark Goodwin <mgoodwin@redhat.com> - 5.0.0-1
- Update to latest PCP sources.

* Fri Aug 16 2019 Nathan Scott <nathans@redhat.com> - 4.3.4-1
- Resolve bootup issues with pmlogger service (BZ 1737091, BZ 1721223)
- Resolve selinux policy issues in PCP tools (BZ 1721644, BZ 1711547)
- Update to latest PCP sources.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Mark Goodwin <mgoodwin@redhat.com> - 4.3.3-1
- Resolve segv running pmchart with bogus timezone (BZ 1718948)
- Resolve pmrep wait.formula for collectl-dm-sD and collectl-sD (BZ 1724288)
- Update to latest PCP sources.

* Mon Jun 10 22:13:21 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.3.2-4
- Rebuild for RPM 4.15

* Mon Jun 10 15:42:04 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.3.2-3
- Rebuild for RPM 4.15

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.3.2-2
- Perl 5.30 rebuild

* Fri Apr 26 2019 Mark Goodwin <mgoodwin@redhat.com> - 4.3.2-1
- Resolve selinux policy issues for pmie daemon mode (BZ 1702589)
- Resolve selinux policy issues for BPF permissions (BZ 1693332)
- Further improvements to daily archive processing (BZ 1647390)
- Update to latest PCP sources.

* Wed Feb 27 2019 Mark Goodwin <mgoodwin@redhat.com> - 4.3.1-1
- Fixes pcp-dstat in --full (all instances) mode (BZ 1661912)
- Remove package dependencies on initscripts (BZ 1592380)
- Set include directory for cppcheck use (BZ 1663372)
- Update to latest PCP sources.

* Fri Dec 21 2018 Nathan Scott <nathans@redhat.com> - 4.3.0-1
- Add the dstat -f/--full option to expand instances (BZ 1651536)
- Improve systemd interaction for local pmie (BZ 1650999)
- SELinux is preventing ps from 'search' accesses on the directory
  .config (BZ 1569697)
- SELinux is preventing pmdalinux from 'search' accesses on
  the directory /var/lib/libvirt/images (BZ 1579988)
- SELinux is preventing pmdalinux from 'unix_read' accesses
  on the semáforo Unknown (BZ 1607658)
- SELinux is preventing pmdalinux from 'unix_read' accesses
  on the shared memory Unknown (BZ 1618756, BZ 1619381, BZ 1601721)
- Update to latest PCP sources.

* Fri Nov 16 2018 Mark Goodwin <mgoodwin@redhat.com> - 4.2.0-1
- Resolves dstat packaging issues (BZ 1640912)
- Resolves dstat cursor positioning problem (BZ 1640913)
- Resolve a signal handling issue in dstat shutdown (BZ 1648552)
- Rename variable named await in python code (BZ 1633367)
- New conditionally-built pcp-pmda-podman sub-package.
- SELinux is preventing pmdalinux from 'unix_read' accesses on the shared memory labeled gpsd_t
  (BZ 1626487)
- SELinux is preventing ps from 'search' accesses on the directory .cache
  (BZ 1634205, BZ 1635522)
- SELinux is preventing ps from 'sys_ptrace' accesses on the cap_userns Unknown
  (BZ 1635394)
- PCP SELinux AVCs (BZ 1633211)
- SELinux is preventing pmdalinux from 'search' accesses on the directory spider
  (BZ 1647843)
- Update to latest PCP sources.

* Fri Sep 21 2018 Nathan Scott <nathans@redhat.com> - 4.1.3-1
- Update to latest PCP sources.

* Wed Aug 29 2018 Nathan Scott <nathans@redhat.com> - 4.1.1-3
- Updated versions of Vector (1.3.1) and Blinkenlights (1.0.1) webapps

* Fri Aug 03 2018 Dave Brolley <brolley@redhat.com> - 4.1.1-2
- pcp.spec: Fix the _with_dstat reference in the %%configure command

* Fri Aug 03 2018 Dave Brolley <brolley@redhat.com> - 4.1.1-1
- SELinux is preventing pmdalinux from 'unix_read' accesses on the shared memory Unknown
  (BZ 1592901)
- SELinux is preventing pmdalinux from getattr, associate access on the shared memory Unknown
  (BZ 1594991)
- PCP BCC PMDA AVCs (BZ 1597978)
- PCP BCC PMDA packaging issue (BZ 1597979)
- pmdaproc only reads the first 1024 bytes of the /proc/*/status file resulting in lost metric
  values(BZ 1600262)
- Update to latest PCP sources.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Petr Pisar <ppisar@redhat.com> - 4.1.0-6
- Perl 5.28 rebuild

* Fri Jun 29 2018 Miro Hrončok <mhroncok@redhat.com> - 4.1.0-5
- Rebuilt for Python 3.7

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.1.0-4
- Perl 5.28 rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.1.0-3
- Rebuilt for Python 3.7

* Fri Jun 15 2018 Nathan Scott <nathans@redhat.com> - 4.1.0-2
- Rapid compression of PCP log data and metadata (BZ 1293471)
- Added Perl package build dependencies.
- Update to latest PCP sources.

* Fri May 11 2018 Mark Goodwin <mgoodwin@redhat.com> - 4.0.2-1
- Propogate build flags throughout PCP (BZ 1538187)
- Further additions to selinux policy (BZ 1565158)
- Update to Vector v1.2.2 in pcp-webapp-vector.
- Update to latest PCP sources.

* Thu Mar 29 2018 Mark Goodwin <mgoodwin@redhat.com> - 4.0.1-1
- Fix selinux policy to allow pmdagluster to work (BZ 1558708)
- pmcd binding only to localhost:44321 by default (BZ 1529915)
- Update to latest PCP sources.

* Thu Mar 01 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.0.0-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Feb 20 2018 Nathan Scott <nathans@redhat.com> - 4.0.0-2
- Disable pmdabcc on architectures without BCC/eBPF support.

* Fri Feb 16 2018 Nathan Scott <nathans@redhat.com> - 4.0.0-1
- pcp-atopsar: robustness around missing data (BZ 1508028)
- python pmcc method checking for missing metrics (BZ 1508026)
- Fix generic -s and -T option handling in libpcp (BZ 1352461)
- Resolve crash in local context mode in libpcp_pmda (BZ 1451475)
- python api: fix timezone segv from incorrect free (BZ 1352465)
- Remove section 1 and 5 man pages for pmview tool (BZ 1289126)
- Update to latest PCP sources.

* Thu Feb 08 2018 Nathan Scott <nathans@redhat.com> - 3.12.2-5
- Update the Vector webapp to latest upstream (v1.2.1).

* Wed Jan 10 2018 Lukas Berk <lberk@redhat.com> - 3.12.2-4
- Remove Obsoletes line for pcp-gui-debuginfo
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.12.2-2
- Remove old crufty coreutils requires

* Wed Oct 18 2017 Lukas Berk <lberk@redhat.com> - 3.12.2-1
- selinux: add pmlogger_exec_t rule from (BZ 1483320)
- selinux: pmlc accessing tcp port 4330 (BZ 1447585)
- selinux: pmnewlog.sh using ps to check pid's for pmloggers (BZ 1488116)
- Update to latest PCP sources.

* Mon Aug 28 2017 Nathan Scott <nathans@redhat.com> - 3.12.1-3
- Disable infiniband and papi packages on armv7hl (BZ 1485692)

* Fri Aug 25 2017 Lukas Berk <lberk@redhat.com> - 3.12.1-2
- Rebuild for infiniband dep breakage.

* Wed Aug 16 2017 Nathan Scott <nathans@redhat.com> - 3.12.1-1
- Update to latest PCP sources.

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 3.12.0-2
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Fri Jun 30 2017 Lukas Berk <lberk@redhat.com> - 3.12.0-1
- Fix pcp-atop failure in open-ended write mode (BZ 1431292)
- Resolve additional selinux policy issues (BZ 1317515)
- Improve poor pmlogconf performance (BZ1376857)
- Update to latest PCP sources.

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.11.10-3
- Perl 5.26 rebuild

* Fri Jun 2 2017 Lukas Berk <lberk@redhat.com> - 3.11.10-2
- Correct subrpm inclusion of zeroconf config files (BZ 1456262)

* Wed May 17 2017 Dave Brolley <brolley@redhat.com> - 3.11.10-1
- python api: handle non-POSIXLY_CORRECT getopt cases (BZ 1289912)
- Fix pmchart reaction to timezone changes from pmtime (BZ 968823)
- Require Qt5 for Fedora.
- Update to latest PCP sources.

* Fri Mar 31 2017 Nathan Scott <nathans@redhat.com> - 3.11.9-1
- Fix pmchart chart legends toggling behaviour (BZ 1359961)
- Improve multiple local context attr handling (BZ 1430248)
- Fix error during installation of pcp-selinux (BZ 1433271)
- Update to latest PCP sources.

* Fri Feb 17 2017 Lukas Berk <lberk@redhat.com> - 3.11.8-1
- Support newer kernels /proc/vmstat file contents (BZ 1396148)
- Added pcp-selinux policy (BZs 1214090, 1381127, 1337968, 1398147)

* Wed Dec 21 2016 Dave Brolley <brolley@redhat.com> - 3.11.7-1
- pmchart run-away mem leak replaying multi-archive when rewinding (BZ 1359975)

* Fri Nov 11 2016 Mark Goodwin <mgoodwin@redhat.com> - 3.11.6-1
- Optimize DSO lookups for local context mode startup (BZ 1275293)
- Correct return code for derive metric help text (BZ 1336208)
- Improve pmrep metrics collection via extend_indom (BZ 1377464)
- Fix network.interface.speed value extraction (BZ 1379431)

* Mon Sep 26 2016 Mark Goodwin <mgoodwin@redhat.com> - 3.11.5-1
- Allow systemd-based auto-restart of all daemons (BZ 1365658)
- Ensure pmieconf and pmlogconf handle empty files (BZ 1249123)
- Ignore rpmsave and rpmnew suffixed control files (BZ 1375415)
- Add new pcp-pmda-libvirt package for virtual machine metrics
- Update to latest PCP sources.

* Fri Aug 05 2016 Nathan Scott <nathans@redhat.com> - 3.11.4-1
- Support inside-container metric values in python (BZ 1333702)
- Fix pmdaproc handling of commands with whitespace (BZ 1350816)
- Use persistent DM names for the filesystem metrics (BZ 1349932)
- Add to the ds389{,log} RPM package dependencies (BZ 1354055)
- Use "dirsrv" as default pmdads389log user account (BZ 1357607)
- Make pmie(1) honour SIGINT while parsing rules (BZ 1327226)
- Add pmlogconf support for pcp-pidstat and pcp-mpstat (BZ 1361943)
- Update to latest PCP sources.

* Fri Jun 17 2016 Nathan Scott <nathans@redhat.com> - 3.11.3-1
- Fix memory leak in derived metrics error handling (BZ 1331973)
- Correctly propogate indom in mixed derived metrics (BZ 1337212, BZ 1336130)
- Disallow stopping pmie/pmlogger daemons from cron (BZ 1336792)
- Fail fast for easily detected bad pmcd configuration (BZ 1336210)
- Implement primary (local) pmie concept in rc pmie (BZ 1323851)
- Update to latest PCP sources.

* Mon May 16 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.11.2-2.1
- Perl 5.24 rebuild

* Fri Apr 29 2016 Lukas Berk <lberk@redhat.com> - 3.11.2-1
- Negative nice values reported incorrectly (BZ 1328432)
- Multithreaded clients with concurrent pmNewContext improvements (BZ 1325363)
- PMCD agent auto-restart (BZ 1323521)
- Segv in libpcp during discovery error processing (BZ 1319288)
- Update to latest PCP sources.

* Fri Mar 18 2016 Dave Brolley <brolley@redhat.com> - 3.11.1-1
- Call Remove script when uninstalling individual PMDAs (BZ 1304722)
- Restrict pmcd.services to checking known pcp services (BZ 1286361)
- Support for multi-archive contexts, across all clients (BZ 1262723)
- Remove the default shotgun approach to stopping daemons (BZ 1210976)
- Add mechanism for automatic recovery from PMDA timeouts (BZ 1065803)
- Update to latest PCP sources.

* Fri Jan 29 2016 Mark Goodwin <mgoodwin@redhat.com> - 3.11.0-1
- Significant speedups to elapsed time stopping pmcd (BZ 1292027)
- Fix python derived metric exception handling issues (BZ 1299806)
- incorrect interpolation across <mark> record in a merged archive (BZ 1296750)
- pcp requires pcp-compat pulling in a lot of unneeded pcp-pmda-* packages (BZ 1293466)
- Update to latest PCP sources.

* Wed Dec 16 2015 Lukas Berk <lberk@redhat.com> - 3.10.9-1
- Add -V/--version support to several more commands (BZ 1284411)
- Resolve a pcp-iostat(1) transient device exception (BZ 1249572)
- Provides pmdapipe, an output-capturing domain agent (BZ 1163413)
- Python PMAPI pmSetMode allows None timeval parameter (BZ 1284417)
- Python PMI pmiPutValue now supports singular metrics (BZ 1285371)
- Fix python PMAPI pmRegisterDerived wrapper interface (BZ 1286733)
- Fix pmstat SEGV when run with graphical time control (BZ 1287678)
- Make pmNonOptionsFromList error message less cryptic (BZ 1287778)
- Drop unimplemented pmdumptext options from usage, man page (BZ 1289909)
- Stop creating configuration files in tmp_t locations (BZ 1256125)
- Update to latest PCP sources.

* Fri Oct 30 2015 Mark Goodwin <mgoodwin@redhat.com> - 3.10.8-1
- Update pmlogger to log an immediate sample first (BZ 1269921)
- Add pmOption host and archive setter python APIs (BZ 1270176)
- Replace old pmatop(1) man page with pcp-atop(1) (BZ 1270761)
- Update to latest PCP sources.

* Wed Sep 16 2015 Nathan Scott <nathans@redhat.com> - 3.10.7-1
- Resolved pmchart sigsegv opening view without context (BZ 1256708)
- Fixed pmchart memory corruption restoring Saved Hosts (BZ 1257009)
- Fix perl PMDA API double-free on socket error path (BZ 1258862)
- Fix python API pmGetOption(3) alignment interface (BZ 1262722)
- Added missing RPM dependencies to several PMDA sub-packages.
- Update to latest stable Vector release for pcp-vector-webapp.
- Update to latest PCP sources.

* Sat Sep 05 2015 Kalev Lember <klember@redhat.com> - 3.10.6-2.1
- Rebuilt for librpm soname bump

* Thu Aug 06 2015 Lukas Berk <lberk@redhat.com> - 3.10.6-2
- Fix SDT related build error (BZ 1250894)

* Tue Aug 04 2015 Nathan Scott <nathans@redhat.com> - 3.10.6-1
- Fix pcp2graphite write method invocation failure (BZ 1243123)
- Reduce diagnostics in pmdaproc unknown state case (BZ 1224431)
- Derived metrics via multiple files, directory expansion (BZ 1235556)
- Update to latest PCP sources.

* Mon Jun 15 2015 Mark Goodwin <mgoodwin@redhat.com> - 3.10.5-1
- Provide and use non-exit(1)ing pmGetConfig(3) variant (BZ 1187588)
- Resolve a pmdaproc.sh pmlogger restart regression (BZ 1229458)
- Replacement of pmatop/pcp-atop(1) utility (BZ 1160811, BZ 1018575)
- Reduced installation size for minimal applications (BZ 1182184)
- Ensure pmlogger start scripts wait on pmcd startup (BZ 1185760)
- Need to run pmcd at least once before pmval -L will work (BZ 185749)

* Wed Apr 15 2015 Nathan Scott <nathans@redhat.com> - 3.10.4-1
- Update to latest PCP, pcp-webjs and Vector sources.
- Packaging improvements after re-review (BZ 1204467)
- Start pmlogger/pmie independent of persistent state (BZ 1185755)
- Fix cron error reports for disabled pmlogger service (BZ 1208699)
- Incorporate Vector from Netflix (https://github.com/Netflix/vector)
- Sub-packages for pcp-webjs allowing choice and reducing used space.

* Wed Mar 04 2015 Dave Brolley <brolley@redhat.com> - 3.10.3-2
- papi 5.4.1 rebuild

* Mon Mar 02 2015 Dave Brolley <brolley@redhat.com> - 3.10.3-1
- Update to latest PCP sources.
- New sub-package for pcp-import-ganglia2pcp.
- Python3 support, enabled by default in f22 onward (BZ 1194324)

* Mon Feb 23 2015 Slavek Kabrda <bkabrda@redhat.com> - 3.10.2-3
- Only use Python 3 in Fedora >= 23, more info at
  https://bugzilla.redhat.com/show_bug.cgi?id=1194324#c4

* Mon Feb 23 2015 Nathan Scott <nathans@redhat.com> - 3.10.2-2
- Initial changes to support python3 as default (BZ 1194324)

* Fri Jan 23 2015 Dave Brolley <brolley@redhat.com> - 3.10.2-1
- Update to latest PCP sources.
- Improve pmdaInit diagnostics for DSO helptext (BZ 1182949)
- Tighten up PMDA termination on pmcd stop (BZ 1180109)
- Correct units for cgroup memory metrics (BZ 1180351)
- Add the pcp2graphite(1) export script (BZ 1163986)

* Mon Dec 01 2014 Nathan Scott <nathans@redhat.com> - 3.10.1-1
- New conditionally-built pcp-pmda-perfevent sub-package.
- Update to latest PCP sources.

* Tue Nov 18 2014 Dave Brolley <brolley@redhat.com> - 3.10.0-2
- papi 5.4.0 rebuild

* Fri Oct 31 2014 Nathan Scott <nathans@redhat.com> - 3.10.0-1
- Create new sub-packages for pcp-webjs and python3-pcp.
- Fix __pmDiscoverServicesWithOptions(1) codes (BZ 1139529)
- Update to latest PCP sources.

* Fri Sep 05 2014 Nathan Scott <nathans@redhat.com> - 3.9.10-1
- Convert PCP init scripts to systemd services (BZ 996438)
- Fix pmlogsummary -S/-T time window reporting (BZ 1132476)
- Resolve pmdumptext segfault with invalid host (BZ 1131779)
- Fix signedness in some service discovery codes (BZ 1136166)
- New conditionally-built pcp-pmda-papi sub-package.
- Update to latest PCP sources.

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.9.9-1.2
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.9-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Nathan Scott <nathans@redhat.com> - 3.9.9-1
- Update to latest PCP sources.

* Wed Jul 16 2014 Mark Goodwin <mgoodwin@redhat.com> - 3.9.7-1
- Update to latest PCP sources.

* Wed Jun 18 2014 Dave Brolley <brolley@redhat.com> - 3.9.5-1
- Daemon signal handlers no longer use unsafe APIs (BZ 847343)
- Handle /var/run setups on a temporary filesystem (BZ 656659)
- Resolve pmlogcheck sigsegv for some archives (BZ 1077432)
- Ensure pcp-gui-{testsuite,debuginfo} packages get replaced.
- Revive support for EPEL5 builds, post pcp-gui merge.
- Update to latest PCP sources.

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.4-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Nathan Scott <nathans@redhat.com> - 3.9.4-1
- Merged pcp-gui and pcp-doc packages into core PCP.
- Allow for conditional libmicrohttpd builds in spec file.
- Adopt slow-start capability in systemd PMDA (BZ 1073658)
- Resolve pmcollectl network/disk mis-reporting (BZ 1097095)
- Update to latest PCP sources.

* Tue Apr 15 2014 Dave Brolley <brolley@redhat.com> - 3.9.2-1
- Improve pmdarpm(1) concurrency complications (BZ 1044297)
- Fix pmconfig(1) shell output string quoting (BZ 1085401)
- Update to latest PCP sources.

* Wed Mar 19 2014 Nathan Scott <nathans@redhat.com> - 3.9.1-1
- Update to latest PCP sources.

* Thu Feb 20 2014 Nathan Scott <nathans@redhat.com> - 3.9.0-2
- Workaround further PowerPC/tapset-related build fallout.

* Wed Feb 19 2014 Nathan Scott <nathans@redhat.com> - 3.9.0-1
- Create new sub-packages for pcp-webapi and pcp-manager
- Split configuration from pcp-libs into pcp-conf (multilib)
- Fix pmdagluster to handle more volumes, fileops (BZ 1066544)
- Update to latest PCP sources.

* Wed Jan 29 2014 Nathan Scott <nathans@redhat.com> - 3.8.12-1
- Resolves SNMP procfs file ICMP line parse issue (BZ 1055818)
- Update to latest PCP sources.

* Wed Jan 15 2014 Nathan Scott <nathans@redhat.com> - 3.8.10-1
- Update to latest PCP sources.

* Thu Dec 12 2013 Nathan Scott <nathans@redhat.com> - 3.8.9-1
- Reduce set of exported symbols from DSO PMDAs (BZ 1025694)
- Symbol-versioning for PCP shared libraries (BZ 1037771)
- Fix pmcd/Avahi interaction with multiple ports (BZ 1035513)
- Update to latest PCP sources.

* Sun Nov 03 2013 Nathan Scott <nathans@redhat.com> - 3.8.8-1
- Update to latest PCP sources (simple build fixes only).

* Fri Nov 01 2013 Nathan Scott <nathans@redhat.com> - 3.8.6-1
- Update to latest PCP sources.
- Rework pmpost test which confused virus checkers (BZ 1024850)
- Tackle pmatop reporting issues via alternate metrics (BZ 998735)

* Fri Oct 18 2013 Nathan Scott <nathans@redhat.com> - 3.8.5-1
- Update to latest PCP sources.
- Disable pcp-pmda-infiniband sub-package on RHEL5 (BZ 1016368)

* Mon Sep 16 2013 Nathan Scott <nathans@redhat.com> - 3.8.4-2
- Disable the pcp-pmda-infiniband sub-package on s390 platforms.

* Sun Sep 15 2013 Nathan Scott <nathans@redhat.com> - 3.8.4-1
- Very minor release containing mostly QA related changes.
- Enables many more metrics to be logged for Linux hosts.

* Wed Sep 11 2013 Stan Cox <scox@redhat.com> - 3.8.3-2
- Disable pmcd.stp on el5 ppc.

* Mon Sep 09 2013 Nathan Scott <nathans@redhat.com> - 3.8.3-1
- Default to Unix domain socket (authenticated) local connections.
- Introduces new pcp-pmda-infiniband sub-package.
- Disable systemtap-sdt-devel usage on ppc.

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 3.8.2-1.1
- Perl 5.18 rebuild

* Wed Jul 31 2013 Nathan Scott <nathans@redhat.com> - 3.8.2-1
- Update to latest PCP sources.
- Integrate gluster related stats with PCP (BZ 969348)
- Fix for iostat2pcp not parsing iostat output (BZ 981545)
- Start pmlogger with usable config by default (BZ 953759)
- Fix pmatop failing to start, gives stacktrace (BZ 963085)

* Wed Jun 19 2013 Nathan Scott <nathans@redhat.com> - 3.8.1-1
- Update to latest PCP sources.
- Fix log import silently dropping >1024 metrics (BZ 968210)
- Move some commonly used tools on the usual PATH (BZ 967709)
- Improve pmatop handling of missing proc metrics (BZ 963085)
- Stop out-of-order records corrupting import logs (BZ 958745)

* Tue May 14 2013 Nathan Scott <nathans@redhat.com> - 3.8.0-1
- Update to latest PCP sources.
- Validate metric names passed into pmiAddMetric (BZ 958019)
- Install log directories with correct ownership (BZ 960858)

* Fri Apr 19 2013 Nathan Scott <nathans@redhat.com> - 3.7.2-1
- Update to latest PCP sources.
- Ensure root namespace exists at the end of install (BZ 952977)

* Wed Mar 20 2013 Nathan Scott <nathans@redhat.com> - 3.7.1-1
- Update to latest PCP sources.
- Migrate all tempfiles correctly to the new tempdir hierarchy.

* Sun Mar 10 2013 Nathan Scott <nathans@redhat.com> - 3.7.0-1
- Update to latest PCP sources.
- Migrate all configuration files below the /etc/pcp hierarchy.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.10-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 28 2012 Nathan Scott <nathans@redhat.com> - 3.6.10-2
- Ensure tmpfile directories created in %%files section.
- Resolve tmpfile create/teardown race conditions.

* Mon Nov 19 2012 Nathan Scott <nathans@redhat.com> - 3.6.10-1
- Update to latest PCP sources.
- Resolve tmpfile security flaws: CVE-2012-5530
- Introduces new "pcp" user account for all daemons to use.

* Fri Oct 12 2012 Nathan Scott <nathans@redhat.com> - 3.6.9-1
- Update to latest PCP sources.
- Fix pmcd sigsegv in NUMA/CPU indom setup (BZ 858384)
- Fix sar2pcp uninitialised perl variable warning (BZ 859117)
- Fix pcp.py and pmcollectl with older python versions (BZ 852234)

* Fri Sep 14 2012 Nathan Scott <nathans@redhat.com> - 3.6.8-1
- Update to latest PCP sources.

* Wed Sep 05 2012 Nathan Scott <nathans@redhat.com> - 3.6.6-1.1
- Move configure step from prep to build section of spec (BZ 854128)

* Tue Aug 28 2012 Mark Goodwin <mgoodwin@redhat.com> - 3.6.6-1
- Update to latest PCP sources, see installed CHANGELOG for details.
- Introduces new python-pcp and pcp-testsuite sub-packages.

* Thu Aug 16 2012 Mark Goodwin <mgoodwin@redhat.com> - 3.6.5-1
- Update to latest PCP sources, see installed CHANGELOG for details.
- Fix security flaws: CVE-2012-3418 CVE-2012-3419 CVE-2012-3420 and CVE-2012-3421 (BZ 848629)

* Thu Jul 19 2012 Mark Goodwin <mgoodwin@redhat.com>
- pmcd and pmlogger services are not supposed to be enabled by default (BZ 840763) - 3.6.3-1.3

* Thu Jun 21 2012 Mark Goodwin <mgoodwin@redhat.com>
- remove pcp-import-sheet2pcp subpackage due to missing deps (BZ 830923) - 3.6.3-1.2

* Fri May 18 2012 Dan Hork <dan[at]danny.cz> - 3.6.3-1.1
- fix build on s390x

* Mon Apr 30 2012 Mark Goodwin - 3.6.3-1
- Update to latest PCP sources

* Thu Apr 26 2012 Mark Goodwin - 3.6.2-1
- Update to latest PCP sources

* Thu Apr 12 2012 Mark Goodwin - 3.6.1-1
- Update to latest PCP sources

* Thu Mar 22 2012 Mark Goodwin - 3.6.0-1
- use %%configure macro for correct libdir logic
- update to latest PCP sources

* Thu Dec 15 2011 Mark Goodwin - 3.5.11-2
- patched configure.in for libdir=/usr/lib64 on ppc64

* Thu Dec 01 2011 Mark Goodwin - 3.5.11-1
- Update to latest PCP sources.

* Fri Nov 04 2011 Mark Goodwin - 3.5.10-1
- Update to latest PCP sources.

* Mon Oct 24 2011 Mark Goodwin - 3.5.9-1
- Update to latest PCP sources.

* Mon Aug 08 2011 Mark Goodwin - 3.5.8-1
- Update to latest PCP sources.

* Fri Aug 05 2011 Mark Goodwin - 3.5.7-1
- Update to latest PCP sources.

* Fri Jul 22 2011 Mark Goodwin - 3.5.6-1
- Update to latest PCP sources.

* Tue Jul 19 2011 Mark Goodwin - 3.5.5-1
- Update to latest PCP sources.

* Thu Feb 03 2011 Mark Goodwin - 3.5.0-1
- Update to latest PCP sources.

* Thu Sep 30 2010 Mark Goodwin - 3.4.0-1
- Update to latest PCP sources.

* Fri Jul 16 2010 Mark Goodwin - 3.3.3-1
- Update to latest PCP sources.

* Sat Jul 10 2010 Mark Goodwin - 3.3.2-1
- Update to latest PCP sources.

* Tue Jun 29 2010 Mark Goodwin - 3.3.1-1
- Update to latest PCP sources.

* Fri Jun 25 2010 Mark Goodwin - 3.3.0-1
- Update to latest PCP sources.

* Thu Mar 18 2010 Mark Goodwin - 3.1.2-1
- Update to latest PCP sources.

* Wed Jan 27 2010 Mark Goodwin - 3.1.0-1
- BuildRequires: initscripts for %%{_vendor} == redhat.

* Thu Dec 10 2009 Mark Goodwin - 3.0.3-1
- BuildRequires: initscripts for FC12.

* Wed Dec 02 2009 Mark Goodwin - 3.0.2-1
- Added sysfs.kernel metrics, rebased to minor community release.

* Mon Oct 19 2009 Martin Hicks <mort@sgi.com> - 3.0.1-2
- Remove IB dependencies.  The Infiniband PMDA is being moved to
  a stand-alone package.
- Move cluster PMDA to a stand-alone package.

* Fri Oct 09 2009 Mark Goodwin <mgoodwin@redhat.com> - 3.0.0-9
- This is the initial import for Fedora
- See 3.0.0 details in CHANGELOG
