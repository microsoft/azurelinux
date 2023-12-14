# Disable stripping - strip is trying to strip binaries (.img, .elf, etc.) built for different architectures.
%global __strip /bin/true
%global libfdt_version 1.6.0
%global libseccomp_version 2.4.0
%global libusbx_version 1.0.23
%global meson_version 0.58.2
%global usbredir_version 0.7.1
%global ipxe_version 1.20.1
%global excluded_targets moxie-softmmu
%global have_memlock_limits 0
%global need_qemu_kvm 0
%ifarch x86_64
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch aarch64
%global kvm_package   system-aarch64
%endif
%global modprobe_kvm_conf %{_sourcedir}/kvm.conf
%ifarch x86_64
    %global modprobe_kvm_conf %{_sourcedir}/kvm-x86.conf
%endif
%global tools_only 0
%global user_static 0
%global have_kvm 1
%global have_numactl 1
%global have_spice 0
%global have_xen 0
%global have_liburing 1
%global have_virgl 1
%global have_jack 0
%global have_sdl_image 0
%global have_fdt 1
%global have_opengl 1
%global have_usbredir 1
%global enable_werror 0
%global have_edk2 0
%global have_pmem 0
%ifarch x86_64
%global have_pmem 1
%endif
# All modules should be listed here.
%define have_block_rbd 1
%global have_block_gluster 0
%define have_block_nfs 1
%define have_librdma 1
%define have_libcacard 1
# LTO still has issues with qemu on armv7hl and aarch64
# https://bugzilla.redhat.com/show_bug.cgi?id=1952483
%global _lto_cflags %{nil}

# Needed until CBL-Mariner starts cross-compiling 'ipxe', 'seabios' and 'sgabios' for other architectures.
%ifarch x86_64
%global firmwaredirs "%{_datadir}/qemu-firmware:%{_datadir}/ipxe/qemu:%{_datadir}/seavgabios:%{_datadir}/seabios:%{_datadir}/sgabios"
%else
%global firmwaredirs "%{_datadir}/qemu-firmware"
%endif

%global qemudocdir %{_docdir}/%{name}
%define evr %{version}-%{release}
%define requires_block_curl Requires: %{name}-block-curl = %{evr}
%define requires_block_dmg Requires: %{name}-block-dmg = %{evr}
%if %{have_block_gluster}
%define requires_block_gluster Requires: %{name}-block-gluster = %{evr}
%define obsoletes_block_gluster %{nil}
%else
%define requires_block_gluster %{nil}
%define obsoletes_block_gluster Obsoletes: %{name}-block-gluster < %{evr}
%endif
%define requires_block_iscsi Requires: %{name}-block-iscsi = %{evr}
%if %{have_block_nfs}
%define requires_block_nfs Requires: %{name}-block-nfs = %{evr}
%define obsoletes_block_nfs %{nil}
%else
%define requires_block_nfs %{nil}
%define obsoletes_block_nfs Obsoletes: %{name}-block-nfs < %{evr}
%endif
%if %{have_block_rbd}
%define requires_block_rbd Requires: %{name}-block-rbd = %{evr}
%define obsoletes_block_rbd %{nil}
%else
%define requires_block_rbd %{nil}
%define obsoletes_block_rbd Obsoletes: %{name}-block-rbd < %{evr}
%endif
%define requires_audio_alsa Requires: %{name}-audio-alsa = %{evr}
%define requires_audio_oss Requires: %{name}-audio-oss = %{evr}
%if %{with brltty}
%define requires_char_baum Requires: %{name}-char-baum = %{evr}
%else
%define requires_char_baum %{nil}
%endif
%define requires_device_usb_host Requires: %{name}-device-usb-host = %{evr}
%define requires_device_usb_redirect Requires: %{name}-device-usb-redirect = %{evr}
%define requires_ui_curses Requires: %{name}-ui-curses = %{evr}
%define requires_ui_gtk Requires: %{name}-ui-gtk = %{evr}
%define requires_ui_egl_headless Requires: %{name}-ui-egl-headless = %{evr}
%define requires_ui_opengl Requires: %{name}-ui-opengl = %{evr}
%define requires_device_display_virtio_gpu Requires: %{name}-device-display-virtio-gpu = %{evr}
%define requires_device_display_virtio_gpu_gl Requires: %{name}-device-display-virtio-gpu-gl = %{evr}
%define requires_device_display_virtio_gpu_pci Requires: %{name}-device-display-virtio-gpu-pci = %{evr}
%define requires_device_display_virtio_gpu_pci_gl Requires: %{name}-device-display-virtio-gpu-pci-gl = %{evr}
%define requires_device_display_virtio_gpu_ccw Requires: %{name}-device-display-virtio-gpu-ccw = %{evr}
%define requires_device_display_virtio_vga Requires: %{name}-device-display-virtio-vga = %{evr}
%define requires_device_display_virtio_vga_gl Requires: %{name}-device-display-virtio-vga-gl = %{evr}
%if %{with libssh}
%define requires_block_ssh Requires: %{name}-block-ssh = %{evr}
%else
%define requires_block_ssh %{nil}
%endif
%if %{with pulseaudio}
%define pa_drv pa,
%define requires_audio_pa Requires: %{name}-audio-pa = %{evr}
%else
%define requires_audio_pa %{nil}
%endif
%if %{with sdl}
%define sdl_drv sdl,
%define requires_audio_sdl Requires: %{name}-audio-sdl = %{evr}
%define requires_ui_sdl Requires: %{name}-ui-sdl = %{evr}
%else
%define requires_audio_sdl %{nil}
%define requires_ui_sdl %{nil}
%endif
%if %{have_virgl}
%define requires_device_display_vhost_user_gpu Requires: %{name}-device-display-vhost-user-gpu = %{evr}
%else
%define requires_device_display_vhost_user_gpu %{nil}
%endif
%if %{have_jack}
%define jack_drv jack,
%define requires_audio_jack Requires: %{name}-audio-jack = %{evr}
%else
%define requires_audio_jack %{nil}
%endif
%if %{have_spice}
%define requires_ui_spice_app Requires: %{name}-ui-spice-app = %{evr}
%define requires_ui_spice_core Requires: %{name}-ui-spice-core = %{evr}
%define requires_device_display_qxl Requires: %{name}-device-display-qxl = %{evr}
%define requires_audio_spice Requires: %{name}-audio-spice = %{evr}
%define requires_char_spice Requires: %{name}-char-spice = %{evr}
%else
%define requires_ui_spice_app %{nil}
%define requires_ui_spice_core %{nil}
%define requires_device_display_qxl %{nil}
%define requires_audio_spice %{nil}
%define requires_char_spice %{nil}
%endif
%if %{have_libcacard}
%define requires_device_usb_smartcard Requires: %{name}-device-usb-smartcard = %{evr}
%else
%define requires_device_usb_smartcard %{nil}
%endif
%global requires_all_modules \
%requires_block_curl \
%requires_block_dmg \
%requires_block_gluster \
%requires_block_iscsi \
%requires_block_nfs \
%requires_block_rbd \
%requires_block_ssh \
%requires_audio_alsa \
%requires_audio_oss \
%requires_audio_pa \
%requires_audio_sdl \
%requires_audio_jack \
%requires_audio_spice \
%requires_ui_curses \
%requires_ui_gtk \
%requires_ui_sdl \
%requires_ui_egl_headless \
%requires_ui_opengl \
%requires_ui_spice_app \
%requires_ui_spice_core \
%requires_char_baum \
%requires_char_spice \
%requires_device_display_qxl \
%requires_device_display_vhost_user_gpu \
%requires_device_display_virtio_gpu \
%requires_device_display_virtio_gpu_gl \
%requires_device_display_virtio_gpu_pci \
%requires_device_display_virtio_gpu_pci_gl \
%requires_device_display_virtio_vga \
%requires_device_display_virtio_vga_gl \
%requires_device_usb_host \
%requires_device_usb_redirect \
%requires_device_usb_smartcard \
# Modules which can be conditionally built
%global obsoletes_some_modules \
%{obsoletes_block_gluster} \
%{obsoletes_block_rbd} \
%{obsoletes_block_rbd} \
Obsoletes: %{name}-system-lm32 <= %{version}-%{release} \
Obsoletes: %{name}-system-lm32-core <= %{version}-%{release} \
Obsoletes: %{name}-system-moxie <= %{version}-%{release} \
Obsoletes: %{name}-system-moxie-core <= %{version}-%{release} \
Obsoletes: %{name}-system-unicore32 <= %{version}-%{release} \
Obsoletes: %{name}-system-unicore32-core <= %{version}-%{release}
# Mariner builds all default targets except for Moxie, PPC, SPARC targets
# The Moxie exclusion is inherited from Fedora
# Both PPC and SPARC targets require packages that only build natively on the target platforms
# and Mariner cannot support that at the moment.
%bcond_with ppc_support
%bcond_with sparc_support
# Temporarily disabled features waiting for missing BRs:
%bcond_with brltty
%bcond_with capstone
%bcond_with libssh
%bcond_with pulseaudio
%bcond_with sdl
%if %{without ppc_support}
%global excluded_targets %{excluded_targets},ppc-softmmu,ppc64-softmmu,ppc-linux-user,ppc64-linux-user,ppc64le-linux-user
%endif
%if %{without sparc_support}
%global excluded_targets %{excluded_targets},sparc-softmmu,sparc64-softmmu,sparc-linux-user,sparc32plus-linux-user,sparc64-linux-user
%endif
Summary:        QEMU is a FAST! processor emulator
Name:           qemu
Version:        6.2.0
Release:        20%{?dist}
License:        BSD AND CC-BY AND GPLv2+ AND LGPLv2+ AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.qemu.org/
Source0:        https://download.qemu.org/%{name}-%{version}.tar.xz
Source10:       qemu-guest-agent.service
Source11:       99-qemu-guest-agent.rules
Source12:       bridge.conf
Source17:       qemu-ga.sysconfig
Source21:       95-kvm-memlock.conf
Source26:       vhost.conf
Source27:       kvm.conf
Source30:       kvm-s390x.conf
Source31:       kvm-x86.conf
Source36:       README.tests
Patch1:         fixing-glibc-struct-statx-usage.patch
Patch2:         disable_qos_test.patch
Patch3:         0001-sgx-stub-fix.patch
# Fix various crashes with virtiofsd on F36+
# https://bugzilla.redhat.com/2070066
Patch4:         0001-tools-virtiofsd-Add-rseq-syscall-to-the-seccomp-allo.patch
Patch5:         0002-virtiofsd-Do-not-support-blocking-flock.patch
# acpi: fix QEMU crash when started with SLIC table
# https://bugzilla.redhat.com/show_bug.cgi?id=2072303
Patch6:         0001-acpi-fix-QEMU-crash-when-started-with-SLIC-table.patch
Patch7:         0001-ebpf-replace-deprecated-bpf_program__set_socket_filt.patch
# CVE-2022-0358 is fixed in 7.0.0 by https://gitlab.com/qemu-project/qemu/-/commit/48302d4eb628ff0bea4d7e92cbf6b726410eb4c3
# From https://bugzilla.redhat.com/show_bug.cgi?id=2046202
Patch1000:      CVE-2022-0358.patch
# CVE-2021-20255 does not seem to have been fixed in a release yet
# From https://lists.gnu.org/archive/html/qemu-devel/2021-02/msg06098.html
Patch1001:      CVE-2021-20255.patch
# CVE-2022-1050 does not seem to have been fixed in a release yet
# From https://lists.nongnu.org/archive/html/qemu-devel/2022-03/msg05197.html
Patch1002:      CVE-2022-1050.patch
# CVE-2022-26354 is fixed in 7.0.0 by https://gitlab.com/qemu-project/qemu/-/commit/8d1b247f3748ac4078524130c6d7ae42b6140aaf
Patch1003:      CVE-2022-26354.patch
Patch1004:      CVE-2022-26353.patch
Patch1005:      CVE-2021-4206.patch
Patch1006:      CVE-2022-35414.patch
# CVE-2021-4158 is fixed in 7.0.0 by https://gitlab.com/qemu-project/qemu/-/commit/9bd6565ccee68f72d5012e24646e12a1c662827e
Patch1007:      CVE-2021-4158.patch
# CVE-2022-2962 will be fixed in 7.2.0 by https://gitlab.com/qemu-project/qemu/-/commit/36a894aeb64a2e02871016da1c37d4a4ca109182
Patch1008:      0001-removed-tulip.c-from-build-process-due-to-CVE-2022-2962.patch
# CVE-2022-4144 will be fixed in 7.2.0 by https://gitlab.com/qemu-project/qemu/-/commit/6dbbf055148c6f1b7d8a3251a65bd6f3d1e1f622
Patch1009:      CVE-2022-4144.patch
Patch1010:      CVE-2022-3872.patch
# CVE-2021-3929 is fixed in 7.0.0 by https://gitlab.com/qemu-project/qemu/-/commit/736b01642d85be832385
Patch1011:      CVE-2021-3929.patch
# CVE-2021-4207 is fixed in 7.0.0 by https://gitlab.com/qemu-project/qemu/-/commit/9569f5cb
Patch1012:      CVE-2021-4207.patch
Patch1013:      CVE-2022-3165.patch
# CVE-2021-3750 fix is not in a release yet
# https://gitlab.com/qemu-project/qemu/-/issues/541
Patch1014:      CVE-2021-3750.patch
Patch1015:      CVE-2022-36648.patch
Patch1016:      CVE-2023-3354.patch
Patch1017:      CVE-2023-2861.patch

# alsa audio output
BuildRequires:  alsa-lib-devel
# reading bzip2 compressed dmg images
BuildRequires:  bzip2-devel
BuildRequires:  cyrus-sasl-devel
# nvdimm dax
BuildRequires:  daxctl-devel
# qemu-pr-helper multipath support (requires libudev too)
BuildRequires:  device-mapper-multipath-devel
# fuse block device
BuildRequires:  fuse-devel
BuildRequires:  fuse3-devel
BuildRequires:  gcc
# GTK translations
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  gnutls-devel
# GTK frontend
BuildRequires:  gtk3-devel
# `hostname` used by test suite
BuildRequires:  hostname
BuildRequires:  libaio-devel
BuildRequires:  libattr-devel
BuildRequires:  libbpf-devel
%if %{have_libcacard}
# smartcard device
BuildRequires:  libcacard-devel
%endif
# For virtiofs
BuildRequires:  libcap-ng-devel
# For network block driver
BuildRequires:  libcurl-devel
BuildRequires:  libiscsi-devel
# VNC JPEG support
BuildRequires:  libjpeg-devel
# For VNC PNG support
BuildRequires:  libpng-devel
BuildRequires:  libselinux-devel
BuildRequires:  libseccomp-devel >= %{libseccomp_version}
BuildRequires:  libslirp-devel
# TLS test suite
BuildRequires:  libtasn1-devel
# qemu-ga
BuildRequires:  libudev-devel
BuildRequires:  libusbx-devel >= %{libusbx_version}
# parallels disk images require libxml2
BuildRequires:  libxml2-devel
# zstd compression support
BuildRequires:  libzstd-devel
# For compressed guest memory dumps
BuildRequires:  lzo-devel
BuildRequires:  make
BuildRequires:  meson >= %meson_version
# curses display backend
BuildRequires:  ncurses-devel
# qauth infrastructure
BuildRequires:  pam-devel
BuildRequires:  perl-Test-Harness
# Hard requirement for version >= 1.3
BuildRequires:  pixman-devel
BuildRequires:  pkg-config
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme
BuildRequires:  snappy-devel
BuildRequires:  systemd-devel
# We need both because the 'stap' binary is probed for by configure
BuildRequires:  systemtap
BuildRequires:  systemtap-sdt-devel
BuildRequires:  texinfo
BuildRequires:  vte291-devel
BuildRequires:  zlib-devel
# qemu-keymap
BuildRequires:  pkgconfig(xkbcommon)
%if %{have_usbredir}
BuildRequires:  usbredir-devel >= %{usbredir_version}
%endif
%if %{with libssh}
BuildRequires:  libssh-devel
%endif
%if %{have_block_rbd}
BuildRequires:  librbd-devel
%endif
# For rdma
%if %{have_librdma}
BuildRequires:  rdma-core-devel
%endif
%if %{have_fdt}
BuildRequires:  libfdt-devel >= %{libfdt_version}
%endif
# For NUMA memory binding
%if %{have_numactl}
BuildRequires:  numactl-devel
%endif
%if %{have_pmem}
BuildRequires:  libpmem-devel
%endif
%if %{have_opengl}
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libdrm)
%endif
%if %{with sdl}
# -display sdl support
BuildRequires:  SDL2-devel
%if %{have_sdl_image}
BuildRequires:  SDL2_image-devel
%endif
%endif
%if %{with pulseaudio}
# pulseaudio audio output
BuildRequires:  pulseaudio-libs-devel
%endif
%if %{have_block_nfs}
# NFS drive support
BuildRequires:  libnfs-devel
%endif
%if %{have_spice}
# spice graphics support
BuildRequires:  spice-protocol
BuildRequires:  spice-server-devel
%endif
%if %{with brltty}
# Braille device support
BuildRequires:  brlapi-devel
%endif
%if %{have_block_gluster}
# gluster block driver
BuildRequires:  glusterfs-api-devel
%endif
%if %{have_xen}
# Xen support
BuildRequires:  xen-devel
%endif
%if %{have_virgl}
# virgl 3d support
BuildRequires:  virglrenderer-devel
%endif
%if %{with capstone}
# preferred disassembler for TCG
BuildRequires:  capstone-devel
%endif
%if %{have_liburing}
# liburing support. Library isn't built for arm
BuildRequires:  liburing-devel
%endif
%if %{have_jack}
# jack audio driver
BuildRequires:  jack-audio-connection-kit-devel
%endif
Requires:       %{name}-img = %{version}-%{release}
Requires:       %{name}-system-aarch64 = %{version}-%{release}
Requires:       %{name}-system-alpha = %{version}-%{release}
Requires:       %{name}-system-arm = %{version}-%{release}
Requires:       %{name}-system-avr = %{version}-%{release}
Requires:       %{name}-system-cris = %{version}-%{release}
Requires:       %{name}-system-m68k = %{version}-%{release}
Requires:       %{name}-system-microblaze = %{version}-%{release}
Requires:       %{name}-system-mips = %{version}-%{release}
Requires:       %{name}-system-nios2 = %{version}-%{release}
Requires:       %{name}-system-or1k = %{version}-%{release}
Requires:       %{name}-system-riscv = %{version}-%{release}
Requires:       %{name}-system-rx = %{version}-%{release}
Requires:       %{name}-system-s390x = %{version}-%{release}
Requires:       %{name}-system-sh4 = %{version}-%{release}
Requires:       %{name}-system-tricore = %{version}-%{release}
Requires:       %{name}-system-xtensa = %{version}-%{release}
Requires:       %{name}-tools = %{version}-%{release}
Requires:       vhostuser-backend(fs)
# Requires for the 'qemu' metapackage
Requires:       %{name}-user = %{version}-%{release}
Requires:       qemu-pr-helper = %{version}-%{release}
%if %{with ppc_support}
Requires:       %{name}-system-ppc = %{version}-%{release}
%endif
%if %{with sparc_support}
Requires:       %{name}-system-sparc = %{version}-%{release}
%endif
%ifarch x86_64
Requires:       %{name}-system-x86 = %{version}-%{release}
%endif

%description
%{name} is an open source virtualizer that provides hardware
emulation for the KVM hypervisor. %{name} acts as a virtual
machine monitor together with the KVM kernel modules, and emulates the
hardware for a full system such as a PC and its associated peripherals.

%package        common
Summary:        QEMU common files needed by all QEMU targets
%ifarch x86_64
Requires:       ipxe >= %{ipxe_version}
%endif
Requires(post): %{_bindir}/getent
Requires(post): %{_sbindir}/groupadd
Requires(post): %{_sbindir}/useradd
Requires(post): systemd-units
Requires(postun): systemd-units
Requires(preun): systemd-units
%{obsoletes_some_modules}

%description common
%{name} is an open source virtualizer that provides hardware emulation for
the KVM hypervisor.

This package provides documentation and auxiliary programs used with %{name}.

%package        docs
Summary:        %{name} documentation

%description docs
%{name}-docs provides documentation files regarding %{name}.

%package -n     qemu-img
Summary:        QEMU command line tool for manipulating disk images

%description -n qemu-img
This package provides a command line tool for manipulating disk images.

%package -n     qemu-guest-agent
Summary:        QEMU guest agent
Requires(post): systemd-units
Requires(postun): systemd-units
Requires(preun): systemd-units

%description -n qemu-guest-agent
%{name} is an open source virtualizer that provides hardware emulation for
the KVM hypervisor.

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.

%package        tools
Summary:        %{name} support tools

%description tools
%{name}-tools provides various tools related to %{name} usage.

%package -n     qemu-pr-helper
Summary:        qemu-pr-helper utility for %{name}

%description -n qemu-pr-helper
This package provides the qemu-pr-helper utility that is required for certain
SCSI features.

%package -n     qemu-virtiofsd
Summary:        QEMU virtio-fs shared file system daemon
Provides:       vhostuser-backend(fs)
# qemu-common provided %%{_libexecdir}/virtiofsd prior to 6.2.0
Obsoletes:      %{name}-common < 6.2.0

%description -n qemu-virtiofsd
This package provides virtiofsd daemon. This program is a vhost-user backend
that implements the virtio-fs device that is used for sharing a host directory
tree with a guest.

%package        tests
%define testsdir %{_libdir}/%{name}/tests-src
Summary:        tests for the %{name} package
Requires:       %{name} = %{version}-%{release}

%description tests
The %{name}-tests rpm contains tests that can be used to verify
the functionality of the installed %{name} package

Install this package if you want access to the avocado_qemu
tests, or qemu-iotests.

%package        block-curl
Summary:        QEMU CURL block driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description block-curl
This package provides the additional CURL block driver for QEMU.

Install this package if you want to access remote disks over
http, https, ftp and other transports provided by the CURL library.

%package        block-iscsi
Summary:        QEMU iSCSI block driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description block-iscsi
This package provides the additional iSCSI block driver for QEMU.

Install this package if you want to access iSCSI volumes.

%if %{have_block_rbd}
%package        block-rbd
Summary:        QEMU Ceph/RBD block driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description block-rbd
This package provides the additional Ceph/RBD block driver for QEMU.

Install this package if you want to access remote Ceph volumes
using the rbd protocol.
%endif

%if %{with libssh}
%package        block-ssh
Summary:        QEMU SSH block driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description block-ssh
This package provides the additional SSH block driver for QEMU.

Install this package if you want to access remote disks using
the Secure Shell (SSH) protocol.
%endif

%if %{have_opengl}
%package        ui-opengl
Summary:        QEMU opengl support
Requires:       %{name}-common%{?_isa} = %{version}-%{release}
Requires:       mesa-dri-drivers
Requires:       mesa-libEGL
Requires:       mesa-libGL

%description ui-opengl
This package provides opengl support.
%endif

%package        block-dmg
Summary:        QEMU block driver for DMG disk images
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description block-dmg
This package provides the additional DMG block driver for QEMU.

Install this package if you want to open '.dmg' files.

%if %{have_block_gluster}
%package        block-gluster
Summary:        QEMU Gluster block driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description block-gluster
This package provides the additional Gluster block driver for QEMU.

Install this package if you want to access remote Gluster storage.
%endif


%if %{have_block_nfs}
%package        block-nfs
Summary:        QEMU NFS block driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description block-nfs
This package provides the additional NFS block driver for QEMU.

Install this package if you want to access remote NFS storage.
%endif


%package        audio-alsa
Summary:        QEMU ALSA audio driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description audio-alsa
This package provides the additional ALSA audio driver for QEMU.

%package        audio-oss
Summary:        QEMU OSS audio driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description audio-oss
This package provides the additional OSS audio driver for QEMU.

%if %{with pulseaudio}
%package        audio-pa
Summary:        QEMU PulseAudio audio driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description audio-pa
This package provides the additional PulseAudi audio driver for QEMU.
%endif

%if %{with sdl}
%package        audio-sdl
Summary:        QEMU SDL audio driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description audio-sdl
This package provides the additional SDL audio driver for QEMU.
%endif

%if %{have_jack}
%package        audio-jack
Summary:        QEMU Jack audio driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description audio-jack
This package provides the additional Jack audio driver for QEMU.
%endif


%package        ui-curses
Summary:        QEMU curses UI driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description ui-curses
This package provides the additional curses UI for QEMU.

%package        ui-gtk
Summary:        QEMU GTK UI driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}
Requires:       %{name}-ui-opengl%{?_isa} = %{version}-%{release}

%description ui-gtk
This package provides the additional GTK UI for QEMU.

%if %{with sdl}
%package        ui-sdl
Summary:        QEMU SDL UI driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}
Requires:       %{name}-ui-opengl%{?_isa} = %{version}-%{release}

%description ui-sdl
This package provides the additional SDL UI for QEMU.
%endif

%package        ui-egl-headless
Summary:        QEMU EGL headless driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}
Requires:       %{name}-ui-opengl%{?_isa} = %{version}-%{release}

%description ui-egl-headless
This package provides the additional egl-headless UI for QEMU.

%if %{with brltty}
%package        char-baum
Summary:        QEMU Baum chardev driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description char-baum
This package provides the Baum chardev driver for QEMU.
%endif


%package        device-display-virtio-gpu
Summary:        QEMU virtio-gpu display device
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description device-display-virtio-gpu
This package provides the virtio-gpu display device for QEMU.

%package        device-display-virtio-gpu-gl
Summary:        QEMU virtio-gpu-gl display device
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description device-display-virtio-gpu-gl
This package provides the virtio-gpu-gl display device for QEMU.

%package        device-display-virtio-gpu-pci
Summary:        QEMU virtio-gpu-pci display device
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description device-display-virtio-gpu-pci
This package provides the virtio-gpu-pci display device for QEMU.

%package        device-display-virtio-gpu-pci-gl
Summary:        QEMU virtio-gpu-pci-gl display device
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description device-display-virtio-gpu-pci-gl
This package provides the virtio-gpu-pci-gl display device for QEMU.

%package        device-display-virtio-gpu-ccw
Summary:        QEMU virtio-gpu-ccw display device
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description device-display-virtio-gpu-ccw
This package provides the virtio-gpu-ccw display device for QEMU.

%package        device-display-virtio-vga
Summary:        QEMU virtio-vga display device
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description device-display-virtio-vga
This package provides the virtio-vga display device for QEMU.

%package        device-display-virtio-vga-gl
Summary:        QEMU virtio-vga-gl display device
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description device-display-virtio-vga-gl
This package provides the virtio-vga-gl display device for QEMU.

%package        device-usb-host
Summary:        QEMU usb host device
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description device-usb-host
This package provides the USB pass through driver for QEMU.

%package        device-usb-redirect
Summary:        QEMU usbredir device
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description device-usb-redirect
This package provides the usbredir device for QEMU.

%if %{have_libcacard}
%package        device-usb-smartcard
Summary:        QEMU USB smartcard device
Requires:       %{name}-common%{?_isa} = %{version}-%{release}
%endif

%description device-usb-smartcard
This package provides the USB smartcard device for QEMU.

%if %{have_virgl}
%package        device-display-vhost-user-gpu
Summary:        QEMU QXL display device
Requires:       %{name}-common%{?_isa} = %{version}-%{release}

%description device-display-vhost-user-gpu
This package provides the vhost-user-gpu display device for QEMU.
%endif

%if %{have_spice}
%package        ui-spice-core
Summary:        QEMU spice-core UI driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}
Requires:       %{name}-ui-opengl%{?_isa} = %{version}-%{release}

%description ui-spice-core
This package provides the additional spice-core UI for QEMU.

%package        ui-spice-app
Summary:        QEMU spice-app UI driver
Requires:       %{name}-char-spice%{?_isa} = %{version}-%{release}
Requires:       %{name}-common%{?_isa} = %{version}-%{release}
Requires:       %{name}-ui-spice-core%{?_isa} = %{version}-%{release}

%description ui-spice-app
This package provides the additional spice-app UI for QEMU.

%package        device-display-qxl
Summary:        QEMU QXL display device
Requires:       %{name}-common%{?_isa} = %{version}-%{release}
Requires:       %{name}-ui-spice-core%{?_isa} = %{version}-%{release}

%description device-display-qxl
This package provides the QXL display device for QEMU.

%package        char-spice
Summary:        QEMU spice chardev driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}
Requires:       %{name}-ui-spice-core%{?_isa} = %{version}-%{release}

%description char-spice
This package provides the spice chardev driver for QEMU.

%package        audio-spice
Summary:        QEMU spice audio driver
Requires:       %{name}-common%{?_isa} = %{version}-%{release}
Requires:       %{name}-ui-spice-core%{?_isa} = %{version}-%{release}

%description audio-spice
This package provides the spice audio driver for QEMU.
%endif


%if %{have_kvm}
%package        kvm
Summary:        QEMU metapackage for KVM support
Requires:       qemu-%{kvm_package} = %{version}-%{release}

%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86

%package        kvm-core
Summary:        QEMU metapackage for KVM support
Requires:       qemu-%{kvm_package}-core = %{version}-%{release}

%description kvm-core
This is a meta-package that provides a qemu-system-<arch>-core package
for native architectures where kvm can be enabled. For example, in an
x86 system, this will install qemu-system-x86-core
%endif

%package        user
Summary:        QEMU user mode emulation of qemu targets
Requires:       %{name}-common = %{version}-%{release}

%description user
This package provides the user mode emulation of qemu targets

%package        user-binfmt
Summary:        QEMU user mode emulation of qemu targets
Requires:       %{name}-user = %{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units

%description user-binfmt
This package provides the user mode emulation of qemu targets

%package        ipxe
Summary:        PXE and EFI ROM images for qemu
Requires:       %{name}-common = %{version}-%{release}

%description ipxe
This package provides PXE and EFI ROM images for qemu

%package        system-aarch64
Summary:        QEMU system emulator for AArch64
Requires:       %{name}-system-aarch64-core = %{version}-%{release}
%requires_all_modules

%description system-aarch64
This package provides the QEMU system emulator for AArch64.

%package        system-aarch64-core
Summary:        QEMU system emulator for AArch64
Requires:       %{name}-common = %{version}-%{release}
%if %{have_edk2}
Requires:       edk2-aarch64
%endif
Requires:       %{name}-ipxe = %{version}-%{release}

%description system-aarch64-core
This package provides the QEMU system emulator for AArch64.

# Needed until CBL-Mariner starts cross-compiling 'ipxe', 'seabios' and 'sgabios' for other architectures.
%ifarch x86_64
%package        system-x86
Summary:        QEMU system emulator for x86
Requires:       %{name}-system-x86-core = %{version}-%{release}
%requires_all_modules

%description system-x86
This package provides the QEMU system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.

%package        system-x86-core
Summary:        QEMU system emulator for x86
Requires:       %{name}-common = %{version}-%{release}
Requires:       seabios-bin
Requires:       seavgabios-bin
Requires:       sgabios-bin
%if %{have_edk2}
Requires:       edk2-ovmf
%endif
Requires:       %{name}-ipxe = %{version}-%{release}

%description system-x86-core
This package provides the QEMU system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.
%endif

%package        system-alpha
Summary:        QEMU system emulator for Alpha
Requires:       %{name}-system-alpha-core = %{version}-%{release}
%requires_all_modules

%description system-alpha
This package provides the QEMU system emulator for Alpha systems.

%package        system-alpha-core
Summary:        QEMU system emulator for Alpha
Requires:       %{name}-common = %{version}-%{release}

%description system-alpha-core
This package provides the QEMU system emulator for Alpha systems.


%package        system-arm
Summary:        QEMU system emulator for ARM
Requires:       %{name}-system-arm-core = %{version}-%{release}
%requires_all_modules

%description system-arm
This package provides the QEMU system emulator for ARM systems.

%package        system-arm-core
Summary:        QEMU system emulator for ARM
Requires:       %{name}-common = %{version}-%{release}
%if %{have_edk2}
Requires: edk2-arm
%endif

%description system-arm-core
This package provides the QEMU system emulator for ARM boards.


%package        system-avr
Summary:        QEMU system emulator for AVR
Requires:       %{name}-system-avr-core = %{version}-%{release}
%requires_all_modules

%description system-avr
This package provides the QEMU system emulator for AVR systems.

%package        system-avr-core
Summary:        QEMU system emulator for AVR
Requires:       %{name}-common = %{version}-%{release}

%description system-avr-core
This package provides the QEMU system emulator for AVR systems.


%package        system-cris
Summary:        QEMU system emulator for CRIS
Requires:       %{name}-system-cris-core = %{version}-%{release}
%requires_all_modules

%description system-cris
This package provides the system emulator for CRIS systems.

%package        system-cris-core
Summary:        QEMU system emulator for CRIS
Requires:       %{name}-common = %{version}-%{release}

%description system-cris-core
This package provides the system emulator for CRIS boards.


%package        system-hppa
Summary:        QEMU system emulator for HPPA
Requires:       %{name}-system-hppa-core = %{version}-%{release}
%requires_all_modules

%description system-hppa
This package provides the QEMU system emulator for HPPA.

%package        system-hppa-core
Summary:        QEMU system emulator for hppa
Requires:       %{name}-common = %{version}-%{release}

%description system-hppa-core
This package provides the QEMU system emulator for HPPA.


%package        system-m68k
Summary:        QEMU system emulator for ColdFire (m68k)
Requires:       %{name}-system-m68k-core = %{version}-%{release}
%requires_all_modules

%description system-m68k
This package provides the QEMU system emulator for ColdFire boards.

%package        system-m68k-core
Summary:        QEMU system emulator for ColdFire (m68k)
Requires:       %{name}-common = %{version}-%{release}

%description system-m68k-core
This package provides the QEMU system emulator for ColdFire boards.


%package        system-microblaze
Summary:        QEMU system emulator for Microblaze
Requires:       %{name}-system-microblaze-core = %{version}-%{release}
%requires_all_modules

%description system-microblaze
This package provides the QEMU system emulator for Microblaze boards.

%package        system-microblaze-core
Summary:        QEMU system emulator for Microblaze
Requires:       %{name}-common = %{version}-%{release}

%description system-microblaze-core
This package provides the QEMU system emulator for Microblaze boards.


%package        system-mips
Summary:        QEMU system emulator for MIPS
Requires:       %{name}-system-mips-core = %{version}-%{release}
%requires_all_modules

%description system-mips
This package provides the QEMU system emulator for MIPS systems.

%package        system-mips-core
Summary:        QEMU system emulator for MIPS
Requires:       %{name}-common = %{version}-%{release}

%description system-mips-core
This package provides the QEMU system emulator for MIPS systems.


%package        system-nios2
Summary:        QEMU system emulator for nios2
Requires:       %{name}-system-nios2-core = %{version}-%{release}
%requires_all_modules

%description system-nios2
This package provides the QEMU system emulator for NIOS2.

%package        system-nios2-core
Summary:        QEMU system emulator for nios2
Requires:       %{name}-common = %{version}-%{release}

%description system-nios2-core
This package provides the QEMU system emulator for NIOS2.


%package        system-or1k
Summary:        QEMU system emulator for OpenRisc32
Requires:       %{name}-system-or1k-core = %{version}-%{release}
%requires_all_modules

%description system-or1k
This package provides the QEMU system emulator for OpenRisc32 boards.

%package        system-or1k-core
Summary:        QEMU system emulator for OpenRisc32
Requires:       %{name}-common = %{version}-%{release}

%description system-or1k-core
This package provides the QEMU system emulator for OpenRisc32 boards.

%if %{with ppc_support}
%package        system-ppc
Summary:        QEMU system emulator for PPC
Requires:       %{name}-system-ppc-core = %{version}-%{release}
%requires_all_modules

%description system-ppc
This package provides the QEMU system emulator for PPC and PPC64 systems.

%package        system-ppc-core
Summary:        QEMU system emulator for PPC
Requires:       %{name}-common = %{version}-%{release}
Requires:       SLOF
Requires:       openbios
Requires:       seavgabios-bin

%description system-ppc-core
This package provides the QEMU system emulator for PPC and PPC64 systems.
%endif


%package        system-riscv
Summary:        QEMU system emulator for RISC-V
Requires:       %{name}-system-riscv-core = %{version}-%{release}
%requires_all_modules

%description system-riscv
This package provides the QEMU system emulator for RISC-V systems.

%package        system-riscv-core
Summary:        QEMU system emulator for RISC-V
Requires:       %{name}-common = %{version}-%{release}

%description system-riscv-core
This package provides the QEMU system emulator for RISC-V systems.


%package        system-rx
Summary:        QEMU system emulator for RX
Requires:       %{name}-system-rx-core = %{version}-%{release}
%requires_all_modules

%description system-rx
This package provides the QEMU system emulator for RX systems.

%package        system-rx-core
Summary:        QEMU system emulator for RX
Requires:       %{name}-common = %{version}-%{release}

%description system-rx-core
This package provides the QEMU system emulator for RX systems.


%package        system-s390x
Summary:        QEMU system emulator for S390
Requires:       %{name}-system-s390x-core = %{version}-%{release}
%requires_all_modules

%description system-s390x
This package provides the QEMU system emulator for S390 systems.

%package        system-s390x-core
Summary:        QEMU system emulator for S390
Requires:       %{name}-common = %{version}-%{release}

%description system-s390x-core
This package provides the QEMU system emulator for S390 systems.


%package        system-sh4
Summary:        QEMU system emulator for SH4
Requires:       %{name}-system-sh4-core = %{version}-%{release}
%requires_all_modules

%description system-sh4
This package provides the QEMU system emulator for SH4 boards.

%package        system-sh4-core
Summary:        QEMU system emulator for SH4
Requires:       %{name}-common = %{version}-%{release}

%description system-sh4-core
This package provides the QEMU system emulator for SH4 boards.

%if %{with sparc_support}
%package        system-sparc
Summary:        QEMU system emulator for SPARC
Requires:       %{name}-system-sparc-core = %{version}-%{release}
%requires_all_modules

%description system-sparc
This package provides the QEMU system emulator for SPARC and SPARC64 systems.

%package        system-sparc-core
Summary:        QEMU system emulator for SPARC
Requires:       %{name}-common = %{version}-%{release}
Requires:       openbios

%description system-sparc-core
This package provides the QEMU system emulator for SPARC and SPARC64 systems.
%endif


%package        system-tricore
Summary:        QEMU system emulator for tricore
Requires:       %{name}-system-tricore-core = %{version}-%{release}
%requires_all_modules

%description system-tricore
This package provides the QEMU system emulator for Tricore.

%package        system-tricore-core
Summary:        QEMU system emulator for tricore
Requires:       %{name}-common = %{version}-%{release}

%description system-tricore-core
This package provides the QEMU system emulator for Tricore.


%package        system-xtensa
Summary:        QEMU system emulator for Xtensa
Requires:       %{name}-system-xtensa-core = %{version}-%{release}
%requires_all_modules

%description system-xtensa
This package provides the QEMU system emulator for Xtensa boards.

%package        system-xtensa-core
Summary:        QEMU system emulator for Xtensa
Requires:       %{name}-common = %{version}-%{release}

%description system-xtensa-core
This package provides the QEMU system emulator for Xtensa boards.

%prep
%setup -q -n qemu-%{version}%{?rcstr}
%autopatch -p1

%global qemu_kvm_build qemu_kvm_build
mkdir -p %{qemu_kvm_build}

%build
%define disable_everything         \\\
  --audio-drv-list=                \\\
  --disable-attr                   \\\
  --disable-auth-pam               \\\
  --disable-avx2                   \\\
  --disable-avx512f                \\\
  --disable-block-drv-whitelist-in-tools \\\
  --disable-bpf                    \\\
  --disable-bochs                  \\\
  --disable-brlapi                 \\\
  --disable-bsd-user               \\\
  --disable-bzip2                  \\\
  --disable-cap-ng                 \\\
  --disable-capstone               \\\
  --disable-cfi                    \\\
  --disable-cfi-debug              \\\
  --disable-cloop                  \\\
  --disable-cocoa                  \\\
  --disable-coroutine-pool         \\\
  --disable-crypto-afalg           \\\
  --disable-curl                   \\\
  --disable-curses                 \\\
  --disable-debug-info             \\\
  --disable-debug-mutex            \\\
  --disable-debug-tcg              \\\
  --disable-dmg                    \\\
  --disable-docs                   \\\
  --disable-fdt                    \\\
  --disable-fuse                   \\\
  --disable-fuse-lseek             \\\
  --disable-gcrypt                 \\\
  --disable-gio                    \\\
  --disable-glusterfs              \\\
  --disable-gnutls                 \\\
  --disable-gtk                    \\\
  --disable-guest-agent            \\\
  --disable-guest-agent-msi        \\\
  --disable-hax                    \\\
  --disable-hvf                    \\\
  --disable-iconv                  \\\
  --disable-kvm                    \\\
  --disable-libdaxctl              \\\
  --disable-libiscsi               \\\
  --disable-libnfs                 \\\
  --disable-libpmem                \\\
  --disable-libssh                 \\\
  --disable-libudev                \\\
  --disable-libusb                 \\\
  --disable-libxml2                \\\
  --disable-linux-aio              \\\
  --disable-linux-io-uring         \\\
  --disable-linux-user             \\\
  --disable-live-block-migration   \\\
  --disable-lto                    \\\
  --disable-lzfse                  \\\
  --disable-lzo                    \\\
  --disable-malloc-trim            \\\
  --disable-membarrier             \\\
  --disable-modules                \\\
  --disable-module-upgrades        \\\
  --disable-mpath                  \\\
  --disable-multiprocess           \\\
  --disable-netmap                 \\\
  --disable-nettle                 \\\
  --disable-numa                   \\\
  --disable-opengl                 \\\
  --disable-parallels              \\\
  --disable-pie                    \\\
  --disable-pvrdma                 \\\
  --disable-qcow1                  \\\
  --disable-qed                    \\\
  --disable-qom-cast-debug         \\\
  --disable-rbd                    \\\
  --disable-rdma                   \\\
  --disable-replication            \\\
  --disable-rng-none               \\\
  --disable-safe-stack             \\\
  --disable-sanitizers             \\\
  --disable-sdl                    \\\
  --disable-sdl-image              \\\
  --disable-seccomp                \\\
  --disable-slirp                  \\\
  --disable-slirp-smbd             \\\
  --disable-smartcard              \\\
  --disable-snappy                 \\\
  --disable-sparse                 \\\
  --disable-spice                  \\\
  --disable-spice-protocol         \\\
  --disable-strip                  \\\
  --disable-system                 \\\
  --disable-tcg                    \\\
  --disable-tools                  \\\
  --disable-tpm                    \\\
  --disable-u2f                    \\\
  --disable-usb-redir              \\\
  --disable-user                   \\\
  --disable-vde                    \\\
  --disable-vdi                    \\\
  --disable-vhost-crypto           \\\
  --disable-vhost-kernel           \\\
  --disable-vhost-net              \\\
  --disable-vhost-scsi             \\\
  --disable-vhost-user             \\\
  --disable-vhost-user-blk-server  \\\
  --disable-vhost-vdpa             \\\
  --disable-vhost-vsock            \\\
  --disable-virglrenderer          \\\
  --disable-virtfs                 \\\
  --disable-virtiofsd              \\\
  --disable-vnc                    \\\
  --disable-vnc-jpeg               \\\
  --disable-vnc-png                \\\
  --disable-vnc-sasl               \\\
  --disable-vte                    \\\
  --disable-vvfat                  \\\
  --disable-werror                 \\\
  --disable-whpx                   \\\
  --disable-xen                    \\\
  --disable-xen-pci-passthrough    \\\
  --disable-xfsctl                 \\\
  --disable-xkbcommon              \\\
  --disable-zstd                   \\\
  --with-git-submodules=ignore     \\\
  --without-default-devices

run_configure() {
    ../configure  \
        --cc=gcc \
        --cxx=/bin/false \
        --prefix="%{_prefix}" \
        --libdir="%{_libdir}" \
        --datadir="%{_datadir}" \
        --sysconfdir="%{_sysconfdir}" \
        --interp-prefix=%{_prefix}/qemu-%{M} \
        --localstatedir="%{_localstatedir}" \
        --docdir="%{_docdir}" \
        --libexecdir="%{_libexecdir}" \
        --extra-ldflags="%{build_ldflags}" \
        --extra-cflags="%{optflags}" \
        --with-pkgversion="%{name}-%{version}-%{release}" \
        --with-suffix="%{name}" \
        --firmwarepath="%{firmwaredirs}" \
        --meson="%{__meson}" \
        --enable-trace-backends=dtrace \
        --with-coroutine=ucontext \
        --with-git=git \
        --tls-priority=@QEMU,SYSTEM \
        %{disable_everything} \
        "$@"

    echo "config-host.mak contents:"
    echo "==="
    cat config-host.mak
    echo "==="
}


pushd %{qemu_kvm_build}
run_configure \
%if %{defined target_list}
  --target-list="%{target_list}" \
%endif
%if %{defined block_drivers_rw_list}
  --block-drv-rw-whitelist=%{block_drivers_rw_list} \
%endif
%if %{defined block_drivers_ro_list}
  --block-drv-ro-whitelist=%{block_drivers_ro_list} \
%endif
  --enable-attr \
%ifarch %{ix86} x86_64
  --enable-avx2 \
%endif
  --enable-bpf \
  --enable-cap-ng \
%if %{with capstone}
  --enable-capstone \
%endif
  --enable-coroutine-pool \
  --enable-curl \
  --enable-debug-info \
  --enable-docs \
%if %{have_fdt}
  --enable-fdt=system \
%endif
  --enable-gnutls \
  --enable-guest-agent \
  --enable-iconv \
  --enable-kvm \
  --enable-libiscsi \
%if %{have_pmem}
  --enable-libpmem \
%endif
%if %{with libssh}
  --enable-libssh \
%endif
  --enable-libusb \
  --enable-libudev \
  --enable-linux-aio \
%if "%{_lto_cflags}" != "%{nil}"
  --enable-lto \
%endif
  --enable-lzo \
  --enable-malloc-trim \
  --enable-modules \
  --enable-mpath \
%if %{have_numactl}
  --enable-numa \
%endif
%if %{have_opengl}
  --enable-opengl \
%endif
  --enable-pie \
%if %{have_block_rbd}
  --enable-rbd \
%endif
%if %{have_librdma}
  --enable-rdma \
%endif
  --enable-seccomp \
  --enable-slirp=system \
  --enable-slirp-smbd \
  --enable-snappy \
  --enable-system \
  --enable-tcg \
  --enable-tools \
  --enable-tpm \
%if %{have_usbredir}
  --enable-usb-redir \
%endif
  --enable-virtiofsd \
  --enable-vhost-kernel \
  --enable-vhost-net \
  --enable-vhost-user \
  --enable-vhost-user-blk-server \
  --enable-vhost-vdpa \
  --enable-vhost-vsock \
  --enable-vnc \
  --enable-vnc-png \
  --enable-vnc-sasl \
%if %{enable_werror}
  --enable-werror \
%endif
  --enable-xkbcommon \
  \
  \
  --audio-drv-list=%{?pa_drv}%{?sdl_drv}alsa,%{?jack_drv}oss \
  --target-list-exclude=%{excluded_targets} \
  --with-default-devices \
  --enable-auth-pam \
  --enable-bochs \
%if %{with brltty}
  --enable-brlapi \
%endif
  --enable-bzip2 \
  --enable-cloop \
  --enable-curses \
  --enable-dmg \
  --enable-fuse \
  --enable-gio \
%if %{have_block_gluster}
  --enable-glusterfs \
%endif
  --enable-gtk \
  --enable-libdaxctl \
%if %{have_block_nfs}
  --enable-libnfs \
%endif
  --enable-libudev \
  --enable-libxml2 \
%if %{have_liburing}
  --enable-linux-io-uring \
%endif
  --enable-linux-user \
  --enable-live-block-migration \
  --enable-multiprocess \
  --enable-vnc-jpeg \
  --enable-parallels \
%if %{have_librdma}
  --enable-pvrdma \
%endif
  --enable-qcow1 \
  --enable-qed \
  --enable-qom-cast-debug \
  --enable-replication \
%if %{with sdl}
  --enable-sdl \
%if %{have_sdl_image}
  --enable-sdl-image \
%endif
%endif
%if %{have_libcacard}
  --enable-smartcard \
%endif
%if %{have_spice}
  --enable-spice \
  --enable-spice-protocol \
%endif
  --enable-usb-redir \
  --enable-vdi \
  --enable-vhost-crypto \
  --enable-vhost-scsi \
%if %{have_virgl}
  --enable-virglrenderer \
%endif
  --enable-virtfs \
  --enable-vnc-jpeg \
  --enable-vte \
  --enable-vvfat \
%if %{have_xen}
  --enable-xen \
  --enable-xen-pci-passthrough \
%endif
  --enable-zstd

%if %{tools_only}
%make_build qemu-img
%make_build qemu-io
%make_build qemu-nbd
%make_build storage-daemon/qemu-storage-daemon

%make_build docs/qemu-img.1
%make_build docs/qemu-nbd.8
%make_build docs/qemu-storage-daemon.1
%make_build docs/qemu-storage-daemon-qmp-ref.7

%make_build qga/qemu-ga
%make_build docs/qemu-ga.8
# endif tools_only
%endif


%if !%{tools_only}
%make_build
popd


# We don't support qemu-ser-static

# endif !tools_only
%endif

%install
# Install qemu-guest-agent service and udev rules
install -D -m 0644 %{_sourcedir}/qemu-guest-agent.service %{buildroot}%{_unitdir}/qemu-guest-agent.service
install -D -m 0644 %{_sourcedir}/qemu-ga.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/qemu-ga
install -D -m 0644 %{_sourcedir}/99-qemu-guest-agent.rules %{buildroot}%{_udevrulesdir}/99-qemu-guest-agent.rules


# Install qemu-ga fsfreeze bits
mkdir -p %{buildroot}%{_sysconfdir}/qemu-ga/fsfreeze-hook.d
install -p scripts/qemu-guest-agent/fsfreeze-hook %{buildroot}%{_sysconfdir}/qemu-ga/fsfreeze-hook
mkdir -p %{buildroot}%{_datadir}/%{name}/qemu-ga/fsfreeze-hook.d/
install -p -m 0644 scripts/qemu-guest-agent/fsfreeze-hook.d/*.sample %{buildroot}%{_datadir}/%{name}/qemu-ga/fsfreeze-hook.d/
mkdir -p -v %{buildroot}%{_localstatedir}/log/qemu-ga/


%if %{tools_only}
pushd %{qemu_kvm_build}
install -D -p -m 0755 qga/qemu-ga %{buildroot}%{_bindir}/qemu-ga
install -D -p -m 0755 qemu-img %{buildroot}%{_bindir}/qemu-img
install -D -p -m 0755 qemu-io %{buildroot}%{_bindir}/qemu-io
install -D -p -m 0755 qemu-nbd %{buildroot}%{_bindir}/qemu-nbd
install -D -p -m 0755 storage-daemon/qemu-storage-daemon %{buildroot}%{_bindir}/qemu-storage-daemon

mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_mandir}/man7/
mkdir -p %{buildroot}%{_mandir}/man8/

install -D -p -m 644 docs/qemu-img.1* %{buildroot}%{_mandir}/man1
install -D -p -m 644 docs/qemu-nbd.8* %{buildroot}%{_mandir}/man8
install -D -p -m 644 docs/qemu-storage-daemon.1* %{buildroot}%{_mandir}/man1
install -D -p -m 644 docs/qemu-storage-daemon-qmp-ref.7* %{buildroot}%{_mandir}/man7
install -D -p -m 644 docs/qemu-ga.8* %{buildroot}%{_mandir}/man8
popd
# endif tools_only
%endif


%if !%{tools_only}
# Install rules to use the bridge helper with libvirt's virbr0
install -D -m 0644 %{_sourcedir}/bridge.conf %{buildroot}%{_sysconfdir}/%{name}/bridge.conf

# Install qemu-pr-helper service
install -m 0644 contrib/systemd/qemu-pr-helper.service %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/qemu-pr-helper.socket %{buildroot}%{_unitdir}

%if %{have_memlock_limits}
install -D -p -m 644 %{_sourcedir}/95-kvm-memlock.conf %{buildroot}%{_sysconfdir}/security/limits.d/95-kvm-memlock.conf
%endif

%if %{have_kvm}
install -D -p -m 0644 %{_sourcedir}/vhost.conf %{buildroot}%{_sysconfdir}/modprobe.d/vhost.conf
install -D -p -m 0644 %{modprobe_kvm_conf} %{buildroot}%{_sysconfdir}/modprobe.d/kvm.conf
%endif

# Copy some static data into place
install -D -p -m 0644 -t %{buildroot}%{qemudocdir} README.rst COPYING COPYING.LIB LICENSE docs/interop/qmp-spec.txt
install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/%{name}.conf

install -m 0644 scripts/dump-guest-memory.py %{buildroot}%{_datadir}/%{name}


# Install simpletrace
install -m 0755 scripts/simpletrace.py %{buildroot}%{_datadir}/%{name}/simpletrace.py
mkdir -p %{buildroot}%{_datadir}/%{name}/tracetool
install -m 0644 -t %{buildroot}%{_datadir}/%{name}/tracetool scripts/tracetool/*.py
mkdir -p %{buildroot}%{_datadir}/%{name}/tracetool/backend
install -m 0644 -t %{buildroot}%{_datadir}/%{name}/tracetool/backend scripts/tracetool/backend/*.py
mkdir -p %{buildroot}%{_datadir}/%{name}/tracetool/format
install -m 0644 -t %{buildroot}%{_datadir}/%{name}/tracetool/format scripts/tracetool/format/*.py


# Create new directories and put them all under tests-src
mkdir -p %{buildroot}%{testsdir}/python
mkdir -p %{buildroot}%{testsdir}/tests
mkdir -p %{buildroot}%{testsdir}/tests/avocado
mkdir -p %{buildroot}%{testsdir}/tests/qemu-iotests
mkdir -p %{buildroot}%{testsdir}/scripts/qmp

# Install avocado_qemu tests
cp -R %{qemu_kvm_build}/tests/avocado/* %{buildroot}%{testsdir}/tests/avocado/

# Install qemu.py and qmp/ scripts required to run avocado_qemu tests
cp -R %{qemu_kvm_build}/python/qemu %{buildroot}%{testsdir}/python
cp -R %{qemu_kvm_build}/scripts/qmp/* %{buildroot}%{testsdir}/scripts/qmp
install -p -m 0755 tests/Makefile.include %{buildroot}%{testsdir}/tests/

# Install qemu-iotests
cp -R tests/qemu-iotests/* %{buildroot}%{testsdir}/tests/qemu-iotests/
cp -ur %{qemu_kvm_build}/tests/qemu-iotests/* %{buildroot}%{testsdir}/tests/qemu-iotests/

# Install our custom tests README
install -p -m 0644 %{_sourcedir}/README.tests %{buildroot}%{testsdir}/README


# Do the actual qemu tree install
pushd %{qemu_kvm_build}
%make_install
popd


# We need to make the block device modules and other qemu SO files executable
# otherwise RPM won't pick up their dependencies.
chmod +x %{buildroot}%{_libdir}/%{name}/*.so

# Remove docs we don't care about
find %{buildroot}%{qemudocdir} -name .buildinfo -delete
rm -rf %{buildroot}%{qemudocdir}/specs


# Provided by package openbios
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-ppc
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc32
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc64
# Provided by package SLOF
rm -rf %{buildroot}%{_datadir}/%{name}/slof.bin
# Provided by package seavgabios
rm -rf %{buildroot}%{_datadir}/%{name}/vgabios*bin
# Provided by package seabios
rm -rf %{buildroot}%{_datadir}/%{name}/bios*.bin
# Provided by package sgabios
rm -rf %{buildroot}%{_datadir}/%{name}/sgabios.bin
# Provided by edk2
rm -rf %{buildroot}%{_datadir}/%{name}/edk2*
rm -rf %{buildroot}%{_datadir}/%{name}/firmware

# Remove datadir files packaged with excluded targets
%if %{without ppc_support}
rm -rf %{buildroot}%{_datadir}/%{name}/bamboo.dtb
rm -rf %{buildroot}%{_datadir}/%{name}/canyonlands.dtb
rm -rf %{buildroot}%{_datadir}/%{name}/qemu_vga.ndrv
rm -rf %{buildroot}%{_datadir}/%{name}/skiboot.lid
rm -rf %{buildroot}%{_datadir}/%{name}/u-boot.e500
rm -rf %{buildroot}%{_datadir}/%{name}/u-boot-sam460-20100605.bin
%endif

%if %{without sparc_support}
rm -rf %{buildroot}%{_datadir}/%{name}/QEMU,tcx.bin
rm -rf %{buildroot}%{_datadir}/%{name}/QEMU,cgthree.bin
%endif

%find_lang %{name}

# Generate qemu-system-* man pages
chmod -x %{buildroot}%{_mandir}/man1/*
for emu in %{buildroot}%{_bindir}/qemu-system-*; do
    ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/$(basename $emu).1.gz
 done

%ifarch x86_64
# Install kvm specific source bits, and qemu-kvm manpage
%if %{need_qemu_kvm}
ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/qemu-kvm.1.gz
ln -sf qemu-system-x86_64 %{buildroot}%{_bindir}/qemu-kvm
%endif
%else
# Needed until CBL-Mariner starts cross-compiling 'ipxe', 'seabios' and 'sgabios' for other architectures.
rm -rf %{buildroot}%{_bindir}/qemu-system-i386
rm -rf %{buildroot}%{_bindir}/qemu-system-x86_64
rm -rf %{buildroot}%{_libdir}/%{name}/accel-tcg-i386.so
rm -rf %{buildroot}%{_libdir}/%{name}/accel-tcg-x86_64.so
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-i386*.stp
rm -rf %{buildroot}%{_datadir}/systemtap/tapset/qemu-system-x86_64*.stp
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-i386.1*
rm -rf %{buildroot}%{_mandir}/man1/qemu-system-x86_64.1*
rm -rf %{buildroot}%{_datadir}/%{name}/kvmvapic.bin
rm -rf %{buildroot}%{_datadir}/%{name}/linuxboot.bin
rm -rf %{buildroot}%{_datadir}/%{name}/multiboot.bin
rm -rf %{buildroot}%{_datadir}/%{name}/multiboot_dma.bin
rm -rf %{buildroot}%{_datadir}/%{name}/pvh.bin
rm -rf %{buildroot}%{_datadir}/%{name}/qboot.rom
%endif


# Install binfmt
%global binfmt_dir %{buildroot}%{_libdir}/binfmt.d
mkdir -p %{binfmt_dir}

./scripts/qemu-binfmt-conf.sh --systemd ALL --exportdir %{binfmt_dir} --qemu-path %{_bindir}
for i in %{binfmt_dir}/*; do mv $i $(echo $i | sed 's/.conf/-dynamic.conf/'); done

# endif !tools_only
%endif



%check
# Suppress check as it stall the pipeline indefinetly
%if !%{tools_only}

pushd %{qemu_kvm_build}
echo "Testing %{name}-build"
# 2021-06: s390x tests randomly failing with 'Broken pipe' errors
# dhorak couldn't reproduce locally on an s390x machine so guessed
# it's a resource issue
# 2021-07: ppc64le intermittently hanging
%ifnarch s390x %{power64}
%make_build check
%endif

popd

# endif !tools_only
%endif


%post -n qemu-guest-agent
%systemd_post qemu-guest-agent.service

%preun -n qemu-guest-agent
%systemd_preun qemu-guest-agent.service

%postun -n qemu-guest-agent
%systemd_postun_with_restart qemu-guest-agent.service


%if !%{tools_only}
%post common
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
useradd -r -u 107 -g qemu -G kvm -d / -s %{_sbindir}/nologin \
  -c "qemu user" qemu

%post user-binfmt
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%postun user-binfmt
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

# endif !tools_only
%endif



%files -n qemu-img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_bindir}/qemu-storage-daemon
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*
%{_mandir}/man1/qemu-storage-daemon.1*
%{_mandir}/man7/qemu-storage-daemon-qmp-ref.7*

%files -n qemu-guest-agent
%license COPYING
%doc README.rst
%{_bindir}/qemu-ga
%{_mandir}/man8/qemu-ga.8*
%{_unitdir}/qemu-guest-agent.service
%{_udevrulesdir}/99-qemu-guest-agent.rules
%config(noreplace) %{_sysconfdir}/sysconfig/qemu-ga
%{_sysconfdir}/qemu-ga
%{_datadir}/%{name}/qemu-ga
%dir %{_localstatedir}/log/qemu-ga

%if !%{tools_only}
%files
# Deliberately empty

%files -n qemu-pr-helper
%{_bindir}/qemu-pr-helper
%{_unitdir}/qemu-pr-helper.service
%{_unitdir}/qemu-pr-helper.socket
%{_mandir}/man8/qemu-pr-helper.8*

%files -n qemu-virtiofsd
%{_mandir}/man1/virtiofsd.1*
%{_libexecdir}/virtiofsd
%{_datadir}/qemu/vhost-user/50-qemu-virtiofsd.json

%files tools
%{_bindir}/qemu-keymap
%{_bindir}/qemu-edid
%{_bindir}/qemu-trace-stap
%{_datadir}/%{name}/simpletrace.py*
%{_datadir}/%{name}/tracetool/*.py*
%{_datadir}/%{name}/tracetool/backend/*.py*
%{_datadir}/%{name}/tracetool/format/*.py*
%{_datadir}/%{name}/dump-guest-memory.py*
%{_datadir}/%{name}/trace-events-all
%{_mandir}/man1/qemu-trace-stap.1*
%{_bindir}/elf2dmp

%files docs
%doc %{qemudocdir}

%files common -f %{name}.lang
%license COPYING COPYING.LIB LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/icons/*
%{_datadir}/%{name}/keymaps/
%{_datadir}/%{name}/linuxboot_dma.bin
%attr(4755, -, -) %{_libexecdir}/qemu-bridge-helper
%{_mandir}/man1/%{name}.1*
%{_mandir}/man7/qemu-block-drivers.7*
%{_mandir}/man7/qemu-cpu-models.7*
%{_mandir}/man7/qemu-ga-ref.7*
%{_mandir}/man7/qemu-qmp-ref.7*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/bridge.conf
%if %{have_kvm}
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/vhost.conf
%endif
%config(noreplace) %{_sysconfdir}/sasl2/%{name}.conf

%{_datadir}/applications/qemu.desktop
%exclude %{_datadir}/%{name}/qemu-nsis.bmp
%{_libexecdir}/virtfs-proxy-helper
%{_mandir}/man1/virtfs-proxy-helper.1*

%files tests
%{testsdir}
%{_libdir}/%{name}/accel-qtest-*.so

%files block-curl
%{_libdir}/%{name}/block-curl.so

%files block-iscsi
%{_libdir}/%{name}/block-iscsi.so
%if %{have_block_rbd}
%files block-rbd
%{_libdir}/%{name}/block-rbd.so
%endif

%if %{with libssh}
%files block-ssh
%{_libdir}/%{name}/block-ssh.so
%endif

%if %{have_opengl}
%files ui-opengl
%{_libdir}/%{name}/ui-opengl.so
%endif


%files block-dmg
%{_libdir}/%{name}/block-dmg-bz2.so
%if %{have_block_gluster}
%files block-gluster
%{_libdir}/%{name}/block-gluster.so
%endif

%if %{have_block_nfs}
%files block-nfs
%{_libdir}/%{name}/block-nfs.so
%endif

%files audio-alsa
%{_libdir}/%{name}/audio-alsa.so

%files audio-oss
%{_libdir}/%{name}/audio-oss.so

%if %{with pulseaudio}
%files audio-pa
%{_libdir}/%{name}/audio-pa.so
%endif

%if %{with sdl}
%files audio-sdl
%{_libdir}/%{name}/audio-sdl.so
%endif

%if %{have_jack}
%files audio-jack
%{_libdir}/%{name}/audio-jack.so
%endif


%files ui-curses
%{_libdir}/%{name}/ui-curses.so

%files ui-gtk
%{_libdir}/%{name}/ui-gtk.so

%if %{with sdl}
%files ui-sdl
%{_libdir}/%{name}/ui-sdl.so
%endif

%files ui-egl-headless
%{_libdir}/%{name}/ui-egl-headless.so

%if %{with brltty}
%files char-baum
%{_libdir}/%{name}/chardev-baum.so
%endif

%files device-display-virtio-gpu
%{_libdir}/%{name}/hw-display-virtio-gpu.so

%files device-display-virtio-gpu-gl
%{_libdir}/%{name}/hw-display-virtio-gpu-gl.so

%files device-display-virtio-gpu-pci
%{_libdir}/%{name}/hw-display-virtio-gpu-pci.so

%files device-display-virtio-gpu-pci-gl
%{_libdir}/%{name}/hw-display-virtio-gpu-pci-gl.so

%files device-display-virtio-gpu-ccw
%{_libdir}/%{name}/hw-s390x-virtio-gpu-ccw.so

%files device-display-virtio-vga
%{_libdir}/%{name}/hw-display-virtio-vga.so

%files device-display-virtio-vga-gl
%{_libdir}/%{name}/hw-display-virtio-vga-gl.so

%files device-usb-host
%{_libdir}/%{name}/hw-usb-host.so

%files device-usb-redirect
%{_libdir}/%{name}/hw-usb-redirect.so

%if %{have_libcacard}
%files device-usb-smartcard
%{_libdir}/%{name}/hw-usb-smartcard.so
%endif

%if %{have_virgl}
%files device-display-vhost-user-gpu
%{_datadir}/%{name}/vhost-user/50-qemu-gpu.json
%{_libexecdir}/vhost-user-gpu
%endif

%if %{have_spice}
%files audio-spice
%{_libdir}/%{name}/audio-spice.so

%files char-spice
%{_libdir}/%{name}/chardev-spice.so

%files device-display-qxl
%{_libdir}/%{name}/hw-display-qxl.so

%files ui-spice-core
%{_libdir}/%{name}/ui-spice-core.so

%files ui-spice-app
%{_libdir}/%{name}/ui-spice-app.so
%endif


%if %{have_kvm}
%files kvm
# Deliberately empty

%files kvm-core
# Deliberately empty
%endif


%files user
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-aarch64
%{_bindir}/qemu-aarch64_be
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-hppa
%{_bindir}/qemu-hexagon
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-mips64
%{_bindir}/qemu-mips64el
%{_bindir}/qemu-mipsn32
%{_bindir}/qemu-mipsn32el
%{_bindir}/qemu-nios2
%{_bindir}/qemu-or1k
%if %{with ppc_support}
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64le
%endif
%{_bindir}/qemu-riscv32
%{_bindir}/qemu-riscv64
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%if %{with sparc_support}
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%endif
%{_bindir}/qemu-xtensa
%{_bindir}/qemu-xtensaeb

%{_datadir}/systemtap/tapset/qemu-i386*.stp
%{_datadir}/systemtap/tapset/qemu-x86_64*.stp
%{_datadir}/systemtap/tapset/qemu-aarch64*.stp
%{_datadir}/systemtap/tapset/qemu-alpha*.stp
%{_datadir}/systemtap/tapset/qemu-arm*.stp
%{_datadir}/systemtap/tapset/qemu-cris*.stp
%{_datadir}/systemtap/tapset/qemu-hppa*.stp
%{_datadir}/systemtap/tapset/qemu-hexagon*.stp
%{_datadir}/systemtap/tapset/qemu-m68k*.stp
%{_datadir}/systemtap/tapset/qemu-microblaze*.stp
%{_datadir}/systemtap/tapset/qemu-mips*.stp
%{_datadir}/systemtap/tapset/qemu-nios2*.stp
%{_datadir}/systemtap/tapset/qemu-or1k*.stp
%if %{with ppc_support}
%{_datadir}/systemtap/tapset/qemu-ppc*.stp
%endif
%{_datadir}/systemtap/tapset/qemu-riscv*.stp
%{_datadir}/systemtap/tapset/qemu-s390x*.stp
%{_datadir}/systemtap/tapset/qemu-sh4*.stp
%if %{with sparc_support}
%{_datadir}/systemtap/tapset/qemu-sparc*.stp
%endif
%{_datadir}/systemtap/tapset/qemu-xtensa*.stp

%files user-binfmt
%{_libdir}/binfmt.d/qemu-*-dynamic.conf

%files system-aarch64

%files system-aarch64-core
%{_bindir}/qemu-system-aarch64
%{_datadir}/systemtap/tapset/qemu-system-aarch64*.stp
%{_mandir}/man1/qemu-system-aarch64.1*

%files ipxe
%{_datadir}/%{name}/pxe*rom
%{_datadir}/%{name}/efi*rom

%ifarch x86_64
%files system-x86

%files system-x86-core
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_libdir}/%{name}/accel-tcg-i386.so
%{_libdir}/%{name}/accel-tcg-x86_64.so
%{_datadir}/systemtap/tapset/qemu-system-i386*.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64*.stp
%{_mandir}/man1/qemu-system-i386.1*
%{_mandir}/man1/qemu-system-x86_64.1*
%{_datadir}/%{name}/kvmvapic.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/multiboot_dma.bin
%{_datadir}/%{name}/pvh.bin
%{_datadir}/%{name}/qboot.rom
%if %{need_qemu_kvm}
%{_bindir}/qemu-kvm
%{_mandir}/man1/qemu-kvm.1*
%endif
%endif

%files system-alpha

%files system-alpha-core
%{_bindir}/qemu-system-alpha
%{_datadir}/systemtap/tapset/qemu-system-alpha*.stp
%{_mandir}/man1/qemu-system-alpha.1*
%{_datadir}/%{name}/palcode-clipper

%files system-arm

%files system-arm-core
%{_bindir}/qemu-system-arm
%{_datadir}/%{name}/npcm7xx_bootrom.bin
%{_datadir}/systemtap/tapset/qemu-system-arm*.stp
%{_mandir}/man1/qemu-system-arm.1*

%files system-avr

%files system-avr-core
%{_bindir}/qemu-system-avr
%{_datadir}/systemtap/tapset/qemu-system-avr*.stp
%{_mandir}/man1/qemu-system-avr.1*

%files system-cris

%files system-cris-core
%{_bindir}/qemu-system-cris
%{_datadir}/systemtap/tapset/qemu-system-cris*.stp
%{_mandir}/man1/qemu-system-cris.1*

%files system-hppa

%files system-hppa-core
%{_bindir}/qemu-system-hppa
%{_datadir}/systemtap/tapset/qemu-system-hppa*.stp
%{_mandir}/man1/qemu-system-hppa.1*
%{_datadir}/%{name}/hppa-firmware.img

%files system-m68k

%files system-m68k-core
%{_bindir}/qemu-system-m68k
%{_datadir}/systemtap/tapset/qemu-system-m68k*.stp
%{_mandir}/man1/qemu-system-m68k.1*

%files system-microblaze

%files system-microblaze-core
%{_bindir}/qemu-system-microblaze
%{_bindir}/qemu-system-microblazeel
%{_datadir}/systemtap/tapset/qemu-system-microblaze*.stp
%{_mandir}/man1/qemu-system-microblaze.1*
%{_mandir}/man1/qemu-system-microblazeel.1*
%{_datadir}/%{name}/petalogix*.dtb

%files system-mips

%files system-mips-core
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%{_datadir}/systemtap/tapset/qemu-system-mips*.stp
%{_mandir}/man1/qemu-system-mips.1*
%{_mandir}/man1/qemu-system-mipsel.1*
%{_mandir}/man1/qemu-system-mips64el.1*
%{_mandir}/man1/qemu-system-mips64.1*

%files system-nios2

%files system-nios2-core
%{_bindir}/qemu-system-nios2
%{_datadir}/systemtap/tapset/qemu-system-nios2*.stp
%{_mandir}/man1/qemu-system-nios2.1*

%files system-or1k

%files system-or1k-core
%{_bindir}/qemu-system-or1k
%{_datadir}/systemtap/tapset/qemu-system-or1k*.stp
%{_mandir}/man1/qemu-system-or1k.1*

%if %{with ppc_support}
%files system-ppc

%files system-ppc-core
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_datadir}/systemtap/tapset/qemu-system-ppc*.stp
%{_mandir}/man1/qemu-system-ppc.1*
%{_mandir}/man1/qemu-system-ppc64.1*
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/canyonlands.dtb
%{_datadir}/%{name}/qemu_vga.ndrv
%{_datadir}/%{name}/skiboot.lid
%{_datadir}/%{name}/u-boot.e500
%{_datadir}/%{name}/u-boot-sam460-20100605.bin
%if %{have_memlock_limits}
%{_sysconfdir}/security/limits.d/95-kvm-memlock.conf
%endif
%endif


%files system-riscv

%files system-riscv-core
%{_bindir}/qemu-system-riscv32
%{_bindir}/qemu-system-riscv64
%{_datadir}/%{name}/opensbi-riscv*.bin
%{_datadir}/%{name}/opensbi-riscv*.elf
%{_datadir}/systemtap/tapset/qemu-system-riscv*.stp
%{_mandir}/man1/qemu-system-riscv*.1*

%files system-rx

%files system-rx-core
%{_bindir}/qemu-system-rx
%{_datadir}/systemtap/tapset/qemu-system-rx*.stp
%{_mandir}/man1/qemu-system-rx.1*

%files system-s390x

%files system-s390x-core
%{_bindir}/qemu-system-s390x
%{_datadir}/systemtap/tapset/qemu-system-s390x*.stp
%{_mandir}/man1/qemu-system-s390x.1*
%{_datadir}/%{name}/s390-ccw.img
%{_datadir}/%{name}/s390-netboot.img

%files system-sh4

%files system-sh4-core
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
%{_datadir}/systemtap/tapset/qemu-system-sh4*.stp
%{_mandir}/man1/qemu-system-sh4.1*
%{_mandir}/man1/qemu-system-sh4eb.1*

%if %{with sparc_support}
%files system-sparc

%files system-sparc-core
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-sparc64
%{_datadir}/systemtap/tapset/qemu-system-sparc*.stp
%{_mandir}/man1/qemu-system-sparc.1*
%{_mandir}/man1/qemu-system-sparc64.1*
%{_datadir}/%{name}/QEMU,tcx.bin
%{_datadir}/%{name}/QEMU,cgthree.bin
%endif

%files system-tricore

%files system-tricore-core
%{_bindir}/qemu-system-tricore
%{_datadir}/systemtap/tapset/qemu-system-tricore*.stp
%{_mandir}/man1/qemu-system-tricore.1*

%files system-xtensa

%files system-xtensa-core
%{_bindir}/qemu-system-xtensa
%{_bindir}/qemu-system-xtensaeb
%{_datadir}/systemtap/tapset/qemu-system-xtensa*.stp
%{_mandir}/man1/qemu-system-xtensa.1*
%{_mandir}/man1/qemu-system-xtensaeb.1*

# endif !tools_only
%endif


%changelog
* Thu Dec 14 2023 Elaine Zhao <elainezhao@microsoft.com> - 6.2.0-20
- Address CVE-2023-2861

* Mon Oct 30 2023 Jonathan Behrens <jbehrens@microsoft.com> - 6.2.0-19
- Address CVE-2023-3354

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 6.2.0-18
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Aug 28 2023 Brian Fjeldstad <bfjelds@microsoft.com> - 6.2.0-17
- Address CVE-2022-36648

* Thu Jun 15 2023 Dylan Garrett <dylang@microsoft.com> - 6.2.0-16
- Address CVE-2021-3750

* Fri Apr 21 2023 Amrita Kohli <amritakohli@microsoft.com> - 6.2.0-15
- Patch for CVE-2022-3165

* Wed Feb 15 2023 Vince Perri <viperri@microsoft.com> - 6.2.0-14
- Move PXE and EFI ROM images from system-x86-core to new ipxe subpackage
- Require ipxe for both system-x86-core and system-aarch64-core packages

* Tue Dec 20 2022 Nan Liu <liunan@microsoft.com> - 6.2.0-13
- Address CVE-2021-3929, CVE-2021-4207

* Mon Dec 19 2022 Nan Liu <liunan@microsoft.com> - 6.2.0-12
- Address CVE-2022-3872

* Tue Dec 6 2022 Elaine Zhao <elainezhao@microsoft.com> - 6.2.0-11
- Address CVE-2022-4144

* Wed Oct 26 2022 Olivia Crain <oliviacrain@microsoft.com> - 6.2.0-10
- Have virtiofsd subpackage obsolete qemu-common from 6.1.0 releases

* Wed Sep 28 2022 Saul Paredes <saulparedes@microsoft.com> - 6.2.0-9
- Address CVE-2022-2962

* Fri Sep 09 2022 Muhammad Falak <mwani@microsoft.com> - 6.2.0-8
- Introduce patch from upstream to fix build with libbpf 1.0.0

* Tue Sep 06 2022 Daniel McIlvaney <damcilva@microsoft.com> - 6.2.0-7
- Patched CVE-2021-4158

* Tue Aug 23 2022 Nicolas Guibourge <mwani@microsoft.com> - 6.2.0-6
- address CVE-2022-35414

* Fri Jul 01 2022 Muhammad Falak <mwani@microsoft.com> - 6.2.0-5
- Ship efi*rom & pxe*rom rom files

* Wed Jun 15 2022 Muhammad Falak <mwani@microsoft.com> - 6.2.0-4
- Address CVE-2021-4206

* Fri May 20 2022 Chris Co <chrco@microsoft.com> - 6.2.0-3
- Patched CVE-2022-26353

* Fri May 06 2022 Daniel McIlvaney <damcilva@microsoft.com> - 6.2.0-2
- Remove multiboot_dma.bin from aarch64 builds

* Wed Apr 20 2022 Daniel McIlvaney <damcilva@microsoft.com> - 6.2.0-1
- Updated to match Fedora 36 (license: MIT)
- Patched CVE-2022-0358, CVE-2021-20225, CVE-2022-1050
- Backported patch for CVE-2022-26354

* Mon Jan 03 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.1.0-14
- Disabling 'qemu-system-x86*' subpackages build for non-AMD64 architectures.
- Disabling dependency on 'ipxe' for non-AMD64 architectures.

* Mon Jan 03 2022 Bala <balakumaran.kannan@microsoft.com> - 6.1.0-13
- Skip qos test from ptest as it hungs indefinitely

* Fri Dec 10 2021 Thomas Crain <thcrain@microsoft.com> - 6.1.0-12
- Lint spec
- Remove user-static subpackage references- no plans to support at this time

* Fri Dec 10 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.1.0-11
- License verified.

* Thu Dec 09 2021 Muhammad Falak <mwani@microsoft.com> - 6.1.0-10
- Introduce macro '%%{mariner_failing_tests}' to gate `--run-check` failures

* Wed Dec 08 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.1.0-9
- Conditionally disabling build options: brltty, capstone, libssh, pulseaudio, and sdl.
- Adding a fix for glibc 2.34.
- Disabled stripping of binaries.

* Wed Dec 1 2021 Muhammad Falak <mwani@microsoft.com> - 6.1.0-8
- Remove epoch

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2:6.1.0-7
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Sep 30 2021 Thomas Crain <thcrain@microsoft.com> - 2:6.1.0-6
- Initial CBL-Mariner import from Fedora 35 (license: MIT).
- Remove parts specific to unsupported build host architectures
- Remove default support for PPC and SPARC architectures
- Disable certain requirements/subpackages based on packages currently available
- Use IPXE release version constraints instead of timestamps
- Depend on base ipxe package rather than ipxe-roms-qemu

* Tue Aug 31 2021 Richard W.M. Jones <rjones@redhat.com> - 6.1.0-5
- Fix -cpu max (RHBZ#1999700)

* Fri Aug 27 2021 Richard W.M. Jones <rjones@redhat.com> - 6.1.0-4
- Disable gcrypt (for real this time).

* Fri Aug 27 2021 Richard W.M. Jones <rjones@redhat.com> - 6.1.0-3
- Revert "Disable gcrypt" which seems to disable gnutls (RHBZ#1998452)

* Thu Aug 26 2021 Richard W.M. Jones <rjones@redhat.com> - 6.1.0-2
- Fix dependency pci_gl -> pci-gl and vga_gl -> vga-gl (RHBZ#1997855)

* Tue Aug 24 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 6.1.0-1
- Rebase to qemu 6.1.0

* Tue Aug 10 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 6.1.0-0.3-rc4
- Rebase to qemu 6.1.0-rc4

* Tue Aug 10 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 6.1.0-0.2-rc3
- Rebase to qemu 6.1.0-rc3

* Mon Aug 9 2021 Eduardo Lima (Etrunko) <etrunko@redhat.com> - 6.1.0-0.1-rc2
- Rebase to qemu 6.1.0-rc2

* Thu Jul 29 2021 Cole Robinson <crobinso@redhat.com> - 6.0.0-12
- Drop python3 shebang fixup for tests rpm
- Parallelize make check
- Explicitly disable c++ build

* Fri Jul 23 2021 Richard W.M. Jones <rjones@redhat.com> - 6.0.0-11
- Fix dependencies of qemu metapackage.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:6.0.0-10.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 18 2021 Cole Robinson <crobinso@redhat.com> - 6.0.0-10
- Split out qemu-pr-helper and qemu-tools subpackages

* Wed Jul 07 2021 Cole Robinson <crobinso@redhat.com> - 6.0.0-9
- Use standard fedora build macros
- Access roms directly in ipxe, seabios, seavgabios directories

* Wed Jun 30 2021 Cole Robinson <crobinso@redhat.com> - 6.0.0-8
- Relax meson version to fix building on older Fedora
- More attempts to get CI working

* Wed Jun 23 2021 Cole Robinson <crobinso@redhat.com> - 6.0.0-7
- Add qemu-tests package
- Move qemu-sanity-check test to fedora CI
- Add s390x and generic kvm modprobe file from RHEL
- Add vhost modprobe file from RHEL
- Distribute tracetool, simpletrace, dump-guest-memory tools

* Wed Jun 16 2021 Cole Robinson <crobinso@redhat.com> - 6.0.0-6
- Build against fuse3 and SDL2_image
- Move qemu-storage-daemon to qemu-img subpackage

* Mon Jun 07 2021 Cole Robinson <crobinso@redhat.com> - 6.0.0-5
- Rebuild for xen 4.15

* Tue Jun 01 2021 Cole Robinson <crobinso@redhat.com> - 2:6.0.0-4
- Split out qemu-device-display-vhost-user-gpu subpackage
- Split out qemu-docs subpackage

* Wed May 19 2021 Paolo Bonzini <pbonzini@redhat.com> - 2:6.0.0-3
- add another patch to fix configuration files

* Wed May 19 2021 Paolo Bonzini <pbonzini@redhat.com> - 2:6.0.0-2
- fix spice option from configuration file
- fix object option from configuration file
- allow not specifying size in -m when using -M memory-backend

* Wed May 12 2021 Cole Robinson <crobinso@redhat.com> - 2:6.0.0-1
- Rebase to qemu 6.0.0 GA

* Wed Apr 21 2021 Cole Robinson <crobinso@redhat.com> - 2:6.0.0-0.3.rc4
- Rebase to qemu 6.0.0-rc4

* Wed Apr 14 2021 Richard W.M. Jones <rjones@redhat.com> - 2:6.0.0-0.2.rc2
- Rebuild for updated liburing.

* Tue Apr 06 2021 Cole Robinson <aintdiscole@gmail.com> - 6.0.0-0.1.rc2
- Rebase to qemu 6.0.0-rc2

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2:5.2.0-6.1
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Mar 01 2021 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-6
- Fix building on centos stream in copr

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:5.2.0-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Paolo Bonzini <pbonzini@redhat.com> - 2:5.2.0-5
- Use symlink for qemu-kvm.
- Fix make check on bash 5.1.

* Fri Dec 11 2020 Richard W.M. Jones <rjones@redhat.com> - 2:5.2.0-4
- qemu-char-spice not qemu-chardev-spice.

* Thu Dec 10 2020 Mohan Boddu <mboddu@bhujji.com> - 5.2.0-2
- Fixing the ISA Dependencies

* Wed Dec 09 2020 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-1
- Rebase to qemu-5.2.0 GA
- Fix spice and GL UI module deps (bz 1904603)

* Thu Dec 03 2020 Richard W.M. Jones <rjones@redhat.com> - 5.2.0-0.9.rc4
- Enable qemu-kvm-core package on riscv64.

* Thu Dec 03 2020 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-0.8.rc4
- Rebase to qemu-5.2.0-rc4

* Tue Nov 24 2020 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-0.7.rc2
- Fix running 9p tests in copr

* Thu Nov 19 2020 Paolo Bonzini <pbonzini@redhat.com> - 5.2.0-0.6.rc2
- Remove --python=... to force use of system meson

* Thu Nov 19 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.2.0-0.5.rc2
- Re-enable systemtap tracing

* Wed Nov 18 2020 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-0.4.rc2
- Rebase to qemu-5.2.0-rc2

* Fri Nov 13 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.2.0-0.3.rc1
- Disable user mode static builds in ELN

* Wed Nov 11 2020 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-0.2.rc1
- Rebase to qemu-5.2.0-rc1

* Sun Nov 08 2020 Cole Robinson <aintdiscole@gmail.com> - 5.2.0-0.1.rc0
- Rebase to qemu-5.2.0-rc0

* Thu Nov  5 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.1.0-7
- Disable LTO again. Tests were not passing, we were ignoring failures.

* Mon Oct 26 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.1.0-6
- Re-enable LTO since tests now pass without asserts

* Fri Sep  4 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.1.0-5
- Drop conditions for ppc, ppc64, mips64 and s390 arches
- Fix host qemu binary path for aarch64
- Re-enable kernel BR for QEMU sanity check
- Fix conditionals for enabling QEMU sanity check
- Check whether emulator works before doing sanity check
- Provide explicit kernel path for QEMU sanity check
- Make QEMU sanity check a build blocker

* Thu Sep  3 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.1.0-4
- Add btrfs ioctls to linux-user (rhbz #1872918)

* Tue Aug 18 2020 Tom Stellard <tstellar@redhat.com> - 5.1.0-3
- Add BuildRequires: gcc
- https://fedoraproject.org/wiki/Packaging:C_and_C%2B%2B#BuildRequires_and_Requires

* Mon Aug 17 2020 Cole Robinson <aintdiscole@gmail.com> - 5.1.0-2
- Disable dtrace generation to fix use of modules (bz 1869339)

* Tue Aug 11 2020 Cole Robinson <crobinso@redhat.com> - 5.1.0-1
- Update to version 5.1.0

* Fri Aug 07 2020 Cole Robinson <crobinso@redhat.com> - 5.1.0-0.3.rc3
- Update to version 5.1.0-rc3

* Thu Aug 06 2020 Merlin Mathesius <mmathesi@redhat.com> - 5.1.0-0.2.rc2
- Use new %%{kernel_arches} macro to determine when a full kernel is available

* Wed Aug 05 2020 Cole Robinson <aintdiscole@gmail.com> - 5.1.0-0.2.rc2
- Pull in new modules by default, like we do for others

* Tue Aug 04 2020 Cole Robinson <aintdiscole@gmail.com> - 5.1.0-0.1.rc2
- Update to qemu 5.1.0 rc2

* Fri Jul 31 2020 Daniel P. Berrangé <berrange@redhat.com> - 5.0.0-6
- Remove obsolete Fedora conditionals (PR#9)

* Thu Jul 30 2020 Richard W.M. Jones <rjones@redhat.com> - 5.0.0-5
- Disable LTO as it caused many strange assert failures.

* Wed Jul 29 2020 Richard W.M. Jones <rjones@redhat.com> - 5.0.0-4
- Backport Dan's upstream patch to fix insecure cert in test suite.

* Mon Jul 27 2020 Kevin Fenzi <kevin@scrye.com> - 5.0.0-3
- Rebuild for new xen

* Wed May 13 2020 Cole Robinson <crobinso@redhat.com> - 5.0.0-2
- Fix iouring hang (bz #1823751)

* Wed May 06 2020 Cole Robinson <crobinso@redhat.com> - 5.0.0-1
- Update to version 5.0.0

* Thu Apr 16 2020 Cole Robinson <aintdiscole@gmail.com> - 5.0.0-0.3.rc3
- Update to qemu 5.0.0 rc3

* Thu Apr 09 2020 Cole Robinson <aintdiscole@gmail.com> - 5.0.0-0.3.rc2
- Update to qemu 5.0.0 rc2

* Wed Apr 08 2020 Adam Williamson <awilliam@redhat.com> - 2:5.0.0-0.2.rc0
- Rebuild for new brltty

* Wed Mar 25 2020 Cole Robinson <crobinso@redhat.com> - 2:5.0.0-0.1.rc0
- Update to qemu-5.0.0-rc0

* Tue Mar 17 2020 Fabiano Fidêncio <fidencio@redhat.com> - 2:4.2.0-7
- Fix segfault with SR-IOV hot-{plug,unplug} (bz #1814017)

* Tue Feb 25 2020 Cole Robinson <crobinso@redhat.com> - 2:4.2.0-6
- Rebuild for libiscsi soname bump

* Sat Feb 15 2020 Cole Robinson <crobinso@redhat.com> - 2:4.2.0-5
- Fix ppc shutdown issue (bz #1784961)

* Tue Jan 28 2020 Cole Robinson <crobinso@redhat.com> - 2:4.2.0-4
- virtio-fs support

* Sat Jan 25 2020 Richard W.M. Jones <rjones@redhat.com> - 4.2.0-3
- Add miscellaneous fixes for RISC-V (RHBZ#1794902).
