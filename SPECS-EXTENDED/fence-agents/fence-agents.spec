Vendor:         Microsoft Corporation
Distribution:   Mariner
# Copyright 2004-2011 Red Hat, Inc.
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2.

# keep around ready for later user
## global alphatag git0a6184070

Name: fence-agents
Summary: Set of unified programs capable of host isolation ("fencing")
Version: 4.5.2
Release: 3%{?dist}
License: GPLv2+ and LGPLv2+
URL: https://github.com/ClusterLabs/fence-agents
Source0: https://fedorahosted.org/releases/f/e/fence-agents/%{name}-%{version}.tar.gz

# skipped: pve, raritan, rcd-serial, virsh
%global allfenceagents %(cat <<EOF
fence-agents-alom \\
fence-agents-amt \\
fence-agents-amt-ws \\
fence-agents-apc \\
fence-agents-apc-snmp \\
fence-agents-aws \\
fence-agents-azure-arm \\
fence-agents-bladecenter \\
fence-agents-brocade \\
fence-agents-cisco-mds \\
fence-agents-cisco-ucs \\
fence-agents-docker \\
fence-agents-drac \\
fence-agents-drac5 \\
fence-agents-eaton-snmp \\
fence-agents-emerson \\
fence-agents-eps \\
fence-agents-gce \\
fence-agents-hds-cb \\
fence-agents-heuristics-ping \\
fence-agents-hpblade \\
fence-agents-ibmblade \\
fence-agents-ifmib \\
fence-agents-ilo-moonshot \\
fence-agents-ilo-mp \\
fence-agents-ilo-ssh \\
fence-agents-ilo2 \\
fence-agents-intelmodular \\
fence-agents-ipdu \\
fence-agents-ipmilan \\
fence-agents-kdump \\
fence-agents-ldom \\
fence-agents-lpar \\
fence-agents-mpath \\
fence-agents-netio \\
fence-agents-ovh \\
fence-agents-redfish \\
fence-agents-rhevm \\
fence-agents-rsa \\
fence-agents-rsb \\
fence-agents-sanbox2 \\
fence-agents-sbd \\
fence-agents-scsi \\
fence-agents-vbox \\
fence-agents-vmware \\
fence-agents-vmware-rest \\
fence-agents-vmware-soap \\
fence-agents-vmware-vcloud \\
fence-agents-wti \\
fence-agents-xenapi \\
fence-agents-zvm \\

EOF)

%ifarch x86_64 ppc64le
%global allfenceagents %(cat <<EOF
%{allfenceagents} \\
fence-agents-compute \\
fence-agents-ironic \\
fence-agents-openstack

EOF)
%endif

# Build dependencies
## general
BuildRequires: autoconf automake libtool
## compiled code (-kdump)
BuildRequires: gcc
## man pages generating
BuildRequires: libxslt
## establishing proper paths to particular programs
BuildRequires: gnutls-utils
## Python dependencies
BuildRequires: python3-devel
BuildRequires: python3-pexpect python3-pycurl python3-requests
BuildRequires: python3-suds openwsman-python3 python3-boto3
BuildRequires: python3-google-api-client

# (-openstack)
BuildRequires: python3-novaclient python3-keystoneclient

# turn off the brp-python-bytecompile script
# (for F28+ or equivalent, the latter is the preferred form)
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompilespace:.*$!!g')
#undefine __brp_python_bytecompile

%prep
%setup -q -n %{name}-%{version}
%autopatch -p1
# prevent compilation of something that won't get used anyway
sed -i.orig 's|FENCE_ZVM=1|FENCE_ZVM=0|' configure.ac

%build
./autogen.sh
%{configure} PYTHON="%{__python3}"
CFLAGS="$(echo '%{optflags}')" make %{_smp_mflags}

%install
make install DESTDIR=%{buildroot}
# bytecompile Python source code in a non-standard location
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/fence
# XXX unsure if /usr/sbin/fence_* should be compiled as well

## tree fix up
# fix libfence permissions
chmod 0755 %{buildroot}%{_datadir}/fence/*.py
# remove docs
rm -rf %{buildroot}/usr/share/doc/fence-agents

%post
ccs_update_schema > /dev/null 2>&1 ||:

%description
A collection of executables to handle isolation ("fencing") of possibly
misbehaving hosts by the means of remote power management, blocking
network, storage, or similar. They operate through a unified interface
(calling conventions) devised for the original Red Hat clustering solution.

%package common
License: GPLv2+ and LGPLv2+
Summary: Common base for Fence Agents
Requires: python3-pexpect python3-pycurl
BuildArch: noarch
%description common
A collection of executables to handle isolation ("fencing") of possibly
misbehaving hosts by the means of remote power management, blocking
network, storage, or similar.

This package contains support files including the Python fencing library.
%files common
%doc doc/COPYING.* doc/COPYRIGHT doc/README.licence
%{_datadir}/fence
%exclude %{_datadir}/fence/azure_fence.*
%exclude %{_datadir}/fence/__pycache__/azure_fence.*
%exclude %{_datadir}/fence/XenAPI.*
%exclude %{_datadir}/fence/__pycache__/XenAPI.*
%{_datadir}/cluster
%exclude %{_datadir}/cluster/fence_scsi_check*
%exclude %{_sbindir}/*
%exclude %{_mandir}/man8/*

%package all
License: GPLv2+, LGPLv2+ and ASL 2.0
Summary: Set of unified programs capable of host isolation ("fencing")
Requires: %{allfenceagents}
Provides: fence-agents = %{version}-%{release}
Obsoletes: fence-agents < 3.1.13
%description all
A collection of executables to handle isolation ("fencing") of possibly
misbehaving hosts by the means of remote power management, blocking
network, storage, or similar.

This package serves as a catch-all for all supported fence agents.
%files all

%package alom
License: GPLv2+ and LGPLv2+
Summary: Fence agent for SUN ALOM
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description alom
Fence agent for SUN ALOM.
%files alom
%{_sbindir}/fence_alom
%{_mandir}/man8/fence_alom.8*

%package amt
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Intel AMT devices
Requires: amtterm
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description amt
Fence agent for AMT compatibile devices that are accessed via
3rd party software.
%files amt
%{_sbindir}/fence_amt
%{_mandir}/man8/fence_amt.8*

%package amt-ws
License: ASL 2.0
Summary: Fence agent for Intel AMT (WS-Man) devices
Requires: fence-agents-common = %{version}-%{release}
Requires: openwsman-python3
BuildArch: noarch
%description amt-ws
Fence agent for AMT (WS-Man) devices.
%files amt-ws
%{_sbindir}/fence_amt_ws
%{_mandir}/man8/fence_amt_ws.8*

%package apc
License: GPLv2+ and LGPLv2+
Summary: Fence agent for APC devices
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description apc
Fence agent for APC devices that are accessed via telnet or SSH.
%files apc
%{_sbindir}/fence_apc
%{_mandir}/man8/fence_apc.8*

%package apc-snmp
License: GPLv2+ and LGPLv2+
Summary: Fence agents for APC devices (SNMP)
Requires: net-snmp-utils
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description apc-snmp
Fence agents for APC devices that are accessed via the SNMP protocol.
%files apc-snmp
%{_sbindir}/fence_apc_snmp
%{_mandir}/man8/fence_apc_snmp.8*
%{_sbindir}/fence_tripplite_snmp
%{_mandir}/man8/fence_tripplite_snmp.8*

%package aws
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Amazon AWS
Requires: fence-agents-common = %{version}-%{release}
Requires: python3-boto3
BuildArch: noarch
Obsoletes: fence-agents
%description aws
Fence agent for Amazon AWS instances.
%files aws
%{_sbindir}/fence_aws
%{_mandir}/man8/fence_aws.8*

%package azure-arm
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Azure Resource Manager
Requires: fence-agents-common = %{version}-%{release}
Requires: python3-azure-sdk
BuildArch: noarch
Obsoletes: fence-agents
%description azure-arm
Fence agent for Azure Resource Manager instances.
%files azure-arm
%{_sbindir}/fence_azure_arm
%{_datadir}/fence/azure_fence.py*
%{_datadir}/fence/__pycache__/azure_fence.*
%{_mandir}/man8/fence_azure_arm.8*

%package bladecenter
License: GPLv2+ and LGPLv2+
Summary: Fence agent for IBM BladeCenter
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description bladecenter
Fence agent for IBM BladeCenter devices that are accessed
via telnet or SSH.
%files bladecenter
%{_sbindir}/fence_bladecenter
%{_mandir}/man8/fence_bladecenter.8*

%package brocade
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Brocade switches
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description brocade
Fence agent for Brocade devices that are accessed via telnet or SSH.
%files brocade
%{_sbindir}/fence_brocade
%{_mandir}/man8/fence_brocade.8*

%package cisco-mds
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Cisco MDS 9000 series
Requires: net-snmp-utils
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description cisco-mds
Fence agent for Cisco MDS 9000 series devices that are accessed
via the SNMP protocol.
%files cisco-mds
%{_sbindir}/fence_cisco_mds
%{_mandir}/man8/fence_cisco_mds.8*

%package cisco-ucs
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Cisco UCS series
Requires: python3-pycurl
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description cisco-ucs
Fence agent for Cisco UCS series devices that are accessed
via the SNMP protocol.
%files cisco-ucs
%{_sbindir}/fence_cisco_ucs
%{_mandir}/man8/fence_cisco_ucs.8*

%package compute
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Nova compute nodes
Requires: python3-requests
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description compute
Fence agent for Nova compute nodes.
%files compute
%{_sbindir}/fence_compute
%{_sbindir}/fence_evacuate
%{_mandir}/man8/fence_compute.8*
%{_mandir}/man8/fence_evacuate.8*

%package docker
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Docker
Requires: python3-pycurl
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description docker
Fence agent for Docker images that are accessed over HTTP.
%files docker
%{_sbindir}/fence_docker
%{_mandir}/man8/fence_docker.8*

%package drac
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Dell DRAC
Requires: telnet
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description drac
Fence agent for Dell DRAC IV series devices that are accessed
via telnet.
%files drac
%{_sbindir}/fence_drac
%{_mandir}/man8/fence_drac.8*

%package drac5
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Dell DRAC 5
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description drac5
Fence agent for Dell DRAC 5 series devices that are accessed
via telnet or SSH.
%files drac5
%{_sbindir}/fence_drac5
%{_mandir}/man8/fence_drac5.8*

%package eaton-snmp
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Eaton network power switches
Requires: net-snmp-utils
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description eaton-snmp
Fence agent for Eaton network power switches that are accessed
via the SNMP protocol.
%files eaton-snmp
%{_sbindir}/fence_eaton_snmp
%{_mandir}/man8/fence_eaton_snmp.8*

%package emerson
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Emerson devices (SNMP)
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description emerson
Fence agent for Emerson devices that are accessed via
the SNMP protocol.
%files emerson
%{_sbindir}/fence_emerson
%{_mandir}/man8/fence_emerson.8*

%package eps
License: GPLv2+ and LGPLv2+
Summary: Fence agent for ePowerSwitch 8M+ power switches
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description eps
Fence agent for ePowerSwitch 8M+ power switches that are accessed
via the HTTP(s) protocol.
%files eps
%{_sbindir}/fence_eps
%{_mandir}/man8/fence_eps.8*

%package gce
License: GPLv2+ and LGPLv2+
Summary: Fence agent for GCE (Google Cloud Engine)
Requires: fence-agents-common = %{version}-%{release}
Requires: python3-google-api-client
BuildArch: noarch
Obsoletes: fence-agents
%description gce
Fence agent for GCE (Google Cloud Engine) instances.
%files gce
%{_sbindir}/fence_gce
%{_mandir}/man8/fence_gce.8*

%package hds-cb
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Hitachi Compute Blade systems
Requires: telnet
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description hds-cb
Fence agent for Hitachi Compute Blades that are accessed via telnet.
%files hds-cb
%{_sbindir}/fence_hds_cb
%{_mandir}/man8/fence_hds_cb.8*

%package heuristics-ping
License: GPLv2+ and LGPLv2+
Summary: Pseudo fence agent to affect other agents based on ping-heuristics
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
Obsoletes: fence-agents
%description heuristics-ping
Fence pseudo agent used to affect other agents based on
ping-heuristics.
%files heuristics-ping
%{_sbindir}/fence_heuristics_ping
%{_mandir}/man8/fence_heuristics_ping.8*

%package hpblade
License: GPLv2+ and LGPLv2+
Summary: Fence agent for HP BladeSystem devices
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description hpblade
Fence agent for HP BladeSystem devices that are accessed via telnet
or SSH.
%files hpblade
%{_sbindir}/fence_hpblade
%{_mandir}/man8/fence_hpblade.8*

%package ibmblade
License: GPLv2+ and LGPLv2+
Summary: Fence agent for IBM BladeCenter
Requires: net-snmp-utils
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description ibmblade
Fence agent for IBM BladeCenter devices that are accessed
via the SNMP protocol.
%files ibmblade
%{_sbindir}/fence_ibmblade
%{_mandir}/man8/fence_ibmblade.8*

%package ifmib
License: GPLv2+ and LGPLv2+
Summary: Fence agent for devices with IF-MIB interfaces
Requires: net-snmp-utils
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description ifmib
Fence agent for IF-MIB interfaces that are accessed via
the SNMP protocol.
%files ifmib
%{_sbindir}/fence_ifmib
%{_mandir}/man8/fence_ifmib.8*

%package ilo2
License: GPLv2+ and LGPLv2+
Summary: Fence agents for HP iLO2 devices
Requires: gnutls-utils
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description ilo2
Fence agents for HP iLO2 devices that are accessed via
the HTTP(s) protocol.
%files ilo2
%{_sbindir}/fence_ilo
%{_sbindir}/fence_ilo2
%{_mandir}/man8/fence_ilo.8*
%{_mandir}/man8/fence_ilo2.8*

%package ilo-moonshot
License: GPLv2+ and LGPLv2+
Summary: Fence agent for HP iLO Moonshot devices
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description ilo-moonshot
Fence agent for HP iLO Moonshot devices that are accessed
via telnet or SSH.
%files ilo-moonshot
%{_sbindir}/fence_ilo_moonshot
%{_mandir}/man8/fence_ilo_moonshot.8*

%package ilo-mp
License: GPLv2+ and LGPLv2+
Summary: Fence agent for HP iLO MP devices
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description ilo-mp
Fence agent for HP iLO MP devices that are accessed via telnet or SSH.
%files ilo-mp
%{_sbindir}/fence_ilo_mp
%{_mandir}/man8/fence_ilo_mp.8*

%package ilo-ssh
License: GPLv2+ and LGPLv2+
Summary: Fence agents for HP iLO devices over SSH
Requires: openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description ilo-ssh
Fence agents for HP iLO devices that are accessed via telnet or SSH.
%files ilo-ssh
%{_sbindir}/fence_ilo_ssh
%{_mandir}/man8/fence_ilo_ssh.8*
%{_sbindir}/fence_ilo3_ssh
%{_mandir}/man8/fence_ilo3_ssh.8*
%{_sbindir}/fence_ilo4_ssh
%{_mandir}/man8/fence_ilo4_ssh.8*
%{_sbindir}/fence_ilo5_ssh
%{_mandir}/man8/fence_ilo5_ssh.8*

%package intelmodular
License: GPLv2+ and LGPLv2+
Summary: Fence agent for devices with Intel Modular interfaces
Requires: net-snmp-utils
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description intelmodular
Fence agent for Intel Modular interfaces that are accessed
via the SNMP protocol.
%files intelmodular
%{_sbindir}/fence_intelmodular
%{_mandir}/man8/fence_intelmodular.8*

%package ipdu
License: GPLv2+ and LGPLv2+
Summary: Fence agent for IBM iPDU network power switches
Requires: net-snmp-utils
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description ipdu
Fence agent for IBM iPDU network power switches that are accessed
via the SNMP protocol.
%files ipdu
%{_sbindir}/fence_ipdu
%{_mandir}/man8/fence_ipdu.8*

%package ipmilan
License: GPLv2+ and LGPLv2+
Summary: Fence agents for devices with IPMI interface
Requires: /usr/bin/ipmitool
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description ipmilan
Fence agents for devices with IPMI interface.
%files ipmilan
%{_sbindir}/fence_ipmilan
%{_mandir}/man8/fence_ipmilan.8*
%{_sbindir}/fence_idrac
%{_mandir}/man8/fence_idrac.8*
%{_sbindir}/fence_ilo3
%{_mandir}/man8/fence_ilo3.8*
%{_sbindir}/fence_ilo4
%{_mandir}/man8/fence_ilo4.8*
%{_sbindir}/fence_ilo5
%{_mandir}/man8/fence_ilo5.8*
%{_sbindir}/fence_imm
%{_mandir}/man8/fence_imm.8*

%package ironic
License: GPLv2+ and LGPLv2+
Summary: Fence agent for OpenStack's Ironic (Bare Metal as a service)
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description ironic
Fence agent for OpenStack's Ironic (Bare Metal as a service) service.
%files ironic
%{_sbindir}/fence_ironic
%{_mandir}/man8/fence_ironic.8*

%package kdump
License: GPLv2+ and LGPLv2+
Summary: Fence agent for use with kdump crash recovery service
Requires: fence-agents-common = %{version}-%{release}
# this cannot be noarch since it's compiled
%description kdump
Fence agent for use with kdump crash recovery service.
%files kdump
%{_sbindir}/fence_kdump
%{_libexecdir}/fence_kdump_send
%{_mandir}/man8/fence_kdump.8*
%{_mandir}/man8/fence_kdump_send.8*

%package ldom
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Sun LDom virtual machines
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description ldom
Fence agent for APC devices that are accessed via telnet or SSH.
%files ldom
%{_sbindir}/fence_ldom
%{_mandir}/man8/fence_ldom.8*

%package lpar
License: GPLv2+ and LGPLv2+
Summary: Fence agent for IBM LPAR
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description lpar
Fence agent for IBM LPAR devices that are accessed via telnet or SSH.
%files lpar
%{_sbindir}/fence_lpar
%{_mandir}/man8/fence_lpar.8*

%package mpath
License: GPLv2+ and LGPLv2+
Summary: Fence agent for reservations over Device Mapper Multipath
Requires: device-mapper-multipath
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description mpath
Fence agent for SCSI persistent reservation over
Device Mapper Multipath.
%files mpath
%{_sbindir}/fence_mpath
%{_mandir}/man8/fence_mpath.8*

%package netio
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Koukaam NETIO devices
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description netio
Fence agent for Koukaam NETIO devices that are accessed
via telnet or SSH.
%files netio
%{_sbindir}/fence_netio
%{_mandir}/man8/fence_netio.8*

%package openstack
License: GPLv2+ and LGPLv2+
Summary: Fence agent for OpenStack's Nova service
Requires: python3-requests
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description openstack
Fence agent for OpenStack's Nova service.
%files openstack
%{_sbindir}/fence_openstack
%{_mandir}/man8/fence_openstack.8*

%package ovh
License: GPLv2+ and LGPLv2+
Summary: Fence agent for OVH provider
Requires: python3-suds
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description ovh
Fence agent for OVH hosting provider.
%files ovh
%{_sbindir}/fence_ovh
%{_mandir}/man8/fence_ovh.8*

# skipped from allfenceagents
%package pve
License: GPLv2+ and LGPLv2+
Summary: Fence agent for PVE
Requires: python3-pycurl
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description pve
Fence agent for PVE.
%files pve
%{_sbindir}/fence_pve
%{_mandir}/man8/fence_pve.8*

# skipped from allfenceagents
%package raritan
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Raritan Dominion PX
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description raritan
Fence agent for Raritan Dominion PX.
%files raritan
%{_sbindir}/fence_raritan
%{_mandir}/man8/fence_raritan.8*

# skipped from allfenceagents
%package rcd-serial
License: GPLv2+ and LGPLv2+
Summary: Fence agent for RCD serial
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description rcd-serial
Fence agent for RCD serial.
%files rcd-serial
%{_sbindir}/fence_rcd_serial
%{_mandir}/man8/fence_rcd_serial.8*

%package redfish
License: GPLv2+ and LGPLv2+
Group: System Environment/Base
Summary: Fence agent for Redfish
Requires: fence-agents-common >= %{version}-%{release}
Requires: python3-requests
Obsoletes: fence-agents
%description redfish
The fence-agents-redfish package contains a fence agent for Redfish
%files redfish
%defattr(-,root,root,-)
%{_sbindir}/fence_redfish
%{_mandir}/man8/fence_redfish.8*

%package rhevm
License: GPLv2+ and LGPLv2+
Summary: Fence agent for RHEV-M
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description rhevm
Fence agent for RHEV-M via REST API.
%files rhevm
%{_sbindir}/fence_rhevm
%{_mandir}/man8/fence_rhevm.8*

%package rsa
License: GPLv2+ and LGPLv2+
Summary: Fence agent for IBM RSA II
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description rsa
Fence agent for IBM RSA II devices that are accessed
via telnet or SSH.
%files rsa
%{_sbindir}/fence_rsa
%{_mandir}/man8/fence_rsa.8*

%package rsb
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Fujitsu RSB
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description rsb
Fence agent for Fujitsu RSB devices that are accessed
via telnet or SSH.
%files rsb
%{_sbindir}/fence_rsb
%{_mandir}/man8/fence_rsb.8*

%package sanbox2
License: GPLv2+ and LGPLv2+
Summary: Fence agent for QLogic SANBox2 FC switches
Requires: telnet
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description sanbox2
Fence agent for QLogic SANBox2 switches that are accessed via telnet.
%files sanbox2
%{_sbindir}/fence_sanbox2
%{_mandir}/man8/fence_sanbox2.8*

%package sbd
License: GPLv2+ and LGPLv2+
Summary: Fence agent for SBD (storage-based death)
Requires: sbd
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description sbd
Fence agent for SBD (storage-based death).
%files sbd
%{_sbindir}/fence_sbd
%{_mandir}/man8/fence_sbd.8*

%package scsi
License: GPLv2+ and LGPLv2+
Summary: Fence agent for SCSI persistent reservations
Requires: sg3_utils
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description scsi
Fence agent for SCSI persistent reservations.
%files scsi
%{_sbindir}/fence_scsi
%{_datadir}/cluster/fence_scsi_check
%{_datadir}/cluster/fence_scsi_check_hardreboot
%{_mandir}/man8/fence_scsi.8*

%package vbox
License: GPLv2+ and LGPLv2+
Summary: Fence agent for VirtualBox
Requires: openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description vbox
Fence agent for VirtualBox dom0 accessed via SSH.
%files vbox
%{_sbindir}/fence_vbox
%{_mandir}/man8/fence_vbox.8*

# skipped from allfenceagents
%package virsh
License: GPLv2+ and LGPLv2+
Summary: Fence agent for virtual machines based on libvirt
Requires: openssh-clients /usr/bin/virsh
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description virsh
Fence agent for virtual machines that are accessed via SSH.
%files virsh
%{_sbindir}/fence_virsh
%{_mandir}/man8/fence_virsh.8*

%package vmware
License: GPLv2+ and LGPLv2+
Summary: Fence agent for VMWare with VI Perl Toolkit or vmrun
Requires: python3-pexpect
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description vmware
Fence agent for VMWare accessed with VI Perl Toolkit or vmrun.
%files vmware
%{_sbindir}/fence_vmware
%{_mandir}/man8/fence_vmware.8*

%package vmware-rest
License: GPLv2+ and LGPLv2+
Summary: Fence agent for VMWare with REST API
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
Obsoletes: fence-agents
%description vmware-rest
Fence agent for VMWare with REST API.
%files vmware-rest
%{_sbindir}/fence_vmware_rest
%{_mandir}/man8/fence_vmware_rest.8*

%package vmware-soap
License: GPLv2+ and LGPLv2+
Summary: Fence agent for VMWare with SOAP API v4.1+
Requires: python3-suds
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description vmware-soap
Fence agent for VMWare with SOAP API v4.1+.
%files vmware-soap
%{_sbindir}/fence_vmware_soap
%{_mandir}/man8/fence_vmware_soap.8*

%package vmware-vcloud
License: GPLv2+ and LGPLv2+
Summary: Fence agent for VMWare vCloud Director
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
Obsoletes: fence-agents
%description vmware-vcloud
Fence agent for VMWare vCloud Director.
%files vmware-vcloud
%{_sbindir}/fence_vmware_vcloud
%{_mandir}/man8/fence_vmware_vcloud.8*

%package wti
License: GPLv2+ and LGPLv2+
Summary: Fence agent for WTI Network power switches
Requires: telnet openssh-clients
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description wti
Fence agent for WTI network power switches that are accessed
via telnet or SSH.
%files wti
%{_sbindir}/fence_wti
%{_mandir}/man8/fence_wti.8*

%package xenapi
License: GPLv2+ and LGPLv2+
Summary: Fence agent for Citrix XenServer over XenAPI
Requires: python3-pexpect
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description xenapi
Fence agent for Citrix XenServer accessed over XenAPI.
%files xenapi
%{_sbindir}/fence_xenapi
%{_datadir}/fence/XenAPI.py*
%{_datadir}/fence/__pycache__/XenAPI.*
%{_mandir}/man8/fence_xenapi.8*

%package zvm
License: GPLv2+ and LGPLv2+
Summary: Fence agent for IBM z/VM over IP
Requires: fence-agents-common = %{version}-%{release}
BuildArch: noarch
%description zvm
Fence agent for IBM z/VM over IP.
%files zvm
%{_sbindir}/fence_zvmip
%{_mandir}/man8/fence_zvmip.8*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.5.2-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 23 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.5.2-1
- new upstream release
- added openstack subpackage
- spec improvements based on upstream spec-file

* Tue Sep 24 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.5.1-1
- new upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun  4 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.4.0-1
- new upstream release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.3.3-2
- fence-agents-scsi: add missing fence-agents-common dependency

* Mon Dec  3 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.3.3-1
- new upstream release

* Fri Oct  5 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.3.0-1
- new upstream release

* Wed Sep 19 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.2.1-6
- Fix missing fence-agents-all subpackage after spec improvements

* Wed Aug 22 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.2.1-5
- Python 3: fix has_key() issues

* Mon Aug 20 2018 Jan Pokorný <jpokorny+rpm-booth@fedoraproject.org> - 4.2.1-4
- mark non-compiled packages properly as noarch, restructure excludes
- move azure_fence.py and XenAPI.py to respective subpackages from -common
- sanitize allfenceagents internally defined enumeration
- sanitize BuildRequires with respect to packaging guidelines
- bytecompile native Python modules and ship these bytecodes properly
- only refer to Python binary symbolically, drop buildroot cleanup
- cleanup package summaries/descriptions, order agent subpackages properly

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.2.1-2
- fence_vmware_soap: fix python3-suds issue

* Thu May 31 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.2.1-1
- new upstream release

* Fri May 25 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.2.0-2
- fence_scsi: fix Python 3 encoding issue

* Thu May 17 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.2.0-1
- new upstream release

* Thu Feb 15 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.1-1
- new upstream release
- fence_vmware_soap / fence_ovh: use Python 2 till python3-suds bug
  is fixed

* Fri Feb  9 2018 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.1.0-2
- new upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.24-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.0.24-14
- Cleanup no longer needed Python 2 dependencies

* Tue Nov 07 2017 Troy Dawson <tdawson@redhat.com> - 4.0.24-13
- Cleanup spec file conditionals

* Tue Aug 29 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.0.24-12
- fence-agents-common: remove fence_scsi_check files
- fence-scsi: add "fence_scsi_check_hardreboot"

* Thu Aug  3 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.0.24-10
- fence_zvm: fix "uintptr_t" undeclared

* Thu Aug  3 2017 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.0.24-9
- Fix encoding for pexpect with Python 3.6

  Resolves: rhbz#1473908

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.24-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.24-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 23 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.0.24-5
- Fix to build in Python 3 only environment

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 4.0.24-4
- Rebuild for Python 3.6

* Wed Sep 21 2016 Marek Grac <mgrac@redhat.com> - 4.0.24-4
- Remove Obsoletes that are no longer valid

* Fri Sep  2 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.0.24-2
- fence-agents-common: add dependency on python3-pycurl

* Fri Aug 26 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.0.24-1
- new upstream release

* Wed Jul 13 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.0.23-2
- fix build issue on s390

* Tue Jul 12 2016 Oyvind Albrigtsen <oalbrigt@redhat.com> - 4.0.23-1
- new upstream release
- new package fence-agents-amt-ws
- new package fence-agents-compute
- new package fence-agents-drac
- new package fence-agents-hds-cb
- new package fence-agents-mpath
- new package fence-agents-sanbox2
- new package fence-agents-sbd
- new package fence-agents-vbox
- new package fence-agents-vmware
- new package fence-agents-xenapi

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 11 2015 Marek Grac <mgrac@redhat.com> - 4.0.20-1
- new upstream release
- new package fence-agents-rcd-serial

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 05 2015 Marek Grac <mgrac@redhat.com> - 4.0.16-1
- new upstream release

* Mon Feb 09 2015 Marek Grac <mgrac@redhat.com> - 4.0.15-1
- new upstream release

* Thu Jan 08 2015 Marek Grac <mgrac@redhat.com> - 4.0.14-1
- new upstream release
- new packages fence-agents-zvm and fence-agents-emerson

* Thu Oct 16 2014 Marek Grac <mgrac@redhat.com> - 4.0.12-1
- new upstream release
- new package fence-agents-ilo-ssh

* Wed Aug 27 2014 Marek Grac <mgrac@redhat.com> - 4.0.10
- new upstream release
- new package fence-agents-ilo-moonshot

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Marek Grac <mgrac@redhat.com> - 4.0.9
- new upstream release
- new package fence-agents-pve

* Mon Apr 07 2014 Marek Grac <mgrac@redhat.com> - 4.0.8-1
- new upstream release
- new package fence-agents-raritan

* Wed Feb 26 2014 Marek Grac <mgrac@redhat.com> - 4.0.7-3
- requires a specific version of fence-agents-common

* Mon Feb 17 2014 Marek Grac <mgrac@redhat.com> - 4.0.7-2
- new upstream release
- changed dependancy from nss/nspr to gnutls-utils

* Fri Jan 10 2014 Marek Grac <mgrac@redhat.com> - 4.0.4-4
- new upstream release
- new package fence-agents-amt

* Mon Oct 07 2013 Marek Grac <mgrac@redhat.com> - 4.0.4-3
- new upstream release
- new package fence-agents-netio

* Tue Sep 03 2013 Marek Grac <mgrac@redhat.com> - 4.0.3-1
- new upstream release
- new packages fence-agents-brocade and fence-agents-ovh

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 4.0.1-2
- Perl 5.18 rebuild

* Mon Jul 01 2013 Marek Grac <mgrac@redhat.com> - 4.0.1-1
- new upstream release

* Mon Jun 24 2013 Marek Grac <mgrac@redhat.com> - 4.0.0-5
- fence-agents-all should provide fence-agent for clean update path

* Wed Apr 03 2013 Marek Grac <mgrac@redhat.com> - 4.0.0-4
- minor changes in spec file

* Thu Mar 21 2013 Marek Grac <mgrac@redhat.com> - 4.0.0-3
- minor changes in spec file

* Mon Mar 18 2013 Marek Grac <mgrac@redhat.com> - 4.0.0-2
- minor changes in spec file

* Mon Mar 11 2013 Marek Grac <mgrac@redhat.com> - 4.0.0-1
- new upstream release
- introducing subpackages


