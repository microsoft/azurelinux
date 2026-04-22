# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		f2fs-tools
Version:	1.16.0
Release: 10%{?dist}
Summary:	Tools for Flash-Friendly File System (F2FS)
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:	GPL-2.0-or-later
URL:		http://sourceforge.net/projects/f2fs-tools/
Source0:	http://git.kernel.org/cgit/linux/kernel/git/jaegeuk/f2fs-tools.git/snapshot/%{name}-%{version}.tar.gz
# Patch  from https://git.kernel.org/pub/scm/linux/kernel/git/jaegeuk/f2fs-tools.git/patch/?id=6617d15a660becc23825007ab3fc2d270b5b250f
Patch0:		f2fs-tools-1.16.0-c23.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	uuid-devel
BuildRequires:	libuuid-devel
BuildRequires:	libtool
BuildRequires:	libselinux-devel
BuildRequires:	libblkid-devel
BuildRequires:	make

%description
NAND flash memory-based storage devices, such as SSD, and SD cards,
have been widely being used for ranging from mobile to server systems. 
Since they are known to have different characteristics from the 
conventional rotational disks,a file system, an upper layer to 
the storage device, should adapt to the changes
from the sketch.

F2FS is a new file system carefully designed for the 
NAND flash memory-based storage devices. 
We chose a log structure file system approach,
but we tried to adapt it to the new form of storage. 
Also we remedy some known issues of the very old log
structured file system, such as snowball effect 
of wandering tree and high cleaning overhead.

Because a NAND-based storage device shows different characteristics 
according to its internal geometry or flash memory management 
scheme aka FTL, we add various parameters not only for configuring 
on-disk layout, but also for selecting allocation
and cleaning algorithms.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?isa} = %{version}-%{release}
%description devel
This package contains the libraries needed to develop applications
that use %{name}

%prep
%setup -q
%patch 0 -p1 -b .c23
sed -i 's/AC_PROG_LIBTOOL/LT_INIT/' configure.ac


%build
autoreconf --install
%configure --disable-static
%{make_build}


%install
%{make_install}
install -m 644 mkfs/f2fs_format_utils.h %{buildroot}%{_includedir}
find %{buildroot} -type f -name "*.la" -delete

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS ChangeLog
%{_sbindir}/mkfs.f2fs
%{_sbindir}/fibmap.f2fs
%{_sbindir}/fsck.f2fs
%{_sbindir}/dump.f2fs
%{_sbindir}/parse.f2fs
%{_sbindir}/defrag.f2fs
%{_sbindir}/resize.f2fs
%{_sbindir}/sload.f2fs
%{_sbindir}/f2fs_io
%{_sbindir}/f2fscrypt
%{_sbindir}/f2fslabel

%{_libdir}/*.so.*
%{_mandir}/man8/*f2*.gz

%files devel
%{_includedir}/*.h
%{_libdir}/*.so

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 25 2025 Eduardo Echeverria <echevemaster@gmail.com> - 1.16.0-8
- Rebuilt due to FTBFS in f42
- The existing bool definition is broken for c23, where bool is now a keyword.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 1.16.0-6
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 21 2023 Filipe Rosset <rosset.filipe@gmail.com> - 1.16.0-1
- Update to 1.16.0 fixes rhbz#2098509

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 24 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1.14.0-1
- Update to 1.14.0

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Dec 15 2019 Nicolas Chauvet <kwizart@gmail.com> - 1.13.0-1
- Update to 1.13.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Apr 14 2019 Filipe Rosset <rosset.filipe@gmail.com> - 1.12.0-1
- Update to 1.12.0, fixes rhbz#1603942 and rhbz#1674870
- added libblkid-devel as BR, added new binary sg_write_buffer

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Filipe Rosset <rosset.filipe@gmail.com> - 1.10.0-1
- Update to 1.10.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 12 2017 Eduardo Echeverria <echevemaster@gmail.com> - 1.8.0-1
- Update to 1.8.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Oct 08 2016 Eduardo Echeverria <echevemaster@gmail.com> - 1.7.0-1
- Bumped to 1.7.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Aug 8  2015 Eduardo Echeverria  <echevemaster@gmail.com> - 1.4.1-1
- Updated to 1.4.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 03 2015 Dan Horák <dan[at]danny.cz> - 1.4.0-3
- fix build on big endian arches

* Fri Dec 26 2014 Jonathan Dieter <jdieter@lesbg.com> - 1.4.0-2
- Add missing header to development package

* Thu Dec 25 2014 Eduardo Echeverria  <echevemaster@gmail.com> - 1.4.0-1
- Update to the latest upstream version

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 19 2014 Eduardo Echeverria  <echevemaster@gmail.com> - 1.2.0-1
- Update to the latest upstream version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Eduardo Echeverria  <echevemaster@gmail.com> - 1.1.0-2
- Minor fix in the changelogs

* Mon Mar 18 2013 Eduardo Echeverria  <echevemaster@gmail.com> - 1.1.0-1
- Updated to the new upstream release

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 22 2012 Eduardo Echeverria  <echevemaster@gmail.com> - 1.0.0-3
- Change to the correct license GPLv2+
- Remove README file to the section doc

* Mon Oct 15 2012 Eduardo Echeverria  <echevemaster@gmail.com> - 1.0.0-2
- Add Changelog AUTHORS files to section doc
- Add wilcard to the manpages section.

* Sun Oct 07 2012 Eduardo Echeverria  <echevemaster@gmail.com> - 1.0.0-1
- Initial packaging
