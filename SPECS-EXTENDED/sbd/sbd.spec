Vendor:         Microsoft Corporation
Distribution:   Mariner
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
%global longcommit 044643922c3044c0bac2f91b1382ff3f2c64a4a2
%global shortcommit %(echo %{longcommit}|cut -c1-8)
%global github_owner Clusterlabs

%ifarch s390x s390
# minimum timeout on LPAR diag288 watchdog is 15s
%global watchdog_timeout_default 15
%else
%global watchdog_timeout_default 5
%endif

%global sync_resource_startup_default no
%global sync_resource_startup_sysconfig yes

Name:           sbd
Summary:        Storage-based death
License:        GPLv2+
Version:        1.4.2
Release:        4%{?dist}
Url:            https://github.com/%{github_owner}/%{name}
Source0:        https://github.com/%{github_owner}/%{name}/archive/%{longcommit}/%{name}-%{longcommit}.tar.gz
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
Conflicts:      pacemaker-libs < 2.0.5-10

%if 0%{?rhel}
ExclusiveArch: i686 x86_64 s390x aarch64 ppc64le
%endif

%if %{defined systemd_requires}
%systemd_requires
%endif

%description

This package contains the storage-based death functionality.

%package tests
Summary:        Storage-based death environment for regression tests
License:        GPLv2+

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
           --with-sync-resource-startup-default=%{sync_resource_startup_default} \
           --with-sync-resource-startup-sysconfig=%{sync_resource_startup_sysconfig}
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
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.2-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

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
