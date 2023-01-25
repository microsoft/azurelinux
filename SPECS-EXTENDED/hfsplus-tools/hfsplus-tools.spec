# we want this to end up with the other mkfs.*'s, in /sbin
%define _exec_prefix /
Summary:        Tools to create/check Apple HFS+ filesystems
Name:           hfsplus-tools
Version:        540.1.linux3
Release:        27%{?dist}
License:        APSL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
# Project's web page (http://gentoo-wiki.com/HOWTO_hfsplus) is no longer online.
Source0:        https://src.fedoraproject.org/repo/pkgs/hfsplus-tools/diskdev_cmds-540.1.linux3.tar.gz/0435afc389b919027b69616ad1b05709/diskdev_cmds-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source100:      http://www.opensource.org/licenses/apsl-2.0.txt
Patch0:         hfsplus-tools-no-blocks.patch
Patch1:         hfsplus-tools-learn-to-stdarg.patch
Patch2:         hfsplus-tools-sysctl.patch
BuildRequires:  gcc
BuildRequires:  libuuid-devel
BuildRequires:  make
BuildRequires:  openssl-devel
# those tools are outdated, given the rebuilt mkfs/fsck.hfsplus in this
# package.  However, I don't want to Obsolete that package yet, as some people
# may have a valid use for it on their systems.
Conflicts:      hfsplusutils

%description
HFS+, HFS Plus, or Mac OS Extended are names for a file system developed by
Apple Computer to replace their Hierarchical File System (HFS). In addition to
being the default file system on modern Apple computers, HFS+ is one of two
formats, FAT being the other, that are supported by the iPod hard-disk based
music player. Unlike FAT, HFS+ supports UNIX style file permissions, which
makes it useful, for serving and sharing files in a secured manner. As Apple
Computer's devices and systems become increasingly ubiquitous, it becomes
important that Linux fully support this format.  This package provides tools
to create and check HFS+ filesystems under Linux.

The Linux kernel does not support writing to HFS+ journals, writing to a
hfsplus partition is recommended only after disabling journaling; however, the
kernel, as of version 2.6.16, supports case-sensitivity (also known as HFSX)
commit.

%prep
%setup -q -n hfsplus-mkfs-%{version} -n diskdev_cmds-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# remove errant execute bits
find . -type f -name '*.[ch]' -exec chmod -c -x {} +

# make life easier on doc
cp %{SOURCE100} .


%build
export CFLAGS="%{optflags}"
make %{?_smp_mflags} -f Makefile


%install
# the actual install...
mkdir -p %{buildroot}/%{_sbindir}
cp newfs_hfs.tproj/newfs_hfs %{buildroot}/%{_sbindir}/mkfs.hfsplus
cp fsck_hfs.tproj/fsck_hfs %{buildroot}/%{_sbindir}/fsck.hfsplus

# man pages -- a mildly non-invasive name change is in order
mkdir -p %{buildroot}/%{_mandir}/man8
cat fsck_hfs.tproj/fsck_hfs.8 | sed -e 's/[F|f]sck_hfs/fsck.hfsplus/g' \
    > %{buildroot}/%{_mandir}/man8/fsck.hfsplus.8
cat newfs_hfs.tproj/newfs_hfs.8 | sed -e 's/[N|n]ewfs_hfs/mkfs.hfsplus/g' \
    > %{buildroot}/%{_mandir}/man8/mkfs.hfsplus.8

# and a utility symlink...
cd %{buildroot}/%{_sbindir}
ln -s fsck.hfsplus fsck.hfs
cd %{buildroot}/%{_mandir}/man8
ln -s fsck.hfsplus.8 fsck.hfs.8


%files
%doc apsl-2.0.txt
%{_sbindir}/mkfs.hfsplus
%{_sbindir}/fsck.hfsplus
%{_sbindir}/fsck.hfs
%{_mandir}/man8/mkfs.hfsplus.8.gz
%{_mandir}/man8/fsck.hfsplus.8.gz
%{_mandir}/man8/fsck.hfs.8.gz

%changelog
* Tue Jan 31 2022 Suresh Thelkar <sthelkar@microsoft.com> - 540.1.linux3-27
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 540.1.linux3-25
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 11 2020 Adam Jackson <ajax@redhat.com> - 540.1.linux3-22
- <sys/sysctl.h> -> <linux/sysctl.h>

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-21
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 540.1.linux3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 540.1.linux3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 540.1.linux3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 18 2014 Adam Jackson <ajax@redhat.com> 540.1.linux3-8
- Remove asinine blocks usage so we don't need clang, build with gcc, and
  remove ExcludeArchery to match
- Fix FTBFS on arm due to a... fascinating interpretation of how varargs work

* Tue Jun 10 2014 Richard W.M. Jones <rjones@redhat.com> - 540.1.linux3-7
- ExcludeArch arm because clang doesn't select the correct float ABI.
- Remove unnecessary cruft not required by modern RPM.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 540.1.linux3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 540.1.linux3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Dan Horák <dan[at]danny.cz> - 540.1.linux3-4
- exclude ppc and s390, no working clang there

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 540.1.linux3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 540.1.linux3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 16 2012 Matthew Garrett <mjg@redhat.com> 540.1.linux3-1
- update to new upstream

* Fri Feb 03 2012 Matthew Garrett <mjg@redhat.com> 540.1.linux2-1
- update to new upstream

* Fri Feb 03 2012 Matthew Garrett <mjg@redhat.com> 540.1.linux1-1
- update to new upstream
- No longer provides mkfs.hfs - use hfsutils instead

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 332.14-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 19 2011 Matthew Garrett <mjg@redhat,com> 332.14-13
- hfsplus-tools-332.14-fix-uuid.patch: Fix UUID generation

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 332.14-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 16 2010 Adam Jackson <ajax@redhat.com> 332.14 -11
- hfsplus-tools-332.14-add-needed.patch: Fix FTBFS from --no-add-needed

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 332.14-11
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 332.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 332.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - 332.14-8
- rebuild with new openssl

* Wed Sep 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 332.14-7
- RH Legal was kind enough to point out what I had overlooked, the clause in the APSL
  which permits "any subsequent version of this License published by Apple".
- Fixed license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 332.14-6
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 332.14-5
- bump, minor spec fixes

* Tue Nov 21 2006 Chris Weyl <cweyl@alumni.drew.edu> 332.14-4
- include hfsbootdata (BZ#213365)

* Thu Aug 31 2006 Chris Weyl <cweyl.drew.edu> 332.14-3
- bump for mass rebuild

* Fri Aug 18 2006 Chris Weyl <cweyl@alumni.drew.edu> 332.14-2
- bump 

* Wed Jul 26 2006 Chris Weyl <cweyl@alumni.drew.edu> 332.14-1
- update to 332.14

* Thu Jul 20 2006 Chris Weyl <cweyl@alumni.drew.edu> 332.11-1
- add manpages
- add a copy of the license
- tweak makefiles to build with our CFLAG optimizations, not those hippy
  optimizations gentoo uses ;)

* Tue Jul 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 332.11-0
- Build process snagged from Gentoo.  Thanks, guys :)
- Initial spec file for F-E
