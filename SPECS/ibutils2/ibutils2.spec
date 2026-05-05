#--
# Copyright (c) 2004-2010 Mellanox Technologies LTD. All rights reserved.
# Copyright (c) 2024-2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# This software is available to you under the terms of the
# OpenIB.org BSD license included below:
#
#     Redistribution and use in source and binary forms, with or
#     without modification, are permitted provided that the following
#     conditions are met:
#
#      - Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      - Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials
#        provided with the distribution.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#--


Summary: OpenIB Mellanox InfiniBand Diagnostic Tools
Name: ibutils2
Version: 2.1.1
Release:        1%{?dist}
License: Mellanox Confidential and Proprietary
#Url: 
Group: System Environment/Libraries
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.2.2/SOURCES/mlnx_ofed/OFED-internal-25.10-2.4.1.tgz
Source0:         %{_distro_sources_url}/ibutils2-2.1.1.tar.gz
BuildRoot:       /var/tmp/%{name}-%{version}-build
BuildRequires: rdma-core-devel gcc-c++
#Requires: opensm
Vendor:          Microsoft Corporation

Conflicts: ibutils
Obsoletes: ibutils
Provides: ibutils

%description
ibutils provides IB network and path diagnostics.


%prep
%setup -n %{name}-%{version}


%build
%{configure}	\
	--with-umad=%{?_with_umad}	\
	%{?_configure_options}


#export CFLAGS="$RPM_OPT_FLAGS"
%{__make}

%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT
install -m 755 scripts/ibdiagm.sh $RPM_BUILD_ROOT%{_prefix}/bin/ibdiagm.sh
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ibutils2
$RPM_BUILD_ROOT%{_prefix}/bin/ibdiagm.sh -c $RPM_BUILD_ROOT%{_sysconfdir}/ibutils2/ibdiagm.conf

%clean
rm -rf ${RPM_BUILD_ROOT}
rm -rf ${RPM_BUILD_DIR}/%{name}-%{version}

%global __brp_remove_la_files %nil

%files
%defattr(-,root,root)
#%doc COPYING
%license LICENSE
%{_prefix}/share/doc/ibutils2/release_notes.md
%{_prefix}/share/doc/ibutils2/ibdiagnet_scope.md
%{_prefix}/bin/dump2psl.pl
%{_prefix}/bin/dump2slvl.pl
%{_prefix}/bin/ibdiagnet
%{_prefix}/bin/ibdmchk
%{_prefix}/bin/ibdmtr
%{_prefix}/bin/ibnlparse
%{_prefix}/bin/ibtopodiff
%{_prefix}/bin/ibcongest
%{_prefix}/bin/ibnetsplit
%{_prefix}/bin/ibgenperm
%{_prefix}/bin/smparquery
%{_prefix}/bin/ibdiagnet_csv2xml.*
%{_libdir}/libinifile.a
%{_libdir}/libinifile.la
%{_libdir}/libinifile*.so*
%{_libdir}/libcmdparser.a
%{_libdir}/libcmdparser.la
%{_libdir}/libcmdparser*.so*
%{_libdir}/libibdiag.a
%{_libdir}/libibdiag.la
%{_libdir}/libibdiag*.so*
%{_libdir}/libibdiagnet_plugins_ifc.a
%{_libdir}/libibdiagnet_plugins_ifc.la
%{_libdir}/libibdiagnet_plugins_ifc*.so*
%{_libdir}/libibdiagnet_intenal_packets.a
%{_libdir}/libibdiagnet_intenal_packets.la
%{_libdir}/libibdiagnet_intenal_packets*.so*
%{_libdir}/libibdmcom.a
%{_libdir}/libibdmcom.la
%{_libdir}/libibdmcom*.so*
%{_libdir}/libibis.a
%{_libdir}/libibis.la
%{_libdir}/libibis*.so*
%{_libdir}/libibsysapi.a
%{_libdir}/libibsysapi.la
%{_libdir}/libibsysapi*.so*
%{_libdir}/libtt.a
%{_libdir}/libtt.la
%{_libdir}/libtt*.so*
%{_prefix}/include/infiniband
%{_datadir}/ibdiagnet2.1.1
%{_datadir}/ibdm2.1.1
%{_mandir}/man1/ibdmchk.1*
%{_mandir}/man1/ibdm-ibnl-file.1*
%{_mandir}/man1/ibdm-topo-file.1*
%{_mandir}/man1/ibdmtr.1*
%{_mandir}/man1/ibtopodiff.1*
%{_mandir}/man1/dump2slvl.1*
%{_mandir}/man1/dump2psl.1*
%{_mandir}/man1/ibcongest.1*
%{_mandir}/man1/ibnetsplit.1*
%{_mandir}/man1/ibdiagnet_csv2xml.1*
%{_prefix}/bin/ibdiagm.sh
%{_sysconfdir}/ibutils2/ibdiagm.conf
# END Files


%changelog
* Thu Apr 17 2026 Azure Linux Team - 2.1.1-1
- Initial Azure Linux import from NVIDIA (license: Mellanox Confidential and Proprietary)
- License verified
