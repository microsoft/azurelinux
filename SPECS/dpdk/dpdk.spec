%define _unpackaged_files_terminate_build 0
# Add option to build without examples
%define target %{machine_arch}-%{machine_tmpl}-linuxapp-gcc
# machine_arch maps between rpm and dpdk arch name, often same as _target_cpu
# machine_tmpl is the config template machine name, often "native"
# machine is the actual machine name used in the dpdk make system
%ifarch x86_64
%define machine_arch x86_64
%define machine_tmpl native
%define machine default
%endif
%ifarch i686
%define machine_arch i686
%define machine_tmpl native
%define machine default
%endif
%ifarch aarch64
%define machine_arch arm64
%define machine_tmpl armv8a
%define machine armv8a
%endif
%ifarch ppc64le
%define machine_arch ppc_64
%define machine_tmpl power8
%define machine power8
%endif
# Add option to build with examples, tools subpackages
%bcond_with examples
%bcond_without tools
Summary:        Set of libraries and drivers for fast packet processing
Name:           dpdk
Version:        18.11.2
Release:        7%{?dist}
License:        BSD AND LGPLv2 AND GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://dpdk.org
Source0:        https://fast.%{name}.org/rel/%{name}-%{version}.tar.xz
Patch0:         app-pie.patch
Patch1:         fcf-protection.patch
Patch2:         dpdk-rte-ether-align.patch
BuildRequires:  gcc
BuildRequires:  kernel-headers
BuildRequires:  libnuma-devel
BuildRequires:  libpcap-devel
BuildRequires:  mariner-rpm-macros
BuildRequires:  python3-sphinx
BuildRequires:  zlib-devel
#
# The DPDK is designed to optimize througput of network traffic using, among
# other techniques, carefully crafted assembly instructions.  As such it
# needs extensive work to port it to other architectures.
#
ExclusiveArch:  x86_64 i686 aarch64 ppc64le

%description
The Data Plane Development Kit is a set of libraries and drivers for
fast packet processing in the user space.

%package devel
Summary:        Data Plane Development Kit development files
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3

%description devel
This package contains the headers and other files needed for developing
applications with the Data Plane Development Kit.

%package doc
Summary:        Data Plane Development Kit API documentation
BuildArch:      noarch

%description doc
API programming documentation for the Data Plane Development Kit.

%if %{with tools}
%package tools
Summary:        Tools for setting up Data Plane Development Kit environment
Requires:       %{name} = %{version}-%{release}
Requires:       findutils
Requires:       iproute
Requires:       kmod
Requires:       pciutils
Requires:       python3-pyelftools

%description tools
%{summary}
%endif

%if %{with examples}
%package examples
Summary:        Data Plane Development Kit example applications
BuildRequires:  libvirt-devel

%description examples
Example applications utilizing the Data Plane Development Kit, such
as L2 and L3 forwarding.
%endif

%define sdkdir  %{_datadir}/%{name}
%define docdir  %{_docdir}/%{name}
%define incdir %{_includedir}/%{name}
%define pmddir %{_libdir}/%{name}-pmds
Vendor:         Microsoft Corporation
Distribution:   Mariner

%prep
%setup -q -n dpdk-stable-%{version}
%patch0 -p1
%ifarch x86_64 i686
%patch1 -p1
%endif
%patch2 -p1

%build
%{set_build_flags}
# set up a method for modifying the resulting .config file
function setconf() {
	if grep -q ^$1= %{target}/.config; then
		sed -i "s:^$1=.*$:$1=$2:g" %{target}/.config
	else
		echo $1=$2 >> %{target}/.config
	fi
}

# In case dpdk-devel is installed, we should ignore its hints about the SDK directories
unset RTE_SDK RTE_INCLUDE RTE_TARGET

# Avoid appending second -Wall to everything, it breaks upstream warning
# disablers in makefiles. Strip expclit -march= from optflags since they
# will only guarantee build failures, DPDK is picky with that.
# Note: _hardening_ldflags has to go on the extra cflags line because dpdk is
# astoundingly convoluted in how it processes its linker flags.  Fixing it in
# dpdk is the preferred solution, but adjusting to allow a gcc option in the
# ldflags, even when gcc is used as the linker, requires large tree-wide changes
touch obj.o
gcc -### obj.o 2>&1 | awk '/.*collect2.*/ { print $0}' > ./noopts.txt
gcc -### $(rpm --eval '%{build_ldflags}') obj.o 2>&1 | awk '/.*collect2.*/ {print $0}' > ./opts.txt
EXTRA_RPM_LDFLAGS=$(wdiff -3 -n ./noopts.txt ./opts.txt | sed -e"/^=\+$/d" -e"/^.*\.res.*/d" -e"s/\[-//g" -e"s/\-\]//g" -e"s/{+//g" -e"s/+}//g" -e"s/\/.*\.o //g" -e"s/ \/.*\.o$//g" -e"s/-z .*//g" | tr '\n' ' ')
rm -f obj.o

export EXTRA_CFLAGS="$(echo %{optflags} | sed -e 's:-Wall::g' -e 's:-march=[[:alnum:]]* ::g') -Wformat -fPIC %{_hardening_ldflags}"
%ifarch x86_64 i686
export EXTRA_CFLAGS="$EXTRA_CFLAGS -fcf-protection=full"
%endif
export EXTRA_LDFLAGS=$(echo %{build_ldflags} | sed -e's/-Wl,//g' -e's/-spec.*//')
export HOST_EXTRA_CFLAGS="$EXTRA_CFLAGS $EXTRA_RPM_LDFLAGS"
export EXTRA_HOST_LDFLAGS=$(echo %{build_ldflags} | sed -e's/-spec.*//')

# DPDK defaults to using builder-specific compiler flags.  However,
# the config has been changed by specifying CONFIG_RTE_MACHINE=default
# in order to build for a more generic host.  NOTE: It is possible that
# the compiler flags used still won't work for all Fedora-supported
# machines, but runtime checks in DPDK will catch those situations.

make V=1 O=%{target} T=%{target} %{?_smp_mflags} config

setconf CONFIG_RTE_MACHINE '"%{machine}"'
# Disable experimental features
setconf CONFIG_RTE_NEXT_ABI n
setconf CONFIG_RTE_LIBRTE_MBUF_OFFLOAD n
# Disable unmaintained features
setconf CONFIG_RTE_LIBRTE_POWER n

# Enable automatic driver loading from this path
setconf CONFIG_RTE_EAL_PMD_PATH '"%{pmddir}"'

setconf CONFIG_RTE_LIBRTE_BNX2X_PMD y
setconf CONFIG_RTE_LIBRTE_PMD_PCAP y
setconf CONFIG_RTE_LIBRTE_VHOST_NUMA y

setconf CONFIG_RTE_EAL_IGB_UIO n
setconf CONFIG_RTE_LIBRTE_KNI n
setconf CONFIG_RTE_KNI_KMOD n
setconf CONFIG_RTE_KNI_PREEMPT_DEFAULT n

setconf CONFIG_RTE_APP_EVENTDEV n

setconf CONFIG_RTE_LIBRTE_NFP_PMD y

%ifarch aarch64
setconf CONFIG_RTE_LIBRTE_DPAA_BUS n
setconf CONFIG_RTE_LIBRTE_DPAA_MEMPOOL n
setconf CONFIG_RTE_LIBRTE_DPAA_PMD n
%endif

setconf CONFIG_RTE_BUILD_SHARED_LIB y

make V=1 O=%{target} %{?_smp_mflags} -Wimplicit-fallthrough=0

%if %{with examples}
make V=1 O=%{target}/examples T=%{target} %{?_smp_mflags} examples
%endif

%install
# In case dpdk-devel is installed
unset RTE_SDK RTE_INCLUDE RTE_TARGET

%make_install O=%{target} prefix=%{_usr} libdir=%{_libdir}

%if ! %{with tools}
rm -rf %{buildroot}%{sdkdir}/usertools
rm -rf %{buildroot}%{_sbindir}/dpdk_nic_bind
rm -rf %{buildroot}%{_bindir}/dpdk-test-crypto-perf
rm -rf %{buildroot}%{_bindir}/testbbdev
%else
mv %{buildroot}%{_bindir}/testbbdev %{buildroot}%{_bindir}/dpdk-test-bbdev
%endif
rm -f %{buildroot}%{sdkdir}/usertools/dpdk-setup.sh
rm -f %{buildroot}%{sdkdir}/usertools/meson.build

%if %{with examples}
find %{target}/examples/ -name "*.map" | xargs rm -f
for f in %{target}/examples/*/%{target}/app/*; do
    bn=`basename ${f}`
    cp -p ${f} %{buildroot}%{_bindir}/dpdk_example_${bn}
done
%endif

# Replace /usr/bin/env python with /usr/bin/python3
find %{buildroot}%{sdkdir}/ -name "*.py" -exec \
  sed -i -e 's|#!\s*/usr/bin/env python|#!/usr/bin/python3|' {} +

# Create a driver directory with symlinks to all pmds
mkdir -p %{buildroot}/%{pmddir}
for f in %{buildroot}/%{_libdir}/*_pmd_*.so.*; do
    bn=$(basename ${f})
    ln -s ../${bn} %{buildroot}%{pmddir}/${bn}
done

# Setup RTE_SDK environment as expected by apps etc
mkdir -p %{buildroot}/%{_sysconfdir}/profile.d
cat << EOF > %{buildroot}/%{_sysconfdir}/profile.d/dpdk-sdk-%{_arch}.sh
if [ -z "\${RTE_SDK}" ]; then
    export RTE_SDK="%{sdkdir}"
    export RTE_TARGET="%{target}"
    export RTE_INCLUDE="%{incdir}"
fi
EOF

cat << EOF > %{buildroot}/%{_sysconfdir}/profile.d/dpdk-sdk-%{_arch}.csh
if ( ! \$?RTE_SDK ) then
    setenv RTE_SDK "%{sdkdir}"
    setenv RTE_TARGET "%{target}"
    setenv RTE_INCLUDE "%{incdir}"
endif
EOF

# Fixup target machine mismatch
sed -i -e 's:-%{machine_tmpl}-:-%{machine}-:g' %{buildroot}/%{_sysconfdir}/profile.d/dpdk-sdk*

%files
# BSD
%doc README MAINTAINERS
%license license/README
%license license/bsd-3-clause.txt
%license license/exceptions.txt
%license license/gpl-2.0.txt
%license license/lgpl-2.1.txt
%{_bindir}/testpmd
%{_bindir}/dpdk-procinfo
%{_libdir}/*.so.*
%{pmddir}/

%files devel
#BSD
%{incdir}/
%{sdkdir}

%if %{with tools}
%exclude %{sdkdir}/usertools/
%endif

%if %{with examples}
%exclude %{sdkdir}/examples/
%endif

%{_sysconfdir}/profile.d/dpdk-sdk-*.*
%{_libdir}/*.so

%if %{with tools}
%files tools
%{sdkdir}/usertools/
%{_sbindir}/dpdk-devbind
%{_bindir}/dpdk-pdump
%{_bindir}/dpdk-pmdinfo
%{_bindir}/dpdk-test-bbdev
%{_bindir}/dpdk-test-crypto-perf
%endif

%if %{with examples}
%files examples
%doc %{sdkdir}/examples
%{_bindir}/dpdk_example_*
%endif

%changelog
* Wed Oct 27 2021 Muhammad Falak <mwani@microsft.com> - 18.11.2-7
- Remove epoch

* Sat Sep 25 2021 Muhammad Falak <mwani@microsoft.com> - 2:18.11.2-6
- Enable `tools` subpackage by default

* Thu Aug 05 2021 Thomas Crain <thcrain@microsoft.com> - 2:18.11.2-5
- Disable examples subpackage by default

* Thu Nov 05 2020 Joe Schmit <joschmit@microsoft.com> - 2:18.11.2-4
- Build without tools subpackage and dependencies.
- Set _unpackaged_files_terminate_build since tools are not being packaged.

* Wed Oct 28 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2:18.11.2-3
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Added the "Vendor" and "Distribution" tags.
- License verified.
- Added the %%license macro.
- Removed redundant or unused variables.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:18.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Timothy Redaelli <tredaelli@redhat.com> - 2:18.11.2-1
- Update to latest 18.11 LTS (bz1721056)

* Thu Feb 28 2019 Timothy Redaelli <tredaelli@redhat.com> - 2:18.11.0-1
- Update to latest LTS release (bz1684107)

* Wed Feb 13 2019 Neil Horman <nhorman@redhat.com> - 2:17.11.2-6
- Fix some FTBFS errors (1674825)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:17.11.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 27 2018 Neil Horman <nhorman@redhat.com> - 2:17.11.2-4
- Add wdiff to BuildRequires

* Thu Sep 27 2018 Neil Horman <nhorman@tuxdriver.com> - 2:17.11.2-3
- quiet annocheck complaints (bz1548404)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:17.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 24 2018 Neil Horman <nhorman@redhat.com> 2:17.11.2-1
- Update to latest 17.11 LTS (fixes bz 1571361)

* Tue Apr 10 2018 Timothy Redaelli <tredaelli@redhat.com> - 2:17.11.1-3
- Fix Requires dpdk by adding epoch

* Fri Apr 06 2018 Neil Horman <nhorman@redhat.com> 2:17.11.1-2
- Fix aarch64 build issue

* Fri Apr 06 2018 Neil Horman <nhorman@redhat.com> 2:17.11.1-1
- Update to latest LTS release for OVS

* Fri Apr 06 2018 Timothy Redaelli <tredaelli@redhat.com> -  18.02 -6
- Replace "/usr/bin/env python" with "/usr/bin/python3" (bz 1564215)

* Thu Apr 05 2018 Neil Horman <nhorman@redhat.com> - 18.02-5
- Fix compiler flag error (bz 1548404)
- Update spec file to switch to python3

* Wed Mar 14 2018 Neil Horman <nhorman@redhat.com>< -18.02-4
- Fixing date in changelog below

* Thu Mar 08 2018 Neil Horman <nhorman@redhat.com> - 18.02-3
- Fixing missing c/ldflags for pmdinfogen (bz 1548404)

* Tue Feb 27 2018 Neil Horman <nhorman@redhat.com> - 18.02-2
- Fix rpm ldflags usage (bz 1548404)

* Mon Feb 19 2018 Neil Horman <nhorman@redhat.com> - 18.02-1
- update to latest upstream

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 17.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 03 2018 Iryna Shcherbina <ishcherb@redhat.com> - 17.11-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Nov 30 2017 Neil Horman <nhorman@redhat.com> - 17.11-2
- Fix dangling symlinks (bz 1519322)
- Fix devtools->usertools conversion (bz 1519332)
- Fix python-pyelftools requirement (bz 1519336)

* Thu Nov 16 2017 Neil Horman <nhorman@redhat.com> - 17.11-1
- Update to latest upstream

* Wed Aug 09 2017 Neil Horman <nhorman@redhat.com> - 17.08-1
- Update to latest upstream

* Mon Jul 31 2017 Neil Horman <nhorman@redhat.com> - 17.05-2
- backport rte_eth_tx_done_cleanup map fix (#1476341)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 17.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Neil Horman <nhorman@redhat.com> - 17.05-1
- Update to latest upstream

* Fri Feb 24 2017 Neil Horman <nhorman@redhat.com> - 17-02-2
- Add python dependency (#1426561)

* Wed Feb 15 2017 Fedora Release Monitoring  <release-monitoring@fedoraproject.org> - 17.02-1
- Update to 17.02 (#1422285)

* Mon Feb 06 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 16.11-2
- Enable aarch64, ppc64le (#1419731)

* Tue Nov 15 2016 Neil Horman <nhorman@redhat.com> - 16.11-1
- Update to 16.11

* Tue Aug 02 2016 Neil Horman <nhorman@redhat.com> - 16.07-1

* Update to 16.07

* Thu Apr 14 2016 Panu Matilainen <pmatilai@redhat.com> - 16.04-1
- Update to 16.04
- Drop all patches, they're not needed anymore
- Drop linker script generation, its upstream now
- Enable vhost numa support again

* Wed Mar 16 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-7
- vhost numa code causes crashes, disable until upstream fixes
- Generalize target/machine/etc macros to enable i686 builds

* Tue Mar 01 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-6
- Drop no longer needed bnx2x patch, the gcc false positive has been fixed
- Drop no longer needed -Wno-error=array-bounds from CFLAGS
- Eliminate the need for the enic patch by eliminating second -Wall from CFLAGS
- Disable unmaintained librte_power as per upstream recommendation

* Mon Feb 15 2016 Neil Horman <nhorman@redhat.com> 2.2.0-5
- Fix ftbfs isssue (1307431)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-3
- Use a different quoting method to avoid messing up vim syntax highlighting
- A string is expected as CONFIG_RTE_MACHINE value, quote it too

* Mon Jan 25 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-2
- Enable librte_vhost NUMA-awareness

* Wed Jan 20 2016 Panu Matilainen <pmatilai@redhat.com> - 2.2.0-1
- Update to 2.2.0
- Establish a driver directory for automatic driver loading
- Move the unversioned pmd symlinks from libdir -devel
- Make option matching stricter in spec setconf
- Spec cleanups
- Adopt upstream standard installation layout

* Thu Oct 22 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-3
- Include examples binaries
- Enable the Broadcom NetXtreme II 10Gb PMD
- Fix up linkages for the dpdk-devel package

* Wed Sep 30 2015 Aaron Conole <aconole@redhat.com> - 2.1.0-2
- Re-enable the IGB, IXGBE, I40E PMDs
- Bring the Fedora and RHEL packages more in-line.

* Wed Aug 26 2015 Neil Horman <nhorman@redhat.com> - 2.1.0-1
- Update to latest version

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 06 2015 Neil Horman <nhorman@redhat.com> - 2.0.0-1
- Update to dpdk 2.0
- converted --with shared option to --without shared option

* Wed Jan 28 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-8
- Always build with -fPIC

* Wed Jan 28 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-7
- Policy compliance: move static libraries to -devel, provide dpdk-static
- Add a spec option to build as shared libraries

* Wed Jan 28 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-6
- Avoid variable expansion in the spec here-documents during build
- Drop now unnecessary debug flags patch
- Add a spec option to build a combined library

* Tue Jan 27 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-5
- Avoid unnecessary use of %%global, lazy expansion is normally better
- Drop unused destdir macro while at it
- Arrange for RTE_SDK environment + directory layout expected by DPDK apps
- Drop config from main package, it shouldn't be needed at runtime

* Tue Jan 27 2015 Panu Matilainen <pmatilai@redhat.com> - 1.7.0-4
- Copy the headers instead of broken symlinks into -devel package
- Force sane mode on the headers
- Avoid unnecessary %%exclude by not copying unpackaged content to buildroot
- Clean up summaries and descriptions
- Drop unnecessary kernel-devel BR, we are not building kernel modules

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 - John W. Linville <linville@redhat.com> - 1.7.0-2
- Use EXTRA_CFLAGS to include standard Fedora compiler flags in build
- Set CONFIG_RTE_MACHINE=default to build for least-common-denominator machines
- Turn-off build of librte_acl, since it does not build on default machines
- Turn-off build of physical device PMDs that require kernel support
- Clean-up the install rules to match current packaging
- Correct changelog versions 1.0.7 -> 1.7.0
- Remove ix86 from ExclusiveArch -- it does not build with above changes

* Thu Jul 10 2014 - Neil Horman <nhorman@tuxdriver.com> - 1.7.0-1.0
- Update source to official 1.7.0 release 

* Thu Jul 03 2014 - Neil Horman <nhorman@tuxdriver.com>
- Fixing up release numbering

* Tue Jul 01 2014 - Neil Horman <nhorman@tuxdriver.com> - 1.7.0-0.9.1.20140603git5ebbb1728
- Fixed some build errors (empty debuginfo, bad 32 bit build)

* Wed Jun 11 2014 - Neil Horman <nhorman@tuxdriver.com> - 1.7.0-0.9.20140603git5ebbb1728
- Fix another build dependency

* Mon Jun 09 2014 - Neil Horman <nhorman@tuxdriver.com> - 1.7.0-0.8.20140603git5ebbb1728
- Fixed doc arch versioning issue

* Mon Jun 09 2014 - Neil Horman <nhorman@tuxdriver.com> - 1.7.0-0.7.20140603git5ebbb1728
- Added verbose output to build

* Tue May 13 2014 - Neil Horman <nhorman@tuxdriver.com> - 1.7.0-0.6.20140603git5ebbb1728
- Initial Build
