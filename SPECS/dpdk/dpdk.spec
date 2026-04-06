## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Add option to build as static libraries (--without shared)
%bcond_without shared
# Add option to build without examples
%bcond_with examples
# Add option to build without tools
%bcond_without tools

# Avoid architecture-specific name of build-dir to fix per-arch reproducibility with doxygen
%global _vpath_builddir %{_vendor}-%{_target_os}-build

Name: dpdk
Version: 24.11.4
Release: %autorelease
Epoch: 2
URL: http://dpdk.org
Source: https://fast.dpdk.org/rel/dpdk-%{version}.tar.xz

BuildRequires: meson
BuildRequires: python3-pyelftools

Summary: Set of libraries and drivers for fast packet processing

#
# Note that, while this is dual licensed, all code that is included with this
# Pakcage are BSD licensed. The only files that aren't licensed via BSD is the
# kni kernel module which is dual LGPLv2/BSD, and thats not built for fedora.
#
# Automatically converted from old format: BSD and LGPLv2 and GPLv2 - review is highly recommended.
License: LicenseRef-Callaway-BSD AND LicenseRef-Callaway-LGPLv2 AND GPL-2.0-only

#
# The DPDK is designed to optimize througput of network traffic using, among
# other techniques, carefully crafted assembly instructions.  As such it
# needs extensive work to port it to other architectures.
#
ExclusiveArch: x86_64 i686 aarch64 ppc64le

BuildRequires: gcc
BuildRequires: kernel-headers, libpcap-devel, doxygen, /usr/bin/sphinx-build, zlib-devel
BuildRequires: numactl-devel
BuildRequires: rdma-core-devel
BuildRequires: openssl-devel
%ifnarch %{ix86}
BuildRequires: libbpf-devel
%endif
BuildRequires: libfdt-devel
BuildRequires: libatomic
BuildRequires: libarchive-devel

%description
The Data Plane Development Kit is a set of libraries and drivers for
fast packet processing in the user space.

%package devel
Summary: Data Plane Development Kit development files
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release} python3
%if ! %{with shared}
Provides: %{name}-static = %{?epoch:%{epoch}:}%{version}-%{release}
%endif
Requires: rdma-core-devel

%description devel
This package contains the headers and other files needed for developing
applications with the Data Plane Development Kit.

%package doc
Summary: Data Plane Development Kit API documentation
BuildArch: noarch

%description doc
API programming documentation for the Data Plane Development Kit.

%if %{with tools}
%package tools
Summary: Tools for setting up Data Plane Development Kit environment
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: kmod pciutils findutils iproute python3-pyelftools

%description tools
%{summary}
%endif

%if %{with examples}
%package examples
Summary: Data Plane Development Kit example applications
BuildRequires: libvirt-devel
BuildRequires: make

%description examples
Example applications utilizing the Data Plane Development Kit, such
as L2 and L3 forwarding.
%endif

%define sdkdir  %{_datadir}/%{name}
%define docdir  %{_docdir}/%{name}
%define incdir %{_includedir}/%{name}
%define pmddir %{_libdir}/%{name}-pmds

%pretrans -p <lua>
-- This is to clean up directories before links created
-- See https://fedoraproject.org/wiki/Packaging:Directory_Replacement

directories = {
    "/usr/share/dpdk/mk/exec-env/bsdapp",
    "/usr/share/dpdk/mk/exec-env/linuxapp"
}
for i,path in ipairs(directories) do
  st = posix.stat(path)
  if st and st.type == "directory" then
    status = os.rename(path, path .. ".rpmmoved")
    if not status then
      suffix = 0
      while not status do
        suffix = suffix + 1
        status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
      end
      os.rename(path, path .. ".rpmmoved")
    end
  end
end
%prep
%autosetup -p1 -n dpdk%(awk -F. '{ if (NF > 2) print "-stable" }' <<<%{version})-%{version}

%build
CFLAGS="$(echo %{optflags} -fcommon)" \
%meson --includedir=include/dpdk \
       -Ddrivers_install_subdir=dpdk-pmds \
       -Denable_docs=true \
       -Dmachine=generic \
%if %{with examples}
       -Dexamples=all \
%endif
%if %{with shared}
  --default-library=shared
%else
  --default-library=static
%endif

%meson_build

%install
%meson_install

# Taken from debian/rules
rm -f %{buildroot}%{docdir}/html/.buildinfo
rm -f %{buildroot}%{docdir}/html/objects.inv
rm -rf %{buildroot}%{docdir}/html/.doctrees
find %{buildroot}%{_mandir}/ -type f -a ! -iname "*rte_*" -delete

%files
# BSD
%{_bindir}/dpdk-testpmd
%{_bindir}/dpdk-proc-info
%if %{with shared}
%{_libdir}/*.so.*
%{pmddir}/*.so.*
%endif

%files doc
#BSD
%{docdir}

%files devel
#BSD
%{incdir}/
%{sdkdir}
%{_mandir}
%ghost %{sdkdir}/mk/exec-env/bsdapp
%ghost %{sdkdir}/mk/exec-env/linuxapp
%if %{with tools}
%exclude %{_bindir}/dpdk-*.py
%endif
%if %{with examples}
%exclude %{sdkdir}/examples/
%endif
%if ! %{with shared}
%{_libdir}/*.a
%exclude %{_libdir}/*.so
%exclude %{pmddir}/*.so
%else
%{_libdir}/*.so
%{pmddir}/*.so
%exclude %{_libdir}/*.a
%endif
%{_libdir}/pkgconfig/libdpdk.pc
%{_libdir}/pkgconfig/libdpdk-libs.pc

%if %{with tools}
%files tools
%ifnarch %{ix86}
%{_bindir}/dpdk-dumpcap
%{_bindir}/dpdk-pdump
%endif
%{_bindir}/dpdk-graph
%{_bindir}/dpdk-test
%{_bindir}/dpdk-test-*
%{_bindir}/dpdk-*.py
%endif

%if %{with examples}
%files examples
%{_bindir}/dpdk_example_*
%doc %{sdkdir}/examples
%endif

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 2:24.11.4-2
- Latest state for dpdk

* Fri Feb 13 2026 Timothy Redaelli <timothy.redaelli@gmail.com> - 2:24.11.4-1
- Update to 24.11.4

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:24.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 17 2025 Timothy Redaelli <tredaelli@redhat.com> - 2:24.11.2-2
- Update to 24.11.2

* Tue Jun 17 2025 Timothy Redaelli <tredaelli@redhat.com> - 2:24.11.2-1
- Update to 24.11.2

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:24.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jan 04 2025 Timothy Redaelli <tredaelli@redhat.com> - 2:24.11.1-2
- Add smoke test

* Thu Jan 02 2025 Timothy Redaelli <tredaelli@redhat.com> - 2:24.11.1-1
- Update to 24.11.1

* Thu Jan 02 2025 Timothy Redaelli <tredaelli@redhat.com> - 2:24.11-2
- Don't build stuff related to bpf on i686

* Thu Jan 02 2025 Timothy Redaelli <tredaelli@redhat.com> - 2:24.11-1
- Update to 24.11 and migrate to use %%autorelease and %%autochangelog

* Wed Oct 23 2024 Timothy Redaelli <tredaelli@redhat.com> - 2:23.11.2-3
- Add build fixes for Rawhide

* Wed Oct 23 2024 Timothy Redaelli <tredaelli@redhat.com> - 2:23.11.2-2
- Backport upstream fix for Rawhide

* Wed Oct 23 2024 Timothy Redaelli <tredaelli@redhat.com> - 2:23.11.2-1
- Update to 23.11.2

* Wed Oct 23 2024 Timothy Redaelli <tredaelli@redhat.com> - 2:23.11-4
- Add gating support

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 2:23.11-3
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:23.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Mar 04 2024 Timothy Redaelli <tredaelli@redhat.com> - 2:23.11-1
- Update to 23.11

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:22.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:22.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:22.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 03 2023 Timothy Redaelli <tredaelli@redhat.com> - 2:22.11.1-1
- Update to 22.11.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:21.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 28 2022 Jiri Olsa <jolsa@kernel.org> - 2:21.11.2-2
- Rebuild for libbpf 1.0.0

* Fri Sep 09 2022 Timothy Redaelli <tredaelli@redhat.com> - 2:21.11.2-1
- Update to 21.11.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:21.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 06 2022 Timothy Redaelli <tredaelli@redhat.com> - 2:21.11.1-3
- Support compressed firmwares

* Fri Apr 29 2022 Timothy Redaelli <tredaelli@redhat.com> - 2:21.11.1-2
- Use -stable as directory for stable builds

* Fri Apr 29 2022 Timothy Redaelli <tredaelli@redhat.com> - 2:21.11.1-1
- Update to 21.11.1

* Wed Mar 09 2022 Timothy Redaelli <tredaelli@redhat.com> - 2:21.11-2
- Fix changelog

* Wed Mar 09 2022 Timothy Redaelli <tredaelli@redhat.com> - 2:21.11-1
- Update to 21.11

* Mon Jan 31 2022 nucleo <nucleo@fedoraproject.org> - 2:20.11-5
- fix error: %%changelog not in descending chronological order

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:20.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:20.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 17 2021 Timothy Redaelli <tredaelli@redhat.com> - 2:20.11-2
- Fix dpdk-doc generation

* Tue Feb 16 2021 Timothy Redaelli <tredaelli@redhat.com> - 2:20.11-1
- Update to 20.11

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:19.11.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 17 2020 Tom Stellard <tstellar@redhat.com> - 2:19.11.3-3
- Add BuildRequires: make

* Tue Sep 01 2020 Jeff Law <law@redhat.com> - 2:19.11.3-2
- Re-enable LTO

* Tue Sep 01 2020 Timothy Redaelli <tredaelli@redhat.com> - 2:19.11.3-1
- Update to latest 19.11 LTS

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:19.11.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Jeff Law <law@redhat.com> - 2:19.11.1-7
- Disable LTO

* Tue Jun 23 2020 Timothy Redaelli <tredaelli@redhat.com> - 2:19.11.1-6
- Fix missing Requires for dpdk-devel (bz1843590)

* Thu Jun 04 2020 Neil Horman <nhorman@tuxdriver.com> - 2:19.11.1-5
- Resolves: 1843590

* Thu Jun 04 2020 Neil Horman <nhorman@tuxdriver.com> - 2:19.11.1-4
- Resolves: bz1843590

* Thu May 07 2020 Neil Horman <nhorman@tuxdriver.com> - 2:19.11.1-3
- resolves: bz1832416

* Mon Apr 06 2020 Timothy Redaelli <tredaelli@redhat.com> - 2:19.11.1-2
- Remove some PMDs on aarch64

* Mon Apr 06 2020 Timothy Redaelli <tredaelli@redhat.com> - 2:19.11.1-1
- Add missing changelog for previous commit

* Mon Apr 06 2020 Timothy Redaelli <tredaelli@redhat.com> - 2:19.11-1
- Update to DPDK 19.11.1

* Fri Feb 07 2020 Timothy Redaelli <tredaelli@redhat.com> - 2:18.11.6-1
- Update to latest 18.11 LTS Add -fcommon to CFLAGS as workaround in order
  to make it build on GCC 10

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:18.11.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 04 2019 Timothy Redaelli <tredaelli@redhat.com> - 2:18.11.2-5
- Pass the correct LDFLAGS to host apps (dpdk-pmdinfogen) too

* Wed Sep 11 2019 Than Ngo <than@redhat.com> - 2:18.11.2-4
- Fix multilib issue, different outputs on different arches

* Mon Aug 26 2019 Neil Horman <nhorman@tuxdriver.com> - 2:18.11.2-3
- Resolves: bz1742942

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:18.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Timothy Redaelli <tredaelli@redhat.com> - 2:18.11.2-1
- Update to latest 18.11 LTS

* Thu Feb 28 2019 Timothy Redaelli <tredaelli@redhat.com> - 2:18.11-1
- Update to latest LTS release

* Thu Feb 28 2019 Timothy Redaelli <tredaelli@redhat.com> - 2:17.11.2-11
- Fix changelog date

* Sat Feb 16 2019 Eric Kinzie <eric@qosient.com> - 2:17.11.2-10
- fix test for RTE_SDK variable in csh profile

* Wed Feb 13 2019 Neil Horman <nhorman@tuxdriver.com> - 2:17.11.2-9
- Resolves: 1674825

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:17.11.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 28 2018 Neil Horman <nhorman@tuxdriver.com> - 2:17.11.2-7
- Add wdiff to BuildRequires

* Thu Sep 27 2018 Neil Horman <nhorman@tuxdriver.com> - 2:17.11.2-6
- Resolves: bz 1548404

* Thu Sep 27 2018 Neil Horman <nhorman@tuxdriver.com> - 2:17.11.2-5
- Resolves: bz 1548404

* Thu Sep 27 2018 Neil Horman <nhorman@tuxdriver.com> - 2:17.11.2-4
- Resolves: bz1548404

* Thu Sep 27 2018 Neil Horman <nhorman@tuxdriver.com> - 2:17.11.2-3
- Resolves: bz 1548404

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:17.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 24 2018 Neil Horman <nhorman@tuxdriver.com> - 2:17.11.2-1
- Resolves: bz1571361

* Tue Apr 10 2018 Timothy Redaelli <tredaelli@redhat.com> - 2:17.11.1-3
- Fix "Requires: dpdk" by adding epoch

* Fri Apr 06 2018 Neil Horman <nhorman@tuxdriver.com> - 2:17.11.1-2
- Resolves: bz 1564548

* Fri Apr 06 2018 Neil Horman <nhorman@tuxdriver.com> - 2:17.11.1-1
- Update DPDK to LTS release 17.11.1

* Fri Apr 06 2018 Timothy Redaelli <tredaelli@redhat.com> - 18.02-8
- Replace "/usr/bin/env python" with "/usr/bin/python3"

* Thu Apr 05 2018 Neil Horman <nhorman@tuxdriver.com> - 18.02-7
- Resolves: bz 1564215

* Wed Mar 14 2018 Neil Horman <nhorman@tuxdriver.com> - 18.02-6
- Fixing date in changelog

* Thu Mar 08 2018 Neil Horman <nhorman@tuxdriver.com> - 18.02-5
- Resolves: 1548404

* Tue Feb 27 2018 Neil Horman <nhorman@tuxdriver.com> - 18.02-4
- Resolves bz 1548404

* Tue Feb 27 2018 Neil Horman <nhorman@tuxdriver.com> - 18.02-3
- Resolves bz 1548404

* Tue Feb 27 2018 Neil Horman <nhorman@tuxdriver.com> - 18.02-2
- Resolves bz 1548404

* Mon Feb 26 2018 Neil Horman <nhorman@tuxdriver.com> - 18.02-1
- Resolves: bz 1545455

* Mon Feb 19 2018 Timothy Redaelli <tredaelli@redhat.com> - 17.11-5
- Add BuildRequires: gcc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 17.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 03 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 17.11-3
- Update Python 2 dependency declarations to new packaging standards

* Thu Nov 30 2017 Neil Horman <nhorman@tuxdriver.com> - 17.11-2
- Resolves: bz1519322 Resolves: bz1519332 Resolves: bz1519336

* Thu Nov 16 2017 Neil Horman <nhorman@tuxdriver.com> - 17.11-1
- Update to latest upstream

* Thu Aug 10 2017 Neil Horman <nhorman@tuxdriver.com> - 17.08-1
- dpdk: update to 17.08 (bz 1479601)

* Mon Jul 31 2017 Neil Horman <nhorman@tuxdriver.com> - 17.05-3
- Resolves: bz 1476341

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 17.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Neil Horman <nhorman@hmswarspite.think-freely.org> - 17.05-1
- Resolves: bz 1450021

* Fri Feb 24 2017 Neil Horman <nhorman@hmswarspite.think-freely.org> - 17.02-2
- Resolves: bz 1426561

* Wed Feb 22 2017 Neil Horman <nhorman@hmswarspite.think-freely.org> - 17.02-1
- Resolves: bz 142285

* Tue Feb 07 2017 Neil Horman <nhorman@hmswarspite.think-freely.org> - 16.11-3
- REsolves: bz 1419731

* Tue Feb 07 2017 Neil Horman <nhorman@hmswarspite.think-freely.org> - 16.11-2
- Resolves: bz 1419731

* Tue Nov 15 2016 Neil Horman <nhorman@redhat.com> - 16.11-1
- Resolves: Bz 1394589

* Tue Aug 02 2016 Neil Horman <nhorman@redhat.com> - 16.07-1
- resolves: bz 1361451

* Thu Apr 14 2016 Panu Matilainen <pmatilai@redhat.com> - 16.04-1
- Update to 16.04 - Drop all patches, they're not needed anymore - Drop
  linker script generation, its upstream now - Enable vhost numa support
  again

* Wed Mar 16 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-15
- Generalize target/machine/etc macros to enable i686 builds

* Wed Mar 16 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-14
- vhost numa code causes crashes, disable until upstream fixes

* Tue Mar 01 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-13
- Disable unmaintained librte_power as per upstream recommendation

* Tue Mar 01 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-12
- Eliminate the need for the enic patch by eliminating second -Wall from
  CFLAGS

* Tue Mar 01 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-11
- Drop no longer needed -Wno-error=array-bounds from CFLAGS

* Tue Mar 01 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-10
- Drop no longer needed bnx2x patch, the gcc false positive has been fixed

* Tue Feb 16 2016 Neil Horman <nhorman@tuxdriver.com> - 2.2.0-9
- Resolves: bz 1307431

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us> - 2.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-7
- Quoting fixes in the spec
- Use a different quoting method to avoid messing up vim syntax
  highlighting
- CONFIG_RTE_MACHINE value needs to be quoted too

* Mon Jan 25 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-6
- Enable librte_vhost NUMA-awareness

* Wed Jan 20 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-5
- Adopt upstream standard installation layout now that there is one.

* Wed Jan 20 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-4
- Define & use a macro for includedir location throughout the spec

* Wed Jan 20 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-3
- Make option matching stricter in spec setconf

* Wed Jan 20 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-2
- Establish a driver directory for automatic driver loading.

* Wed Jan 20 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-1
- Update to dpdk 2.2.0

* Fri Nov 13 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-16
- dpdk.spec: Build an examples SDK package

* Fri Nov 13 2015 Panu Matilainen <pmatilai@redhat.com> - 2.1.0-15
- dpdk.spec: PMD builds: Enable the bnx2x build

* Fri Nov 13 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-14
- dpdk.spec: linkage and file overlap

* Tue Oct 27 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-13
- dpdk.spec: dpdk: bundle tools separately

* Fri Oct 02 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-12
- dpdk.spec: Add a changelog entry and bump minor to 2

* Fri Oct 02 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-11
- dpdk.spec: Rename the combined library from libintel_dpdk to libdpdk

* Fri Oct 02 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-10
- dpdk-config: Remove the config patch file, and rewrite the config file
  post `make config'

* Fri Oct 02 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-9
- dpdk.spec: Move the sdk libraries into the system library directory

* Fri Oct 02 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-8
- dpdk.spec: Allow builds to have the lightweight api-guide as well as the
  full pdf build

* Fri Oct 02 2015 Panu Matilainen <pmatilai@redhat.com> - 2.1.0-7
- dpdk.spec: Make lib and include available both ways in the SDK paths

* Fri Oct 02 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-6
- dpdk.spec: Remove the combined build option

* Fri Oct 02 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-5
- dpdk.spec: Include the scripts directory.

* Fri Oct 02 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-4
- dpdk.spec: Do not honor environmental IDs for RTE_SDK, etc.

* Fri Oct 02 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-3
- dpdk.spec: Package the dpdk tools into the -tools package

* Fri Oct 02 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-2
- dpdk.spec: Do not avoid array-bounds warning by patching the sources

* Thu Aug 27 2015 Neil Horman <nhorman@tuxdriver.com> - 2.1.0-1
- Resolves: bz 1256137

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 08 2015 Neil Horman <nhorman@tuxdriver.com> - 2.0.0-1
- Resolves: bz1208922

* Wed Jan 28 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-23
- Always build with -fPIC

* Wed Jan 28 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-22
- Doh, bogus dates + remember to bump the actual release too

* Wed Jan 28 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-21
- Add a spec option to build as shared libraries, default to static for now

* Wed Jan 28 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-20
- Comply to Fedora static package policies
- Move static libraries to -devel, there's no point in having them in a
  "runtime" package anyway
- Add dpdk-static = %%{version}-%%{release} provide to -devel
- Have the main package always own the private library directory though

* Wed Jan 28 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-19
- Add a spec option to build a combined library

* Wed Jan 28 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-18
- Drop now unnecessary debug flags patch.

* Wed Jan 28 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-17
- Avoid variable expansion in the spec here-documents during build

* Tue Jan 27 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-16
- Arrange for RTE_SDK environment + directory layout expected by DPDK apps
  - Drop config from main package, it shouldn't be needed at runtime

* Tue Jan 27 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-15
- Avoid unnecessary use of %%global, lazy expansion is normally better.
  (yes, Fedora recommendation is misguided wrt this: %%global has unwanted
  side-effects when used blindly for "everything", greetings from your
  friendly former rpm maintainer) - Drop unused destdir macro from the spec
  while at it

* Tue Jan 27 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-14
- Drop unnecessary kernel-devel BR, we are not building kernel modules

* Tue Jan 27 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-13
- Clean up summaries and descriptions. The ones copied from upstream spec
  talk about kernel modules and other yadda that we will not include.

* Tue Jan 27 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-12
- Avoid unnecessary %%exclude by not copying unpackaged content to
  buildroot, %%exclude can have side-effects when used like this.

* Tue Jan 27 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-11
- Force sane mode on the headers

* Tue Jan 27 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-10
- Copy the headers instead of broken symlinks into -devel package

* Sat Aug 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 21 2014 John W. Linville <linville@tuxdriver.com> - 1.7.0-8
- Several changes to better comply with packaging guidelines...
- Use EXTRA_CFLAGS to include standard Fedora compiler flags in build
- Set CONFIG_RTE_MACHINE=default to build for least-common-denominator
  machines
- Turn-off build of librte_acl, since it does not build on default machines
- Turn-off build of physical device PMDs that require kernel support
- Clean-up the install rules to match current packaging
- Correct changelog versions 1.0.7 -> 1.7.0
- Remove ix86 from ExclusiveArch -- it does not build with above changes

* Thu Jul 10 2014 Neil Horman <nhorman@tuxdriver.com> - 1.7.0-7
- Updating dpdk to official 1.7.0 release

* Thu Jul 03 2014 Neil Horman <nhorman@tuxdriver.com> - 1.7.0-6
- Fixing up release numbering

* Tue Jul 01 2014 Neil Horman <nhorman@tuxdriver.com> - 1.7.0-5
- Fixing some build issues (debuginfo empty, 32 bit build missing)

* Wed Jun 11 2014 Neil Horman <nhorman@tuxdriver.com> - 1.7.0-4
- Fix doc package dependency

* Mon Jun 09 2014 Neil Horman <nhorman@tuxdriver.com> - 1.7.0-3
- Fixed doc package arch dependency

* Mon Jun 09 2014 Neil Horman <nhorman@tuxdriver.com> - 1.7.0-2
- Fix verbose build and debuginfo missing source issue

* Fri Jun 06 2014 Neil Horman <nhorman@tuxdriver.com> - 1.7.0-1
- Initial commit
## END: Generated by rpmautospec
