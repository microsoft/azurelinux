# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		fuse
Version:	2.9.9
Release: 25%{?dist}
Summary:	File System in Userspace (FUSE) v2 utilities
License:	GPL-1.0-or-later
URL:		http://fuse.sf.net
Source0:	https://github.com/libfuse/libfuse/releases/download/%{name}-%{version}.tar.gz

Patch1: fuse2-0001-More-parentheses.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=970768
Patch2: fuse2-0002-add-fix-for-namespace-conflict-in-fuse_kernel.h.patch
# https://github.com/libfuse/libfuse/commit/4f8f034a8969a48f210bf00be78a67cfb6964c72
# backported for fuse2
Patch3: fuse2-0003-make-buffer-size-match-kernel-max-transfer-size.patch
# https://bugzilla.redhat.com/1694552#c7
# https://github.com/libfuse/libfuse/pull/392
# backported for fuse2
Patch4: fuse2-0004-Whitelist-SMB2-found-on-some-NAS-devices.patch
# cherry-picked from upstream
Patch5:	fuse2-0005-Whitelist-UFSD-backport-to-2.9-branch-452.patch
# cherry-picked from upstream
Patch6: fuse2-0006-Correct-errno-comparison-571.patch
# cherry-picked from upstream
# https://bugzilla.redhat.com/show_bug.cgi?id=1984776
Patch7: fuse2-0007-util-ulockmgr_server.c-conditionally-define-closefro.patch

Requires:	which
Conflicts:	filesystem < 3
BuildRequires:	libselinux-devel
BuildRequires:	autoconf, automake, libtool, gettext-devel, make
BuildRequires:  systemd-udev
# fuse-common 3.4.2-3 and earlier included man pages
Requires:       fuse-common >= 3.4.2-4

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE v2 userspace tools to
mount a FUSE filesystem.

%package libs
Summary:	File System in Userspace (FUSE) v2 libraries
License:	LGPL-2.1-or-later
Conflicts:	filesystem < 3

%description libs
Devel With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE v2 libraries.

%package devel
Summary:	File System in Userspace (FUSE) v2 devel files
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pkgconfig
License:	LGPL-2.1-or-later
Conflicts:	filesystem < 3

%description devel
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains development files (headers,
pgk-config) to develop FUSE v2 based applications/filesystems.

%prep
%autosetup -p 1

export ACLOCAL_PATH=/usr/share/gettext/m4/
# ./makeconf.sh
#disable device creation during build/install
sed -i 's|mknod|echo Disabled: mknod |g' util/Makefile.in
autoreconf -ivf

%build
# Can't pass --disable-static here, or else the utils don't build
export MOUNT_FUSE_PATH="%{_sbindir}"
CFLAGS="%{optflags} -D_GNU_SOURCE" %configure
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/%{_libdir}/pkgconfig
install -m 0755 lib/.libs/libfuse.so.%{version} %{buildroot}/%{_libdir}
install -m 0755 lib/.libs/libulockmgr.so.1.0.1 %{buildroot}/%{_libdir}
install -p fuse.pc %{buildroot}/%{_libdir}/pkgconfig/
mkdir -p %{buildroot}/%{_bindir}
install -m 0755 util/fusermount %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sbindir}
install -m 0755 util/mount.fuse %{buildroot}/%{_sbindir}
install -m 0755 util/ulockmgr_server %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_includedir}/fuse
install -p include/old/fuse.h %{buildroot}/%{_includedir}/
install -p include/ulockmgr.h %{buildroot}/%{_includedir}/
for i in cuse_lowlevel.h fuse_common_compat.h fuse_common.h fuse_compat.h fuse.h fuse_lowlevel_compat.h fuse_lowlevel.h fuse_opt.h; do
	install -p include/$i %{buildroot}/%{_includedir}/fuse/
done
mkdir -p %{buildroot}/%{_mandir}/man1/
cp -a doc/fusermount.1 doc/ulockmgr_server.1 %{buildroot}/%{_mandir}/man1/
mkdir -p %{buildroot}/%{_mandir}/man8/
cp -a doc/mount.fuse.8 %{buildroot}/%{_mandir}/man8/
pushd %{buildroot}/%{_libdir}
ln -s libfuse.so.%{version} libfuse.so.2
ln -s libfuse.so.%{version} libfuse.so
ln -s libulockmgr.so.1.0.1 libulockmgr.so.1
ln -s libulockmgr.so.1.0.1 libulockmgr.so
popd

# Get rid of static libs
rm -f %{buildroot}/%{_libdir}/*.a

%ldconfig_scriptlets libs

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README.md README.NFS
%{_sbindir}/mount.fuse
%attr(4755,root,root) %{_bindir}/fusermount
%{_bindir}/ulockmgr_server
%{_mandir}/man1/*
%{_mandir}/man8/*

%files libs
%license COPYING.LIB
%{_libdir}/libfuse.so.*
%{_libdir}/libulockmgr.so.*

%files devel
%{_libdir}/libfuse.so
%{_libdir}/libulockmgr.so
%{_libdir}/pkgconfig/fuse.pc
%{_includedir}/fuse.h
%{_includedir}/ulockmgr.h
%{_includedir}/fuse

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 03 2023 Pavel Reichl <preichl@redhat.com> - 2.9.9-18
- Convert License tag to SPDX format

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Peter Lemenkov <lemenkov@gmail.com> - 2.9.9-13
- Fix FTBFS in Rawhide (rhbz#1984776)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 01 2019 Dave Dykstra <dwd@fedoraproject.org> - 2.9.9-7
- Update the Requires: fuse-common >= version to 3.4.2-4 because
  fuse-common > 3.4.2-3 is insufficient to force the new version

* Wed May 01 2019 Dave Dykstra <dwd@fedoraproject.org> - 2.9.9-6
- Fix name of libfuse.so.2

* Wed May 01 2019 Dave Dykstra <dwd@fedoraproject.org> - 2.9.9-5
- Update the Requires: fuse-common > version to 3.4.2-3

* Wed May 01 2019 Dave Dykstra <dwd@fedoraproject.org> - 2.9.9-4
- Separate fuse3 out into its own package

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 2.9.9-3
- Rebuild with Meson fix for #1699099

* Thu Apr 04 2019 Peter Lemenkov <lemenkov@gmail.com> - 2.9.9-2
- Whitelist SMB2 (rhbz#1694552)

* Mon Mar 25 2019 Tom Callaway <spot@fedoraproject.org> - 2.9.9-1
- update fuse to 2.9.9
- update fuse3 to 3.4.2

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.9.7-16
- Rebuild for tinyxml2 7.x

* Fri Nov 09 2018 Dan Horák <dan[at]danny.cz> - 2.9.7-15
- backport buffer-size patch to fuse2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 14 2018 Tom Callaway <spot@fedoraproject.org> - 2.9.7-13
- update fuse3 to 3.2.3

* Mon Apr  2 2018 Tom Callaway <spot@fedoraproject.org> - 2.9.7-12
- update fuse3 to 3.2.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 16 2017 Tom Callaway <spot@fedoraproject.org> 2.9.7-10
- update fuse3 to 3.2.1

* Mon Aug  7 2017 Tom Callaway <spot@fedoraproject.org> 2.9.7-9
- update fuse3 to 3.1.1

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Fri Jul 28 2017 Tom Callaway <spot@fedoraproject.org> - 2.9.7-7
- use -D_FILE_OFFSET_BITS=64 to force off_t to be 64bit on 32bit arches

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Tom Callaway <spot@fedoraproject.org> - 3.1.0-5
- update to 3.1.0

* Thu Jun  1 2017 Tom Callaway <spot@fedoraproject.org> - 3.0.2-4
- update to 3.0.2

* Sun Mar 26 2017 Tom Callaway <spot@fedoraproject.org> - 3.0.0-3
- update release to 3 to make clean upgrade

* Tue Mar 21 2017 Tom Callaway <spot@fedoraproject.org> - 3.0.0-1
- update to 3.0.0
- split out fuse3 packages

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jul  6 2016 Tom Callaway <spot@fedoraproject.org> - 2.9.7-1
- update to 2.9.7

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 08 2015 Adam Williamson <awilliam@redhat.com> - 2.9.4-3
- backport patch allowing setting SELinux context on FUSE mounts

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 Tom Callaway <spot@fedoraproject.org> 2.9.4-1
- update to 2.9.4
- fixes CVE-2015-3202

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul  6 2013 Tom Callaway <spot@fedoraproject.org> - 2.9.3-1
- update to 2.9.3

* Wed Jun 26 2013 Tom Callaway <spot@fedoraproject.org> - 2.9.2-4
- add fix for namespace conflict in fuse_kernel.h

* Sat May 18 2013 Peter Lemenkov <lemenkov@gmail.com> - 2.9.2-3
- Removed pre-F12 stuff
- Dropped ancient dependency on initscripts and chkconfig

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Adam Jackson <ajax@redhat.com>
- Remove ancient Requires: kernel >= 2.6.14, FC6 was 2.6.18.

* Tue Oct 23 2012 Tom Callaway <spot@fedoraproject.org> - 2.9.2-1
- update to 2.9.2

* Tue Aug 28 2012 Tom Callaway <spot@fedoraproject.org> - 2.9.1-1
- update to 2.9.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 16 2012 Peter Lemenkov <lemenkov@gmail.com> - 2.8.7-1
- Ver. 2.8.7

* Sun Apr 15 2012 Kay Sievers <kay@redhat.com> - 2.8.6-4
- remove needless udev rule

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 2.8.6-3
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.8.6-1
- Ver. 2.8.6
- Dropped patch 3 - fixed upstream

* Thu Mar 03 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.8.5-5
- Use noreplace for /etc/fuse.conf

* Tue Feb 15 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.8.5-4
- Provide /etc/fuse.conf (see rhbz #292811)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 27 2010 Peter Lemenkov <lemenkov@gmail.com> 2.8.5-2
- Fixed rhbz #622255

* Tue Oct 26 2010 Peter Lemenkov <lemenkov@gmail.com> 2.8.5-1
- Ver. 2.8.5

* Tue Jun  8 2010 Peter Lemenkov <lemenkov@gmail.com> 2.8.4-1
- Ver. 2.8.4
- CVE-2009-3297 patch dropped (merged upstream)

* Tue Jan 26 2010 Peter Lemenkov <lemenkov@gmail.com> 2.8.1-4
- Fixed CVE-2009-3297 (rhbz #558833)

* Thu Nov 19 2009 Peter Lemenkov <lemenkov@gmail.com> 2.8.1-3
- Fixed udev rules (bz# 538606)

* Thu Nov 19 2009 Peter Lemenkov <lemenkov@gmail.com> 2.8.1-2
- Removed support for MAKEDEV (bz# 511220)

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> 2.8.1-1
- Ver. 2.8.1

* Wed Aug 19 2009 Peter Lemenkov <lemenkov@gmail.com> 2.8.0-1
- Ver. 2.8.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Peter Lemenkov <lemenkov@gmail.com> 2.7.4-2
- Fixed BZ#479581

* Sat Aug 23 2008 Peter Lemenkov <lemenkov@gmail.com> 2.7.4-1
- Ver. 2.7.4

* Sat Jul 12 2008 Peter Lemenkov <lemenkov@gmail.com> 2.7.3-3
- Fixed initscripts (BZ#441284)

* Thu Feb 28 2008 Peter Lemenkov <lemenkov@gmail.com> 2.7.3-2
- Fixed BZ#434881

* Wed Feb 20 2008 Peter Lemenkov <lemenkov@gmail.com> 2.7.3-1
- Ver. 2.7.3
- Removed usergroup fuse
- Added chkconfig support (BZ#228088)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.7.2-2
- Autorebuild for GCC 4.3

* Mon Jan 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.2-1
- bump to 2.7.2
- fix license tag

* Sun Nov  4 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-9
- fix initscript to work with chkconfig

* Mon Oct  1 2007 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-8
- Added Require: which (BZ#312511)

* Fri Sep 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-7
- revert udev rules change

* Thu Sep 20 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-6
- change udev rules so that /dev/fuse is chmod 666 (bz 298651)

* Wed Aug 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-5
- fix open issue (bz 265321)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.7.0-4
- Rebuild for selinux ppc32 issue.

* Sun Jul 22 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-3
- put pkgconfig file in correct place
- enable compat symlinks for files in /bin

* Sat Jul 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.7.0-2
- redefine exec_prefix to /
- redefine bindir to /bin
- redefine libdir to %%{_lib}
- don't pass --disable-static to configure
- manually rm generated static libs

* Wed Jul 18 2007 Peter Lemenkov <lemenkov@gmail.com> 2.7.0-1
- Version 2.7.0
- Redefined exec_prefix due to demands from NTFS-3G

* Wed Jun  6 2007 Peter Lemenkov <lemenkov@gmail.com> 2.6.5-2
- Add BR libselinux-devel (bug #235145)
- Config files properly marked as config (bug #211122)

* Sat May 12 2007 Peter Lemenkov <lemenkov@gmail.com> 2.6.5-1
- Version 2.6.5

* Thu Feb 22 2007 Peter Lemenkov <lemenkov@gmail.com> 2.6.3-2
- Fixed bug #229642

* Wed Feb  7 2007 Peter Lemenkov <lemenkov@gmail.com> 2.6.3-1
* Ver. 2.6.3

* Tue Dec 26 2006 Peter Lemenkov <lemenkov@gmail.com> 2.6.1-1
- Ver. 2.6.1

* Sat Nov 25 2006 Peter Lemenkov <lemenkov@gmail.com> 2.6.0-2
- fixed nasty typo (see bug #217075)

* Fri Nov  3 2006 Peter Lemenkov <lemenkov@gmail.com> 2.6.0-1
- Ver. 2.6.0

* Sun Oct 29 2006 Peter Lemenkov <lemenkov@gmail.com> 2.5.3-5
- Fixed udev-rule again

* Sat Oct  7 2006 Peter Lemenkov <lemenkov@gmail.com> 2.5.3-4
- Fixed udev-rule

* Tue Sep 12 2006 Peter Lemenkov <lemenkov@gmail.com> 2.5.3-3%{?dist}
- Rebuild for FC6

* Wed May 03 2006 Peter Lemenkov <lemenkov@newmail.ru> 2.5.3-1%{?dist}
- Update to 2.5.3

* Thu Mar 30 2006 Peter Lemenkov <lemenkov@newmail.ru> 2.5.2-4%{?dist}
- rebuild

* Mon Feb 13 2006 Peter Lemenkov <lemenkov@newmail.ru> - 2.5.2-3
- Proper udev rule

* Mon Feb 13 2006 Peter Lemenkov <lemenkov@newmail.ru> - 2.5.2-2
- Added missing requires

* Tue Feb 07 2006 Peter Lemenkov <lemenkov@newmail.ru> - 2.5.2-1
- Update to 2.5.2
- Dropped fuse-mount.fuse.patch

* Wed Nov 23 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.2-1
- Use dist

* Wed Nov 23 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.2-1
- Update to 2.4.2 (solves CVE-2005-3531)
- Update README.fedora

* Sat Nov 12 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.1-3
- Add README.fedora
- Add hint to README.fedora and that you have to be member of the group "fuse"
  in the description
- Use groupadd instead of fedora-groupadd

* Fri Nov 04 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.1-2
- Rename packages a bit
- use makedev.d/40-fuse.nodes
- fix /sbin/mount.fuse
- Use a fuse group to restict access to fuse-filesystems

* Fri Oct 28 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.4.1-1
- Initial RPM release.
