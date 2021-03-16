%define debug_package %{nil}
%define __os_install_post %{nil}

# Gnulib does not produce source tarball releases, and grub's bootstrap.conf
# bakes in a specific commit id to pull (GNULIB_REVISION). Use this commit id below.
%global gnulibversion d271f868a8df9bbec29049d01e056481b7a1a263

Summary:        GRand Unified Bootloader
Name:           grub2
Version:        2.06
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.gnu.org/software/grub
Source0:        https://git.savannah.gnu.org/cgit/grub.git/snapshot/grub-%{version}-rc1.tar.gz
Source1:        https://git.savannah.gnu.org/cgit/gnulib.git/snapshot/gnulib-%{gnulibversion}.tar.gz
Source2:        sbat.csv.in

BuildRequires:  device-mapper-devel
BuildRequires:  systemd-devel
BuildRequires:  xz-devel
BuildRequires:  autoconf

Requires:       device-mapper
Requires:       xz

%description
The GRUB package contains the GRand Unified Bootloader.

%ifarch x86_64
%package pc
Summary:        GRUB Library for BIOS
Group:          System Environment/Programming

Requires:       %{name} = %{version}

%description pc
Additional library files for grub
%endif

%package efi
Summary:        GRUB Library for UEFI
Group:          System Environment/Programming

Requires:       %{name} = %{version}

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

%description efi-binary
GRUB UEFI bootloader binaries

%prep
%setup -q -n grub-%{version}-rc1
cp %{SOURCE1} gnulib-%{gnulibversion}.tar.gz
tar -zxf gnulib-%{gnulibversion}.tar.gz
mv gnulib-%{gnulibversion} gnulib

%build
./bootstrap --no-git --gnulib-srcdir=./gnulib
%ifarch x86_64
mkdir build-for-pc
pushd build-for-pc
# Modify the default CFLAGS to support the i386 build
# TODO: Identify which CFLAGS are causing HyperV Gen1 build to fail to boot
CFLAGS=""
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
mkdir %{buildroot}%{_sysconfdir}/sysconfig
ln -sf %{_sysconfdir}/default/grub %{buildroot}%{_sysconfdir}/sysconfig/grub
install -vdm 700 %{buildroot}/boot/%{name}
touch %{buildroot}/boot/%{name}/grub.cfg
chmod 600 %{buildroot}/boot/%{name}/grub.cfg
rm -rf %{buildroot}%{_infodir}

# Add SBAT
sed -e "s,@@VERSION@@,%{version}-%{release},g" %{SOURCE2} > ./sbat.csv
cat ./sbat.csv

# Generate grub efi image
install -d %{buildroot}%{_datadir}/grub2-efi
%ifarch x86_64
./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/x86_64-efi/ --sbat ./sbat.csv -o %{buildroot}%{_datadir}/grub2-efi/grubx64.efi -p /boot/grub2 -O x86_64-efi fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop efi_uga ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm cryptodisk luks gcry_rijndael gcry_sha512
%endif
%ifarch aarch64
./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/arm64-efi/ --sbat ./sbat.csv -o %{buildroot}%{_datadir}/grub2-efi/grubaa64.efi -p /boot/grub2 -O arm64-efi fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm cryptodisk luks gcry_rijndael gcry_sha512
%endif

# Install to efi directory
EFI_BOOT_DIR=%{buildroot}/boot/efi/EFI/BOOT
GRUB_MODULE_NAME=
GRUB_MODULE_SOURCE=

install -d $EFI_BOOT_DIR

%ifarch x86_64
GRUB_MODULE_NAME=grubx64.efi
GRUB_MODULE_SOURCE=%{buildroot}%{_datadir}/grub2-efi/grubx64.efi
%endif

%ifarch aarch64
GRUB_MODULE_NAME=grubaa64.efi
GRUB_MODULE_SOURCE=%{buildroot}%{_datadir}/grub2-efi/grubaa64.efi
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
%config() %{_sysconfdir}/grub.d/30_uefi-firmware
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
%{_datadir}/grub2-efi/*

%files efi-binary
%ifarch x86_64
/boot/efi/EFI/BOOT/grubx64.efi
%endif
%ifarch aarch64
/boot/efi/EFI/BOOT/grubaa64.efi
%endif

%ifarch aarch64
%files efi
%{_libdir}/grub/*
%endif

%changelog
* Wed Mar 10 2021 Chris Co <chrco@microsoft.com> - 2.06-1
- Update to 2.06-rc1
- Incorporate SBAT data
- Remove grub2-lang (locale) subpackage

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
