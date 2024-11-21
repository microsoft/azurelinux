%define debug_package %{nil}
%define __os_install_post %{nil}
# Gnulib does not produce source tarball releases, and grub's bootstrap.conf
# bakes in a specific commit id to pull (GNULIB_REVISION).
%global gnulibversion 9f48fb992a3d7e96610c4ce8be969cff2d61a01b
%undefine distro_module_ldflags
Summary:        GRand Unified Bootloader
Name:           grub2
Version:        2.12
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/System
URL:            https://www.gnu.org/software/grub
Source0:        https://git.savannah.gnu.org/cgit/grub.git/snapshot/grub-%{version}.tar.gz
Source1:        https://git.savannah.gnu.org/cgit/gnulib.git/snapshot/gnulib-%{gnulibversion}.tar.gz
Source2:        sbat.csv.in
Source3:        macros.grub2
# The Azure Linux team created this patch since the gcc version in use at the
# time optimizes the code incorrectly, leading to network traffic getting
# dropped in scenarios like PXE booting.
Patch:          disable-checksum-code-optimization.patch
BuildRequires:  autoconf
BuildRequires:  device-mapper-devel
BuildRequires:  python3
BuildRequires:  xz-devel
Requires:       device-mapper
Requires:       systemd-udev
Requires:       xz
Requires:       %{name}-tools-minimal = %{version}-%{release}

# Some distros split 'grub2' into more subpackages. For now we're bundling it all together
# inside the default package and adding these 'Provides' to make installation more user-friendly
# for people used to other distributions.
Provides:       %{name}-common = %{version}-%{release}
Provides:       %{name}-tools = %{version}-%{release}
Provides:       %{name}-tools-efi = %{version}-%{release}
Provides:       %{name}-tools-extra = %{version}-%{release}

%description
The GRUB package contains the GRand Unified Bootloader.

%ifarch x86_64
%package pc
Summary:        GRUB Library for BIOS
Group:          System Environment/Programming
Requires:       %{name} = %{version}

# Some distros split 'grub2' into more subpackages. For now we're bundling it all together
# inside the default package and adding these 'Provides' to make installation more user-friendly
# for people used to other distributions.
Provides:       %{name}-pc-modules = %{version}-%{release}

%description pc
Additional library files for grub
%endif

%package efi
Summary:        GRUB Library for UEFI
Group:          System Environment/Programming
Requires:       %{name} = %{version}

# Some distros split 'grub2' into more subpackages. For now we're bundling it all together
# inside the default package and adding these 'Provides' to make installation more user-friendly
# for people used to other distributions.
Provides:       %{name}-efi-modules = %{version}-%{release}

%ifarch x86_64
Provides:       %{name}-efi-x64-modules = %{version}-%{release}
%endif

%ifarch aarch64
Provides:       %{name}-efi-aa64-modules = %{version}-%{release}
%endif

%description efi
Additional library files for grub

%package efi-unsigned
Summary:        Unsigned GRUB UEFI image
Group:          System Environment/Base

%description efi-unsigned
Unsigned GRUB UEFI image

%package efi-binary
Summary:        GRUB UEFI image
Group:          System Environment/Base
Requires:       %{name}-tools-minimal = %{version}-%{release}

# Some distros split 'grub2' into more subpackages. For now we're bundling it all together
# inside the default package and adding these 'Provides' to make installation more user-friendly
# for people used to other distributions.
%ifarch x86_64
Provides:       %{name}-efi-x64 = %{version}-%{release}
%endif

%description efi-binary
GRUB UEFI bootloader binaries

%package efi-binary-noprefix
Summary:        GRUB UEFI image with no prefix directory set
Group:          System Environment/Base
Requires:       %{name}-tools-minimal = %{version}-%{release}

%description efi-binary-noprefix
GRUB UEFI bootloader binaries with no prefix directory set

%package rpm-macros
Summary:        GRUB RPM Macros
Group:          System Environment/Base

%description rpm-macros
GRUB RPM Macros for enabling package updates supporting
the grub2-mkconfig flow on AzureLinux

%package configuration
Summary:        Location for local grub configurations
Group:          System Environment/Base

%description configuration
Directory for package-specific boot configurations
to be persistently stored on AzureLinux

%package tools-minimal
Summary:        Minimal set of utilities to configure a grub-based system
Group:          System Environment/Base
Requires:       %{name}-configuration = %{version}-%{release}

%description tools-minimal
Minimal set of utilities to configure a grub-based system

%prep

%autosetup -p1 -n grub-%{version}
cp %{SOURCE1} gnulib-%{gnulibversion}.tar.gz
tar -zxf gnulib-%{gnulibversion}.tar.gz
mv gnulib-%{gnulibversion} gnulib

%build
# Add linker option -d "assign space to common symbols", otherwise some symbols in grub's
# kernel.img will be assigned to the SHN_COMMON section which is not supported by grub-mkimage
LDFLAGS="-Wl,-d %{build_ldflags}"
export LDFLAGS

export PYTHON=%{python3}
./bootstrap --no-git --gnulib-srcdir=./gnulib
%ifarch x86_64
mkdir build-for-pc
pushd build-for-pc
# Modify the default CFLAGS to support the i386 build
CFLAGS="`echo " %{build_cflags} "          | \
        sed 's/-fcf-protection//'          | \
        sed 's/-fstack-protector-strong//' | \
        sed 's/-m64//'                     | \
        sed 's/-specs.*cc1//'              | \
        sed 's/-mtune=generic//'           | \
        sed 's/-O. //'                     | \
        sed 's/-fexceptions//'             | \
        sed 's/-Wp,-D_FORTIFY_SOURCE=2//'`"
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
# Note: bin & sbin binaries are expected to differ due to different CFLAGS
# Just compare files under _sysconfdir and _datarootdir
diff -sr install-for-efi%{_sysconfdir} install-for-pc%{_sysconfdir}
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
mkdir %{buildroot}%{_sysconfdir}/default/grub.d
mkdir %{buildroot}%{_sysconfdir}/sysconfig
ln -sf %{_sysconfdir}/default/grub %{buildroot}%{_sysconfdir}/sysconfig/grub
install -vdm 700 %{buildroot}/boot/%{name}
touch %{buildroot}/boot/%{name}/grub.cfg
chmod 400 %{buildroot}/boot/%{name}/grub.cfg
rm -rf %{buildroot}%{_infodir}

# Add SBAT
sed -e "s,@@VERSION@@,%{version},g" -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" %{SOURCE2} > ./sbat.csv
cat ./sbat.csv

# Generate grub efi image
install -d %{buildroot}%{_datadir}/grub2-efi
%ifarch x86_64
./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/x86_64-efi/ --sbat ./sbat.csv -o %{buildroot}%{_datadir}/grub2-efi/grubx64.efi -p /boot/grub2 -O x86_64-efi fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop efi_uga ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm cryptodisk luks gcry_rijndael gcry_sha512 tpm efinet tftp multiboot2 xfs
./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/x86_64-efi/ --sbat ./sbat.csv -o %{buildroot}%{_datadir}/grub2-efi/grubx64-noprefix.efi --prefix= -O x86_64-efi fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop efi_uga ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm cryptodisk luks gcry_rijndael gcry_sha512 tpm efinet tftp multiboot2 xfs
%endif
%ifarch aarch64
./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/arm64-efi/ --sbat ./sbat.csv -o %{buildroot}%{_datadir}/grub2-efi/grubaa64.efi -p /boot/grub2 -O arm64-efi fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm cryptodisk luks gcry_rijndael gcry_sha512 tpm efinet tftp xfs
./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/arm64-efi/ --sbat ./sbat.csv -o %{buildroot}%{_datadir}/grub2-efi/grubaa64-noprefix.efi --prefix= -O arm64-efi fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm cryptodisk luks gcry_rijndael gcry_sha512 tpm efinet tftp xfs
%endif

# Install to efi directory
EFI_BOOT_DIR=%{buildroot}/boot/efi/EFI/BOOT
GRUB_MODULE_NAME=
GRUB_MODULE_SOURCE=

install -d $EFI_BOOT_DIR

# Install grub2 macros
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -m 644 %{SOURCE3} %{buildroot}/%{_rpmconfigdir}/macros.d

%ifarch x86_64
GRUB_MODULE_NAME=grubx64.efi
GRUB_PXE_MODULE_NAME=grubx64-noprefix.efi
GRUB_MODULE_SOURCE=%{buildroot}%{_datadir}/grub2-efi/grubx64.efi
GRUB_PXE_MODULE_SOURCE=%{buildroot}%{_datadir}/grub2-efi/grubx64-noprefix.efi
%endif

%ifarch aarch64
GRUB_MODULE_NAME=grubaa64.efi
GRUB_PXE_MODULE_NAME=grubaa64-noprefix.efi
GRUB_MODULE_SOURCE=%{buildroot}%{_datadir}/grub2-efi/grubaa64.efi
GRUB_PXE_MODULE_SOURCE=%{buildroot}%{_datadir}/grub2-efi/grubaa64-noprefix.efi
%endif

cp $GRUB_MODULE_SOURCE $EFI_BOOT_DIR/$GRUB_MODULE_NAME
cp $GRUB_PXE_MODULE_SOURCE $EFI_BOOT_DIR/$GRUB_PXE_MODULE_NAME

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%dir /boot/%{name}
%config() %{_sysconfdir}/bash_completion.d/grub
%{_sysconfdir}/sysconfig/grub
/sbin/grub2-bios-setup
/sbin/grub2-install
/sbin/grub2-macbless
/sbin/grub2-ofpathname
/sbin/grub2-reboot
/sbin/grub2-set-default
/sbin/grub2-sparc64-setup
%{_bindir}/grub2-fstest
%{_bindir}/grub2-glue-efi
%{_bindir}/grub2-kbdcomp
%{_bindir}/grub2-menulst2cfg
%{_bindir}/grub2-mkimage
%{_bindir}/grub2-mklayout
%{_bindir}/grub2-mknetdir
%{_bindir}/grub2-mkpasswd-pbkdf2
%{_bindir}/grub2-mkrescue
%{_bindir}/grub2-mkstandalone
%{_bindir}/grub2-render-label
%{_bindir}/grub2-syslinux2cfg

%files tools-minimal
%{_datarootdir}/grub/grub-mkconfig_lib
/sbin/grub2-probe
/sbin/grub2-mkconfig
%{_bindir}/grub2-editenv
%{_bindir}/grub2-script-check
%{_bindir}/grub2-file
%{_bindir}/grub2-mkrelpath

%ifarch x86_64
%files pc
%{_libdir}/grub/i386-pc

%files efi
%{_libdir}/grub/x86_64-efi
%endif

%files efi-unsigned
%{_datadir}/grub2-efi/*

%files efi-binary
%ifarch x86_64
/boot/efi/EFI/BOOT/grubx64.efi
%endif
%ifarch aarch64
/boot/efi/EFI/BOOT/grubaa64.efi
%endif

%files efi-binary-noprefix
%ifarch x86_64
/boot/efi/EFI/BOOT/grubx64-noprefix.efi
%endif
%ifarch aarch64
/boot/efi/EFI/BOOT/grubaa64-noprefix.efi
%endif

%ifarch aarch64
%files efi
%{_libdir}/grub/*
%endif

%files rpm-macros
%{_rpmconfigdir}/macros.d/macros.grub2

%files configuration
%dir %{_sysconfdir}/grub.d
%dir %{_sysconfdir}/default/grub.d
%{_sysconfdir}/grub.d/README
%attr(0644,root,root) %ghost %config(noreplace) %{_sysconfdir}/default/grub
%ghost %config(noreplace) /boot/%{name}/grub.cfg
%config() %{_sysconfdir}/grub.d/00_header
%config() %{_sysconfdir}/grub.d/10_linux
%config() %{_sysconfdir}/grub.d/20_linux_xen
%config() %{_sysconfdir}/grub.d/25_bli
%config() %{_sysconfdir}/grub.d/30_os-prober
%config() %{_sysconfdir}/grub.d/30_uefi-firmware
%config(noreplace) %{_sysconfdir}/grub.d/40_custom
%config(noreplace) %{_sysconfdir}/grub.d/41_custom

%changelog
* Fri Jun 14 2024 Gary Swalling <gaswal@microsoft.com> - 2.12-1
- Upgrade to 2.12 - fixes and features in latest full release

* Wed Jun 12 2024 George Mileka <gmileka@microsoft.com> - 2.06-19
- disable code optimization for ip checksum calculation

* Mon Apr 15 2024 Dan Streetman <ddstreet@microsoft.com> - 2.06-18
- update grub to sbat 4

* Tue Mar 19 2024 Cameron Baird <cameronbaird@microsoft.com> - 2.06-17
- Introduce grub2-tools-minimal subpackage

* Wed Mar 06 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.06-16
- Updated sbat.csv.in to reflect new distro name.

* Tue Mar 05 2024 Cameron Baird <cameronbaird@microsoft.com> - 2.06-15
- Explicitly depend on systemd-udev for image install

* Thu Jan 25 10:49:55 EST 2024 Dan Streetman <ddstreet@ieee.org> - 2.06-14
- remove systemd-devel build dep

* Mon Nov 27 2023 Cameron Baird <cameronbaird@microsoft.com> - 2.06-13
- Move /etc/grub.d to the configuration subpackage

* Wed Oct 18 2023 Gary Swalling <gaswal@microsoft.com> - 2.06-12
- CVE-2021-3695 CVE-2021-3696 CVE-2021-3697 CVE-2022-28733 CVE-2022-28734
  CVE-2022-28735 CVE-2022-28736 and increment SBAT level to 2

* Fri Aug 11 2023 Cameron Baird <cameronbaird@microsoft.com> - 2.06-11
- Enable support for grub2-mkconfig grub.cfg generation
- Introduce rpm-macros, configuration subpackage
- The Mariner /etc/default/grub now sources files from /etc/default/grub.d
    before the remainder of grub2-mkconfig runs. This allows RPM to 
    install package-specific configurations that the users can safely
    override.

* Thu Jun 08 2023 Daniel McIlvaney <damcilva@microsoft.com> - 2.06-10
- CVE-2022-3775

* Wed Apr 05 2023 Andy Zaugg <azaugg@linkedin.com> - 2.06-9
- Adding XFS support to GRUB

* Thu Dec 29 2022 Mykhailo Bykhovtsev <mbykhovtsev@microsoft@microsoft.com> - 2.06-8
- Fix CVE-2022-2601 (Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com>).

* Wed Sep 07 2022 Zhichun Wan <zhichunwan@microsoft.com> - 2.06-7
- Port internal patch for reseting grub_errno on success (George mileka <gmileka@microsoft.com>).

* Thu Jul 28 2022 Minghe Ren <mingheren@microsoft.com> - 2.06-6
- Change permission on grub.cfg to improve security

* Tue Jul 19 2022 Henry Li <lihl@microsoft.com> - 2.06-5
- Resolve CVE-2021-3981
- Remove specification of nopatch files in the spec file

* Fri Jul 08 2022 Henry Li <lihl@microsoft.com> - 2.06-4
- Create additional efi binary that has no prefix directory set
- Add grub2-efi-binary-noprefix subpackage for efi binary with no prefix set

* Fri Feb 25 2022 Henry Li <lihl@microsoft.com> - 2.06-3
- Enable multiboot2 support for x86_64

* Thu Feb 17 2022 Andrew Phelps <anphel@microsoft.com> - 2.06-2
- Use _topdir instead of hard-coded value /usr/src/mariner

* Wed Feb 09 2022 Chris Co <chrco@microsoft.com> - 2.06-1
- Update to 2.06 release
- Add efinet and tftp modules to grub efi binary

* Tue Feb 08 2022 Chris Co <chrco@microsoft.com> - 2.06~rc1-8
- Bump release number to force binary signing with new secure boot key

* Tue Sep 14 2021 Andrew Phelps <anphel@microsoft.com> - 2.06~rc1-7
- Disable module_info.ld script due to issue with ELF metadata note

* Tue Jul 20 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.06~rc1-6
- License verified.
- Adding 'Provides' for:
  - 'grub2-common',
  - 'grub2-efi-aa64-modules',
  - 'grub2-efi-modules',
  - 'grub2-efi-x64',
  - 'grub2-efi-x64-modules',
  - 'grub2-pc-modules',
  - 'grub2-tools',
  - 'grub2-tools-efi',
  - 'grub2-tools-extra',
  - 'grub2-tools-minimal'.

* Tue May 25 2021 Thomas Crain <thcrain@microsoft.com> - 2.06~rc1-5
- Explicitly specify python 3 as the python interpreter for bootstrapping

* Fri Apr 16 2021 Chris Co <chrco@microsoft.com> - 2.06~rc1-4
- Bump version to match grub-efi-binary-signed spec

* Fri Apr 02 2021 Rachel Menge <rachelmenge@microsoft.com> - 2.06~rc1-3
- Apply no patches for CVE-2021-3418 CVE-2020-14372 CVE-2020-25632
  CVE-2020-25647 CVE-2020-27779 CVE-2021-20233 CVE-2020-10713 CVE-2020-14308
  CVE-2020-14309 CVE-2020-14310 CVE-2020-14311 CVE-2020-27749 CVE-2021-20225

* Fri Mar 26 2021 Chris Co <chrco@microsoft.com> - 2.06~rc1-2
- Add a few more F34 patches (017, 037, 052, 069, 166)

* Wed Mar 10 2021 Chris Co <chrco@microsoft.com> - 2.06~rc1-1
- Update to 2.06-rc1. Remove old out-of-tree patches. Add patches from F34
- Incorporate SBAT data
- Remove grub2-lang (locale) subpackage
- Enable tpm module to EFI binary

* Mon Dec 14 2020 Andrew Phelps <anphel@microsoft.com> - 2.02-26
- Modify check test

* Fri Oct 30 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.02-25
- Fix CVE-2020-15705 (BootHole cont.).

* Thu Aug 13 2020 Chris Co <chrco@microsoft.com> - 2.02-24
- Remove signed subpackage and macro

* Thu Jul 30 2020 Chris Co <chrco@microsoft.com> - 2.02-23
- Fix CVE-2020-10713 (BootHole)
- Fix CVE-2020-14308
- Fix CVE-2020-14309
- Fix CVE-2020-14310
- Fix CVE-2020-14311
- Fix CVE-2020-15706
- Fix CVE-2020-15707

* Wed Jul 22 2020 Joe Schmitt <joschmit@microsoft.com> - 2.02-22
- Always include Patch100, but conditionally apply it.
- Switch URL to https.

* Tue Jun 30 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.02-21
- Add cryptodisk, luks, gcry_rijndael and gcry_sha512 modules to EFI files.

* Fri Jun 19 2020 Chris Co <chrco@microsoft.com> - 2.02-20
- Add grub2-efi-binary subpackage
- Add grub2-efi-binary-signed subpackage and macros for adding offline signed grub binaries

* Mon Jun 01 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.02-19
- Address compilation errors from hardened cflags.

* Tue May 26 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.02-18
- Change /boot directory permissions to 600.

* Fri May 22 2020 Chris Co <chrco@microsoft.com> - 2.02-17
- Create grubaa64.efi as part of the grub2-efi-unsigned subpackage

* Wed May 13 2020 Nick Samson <nisamson@microsoft.com> - 2.02-16
- Added %%license line automatically

* Mon May 11 2020 Chris Co <chrco@microsoft.com> - 2.02-15
- Create new grub2-efi-unsigned subpackage containing grubx64.efi

* Thu Apr 30 2020 Chris Co <chrco@microsoft.com> - 2.02-14
- Add fdt rework patch to fix aarch64 build errors
- Enable aarch64 build

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.02-13
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> - 2.02-12
- Update grub version from ~rc3 to release.
- Enhance SB + TPM support (19 patches from grub2-2.02-70.fc30)
- Remove i386-pc modules from grub2-efi

* Fri Jan 25 2019 Alexey Makhalov <amakhalov@vmware.com> - 2.02-11
- Disable efinet for aarch64 to workwround NXP ls1012a frwy PFE bug.

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.02-10
- Aarch64 support

* Fri Jun 2  2017 Bo Gan <ganb@vmware.com> - 2.02-9
- Split grub2 to grub2 and grub2-pc, remove grub2-efi spec

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.02-8
- Version update to 2.02~rc2

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com> - 2.02-7
- Add fix for CVE-2015-8370

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com> - 2.02-6
- Change systemd dependency

* Thu Oct 06 2016 ChangLee <changlee@vmware.com> - 2.02-5
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.02-4
- GA - Bump release of all rpms

* Fri Oct 02 2015 Divya Thaluru <dthaluru@vmware.com> - 2.02-3
- Adding patch to boot entries with out password.

* Wed Jul 22 2015 Divya Thaluru <dthaluru@vmware.com> - 2.02-2
- Changing program name from grub to grub2.

* Mon Jun 29 2015 Divya Thaluru <dthaluru@vmware.com> - 2.02-1
- Updating grub to 2.02

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 2.00-1
- Initial build.  First version
