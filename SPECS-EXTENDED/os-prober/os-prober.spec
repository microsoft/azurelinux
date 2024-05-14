Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           os-prober
Version:        1.77
Release:        7%{?dist}
Summary:        Probes disks on the system for installed operating systems

# For more information about licensing, see copyright file.
License:        GPLv2+ and GPL+
URL:            https://kitenet.net/~joey/code/os-prober/
Source0:        https://ftp.us.debian.org/debian/pool/main/o/os-prober/%{name}_%{version}.tar.xz
Patch0:         os-prober-no-dummy-mach-kernel.patch
# Sent upstream
Patch1:         os-prober-mdraidfix.patch
Patch2:         os-prober-btrfsfix.patch
Patch3:         os-prober-bootpart-name-fix.patch
Patch4:         os-prober-mounted-partitions-fix.patch
Patch5:         os-prober-factor-out-logger.patch
# To be sent upstream
Patch6:         os-prober-factored-logger-efi-fix.patch
Patch7:         os-prober-umount-fix.patch
Patch8:         os-prober-grub2-parsefix.patch
Patch9:         os-prober-grepfix.patch
Patch10:        os-prober-gentoo-fix.patch
Patch11:        os-prober-grub2-mount-workaround.patch

Requires:       udev coreutils util-linux
Requires:       grep /bin/sed /sbin/modprobe
Requires:       grub2-tools-minimal

BuildRequires:  gcc git

%description
This package detects other OSes available on a system and outputs the results
in a generic machine-readable format. Support for new OSes and Linux
distributions can be added easily. 

%prep
%autosetup -n %{name}-%{version} -S git

find -type f -exec sed -i -e 's|usr/lib|usr/libexec|g' {} \;
sed -i -e 's|grub-probe|grub2-probe|g' os-probes/common/50mounted-tests \
     linux-boot-probes/common/50mounted-tests
sed -i -e 's|grub-mount|grub2-mount|g' os-probes/common/50mounted-tests \
     linux-boot-probes/common/50mounted-tests common.sh

%build
%set_build_flags
%make_build LDFLAGS="$LDFLAGS -fPIC"

%install
install -m 0755 -d %{buildroot}%{_bindir}
install -m 0755 -d %{buildroot}%{_var}/lib/%{name}

install -m 0755 -p os-prober linux-boot-prober %{buildroot}%{_bindir}
install -m 0755 -Dp newns %{buildroot}%{_libexecdir}/os-prober/newns
install -m 0644 -Dp common.sh %{buildroot}%{_datadir}/%{name}/common.sh

%ifarch m68k
ARCH=m68k
%endif
%ifarch ppc ppc64
ARCH=powerpc
%endif
%ifarch sparc sparc64
ARCH=sparc
%endif
%ifarch %{ix86} x86_64
ARCH=x86
%endif

for probes in os-probes os-probes/mounted os-probes/init \
              linux-boot-probes linux-boot-probes/mounted; do
        install -m 755 -d %{buildroot}%{_libexecdir}/$probes 
        cp -a $probes/common/* %{buildroot}%{_libexecdir}/$probes
        if [ -e "$probes/$ARCH" ]; then 
                cp -a $probes/$ARCH/* %{buildroot}%{_libexecdir}/$probes 
        fi
done
if [ "$ARCH" = x86 ]; then
        install -m 755 -p os-probes/mounted/powerpc/20macosx \
            %{buildroot}%{_libexecdir}/os-probes/mounted
fi

%files
%doc README TODO debian/changelog
%license debian/copyright
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/%{name}
%{_var}/lib/%{name}

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.77-7
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Sat Oct 10 2020 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.77-6
- Workaround for grub2-mount slow wildcard file matching, fixes #1770599

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.77-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.77-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.77-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 14 2019 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.77-2
- Use distro LDFLAGS when building the package, fixes #1543863

* Tue May 14 2019 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.77-1
- Update to 1.77, use grub2-mount rather than device mapper for mounts, fixes #1447156

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.74-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.74-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Feb 18 2018 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.74-6
- Add gcc build dependency

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.74-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 29 2017 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.74-4
- Fix a path problem in btrfsfix.patch, fixes #1529616

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.74-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.74-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 27 2017 Neal Gompa <ngompa13@gmail.com> - 1.74-1
- Update to upstream version 1.74
- Drop merged patches
- Rediff remaining patches
- Move newns to /usr/libexec/os-prober (debuginfo generation works)
- Mark copyright file as license file

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Mar 04 2016 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.71-1
- Update to upstream version 1.71
- Use git based autosetup for applying patches

* Mon Feb 15 2016 Peter Jones <pjones@redhat.com> - 1.70-3
- Don't keep backups with 'patch -b'; they wind up in the ouput package.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.70-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 13 2015 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.70-1
- Update to upstream version 1.70, fixes #1275641
- Fix bug #1236358 - os-prober duplicates grub entries for read/write btrfs
  subvolumes, thanks to Helmut Horvath
- Fix bug #1236649 - os-prober does not detect os on btrfs partition without
  any subvolume

* Tue Oct 20 2015 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.68-1
- Update to upstream version 1.68, bug #1267779
- Support a case where a kernel named vmlinuz/x is used under Gentoo, bug #1223237

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.65-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 23 2014 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.65-2
- Fix using grep for searching binary files, fixes #1172405. Thanks Paul Eggert
  for initial patch fixing grep usage in 83haiku

* Sun Dec 07 2014 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.65-1
- Using latest upstream version tarball to be consistent with upstream
  versioning

* Sat Oct 25 2014 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.58-11
- Fix parsing grub2's initrd/linux variations, rhbz #1108344

* Mon Sep 08 2014 Peter Jones <pjones@redhat.com> - 1.58-10
- Make os-prober output include partitions for UEFI chainloads.
  Resolves: rhbz#873207

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.58-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 06 2014 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.58-8
- Fix bug in counting LVM LVs which their name contains 'btrfs' as btrfs volumes

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.58-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.58-6
- Fix separate /usr partitions for usrmove distros (bug #1044760)
- Fix umount error when directory is temporarily busy (bug #903906)

* Thu Apr 24 2014 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.58-5
- Fixed bug #982009: fix btrfs support
- Suppress some more debug messages when debug messages are disabled

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.58-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 Adam Williamson <awilliam@redhat.com> - 1.58-3
- revert factored-logger-efi-fix.patch until grub2 is updated to match

* Tue Jun 18 2013 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.58-2
- Fix a bug in EFI detection because of redirecting result output

* Sun May 05 2013 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.58-1
- Update to upstream version 1.58, with UEFI support

* Sat Feb 02 2013 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.57-2
- Fix a bug in recent btrfs patch when an extended partition is examined. 
  (H.J. Lu) (bug #906847)
- Fix naming of /boot partitions according to their fstab entry (bug #893472)
- Don't generate .btrfsfix files which will be included in final rpm
- Fix wrong boot partition set by linux-boot-prober when / and /boot are
  mounted (bug #906886)
- Factor out 'logger', so that it is run once and logs are piped to it (John
  Reiser) (bug #875356)

* Tue Jan 22 2013 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.57-1
- Update to 1.57 (#890409)
- Use shell string processing rather than 'basename' (#875356)
- Make it possible to disable logging debug messages by assigning a value to
  OS_PROBER_DISABLE_DEBUG environment variable (Gene Czarcinski) (#893997).
- Detect multi btrfs pools/volumes (Gene Czarcinski) (#888341)

* Thu Oct 11 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.56-1
- Update to 1.56 with a bug fix and applied one of my patches

* Mon Aug 27 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.55-1
- Update to new upstream version: 1.55

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.53-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 02 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.53-3
- Consider usrmoved distribtions in fallback linux detector (bug #826754)
- Remove patch backup files from final rpm package (by not creating a backup!)

* Fri May 25 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.53-2
- Add support for OSes installed on Linux mdraid partitions, bug #752402
- Add Fedora's grub2 config path, fixes generating menu entries for other
  installed Fedora's
- Fixed bug in parsing yaboot.conf: accept spaces around '=' for append, 
  bug #825041

* Fri May 11 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.53-1
- Updated to 1.53 for a bugfix
- Fixed directory name in upstream tarbal

* Thu May 10 2012 Peter Jones <pjones@redhat.com> - 1.52-3
- Don't detect our Mac boot blocks as OS X.
  Resolves: rhbz#811412

* Sun Apr 29 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.52-2
- use correct directory name for setup

* Sun Apr 29 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.52-1
- Updated to 1.52, supports win 8

* Wed Mar 28 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.51-1
- Update to latest upstream version, 1.51

* Sat Jan 21 2012 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.48-3
- Remove dmraid and lvm2 dependency. bug #770393

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.48-1
- Updated to 1.48 release

* Thu May 19 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.47-1
- Updated to the new upstream version 1.47

* Wed May 04 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.46-2
- Removed obsolete parts (build tag, defattr, etc)
- Added a patch to move newns outside of os-prober subdirectory
- Added required utilities as package requires

* Sat Apr 30 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.46-1
- Updated to 1.46 release

* Tue Feb 22 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.42-2
- Remove executable permission from common.sh

* Thu Feb 17 2011 Hedayat Vatankhah <hedayat.fwd+rpmchlog@gmail.com> - 1.42-1
- Initial version
