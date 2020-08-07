%global with_signed 0
%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        GRand Unified Bootloader
Name:           grub2
Version:        2.02
Release:        23%{?dist}
License:        GPLv3+
URL:            https://www.gnu.org/software/grub
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        ftp://ftp.gnu.org/gnu/grub/grub-2.02.tar.xz

%if 0%{?with_signed}
Source100:    grubx64.efi.%{version}-%{release}.signed
Source101:    grubaa64.efi.%{version}-%{release}.signed
%endif

Patch0:     release-to-master.patch
Patch1:     0001-Add-support-for-Linux-EFI-stub-loading.patch
Patch2:     0002-Rework-linux-command.patch
Patch3:     0003-Rework-linux16-command.patch
Patch4:     0004-Add-secureboot-support-on-efi-chainloader.patch
Patch5:     0005-Make-any-of-the-loaders-that-link-in-efi-mode-honor-.patch
Patch6:     0006-Handle-multi-arch-64-on-32-boot-in-linuxefi-loader.patch

# CVE-2015-8370
Patch7:     0067-Fix-security-issue-when-reading-username-and-passwor.patch

Patch8:     0127-Core-TPM-support.patch
Patch9:     0128-Measure-kernel-initrd.patch
Patch10:    0131-Measure-the-kernel-commandline.patch
Patch11:    0132-Measure-commands.patch
Patch12:    0133-Measure-multiboot-images-and-modules.patch
Patch13:    0135-Rework-TPM-measurements.patch
Patch14:    0136-Fix-event-log-prefix.patch
Patch15:    0139-Make-TPM-errors-less-fatal.patch
Patch16:    0156-TPM-Fix-hash_log_extend_event-function-prototype.patch
Patch17:    0157-TPM-Fix-compiler-warnings.patch
Patch18:    0216-Disable-multiboot-multiboot2-and-linux16-modules-on-.patch
Patch19:    0224-Rework-how-the-fdt-command-builds.patch

# These patches are not required but help to apply the BootHole patches and are
# low risk to take on (mostly just additional security or bug fixes)
Patch20:    0001-chainloader-Fix-gcc9-error-Waddress-of-packed-member.patch
Patch21:    0001-efi-Fix-gcc9-error-Waddress-of-packed-member.patch
Patch22:    0001-hfsplus-Fix-gcc9-error-with-Waddress-of-packed-membe.patch
Patch23:    0001-btrfs-Move-the-error-logging-from-find_device-to-its.patch
Patch24:    0001-btrfs-Avoid-a-rescan-for-a-device-which-was-already-.patch
Patch25:    0001-multiboot2-Set-min-address-for-mbi-allocation-to-0x1.patch
Patch26:    0001-Add-missing-strtoull_test.c.patch
Patch27:    0001-misc-Make-grub_strtol-end-pointers-have-safer-const-.patch

# Start of BootHole security patches
# CVE-2020-10713 - 0001-yylex-Make-lexer-fatal-errors-actually-be-fatal.patch
Patch28:    CVE-2020-10713.patch
Patch29:    0002-safemath-Add-some-arithmetic-primitives-that-check-f.patch
Patch30:    0003-calloc-Make-sure-we-always-have-an-overflow-checking.patch
# CVE-2020-14308 - 0004-calloc-Use-calloc-at-most-places.patch
Patch31:    CVE-2020-14308.patch
# CVE-2020-14309 - 0005-malloc-Use-overflow-checking-primitives-where-we-do-.patch
# CVE-2020-14310 - 0005-malloc-Use-overflow-checking-primitives-where-we-do-.patch
# CVE-2020-14311 - 0005-malloc-Use-overflow-checking-primitives-where-we-do-.patch
Patch32:    CVE-2020-14309.patch
Patch33:    CVE-2020-14310.nopatch
Patch34:    CVE-2020-14311.nopatch
Patch35:    0006-iso9660-Don-t-leak-memory-on-realloc-failures.patch
Patch36:    0007-font-Do-not-load-more-than-one-NAME-section.patch
Patch37:    0008-gfxmenu-Fix-double-free-in-load_image.patch
Patch38:    0009-xnu-Fix-double-free-in-grub_xnu_devprop_add_property.patch
# Ignore the json double-free patch. Grub added a json library well after 2.02.
# Revisit this if we want to enable LUKS2 encryption.
# 0010-json-Avoid-a-double-free-when-parsing-fails.patch
Patch39:    0011-lzma-Make-sure-we-don-t-dereference-past-array.patch
Patch40:    0012-term-Fix-overflow-on-user-inputs.patch
Patch41:    0013-udf-Fix-memory-leak.patch
# Ignore the multiboot memleak patch. The patch is to fix a memleak that was
# introduced with Grub's verifiers feature, which landed after 2.02.
# Revisit this if we want to enable the verifiers feature.
# 0014-multiboot2-Fix-memory-leak-if-grub_create_loader_cmd.patch
Patch42:    0015-tftp-Do-not-use-priority-queue.patch
Patch43:    0016-relocator-Protect-grub_relocator_alloc_chunk_addr-in.patch
Patch44:    0017-relocator-Protect-grub_relocator_alloc_chunk_align-m.patch
Patch45:    0018-script-Remove-unused-fields-from-grub_script_functio.patch
# CVE-2020-15706 - 0019-script-Avoid-a-use-after-free-when-redefining-a-func.patch
Patch46:    CVE-2020-15706.patch
Patch47:    0020-relocator-Fix-grub_relocator_alloc_chunk_align-top-m.patch
Patch48:    0021-hfsplus-Fix-two-more-overflows.patch
Patch49:    0022-lvm-Fix-two-more-potential-data-dependent-alloc-over.patch
Patch50:    0023-emu-Make-grub_free-NULL-safe.patch
Patch51:    0024-efi-Fix-some-malformed-device-path-arithmetic-errors.patch
Patch52:    0025-efi-chainloader-Propagate-errors-from-copy_file_path.patch
Patch53:    0026-efi-Fix-use-after-free-in-halt-reboot-path.patch
Patch54:    0027-loader-linux-Avoid-overflow-on-initrd-size-calculati.patch
# CVE-2020-15707 - 0028-linux-Fix-integer-overflows-in-initrd-size-handling.patch
Patch55:    CVE-2020-15707.patch
# End of BootHole security patches

Patch100:   0001-efinet-do-not-start-EFI-networking-at-module-init-ti.patch

BuildRequires:  device-mapper-devel
BuildRequires:  xz-devel
BuildRequires:  systemd-devel
Requires:   xz
Requires:   device-mapper
%description
The GRUB package contains the GRand Unified Bootloader.

%package lang
Summary: Additional language files for grub
Group: System Environment/Programming
Requires: %{name} = %{version}
%description lang
These are the additional language files of grub.

%ifarch x86_64
%package pc
Summary: GRUB Library for BIOS
Group: System Environment/Programming
Requires: %{name} = %{version}
%description pc
Additional library files for grub
%endif

%package efi
Summary: GRUB Library for UEFI
Group: System Environment/Programming
Requires: %{name} = %{version}
%description efi
Additional library files for grub

%package efi-unsigned
Summary: Unsigned GRUB UEFI image
Group: System Environment/Base
%description efi-unsigned
Unsigned GRUB UEFI image

%package efi-binary
Summary: GRUB UEFI image
Group: System Environment/Base
%description efi-binary
GRUB UEFI bootloader binaries

%if 0%{?with_signed}
%package efi-binary-signed
Summary: Production Signed GRUB UEFI image
Group: System Environment/Base
Requires:  %{name}-efi-binary = %{version}-%{release}
%description efi-binary-signed
GRUB UEFI image signed with the secure boot production key
%endif

%prep
%setup -qn grub-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%ifarch aarch64
%patch100 -p1
%endif
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
# Nopatch 33 and 34
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1

%build
./autogen.sh
%ifarch x86_64
mkdir build-for-pc
pushd build-for-pc
# Modify the default CFLAGS to support the i386 build
CFLAGS="`echo " %{build_cflags} "          | \
        sed 's/-fcf-protection//'          | \
        sed 's/-fstack-protector-strong//' | \
        sed 's/-m64//'                     | \
        sed 's/-specs.*cc1//'              | \
        sed 's/-mtune=generic//'`"
export CFLAGS

../configure \
    --prefix=%{_prefix} \
    --sbindir=/sbin \
    --sysconfdir=%{_sysconfdir} \
    --disable-werror \
    --disable-efiemu \
    --with-grubdir=grub2 \
    --with-platform=pc \
    --target=i386 \
    --program-transform-name=s,grub,%{name}, \
    --with-bootdir="/boot"
make %{?_smp_mflags}
make DESTDIR=$PWD/../install-for-pc install
popd
%endif

# Disable stack-protector and PIE spec to fix compilation
CFLAGS="`echo " %{build_cflags} "              | \
         sed 's/-specs.*cc1//'                 | \
         sed 's/-fstack-protector-strong//'`"
export CFLAGS

mkdir build-for-efi
pushd build-for-efi
../configure \
    --prefix=%{_prefix} \
    --sbindir=/sbin \
    --sysconfdir=%{_sysconfdir} \
    --disable-werror \
    --disable-efiemu \
    --with-grubdir=grub2 \
    --with-platform=efi \
    --target=%{_arch} \
    --program-transform-name=s,grub,%{name}, \
    --with-bootdir="/boot"
make %{?_smp_mflags}
make DESTDIR=$PWD/../install-for-efi install
popd

#make sure all the files are same between two configure except the /usr/lib/grub
%check
%ifarch x86_64
diff -sr install-for-efi/sbin install-for-pc/sbin && \
diff -sr install-for-efi%{_bindir} install-for-pc%{_bindir} && \
diff -sr install-for-efi%{_sysconfdir} install-for-pc%{_sysconfdir} && \
diff -sr install-for-efi%{_datarootdir} install-for-pc%{_datarootdir}
%endif

%install
mkdir -p %{buildroot}
cp -a install-for-efi/. %{buildroot}/.
%ifarch x86_64
cp -a install-for-pc/. %{buildroot}/.
%endif
mkdir %{buildroot}%{_sysconfdir}/default
touch %{buildroot}%{_sysconfdir}/default/grub
mkdir %{buildroot}%{_sysconfdir}/sysconfig
ln -sf %{_sysconfdir}/default/grub %{buildroot}%{_sysconfdir}/sysconfig/grub
install -vdm 700 %{buildroot}/boot/%{name}
touch %{buildroot}/boot/%{name}/grub.cfg
chmod 600 %{buildroot}/boot/%{name}/grub.cfg
rm -rf %{buildroot}%{_infodir}

# Generate grub efi image
install -d %{buildroot}/usr/share/grub2-efi
%ifarch x86_64
./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/x86_64-efi/ -o %{buildroot}/usr/share/grub2-efi/grubx64.efi -p /boot/grub2 -O x86_64-efi fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop efi_uga ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm cryptodisk luks gcry_rijndael gcry_sha512
%endif
%ifarch aarch64
./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/arm64-efi/ -o %{buildroot}/usr/share/grub2-efi/grubaa64.efi -p /boot/grub2 -O arm64-efi fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm cryptodisk luks gcry_rijndael gcry_sha512
%endif

# Install to efi directory
EFI_BOOT_DIR=%{buildroot}/boot/efi/EFI/BOOT
GRUB_MODULE_NAME=
GRUB_MODULE_SOURCE=

install -d $EFI_BOOT_DIR

%ifarch x86_64
GRUB_MODULE_NAME=grubx64.efi

%if 0%{?with_signed}
GRUB_MODULE_SOURCE=%{SOURCE100}
%else
GRUB_MODULE_SOURCE=%{buildroot}/usr/share/grub2-efi/grubx64.efi
%endif

%endif

%ifarch aarch64
GRUB_MODULE_NAME=grubaa64.efi

%if 0%{?with_signed}
GRUB_MODULE_SOURCE=%{SOURCE101}
%else
GRUB_MODULE_SOURCE=%{buildroot}/usr/share/grub2-efi/grubaa64.efi
%endif

%endif

cp $GRUB_MODULE_SOURCE $EFI_BOOT_DIR/$GRUB_MODULE_NAME

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%dir %{_sysconfdir}/grub.d
%dir /boot/%{name}
%config() %{_sysconfdir}/bash_completion.d/grub
%config() %{_sysconfdir}/grub.d/00_header
%config() %{_sysconfdir}/grub.d/10_linux
%config() %{_sysconfdir}/grub.d/20_linux_xen
%config() %{_sysconfdir}/grub.d/30_os-prober
%config(noreplace) %{_sysconfdir}/grub.d/40_custom
%config(noreplace) %{_sysconfdir}/grub.d/41_custom
%{_sysconfdir}/grub.d/README
/sbin/*
%{_bindir}/*
%{_datarootdir}/grub/*
%{_sysconfdir}/sysconfig/grub
%{_sysconfdir}/default/grub
%ghost %config(noreplace) /boot/%{name}/grub.cfg

%ifarch x86_64
%files pc
%{_libdir}/grub/i386-pc
%files efi
%{_libdir}/grub/x86_64-efi
%endif

%files efi-unsigned
/usr/share/grub2-efi/*

%files efi-binary
%ifarch x86_64
/boot/efi/EFI/BOOT/grubx64.efi
%endif
%ifarch aarch64
/boot/efi/EFI/BOOT/grubaa64.efi
%endif

%if 0%{?with_signed}
%files efi-binary-signed
%endif

%ifarch aarch64
%files efi
%{_libdir}/grub/*
%endif

%files lang
%defattr(-,root,root)
%{_datarootdir}/locale/*

%changelog
*   Thu Jul 30 2020 Chris Co <chrco@microsoft.com> 2.02-23
-   Fix CVE-2020-10713 (BootHole)
-   Fix CVE-2020-14308
-   Fix CVE-2020-14309
-   Fix CVE-2020-14310
-   Fix CVE-2020-14311
-   Fix CVE-2020-15706
-   Fix CVE-2020-15707
*   Wed Jul 22 2020 Joe Schmitt <joschmit@microsoft.com> 2.02-22
-   Always include Patch100, but conditionally apply it.
-   Switch URL to https.
*   Tue Jun 30 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.02-21
-   Add cryptodisk, luks, gcry_rijndael and gcry_sha512 modules to EFI files.
*   Fri Jun 19 2020 Chris Co <chrco@microsoft.com> 2.02-20
-   Add grub2-efi-binary subpackage
-   Add grub2-efi-binary-signed subpackage and macros for adding offline signed grub binaries
*   Mon Jun 01 2020 Henry Beberman <henry.beberman@microsoft.com> 2.02-19
-   Address compilation errors from hardened cflags.
*   Tue May 26 2020 Emre Girgin <mrgirgin@microsoft.com> 2.02-18
-   Change /boot directory permissions to 600.
*   Fri May 22 2020 Chris Co <chrco@microsoft.com> - 2.02-17
-   Create grubaa64.efi as part of the grub2-efi-unsigned subpackage
*   Wed May 13 2020 Nick Samson <nisamson@microsoft.com> - 2.02-16
-   Added %%license line automatically
*   Mon May 11 2020 Chris Co <chrco@microsoft.com> 2.02-15
-   Create new grub2-efi-unsigned subpackage containing grubx64.efi
*   Thu Apr 30 2020 Chris Co <chrco@microsoft.com> 2.02-14
-   Add fdt rework patch to fix aarch64 build errors
-   Enable aarch64 build
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.02-13
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.02-12
-   Update grub version from ~rc3 to release.
-   Enhance SB + TPM support (19 patches from grub2-2.02-70.fc30)
-   Remove i386-pc modules from grub2-efi
*   Fri Jan 25 2019 Alexey Makhalov <amakhalov@vmware.com> 2.02-11
-   Disable efinet for aarch64 to workwround NXP ls1012a frwy PFE bug.
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.02-10
-   Aarch64 support
*   Fri Jun 2  2017 Bo Gan <ganb@vmware.com> 2.02-9
-   Split grub2 to grub2 and grub2-pc, remove grub2-efi spec
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com>  2.02-8
-   Version update to 2.02~rc2
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  2.02-7
-   Add fix for CVE-2015-8370
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  2.02-6
-   Change systemd dependency
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.02-5
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.02-4
-   GA - Bump release of all rpms
*   Fri Oct 02 2015 Divya Thaluru <dthaluru@vmware.com> 2.02-3
-   Adding patch to boot entries with out password.
*   Wed Jul 22 2015 Divya Thaluru <dthaluru@vmware.com> 2.02-2
-   Changing program name from grub to grub2.
*   Mon Jun 29 2015 Divya Thaluru <dthaluru@vmware.com> 2.02-1
-   Updating grub to 2.02
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.00-1
-   Initial build.  First version
