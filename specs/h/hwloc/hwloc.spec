## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:   Portable Hardware Locality - portable abstraction of hierarchical architectures
Name:      hwloc
Version:   2.12.0
Release:   %autorelease
License:   BSD-2-Clause
URL:       http://www.open-mpi.org/projects/hwloc/
Source0:   https://download.open-mpi.org/release/hwloc/v2.11/hwloc-%{version}.tar.bz2
Requires:  %{name}-libs%{?_isa} = %{version}-%{release}

BuildRequires: gcc
# C++ only for hwloc-hello-cpp test:
BuildRequires: gcc-c++
BuildRequires: cairo-devel
BuildRequires: libpciaccess-devel
BuildRequires: libX11-devel
BuildRequires: libxml2-devel
BuildRequires: lynx
BuildRequires: ncurses-devel
%if %{undefined rhel}
%ifarch x86_64
BuildRequires: oneapi-level-zero-devel
%endif
%endif
BuildRequireS: opencl-headers
BuildRequireS: ocl-icd-devel
BuildRequires: desktop-file-utils
BuildRequires: numactl-devel
BuildRequires: rdma-core-devel
BuildRequires: systemd-devel
%ifarch %{ix86} x86_64
%{?systemd_requires}
BuildRequires: systemd
%endif
BuildRequires: make

%description
The Portable Hardware Locality (hwloc) software package provides
a portable abstraction (across OS, versions, architectures, ...)
of the hierarchical topology of modern architectures, including
NUMA memory nodes,  shared caches, processor sockets, processor cores
and processing units (logical processors or "threads"). It also gathers
various system attributes such as cache and memory information. It primarily
aims at helping applications with gathering information about modern
computing hardware so as to exploit it accordingly and efficiently.

hwloc may display the topology in multiple convenient formats.
It also offers a powerful programming interface (C API) to gather information
about the hardware, bind processes, and much more.

%package devel
Summary:   Headers and shared development libraries for hwloc
Requires:  %{name}-libs%{?_isa} = %{version}-%{release}
%ifnarch %{arm}
Requires:  rdma-core-devel%{?_isa}
%endif

%description devel
Headers and shared object symbolic links for the hwloc.

%package libs
Summary:   Run time libraries for the hwloc

%description libs
Run time libraries for the hwloc

%package gui
Summary:   The gui-based hwloc program(s)
Requires:  %{name}-libs%{?_isa} = %{version}-%{release}

%description gui
GUI-based tool for displaying system topology information.

%package plugins
Summary:   Plugins for hwloc
Requires:  %{name}-plugins%{?_isa} = %{version}-%{release}

%description plugins
 This package contains plugins for hwloc. This includes
  - PCI support
  - GL support
  - libxml support

%prep
%autosetup -p1

%build
%configure --enable-plugins --disable-silent-rules --runstatedir=/run
# Remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

%install
%make_install

# We don't ship .la files.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

cp -p AUTHORS COPYING NEWS README VERSION %{buildroot}%{_pkgdocdir}
cp -pr doc/examples %{buildroot}%{_pkgdocdir}
# Fix for BZ1253977
mv  %{buildroot}%{_pkgdocdir}/examples/Makefile  %{buildroot}%{_pkgdocdir}/examples/Makefile_%{_arch}

desktop-file-validate %{buildroot}/%{_datadir}/applications/lstopo.desktop

# Avoid making hwloc-gui depend on hwloc
rm %{buildroot}%{_mandir}/man1/lstopo.1
ln %{buildroot}%{_mandir}/man1/lstopo-no-graphics.1 %{buildroot}%{_mandir}/man1/lstopo.1

# Deal with service file
# https://github.com/open-mpi/hwloc/issues/221
%ifarch %{ix86} x86_64
mkdir -p %{buildroot}%{_unitdir}
mv %{buildroot}%{_datadir}/%{name}/hwloc-dump-hwdata.service %{buildroot}%{_unitdir}/
%else
rm %{buildroot}%{_datadir}/%{name}/hwloc-dump-hwdata.service
%endif

%check
LD_LIBRARY_PATH=$PWD/hwloc/.libs make check

%ifarch %{ix86} x86_64
%post
%systemd_post hwloc-dump-hwdata.service

%preun
%systemd_preun hwloc-dump-hwdata.service

%postun
%systemd_postun_with_restart hwloc-dump-hwdata.service
%endif

%files
%{_datadir}/bash-completion/completions/*
%{_bindir}/%{name}*
%{_bindir}/lstopo-no-graphics
%{_datadir}/hwloc/hwloc-ps.www/
%{_mandir}/man1/%{name}*
%{_mandir}/man1/lstopo-no-graphics*
%ifarch %{ix86} x86_64
%{_sbindir}/hwloc-dump-hwdata
%{_unitdir}/hwloc-dump-hwdata.service
%endif

%files devel
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_includedir}/%{name}.h
%{_pkgdocdir}/examples
%{_libdir}/*.so

%files libs
%{_mandir}/man7/%{name}*
%dir %{_datadir}/%{name}
%{_datadir}/hwloc/hwloc.dtd
%{_datadir}/hwloc/hwloc-valgrind.supp
%{_datadir}/hwloc/hwloc2.dtd
%{_datadir}/hwloc/hwloc2-diff.dtd
%dir %{_pkgdocdir}/
%{_pkgdocdir}/*[^c]
%{_libdir}/libhwloc*so.15*

%files gui
%{_bindir}/lstopo
%{_mandir}/man1/lstopo.1*
%{_datadir}/applications/lstopo.desktop

%files plugins
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/hwloc*

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2.12.0-3
- test: add initial lock files

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Mar 10 2025 Jirka Hladky <jhladky@redhat.com> - 2.12.0-1
- Updated to hwloc-2.12.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 27 2024 Jirka Hladky <jhladky@redhat.com> - 2.11.2-1
- Updated to hwloc-2.11.2

* Wed Aug 21 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.11.1-3
- Disable oneapi-level-zero in RHEL

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Jirka Hladky <jhladky@redhat.com> - 2.11.1-1
- Updated to 2.11.1

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 05 2023 Jirka Hladky <jhladky@redhat.com> - 2.10.0-1
- Updated to version 2.10.0

* Mon Oct 09 2023 Jirka Hladky <jhladky@redhat.com> - 2.9.3-1
- Updated to version 2.9.3

* Sat Jul 29 2023 Prarit Bhargava <prarit@redhat.com> - 2.9.0-8
- hwloc.spec: migrated to SPDX license

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Feb 24 2023 Michal Schmidt <mschmidt@redhat.com> - 2.9.0-6
- oneapi-level-zero-devel is ExclusiveArch x86_64

* Fri Feb 24 2023 Michal Schmidt <mschmidt@redhat.com> - 2.9.0-5
- add BRs for optional hwloc functionality

* Fri Feb 24 2023 Michal Schmidt <mschmidt@redhat.com> - 2.9.0-4
- Drop %%ifnarch conditions about no longer relevant archs

* Fri Feb 24 2023 Michal Schmidt <mschmidt@redhat.com> - 2.9.0-3
- drop BRs for generating docs

* Fri Feb 24 2023 Michal Schmidt <mschmidt@redhat.com> - 2.9.0-2
- drop ldconfig_scriptlets

* Fri Feb 24 2023 Michal Schmidt <mschmidt@redhat.com> - 2.9.0-1
- Update to v2.9.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 11 2021 Jirka Hladky <hladky.jiri@gmail.com> - 2.5.0-1
- Update to 2.5.0

* Thu Mar 18 2021 Dan Horák <dan[at]danny.cz> - 2.4.1-3
- use lynx instead of w3m to reduce deps

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.1-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Mar 01 2021 Jirka Hladky <hladky.jiri@gmail.com> - 2.4.1-1
- Update to 2.4.1

* Wed Feb 24 2021 Prarit Bhargava <prarit@redhat.com> - 2.2.0-3
- remove libXNVCtrl dependency

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 03 2020 Orion Poplawski <orion@nwra.com> - 2.2.0-1
- Update to 2.2.0

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Orion Poplawski <orion@nwra.com> - 2.0.4-2
- Drop BR/R on rdma-core-devel on arm (bz#1780813)

* Sat Aug 24 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.4-1
- Update to latest version (#1663624)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Michal Schmidt <mschmidt@redhat.com> - 1.11.12-1
- Upstream release 1.11.12.
- BR rdma-core-devel even on arm.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 05 2018 Michal Schmidt <mschmidt@redhat.com> - 1.11.9-1
- Update to 1.11.9.
- BuildRequire gcc, gcc-c++. Drop Group tags.
- BuildRequire numactl-devel on s390x too.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.11.8-5
- Switch to %%ldconfig_scriptlets

* Thu Nov 16 2017 Michal Schmidt <mschmidt@redhat.com> - 1.11.8-4
- Configure with runstatedir set to /run.

* Tue Nov 14 2017 Michal Schmidt <mschmidt@redhat.com> - 1.11.8-3
- BuildRequire rdma-core-devel on s390(x).
- Install the hwloc-dump-hwdata.service systemd service on x86/x86_64.

* Thu Nov 02 2017 Michal Schmidt <mschmidt@redhat.com> - 1.11.8-2
- Use the _pkgdocdir macro.
- Deal with rpaths using the method from Packaging Guidelines.

* Fri Oct 27 2017 Michal Schmidt <mschmidt@redhat.com> - 1.11.8-1
- Update to 1.11.8.

* Wed Aug 23 2017 Adam Williamson <awilliam@redhat.com> - 1.11.5-6
- Use 'rdma-core-devel' not 'libibverbs-devel' for dependencies

* Wed Aug 23 2017 Adam Williamson <awilliam@redhat.com> - 1.11.5-5
- Disable libibverbs support on 32-bit ARM (#1484155)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 23 2016 Orion Poplawski <orion@cora.nwra.com> - 1.11.5-1
- Update to 1.11.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 16 2015 Orion Poplawski <orion@cora.nwra.com> - 1.11.0-5
- numactl is available on aarch64 now

* Fri Sep 04 2015 Dan Horák <dan[at]danny.cz> - 1.11.0-4
- fix devel Requires for s390(x)

* Tue Aug 18 2015 Jirka Hladky <hladky.jiri@gmail.com> - 1.10.0-3
- Fix for BZ1253977

* Tue Jul 21 2015 Orion Poplwski <orion@cora.nwra.com> - 1.11.0-1
- Update to version 1.11.0 (fixes bug #1208279)
- Drop arm patch applied upstream
- Make hwloc-devel require libibverbs-devel (bug #1191770)
- Fix man page manipulation (bug #1235954)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 4 2015 Orion Poplwski <orion@cora.nwra.com> - 1.10.1-2
- Fix hwloc issue on arm

* Wed Apr 1 2015 Orion Poplwski <orion@cora.nwra.com> - 1.10.1-1
- Update to version 1.10.1

* Tue Oct 07 2014 Jirka Hladky <hladky.jiri@gmail.com> - 1.10.0-1
- Update to version 1.10.0

* Fri Sep 26 2014 Jirka Hladky <hladky.jiri@gmail.com> - 1.9.1-1
- Update to version 1.9.1
- Added support for plugins

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr  1 2014 Jirka Hladky <hladky.jiri@gmail.com> - 1.9-1
- Update to 1.9
- Split out lstopo into a -gui subpackage, so the hwloc base package
  does not pull in all of X.

* Fri Feb 14 2014 Jirka Hladky <hladky.jiri@gmail.com> - 1.8.1-2
- Fixed BuildRequires

* Thu Feb 13 2014 Jirka Hladky <hladky.jiri@gmail.com> - 1.8.1-1
- Update to 1.8.1

* Sat Jan 04 2014 Jirka Hladky <hladky.jiri@gmail.com> - 1.8-2
- Unversioned docdir change, more info on
  https://fedoraproject.org/wiki/Changes/UnversionedDocdirs

* Thu Dec 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.8-1
- Update to 1.8
- No numa on aarch64
- Cleanup and modernise spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May  9 2013 Jirka Hladky <hladky.jiri@gmail.com> - 1.7-1
- Minor issue with the man page fixed

* Tue Apr 23 2013 Jirka Hladky <hladky.jiri@gmail.com> - 1.7-0
- Update to version 1.7

* Thu Jan 31 2013 Jirka Hladky <hladky.jiri@gmail.com> - 1.6.1-1
- Created libs package with reduced dependencies

* Sat Jan 19 2013 Jirka Hladky <hladky.jiri@gmail.com> - 1.6.1-0
- Update to version 1.6.1

* Mon Nov  5 2012  Jirka Hladky  <hladky.jiri@gmail.com> - 1.5.1-1
- Update to version 1.5.1

* Wed Aug 15 2012 Jirka Hladky  <hladky.jiri@gmail.com> - 1.5-1
- Update to version 1.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> - 1.4.2-1
- Update to version 1.4.2

* Wed Apr 18 2012 Jirka Hladky  <hladky.jiri@gmail.com> - 1.4.1-2
- Fixed build dependency for s390x

* Mon Apr 16 2012 Jirka Hladky  <hladky.jiri@gmail.com> - 1.4.1-1
- Update to version 1.4.1
- BZ812622 - libnuma was splitted out of numactl package

* Thu Apr 12 2012 Dan Horák <dan[at]danny.cz> - 1.4-2
- no InfiniBand on s390(x)

* Tue Feb 14 2012 Jirka Hladky  <hladky.jiri@gmail.com> - 1.4-1
- Update to 1.4 release

* Mon Nov 14 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3-1
- Update build for ARM support

* Sat Oct 15 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.3-0
- 1.3 release
- added dependency on libibverbs-devel pciutils-devel
- cannot provide support for cuda (cuda_runtime_api.h).
- Nvidia CUDA is free but not open-source therefore not in Fedora.

* Fri Oct 07 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2.2-1
- moved *.so to the devel package
- libhwloc*so* in the main package

* Wed Oct 05 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2.2-0
- 1.2.2 release
- Fix for BZ https://bugzilla.redhat.com/show_bug.cgi?id=724937 for 32-bit PPC

* Sat Sep 17 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2.1-0
- 1.2.1 release
- Moved libhwloc*.so* to the main package

* Mon Jun 27 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2-0
- 1.2 release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan  3 2011 Dan Horák <dan[at]danny.cz> - 1.1-0.1
- fix build on s390(x) where numactl is missing

* Sat Jan  1 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.1-0
- 1.1 rel# Patch to the 1.1 fix 2967 http://www.open-mpi.org/software/hwloc/nightly/v1.1/hwloc-1.1rc6r2967.tar.bz2
- Fix hwloc_bitmap_to_ulong right after allocating the bitmap.
- Fix the minimum width of NUMA nodes, caches and the legend in the graphical lstopo output.
- Cleanup error management in hwloc-gather-topology.sh.
- Add a manpage and usage for hwloc-gather-topology.sh on Linux.
- Rename hwloc-gather-topology.sh to hwloc-gather-topology to be consistent with the upcoming version 1.2ease

* Mon Jul 19 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.2-1
- 1.0.2 release
- added "check" section to the RPM SPEC file

* Mon Jul 19 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.2-0.1.rc1r2330
- 1.0.2 release candidate

* Mon Jul 12 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.1-19
- Fixed issues as described at https://bugzilla.redhat.com/show_bug.cgi?id=606498#c6

* Fri Jul 09 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.1-18
- Fixed issues as described at https://bugzilla.redhat.com/show_bug.cgi?id=606498

* Fri Jun 18 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.1-17
- Initial build

## END: Generated by rpmautospec
