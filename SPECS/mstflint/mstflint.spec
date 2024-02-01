Summary:        Mellanox firmware burning application
Name:           mstflint
Version:        4.26.0
Release:        1%{?dist}
License:        GPLv2 OR BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/Mellanox/%{name}
Source0:        https://github.com/Mellanox/%{name}/releases/download/v%{version}-1/%{name}-%{version}-1.tar.gz
ExclusiveArch: arm64 aarch64
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  boost-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libcurl-devel
BuildRequires:  libibmad-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
Requires:       python3

%description
This package contains firmware update tool, vpd dump and register dump tools
for network adapters based on Mellanox Technologies chips.

%package devel
Summary:        Scripts and header files for mstflint
Requires:       %{name} = %{version}-1
Provides:       mstflint-devel = %{version}-1

%prep
%setup -q

%build

MSTFLINT_VERSION_STR="%{name} %{version}-%{release}"
%configure --enable-fw-mgr --enable-adb-generic-tools MSTFLINT_VERSION_STR="${MSTFLINT_VERSION_STR}"
%make_build

%install
%make_install DESTDIR=%{buildroot}
# remove unpackaged files from the buildroot
rm -f %{buildroot}/%{_libdir}/*.la
# create softlinks to old mtcr header and lib locations
# link mtcr_ul to old location
mkdir -p %{buildroot}/%{_includedir}/mtcr_ul
ln -s %{_includedir}/mstflint/mtcr.h %{buildroot}/%{_includedir}/mtcr_ul/mtcr.h
ln -s %{_includedir}/mstflint/mtcr_com_defs.h %{buildroot}/%{_includedir}/mtcr_ul/mtcr_com_defs.h
# link mtcr_ul to old lib path
ln -s %{_libdir}/mstflint/libmtcr_ul.a %{buildroot}/%{_libdir}/libmtcr_ul.a 

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/mstmread
%{_bindir}/mstmwrite
%{_bindir}/mstflint
%{_bindir}/mstregdump
%{_bindir}/mstmtserver
%{_bindir}/mstvpd
%{_bindir}/mstmcra
%{_bindir}/mstconfig
%{_bindir}/mstfwreset
%{_bindir}/mstcongestion
%{_bindir}/mstprivhost
%{_bindir}/mstfwtrace
%{_bindir}/mstresourcedump
%{_bindir}/mstresourceparse
%{_bindir}/mstfwmanager
%{_bindir}/mstarchive
%{CONF_DIR}/ca-bundle.crt
%{_bindir}/mstreg
%{_bindir}/mstlink

%files devel
%{_includedir}/mstflint/cmdif/icmd_cif_common.h
%{_includedir}/mstflint/cmdif/icmd_cif_open.h
%{_includedir}/mstflint/common/compatibility.h
%{_includedir}/mstflint/mtcr.h
%{_includedir}/mstflint/mtcr_com_defs.h
%{_includedir}/mstflint/mtcr_mf.h
%{_includedir}/mstflint/tools_layouts/adb_to_c_utils.h
%{_includedir}/mstflint/tools_layouts/icmd_layouts.h
%{_includedir}/mtcr_ul/mtcr.h
%{_includedir}/mtcr_ul/mtcr_com_defs.h
%{_libdir}/mstflint/libmtcr_ul.a
%{_libdir}/libmtcr_ul.a

%{mstflint_python_tools}/tools_version.py
%{mstflint_python_tools}/mft_logger.py
%{mstflint_python_tools}/mlxpci/*.py
%{mstflint_python_tools}/mstfwtrace/*.py
%{mstflint_python_tools}/mstfwreset/mstfwreset.py
%{mstflint_python_tools}/mstfwreset/mlxfwresetlib/*.py
%{mstflint_python_tools}/mtcr.py
%{mstflint_python_tools}/cmtcr.so
%{mstflint_python_tools}/cmdif.py
%{mstflint_python_tools}/ccmdif.so
%{mstflint_python_tools}/regaccess.py
%{mstflint_python_tools}/regaccess_hca_ext_structs.py
%{mstflint_python_tools}/regaccess_switch_ext_structs.py
%{mstflint_python_tools}/rreg_access.so
%{mstflint_python_tools}/dev_mgt.py
%{mstflint_python_tools}/c_dev_mgt.so
%{mstflint_python_tools}/mstprivhost/mstprivhost.py
%{mstflint_sdkdir}/libresource_dump_sdk.so
%{mstflint_python_tools}/resourcetools/*.py
%{mstflint_python_tools}/resourcetools/segments/*.py

%{mstflint_python_tools}/resourcetools/resourcedump_lib/*.py
%{mstflint_python_tools}/resourcetools/resourcedump_lib/commands/*.py
%{mstflint_python_tools}/resourcetools/resourcedump_lib/cresourcedump/*.py
%{mstflint_python_tools}/resourcetools/resourcedump_lib/fetchers/*.py
%{mstflint_python_tools}/resourcetools/resourcedump_lib/filters/*.py
%{mstflint_python_tools}/resourcetools/resourcedump_lib/utils/*.py
%{mstflint_python_tools}/resourcetools/resourcedump_lib/validation/*.py

%{mstflint_python_tools}/resourcetools/resourceparse_lib/*.py
%{mstflint_python_tools}/resourcetools/resourceparse_lib/parsers/*.py
%{mstflint_python_tools}/resourcetools/resourceparse_lib/resource_data/*.py
%{mstflint_python_tools}/resourcetools/resourceparse_lib/utils/*.py
%{_datadir}/mstflint
%{_mandir}/man1/*

%changelog
* Mon Jan 29 2024 Juan Camposeco <juanarturoc@microsoft.com> - 4.26.0-1
- Upgrade to version 4.26.0-1 from 4.21.0-4

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 4.21.0-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Feb 23 2023 Elaheh Dehghani <edehghani@microsoft.com> - 4.21.0-3
- Enabled 'adb-generic-tools' in build config.

* Tue Aug 30 2022 Zhichun Wan <zhichunwan@microsoft.com> - 4.21.0-2
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Removed Obsoletes
- License verified

* Wed Aug 03 2022 Michal Schmidt <mschmidt@redhat.com> - 4.21.0-1
- Update to upstream release 4.21.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Michal Schmidt <mschmidt@redhat.com> - 4.20.1-1
- Update to upstream release 4.20.1

* Wed May 25 2022 Izabela Bakollari <izabela.bakollari@gmail.com> - 4.20.0-1
- Update to upstream release 4.20.0

* Mon Mar 28 2022 Michal Schmidt <mschmidt@redhat.com> - 4.19.0-0.3
- Rebase to the almost released 4.19.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 03 2021 Honggang Li <honli@redhat.com> - 4.18.0-1
- Rebase mstflint to latest upstream release v4.18.0-1

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 4.17.0-3
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 01 2021 Honggang Li <honli@redhat.com> - 4.17.0-1
- Rebase mstflint to latest upstream release v4.17.0-1

* Wed Apr 07 2021 Honggang Li <honli@redhat.com> - 4.16.0-2
- Rebase mstflint to latest upstream release v4.16.0-2

* Sun Jan 31 2021 Honggang Li <honli@redhat.com> - 4.16.0-1
- Rebase mstflint to latest upstream release v4.16.0-1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 16 2020 Honggang Li <honli@redhat.com> - 4.15.0-1
- Rebase mstflint to latest upstream release v4.15.0-1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 4.14.0-4
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Mon Jun 22 2020 Honggang Li <honli@redhat.com> - 4.14.0-3
- Rebase mstflint to latest upstream release v4.14.0-3

* Sat May 30 2020 Jonathan Wakely <jwakely@redhat.com> - 4.14.0-2
- Rebuilt for Boost 1.73

* Tue Mar 31 2020 Honggang Li <honli@redhat.com> - 4.14.0-1
- Rebase mstflint to latest upstream release v4.14.0-1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Honggang Li <honli@redhat.com> - 4.13.3-2
- Rebase mstflint to latest upstream release v4.13.3-2

* Sun Jan 05 2020 Honggang Li <honli@redhat.com> - 4.13.3-1
- Rebase mstflint to latest upstream release v4.13.3-1

* Thu Oct 17 2019 Honggang Li <honli@redhat.com> - 4.13.1-1
- Rebase mstflint to latest upstream release v4.13.1-1

* Wed Oct 02 2019 Honggang Li <honli@redhat.com> - 4.13.0-1
- Rebase mstflint to latest upstream release v4.13.0-1
- Resolves: bz1758011

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 15 2019 Honggang Li <honli@redhat.com> - 4.11.0-5
- Rebase mstflint to latest upstream release v4.11.0-4

* Fri Feb 22 2019 Honggang Li <honli@redhat.com> - 4.11.0-4
- Fix mstflint segment fault issue for ConnectX-5 HCA
- Resolves: 1679844

* Tue Feb 12 2019 Honggang Li <honli@redhat.com> - 4.11.0-3
- Rebase mstflint to latest upstream release v4.11.0-3
- Resolves: 1676338

* Fri Feb  1 2019 Honggang Li <honli@redhat.com> - 4.11.0-2
- Rebase mstflint to latest upstream release v4.11.0-2
- Resolves: bz1671710

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Jonathan Wakely <jwakely@redhat.com> - 4.10.0-3
- Rebuilt for Boost 1.69

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Honggang Li <honli@redhat.com> - 4.10.0-1
- Rebase to latest upstream release v4.10.0-1
- Resolves: bz1550400

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 4.8.0-4
- Rebuilt for Boost 1.66

* Fri Dec 15 2017 Honggang Li <honli@redhat.com> - 4.8.0-3
- Rebase mstflint to latest upstream release v4.8.0-2
- Resolves: bz1526293

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 27 2017 Honggang Li <honli@redhat.com> - 4.6.0-2
- Add man pages.
- Resolves: bz1427063

* Wed Feb 22 2017 Honggang Li <honli@redhat.com> - 4.6.0-1
- Rebase to latest upstream release 4.6.0.
- Update mstflint package from github.
- Resolves: bz1423970

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-2.12.gd1edd58.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 24 2016 Honggang Li <honli@redhat.com> - 4.4.0-1.12.gd1edd58.1
- Rebase to latest upstream release 4.4.0-1.12.gd1edd58 (bz1369683).

* Fri Apr  8 2016 Honggang Li <honli@redhat.com> - 4.3.0-1.49.g9b9af70.1
- Rebase to latest upstream version 4.3.0-1.49.g9b9af70.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-0.47.gb1cdaf7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 02 2015 Doug Ledford <dledford@redhat.com> - 4.1.0-0.46.gb1cdaf7.1
- Update to latest upstream sources (enables ConnectX-4 support)
- Drop patch that no longer applies

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.11.g6961daa.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.0-0.10.g6961daa.1
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.9.g6961daa.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 20 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 3.0-0.8.g6961daa.1
- Fix FTBFS with -Werror=format-security (#1037207, #1106248)
- ExcludeArch: %%arm aarch64
- Cleanup spec

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.7.g6961daa.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 16 2013 Doug Ledford <dledford@redhat.com> - 3.0-0.6.g6961daa.1
- Update to latest upstream version, which resovles some licensing issues
  on some of the source files

* Fri Aug 09 2013 Doug Ledford <dledford@redhat.com> - 3.0-0.5.gff93670.1
- Update to latest upstream version, which include ConnectIB support

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Doug Ledford <dledford@redhat.com> - 1.4-7
- The upstream tarball as provided is broken.  Clean up the tarball so
  the package builds properly

* Fri Jan 06 2012 Doug Ledford <dledford@redhat.com> - 1.4-6
- Initial import into Fedora

* Wed Oct 26 2011 Doug Ledford <dledford@redhat.com> - 1.4-5.el6
- Update to a version that will support the latest Mellanox CX3 hardware
- Resolves: bz748244

* Mon Aug 08 2011 Doug Ledford <dledford@redhat.com> - 1.4-4.el6
- Fix a bug in mmio space unmapping
- Resolves: bz729061
- Related: bz725016

* Fri Feb 19 2010 Doug Ledford <dledford@redhat.com> - 1.4-3.el6
- Don't include mtcr.h as we don't really expect anything to need Mellanox
  card register definitions except this program, and we already have the
  file.
- Change to ExcludeArch instead of ExclusiveArch so we build in all the right
  places.
- Related: bz543948

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 1.4-2.el6
- Update to tarball from URL instead of from OFED
- Minor tweaks for pkgwrangler import
- Related: bz543948

* Sat Apr 18 2009 Doug Ledford <dledford@redhat.com> - 1.4-1.el5
- Update to ofed 1.4.1-rc3 version
- Related: bz459652

* Tue Apr 01 2008 Doug Ledford <dledford@redhat.com> - 1.3-1
- Update to OFED 1.3 final bits
- Related: bz428197

* Sun Jan 27 2008 Doug Ledford <dledford@redhat.com> - 1.2-2
- Obsolete the old openib-mstflint package

* Fri Jan 25 2008 Doug Ledford <dledford@redhat.com> - 1.2-1
- Initial import into CVS
- Related: bz428197

* Thu Jul 19 2007 - Vladimir Sokolovsky vlad@mellanox.co.il
- Initial Package, Version 1.2
