Summary:        Linux NTFS userspace driver
Name:           ntfs-3g
Version:        2022.10.3
Release:        2%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.tuxera.com/company/open-source/
Source0:        https://tuxera.com/opensource/%{name}_ntfsprogs-%{version}.tgz
Patch0:         ntfs-3g_ntfsprogs-2011.10.9-RC-ntfsck-unsupported-return-0.patch
Patch1:         CVE-2023-52890.patch

BuildRequires:  fuse-devel
BuildRequires:  gnutls-devel
BuildRequires:  libattr-devel
BuildRequires:  libconfig-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libtool
BuildRequires:  libuuid-devel

Recommends:     ntfs-3g-system-compression

Requires:       %{name}-libs = %{version}-%{release}
Requires:       fuse

Provides:       ntfsprogs-fuse = %{version}-%{release}
Provides:       fuse-ntfs-3g = %{version}-%{release}

%description
NTFS-3G is a stable, open source, GPL licensed, POSIX, read/write NTFS
driver for Linux and many other operating systems. It provides safe
handling of the Windows XP, Windows Server 2003, Windows 2000, Windows
Vista, Windows Server 2008 and Windows 7 NTFS file systems. NTFS-3G can
create, remove, rename, move files, directories, hard links, and streams;
it can read and write normal and transparently compressed files, including
streams and sparse files; it can handle special files like symbolic links,
devices, and FIFOs, ACL, extended attributes; moreover it provides full
file access right and ownership support.

%package devel
Summary:        Development files and libraries for ntfs-3g

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkg-config

Provides:       ntfsprogs-devel = %{version}-%{release}

%description devel
Headers and libraries for developing applications that use ntfs-3g
functionality.

%package libs
Summary:        Runtime libraries for ntfs-3g

%description libs
Libraries for applications to use ntfs-3g functionality.

%package -n ntfsprogs
Summary:        NTFS filesystem libraries and utilities

%description -n ntfsprogs
The ntfsprogs package currently consists of a library and utilities such as
mkntfs, ntfscat, ntfsls, ntfsresize, and ntfsundelete (for a full list of
included utilities see man 8 ntfsprogs after installation).

%prep
%autosetup -n %{name}_ntfsprogs-%{version} -p1

%build
CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64"
%configure \
	--disable-static \
	--disable-ldconfig \
	--with-fuse=external \
	--exec-prefix=/ \
	--enable-posix-acls \
	--enable-xattr-mappings \
	--enable-crypto \
	--enable-extras \
	--enable-quarantined

%make_build LIBTOOL=%{_bindir}/libtool

%install
%make_install LIBTOOL=%{_bindir}/libtool

find %{buildroot} -type f -name "*.la" -delete -print
rm -rf %{buildroot}%{_libdir}/*.a

rm -rf %{buildroot}/%{_sbindir}/mount.ntfs-3g
cp -a %{buildroot}/%{_bindir}/ntfs-3g %{buildroot}/%{_sbindir}/mount.ntfs-3g

# Actually make some symlinks for simplicity...
# ... since we're obsoleting ntfsprogs-fuse
pushd %{buildroot}/%{_bindir}
ln -s ntfs-3g ntfsmount
popd
pushd %{buildroot}/%{_sbindir}
ln -s mount.ntfs-3g mount.ntfs-fuse
# And since there is no other package in Fedora that provides an ntfs
# mount...
ln -s mount.ntfs-3g mount.ntfs
# Need this for fsck to find it
ln -s ../bin/ntfsck fsck.ntfs
popd

mv %{buildroot}/sbin/* %{buildroot}/%{_sbindir}
rmdir %{buildroot}/sbin

# We get this on our own, thanks.
rm -rf %{buildroot}%{_defaultdocdir}/%{name}/README

%ldconfig_scriptlets libs

%files
%doc AUTHORS ChangeLog CREDITS NEWS README
%license COPYING
%{_sbindir}/mount.ntfs
%{_sbindir}/mount.ntfs-3g
%{_sbindir}/mount.ntfs-fuse
%{_sbindir}/mount.lowntfs-3g
%{_bindir}/ntfs-3g
%{_bindir}/ntfsmount
%{_bindir}/ntfs-3g.probe
%{_bindir}/lowntfs-3g
%{_mandir}/man8/mount.lowntfs-3g.*
%{_mandir}/man8/mount.ntfs-3g.*
%{_mandir}/man8/ntfs-3g*

%files libs
%license COPYING
%{_libdir}/libntfs-3g.so.*

%files devel
%{_includedir}/ntfs-3g/
%{_libdir}/libntfs-3g.so
%{_libdir}/pkgconfig/libntfs-3g.pc

%files -n ntfsprogs
%doc AUTHORS CREDITS ChangeLog NEWS README
%license COPYING
%{_bindir}/ntfscat
%{_bindir}/ntfscluster
%{_bindir}/ntfscmp
%{_bindir}/ntfsfix
%{_bindir}/ntfsinfo
%{_bindir}/ntfsls
%{_bindir}/ntfssecaudit
%{_bindir}/ntfsusermap
# Extras
%{_bindir}/ntfsck
%{_bindir}/ntfsdecrypt
%{_bindir}/ntfsdump_logfile
%{_bindir}/ntfsfallocate
%{_bindir}/ntfsmftalloc
%{_bindir}/ntfsmove
%{_bindir}/ntfsrecover
%{_bindir}/ntfstruncate
%{_bindir}/ntfswipe
%{_sbindir}/fsck.ntfs
%{_sbindir}/mkfs.ntfs
%{_sbindir}/mkntfs
%{_sbindir}/ntfsclone
%{_sbindir}/ntfscp
%{_sbindir}/ntfslabel
%{_sbindir}/ntfsresize
%{_sbindir}/ntfsundelete
%{_mandir}/man8/mkntfs.8*
%{_mandir}/man8/mkfs.ntfs.8*
%{_mandir}/man8/ntfs[^m][^o]*.8*
%exclude %{_mandir}/man8/ntfs-3g*

%changelog
* Mon Jun 17 2024 Suresh Thelkar <sthelkar@microsoft.com> - 2022.10.3-2
- Patch CVE-2023-52890

* Mon Nov 14 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2022.10.3-1
- Auto-upgrade to 2022.10.3 - CVE-2022-40284

* Wed Jun 01 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 2022.5.17-1
- Updating to 2022.5.17 to fix CVE-2021-46790.

* Wed Apr 13 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2021.8.22-1
- Updating to 2021.8.22.
- Splitting out the "*-libs" subpackage using Fedora 36 spec (license: MIT) for guidance.

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2017.3.23-16
- Cleaning-up spec. License verified.

* Fri Oct 29 2021 Muhammad Falak <mwani@microsft.com> - 2017.3.23-15
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2:2017.3.23-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:2017.3.23-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:2017.3.23-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 29 2019 Tom Callaway <spot@fedoraproject.org> - 2:2017.3.23-11
- add upstream fix for CVE-2019-9755

* Mon Mar 11 2019 Kamil Páral <kparal@redhat.com> - 2:2017.3.23-10
- add Recommends: ntfs-3g-system-compression. That allows people with
  Windows 10 to read system files.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:2017.3.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 16 2018 Richard W.M. Jones <rjones@redhat.com> - 2:2017.3.23-8
- Fix for ntfsclone crash (RHBZ#1601146).

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2017.3.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 21 2018 Tom Callaway <spot@fedoraproject.org> - 2:2017.3.23-6
- apply updated big sectors patch

* Mon May  7 2018 Tom Callaway <spot@fedoraproject.org>
- big sectors patch from Jean-Pierre André

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2017.3.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan  4 2018 Tom Callaway <spot@fedoraproject.org> - 2:2017.3.23-4
- use upstream tarball again (non-free file is removed)
- remove unused CVE-2015-3202 patch

* Wed Dec 20 2017 Tom Callaway <spot@fedoraproject.org> - 2:2017.3.23-3.1
- test build with patch from Jean-Pierre André to fix the $MFT/$MFTMirr mismatch

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2017.3.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2017.3.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 30 2017 Tom Callaway <spot@fedoraproject.org> - 2:2017.3.23-1
- update to 2017.3.23

* Wed Feb  8 2017 Tom Callaway <spot@fedoraproject.org> - 2:2016.2.22-4
- apply patch for CVE-2017-0358
- NOTE: Fedora does not setuid ntfs-3g, so it should not be vulnerable 
  but some users might make this change so we applied the patch anyways

* Wed Nov  2 2016 Tom Callaway <spot@fedoraproject.org> - 2:2016.2.22-3
- enable posix ACLS
- enable xattr mappings

* Tue Aug  9 2016 Tom Callaway <spot@fedoraproject.org> - 2:2016.2.22-2
- replace non-free ntfsprogs/boot.c with boot-gpl.c (resolves bz1364710)

* Wed Mar 23 2016 Tom Callaway <spot@fedoraproject.org> - 2:2016.2.22-1
- update to 2016.2.22

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:2015.3.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Tom Callaway <spot@fedoraproject.org> - 2:2015.3.14-4
- spec file cleanups

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2015.3.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 Tom Callaway <spot@fedoraproject.org> 2:2015.3.14-2
- fix CVE-2015-3202

* Tue Apr  7 2015 Tom Callaway <spot@fedoraproject.org> 2:2015.3.14-1
- update to 2015.3.14

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2:2014.2.15-8
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Jan 13 2015 Tom Callaway <spot@fedoraproject.org> - 2:2014.2.15-7
- add patch to ignore -s option

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2014.2.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug  5 2014 Richard W.M. Jones <rjones@redhat.com> - 2:2014.2.15-5
- Add upstream patch to fix fstrim so it works on partitions as well
  as whole disks.

* Thu Jul 31 2014 Richard W.M. Jones <rjones@redhat.com> - 2:2014.2.15-4
- Upstream patches which add fstrim support.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2014.2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Tomáš Mráz <tmraz@redhat.com> - 2:2014.2.15-2
- Rebuild for new libgcrypt

* Wed Feb 26 2014 Tom Callaway <spot@fedoraproject.org> 2:2014.2.15-1
- update to 2014.2.15

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2013.1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Tom Callaway <spot@fedoraproject.org> - 2:2013.1.13-5
- fix bug preventing reads on compressed files on windows 8 partitions (bz967301)

* Mon May  6 2013 Tom Callaway <spot@fedoraproject.org> - 2:2013.1.13-4
- apply fixes from upstream for issue with 4K sector drives (bz951603) 
  and truncated check for Interix types on a 32-bit CPU (bz958681)

* Thu Feb  7 2013 Tom Callaway <spot@fedoraproject.org> - 2:2013.1.13-3
- drop redundant manpages from ntfsprogs subpackage

* Thu Jan 31 2013 Tom Callaway <spot@fedoraproject.org> - 2:2013.1.13-2
- drop hal files, since hal is very dead

* Tue Jan 22 2013 Richard W.M. Jones <rjones@redhat.com> - 2:2013.1.13-1
- New upstream version 2013.1.13 (RHBZ#902729).
- Drop ntfs-3g-junction-point-fix.patch (now upstream).
- Drop Windows 8 patches x 2 (both now upstream).
- Remove obsolete patches from Fedora git repository.
- Fix .gitignore file.

* Mon Oct 15 2012 Tom Callaway <spot@fedoraproject.org> - 2:2012.1.15-5
- Limit obsoletes to last ntfsprogs-* versions ( < 2.0.0-17 ) to
  minimize yum churn (where it would obsolete itself on every upgrade)
  BZ#863641

* Thu Oct  4 2012 Tom Callaway <spot@fedoraproject.org> - 2:2012.1.15-4
- add patches from upstream git to add a level of safety in the case where windows 8
  leaves the NTFS filesystem in an unsafe state and Linux access could result in data loss.
  Basically, with these patches, Linux will refuse to mount the ntfs partition. For the details
  refer to: https://bugzilla.redhat.com/show_bug.cgi?id=859373

* Sun Aug 19 2012 Tom Callaway <spot@fedoraproject.org> - 2:2012.1.15-3
- apply upstream fix for junction points (bz849332)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2012.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Tom Callaway <spot@fedoraproject.org> 2:2012.1.15-1
- update to 2012.1.15

* Wed Feb  1 2012 Kay Sievers <kay@redhat.com> 2:2011.10.9-3
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2011.10.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Tom Callaway <spot@fedoraproject.org> - 2:2011.10.9-1
- 2011.10.9-RC
- patch ntfsck to return 0 instead of 1 on unsupported filesystem cases

* Mon Sep 12 2011 Tom Callaway <spot@fedoraproject.org> - 2:2011.4.12-5
- fix ntfsck symlink (thanks to Chris Smart for catching it)

* Wed Sep  7 2011 Tom Callaway <spot@fedoraproject.org> - 2:2011.4.12-4
- fix issue preventing some volume types from not working properly (bz735862)
- create fsck.ntfs symlink to ntfsck (bz735612).
- apply cleanups from git trunk for ntfsck (bz 706638)
- apply cleanups from git trunk for ntfsfix (bz 711662, 723562)

* Mon May  9 2011 Tom Callaway <spot@fedoraproject.org> - 2:2011.4.12-3
- add Obsoletes to resolve multi-lib upgrade issue (bz702671)

* Mon Apr 25 2011 Tom Callaway <spot@fedoraproject.org> - 2:2011.4.12-2
- add --enable-extras flag (and use it) to ensure proper binary installation

* Thu Apr 14 2011 Tom Callaway <spot@fedoraproject.org> - 2:2011.4.12-1
- update to 2011.4.12
- pickup ntfsprogs and obsolete the old separate packages

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2011.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Tom Callaway <spot@fedoraproject.org> - 2:2011.1.15-1
- update to 2011.1.15

* Mon Oct 11 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2010.10.2-1
- update to 2010.10.2, all patches merged upstream

* Thu Sep  9 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2010.8.8-2
- add support for context= mount option (Till Maas) (bz502946)

* Mon Aug  9 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2010.8.8-1
- update to 2010.8.8

* Fri Jul  9 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2010.6.31-1
- update to 2010.6.31-RC

* Fri Jul  9 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2010.5.22-1
- update to 2010.5.22

* Tue May 18 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2010.5.16-1
- update to 2010.5.16
- fix makefile to build secaudit/usermap tools

* Mon Mar  8 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2010.3.6-1
- update to 2010.3.6

* Mon Feb 15 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2010.2.6-1
- update to 2010.2.6-RC
- fix summary text

* Wed Jan 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2010.1.16-1
- update to 2010.1.16

* Fri Nov 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.11.14-2
- missing BuildRequires: libattr-devel

* Fri Nov 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.11.14-1
- update to 2009.11.14

* Fri Oct 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.10.5-0.1.RC
- bump to 2009.10.5-RC

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> - 2:2009.4.4-3
- Rebuilt with new fuse

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2009.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr  3 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.4.4-1
- update to 4.4, patch for mount issue merged

* Mon Mar 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.3.8-2
- Patch from upstream provided as temporary workaround for bz 486619

* Thu Mar 26 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.3.8-1
- update to 2009.3.8

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2009.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.2.1-2
- update fdi to fix nautilus mount bug

* Thu Feb 12 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.2.1-1
- update to 2009.2.1

* Fri Jan 30 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:2009.1.1-1
- new release, new versioning scheme from upstream

* Thu Jan  8 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5222-0.2.RC
- move pkgconfig Requires to -devel package where it belongs

* Mon Dec 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5222-0.1.RC
- 1.5222-RC

* Tue Dec  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5130-1
- update to 1.5130

* Wed Oct 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5012-4
- fix hal file to properly ignore internal recovery partitions

* Wed Oct 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5012-3
- fix hal file to cover all mount cases (thanks to Richard Hughes)

* Mon Oct 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5012-2
- add fdi file to enable hal automounting

* Wed Oct 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.5012-1
- update to 1.5012 (same code as 1.2926-RC)

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2926-0.1.RC
- update to 1.2926-RC (rawhide, F10)

* Fri Aug 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2812-1
- update to 1.2812

* Sat Jul 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2712-1
- update to 1.2712

* Mon May  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2506-1
- update to 1.2506

* Tue Apr 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2412-1
- update to 1.2412

* Mon Mar 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2310-2
- update sources

* Mon Mar 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2310-1
- update to 1.2310
- make -n a noop (bz 403291)

* Tue Feb 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:1.2216-3
- rebuild against fixed gcc (PR35264, bugzilla 433546)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2:1.2216-2
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.2216-1
- update to 1.2216

* Tue Nov 20 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.1120-1
- bump to 1.1120
- default to fuse-lite (internal to ntfs-3g), but enable --with externalfuse 
  as an option

* Thu Nov  8 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.1104-1
- bump to 1.1104

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.1030-1
- bump to 1.1030

* Sat Oct  6 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.1004-1
- bump to 1.1004

* Thu Sep 20 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.913-2
- don't set /sbin/mount.ntfs-3g setuid

* Mon Sep 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.913-1
- bump to 1.913

* Sun Aug 26 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.826-1
- bump to 1.826
- glibc27 patch is upstreamed

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.810-1
- bump to 1.810
- fix license tag
- rebuild for ppc32

* Sun Jul 22 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.710-1
- bump to 1.710
- add compat symlinks

* Wed Jun 27 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.616-1
- bump to 1.616

* Tue May 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.516-1
- bump to 1.516
- fix bugzilla 232031

* Sun Apr 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.417-1
- bump to 1.417

* Sun Apr 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.416-1
- bump to 1.416
- drop patch0, upstreamed

* Wed Apr  4 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.328-2
- allow non-root users to mount/umount ntfs volumes (Laszlo Dvornik)

* Sat Mar 31 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.328-1
- bump to 1.328
- drop patch, use --disable-ldconfig instead

* Wed Feb 21 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:1.0-1
- 1.0 release!

* Fri Jan 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:0-0.9.20070118
- symlink to mount.ntfs

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:0-0.8.20070118
- bump to 20070118

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2:0-0.7.20070116
- bump to latest version for all active dists

* Wed Jan  3 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1:0-0.6.20070102
- bump to latest version (note that upstream fixed their date mistake)

* Wed Nov  1 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:0-0.5.20070920
- add an obsoletes for ntfsprogs-fuse
- make some convenience symlinks

* Wed Oct 25 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:0-0.4.20070920
- add some extra Provides

* Mon Oct 16 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:0-0.3.20070920
- add explicit Requires on fuse

* Mon Oct 16 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1:0-0.2.20070920
- fixed versioning (bumped epoch, since it now shows as older)
- change sbin symlink to actual copy to be safe

* Sun Oct 15 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.1.20070920-1
- Initial package for Fedora Extras
