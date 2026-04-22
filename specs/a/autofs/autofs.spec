# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# $Id: autofs.spec,v 1.11 2003/12/04 15:41:32 raven Exp $
#
# Use --without systemd in your rpmbuild command or force values to 0 to
# disable them.
%bcond systemd 1

# Use --without fedfs in your rpmbuild command or force values to 0 to
# disable them.
%bcond fedfs 1

# RHEL 10+ does not include NIS support
%bcond nis %{undefined rhel}

Summary: A tool for automatically mounting and unmounting filesystems
Name: autofs
Version: 5.1.9
Release: 11%{?dist}
Epoch: 1
License: GPL-2.0-or-later
Source: https://www.kernel.org/pub/linux/daemons/autofs/v5/autofs-%{version}.tar.gz
Patch1: autofs-5.1.9-update-configure.patch
Patch2: autofs-5.1.9-fix-ldap_parse_page_control-check.patch
Patch3: autofs-5.1.9-fix-crash-in-make_options_string.patch
Patch4: autofs-5.1.9-Fix-incompatible-function-pointer-types-in-cyrus-sasl-module.patch
Patch5: autofs-5.1.9-fix-always-recreate-credential-cache.patch
Patch6: autofs-5.1.9-fix-changelog.patch

%if %{with systemd}
BuildRequires: systemd-units
BuildRequires: systemd-devel
%endif
BuildRequires: gcc
BuildRequires: autoconf, openldap-devel, bison, flex, libxml2-devel
BuildRequires: cyrus-sasl-devel, openssl-devel module-init-tools util-linux
BuildRequires: e2fsprogs libtirpc-devel libsss_autofs
%if %{with nis}
BuildRequires: libnsl2-devel
%endif
BuildRequires: pkgconfig krb5-devel
BuildRequires: make
Conflicts: cyrus-sasl-lib < 2.1.23-9
Requires: bash coreutils sed gawk grep module-init-tools /bin/ps
%if %{with systemd}
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%else
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service
Requires(postun): /sbin/chkconfig
%endif
Summary(de): autofs daemon 
Summary(fr): démon autofs
Summary(tr): autofs sunucu süreci
Summary(sv): autofs-daemon

%description
autofs is a daemon which automatically mounts filesystems when you use
them, and unmounts them later when you are not using them.  This can
include network filesystems, CD-ROMs, floppies, and so forth.

%description -l de
autofs ist ein Dämon, der Dateisysteme automatisch montiert, wenn sie 
benutzt werden, und sie später bei Nichtbenutzung wieder demontiert. 
Dies kann Netz-Dateisysteme, CD-ROMs, Disketten und ähnliches einschließen. 

%description -l fr
autofs est un démon qui monte automatiquement les systèmes de fichiers
lorsqu'on les utilise et les démonte lorsqu'on ne les utilise plus. Cela
inclus les systèmes de fichiers réseau, les CD-ROMs, les disquettes, etc.

%description -l tr
autofs, kullanýlan dosya sistemlerini gerek olunca kendiliðinden baðlar
ve kullanýmlarý sona erince yine kendiliðinden çözer. Bu iþlem, að dosya
sistemleri, CD-ROM'lar ve disketler üzerinde yapýlabilir.

%description -l sv
autofs är en daemon som mountar filsystem när de använda, och senare
unmountar dem när de har varit oanvända en bestämd tid.  Detta kan
inkludera nätfilsystem, CD-ROM, floppydiskar, och så vidare.

%prep
%autosetup -p1 -n %{name}-%{version}
echo %{version}-%{release} > .version
%if %{with systemd}
  %define unitdir %{?_unitdir:/usr/lib/systemd/system}
  %define systemd_configure_arg --with-systemd
%endif
%if %{with fedfs}
  %define fedfs_configure_arg --enable-fedfs
%endif

%build
autoreconf -iv
LDFLAGS=-Wl,-z,now
%configure \
	--disable-mount-locking \
	--enable-ignore-busy \
	--enable-force-shutdown \
	--without-hesiod \
	--with-libtirpc \
	%{?systemd_configure_arg:} \
	%{?fedfs_configure_arg:}

make initdir=%{_initrddir} DONTSTRIP=1

%install
%if %{with systemd}
install -d -m 755 $RPM_BUILD_ROOT%{unitdir}
%else
mkdir -p -m755 $RPM_BUILD_ROOT%{_initrddir}
%endif
mkdir -p -m755 $RPM_BUILD_ROOT%{_sbindir}
mkdir -p -m755 $RPM_BUILD_ROOT%{_libdir}/autofs
mkdir -p -m755 $RPM_BUILD_ROOT%{_mandir}/{man5,man8}
mkdir -p -m755 $RPM_BUILD_ROOT/etc/sysconfig
mkdir -p -m755 $RPM_BUILD_ROOT/etc/auto.master.d

make install mandir=%{_mandir} initdir=%{_initrddir} systemddir=%{unitdir} INSTALLROOT=$RPM_BUILD_ROOT
echo make -C redhat
make -C redhat
install -m 755 -d $RPM_BUILD_ROOT/misc
%if %{with systemd}
# Configure can get this wrong when the unit files appear under /lib and /usr/lib
find $RPM_BUILD_ROOT -type f -name autofs.service -exec rm -f {} \;
install -m 644 redhat/autofs.service $RPM_BUILD_ROOT%{unitdir}/autofs.service
%define init_file_name %{unitdir}/autofs.service
%else
install -m 755 redhat/autofs.init $RPM_BUILD_ROOT%{_initrddir}/autofs
%define init_file_name /etc/rc.d/init.d/autofs
%endif
install -m 644 redhat/autofs.conf $RPM_BUILD_ROOT/etc/autofs.conf
install -m 644 redhat/autofs.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/autofs

install -m 644 samples/auto.master $RPM_BUILD_ROOT/etc/auto.master
install -m 644 samples/auto.misc $RPM_BUILD_ROOT/etc/auto.misc
install -m 755 samples/auto.net $RPM_BUILD_ROOT/etc/auto.net
install -m 755 samples/auto.smb $RPM_BUILD_ROOT/etc/auto.smb
install -m 600 samples/autofs_ldap_auth.conf $RPM_BUILD_ROOT/etc/autofs_ldap_auth.conf

%post
%if %{with systemd}
%systemd_post %{name}.service
%else
if [ $1 -eq 1 ]; then
	%{_sbindir}/sbin/chkconfig --add autofs
fi
%endif

%preun
%if %{with systemd}
%systemd_preun %{name}.service
%else
if [ $1 -eq 0 ] ; then
    %{_sbindir}/service autofs stop > /dev/null 2>&1 || :
    %{_sbindir}/chkconfig --del autofs
fi
%endif

%postun
%if %{with systemd}
%systemd_postun_with_restart %{name}.service
%else
if [ $1 -ge 1 ] ; then
    %{_sbindir}/sbin/service autofs condrestart > /dev/null 2>&1 || :
fi
%endif

%triggerun -- %{name} < 5.0.6-5
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply %{name}
# to migrate them to systemd targets
%{_bindir}/systemd-sysv-convert --save %{name} >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
%{_sbindir}/chkconfig --del %{name} >/dev/null 2>&1 || :
%{_bindir}/systemctl try-restart %{name}.service >/dev/null 2>&1 || :

%files
%doc CREDITS INSTALL COPY* README* samples/ldap* samples/autofs.schema
%config %{init_file_name}
%config(noreplace,missingok) /etc/auto.master
%config(noreplace) /etc/autofs.conf
%config(noreplace,missingok) /etc/auto.misc
%config(noreplace,missingok) /etc/auto.net
%config(noreplace,missingok) /etc/auto.smb
%config(noreplace) /etc/sysconfig/autofs
%config(noreplace) /etc/autofs_ldap_auth.conf
%{_sbindir}/automount
%if %{with fedfs}
%{_sbindir}/mount.fedfs
%{_sbindir}/fedfs-map-nfs4
%endif
%{_libdir}/libautofs.so
%{_libdir}/autofs/
%{_mandir}/*/*
%dir /etc/auto.master.d

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 23 2024 Ian Kent <ikent@redhat.com> - 1:5.1.9-7
- Update configure script.
- fix ldap_parse_page_control() check.
- fix crash in make_options_string().
- Fix incompatible function pointer types in cyrus-sasl module.
- fix always recreate credential cache.
- update changelog.

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Florian Weimer <fweimer@redhat.com> - 1:5.1.9-4
- Further C compatibility fixes, run autoconf

* Tue Nov 07 2023 Ian Kent <ikent@redhat.com> - 1:5.1.9-3
- Also update package revision.

* Tue Nov 07 2023 Ian Kent <ikent@redhat.com> - 1:5.1.9-2
- correct changelog entry submitter name.

* Tue Nov 07 2023 Ian Kent <ikent@redhat.com> - 1:5.1.9-1
- Update to autofs 5.1.9 release.

* Fri Oct 06 2023 Pavel Reichl <preichl@redhat.com> - 1:5.1.8-23
- Convert License tag to SPDX format

* Fri Sep 29 2023 Florian Weimer <fweimer@redhat.com> - 1:5.1.8-22
- Update autofs-5.1.8-configure-c99.patch with -Wint-conversion fix

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.8-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Mar 25 2023 Ian Kent <ikent@redhat.com> - 1:5.1.8-20
- fix autofs regression due to positive_timeout.
- fix parse module instance mutex naming.
- serialise lookup module open and reinit.
- coverity fix for invalid access.
- fix hosts map deadlock on restart.
- fix deadlock with hosts map reload.
- fix memory leak in update_hosts_mounts().
- fix minus only option handling in concat_options().
- fix incorrect path for is_mounted() in try_remount().
- fix additional tsv invalid access.
- fix use_ignore_mount_option description.
- include addtional log info for mounts.
- fail on empty replicated host name.
- improve handling of ENOENT in sss setautomntent().
- don't immediately call function when waiting.
- fix return status of mount_autofs().
- don't close lookup at umount.
- fix deadlock in lookups.
- dont delay expire.
- make amd mapent search function name clear.
- rename statemachine() to signal_handler().
- make signal handling consistent.
- eliminate last remaining state_pipe usage.
- add function master_find_mapent_by_devid().
- use device id to locate autofs_point when setting log priotity.
- add command pipe handling functions.
- switch to application wide command pipe.
- get rid of unused field submnt_count.
- fix mount tree startup reconnect.
- fix unterminated read in handle_cmd_pipe_fifo_message().

* Fri Mar 10 2023 Arjun Shankar <arjun@redhat.com> - 1:5.1.8-9
- Port configure script to C99

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 19 2022 Ian Kent <ikent@redhat.com> - 1:5.1.8-7
- fix invalid tsv access.

* Tue Sep 13 2022 Ian Kent <ikent@redhat.com> - 1:5.1.8-6
- fix changelog out of order entry.
- fix missing unlock in sasl_do_kinit_ext_cc().
- fix file listed twice in spec file.

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri May 06 2022 Ian Kent <ikent@redhat.com> - 1:5.1.8-4
- fix kernel mount status notification.
- fix set open file limit.
- improve descriptor open error reporting.
- fix root offset error handling.
- fix nonstrict fail handling of last offset mount.
- dont fail on duplicate offset entry tree add.
- fix loop under run in cache_get_offset_parent().
- bailout on rpc systemerror.
- fix nfsv4 only mounts should not use rpcbind.
- simplify cache_add() a little.
- fix use after free in tree_mapent_delete_offset_tree().
- fix memory leak in xdr_exports().
- avoid calling pthread_getspecific() with NULL key_thread_attempt_id.
- fix sysconf(3) return handling.
- remove nonstrict parameter from tree_mapent_umount_offsets().
- fix handling of incorrect return from umount_ent().
- dont use initgroups() at spawn.

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 Björn Esser <besser82@fedoraproject.org> - 1:5.1.8-2
- Rebuild(libnsl2)

* Tue Oct 19 2021 Ian Kent <ikent@redhat.com> - 1:5.1.8-1
- Update to upstream release 5.1.8.

* Wed Oct 13 2021 Ian Kent <ikent@redhat.com> - 1:5.1.7-21
- fix use of possibly NULL var in lookup_program.c:match_key().
- fix incorrect print format specifiers in get_pkt().
- add mapent path length check in handle_packet_expire_direct().
- add copy length check in umount_autofs_indirect().
- add some buffer length checks to master map parser.
- add buffer length check to rmdir_path().
- eliminate buffer usage from handle_mounts_cleanup().
- add buffer length checks to autofs mount_mount().
- make NFS version check flags consistent.
- refactor get_nfs_info().
- also require TCP_REQUESTED when setting NFS port.

* Mon Aug 02 2021 Ian Kent <ikent@redhat.com> - 1:5.1.7-20
- fix potential memory leak in "eliminate some more alloca usage" patch.
- remove unused parameter from add_path() in "eliminate some more alloca usage" patch.

* Thu Jul 22 2021 Ian Kent <ikent@redhat.com> - 1:5.1.7-19
- fix concat_options() error handling.
- eliminate some more alloca usage.
- use default stack size for threads.

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 19 2021 Ian Kent <ikent@redhat.com> - 1:5.1.7-17
- correct patch, fix nonstrict offset mount fail handling.

* Thu Jun 17 2021 Ian Kent <ikent@redhat.com> - 1:5.1.7-16
- fix nonstrict offset mount fail handling.

* Tue Jun 15 2021 Ian Kent <ikent@redhat.com> - 1:5.1.7-15
- fix amd hosts mount expire.
- fix offset entries order.
- use mapent tree root for tree_mapent_add_node().
- eliminate redundant cache lookup in tree_mapent_add_node().
- fix hosts map offset order.
- fix direct mount deadlock.
- add missing desciption of null map option.

* Mon May 31 2021 Ian Kent <ikent@redhat.com> - 1:5.1.7-13
- dont use AUTOFS_DEV_IOCTL_CLOSEMOUNT.
- fix lookup_prune_one_cache() refactoring change.

* Mon Apr 19 2021 Ian Kent <ikent@redhat.com> - 1:5.1.7-12
  - Coverity fixes.
    - add missing free in handle_mounts().
    - remove redundant if check.
    - fix possible memory leak in master_parse().
    - fix possible memory leak in mnts_add_amdmount().
    - fix double unlock in parse_mount().
    - add length check in umount_subtree_mounts().
    - fix flags check in umount_multi().
    - dont try umount after stat() ENOENT fail.
    - remove redundant assignment in master_add_amd_mount_section_mounts().
    - fix dead code in mnts_add_mount().
    - fix arg not used in error print.
    - fix missing lock release in mount_subtree().
    - fix double free in parse_mapent().
    - refactor lookup_prune_one_cache() a bit.
    - cater for empty mounts list in mnts_get_expire_list().
    - add ext_mount_hash_mutex lock helpers.
  - fix amd section mounts map reload.
  - fix dandling symlink creation if nis support is not available.

* Tue Mar 16 2021 Ian Kent <ikent@redhat.com> - 1:5.1.7-10
  - add xdr_exports().
  - remove mount.x and rpcgen dependencies.
  - dont use realloc in host exports list processing.
  - use sprintf() when constructing hosts mapent.
  - fix mnts_remove_amdmount() uses wrong list.
  - Fix option for master read wait.
  - eliminate cache_lookup_offset() usage.
  - fix is mounted check on non existent path.
  - simplify cache_get_parent().
  - set offset parent in update_offset_entry().
  - remove redundant variables from mount_autofs_offset().
  - remove unused parameter form do_mount_autofs_offset().
  - refactor umount_multi_triggers().
  - eliminate clean_stale_multi_triggers().
  - simplify mount_subtree() mount check.
  - fix mnts_get_expire_list() expire list construction.
  - fix inconsistent locking in umount_subtree_mounts().
  - fix return from umount_subtree_mounts() on offset list delete.
  - pass mapent_cache to update_offset_entry().
  - fix inconsistent locking in parse_mount().
  - remove unused mount offset list lock functions.
  - eliminate count_mounts() from expire_proc_indirect().
  - eliminate some strlen calls in offset handling.
  - don't add offset mounts to mounted mounts table.
  - reduce umount EBUSY check delay.
  - cleanup cache_delete() a little.
  - rename path to m_offset in update_offset_entry().
  - don't pass root to do_mount_autofs_offset().
  - rename tree implementation functions.
  - add some multi-mount macros.
  - remove unused functions cache_dump_multi() and cache_dump_cache().
  - add a len field to struct autofs_point.
  - make tree implementation data independent.
  - add mapent tree implementation.
  - add tree_mapent_add_node().
  - add tree_mapent_delete_offsets().
  - add tree_mapent_traverse_subtree().
  - fix mount_fullpath().
  - add tree_mapent_cleanup_offsets().
  - add set_offset_tree_catatonic().
  - add mount and umount offsets functions.
  - switch to use tree implementation for offsets.
  - remove obsolete functions.
  - remove redundant local var from sun_mount().
  - use mount_fullpath() in one spot in parse_mount().
  - pass root length to mount_fullpath().
  - remove unused function master_submount_li.st_empty().
  - move amd mounts removal into lib/mounts.c.
  - check for offset with no mount location.
  - remove mounts_mutex.
  - remove unused variable from get_exports().

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:5.1.7-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Ian Kent <ikent@redhat.com> - 1:5.1.7-1
- Update to upstream release 5.1.7.

* Mon Aug 31 2020 Ian Kent <ikent@redhat.com> - 1:5.1.6-11
- fix configure force shutdown check.

* Tue Aug 25 2020 Ian Kent <ikent@redhat.com> - 1:5.1.6-10
- fix incorrect configure option.

* Tue Aug 25 2020 Ian Kent <ikent@redhat.com> - 1:5.1.6-9
- mount_nfs.c fix local rdma share not mounting.
- fix ldap sasl reconnect problem.
- samples/ldap.schema fix.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 17 2020 Ian Kent <ikent@redhat.com> - 1:5.1.6-7
- initialize struct addrinfo for getaddrinfo() calls.
- fix quoted string length calc in expandsunent().
- fix double quoting of ampersand in auto.smb as well.
- fix autofs mount options construction.

* Mon Jun 01 2020 Ian Kent <ikent@redhat.com> - 1:5.1.6-4
- fix changelog message.
- actually commit the patches referred to in the commit.
- adjust revision to allow fixing f32 revision on update.

* Mon Jun 01 2020 Ian Kent <ikent@redhat.com> - 1:5.1.6-3
- make bind mounts propagation slave by default.
- update ldap READMEs and schema definitions.
- fix program map multi-mount lookup after mount fail.
- fix browse dir not re-created on symlink expire.
- fix a regression with map instance lookup.
- correct fsf address.
- fix Makefile targets' directory dependencies.
- remove intr hosts map mount option.
- fix trailing dollar sun entry expansion.
- fix double quoting in auto.smb.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 07 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.6-1
- update to upstream 5.1.6 release.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 14 2019 Ian Kent <ikent@redhat.com> - 1:5.1.5-4
- add BuildRequires: krb5-devel.

* Tue May 14 2019 Ian Kent <ikent@redhat.com> - 1:5.1.5-4
- support strictexpire mount option.
- fix hesiod string check in master_parse().

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 05 2018 Ian Kent <ikent@redhat.com> - 1:5.1.5-2
- update spec file to build without hesiod.

* Mon Nov 05 2018 Ian Kent <ikent@redhat.com> - 1:5.1.5-1
- update to upstream 5.1.5 release.

* Fri Aug 17 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-21
- fix use after free in parse_ldap_config().

* Mon Aug 06 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-20
- fix update_negative_cache() map source usage.
- fix program usage message.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-18
- add man page note about extra slashes in paths.
- add a number of covarity identified fixes.
- change expire type naming to better reflect usage.
- use defines for expire type.
- make umount_ent() recognise forced umount.
- enable SIGUSR2 handling in rpm spec file.
- fix age setting at startup.

* Thu May 17 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-17
- fix fd leak in rpc_do_create_client().

* Mon Mar 26 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-16
- also add missing "BuildRequires: systemd-devel".

* Mon Mar 26 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-15
- tiny patch for autofs typo and possible bug.
- add units After line to include statd service.
- use systemd sd_notify() at startup.
- fix NFS version mask usage.
- fix incorrect date in changelog.

* Tue Mar 06 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-14
- improve hostname lookup error logging.

* Tue Mar 06 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-13
- fix install permissions of auto.net and auto.smb.
- update change log.

* Mon Feb 19 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-12
- dont allow trailing slash in master map mount points.
- fix libresolv configure check.
- add fedfs-getsrvinfo.c.
- add mount.fedfs.c.
- add fedfs-map-nfs4.c
- add conditional inclusion of fedfs binaries.
- add an example fedfs master map entry to the installed master map.

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:5.1.4-11
- Escape macros in %%changelog

* Fri Feb 9 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-10
- clean up obsolete spec file directives.

* Wed Feb 7 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-9
- fix install mode of autofs_ldap_auth.conf.

* Tue Feb 6 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-8
- add missing BuildRequires.

* Mon Feb 5 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-7
- add error handling for ext_mount_add().
- account for recent libnsl changes.
- use_hostname_for_mounts shouldn't prevent selection among replicas.
- fix monotonic_elapse.
- Makefiles.rules: remove 'samples' from SUBDIRS.

* Thu Feb 1 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-6
- dont use array for path when not necessary.
- fix prefix option handling in expand_entry().
- fix sublink option not set from defaults.
- fix error return in do_nfs_mount().

* Wed Jan 10 2018 Ian Kent <ikent@redhat.com> - 1:5.1.4-5
- actually apply fix use after free in do_master_list_reset().
- fix deadlock in dumpmaps.
- fix rpcgen dependency problem.

* Fri Dec 22 2017 Ian Kent <ikent@redhat.com> - 1:5.1.4-4
- fix use after free in do_master_list_reset().

* Wed Dec 20 2017 Ian Kent <ikent@redhat.com> - 1:5.1.4-3
- fix email in last two changelog entries.

* Tue Dec 19 2017 Ian Kent <ikent@redhat.com> - 1:5.1.4-2
- fix flag file permission.
- fix directory create permission.

* Tue Dec 19 2017 Ian Kent <ikent@redhat.com> - 1:5.1.4-1
- Update to upstream 5.1.4 release.

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:5.1.3-5
- Remove old crufty coreutils requires

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 29 2017 Ian Kent <ikent@redhat.com> - 1:5.1.3-2
- Fix "Source:" URL and changelog anotations.

* Mon May 29 2017 Ian Kent <ikent@redhat.com> - 1:5.1.3-1
- update to upstream 5.1.3 release.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.2-1
- update to upstream 5.1.2 release.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Ian Kent <ikent@redhat.com> - 1:5.1.1-21
- add some new upstream memory leak and use after free bug fixes.

* Wed Jan 20 2016 Ian Kent <ikent@redhat.com> - 1:5.1.1-20
- fix incorrect committer changelog entries.
- add current released upstream patches.

* Wed Nov 04 2015 Ian Kent <ikent@redhat.com> - 1:5.1.1-7
- revert fix libtirpc name clash patch (an old 5.0.6 patch).

* Wed Nov 04 2015 Ian Kent <ikent@redhat.com> - 1:5.1.1-6
- remove unnecessary nfs-utils BuildRequires (bz1277669).

* Mon Nov 02 2015 Ian Kent <ikent@redhat.com> - 1:5.1.1-5
- fix fix gcc5 complaints.
- update libtirpc workaround for new soname.

* Sun Nov 01 2015 Kalev Lember <klember@redhat.com> - 1:5.1.1-4
- Rebuilt for libtirpc soname bump

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Ian Kent <ikent@redhat.com> - 1:5.1.1-2
- add build requires for gcc.

* Thu Apr 23 2015 Ian Kent <ikent@redhat.com> - 1:5.1.1-1
- Update to autofs-5.1.1.

* Mon Mar 23 2015 Ian Kent <ikent@redhat.com> - 1:5.1.0-12
- fix gcc5 complaints (bz1204685).

* Mon Mar 23 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1:5.1.0-11
- Drop ancient 2.6 kernel patches from docs

* Wed Jan 21 2015 Ian Kent <ikent@redhat.com> - 1:5.1.0-10
- make negative cache update consistent for all lookup modules.
- ensure negative cache isn't updated on remount.
- dont add wildcard to negative cache.
- make service want network-online (bz1071591).

* Tue Nov 18 2014 Ian Kent <ikent@redhat.com> - 1:5.1.0-9
- fix custom autofs.conf not being installed.
- init qdn before use in get_query_dn().
- fix typo in update_hosts_mounts().
- fix hosts map update on reload.


* Fri Oct 17 2014 Ian Kent <ikent@redhat.com> - 1:5.1.0-8
- fix fix master map type check.

* Wed Oct 15 2014 Ian Kent <ikent@redhat.com> - 1:5.1.0-7
- force disable browse mode for amd format maps.
- fix hosts map options check in lookup_amd_instance().
- fix memory leak in create_client().
- fix memory leak in get_exports().
- fix memory leak in get_defaults_entry().
- fix out of order clearing of options buffer.
- fix reset amd lexer scan buffer.
- ignore multiple commas in options strings.
- fix typo in flagdir configure option.
- clarify multiple mounts description.
- gaurd against incorrect umount return.
- update man page autofs(8) for systemd.
- remove ancient kernel Requires.

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 8 2014 Ian Kent <ikent@redhat.com> - 1:5.1.0-5
- rename two incorrectly named patches.
- add missing change entry to another patch.

* Mon Jul 7 2014 Ian Kent <ikent@redhat.com> - 1:5.1.0-4
- add mutex call return check in defaults.c.

* Mon Jul 7 2014 Ian Kent <ikent@redhat.com> - 1:5.1.0-3
- fix compile error in defaults.c.
- add serialization to sasl init.
- dont allocate dev_ctl_ops too early.
- fix incorrect round robin host detection.
- fix race accessing qdn in get_query_dn().
- fix leak in cache_push_mapent().
- fix config entry read buffer not checked.
- fix FILE pointer check in defaults_read_config().
- fix memory leak in conf_amd_get_log_options().
- fix signed comparison in inet_fill_net().
- fix buffer size checks in get_network_proximity().
- fix leak in get_network_proximity().
- fix buffer size checks in merge_options().
- check amd lex buffer len before copy.
- add return check in ldap check_map_indirect().
- check host macro is set before use.
- check options length before use in parse_amd.c.
- fix some out of order evaluations in parse_amd.c.
- fix copy and paste error in dup_defaults_entry().

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 5 2014 Ian Kent <ikent@redhat.com> - 1:5.1.0-1
- update to upstream release, 5.1.0.
  - fix reset flex scan buffer on init.
  - fix fix negative status being reset on map read.
  - fix out of order amd timestamp lookup.
  - fix ldap default schema config.
  - fix ldap default master map name config.
  - fix map format init in lookup_init().
  - fix incorrect max key length in defaults get_hash().
  - fix xfn sets incorrect lexer state.
  - fix old style key lookup.
  - fix expire when server not responding.
  - fix ldap_uri config update.
  - fix typo in conf_load_autofs_defaults().
  - fix hash on confg option add and delete.
  - add plus to path match pattern.
  - fix multi entry ldap option handling.
  - cleanup options in amd_parse.c.
  - allow empty value for some map options.
  - allow empty value in macro selectors.

* Sun Apr 13 2014 Ian Kent <ikent@redhat.com> - 1:5.1.0-0.beta1.1
- amd lookup update lookup ldap to handle amd keys
  - inadvertantly drop from initial series.
- amd lookup update lookup hesiod to handle amd keys
  - inadvertantly drop from initial series.
- fix wildcard key lookup.
- check for non existent negative entries in lookup_ghost().

* Wed Apr 2 2014 Ian Kent <ikent@redhat.com> - 1:5.1.0-0.beta1
- Update to autofs-5.0.1-beta1.

* Wed Feb 19 2014 Ian Kent <ikent@redhat.com> - 1:5.0.8-6
- fix portmap not trying proto v2.

* Tue Dec 24 2013 Ian Kent <ikent@redhat.com> - 1:5.0.8-5
- fix ipv6 link local address handling.
- fix fix ipv6 libtirpc getport.
- get_nfs_info() should query portmapper if port is not given.
- fix rpc_portmap_getport() proto not set.

* Mon Nov 25 2013 Ian Kent <ikent@redhat.com> - 1:5.0.8-4
- allow --with-systemd to take a path arg.
- fix WITH_LIBTIRPC function name.
- fix ipv6 libtirpc getport (bz1033918).

* Thu Nov 7 2013 Ian Kent <ikent@redhat.com> - 1:5.0.8-3
- fix undefined authtype_requires_creds err if ldap enabled but without sasl.
- fix master map type check.
- fix task manager not getting signaled.

* Mon Oct 21 2013 Ian Kent <ikent@redhat.com> - 1:5.0.8-2
- remove now unused patch files (bz1020242).

* Mon Oct 21 2013 Ian Kent <ikent@redhat.com> - 1:5.0.8-1
- update to upstream version 5.0.8 (bz1020242).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.0.7-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-28
- add after sssd dependency to unit file (bz984089).

* Sat Jul 13 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-27
- fix a couple of compiler warnings.

* Fri Jul 12 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-26
- link with full reloc options.

* Fri Jul 12 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-25
- fix default path used for unitdir.
- fix changelog inconsistent dates.

* Wed Jul 10 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-24
- check for protocol option.
- use ulimit max open files if greater than internal maximum.

* Fri Jun 28 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-23
- fix add null check in parse_server_string() (bz979155).

* Wed Jun 19 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-22
- misc man page fixes (bz948517).

* Wed Jun 12 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-21
- fix probe each nfs version in turn for singleton mounts (bz973537).

* Tue Jun 11 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-20
- fix master map mount options matching.
- fix master map bogus keywork match.
- fix fix map entry duplicate offset detection.
- add a number of fixes based on a Covarity report.

* Mon May 27 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-19
- dont probe rdma mounts.

* Fri May 24 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-17
- fix interface address null check.

* Mon May 13 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-16
- make dump maps check for duplicate indirect mounts (bz961312).
- document allowed map sources in auto.master(5) (bz961312).
- add enable sloppy mount option to configure.

* Sun Apr 28 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-14
- fix syncronize of handle_mounts() shutdown.
- fix submount tree not all expiring.

* Tue Mar 26 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-13
- fix some automount(8) typos (bz664178).

* Tue Mar 12 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-12
- dont fail on master map self include.
- fix wildcard multi map regression.
- fix file descriptor leak when reloading the daemon.
- depricate nosymlink pseudo option.
- add symlink pseudo option.
- update kernel include files.
- fix requires in spec file.
- fix libtirpc build option.
- fix systemd unidir in spec file.
- document browse option in man page.
- fix automounter support on parisc.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.0.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Ian Kent <ikent@redhat.com> - 1:5.0.7-10
- fix submount offset delete.
- fix init script status return.
- fix use get_proximity() without libtirpc.
- don't use dirent d_type to filter out files in scandir().
- don't schedule new alarms after readmap.
- use numeric protocol ids instead of protoent structs.
- lib/defaults.c: use WITH_LDAP conditional around LDAP types.
- make yellow pages support optional.
- modules/replicated.c: use sin6_addr.s6_addr32.
- workaround missing GNU versionsort extension.

* Tue Nov 20 2012 Ian Kent <ikent@redhat.com> - 1:5.0.7-9
- fix nobind man page description.

* Tue Nov 20 2012 Ian Kent <ikent@redhat.com> - 1:5.0.7-8
- fix map entry duplicate offset detection.
- Allow nsswitch.conf to not contain "automount:" lines.

* Thu Oct 18 2012 Ian Kent <ikent@redhat.com> - 1:5.0.7-7
- use spec file systemd unit file location.

* Thu Oct 18 2012 Ian Kent <ikent@redhat.com> - 1:5.0.7-6
- fix recursive mount deadlock.
- increase file map read buffer size.
- handle new location of systemd.

* Tue Oct 16 2012 Ian Kent <ikent@redhat.com> - 1:5.0.7-5
- configure: allow cross compilation update.
- fix date in changelog entry.

* Mon Oct 15 2012 Ian Kent <ikent@redhat.com> - 1:5.0.7-4
- include usage in usage message.
- dont wait forever to restart.
- add option description to man page.
- fix null map entry order handling.
- make description of default MOUNT_WAIT setting clear.
- configure.in: allow cross compilation.
- README: update mailing list subscription info.
- allow non root user to check status.

* Mon Sep 10 2012 Ian Kent <ikent@redhat.com> - 1:5.0.7-3
- fix nobind sun escaped map entries.
- fix use cache entry after free mistake.
- fix ipv6 proximity calculation.
- fix parse buffer initialization.
- fix typo in automount(8).

* Mon Aug 27 2012 Ian Kent <ikent@redhat.com> - 1:5.0.7-2
- update systemd scriplet macros (bz850040).

* Wed Jul 25 2012 Ian Kent <ikent@redhat.com> - 1:5.0.7-1
- Update to upstream version 5.0.7.

* Wed Jul 25 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-24
- fix changelog message commit dates.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.0.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-21
- fix systemd argument passing.
- fix get_nfs_info() can incorrectly fail.
- fix offset directory removal.

* Tue Jul 3 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-21
- fix fix LDAP result leaks on error paths.
- report map not read when debug logging.
- duplicate parent options for included maps.
- update ->timeout() function to not return timeout.
- move timeout to map_source.
- fix kernel verion check of version components.
- dont retry ldap connect if not required.
- check if /etc/mtab is a link to /proc/self/mounts.
- fix nfs4 contacts portmap.
- make autofs wait longer for shutdown.
- fix sss map age not updated.
- fix remount deadlock.
- fix umount recovery of busy direct mount.
- fix offset mount point directory removal.
- remove move mount code and configure option.
- fix remount of multi mount.
- fix devce ioctl alloc path check.
- refactor hosts lookup module.
- remove cache update from parse_mount().
- add function to delete offset cache entry.
- allow update of multi mount offset entries.
- add hup signal handling to hosts map.

* Tue May 22 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-19
- fix libtirpc name clash (bz821847).

* Tue May 22 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-18
- update patch fix initialization in rpc create_client() (bz821847).

* Wed May 16 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-17
- fix initialization in rpc create_client() (bz821847).

* Tue May 1 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-16
- add libsss_autofs as a build dependency.

* Tue May 1 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-15
- fix typo in libtirpc file name.
- fix rework error return handling in rpc code.
- allow MOUNT_WAIT to override probe.
- improve UDP RPC timeout handling.
- fix segfault in get_query_dn().
- use strtok_r() in linux_version_code().
- fix sss wildcard match.
- fix dlopen() error handling in sss module.
- fix configure string length tests for sss library.

* Wed Feb 29 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-14
- fix function to check mount.nfs version.

* Sun Feb 26 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-13
- fix error in %%post scriplet.

* Fri Feb 24 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-12
- ignore duplicate exports in auto.net.
- add kernel verion check function.
- add function to check mount.nfs version.
- reinstate singleton mount probe.
- rework error return handling in rpc code.
- catch EHOSTUNREACH and bail out early.
- systemd support fixes.
- fix segmentation fault in do_remount_indirect().

* Thu Feb 9 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-11
- fix fuzz in CHANGELOG hunk when applying patch26.

* Tue Feb 7 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-10
- fix rpc build error.
- add sss lookup module.
- teach automount about sss source.

* Mon Jan 23 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-9
- add correct patch for "fix improve mount location error reporting".
- add correct patch for "fix fix wait for master source mutex".

* Mon Jan 23 2012 Ian Kent <ikent@redhat.com> - 1:5.0.6-8
- fix fix wait for master source mutex.
- fix improve mount location error reporting (bz783496).

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 9 2011 Ian Kent <ikent@redhat.com> - 1:5.0.6-6
- remove empty command line arguments (passed by systemd).

* Mon Dec 5 2011 Ian Kent <ikent@redhat.com> - 1:5.0.6-5
- fix ipv6 name lookup check.
- fix ipv6 rpc calls.
- fix ipv6 configure check.
- add piddir to configure.
- add systemd unit support.
- fix MNT_DETACH define.

* Mon Dec 5 2011 Ian Kent <ikent@redhat.com> - 1:5.0.6-4
- fix lsb service name in init script 2 (bz712504).

* Tue Nov 8 2011 Ian Kent <ikent@redhat.com> - 1:5.0.6-3
- improve mount location error reporting.
- fix paged query more results check.
- fix dumpmaps not reading maps.
- fix result null check in read_one_map().
- Fix LDAP result leaks on error paths.
- code analysis fixes 1.
- fix not bind mounting local filesystem.
- update dir map-type patch for changed patch order.
- fix wait for master source mutex.
- fix submount shutdown race
- fix fix map source check in file lookup.
- add disable move mount configure option.

* Wed Jul 6 2011 Ian Kent <ikent@redhat.com> - 1:5.0.6-2
- add missing spec file entries for dir-type change (bz719208).

* Mon Jul 4 2011 Ian Kent <ikent@redhat.com> - 1:5.0.6-1
- update source to 5.0.6.
- fix ipv6 name for lookup fix.
- add dir map-type patch.

* Tue Jun 14 2011 Ian Kent <ikent@redhat.com> - 1:5.0.5-38
- fix lsb service name in init script (bz692963).

* Fri Mar 18 2011 Ian Kent <ikent@redhat.com> - 1:5.0.5-37
- replace GPLv3 code with GPLv2 equivalent.
 
* Thu Mar 03 2011 Ian Kent <ikent@redhat.com> - 1:5.0.5-36
- use weight only for server selection.
- fix isspace() wild card substition.
- auto adjust ldap page size.
- fix prune cache valid check.
- fix mountd vers retry.
- fix expire race.
- add lsb force-reload and try-restart.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.0.5-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 23 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-34.fc15
- revert wait for master map to be available at start.

* Mon Nov 22 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-33.fc15
- fix wait for master map to be available at start.

* Mon Nov 8 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-32.fc15
- always read file maps mount lookup map read fix.
- fix direct map not updating on reread.
- add external bind method.
- fix add simple bind auth.
- add option to dump configured automount maps.
- wait for master map to be available at start.

* Fri Aug 27 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-31.fc15
- fix status privilege error (bz627605).

* Wed Aug 18 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-30.fc15
- fix restart not working (bz624694).

* Wed Aug 11 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-29
- remove ERR_remove_state() openssl call.

* Tue Aug 10 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-28
- remove extra read master map call.
- remove extra cache create call in master_add_map_source().
- fix error handing in do_mount_indirect().
- expire thread use pending mutex.
- explicity link against the Kerberos library.
- remove some log message duplication for verbose logging.

* Mon May 24 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-27.fc14
- fix master map source server unavailable handling.
- add autofs_ldap_auth.conf man page.
- fix random selection for host on different network.
- make redhat init script more lsb compliant.
- don't hold lock for simple mounts.
- fix remount locking.
- fix wildcard map entry match.
- fix parse_sun() module init.
- dont check null cache on expire.
- fix null cache race.
- fix cache_init() on source re-read.
- fix mapent becomes negative during lookup.
- check each dc server individually.
- fix negative cache included map lookup.
- remove state machine timed wait.

* Fri Apr 30 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-26.fc14
- remove URL tag as there is not official autofs wiki (bz529804).

* Wed Apr 7 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-25.fc14
- make nfs4 default for replicated selection configuration (bz579949).
- add simple bind authentication option (bz579951).

* Fri Mar 26 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-24.fc14
- fix add locality as valid ldap master map attribute (bz575863).

* Wed Mar 17 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-22
- fix get query dn failure.
- fix ampersand escape in auto.smb.
- add locality as valid ldap master map attribute.

* Wed Mar 17 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-22
- add Conflicts to ensure we get fixed cyrus-sasl-lib for rev 21 change.

* Tue Feb 23 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-21
- add missing sasl mutex callbacks.

* Thu Feb 11 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-19
- fix segfault upon reconnect cannot find valid base dn.

* Mon Feb 1 2010 Ian Kent <ikent@redhat.com> - 1:5.0.5-17
- dont connect at ldap lookup module init.
- fix random selection option.
- fix disable timeout.
- fix strdup() return value check.

* Tue Dec 8 2009 Ian Kent <ikent@redhat.com> - 1:5.0.5-16
- fix memory leak on reload (bz545137).

* Fri Dec 4 2009 Ian Kent <ikent@redhat.com> - 1:5.0.5-14
- fix rpc fail on large export list (bz543023).

* Mon Nov 30 2009 Ian Kent <ikent@redhat.com> - 1:5.0.5-12
- check for path mount location in generic module.
- dont fail mount on access fail.

* Tue Nov 24 2009 Ian Kent <ikent@redhat.com> - 1:5.0.5-10
- fix pidof init script usage.

* Mon Nov 23 2009 Ian Kent <ikent@redhat.com> - 1:5.0.5-8
- fix timeout in connect_nb().

* Mon Nov 16 2009 Ian Kent <ikent@redhat.com> - 1:5.0.5-6
- don't use master_lex_destroy() to clear parse buffer.
- make documentation for set-log-priority clearer.

* Tue Nov 10 2009 Ian Kent <ikent@redhat.com> - 1:5.0.5-5
- fix ext4 "preen" fsck at mount.

* Mon Nov 9 2009 Ian Kent <ikent@redhat.com> - 1:5.0.5-4
- fix stale initialization for file map instance patch was not applied.

* Tue Nov 3 2009 Ian Kent <ikent@redhat.com> - 1:5.0.5-3
- fix stale initialization for file map instance.

* Tue Oct 6 2009 Ian Kent <kent@redhat.com> - 1:5.0.5-2
- fix included map read fail handling.
- refactor ldap sasl authentication bind to eliminate extra connect
  causing some servers to reject the request. 
- add mount wait parameter to allow timeout of mount requests to
  unresponsive servers.
- special case cifs escape handling.
- fix libxml2 workaround configure.
- more code analysis corrections (and fix a typo in an init script).
- fix backwards #ifndef INET6.

* Fri Sep 4 2009 Ian Kent <ikent@redhat.com> - 1:5.0.5-1
- update source to latest upstream version.
  - this is essentially a consolidation of the patches already in this rpm.
- add dist tag to match latest RHEL-5 package tag format.

* Thu Sep 3 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-39
- fix libxml2 non-thread-safe calls.
- fix direct map cache locking.
- fix patch "dont umount existing direct mount on reread" deadlock.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.0.4-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-34
- fix typo in patch to allow dumping core.

* Wed Jul 15 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-32
- fix an RPC fd leak.
- don't block signals we expect to dump core.
- fix pthread push order in expire_proc_direct().

* Fri Jun 12 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-30
- fix incorrect dclist free.
- srv lookup handle endianness.
- fix bug introduced by library reload changes which causes autofs to
  not release mount thread resources when using submounts.
- fix notify mount message path.
- try harder to work out if we created mount point at remount.
- fix double free in do_sasl_bind().
- manual umount recovery fixes.
- fix map type info parse error.

* Mon May 18 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-28
- use intr option as hosts mount default.
- sync kernel includes with upstream kernel.
- dont umount existing direct mount on master re-read.
- fix incorrect shutdown introduced by library relaod fixes.
- improve manual umount recovery.
- dont fail on ipv6 address when adding host.
- always read file maps multi map fix.
- always read file maps key lookup fixes.
- add support for LDAP_URI="ldap:///<domain db>" SRV RR lookup.

* Thu Apr 16 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-26
- fix lsb init script header.
- fix memory leak reading ldap master map.
- fix st_remove_tasks() locking.
- reset flex scanner when setting buffer.
- zero s_magic is valid.

* Mon Mar 30 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-24
- clear rpc client on lookup fail.

* Fri Mar 20 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-23
- fix call restorecon when misc device file doesn't exist.

* Wed Mar 18 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-22
- use misc device ioctl interface by default, if available.

* Tue Mar 17 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-21
- fix file map lookup when reading included or nsswitch sources.
  - a regression introduced by file map lookup optimisation in rev 9.

* Fri Mar 13 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-20
- add LSB init script parameter block.

* Fri Mar 13 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-19
- another easy alloca replacements fix.

* Thu Mar 12 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-18
- fix return start status on fail.
- fix double free in expire_proc().

* Wed Feb 25 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-17
- fix bad token declaration in master map parser.

* Wed Feb 25 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-16
- correct mkdir command in %%install section, bz481132.

* Tue Feb 24 2009 Ian Kent <ikent@redhat.com> - 1:5.0.4-15
- fix array out of bounds accesses and cleanup couple of other alloca() calls.
- Undo mistake in copy order for submount path introduced by rev 11 patch.
- add check for alternate libxml2 library for libxml2 tsd workaround.
- add check for alternate libtirpc library for libtirpc tsd workaround.
- cleanup configure defines for libtirpc.
- add WITH_LIBTIRPC to -V status report.
- add libtirpc-devel to BuildRequires.
- add nfs mount protocol default configuration option.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Ian Kent <ikent@redhat.com> - 5.0.4-10
- fix mntent.h not included before use of setmntent_r().

* Mon Feb 16 2009 Ian Kent <ikent@redhat.com> - 5.0.4-9
- fix hosts map use after free.
- fix uri list locking (again).
- check for stale SASL credentials upon connect fail.
- add "forcestart" and "forcerestart" init script options to allow
  use of 5.0.3 strartup behavior if required.
- always read entire file map into cache to speed lookups.
- make MAX_ERR_BUF and PARSE_MAX_BUF use easier to audit.
- make some easy alloca replacements.
- update to configure libtirpc if present.
- update to provide ipv6 name and address support.
- update to provide ipv6 address parsing.

* Thu Feb 5 2009 Ian Kent <ikent@redhat.com> - 5.0.4-8
- rename program map parsing bug fix patch.
- use CLOEXEC flag functionality for setmntent also, if present.

* Wed Jan 21 2009 Jeff Moyer <jmoyer@redhat.com> - 5.0.4-6
- fix a bug in the program map parsing routine

* Thu Jan 15 2009 Ian Kent <kent@redhat.com> - 5.0.4-5
- fix negative caching of non-existent keys.
- fix ldap library detection in configure.
- use CLOEXEC flag functionality if present.
- fix select(2) fd limit.
- make hash table scale to thousands of entries.

* Wed Dec 3 2008 Ian Kent <kent@redhat.com> - 5.0.4-4
- fix nested submount expire deadlock.

* Wed Nov 19 2008 Ian Kent <kent@redhat.com> - 5.0.4-3
- fix libxml2 version check for deciding whether to use workaround.

* Tue Nov 11 2008 Ian Kent <kent@redhat.com> - 5.0.4-2
- Fix tag confusion.

* Tue Nov 11 2008 Ian Kent <kent@redhat.com> - 5.0.4-1
- Upstream source version 5.0.4.

* Tue Nov 11 2008 Ian Kent <kent@redhat.com> - 5.0.3-32
- correct buffer length setting in autofs-5.0.3-fix-ifc-buff-size-fix.patch.

* Sun Nov 2 2008 Ian Kent <kent@redhat.com> - 5.0.3-30
- fix segv during library re-open.
- fix incorrect pthreads condition handling for expire requests.
- fix master map lexer eval order.
- fix bad alloca usage.

* Thu Oct 23 2008 Ian Kent <ikent@redhat.com> - 5.0.3-28
- don't close file handle for rootless direct mounti-mount at mount.
- wait submount expire thread completion when expire successful.
- add inadvertantly ommitted server list locking in LDAP module.

* Fri Oct 10 2008 Ian Kent <ikent@redhat.com> - 5.0.3-26
- add map-type-in-map-name fix patch to sync with upstream and RHEL.
- don't readmap on HUP for new mount.
- add NIS_PARTIAL to map entry not found check and fix use after free bug.

* Fri Sep 26 2008 Ian Kent <ikent@redhat.com> - 5.0.3-25
- fix fd leak at multi-mount non-fatal mount fail.
- fix incorrect multi-mount mountpoint calcualtion.

* Fri Sep 19 2008 Ian Kent <ikent@redhat.com> - 5.0.3-23
- add upstream bug fixes
  - bug fix for mtab check.
  - bug fix for zero length nis key.
  - update for ifc buffer handling.
  - bug fix for kernel automount handling.
- warning: I found a bunch of patches that were present but not
  being applied.
  
* Mon Aug 25 2008 Ian Kent <ikent@redhat.com> - 5.0.3-21
- add upstream bug fix patches
  - add command line option to override is running check.
  - don't use proc fs for is running check.
  - fix fail on included browse map not found.
  - fix incorrect multi source messages.
  - clear stale flag on map read.
  - fix proximity other rpc ping timeout.
  - refactor mount request vars code.
  - make handle_mounts startup condition distinct.
  - fix submount shutdown handling.
  - try not to block on expire.
  - add configuration paramter UMOUNT_WAIT.
  - fix multi mount race.
  - fix nfs4 colon escape handling.
  - check replicated list after probe.
  - add replicated server selection debug logging.
  - update replicated server selection documentation.
  - use /dev/urandom instead of /dev/random.
  - check for mtab pointing to /proc/mounts.
  - fix interface config buffer size.
  - fix percent hack heap corruption.

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.0.3-19
- change conflicts to requires
- fix license tag

* Mon Jun 30 2008 Ian Kent <ikent@redhat.com> - 5.0.3-18
- don't abuse the ap->ghost field on NFS mount.
- multi-map doesn't pickup NIS updates automatically.
- eliminate redundant DNS name lookups.
- mount thread create condition handling fix.
- allow directory create on NFS root.
- check direct mount path length.
- fix incorrect in check in get user info.
- fix a couple of memory leaks.

* Wed May 14 2008 Ian Kent <ikent@redhat.com> - 5.0.3-16
- update patches, documentation and comments only change.
- rename patch and add to CVS.

* Mon May 12 2008 Ian Kent <ikent@redhat.com> - 5.0.3-14
- check for nohide mounts (bz 442618).
- ignore nsswitch sources that aren't supported (bz 445880).

* Thu Apr 17 2008 Ian Kent <ikent@redhat.com> - 5.0.3-13
- fix typo in patch for incorrect pthreads condition handling patch.

* Mon Apr 14 2008 Ian Kent <ikent@redhat.com> - 5.0.3-12
- fix incorrect pthreads condition handling for mount requests.

* Tue Apr 1 2008 Ian Kent <ikent@redhat.com> - 5.0.3-11
- and another try at fixing lexer matching map type in map name.

* Sun Mar 30 2008 Ian Kent <ikent@redhat.com> - 5.0.3-10
- another try a fixing lexer matching map type in map name.

* Wed Mar 26 2008 Ian Kent <ikent@redhat.com> - 5.0.3-9
- fix lexer ambiguity in match when map type name is included in map name.

* Mon Mar 24 2008 Ian Kent <ikent@redhat.com> - 5.0.3-8
- revert miscellaneous device node related patches.
- add missing check for zero length NIS key.
- fix incorrect match of map type name when included in map name.
- update rev 7 sasl callbacks patch.

* Thu Mar 20 2008 Ian Kent <ikent@redhat.com> - 5.0.3-7
- add patch to initialize sasl callbacks unconditionally on autofs
  LDAP lookup library load.

* Mon Feb 25 2008 Ian Kent <ikent@redhat.com> - 5.0.3-6
- fix expire calling kernel more often than needed.
- fix unlink of mount tree incorrectly causing autofs mount fail.
- add miscellaneous device node interface library.
- use miscellaneous device node, if available, for active restart.
- device node and active restart fixes.
- update is_mounted to use device node ioctl, if available.

* Fri Feb 1 2008 Ian Kent <ikent@redhat.com> - 5.0.3-5
- another fix for don't fail on empty master map.

* Fri Jan 25 2008 Ian Kent <ikent@redhat.com> - 5.0.3-4
- correction to the correction for handling of LDAP base dns with spaces.
- avoid using UDP for probing NFSv4 mount requests.
- use libldap instead of libldap_r.

* Mon Jan 21 2008 Ian Kent <ikent@redhat.com> - 5.0.3-3
- catch "-xfn" map type and issue "no supported" message.
- another correction for handling of LDAP base dns with spaces.

* Mon Jan 14 2008 Ian Kent <ikent@redhat.com> - 5.0.3-2
- correct configure test for ldap page control functions.

* Mon Jan 14 2008 Ian Kent <ikent@redhat.com> - 5.0.3-1
- update source to version 5.0.3.

* Fri Dec 21 2007 Ian Kent <ikent@redhat.com> - 5.0.2-25
- Bug 426401: CVE-2007-6285 autofs default doesn't set nodev in /net [rawhide]
  - use mount option "nodev" for "-hosts" map unless "dev" is explicily specified.

* Tue Dec 18 2007 Ian Kent <ikent@redhat.com> - 5.0.2-23
- Bug 397591 SELinux is preventing /sbin/rpc.statd (rpcd_t) "search" to <Unknown> (sysctl_fs_t).
  - prevent fork between fd open and setting of FD_CLOEXEC.

* Thu Dec 13 2007 Ian Kent <ikent@redhat.com> - 5.0.2-21
- Bug 421371: CVE-2007-5964 autofs defaults don't restrict suid in /net [rawhide]
  - use mount option "nosuid" for "-hosts" map unless "suid" is explicily specified.

* Thu Dec  6 2007 Jeremy Katz <katzj@redhat.com> - 1:5.0.2-19
- rebuild for new ldap

* Tue Nov 20 2007 Ian Kent <ikent@redhat.com> - 5.0.2-18
- fix schema selection in LDAP schema discovery.
- check for "*" when looking up wildcard in LDAP.
- fix couple of edge case parse fails of timeout option.
- add SEARCH_BASE configuration option.
- add random selection as a master map entry option.
- re-read config on HUP signal.
- add LDAP_URI, LDAP_TIMEOUT and LDAP_NETWORK_TIMEOUT configuration options.
- fix deadlock in submount mount module.
- fix lack of ferror() checking when reading files.
- fix typo in autofs(5) man page.
- fix map entry expansion when undefined macro is present.
- remove unused export validation code.
- add dynamic logging (adapted from v4 patch from Jeff Moyer).
- fix recursive loopback mounts (Matthias Koenig).
- add map re-load to verbose logging.
- fix handling of LDAP base dns with spaces.
- handle MTAB_NOTUPDATED status return from mount.
- when default master map, auto.master, is used also check for auto_master.
- update negative mount timeout handling.
- fix large group handling (Ryan Thomas).
- fix for dynamic logging breaking non-sasl build (Guillaume Rousse).
- eliminate NULL proc ping for singleton host or local mounts.

* Mon Sep 24 2007 Ian Kent <ikent@redhat.com> - 5.0.2-16
- add descriptive comments to config about LDAP schema discovery.
- work around segfault at exit caused by libxml2.
- fix foreground logging (also fixes shutdown needing extra signal bug).

* Wed Sep 5 2007 Ian Kent <ikent@redhat.com> - 5.0.2-15
- fix LDAP schema discovery.

* Tue Aug 28 2007 Ian Kent <ikent@redhat.com> - 5.0.2-14
- update patch to prevent failure on empty master map.
- if there's no "automount" entry in nsswitch.conf use "files" source.
- add LDAP schema discovery if no schema is configured.

* Wed Aug 22 2007 Ian Kent <ikent@redhat.com> - 5.0.2-13
- fix "nosymlink" option handling and add desription to man page.

* Tue Aug 21 2007 Ian Kent <ikent@redhat.com> - 5.0.2-12
- change random multiple server selection option name to be consistent
  with upstream naming.

* Tue Aug 21 2007 Ian Kent <ikent@redhat.com> - 5.0.2-11
- don't fail on empty master map.
- add support for the "%%" hack for case insensitive attribute schemas.

* Mon Jul 30 2007 Ian Kent <ikent@redhat.com> - 5.0.2-10
- mark map instances stale so they aren't "cleaned" during updates.
- fix large file compile time option.

* Fri Jul 27 2007 Ian Kent <ikent@redhat.com> - 5.0.2-9
- fix version passed to get_supported_ver_and_cost (bz 249574).

* Tue Jul 24 2007 Ian Kent <ikent@redhat.com> - 5.0.2-8
- fix parse confusion between attribute and attribute value.

* Fri Jul 20 2007 Ian Kent <ikent@redhat.com> - 5.0.2-7
- fix handling of quoted slash alone (bz 248943).

* Wed Jul 18 2007 Ian Kent <ikent@redhat.com> - 5.0.2-6
- fix wait time resolution in alarm and state queue handlers (bz 247711).

* Mon Jul 16 2007 Ian Kent <ikent@redhat.com> - 5.0.2-5
- fix mount point directory creation for bind mounts.
- add quoting for exports gathered by hosts map.

* Mon Jun 25 2007 Ian Kent <ikent@redhat.com> - 5.0.2-4
- update multi map nsswitch patch.

* Mon Jun 25 2007 Ian Kent <ikent@redhat.com> - 5.0.2-3
- add missing "multi" map support.
- add multi map nsswitch lookup.

* Wed Jun 20 2007 Ian Kent <ikent@redhat.com> - 5.0.2-2
- include krb5.h in lookup_ldap.h (some openssl doesn't implicitly include it).
- correct initialization of local var in parse_server_string.

* Mon Jun 18 2007 Ian Kent <ikent@redhat.com> - 5.0.2-1
- Update to upstream release 5.0.2.

* Tue Jun 12 2007 Ian Kent <ikent@redhat.com> - 5.0.1-16
- add ldaps support.
  - note: it's no longer possible to have multiple hosts in an ldap map spec.
  - note: to do this you need to rely on the ldap client config.

* Thu Jun 7 2007 Ian Kent <ikent@redhat.com> - 5.0.1-14
- fix deadlock in alarm manager module.

* Sun Jun 3 2007 Ian Kent <ikent@redhat.com> - 5.0.1-12
- correct mistake in logic test in wildcard lookup.

* Mon May 7 2007 Ian Kent <ikent@redhat.com> - 5.0.1-10
- fix master map lexer to admit "." in macro values.

* Tue Apr 17 2007 Ian Kent <ikent@redhat.com> - 5.0.1-9
- upstream fix for filesystem is local check.
- disable exports access control check (bz 203277).
- fix patch to add command option for set a global mount options (bz 214684).

* Mon Apr 16 2007 Ian Kent <ikent@redhat.com> - 5.0.1-8
- add configuration variable to control appending of global options (bz 214684).
- add command option to set a global mount options string (bz 214684).

* Tue Apr 3 2007 Ian Kent <ikent@redhat.com> - 5.0.1-7
- fix "null" domain netgroup match for "-hosts" map.

* Thu Mar 29 2007 Ian Kent <ikent@redhat.com> - 5.0.1-6
- fix directory creation for browse mounts.
- fix wildcard map handling and improve nsswitch source map update.

* Fri Mar 16 2007 Ian Kent <ikent@redhat.com> - 5.0.1-5
- drop "DEFAULT_" prefix from configuration names.
- add option to select replicated server at random (instead of
  ping response time) (bz 227604).
- fix incorrect cast in directory cleanup routines (bz 231864).

* Thu Mar 8 2007 Ian Kent <ikent@redhat.com> - 5.0.1-4
- fixed numeric export match (bz 231188).

* Thu Mar 1 2007 Ian Kent <ikent@redhat.com> - 5.0.1-3
- change file map lexer to allow white-space only blank lines (bz 229434).

* Fri Feb 23 2007 Ian Kent <ikent@redhat.com> - 5.0.1-2
- update "@network" matching patch.

* Thu Feb 22 2007 Ian Kent <ikent@redhat.com> - 5.0.1-1
- update to release tar.
- fix return check for getpwuid_r and getgrgid_r.
- patch to give up trying to update exports list while host is mounted.
- fix to "@network" matching. 
- patch to check for fstab update and retry if not updated.

* Tue Feb 20 2007 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc3.24
- add "condrestart" to init script (bz 228860).
- add "@network" and .domain.name export check.
- fix display map name in mount entry for "-hosts" map.

* Fri Feb 16 2007 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc3.22
- fix localhost replicated mounts not working (bz 208757).

* Wed Feb 14 2007 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc3.20
- correct return status from do_mkdir (bz 223480).

* Sat Feb 10 2007 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc3.18
- update the "task done race" patch to fix a deadlock.
- added URL tag.
- removed obsoletes autofs-ldap.
- replaced init directory paths with %%{_initrddir} macro.

* Fri Feb 9 2007 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc3.17
- make use of spaces and tabs in spec file consistent.
- escape embedded macro text in %%changelog.
- eliminate redundant %%version and %%release.
- remove redundant conditional check from %%clean.
- remove redundant exit from %%preun.
- correct %%defattr spec.
- remove empty %%doc and redundant %%dir misc lines.
- combine program module spec lines into simpler one line form.

* Tue Feb 6 2007 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc3.15
- fix race when setting task done (bz 227268).

* Mon Jan 29 2007 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc3.13
- make double quote handing consistent (at least as much as we can).
- fix handling of trailing white space in wildcard lookup (forward port bz 199720).
- check fqdn of each interface when matching export access list (bz 213700).

* Thu Jan 18 2007 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc3.11
- correct check for busy offset mounts before offset umount (bz 222872).

* Wed Jan 17 2007 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc3.9
- fix another expire regression introduced in the "mitigate manual umount"
  patch (bz 222872).

* Mon Jan 15 2007 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc3.7
- ignore "winbind" if it appears in "automount" nsswitch.conf (bz 214632).

* Wed Jan 10 2007 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc3.5
- remove fullstop from Summary tag.
- change Buildroot to recommended form.
- replace Prereq with Requires.

* Tue Jan 9 2007 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc3.3
- remove redundant rpath link option (prep for move to Extras).

* Tue Jan 9 2007 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc3.1
- consolidate to rc3.
- fix typo in Fix typo in var when removing temp directory (bz 221847).

* Wed Dec 27 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.41
- fix nonstrict multi-mount handling (bz 219383).
- correct detection of duplicate indirect mount entries (bz 220799).

* Thu Dec 14 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.38
- update master map tokenizer to admit "slasify-colons" option.
- update location validation to accept "_" (bz 219445).
- set close-on-exec flag on open sockets (bz 215757).

* Mon Dec 11 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.35
- update "replace-tempnam" patch to create temp files in sane location.

* Mon Dec 11 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.34
- change mount "device" from "automount" to the map name.
- check for buffer overflow in mount_afs.c.
- replace tempnam with mkdtemp.

* Sun Dec 10 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.33
- expand export access checks to include missing syntax options.
- make "-hosts" module try to be sensitive to exports list changes.

* Thu Dec 7 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.32
- remove ability to use multiple indirect mount entries in master
  map (bz 218616).

* Wed Dec 6 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.29
- alter nfs4 host probing to not use portmap lookup and add options
  check for "port=" parameter (bz 208757).
- correct semantics of "-null" map handling (bzs 214800, 208091).

* Sat Nov 25 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.26
- fix parsing of bad mount mount point in master map (bz 215620).
- fix use after free memory access in cache.c and lookup_yp.c (bz 208091).
- eliminate use of pthread_kill to detect task completion (bz 208091).

* Sun Nov 12 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.23
- fix tokenizer to distinguish between global option and dn string (bz 214684).
- fix incorrect return from spawn.

* Wed Nov 8 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.21
- mitigate manual umount of automounts where possible.
- fix multiply recursive bind mounts.
- check kernel module version and require 5.00 or above.
- fix expire regression introduced in the "mitigate manual umount" patch.
- still more on multiply recursive bind mounts.

* Mon Oct 30 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.20
- Update patch for changed semantics of mkdir in recent kernels.
- fix macro table locking (bz 208091).
- fix nsswitch parser locking (bz 208091).
- allow only one master map read task at a time.
- fix misc memory leaks.

* Wed Oct 25 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.19
- deal with changed semantics of mkdir in recent kernels.

* Fri Oct 20 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.16
- fix get_query_dn not looking in subtree for LDAP search (missed
  econd occurance).
- allow additional common LDAP attributes in map dn.
- Resolves: rhbz#205997

* Mon Oct 16 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.13
- fix parsing of numeric host names in LDAP map specs (bz 205997).

* Mon Oct 16 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.12
- fix "-fstype=nfs4" server probing (part 2 of bz 208757).
- set close-on-exec flag on open files where possible (bz 207678).

* Fri Oct 13 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.11
- fix file handle leak in nsswitch parser (bz 207678).
- fix memory leak in mount and expire request processing (bz 207678).
- add additional check to prevent running of cancelled tasks.
- fix potential file handle leakage in rpc_subs.c for some failure
  cases (bz 207678).
- fix file handle leak in included map lookup (bz 207678).

* Sat Oct 7 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.10
- fix get_query_dn not looking in subtree for LDAP search.
- allow syntax "--timeout <secs>" for backward compatibility
  (bz 193948).
- make masked_match independent of hostname for exports comparison
  (bz 209638).

* Thu Oct 5 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.9
- fix "-fstype=nfs4" handling (bz 208757).

* Wed Sep 27 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.8
- review and fix master map options update for map reload.

* Wed Sep 27 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.7
- make default installed master map for /net use "-hosts" instead
  of auto.net.
- fix included map recursive map key lookup.

* Mon Sep 25 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.6
- remove unused option UNDERSCORETODOT from default config files.

* Mon Sep 25 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.5
- fix LDAP lookup delete cache entry only if entry doesn't exist.
- add missing socket close in replicated host check (Jeff Moyer).

* Wed Sep 20 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.4
- fix cache entrys not being cleaned up on submount expire.

* Sun Sep 17 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.3
- fix include check full patch for file map of same name.

* Wed Sep 13 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.2
- fix handling of autofs specific mount options (bz 199777).

* Fri Sep 1 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc2.1
- consolidate to rc2.
- fix colon escape handling.
- fix recusively referenced bind automounts.
- update kernel patches.

* Fri Aug 25 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.17
- fix task cancelation at shutdown (more)
- fix concurrent mount and expire race with nested submounts.

* Sun Aug 20 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.16
- fix included map lookup.
- fix directory cleanup on expire.
- fix task cancelation at shutdown.
- fix included map wild card key lookup.

* Wed Aug 16 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.15
- expire individual submounts.
- add ino_index locking.
- fix nested submount expiring away when pwd is base of submount.
- more expire re-work to cope better with shutdown following cthon tests.
- allow hostname to start with numeric when validating.

* Mon Aug 7 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.14
- remove SIGCHLD handler because it is no longer needed and was
  causing expire problems.
- alter expire locking of multi-mounts to lock sub-tree instead of
  entire tree.
- review verbose message feedback and update.
- correction for expire of multi-mounts.
- spelling corrections to release notes (Jeff Moyer).
- add back sloppy mount option, removed for Connectathon testing.
- disable mtab locking again.

* Fri Aug 4 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.13
- tidy up directory cleanup and add validation check to rmdir_path.

* Fri Aug 4 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.12
- enable mtab locking until I can resolve the race with it.

* Fri Aug 4 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.11
- cthon fix expire of wildcard and program mounts broken by recent
  patches.

* Thu Aug 3 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.10
- cthon corrections for shutdown patch below and fix shutdown expire.

* Wed Aug 2 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.9
- cthon fix some shutdown races.

* Thu Jul 27 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.8
- Fix compile error.

* Thu Jul 27 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.7
- cthon fix expire of various forms of nested mounts.

* Mon Jul 24 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.6
- cthon more parser corrections and attempt to fix multi-mounts
  with various combinations of submounts (still not right).

* Wed Jul 19 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.5
- Add conflicts kernel < 2.6.17.
- Fix submount operation broken by connectathon updates.

* Wed Jul 19 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.4
- Correction to host name validation test for connectathon tests.

* Wed Jul 19 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.3
- More code cleanup and corrections for connectathon tests.

* Wed Jul 19 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.2
- Code cleanup and fixes for connectathon tests.

* Thu Jul 13 2006 Ian Kent <ikent@redhat.com> - 5.0.1-0.rc1.1
- Update version label to avoid package update problems.

* Thu Jul 13 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta6-8
- add cacheing of negative lookups to reduce unneeded map
  lookups (bz 197746 part 2).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:5.0.0_beta6-7.1
- rebuild

* Tue Jul 11 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta6-7
- correct directory cleanup in mount modules.
- merge key and wildcard LDAP query for lookups (bz 197746).

* Sat Jul 8 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta6-6
- correct test for libhesiod.

* Fri Jul 7 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta6-5
- correct auto.net installed as auto.smb.
- update LDAP auth - add autodectect option.

* Wed Jul 5 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta6-4
- correct shutdown log message print.
- correct auth init test when no credentials required.

* Tue Jul 4 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta6-3
- correct test for existence of auth config file.

* Mon Jul 3 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta6-2
- merge LDAP authentication update for GSSAPI (Jeff Moyer).
- update default auth config to add options documenetation (Jeff Moyer).
- workaround segfaults at exit after using GSSAPI library.
- fix not checking return in init_ldap_connection (jeff Moyer).

* Thu Jun 29 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta6-1
- consolidate to beta6, including:
  - mode change update for config file.
  - correction to get_query_dn fix from beta5-4.

* Wed Jun 28 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta5-6
- cleanup defaults_read_config (Jeff Moyer).

* Tue Jun 27 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta5-5
- allow global macro defines to override system macros.
- correct spelling error in default config files missed by
  previous update.
- misc correctness and a memory leak fix.

* Mon Jun 26 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta5-4
- correct spelling error in default config.
- fix default auth config not being installed.
- change LDAP query method as my test db was incorrect.
- change ldap defaults code to handle missing auth config.
- fix mistake in parsing old style LDAP specs.
- update LDAP so that new query method also works for old syntax.

* Fri Jun 23 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta5-3
- lookup_init cleanup and fix missed memory leak.
- use nis map order to check if update is needed.
- fix couple of memory leaks in lookup_yp.c.
- fix pasre error in replicated server module.

* Wed Jun 21 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta5-2
- Add openssl-devel to the BuildRequires, as it is needed for the LDAP
  authentication bitsi also.

* Tue Jun 20 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta5-1
- promote to beta5.

* Tue Jun 20 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta4-14
- fix directory cleanup at exit.

* Mon Jun 19 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta4-13
- Change LDAP message severity from crit to degug (bz# 183893).
- Corrections to INSTALL and README.v5.release.
- Add patch to fix segv on overlength map keys in file maps (Jeff Moter).
- Add patch to restrict scanning of /proc to pid directories only (Jeff Moyer).

* Thu Jun 15 2006 Jeff Moyer <jmoyer@redhat.com> - 5.0.0_beta4-12
- Change BuildPrereq to BuildRequires as per the package guidelines.
- Add libxml2-devel to the BuildRequires, as it is needed for the LDAP
  authentication bits.

* Wed Jun 14 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta4-11
- add export access list matching to "hosts" lookup module (bz # 193585).

* Tue Jun 13 2006 Jeff Moyer <jmoyer@redhat.com> - 5.0.0_beta4-10
- Add a BuildPrereq for cyrus-sasl-devel

* Tue Jun 13 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta4-9
- move autofs4 module loading back to init script (part bz # 194061).

* Mon Jun 12 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta4-8
- fix handling of master map entry update (bz # 193718).
- fix program map handling of invalid multi-mount offsets.

* Sat Jun 10 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta4-7
- fix context init error (introduced by memory leak patch).

* Fri Jun 9 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta4-6
- add free for working var in get_default_logging.
- add inialisation for kver in autofs_point struct.
- fix sources list corruption in check_update_map_sources.
- fix memory leak in walk_tree.
- fix memory leak in rpc_portmap_getport and rpc_ping_proto.
- fix memory leak in initialisation of lookup modules.

* Thu Jun 8 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta4-5
- misc fixes for things found while investigating map re-read problem.

* Wed Jun 7 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta4-4
- check base of offset mount tree is not a mount before umounting
  its offsets.
- fix replicated mount parse for case where last name in list
  fails lookup.
- correct indirect mount expire broken by the wildcard lookup fix.
- fix up multi-mount handling when wildcard map entry present.

* Mon Jun 5 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta4-3
- correct config names in default.c (jpro@bas.ac.uk).

* Mon Jun 5 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta4-2
- re-instate v4 directory cleanup (bz# 193832 again).
- backout master map lookup changes made to beta3.
- change default master map from /etc/auto.master to auto.master
  so that we always use nsswitch to locate master map.
- change default installed master map to include "+auto.master"
  to pickup NIS master map (all bz# 193831 again).

* Fri Jun 2 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta4-1
- update to beta4.
- should address at least bzs 193798, 193770, 193831 and
  possibly 193832.

* Mon May 29 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta3-6
- add back test for nested mount in program map lookup.
  - I must have commented this out for a reason. I guess we'll
    find out soon enough.

* Mon May 29 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta3-5
- fix handling of autofs filesystem mount fail on init.

* Sat May 27 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta3-4
- updated hesiod patch.

* Sat May 27 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta3-3
- update hesiod module (Jeff Moyer).
  - add mutex to protect against overlapping mount requests.
  - update return from mount request to give more sensible NSS_*
    values.

* Fri May 26 2006 Jeff Moyer <jmoyer@redhat.com> - 1:5.0.0_beta3-2
- Fix the install permissions for auto.master and auto.misc.

* Thu May 25 2006 Ian Kent <ikent@redhat.com> - 5.0.0_beta3-1
- update source to version 5.0.0_beta3.
- add patch to remove extra debug print.
- add patch to
  - fix memory alloc error in nis lookup module.
  - add "_" to "." mapname translation to nis lookup module.
- add patch to add owner pid to mount list struct.
- add patch to disable NFSv4 when probing hosts (at least foe now).
- add patch to fix white space handling in replicated server selection code.
- add patch to prevent striping of debug info macro patch (Jeff Moyer).
- add patch to add sanity checks on rmdir_path and unlink (Jeff Moyer).
- add patch to fix e2fsck error code check (Jeff Moyer).

* Tue May 16 2006 Ian Kent <ikent@redhat.com> - 1:4.1.4-23
- add patch to ignore the "bg" and "fg" mount options as they
  aren't relevant for autofs mounts (bz #184386).

* Tue May 2 2006 Ian Kent <ikent@redhat.com> - 1:4.1.4-20
- add patch to use "cifs" instead of smbfs and escape speces
  in share names (bz #163999, #187732).

* Tue Apr 11 2006 Ian Kent <ikent@redhat.com> - 1:4.1.4-18
- Add patch to allow customization of arguments to the
  autofs-ldap-auto-master program (bz #187525).
- Add patch to escap "#" characters in exports from auto.net
  program mount (bz#178304).

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:4.1.4-16.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:4.1.4-16.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Feb 1 2006 Ian Kent <ikent@redhat.com> - 1:4.1.4-16.2
- Add more general patch to translate "_" to "." in map names. (bz #147765)

* Wed Jan 25 2006 Ian Kent <ikent@redhat.com> - 1:4.1.4-16.1
- Add patch to use LDAP_DEPRICATED compile option. (bz #173833)

* Tue Jan 17 2006 Ian Kent <ikent@redhat.com> - 1:4.1.4-16
- Replace check-is-multi with more general multi-parse-fix.
- Add fix for premature return when waiting for lock file.
- Update copyright declaration for reentrant-syslog source.
- Add patch for configure option to disable locking during mount.
  But don't disable locking by default.
- Add ability to handle automount schema used in Sun directory server.
- Quell compiler warning about getsockopt parameter.
- Quell compiler warning about yp_order parameter.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 17 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.4-14
- Removed the /misc entry from the default auto.master.  auto.misc has
  an entry for the cdrom device, and the preferred method of mounting the
  cd is via udev/hal.

* Mon Nov  7 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.4-13
- Changed to sort -k 1, since that should be the same as +0.

* Thu Nov  3 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.4-12
- The sort command no longer accepts options of the form "+0".  This broke
  auto.net, so the option was removed.  Fixes bz #172111.

* Wed Oct 26 2005  <jmoyer@redhat.com> - 1:4.1.4-11
- Check the return code of is_local_addr in get_best_mount. (bz #169523)

* Wed Oct 26 2005  <jmoyer@redhat.com> - 1:4.1.4-10
- Fix some bugs in the parser
- allow -net instead of /etc/auto.net
- Fix a buffer overflow with large key lengths
- Don't allow autofs to unlink files, only to remove directories
- change to the upstream reentrant syslog patch from the band-aid deferred
  syslog patch.
- Get rid of the init script patch that hard-coded the release to redhat.
  This should be handled properly by all red hat distros.

* Wed May  4 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.4-8
- Add in the deferred syslog patch.  This fixes a hung automounter issue
  related to unsafe calls to syslog in signal handler context.

* Tue May  3 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.4-7
- I reversed the checking for multimount entries, breaking those configs!
  This update puts the code back the way it was before I broke it.

* Tue Apr 26 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.4-6
- Fix a race between mounting a share and updating the cache in the parent
  process.  If the mount completed first, the parent would not expire the
  stale entry, leaving it first on the list.  This causes map updates to not
  be recognized (well, worse, they are recognized after the first expire, but
  not subsequent ones).  Fixes a regression, bug #137026 (rhel3 bug).

* Fri Apr 15 2005 Chris Feist <cfeist@redhat.com> - 1:4.1.4-5
- Fixed regression with -browse not taking effect.

* Wed Apr 13 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.4-4
- Finish up with the merge breakage.
- Temporary fix for the multimount detection code.  It seems half-baked.

* Wed Apr 13 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.4-3
- Fix up the one-auto-master patch.  My "improvements" had side-effects.

* Wed Apr 13 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.4-2
- Import 4.1.4 and merge.

* Mon Apr  4 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-123
- Add in an error case that was omitted in the multi-over patch.
- Update our auto.net to reflect the changes that went into 4.1.4_beta2.
  This fixes a problem seen by at least one customer where a malformed entry
  appeared first in the multimount list, thus causing the entire multimount
  to be ignored.  This new auto.net places that entry at the end, purely by
  luck, but it fixes the problem in this one case.

* Thu Mar 31 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-119
- Merge in the multi-over patch.  This resolves an issue whereby multimounts
  (such as those used for /net) could be processed in the wrong order,
  resulting in directories not showing up in a multimount tree.  The fix
  is to process these directories in order, shortest to longer path.

* Wed Mar 23 2005 Chris Feist <cfeist@redhat.com> - 1:4.1.3-115
- Fixed regression causing any entries after a wildcard in an
  indirect map to be ignored. (bz #151668).
- Fixed regression which caused local hosts to be mount instead
  of --bind local directories. (bz #146887)

* Thu Mar 17 2005 Chris Feist <cfeist@redhat.com> - 1:4.1.3-111
- Fixed one off bug in the submount-variable-propagation patch.
  (bz #143074)
- Fixed a bug in the init script which wouldn't find the -browse
  option if it was preceded by another option. (fz #113494)

* Mon Feb 28 2005 Chris Feist <cfeist@redhat.com> - 1:4.1.3-100
- When using ldap if auto.master doesn't exist we now check for auto_master.
  Addresses bz #130079
- When using an auto.smb map we now remove the leading ':' from the path which
  caused mount to fail in the past.  Addresses bz #147492
- Autofs now checks /etc/nsswitch.conf to determine in what order files & nis
  are checked when looking up autofs submount maps which don't specify a
  maptype.  Addresses IT #57612.

* Mon Feb 14 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-99
- Change Copyright to License in the spec file so it will build.

* Fri Feb 11 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-98
- Program maps can repeat the last character of output.  Fix this.  
  Addresses bz #138606
- Return first entry when there are duplicate keys in a map.  Addresses
  bz #140108.
- Propagate custom map variables to submounts.  Fixes bz #143074.
- Create a sysconfig variable to control whether we source only one master
  map (the way sun does), or source all maps found (which is the default for
  backwards compatibility).  Addresses bz #143126.
- Revised version of the get_best_mount patch. (#146887) cfeist@redhat.com
  The previous patch introduced a regression.  Non-replicated mounts would
  not have the white space stripped from the entry and the mount would fail.
- Handle comment characters in the middle of the automount line in
  /etc/nsswitch.conf.  Addresses bz #127457.

* Wed Feb  2 2005 Chris Feist <cfeist@redhat.com> - 1:4.1.3-94
- Stop automount from pinging hosts if there is only one host (#146887)

* Wed Feb  2 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-90
- Fix potential double free in cache_release.  This bug showed up in a
  multi-map setup.  Two calls to cache_release would result in a SIGSEGV,
  and the automount process would never exit.

* Mon Jan 24 2005 Chris Feist <cfeist@redhat.com> - 1:4.3-82
- Fixed documentation so users know that any local mounts override
  any other weighted mount.

* Mon Jan 24 2005 Chris Feist <cfeist@redhat.com> - 1:4.3-80
- Added a variable to determine if we created the directory or not
  so we don't accidently remove a directory that we didn't create when
  we stop autofs.  (bz #134399)

* Tue Jan 11 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-76
- Fix the large program map patch.

* Tue Jan 11 2005 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-75
- Fix some merging breakages that caused the package not to build.

* Thu Jan  6 2005  <jmoyer@redhat.com> - 1:4.1.3-74
- Add in the map expiry patch
- Bring in other patches that have been committed to other branches. This 
  version should now contain all fixes we have to date
- Merge conflicts due to map expiry changes

* Fri Nov 19 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-57
- Pass a socket into clntudp_bufcreate so that we don't use up additional 
  reserved ports.  This patch, along with the socket leak fix, addresses
  bz #128966.

* Wed Nov 17 2004  <jmoyer@redhat.com> - 1:4.1.3-56
- Somehow the -browse patch either didn't get committed or got reverted.
  Fixed.

* Tue Nov 16 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-55
- Fix program maps so that they can have gt 4k characters. (Neil Horman)
  Addresses bz #138994.
- Add a space after the colon here "Starting automounter:" in init script.
  Fixes bz #138513.

* Mon Nov 15 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-53
- Make autofs understand -[no]browse.  Addresses fz #113494.

* Thu Nov 11 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-48
- Fix the umount loop device function in the init script.

* Wed Oct 27 2004 Chris Feist <cfeist@redhat.com> - 1:4.1.3-34
- Added a patch to fix the automounter failing on ldap maps
  when it couldn't get the whole map.  (ie. when the search
  limit was lower than the number of results)

* Thu Oct 21 2004 Chris Feist <cfeist@redhat.com> - 1:4.1.3-32
- Fixed the use of +ypmapname so the maps included with +ypmapname
  are used in the correct order.  (In the past the '+' entries
  were always processed after local entries.)

* Thu Oct 21 2004 Chris Feist <cfeist@redhat.com> - 1:4.1.3-31
- Fixed the duplicate map detection code to detect if maps try
  to mount on top of existing maps. 

* Wed Oct 20 2004 Chris Feist <cfeist@redhat.com> - 1:4.1.3-29
- Fixed a problem with backwards compatability. Specifying local
  maps without '/etc/' prepended to them now works. (bz #136038)

* Fri Oct 15 2004 Chris Feist <cfeist@redhat.com> - 1:4.1.3-28
- Fixed a bug which caused directories to never be unmounted. (bz #134403)

* Thu Oct 14 2004 Chris Feist <cfeist@redhat.com> - 1:4.1.3-27
- Fixed an error in the init script which caused duplicate entries to be
  displayed when asking for autofs status.

* Fri Oct  1 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-22
- Comment out map expiry (and related) patch for an FC3 build.

* Thu Sep 23 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-21
- Make local options apply to all maps in a multi-map entry.

* Tue Sep 21 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-20
- Merged my and Ian's socket leak fixes into one, smaller patch. Only
  partially addresses bz #128966.
- Fix some more echo lines for internationalization. bz #77820
- Revert the only one auto.master patch until we implement the +auto_master
  syntax.  Temporarily addresses bz #133055.

* Thu Sep  2 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-18
- Umount loopback filesystems under automount points when stopping the 
  automounter.
- Uncomment the map expiry patch.
- change a close to an fclose in lookup_file.c

* Tue Aug 31 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-17
- Add patch to support parsing nsswitch.conf to determine map sources.
- Disable this patch, and Ian's map expiry patch for a FC build.

* Tue Aug 24 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-16
- Version 3 of Ian's map expiry changes.

* Wed Aug 18 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-15
- Fix a socket leak in the rpc_subs, causing mounts to fail since we are 
  running out of port space fairly quickly.

* Wed Aug 18 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-14
- New map expiry patch from Ian.
- Fix a couple signal races.  No known problem reports of these, but they
  are holes, none-the-less.

* Tue Aug 10 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-13
- Only read one auto.master map (instead of concatenating all found sources).
- Uncomment Ian's experimental mount expiry patch.

* Fri Aug  6 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-12
- Add a sysconfig entry to disable direct map support, and set this to 
  1 by default.
- Disable the beta map expiry logic so I can build into a stable distro.
- Add defaults for all of the sysconfig variables to the init script so 
  we don't trip over user errors (i.e. deleting /etc/sysconfig/autofs).

* Wed Aug  4 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-11
- Add beta map expiry code for wider testing. (Ian Kent)
- Fix check for ghosting option.  I forgot to check for it in DAEMONOPTIONS.
- Remove STRIPDASH from /etc/sysconfig/autofs

* Mon Jul 12 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-10
- Add bad chdir patch from Ian Kent.
- Add a typo fix for the mtab lock file.
- Nuke the stripdash patch.  It didn't solve a problem.

* Tue Jun 22 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-9
- Bump revison for inclusion in RHEL 3.

* Mon Jun 21 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-8
- Change icmp ping to an rpc ping.  (Ian Kent)
- Fix i18n patch
  o Remove the extra \" from one echo line.
  o Use echo -e if we are going to do a \n in the echo string.

* Mon Jun 21 2004 Alan Cox <alan@redhat.com>
- Fixed i18n bug #107463

* Mon Jun 21 2004 Alan Cox <alan@redhat.com>
- Fixed i18n bug #107461

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jun  5 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-4
- Perform an icmp ping request before rpc_pings, since the rpc clnt_create
  function has a builtin default timeout of 60 seconds.  This could result
  in a long delay when a server in a replicated mount setup is down.
- For non-replicated server entries, ping a host before attempting to mount.
  (Ian Kent)
- Change to %%configure.
- Put version-release into .version to allow for automount --version to
  print exact info.
- Nuke my get-best-mount patch which always uses the long timeout.  This
  should no longer be needed.
- Put name into changelog entries to make them consistent.  Add e:n-v-r
  into Florian's entry.
- Stop autofs before uninstalling

* Sat Jun 05 2004 Florian La Roche <Florian.LaRoche@redhat.de> - 1:4.1.3-3
- add a preun script to remove autofs

* Tue Jun  1 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-2
- Incorporate patch from Ian which fixes an infinite loop seen by those
  running older versions of the kernel patches (triggered by non-strict mounts
  being the default).

* Tue Jun  1 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.3-1
- Update to upstream 4.1.3.

* Thu May  6 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.2-6
- The lookup_yp module only dealt with YPERR_KEY, all other errors were 
  treated as success.  As a result, if the ypdomain was not bound, the 
  subprocess that starts mounts would SIGSEGV.  This is now fixed.
- Option parsing in the init script was not precise enough, sometimes matching
  filesystem options to one of --ghost, --timeout, --verbose, or --debug.  
  The option-parsing patch addresses this issue by making the regexp's much
  more precise.
- Ian has rolled a third version of the replicated mount fixes.

* Tue May  4 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.2-5
- Ian has a new fix for replicated server and multi-mounts.  Updated the 
  patch for testing.  Still beta.  (Ian Kent)

* Mon May  3 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.2-4
- Fix broken multi-mounts.  test patch.  (Ian Kent)

* Tue Apr 20 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.2-3
- Fix a call to spawnl which forgot to specify a lock file. (nphilipp)

* Wed Apr 14 2004  <jmoyer@redhat.com> - 1:4.1.2-2
- Pass --libdir= to ./configure so we get this right on 64 bit platforms that 
  support backwards compat.

* Wed Apr 14 2004  Jeff Moyer <jmoyer@redhat.com> - 1:4.1.2-1
- Change hard-coded paths in the spec file to the %%{_xxx} variety.
- Update to upstream 4.1.2.
- Add a STRIPDASH option to /etc/sysconfig/autofs which allows for
  compatibility with the Sun automounter options specification syntax in
  auto.master.  See /etc/sysconfig/autofs for more information.  Addresses
  bug 113950.

* Tue Apr  6 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.1-6
- Add the /etc/sysconfig/autofs file, and supporting infrastructure in 
  the init script.
- Add support for UNDERSCORE_TO_DOT for those who want it.
- We no longer own /net.  Move it to the filesystem package.

* Tue Mar 30 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.1-5
- Clarify documentation on direct maps.
- Send automount daemons a HUP signal during reload.  This tells them to 
  re-read maps (otherwise they use a cached version.  Patch from the autofs
  maintainer.

* Mon Mar 22 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.1-4
- Fix init script to print out failures where appropriate.
- Build the automount daemon as a PIE.

* Thu Mar 18 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.1-3
- Fix bug in get_best_mount, whereby if there is only one option, we 
  choose nothing.  This is primarily due to the fact that we pass 0 in to
  the get_best_mount function for the long timeout parameter.  So, we
  timeout trying to contact our first and only server, and never retry.

* Thu Mar 18 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.1-2
- Prevent startup if a mountpoint is already mounted.

* Thu Mar 18 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.1-1
- Update to 4.1.1, as it fixes problems with wildcards that people are 
  seeing quite a bit.

* Wed Mar 17 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.0-8
- Fix ldap init code to parse server name and options correctly.

* Tue Mar 16 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.0-7
- Moved the freeing of ap.path to cleanup_exit, as we would otherwise 
  reference an already-freed variable.

* Mon Mar 15 2004 Jeff Moyer <jmoyer@redhat.com> - 1:4.1.0-6
- add %%config(noreplace) for auto.* config files.

* Wed Mar 10 2004 Jeff Moyer <jmoyer@redhat.com> 1:4.1.0-5
- make the init script only recognize redhat systems.  Nalin seems to remember
  some arcane build system error that can be caused if we don't do this.

* Wed Mar 10 2004 Jeff Moyer <jmoyer@redhat.com> 1:4.1.0-4
- comment out /net and /misc from the default auto.master.  /net is important
  since in a default shipping install, we can neatly co-exist with amd.

* Wed Mar 10 2004 Jeff Moyer <jmoyer@redhat.com> 1:4.1.0-3
- Ported forward Red Hat's patches from 3.1.7 that were not already present
  in 4.1.0.
- Moving autofs from version 3.1.7 to 4.1.0

* Mon Sep 29 2003 Ian Kent <raven@themaw.net>
- Added work around for O(1) patch oddity.

* Sat Aug 16 2003 Ian Kent <raven@themaw.net>
- Fixed tree mounts.
- Corrected transciption error in autofs4-2.4.18 kernel module

* Sun Aug 10 2003 Ian Kent <raven@themaw.net>
- Checked and merged most of the RedHat v3 patches
- Fixed kernel module handling wu-ftpd login problem (again)

* Thu Aug 7 2003 Ian Kent <raven@themaw.net>
- Removed ineffective lock stuff
- Added -n to bind mount to prevent mtab update error
- Added retry to autofs umount to clean matb after fail
- Redirected messages from above to debug log and added info message
- Fixed autofs4 module reentrancy, pwd and chroot handling

* Wed Jul 30 2003 Ian Kent <raven@themaw.net>
- Fixed autofs4 ghosting patch for 2.4.19 and above (again)
- Fixed autofs directory removal on failure of autofs mount
- Fixed lock file wait function overlapping calls to (u)mount

* Sun Jul 27 2003 Ian Kent <raven@themaw.net>
- Implemented LDAP direct map handling for nisMap and automountMap schema
- Fixed autofs4 ghosting patch for 2.4.19 and above (again)
- Added locking to fix overlapping internal calls to (u)mount 
- Added wait for mtab~ to improve tolerance of overlapping external calls to (u)mount
- Fixed ghosted directory removal after failed mount attempt

* Wed May 28 2003 Ian Kent <raven@themaw.net>
- Cleaned up an restructured my added code
- Corrected ghosting problem with 2.4.19 and above
- Added autofs4 ghosting patch for 2.4.19 and above
- Implemented HUP signal to force update of ghosted maps

* Sat Mar 23 2002 Ian Kent <ian.kent@pobox.com>
- Add patch to implement directory ghosting and direct mounts
- Add patch to for autofs4 module to support ghosting

* Wed Jan 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- use -fPIC instead of -fpic for modules and honor other RPM_OPT_FLAGS

* Tue Feb 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable hesiod support over libbind

* Fri Aug 13 1999 Cristian Gafton <gafton@redhat.com>
- add patch from rth to avoid an infinite loop
