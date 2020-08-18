%global with_signed 0
%global security_hardening none
Summary:        Linux Kernel
Name:           kernel
Version:        5.4.42
Release:        10%{?dist}
License:        GPLv2
URL:            https://github.com/microsoft/WSL2-Linux-Kernel
Group:          System Environment/Kernel
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/microsoft/WSL2-Linux-Kernel/archive/linux-msft-%{version}.tar.gz
Source1:        config
Source2:        config_aarch64
%if 0%{?with_signed}
Source100:      vmlinuz-x86_64.%{version}-%{release}.signed
Source101:      vmlinuz-aarch64.%{version}-%{release}.signed
%endif
Patch0:         e1000e-add-support-for-comet-lake.patch

Patch1000:      CVE-2020-8992.nopatch
Patch1001:      CVE-2020-12770.nopatch
Patch1002:      CVE-2020-13143.nopatch
Patch1003:      CVE-2020-11884.nopatch

BuildRequires:  bc
BuildRequires:  kbd
BuildRequires:  kmod-devel
BuildRequires:  glib-devel
BuildRequires:  xerces-c-devel
BuildRequires:  libdnet-devel
BuildRequires:  libmspack-devel
BuildRequires:  pam-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  audit-devel
Requires:       filesystem kmod
Requires(post): coreutils
Requires(postun): coreutils
%define uname_r %{version}-%{release}

%description
The kernel package contains the Linux kernel.

%if 0%{?with_signed}
%package signed
Summary:        Production-signed Linux Kernel
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description signed
This package contains the Linux kernel package with kernel signed with the production key
%endif

%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Obsoletes:      linux-dev
Requires:       %{name} = %{version}-%{release}
Requires:       python3 gawk
%description devel
This package contains the Linux kernel dev files

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

%ifarch x86_64
%package oprofile
Summary:        Kernel driver for oprofile, a statistical profiler for Linux systems
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description oprofile
Kernel driver for oprofile, a statistical profiler for Linux systems
%endif

%package tools
Summary:        This package contains the 'perf' performance analysis tools for Linux kernel
Group:          System/Tools
Requires:       %{name} = %{version}
Requires:       audit
%description tools
This package contains the 'perf' performance analysis tools for Linux kernel.

%prep
%setup -q -n WSL2-Linux-Kernel-linux-msft-%{version}

%patch0 -p1

%build
make mrproper

%ifarch x86_64
cp %{SOURCE1} .config
arch="x86_64"
archdir="x86"
%endif

%ifarch aarch64
cp %{SOURCE2} .config
arch="arm64"
archdir="arm64"
%endif

sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{release}"/' .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1" KBUILD_BUILD_HOST="CBL-Mariner" ARCH=${arch} %{?_smp_mflags}
make -C tools perf

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
install -vdm 755 %{buildroot}/etc
install -vdm 700 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/linux-%{uname_r}
install -vdm 755 %{buildroot}/usr/src/linux-headers-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64
# Verify for build-id match
# We observe different IDs sometimes
# TODO: debug it
ID1=`readelf -n vmlinux | grep "Build ID"`
./scripts/extract-vmlinux arch/x86/boot/bzImage > extracted-vmlinux
ID2=`readelf -n extracted-vmlinux | grep "Build ID"`
if [ "$ID1" != "$ID2" ] ; then
        echo "Build IDs do not match"
        echo $ID1
        echo $ID2
        exit 1
fi
install -vm 600 arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
%endif

%ifarch aarch64
install -vm 600 arch/arm64/boot/Image %{buildroot}/boot/vmlinuz-%{uname_r}
%endif

# Restrict the permission on System.map-X file
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 600 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/linux-%{uname_r}
install -vm 644 vmlinux %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux

cat > %{buildroot}/boot/linux-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
mariner_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta crashkernel=128M
mariner_linux=vmlinuz-%{uname_r}
mariner_initrd=initrd.img-%{uname_r}
EOF
chmod 600 %{buildroot}/boot/linux-%{uname_r}.cfg

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "xen-scsifront xen-blkfront xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon cn"
EOF

#    Cleanup dangling symlinks
rm -rf %{buildroot}/lib/modules/%{uname_r}/source
rm -rf %{buildroot}/lib/modules/%{uname_r}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/linux-headers-%{uname_r}' copy
find arch/${archdir}/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/linux-headers-%{uname_r}' copy
find $(find arch/${archdir} -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/linux-headers-%{uname_r}' copy
find arch/${archdir}/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/linux-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}/usr/src/linux-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}/usr/src/linux-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}/usr/src/linux-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "/usr/src/linux-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%ifarch aarch64
cp arch/arm64/kernel/module.lds %{buildroot}/usr/src/linux-headers-%{uname_r}/arch/arm64/kernel/
%endif

# disable (JOBS=1) parallel build to fix this issue:
# fixdep: error opening depfile: ./.plugin_cfg80211.o.d: No such file or directory
# Linux version that was affected is 4.4.26
make -C tools JOBS=1 DESTDIR=%{buildroot} prefix=%{_prefix} perf_install

# Incorporate signed kernel binaries if enabled
%if 0%{?with_signed}
%ifarch x86_64
echo "Overwriting kernel binary with signed x86_64 kernel binary"
cp %{SOURCE100} %{buildroot}/boot/vmlinuz-%{uname_r}
%else
echo "Overwriting kernel binary with signed aarch64 kernel binary"
cp %{SOURCE101} %{buildroot}/boot/vmlinuz-%{uname_r}
%endif
%endif

%triggerin -- initramfs
mkdir -p %{_localstatedir}/lib/rpm-state/initramfs/pending
touch %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
echo "initrd generation of kernel %{uname_r} will be triggered later" >&2

%triggerun -- initramfs
rm -rf %{_localstatedir}/lib/rpm-state/initramfs/pending/%{uname_r}
rm -rf /boot/initrd.img-%{uname_r}
echo "initrd of kernel %{uname_r} removed" >&2

%postun
if [ ! -e /boot/mariner.cfg ]
then
     if [ `ls /boot/linux-*.cfg 1> /dev/null 2>&1` ]
     then
          list=`ls -tu /boot/linux-*.cfg | head -n1`
          test -n "$list" && ln -sf "$list" /boot/mariner.cfg
     fi
fi

%post
/sbin/depmod -a %{uname_r}
ln -sf linux-%{uname_r}.cfg /boot/mariner.cfg

%post drivers-sound
/sbin/depmod -a %{uname_r}

%ifarch x86_64
%post oprofile
/sbin/depmod -a %{uname_r}
%endif

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/linux-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
%exclude /lib/modules/%{uname_r}/build
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound
%ifarch x86_64
%exclude /lib/modules/%{uname_r}/kernel/arch/x86/oprofile/
%endif

%if 0%{?with_signed}
%files signed
%endif

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/linux-%{uname_r}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
/usr/src/linux-headers-%{uname_r}

%files drivers-sound
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/sound

%ifarch x86_64
%files oprofile
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/arch/x86/oprofile/
%endif

%files tools
%defattr(-,root,root)
/usr/libexec
%exclude %{_libdir}/debug
%ifarch x86_64
/usr/lib64/traceevent
%endif
%ifarch aarch64
/usr/lib/traceevent
%endif
%{_bindir}
/etc/bash_completion.d/*
/usr/share/perf-core/strace/groups/file
/usr/share/perf-core/strace/groups/string
/usr/share/doc/*
%{_libdir}/perf/examples/bpf/*
%{_libdir}/perf/include/bpf/*

%changelog
*   Mon Aug 17 2020 Chris Co <chrco@microsoft.com> 5.4.42-10
-   Enable BPF, PC104, userfaultfd, SLUB sysfs, SMC, XDP sockets monitoring configs
*   Fri Aug 07 2020 Mateusz Malisz <mamalisz@microsoft.com> 5.4.42-9
-   Add crashkernel=128M to the kernel cmdline
-   Update config to support kexec and kexec_file_load
*   Tue Aug 04 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 5.4.42-8
-   Updating "KBUILD_BUILD_VERSION" and "KBUILD_BUILD_HOST" with correct
    distribution name.
*   Wed Jul 22 2020 Chris Co <chrco@microsoft.com> 5.4.42-7
-   Address CVE-2020-8992, CVE-2020-12770, CVE-2020-13143, CVE-2020-11884
*   Fri Jul 17 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 5.4.42-6
-   Enable CONFIG_MLX5_CORE_IPOIB and CONFIG_INFINIBAND_IPOIB config flags
*   Fri Jul 17 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 5.4.42-5
-   Adding XDP config flag
*   Thu Jul 09 2020 Anand Muthurajan <anandm@microsoft.com> 5.4.42-4
-   Enable CONFIG_QED, CONFIG_QEDE, CONFIG_QED_SRIOV and CONFIG_QEDE_VXLAN flags
*   Wed Jun 24 2020 Chris Co <chrco@microsoft.com> 5.4.42-3
-   Regenerate input config files
*   Fri Jun 19 2020 Chris Co <chrco@microsoft.com> 5.4.42-2
-   Add kernel-secure subpackage and macros for adding offline signed kernels
*   Fri Jun 12 2020 Chris Co <chrco@microsoft.com> 5.4.42-1
-   Update source to 5.4.42
*   Thu Jun 11 2020 Chris Co <chrco@microsoft.com> 5.4.23-17
-   Enable PAGE_POISONING configs
-   Disable PROC_KCORE config
-   Enable RANDOM_TRUST_CPU config for x86_64
*   Fri Jun 05 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 5.4.23-16
-   Adding BPF config flags
*   Thu Jun 04 2020 Chris Co <chrco@microsoft.com> 5.4.23-15
-   Add config support for USB video class devices
*   Wed Jun 03 2020 Nicolas Ontiveros <niontive@microsoft.com> 5.4.23-14
-   Add CONFIG_CRYPTO_XTS=y to config.
*   Wed Jun 03 2020 Chris Co <chrco@microsoft.com> 5.4.23-13
-   Add patch to support CometLake e1000e ethernet
-   Remove drivers-gpu subpackage
-   Inline the initramfs trigger and postun source files
-   Remove rpi3 dtb and ls1012 dtb subpackages
*   Wed May 27 2020 Chris Co <chrco@microsoft.com> 5.4.23-12
-   Update arm64 security configs
-   Disable devmem in x86_64 config
*   Tue May 26 2020 Daniel Mihai <dmihai@microsoft.com> 5.4.23-11
-   Disabled Reliable Datagram Sockets protocol (CONFIG_RDS).
*   Fri May 22 2020 Emre Girgin <mrgirgin@microsoft.com> 5.4.23-10
-   Change /boot directory permissions to 600.
*   Thu May 21 2020 Chris Co <chrco@microsoft.com> 5.4.23-9
-   Update x86_64 security configs
*   Wed May 20 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 5.4.23-8
-   Adding InfiniBand config flags
*   Tue May 11 2020 Anand Muthurajan <anandm@microsoft.com> 5.4.23-7
-   Adding PPP config flags
*   Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 5.4.23-6
-   Renaming Linux-PAM to pam
*   Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 5.4.23-5
-   Renaming linux to kernel
*   Tue Apr 14 2020 Emre Girgin <mrgirgin@microsoft.com> 5.4.23-4
-   Remove linux-aws and linux-esx references.
-   Remove kat_build usage.
-   Remove ENA module.
*   Fri Apr 10 2020 Emre Girgin <mrgirgin@microsoft.com> 5.4.23-3
-   Remove xml-security-c dependency.
*   Wed Apr 08 2020 Nicolas Ontiveros <niontive@microsoft.com> 5.4.23-2
-   Remove toybox and only use coreutils for requires.
*   Tue Dec 10 2019 Chris Co <chrco@microsoft.com> 5.4.23-1
-   Update to Microsoft Linux Kernel 5.4.23
-   Remove patches
-   Update ENA module to 2.1.2 to work with Linux 5.4.23
-   Remove xr module
-   Remove Xen tmem module from dracut module list to fix initramfs creation
-   Add patch to fix missing trans_pgd header in aarch64 build
*   Fri Oct 11 2019 Henry Beberman <hebeberm@microsoft.com> 4.19.52-8
-   Enable Hyper-V TPM in config
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.19.52-7
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Jul 25 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-6
-   Fix postun scriplet.
*   Thu Jul 11 2019 Keerthana K <keerthanak@vmware.com> 4.19.52-5
-   Enable kernel configs necessary for BPF Compiler Collection (BCC).
*   Wed Jul 10 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-4
-   Deprecate linux-aws-tools in favor of linux-tools.
*   Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.52-3
-   Fix 9p vsock 16bit port issue.
*   Thu Jun 20 2019 Tapas Kundu <tkundu@vmware.com> 4.19.52-2
-   Enabled CONFIG_I2C_CHARDEV to support lm-sensors
*   Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.52-1
-   Update to version 4.19.52
-   Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12380, CVE-2019-12381,
-   CVE-2019-12382, CVE-2019-12378, CVE-2019-12455
*   Tue May 28 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.40-3
-   Change default I/O scheduler to 'deadline' to fix performance issue.
*   Tue May 14 2019 Keerthana K <keerthanak@vmware.com> 4.19.40-2
-   Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
-   mulitple kernels are installed and current linux kernel is removed.
*   Tue May 07 2019 Ajay Kaher <akaher@vmware.com> 4.19.40-1
-   Update to version 4.19.40
*   Thu Apr 11 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-3
-   Update config_aarch64 to fix ARM64 build.
*   Fri Mar 29 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-2
-   Fix CVE-2019-10125
*   Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.32-1
-   Update to version 4.19.32
*   Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.29-1
-   Update to version 4.19.29
*   Tue Mar 05 2019 Ajay Kaher <akaher@vmware.com> 4.19.26-1
-   Update to version 4.19.26
*   Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.15-3
-   Fix CVE-2019-8912
*   Thu Jan 24 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.15-2
-   Add WiFi (ath10k), sensors (i2c,spi), usb support for NXP LS1012A board.
*   Tue Jan 15 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.15-1
-   Update to version 4.19.15
*   Fri Jan 11 2019 Srinidhi Rao <srinidhir@vmware.com> 4.19.6-7
-   Add Network support for NXP LS1012A board.
*   Wed Jan 09 2019 Ankit Jain <ankitja@vmware.com> 4.19.6-6
-   Enable following for x86_64 and aarch64:
-    Enable Kernel Address Space Layout Randomization.
-    Enable CONFIG_SECURITY_NETWORK_XFRM
*   Fri Jan 04 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-5
-   Enable AppArmor by default.
*   Wed Jan 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.19.6-4
-   .config: added Compulab fitlet2 device drivers
-   .config_aarch64: added gpio sysfs support
-   renamed -sound to -drivers-sound
*   Tue Jan 01 2019 Ajay Kaher <akaher@vmware.com> 4.19.6-3
-   .config: Enable CONFIG_PCI_HYPERV driver
*   Wed Dec 19 2018 Srinidhi Rao <srinidhir@vmware.com> 4.19.6-2
-   Add NXP LS1012A support.
*   Mon Dec 10 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.6-1
-   Update to version 4.19.6
*   Fri Dec 07 2018 Alexey Makhalov <amakhalov@vmware.com> 4.19.1-3
-   .config: added qmi wwan module
*   Mon Nov 12 2018 Ajay Kaher <akaher@vmware.com> 4.19.1-2
-   Fix config_aarch64 for 4.19.1
*   Mon Nov 05 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.1-1
-   Update to version 4.19.1
*   Tue Oct 16 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.18.9-5
-   Change in config to enable drivers for zigbee and GPS
*   Fri Oct 12 2018 Ajay Kaher <akaher@vmware.com> 4.18.9-4
-   Enable LAN78xx for aarch64 rpi3
*   Fri Oct 5 2018 Ajay Kaher <akaher@vmware.com> 4.18.9-3
-   Fix config_aarch64 for 4.18.9
-   Add module.lds for aarch64
*   Wed Oct 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-2
-   Use updated steal time accounting patch.
-   .config: Enable CONFIG_CPU_ISOLATION and a few networking options
-   that got accidentally dropped in the last update.
*   Mon Oct 1 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.18.9-1
-   Update to version 4.18.9
*   Tue Sep 25 2018 Ajay Kaher <akaher@vmware.com> 4.14.67-2
-   Build hang (at make oldconfig) fix in config_aarch64
*   Wed Sep 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.67-1
-   Update to version 4.14.67
*   Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-7
-   Add rdrand-based RNG driver to enhance kernel entropy.
*   Sun Sep 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-6
-   Add full retpoline support by building with retpoline-enabled gcc.
*   Thu Aug 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.14.54-5
-   Apply out-of-tree patches needed for AppArmor.
*   Wed Aug 22 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.54-4
-   Fix overflow kernel panic in rsi driver.
-   .config: enable BT stack, enable GPIO sysfs.
-   Add Exar USB serial driver.
*   Fri Aug 17 2018 Ajay Kaher <akaher@vmware.com> 4.14.54-3
-   Enabled USB PCI in config_aarch64
-   Build hang (at make oldconfig) fix in config_aarch64
*   Thu Jul 19 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.54-2
-   .config: usb_serial_pl2303=m,wlan=y,can=m,gpio=y,pinctrl=y,iio=m
*   Mon Jul 09 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.14.54-1
-   Update to version 4.14.54
*   Fri Jan 26 2018 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-2
-   Added vchiq entry to rpi3 dts
-   Added dtb-rpi3 subpackage
*   Fri Dec 22 2017 Alexey Makhalov <amakhalov@vmware.com> 4.14.8-1
-   Version update
*   Wed Dec 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-4
-   KAT build support
*   Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-3
-   Aarch64 support
*   Tue Dec 05 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-2
-   Sign and compress modules after stripping. fips=1 requires signed modules
*   Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
-   Version update
*   Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
-   Version update
*   Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
-   Version update
*   Wed Oct 11 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-3
-   Add patch "KVM: Don't accept obviously wrong gsi values via
    KVM_IRQFD" to fix CVE-2017-1000252.
*   Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.53-2
-   Build hang (at make oldconfig) fix.
*   Thu Oct 05 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-1
-   Version update
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-3
-   Allow privileged CLONE_NEWUSER from nested user namespaces.
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-2
-   Fix CVE-2017-11472 (ACPICA: Namespace: fix operand cache leak)
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-1
-   Version update
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-2
-   Requires coreutils or toybox
*   Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-1
-   Fix CVE-2017-11600
*   Tue Aug 22 2017 Anish Swaminathan <anishs@vmware.com> 4.9.43-2
-   Add missing xen block drivers
*   Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.43-1
-   Version update
-   [feature] new sysctl option unprivileged_userns_clone
*   Wed Aug 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-2
-   Fix CVE-2017-7542
-   [bugfix] Added ccm,gcm,ghash,lzo crypto modules to avoid
    panic on modprobe tcrypt
*   Mon Aug 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-1
-   Version update
*   Fri Aug 04 2017 Bo Gan <ganb@vmware.com> 4.9.38-6
-   Fix initramfs triggers
*   Tue Aug 01 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-5
-   Allow some algorithms in FIPS mode
-   Reverts 284a0f6e87b0721e1be8bca419893902d9cf577a and backports
-   bcf741cb779283081db47853264cc94854e7ad83 in the kernel tree
-   Enable additional NF features
*   Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-4
-   Add patches in Hyperv codebase
*   Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-3
-   Add missing hyperv drivers
*   Thu Jul 20 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-2
-   Disable scheduler beef up patch
*   Tue Jul 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-1
-   Fix CVE-2017-11176 and CVE-2017-10911
*   Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-3
-   Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 4.9.34-2
-   Added obsolete for deprecated linux-dev package
*   Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
-   [feature] 9P FS security support
-   [feature] DM Delay target support
-   Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
*   Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
-   Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
-   [feature] IPV6 netfilter NAT table support
*   Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
-   Added ENA driver for AMI
-   Fix CVE-2017-7487 and CVE-2017-9059
*   Wed May 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.9.28-2
-   Enable IPVLAN module.
*   Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.28-1
-   Version update
*   Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.27-1
-   Version update
*   Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.26-1
-   Version update
-   Removed version suffix from config file name
*   Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 4.9.24-2
-   Support dynamic initrd generation
*   Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.24-1
-   Fix CVE-2017-6874 and CVE-2017-7618.
-   Fix audit-devel BuildRequires.
-   .config: build nvme and nvme-core in kernel.
*   Mon Mar 6 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-2
-   .config: NSX requirements for crypto and netfilter
*   Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
-   Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
*   Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
-   Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
-   .config: added CRYPTO_FIPS support.
*   Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
-   Update to linux-4.9.2 to fix CVE-2016-10088
-   Move linux-tools.spec to linux.spec as -tools subpackage
*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
-   BuildRequires Linux-PAM-devel
*   Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
-   Update to linux-4.9.0
-   Add paravirt stolen time accounting feature (from linux-esx),
    but disable it by default (no-vmw-sta cmdline parameter)
*   Thu Dec  8 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-3
-   net-packet-fix-race-condition-in-packet_set_ring.patch
    to fix CVE-2016-8655
*   Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-2
-   Expand `uname -r` with release number
-   Check for build-id matching
-   Added syscalls tracing support
-   Compress modules
*   Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-1
-   Update to linux-4.4.35
-   vfio-pci-fix-integer-overflows-bitmask-check.patch
    to fix CVE-2016-9083
*   Tue Nov 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-4
-   net-9p-vsock.patch
*   Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-3
-   tty-prevent-ldisc-drivers-from-re-using-stale-tty-fields.patch
    to fix CVE-2015-8964
*   Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-2
-   .config: add cgrup_hugetlb support
-   .config: add netfilter_xt_{set,target_ct} support
-   .config: add netfilter_xt_match_{cgroup,ipvs} support
*   Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-1
-   Update to linux-4.4.31
*   Fri Oct 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-1
-   Update to linux-4.4.26
*   Wed Oct 19 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-6
-   net-add-recursion-limit-to-GRO.patch
-   scsi-arcmsr-buffer-overflow-in-arcmsr_iop_message_xfer.patch
*   Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-5
-   ipip-properly-mark-ipip-GRO-packets-as-encapsulated.patch
-   tunnels-dont-apply-GRO-to-multiple-layers-of-encapsulation.patch
*   Mon Oct  3 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-4
-   Package vmlinux with PROGBITS sections in -debuginfo subpackage
*   Tue Sep 27 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-3
-   .config: CONFIG_IP_SET_HASH_{IPMARK,MAC}=m
*   Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-2
-   Add -release number for /boot/* files
-   Use initrd.img with version and release number
-   Rename -dev subpackage to -devel
*   Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
-   Update to linux-4.4.20
-   apparmor-fix-oops-validate-buffer-size-in-apparmor_setprocattr.patch
-   keys-fix-asn.1-indefinite-length-object-parsing.patch
*   Thu Aug 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-11
-   vmxnet3 patches to bumpup a version to 1.4.8.0
*   Wed Aug 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-10
-   Added VSOCK-Detach-QP-check-should-filter-out-non-matching-QPs.patch
-   .config: pmem hotplug + ACPI NFIT support
-   .config: enable EXPERT mode, disable UID16 syscalls
*   Thu Jul 07 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-9
-   .config: pmem + fs_dax support
*   Fri Jun 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-8
-   patch: e1000e-prevent-div-by-zero-if-TIMINCA-is-zero.patch
-   .config: disable rt group scheduling - not supported by systemd
*   Wed Jun 15 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-7
-   fixed the capitalization for - System.map
*   Thu May 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-6
-   patch: REVERT-sched-fair-Beef-up-wake_wide.patch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-5
-   GA - Bump release of all rpms
*   Mon May 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-4
-   Fixed generation of debug symbols for kernel modules & vmlinux.
*   Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> 4.4.8-3
-   Added patches to fix CVE-2016-3134, CVE-2016-3135
*   Wed May 18 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-2
-   Enabled CONFIG_UPROBES in config as needed by ktap
*   Wed May 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
-   Update to linux-4.4.8
-   Added net-Drivers-Vmxnet3-set-... patch
*   Tue May 03 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-27
-   Compile Intel GigE and VMXNET3 as part of kernel.
*   Thu Apr 28 2016 Nick Shi <nshi@vmware.com> 4.2.0-26
-   Compile cramfs.ko to allow mounting cramfs image
*   Tue Apr 12 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-25
-   Revert network interface renaming disable in kernel.
*   Tue Mar 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-24
-   Support kmsg dumping to vmware.log on panic
-   sunrpc: xs_bind uses ip_local_reserved_ports
*   Mon Mar 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-23
-   Enabled Regular stack protection in Linux kernel in config
*   Thu Mar 17 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-22
-   Restrict the permissions of the /boot/System.map-X file
*   Fri Mar 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-21
-   Patch: SUNRPC: Do not reuse srcport for TIME_WAIT socket.
*   Wed Mar 02 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-20
-   Patch: SUNRPC: Ensure that we wait for connections to complete
    before retrying
*   Fri Feb 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-19
-   Disable watchdog under VMware hypervisor.
*   Thu Feb 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-18
-   Added rpcsec_gss_krb5 and nfs_fscache
*   Mon Feb 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-17
-   Added sysctl param to control weighted_cpuload() behavior
*   Thu Feb 18 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.0-16
-   Disabling network renaming
*   Sun Feb 14 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-15
-   veth patch: don’t modify ip_summed
*   Thu Feb 11 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-14
-   Full tickless -> idle tickless + simple CPU time accounting
-   SLUB -> SLAB
-   Disable NUMA balancing
-   Disable stack protector
-   No build_forced no-CBs CPUs
-   Disable Expert configuration mode
-   Disable most of debug features from 'Kernel hacking'
*   Mon Feb 08 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-13
-   Double tcp_mem limits, patch is added.
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  4.2.0-12
-   Fixes for CVE-2015-7990/6937 and CVE-2015-8660.
*   Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 4.2.0-11
-   Revert CONFIG_HZ=250
*   Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-10
-   Fix for CVE-2016-0728
*   Wed Jan 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-9
-   CONFIG_HZ=250
*   Tue Jan 12 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-8
-   Remove rootfstype from the kernel parameter.
*   Mon Jan 04 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-7
-   Disabled all the tracing options in kernel config.
-   Disabled preempt.
-   Disabled sched autogroup.
*   Thu Dec 17 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-6
-   Enabled kprobe for systemtap & disabled dynamic function tracing in config
*   Fri Dec 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-5
-   Added oprofile kernel driver sub-package.
*   Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-4
-   Change the linux image directory.
*   Wed Nov 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-3
-   Added the build essential files in the dev sub-package.
*   Mon Nov 09 2015 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-2
-   Enable Geneve module support for generic kernel.
*   Fri Oct 23 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-1
-   Upgraded the generic linux kernel to version 4.2.0 & and updated timer handling to full tickless mode.
*   Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.9-5
-   Added driver support for frame buffer devices and ACPI
*   Wed Sep 2 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-4
-   Added mouse ps/2 module.
*   Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-3
-   Use photon.cfg as a symlink.
*   Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-2
-   Added environment file(photon.cfg) for grub.
*   Wed Aug 12 2015 Sharath George <sharathg@vmware.com> 4.0.9-1
-   Upgrading kernel version.
*   Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 3.19.2-5
-   Updated OVT to version 10.0.0.
-   Rename -gpu-drivers to -drivers-gpu in accordance to directory structure.
-   Added -sound package/
*   Tue Aug 11 2015 Anish Swaminathan<anishs@vmware.com> 3.19.2-4
-   Removed Requires dependencies.
*   Fri Jul 24 2015 Harish Udaiya Kumar <hudaiyakumar@gmail.com> 3.19.2-3
-   Updated the config file to include graphics drivers.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.13.3-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-   Initial build. First version
