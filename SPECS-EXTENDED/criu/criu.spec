%global py_prefix python3
%global py_binary %{py_prefix}

# With annobin enabled, CRIU does not work anymore. It seems CRIU's
# parasite code breaks if annobin is enabled.
%undefine _annotated_build

# Disable automatic call to the set_build_flags macro
# at the beginning of the build, check, and install.
# This change was introduced in Fedora 36.
%undefine _auto_set_build_flags

Name: criu
Version: 4.0
Release: 2%{?dist}
Summary: Tool for Checkpoint/Restore in User-space
License: GPL-2.0-only AND LGPL-2.1-only AND MIT
URL: http://criu.org/
Source0: https://github.com/checkpoint-restore/criu/archive/v%{version}/criu-%{version}.tar.gz

# Add protobuf-c as a dependency.
# We use this patch because the protobuf-c package name
# in RPM and DEB is different.
Patch99: criu.pc.patch

Patch100: Makefile.config-set-CR_PLUGIN_DEFAULT-variable.patch

Source5: criu-tmpfiles.conf

BuildRequires: gcc
BuildRequires: systemd
BuildRequires: libnet-devel
BuildRequires: protobuf-devel protobuf-c-devel %{py_prefix}-devel libnl3-devel libcap-devel
BuildRequires: %{py_prefix}-pip
BuildRequires: %{py_prefix}-setuptools
BuildRequires: %{py_prefix}-wheel
BuildRequires: %{py_prefix}-protobuf
BuildRequires: asciidoctor
BuildRequires: perl-interpreter
BuildRequires: libselinux-devel
BuildRequires: gnutls-devel
BuildRequires: libdrm-devel
# Checkpointing containers with a tmpfs requires tar
Recommends: tar
# CRIU requires some version of iptables-restore for network locking
Recommends: iptables
%if 0%{?fedora}
BuildRequires: libbsd-devel
BuildRequires: nftables-devel
%endif
BuildRequires: make

# user-space and kernel changes are only available for x86_64, arm,
# ppc64le, aarch64 and s390x
# https://bugzilla.redhat.com/show_bug.cgi?id=902875
ExclusiveArch: x86_64 %{arm} ppc64le aarch64 s390x

%description
criu is the user-space part of Checkpoint/Restore in User-space
(CRIU), a project to implement checkpoint/restore functionality for
Linux in user-space.

%package devel
Summary: Header files and libraries for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description devel
This package contains header files and libraries for %{name}.

%package libs
Summary: Libraries for %{name}
Requires: %{name} = %{version}-%{release}

%description libs
This package contains the libraries for %{name}

%package amdgpu-plugin
Summary: AMD GPU plugin for %{name}
Requires: %{name} = %{version}-%{release}

%description amdgpu-plugin
This package contains the AMD GPU plugin for %{name}

%package cuda-plugin
Summary: CUDA plugin for %{name}
Requires: %{name} = %{version}-%{release}

%description cuda-plugin
This package contains the CUDA plugin for %{name}

%package -n %{py_prefix}-%{name}
%{?python_provide:%python_provide %{py_prefix}-%{name}}
Summary: Python bindings for %{name}
Requires: %{py_prefix}-protobuf

%description -n %{py_prefix}-%{name}
%{py_prefix}-%{name} contains Python bindings for %{name}.

%package -n crit
Summary: CRIU image tool
Requires: %{py_prefix}-%{name} = %{version}-%{release}

%description -n crit
crit is a tool designed to decode CRIU binary dump files and show
their content in human-readable form.

%package -n criu-ns
Summary: Tool to run CRIU in different namespaces
Requires: %{name} = %{version}-%{release}

%description -n criu-ns
The purpose of the criu-ns wrapper script is to enable restoring a process
tree that might require a specific PID that is already used on the system.
This script can help to workaround the so called "PID mismatch" problem.

%prep
%setup -q
%patch -P 99 -p1

%patch -P 100 -p1

%build
# This package calls LD directly without specifying the LTO plugins.  Until
# that is fixed, disable LTO.
%define _lto_cflags %{nil}

# %{?_smp_mflags} does not work
# -fstack-protector breaks build
CFLAGS+=`echo %{optflags} | sed -e 's,-fstack-protector\S*,,g'` make V=1 WERROR=0 PREFIX=%{_prefix} RUNDIR=/run/criu PYTHON=%{py_binary} PLUGINDIR=%{_libdir}/criu
make V=1 WERROR=0 PREFIX=%{_prefix} PLUGINDIR=%{_libdir}/criu amdgpu_plugin
make docs V=1


%install
sed -e "s,--upgrade --ignore-installed,--no-index --no-deps -v --no-build-isolation,g" -i lib/Makefile -i crit/Makefile
make install-criu DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} LIBDIR=%{_libdir}
make install-lib DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} LIBDIR=%{_libdir} PYTHON=%{py_binary} PIPFLAGS="--no-build-isolation --no-index --no-deps --progress-bar off --upgrade --ignore-installed"
make install-amdgpu_plugin DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} LIBDIR=%{_libdir} PLUGINDIR=%{_libdir}/criu
make install-cuda_plugin DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} LIBDIR=%{_libdir} PLUGINDIR=%{_libdir}/criu
make install-crit DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} LIBDIR=%{_libdir} PYTHON=%{py_binary} PIPFLAGS="--no-build-isolation --no-index --no-deps --progress-bar off --upgrade --ignore-installed"
make install-man DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} LIBDIR=%{_libdir}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/compel.1

mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -d -m 0755 %{buildroot}/run/%{name}/

# remove static lib
rm -f $RPM_BUILD_ROOT%{_libdir}/libcriu.a

%files
%{_sbindir}/%{name}
%doc %{_mandir}/man8/criu.8*
%{_libexecdir}/%{name}
%dir /run/%{name}
%{_tmpfilesdir}/%{name}.conf
%doc README.md COPYING

%files devel
%{_includedir}/criu
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files libs
%{_libdir}/*.so.*

%files amdgpu-plugin
%{_libdir}/%{name}/amdgpu_plugin.so
%doc %{_mandir}/man1/criu-amdgpu-plugin.1*

%files cuda-plugin
%{_libdir}/%{name}/cuda_plugin.so
%doc plugins/cuda/README.md

%files -n %{py_prefix}-%{name}
%{python3_sitelib}/pycriu*

%files -n crit
%{_bindir}/crit
%{python3_sitelib}/crit-%{version}.dist-info/
%{python3_sitelib}/crit
%doc %{_mandir}/man1/crit.1*

%files -n criu-ns
%{_sbindir}/criu-ns
%doc %{_mandir}/man1/criu-ns.1*

%post
%tmpfiles_create %{name}.conf

%changelog
* Thu Oct 17 2024 Adrian Reber <adrian@lisas.de> - 4.0-2
- Recommends: iptables

* Thu Sep 26 2024 Radostin Stoyanov <rstoyanov@fedoraproject.org> - 4.0-1
- Update to 4.0
- Add package for cuda-plugin
- Run pip install without internet access

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Radostin Stoyanov <rstoyanov@fedoraproject.org> - 3.19-6
- Add package for amdgpu-plugin

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 3.19-5
- Rebuilt for Python 3.13

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 28 2023 Adrian Reber <adrian@lisas.de> - 3.19-2
- Fix test setup

* Tue Nov 28 2023 Adrian Reber <adrian@lisas.de> - 3.19-1
- Update to 3.19

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Adrian Reber <adrian@lisas.de> - 3.18-3
- migrated to SPDX license
- remove RHEL 7 conditionals

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.18-2
- Rebuilt for Python 3.12

* Tue Apr 25 2023 Adrian Reber <adrian@lisas.de> - 3.18-1
- Update to 3.18
- Apply patch from upstream to support newer CPUs

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.17.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec  2 2022 Florian Weimer <fweimer@redhat.com> - 3.17.1-4
- Fix FTBFS with glibc 2.36

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Adrian Reber <adrian@lisas.de> - 3.17.1-2
- Rebuilt to pick up glibc rseq() changes

* Mon Jun 27 2022 Radostin Stoyanov <rstoyanov@fedoraproject.org> - 3.17.1-1
- Update to release version 3.17.1

* Mon Jun 20 2022 Adrian Reber <adrian@lisas.de> - 3.17-4
- Apply upstream patch to fix mount v2 errors

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.17-3
- Rebuilt for Python 3.11

* Thu May 19 2022 Radostin Stoyanov <rstoyanov@fedoraproject.org> - 3.17-2
- Use mntns-compat-mode as a temporary fix for runc

* Fri May 6 2022 Radostin Stoyanov <rstoyanov@fedoraproject.org> - 3.17-1
- Update to release version 3.17
- Do not install compel and amdgpu_plugin man pages

* Tue Apr 5 2022 Radostin Stoyanov <rstoyanov@fedoraproject.org> - 3.16.1-12
- Update rseq patches

* Tue Apr 5 2022 Radostin Stoyanov <rstoyanov@fedoraproject.org> - 3.16.1-11
- Update rseq patches

* Tue Apr 5 2022 Radostin Stoyanov <rstoyanov@fedoraproject.org> - 3.16.1-10
- Update fixup patch

* Tue Apr 5 2022 Radostin Stoyanov <rstoyanov@fedoraproject.org> - 3.16.1-9
- Update rseq support patches

* Fri Feb 18 2022 Radostin Stoyanov <rstoyanov@fedoraproject.org> - 3.16.1-8
- rebuilt

* Tue Feb 8 2022 Radostin Stoyanov <radostin@redhat.com> - 3.16.1-7
- Drop global -ffreestanding

* Mon Jan 31 2022 Radostin Stoyanov <radostin@redhat.com> - 3.16.1-6
- Fix typo in changelog
- Replace `asciidoc` and `xmlto` with `asciidoctor`
- Enable initial rseq support

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 06 2021 Adrian Reber <adrian@lisas.de> - 3.16.1-4
- Rebuilt for protobuf 3.19.0

* Mon Oct 25 2021 Adrian Reber <adrian@lisas.de> - 3.16.1-3
- Rebuilt for protobuf 3.18.1

* Tue Oct 19 2021 Radostin Stoyanov <radostin@redhat.com> - 3.16.1-2
- Update protobuf-c to libprotobuf-c requirement

* Thu Oct 14 2021 Radostin Stoyanov <radostin@redhat.com> - 3.16.1-1
- Update to 3.16.1
- Add protobuf-c as required dependency (#2013775)

* Tue Oct 05 2021 Adrian Reber <adrian@lisas.de> - 3.16-3
- Fix build on RHEL 8

* Thu Sep 23 2021 Adrian Reber <adrian@lisas.de> - 3.16-2
- Include criu-ns sub package
- Use new github Source0 location

* Wed Sep 22 2021 Adrian Reber <adrian@lisas.de> - 3.16-1
- Update to 3.16

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.15-5
- Rebuilt for Python 3.10

* Fri Apr 09 2021 Adrian Reber <adrian@lisas.de> - 3.15-4
- Test for testing

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Adrian Reber <adrian@lisas.de> - 3.15-2
- Rebuilt for protobuf 3.14

* Wed Nov 04 2020 Adrian Reber <adrian@lisas.de> - 3.15-1
- Update to 3.15

* Wed Sep 23 2020 Adrian Reber <adrian@lisas.de> - 3.14-8
- Rebuilt for protobuf 3.13

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Jeff Law <law@redhat.com> - 3.14-6
- Disable LTO

* Sun Jun 14 2020 Adrian Reber <adrian@lisas.de> - 3.14-5
- Rebuilt for protobuf 3.12

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.14-4
- Rebuilt for Python 3.9

* Thu Apr 30 2020 Adrian Reber <adrian@lisas.de> - 3.14-3
- BuildRequire nftables-devel for working CI

* Thu Apr 30 2020 Adrian Reber <adrian@lisas.de> - 3.14-2
- Rebuild for CI fixes

* Wed Apr 29 2020 Adrian Reber <adrian@lisas.de> - 3.14-1
- Update to 3.14 (#1829399)

* Sun Mar 29 2020 Andrei Vagin <avagin@gmail.com> - 3.13-7
- Added patch for gcc-10

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 16 2019 Adrian Reber <adrian@lisas.de> - 3.13-5
- Update to 3.13 (#1751146)
- Drop upstreamed patches
- Drop static library
- Add compel man-page

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.12-14
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 14 2019 Adrian Reber <adrian@lisas.de> - 3.12-11
- Test different decision_context in gating.yaml

* Mon May 13 2019 Adrian Reber <adrian@lisas.de> - 3.12-10
- Added additional fixup patches for the socket labelling

* Sat May 04 2019 Adrian Reber <adrian@lisas.de> - 3.12-8
- Patch for socket labelling has changed upstream

* Mon Apr 29 2019 Adrian Reber <adrian@lisas.de> - 3.12-4
- Applied patch to correctly restore socket()s

* Sat Apr 27 2019 Adrian Reber <adrian@lisas.de> - 3.12-3
- Correctly exclude libs and devel for RHEL

* Thu Apr 25 2019 Adrian Reber <adrian@lisas.de> - 3.12-2
- Updated to official 3.12

* Tue Apr 23 2019 Adrian Reber <adrian@lisas.de> - 3.12-0.1
- Updated to 3.12 (pre-release)
- Create libs subpackage
- Build against SELinux (Fedora and RHEL8)
- Build against libbsd (Fedora)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 19 2019 Adrian Reber <adrian@lisas.de> - 3.11-2
- Added patch for gcc-9

* Tue Nov 06 2018 Adrian Reber <adrian@lisas.de> - 3.11-1
- Updated to 3.11
- Removed upstreamed patches

* Tue Oct 30 2018 Adrian Reber <adrian@lisas.de> - 3.10-5
- Added Recommends: tar
  It is necessary when checkpointing containers with a tmpfs

* Mon Jul 16 2018 Adrian Reber <adrian@lisas.de> - 3.10-4
- Add patch to fix errors with read-only runc

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Adrian Reber <adrian@lisas.de> - 3.10-2
- Disable annobin as it seems to break CRIU

* Tue Jul 10 2018 Adrian Reber <adrian@lisas.de> - 3.10-1
- Update to 3.10 (#1599710)
- Switch to python3

* Wed Jun 06 2018 Adrian Reber <adrian@lisas.de> - 3.9-2
- Simplify ExclusiveArch now that there is no more F26

* Fri Jun 01 2018 Adrian Reber <adrian@lisas.de> - 3.9-1
- Update to 3.9

* Tue Apr 03 2018 Adrian Reber <adrian@lisas.de> - 3.8.1-1
- Update to 3.8.1

* Thu Mar 22 2018 Adrian Reber <adrian@lisas.de> - 3.8-2
- Bump release for COPR

* Wed Mar 14 2018 Adrian Reber <adrian@lisas.de> - 3.8-1
- Update to 3.8

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.7-4
- Switch to %%ldconfig_scriptlets

* Fri Jan 12 2018 Adrian Reber <adrian@lisas.de> - 3.7-3
- Fix python/python2 dependencies accross all branches

* Wed Jan 03 2018 Merlin Mathesius <mmathesi@redhat.com> - 3.7-2
- Cleanup spec file conditionals

* Sat Dec 30 2017 Adrian Reber <adrian@lisas.de> - 3.7-1
- Update to 3.7

* Fri Dec 15 2017 Iryna Shcherbina <ishcherb@redhat.com> - 3.6-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Oct 26 2017 Adrian Reber <adrian@lisas.de> - 3.6-1
- Update to 3.6

* Wed Oct 18 2017 Adrian Reber <adrian@lisas.de> - 3.5-5
- Added patch to fix build on Fedora rawhide aarch64

* Tue Oct 10 2017 Adrian Reber <areber@redhat.com> - 3.5-4
- Upgrade imported manpages to 3.5

* Mon Oct 09 2017 Adrian Reber <areber@redhat.com> - 3.5-3
- Fix ExclusiveArch on RHEL

* Mon Oct 02 2017 Adrian Reber <adrian@lisas.de> - 3.5-2
- Merge RHEL and Fedora spec file

* Thu Sep 28 2017 Adrian Reber <adrian@lisas.de> - 3.5-1
- Update to 3.5 (#1496614)

* Sun Aug 27 2017 Adrian Reber <adrian@lisas.de> - 3.4-1
- Update to 3.4 (#1483774)
- Removed upstreamed patches
- Added s390x (#1475719)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.3-5
- Python 2 binary package renamed to python2-criu
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Adrian Reber <adrian@lisas.de> - 3.3-2
- Added patches to handle changes in glibc

* Wed Jul 19 2017 Adrian Reber <adrian@lisas.de> - 3.3-1
- Update to 3.3

* Fri Jun 30 2017 Adrian Reber <adrian@lisas.de> - 3.2.1-2
- Added patches to handle unified hierarchy and new glibc

* Wed Jun 28 2017 Adrian Reber <adrian@lisas.de> - 3.2.1-1
- Update to 3.2.1-1

* Tue Jun 13 2017 Orion Poplawski <orion@cora.nwra.com> - 3.1-2
- Rebuild for protobuf 3.3.1

* Mon May 22 2017 Adrian Reber <adrian@lisas.de> - 3.1-1
- Update to 3.1

* Tue Apr 25 2017 Adrian Reber <adrian@lisas.de> - 3.0-1
- Update to 3.0

* Thu Mar 09 2017 Adrian Reber <adrian@lisas.de> - 2.12-1
- Update to 2.12

* Fri Feb 17 2017 Adrian Reber <adrian@lisas.de> - 2.11.1-1
- Update to 2.11.1

* Thu Feb 16 2017 Adrian Reber <adrian@lisas.de> - 2.11-1
- Update to 2.11

* Mon Feb 13 2017 Adrian Reber <adrian@lisas.de> - 2.10-4
- Added patch to fix build on ppc64le

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Orion Poplawski <orion@cora.nwra.com> - 2.10-2
- Rebuild for protobuf 3.2.0

* Mon Jan 16 2017 Adrian Reber <adrian@lisas.de> - 2.10-1
- Update to 2.10

* Mon Dec 12 2016 Adrian Reber <adrian@lisas.de> - 2.9-1
- Update to 2.9
- Added crit manpage to crit subpackage

* Sat Nov 19 2016 Orion Poplawski <orion@cora.nwra.com> - 2.8-2
- Rebuild for protobuf 3.1.0

* Tue Nov 15 2016 Adrian Reber <adrian@lisas.de> - 2.8-1
- Update to 2.8
- Dropped 'mount_resolve_path()' patch

* Wed Oct 19 2016 Adrian Reber <adrian@lisas.de> - 2.7-2
- Added upstream patch to fix #1381351
  ("criu: mount_resolve_path(): criu killed by SIGSEGV")

* Wed Oct 19 2016 Adrian Reber <adrian@lisas.de> - 2.7-1
- Update to 2.7

* Tue Sep 13 2016 Adrian Reber <adrian@lisas.de> - 2.6-1
- Update to 2.6

* Tue Aug 30 2016 Adrian Reber <adrian@lisas.de> - 2.5-1
- Update to 2.5

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jul 12 2016 Adrian Reber <adrian@lisas.de> - 2.4-1
- Update to 2.4

* Tue Jun 14 2016 Adrian Reber <areber@redhat.com> - 2.3-1
- Update to 2.3
- Copy man-page from Fedora 24 for RHEL

* Mon May 23 2016 Adrian Reber <adrian@lisas.de> - 2.2-1
- Update to 2.2

* Tue Apr 12 2016 Adrian Reber <adrian@lisas.de> - 2.1-2
- Remove crtools symbolic link

* Mon Apr 11 2016 Adrian Reber <adrian@lisas.de> - 2.1-1
- Update to 2.1

* Wed Apr 06 2016 Adrian Reber <areber@redhat.com> - 2.0-2
- Merge changes from Fedora

* Thu Mar 10 2016 Andrey Vagin <avagin@openvz.org> - 2.0-1
- Update to 2.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 07 2015 Adrian Reber <adrian@lisas.de> - 1.8-1
- Update to 1.8

* Mon Nov 02 2015 Adrian Reber <adrian@lisas.de> - 1.7.2-1
- Update to 1.7.2

* Mon Sep 7 2015 Andrey Vagin <avagin@openvz.org> - 1.7-1
- Update to 1.7

* Thu Sep 3 2015 Andrey Vagin <avagin@openvz.org> - 1.6.1-3
- Build only for power64le

* Thu Sep 3 2015 Andrey Vagin <avagin@openvz.org> - 1.6.1-2
- Build for aarch64 and power64

* Thu Aug 13 2015 Adrian Reber <adrian@lisas.de> - 1.6.1-1
- Update to 1.6.1
- Merge changes for RHEL packaging

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Adrian Reber <areber@redhat.com> - 1.6-1.1
- adapt to RHEL7

* Mon Jun 01 2015 Andrew Vagin <avagin@openvz.org> - 1.6-1
- Update to 1.6

* Thu Apr 30 2015 Andrew Vagin <avagin@openvz.org> - 1.5.2-2
- Require protobuf-python and python-ipaddr for python-criu

* Tue Apr 28 2015 Andrew Vagin <avagin@openvz.org> - 1.5.2
- Update to 1.5.2

* Sun Apr 19 2015 Nikita Spiridonov <nspiridonov@odin.com> - 1.5.1-2
- Create python-criu and crit subpackages

* Tue Mar 31 2015 Andrew Vagin <avagin@openvz.org> - 1.5.1
- Update to 1.5.1

* Sat Dec 06 2014 Adrian Reber <adrian@lisas.de> - 1.4-1
- Update to 1.4

* Tue Sep 23 2014 Adrian Reber <adrian@lisas.de> - 1.3.1-1
- Update to 1.3.1 (#1142896)

* Tue Sep 02 2014 Adrian Reber <adrian@lisas.de> - 1.3-1
- Update to 1.3
- Dropped all upstreamed patches
- included pkgconfig file in -devel

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 07 2014 Andrew Vagin <avagin@openvz.org> - 1.2-4
- Include inttypes.h for PRI helpers

* Thu Aug 07 2014 Andrew Vagin <avagin@openvz.org> - 1.2-3
- Rebuilt for https://bugzilla.redhat.com/show_bug.cgi?id=1126751

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 28 2014 Adrian Reber <adrian@lisas.de> - 1.2-1
- Update to 1.2
- Dropped all upstreamed patches

* Tue Feb 04 2014 Adrian Reber <adrian@lisas.de> - 1.1-4
- Create -devel subpackage

* Wed Dec 11 2013 Andrew Vagin <avagin@openvz.org> - 1.0-3
- Fix the epoch of crtools

* Tue Dec 10 2013 Andrew Vagin <avagin@openvz.org> - 1.0-2
- Rename crtools to criu #1034677

* Wed Nov 27 2013 Andrew Vagin <avagin@openvz.org> - 1.0-1
- Update to 1.0

* Thu Oct 24 2013 Andrew Vagin <avagin@openvz.org> - 0.8-1
- Update to 0.8

* Tue Sep 10 2013 Andrew Vagin <avagin@openvz.org> - 0.7-1
- Update to 0.7

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Andrew Vagin <avagin@openvz.org> - 0.6-3
- Delete all kind of -fstack-protector gcc options

* Wed Jul 24 2013 Andrew Vagin <avagin@openvz.org> - 0.6-3
- Added arm macro to ExclusiveArch

* Wed Jul 03 2013 Andrew Vagin <avagin@openvz.org> - 0.6-2
- fix building on ARM
- fix null pointer dereference

* Tue Jul 02 2013 Adrian Reber <adrian@lisas.de> - 0.6-1
- updated to 0.6
- upstream moved binaries to sbin
- using upstream's make install

* Tue May 14 2013 Adrian Reber <adrian@lisas.de> - 0.5-1
- updated to 0.5

* Fri Feb 22 2013 Adrian Reber <adrian@lisas.de> - 0.4-1
- updated to 0.4

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Adrian Reber <adrian@lisas.de> - 0.3-3
- added ExclusiveArch blocker bug

* Fri Jan 18 2013 Adrian Reber <adrian@lisas.de> - 0.3-2
- improved Summary and Description

* Mon Jan 14 2013 Adrian Reber <adrian@lisas.de> - 0.3-1
- updated to 0.3
- fix building Documentation/

* Tue Aug 21 2012 Adrian Reber <adrian@lisas.de> - 0.2-2
- remove macros like %%{__mkdir_p} and %%{__install}
- add comment why it is only x86_64

* Tue Aug 21 2012 Adrian Reber <adrian@lisas.de> - 0.2-1
- initial release
