# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This package calls binutils components directly and would need to pass
# in flags to enable the LTO plugins
# Disable LTO
%global _lto_cflags %{nil}

%undefine _hardened_build
%undefine _package_note_file

%global tarversion 2.12
%undefine _missing_build_ids_terminate_build
%global _configure_gnuconfig_hack 0

# It's a commit from their gnulib's development tree.  They don't do releases,
# and it is *awful* to update this.
%global gnulibversion 9f48fb992a3d7e96610c4ce8be969cff2d61a01b

Name:		grub2
Epoch:		1
Version:	2.12
Release: 41%{?dist}
Summary:	Bootloader with support for Linux, Multiboot and more
License:	GPL-3.0-or-later
URL:		http://www.gnu.org/software/grub/
Obsoletes:	grub < 1:0.98
Source0:	https://ftp.gnu.org/gnu/grub/grub-%{tarversion}.tar.xz
Source1:	grub.macros
Source2:	gnulib-%{gnulibversion}.tar.gz
Source3:	99-grub-mkconfig.install
Source4:	http://unifoundry.com/pub/unifont/unifont-13.0.06/font-builds/unifont-13.0.06.pcf.gz
Source5:	theme.tar.bz2
Source6:	gitignore
Source7:	bootstrap
Source8:	bootstrap.conf
Source9:	strtoull_test.c
Source10:	20-grub.install
Source11:	grub.patches
Source12:	sbat.csv.in
Source13:	gen_grub_cfgstub
Source14:	55-set-boot-entry.install

%include %{SOURCE1}

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	binutils
BuildRequires:	bison
BuildRequires:	bzip2-devel
BuildRequires:	dejavu-sans-fonts
BuildRequires:	device-mapper-devel
BuildRequires:	efi-srpm-macros
BuildRequires:	flex
BuildRequires:	freetype-devel
BuildRequires:	freetype-devel
BuildRequires:	fuse3-devel
BuildRequires:	gcc
BuildRequires:	gettext-devel
BuildRequires:	git
BuildRequires:	help2man
BuildRequires:	ncurses-devel
BuildRequires:	python3
BuildRequires:	rpm-devel
BuildRequires:	rpm-libs
BuildRequires:	squashfs-tools
BuildRequires:	texinfo
BuildRequires:	xz-devel

# For %%_userunitdir and %%systemd_* macros
BuildRequires:	systemd-rpm-macros

%ifarch %{efi_arch}
BuildRequires:	pesign >= 0.99-8
%endif

%if %{?_with_ccache: 1}%{?!_with_ccache: 0}
BuildRequires:	ccache
%endif

ExcludeArch:	s390 s390x %{ix86}
Obsoletes:	grub2 <= %{evr}

%if 0%{with_legacy_arch}
Requires:	grub2-%{legacy_package_arch} = %{evr}
%else
Requires:	grub2-%{package_arch} = %{evr}
%endif

%global desc \
The GRand Unified Bootloader (GRUB) is a highly configurable and \
customizable bootloader with modular architecture.  It supports a rich \
variety of kernel formats, file systems, computer architectures and \
hardware devices.\
%{nil}

# generate with do-rebase
%include %{SOURCE11}

%description
%{desc}

%package common
Summary:	grub2 common layout
BuildArch:	noarch
Conflicts:	grubby < 8.40-18
Requires(posttrans): util-linux-core
Requires(posttrans): coreutils
Requires(posttrans): grep

%description common
This package provides some directories which are required by various grub2
subpackages.

%package tools
Summary:	Support tools for GRUB.
Requires:	grub2-common = %{epoch}:%{version}-%{release}
Requires:	gettext-runtime os-prober file
Requires(pre):	dracut
Requires(pre):	grep
Requires(pre):	sed
%{?systemd_requires}

%description tools
%{desc}
This subpackage provides tools for support of all platforms.

%ifarch x86_64
%package tools-efi
Summary:	Support tools for GRUB.
Requires:	gettext-runtime os-prober file
Requires:	grub2-common = %{epoch}:%{version}-%{release}

%description tools-efi
%{desc}
This subpackage provides tools for support of EFI platforms.
%endif

%package tools-minimal
Summary:	Support tools for GRUB.
Requires:	gettext-runtime
Requires:	grub2-common = %{epoch}:%{version}-%{release}

%description tools-minimal
%{desc}
This subpackage provides tools for support of all platforms.

%package tools-extra
Summary:	Support tools for GRUB.
Requires:	gettext-runtime os-prober file
Requires:	grub2-tools-minimal = %{epoch}:%{version}-%{release}
Requires:	grub2-common = %{epoch}:%{version}-%{release}
Requires:	mtools

%description tools-extra
%{desc}
This subpackage provides tools for support of all platforms.

%if 0%{with_efi_arch}
%{expand:%define_efi_variant %%{package_arch} -o}
%endif
%if 0%{with_alt_efi_arch}
%{expand:%define_efi_variant %%{alt_package_arch}}
%endif
%if 0%{with_legacy_arch}
%{expand:%define_legacy_variant %%{legacy_package_arch}}
%endif
%if 0%{with_xen_arch}
%{expand:%define_xen_variant %%{xen_package_arch} -o}
%endif
%if 0%{with_xen_pvh_arch}
%{expand:%define_xen_pvh_variant %%{xen_pvh_package_arch} -o}
%endif

%if 0%{with_emu_arch}
%package emu
Summary:	GRUB user-space emulation.
Requires:	grub2-tools-minimal = %{epoch}:%{version}-%{release}

%description emu
%{desc}
This subpackage provides the GRUB user-space emulation support of all platforms.

%package emu-modules
Summary:	GRUB user-space emulation modules.
Requires:	grub2-tools-minimal = %{epoch}:%{version}-%{release}

%description emu-modules
%{desc}
This subpackage provides the GRUB user-space emulation modules.
%endif

%prep
%do_common_setup
%if 0%{with_efi_arch}
mkdir grub-%{grubefiarch}-%{tarversion}
grep -A100000 '# stuff "make" creates' .gitignore > grub-%{grubefiarch}-%{tarversion}/.gitignore
cp %{SOURCE4} grub-%{grubefiarch}-%{tarversion}/unifont.pcf.gz
sed -e "s,@@VERSION@@,%{version},g" -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" \
    %{SOURCE12} > grub-%{grubefiarch}-%{tarversion}/sbat.csv
git add grub-%{grubefiarch}-%{tarversion}
%endif
%if 0%{with_alt_efi_arch}
mkdir grub-%{grubaltefiarch}-%{tarversion}
grep -A100000 '# stuff "make" creates' .gitignore > grub-%{grubaltefiarch}-%{tarversion}/.gitignore
cp %{SOURCE4} grub-%{grubaltefiarch}-%{tarversion}/unifont.pcf.gz
git add grub-%{grubaltefiarch}-%{tarversion}
%endif
%if 0%{with_legacy_arch}
mkdir grub-%{grublegacyarch}-%{tarversion}
grep -A100000 '# stuff "make" creates' .gitignore > grub-%{grublegacyarch}-%{tarversion}/.gitignore
cp %{SOURCE4} grub-%{grublegacyarch}-%{tarversion}/unifont.pcf.gz
git add grub-%{grublegacyarch}-%{tarversion}
%endif
%if 0%{with_emu_arch}
mkdir grub-emu-%{tarversion}
grep -A100000 '# stuff "make" creates' .gitignore > grub-emu-%{tarversion}/.gitignore
cp %{SOURCE4} grub-emu-%{tarversion}/unifont.pcf.gz
git add grub-emu-%{tarversion}
%endif
%if 0%{with_xen_arch}
mkdir grub-%{grubxenarch}-%{tarversion}
grep -A100000 '# stuff "make" creates' .gitignore > grub-%{grubxenarch}-%{tarversion}/.gitignore
cp %{SOURCE4} grub-%{grubxenarch}-%{tarversion}/unifont.pcf.gz
sed -e "s,@@VERSION@@,%{version},g" -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" \
    %{SOURCE12} > grub-%{grubxenarch}-%{tarversion}/sbat.csv
git add grub-%{grubxenarch}-%{tarversion}
%endif
%if 0%{with_xen_pvh_arch}
mkdir grub-%{grubxenpvharch}-%{tarversion}
grep -A100000 '# stuff "make" creates' .gitignore > grub-%{grubxenpvharch}-%{tarversion}/.gitignore
cp %{SOURCE4} grub-%{grubxenpvharch}-%{tarversion}/unifont.pcf.gz
sed -e "s,@@VERSION@@,%{version},g" -e "s,@@VERSION_RELEASE@@,%{version}-%{release},g" \
    %{SOURCE12} > grub-%{grubxenpvharch}-%{tarversion}/sbat.csv
git add grub-%{grubxenpvharch}-%{tarversion}
%endif
git commit -m "After making subdirs"

%build
%if 0%{with_efi_arch}
%{expand:%do_primary_efi_build %%{grubefiarch} %%{grubefiname} %%{grubeficdname} %%{_target_platform} %%{efi_target_cflags} %%{efi_host_cflags}}
%endif
%if 0%{with_alt_efi_arch}
%{expand:%do_alt_efi_build %%{grubaltefiarch} %%{grubaltefiname} %%{grubalteficdname} %%{_alt_target_platform} %%{alt_efi_target_cflags} %%{alt_efi_host_cflags}}
%endif
%if 0%{with_legacy_arch}
%{expand:%do_legacy_build %%{grublegacyarch}}
%endif
%if 0%{with_emu_arch}
%{expand:%do_emu_build}
%endif
%if 0%{with_xen_arch}
%{expand:%do_xen_build %%{grubxenarch} %%{_target_platform} %%{xen_target_cflags} %%{xen_host_cflags}}
%endif
%if 0%{with_xen_pvh_arch}
%{expand:%do_xen_pvh_build %%{grubxenpvharch} %%{_target_platform} %%{xen_pvh_target_cflags} %%{xen_pvh_host_cflags}}
%endif
%ifarch ppc64le
%{expand:%do_ieee1275_build_images %%{grublegacyarch} %{grubelfname} %{sb_cer} %{sb_key}}
%endif
makeinfo --info --no-split -I docs -o docs/grub-dev.info \
	docs/grub-dev.texi
makeinfo --info --no-split -I docs -o docs/grub.info \
	docs/grub.texi
makeinfo --html --no-split -I docs -o docs/grub-dev.html \
	docs/grub-dev.texi
makeinfo --html --no-split -I docs -o docs/grub.html \
	docs/grub.texi

%install
set -e
rm -fr $RPM_BUILD_ROOT

%do_common_install
%if 0%{with_efi_arch}
%{expand:%do_efi_install %%{grubefiarch} %%{grubefiname} %%{grubeficdname}}
%endif
%if 0%{with_alt_efi_arch}
%{expand:%do_alt_efi_install %%{grubaltefiarch} %%{grubaltefiname} %%{grubalteficdname}}
%endif
%if 0%{with_legacy_arch}
%{expand:%do_legacy_install %%{grublegacyarch} %%{alt_grub_target_name} 0%{with_efi_arch}}
%endif
%if 0%{with_emu_arch}
%{expand:%do_emu_install %%{package_arch}}
%endif
%if 0%{with_xen_arch}
%{expand:%do_xen_install %%{grubxenarch}}
%endif
%if 0%{with_xen_pvh_arch}
%{expand:%do_xen_pvh_install %%{grubxenpvharch}}
%endif
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
ln -s grub2-set-password ${RPM_BUILD_ROOT}/%{_sbindir}/grub2-setpassword
echo '.so man8/grub2-set-password.8' > ${RPM_BUILD_ROOT}/%{_datadir}/man/man8/grub2-setpassword.8
%ifnarch x86_64
rm -vf ${RPM_BUILD_ROOT}/%{_bindir}/grub2-render-label
rm -vf ${RPM_BUILD_ROOT}/%{_sbindir}/grub2-bios-setup
rm -vf ${RPM_BUILD_ROOT}/%{_sbindir}/grub2-macbless
%endif
%{expand:%%do_install_protected_file grub2-tools-minimal}

%find_lang grub

# Install kernel-install scripts
install -d -m 0755 %{buildroot}%{_prefix}/lib/kernel/install.d/
install -D -m 0755 -t %{buildroot}%{_prefix}/lib/kernel/install.d/ %{SOURCE10}
install -D -m 0755 -t %{buildroot}%{_prefix}/lib/kernel/install.d/ %{SOURCE14}
install -D -m 0755 -t %{buildroot}%{_prefix}/lib/kernel/install.d/ %{SOURCE3}
install -d -m 0755 %{buildroot}%{_sysconfdir}/kernel/install.d/
# Install systemd user service to set the boot_success flag
install -D -m 0755 -t %{buildroot}%{_userunitdir} \
	docs/grub-boot-success.{timer,service}
# Install systemd system-update unit to set boot_indeterminate for offline-upd
install -D -m 0755 -t %{buildroot}%{_unitdir} docs/grub-boot-indeterminate.service
install -d -m 0755 %{buildroot}%{_unitdir}/system-update.target.wants
install -d -m 0755 %{buildroot}%{_unitdir}/reboot.target.wants
ln -s ../grub-boot-indeterminate.service \
	%{buildroot}%{_unitdir}/system-update.target.wants
ln -s ../grub2-systemd-integration.service \
	%{buildroot}%{_unitdir}/reboot.target.wants

# Don't run debuginfo on all the grub modules and whatnot; it just
# rejects them, complains, and slows down extraction.
%global finddebugroot "%{_builddir}/%{?buildsubdir}/debug"

%global dip RPM_BUILD_ROOT=%{finddebugroot} %{__debug_install_post}
%define __debug_install_post (						\
	mkdir -p %{finddebugroot}/usr					\
	mv %{buildroot}/usr/bin %{finddebugroot}/usr/bin		\
	[ "%{_sbindir}" != "%{_bindir}" ] &&				\\\
		mv %{buildroot}/usr/sbin %{finddebugroot}/usr/sbin	\
	%{dip}								\
	install -m 0755 -d %{buildroot}/usr/lib/ %{buildroot}/usr/src/	\
	cp -al %{finddebugroot}/usr/lib/debug/				\\\
		%{buildroot}/usr/lib/debug/				\
	cp -al %{finddebugroot}/usr/src/debug/				\\\
		%{buildroot}/usr/src/debug/ )				\
	mv %{finddebugroot}/usr/bin %{buildroot}/usr/bin		\
	[ "%{_sbindir}" != "%{_bindir}" ] &&				\\\
		mv %{finddebugroot}/usr/sbin %{buildroot}/usr/sbin	\
	%{nil}

%undefine buildsubdir

%pre tools
if [ -f /boot/grub2/user.cfg ]; then
    if grep -q '^GRUB_PASSWORD=' /boot/grub2/user.cfg ; then
	sed -i 's/^GRUB_PASSWORD=/GRUB2_PASSWORD=/' /boot/grub2/user.cfg
    fi
elif [ -f %{efi_esp_dir}/user.cfg ]; then
    if grep -q '^GRUB_PASSWORD=' %{efi_esp_dir}/user.cfg ; then
	sed -i 's/^GRUB_PASSWORD=/GRUB2_PASSWORD=/' \
	    %{efi_esp_dir}/user.cfg
    fi
elif [ -f /etc/grub.d/01_users ] && \
	grep -q '^password_pbkdf2 root' /etc/grub.d/01_users ; then
    if [ -f %{efi_esp_dir}/grub.cfg ]; then
	# on EFI we don't get permissions on the file, but
	# the directory is protected.
	grep '^password_pbkdf2 root' /etc/grub.d/01_users | \
		sed 's/^password_pbkdf2 root \(.*\)$/GRUB2_PASSWORD=\1/' \
	    > %{efi_esp_dir}/user.cfg
    fi
    if [ -f /boot/grub2/grub.cfg ]; then
	install -m 0600 /dev/null /boot/grub2/user.cfg
	chmod 0600 /boot/grub2/user.cfg
	grep '^password_pbkdf2 root' /etc/grub.d/01_users | \
		sed 's/^password_pbkdf2 root \(.*\)$/GRUB2_PASSWORD=\1/' \
	    > /boot/grub2/user.cfg
    fi
fi
# ensure we exit 0
:

%post tools
%systemd_user_post grub-boot-success.timer

%preun tools
%systemd_user_preun grub-boot-success.timer

%postun tools
%systemd_user_postun_with_restart grub-boot-success.timer

%triggerpostun tools -- grub2-tools < 1:2.06-107
# grub-boot-success.timer was moved from a hard symlink under /lib/systemd
# to a preset, apply the preset when upgrading from pre-preset versions
/usr/lib/systemd/systemd-update-helper install-user-units grub-boot-success.timer

%posttrans common
set -eu

EFI_HOME=%{efi_esp_dir}
GRUB_HOME=/boot/grub2
ESP_PATH=/boot/efi

if ! mountpoint -q ${ESP_PATH}; then
    exit 0 # no ESP mounted, nothing to do
fi

if test ! -f ${GRUB_HOME}/grub.cfg; then
    # there's no config in GRUB home, create one
    grub2-mkconfig -o ${GRUB_HOME}/grub.cfg
else
    GRUB_CFG_MODE=$(stat --format="%a" ${GRUB_HOME}/grub.cfg)
    if ! test "${GRUB_CFG_MODE}" = "600"; then
        # when upgrading from <=2.06-126 to newer versions, the grub config stub
        # may have different mode than 0600, so set the latter if this is the case
        chmod 0600 ${GRUB_HOME}/grub.cfg
    fi
fi

if test -f ${EFI_HOME}/grub.cfg; then
    if (((grep -q "configfile" ${EFI_HOME}/grub.cfg && grep -q "root-dev-only" ${EFI_HOME}/grub.cfg) || grep -q "source" ${EFI_HOME}/grub.cfg) && ! grep -q "# It is automatically generated by grub2-mkconfig using templates" ${EFI_HOME}/grub.cfg); then
        exit 0 #Already unified
    fi
fi

# create a stub grub2 config in EFI
gen_grub_cfgstub $GRUB_HOME $EFI_HOME || :

if test -f ${EFI_HOME}/grubenv; then
    cp -a ${EFI_HOME}/grubenv ${EFI_HOME}/grubenv.rpmsave
    mv --force ${EFI_HOME}/grubenv ${GRUB_HOME}/grubenv
fi

%files common -f grub.lang
%dir %{_libdir}/grub/
%dir %{_datarootdir}/grub/
%attr(0700,root,root) %dir %{_sysconfdir}/grub.d
%{_prefix}/lib/kernel/install.d/20-grub.install
%{_prefix}/lib/kernel/install.d/55-set-boot-entry.install
%{_prefix}/lib/kernel/install.d/99-grub-mkconfig.install
%dir %{_datarootdir}/grub
%exclude %{_datarootdir}/grub/*
%dir /boot/grub2
%dir /boot/grub2/themes/
%dir /boot/grub2/themes/system
%attr(0700,root,root) %dir /boot/grub2
%exclude /boot/grub2/*
%dir %attr(0700,root,root) %{efi_esp_dir}
%exclude %{efi_esp_dir}/*
%ghost %config(noreplace) %verify(not size mode md5 mtime) /boot/grub2/grubenv
%license COPYING
%doc THANKS
%doc docs/grub.html
%doc docs/grub-dev.html
%doc docs/font_char_metrics.png

%files tools-minimal
%{_sbindir}/grub2-get-kernel-settings
%{_sbindir}/grub2-probe
%attr(4755, root, root) %{_sbindir}/grub2-set-bootflag
%{_sbindir}/grub2-set-default
%{_sbindir}/grub2-set*password
%{_bindir}/grub2-editenv
%{_bindir}/grub2-mkpasswd-pbkdf2
%{_bindir}/grub2-mount
%attr(0644,root,root) %config(noreplace) /etc/dnf/protected.d/grub2-tools-minimal.conf

%{_datadir}/man/man3/grub2-get-kernel-settings*
%{_datadir}/man/man8/grub2-set-default*
%{_datadir}/man/man8/grub2-set*password*
%{_datadir}/man/man1/grub2-editenv*
%{_datadir}/man/man1/grub2-mkpasswd-*

%ifarch x86_64
%files tools-efi
%{_bindir}/grub2-glue-efi
%{_bindir}/grub2-render-label
%{_sbindir}/grub2-macbless
%{_datadir}/man/man1/grub2-glue-efi*
%{_datadir}/man/man1/grub2-render-label*
%{_datadir}/man/man8/grub2-macbless*
%endif

%files tools
%attr(0644,root,root) %ghost %config(noreplace) %{_sysconfdir}/default/grub
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/grub.d/README
%{_userunitdir}/grub-boot-success.timer
%{_userunitdir}/grub-boot-success.service
%{_unitdir}/grub-boot-indeterminate.service
%{_unitdir}/system-update.target.wants
%{_unitdir}/grub2-systemd-integration.service
%{_unitdir}/reboot.target.wants
%{_unitdir}/systemd-logind.service.d
%{_infodir}/grub2*
%{_datarootdir}/grub/*
%{_sbindir}/grub2-install
%exclude %{_datarootdir}/grub/themes
%exclude %{_datarootdir}/grub/*.h
%{_datarootdir}/bash-completion/completions/grub
%{_sbindir}/grub2-mkconfig
%{_sbindir}/grub2-switch-to-blscfg
%{_sbindir}/grub2-reboot
%{_bindir}/grub2-file
%{_bindir}/grub2-menulst2cfg
%{_bindir}/grub2-mkimage
%{_bindir}/grub2-mkrelpath
%{_bindir}/grub2-script-check
%{_libexecdir}/grub2
%{_datadir}/man/man?/*

# exclude man pages from tools-extra
%exclude %{_datadir}/man/man8/grub2-sparc64-setup*
%exclude %{_datadir}/man/man1/grub2-fstest*
%exclude %{_datadir}/man/man1/grub2-glue-efi*
%exclude %{_datadir}/man/man1/grub2-kbdcomp*
%exclude %{_datadir}/man/man1/grub2-mkfont*
%exclude %{_datadir}/man/man1/grub2-mklayout*
%exclude %{_datadir}/man/man1/grub2-mknetdir*
%exclude %{_datadir}/man/man1/grub2-mkrescue*
%exclude %{_datadir}/man/man1/grub2-mkstandalone*
%exclude %{_datadir}/man/man1/grub2-syslinux2cfg*

# exclude man pages from tools-minimal
%exclude %{_datadir}/man/man3/grub2-get-kernel-settings*
%exclude %{_datadir}/man/man8/grub2-set-default*
%exclude %{_datadir}/man/man8/grub2-set*password*
%exclude %{_datadir}/man/man1/grub2-editenv*
%exclude %{_datadir}/man/man1/grub2-mkpasswd-*
%exclude %{_datadir}/man/man8/grub2-macbless*
%exclude %{_datadir}/man/man1/grub2-render-label*

%if %{with_legacy_arch}
%ifarch x86_64
%{_sbindir}/grub2-bios-setup
%else
%exclude %{_sbindir}/grub2-bios-setup
%exclude %{_datadir}/man/man8/grub2-bios-setup*
%endif
%ifarch %{sparc}
%{_sbindir}/grub2-sparc64-setup
%else
%exclude %{_sbindir}/grub2-sparc64-setup
%exclude %{_datadir}/man/man8/grub2-sparc64-setup*
%endif
%ifarch %{sparc} ppc ppc64 ppc64le
%{_sbindir}/grub2-ofpathname
%else
%exclude %{_sbindir}/grub2-ofpathname
%exclude %{_datadir}/man/man8/grub2-ofpathname*
%endif
%endif

%files tools-extra
%{_bindir}/grub2-fstest
%{_bindir}/grub2-kbdcomp
%{_bindir}/grub2-mkfont
%{_bindir}/grub2-mklayout
%{_bindir}/grub2-mknetdir
%ifnarch %{sparc}
%{_bindir}/grub2-mkrescue
%{_datadir}/man/man1/grub2-mkrescue*
%else
%exclude %{_datadir}/man/man1/grub2-mkrescue*
%endif
%{_bindir}/grub2-mkstandalone
%{_bindir}/grub2-syslinux2cfg
%{_sysconfdir}/sysconfig/grub
%{_datadir}/man/man1/grub2-fstest*
%{_datadir}/man/man1/grub2-kbdcomp*
%{_datadir}/man/man1/grub2-mkfont*
%{_datadir}/man/man1/grub2-mklayout*
%{_datadir}/man/man1/grub2-mknetdir*
%{_datadir}/man/man1/grub2-mkstandalone*
%{_datadir}/man/man1/grub2-syslinux2cfg*
%exclude %{_bindir}/grub2-glue-efi
%exclude %{_sbindir}/grub2-sparc64-setup
%exclude %{_sbindir}/grub2-ofpathname
%exclude %{_datadir}/man/man1/grub2-glue-efi*
%exclude %{_datadir}/man/man8/grub2-ofpathname*
%exclude %{_datadir}/man/man8/grub2-sparc64-setup*
%exclude %{_datarootdir}/grub/themes/starfield

%if 0%{with_efi_arch}
%{expand:%define_efi_variant_files %%{package_arch} %%{grubefiname} %%{grubeficdname} %%{grubefiarch} %%{target_cpu_name} %%{grub_target_name}}
%endif
%if 0%{with_alt_efi_arch}
%{expand:%define_efi_variant_files %%{alt_package_arch} %%{grubaltefiname} %%{grubalteficdname} %%{grubaltefiarch} %%{alt_target_cpu_name} %%{alt_grub_target_name}}
%endif
%if 0%{with_legacy_arch}
%{expand:%define_legacy_variant_files %%{legacy_package_arch} %%{grublegacyarch}}
%endif
%if 0%{with_xen_arch}
%{expand:%define_xen_variant_files %%{xen_package_arch} %%{xen_grub_target_name}}
%endif
%if 0%{with_xen_pvh_arch}
%{expand:%define_xen_pvh_variant_files %%{xen_pvh_package_arch} %%{xen_pvh_grub_target_name}}
%endif

%if 0%{with_emu_arch}
%files emu
%{_bindir}/grub2-emu*
%{_datadir}/man/man1/grub2-emu*

%files emu-modules
%{_libdir}/grub/%{emuarch}-emu/*
%exclude %{_libdir}/grub/%{emuarch}-emu/*.module
%endif

%changelog
* Wed Aug 6 2025 Jan Stancek <jstancek@redhat.com> - 2.12-40
- 55-set-boot-entry.install: fix initrd check
- Resolves: #2386118

* Tue Jul 15 2025 FeRD (Frank Dana) <ferdnyc@gmail.com> - 2.12-39
- kernel-install: Suppress warnings about missing /etc/default/grub
  file when attempting to grep its contents

* Tue Jul 29 2025 Leo Sandoval <lsandova@redhat.com> 2.12-38
- Set correctly the memory attributes for the kernel PE sections

* Tue Jul 8 2025 Nicolas Frayer <nfrayer@redhat.com> - 2.12-37
- spec: fix grub stub cfg creation script

* Thu Jun 12 2025 Nicolas Frayer <nfrayer@redhat.com> - 2.12-36
- spec: moved grub stub cfg creation into a script

* Thu Jun 5 2025 Nicolas Frayer <nfrayer@redhat.com> - 2.12-35
- osdep/linux/getroot: Detect DDF container similar to IMSM

* Wed May 28 2025 Nicolas Frayer <nfrayer@redhat.com> - 2.12-34
- Some fixes addressing memory freeing and dereferencing
- Resolves: #2368939
- Resolves: #2368945

* Fri May 16 2025 Nicolas Frayer <nfrayer@redhat.com> - 2.12-33
- sbat: bump grub sbat

* Tue May 06 2025 Leo Sandoval <lsandova@redhat.com> - 2.12-32
- Fix several cryptodisk vulnerabilities
- Resolves: CVE-2025-4382

* Tue May 6 2025 Leo Sandoval <lsandova@redhat.com> 2.12-31
- Handle special kernel parameter characters properly
- Resolves: #2362821

* Fri Apr 18 2025 Nicolas Frayer <nfrayer@redhat.com> - 2.12-30
- ppc/mkimage: SBAT support on powerpc

* Tue Mar 25 2025 Nicolas Frayer <nfrayer@redhat.com> 2.12-29
- ieee1275/ofnet: Fix grub_malloc() removed after added safe

* Tue Mar 25 2025 Nicolas Frayer <nfrayer@redhat.com> 2.12-28
- Fix the fallback mechanism when menu entries fail to boot

* Wed Mar 19 2025 Nicolas Frayer <nfrayer@redhat.com> 2.12-27
- powerpc: increase MIN RMA size for CAS negotiation

* Mon Mar 10 2025 Leo Sandoval <lsandova@redhat.com> 2.12-26
- Remove 'fs/ntfs: Implement attribute verification' patch
- Resolves: #2350327

* Tue Feb 25 2025 Nicolas Frayer <nfrayer@redhat.com> 2.12-25
- fs/ext2: Rework out-of-bounds read for inline and external extents
- Resolves: #2346804

* Tue Feb 18 2025 Leo Sandoval <lsandova@redhat.com> - 2.02-24
- Add Several CVE fixes
- Resolves: CVE-2024-45781 CVE-2024-45783 CVE-2024-45778
- Resolves: CVE-2024-45775 CVE-2024-45780 CVE-2024-45774
- Resolves: CVE-2025-0690 CVE-2025-1118 CVE-2024-45782
- Resolves: CVE-2025-0624 CVE-2024-45779 CVE-2024-45776
- Resolves: CVE-2025-0622 CVE-2025-0677
- Related: #RHEL-79703
- Related: #RHEL-79708
- Related: #RHEL-79340
- Related: #RHEL-73786
- Related: #RHEL-79701
- Related: #RHEL-73784
- Related: #RHEL-79856
- Related: #RHEL-79874
- Related: #RHEL-79706
- Related: #RHEL-79836
- Related: #RHEL-79699
- Related: #RHEL-75736
- Related: #RHEL-79712
- Related: #RHEL-79848

* Tue Feb 11 2025 Nicolas Frayer <nfrayer@redhat.com> 2.12-23
- Revert commit for bootloader update proposal for now as not all components are ready

* Tue Feb 4 2025 Marta Lewandowska <mlewando@redhat.com> - 2.12-22
- Phase 1 of the bootloader updates proposal implementation
- https://fedoraproject.org/wiki/Changes/BootLoaderUpdatesPhase1

* Tue Jan 28 2025 Nicolas Frayer <nfrayer@redhat.com> 2.12-21
- commands/bli: Fix crash in get_part_uuid()
- Resolves: #2339164

* Wed Jan 22 2025 Leo Sandoval <lsandova@redhat.com> 2.12-20
- fix pending SAST issues
- Related: #RHEL-50504

* Mon Jan 13 2025 Leo Sandoval <lsandova@redhat.com> 2.12-19
- term/nns8250-spcr: return if redirection is disabled

* Thu Jan 9 2025 Nicolas Frayer <nfrayer@redhat.com> - 2.12-18
- fs/xfs: fix large extent counters incompat feature support

* Wed Nov 27 2024 Marta Lewandowska <mlewando@redhat.com> - 2.12-17
- 99-grub-mkconfig.install: on PPC systems, remove petiboot's version checks

* Wed Nov 27 2024 Marta Lewandowska <mlewando@redhat.com> - 2.12-16
- 99-grub-mkconfig.install: Disable BLS and run grub2-mkconfig when GRUB_ENABLE_BLSCFG is disable
- Resolves: #2325960

* Thu Nov 21 2024 Andrea Bolognani <abologna@redhat.com> 2.12-15
- Add riscv64 support (thanks Jason Montleon)

* Wed Nov 20 2024 Nicolas Frayer <nfrayer@redhat.com> 2.12-14
- Build modules for Xen PV and PVH

* Fri Nov 15 2024 Nicolas Frayer <nfrayer@redhat.com> 2.12-13
- posttrans: added check for efi_home/grub.cfg
- Resolves: #2326502

* Wed Oct 23 2024 Leo Sandoval <lsandova@redhat.com> 2.12-12
- do-rebase: refactor command line parameters

* Wed Oct 23 2024 Nicolas Frayer <nfrayer@redhat.com> 2.12-11
- cmd/search: Fix a possible NULL ptr dereference

* Thu Oct 17 2024 Nicolas Frayer <nfrayer@redhat.com> 2.12-10
- acpi: Fix out of bounds access in grub_acpi_xsdt_find_table()
- Resolves: #2317048

* Thu Oct 3 2024 Nicolas Frayer <nfrayer@redhat.com> 2.12-9
- Stop grub.efi from always printing "dynamic_load_symbols %p\n" during boot
- Resolves: #2316279

* Wed Sep 25 2024 Nicolas Frayer <nfrayer@redhat.com> 2.12-8
- NX: efi/loader, add a call to grub_efi_check_nx_required()

* Tue Sep 17 2024 Nicolas Frayer <nfrayer@redhat.com> - 2.12-7
- aarch64/macros: Build gnulib with -mbranch-protection=standard

* Thu Sep 5 2024 Leo Sandoval <lsandova@redhat.com> - 2.12-6
- load EFI commands inside test expressions
- Resolves: #2305291

* Thu Aug 29 2024 Leo Sandoval <lsandova@redhat.com> - 2.12-5
- Fix netbooting regressions introduced at 2.12-1
- Resolves: #2303727

* Thu Aug 08 2024 Peter Robinson <pbrobinson@fedoraproject.org> 2.12-4
- Build using fuse3

* Tue Aug 6 2024 Leo Sandoval <lsandova@redhat.com> - 2.12-3
- Remove 'efi: Use shim's loader protocol for EFI image verification'

* Tue Aug 6 2024 Nicolas Frayer <nfrayer@redhat.com> - 2.12-2
- mkconfig: More hardening to prevent overwriting grub cfg stub

* Mon Aug 5 2024 Leo Sandoval <lsandova@redhat.com> - 2.12-1
- Rebased to release grub2-2.12

* Fri Aug 2 2024 Leo Sandoval <lsandova@redhat.com> - 2.06-127
- Set /boot/grub2/grub.cfg to 0600 mode if present

* Mon Jul 22 2024 Leo Sandoval <lsandova@redhat.com> - 2.06.126
- grub.cfg: Fix rpm grub.cfg verification issues

* Tue Jul 16 2024 Nicolas Frayer <nfrayer@redhat.com> - 2.06-125
- grub2-mkconfig: Prevent mkconfig from overwriting grub cfg stub

* Tue Jul 2 2024 Nicolas Frayer <nfrayer@redhat.com> - 2.06-124
- KVM/PowerVM: Add support for KVM on PowerVM
- Resolved: #2294883

* Tue May 28 2024 Leo Sandoval <lsandova@redhat.com> - 2.06.123
- grub-mkconfig.in: turn off executable owner bit
- Resolves: #2281464

* Thu May 23 2024 Nicolas Frayer <nfrayer@redhat.com> - 2.06-122
- cmd/search: Rework of CVE-2023-4001 fix
- Related: #2224951
- Resolved: #2263369

* Fri Apr 12 2024 Nicolas Frayer <nfrayer@redhat.com> - 2.06-121
- fs/xfs: Handle non-continuous data blocks in directory extents
- Related: #2254370

* Fri Mar 8 2024 Nicolas Frayer <nfrayer@redhat.com> - 2.06-120
- GRUB2 NTFS driver vulnerabilities
- (CVE-2023-4692)
- (CVE-2023-4693)
- Resolves: #2236613
- Resolves: #2241978
- Resolves: #2241976
- Resolves: #2238343

* Wed Feb 7 2024 Nicolas Frayer <nfrayer@redhat.com> - 2.06-119
- grub-set-bootflag: Fix for CVE-2024-1048
- (CVE-2024-1048)
- Resolves: #2256678

* Tue Jan 23 2024 Leo Sandoval <lsandova@redhat.com> - 2.06-118
- xfs: include the 'directory extent parsing patch', otherwise
XFS-formatted partitions do not boot. This change effectively
reverts 2.06-115
- Resolves: #2259266

* Wed Jan 17 2024 Nicolas Frayer <nfrayer@redhat.com> - 2.06-117
- Compiler flags: ignore incompatible types for now as it prevents
CI builds

* Wed Jan 17 2024 Nicolas Frayer <nfrayer@redhat.com> - 2.06-116
- grub-core/commands: add flag to only search root dev
- Resolves: #2223437
- Resolves: #2224951
- Resolves: #2258096
- Resolves: CVE-2023-4001

* Wed Jan 17 2024 Nicolas Frayer <nfrayer@redhat.com> - 2.06-115
- xfs: some bios systems can't boot with one of the xfs upstream patches
- Resolves: #2254370

* Sat Jan 13 2024 Hector Martin <marcan@fedoraproject.org> - 2.06-114
- Switch memdisk compression to lzop

* Thu Jan 11 2024 Daan De Meyer <daan.j.demeyer@gmail.com> - 2.06-113
-  Don't obsolete the tools package with minimal

* Tue Dec 19 2023 Nicolas Frayer <nfrayer@redhat.com> - 2.06-112
- normal: fix prefix when loading modules
- Resolves: #2209435
- Resolves: #2173015

* Tue Dec 12 2023 leo sandoval <lsandova@redhat.com> - 2.06-111
- chainloader: remove device path debug message

* Fri Dec 1 2023 Nicolas Frayer <nfrayer@redhat.com> - 2.06-110
- fs/xfs: Add several fixes/improvements to xfs fs from upstream
- Resolves: #2247926

* Wed Nov 15 2023 Nicolas Frayer <nfrayer@redhat.com> - 2.06-109
- Linker: added --no-warn-rwx-segments as build will fail after
ld.bfd default options have been changed.
https://fedoraproject.org/wiki/Changes/Linker_Error_On_Security_Issues

* Tue Nov 14 2023 Nicolas Frayer <nfrayer@redhat.com> - 2.06-108
- Remove [Install] section from aux systemd units
- Related: #2247635

* Tue Nov 14 2023 Hans de Goede <hdegoede@redhat.com> - 2.06-107
- spec: Switch back to static enablement for grub services in tools package
- spec: Add %%triggerpostun to apply grub-boot-success.timer preset
  when upgrading from older versions where this was not a preset
- Resolves: #2247635

* Mon Nov 6 2023 Nicolas Frayer <nfrayer@redhat.com> - 2.06-106
- util: grub-install on EFI if forced
- Resolves: #1917213
- Resolves: #2240994

* Fri Oct 20 2023 Nicolas Frayer <nfrayer@redhat.com> - 2.06-105
- kern/ieee1275/init: ppc64: Restrict high memory in presence
  of fadump

* Wed Oct 11 2023 Janne Grunau <j@jannau.net> - 2.06-104
- 20-grub.install: Copy device-tree directory recursively
- Resolves: #2243060

* Fri Sep 29 2023 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 1:2.06-103
- Rename installed kernel to match name used in boot entry
- Resolves: #2239008

* Fri Sep 29 2023 Nicolas Frayer <nfrayer@redhat.com> - 2.06-102
- ofdisk: Fix missing #include in ofdisk.c

* Thu Sep 28 2023 Christian Glombek <cglombek@redhat.com> - 2.06-101
- spec: Fix grub2-systemd-integration.service name

* Wed Sep 13 2023 Nicolas Frayer <nfrayer@redhat.com> - 2.06-100
- arm64: Use proper memory type for kernel allocation
- Resolves: #2149020

* Fri Sep 01 2023 Christian Glombek <cglombek@redhat.com> - 2.06-99
- spec: Use systemd presets and macros for units in tools package
- Resolves: #2230575

* Thu Aug 31 2023 Nicolas Frayer <nfrayer@redhat.com> - 2.06-98
- spec: Modified posttrans to harden grub config detection
- Resolves: #2235692

* Tue Aug 22 2023 Nicolas Frayer <nfrayer@redhat.com> - 2.06-97
- efi/http: change uint32_t to uintn_t

* Tue Aug 22 2023 Nicolas Frayer <nfrayer@redhat.com> - 2.06-96
- util: Enable default kernel for updates

* Wed Apr 12 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-95
- Add switch-root support to grub-emu

* Mon Apr 10 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-94
- Fix aa64 page fault with EFI_MEMORY_ATTRIBUTE_PROTOCOL

* Fri Mar 31 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-93
- Add legacy pxe core.0 (cmadams)

* Thu Mar 30 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-92
- Disable the tpm verifier if the TPM device is not present 

* Thu Mar 30 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-91
- ppc64le: more cas vec5 shenanigans

* Wed Mar 22 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-90
- emu: work around systemctl bad behavior

* Thu Mar 09 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-89
- emu: handle BLS /boot weirdness

* Mon Feb 20 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-88
- Update mm fixes from upstream

* Thu Feb 16 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-87
- Fix disk sector size computation

* Fri Feb 10 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-86
- Override the linker and force nonexecutable stacks

* Wed Feb 08 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-85
- ppc64le: sync cas/tpm patchset with upstream

* Mon Feb 06 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-84
- emu: support newer kexec syscall

* Mon Feb 06 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-83
- ppc64le: cas5, take 3

* Mon Feb 06 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-82
- Fix implicit function declaration warnings

* Wed Feb 01 2023 Javier Martinez Canillas <javierm@redhat.com> - 2.06-81
- 20-grub-install: Explicitly check '+debug' suffix for debug kernels
- Resolves: #2148351

* Wed Feb 01 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-80
- Bump to re-run signing

* Tue Jan 31 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-79
- Disable mdraid < 1.1 on ppc64le

* Fri Jan 27 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-78
- Fix grub2-probe issue with previous commit
- Resolves: #2165136

* Fri Jan 27 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-77
- ppc64le: update signed media fixes

* Fri Jan 13 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-76
- ppc64le: fix issues using core.elf on boot media

* Wed Jan 11 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-75
- Pull allocator improvements from upstream

* Wed Jan 11 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-74
- Apply more hardening to host binaries

* Tue Jan 10 2023 Robbie Harwood <rharwood@redhat.com> - 2.06-73
- Allow internal grub allocations over 4GB

* Wed Dec 21 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-72
- Fix prefix setting with memdisk creation for network boot

* Mon Dec 19 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-71
- Attempt to fix eln build

* Wed Dec 14 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-70
- ppc64le: fix lpar cas5
- Resolves: #2152547

* Tue Dec 06 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-69
- Fix error handling in grub_file_open()

* Mon Dec 05 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-68
- Allow for xz'd symvers file (prarit)

* Wed Nov 23 2022 Tomas Hrcka <thrcka@redhat.com> - 1:2.06-67
- install unicode.pf2 into place so lorax works

* Tue Nov 22 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-66
- Bundle unicode.pf2 with images
- Resolves: #2143725
- Resolves: #2144113

* Tue Nov 22 2022 Robbie Harwood <rharwood@redhat.com> - 1:2.06-65
- Don't obsolete the tools package with extra/efi (pbrobinson)

* Mon Nov 21 2022 Robbie Harwood <rharwood@redhat.com> - 1:2.06-64
- Forward-port ppc64le image creation (with nerfed signing)

* Tue Nov 08 2022 Robbie Harwood <rharwood@redhat.com> - 1:2.06-63
- Font fixes (CVE-2022-2601 batch)

* Tue Nov 01 2022 Robbie Harwood <rharwood@redhat.com> - 1:2.06-62
- Try dropping custom sort again
- See-also: https://github.com/rpm-software-management/rpm/pull/2249

* Fri Oct 28 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-61
- TDX measurements to RTMR

* Wed Oct 12 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-60
- x86-efi: Fix an incorrect array size in kernel allocation

* Tue Oct 04 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-59
- Flush instruction cache before starting aa64 kernel

* Fri Sep 09 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-58
- Bump spec for grub.macros gettext changes from Jens

* Thu Sep 08 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-57
- aa64: support pe/coff decompressor

* Wed Sep 07 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-56
- Revert patches to claim more memory for the arena

* Thu Aug 25 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-55
- Fix root definition for blscfg in emu

* Thu Aug 25 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-54
- gettext to gettext-runtime migration from Jens

* Thu Aug 25 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-53
- ieee1275: implement vec5 for cas negotiation

* Wed Aug 17 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-52
- Handle ostree's non-writable /etc/kernel

* Wed Aug 17 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-51
- Give up on rhgb quiet

* Wed Aug 17 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-50
- Fix duplicated args and cope with /etc/default/grub modification

* Mon Aug 15 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-49
- Skip rpm mtime verification on likely-vfat filesystems

* Mon Aug 15 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-48
- Use --with-rpm-version
- Resolves: #2118390

* Mon Aug 08 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-47
- Try reserving less RAM to fix windows booting
- Related: #2115202

* Tue Aug 02 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-46
- Populate /etc/kernel/cmdline during mkconfig

* Tue Aug 02 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-45
- Rest of allocator fixes

* Mon Aug 01 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-44
- Some allocator fixes for kernel

* Tue Jul 19 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-43
- Handle FAT mtime of 0
- Resolves: #2096192

* Mon May 16 2022 Robbie Harwood <rharwood@redhat.com> - 1:2.06-42
- CVE fixes for 2022-05-24
- Resolves: CVE-2022-28736 CVE-2022-28735 CVE-2022-28734 CVE-2022-28733
- Resolves: CVE-2021-3697 CVE-2021-3696 CVE-2021-3695

* Mon May 16 2022 Robbie Harwood <rharwood@redhat.com> - 1:2.06-41
- ppc64le: make ofdisk retries optional

* Thu May 05 2022 Robbie Harwood <rharwood@redhat.com> - 1:2.06-40
- Fix missing declaration of strchrnul in rpm-sort

* Wed May 04 2022 Robbie Harwood <rharwood@redhat.com> - 1:2.06-39
- ppc64le: CAS improvements, prefix detection, and vTPM support

* Tue Apr 19 2022 Dominik Mierzejewski <dominik@greysector.net> - 1:2.06-38
- fix "grub2-mkrescue: error: `mformat` invocation failed"

* Mon Apr 18 2022 Robbie Harwood <rharwood@redhat.com> - 1:2.06-37
- Attempt to fix version display

* Mon Apr 18 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-36
- Fix permission change report from rpm verification on grub.cfg

* Wed Apr 13 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-35
- Enable "read" module
- Resolves: #2071644

* Tue Apr 12 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-34
- Bump for requirements updates; no code changes

* Thu Mar 31 2022 Robbie Harwood <rharwood@redhat.com> - 1:2.06-33
- Drop i32 build for real this time

* Thu Mar 31 2022 Robbie Harwood <rharwood@redhat.com> - 1:2.06-32
- Switch to upstream man pages

* Wed Mar 30 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-31
- Revert previous change (grub2-pc-modules is built on i32)

* Tue Mar 29 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-30
- Drop i32 support

* Wed Mar 23 2022 Adam Williamson <awilliam@redhat.com> - 2.06-29
- Fix a syntax error in the ostree BLS fix attempt

* Wed Mar 23 2022 Peter Robinson <pbrobinson@fedoraproject.org> 2.06-28
- Rebuild for secure-boot signing

* Tue Mar 22 2022 Adam Williamson <awilliam@redhat.com> - 2.06-27
- Revert "Use my sort patch instead", it broke Rawhide
- Tweak BLS skipping on ostree to work in chroots (I hope)
- Resolves: #2066969
- Resolves: #2059776

* Tue Mar 22 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-26
- Fix rebase on x509 embedding patch

* Mon Mar 21 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-25
- Use my sort patch instead

* Mon Mar 21 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-24
- Fix missing format specifier in appended signature commit

* Fri Mar 18 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-23
- Don't verify kernels twice

* Thu Mar 10 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-22
- Skip updating BLS on ostree installations
- Resolves: #2059776

* Wed Mar 09 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-21
- Fix initialization in efidisk patch

* Mon Feb 28 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-20
- Disable the .package_note awfulness
- Resolves: #2058712
- Resolves: #2058527

* Fri Feb 25 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-19
- Fix stripping of annobin -spec

* Thu Feb 24 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-18
- Add efidisk/connectefi patches

* Thu Feb 24 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-17
- Fix appended signature support commit (thanks: pjones)

* Thu Feb 24 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-16
- Suffer through updating gnulib

* Thu Jan 20 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-15
- Skip machine ID check when updating BLS

* Tue Jan 18 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-14
- Add location of DejaVu Sans font

* Mon Jan 17 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-13
- Update patches; minor changes at most, if correct

* Thu Jan 06 2022 Robbie Harwood <rharwood@redhat.com> - 2.06-12
- btrfs: use full bootloader area

* Fri Dec 10 2021 Robbie Harwood <rharwood@redhat.com> - 2.06-11
- Bump to rerun signing (no code changes)

* Thu Dec 09 2021 Robbie Harwood <rharwood@redhat.com> - 2.06-10
- restore umask for grub.cfg (CVE-2021-3981)

* Thu Nov 04 2021 Robbie Harwood <rharwood@redhat.com> - 2.06-9
- Drop UI patches and update provenance information

* Thu Oct 07 2021 Peter Jones <pjones@redhat.com> - 2.06-8
- Fix "grub2-mkimage --appended-signature-size" parsing.

* Wed Sep 29 2021 Robbie Harwood <rharwood@redhat.com> - 2.06-7
- Rebuild; no code changes

* Wed Sep 29 2021 Robbie Harwood <rharwood@redhat.com> - 2.06-6
- fs/xfs: Fix unreadable filesystem with v4 superblock
- Arm: check for the PE magic for the compiled arch
- Resolves: rhbz#2008819

* Mon Aug 30 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.06-5
- A few fixes for ppc64le LPAR Secure Boot support

* Tue Aug 24 2021 Peter Jones <pjones@redhat.com> - 2.06-4
- Fix aarch64 kernel alignment.
- Fix annobin regexp on ppc64le

* Tue Jul 06 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.06-3
- Add luks2 to GRUB_MODULES
- 20-grub-install: Create a symvers.gz symbolic link
- 20-grub-install: Always use fedora as the boot entry --class
  Resolves: rhbz#1957014
- grub.macros: Install font in /boot/grub2 instead of the ESP
  Resolves: rhbz#1739762
- grub.macros: Use consistent file mode for legacy and EFI
  Resolves: rhbz#1965794
- Drop grub2 prelink configuration
  Resolves: rhbz#1659675
- Remove triggers needed to upgrade from legacy GRUB
- Don't harcode grub2 in the spec file
- Update to unifont-13.0.06
  Resolves: rhbz#1939125
- 20-grub-install: Use relative paths for btrfs in BLS snippets
  Resolves: rhbz#1906191
- Don't update the cmdline when generating legacy menuentry commands
- Suppress gettext error message
  Resolves: rhbz#1592124
- grub-boot-success.timer: Only run if not in a container
  Resolves: rhbz#1914571
- grub-set-password: Always use /boot/grub2/user.cfg as password default
  Resolves: rhbz#1955294
- Remove outdated URL for BLS document
  Resolves: rhbz#1926453
- templates: Check for EFI at runtime instead of config generation time
  Resolves: rhbz#1823864
- efi: Print an error if boot to firmware setup is not supported
  Resolves: rhbz#1823864

* Tue Jun 15 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.06-2
- Only try to generate a config if the ESP is mounted

* Mon Jun 14 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.06-1
- Update to 2.06 final release and ton of fixes

* Mon May 03 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.06~rc1-7
- Add XFS needsrepair support

* Fri Apr 23 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.06~rc1-6
- Find and claim more memory for ieee1275 (dja)

* Wed Apr 14 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.06~rc1-5
- Add XFS bigtime support (cmaiolino)

* Mon Apr 12 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.06~rc1-4
- Add again 20_linux_xen script fix that got dropped by mistake
  Resolves: rhbz#1858364

* Thu Mar 25 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.06~rc1-3
- Prevent %%posttrans scriptlet to fail if grubenv isn't present in the ESP

* Wed Mar 24 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.06~rc1-2
- Fix a couple of merge mistakes made when rebasing to 2.06~rc1
  Resolves: rhbz#1940524

* Fri Mar 12 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.06~rc1-1
- Update to 2.06~rc1 to fix a bunch of CVEs
  Resolves: CVE-2020-14372
  Resolves: CVE-2020-25632
  Resolves: CVE-2020-25647
  Resolves: CVE-2020-27749
  Resolves: CVE-2020-27779
  Resolves: CVE-2021-20225
  Resolves: CVE-2021-20233

* Thu Mar 11 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.04-39
- Fix config file generation failing due invalid petitboot version value
  Resolves: rhbz#1921479

* Fri Mar 05 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.04-38
- Fix keyboards that report IBM PC AT scan codes (rmetrich)

* Thu Feb 25 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.04-37
- Don't attempt to unify if there is no grub.cfg on EFI (gicmo)
  Resolves: rhbz#1933085

* Mon Feb 22 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.04-36
- Switch EFI users to new unified config
  Resolves: rhbz#1918817
- Fix ESC key no longer showing the menu
  Resolves: rhbz#1928595

* Mon Feb 08 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.04-35
- Remove -fcf-protection compiler flag to allow i386 builds (law)
  Related: rhbz#1915452
- Unify GRUB configuration file location across all platforms
  Related: rhbz#1918817
- Add 'at_keyboard_fallback_set' var to force the set manually (rmetrich)
- Add appended signatures support for ppc64le LPAR Secure Boot (daxtens)

* Tue Jan 12 2021 Javier Martinez Canillas <javierm@redhat.com> - 2.04-34
- at_keyboard: use set 1 when keyboard is in Translate mode (rmetrich)

* Thu Dec 31 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-33
- Add DNF protected.d fragments for GRUB packages
  Resolves: rhbz#1874541
 - Include keylayouts and at_keyboard modules in EFI builds
 - Add GRUB enhanced debugging features
 - ieee1275: Avoiding many unecessary open/close
 - ieee1275: device mapper and fibre channel discovery support
 - Fix tps-rpmtest failing due /boot/grub2/grubenv attributes mismatch

* Thu Nov 12 2020 Peter Hazenberg <fedoraproject@haas-en-berg.nl> - 2.04-32
- Fixed some typos in grub-install.8 man page

* Mon Aug 31 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-31
- Roll over TFTP block counter to prevent timeouts with data packets
  Resolves: rhbz#1869335

* Fri Aug 21 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-30
- Set TFTP blocksize to 1428 instead of 2048 to avoid IP fragmentation
  Resolves: rhbz#1869335

* Fri Aug 21 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-29
- Fix TFTP timeouts when trying to fetch files larger than 65535 KiB
  Resolves: rhbz#1869335

* Wed Aug 12 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-28
- Add support for "systemctl reboot --boot-loader-menu=xx" (hdegoede)
  Related: rhbz#1857389

* Mon Aug 10 2020 Peter Jones <pjones@redhat.com> - 2.04-27
- Attempt to enable dual-signing in f33
- "Minor" bug fixes.  For f33:
  Resolves: CVE-2020-10713
  Resolves: CVE-2020-14308
  Resolves: CVE-2020-14309
  Resolves: CVE-2020-14310
  Resolves: CVE-2020-14311
  Resolves: CVE-2020-15705
  Resolves: CVE-2020-15706
  Resolves: CVE-2020-15707

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 2.04-26
- Disable LTO

* Thu Jun 18 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-25
- Only mark GRUB as BLS supported in OSTree systems with a boot partition

* Mon Jun 08 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-24
- http: Prepend prefix when the HTTP path is relative as done in efi/http
- Fix build with rpm-4.16 (thierry.vignaud)

* Fri Jun 05 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-23
- Install GRUB as \EFI\BOOT\BOOTARM.EFI in armv7hl

* Tue May 26 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-22
- Fix an out of memory error when loading large initrd images
  Resolves: rhbz#1838633

* Wed May 20 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-21
- Don't update BLS files that aren't managed by GRUB scripts
  Resolves: rhbz#1837783

* Mon May 18 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-20
- Only enable the tpm module for EFI platforms

* Sat May 16 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-19
- Enable tpm module and make system to boot even if TPM measurements fail
  Resolves: rhbz#1836433

* Thu May 14 2020 Adam Williamson <awilliam@redhat.com> - 2.04-18
- 10_linux.in: restore existence check in `get_sorted_bls`
  Resolves: rhbz#1836020

* Wed May 13 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-17
- Store cmdline in BLS snippets instead of using a grubenv variable

* Tue May 12 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-16
- Fix a segfault in grub2-editenv when attempting to shrink a variable

* Thu Apr 30 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-15
- blscfg: Lookup default_kernelopts variable as fallback for options
  Related: rhbz#1765297
- 10_linux.in: fix early exit due error when reading petitboot version
  Resolves: rhbz#1827397

* Thu Apr 23 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-14
- efi: Set image base address before jumping to the PE/COFF entry point
  Resolves: rhbz#1825411

* Thu Apr 16 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-13
- Make the grub-switch-to-blscfg and 10_linux scripts more robust

* Thu Apr 02 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-12
- Merge 10_linux_bls logic into 10_linux and avoid issues if blsdir is set

* Thu Mar 26 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-11
- grub-switch-to-blscfg: Update grub2 binary in ESP for OSTree systems
  Related: rhbz#1751272

* Tue Mar 17 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-10
- Fix for entries having an empty initrd command and HTTP boot issues
  Resolves: rhbz#1806022

* Thu Jan 16 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-9
- Add riscv64 support to grub.macros and RISC-V build fixes (davidlt)
- blscfg: Always use the root variable to search for BLS snippets
- bootstrap.conf: Force autogen.sh to use python3

* Mon Jan 13 2020 Javier Martinez Canillas <javierm@redhat.com> - 2.04-8
- Make the blscfg module honour the GRUB_SAVEDEFAULT option (fritz)
  Resolves: rhbz#1704926

* Mon Jan 06 2020 Peter Jones <pjones@redhat.com> - 2.04-7
- Add zstd to the EFI module list.
  Related: rhbz#1418336

* Thu Dec 05 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.04-6
- Various grub2 cleanups (pbrobinson)
- Another fix for blscfg variable expansion support
- blscfg: Add support for sorting the plus ('+') higher than base version
  Resolves: rhbz#1767395

* Wed Nov 27 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.04-5
- blscfg: add a space char when appending fields for variable expansion
- grub.d: Fix boot_indeterminate getting set on boot_success=0 boot

* Tue Nov 26 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.04-4
- grub-set-bootflag: Write new env to tmpfile and then rename (hdegoede)
  Resolves: CVE-2019-14865
  Resolves: rhbz#1776580

* Thu Oct 17 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.04-3
- 20-grub-install: Don't add an id field to generated BLS snippets
- 99-grub-mkconfig: Disable BLS usage for Xen machines
  Resolves: rhbz#1703700
- Don't add a class option to menu entries generated for ppc64le
  Resolves: rhbz#1758225
- 10_linux.in: Also use GRUB_CMDLINE_LINUX_DEFAULT to set kernelopts
- blscfg: Don't hardcode an env var as fallback for the BLS options field
  Resolves: rhbz#1710483

* Wed Sep 18 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.04-2
- A couple of RISC-V fixes
- Remove grub2-tools %%posttrans scriptlet that migrates to a BLS config
- Add blscfg device tree support
  Resolves: rhbz#1751307

* Thu Aug 15 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.04-1
- Update to 2.04
  Resolves: rhbz#1727279

* Wed Aug 07 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-97
- Include regexp module in EFI builds

* Thu Aug 01 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-96
- Manual build for the Fedora 31 mass rebuild to succeed

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-94
- 20-grub-install: Restore default SELinux security contexts for BLS files
  Resolves: rhbz#1726020

* Wed Jul 17 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-93
- Add btrfs snapshot submenu when BLS configuration is used
- Move grub2-probe to the grub2-tools-minimal subpackage
  Resolves: rhbz#1715994

* Tue Jul 16 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-92
- Cleanup our patchset to reduce the number of patches

* Sat Jul 13 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-91
- Includes security modules in Grub2 EFI builds (benjamin.doron)
  Resolves: rhbz#1722938
- Enable again multiboot and multiboot2 modules on EFI builds
  Resolves: rhbz#1703872

* Fri Jul 05 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-90
- Fix failure to request grub.cfg over HTTP
- Some ARM fixes (pbrobinson)
- Preserve multi-device workflows (Yclept Nemo)

* Thu Jun 27 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-89
- Fix --bls-directory option comment in grub2-switch-to-blscfg man page
  Resolves: rhbz#1714835
- 10_linux_bls: use '=' to separate --id argument due a Petitboot bug
- grub-set-bootflag: Print an error if failing to read from grubenv
  Resolves: rhbz#1702354
- 10_linux: generate BLS section even if no kernels are found in /boot
- 10_linux: don't search for OSTree kernels

* Tue Jun 18 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 2.02-88
- Use '-g' instead of '-g3' when compiling grub2.
  Resolves: rhbz#1708780

* Tue Jun 11 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-87
- Rebuild for RPM 4.15

* Mon Jun 10 22:13:19 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org>
- Rebuild for RPM 4.15

* Mon Jun 10 15:42:01 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org>
- Rebuild for RPM 4.15

* Mon May 20 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-84
- Don't try to switch to a BLS config if GRUB_ENABLE_BLSCFG is already set

* Wed May 15 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-83
- Fix error messages wrongly being printed when executing blscfg command
  Resolves: rhbz#1699761
- Remove bogus load_env after blscfg command in 10_linux

* Tue May 07 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-82
- Make blscfg module compatible at least up to the Fedora 19 GRUB core
  Related: rhbz#1652806

* Fri May 03 2019 Neal Gompa <ngompa13@gmail.com> - 2.02-81
- Add grub2-mount to grub2-tools-minimal subpackage
  Resolves: rhbz#1471267

* Fri May 03 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-80
- Add grub2-emu subpackage

* Fri May 03 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 2.02-79
- Fix description of grub2-pc
  Resolves: rhbz#1484298

* Thu Apr 18 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-78
- Add 10_reset_boot_success to Makefile
  Related: rhbz#17010

* Thu Apr 18 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-77
- Never remove boot loader configuration for other boot loaders from the ESP.
  This would render machines with sd-boot unbootable (zbyszek)
- Execute grub2-switch-to-blscfg script in %%posttrans instead of %%post
- grub.d: Split out boot success reset from menu auto hide script (lorbus)
- HTTP boot: strncmp returns 0 on equal (stephen)
- Some grub2-emu fixes and make it to not print unnecessary messages
- Don't assume that boot commands will only return on fail

* Thu Mar 28 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-76
- 10_linux_bls: don't add --users option to generated menu entries
  Resolves: rhbz#1693515

* Tue Mar 26 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-75
- A set of EFI fixes to support arm64 QCom UEFI firmwares (pbrobinson)

* Fri Mar 22 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-74
- Fix some BLS snippets not being displayed in the GRUB menu
  Resolves: rhbz#1691232
- Fix possible undefined behaviour due wrong grub_efi_status_t type (pjones)

* Wed Mar 20 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-73
- Only set blsdir if /boot/loader/entries is in a btrfs or zfs partition
  Related: rhbz#1688453

* Mon Mar 11 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-72
- Avoid grub2-efi package to overwrite existing /boot/grub2/grubenv file
  Resolves: rhbz#1687323
- Switch to BLS in tools package %%post scriptlet
  Resolves: rhbz#1652806

* Wed Feb 27 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-71
- 20-grub-install: Replace, rather than overwrite, the existing kernel (pjones)
  Resolves: rhbz#1642402
- 99-grub-mkconfig: Don't update grubenv generating entries on ppc64le
  Related: rhbz#1637875
- blscfg: fallback to default_kernelopts if BLS option field isn't set
  Related: rhbz#1625124
- grub-switch-to-blscfg: copy increment.mod for legacy BIOS and ppc64
  Resolves: rhbz#1652806

* Fri Feb 15 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-70
- Check if blsdir exists before attempting to get it's real path
  Resolves: rhbz#1677415

* Wed Feb 13 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-69
- Don't make grub_strtoull() print an error if no conversion is performed
  Resolves: rhbz#1674512
- Set blsdir if the BLS directory path isn't one of the looked up by default
  Resolves: rhbz#1657240

* Mon Feb 04 2019 Javier Martinez Canillas <javierm@redhat.com> - 2.02-68
- Don't build the grub2-efi-ia32-* packages on i686 (pjones)
- Add efi-export-env and efi-load-env commands (pjones)
- Make it possible to subtract conditions from debug= (pjones)
- Try to set -fPIE and friends on libgnu.a (pjones)
- Add more options to blscfg command to make it more flexible
- Add support for prepend early initrds to the BLS entries
- Fix grub.cfg-XXX look up when booting over TFTP

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 17 2018 Javier Martinez Canillas <javierm@redhat.com> - 2.02-66
- Don't exclude /etc/grub.d/01_fallback_counting anymore

* Tue Dec 11 2018 Javier Martinez Canillas <javierm@redhat.com> - 2.02-65
- BLS files should only be copied by grub-switch-to-blscfg if BLS isn't set
  Related: rhbz#1638117
- Fix get_entry_number() wrongly dereferencing the tail pointer
  Resolves: rhbz#1654936
- Make grub2-mkconfig to honour GRUB_CMDLINE_LINUX in /etc/default/grub
  Resolves: rhbz#1637875

* Fri Nov 30 2018 Javier Martinez Canillas <javierm@redhat.com> - 2.02-64
- Add comments and revert logic changes in 01_fallback_counting
- Remove quotes when reading ID value from /etc/os-release
  Related: rhbz#1650706
- blscfg: expand grub_users before passing to grub_normal_add_menu_entry()
  Resolves: rhbz#1650706
- Drop buggy downstream patch "efinet: retransmit if our device is busy"
  Resolves: rhbz#1649048
- Make the menu entry users option argument to be optional
  Related: rhbz#1652434
- 10_linux_bls: add missing menu entries options
  Resolves: rhbz#1652434
- Drop "Be more aggro about actually using the *configured* network device."
  Resolves: rhbz#1654388
- Fix menu entry selection based on title
  Resolves: rhbz#1654936

* Wed Nov 21 2018 Javier Martinez Canillas <javierm@redhat.com> - 2.02-63
- add 10_linux_bls grub.d snippet to generate menu entries from BLS files
  Resolves: rhbz#1636013
- Only set kernelopts in grubenv if it wasn't set before
  Resolves: rhbz#1636466
- kernel-install: Remove existing initramfs if it's older than the kernel (pjones)
  Resolves: rhbz#1638405
- Update the saved entry correctly after a kernel install (pjones)
  Resolves: rhbz#1638117
- blscfg: sort everything with rpm *package* comparison (pjones)
  Related: rhbz#1638103
- blscfg: Make 10_linux_bls sort the same way as well
  Related: rhbz#1638103
- don't set saved_entry on grub2-mkconfig
  Resolves: rhbz#1636466
- Fix menu entry selection based on ID and title (pjones)
  Resolves: rhbz#1640979
- Don't unconditionally set default entry when installing debug kernels
  Resolves: rhbz#1636346
- Remove installkernel-bls script
  Related: rhbz#1647721

* Thu Oct 04 2018 Peter Jones <pjones@redhat.com> - 2.02-62
- Exclude /etc/grub.d/01_fallback_counting until we work through some design
  questions.
  Resolves: rhbz#1614637

* Wed Oct 03 2018 Peter Jones <pjones@redhat.com> - 2.02-61
- Fix the fallback counting script even harder. Apparently, this wasn't
  tested well enough.
  Resolves: rhbz#1614637

* Tue Oct 02 2018 Peter Jones <pjones@redhat.com> - 2.02-60
- Fix grub.cfg boot counting snippet generation (lorbus)
  Resolves: rhbz#1614637
- Fix spurrious allocation error reporting on EFI boot
  Resolves: rhbz#1635319
- Stop doing TPM on BIOS *again*.  It just doesn't work.
  Related: rhbz#1579835
- Make blscfg module loadable on older grub2 i386-pc and powerpc-ieee1275
  builds
- Fix execstack cropping up in grub2-tools
- Ban stack trampolines with compiler flags.

* Tue Sep 25 2018 Hans de Goede <hdegoede@redhat.com> - 2.02-59
- Stop using pkexec for grub2-set-bootflag, it does not work under gdm
  instead make it suid root (it was written with this in mind)

* Tue Sep 25 2018 Peter Jones <pjones@redhat.com>
- Use bounce buffers for addresses above 4GB
- Allow initramfs, cmdline, and params >4GB, but not kernel

* Wed Sep 12 2018 Peter Jones <pjones@redhat.com> - 2.02-58
- Add 2 conditions to boot-success timer and service:
  - Don't run it for system users
  Resolves: rhbz#1592201
  - Don't run it when pkexec isn't available
  Resolves: rhbz#1619445
- Use -Wsign-compare -Wconversion -Wextra in the build.

* Tue Sep 11 2018 Peter Jones <pjones@redhat.com> - 2.02-57
- Limit grub_malloc() on x86_64 to < 31bit addresses, as some devices seem to
  have a colossally broken storage controller (or UEFI driver) that can't do
  DMA to higher memory addresses, but fails silently.
  Resolves: rhbz#1626844 (possibly really resolving it this time.)
- Also integrate Hans's attempt to fix the related error from -54, but do it
  the other way around: try the low addresses first and *then* the high one if
  the allocation fails.  This way we'll get low regions by default, and if
  kernel/initramfs don't fit anywhere, it'll try the higher addresses.
  Related: rhbz#1624532
- Coalesce all the intermediate debugging junk from -54/-55/-56.

* Tue Sep 11 2018 Peter Jones <pjones@redhat.com> - 2.02-56
- Don't mangle fw_path even harder.
  Resolves: rhbz#1626844
- Fix reboot being missing on some platforms, and make it alias to
  "reset" as well.
- More dprintf().

* Mon Sep 10 2018 Peter Jones <pjones@redhat.com> - 2.02-55
- Fix UEFI memory problem in a different way.
  Related: rhbz#1624532
- Don't mangle fw_path with a / unless we're on http
  Resolves: rhbz#1626844

* Fri Sep 07 2018 Kevin Fenzi <kevin@scrye.com> - 2.02-54
- Add patch from https://github.com/rhboot/grub2/pull/30 to fix uefi booting
  Resolves: rhbz#1624532

* Thu Aug 30 2018 Peter Jones <pjones@redhat.com> - 2.02-53
- Fix AArch64 machines with no RAM latched lower than 1GB
  Resolves: rhbz#1615969
- Set http_path and http_url when HTTP booting
- Hopefully slightly better error reporting in some cases
- Better allocation of kernel+initramfs on x86_64 and aarch64
  Resolves: rhbz#1572126

* Mon Aug 20 2018 Peter Jones <pjones@redhat.com> - 2.02-52
- Update conflicts on grubby not to care about %%{?dist}

* Sun Aug 19 2018 Peter Jones <pjones@redhat.com> - 2.02-51
- Make it quieter.

* Thu Aug 16 2018 Peter Jones <pjones@redhat.com> - 2.02-50
- Fix arm32 off-by-one error on reading the PE header.

* Tue Aug 14 2018 Peter Jones <pjones@redhat.com> - 2.02-50
- Fix typo in /etc/grub.d/01_fallback_counting
  Resolves: rhbz#1614637

* Fri Aug 10 2018 Javier Martinez Canillas <javierm@redhat.com> - 2.02-50
- Add an installkernel script for BLS configurations

* Tue Aug 07 2018 Peter Jones <pjones@redhat.com> - 2.02-49
- Temporarily make -cdboot perms 0700 again.

* Fri Aug 03 2018 Peter Jones <pjones@redhat.com> - 2.02-48
- Kill .note.gnu.property with fire.
  Resolves: rhbz#1612339

* Thu Aug 02 2018 Peter Jones <pjones@redhat.com> - 2.02-47
- Enable armv7 EFI builds.  This was way harder than I expected.

* Tue Jul 17 2018 Peter Jones <pjones@redhat.com> - 2.02-46
- Fix some minor BLS issues
- Rework the FDT module linking to make aarch64 build and boot right

* Mon Jul 16 2018 pjones <pjones@redhat.com> - 2.02-45
- Rework SB patches and 10_linux.in changes even harder.
  Resolves: rhbz#1601578

* Mon Jul 16 2018 Hans de Goede <hdegoede@redhat.com> - 2.02-44
- Make the user session automatically set the boot_success grubenv flag
- Make offline-updates increment the boot_indeterminate grubenv variable

* Mon Jul 16 2018 pjones <pjones@redhat.com> - 2.02-43
- Rework SB patches and 10_linux.in changes

* Fri Jul 13 2018 Peter Jones <pjones@redhat.com> - 2.02-42
- Revert broken moduledir fix *again*.

* Thu Jul 12 2018 Peter Jones <pjones@redhat.com> - 2.02-41
- Fix our linuxefi/linux command reunion.

* Wed Jul 11 2018 Peter Jones <pjones@redhat.com> - 2.02-40
- Port several fixes from the F28 tree and a WIP tree.

* Mon Jul 09 2018 pjones <pjones@redhat.com> - 2.02-39
- Fix my fix of grub2-switch-to-blscfg (javierm and pjones)

* Mon Jul 02 2018 Javier Martinez Canillas <javierm@redhat.com> - 2.02-38
- Use BLS fragment filename as menu entry id and for sort criterion

* Tue Jun 26 2018 Javier Martinez Canillas <javierm@redhat.com>
- Cleanups and fixes for grub2-switch-to-blscfg (pjones)
- Use /boot/loader/entries as BLS dir also on EFI (javierm)

* Tue Jun 19 2018 Peter Jones <pjones@redhat.com> - 2.02-37
- Fix some TPM errors on 32-bit (hdegoede)
- More fixups to avoid compiler changes (pjones)
- Put lsmmap into the EFI builds (pjones)
  Related: rhbz#1572126
- Make 20-grub.install to exit if there is no machine ID set (javierm)
  Resolves: rhbz#1576573
- More fixes for BLS (javierm)
  Resolves: rhbz#1588184

* Wed May 16 2018 Peter Jones <pjones@redhat.com> - 2.02-37.fc29
- Fixups to work with gcc 8
- Experimental https boot support on UEFI
- XFS fixes for sparse inode support
  Resolves: rhbz#1575797

* Thu May 10 2018 Javier Martinez Canillas <javierm@redhat.com> - 2.02-36
- Use version field to sort BLS entries if id field isn't defined
- Add version field to BLS fragments generated by 20-grub.install

* Tue Apr 24 2018 Peter Jones <pjones@redhat.com> - 2.02-35
- A couple of fixes needed by Fedora Atomic - javierm

* Mon Apr 23 2018 Peter Jones <pjones@redhat.com> - 2.02-34
- Put the os-prober dep back in - we need to change test plans and criteria
  before it can go.
  Resolves: rhbz#1569411

* Wed Apr 11 2018 Peter Jones <pjones@redhat.com> - 2.02-33
- Work around some issues with older automake found in CentOS.
- Make multiple initramfs images work in BLS.

* Wed Apr 11 2018 Javier Martinez Canillas <javierm@redhat.com> - 2.02-32
- Make 20-grub.install to generate debug BLS when MAKEDEBUG is set.

* Fri Apr 06 2018 Peter Jones <pjones@redhat.com> - 2.02-31
- Pull in some TPM fixes I missed.

* Fri Apr 06 2018 Peter Jones <pjones@redhat.com> - 2.02-30
- Enable TPM measurements
- Set the default boot entry to the first entry when we're using BLS.

* Tue Apr 03 2018 Peter Jones <pjones@redhat.com> - 2.02-29
- Fix for BLS paths on BIOS / non-UEFI (javierm)

* Fri Mar 16 2018 Peter Jones <pjones@redhat.com> - 2.02-28
- Install kernel-install scripts. (javierm)
- Add grub2-switch-to-blscfg

* Tue Mar 06 2018 Peter Jones <pjones@redhat.com> - 2.02-27
- Build the blscfg module in on EFI builds.

* Wed Feb 28 2018 Peter Jones <pjones@redhat.com> - 2.02-26
- Try to fix things for new compiler madness.
  I really don't know why gcc decided __attribute__((packed)) on a "typedef
  struct" should imply __attribute__((align (1))) and that it should have a
  warning that it does so.  The obvious behavior would be to keep the alignment
  of the first element unless it's used in another object or type that /also/
  hask the packed attribute.  Why should it change the default alignment at
  all?
- Merge in the BLS patches Javier and I wrote.
- Attempt to fix pmtimer initialization failures to not be super duper slow.

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org>
- Escape macros in %%changelog

* Tue Jan 23 2018 Peter Jones <pjones@redhat.com> - 2.02-24
- Fix a merge error from 2.02-21 that affected kernel loading on Aarch64.
  Related: rhbz#1519311
  Related: rhbz#1506704
  Related: rhbz#1502312

* Fri Jan 19 2018 Peter Jones <pjones@redhat.com> - 2.02-23
- Only nerf annobin, not -fstack-crash-protection.
- Fix a conflict on /boot/efi directory permissions between -cdboot and the
  normal bootloader.

* Thu Jan 18 2018 Peter Jones <pjones@redhat.com> - 2.02-22
- Nerf some gcc 7.2.1-6 'features' that cause grub to crash on start.

* Thu Jan 18 2018 Peter Jones <pjones@redhat.com> - 2.02-21
- Fix grub2-efi-modules provides/obsoletes generation
  Resolves: rhbz#1506704
- *Also* build grub-efi-ia32{,-*,!-modules} packages for i686 builds
  Resolves: rhbz#1502312
- Make everything under /boot/efi be mode 0700, since that's what FAT will
  show anyway.

* Wed Jan 17 2018 Peter Jones <pjones@redhat.com> - 2.02-20
- Update to newer upstream for F28
- Pull in patches for Apollo Lake hardware
  Resolves: rhbz#1519311

* Tue Oct 24 2017 Peter Jones <pjones@redhat.com> - 2.02-19
- Handle xen module loading (somewhat) better
  Resolves: rhbz#1486002

* Wed Sep 20 2017 Peter Jones <pjones@redhat.com> - 2.02-18
- Make grub2-efi-aa64 provide grub2
  Resolves: rhbz#1491045

* Mon Sep 11 2017 Dennis Gilmore <dennis@ausil.us> - 2.02-17
- bump for Obsoletes again

* Wed Sep 06 2017 Peter Jones <pjones@redhat.com> - 2.02-16
- Fix Obsoletes on grub2-pc

* Wed Aug 30 2017 Petr Šabata <contyk@redhat.com> - 2.02-15
- Limit the pattern matching in do_alt_efi_install to files to
  unbreak module builds

* Fri Aug 25 2017 Peter Jones <pjones@redhat.com> - 2.02-14
- Revert the /usr/lib/.build-id/ change:
  https://fedoraproject.org/wiki/Changes/ParallelInstallableDebuginfo
  says (without any particularly convincing reasoning):
    The main build-id file should not be in the debuginfo file, but in the
    main package (this was always a problem since the package and debuginfo
    package installed might not match). If we want to make usr/lib/debug/ a
    network resource then we will need to move the symlink to another
    location (maybe /usr/lib/.build-id).
  So do it that way.  Of course it doesn't matter, because exclude gets
  ignored due to implementation details.

* Fri Aug 25 2017 Peter Jones <pjones@redhat.com> - 2.02-13
- Add some unconditional Provides:
  grub2-efi on grub2-efi-${arch}
  grub2-efi-cdboot on grub2-efi-${arch}-cdboot
  grub2 on all grub2-${arch} pacakges
- Something is somehow adding /usr/lib/.build-id/... to all the -tools
  subpackages, so exclude all that.

* Thu Aug 24 2017 Peter Jones <pjones@redhat.com> - 2.02-12
- Fix arm kernel command line allocation
  Resolves: rhbz#1484609
- Get rid of the temporary extra efi packages hack.

* Wed Aug 23 2017 Peter Jones <pjones@redhat.com> - 2.02-11
- Put grub2-mkimage in -tools, not -tools-extra.
- Fix i686 building
- Fix ppc HFS+ usage due to /boot/efi's presence.

* Fri Aug 18 2017 Peter Jones <pjones@redhat.com> - 2.02-10
- Add the .img files into grub2-pc-modules (and all legacy variants)

* Wed Aug 16 2017 Peter Jones <pjones@redhat.com> - 2.02-9
- Re-work for ia32-efi.

* Wed Aug 16 2017 pjones <pjones@redhat.com> - 2.02-8
- Rebased to newer upstream for fedora-27

* Tue Aug 15 2017 Peter Jones <pjones@redhat.com> - 2.02-7
- Rebuild again with new fixed rpm. (bug #1480407)

* Fri Aug 11 2017 Kevin Fenzi <kevin@scrye.com> - 2.02-6
- Rebuild again with new fixed rpm. (bug #1480407)

* Thu Aug 10 2017 Kevin Fenzi <kevin@scrye.com> - 2.02-5
- Rebuild for rpm soname bump again.

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.02-4
- Rebuilt for RPM soname bump

* Thu Aug 03 2017 Peter Jones <pjones@redhat.com> - 2.02-3
- Rebuild so it gets SB signed correctly.
  Related: rhbz#1335533
- Enable lsefi

* Mon Jul 24 2017 Michael Cronenworth <mike@cchtml.com> - 2.02-2
- Fix symlink to work on both EFI and BIOS machines
  Resolves: rhbz#1335533

* Mon Jul 10 2017 Peter Jones <pjones@redhat.com> - 2.02-1
- Rebased to newer upstream for fedora-27

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 2.02-0.39
- Add missing %%license macro
- Fix deps that should have moved to -tools but didn't.

* Thu Dec 08 2016 Peter Jones <pjones@redhat.com> - 2.02-0.38
- Fix regexp in power compile flags, and synchronize release number with
  other branches.

* Fri Dec 02 2016 pjones <pjones@redhat.com> - 1:2.02-0.37
- Rebased to newer upstream for fedora-26

* Thu Dec 01 2016 Peter Jones <pjones@redhat.com> - 2.02-0.36
- Update version to .36 because I already built an f25 one named 0.35

* Thu Dec 01 2016 pjones <pjones@redhat.com> - 1:2.02-0.35
- Rebased to newer upstream for fedora-26

* Thu Dec 01 2016 Peter Jones <pjones@redhat.com> - 2.02-0.34
- Fix power6 makefile bits for newer autoconf defaults.
- efi/chainloader: fix wrong sanity check in relocate_coff() (Laszlo Ersek)
  Resolves: rhbz#1347291

* Thu Aug 25 2016 Peter Jones <pjones@redhat.com> - 2.02-0.34
- Update to be newer than f24's branch.
- Add grub2-get-kernel-settings
  Related: rhbz#1226325

* Thu Apr 07 2016 pjones <pjones@redhat.com> - 1:2.02-0.30
- Revert 27e66193, which was replaced by upstream's 49426e9fd
  Resolves: rhbz#1251600

* Thu Apr 07 2016 Peter Jones <pjones@redhat.com> - 2.02-0.29
- Fix ppc64 build failure and rebase to newer f24 code.

* Tue Apr 05 2016 pjones <pjones@redhat.com> - 1:2.02-0.27
- Pull TPM updates from mjg59.
  Resolves: rhbz#1318067

* Tue Mar 08 2016 pjones <pjones@redhat.com> - 1:2.02-0.27
- Fix aarch64 build problem.

* Fri Mar 04 2016 Peter Jones <pjones@redhat.com> - 2.02-0.26
- Rebased to newer upstream (grub-2.02-beta3) for fedora-24

* Thu Dec 10 2015 Peter Jones <pjones@redhat.com> - 2.02-0.25
- Fix security issue when reading username and password
  Related: CVE-2015-8370
- Do a better job of handling GRUB2_PASSWORD
  Related: rhbz#1284370

* Fri Nov 20 2015 Peter Jones <pjones@redhat.com> - 2.02-0.24
- Rebuild without multiboot* modules in the EFI image.
  Related: rhbz#1264103

* Sat Sep 05 2015 Kalev Lember <klember@redhat.com> - 2.02-0.23
- Rebuilt for librpm soname bump

* Wed Aug 05 2015 Peter Jones <pjones@redhat.com> - 2.02-0.21
- Back out one of the debuginfo generation patches; it doesn't work right on
  aarch64 yet.
  Resolves: rhbz#1250197

* Mon Aug 03 2015 Peter Jones <pjones@redhat.com> - 2.02-0.20
- The previous fix was completely not right, so fix it a different way.
  Resolves: rhbz#1249668

* Fri Jul 31 2015 Peter Jones <pjones@redhat.com> - 2.02-0.19
- Fix grub2-mkconfig's sort to put kernels in the right order.
  Related: rhbz#1124074

* Thu Jul 30 2015 Peter Jones <pjones@redhat.com> - 2.02-0.18
- Fix a build failure on aarch64

* Wed Jul 22 2015 Peter Jones <pjones@redhat.com> - 2.02-0.17
- Don't build hardened (fixes FTBFS) (pbrobinson)
- Reconcile with the current upstream
- Fixes for gcc 5

* Tue Apr 28 2015 Peter Jones <pjones@redhat.com> - 2.02-0.16
- Make grub2-mkconfig produce the kernel titles we actually want.
  Resolves: rhbz#1215839

* Sat Feb 21 2015 Till Maas <opensource@till.name>
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Jan 05 2015 Peter Jones <pjones@redhat.com> - 2.02-0.15
- Bump release to rebuild with Ralf Corsépius's fixes.

* Sun Jan 04 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.02-0.14
- Move grub2.info/grub2-dev.info install-info scriptlets into *-tools package.
- Use sub-shell in %%__debug_install_post (RHBZ#1168732).
- Cleanup grub2-starfield-theme packaging.

* Thu Dec 04 2014 Peter Jones <pjones@redhat.com> - 2.02-0.13
- Update minilzo to 2.08 for CVE-2014-4607
  Resolves: rhbz#1131793

* Thu Nov 13 2014 Peter Jones <pjones@redhat.com> - 2.02-0.12
- Make backtrace and usb conditional on !arm
- Make sure gcdaa64.efi is packaged.
  Resolves: rhbz#1163481

* Fri Nov 07 2014 Peter Jones <pjones@redhat.com> - 2.02-0.11
- fix a copy-paste error in patch 0154.
  Resolves: rhbz#964828

* Mon Oct 27 2014 Peter Jones <pjones@redhat.com> - 2.02-0.10
- Try to emit linux16/initrd16 and linuxefi/initrdefi when appropriate
  in 30_os-prober.
  Resolves: rhbz#1108296
- If $fw_path doesn't work to find the config file, try $prefix as well
  Resolves: rhbz#1148652

* Mon Sep 29 2014 Peter Jones <pjones@redhat.com> - 2.02-0.9
- Clean up the build a bit to make it faster
- Make grubenv work right on UEFI machines
  Related: rhbz#1119943
- Sort debug and rescue kernels later than normal ones
  Related: rhbz#1065360
- Allow "fallback" to include entries by title as well as number.
  Related: rhbz#1026084
- Fix a segfault on aarch64.
- Load arm with SB enabled if available.
- Add some serial port options to GRUB_MODULES.

* Tue Aug 19 2014 Peter Jones <pjones@redhat.com> - 2.02-0.8
- Add ppc64le support.
  Resolves: rhbz#1125540

* Thu Jul 24 2014 Peter Jones <pjones@redhat.com> - 2.02-0.7
- Enabled syslinuxcfg module.

* Wed Jul 02 2014 Peter Jones <pjones@redhat.com> - 2.02-0.6
- Re-merge RHEL 7 changes and ARM works in progress.

* Mon Jun 30 2014 Peter Jones <pjones@redhat.com> - 2.02-0.5
- Avoid munging raw spaces when we're escaping command line arguments.
  Resolves: rhbz#923374

* Tue Jun 24 2014 Peter Jones <pjones@redhat.com> - 2.02-0.4
- Update to latest upstream.

* Thu Mar 13 2014 Peter Jones <pjones@redhat.com> - 2.02-0.3
- Merge in RHEL 7 changes and ARM works in progress.

* Mon Jan 06 2014 Peter Jones <pjones@redhat.com> - 2.02-0.2
- Update to grub-2.02~beta2

* Sat Aug 10 2013 Peter Jones <pjones@redhat.com> - 2.00-25
- Last build failed because of a hardware error on the builder.

* Mon Aug 05 2013 Peter Jones <pjones@redhat.com> - 2.00-24
- Fix compiler flags to deal with -fstack-protector-strong

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.00-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 Dennis Gilmore <dennis@ausil.us> - 2.00-23
- add epoch to obsoletes

* Fri Jun 21 2013 Peter Jones <pjones@redhat.com> - 2.00-22
- Fix linewrapping in edit menu.
  Resolves: rhbz #976643

* Thu Jun 20 2013 Peter Jones <pjones@redhat.com> - 2.00-21
- Fix obsoletes to pull in -starfield-theme subpackage when it should.

* Fri Jun 14 2013 Peter Jones <pjones@redhat.com> - 2.00-20
- Put the theme entirely ento the subpackage where it belongs (#974667)

* Wed Jun 12 2013 Peter Jones <pjones@redhat.com> - 2.00-19
- Rebase to upstream snapshot.
- Fix PPC build error (#967862)
- Fix crash on net_bootp command (#960624)
- Reset colors on ppc when appropriate (#908519)
- Left align "Loading..." messages (#908492)
- Fix probing of SAS disks on PPC (#953954)
- Add support for UEFI OSes returned by os-prober
- Disable "video" mode on PPC for now (#973205)
- Make grub fit better into the boot sequence, visually (#966719)

* Fri May 10 2013 Matthias Clasen <mclasen@redhat.com> - 2.00-18
- Move the starfield theme to a subpackage (#962004)
- Don't allow SSE or MMX on UEFI builds (#949761)

* Wed Apr 24 2013 Peter Jones <pjones@redhat.com> - 2.00-17.pj0
- Rebase to upstream snapshot.

* Thu Apr 04 2013 Peter Jones <pjones@redhat.com> - 2.00-17
- Fix booting from drives with 4k sectors on UEFI.
- Move bash completion to new location (#922997)
- Include lvm support for /boot (#906203)

* Thu Feb 14 2013 Peter Jones <pjones@redhat.com> - 2.00-16
- Allow the user to disable submenu generation
- (partially) support BLS-style configuration stanzas.

* Tue Feb 12 2013 Peter Jones <pjones@redhat.com> - 2.00-15.pj0
- Add various config file related changes.

* Thu Dec 20 2012 Dennis Gilmore <dennis@ausil.us> - 2.00-15
- bump nvr

* Mon Dec 17 2012 Karsten Hopp <karsten@redhat.com> 2.00-14
- add bootpath device to the device list (pfsmorigo, #886685)

* Tue Nov 27 2012 Peter Jones <pjones@redhat.com> - 2.00-13
- Add vlan tag support (pfsmorigo, #871563)
- Follow symlinks during PReP installation in grub2-install (pfsmorigo, #874234)
- Improve search paths for config files on network boot (pfsmorigo, #873406)

* Tue Oct 23 2012 Peter Jones <pjones@redhat.com> - 2.00-12
- Don't load modules when grub transitions to "normal" mode on UEFI.

* Mon Oct 22 2012 Peter Jones <pjones@redhat.com> - 2.00-11
- Rebuild with newer pesign so we'll get signed with the final signing keys.

* Thu Oct 18 2012 Peter Jones <pjones@redhat.com> - 2.00-10
- Various PPC fixes.
- Fix crash fetching from http (gustavold, #860834)
- Issue separate dns queries for ipv4 and ipv6 (gustavold, #860829)
- Support IBM CAS reboot (pfsmorigo, #859223)
- Include all modules in the core image on ppc (pfsmorigo, #866559)

* Mon Oct 01 2012 Peter Jones <pjones@redhat.com> - 1:2.00-9
- Work around bug with using "\x20" in linux command line.
  Related: rhbz#855849

* Thu Sep 20 2012 Peter Jones <pjones@redhat.com> - 2.00-8
- Don't error on insmod on UEFI/SB, but also don't do any insmodding.
- Increase device path size for ieee1275
  Resolves: rhbz#857936
- Make network booting work on ieee1275 machines.
  Resolves: rhbz#857936

* Wed Sep 05 2012 Matthew Garrett <mjg@redhat.com> - 2.00-7
- Add Apple partition map support for EFI

* Thu Aug 23 2012 David Cantrell <dcantrell@redhat.com> - 2.00-6
- Only require pesign on EFI architectures (#851215)

* Tue Aug 14 2012 Peter Jones <pjones@redhat.com> - 2.00-5
- Work around AHCI firmware bug in efidisk driver.
- Move to newer pesign macros
- Don't allow insmod if we're in secure-boot mode.

* Wed Aug 08 2012 Peter Jones <pjones@redhat.com>
- Split module lists for UEFI boot vs UEFI cd images.
- Add raid modules for UEFI image (related: #750794)
- Include a prelink whitelist for binaries that need execstack (#839813)
- Include fix efi memory map fix from upstream (#839363)

* Wed Aug 08 2012 Peter Jones <pjones@redhat.com> - 2.00-4
- Correct grub-mkimage invocation to use efidir RPM macro (jwb)
- Sign with test keys on UEFI systems.
- PPC - Handle device paths with commas correctly.
  Related: rhbz#828740

* Wed Jul 25 2012 Peter Jones <pjones@redhat.com> - 2.00-3
- Add some more code to support Secure Boot, and temporarily disable
  some other bits that don't work well enough yet.
  Resolves: rhbz#836695

* Wed Jul 11 2012 Matthew Garrett <mjg@redhat.com> - 2.00-2
- Set a prefix for the image - needed for installer work
- Provide the font in the EFI directory for the same reason

* Thu Jun 28 2012 Peter Jones <pjones@redhat.com> - 2.00-1
- Rebase to grub-2.00 release.

* Mon Jun 18 2012 Peter Jones <pjones@redhat.com> - 2.0-0.37.beta6
- Fix double-free in grub-probe.

* Wed Jun 06 2012 Peter Jones <pjones@redhat.com> - 2.0-0.36.beta6
- Build with patch19 applied.

* Wed Jun 06 2012 Peter Jones <pjones@redhat.com> - 2.0-0.35.beta6
- More ppc fixes.

* Wed Jun 06 2012 Peter Jones <pjones@redhat.com> - 2.0-0.34.beta6
- Add IBM PPC fixes.

* Mon Jun 04 2012 Peter Jones <pjones@redhat.com> - 2.0-0.33.beta6
- Update to beta6.
- Various fixes from mads.

* Fri May 25 2012 Peter Jones <pjones@redhat.com> - 2.0-0.32.beta5
- Revert builddep change for crt1.o; it breaks ppc build.

* Fri May 25 2012 Peter Jones <pjones@redhat.com> - 2.0-0.31.beta5
- Add fwsetup command (pjones)
- More ppc fixes (IBM)

* Tue May 22 2012 Peter Jones <pjones@redhat.com> - 2.0-0.30.beta5
- Fix the /other/ grub2-tools require to include epoch.

* Mon May 21 2012 Peter Jones <pjones@redhat.com> - 2.0-0.29.beta5
- Get rid of efi_uga and efi_gop, favoring all_video instead.

* Mon May 21 2012 Peter Jones <pjones@redhat.com> - 2.0-0.28.beta5
- Name grub.efi something that's arch-appropriate (kiilerix, pjones)
- use EFI/$SOMETHING_DISTRO_BASED/ not always EFI/redhat/grub2-efi/ .
- move common stuff to -tools (kiilerix)
- spec file cleanups (kiilerix)

* Mon May 14 2012 Peter Jones <pjones@redhat.com> - 2.0-0.27.beta5
- Fix module trampolining on ppc (benh)

* Thu May 10 2012 Peter Jones <pjones@redhat.com> - 2.0-0.27.beta5
- Fix license of theme (mizmo)
  Resolves: rhbz#820713
- Fix some PPC bootloader detection IBM problem
  Resolves: rhbz#820722

* Thu May 10 2012 Peter Jones <pjones@redhat.com> - 2.0-0.26.beta5
- Update to beta5.
- Update how efi building works (kiilerix)
- Fix theme support to bring in fonts correctly (kiilerix, pjones)

* Wed May 09 2012 Peter Jones <pjones@redhat.com> - 2.0-0.25.beta4
- Include theme support (mizmo)
- Include locale support (kiilerix)
- Include html docs (kiilerix)

* Thu Apr 26 2012 Peter Jones <pjones@redhat.com> - 2.0-0.24
- Various fixes from Mads Kiilerich

* Thu Apr 19 2012 Peter Jones <pjones@redhat.com> - 2.0-0.23
- Update to 2.00~beta4
- Make fonts work so we can do graphics reasonably

* Thu Mar 29 2012 David Aquilina <dwa@redhat.com> - 2.0-0.22
- Fix ieee1275 platform define for ppc

* Thu Mar 29 2012 Peter Jones <pjones@redhat.com> - 2.0-0.21
- Remove ppc excludearch lines (dwa)
- Update ppc terminfo patch (hamzy)

* Wed Mar 28 2012 Peter Jones <pjones@redhat.com> - 2.0-0.20
- Fix ppc64 vs ppc exclude according to what dwa tells me they need
- Fix version number to better match policy.

* Tue Mar 27 2012 Dan Horák <dan[at]danny.cz> - 1.99-19.2
- Add support for serial terminal consoles on PPC by Mark Hamzy

* Sun Mar 25 2012 Dan Horák <dan[at]danny.cz> - 1.99-19.1
- Use Fix-tests-of-zeroed-partition patch by Mark Hamzy

* Thu Mar 15 2012 Peter Jones <pjones@redhat.com> - 1.99-19
- Use --with-grubdir= on configure to make it behave like -17 did.

* Wed Mar 14 2012 Peter Jones <pjones@redhat.com> - 1.99-18
- Rebase from 1.99 to 2.00~beta2

* Wed Mar 07 2012 Peter Jones <pjones@redhat.com> - 1.99-17
- Update for newer autotools and gcc 4.7.0
  Related: rhbz#782144
- Add /etc/sysconfig/grub link to /etc/default/grub
  Resolves: rhbz#800152
- ExcludeArch s390*, which is not supported by this package.
  Resolves: rhbz#758333

* Fri Feb 17 2012 Orion Poplawski <orion@cora.nwra.com> - 1:1.99-16
- Build with -Os (bug 782144)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.99-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Matthew Garrett <mjg@redhat.com> - 1.99-14
- fix up various grub2-efi issues

* Thu Dec 08 2011 Adam Williamson <awilliam@redhat.com> - 1.99-13
- fix hardwired call to grub-probe in 30_os-prober (rhbz#737203)

* Mon Nov 07 2011 Peter Jones <pjones@redhat.com> - 1.99-12
- Lots of .spec fixes from Mads Kiilerich:
  Remove comment about update-grub - it isn't run in any scriptlets
  patch info pages so they can be installed and removed correctly when renamed
  fix references to grub/grub2 renames in info pages (#743964)
  update README.Fedora (#734090)
  fix comments for the hack for upgrading from grub2 < 1.99-4
  fix sed syntax error preventing use of $RPM_OPT_FLAGS (#704820)
  make /etc/grub2*.cfg %%config(noreplace)
  make grub.cfg %%ghost - an empty file is of no use anyway
  create /etc/default/grub more like anaconda would create it (#678453)
  don't create rescue entries by default - grubby will not maintain them anyway
  set GRUB_SAVEDEFAULT=true so saved defaults works (rbhz#732058)
  grub2-efi should have its own bash completion
  don't set gfxpayload in efi mode - backport upstream r3402
- Handle dmraid better. Resolves: rhbz#742226

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.99-11
- Rebuilt for glibc bug#747377

* Wed Oct 19 2011 Adam Williamson <awilliam@redhat.com> - 1.99-10
- /etc/default/grub is explicitly intended for user customization, so
  mark it as config(noreplace)

* Tue Oct 11 2011 Peter Jones <pjones@redhat.com> - 1.99-9
- grub has an epoch, so we need that expressed in the obsolete as well.
  Today isn't my day.

* Tue Oct 11 2011 Peter Jones <pjones@redhat.com> - 1.99-8
- Fix my bad obsoletes syntax.

* Thu Oct 06 2011 Peter Jones <pjones@redhat.com> - 1.99-7
- Obsolete grub
  Resolves: rhbz#743381

* Wed Sep 14 2011 Peter Jones <pjones@redhat.com> - 1.99-6
- Use mv not cp to try to avoid moving disk blocks around for -5 fix
  Related: rhbz#735259
- handle initramfs on xen better (patch from Marko Ristola)
  Resolves: rhbz#728775

* Sat Sep 03 2011 Kalev Lember <kalevlember@gmail.com> - 1.99-5
- Fix upgrades from grub2 < 1.99-4 (#735259)

* Fri Sep 02 2011 Peter Jones <pjones@redhat.com> - 1.99-4
- Don't do sysadminny things in %%preun or %%post ever. (#735259)
- Actually include the changelog in this build (sorry about -3)

* Thu Sep 01 2011 Peter Jones <pjones@redhat.com> - 1.99-2
- Require os-prober (#678456) (patch from Elad Alfassa)
- Require which (#734959) (patch from Elad Alfassa)

* Thu Sep 01 2011 Peter Jones <pjones@redhat.com> - 1.99-1
- Update to grub-1.99 final.
- Fix crt1.o require on x86-64 (fix from Mads Kiilerich)
- Various CFLAGS fixes (from Mads Kiilerich)
  - -fexceptions and -m64
- Temporarily ignore translations (from Mads Kiilerich)

* Thu Jul 21 2011 Peter Jones <pjones@redhat.com> - 1.99-0.3
- Use /sbin not /usr/sbin .

* Thu Jun 23 2011 Peter Lemenkov <lemenkov@gmail.com> - 1:1.99-0.2
- Fixes for ppc and ppc64

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.98-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
