# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# PASST - Plug A Simple Socket Transport
#  for qemu/UNIX domain socket mode
#
# PASTA - Pack A Subtle Tap Abstraction
#  for network namespace/tap device mode
#
# Copyright (c) 2022 Red Hat GmbH
# Author: Stefano Brivio <sbrivio@redhat.com>

%global git_hash 386b5f5472b89769c025f5d5056348532a823b93
%global selinuxtype targeted
%global selinux_policy_version 41.41

Name:		passt
Version:	0^20260120.g386b5f5
Release:	1%{?dist}
Summary:	User-mode networking daemons for virtual machines and namespaces
License:	GPL-2.0-or-later AND BSD-3-Clause
Group:		System Environment/Daemons
URL:		https://passt.top/
Source:		https://passt.top/passt/snapshot/passt-%{git_hash}.tar.xz

BuildRequires:	gcc, make, checkpolicy, selinux-policy-devel
Requires:	(%{name}-selinux = %{version}-%{release} if selinux-policy-%{selinuxtype})

%description
passt implements a translation layer between a Layer-2 network interface and
native Layer-4 sockets (TCP, UDP, ICMP/ICMPv6 echo) on a host. It doesn't
require any capabilities or privileges, and it can be used as a simple
replacement for Slirp.

pasta (same binary as passt, different command) offers equivalent functionality,
for network namespaces: traffic is forwarded using a tap interface inside the
namespace, without the need to create further interfaces on the host, hence not
requiring any capabilities or privileges.

%package		    selinux
BuildArch:		    noarch
Summary:		    SELinux support for passt and pasta
%if 0%{?fedora} > 43
BuildRequires:      selinux-policy-devel
%selinux_requires_min
%else
BuildRequires:      pkgconfig(systemd)
Requires(post):     libselinux-utils
Requires(post):     policycoreutils
%endif
Requires:		    container-selinux
Requires:		    selinux-policy-%{selinuxtype}
Requires(post):		container-selinux
Requires(post):		selinux-policy-%{selinuxtype}

%description selinux
This package adds SELinux enforcement to passt(1), pasta(1), passt-repair(1).

%prep
%setup -q -n passt-%{git_hash}

%build
%set_build_flags
# The Makefile creates symbolic links for pasta, but we need actual copies for
# SELinux file contexts to work as intended. Same with pasta.avx2 if present.
# Build twice, changing the version string, to avoid duplicate Build-IDs.
%make_build VERSION="%{version}-%{release}.%{_arch}-pasta"
mv -f passt pasta
%ifarch x86_64
mv -f passt.avx2 pasta.avx2
%make_build passt passt.avx2 VERSION="%{version}-%{release}.%{_arch}"
%else
%make_build passt VERSION="%{version}-%{release}.%{_arch}"
%endif

%install
# Already built (not as symbolic links), see above
touch pasta
%ifarch x86_64
touch pasta.avx2
%endif

%make_install DESTDIR=%{buildroot} prefix=%{_prefix} bindir=%{_bindir} mandir=%{_mandir} docdir=%{_docdir}/%{name}
%ifarch x86_64
ln -sr %{buildroot}%{_mandir}/man1/passt.1 %{buildroot}%{_mandir}/man1/passt.avx2.1
ln -sr %{buildroot}%{_mandir}/man1/pasta.1 %{buildroot}%{_mandir}/man1/pasta.avx2.1
install -p -m 755 %{buildroot}%{_bindir}/passt.avx2 %{buildroot}%{_bindir}/pasta.avx2
%endif

pushd contrib/selinux
make -f %{_datadir}/selinux/devel/Makefile
install -p -m 644 -D passt.pp %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/passt.pp
install -p -m 644 -D passt.if %{buildroot}%{_datadir}/selinux/devel/include/distributed/passt.if
install -p -m 644 -D pasta.pp %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/pasta.pp
install -p -m 644 -D passt-repair.pp %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/passt-repair.pp
popd

%pre selinux
%selinux_relabel_pre -s %{selinuxtype}

%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/passt.pp %{_datadir}/selinux/packages/%{selinuxtype}/pasta.pp %{_datadir}/selinux/packages/%{selinuxtype}/passt-repair.pp

%postun selinux
if [ $1 -eq 0 ]; then
	%selinux_modules_uninstall -s %{selinuxtype} passt pasta passt-repair
fi

%posttrans selinux
%selinux_relabel_post -s %{selinuxtype}

%files
%license LICENSES/{GPL-2.0-or-later.txt,BSD-3-Clause.txt}
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/demo.sh
%{_bindir}/passt
%{_bindir}/pasta
%{_bindir}/qrap
%{_bindir}/passt-repair
%{_mandir}/man1/passt.1*
%{_mandir}/man1/pasta.1*
%{_mandir}/man1/qrap.1*
%{_mandir}/man1/passt-repair.1*
%ifarch x86_64
%{_bindir}/passt.avx2
%{_mandir}/man1/passt.avx2.1*
%{_bindir}/pasta.avx2
%{_mandir}/man1/pasta.avx2.1*
%endif

%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/passt.pp
%{_datadir}/selinux/devel/include/distributed/passt.if
%{_datadir}/selinux/packages/%{selinuxtype}/pasta.pp
%{_datadir}/selinux/packages/%{selinuxtype}/passt-repair.pp

%changelog
* Tue Jan 20 2026 Stefano Brivio <sbrivio@redhat.com> - 0^20260120.g386b5f5-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2026_01_17.81c97f6..2026_01_20.386b5f5

* Sat Jan 17 2026 Stefano Brivio <sbrivio@redhat.com> - 0^20260117.g81c97f6-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_12_23.2ba9fd5..2026_01_17.81c97f6

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0^20251223.g2ba9fd5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Dec 23 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20251223.g2ba9fd5-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_12_15.b40f5cd..2025_12_23.2ba9fd5

* Mon Dec 15 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20251215.gb40f5cd-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_12_10.d04c480..2025_12_15.b40f5cd

* Wed Dec 10 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20251210.gd04c480-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_12_09.c3f1ba7..2025_12_10.d04c480

* Tue Dec  9 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20251209.gc3f1ba7-1
- Fix build on Fedora 43, selinux_requires_min not available on Copr builders
- use %%selinux_requires_min macro, drop overlapping dependencies
- use regex instead of SELinux template
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_09_19.623dbf6..2025_12_09.c3f1ba7

* Fri Sep 19 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20250919.g623dbf6-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_09_11.6cbcccc..2025_09_19.623dbf6

* Thu Sep 11 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20250911.g6cbcccc-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_08_05.309eefd..2025_09_11.6cbcccc

* Tue Aug  5 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20250805.g309eefd-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_06_11.0293c6f..2025_08_05.309eefd

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0^20250611.g0293c6f-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 11 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20250611.g0293c6f-1
- Hide restorecon(8) errors in post-transaction scriptlet
- Add container-selinux as dependency for passt-selinux
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_06_06.754c6d7..2025_06_11.0293c6f

* Fri Jun  6 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20250606.g754c6d7-1
- Depend on SELinux tools and policy version, drop circular dependency
- Call %%selinux_modules_* macros only once
- Separately restore context for /run/user in %%posttrans selinux
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_05_12.8ec1341..2025_06_06.754c6d7

* Mon May 12 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20250512.g8ec1341-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_05_07.eea8a76..2025_05_12.8ec1341

* Wed May  7 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20250507.geea8a76-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_05_03.587980c..2025_05_07.eea8a76

* Sat May  3 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20250503.g587980c-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_04_15.2340bbf..2025_05_03.587980c

* Tue Apr 15 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20250415.g2340bbf-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_03_20.32f6212..2025_04_15.2340bbf

* Thu Mar 20 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20250320.g32f6212-1
- Actually install passt-repair SELinux policy file
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_02_17.a1e48a0..2025_03_20.32f6212

* Mon Feb 17 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20250217.ga1e48a0-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2025_01_21.4f2c8e7..2025_02_17.a1e48a0

* Tue Jan 21 2025 Stefano Brivio <sbrivio@redhat.com> - 0^20250121.g4f2c8e7-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_12_11.09478d5..2025_01_21.4f2c8e7

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0^20241211.g09478d5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 11 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20241211.g09478d5-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_11_27.c0fbc7e..2024_12_11.09478d5

* Wed Nov 27 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20241127.gc0fbc7e-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_11_21.238c69f..2024_11_27.c0fbc7e

* Thu Nov 21 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20241121.g238c69f-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_10_30.ee7d0b6..2024_11_21.238c69f

* Wed Oct 30 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20241030.gee7d0b6-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_09_06.6b38f07..2024_10_30.ee7d0b6

* Fri Sep  6 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240906.g6b38f07-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_08_21.1d6142f..2024_09_06.6b38f07

* Wed Aug 21 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240821.g1d6142f-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_08_14.61c0b0d..2024_08_21.1d6142f

* Wed Aug 14 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240814.g61c0b0d-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_08_06.ee36266..2024_08_14.61c0b0d

* Tue Aug  6 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240806.gee36266-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_07_26.57a21d2..2024_08_06.ee36266

* Fri Jul 26 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240726.g57a21d2-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_06_24.1ee2eca..2024_07_26.57a21d2

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0^20240624.g1ee2eca-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 24 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240624.g1ee2eca-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_06_07.8a83b53..2024_06_24.1ee2eca

* Fri Jun  7 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240607.g8a83b53-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_05_23.765eb0b..2024_06_07.8a83b53

* Thu May 23 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240523.g765eb0b-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_05_10.7288448..2024_05_23.765eb0b

* Fri May 10 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240510.g7288448-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_04_26.d03c4e2..2024_05_10.7288448

* Fri Apr 26 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240426.gd03c4e2-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_04_05.954589b..2024_04_26.d03c4e2

* Fri Apr  5 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240405.g954589b-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_03_26.4988e2b..2024_04_05.954589b

* Tue Mar 26 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240326.g4988e2b-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_03_20.71dd405..2024_03_26.4988e2b

* Wed Mar 20 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240320.g71dd405-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_03_19.d35bcbe..2024_03_20.71dd405

* Tue Mar 19 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240319.gd35bcbe-1
- Upstream change: https://passt.top/passt/log/?qt=range&q=2024_03_18.615d370..2024_03_19.d35bcbe

* Mon Mar 18 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240318.g615d370-1
- Switch license identifier to SPDX (Dan Čermák)
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_02_20.1e6f92b..2024_03_18.615d370

* Tue Feb 20 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240220.g1e6f92b-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_02_19.ff22a78..2024_02_20.1e6f92b

* Mon Feb 19 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240219.gff22a78-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2024_02_16.08344da..2024_02_19.ff22a78

* Fri Feb 16 2024 Stefano Brivio <sbrivio@redhat.com> - 0^20240216.g08344da-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_12_30.f091893..2024_02_16.08344da

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0^20231230.gf091893-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0^20231230.gf091893-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 30 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20231230.gf091893-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_12_04.b86afe3..2023_12_30.f091893

* Mon Dec  4 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20231204.gb86afe3-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_11_19.4f1709d..2023_12_04.b86afe3

* Sun Nov 19 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20231119.g4f1709d-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_11_10.5ec3634..2023_11_19.4f1709d

* Fri Nov 10 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20231110.g5ec3634-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_11_07.74e6f48..2023_11_10.5ec3634

* Tue Nov  7 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20231107.g56d9f6d-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_10_04.f851084..2023_11_07.56d9f6d
- SELinux: allow passt_t to use unconfined_t UNIX domain sockets for
  --fd option (https://bugzilla.redhat.com/show_bug.cgi?id=2247221)

* Wed Oct  4 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20231004.gf851084-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_09_08.05627dc..2023_10_04.f851084

* Fri Sep  8 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230908.g05627dc-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_09_07.ee58f37..2023_09_08.05627dc

* Thu Sep  7 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230907.gee58f37-1
- Replace pasta hard links by separate builds
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_08_23.a7e4bfb..2023_09_07.ee58f37

* Wed Aug 23 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230823.ga7e4bfb-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_08_18.0af928e..2023_08_23.a7e4bfb

* Fri Aug 18 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230818.g0af928e-1
- Install pasta as hard link to ensure SELinux file context match
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_06_27.289301b..2023_08_18.0af928e

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0^20230627.g289301b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230627.g289301b-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_06_25.32660ce..2023_06_27.289301b

* Sun Jun 25 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230625.g32660ce-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_06_03.429e1a7..2023_06_25.32660ce

* Sat Jun  3 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230603.g429e1a7-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_05_09.96f8d55..2023_06_03.429e1a7

* Tue May  9 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230509.g96f8d55-1
- Relicense to GPL 2.0, or any later version
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_03_29.b10b983..2023_05_09.96f8d55

* Wed Mar 29 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230329.gb10b983-1
- Adjust path for SELinux policy and interface file to latest guidelines
- Don't install useless SELinux interface file for pasta
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_03_21.1ee2f7c..2023_03_29.b10b983

* Tue Mar 21 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230321.g1ee2f7c-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_03_17.dd23496..2023_03_21.1ee2f7c

* Fri Mar 17 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230317.gdd23496-1
- Refresh SELinux labels in scriptlets, require -selinux package
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_03_10.70c0765..2023_03_17.dd23496

* Fri Mar 10 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230310.g70c0765-1
- Install SELinux interface files to shared include directory
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_03_09.7c7625d..2023_03_10.70c0765

* Thu Mar  9 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230309.g7c7625d-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_02_27.c538ee8..2023_03_09.7c7625d

* Mon Feb 27 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230227.gc538ee8-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_02_22.4ddbcb9..2023_02_27.c538ee8

* Wed Feb 22 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230222.g4ddbcb9-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2023_02_16.4663ccc..2023_02_22.4ddbcb9

* Thu Feb 16 2023 Stefano Brivio <sbrivio@redhat.com> - 0^20230216.g4663ccc-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_11_16.ace074c..2023_02_16.4663ccc

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0^20221116.gace074c-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 16 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20221116.gace074c-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_11_10.4129764..2022_11_16.ace074c

* Thu Nov 10 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20221110.g4129764-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_11_04.e308018..2022_11_10.4129764

* Fri Nov  4 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20221104.ge308018-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_10_26.f212044..2022_11_04.e308018

* Wed Oct 26 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20221026.gf212044-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_10_26.e4df8b0..2022_10_26.f212044

* Wed Oct 26 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20221026.ge4df8b0-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_10_24.c11277b..2022_10_26.e4df8b0

* Mon Oct 24 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20221024.gc11277b-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_10_22.b68da10..2022_10_24.c11277b

* Sat Oct 22 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20221022.gb68da10-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_10_15.b3f3591..2022_10_22.b68da10

* Sat Oct 15 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20221015.gb3f3591-1
- Add versioning information
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_09_29.06aa26f..2022_10_15.b3f3591

* Thu Sep 29 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20220929.g06aa26f-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_09_24.8978f65..2022_09_29.06aa26f

* Sat Sep 24 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20220924.g8978f65-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_09_23.d6f865a..2022_09_24.8978f65

* Fri Sep 23 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20220923.gd6f865a-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_09_06.e2cae8f..2022_09_23.d6f865a

* Wed Sep  7 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20220907.ge2cae8f-1
- Escape %% characters in spec file's changelog
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_09_01.7ce9fd1..2022_09_06.e2cae8f

* Fri Sep  2 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20220902.g7ce9fd1-1
- Add selinux-policy Requires: tag
- Add %%dir entries for own SELinux policy directory and documentation
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_08_29.0cb795e..2022_09_01.7ce9fd1

* Tue Aug 30 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20220830.g0cb795e-1
- Pass explicit bindir, mandir, docdir, and drop OpenSUSE override
- Use full versioning for SELinux subpackage Requires: tag
- Define git_hash in spec file and reuse it
- Drop comment stating the spec file is an example file
- Drop SPDX identifier from spec file
- Adopt versioning guideline for snapshots
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_08_24.60ffc5b..2022_08_29.0cb795e

* Wed Aug 24 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20220824.g60ffc5b-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_08_21.7b71094..2022_08_24.60ffc5b

* Sun Aug 21 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20220821.g7b71094-1
- Use more GNU-style directory variables, explicit docdir for OpenSUSE
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_08_20.f233d6c..2022_08_21.7b71094

* Sat Aug 20 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20220820.gf233d6c-1
- Fix man pages wildcards in spec file
- Don't hardcode CFLAGS setting, use %%set_build_flags macro instead
- Build SELinux subpackage as noarch
- Change source URL to HEAD link with explicit commit SHA
- Drop VCS tag from spec file
- Start Release tag from 1, not 0
- Introduce own rpkg macro for changelog
- Install "plain" README, instead of web version, and demo script
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_08_04.b516d15..2022_08_20.f233d6c

* Mon Aug  1 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20220801.gb516d15-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_07_20.9af2e5d..2022_08_04.b516d15

* Wed Jul 20 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20220720.g9af2e5d-1
- Upstream changes: https://passt.top/passt/log/?qt=range&q=2022_07_14.b86cd00..2022_07_20.9af2e5d

* Thu Jul 14 2022 Stefano Brivio <sbrivio@redhat.com> - 0^20220714.gb86cd00-1
- Use pre-processing macros in spec file
- Drop dashes from version
- Add example spec file for Fedora
- Upstream changes: https://passt.top/passt/log/?qt=range&q=e653f9b3ed1b60037e3bc661d53b3f9407243fc2..2022_07_14.b86cd00
