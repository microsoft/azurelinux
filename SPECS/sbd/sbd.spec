# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# spec file for package sbd
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2013 Lars Marowsky-Bree
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
%global longcommit cf5c2208bad2db2dff9b09624b89b05415c3bc11
%global shortcommit %(echo %{longcommit}|cut -c1-8)
%global modified %(echo %{longcommit}-|cut -f2 -d-)
%global github_owner Clusterlabs
%global baserelease 2

%ifarch s390x s390
# minimum timeout on LPAR diag288 watchdog is 15s
%global watchdog_timeout_default 15
%else
%global watchdog_timeout_default 5
%endif

# Be careful with sync_resource_startup_default
# being enabled. This configuration has
# to be in sync with configuration in pacemaker
# where it is called sbd_sync - assure by e.g.
# mutual rpm dependencies.
%bcond_without sync_resource_startup_default
# Syncing enabled per default will lead to
# syncing enabled on upgrade without adaption
# of the config.
# Setting can still be overruled via sysconfig.
# The setting in the config-template packaged
# will follow the default if below is is left
# empty. But it is possible to have the setting
# in the config-template deviate from the default
# by setting below to an explicit 'yes' or 'no'.
%global sync_resource_startup_sysconfig ""

Name:           sbd
Summary:        Storage-based death
License:        GPL-2.0-or-later
Version:        1.5.2
Release:        %{baserelease}%{?dist}
Url:            https://github.com/%{github_owner}/%{name}
Source0:        https://github.com/%{github_owner}/%{name}/archive/%{longcommit}/%{name}-%{longcommit}.tar.gz
Patch0:         0001-Fix-query-watchdog-avoid-issues-on-heap-allocation-f.patch
Patch1:         0002-Refactor-sbd-md-alloc-de-alloc-reverse-order.patch
Patch2:         0003-spec-convert-license-naming-to-SPDX.patch
Patch3:         0004-Fix-sbd-cluster-cleanly-include-crm-crm.h-for-crm_sy.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libuuid-devel
BuildRequires:  glib2-devel
BuildRequires:  libaio-devel
BuildRequires:  corosync-devel
BuildRequires:  pacemaker-libs-devel
BuildRequires:  libtool
BuildRequires:  libuuid-devel
BuildRequires:  libxml2-devel
BuildRequires:  pkgconfig
BuildRequires:  make
BuildRequires:  systemd
Conflicts:      fence-agents-sbd < 4.5.0
Conflicts:      pacemaker-libs < 2.1.0-6

%if %{defined systemd_requires}
%systemd_requires
%endif

%description

This package contains the storage-based death functionality.

Available rpmbuild rebuild options:
  --with(out) : sync_resource_startup_default

%package tests
Summary:        Storage-based death environment for regression tests
License:        GPL-2.0-or-later

%description tests
This package provides an environment + testscripts for
regression-testing sbd.

###########################################################

%prep
%autosetup -n %{name}-%{longcommit} -p1

###########################################################

%build
./autogen.sh
export CFLAGS="$RPM_OPT_FLAGS -Wall -Werror"
%configure --with-watchdog-timeout-default=%{watchdog_timeout_default} \
           --with-sync-resource-startup-default=%{?with_sync_resource_startup_default:yes}%{!?with_sync_resource_startup_default:no} \
           --with-sync-resource-startup-sysconfig=%{sync_resource_startup_sysconfig} \
           --with-runstatedir=%{_rundir}
make %{?_smp_mflags}

###########################################################

%install

make DESTDIR=$RPM_BUILD_ROOT LIBDIR=%{_libdir} install
rm -rf ${RPM_BUILD_ROOT}%{_libdir}/stonith

install -D -m 0755 tests/regressions.sh $RPM_BUILD_ROOT/usr/share/sbd/regressions.sh
%if %{defined _unitdir}
install -D -m 0644 src/sbd.service $RPM_BUILD_ROOT/%{_unitdir}/sbd.service
install -D -m 0644 src/sbd_remote.service $RPM_BUILD_ROOT/%{_unitdir}/sbd_remote.service
%endif

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
install -m 644 src/sbd.sysconfig ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/sbd

# Don't package static libs
find %{buildroot} -name '*.a' -type f -print0 | xargs -0 rm -f
find %{buildroot} -name '*.la' -type f -print0 | xargs -0 rm -f

###########################################################

%if %{defined _unitdir}
%post
%systemd_post sbd.service
%systemd_post sbd_remote.service
if [ $1 -ne 1 ] ; then
	if systemctl --quiet is-enabled sbd.service 2>/dev/null
	then
		systemctl --quiet reenable sbd.service 2>/dev/null || :
	fi
	if systemctl --quiet is-enabled sbd_remote.service 2>/dev/null
	then
		systemctl --quiet reenable sbd_remote.service 2>/dev/null || :
	fi
fi

%preun
%systemd_preun sbd.service
%systemd_preun sbd_remote.service

%postun
%systemd_postun sbd.service
%systemd_postun sbd_remote.service
%endif

%files
###########################################################
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/sysconfig/sbd
%{_sbindir}/sbd
%{_datadir}/sbd
%{_datadir}/pkgconfig/sbd.pc
%exclude %{_datadir}/sbd/regressions.sh
%doc %{_mandir}/man8/sbd*
%if %{defined _unitdir}
%{_unitdir}/sbd.service
%{_unitdir}/sbd_remote.service
%endif
%doc COPYING

%files tests
###########################################################
%defattr(-,root,root)
%dir %{_datadir}/sbd
%{_datadir}/sbd/regressions.sh
%{_libdir}/libsbdtestbed*

%changelog
* Thu Sep 18 2025 Klaus Wenninger <kwenning@redhat.com> - 1.5.2-2
- Convert STI tests to TMT (rhbz#2383068)
- use baserelease as that rpmdev-bumpspec can be used
- cleanly include <crm/crm.h> for crm_system_name and others

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-1.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-1.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 21 2024 Klaus Wenninger <kwenning@redhat.com> - 1.5.2-1.5
- Fixes bz#2327766

* Thu Nov 21 2024 Klaus Wenninger <kwenning@redhat.com> - 1.5.2-1.4
- Rebuild due to library bumps in pacemaker-3.0.0-rc1

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Feb 3 2023 Klaus Wenninger <kwenning@redhat.com> - 1.5.2-1
- rebase to upstream v1.5.2
- convert license naming to SPDX
- make static analysis happy with a few checks & rearanges with
  dynamic-memory-management

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jan 31 2022 Klaus Wenninger <kwenning@redhat.com> - 1.5.1-2
- Having de-allocation in the reverse order compared to
  allocation seems to make gcc-12 static analysis of
  dynamic-memory-management happy.

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 19 2021 Klaus Wenninger <kwenning@redhat.com> - 1.5.1-1
- sync with upstream spec-file
- Rebase to upstream v1.5.1
- added policy for rhel to gating

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 6 2021 Klaus Wenninger <kwenning@redhat.com> - 1.5.0-1
- sync with upstream spec-file
- Rebase to upstream v1.5.0
- added fix from upstream for build-regression
- added fix from upstream for handling leading space in devices

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 7 2020 Klaus Wenninger <kwenning@redhat.com> - 1.4.2-3
- this time really remove dist.depcheck from gating

* Mon Dec 7 2020 Klaus Wenninger <kwenning@redhat.com> - 1.4.2-2
- remove deprecated dist.depcheck from gating
- add tier0 to push_stable to have rawhide gated as well

* Mon Dec 7 2020 Klaus Wenninger <kwenning@redhat.com> - 1.4.2-1
- Rebase to upstream v1.4.2
- Conflict with pacemaker that doesn't have pacemakerd-api
- Set default to not do startup/shutdown-syncing via pacemakerd-api
  but enable in template-config

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 14 2020 Klaus Wenninger <kwenning@redhat.com> - 1.4.1-7
- Rebuild against libqb2.0 (f33-build-side-23348)

* Wed Mar 11 2020 Klaus Wenninger <kwenning@redhat.com> - 1.4.1-6
- Rebuild because tagging the build failed

* Thu Mar 5 2020 Klaus Wenninger <kwenning@redhat.com> - 1.4.1-5
- Rebase to upstream v1.4.1
- Make coverity happy with parameter passing in regressions.sh
- Add auto generated environment section to man-page
- Overhaul setting scheduler policy/priority
- Enable Fedora CI Gating

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 1 2019 Klaus Wenninger <kwenning@redhat.com> - 1.4.0-1
- Rebase to upstream v1.4.0
- Fail earlier on invalid servants (solves GCC9 build issue as well)

* Wed Nov 21 2018 Klaus Wenninger <kwenning@redhat.com> - 1.3.1-1.git4927571
- Rebased to commit 4927571f8e9b00db8242654b1329dfbd71dcfe99
- Removed disabling of shared-disk-support
  Resolves rhbz#1606301

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar 18 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2.1-4.2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Merlin Mathesius <mmathesi@redhat.com> - 1.2.1-4
- Patch to use correct C inline function semantics to fix FTBFS (BZ#1424417)
  Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Jan Pokorný <jpokorny+rpm-sbd@redhat.com> - 1.2.1-3
- Rebuilt for libpe_status soname bump arising from Pacemaker 1.1.14

* Thu Jul 02 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.2.1-2
- Add dist-tag (RHBZ #1237187).

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Oct 30 2014 <andrew@beekhof.net> - 1.2.1-1
- Correctly enable /proc/pid validation for sbd_lock_running()
- Improved integration with the el7 environment

* Fri Aug 29 2014 <andrew@beekhof.net> - 1.2.1-0.2.8f912945.git
- Remove some additional SUSE-isms

* Fri Aug 29 2014 <andrew@beekhof.net> - 1.2.1-0.1.8f912945.git
- Prepare for package review
  Resolves: rhbz#1134245
