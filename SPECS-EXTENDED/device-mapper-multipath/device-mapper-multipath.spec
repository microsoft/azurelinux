Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:    device-mapper-multipath
Version: 0.8.2
Release: 5%{?dist}
Summary: Tools to manage multipath devices using device-mapper
License: GPLv2
URL:     http://christophe.varoqui.free.fr/

# The source for this package was pulled from upstream's git repo.  Use the
# following command to generate the tarball
# curl "https://git.opensvc.com/?p=multipath-tools/.git;a=snapshot;h=refs/tags/0.8.2;sf=tgz" -o multipath-tools-0.8.2.tgz
Source0: multipath-tools-0.8.2.tgz
Source1: multipath.conf
Patch0001: 0001-libmultipath-make-vector_foreach_slot_backwards-work.patch
Patch0002: 0002-libmultipath-add-marginal-paths-and-groups-infrastru.patch
Patch0003: 0003-tests-add-path-grouping-policy-unit-tests.patch
Patch0004: 0004-libmultipath-add-wrapper-function-around-pgpolicyfn.patch
Patch0005: 0005-tests-update-pgpolicy-tests-to-work-with-group_paths.patch
Patch0006: 0006-libmultipath-fix-double-free-in-pgpolicyfn-error-pat.patch
Patch0007: 0007-libmultipath-consolidate-group_by_-functions.patch
Patch0008: 0008-libmultipath-make-pgpolicyfn-take-a-paths-vector.patch
Patch0009: 0009-libmultipath-make-group_paths-handle-marginal-paths.patch
Patch0010: 0010-tests-add-tests-for-grouping-marginal-paths.patch
Patch0011: 0011-libmultipath-add-marginal_pathgroups-config-option.patch
Patch0012: 0012-libmutipath-deprecate-delay_-_checks.patch
Patch0013: 0013-multipathd-use-marginal_pathgroups.patch
Patch0014: 0014-multipath-update-man-pages.patch
Patch0015: 0015-multipath.conf-add-enable_foreign-parameter.patch
Patch0016: 0016-multipath.conf.5-document-foreign-library-support.patch
Patch0017: 0017-mpathpersist-remove-broken-unused-code.patch
Patch0018: 0018-libmultipath-EMC-PowerMax-NVMe-device-config.patch
Patch0019: 0019-mpathpersist-fix-leaks.patch
Patch0020: 0020-libmultipath-fix-mpcontext-initialization.patch
Patch0021: 0021-RH-fixup-udev-rules-for-redhat.patch
Patch0022: 0022-RH-Remove-the-property-blacklist-exception-builtin.patch
Patch0023: 0023-RH-don-t-start-without-a-config-file.patch
Patch0024: 0024-RH-use-rpm-optflags-if-present.patch
Patch0025: 0025-RH-add-mpathconf.patch
Patch0026: 0026-RH-add-wwids-from-kernel-cmdline-mpath.wwids-with-A.patch
Patch0027: 0027-RH-warn-on-invalid-regex-instead-of-failing.patch
Patch0028: 0028-RH-reset-default-find_mutipaths-value-to-off.patch
Patch0029: 0029-RH-Fix-nvme-compilation-warning.patch
Patch0030: 0030-RH-attempt-to-get-ANA-info-via-sysfs-first.patch
Patch0031: 0031-multipath-fix-issues-found-by-compiling-with-gcc-10.patch
Patch0032: 0032-libdmmp-private-boolean.patch

# runtime
Requires: %{name}-libs = %{version}-%{release}
Requires: kpartx = %{version}-%{release}
Requires: device-mapper >= 1.02.96
Requires: userspace-rcu
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# Starting with 0.7.7-1, 62-multipath.rules changed in a way that is
# incompatible with 65-md-incremental.rules in earlier mdadm packages.
# Later mdadm packages are compatible with any version of
# device-mapper-multipath. See bz #1628192 for more details
Conflicts: mdadm < 4.1-rc2.0.2
# Starting with 0.7.7-1, 62-multipath.rules changed in a way that is
# incompatible with 80-udisks2.rules in earlier udisks2 packages.
# Later udisks2 packages are compatible with any version of
# device-mapper-multipath. See bz #1628192 for more details
Conflicts: udisks2 < 2.8.0-2

# build/setup
BuildRequires: libaio-devel, device-mapper-devel >= 1.02.89
BuildRequires: libselinux-devel, libsepol-devel
BuildRequires: readline-devel, ncurses-devel
BuildRequires: systemd-units, systemd-devel
BuildRequires: json-c-devel, perl-interpreter, pkgconfig, gcc
BuildRequires: userspace-rcu-devel

%description
%{name} provides tools to manage multipath devices by
instructing the device-mapper multipath kernel module what to do. 
The tools are :
* multipath - Scan the system for multipath devices and assemble them.
* multipathd - Detects when paths fail and execs multipath to update things.

%package libs
Summary: The %{name} modules and shared library
# only libmpathcmd is LGPLv2+
License: GPLv2 and LGPLv2+

%description libs
The %{name}-libs provides the path checker
and prioritizer modules. It also contains the libmpathpersist and
libmpathcmd shared libraries, as well as multipath's internal library,
libmultipath.

%package devel
Summary: Development libraries and headers for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description devel
This package contains the files need to develop applications that use
device-mapper-multipath's lbmpathpersist and libmpathcmd libraries.

%package -n kpartx
Summary: Partition device manager for device-mapper devices

%description -n kpartx
kpartx manages partition creation and removal for device-mapper devices.

%package -n libdmmp
Summary: device-mapper-multipath C API library
License: GPLv3+
Requires: json-c
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description -n libdmmp
This package contains the shared library for the device-mapper-multipath
C API library.

%package -n libdmmp-devel
Summary: device-mapper-multipath C API library headers
Requires: pkgconfig
Requires: libdmmp = %{version}-%{release}

%description -n libdmmp-devel
This package contains the files needed to develop applications that use
device-mapper-multipath's libdmmp C API library

%prep
%autosetup -n multipath-tools-0.8.2 -p1
cp %{SOURCE1} .

%build
%define _sbindir /usr/sbin
%define _libdir /usr/%{_lib}
%define _libmpathdir %{_libdir}/multipath
%define _pkgconfdir %{_libdir}/pkgconfig
make %{?_smp_mflags} LIB=%{_lib}

%install
make install \
	DESTDIR=%{buildroot} \
	bindir=%{_sbindir} \
	syslibdir=%{_libdir} \
	usrlibdir=%{_libdir} \
	libdir=%{_libmpathdir} \
	rcdir=%{_initrddir} \
	unitdir=%{_unitdir} \
	includedir=%{_includedir} \
	pkgconfdir=%{_pkgconfdir}

# tree fix up
install -d %{buildroot}/etc/multipath
rm -rf %{buildroot}/%{_initrddir}


%post
%systemd_post multipathd.service

%preun
%systemd_preun multipathd.service

%postun
if [ $1 -ge 1 ] ; then
	/sbin/multipathd forcequeueing daemon > /dev/null 2>&1 || :
fi
%systemd_postun_with_restart multipathd.service

%triggerun -- %{name} < 0.4.9-37
# make sure old systemd symlinks are removed after changing the [Install]
# section in multipathd.service from multi-user.target to sysinit.target
/bin/systemctl --quiet is-enabled multipathd.service >/dev/null 2>&1 && /bin/systemctl reenable multipathd.service ||:

%files
%license LICENSES/GPL-2.0 LICENSES/LGPL-2.0
%{_sbindir}/multipath
%{_sbindir}/multipathd
%{_sbindir}/mpathconf
%{_sbindir}/mpathpersist
%{_unitdir}/multipathd.service
%{_unitdir}/multipathd.socket
%{_mandir}/man5/multipath.conf.5.gz
%{_mandir}/man8/multipath.8.gz
%{_mandir}/man8/multipathd.8.gz
%{_mandir}/man8/mpathconf.8.gz
%{_mandir}/man8/mpathpersist.8.gz
%config /usr/lib/udev/rules.d/62-multipath.rules
%config /usr/lib/udev/rules.d/11-dm-mpath.rules
%doc README
%doc README.alua
%doc multipath.conf
%dir /etc/multipath

%files libs
%license LICENSES/GPL-2.0 LICENSES/LGPL-2.0
%doc README
%{_libdir}/libmultipath.so
%{_libdir}/libmultipath.so.*
%{_libdir}/libmpathpersist.so.*
%{_libdir}/libmpathcmd.so.*
%dir %{_libmpathdir}
%{_libmpathdir}/*

%ldconfig_scriptlets libs

%files devel
%doc README
%{_libdir}/libmpathpersist.so
%{_libdir}/libmpathcmd.so
%{_includedir}/mpath_cmd.h
%{_includedir}/mpath_persist.h
%{_mandir}/man3/mpath_persistent_reserve_in.3.gz
%{_mandir}/man3/mpath_persistent_reserve_out.3.gz

%files -n kpartx
%license LICENSES/GPL-2.0
%doc README
%{_sbindir}/kpartx
/usr/lib/udev/kpartx_id
%{_mandir}/man8/kpartx.8.gz
%config /usr/lib/udev/rules.d/11-dm-parts.rules
%config /usr/lib/udev/rules.d/66-kpartx.rules
%config /usr/lib/udev/rules.d/68-del-part-nodes.rules

%files -n libdmmp
%license LICENSES/GPL-3.0
%doc README
%{_libdir}/libdmmp.so.*

%ldconfig_scriptlets -n libdmmp

%files -n libdmmp-devel
%doc README
%{_libdir}/libdmmp.so
%dir %{_includedir}/libdmmp
%{_includedir}/libdmmp/*
%{_mandir}/man3/dmmp_*
%{_mandir}/man3/libdmmp.h.3.gz
%{_pkgconfdir}/libdmmp.pc

%changelog
* Sat Jul 24 2021 Jon Slobodzian <jslobodzian@microsoft.com> - 0.8.2-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add Patch0032: 0032-libdmmp-private-boolean.patch to fix compilation issue

* Mon Apr 13 2020 Björn Esser <besser82@fedoraproject.org> - 0.8.2-4
- Fix macro escaping in %%changelog

* Wed Feb 12 2020  Benjamin Marzinski <bmarzins@redhat.com> - 0.8.2-3
- Add 0031-multipath-fix-issues-found-by-compiling-with-gcc-10.patch
  * Patch submitted upstream
- Resolves bz #1799276

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Benjamin Marzinski <bmarzins@redhat.com> - 0.8.2-1
- Update Source to upstream version 0.8.2
  * Previoud patches 0001-0017 & 0027 are included in this commit
- Rename files
  * Previous patches 0018-0026 & 0028 are not patches 0021-0030
- Add 0001-libmultipath-make-vector_foreach_slot_backwards-work.patch
- Add 0002-libmultipath-add-marginal-paths-and-groups-infrastru.patch
- Add 0003-tests-add-path-grouping-policy-unit-tests.patch
- Add 0004-libmultipath-add-wrapper-function-around-pgpolicyfn.patch
- Add 0005-tests-update-pgpolicy-tests-to-work-with-group_paths.patch
- Add 0006-libmultipath-fix-double-free-in-pgpolicyfn-error-pat.patch
- Add 0007-libmultipath-consolidate-group_by_-functions.patch
- Add 0008-libmultipath-make-pgpolicyfn-take-a-paths-vector.patch
- Add 0009-libmultipath-make-group_paths-handle-marginal-paths.patch
- Add 0010-tests-add-tests-for-grouping-marginal-paths.patch
- Add 0011-libmultipath-add-marginal_pathgroups-config-option.patch
- Add 0012-libmutipath-deprecate-delay_-_checks.patch
- Add 0013-multipathd-use-marginal_pathgroups.patch
- Add 0014-multipath-update-man-pages.patch
  * The above 13 patches add the marinal_pathgroups option
- Add 0015-multipath.conf-add-enable_foreign-parameter.patch
- Add 0016-multipath.conf.5-document-foreign-library-support.patch
  * The above 2 patches add the enable_foreign option
- Add 0017-mpathpersist-remove-broken-unused-code.patch
- Add 0018-libmultipath-EMC-PowerMax-NVMe-device-config.patch
- Add 0019-mpathpersist-fix-leaks.patch
- Add 0020-libmultipath-fix-mpcontext-initialization.patch
  * The above 20 patches have been submitted upstream

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr 12 2019 Benjamin Marzinski <bmarzins@redhat.com> - 0.8.0-2
- Add 0028-RH-attempt-to-get-ANA-info-via-sysfs-first.patch
  * try to get ANA state from sysfs first, with the ioctl as a fallback

* Thu Apr  4 2019 Benjamin Marzinski <bmarzins@redhat.com> - 0.8.0-1
- Update Source to upstream version 0.8.0
  * Previous patches 0006 & 0007 are included in this commit
- Rename files
  * Previous patches 0008-0016 & 0100 are now patches 0018-0027
- Add 0006-multipathd-Fix-miscounting-active-paths.patch
- Add 0007-multipathd-ignore-failed-wwid-recheck.patch
  * multipathd will no longer disable paths if it is unable to
    get their wwid on a change event
- Add 0008-libmutipath-continue-to-use-old-state-on-PATH_PENDIN.patch
- Add 0009-multipathd-use-update_path_groups-instead-of-reload_.patch
- Add 0010-multipath.conf-add-missing-options-to-man-page.patch
- Add 0011-libmultipath-add-get_uid-fallback-code-for-NVMe-devi.patch
- Add 0012-libmulitpath-cleanup-uid_fallback-code.patch
- Add 0013-multipathd-handle-changed-wwids-by-removal-and-addit.patch
  * if a path device changes wwid, it will now be removed and re-added
    to the correct multipath device.
- Add 0014-multipathd-remove-wwid_changed-path-attribute.patch
- Add 0015-multipathd-ignore-disable_changed_wwids.patch
- Add 0016-multipathd-Don-t-use-fallback-code-after-getting-wwi.patch
- Add 0017-libmultipath-silence-dm_is_mpath-error-messages.patch
  * The above 12 patches have been submitted upstream

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.9-6.git2df6110
- Rebuild for readline 8.0

* Thu Jan 31 2019 Benjamin Marzinski <bmarzins@redhat.com> - 0.7.9-5.git2df6110
- Rename files
  * Previous patch 0006-0014 are now patches 0008-0016
- Add 0006-multipathd-avoid-null-pointer-dereference-in-LOG_MSG.patch
- Add 0007-multipath-blacklist-zram-devices.patch
  * The above 2 patches have been submitted upstream
- Resolves: bz #1672761

* Thu Jan 31 2019 Benjamin Marzinski <bmarzins@redhat.com> - 0.7.9-4.git2df6110
- Update Source to latest upstream commit
  * previous patch 0001-libmultipath-dm_is_mpath-cleanup.patch is included
    in this commit
- Rename files
  * Previous patches 0002-0009 are now patches 0006-0013
- Add 0001-BZ-1668693-disable-user_friendly_names-for-NetApp.patch
- Add 0002-libmultipath-handle-existing-paths-in-marginal_path-.patch
- Add 0003-multipathd-cleanup-marginal-paths-checking-timers.patch
- Add 0004-libmultipath-fix-marginal-paths-queueing-errors.patch
- Add 0005-libmultipath-fix-marginal_paths-nr_active-check.patch
  * The above 5 patches have been submitted upstream
- Add 0014-RH-Fix-nvme-compilation-warning.patch
  * This change is only necessary because of Red Hat compilation
    differences.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9-3.git17a6101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Benjamin Marzinski <bmarzins@redhat.com> 0.7.9-2.git17a6101
- Update Source to latest upstream commit
  * Previous patches 0001-0003 are included in this version
- Rename files
  * Previous patches 0004-0011 are now patches 0002-0009
- Add 0001-libmultipath-dm_is_mpath-cleanup.patch
  * This patch has been submitted upstream

* Mon Dec  3 2018 Benjamin Marzinski <bmarzins@redhat.com> 0.7.9-1
- Update Source to upstream version 0.7.9
  * Previous patches 0001-0006 are included in this version
- Rename files
  * Previous patches 0007-0014 are now patches 0004-0011
- Add 0001-multipathd-fix-mpp-hwe-handling-when-paths-are-freed.patch
- Add 0002-libmultipath-cleanup-pthread_cleanup_pop-call.patch
- Add 0003-libmultipath-fix-false-removes-in-dmevents-polling-c.patch
  * The above 3 patches have been submitted upstream

* Wed Oct 10 2018 Benjamin Marzinski <bmarzins@redhat.com> 0.7.8-1
- Update Source to upstream version 0.7.8
  * Previous patches 0001-0020 are included in this version
- Rename files
  * Previous patches 0021-0025 are now patches 0001-0005
  * Previous patches 0026-0033 are now patches 0007-0014
- Add 0006-libmultipath-timeout-on-unresponsive-tur-thread.patch
  * has been submitted upstream

* Tue Oct  9 2018 Benjamin Marzinski <bmarzins@redhat.com> 0.7.7-7.gitb80318b
- Update Source to latest upstream commit
- Rename files
  * Previous patches 0001-0020 are now patches 0002-0021
  * Previous patches 0021-0028 are now patches 0026-0033
- Add 0001-kpartx-Use-absolute-paths-to-create-mappings.patch
- Add 0022-multipathd-check-for-NULL-udevice-in-cli_add_path.patch
- Add 0023-libmultipath-remove-max_fds-code-duplication.patch
- Add 0024-multipathd-set-return-code-for-multipathd-commands.patch
- Add 0025-mpathpersist-fix-registration-rollback-issue.patch
  * The above 5 patches have been submitted upstream

* Thu Sep 27 2018 Benjamin Marzinski <bmarzins@redhat.com> 0.7.7-6.git1a8625a
- Update Source to latest upstream commit
  * Previous patches 0001-0011 are included in this commit
- Rename files
  * Previous patches 0012-0019 are now patches 0021-0028
- Add 0001-libmultipath-fix-tur-checker-timeout.patch
- Add 0002-libmultipath-fix-tur-checker-double-locking.patch
- Add 0003-libmultipath-fix-tur-memory-misuse.patch
- Add 0004-libmultipath-cleanup-tur-locking.patch
- Add 0005-libmultipath-fix-tur-checker-timeout-issue.patch
  * The above 5 patches cleanup locking issues with the
    tur checker threads
- Add 0006-libmultipath-fix-set_int-error-path.patch
- Add 0007-libmultipath-fix-length-issues-in-get_vpd_sgio.patch
- Add 0008-libmultipath-_install_keyword-cleanup.patch
- Add 0009-libmultipath-remove-unused-code.patch
- Add 0010-libmultipath-fix-memory-issue-in-path_latency-prio.patch
- Add 0011-libmultipath-fix-null-dereference-int-alloc_path_gro.patch
- Add 0012-libmutipath-don-t-use-malformed-uevents.patch
- Add 0013-multipath-fix-max-array-size-in-print_cmd_valid.patch
- Add 0014-multipathd-function-return-value-tweaks.patch
- Add 0015-multipathd-minor-fixes.patch
- Add 0016-multipathd-remove-useless-check-and-fix-format.patch
- Add 0017-multipathd-fix-memory-leak-on-error-in-configure.patch
  * The above 12 patches fix minor issues found by coverity
- Add 0018-libmultipath-Don-t-blank-intialized-paths.patch
- Add 0019-libmultipath-Fixup-updating-paths.patch
  * Fix issues with paths whose wwid was not set or later changes
- Add 0020-multipath-tweak-logging-style.patch
  * multipathd interactive commands now send errors to stderr, instead
    of syslog
  * The above 20 patches have been submitted upstream

* Fri Sep 14 2018 Benjamin Marzinski <bmarzins@redhat.com> 0.7.7-5.gitef6d98b
- Add Conflicts for mdadm < 4.1-rc2.0.2 and udisks2 < 2.8.0-2
  * Multipath udev rule update from 0.7.7-1 is incompatible with older versions
    (bz #1628192)

* Thu Jul 12 2018 Benjamin Marzinski <bmarzins@redhat.com> 0.7.7-4.gitef6d98b
- Update Source to latest upstream commit
  * Previous patches 0001-0018 are included in this commit
- Rename files
  * Previous patches 0019-0028 are now patches 0002-0003 & 0012-0019
- Add 0001-libmultipath-remove-last-of-rbd-code.patch
- Add 0004-mpathpersist-add-param-alltgpt-option.patch
  * mpathpersist now accepts --param-alltgpt
- Add 0005-libmutipath-remove-unused-IDE-bus-type.patch
- Add 0006-multipathd-add-new-protocol-path-wildcard.patch
  * multipathd show paths format now accepts %%P for the path
    protocol/transport
- Add 0007-libmultipath-add-protocol-blacklist-option.patch
  * You can now use the "protocol" blacklist section parameter to blacklist
    by protocol/transport
- Add 0008-libmultipath-remove-_filter_-blacklist-functions.patch
- Add 0009-multipath-tests-change-to-work-with-old-make-version.patch
- Add 0010-multipath-tests-add-blacklist-tests.patch
- Add 0011-mpathpersist-add-missing-param-rk-usage-info.patch
- Refresh 0013-RH-Remove-the-property-blacklist-exception-builtin.patch
- Modify 0016-RH-add-mpathconf.patch
  * improve usage message and man page

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.7-2
- Spec cleanups, drop remains of initscripts dependencies

* Tue Jun 12 2018 Benjamin Marzinski <bmarzins@redhat.com> 0.7.7-1
- Update Source to 0.7.7
  * Previous patches 0001-0009 & 0018 are included in this commit
- Add upstream patches since 0.7.7
  * patches 0001-0012 are from upstream commits since 0.7.7
- Add 0015-mpathpersist-add-all_tg_pt-option.patch
  * add new all_tg_pt multpiath.conf option. posted upstream
- Add 0016-libmultipath-remove-rbd-code.patch
  * remove unused rbd code. posted upstream
- Add 0017-mpathpersist-fix-aptpl-support.patch
  * add ":aptpl" suffix for reservation_key to fix aptpl support.
    posted upstream
- Add 0018-multipath-don-t-check-timestamps-without-a-path.patch
  * fix multipath null dereference crash. posted upstream
- Add 0019-libmultipath-fix-detect-alua-corner-case.patch
  * fix alua detection with retain_hardware_handler set to off. posted
    upstream
- Add 0020-multipath-fix-setting-conf-version.patch
  * multipath wasn't setting the kernel version correctly. posted upstream
- Add 0028-RH-reset-default-find_mutipaths-value-to-off.patch
  * default to RHEL7 and older device detection style. Redhat specific, to
    keep customer experience the same.
- Rename files
  * Previous patches 0010-0011 are now patches 0013-0014
  * Previous patches 0012-0017 & 0019 are now patches 0021-0027
- Modify 0021-RH-fixup-udev-rules-for-redhat.patch
  * Fix spurious compile warning with redhat compile options


* Tue May 15 2018 Benjamin Marzinski <bmarzins@redhat.com> 0.7.6-4.git1cb704b
- Add 0010-libmultipath-print-correct-default-for-delay_-_check.patch
  * fix minor configuration printing issue
- Add 0011-multipath.conf.5-clarify-property-whitelist-handling.patch
  * clarify property blacklist_excecptions handling in man page
- Rename files
  * Previous patches 0010-0017 are now patches 0012-0019
- Modify 0013-RH-Remove-the-property-blacklist-exception-builtin.patch
  * clarify changes in man page

* Tue Apr 24 2018 Benjamin Marzinski <bmarzins@redhat.com> 0.7.6-3.git1cb704b
- Add 0008-multipathd-add-failures-path-format-wildcard.patch
- Add 0009-multipathd-fix-reservation_key-check.patch
- Rename files
  * Previous patches 0008-0015 are now patches 0010-0017

* Fri Apr 13 2018 Benjamin Marzinski <bmarzins@redhat.com> 0.7.6-2.git1cb704b
- Add 0007-libmultipath-Fix-logic-in-should_multipath.patch
  * fix bug in identifying multipathable devices. posted upstream
- Rename files
  * Previous patches 0007-0014 are now patches 0008-0015

* Tue Apr 02 2018 Björn Esser <besser82@fedoraproject.org> - 0.7.6-1.git1cb704b
- Update Source to the latest upstream commit
  * Previous patches 0001-0014 are included in this commit
  * Previous patches 0015-0022 are now patches 0007-0014
- 0001-multipathd-remove-incorrect-pthread_testcancel.patch
  * Fixed pthread cancellation issue. posted upstream
- 0002-multipath-add-comments.patch
  * Posted upstream
- 0003-multipathd-minor-dmevents-polling-code-cleanups.patch
  * Fixed minor polling issues. posted upstream
- 0004-multipathd-remove-unneeded-function-parameter.patch
  * Posted upstream
- 0005-mpathcmd-fix-libmpathcmd-license.patch
  * License clarification. posted upstream
- 0006-libmultipath-don-t-print-undefined-values.patch
  * Fixed bug in 'multipath show config'. posted upstream

* Tue Mar 06 2018 Björn Esser <besser82@fedoraproject.org> - 0.7.4-2.git07e7bd5
- Rebuilt for libjson-c.so.4 (json-c v0.13.1)

* Thu Feb 15 2018 Benjamin Marzinski <bmarzins@redhat.com> 0.7.4-1.git07e7bd5
- Update Source to the latest upstream commit
  * Previous patches 0001-0006 are included in this commit
  * Previous patches 0007-0014 are now patches 0015-0022
- Add 0001-libmultipath-fix-tur-checker-locking.patch
  * Fixed spinlock bug. posted upstream
- Add 0002-multipath-fix-DEF_TIMEOUT-use.patch
  * Add missing sec to ms conversion. posted upstream
- Add 0003-multipathd-remove-coalesce_paths-from-ev_add_map.patch
  * Remove unused code. posted upstream
- Add 0004-multipathd-remove-unused-configure-parameter.patch
  * Remove unused code. posted upstream
- Add 0005-Fix-set_no_path_retry-regression.patch
  * Fix issue with queueing and path addition. posted upstream
- Add 0006-multipathd-change-spurious-uevent-msg-priority.patch
  * Change message priority to Notice. posted upstream
- Add 0007-multipath-print-sysfs-state-in-fast-list-mode.patch
  * Show sysfs state correctly in fast list mode (-l). posted upstream
- Add 0008-libmultipath-move-remove_map-waiter-code-to-multipat.patch
  * Move code around. posted upstream
- Add 0009-move-waiter-code-from-libmultipath-to-multipathd.patch
  * Move code around. posted upstream
- Add 0010-call-start_waiter_thread-before-setup_multipath.patch
  * Fix race on multipath device creations. posted upstream
- Add 0011-libmultipath-add-helper-functions.patch
  * posted upstream
- Add 0012-multipathd-RFC-add-new-polling-dmevents-waiter-threa.patch
  * Add alternate method of getting dmevents, that doesn't
    require a thread per device. posted upstream
- Add 0013-libmultipath-condlog-log-to-stderr.patch
  * change condlog to log to stderr instead of stdout. posted upstream
- Add 0014-multipathd-fix-compiler-warning-for-uev_pathfail_che.patch
  * fix indentation issue. posted upstream

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 10 2017 Björn Esser <besser82@fedoraproject.org> - 0.7.3-2
- Rebuilt for libjson-c.so.3

* Tue Nov  7 2017 Benjamin Marzinski <bmarzins@redhat.com> 0.7.3-1
- Update Source to upstream 0.7.3 release
  * Previous patch 0001 is included in this commit, and 0002 was solved in a
    different manner causing some change to previous patch 0003
  * Previous patches 0003-0010 are now patches 0007-0014
- Add 0001-mpathpersist-Fix-invalid-condition-check.patch
  * Fix incorrect check. posted upstream
- Add 0002-multipath-add-man-page-info-for-my-prkey-changes.patch
  * Add missing man page info. posted upstream
- Add 0003-multipath-there-is-no-none-path-state.patch
  * remove incorrect path state. posted upstream
- Add 0004-mutipath-updated-Huawei-storage-config.patch
  * update builtin device configuration. posted upstream
- Add 0005-multipath-fix-doc-typo.patch
  * fix man page typo. posted upstream
- Add 0006-multipath-add-ghost_delay-parameter.patch
  * add new multipath.conf parameter "ghost_delay". posted upstream


* Tue Nov  7 2017 Benjamin Marzinski <bmarzins@redhat.com> 0.7.1-8.git847cc43
- Refresh 0001-libmultipath-update-3PARdata-builtin-config.patch
- Add 0010-RH-warn-on-invalid-regex-instead-of-failing.patch
  * Change old-style multipath.conf regex "*" to a proper ".*" instead of
    failing

* Wed Aug  2 2017 Benjamin Marzinski <bmarzins@redhat.com> 0.7.1-7.git847cc43
- Modify 0005-RH-don-t-start-without-a-config-file.patch
  * Fix man page typos

* Mon Jul 31 2017 Troy Dawson <tdawson@redhat.com> - 0.7.1-6.git847cc43
- Clean spec file - remove pre-fedora 23 cruft

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-5.git847cc43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Benjamin Marzinski <bmarzins@redhat.com> 0.7.1-4.git847cc43
- Update Source to the latest upstream commit
  * Previous patches 0001 and 0010-0013 are included in this commit.
- Add 0001-libmultipath-update-3PARdata-builtin-config.patch
  * Change for building configuration. Posted upstream
- Modify 0006-RH-use-rpm-optflags-if-present.patch
  * Add missing lines to actually use RPM_OPT_FLAGS.

* Fri Jun 23 2017 Tom Callaway <spot@fedoraproject.org> - 0.7.1-3.gitf21166a
- rebuild to resolve broken deps

* Fri Jun  2 2017 Benjamin Marzinski <bmarzins@redhat.com> 0.7.1-2.gitf21166a
- Modify 0004-RH-Remove-the-property-blacklist-exception-builtin.patch
  * update multipath.conf.5 man page to remove builtin listing
- Modify 0005-RH-don-t-start-without-a-config-file.patch
  * update multipathd.8 man page to note that a config file is necessary
- Modify 0007-RH-add-mpathconf.patch
  * add property blacklist-exception to default config file
- Add 0010-libmultipath-change-how-RADOS-checker-is-enabled.patch
  * Makefile now autodetects librados. Posted upstream
- Remove related RADOS option from spec file
- Add 0011-multipath-set-verbosity-to-default-during-config.patch
  * Allow multipath to print warning messages during configuration.
    Posted upstream
- Add 0012-mpath-skip-device-configs-without-vendor-product.patch
  * device entries without vendor/product were breaking configurations.
    Posted upsteam
- Add 0013-multipathd-fix-show-maps-json-crash.patch
  * multipathd crashed showing json output with no devices. Posted
    upstream

* Tue May 23 2017 Benjamin Marzinski <bmarzins@redhat.com> 0.7.1-1.gitf21166a
- Update Source to the latest upstream commit
- Add 0001-libmultipath-add-comment-about-resuming.patch
  * posted upstream
- Add 0002-multipath-attempt-at-common-multipath.rules.patch
  * under discussion upstream
- Add 0003-RH-fixup-udev-rules-for-redhat.patch
  * Redhat uses different udev rules that some other distros, so multipath
    has run at a different time. Not all upstream distros link /sbin and
    /usr/sbin either.
- Add 0004-RH-Remove-the-property-blacklist-exception-builtin.patch
  * Allow multipath to be used on devices without multiple paths. NAK'ed
    upstream, but requested by Red Hat
- Add 0005-RH-don-t-start-without-a-config-file.patch
  * Don't start multipath unless a config file exists. NAK'ed upstream,
    but requested by Red Hat
- Add 0006-RH-use-rpm-optflags-if-present.patch
  * Make the build system fedora friendly
- Add 0007-RH-add-mpathconf.patch
  * Add tool to help configure multipath with Red Hat defaults.
- Add 0008-RH-add-wwids-from-kernel-cmdline-mpath.wwids-with-A.patch
  * Make multipath able to claim devices based on the kernel command line
    NAK'ed upstream but requested by Red Hat
- Add 0009-RH-trigger-change-uevent-on-new-device-creation.patch
  * under discussion upstream

* Wed Apr 12 2017 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-87
- Remove Epoch from device-mapper requires
  * The RHEL releases of device-mapper set the Epoch, and this was
    accidentally retained in the fedora spec file.

* Fri Apr  7 2017 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-86
- Modify 0136-RHBZ-1304687-wait-for-map-add.patch
  * switch to missing_uev_wait_timeout to stop waiting for uev
- Refresh 0137-RHBZ-1280524-clear-chkr-msg.patch
- Refresh 0150-RHBZ-1253913-fix-startup-msg.patch
- Refresh 0154-UPBZ-1291406-disable-reinstate.patch
- Refresh 0156-UPBZ-1313324-dont-fail-discovery.patch
- Refresh 0161-RHBZ-1311659-no-kpartx.patch
- Refresh 0167-RHBZ-1335176-fix-show-cmds.patch
- Add 0173-RH-update-man-page.patch
- Add 0174-RHBZ-1362396-modprobe.patch
  * make starting the multipathd service modprobe dm-multipath in the
    sysvinit scripts
- Add 0175-RHBZ-1357382-ordering.patch
  * force multipathd.service to start after systemd-udev-trigger.service
- Add 0176-RHBZ-1363830-fix-rename.patch
  * initialized a variable to make dm_rename not fail randomly
- Add 0177-libmultipath-correctly-initialize-pp-sg_id.patch
  * This and all the following patches add the rbd patch checker
- Add 0178-libmultipath-add-rbd-discovery.patch
- Add 0179-multipath-tools-add-checker-callout-to-repair-path.patch
- Add 0180-multipath-tools-Add-rbd-checker.patch
- Add 0181-multipath-tools-Add-rbd-to-the-hwtable.patch
- Add 0182-multipath-tools-check-for-initialized-checker-before.patch
- Add 0183-multipathd-Don-t-call-repair-on-blacklisted-path.patch
- Add 0184-rbd-fix-sync-repair-support.patch
- Add 0185-rbd-check-for-nonshared-clients.patch
- Add 0186-rbd-check-for-exclusive-lock-enabled.patch
- Add 0187-rbd-fixup-log-messages.patch
- Add 0188-RHBZ-1368501-dont-exit.patch
  * make multipathd not exit if it encounters recoverable errors on startup
- Add 0189-RHBZ-1368211-remove-retries.patch
  * add "remove_retries" multipath.conf parameter to make multiple attempts
    to remove a multipath device if it is busy.
- Add 0190-RHBZ-1380602-rbd-lock-on-read.patch
  * pass lock_on_read when remapping image
- Add 0191-RHBZ-1169168-disable-changed-paths.patch
  * add "disabled_changed_wwids" multipath.conf parameter to disable
    paths whose wwid changes
- Add 0192-RHBZ-1362409-infinibox-config.patch
- Add 0194-RHBZ-1351964-kpartx-recurse.patch
  * fix recursion on corrupt dos partitions
- Add 0195-RHBZ-1359510-no-daemon-msg.patch
  * print a messages when multipathd isn't running
- Add 0196-RHBZ-1239173-dont-set-flag.patch
  * don't set reload flag on reloads when you gain your first
    valid path
- Add 0197-RHBZ-1394059-max-sectors-kb.patch
  * add "max_sectors_kb" multipath.conf parameter to set max_sectors_kb
    on a multipath device and all its path devices
- Add 0198-RHBZ-1372032-detect-path-checker.patch
  * add "detect_checker" multipath.conf parameter to detect ALUA arrays
    and set the path checker to TUR
- Add 0199-RHBZ-1279355-3pardata-config.patch
- Add 0200-RHBZ-1402092-orphan-status.patch
  * clear status on orphan paths
- Add 0201-RHBZ-1403552-silence-warning.patch
- Add 0202-RHBZ-1362120-skip-prio.patch
  * don't run prio on failed paths
- Add 0203-RHBZ-1363718-add-msgs.patch
- Add 0204-RHBZ-1406226-nimble-config.patch
- Add 0205-RHBZ-1416569-reset-stats.patch
  * add "reset maps stats" and "reset map <map> stats" multipathd
    interactive commands to reset the stats tracked by multipathd
- Add 0206-RHBZ-1239173-pt2-no-paths.patch
  * make multipath correctly disable scanning and rules running when
    it gets a uevent and there are not valid paths.
- Add 0207-UP-add-libmpathcmd.patch
  * New shared library, libmpathcmd, that sends and receives messages from
    multipathd. device-mapper-multipath now uses this library internally.
- Add 0208-UPBZ-1430097-multipathd-IPC-changes.patch
  * validation that modifying commands are coming from root.
- Add 0209-UPBZ-1430097-multipath-C-API.patch
  * New shared library. libdmmp, that presents the information from multipathd
    in a structured manner to make it easier for callers to use
- Add 0210-RH-fix-uninstall.patch
  * Minor compilation fixes
- Add 0211-RH-strlen-fix.patch
  * checks that variables are not NULL before passing them to strlen
- Add 0212-RHBZ-1431562-for-read-only.patch
- Make 3 new subpackages
  * device-mapper-multipath-devel, libdmmp, and libdmmp-devel. libmpathcmd
    and libmpathprio are in device-mapper-multipath-libs and
    device-mapper-multipath-devel. libdmmp is in its own subpackages
- Move libmpathprio devel files to device-mapper-multipath-devel
- Added BuildRequires on librados2-devel


* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-85
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.4.9-84
- Rebuild for readline 7.x

* Fri Jul 22 2016 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-83
- Modify 0135-RHBZ-1299600-path-dev-uevents.patch
  * trigger uevents when adding wwids for existing devices during startup
- Refresh 0136-RHBZ-1304687-wait-for-map-add.patch
- Refresh 0150-RHBZ-1253913-fix-startup-msg.patch
- Modify 0159-UPBZ-1255885-udev-waits.patch
  * fix bug in failure path
- Add 0160-RH-udev-flags.patch
- Add 0161-RHBZ-1311659-no-kpartx.patch
  * skip_kpartx option disables kpartx running on multipath devices
- Add 0162-RHBZ-1333331-huawei-config.patch
  * Add default config for Huawei XSG1 array
- Add 0163-UPBZ-1333492-resize-map.patch
  * restore old size if resize fails
- Add 0164-RHBZ-1311463-dos-part-rollover.patch
  * fix incorrect partition size due to 4k device size rollover
- Add 0165-UPBZ-1341748-MSA-2040-conf.patch
  * Add default config for MSA 2040 array
- Add 0166-RHBZ-1323429-dont-allow-new-wwid.patch
  * don't allow path wwid to change while it is in use
- Add 0167-RHBZ-1335176-fix-show-cmds.patch
  * and new show multipath format wildcard, 'f' to sho number of failures.
    This will hopefully be useful for tracking what happens to multipath
    devices for bz #1335176
- Add 0168-RHBZ-1347769-shared-lock.patch
  * make multipath lock the path devices with a shared lock
- Add 0169-UPBZ-1353357-json-output.patch
  * add mulitpathd json output command
- Add 0170-UPBZ-1352925-fix-typo.patch
- Add 0171-UPBZ-1356651-allow-zero-size.patch
  * Allow zero-sized paths to be added to a multipath device
- Add 0172-RHBZ-1350931-no-active-add.patch
  * Allow paths to be added to a new map if no active paths exist. Also
    fixes 1351430


* Thu Apr 21 2016 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-82
- Modify 0005-RH-add-mpathconf.patch
  * changed warning message
- Modify 0102-RHBZ-1160478-mpathconf-template.patch
  * updated man page
- Modify 0104-RHBZ-631009-deferred-remove.patch
  * refactor code and minor fix
- Refresh 0107-RHBZ-1169935-no-new-devs.patch
- Refresh 0112-RHBZ-1194917-add-config_dir-option.patch
- Refresh 0126-RHBZ-1211383-alias-collision.patch
- Add 0133-RHBZ-1296979-fix-define.patch
  * look for the correct libudev function to set define
- Add 0134-RHBZ-1241528-check-mpath-prefix.patch
  * only touch devices with a "mpath-" dm uuid prefix
- Add 0135-RHBZ-1299600-path-dev-uevents.patch
  * trigger path uevent the first time a path is claimed by multipath
- Add 0136-RHBZ-1304687-wait-for-map-add.patch
  * wait for the device to finish being added before reloading it.
- Add 0137-RHBZ-1280524-clear-chkr-msg.patch
- Add 0138-RHBZ-1288660-fix-mpathconf-allow.patch
  * don't remove existing lines from blacklist_exceptions section
- Add 0139-RHBZ-1273173-queue-no-daemon-doc.patch
- Add 0140-RHBZ-1299647-fix-help.patch
- Add 0141-RHBZ-1303953-mpathpersist-typo.patch
- Add 0142-RHBZ-1283750-kpartx-fix.patch
  * only remove devices if their uuid says that they are the correct
    partition device
- Add 0143-RHBZ-1299648-kpartx-sync.patch
  * default to using udev sync mode
- Add 0144-RHBZ-1299652-alua-pref-arg.patch
  * allow "exclusive_pref_bit" argument to alua prioritizer
- Add 0145-UP-resize-help-msg.patch
- Add 0146-UPBZ-1299651-raw-output.patch
  * allow raw format mutipathd show commands, that remove headers and padding
- Add 0147-RHBZ-1272620-fail-rm-msg.patch
- Add 0148-RHBZ-1292599-verify-before-remove.patch
  * verify that all partitions are unused before attempting to remove a device
- Add 0149-RHBZ-1292599-restore-removed-parts.patch
  * don't disable kpartx when restoring the first path of a device.
- Add 0150-RHBZ-1253913-fix-startup-msg.patch
  * wait for multipathd daemon to write pidfile before returning
- Add 0151-RHBZ-1297456-weighted-fix.patch
  * add wwn keyword to weighted prioritizer for persistent naming
- Add 0152-RHBZ-1269293-fix-blk-unit-file.patch
  * use "Wants" instead of "Requires"
- Add 0153-RH-fix-i686-size-bug.patch
  * use 64-bit keycodes for multipathd client commands
- Add 0154-UPBZ-1291406-disable-reinstate.patch
  * don't automatically reinstate ghost paths for implicit alua devices
- Add 0155-UPBZ-1300415-PURE-config.patch
  * Add default config for PURE FlashArray
- Add 0156-UPBZ-1313324-dont-fail-discovery.patch
  * don't fail discovery because individual paths failed.
- Add 0157-RHBZ-1319853-multipath-c-error-msg.patch
  * better error reporting for multipath -c
- Add 0158-RHBZ-1318581-timestamp-doc-fix.patch
  * add documentation for -T
- Add 0159-UPBZ-1255885-udev-waits.patch
  * make multipath and kpartx wait after for udev after each command

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-81
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 25 2015 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-80
- Add 0131-RHBZ-1259523-host_name_len.patch
  * increase size of host string
- Add 0132-UPBZ-1259831-lock-retry.patch
  * retry locking when creating multipath devices

* Mon Aug 17 2015 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-79
- Add 0130-UPBZ-1254292-iscsi-targetname.patch
  * check for targetname iscsi sysfs value

* Thu Aug 13 2015 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-78
- fix triggerun issue and updated requires in spec file.

* Fri Aug  7 2015 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-77
- Modify 0104-RHBZ-631009-deferred-remove.patch
  * add man page info
- Refresh 0112-RHBZ-1194917-add-config_dir-option.patch
- Refresh 0114-RHBZ-1196394-delayed-reintegration.patch
- Add 0118-UPBZ-1200738-update-eternus-config.patch
  * update default config
- Add 0119-RHBZ-1081397-save-alua-info.patch
  * make prioritizers save information between calls to speed them up.
- Add 0120-RHBZ-1043093-realloc-fix.patch
  * free old memory if realloc fails.
- Add 0121-RHBZ-1197234-rules-fix.patch
  * make sure kpartx runs after an DM_ACTIVATION event occurs.
- Add 0122-RHBZ-1212590-dont-use-var.patch
  * use /run instead of /var/run
- Add 0123-UPBZ-1166072-fix-path-offline.patch
  * Don't mark quiesce and transport-offline paths as offline
- Add 0124-RHBZ-1209275-retrigger-uevents.patch
  * Make multipathd retrigger uevents when paths haven't successfully had
    their udev_attribute environment variable set by udev and add
    "retrigger_ties" and "retrigger_delay" to control this
- Add 0125-RHBZ-1153832-kpartx-delete.patch
  * Delete all partition devices with -d (not just the ones in the partition
    table)
- Add 0126-RHBZ-1211383-alias-collision.patch
  * make multipathd use the old alias, if rename failed and add
    "new_bindings_in_boot" to determine if new bindings can be added to
    the bindings file in the initramfs
- Add 0127-RHBZ-1201030-use-blk-availability.patch
  * Make multipath use blk-availability.service
- Add 0128-RHBZ-1222123-mpathconf-allow.patch
  * Add mpathconf --allow for creating specialized config files.
- Add 0129-RHBZ-1241774-sun-partition-numbering.patch
  * Make kpartx correctly number sun partitions.


* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-76
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 11 2015 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-75
- Add 0111-RH-dont-show-pg-timeout.patch
  * The kernel doesn't support pg_timeout, so multipath shouldn't
    bother to display it
- Add 0112-RHBZ-1194917-add-config_dir-option.patch
  * multipath will now also read its configuration from files with
    the .conf suffix in the directory specified by config_dir
    which defaults to /etc/multipath/conf.d
- Add 0113-RHBZ-1194917-cleanup.patch
  * cleanup some unnecessary code
- Add 0114-RHBZ-1196394-delayed-reintegration.patch
  * Add "delay_watch_checks" and "delay_wait_checks" options to delay
    reintegration of flakey paths.
- Add 0115-RHBZ-1198418-fix-double-free.patch
  * multipath was freeing the multipath alias twice if it failed to create the
    multipath device.
- Add 0116-UPBZ-1188179-dell-36xxi.patch
  * new builtin configurations.
- Add 0117-RHBZ-1198424-autodetect-clariion-alua.patch
  * configure multipath to automatically detect alua settings on clariion
    devices.

* Thu Mar 05 2015 Adam Jackson <ajax@redhat.com> 0.4.9-74
- Drop sysvinit subpackage from F23+

* Wed Feb 18 2015 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-73
- Add 0110-RHBZ-blacklist-vd-devs.patch
  * blacklist vd[a-z] devices, since they don't have a WWID for
    multipath to use.

* Thu Dec 18 2014 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-72
- Modify 0107-RHBZ-1169935-no-new-devs.patch
  * instead of using "-n" there is now a new configuration option,
    'ignore_new_boot_devs'. If set to 'yes', multipath will ignore
    devices that aren't in /etc/multipath/wwids when running in the
    initramfs. This option does nothing while multipathd is running
    in the real root filesystem.
- Update 0109-RH-read-only-bindings.patch

* Mon Dec 15 2014 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-71
- Add 0103-RH-cleanup-partmaps-code.patch
  * code refactoring to prepare for next patch
- Add 0104-RHBZ-631009-deferred-remove.patch
  * add deferred_remove option to /etc/multipath.conf
- Add 0105-RHBZ-1148979-fix-partition-mapping-creation-race-with-kpartx.patch
  * Only run kpartx on device activation
- Add 0106-RHBZ-1159337-fix-double-free.patch
  * made ev_remove_path exit immediately after failing setup_multipath, since
    it handles cleaning up the device
- Add 0107-RHBZ-1169935-no-new-devs.patch
  * Add new multipathd option '-n' which keeps multipathd from creating any
    multipath devices that aren't in the /etc/multipath/wwids file.
- Add 0108-RHBZ-1153832-kpartx-remove-devs.patch
  * switch from 'kpartx -a' to 'kpartx -u' to remove missing devices as well.
- Add 0109-RH-read-only-bindings.patch
  * re-enabled -B option for multipathd

* Tue Dec  9 2014 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-70
- Add 0102-RHBZ-1160478-mpathconf-template.patch
  * mpathconf no longer copies the default config template for the
    docs directory.  It simply writes the template itself.
- Resolves: bz# 1160478

* Thu Nov 13 2014 Benjmain Marzinski <bmarzins@redhat.com> 0.4.9-69
- Rebuild

* Tue Sep 16 2014 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-68
- Modify multipath.conf
  * remove getuid_callout example
- Re-add 0050-RH-listing-speedup.patch
- Add 0081-RHBZ-1066264-check-prefix-on-rename.patch
  * make multipath check the prefix on kpartx partitions during rename, and
    copy the existing behaviour
- Add 0082-UPBZ-1109995-no-sync-turs-on-pthread_cancel.patch
  * If async tur checker fails on threads, don't retry with the sync version
- Add 0083-RHBZ-1080055-orphan-paths-on-reload.patch
  * Fix case where pathlist wasn't getting updated properly
- Add 0084-RHBZ-1110000-multipath-man.patch
  * fix errors in multipath man page
- Add 0085-UPBZ-1110006-datacore-config.patch
  * Add support for DataCore Virtual Disk
- Add 0086-RHBZ-1110007-orphan-path-on-failed-add.patch
  * If multipathd fails to add path correctly, it now fully orphans the path
- Add 0087-RHBZ-1110013-config-error-checking.patch
  * Improve multipath.conf error checking.
- Add 0088-RHBZ-1069811-configurable-prio-timeout.patch
  * checker_timeout now adjusts the timeouts of the prioritizers as well.
- Add 0089-RHBZ-1110016-add-noasync-option.patch
  * Add a new defaults option, "force_sync", that disables the async mode
    of the path checkers. This is for cases where to many parallel checkers
    hog the cpu
- Add 0090-UPBZ-1080038-reorder-paths-for-round-robin.patch
  * make multipathd order paths for better throughput in round-robin mode
- Add 0091-RHBZ-1069584-fix-empty-values-fast-io-fail-and-dev-loss.patch
  * check for null pointers in configuration reading code.
- Add 0092-UPBZ-1104605-reload-on-rename.patch
  * Reload table on rename if necessary
- Add 0093-UPBZ-1086825-user-friendly-name-remap.patch
  * Keep existing user_friend_name if possible
- Add 0094-RHBZ-1086825-cleanup-remap.patch
  * Cleanup issues with upstream patch
- Add 0095-RHBZ-1127944-xtremIO-config.patch
  * Add support for EMC ExtremIO devices
- Add 0096-RHBZ-979474-new-wildcards.patch
  * Add N, n, R, and r path wildcards to print World Wide ids
- Add 0097-RH-fix-coverity-errors.patch
  * Fix a number of unterminated strings and memory leaks on failure
    paths.
- Add 0098-UPBZ-1067171-mutipath-i.patch
  * Add -i option to ignore wwids file when checking for valid paths
- Add 0099-RH-add-all-devs.patch
  * Add new devices config option all_devs. This makes the configuration
    overwrite the specified values in all builtin configs
- Add 0100-RHBZ-1067171-multipath-i-update.patch
  * make -i work correctly with find_multipaths
- Add 0101-RH-adapter-name-wildcard.patch
  * Add 'a' path wildcard to print adapter name

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-67
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 0.4.9-66
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-65
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-64
- Modify 0076-RHBZ-1056686-add-hw_str_match.patch
  * free temporary memory used during configuration
- Add 0078-RHBZ-1054044-fix-mpathconf-manpage.patch
  * fix typo
- Add 0079-RHBZ-1070581-add-wwid-option.patch
  * add multipath option "-a". To add a device's wwid to the wwids file
- Add 0080-RHBZ-1075796-cmdline-wwid.patch
  * add multipath option "-A" to add wwids specified by the kernel
    command line mapth.wwid options.

* Fri Jan 24 2014 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-63
- Add 0074-RHBZ-1056976-dm-mpath-rules.patch
  * Add rules to keep from doing work in udev if there are no
    active paths, or if the event was for a multipath device
    reloading its table due to a path change.
- Add 0075-RHBZ-1056976-reload-flag.patch
  * multipath code to identify reloads that the new rules can
    ignore
- Add 0076-RHBZ-1056686-add-hw_str_match.patch
  * add a new default config paramter, "hw_str_match", to make user
    device configs only overwrite builtin device configs if the
    identifier strings match exactly, like the default in RHEL6.

* Fri Jan 10 2014 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-62
- Modify 0072-RHBZ-1039199-check-loop-control.patch
  * only call close on the /dev/loop-control fd the open succeeds
- Add 0073-RH-update-build-flags.patch
  * fix print call to work with -Werror=format-security compile flag

* Tue Dec 10 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-61
- Add 0072-RHBZ-1039199-check-loop-control.patch
  * Make kpartx use LOOP_CTL_GET_FREE and loop-control to find a free
    loop device. This will autoload the loop module.

* Mon Dec  9 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-60
- Add 0067-RHBZ-1022899-fix-udev-partition-handling.patch
  * Make sure to wipe partition devices on change event if they weren't
    wiped on the device add event
- Add 0068-RHBZ-1034578-label-partition-devices.patch
  * Make sure that partition devices are labeled like the whole device
- Add 0069-UPBZ-1033791-improve-rdac-checker.patch
  *  Use RTPG data in RDAC checker
- Add 0070-RHBZ-1036503-blacklist-td-devs.patch
- Add 0071-RHBZ-1031546-strip-dev.patch
  * make multipathd interactive commands able to handle /dev/<devnode>
    instead of just <devnode>

* Sat Oct 12 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-59
- Add 0066-UP-dos-4k-partition-fix.patch
  * Make kpartx correctly handle 4K sector size devices with dos partitions.

* Fri Sep 27 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-58
- Add 0065-UPBZ-995538-fail-rdac-on-unavailable.patch
  * make rdac checker always mark paths with asymmetric access state of
    unavailable as down

* Fri Sep 20 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-57
- Add 0063-RH-fix-warning.patch
  * Fix complier warning
- 0064-fix-ID_FS-attrs.patch
  * make multipath create a timestamp file /run/multipathd/timestamp, and
    add -T<timestamp>:<valid> option to shortcut processing if the
    timestamp hasn't changed

* Thu Sep  5 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-56
- Add 0061-RH-display-find-mpaths.patch
  * display the find_multipaths value in show config
- Add 0062-RH-dont-free-vecs.patch
  * don't free the vecs structure on shutdown. It's more pain than
    it's worth.

* Thu Jul 25 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-55
- Modify 0015-RH-fix-output-buffer.patch
  * Fix memory leak
- Add 0047-RHBZ-kpartx-read-only-loop-devs.patch
  * Fix read only loop device handling
- Add 0048-RH-print-defaults.patch
- Add 0049-RH-remove-ID_FS_TYPE.patch
  * remove ID_FS_TYPE udev enviroment variable for multipath devices
- Add 0051-UP-fix-cli-resize.patch
  * check before dereferencing variables
- Add 0052-RH-fix-bad-derefs.patch
  * setup multipath free the multipath device when it fails, so don't keep
    using it.
- Add 0053-UP-fix-failback.patch
  * setting failback in the devices section was broken
- Add 0054-UP-keep-udev-ref.patch
  * multipathd needs to keep the same udev object across reconfigures
- Add 0055-UP-handle-quiesced-paths.patch
  * quiesced paths should be treated as down
- Add 0056-UP-alua-prio-fix.patch
  * Don't count the preferred bit for paths that are active/optimized
- Add 0057-UP-fix-tmo.patch
  * Cleanup how multipath sets dev_loss_tmo and fast_io_fail_tmo.  Also
    make multipath get changing values directly from sysfs, instead of
    from udev, which caches them.
- Add 0058-UP-fix-failback.patch
  * make failback print the default value when you show configs.
- Add 0059-UP-flush-failure-queueing.patch
  * If you can't flush a multipath device, restore the queue_if_no_paths
    value
- Add 0060-UP-uevent-loop-udev.patch
  * make ueventloop grab it's own udev reference, since it is cancelled
    asychnrously.

* Fri Jul  5 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-54
- Add 0047-RHBZ-980777-kpartx-read-only-loop-devs.patch
  * make kpartx support read-only files better
- Resolves: bz #980777

* Wed Jul  3 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-53
- Add 0044-RHBZ-976688-fix-wipe-wwids.patch
  * Seek back to the start of the file after truncating it
- Add 0045-RHBZ-977297-man-page-fix.patch
  * update man page to match actual defaults
- Add 0046-RHBZ-883981-move-udev-rules.patch
  * move udev rules file from /lib to /usr/lib
- Resolves: bz #883981, #976688, #977297

* Fri Jun 21 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-52
- Add 0038-RHBZ-799860-netapp-config.patch
- Add 0039-RH-detect-prio-fix.patch
  * Don't autodetect ALUA prioritizer unless it actually can get a priority
- Add 0040-RH-bindings-fix.patch
  * Do a better job of trying to get the first free user_friendly_name
- Add 0041-RH-check-for-erofs.patch
  * Don't create/reload a device read-only unless doing it read/write fails
    with EROFS
- Remove 0017-RH-fix-sigusr1.patch
  * fix signal handling upstream way instead
- Add 0042-UP-fix-signal-handling.patch
  * uxlsnr now handles all the signals sent to multipathd. This makes its
    signal handling posix compliant, and harder to mess up.
- Add 0043-RH-signal-waiter.patch
  * ioctl isn't a pthread cancellation point.  Send a signal to the waiter
    thread to break out of waiting in ioctl for a dm event.

* Fri May 17 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-51
- Add 0032-RHBZ-956464-mpathconf-defaults.patch
  * fix defaults listed in usage
- Add 0033-RHBZ-829963-e-series-conf.patch
- Add 0034-RHBZ-851416-mpathconf-display.patch
  * display whether or not multipathd is running in the status
- Add 0035-RHBZ-891921-list-mpp.patch
  * add a new path format wilcard to list the multipath device associated
    with a path
- Add 0036-RHBZ-949239-load-multipath-module.patch
  * load the dm-multipath kernel module when multipathd starts
- Add 0037-RHBZ-768873-fix-rename.patch
  * When deciding on a multipth devices name on reload, don't default to
    the existing name if there is no config file alias and user_friendly_names
    isn't set. Use the wwid.
- Modify multipath.conf
- Resolves: bz #768873, #950252

* Tue Apr 30 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-50
- Add 0031-RHBZ-957188-kpartx-use-dm-name.patch
  * use the basename of the devices that will be created to choose the
    delimiter instead of using the device name from the command line
- Resolves: bz #957188

* Fri Apr 26 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-49
- Modify 0020-RHBZ-907360-static-pthread-init.patch
  * Don't initialize uevent list twice
- Add 0029-RH-no-prio-put-msg.patch
- Add 0030-RHBZ-916528-override-queue-no-daemon.patch
  * Default to "queue_without_daemon no"
  * Add "forcequeueing daemon" and "restorequeueing daemon" cli commands
- Modify spec file to force queue_without_daemon when restarting
  multipathd on upgrades.

* Thu Apr  4 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-48
- Add 0026-fix-checker-time.patch
  * Once multipathd hit it max checker interval, it was reverting to
    to shortest checker interval
- Add 0027-RH-get-wwid.patch
  * Multipath wasn't correctly setting the multipath wwid when it read devices
    in from the kernel
- Add 0028-RHBZ-929078-refresh-udev-dev.patch
  * Make multipath try to get the UID of down devices.  Also, on ev_add_path,
    make multipathd reinitialize existing devices that weren't fully
    initialized before.

* Mon Apr  1 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-47
- Add 0021-RHBZ-919119-respect-kernel-cmdline.patch
  * keep the multipath.rules udev file from running and multipathd from
    starting if nompath is on the kernel command line
- Add 0022-RH-multipathd-check-wwids.patch
  * Whenever multipath runs configure, it will check the wwids, and
    add any missing ones to the wwids file
- Add 0023-RH-multipath-wipe-wwid.patch
  * multipath's -w command will remove a wwid from the wwids file
- Add 0024-RH-multipath-wipe-wwids.patch
  * multipath's -W command will set reset the wwids file to just the current
    devices
- Add 0025-UPBZ-916668_add_maj_min.patch
- Resolves: bz #919119

* Thu Mar 28 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-46
- Add 0020-RHBZ-907360-static-pthread-init.patch
  * statically initialize the uevent pthread structures 

* Sat Mar  2 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-45
- Updated to latest upstrem 0.4.9 code: multipath-tools-130222
  (git commit id: 67b82ad6fe280caa1770025a6bb8110b633fa136)
- Refresh 0001-RH-dont_start_with_no_config.patch
- Modify 0002-RH-multipath.rules.patch
- Modify 0003-RH-Make-build-system-RH-Fedora-friendly.patch
- Refresh 0004-RH-multipathd-blacklist-all-by-default.patch
- Refresh 0005-RH-add-mpathconf.patch
- Refresh 0006-RH-add-find-multipaths.patch
- Add 0008-RH-revert-partition-changes.patch
- Rename 0008-RH-RHEL5-style-partitions.patch to
	 0009-RH-RHEL5-style-partitions.patch
- Rename 0009-RH-dont-remove-map-on-enomem.patch to
	 0010-RH-dont-remove-map-on-enomem.patch
- Rename 0010-RH-deprecate-uid-gid-mode.patch to
	 0011-RH-deprecate-uid-gid-mode.patch
- Rename 0013-RH-kpartx-msg.patch to 0012-RH-kpartx-msg.patch
- Rename 0035-RHBZ-883981-cleanup-rpmdiff-issues.patch to
         0013-RHBZ-883981-cleanup-rpmdiff-issues.patch
- Rename 0039-RH-handle-other-sector-sizes.patch to
	 0014-RH-handle-other-sector-sizes.patch
- Rename 0040-RH-fix-output-buffer.patch to 0015-RH-fix-output-buffer.patch
- Add 0016-RH-dont-print-ghost-messages.patch
- Add 0017-RH-fix-sigusr1.patch
  * Actually this fixes a number of issues related to signals
- Rename 0018-RH-remove-config-dups.patch to 0018-RH-fix-factorize.patch
  * just the part that isn't upstream
- Add 0019-RH-fix-sockets.patch
  * makes abstract multipathd a cli sockets use the correct name.
- Set find_multipaths in the default config

* Wed Feb 20 2013 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-44
- Add 0036-UP-fix-state-handling.patch
  * handle transport-offline and quiesce sysfs state
- Add 0037-UP-fix-params-size.patch
- Add 0038-RH-fix-multipath.rules.patch
  * make sure multipath's link priority gets increased
- Add 0039-RH-handle-other-sector-sizes.patch
  * allow gpt partitions on 4k sector size block devices.
- Add 0040-RH-fix-output-buffer.patch
  * fix multipath -ll for large configuration.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Benjamin Marzinski <bmarizns@redhat.com> 0.4.9-42
- Add 0034-RHBZ-887737-check-for-null-key.patch
- Add 0035-RHBZ-883981-cleanup-rpmdiff-issues.patch
  * Compile multipathd with full RELRO and PIE and install to /usr

* Mon Dec 17 2012 Benjamin Marzinski <bmarizns@redhat.com> 0.4.9-41
- Add 0033-RH-dont-disable-libdm-failback-for-sync-case.patch
  * make kpartx -s and multipath use libdm failback device creation, so
    that they work in environments without udev

* Fri Nov 30 2012 Benjamin Marzinski <bmarizns@redhat.com> 0.4.9-40
- Add 0032-RH-make-path-fd-readonly.patch
  * revert change made when adding persistent reservations, so that path fds
    are again opened O_RDONLY

* Fri Nov 30 2012 Benjamin Marzinski <bmarizns@redhat.com> 0.4.9-39
- Add 0031-RHBZ-882060-fix-null-strncmp.patch

* Fri Nov 30 2012 Benjamin Marzinski <bmarizns@redhat.com> 0.4.9-38
- Add 0026-RH-fix-mpathpersist-fns.patch
- Add 0027-RH-default-partition-delimiters.patch
  * Only use the -p delimiter when the device name ends in a number
- Add 0028-RH-storagetek-config.patch
- Add 0029-RH-kpartx-retry.patch
  * retry delete on busy loop devices
- Add 0030-RH-early-blacklist.patch
  * multipath will now blacklist devices by device type and wwid in
    store_pathinfo, so that it doesn't do a bunch of unnecessary work
    on paths that it would only be removing later on.

* Sat Nov 03 2012 Peter Rajnoha <prajnoha@redhat.com> 0.4.9-37
- Install multipathd.service for sysinit.target instead of multi-user.target.

* Thu Nov 01 2012 Peter Rajnoha <prajnoha@redhat.com> 0.4.9-36
- Start multipathd.service systemd unit before LVM units.

* Wed Oct 24 2012 Benjamin Marzinski <bmarizns@redhat.com> 0.4.9-35
- Add 0022-RHBZ-864368-disable-libdm-failback.patch
  * make kpartx and multiapthd disable libdm failback device creation
- Add 0023-RHBZ-866291-update-documentation.patch
- Resolves: bz #864368, #866291

* Tue Oct 23 2012 Benjamin Marzinski <bmarizns@redhat.com> 0.4.9-34
- Add 0021-RH-fix-oom-adj.patch
  * don't use OOM_ADJUST_MIN unless you're sure it's defined

* Tue Oct 23 2012 Benjamin Marzinski <bmarizns@redhat.com> 0.4.9-33
- Modify 0016-RH-retain_hwhandler.patch
  * Check the dm-multipath module version, and don't enable
    retain_attached_hw_handler if the kernel doesn't support it
- Add 0019-RH-detect-prio.patch
  * add detect_prio option, to make multipath check if the device
    supports the ALUA prio, before defaulting to the configured prio
- Remove 0017-RH-netapp_config.patch
- Add 0020-RH-netapp-config.patch
  * new netapp config that uses retain_attached_hw_handler and
    detect_prio to autoconfigure ALUA and non-ALUA devices.

* Tue Oct  2 2012 Benjamin Marzinski <bmarizns@redhat.com> 0.4.9-32
- Modified 0018-RH-remove-config-dups.patch
  * Made modified config remove original only if the vendor/product
    exactly match

* Thu Sep 27 2012 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-31
- Add 0014-RH-dm_reassign.patch
  * Fix reassign_maps option
- Add 0015-RH-selector_change.patch
  * devices default to using service-time selector
- Add 0016-RH-retain_hwhandler.patch
  * add retain_attached_hw_handler option, to let multipath keep an
    already attached scsi device handler
- Add 0017-RH-netapp_config.patch
- Add 0018-RH-remove-config-dups.patch
  * Clean up duplicates in the devices and blacklist sections

* Wed Sep 05 2012 Václav Pavlín <vpavlin@redhat.com> - 0.4.9-30
- Scriptlets replaced with new systemd macros (#850088)

* Tue Aug 21 2012 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-29
- Updated to latest upstrem 0.4.9 code: multipath-tools-120821.tgz
  (git commit id: 050b24b33d3c60e29f7820d2fb75e84a9edde528)
  * includes 0001-RH-remove_callout.patch, 0002-RH-add-wwids-file.patch,
    0003-RH-add-followover.patch, 0004-RH-fix-cciss-names.patch
- Add 0013-RH-kpartx-msg.patch
- Modify 0002-RH-multipath.rules.patch
  * removed socket call from rules file

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-27
- Updated to latest upstream 0.4.9 code : multipath-tools-120613.tgz
  (git commit id: cb0f7127ba90ab5e8e71fc534a0a16cdbe96a88f)
- Add 0001-RH-remove_callout.patch
  * multipath no longer uses the getuid callout.  It now gets the
    wwid from the udev database or the environment variables
- Add 0004-RH-fix-cciss-names.patch
  * convert cciss device names from cciss/cXdY to sysfs style cciss!cXdY
- Split 0009-RH-add-find-multipaths.patch into 0002-RH-add-wwids-file.patch
        and 0010-RH-add-find-multipaths.patch
- Add 0016-RH-change-configs.patch
  * default fast_io_fail to 5 and don't set the path selector in the
    builtin configs.
Resolves: bz #831978


* Thu May 17 2012 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-26
- Add 0025-RHBZ-822714-update-nodes.patch
- Resolves: bz #822714

* Mon Apr 30 2012 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-25
- Modify 0024-RH-libudev-monitor.patch
- Resolves: bz #805493

* Mon Apr 30 2012 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-24
- Add requirements on libudev to spec file
- Resolves: bz #805493

* Mon Apr 30 2012 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-23
- Add 0024-RH-libudev-monitor.patch

* Fri Feb 10 2012 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-22
- Add 0012-RH-update-on-show-topology.patch
- Add 0013-RH-manpage-update.patch
- Add 0014-RH-RHEL5-style-partitions.patch
- Add 0015-RH-add-followover.patch
- Add 0016-RH-dont-remove-map-on-enomem.patch
- Add 0017-RH-fix-shutdown-crash.patch
- Add 0018-RH-warn-on-bad-dev-loss-tmo.patch
- Add 0019-RH-deprecate-uid-gid-mode.patch
- Add 0020-RH-dont-remove-map-twice.patch
- Add 0021-RH-validate-guid-partitions.patch
- Add 0022-RH-adjust-messages.patch
- Add 0023-RH-manpage-update.patch

* Tue Jan 24 2012 Benjamin Marzinski <bmarzins@redhat.com> 0.4.9-21
- Updated to latest upstream 0.4.9 code : multipath-tools-120123.tgz
  (git commit id: 63704387009443bdb37d9deaaafa9ab121d45bfb)
- Add 0001-RH-fix-async-tur.patch
- Add 0002-RH-dont_start_with_no_config.patch
- Add 0003-RH-multipath.rules.patch
- Add 0004-RH-update-init-script.patch
- Add 0005-RH-cciss_id.patch
- Add 0006-RH-Make-build-system-RH-Fedora-friendly.patch
- Add 0007-RH-multipathd-blacklist-all-by-default.patch
- Add 0008-RH-add-mpathconf.patch
- Add 0009-RH-add-find-multipaths.patch
- Add 0010-RH-check-if-multipath-owns-path.patch
- Add 0011-RH-add-hp_tur-checker.patch

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 20 2011 Benjamin Marzinski <bmarzins@redhat.com> -0.4.9-19
- Modify 0103-add-disable-sync-option.patch
- Add 0104-RHBZ-737989-systemd-unit-fix.patch
  * systemd will only start multipathd if /etc/multipath.conf exists
- Add 0105-fix-oom-adj.patch
  * first try setting oom_score_adj

* Mon Aug 15 2011 Kalev Lember <kalevlember@gmail.com> - 0.4.9-18
- Rebuilt for rpm bug #728707

* Tue Jul 19 2011 Benjamin Marzinski <bmarzins@redhat.com> -0.4.9-17
- Add 0103-add-disable-sync-option.patch
  * add a -n (nosync) option to multipath. This disables synchronous
    file creation with udev. 

* Fri Jul 15 2011 Benjamin Marzinski <bmarzins@redhat.com> -0.4.9-16
- Modify 0012-RH-udev-sync-support.patch
- Modify 0021-RHBZ-548874-add-find-multipaths.patch
- Modify 0022-RHBZ-557845-RHEL5-style-partitions.patch
- Add 0025-RHBZ-508827-update-multipathd-manpage.patch through
      0101-RHBZ-631009-disable-udev-disk-rules-on-reload.patch
  * sync with current state of RHEL6. Next release should include a updated
    source tarball with most of these fixes rolled in.
- Add 0102-RHBZ-690828-systemd-unit-file.patch
  * Add Jóhann B. Guðmundsson's unit file for systemd.
  * Add sub-package sysvinit for SysV init script.
- Resolves: bz #690828

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 16 2010 Benjamin Marzinski <bmarzins@redhat.com> -0.4.9-14
- Modify 0021-RHBZ-548874-add-find-multipaths.patch
  * fix bug where mpathconf wouldn't create a multpath.conf file unless one
    already existed.

* Tue Feb 16 2010 Benjamin Marzinski <bmarzins@redhat.com> -0.4.9-13
- Replace 0012-RH-explicitly-disable-dm-udev-sync-support-in-kpartx.patch
  with 0012-RH-udev-sync-support.patch
  * Add udev sync support to kpartx and multipath. In kpartx it is disabled
    unless you use the -s option.
- Refresh 0013-RH-add-weighted_prio-prioritizer.patch
- Refresh 0021-RHBZ-548874-add-find-multipaths.patch
- Modify 0022-RHBZ-557845-RHEL5-style-partitions.patch
  * kpartx now creates a 2 sector large device for dos extended
    partitions, just like the kernel does on the regular block devices.
- Add 0023-RHBZ-557810-emc-invista-config.patch
- Add 0024-RHBZ-565933-checker-timeout.patch
  * Multipath has a new option checker_timeout. If this is not set, 
    all path checker functions with explicit timeouts use
    /sys/block/sd<x>/device/timeout. If this is set, they use it instead.

* Fri Jan 22 2010 Benjamin Marzinski <bmarzins@redhat.com> -0.4.9-12
- Refresh 0001-RH-queue-without-daemon.patch
- Refresh 0002-RH-path-checker.patch
- Modify 0010-RH-multipath-rules-udev-changes.patch
  * Fix udev rules to use DM_SBIN_PATH when calling kpartx
  * install udev rules to /lib/udev/rules.d instead of /etc/udev/rules.d
- Modify 0014-RH-add-hp_tur-checker.patch
- Add 0003-for-upstream-default-configs.patch
- Add 0016-RHBZ-554561-fix-init-error-msg.patch
- Add 0017-RHBZ-554592-man-page-note.patch
- Add 0018-RHBZ-554596-SUN-6540-config.patch
- Add 0019-RHBZ-554598-fix-multipath-locking.patch
- Add 0020-RHBZ-554605-fix-manual-failover.patch
- Add 0021-RHBZ-548874-add-find-multipaths.patch
  * Added find_multipaths multipath.conf option
  * Added /sbin/mpathconf for simple editting of multipath.conf
- Add 0022-RHBZ-557845-RHEL5-style-partitions.patch
  * Make kpartx deal with logical partitions like it did in RHEL5.
    Don't create a dm-device for the extended partition itself.
    Create the logical partitions on top of the dm-device for the whole disk.

* Mon Nov 16 2009 Benjamin Marzinski <bmarzins@redhat.com> -0.4.9-11
- Add 0002-for-upstream-add-tmo-config-options.patch
  * Add fail_io_fail_tmo and dev_loss_tmo multipath.conf options
- Add 0013-RH-add-weighted_prio-prioritizer.patch
- Add 0014-RH-add-hp_tur-checker.patch
- Add 0015-RH-add-multipathd-count-paths-cmd.patch
- rename multipath.conf.redhat to multipath.conf, and remove the default
  blacklist.

* Tue Oct 27 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.4.9-10
- Updated to latest upstream 0.4.9 code : multipath-tools-091027.tar.gz
  (git commit id: a946bd4e2a529e5fba9c9547d03d3f91806618a3)
- Drop unrequired for-upstream patches.
- BuildRequires and Requires new device-mapper version for udev sync support.

* Tue Oct 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.4.9-9
- 0012-RH-explicitly-disable-dm-udev-sync-support-in-kpartx.patch

* Mon Oct 19 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.4.9-8
- Split patches in "for-upstream" and "RH" series.
- Replace 0011-RH-multipathd-blacklist-all-by-default.patch with
  version from Benjamin Marzinski.
- Update udev rules 0010-RH-multipath-rules-udev-changes.patch.
- rpmlint cleanup:
  * Drop useless-provides kpartx.
  * Cleanup tab vs spaces usage.
  * Summary not capitalized.
  * Missing docs in libs package.
  * Fix init script LSB headers.
- Drop README* files from doc sections (they are empty).

* Thu Oct 15 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.4.9-7
- Add patch 0010-RH-Set-friendly-defaults.patch:
  * set rcdir to fedora default.
  * do not install kpartx udev bits.
  * install redhat init script.
  * Cleanup spec file install target.
- Add patch 0011-RH-multipathd-blacklist-all-by-default.patch:
  * Fix BZ#528059
  * Stop installing default config in /etc and move it to the doc dir.

* Tue Oct 13 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.4.9-6
- Updated to latest upstream 0.4.9 code : multipath-tools-091013.tar.gz
  (git commit id: aa0a885e1f19359c41b63151bfcface38ccca176)
- Drop, now upstream, patches:
  * fix_missed_uevs.patch.
  * log_all_messages.patch.
  * uninstall.patch.
  * select_lib.patch.
  * directio_message_cleanup.patch.
  * stop_warnings.patch.
- Drop redhatification.patch in favour of spec file hacks.
- Drop mpath_wait.patch: no longer required.
- Merge multipath_rules.patch and udev_change.patch.
- Rename all patches based on source.
- Add patch 0009-RH-fix-hp-sw-hardware-table-entries.patch to fix
  default entry for hp_sw and match current kernel.
- Add multipath.conf.redhat as source instead of patch.
- spec file:
  * divide runtime and build/setup bits.
  * update BuildRoot.
  * update install section to apply all the little hacks here and there,
    in favour of patches against upstream.
  * move ldconfig invokation to libs package where it belong.
  * fix libs package directory ownership and files.

* Thu Aug 20 2009 Benjamin Marzinski <bmarzins@redhat.com> - 0.4.9-5
- Fixed problem where maps were being added and then removed.
- Changed the udev rules to fix some issues.

* Thu Jul 30 2009 Benjamin Marzinski <bmarzins@redhat.com> - 0.4.9-4
- Fixed build issue on i686 machines.

* Wed Jul 29 2009 Benjamin Marzinski <bmarzins@redhat.com> - 0.4.9-3
- Updated to latest upstream 0.4.9 code : multipath-tools-090729.tgz
  (git commit id: d678c139719d5631194b50e49f16ca97162ecd0f)
- moved multipath bindings file from /var/lib/multipath to /etc/multipath
- Fixed 354961, 432520

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 6 2009 Mike Snitzer <snitzer@redhat.com> - 0.4.9-1
- Updated to latest upstream 0.4.9 code: multipath-tools-090429.tgz
  (git commit id: 7395bcda3a218df2eab1617df54628af0dc3456e)
- split the multipath libs out to a device-mapper-multipath-libs package
- if appropriate, install multipath libs in /lib64 and /lib64/multipath

* Tue Apr 7 2009 Milan Broz <mbroz@redhat.com> - 0.4.8-10
- Fix insecure permissions on multipathd.sock (CVE-2009-0115)

* Fri Mar 6 2009 Milan Broz <mbroz@redhat.com> - 0.4.8-9
- Fix kpartx extended partition handling (475283)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 26 2008 Benjamin Marzinski <bmarzins@redhat.com> 0.4.8-7
- Since libaio is now in /lib, not /usr/lib, multipath no longer needs to
  statically link against it. Fixed an error with binding file and WWIDs
  that include spaces. Cleaned up the messages from the directio checker
  function.  Fixed the udev rules. Fixed a regression in multipath.conf
  parsing
- Fixed 457530, 457589

* Wed Aug 20 2008 Benjamin Marzinski <bmarzins@redhat.com> 0.4.8-6
- Updated to latest upstream 0.4.8 code: multipath-tools-080804.tgz
  (git commit id: eb87cbd0df8adf61d1c74c025f7326d833350f78)
- fixed 451817, 456397 (scsi_id_change.patch), 457530 (config_space_fix.patch)
  457589 (static_libaio.patch)

* Fri Jun 13 2008 Alasdair Kergon <agk@redhat.com> - 0.4.8-5
- Rebuild (rogue vendor tag). (451292)

* Mon May 19 2008 Benjamin Marzinksi <bmarzins@redhat.com> 0.4.8-4
- Fixed Makefile issues.

* Mon May 19 2008 Benjamin Marzinksi <bmarzins@redhat.com> 0.4.8-3
- Fixed ownership build error.

* Mon May 19 2008 Benjamin Marzinksi <bmarzins@redhat.com> 0.4.8-2
- Forgot to commit some patches.

* Mon May 19 2008 Benjamin Marzinski <bmarzins@redhat.com> 0.4.8-1
- Updated to latest Upstream 0.4.8 code: multipath-tools-080519.tgz
  (git commit id: 42704728855376d2f7da2de1967d7bc71bc54a2f)

* Tue May 06 2008 Alasdair Kergon <agk@redhat.com> - 0.4.7-15
- Remove unnecessary multipath & kpartx static binaries. (bz 234928)

* Fri Feb 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.4.7-14
- fix sparc64
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.7-13
- Autorebuild for GCC 4.3

* Wed Nov 14 2007 Benjamin Marzinski <bmarzins@redhat.com> - 0.4.7-12
- Fixed the dist tag so building will work properly.

* Mon Feb 05 2007 Alasdair Kergon <agk@redhat.com> - 0.4.7-11.fc7
- Add build dependency on new device-mapper-devel package.
- Add dependency on device-mapper.

* Wed Jan 31 2007 Benjamin Marzinksi <bmarzins@redhat.com> - 0.4.7-10.fc7
- Update BuildRoot and PreReq lines.

* Mon Jan 15 2007 Benjamin Marzinksi <bmarzins@redhat.com> - 0.4.7-9.fc7
- Fixed spec file.

* Mon Jan 15 2007 Benjamin Marzinski <bmarzins@redhat.com> - 0.4.7-8.fc7
- Update to latest code (t0_4_7_head2)

* Wed Dec 13 2006 Benjamin Marzinski <bmarzins@redhat.com> - 0.4.7-7.fc7
- Update to latest code (t0_4_7_head1)

* Thu Sep  7 2006 Peter Jones <pjones@redhat.com> - 0.4.7-5
- Fix kpartx to handle with drives >2TB correctly.

* Thu Aug 31 2006 Peter Jones <pjones@redhat.com> - 0.4.7-4.1
- Split kpartx out into its own package so dmraid can use it without
  installing multipathd
- Fix a segfault in kpartx

* Mon Jul 17 2006 Benjamin Marzinski <bmarzins@redhat.com> 0.4.7-4.0
- Updated to latest source. Fixes bug in default multipath.conf

* Wed Jul 12 2006 Benjamin Marzinski <bmarzins@redhat.com> 0.4.7-3.1
- Added ncurses-devel to BuildRequires

* Wed Jul 12 2006 Benjamin Marzinski <bmarzins@redhat.com> 0.4.7-3.0
- Updated to latest source. deals with change in libsysfs API

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.4.7-2.2.1
- rebuild

* Mon Jul 10 2006 Benjamin Marzinski <bmarzins@redhat.com> 0.4.7-2.2
- fix tagging issue.

* Mon Jul 10 2006 Benjamin Marzinski <bmarzins@redhat.com> 0.4.7-2.1
- changed BuildRequires from sysfsutils-devel to libsysfs-devel

* Wed Jun 28 2006 Benjamin Marzinski <bmarzins@redhat.com> 0.4.7-2.0
- Updated to latest upstream source, fixes kpartx udev rule issue

* Tue Jun 06 2006 Benjamin Marzinski <bmarzins@redhat.com> 0.4.7-1.0
- Updated to Christophe's latest source

* Mon May 22 2006 Alasdair Kergon <agk@redhat.com> - 0.4.5-16.0
- Newer upstream source (t0_4_5_post59).

* Mon May 22 2006 Alasdair Kergon <agk@redhat.com> - 0.4.5-12.3
- BuildRequires: libsepol-devel, readline-devel

* Mon Feb 27 2006 Benjamin Marzinski <bmarzins@redhat.com> 0.4.5-12.2
- Prereq: chkconfig

* Mon Feb 20 2006 Karsten Hopp <karsten@redhat.de> 0.4.5-12.1
- BuildRequires: libselinux-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.4.5-12.0.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Benjamin Marzinski <bmarzins@redhat.com> -0.4.5-12.0
- Updated to latest upstream source (t0_4_5_post56)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.4.5-9.1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 19 2005 Benjamin Marzinski <bmarzins@redhat.com> - 0.4.5-9.1
- added patch for fedora changes

* Fri Dec 16 2005 Benjamin Marzinski <bmarzins@redhat.com> - 0.4.5-9.0
- Updated to latest upstream source (t)_4_5_post52)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Dec  4 2005 Peter Jones <pjones@redhat.com> - 0.4.4-2.6
- rebuild for newer libs

* Tue Nov 15 2005 Peter Jones <pjones@redhat.com> - 0.4.4-2.5
- unsplit kpartx.  parted knows how to do this now, so we don't
  need this in a separate package.

* Tue Nov 15 2005 Peter Jones <pjones@redhat.com> - 0.4.4-2.4
- split kpartx out into its own package

* Fri May 06 2005 Bill Nottingham <notting@redhat.com> - 0.4.4-2.3
- Fix last fix.

* Thu May 05 2005 Alasdair Kergon <agk@redhat.com> - 0.4.4-2.2
- Fix last fix.

* Wed May 04 2005 Alasdair Kergon <agk@redhat.com> - 0.4.4-2.1
- By default, disable the multipathd service.

* Tue Apr 19 2005 Alasdair Kergon <agk@redhat.com> - 0.4.4-2.0
- Fix core dump from last build.

* Tue Apr 19 2005 Alasdair Kergon <agk@redhat.com> - 0.4.4-1.0
- Move cache file into /var/cache/multipath.

* Fri Apr 08 2005 Alasdair Kergon <agk@redhat.com> - 0.4.4-0.pre8.1
- Remove pp_balance_units.

* Mon Apr 04 2005 Alasdair Kergon <agk@redhat.com> - 0.4.4-0.pre8.0
- Incorporate numerous upstream fixes.
- Update init script to distribution standards.

* Tue Mar 01 2005 Alasdair Kergon <agk@redhat.com> - 0.4.2-1.0
- Initial import based on Christophe Varoqui's spec file.
