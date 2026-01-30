%global security_hardening none
%global sha512hmac bash %{_sourcedir}/sha512hmac-openssl.sh
%global mstflintver 4.28.0
%define uname_r %{version}-%{release}
%define mariner_version 3
%define short_name 64k

# find_debuginfo.sh arguments are set by default in rpm's macros.
# The default arguments regenerate the build-id for vmlinux in the
# debuginfo package causing a mismatch with the build-id for vmlinuz in
# the kernel package. Therefore, explicilty set the relevant default
# settings to prevent this behavior.
%undefine _unique_build_ids
%undefine _unique_debug_names
%global _missing_build_ids_terminate_build 1
%global _no_recompute_build_ids 1
# Prevent find_debuginfo.sh from removing the BTF section from modules
%define _find_debuginfo_opts --keep-section '.BTF'

%ifarch aarch64
%global __provides_exclude_from %{_libdir}/debug/.build-id/
%define arch arm64
%define archdir arm64
%define config_source %{SOURCE1}
%endif

Summary:        Linux Kernel
Name:           kernel-64k
Version:        6.6.121.1
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Kernel
URL:            https://github.com/microsoft/CBL-Mariner-Linux-Kernel
Source0:        https://github.com/microsoft/CBL-Mariner-Linux-Kernel/archive/rolling-lts/mariner-%{mariner_version}/%{version}.tar.gz#/kernel-%{version}.tar.gz
Source1:        config_aarch64
Source2:        sha512hmac-openssl.sh
Source3:        azurelinux-ca-20230216.pem
Source4:        cpupower
Source5:        cpupower.service
Patch0:         0001-add-mstflint-kernel-%{mstflintver}.patch
Patch1:         0002-efi-Added-efi-cmdline-line-option-to-dynamically-adj.patch
ExclusiveArch:  aarch64
BuildRequires:  audit-devel
BuildRequires:  bash
BuildRequires:  bc
BuildRequires:  build-essential
BuildRequires:  cpio
BuildRequires:  diffutils
BuildRequires:  dwarves
BuildRequires:  elfutils-libelf-devel
BuildRequires:  flex
BuildRequires:  gettext
BuildRequires:  glib-devel
BuildRequires:  grub2-rpm-macros
BuildRequires:  kbd
BuildRequires:  kmod-devel
BuildRequires:  libcap-devel
BuildRequires:  libdnet-devel
BuildRequires:  libmspack-devel
BuildRequires:  libtraceevent-devel
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  procps-ng-devel
BuildRequires:  python3-devel
BuildRequires:  sed
BuildRequires:  slang-devel
BuildRequires:  systemd-bootstrap-rpm-macros
Requires:       filesystem
Requires:       kmod
Requires(post): coreutils
Requires(postun): coreutils
Conflicts:      kernel
Conflicts:      kernel-ipe
Conflicts:      kernel-lpg-innovate
Conflicts:      kernel-rt
Conflicts:      kernel-hwe
%{?grub2_configuration_requires}
# When updating the config files it is important to sanitize them.
# Steps for updating a config file:
#  1. Extract the linux sources into a folder
#  2. Add the current config file to the folder
#  3. Run `make menuconfig` to edit the file (Manually editing is not recommended)
#  4. Save the config file
#  5. Copy the config file back into the kernel spec folder
#  6. Revert any undesired changes (GCC related changes, etc)
#  8. Build the kernel package
#  9. Apply the changes listed in the log file (if any) to the config file
#  10. Verify the rest of the config file looks ok
# If there are significant changes to the config file, disable the config check and build the
# kernel rpm. The final config file is included in /boot in the rpm.

%description
The kernel package contains the Linux kernel.

%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Requires:       gawk
Requires:       python3
Obsoletes:      linux-dev

%description devel
This package contains the Linux kernel dev files

%package drivers-accessibility
Summary:        Kernel accessibility modules
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}

%description drivers-accessibility
This package contains the Linux kernel accessibility support

%package drivers-gpu
Summary:        Kernel gpu modules
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}

%description drivers-gpu
This package contains the Linux kernel gpu support

%package drivers-sound
Summary:        Kernel Sound modules
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}

%description drivers-sound
This package contains the Linux kernel sound support

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3

%description docs
This package contains the Linux kernel doc files

%package tools
Summary:        This package contains the 'perf' performance analysis tools for Linux kernel
Group:          System/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       audit

%description tools
This package contains the 'perf' performance analysis tools for Linux kernel.

%package -n     python3-perf-%{short_name}
Summary:        Python 3 extension for perf tools
Provides:       python3-perf
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description -n python3-perf-%{short_name}
This package contains the Python 3 extension for the 'perf' performance analysis tools for Linux kernel.

%package -n     bpftool-%{short_name}
Summary:        Inspection and simple manipulation of eBPF programs and maps
Provides:       bpftool
Requires:       %{name} = %{version}-%{release}

%description -n bpftool-%{short_name}
This package contains the bpftool, which allows inspection and simple
manipulation of eBPF programs and maps.

%prep
%autosetup -p1 -n CBL-Mariner-Linux-Kernel-rolling-lts-mariner-%{mariner_version}-%{version}
make mrproper

cp %{config_source} .config

# Add CBL-Mariner cert into kernel's trusted keyring
cp %{SOURCE3} certs/mariner.pem
sed -i 's#CONFIG_SYSTEM_TRUSTED_KEYS=""#CONFIG_SYSTEM_TRUSTED_KEYS="certs/mariner.pem"#' .config

cp .config current_config
sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{release}"/' .config
make LC_ALL=  ARCH=%{arch} oldconfig

# Verify the config files match
cp .config new_config
sed -i 's/CONFIG_LOCALVERSION=".*"/CONFIG_LOCALVERSION=""/' new_config
diff --unified new_config current_config > config_diff || true
if [ -s config_diff ]; then
    printf "\n\n\n\n\n\n\n\n"
    cat config_diff
    printf "\n\n\n\n\n\n\n\n"
    echo "Config file has unexpected changes"
    echo "Update config file to set changed values explicitly"

#  (DISABLE THIS IF INTENTIONALLY UPDATING THE CONFIG FILE)
    exit 1
fi

%build
make VERBOSE=1 KBUILD_BUILD_VERSION="1" KBUILD_BUILD_HOST="CBL-Mariner" ARCH=%{arch} %{?_smp_mflags}

# Compile perf, python3-perf
make -C tools/perf PYTHON=%{python3} all

#Compile bpftool
make -C tools/bpf/bpftool

%define __modules_install_post \
for MODULE in `find %{buildroot}/lib/modules/%{uname_r} -name *.ko` ; do \
    ./scripts/sign-file sha512 certs/signing_key.pem certs/signing_key.x509 $MODULE \
    rm -f $MODULE.{sig,dig} \
    xz $MODULE \
    done \
%{nil}

# We want to compress modules after stripping. Extra step is added to
# the default __spec_install_post.
%define __spec_install_post\
    %{?__debug_package:%{__debug_install_post}}\
    %{__arch_install_post}\
    %{__os_install_post}\
    %{__modules_install_post}\
%{nil}

%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 700 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/lib/modules/%{uname_r}

install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -c -m 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/sysconfig/cpupower
install -d -m 755 %{buildroot}%{_unitdir}
install -c -m 644 %{SOURCE5} %{buildroot}%{_unitdir}/cpupower.service

make INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch aarch64
install -vm 600 arch/arm64/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}
%endif

# Restrict the permission on System.map-X file
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 600 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/linux-%{uname_r}
install -vm 744 vmlinux %{buildroot}%{_libdir}/debug/lib/modules/%{uname_r}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}%{_libdir}/debug/lib/modules/%{uname_r}/vmlinux

# hmac sign the kernel for FIPS
%{sha512hmac} %{buildroot}/boot/vmlinuz-%{uname_r} | sed -e "s,$RPM_BUILD_ROOT,," > %{buildroot}/boot/.vmlinuz-%{uname_r}.hmac
cp %{buildroot}/boot/.vmlinuz-%{uname_r}.hmac %{buildroot}/lib/modules/%{uname_r}/.vmlinuz.hmac

# Symlink /lib/modules/uname/vmlinuz to boot partition
ln -s /boot/vmlinuz-%{uname_r} %{buildroot}/lib/modules/%{uname_r}/vmlinuz

#    Cleanup dangling symlinks
rm -rf %{buildroot}/lib/modules/%{uname_r}/source
rm -rf %{buildroot}/lib/modules/%{uname_r}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}' copy
find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}' copy
find arch/%{archdir}/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}' copy

cp .config %{buildroot}%{_prefix}/src/linux-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "%{_prefix}/src/linux-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%ifarch aarch64
cp scripts/module.lds %{buildroot}%{_prefix}/src/linux-headers-%{uname_r}/scripts/module.lds
%endif

# disable (JOBS=1) parallel build to fix this issue:
# fixdep: error opening depfile: ./.plugin_cfg80211.o.d: No such file or directory
# Linux version that was affected is 4.4.26
make -C tools JOBS=1 DESTDIR=%{buildroot} prefix=%{_prefix} perf_install

# Install python3-perf
make -C tools/perf DESTDIR=%{buildroot} prefix=%{_prefix} install-python_ext

# Install bpftool
make -C tools/bpf/bpftool DESTDIR=%{buildroot} prefix=%{_prefix} bash_compdir=%{_sysconfdir}/bash_completion.d/ mandir=%{_mandir} install

# Remove trace (symlink to perf). This file causes duplicate identical debug symbols
rm -vf %{buildroot}%{_bindir}/trace

%triggerin -- initramfs
mkdir -p %{_localstatedir}/lib/rpm-state/initramfs/pending
touch %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
echo "initrd generation of kernel %{uname_r} will be triggered later" >&2

%triggerun -- initramfs
rm -rf %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
rm -rf /boot/initramfs-%{uname_r}.img
echo "initrd of kernel %{uname_r} removed" >&2

%preun tools
%systemd_preun cpupower.service

%postun
%grub2_postun

%postun tools
%systemd_postun cpupower.service

%post
/sbin/depmod -a %{uname_r}
%grub2_post

%post drivers-accessibility
/sbin/depmod -a %{uname_r}

%post drivers-gpu
/sbin/depmod -a %{uname_r}

%post drivers-sound
/sbin/depmod -a %{uname_r}

%post tools
%systemd_post cpupower.service

%files
%defattr(-,root,root)
%license COPYING
%exclude %dir /usr/lib/debug
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
/boot/.vmlinuz-%{uname_r}.hmac
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
/lib/modules/%{uname_r}/.vmlinuz.hmac
%exclude /lib/modules/%{uname_r}/build
%exclude /lib/modules/%{uname_r}/kernel/drivers/accessibility
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
%{_prefix}/src/linux-headers-%{uname_r}

%files drivers-accessibility
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/drivers/accessibility

%files drivers-gpu
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/drivers/gpu

%files drivers-sound
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/sound

%files tools
%defattr(-,root,root)
%{_libexecdir}
%exclude %dir %{_libdir}/debug
%ifarch aarch64
%{_libdir}/libperf-jvmti.so
%endif
%{_bindir}
%{_sysconfdir}/bash_completion.d/*
%{_datadir}/perf-core/strace/groups/file
%{_datadir}/perf-core/strace/groups/string
%{_docdir}/*
%{_includedir}/perf/perf_dlfilter.h
%{_unitdir}/cpupower.service
%config(noreplace) %{_sysconfdir}/sysconfig/cpupower

%files -n python3-perf-%{short_name}
%{python3_sitearch}/*

%files -n bpftool-%{short_name}
%{_sbindir}/bpftool
%{_sysconfdir}/bash_completion.d/bpftool

%changelog
* Wed Jan 28 2026 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.121.1-1
- Auto-upgrade to 6.6.121.1

* Fri Jan 16 2026 Rachel Menge <rachelmenge@microsoft.com> - 6.6.119.3-3
- Bump release to match kernel,kernel-ipe

* Thu Jan 08 2026 Rachel Menge <rachelmenge@microsoft.com> - 6.6.119.3-2
- Enable CONFIG_INET_DIAG_DESTROY

* Tue Jan 06 2026 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.119.3-1
- Auto-upgrade to 6.6.119.3

* Wed Nov 26 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.117.1-1
- Auto-upgrade to 6.6.117.1

* Tue Nov 18 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.116.1-2
- Enable dm-cache

* Mon Nov 10 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.116.1-1
- Auto-upgrade to 6.6.116.1

* Mon Oct 27 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.112.1-2
- Bump release to match kernel

* Wed Oct 15 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.112.1-1
- Auto-upgrade to 6.6.112.1

* Tue Sep 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.104.2-4
- Bump release to match kernel

* Tue Sep 23 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 6.6.104.2-3
- Bump release to match kernel

* Tue Sep 23 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.104.2-2
- Enable ipmitool for kernel-64k

* Wed Sep 17 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.104.2-1
- Auto-upgrade to 6.6.104.2

* Fri Aug 22 2025 Siddharth Chintamaneni <siddharthc@microsoft.com> - 6.6.96.2-2
- Bump release to match kernel

* Fri Aug 15 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.96.2-1
- Auto-upgrade to 6.6.96.2

* Thu Jul 17 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.96.1-2
- Bump release to match kernel

* Mon Jul 07 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.96.1-1
- Auto-upgrade to 6.6.96.1

* Mon Jun 16 2025 Harshit Gupta <guptaharshit@microsoft.com> - 6.6.92.2-3
- Add Conflicts with other kernels
- Rename bpftool and python3-perf to be kernel specific

* Mon Jun 09 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.92.2-2
- Prevent debuginfo from stripping BTF data

* Fri May 30 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.92.2-1
- Auto-upgrade to 6.6.92.2

* Fri May 23 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.90.1-1
- Auto-upgrade to 6.6.90.1

* Tue May 13 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 6.6.85.1-4
- Added a new patch to EFI slack slots issue

* Tue Apr 29 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 6.6.85.1-3
- Updated config_aarch64 based on nvidia patch guide recommendations

* Fri Apr 25 2025 Chris Co <chrco@microsoft.com> - 6.6.85.1-2
- Bump release to rebuild for new kernel release

* Sat Apr 05 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.85.1-1
- Auto-upgrade to 6.6.85.1

* Fri Mar 14 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.82.1-1
- Auto-upgrade to 6.6.82.1

* Tue Mar 11 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.79.1-1
- Auto-upgrade to 6.6.79.1
- Remove jitterentropy patch as it is included in the source

* Mon Mar 10 2025 Chris Co <chrco@microsoft.com> - 6.6.78.1-3
- Add patch to revert UART change that breaks IPMI SEL panic message

* Wed Mar 05 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.78.1-2
- Add slang as BuildRequires, enabling tui on perf

* Mon Mar 03 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.78.1-1
- Auto-upgrade to 6.6.78.1

* Wed Feb 19 2025 Chris Co <chrco@microsoft.com> - 6.6.76.1-2
- Enable Tegra IVC protocol

* Mon Feb 10 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.76.1-1
- Auto-upgrade to 6.6.76.1

* Wed Feb 05 2025 Tobias Brick <tobiasb@microsoft.com> - 6.6.64.2-9
- Apply upstream patches to fix kernel panic in jitterentropy initialization on
  ARM64 FIPS boot

* Tue Feb 04 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 6.6.64.2-8
- Bump release to match kernel

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 6.6.64.2-7
- Bump release to match kernel

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 6.6.64.2-6
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.64.2-5
- Enable ipmitool for kernel-64k

* Sat Jan 18 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.64.2-4
- Build PCI_HYPERV as builtin

* Thu Jan 16 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.64.2-3
- Bump release to match kernel

* Fri Jan 10 2025 Rachel Menge <rachelmenge@microsoft.com> - 6.6.64.2-2
- Bump release to match kernel

* Thu Jan 09 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 6.6.64.2-1
- Auto-upgrade to 6.6.64.2

* Wed Jan 08 2025 Tobias Brick <tobiasb@microsoft.com> - 6.6.57.1-8
- Enable dh kernel module (CONFIG_CRYPTO_DH) in aarch64
- Bump release to match kernel

* Sun Dec 22 2024 Ankita Pareek <ankitapareek@microsoft.com> - 6.6.57.1-7
- Bump release to match kernel

* Wed Dec 18 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.57.1-6
- Enable kexec signature verification

* Thu Nov 07 2024 Rachel Menge <rachelmenge@microsoft.com> - 6.6.57.1-5
- Initial CBL-Mariner import from Photon (license: Apache2).
- Starting with release 5 to align with kernel release.
- License verified
