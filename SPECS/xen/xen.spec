# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Build ocaml bits unless rpmbuild was run with --without ocaml 
# or ocamlopt is missing (the xen makefile doesn't build ocaml bits if it isn't there)
%define with_ocaml  %{?_without_ocaml: 0} %{?!_without_ocaml: 1}
%define build_ocaml %(test -x %{_bindir}/ocamlopt && echo %{with_ocaml} || echo 0)
# Build with docs unless rpmbuild was run with --without docs
%define build_docs %{?_without_docs: 0} %{?!_without_docs: 1}
# Build with stubdom unless rpmbuild was run with --without stubdom
%define build_stubdom %{?_without_stubdom: 0} %{?!_without_stubdom: 1}
# build with ovmf from edk2-ovmf unless rpmbuild was run with --without ovmf
%define build_ovmf %{?_without_ovmf: 0} %{?!_without_ovmf: 1}
# set to 0 for archs that don't use ovmf (reduces build dependencies)
%ifnarch x86_64
%define build_ovmf 0
%endif
# Build with xen hypervisor unless rpmbuild was run with --without hyp
%define build_hyp %{?_without_hyp: 0} %{?!_without_hyp: 1}
# build xsm support unless rpmbuild was run with --without xsm
# or required packages are missing
%define with_xsm  %{?_without_xsm: 0} %{?!_without_xsm: 1}
%define build_xsm %(test -x %{_bindir}/checkpolicy && test -x %{_bindir}/m4 && echo %{with_xsm} || echo 0)
# cross compile 64-bit hypervisor on ix86 unless rpmbuild was run
#	with --without crosshyp
%define build_crosshyp %{?_without_crosshyp: 0} %{?!_without_crosshyp: 1}
%ifnarch %{ix86}
%define build_crosshyp 0
%else
%if ! %build_crosshyp
%define build_hyp 0
%endif
%endif
# no point in trying to build xsm on ix86 without a hypervisor
%if ! %build_hyp
%define build_xsm 0
%endif
# build an efi boot image (where supported) unless rpmbuild was run with
# --without efi
%define build_efi %{?_without_efi: 0} %{?!_without_efi: 1}
# xen only supports efi boot images on x86_64 or aarch64
%ifnarch x86_64 aarch64
%define build_efi 0
%endif
%if "%dist" >= ".fc20"
%define with_systemd_presets 1
%else
%define with_systemd_presets 0
%endif

# Hypervisor ABI
%define hv_abi  4.20

Summary: Xen is a virtual machine monitor
Name:    xen
Version: 4.20.2
Release: 3%{?dist}
# Automatically converted from old format: GPLv2+ and LGPLv2+ and BSD - review is highly recommended.
License: GPL-2.0-or-later AND LicenseRef-Callaway-LGPLv2+ AND LicenseRef-Callaway-BSD
URL:     http://xen.org/
Source0: https://downloads.xenproject.org/release/xen/%{version}/xen-%{version}.tar.gz
Source2: %{name}.logrotate
# used by stubdoms
Source10: lwip-1.3.0.tar.gz
Source11: newlib-1.16.0.tar.gz
Source12: zlib-1.2.3.tar.gz
Source13: pciutils-2.2.9.tar.bz2
Source14: grub-0.97.tar.gz
Source15: polarssl-1.1.4-gpl.tgz
# .config file for xen hypervisor
Source21: xen.hypervisor.config
# mini-os xen-RELEASE-4.20.0 with .git and .gitignore stripped
Source22: mini-os-4.20.0.tar.xz

Patch5: xen.fedora.systemd.patch
Patch6: xen.ocaml.selinux.fix.patch
Patch34: xen.canonicalize.patch
Patch37: droplibvirtconflict.patch
Patch41: xen.gcc9.fixes.patch
Patch43: xen.gcc11.fixes.patch
Patch45: xen.gcc12.fixes.patch
Patch46: xen.efi.build.patch
Patch49: xen.python3.12.patch
Patch50: xsa477.patch
Patch51: xsa479.patch


# build using Fedora seabios and ipxe packages for roms
BuildRequires: seabios-bin ipxe-roms-qemu
%ifarch %{ix86} x86_64
# for the VMX "bios"
BuildRequires: dev86
%endif
BuildRequires: python3-devel ncurses-devel python3-setuptools
BuildRequires: perl-interpreter perl-generators
BuildRequires: gettext
BuildRequires: gnutls-devel
BuildRequires: openssl-devel
# For ioemu PCI passthrough
BuildRequires: pciutils-devel
# Several tools now use uuid
BuildRequires: libuuid-devel
# iasl needed to build hvmloader
BuildRequires: acpica-tools
# modern compressed kernels
BuildRequires: bzip2-devel xz-devel libzstd-devel
# libfsimage
BuildRequires: e2fsprogs-devel
# tools now require yajl and wget
BuildRequires: yajl-devel wget
# remus support now needs libnl3
BuildRequires: libnl3-devel
%if %with_xsm
# xsm policy file needs needs checkpolicy and m4
BuildRequires: checkpolicy m4
%endif
%if %build_crosshyp
# cross compiler for building 64-bit hypervisor on ix86
BuildRequires: gcc-x86_64-linux-gnu
%endif
BuildRequires: gcc make
Requires: iproute
Requires: python3-lxml
Requires: xen-runtime = %{version}-%{release}
# Not strictly a dependency, but kpartx is by far the most useful tool right
# now for accessing domU data from within a dom0 so bring it in when the user
# installs xen.
Requires: kpartx
ExclusiveArch: x86_64 aarch64
%if %with_ocaml
BuildRequires: ocaml, ocaml-findlib
BuildRequires: perl(Data::Dumper)
%endif
%if %with_systemd_presets
Requires(post): systemd
Requires(preun): systemd
BuildRequires: systemd
%endif
BuildRequires: systemd-devel
%ifarch aarch64
BuildRequires: libfdt-devel
%endif
%if %build_hyp
BuildRequires: bison flex
%endif
BuildRequires: hostname

%description
This package contains the XenD daemon and xm command line
tools, needed to manage virtual machines running under the
Xen hypervisor

%package libs
Summary: Libraries for Xen tools
Requires: xen-licenses

%description libs
This package contains the libraries needed to run applications
which manage Xen virtual machines.


%package runtime
Summary: Core Xen runtime environment
Requires: xen-libs = %{version}-%{release}
#Requires: /usr/bin/qemu-img /usr/bin/qemu-nbd
Requires: /usr/bin/qemu-img
# Ensure we at least have a suitable kernel installed, though we can't
# force user to actually boot it.
Requires: xen-hypervisor-abi = %{hv_abi}
# perl is used in /etc/xen/scripts/locking.sh
Recommends: perl
%ifnarch aarch64
# use /usr/bin/qemu-system-i386 in Fedora instead of qemu-xen
Recommends: qemu-system-x86-core
%endif
%if %build_ovmf
Recommends: edk2-ovmf-xen
%endif

%description runtime
This package contains the runtime programs and daemons which
form the core Xen userspace environment.


%package hypervisor
Summary: Libraries for Xen tools
Provides: xen-hypervisor-abi = %{hv_abi}
Requires: xen-licenses
%if %build_hyp
%ifarch %{ix86}
Recommends: grub2-pc-modules
%endif
%ifarch x86_64
Recommends: grub2-pc-modules grub2-efi-x64-modules
%endif
%endif

%description hypervisor
This package contains the Xen hypervisor


%if %build_docs
%package doc
Summary: Xen documentation
BuildArch: noarch
Requires: xen-licenses
# for the docs
BuildRequires: perl(Pod::Man) perl(Pod::Text) perl(File::Find)
BuildRequires: transfig pandoc perl(Pod::Html)

%description doc
This package contains the Xen documentation.
%endif


%package devel
Summary: Development libraries for Xen tools
Requires: xen-libs = %{version}-%{release}
Requires: libuuid-devel

%description devel
This package contains what's needed to develop applications
which manage Xen virtual machines.


%package licenses
Summary: License files from Xen source

%description licenses
This package contains the license files from the source used
to build the xen packages.


%if %build_ocaml
%package ocaml
Summary: Ocaml libraries for Xen tools
Requires: ocaml-runtime, xen-libs = %{version}-%{release}

%description ocaml
This package contains libraries for ocaml tools to manage Xen
virtual machines.


%package ocaml-devel
Summary: Ocaml development libraries for Xen tools
Requires: xen-ocaml = %{version}-%{release}

%description ocaml-devel
This package contains libraries for developing ocaml tools to
manage Xen virtual machines.
%endif


%prep
%setup -q
%patch 5 -p1
%patch 6 -p1
%patch 34 -p1
%patch 37 -p1
%patch 41 -p1
%patch 43 -p1
%patch 45 -p1
%patch 46 -p1
%patch 49 -p1
%patch 50 -p1
%patch 51 -p1

# stubdom sources
cp -v %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} stubdom
# copy xen hypervisor .config file to change settings
cp -v %{SOURCE21} xen/.config
# mini-os is now separate file
mkdir extras
tar -C extras -xf %{SOURCE22}

%build
# This package calls binutils components directly and would need to pass
# in flags to enable the LTO plugins
# Disable LTO
%define _lto_cflags %{nil}

%if !%build_ocaml
%define ocaml_flags OCAML_TOOLS=n
%endif
%if %build_efi
mkdir -p dist/install/boot/efi/efi/fedora
%endif
%if %build_ocaml
mkdir -p dist/install%{_libdir}/ocaml/stublibs
%endif
export EXTRA_CFLAGS_XEN_TOOLS="$RPM_OPT_FLAGS -Wno-error=use-after-free $LDFLAGS"
export PYTHON="/usr/bin/python3"
export LDFLAGS_SAVE=`echo $LDFLAGS | sed -e 's/-Wl,//g' -e 's/,/ /g' -e 's? -specs=[-a-z/0-9]*??g'`
export CFLAGS_SAVE="$CFLAGS"
CONFIG_EXTRA=""
%if %build_ovmf
CONFIG_EXTRA="$CONFIG_EXTRA --with-system-ovmf=/usr/share/edk2/xen/OVMF.fd"
%endif
%ifarch aarch64
CONFIG_EXTRA="$CONFIG_EXTRA --with-system-ipxe=/usr/share/ipxe/10ec8139.rom"
%endif
%if %(test -f /usr/share/seabios/bios-256k.bin && echo 1|| echo 0)
CONFIG_EXTRA="$CONFIG_EXTRA --with-system-seabios=/usr/share/seabios/bios-256k.bin"
%else
CONFIG_EXTRA="$CONFIG_EXTRA --disable-seabios"
%endif
%if %with_systemd_presets
CONFIG_EXTRA="$CONFIG_EXTRA --enable-systemd"
%endif
./configure --prefix=%{_prefix} --libdir=%{_libdir} --libexecdir=%{_libexecdir} --with-system-qemu=/usr/bin/qemu-system-i386 --with-linux-backend-modules="xen-evtchn xen-gntdev xen-gntalloc xen-blkback xen-netback xen-pciback xen-scsiback xen-acpi-processor" $CONFIG_EXTRA
unset CFLAGS CXXFLAGS FFLAGS LDFLAGS
export LDFLAGS="$LDFLAGS_SAVE"
export CFLAGS=`echo "$CFLAGS_SAVE -Wno-error=address" | sed -e s/-specs=\/usr\/lib\/rpm\/redhat/redhat-annobin-cc1//g`

%if %build_hyp
%make_build prefix=/usr xen
%endif
unset CFLAGS CXXFLAGS FFLAGS LDFLAGS

%make_build %{?ocaml_flags} prefix=/usr tools
%if %build_docs
make                 prefix=/usr docs
%endif
export RPM_OPT_FLAGS_RED=`echo $RPM_OPT_FLAGS | sed -e 's/-m64//g' -e 's/--param=ssp-buffer-size=4//g' -e's/-fstack-protector-strong//'`
%if %build_stubdom
%ifnarch armv7hl aarch64
make mini-os-dir
make -C stubdom build
%endif
%ifarch x86_64
export EXTRA_CFLAGS_XEN_TOOLS="$RPM_OPT_FLAGS_RED"
XEN_TARGET_ARCH=x86_32 make -C stubdom pv-grub-if-enabled
%endif
%endif


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -prlP dist/install/* %{buildroot}
%if %build_stubdom
%ifnarch armv7hl aarch64
make DESTDIR=%{buildroot} %{?ocaml_flags} prefix=/usr install-stubdom
%endif
%endif
%if %build_efi
mv %{buildroot}/boot/efi/efi %{buildroot}/boot/efi/EFI
%endif
%if %build_xsm
# policy file should be in /boot/flask
mkdir %{buildroot}/boot/flask
mv %{buildroot}/boot/xenpolicy* %{buildroot}/boot/flask
%else
rm -f %{buildroot}/boot/xenpolicy*
%endif

############ debug packaging: list files ############

find %{buildroot} -print | xargs ls -ld | sed -e 's|.*%{buildroot}||' > f1.list

############ kill unwanted stuff ############

# stubdom: newlib
rm -rf %{buildroot}/usr/*-xen-elf

# hypervisor symlinks
rm -rf %{buildroot}/boot/xen-%{hv_abi}.gz
rm -rf %{buildroot}/boot/xen-4.gz
rm -rf %{buildroot}/boot/xen.gz
%if !%build_hyp
rm -rf %{buildroot}/boot
%endif

# silly doc dir fun
rm -fr %{buildroot}%{_datadir}/doc/xen

# Pointless helper
rm -f %{buildroot}%{_bindir}/xen-python-path

# README's not intended for end users
rm -f %{buildroot}/%{_sysconfdir}/xen/README*

# standard gnu info files
rm -rf %{buildroot}/usr/info

# adhere to Static Library Packaging Guidelines
rm -rf %{buildroot}/%{_libdir}/*.a

%if %build_efi
# clean up extra efi files
rm -f %{buildroot}/%{_libdir}/efi/xen-%{hv_abi}.efi
rm -f %{buildroot}/%{_libdir}/efi/xen-4.efi
rm -f %{buildroot}/%{_libdir}/efi/xen.efi
cp -p %{buildroot}/%{_libdir}/efi/xen-%{version}{,.notstripped}.efi
strip -s %{buildroot}/%{_libdir}/efi/xen-%{version}.efi
%endif

%if ! %build_ocaml
rm -rf %{buildroot}/%{_unitdir}/oxenstored.service
%endif

############ fixup files in /etc ############

# logrotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# init scripts
%define initdloc %(test -d /etc/rc.d/init.d/ && echo rc.d/init.d || echo init.d )

rm %{buildroot}%{_sysconfdir}/%{initdloc}/xen-watchdog
rm %{buildroot}%{_sysconfdir}/%{initdloc}/xencommons
rm %{buildroot}%{_sysconfdir}/%{initdloc}/xendomains
rm %{buildroot}%{_sysconfdir}/%{initdloc}/xendriverdomain

############ create dirs in /var ############

mkdir -p %{buildroot}%{_localstatedir}/lib/xen/images
mkdir -p %{buildroot}%{_localstatedir}/log/xen/console

############ create symlink for x86_64 for compatibility with 4.4 ############

%if "%{_libdir}" != "/usr/lib"
ln -s %{_libexecdir}/%{name} %{buildroot}/%{_libdir}/%{name}
%endif

############ create symlink to qemu-system-i386 in /usr/bin ############
ln -s ../../../bin/qemu-system-i386 %{buildroot}/%{_libexecdir}/%{name}/bin/qemu-system-i386

############ debug packaging: list files ############

find %{buildroot} -print | xargs ls -ld | sed -e 's|.*%{buildroot}||' > f2.list
diff -u f1.list f2.list || true

############ assemble license files ############

mkdir licensedir
# avoid licensedir to avoid recursion, also stubdom/ioemu and dist
# which are copies of files elsewhere
find . -path licensedir -prune -o -path stubdom/ioemu -prune -o \
  -path dist -prune -o -name COPYING -o -name LICENSE | while read file; do
  mkdir -p licensedir/`dirname $file`
  install -m 644 $file licensedir/$file
done

############ move sbin files to bin

mv %{buildroot}/usr/sbin/* %{buildroot}/usr/bin/

############ remove xen*.efi.elf files to avoid debuginfo failure

%ifarch x86_64
rm dist/install/usr/lib/debug/xen-*.efi.elf
rm %{buildroot}/usr/lib/debug/xen-*.efi.elf
%endif

############ all done now ############

%post
%if %with_systemd_presets
%systemd_post xendomains.service
%else
if [ $1 == 1 ]; then
  /bin/systemctl enable xendomains.service
fi
%endif

%preun
%if %with_systemd_presets
%systemd_preun xendomains.service
%else
if [ $1 == 0 ]; then
/bin/systemctl disable xendomains.service
fi
%endif

%post runtime
%if %with_systemd_presets
%systemd_post xenstored.service xenconsoled.service
%else
if [ $1 == 1 ]; then
  /bin/systemctl enable xenstored.service
  /bin/systemctl enable xenconsoled.service
fi
%endif

%preun runtime
%if %with_systemd_presets
%systemd_preun xenstored.service xenconsoled.service
%else
if [ $1 == 0 ]; then
  /bin/systemctl disable xenstored.service
  /bin/systemctl disable xenconsoled.service
fi
%endif

%posttrans runtime
if [ ! -L /usr/lib/xen -a -d /usr/lib/xen ] && [ -z "$(ls -A /usr/lib/xen)" ]; then
  rmdir /usr/lib/xen
fi
if [ ! -e /usr/lib/xen ]; then
  ln -s /usr/libexec/xen /usr/lib/xen
fi

%ldconfig_scriptlets libs

%if %build_hyp
%post hypervisor
do_it() {
    DIR=$1
    TARGET=$2
    if [ -d $DIR ]; then
      if [ ! -d $TARGET ]; then
        mkdir $TARGET
      fi
      for m in relocator.mod multiboot2.mod elf.mod; do
        if [ -f $DIR/$m ]; then
          if [ ! -f $TARGET/$m ] || ! cmp -s $DIR/$m $TARGET/$m; then
            cp -p $DIR/$m $TARGET/$m
          fi
        fi
      done
    fi
}
if [ $1 == 1 -a -f /sbin/grub2-mkconfig ]; then
  for f in /boot/grub2/grub.cfg; do
    if [ -f $f ]; then
      /sbin/grub2-mkconfig -o $f
      sed -i -e '/insmod module2/d' $f
    fi
  done
fi
if [ -f /sbin/grub2-mkconfig ]; then
  if [ -f /boot/grub2/grub.cfg ]; then
    DIR=/usr/lib/grub/i386-pc
    TARGET=/boot/grub2/i386-pc
    do_it $DIR $TARGET
    DIR=/usr/lib/grub/x86_64-efi
    TARGET=/boot/grub2/x86_64-efi
    do_it $DIR $TARGET
  fi
fi

%postun hypervisor
if [ -f /sbin/grub2-mkconfig ]; then
  for f in /boot/grub2/grub.cfg; do
    if [ -f $f ]; then
      /sbin/grub2-mkconfig -o $f
      sed -i -e '/insmod module2/d' $f
    fi
  done
fi
%endif

%if %build_ocaml
%post ocaml
%if %with_systemd_presets
%systemd_post oxenstored.service
%else
if [ $1 == 1 ]; then
  /bin/systemctl enable oxenstored.service
fi
%endif

%preun ocaml
%if %with_systemd_presets
%systemd_preun oxenstored.service
%else
if [ $1 == 0 ]; then
  /bin/systemctl disable oxenstored.service
fi
%endif
%endif

# Base package only contains XenD/xm python stuff
#files -f xen-xm.lang
%files
%doc COPYING README
%{python3_sitearch}/%{name}
%{python3_sitearch}/xen-*.egg-info

# Guest autostart links
%dir %attr(0700,root,root) %{_sysconfdir}/%{name}/auto
# Autostart of guests
%config(noreplace) %{_sysconfdir}/sysconfig/xendomains

%{_unitdir}/xendomains.service

%files libs
%{_libdir}/libxencall.so.1
%{_libdir}/libxencall.so.1.3
%{_libdir}/libxenctrl.so.4.*
%{_libdir}/libxendevicemodel.so.1
%{_libdir}/libxendevicemodel.so.1.4
%{_libdir}/libxenevtchn.so.1
%{_libdir}/libxenevtchn.so.1.2
%{_libdir}/libxenforeignmemory.so.1
%{_libdir}/libxenforeignmemory.so.1.4
%{_libdir}/libxenfsimage.so.4.*
%{_libdir}/libxengnttab.so.1
%{_libdir}/libxengnttab.so.1.2
%{_libdir}/libxenguest.so.4.*
%{_libdir}/libxenlight.so.4.*
%{_libdir}/libxenstat.so.4.*
%{_libdir}/libxenstore.so.4
%{_libdir}/libxenstore.so.4.0
%{_libdir}/libxentoolcore.so.1
%{_libdir}/libxentoolcore.so.1.0
%{_libdir}/libxentoollog.so.1
%{_libdir}/libxentoollog.so.1.0
%{_libdir}/libxenvchan.so.4.*
%{_libdir}/libxlutil.so.4.*
%{_libdir}/xenfsimage
%{_libdir}/libxenhypfs.so.1
%{_libdir}/libxenhypfs.so.1.0

# All runtime stuff except for XenD/xm python stuff
%files runtime
# Hotplug rules

%dir %attr(0700,root,root) %{_sysconfdir}/%{name}
%dir %attr(0700,root,root) %{_sysconfdir}/%{name}/scripts/
%config %attr(0700,root,root) %{_sysconfdir}/%{name}/scripts/*

%{_sysconfdir}/bash_completion.d/xl

%{_unitdir}/proc-xen.mount
%{_unitdir}/xenstored.service
%{_unitdir}/xenconsoled.service
%{_unitdir}/xen-watchdog.service
%{_unitdir}/xen-qemu-dom0-disk-backend.service
%{_unitdir}/xendriverdomain.service
/usr/lib/modules-load.d/xen.conf

%config(noreplace) %{_sysconfdir}/sysconfig/xencommons
%config(noreplace) %{_sysconfdir}/xen/xl.conf
%config(noreplace) %{_sysconfdir}/xen/cpupool
%config(noreplace) %{_sysconfdir}/xen/xlexample*

# Rotate console log files
%config(noreplace) %{_sysconfdir}/logrotate.d/xen

# Programs run by other programs
%dir %{_libexecdir}/%{name}
%dir %{_libexecdir}/%{name}/bin
%attr(0700,root,root) %{_libexecdir}/%{name}/bin/*

# man pages
%if %build_docs
%{_mandir}/man1/xentop.1*
%{_mandir}/man8/xentrace.8*
%{_mandir}/man1/xl.1*
%{_mandir}/man5/xl.cfg.5*
%{_mandir}/man5/xl.conf.5*
%{_mandir}/man5/xlcpupool.cfg.5*
%{_mandir}/man1/xenstore*
%{_mandir}/man5/xl-disk-configuration.5.gz
%{_mandir}/man7/xen-pci-device-reservations.7.gz
%{_mandir}/man7/xen-tscmode.7.gz
%{_mandir}/man7/xen-vtpm.7.gz
%{_mandir}/man7/xen-vtpmmgr.7.gz
%{_mandir}/man5/xl-network-configuration.5.gz
%{_mandir}/man7/xen-pv-channel.7.gz
%{_mandir}/man7/xl-numa-placement.7.gz
%{_mandir}/man1/xenhypfs.1.gz
%{_mandir}/man7/xen-vbd-interface.7.gz
%{_mandir}/man5/xl-pci-configuration.5.gz
%{_mandir}/man8/xenwatchdogd.8.gz
%endif

%{python3_sitearch}/xenfsimage*.so
%{python3_sitearch}/grub
%{python3_sitearch}/pygrub-*.egg-info

# The firmware
%ifarch x86_64
%dir %{_libexecdir}/%{name}/boot
%{_libexecdir}/xen/boot/hvmloader
%{_libexecdir}/%{name}/boot/xen-shim
/usr/lib/debug%{_libexecdir}/xen/boot/xen-shim-syms
%if %build_stubdom
%{_libexecdir}/xen/boot/xenstore-stubdom.gz
%{_libexecdir}/xen/boot/xenstorepvh-stubdom.gz
%endif
%endif
%if "%{_libdir}" != "/usr/lib"
%{_libdir}/%{name}
%endif
%ghost /usr/lib/%{name}
# General Xen state
%dir %{_localstatedir}/lib/%{name}
%dir %{_localstatedir}/lib/%{name}/dump
%dir %{_localstatedir}/lib/%{name}/images
# Xenstore runtime state
%ghost %{_localstatedir}/run/xenstored

# All xenstore CLI tools
%{_bindir}/xenstore
%{_bindir}/xenstore-*
#%#{_bindir}/remus
# XSM
%{_bindir}/flask-*
# Misc stuff
%ifnarch aarch64
%{_bindir}/xen-detect
%endif
%{_bindir}/xencov_split
%ifnarch aarch64
%{_bindir}/gdbsx
%{_bindir}/xen-kdd
%endif
%ifnarch aarch64
%{_bindir}/xen-hptool
%{_bindir}/xen-hvmcrash
%{_bindir}/xen-hvmctx
%endif
%{_bindir}/xenconsoled
%{_bindir}/xenlockprof
%{_bindir}/xenmon
%{_bindir}/xentop
%{_bindir}/xentrace_setmask
%{_bindir}/xenbaked
%{_bindir}/xenstored
%{_bindir}/xenpm
%{_bindir}/xenpmd
%{_bindir}/xenperf
%{_bindir}/xenwatchdogd
%{_bindir}/xl
%ifnarch aarch64
%{_bindir}/xen-lowmemd
%endif
%{_bindir}/xencov
%ifnarch aarch64
%{_bindir}/xen-mfndump
%endif
%{_bindir}/xenalyze
%{_bindir}/xentrace
%{_bindir}/xentrace_setsize
%ifnarch aarch64
%{_bindir}/xen-cpuid
%endif
%{_bindir}/xen-livepatch
%{_bindir}/xen-diag
%ifnarch armv7hl aarch64
%{_bindir}/xen-ucode
%{_bindir}/xen-memshare
%{_bindir}/xen-mceinj
%{_bindir}/xen-vmtrace
%endif
%{_bindir}/vchan-socket-proxy
%{_bindir}/xenhypfs
%{_bindir}/xen-access

# Xen logfiles
%dir %attr(0700,root,root) %{_localstatedir}/log/xen
# Guest/HV console logs
%dir %attr(0700,root,root) %{_localstatedir}/log/xen/console

%files hypervisor
%if %build_hyp
%ifnarch aarch64
/boot/xen-*.gz
/boot/xen*.config
%else
/boot/xen*
%endif
%if %build_xsm
%dir %attr(0755,root,root) /boot/flask
/boot/flask/xenpolicy*
%endif
/usr/lib/debug/xen*
%endif
%if %build_efi
%{_libdir}/efi/*.efi
%endif

%if %build_docs
%files doc
%doc docs/misc/
%doc dist/install/usr/share/doc/xen/html
%endif

%files devel
%{_includedir}/*.h
%dir %{_includedir}/xen
%{_includedir}/xen/*
%dir %{_includedir}/xenstore-compat
%{_includedir}/xenstore-compat/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files licenses
%doc licensedir/*

%if %build_ocaml
%files ocaml
%{_libdir}/ocaml/xen*
%exclude %{_libdir}/ocaml/xen*/*.a
%exclude %{_libdir}/ocaml/xen*/*.cmxa
%exclude %{_libdir}/ocaml/xen*/*.cmx
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner
%{_bindir}/oxenstored
%config(noreplace) %{_sysconfdir}/xen/oxenstored.conf
%{_unitdir}/oxenstored.service

%files ocaml-devel
%{_libdir}/ocaml/xen*/*.a
%{_libdir}/ocaml/xen*/*.cmxa
%{_libdir}/ocaml/xen*/*.cmx
%{_libdir}/ocaml/xsd_glue/*
%{_libexecdir}/xen/ocaml/xsd_glue/xenctrl_plugin/domain_getinfo_v1.cmxs
%endif

%changelog
* Thu Jan 29 2026 Michael Young <m.a.young@durham.ac.uk> - 4.20.2-3
  x86: buffer overrun with shadow paging + tracing [XSA-477, CVE-2025-58150]
	(#2434046)
  x86: incomplete IBPB for vCPU isolation [XSA-479, CVE-2026-23553]
	(#2434048)

* Fri Nov 14 2025 Michael Young <m.a.young@durham.ac.uk> - 4.20.2-1.fc43
- update to xen 4.20.2
  remove patches now included or superceded upstream

* Fri Oct 24 2025 Michael Young <m.a.young@durham.ac.uk> - 4.20.1-8
- Incorrect removal of permissions on PCI device unplug [XSA-476,
	CVE-2025-58149]

* Tue Oct 21 2025 Michael Young <m.a.young@durham.ac.uk> - 4.20.1-7
- x86: Incorrect input sanitisation in Viridian hypercalls [XSA-475,
	CVE-2025-58147, CVE-2025-58148]

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.20.1-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Wed Sep 10 2025 Michael Young <m.a.young@durham.ac.uk> - 4.20.1-5
- Mutiple vulnerabilities in the Viridian interface [XSA-472,
	CVE-2025-27466, CVE-2025-58142, CVE-2025-58143]
- Arm issues with page refcounting [XSA-473, CVE-2025-58144,
	CVE-2025-58145]

* Tue Sep 02 2025 Michael Young <m.a.young@durham.ac.uk> - 4.20.1-4
- tools/xl: don't crash on NULL command line

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.20.1-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Michael Young <m.a.young@durham.ac.uk> - 4.20.1-1
- update to xen 4.20.1
  remove old qemu code for spac file
  remove armv7hl and ix86 code from spec file
  update configuration in xen.hypervisor.config 
  minios is now a separate file
  package extra ocaml files
  unset -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 for hypervisor build
  rebase xen.efi.build.patch
  includes fixes for security vulnerabilites
  x86: Incorrect stubs exception handling for flags recovery [XSA-470,
	CVE-2025-27465]
  x86: Transitive Scheduler Attacks [XSA-471, CVE-2024-36350,
	CVE-2024-36357]

* Fri Jul 11 2025 Jerry James  <loganjerry@gmail.com> - 4.19.2-6
- Rebuild to fix OCaml dependencies

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 4.19.2-5
- Rebuilt for Python 3.14

* Mon May 12 2025 Michael Young <m.a.young@durham.ac.uk> - 4.19.2-4
- x86: Indirect Target Selection [XSA-469, CVE-2024-28956]

* Mon Apr 07 2025 Michael Young <m.a.young@durham.ac.uk> - 4.19.2-2
- update to xen-4.19.2
  remove patches now included or superceded upstream
  remove xen*.efi.elf files to avoid debuginfo failure

* Thu Feb 27 2025 Michael Young <m.a.young@durham.ac.uk> - 4.19.1-7
- deadlock potential with VT-d and legacy PCI device pass-through
	[XSA-467, CVE-2025-1713]

* Thu Jan 23 2025 Michael Young <m.a.young@durham.ac.uk> - 4.19.1-6
- adjust file locations now /usr/sbin is a symlink to /usr/bin
- remove debugedit fix as no longer needed

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 10 2025 Jerry James <loganjerry@gmail.com> - 4.19.1-4
- OCaml 5.3.0 rebuild for Fedora 42

* Thu Jan 09 2025 Michael Young <m.a.young@durham.ac.uk> - 4.19.1-3
- work around debugedit bug to fix aarch64 builds

* Sat Jan 04 2025 Andrea Perotti <aperotti@redhat.com> - 4.19.1-2
- xen-hypervisor %post doesn't load all needed grub2 modules
	(#2335558)

* Thu Dec 05 2024 Michael Young <m.a.young@durham.ac.uk> - 4.19.1-1
- update to xen-4.19.1
  remove patches now included or superceded upstream

* Tue Nov 12 2024 Michael Young <m.a.young@durham.ac.uk> - 4.19.0-5
- Deadlock in x86 HVM standard VGA handling [XSA-463, CVE-2024-45818]
- libxl leaks data to PVH guests via ACPI tables [XSA-464, CVE-2024-45819]
- additional patches so above applies cleanly

* Tue Sep 24 2024 Michael Young <m.a.young@durham.ac.uk> - 4.19.0-4
- x86: Deadlock in vlapic_error() [XSA-462, CVE-2024-45817] (#2314782)

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 4.19.0-3
- convert license to SPDX

* Wed Aug 14 2024 Michael Young <m.a.young@durham.ac.uk> - 4.19.0-2
- error handling in x86 IOMMU identity mapping [XSA-460, CVE-2024-31145]
	(#2314784)
- PCI device pass-through with shared resources [XSA-461, CVE-2024-31146]
	(#2314783)

* Sat Aug 03 2024 Michael Young <m.a.young@durham.ac.uk> - 4.19.0-1
- update to xen-4.19.0
  rebase xen.fedora.systemd.patch, xen.efi.build.patch
  xen.ocaml5.fixes.patch and xen.gcc14.fixes.patch
  remove patches now included or superceded upstream
  now need to enable systemd explicitly 
  xentrace_format has gone, pygrub is now only in /usr/libexec/xen/bin/
  package xenwatchdogd.8.gz
  use relative links for /usr/bin/qemu-system-i386

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.18.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Michael Young <m.a.young@durham.ac.uk> - 4.18.2-4
- double unlock in x86 guest IRQ handling [XSA-458, CVE-2024-31143]
	(#2298690)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.18.2-3
- Rebuilt for Python 3.13

* Mon Jun 03 2024 Michael Young <m.a.young@durham.ac.uk> - 4.18.2-2
- x86: Native Branch History Injection [XSA-456 version 3, CVE-2024-2201]

* Tue Apr 09 2024 Michael Young <m.a.young@durham.ac.uk> - 4.18.2-1
- x86: Native Branch History Injection [XSA-456, CVE-2024-2201]
- update to xen 4.18.2, remove patches now included upstream

* Tue Apr 09 2024 Michael Young <m.a.young@durham.ac.uk> - 4.18.1-2
- x86 HVM hypercalls may trigger Xen bug check [XSA-454, CVE-2023-46842]
- x86: Incorrect logic for BTC/SRSO mitigations [XSA-455, CVE-2024-31142]

* Wed Mar 20 2024 Michael Young <m.a.young@durham.ac.uk> - 4.18.1-1
- update to xen-4.18.1
  rebase xen.gcc12.fixes.patch
  remove patches now included or superceded upstream

* Wed Mar 13 2024 Michael Young <m.a.young@durham.ac.uk> - 4.18.0-7
- x86: Register File Data Sampling [XSA-452, CVE-2023-28746]
- GhostRace: Speculative Race Conditions [XSA-453, CVE-2024-2193]
- additional patches so above applies cleanly

* Tue Feb 27 2024 Michael Young <m.a.young@durham.ac.uk> - 4.18.0-6
- x86: shadow stack vs exceptions from emulation stubs - [XSA-451,
	CVE-2023-46841] (#2266326)

* Sun Feb 04 2024 Michael Young <m.a.young@durham.ac.uk> - 4.18.0-5
- pci: phantom functions assigned to incorrect contexts [XSA-449,
        CVE-2023-46839]
- VT-d: Failure to quarantine devices in !HVM build [XSA-450,
        CVE-2023-46840]
- the glibc32 doesn't seem to add anything to the build so drop it

* Sat Feb 03 2024 Michael Young <m.a.young@durham.ac.uk> - 4.18.0-4
- build fixes for gcc14, replace stubs-32.h requirement with glibc32

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Michael Young <m.a.young@durham.ac.uk> - 4.18.0-2
- arm32: The cache may not be properly cleaned/invalidated (take two)
	[XSA-447, CVE-2023-46837]
- rebuild for OCaml-5.1.1

* Wed Nov 29 2023 Michael Young <m.a.young@durham.ac.uk> - 4.18.0-1
- update to xen-4.18.0
  rebase xen.canonicalize.patch and xen.ocaml5.fixes.patch
  remove or adjust patches now included or superceded upstream
- xencons has been dropped


* Tue Nov 14 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.2-5
- x86/AMD: mismatch in IOMMU quarantine page table levels [XSA-445,
	CVE-2023-46835]
- x86: BTC/SRSO fixes not fully effective [XSA-446, CVE-2023-46836]

* Tue Oct 10 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.2-4
- xenstored: A transaction conflict can crash C Xenstored [XSA-440,
	CVE-2023-34323]
- x86/AMD: missing IOMMU TLB flushing [XSA-442, CVE-2023-34326]
- Multiple vulnerabilities in libfsimage disk handling [XSA-443,
	CVE-2023-34325]
- x86/AMD: Debug Mask handling [XSA-444, CVE-2023-34327,
	CVE-2023-34328]

* Sun Oct 08 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.2-3
- rebuild (f40) for OCaml 5.1

* Tue Sep 26 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.2-2
- arm32: The cache may not be properly cleaned/invalidated [XSA-437,
	CVE-2023-34321]
- top-level shadow reference dropped too early for 64-bit PV guests
	[XSA-438, CVE-2023-34322]
- x86/AMD: Divide speculative information leak [XSA-439, CVE-2023-20588]

* Thu Aug 10 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.2-1
- update to xen-4.17.2 which includes
  x86/AMD: Speculative Return Stack Overflow [XSA-434, CVE-2023-20569]
  x86/Intel: Gather Data Sampling [XSA-435, CVE-2022-40982]
- remove patches now included upstream

* Tue Aug 01 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.1-9
- arm: Guests can trigger a deadlock on Cortex-A77 [XSA-436, CVE-2023-34320]
	(#2228238)

* Mon Jul 31 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.1-8
- bugfix for x86/AMD: Zenbleed [XSA-433, CVE-2023-20593]

* Tue Jul 25 2023 Michael Young <m.a.young@durham.ac.uk>
- adjust OCaml patch condition so eln builds work

* Mon Jul 24 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.1-7
- x86/AMD: Zenbleed [XSA-433, CVE-2023-20593]
- omit OCaml 5 patch on fc38

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.17.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 4.17.1-5
- Add patch for OCaml 5.0.0

* Tue Jun 27 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.1-4
- work around a build problem with python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.17.1-3
- Rebuilt for Python 3.12

* Tue May 16 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.1-2
- Mishandling of guest SSBD selection on AMD hardware
	[XSA-431, CVE-2022-42336]

* Tue May 02 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.1-1
- update to xen-4.17.1
  remove patches now included upstream
  switch from patchN to patch N format for applying patches

* Tue Apr 25 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.0-9
- x86 shadow paging arbitrary pointer dereference [XSA-430, CVE-2022-42335]

* Tue Mar 21 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.0-8
- 3 security issues (#2180425)
  x86 shadow plus log-dirty mode use-after-free [XSA-427, CVE-2022-42332]
  x86/HVM pinned cache attributes mis-handling [XSA-428, CVE-2022-42333,
	CVE-2022-42334]
  x86: speculative vulnerability in 32bit SYSCALL path [XSA-429,
	CVE-2022-42331]

* Sat Feb 18 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.0-7
- use OVMF.fd from new edk2-ovmf-xen package as ovmf.bin file
	built from edk2-ovmf package no longer supports xen (#2170930)

* Tue Feb 14 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.0-6
- x86: Cross-Thread Return Address Predictions [XSA-426, CVE-2022-27672]

* Wed Jan 25 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.0-5
- Guests can cause Xenstore crash via soft reset [XSA-425, CVE-2022-42330]
	(#2164520)

* Tue Jan 24 2023 Michael Young <m.a.young@durham.ac.uk>
- now need BuildRequires for hostname

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.0-3
- build fix for gcc13

* Sun Jan 08 2023 Michael Young <m.a.young@durham.ac.uk> - 4.17.0-2
- fix clean up of init scripts if /etc/rc.d/init.d doesn't exist

* Tue Dec 20 2022 Michael Young <m.a.young@durham.ac.uk>
-  python3-setuptools BuildRequires is needed for python 3.12

* Tue Dec 13 2022 Michael Young <m.a.young@durham.ac.uk> - 4.17.0-1
- update to xen-4.17.0
  rebase xen.fedora.systemd.patch and xen.canonicalize.patch
  remove or adjust patches now included or superceded upstream
  /var/lib/xenstored has moved to /run/xenstored

* Tue Nov 08 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.2-4
- x86: Multiple speculative security issues [XSA-422, CVE-2022-23824]

* Tue Nov 01 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.2-3
- x86: unintended memory sharing between guests [XSA-412, CVE-2022-42327]
- Xenstore: Guests can crash xenstored [XSA-414, CVE-2022-42309]
- Xenstore: Guests can create orphaned Xenstore nodes [XSA-415,
	CVE-2022-42310]
- Xenstore: guests can let run xenstored out of memory [XSA-326,
	CVE-2022-42311, CVE-2022-42312, CVE-2022-42313, CVE-2022-42314,
	CVE-2022-42315, CVE-2022-42316, CVE-2022-42317, CVE-2022-42318]
- Xenstore: Guests can cause Xenstore to not free temporary memory
	[XSA-416, CVE-2022-42319]
- Xenstore: Guests can get access to Xenstore nodes of deleted domains
	[XSA-417, CVE-2022-42320]
- Xenstore: Guests can crash xenstored via exhausting the stack
	[XSA-418, CVE-2022-42321]
- Xenstore: Cooperating guests can create arbitrary numbers of nodes
	[XSA-419, CVE-2022-42322, CVE-2022-42323]
- Oxenstored 32->31 bit integer truncation issues [XSA-420, CVE-2022-42324]
- Xenstore: Guests can create arbitrary number of nodes via transactions
	[XSA-421, CVE-2022-42325, CVE-2022-42326]

* Fri Oct 14 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.2-2
- Arm: unbounded memory consumption for 2nd-level page tables [XSA-409,
	CVE-2022-33747] (#2135268)
- P2M pool freeing may take excessively long [XSA-410, CVE-2022-33746]
	(#2135641)
- lock order inversion in transitive grant copy handling [XSA-411,
	CVE-2022-33748] (#2135263)

* Sat Sep 17 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.2-1
- update to xen-4.16.2
  remove or adjust patches now included or superceded upstream

* Tue Jul 26 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.1-8
- insufficient TLB flush for x86 PV guests in shadow mode [XSA-408,
	CVE-2022-33745] (#2112223)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.16.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 12 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.1-6
- Retbleed - arbitrary speculative code execution with return instructions
	[XSA-407, CVE-2022-23816, CVE-2022-23825, CVE-2022-29900]

* Tue Jul 05 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.1-5
- Linux disk/nic frontends data leaks [XSA-403, CVE-2022-26365,
	CVE-2022-33740, CVE-2022-33741, CVE-2022-33742] (#2104747)

* Tue Jun 21 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.1-4
- x86: MMIO Stale Data vulnerabilities [XSA-404, CVE-2022-21123,
	CVE-2022-21125, CVE-2022-21166]

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.16.1-3
- Rebuilt for Python 3.11 (F37 build only)

* Sat Jun 11 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.1-2
- stop building for ix86 and armv7hl due to missing build dependency
- x86 pv: Race condition in typeref acquisition [XSA-401, CVE-2022-26362]
- x86 pv: Insufficient care with non-coherent mappings [ XSA-402,
	CVE-2022-26363, CVE-2022-26364]
- additional patches so above applies cleanly

* Thu Apr 14 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.1-1
- update to xen-4.16.1
  remove or adjust patches now included or superceded upstream
  renumber patches
- strip .efi file to help EFI partitions with limited space

* Tue Apr 05 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.0-6
- Racy interactions between dirty vram tracking and paging log dirty
	hypercalls [XSA-397, CVE-2022-26356]
- race in VT-d domain ID cleanup [XSA-399, CVE-2022-26357]
- IOMMU: RMRR (VT-d) and unity map (AMD-Vi) handling issues [XSA-400,
	CVE-2022-26358, CVE-2022-26359, CVE-2022-26360, CVE-2022-26361]
- additional patches so above applies cleanly

* Mon Mar 21 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.0-5
- fix build of xen*.efi file and package it in /usr/lib*/efi

* Tue Mar 15 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.0-4
- Multiple speculative security issues [XSA-398]
- additional patches so above applies cleanly

* Sat Jan 29 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.0-3
- adjust build script and patches for gcc12 and package note support

* Sat Jan 29 2022 Michael Young <m.a.young@durham.ac.uk>
- arm: guest_physmap_remove_page not removing the p2m mappings [XSA-393,
	CVE-2022-23033] (#2045044)
- A PV guest could DoS Xen while unmapping a grant [XSA-394, CVE-2022-23034]
	(#2045042)
- Insufficient cleanup of passed-through device IRQs [XSA-395,
	CVE-2022-23035] (#2045040)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Michael Young <m.a.young@durham.ac.uk> - 4.16.0-1
- update to xen-4.16.0
  rebase xen.canonicalize.patch and xen.gcc11.fixes.patch
  drop xen.fedora.efi.build.patch which is no longer useful
  remove or adjust patches now included or superceded upstream
  update libxenstore libary versions
  unpackage /boot/efi/EFI/fedora/xen*.efi
  package xen-mceinj and xen-vmtrace
- don't build qemu-traditional or pv-grub by default (following upstream)
- fix some incorrect dependencies on building qemu-traditional
- change grub module package dependencies from Suggests to Recommends
	and move to hypervisor package
- rework seabios configure logic (bios.bin is no longer useful)
- frontends vulnerable to backends [XSA-376] (document change only)

* Tue Nov 23 2021 Michael Young <m.a.young@durham.ac.uk> - 4.15.1-4
- guests may exceed their designated memory limit [XSA-385, CVE-2021-28706]
- PoD operations on misaligned GFNs [XSA-388, CVE-2021-28704, CVE-2021-28707
	CVE-2021-28708]
- issues with partially successful P2M updates on x86 [XSA-389,
	CVE-2021-28705, CVE-2021-28709]
- certain VT-d IOMMUs may not work in shared page table mode [XSA-390,
	CVE-2021-28710]

* Wed Oct 06 2021 Michael Young <m.a.young@durham.ac.uk> - 4.15.1-3
- rebuild (f36 only) for OCaml 4.13.1

* Tue Oct 05 2021 Michael Young <m.a.young@durham.ac.uk> - 4.15.1-2
- PCI devices with RMRRs not deassigned correctly [XSA-386, CVE-2021-28702]
	(#2011248)

* Sun Sep 12 2021 Michael Young <m.a.young@durham.ac.uk> - 4.15.1-1
- update to xen-4.15.1
  remove or adjust patches now included or superceded upstream
  update libxencall version

* Wed Sep 08 2021 Michael Young <m.a.young@durham.ac.uk> - 4.15.0-7
- Another race in XENMAPSPACE_grant_table handling [XSA-384, CVE-2021-28701]
	(#2002786)
- bugfix for XSA-380
- stop editing grub files in /boot/efi/EFI/fedora

* Wed Aug 25 2021 Michael Young <m.a.young@durham.ac.uk> - 4.15.0-6
- IOMMU page mapping issues on x86 [XSA-378, CVE-2021-28694,
	CVE-2021-28695, CVE-2021-28696] (#1997531) (#1997568)
	(#1997537)
- grant table v2 status pages may remain accessible after de-allocation
	[XSA-379, CVE-2021-28697] (#1997520)
- long running loops in grant table handling [XSA-380, CVE-2021-28698]
	(#1997526)
- inadequate grant-v2 status frames array bounds check [XSA-382,
	CVE-2021-28699] (#1997523)
- xen/arm: No memory limit for dom0less domUs [XSA-383, CVE-2021-28700]
	(#1997527)
- grub x86_64-efi modules now go into /boot/grub2

* Thu Aug 12 2021 Michael Young <m.a.young@durham.ac.uk> - 4.15.0-5
 - work around build issue with GNU ld 2.37 (#1990344)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Michael Young <m.a.young@durham.ac.uk> - 4.15.0-3
- xen/arm: Boot modules are not scrubbed [XSA-372, CVE-2021-28693]
  (#1970542)
- inappropriate x86 IOMMU timeout detection / handling
	[XSA-373, CVE-2021-28692] (#1970540)
- Speculative Code Store Bypass [XSA-375, CVE-2021-0089, CVE-2021-26313]
	(#1970531)
- x86: TSX Async Abort protections not restored after S3
	[XSA-377, CVE-2021-28690] (#1970546)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.15.0-2
- Rebuilt for Python 3.10

* Wed May 05 2021 Michael Young <m.a.young@durham.ac.uk> - 4.15.0-1
- update to xen-4.15.0
  adjust xen.canonicalize.patch
  remove or adjust patches now included or superceded upstream
  renumber patch
  update libxendevicemodel libxenevtchn libxenforeignmemory versions
  /etc/bash_completion.d/xl.sh is now xl
  package xen-access xen-memshare xenstorepvh-stubdom.gz
	xl-pci-configuration.5.gz
- adjust xen.ocaml.4.12.fixes.patch to work with earlier ocaml
- re-copy grub modules if they have changed

* Fri Mar 19 2021 Michael Young <m.a.young@durham.ac.uk> - 4.14.1-8
- HVM soft-reset crashes toolstack [XSA-368, CVE-2021-28687] (#1940610)
- adjust efi test to stop build failing

* Tue Mar 02 2021 Michael Young <m.a.young@durham.ac.uk> - 4.14.1-6
- build fixes for OCaml 4.12.0

* Tue Feb 16 2021 Michael Young <m.a.young@durham.ac.uk> - 4.14.1-5
- Linux: display frontend "be-alloc" mode is unsupported (comment only)
	[XSA-363, CVE-2021-26934] (#1929549)
- arm: The cache may not be cleaned for newly allocated scrubbed pages
	[XSA-364, CVE-2021-26933] (#1929547)

* Mon Feb 01 2021 Michael Young <m.a.young@durham.ac.uk> - 4.14.1-4
- backport upstream zstd dom0 and guest patches
- add libzstd-devel BuildRequires
- add weak dependency on grub modules to improve initial boot setup

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Michael Young <m.a.young@durham.ac.uk> - 4.14.1-2
- IRQ vector leak on x86 [XSA-360]

* Sun Dec 20 2020 Michael Young <m.a.young@durham.ac.uk> - 4.14.1-1
- update to 4.14.1
  adjust xen.canonicalize.patch
  remove or adjust patches now included or superceded upstream
  renumber patches

* Tue Dec 15 2020 Michael Young <m.a.young@durham.ac.uk> - 4.14.0-14
- xenstore watch notifications lacking permission checks [XSA-115,
	CVE-2020-29480] (#1908091)
- Xenstore: new domains inheriting existing node permissions [XSA-322,
	CVE-2020-29481] (#1908095)
- Xenstore: wrong path length check [XSA-323, CVE-2020-29482] (#1908096)
- Xenstore: guests can crash xenstored via watchs [XSA-324, CVE-2020-29484]
	(#1908088)
- Xenstore: guests can disturb domain cleanup [XSA-325, CVE-2020-29483]
	(#1908087)
- oxenstored memory leak in reset_watches [XSA-330, CVE-2020-29485]
	(#1908000)
- undue recursion in x86 HVM context switch code [XSA-348, CVE-2020-29566]
	(#1908085)
- oxenstored: node ownership can be changed by unprivileged clients
	[XSA-352, CVE-2020-29486] (#1908003)
- oxenstored: permissions not checked on root node [XSA-353, CVE-2020-29479]
	(#1908002)
- infinite loop when cleaning up IRQ vectors [XSA-356, CVE-2020-29567]
	(#1907932)
- FIFO event channels control block related ordering [XSA-358,
	CVE-2020-29570] (#1907931)
- FIFO event channels control structure ordering [XSA-359, CVE-2020-29571]
	(#1908089)

* Sat Dec 05 2020 Jeff Law <law@redhat.com> - 4.14.0-13
- Work around another gcc-11 stringop-overflow diagnostic

* Tue Nov 24 2020 Michael Young <m.a.young@durham.ac.uk> - 4.14.0-12
- stack corruption from XSA-346 change [XSA-355]

* Mon Nov 23 2020 Michael Young <m.a.young@durham.ac.uk> - 4.14.0-11
- support zstd compressed kernels (dom0 only) based on linux kernel code

* Tue Nov 10 2020 Michael Young <m.a.young@durham.ac.uk> - 4.14.0-10
- Information leak via power sidechannel [XSA-351, CVE-2020-28368]
	(#1897146)
- add make as build requires

* Tue Nov 03 2020 Michael Young <m.a.young@durham.ac.uk> - 4.14.0-9
- revised patch for XSA-286 (mitigating performance impact)

* Fri Oct 30 2020 Jeff Law <law@redhat.com> - 4.14.0-8
- Work around gcc-11 stringop-overflow diagnostics as well

* Wed Oct 28 2020 Michael Young <m.a.young@durham.ac.uk> - 4.14.0-7
- x86 PV guest INVLPG-like flushes may leave stale TLB entries
	[XSA-286, CVE-2020-27674] (#1891092)
- simplify grub scripts (patches from Thierry Vignaud <tvignaud@redhat.com>)
- some fixes for gcc 11

* Tue Oct 20 2020 Michael Young <m.a.young@durham.ac.uk> - 4.14.0-6
- x86: Race condition in Xen mapping code [XSA-345, CVE-2020-27672]
	(#1891097)
- undue deferral of IOMMU TLB flushes [XSA-346, CVE-2020-27671]
	(#1891093)
- unsafe AMD IOMMU page table updates [XSA-347, CVE-2020-27670]
	(#1891088)

* Tue Sep 22 2020 Michael Young <m.a.young@durham.ac.uk> - 4.14.0-5
- x86 pv: Crash when handling guest access to MSR_MISC_ENABLE [XSA-333,
	CVE-2020-25602] (#1881619)
- Missing unlock in XENMEM_acquire_resource error path [XSA-334,
	CVE-2020-25598] (#1881616)
- race when migrating timers between x86 HVM vCPU-s [XSA-336,
	CVE-2020-25604] (#1881618)
- PCI passthrough code reading back hardware registers [XSA-337,
	CVE-2020-25595] (#1881587)
- once valid event channels may not turn invalid [XSA-338, CVE-2020-25597]
	(#1881588)
- x86 pv guest kernel DoS via SYSENTER [XSA-339, CVE-2020-25596]
	(#1881617)
- Missing memory barriers when accessing/allocating an event channel [XSA-340,
	CVE-2020-25603] (#1881583)
- out of bounds event channels available to 32-bit x86 domains [XSA-342,
	CVE-2020-25600] (#1881582)
- races with evtchn_reset() [XSA-343, CVE-2020-25599] (#1881581)
- lack of preemption in evtchn_reset() / evtchn_destroy() [XSA-344,
	CVE-2020-25601] (#1881586)

* Thu Sep 03 2020 Michael Young <m.a.young@durham.ac.uk> - 4.14.0-4
- rebuild for OCaml 4.11.1

* Mon Aug 24 2020 Michael Young <m.a.young@durham.ac.uk> - 4.14.0-3
- QEMU: usb: out-of-bounds r/w access issue [XSA-335, CVE-2020-14364]
	(#1871850)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 26 2020 Michael Young <m.a.young@durham.ac.uk> - 4.14.0-1
- update to 4.14.0
  remove or adjust patches now included or superceded upstream
  adjust xen.hypervisor.config
  bison and flex packages now needed for hypervisor build
  /usr/bin/vchan-socket-proxy and /usr/sbin/xenhypfs have been added
	with associated libraries and man page
- re-enable pandoc for more documentation
  adding xen-vbd-interface.7.gz
- revise documentation build dependencies
  drop tex, texinfo, ghostscript, graphviz, discount
  add perl(Pod::Html) perl(File::Find)
- additional build dependency for ocaml on perl(Data::Dumper)

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 4.13.1-5
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jul 07 2020 Michael Young <m.a.young@durham.ac.uk> - 4.13.1-4
- incorrect error handling in event channel port allocation leads to
	DoS [XSA-317, CVE-2020-15566] (#1854465)
- inverted code paths in x86 dirty VRAM tracking leads to DoS
	[XSA-319, CVE-2020-15563] (#1854463)
- xen: insufficient cache write-back under VT-d leads to DoS
	[XSA-321, CVE-2020-15565] (#1854467)
- missing alignment check in VCPUOP_register_vcpu_info leads to DoS
	[XSA-327, CVE-2020-15564] (#1854458)
- non-atomic modification of live EPT PTE leads to DoS
	[XSA-328, CVE-2020-15567] (#1854464)

* Tue Jun 30 2020 Jeff Law <law@redhat.com>
Disable LTO

* Wed Jun 10 2020 Michael Young <m.a.young@durham.ac.uk> - 4.13.1-3
- Special Register Buffer speculative side channel [XSA-320]

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.13.1-2
- Rebuilt for Python 3.9

* Tue May 19 2020 Michael Young <m.a.young@durham.ac.uk> - 4.13.1-1
- update to 4.13.1
  remove patches now included or superceded upstream

* Tue May 05 2020 Michael Young <m.a.young@durham.ac.uk> - 4.13.0-8
- build aarch64 hypervisor with -mno-outline-atomics to fix gcc 10 build

* Tue Apr 14 2020 Michael Young <m.a.young@durham.ac.uk> - 4.13.0-7
- multiple xenoprof issues [XSA-313, CVE-2020-11740, CVE-2020-11741]
	(#1823912, #1823914)
- Missing memory barriers in read-write unlock paths [XSA-314,
	CVE-2020-11739] (#1823784)
- Bad error path in GNTTABOP_map_grant [XSA-316, CVE-2020-11743] (#1823926)
- Bad continuation handling in GNTTABOP_copy [XSA-318, CVE-2020-11742]
	(#1823943)

* Tue Mar 17 2020 Michael Young <m.a.young@durham.ac.uk> - 4.13.0-6
- fix issues in pygrub dependency found by python 3.8

* Tue Mar 10 2020 Michael Young <m.a.young@durham.ac.uk> - 4.13.0-5
- setting for --with-system-ipxe should be a rom file (#1778516)
- add weak depends on ipxe-roms-qemu and qemu-system-x86-core

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Michael Young <m.a.young@durham.ac.uk> - 4.13.0-3
- build fixes for OCaml 4.10.0 and gcc 10

* Tue Jan 14 2020 Michael Young <m.a.young@durham.ac.uk> - 4.13.0-2
- arm: a CPU may speculate past the ERET instruction [XSA-312]
- use more explicit library names
- add weak requires for perl (/etc/xen/scripts/locking.sh)

* Wed Dec 18 2019 Michael Young <m.a.young@durham.ac.uk> - 4.13.0-1
- update to 4.13.0
  remove patches now included or superceded upstream
  adjust xen.hypervisor.config
  /usr/sbin/xen-tmem-list-parse has been removed
  pkgconfig files have moved to %%{_libdir}/pkgconfig
  /usr/sbin/xen-ucode has been added (x86 only)

* Sun Dec 15 2019 Michael Young <m.a.young@durham.ac.uk> - 4.12.1-9
- fix build with OCaml 4.09.0

* Wed Dec 11 2019 Michael Young <m.a.young@durham.ac.uk> - 4.12.1-8
- denial of service in find_next_bit() [XSA-307, CVE-2019-19581,
	CVE-2019-19582] (#1782211)
- denial of service in HVM/PVH guest userspace code [XSA-308,
	CVE-2019-19583] (#1782206)
- privilege escalation due to malicious PV guest [XSA-309, CVE-2019-19578]
	(#1782210)
- Further issues with restartable PV type change operations [XSA-310,
	CVE-2019-19580] (#1782207)
- vulnerability in dynamic height handling for AMD IOMMU pagetables
	[XSA-311, CVE-2019-19577] (#1782208)
- add patches needed to apply XSA-311

* Tue Nov 26 2019 Michael Young <m.a.young@durham.ac.uk> - 4.12.1-7
- Device quarantine for alternate pci assignment methods [XSA-306,
	CVE-2019-19579] (#1780559)

* Tue Nov 12 2019 Michael Young <m.a.young@durham.ac.uk> - 4.12.1-6
- add missing XSA-299 patches

* Tue Nov 12 2019 Michael Young <m.a.young@durham.ac.uk> - 4.12.1-5
- x86: Machine Check Error on Page Size Change DoS [XSA-304, CVE-2018-12207]
- TSX Asynchronous Abort speculative side channel [XSA-305, CVE-2019-11135]

* Thu Oct 31 2019 Michael Young <m.a.young@durham.ac.uk> - 4.12.1-4
- VCPUOP_initialise DoS [XSA-296, CVE-2019-18420] (#1771368)
- missing descriptor table limit checking in x86 PV emulation [XSA-298,
	CVE-2019-18425] (#1771341)
- Issues with restartable PV type change operations [XSA-299, CVE-2019-18421]
	(#1767726)
- add-to-physmap can be abused to DoS Arm hosts [XSA-301, CVE-2019-18423]
	(#1771345)
- passed through PCI devices may corrupt host memory after deassignment
	[XSA-302, CVE-2019-18424] (#1767731)
- ARM: Interrupts are unconditionally unmasked in exception handlers
	[XSA-303, CVE-2019-18422] (#1771443)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.12.1-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.12.1-2
- Rebuilt for Python 3.8

* Fri Aug 09 2019 Michael Young <m.a.young@durham.ac.uk> - 4.12.1-1
- update to 4.12.1
  remove patches for issues now fixed upstream
  adjust xen.gcc9.fixes.patch

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 19 2019 Michael Young <m.a.young@durham.ac.uk> - 4.12.0-4
- Unlimited Arm Atomics Operations [XSA-295, CVE-2019-17349,
	CVE-2019-17350] (#1720760)
- some debug files are now properly packaged in debuginfo rpms

* Tue Jun 18 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl>
- Fix build with python3.8 (#1704807)

* Sat Jun 01 2019 Michael Young <m.a.young@durham.ac.uk> - 4.12.0-3
- fix HVM DomU boot on some chipsets
- fix expected FTBFS with Python 3.8 (#1704807)
- adjust grub2 workaround

* Tue May 14 2019 Michael Young <m.a.young@durham.ac.uk> - 4.12.0-2
- Microarchitectural Data Sampling speculative side channel [XSA-297,
	CVE-2018-12126, CVE-2018-12127, CVE-2018-12130, CVE-2019-11091]
- additional patches so above applies cleanly
- work around grub2 issues in dom0

* Fri Apr 05 2019 Michael Young <m.a.young@durham.ac.uk> - 4.12.0-1
- update to 4.12.0 (#1694695)
  remove patches for issues now fixed upstream
  replace xen.use.fedora.ipxe.patch with --with-system-ipxe
  drop xen.glibcfix.patch xen.gcc8.temp.fix.patch which are no longer needed
  adjust xen.python.env.patch xen.gcc9.fixes.patch
  xen.hypervisor.config refresh
  kdd is now xen-kdd, xenmon.py is now xenmon, fsimage.so is now xenfsimage.so
  fs libdir is now xenfsimage libdir
  xen-ringwatch xen-bugtool have been dropped
- remove remaining traces of efiming and efi_flags logic
- switch from python2 to python3
- drop systemd_postun and renumber patches

* Tue Mar 05 2019 Michael Young <m.a.young@durham.ac.uk> - 4.11.1-4
- xen: various flaws (#1685577)
  grant table transfer issues on large hosts [XSA-284, CVE-2019-17340]
  race with pass-through device hotplug [XSA-285, CVE-2019-17341]
  x86: steal_page violates page_struct access discipline
	[XSA-287, CVE-2019-17342]
  x86: Inconsistent PV IOMMU discipline [XSA-288, CVE-2019-17343]
  missing preemption in x86 PV page table unvalidation
	[XSA-290, CVE-2019-17344]
  x86/PV: page type reference counting issue with failed IOMMU update
	[XSA-291, CVE-2019-17345]
  x86: insufficient TLB flushing when using PCID [XSA-292, CVE-2019-17346]
  x86: PV kernel context switch corruption [XSA-293, CVE-2019-17347]
  x86 shadow: Insufficient TLB flushing when using PCID [XSA-294,
	CVE-2019-17348]

* Thu Feb 14 2019 Michael Young <m.a.young@durham.ac.uk> - 4.11.1-3
- add gcc9 build fixes (#1676229)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 11 2018 Michael Young <m.a.young@durham.ac.uk> - 4.11.1-1
- update to 4.11.1
  remove patches for issues now fixed upstream
  adjust xen.use.fedora.ipxe.patch
- only include qemutrad build requirements for platforms that use it
- construct ovmf.bin from edk2-ovmf package (#1656651)

* Tue Nov 20 2018 Michael Young <m.a.young@durham.ac.uk> - 4.11.0-10
- insufficient TLB flushing / improper large page mappings with AMD IOMMUs
	[XSA-275, CVE-2018-19961, CVE-2018-19962] (#1651665)
- x86: DoS from attempting to use INVPCID with a non-canonical addresses
	[XSA-279, CVE-2018-19965] (#1651970)
- xen: various flaws (#1652251)
  resource accounting issues in x86 IOREQ server handling
	[XSA-276, CVE-2018-19963]
  x86: incorrect error handling for guest p2m page removals
	[XSA-277, CVE-2018-19964]
  Fix for XSA-240 conflicts with shadow paging [XSA-280, CVE-2018-19966]

* Tue Nov 06 2018 Michael Young <m.a.young@durham.ac.uk> - 4.11.0-9
- guest use of HLE constructs may lock up host [XSA-282, CVE-2018-19967]

* Wed Oct 24 2018 Michael Young <m.a.young@durham.ac.uk> - 4.11.0-8
- x86: Nested VT-x usable even when disabled [XSA-278, CVE-2018-18883]
	(#1643118)

* Tue Sep 18 2018 Michael Young <m.a.young@durham.ac.uk> - 4.11.0-7
- set /usr/bin/python2 at the start of another python script

* Tue Sep 18 2018 Michael Young <m.a.young@durham.ac.uk> - 4.11.0-6
- move pkgconfig files to xen-devel (#1629643)

* Wed Sep 12 2018 Michael Young <m.a.young@durham.ac.uk>
- set /usr/bin/python2 at the start of some python scripts

* Thu Aug 23 2018 Michael Young <m.a.young@durham.ac.uk> - 4.11.0-5
- move creation of /usr/lib/xen symlink to posttrans to avoid rpm conflict

* Fri Aug 17 2018 Michael Young <m.a.young@durham.ac.uk> - 4.11.0-4
- move files from /usr/lib/xen to /usr/libexec/xen
- create symlink at /usr/lib/xen for compatibility

* Tue Aug 14 2018 Michael Young <m.a.young@durham.ac.uk> - 4.11.0-3
- replace use of deprecated vwprintw

* Tue Aug 14 2018 Michael Young <m.a.young@durham.ac.uk> - 4.11.0-2
- no longer need to set python_sitearch
- L1 Terminal Fault speculative side channel patch bundle [XSA-273,
	CVE-2018-3620, CVE-2018-3646]
  also includes
  Use of v2 grant tables may cause crash on ARM [XSA-268, CVE-2018-15469]
	(#1616081)
  x86: Incorrect MSR_DEBUGCTL handling lets guests enable BTS [XSA-269,
	CVE-2018-15468] (#1616077)
  oxenstored does not apply quota-maxentity [XSA-272, CVE-2018-15470]
	(#1616080)

* Thu Jul 12 2018 Michael Young <m.a.young@durham.ac.uk> - 4.11.0-1
- update to 4.11.0 (#1592976)
  remove patches for issues now fixed upstream
  adjust xen.use.fedora.ipxe.patch
  drop parts of xen.fedora.efi.build.patch & xen.gcc8.temp.fix.patch
- replace use of deprecated brctl command (#1588712)
- add gcc BuildRequires
- adjustments now /usr/bin/python is in a separate package
- update hypervisor configuration for arm
- put back some gcc fixes needed for arm and i686
- work around a build issue with perl
- i686 now want to build EFI hypervisor (actually x86_64) so let it

* Wed Jun 27 2018 Michael Young <m.a.young@durham.ac.uk> - 4.10.1-5
- preemption checks bypassed in x86 PV MM handling [XSA-264, CVE-2018-12891]
	(#1595959)
- x86: #DB exception safety check can be triggered by a guest [XSA-265,
	CVE-2018-12893] (#1595958)
- libxl fails to honour readonly flag on HVM emulated SCSI disks [XSA-266,
	CVE-2018-12892] (#1595957)

* Fri Jun 15 2018 Michael Young <m.a.young@durham.ac.uk> - 4.10.1-4
- Speculative register leakage from lazy FPU context switching
	[XSA-267, CVE-2018-3665]
- fix for change in iasl output

* Tue May 22 2018 Michael Young <m.a.young@durham.ac.uk> - 4.10.1-3
- Speculative Store Bypass [XSA-263, CVE-2018-3639]
	(with extra patches so it applies cleanly)

* Tue May 08 2018 Michael Young <m.a.young@durham.ac.uk> - 4.10.1-2
- x86: mishandling of debug exceptions [XSA-260, CVE-2018-8897]
- x86 vHPET interrupt injection errors [XSA-261, CVE-2018-10982] (#1576089)
- qemu may drive Xen into unbounded loop [XSA-262, CVE-2018-10981] (#1576680)

* Thu May 03 2018 Michael Young <m.a.young@durham.ac.uk> - 4.10.1-1
- update to xen-4.10.1
  adjust xen.use.fedora.ipxe.patch and xen.fedora.efi.build.patch
  remove patches for issues now fixed upstream
  package /usr/lib/debug/usr/lib/xen/boot/xen-shim-syms

* Wed Apr 25 2018 Michael Young <m.a.young@durham.ac.uk> - 4.10.0-9
- Information leak via crafted user-supplied CDROM [XSA-258, CVE-2018-10472]
	(#1571867)
- x86: PV guest may crash Xen with XPTI [XSA-259, CVE-2018-10471] (#1571878)

* Fri Mar 09 2018 Michael Young <m.a.young@durham.ac.uk> - 4.10.0-8
- fix safe-strings patch for OCaml 4.0.6

* Sun Mar 04 2018 Michael Young <m.a.young@durham.ac.uk> - 4.10.0-7
- avoid building parts of xen twice
- hypervisor built with -fcf-protection doesn't work on x86_64

* Wed Feb 28 2018 Michael Young <m.a.young@durham.ac.uk> - 4.10.0-6
- update patch for XPTI mitigation for XSA-254
- add Branch Target Injection (BTI) mitigation for XSA-254
- DoS via non-preemptable L3/L4 pagetable freeing [XSA-252, CVE-2018-7540]
	(#1549568)
- grant table v2 -> v1 transition may crash Xen [XSA-255, CVE-2018-7541]
	(#1549570)
- x86 PVH guest without LAPIC may DoS the host [XSA-256, CVE-2018-7542]
	(#1549572)
- further build issue fixes with gcc8 (some temporary workarounds)
- -mcet and -fcf-protection aren't recognized in hypervisor build x86_64 on
	i686 either

* Fri Feb 23 2018 Michael Young <m.a.young@durham.ac.uk>
- fix some build issues with gcc8

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.10.0-5
- Escape macros in %%changelog

* Sun Feb 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.10.0-4
- Switch to %%ldconfig_scriptlets

* Sun Jan 14 2018 Michael Young <m.a.young@durham.ac.uk> - 4.10.0-3
- fix typo in annobin build fix
- add 4.10.0-shim-comet-3 shim mitigation for [XSA-254, CVE-2017-5753,
	CVE-2017-5715, CVE-2017-5754] + build fixes
  XSA-253 patch included in comet patches
  CONFIG_XEN_GUEST line needed xen.hypervisor.config for comet
  delay and adjust xen.use.fedora.ipxe.patch and xen.fedora.efi.build.patch
  package /usr/lib/xen/boot/xen-shim
- add Xen page-table isolation (XPTI) mitigation for XSA-254
- -fstack-clash-protection isn't recognized in hypervisor build x86_64 on i686
- __python macro is no longer set, replace by /usr/bin/python2

* Thu Jan 04 2018 Michael Young <m.a.young@durham.ac.uk> - 4.10.0-2
- x86: memory leak with MSR emulation [XSA-253, CVE-2018-5244] (#1531110)

* Mon Dec 18 2017 Michael Young <m.a.young@durham.ac.uk> - 4.10.0-1
- renumber patches
- fix build with OCaml 4.0.6 (#1526703)
- disable annobin for x86_64 hypervisor to allow it to build

* Mon Dec 18 2017 Michael Young <m.a.young@durham.ac.uk>
- allow building without hypervisor, docs, qemu-xen-traditional or stubdoms
- fix build without ocaml

* Mon Dec 18 2017 Michael Young <m.a.young@durham.ac.uk>
- update to 4.10.0
  adjust xen.use.fedora.ipxe.patch
  update xen.hypervisor.config
  remove patches for issues now fixed upstream
  tapdisk* qcow-create qcow2raw img2qcow utilities have been dropped
  lock-util tap-ctl td-util vhd-* utilities have been dropped
  package xen-diag and extra manual pages
- iasl BuildRequires is now in acpica-tools

* Tue Dec 12 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.1-4
- another patch related to the [XSA-240, CVE-2017-15595] issue
- xen: various flaws (#1525018)
  x86 PV guests may gain access to internally used page
	[XSA-248, CVE-2017-17566]
  broken x86 shadow mode refcount overflow check [XSA-249, CVE-2017-17563]
  improper x86 shadow mode refcount error handling [XSA-250, CVE-2017-17564]
  improper bug check in x86 log-dirty handling [XSA-251, CVE-2017-17565]

* Sat Dec 02 2017 Richard W.M. Jones <rjones@redhat.com> - 4.9.1-3
- OCaml 4.06.0 rebuild.

* Tue Nov 28 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.1-2
- xen: various flaws (#1518214)
  x86: infinite loop due to missing PoD error checking [XSA-246, CVE-2017-17044]
  Missing p2m error checking in PoD code [XSA-247, CVE-2017-17045]

* Thu Nov 23 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.1-1
- update to 4.9.1 (#1515818)
  adjust xen.use.fedora.ipxe.patch
  and qemu.git-fec5e8c92becad223df9d972770522f64aafdb72.patch
  remove patches for issues now fixed upstream and parts of xen.gcc7.fix.patch
  update xen.hypervisor.config
- update Source0 location

* Wed Nov 15 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.0-14
- fix an issue in patch for [XSA-240, CVE-2017-15595] that might be a
	security issue
- fix for [XSA-243, CVE-2017-15592] could cause hypervisor crash (DOS)

* Thu Oct 26 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.0-13
- pin count / page reference race in grant table code [XSA-236, CVE-2017-15597]
	(#1506693)

* Thu Oct 12 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.0-12
- xen: various flaws (#1501391)
  multiple MSI mapping issues on x86 [XSA-237, CVE-2017-15590]
  DMOP map/unmap missing argument checks [XSA-238, CVE-2017-15591]
  hypervisor stack leak in x86 I/O intercept code [XSA-239, CVE-2017-15589]
  Unlimited recursion in linear pagetable de-typing [XSA-240, CVE-2017-15595]
  Stale TLB entry due to page type release race [XSA-241, CVE-2017-15588]
  page type reference leak on x86 [XSA-242, CVE-2017-15593]
  x86: Incorrect handling of self-linear shadow mappings with translated
	 guests [XSA-243, CVE-2017-15592]
  x86: Incorrect handling of IST settings during CPU hotplug [XSA-244,
	CVE-2017-15594]

* Sun Oct 01 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.0-11
- ARM: Some memory not scrubbed at boot [XSA-245, CVE-2017-17046] (#1499843)
- Qemu: vga: reachable assert failure during during display update
	[CVE-2017-13673] (#1486591)
- Qemu: vga: OOB read access during display update [CVE-2017-13672] (#1486562)

* Tue Sep 12 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.0-10
- xen: various flaws (#1490884)
  Missing NUMA node parameter verification [XSA-231, CVE-2017-14316]
  Missing check for grant table [XSA-232, CVE-2017-14318]
  cxenstored: Race in domain cleanup [XSA-233, CVE-2017-14317]
  insufficient grant unmapping checks for x86 PV guests
	[XSA-234, CVE-2017-14319]

* Tue Aug 29 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.0-9
- Qemu: usb: ohci: infinite loop due to incorrect return value [CVE-2017-9330]
	(#1457698)
- Qemu: nbd: segmentation fault due to client non-negotiation [CVE-2017-9524]
	(#1460173)
- Qemu: qemu-nbd: server breaks with SIGPIPE upon client abort [CVE-2017-10664]
	(#1466466)
- Qemu: exec: oob access during dma operation [CVE-2017-11334] (#1471640)
- revised full fix for XSA-226 (regressed 32-bit Dom0 or backend domains)

* Wed Aug 23 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.0-8
- full fix for XSA-226, replacing workaround
- drop conflict of xendomain and libvirtd as can cause problems (#1398590)
- add-to-physmap error paths fail to release lock on ARM [XSA-235] (#1484476)
- Qemu: audio: host memory leakage via capture buffer [CVE-2017-8309]
	(#1446521)
- Qemu: input: host memory leakage via keyboard events [CVE-2017-8379]
	(#1446561)

* Tue Aug 15 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.0-7
- xen: various flaws (#1481765)
  multiple problems with transitive grants [XSA-226, CVE-2017-12135]
  x86: PV privilege escalation via map_grant_ref [XSA-227, CVE-2017-12137]
  grant_table: Race conditions with maptrack free list handling
	[XSA-228, CVE-2017-12136]
  grant_table: possibly premature clearing of GTF_writing / GTF_reading
	[XSA-230, CVE-2017-12855]

* Sat Aug 12 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.0-6
- files in /usr/lib/debug are not just in efi builds

* Sat Aug 12 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.0-5
- rebuild for ocaml

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.0-3
- Qemu: serial: host memory leakage 16550A UART emulation [CVE-2017-5579]
	(#1416162)
- Qemu: display: cirrus: OOB read access issue [CVE-2017-7718] (#1443444)
- package some files now in /usr/lib/debug

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 14 2017 Michael Young <m.a.young@durham.ac.uk> - 4.9.0-1
- update to 4.9.0 (#1465707)
  adjust xen.use.fedora.ipxe.patch, xen.fedora.efi.build.patch
  and xen.canonicalize.patch
  remove patches for issues now fixed upstream and parts of xen.gcc7.fix.patch
  package new manual pages
- make python dependencies explicitly version 2
- switch xen-doc subpackage to noarch
- require perl-interpreter instead of perl for packaging policy change

* Tue Jun 27 2017 Richard W.M. Jones <rjones@redhat.com> - 4.8.1-5
- Rebuild for OCaml 4.04.2.

* Tue Jun 20 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.1-4
- xen: various flaws (#1463247)
  blkif responses leak backend stack data [XSA-216]
  page transfer may allow PV guest to elevate privilege [XSA-217]
  Races in the grant table unmap code [XSA-218]
  x86: insufficient reference counts during shadow emulation [XSA-219]
  x86: PKRU and BND* leakage between vCPU-s [XSA-220]
  NULL pointer deref in event channel poll [XSA-221] (#1463231)
  stale P2M mappings due to insufficient error checking [XSA-222]
  ARM guest disabling interrupt may crash Xen [XSA-223]
  grant table operations mishandle reference counts [XSA-224]
  arm: vgic: Out-of-bound access when sending SGIs [XSA-225]

* Mon May 15 2017 Richard W.M. Jones <rjones@redhat.com> - 4.8.1-3
- Rebuild for OCaml 4.04.1.

* Wed May 03 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.1-2
- xen: various flaws (#1447345)
  x86: 64bit PV guest breakout via pagetable use-after-mode-change [XSA-213]
  grant transfer allows PV guest to elevate privileges [XSA-214]

* Mon Apr 10 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.1-1
- update to xen-4.8.1
  adjust xen.use.fedora.ipxe.patch, qemu.trad.bug1399055.patch
	and qemu.git-4299b90e9ba9ce5ca9024572804ba751aa1a7e70.patch
  remove upstream patches
  renumber patches

* Wed Apr 05 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.0-13
- gcc7 build fix for arm

* Tue Apr 04 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.0-12
- gcc7 build fix for i686
- proposed upstream fix for [XSA-206] build issue
- Qemu: 9pfs: host memory leakage via v9fs_create [CVE-2017-7377] (#1437873)
- x86: broken check in memory_exchange() permits PV guest breakout
	[XSA-212, CVE-2017-7228] (#1438804)

* Wed Mar 29 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.0-11
- add additional patch for [XSA-206] (#1436690)
- gcc7 build fix for [XSA-206]

* Tue Mar 28 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.0-10
- xenstore denial of service via repeated update [XSA-206] (#1436690)

* Thu Mar 16 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.0-9
- Cirrus VGA Heap overflow via display refresh [XSA-211, CVE-2016-9603]
	(#1432041)
- Qemu: usb: an infinite loop issue in ohci_service_ed_list [CVE-2017-6505]
	(#1429433)

* Wed Mar 01 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.0-8
- make sure efi isn't built on i686

* Wed Mar 01 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.0-7
- actually include one of the XSA-209 patches
- mingw64-binutils no longer needed for building efi for x86_64 on fc26+
- canonicalize is now a maths function in ISO C so rename use in xenstore
	(#1422460)

* Sat Feb 25 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.0-6
- update patches for XSA-209
- arm: memory corruption when freeing p2m pages [XSA-210] (#1426327)

* Wed Feb 22 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.0-5
- cirrus_bitblt_cputovideo does not check if memory region is safe
	[XSA-209, CVE-2017-2620] (#1425420)

* Wed Feb 15 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.0-4
- patch to build with gcc7
- memory leak when destroying guest without PT devices [XSA-207] (#1422492)
- update patches for XSA-208 after upstream revision (no functional change)

* Fri Feb 10 2017 Michael Young <m.a.young@durham.ac.uk> - 4.8.0-3
- Qemu: net: mcf_fec: infinite loop while receiving data in mcf_fec_receive
	[CVE-2016-9776]
- Qemu: audio: memory leakage in ac97 [CVE-2017-5525] (#1414111)
- Qemu: audio: memory leakage in es1370 device [CVE-2017-5526] (#1414211)
- oob access in cirrus bitblt copy [XSA-208, CVE-2017-2615] (#1418243)

* Wed Dec 21 2016 Michael Young <m.a.young@durham.ac.uk> - 4.8.0-2
- qemu ioport array overflow [XSA-199, CVE-2016-9637]
- two security flaws (#1406840)
  x86 PV guests may be able to mask interrupts [XSA-202, CVE-2016-10024]
  x86: missing NULL pointer check in VMFUNC emulation [XSA-203, CVE-2016-10025]
- x86: Mishandling of SYSCALL singlestep during emulation [XSA-204,
	CVE-2016-10013] (#1406260)

* Wed Dec 07 2016 Michael Young <m.a.young@durham.ac.uk> - 4.8.0-1
- update to xen-4.8.0 (#1401490)
  includes fix for [XSA-201, CVE-2016-9815, CVE-2016-9816, CVE-2016-9817,
	CVE-2016-9818] (#1399747)
  adjust xen.use.fedora.ipxe.patch, xen.fedora.efi.build.patch,
	xen.fedora.systemd.patch and xen.hypervisor.config
  use upstream xendriverdomain systemd script
  remove upstream patches
  xenstored.*socket and gtrace* are no longer built
  renumber patches
- add armv7hl and aarch64 builds (experimental in Fedora)
- qemu: Divide by zero vulnerability in cirrus_do_copy (#1399055)
	[CVE-2016-9921, CVE-2016-9922]
- Qemu: 9pfs: memory leakage via proxy/handle callbacks (#1402278)

* Tue Nov 22 2016 Michael Young <m.a.young@durham.ac.uk> - 4.7.1-3
- xen : various security flaws (#1397383)
  x86 null segments not always treated as unusable [XSA-191, CVE-2016-9386]
  x86 task switch to VM86 mode mis-handled [XSA-192, CVE-2016-9382]
  x86 segment base write emulation lacking canonical address checks [XSA-193,
	CVE-2016-9385]
  guest 32-bit ELF symbol table load leaking host data [XSA-194, CVE-2016-9384]
  x86 64-bit bit test instruction emulation broken [XSA-195, CVE-2016-9383]
  x86 software interrupt injection mis-handled [XSA-196, CVE-2016-9377,
	CVE-2016-9378]
  qemu incautious about shared ring processing [XSA-197, CVE-2016-9381]
  delimiter injection vulnerabilities in pygrub [XSA-198, CVE-2016-9379,
	CVE-2016-9380]

* Mon Nov 14 2016 Richard W.M. Jones <rjones@redhat.com> - 4.7.1-2
- Rebuild for OCaml 4.04.0.

* Mon Nov 07 2016 Michael Young <m.a.young@durham.ac.uk> - 4.7.1-1
- update to xen-4.7.1
  adjust xen.use.fedora.ipxe.patch
  remove upstream patches

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 4.7.0-8
- Rebuild for OCaml 4.04.0.

* Sun Oct 30 2016 Michael Young <m.a.young@durham.ac.uk> - 4.7.0-7
- Qemu: usb: xHCI: infinite loop vulnerability in xhci_ring_fetch
	[CVE-2016-8576] (#1382323)
- Qemu: 9pfs: host memory leakage in v9fs_read [CVE-2016-8577] (#1383287)
- Qemu: 9pfs: allocate space for guest originated empty strings [CVE-2016-8578]
	(#1383293)
- Qemu: char: divide by zero error in serial_update_parameters [CVE-2016-8669]
	(#1384910)
- Qemu: net: rtl8139: infinite loop while transmit in C+ mode [CVE-2016-8910]
	(#1388048)
- qemu-kvm: Infinite loop vulnerability in a9_gtimer_update() (#1388301)
- Qemu: 9pfs: information leakage via xattr [CVE-2016-9103] (#1389644)
- Qemu: 9pfs: memory leakage when creating extended attribute [CVE-2016-9102]
	(#1389552)
- Qemu: 9pfs: memory leakage in v9fs_link [CVE-2016-9105] (#1389705)
- Qemu: 9pfs: memory leakage in v9fs_write [CVE-2016-9106] (#1389714)
- Qemu: 9pfs: integer overflow leading to OOB access [CVE-2016-9104] (#1389689)

* Tue Oct 04 2016 Michael Young <m.a.young@durham.ac.uk> - 4.7.0-6
- enable xen livepatch in hypervisor via .config file
- qemu-kvm: Directory traversal flaw in 9p virtio backend [CVE-2016-7116]
	(#1371400)
- qemu: hw: net: Heap overflow in xlnx.xps-ethernetlite [CVE-2016-7161]
	(#1379299)
- CR0.TS and CR0.EM not always honored for x86 HVM guest [XSA-190,
	CVE-2016-7777] (#1381576)

* Thu Sep 08 2016 Michael Young <m.a.young@durham.ac.uk> - 4.7.0-5
- pandoc (documentation) has dependency issues again on F25

* Thu Sep 08 2016 Michael Young <m.a.young@durham.ac.uk> - 4.7.0-4
- fix build problem with glibc 2.24
- x86: Disallow L3 recursive pagetable for 32-bit PV guests [XSA-185,
	CVE-2016-7092] (#1374470)
- x86: Mishandling of instruction pointer truncation during emulation
	[XSA-186, CVE-2016-7093] (#1374471)
- x86 HVM: Overflow of sh_ctxt->seg_reg[] [XSA-187, CVE-2016-7094] (#1374473)

* Wed Aug 10 2016 Michael Young <m.a.young@durham.ac.uk> - 4.7.0-3
- replace xendriverdomain sysvinit script with a systemd file (#1361324)

* Wed Jul 27 2016 Michael Young <m.a.young@durham.ac.uk> - 4.7.0-2
- x86: Privilege escalation in PV guests [XSA-182, CVE-2016-6258] (#1360358)
- x86: Missing SMAP whitelisting in 32-bit exception / event delivery
	[XSA-183, CVE-2016-6259] (#1360359)
- virtio: unbounded memory allocation issue [XSA-184, CVE-2016-5403] (#1360831)
- Qemu: scsi: esp: OOB write access in esp_do_dma [CVE-2016-6351] (#1360599)


* Fri Jul 22 2016 Michael Young <m.a.young@durham.ac.uk> - 4.7.0-1
- update to xen-4.7.0
  adjust xen.use.fedora.ipxe.patch, xen.fedora.efi.build.patch,
    qemu.CVE-2016-2391.patch, qemu.CVE-2016-4002.patch
    and qemu.bug1330513.patch
  package extra files 
    /usr/bin/xen-cpuid
    /usr/sbin/xen-livepatch
    /boot/xen*.config
  remove upstream patches
- set RPM_OPT_FLAGS options in command line rather than patches, similarly
    remove xen.64.bit.hyp.on.ix86.patch, also xen.gcc5.fix.patch and
    xen.gcc6.fix.patch are no longer needed
- drop optional sysv support, make systemd unconditional
- renumber patches

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.3-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Jul 10 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.3-2
- perl build requires change for F25
- allow bigger xs_watch pthread stacksize for Fedora qemu

* Thu Jun 23 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.3-1
- update to xen-4.6.3
  adjust xen.use.fedora.ipxe.patch, xen.fedora.crypt.patch
    and xen.gcc6.fix.patch
  remove upstream patches

* Mon Jun 13 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.1-12
- fix systemd build issue on F25
- Qemu: scsi: esp: OOB r/w access while processing ESP_FIFO
	[CVE-2016-5338] (#1343323)
- Qemu: scsi: megasas: information leakage in megasas_ctrl_get_info
	[CVE-2016-5337] (#1343909)

* Fri Jun 03 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.1-11
- fix for CVE-2016-2858 doesn't build with qemu-xen enabled
- Unsanitised guest input in libxl device handling code
	[XSA-175, CVE-2016-4962] (#1342132)
- Unsanitised driver domain input in libxl device handling
	[XSA-178, CVE-2016-4963] (#1342131)
- arm: Host crash caused by VMID exhaust [XSA-181] (#1342530)
- Qemu: display: vmsvga: out-of-bounds read in vmsvga_fifo_read_raw() routine
	[CVE-2016-4454] (#1340741)
- Qemu: display: vmsvga: infinite loop in vmsvga_fifo_run() routine
	[CVE-2016-4453] (#1340746)
- Qemu: scsi: esp: OOB write when using non-DMA mode in get_cmd
	[CVE-2016-5238] (#1341931)

* Sat May 28 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.1-10
- cleaner way to set kernel module load list
- Unrestricted qemu logging [XSA-180, CVE-2014-3672] (#1339125)
- Qemu: scsi: esp: OOB write while writing to 's->cmdbuf' in esp_reg_write
	[CVE-2016-4439] (#1337502)
- Qemu: scsi: esp: OOB write while writing to 's->cmdbuf' in get_cmd
	[CVE-2016-4441] (#1337505)
- Qemu: scsi: megasas: out-of-bounds write while setting controller properties
	[CVE-2016-5106] (#1339578)
- Qemu: scsi: megasas: stack information leakage while reading configuration
	[CVE-2016-5105] (#1339583)

* Tue May 17 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.1-9
- xen no longer crashes when built without -fno-tree-coalesce-vars
- in systemd only try to load kernel modules that are in Fedora (#1291089)
- x86 software guest page walk PS bit handling flaw
	[XSA-176, CVE-2016-4480] (#1332657)

* Tue May 10 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.1-8
- create link to /usr/bin/qemu-system-i386 from /usr/lib/xen/bin
	for back compatibility and for virt-manager (#1334554) (#1299745)

* Mon May 09 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.1-7
- qemu-kvm: Integer overflow in SDL when creating too wide screen (#1330513)
- QEMU: Banked access to VGA memory (VBE) uses inconsistent bounds checks
	[XSA-179, CVE-2016-3710, CVE-2016-3712] (#1334346) (#1334343)

* Mon Apr 18 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.1-6
- x86 shadow pagetables: address width overflow [XSA-173, CVE-2016-3960]
	(#1328118)
- Qemu: net: buffer overflow in stellaris_enet emulator [CVE-2016-4001]
	(#1325886)
- Qemu: net: buffer overflow in MIPSnet emulator [CVE-2016-4002] (#1326084)
- qemu: Infinite loop vulnerability in usb_ehci using siTD process
	[CVE-2016-4037] (#1328081) (supercedes CVE-2015-8558 patch)

* Sun Apr 03 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.1-5
- build with -fno-tree-coalesce-vars to avoid a crash on boot

* Tue Mar 29 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.1-4
- fix for build problems on F25
- broken AMD FPU FIP/FDP/FOP leak workaround [XSA-172, CVE-2016-3158,
	CVE-2016-3159] (#1321944)

* Mon Mar 07 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.1-3
- pandoc should work again
- Qemu: nvram: OOB r/w access in processing firmware configurations
	CVE-2016-1714 (#1296080)
- Qemu: i386: null pointer dereference in vapic_write() CVE-2016-1922
	(#1292767)
- qemu: Stack-based buffer overflow in megasas_ctrl_get_info CVE-2015-8613
	(#1293305)
- qemu-kvm: Infinite loop and out-of-bounds transfer start in start_xmit()
	and e1000_receive_iov() CVE-2016-1981 (#1299996)
- Qemu: usb ehci out-of-bounds read in ehci_process_itd (#1300235)
- Qemu: usb: ehci null pointer dereference in ehci_caps_write CVE-2016-2198
	(#1303135)
- Qemu: net: ne2000: infinite loop in ne2000_receive CVE-2016-2841 (#1304048)
- Qemu: usb: integer overflow in remote NDIS control message handling
	CVE-2016-2538 (#1305816)
- Qemu: usb: null pointer dereference in remote NDIS control message handling
	CVE-2016-2392 (#1307116)
- Qemu: usb: multiple eof_timers in ohci module leads to null pointer
	dereference CVE-2016-2391 (#1308882)
- Qemu: net: out of bounds read in net_checksum_calculate() CVE-2016-2857
	(#1309565)
- Qemu: OOB access in address_space_rw leads to segmentation fault
	CVE-2015-8817 CVE-2015-8818 (#1313273)
- Qemu: rng-random: arbitrary stack based allocation leading to corruption
	CVE-2016-2858 (#1314678)

* Wed Feb 17 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.1-2
- x86: inconsistent cachability flags on guest mappings [XSA-154,
	CVE-2016-2270] (#1309324)
- VMX: guest user mode may crash guest with non-canonical RIP [XSA-170,
	CVE-2016-2271] (#1309323)

* Fri Feb 12 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.1-1
- update to xen-4.6.1
  adjust xen.use.fedora.ipxe.patch
  remove upstream patches
- don't build with pandoc (documentation) due to dependency issues

* Mon Feb 08 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.0-12
- revise patch to build with gcc6

* Sun Feb 07 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.0-11
- patch to build with gcc6

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Michael Young <m.a.young@durham.ac.uk> - 4.6.0-9
- PV superpage functionality missing sanity checks [XSA-167, CVE-2016-1570]
	(#1300345)
- VMX: intercept issue with INVLPG on non-canonical address [XSA-168,
	 CVE-2016-1571] (#1300342)
- Qemu: pci: null pointer dereference issue CVE-2015-7549 (#1291139)
- qemu: DoS by infinite loop in ehci_advance_state CVE-2015-8558 (#1291310)
- qemu: Heap-based buffer overrun during VM migration CVE-2015-8666 (#1294028)
- Qemu: net: vmxnet3: incorrect l2 header validation leads to a crash
	via assert(2) call CVE-2015-8744 (#1295441)
- qemu: Support reading IMR registers on bar0 CVE-2015-8745 (#1295443)
- Qemu: net: vmxnet3: host memory leakage  CVE-2015-8567 CVE-2015-8568
	(#1289817)
- Qemu: net: ne2000: OOB memory access in ioport r/w functions
	CVE-2015-8743 (#1294788)

* Mon Dec 21 2015 Michael Young <m.a.young@durham.ac.uk> - 4.6.0-8
- x86: unintentional logging upon guest changing callback method
	[XSA-169, CVE-2015-8615] (#1293675)

* Thu Dec 17 2015 Michael Young <m.a.young@durham.ac.uk> - 4.6.0-7
- four security updates (#1292439)
  paravirtualized drivers incautious about shared memory contents
	[XSA-155, CVE-2015-8550]
  qemu-dm buffer overrun in MSI-X handling [XSA-164, CVE-2015-8554]
  information leak in legacy x86 FPU/XMM initialization [XSA-165,
	CVE-2015-8555]
  ioreq handling possibly susceptible to multiple read issue [XSA-166]

* Thu Dec 10 2015 Michael Young <m.a.young@durham.ac.uk> - 4.6.0-6
- eepro100: Prevent two endless loops [CVE-2015-8345] (#1285215)
- pcnet: fix rx buffer overflow [CVE-2015-7512] (#1286563)
- ui: vnc: avoid floating point exception [CVE-2015-8504] (#1289544)
- additional patch for [XSA-158, CVE-2015-8338]

* Tue Dec 08 2015 Michael Young <m.a.young@durham.ac.uk> - 4.6.0-5
- three security updates (#1289568)
  long running memory operations on ARM [XSA-158, CVE-2015-8338]
  XENMEM_exchange error handling issues [XSA-159, CVE-2015-8339, CVE-2015-8340]
  libxl leak of pv kernel and initrd on error [XSA-160, CVE-2015-8341]

* Sun Dec 06 2015 Michael Young <m.a.young@durham.ac.uk> - 4.6.0-4
- heap buffer overflow vulnerability in pcnet emulator [XSA-162,
	CVE-2015-7504] (#1286544)
- virtual PMU is unsupported [XSA-163] (#1285351)

* Tue Nov 10 2015 Michael Young <m.a.young@durham.ac.uk> - 4.6.0-3
- x86: CPU lockup during exception delivery [XSA-156, CVE-2015-5307,
	CVE-2015-8104] (#1279689, #1279690)
- silence 2 macro in comment warnings

* Thu Oct 29 2015 Michael Young <m.a.young@durham.ac.uk> - 4.6.0-2
- nine security updates (#1276344)
  arm: Host crash when preempting a multicall [XSA-145, CVE-2015-7812]
  arm: various unimplemented hypercalls log without rate limiting
	[XSA-146, CVE-2015-7813]
  arm: Race between domain destruction and memory allocation decrease
	[XSA-147, CVE-2015-7814]
  x86: Uncontrolled creation of large page mappings by PV guests
	[XSA-148, CVE-2015-7835]
  leak of main per-domain vcpu pointer array [XSA-149, CVE-2015-7969]
  x86: Long latency populate-on-demand operation is not preemptible
	[XSA-150, CVE-2015-7970]
  x86: leak of per-domain profiling-related vcpu pointer array
	[XSA-151, CVE-2015-7969]
  x86: some pmu and profiling hypercalls log without rate limiting
	[XSA-152, CVE-2015-7971]
  x86: populate-on-demand balloon size inaccuracy can crash guests
	[XSA-153, CVE-2015-7972]

* Sun Oct 11 2015 Michael Young <m.a.young@durham.ac.uk> - 4.6.0-1
- update to xen-4.6.0
  xen-dumpdir.patch no longer needed
  adjust xen.use.fedora.ipxe.patch and xen.fedora.systemd.patch
  remove upstream patches
  add build fix for blktap2 to gcc5 fixes
  udev rules have now gone as have xen-syms in /boot
  package extra files 
    /etc/rc.d/init.d/xendriverdomain
    /usr/bin/xenalyze
    /usr/sbin/xentrace
    /usr/sbin/xentrace_setsize
    /usr/share/pkgconfig/*.pc
- renumber patches
- add build-requires for pandoc and discount to improve docs

* Sat Oct 10 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.1-13
- patch CVE-2015-7295 for qemu-xen-traditional as well

* Thu Oct 08 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.1-12
- Qemu: net: virtio-net possible remote DoS [CVE-2015-7295] (#1264392)

* Tue Oct 06 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.1-11
- create a symbolic link so libvirt VMs from xen 4.0 to 4.4 can still
	find qemu-dm (#1268176), (#1248843) 

* Sun Sep 27 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.1-10
- ide: fix ATAPI command permissions [CVE-2015-6855] (#1261792)

* Sat Sep 26 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.1-9
- ui/vnc: limit client_cut_text msg payload size [CVE-2015-5239] (#1259504)
- e1000: Avoid infinite loop in processing transmit descriptor
	[CVE-2015-6815] (#1260224)
- net: add checks to validate ring buffer pointers [CVE-2015-5279] (#1263278)
- net: avoid infinite loop when receiving packets [CVE-2015-5278] (#1263281)
- qemu buffer overflow in virtio-serial [CVE-2015-5745] (#1251354)

* Tue Sep 15 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.1-8
- libxl fails to honour readonly flag on disks with qemu-xen
	[XSA-142, CVE-2015-7311] (#1257893) (final patch version)

* Tue Sep 01 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.1-7
- printk is not rate-limited in xenmem_add_to_physmap_one (ARM)
	[XSA-141, CVE-2015-6654]

* Mon Aug 03 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.1-6
- Use after free in QEMU/Xen block unplug protocol [XSA-139, CVE-2015-5166]
	(#1249757)
- QEMU leak of uninitialized heap memory in rtl8139 device model
	[XSA-140, CVE-2015-5165] (#1249756)

* Sun Aug 02 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.1-5
- QEMU heap overflow flaw while processing certain ATAPI commands.
	[XSA-138, CVE-2015-5154] (#1247142)
- try again to fix xen-qemu-dom0-disk-backend.service (#1242246)

* Thu Jul 30 2015 Richard W.M. Jones <rjones@redhat.com> - 4.5.1-4
- OCaml 4.02.3 rebuild.

* Thu Jul 23 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.1-3
- correct qemu location in xen-qemu-dom0-disk-backend.service (#1242246)
- rebuild efi grub.cfg if it is present (#1239309)
- re-enable remus by building with libnl3
- modify gnutls use in line with Fedora's crypto policies (#1179352)

* Tue Jul 07 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.1-2
- xl command line config handling stack overflow [XSA-137, CVE-2015-3259]

* Mon Jun 22 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.1-1
- update to 4.5.1
  adjust xen.use.fedora.ipxe.patch and xen.fedora.systemd.patch
  remove patches for issues now fixed upstream
  renumber patches

* Fri Jun 19 2015 Richard W.M. Jones <rjones@redhat.com> - 4.5.0-13
- Rebuild for ocaml-4.02.2.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 16 2015 Michael Young <m.a.young@durham.ac.uk>
- gcc 5 bug is fixed so remove workaround

* Wed Jun 10 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.0-11
- stubs-32.h is back, so revert to previous behaviour
- Heap overflow in QEMU PCNET controller, allowing guest->host escape
	[XSA-135, CVE-2015-3209] (#1230537)
- GNTTABOP_swap_grant_ref operation misbehavior [XSA-134, CVE-2015-4163]
- vulnerability in the iret hypercall handler [XSA-136, CVE-2015-4164]

* Wed Jun 03 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.0-10.1
- stubs-32.h has gone from rawhide, put it back manually

* Tue Jun 02 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.0-10
- replace deprecated gnutls use in qemu-xen-traditional based on
	qemu-xen patches
- work around a gcc 5 bug
- Potential unintended writes to host MSI message data field via qemu
	[XSA-128, CVE-2015-4103] (#1227627)
- PCI MSI mask bits inadvertently exposed to guests [XSA-129, CVE-2015-4104]
	(#1227628)
- Guest triggerable qemu MSI-X pass-through error messages [XSA-130,
	CVE-2015-4105] (#1227629)
- Unmediated PCI register access in qemu [XSA-131, CVE-2015-4106] (#1227631)

* Wed May 13 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.0-9
- Privilege escalation via emulated floppy disk drive [XSA-133,
	CVE-2015-3456] (#1221153)

* Mon Apr 20 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.0-8
- Information leak through XEN_DOMCTL_gettscinfo [XSA-132,
	CVE-2015-3340] (#1214037)

* Tue Mar 31 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.0-7
- Long latency MMIO mapping operations are not preemptible [XSA-125,
	CVE-2015-2752] (#1207741)
- Unmediated PCI command register access in qemu [XSA-126,
	CVE-2015-2756] (#1307738)
- Certain domctl operations may be abused to lock up the host [XSA-127,
	CVE-2015-2751] (#1207739)

* Fri Mar 13 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.0-6
- Additional patch for XSA-98 on arm64

* Thu Mar 12 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.0-5
- HVM qemu unexpectedly enabling emulated VGA graphics backends [XSA-119,
	CVE-2015-2152] (#1201365)

* Tue Mar 10 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.0-4
- Hypervisor memory corruption due to x86 emulator flaw [XSA-123,
	CVE-2015-2151] (#1200398)

* Thu Mar 05 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.0-3
- Information leak via internal x86 system device emulation [XSA-121,
	CVE-2015-2044]
- Information leak through version information hypercall [XSA-122,
	CVE-2015-2045]
- fix a typo in xen.fedora.systemd.patch

* Sat Feb 14 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.0-2
- arm: vgic-v2: GICD_SGIR is not properly emulated [XSA-117, CVE-2015-0268]
- allow certain warnings with gcc5 that would otherwise be treated as errors

* Thu Jan 29 2015 Michael Young <m.a.young@durham.ac.uk> - 4.5.0-1
- update to 4.5.0
  xend has gone, so remove references to xend in spec file, sources and patches
  remove patches for issues now fixed upstream
  adjust some patches due to other code changes
  adjust spec file for renamed xenpolicy files
  set prefix back to /usr (default is now /usr/local)
  use upstream systemd files with patches for Fedora and selinux
	sysconfig for systemd is now in xencommons file
  for x86_64, files in /usr/lib64/xen/bin have moved to /usr/lib/xen/bin
  remus isn't built
  upstream systemd support needs systemd-devel to build
  replace new uint32 with uint32_t in ocaml file for ocaml-4.02.0
  stop oxenstored failing when selinux is enforcing
  re-number patches
- enable building pngs from fig files which is working again
- fix oxenstored.service preset preuninstall script
- arm: vgic: incorrect rate limiting of guest triggered logging [XSA-118,
	CVE-2015-1563] (#1187153)

* Tue Jan 06 2015 Michael Young <m.a.young@durham.ac.uk> - 4.4.1-12
- xen crash due to use after free on hvm guest teardown [XSA-116,
	 CVE-2015-0361] (#1179221)

* Tue Dec 16 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.1-11
- fix xendomains issue introduced by xl migrate --debug patch

* Mon Dec 08 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.1-10
- p2m lock starvation [XSA-114, CVE-2014-9065]
- fix build with --without xsm

* Thu Nov 27 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.1-9
- Excessive checking in compatibility mode hypercall argument translation
	[XSA-111, CVE-2014-8866]
- Insufficient bounding of "REP MOVS" to MMIO emulated inside the hypervisor
	[XSA-112, CVE-2014-8867]
- fix segfaults and failures in xl migrate --debug (#1166461)

* Thu Nov 20 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.1-8
- Guest effectable page reference leak in MMU_MACHPHYS_UPDATE handling
	[XSA-113, CVE-2014-9030] (#1166914)

* Tue Nov 18 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.1-7
- Insufficient restrictions on certain MMU update hypercalls [XSA-109,
	CVE-2014-8594] (#1165205)
- Missing privilege level checks in x86 emulation of far branches [XSA-110,
	CVE-2014-8595] (#1165204)
- Add fix for CVE-2014-0150 to qemu-dm, though it probably isn't
	exploitable from xen (#1086776)

* Wed Oct 01 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.1-6
- Improper MSR range used for x2APIC emulation [XSA-108, CVE-2014-7188]
	(#1148465)

* Tue Sep 30 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.1-5
- xen support is in 256k seabios binary when it exists (#1146260)

* Tue Sep 23 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.1-4
- Race condition in HVMOP_track_dirty_vram [XSA-104, CVE-2014-7154] (#1145736)
- Missing privilege level checks in x86 HLT, LGDT, LIDT, and LMSW emulation
	[XSA-105, CVE-2014-7155] (#1145737)
- Missing privilege level checks in x86 emulation of software interrupts
	[XSA-106, CVE-2014-7156] (#1145738)

* Sun Sep 14 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.1-3
- disable building pngs from fig files which is currently broken in rawhide

* Tue Sep 09 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.1-2
- Mishandling of uninitialised FIFO-based event channel control blocks
	[XSA-107, CVE-2014-6268] (#1140287)
- delete a patch file that was dropped in the last update

* Tue Sep 02 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.1-1
- update to xen-4.4.1
  remove patches for fixes that are now included
- replace uint32 with uint32_t in ocaml file for ocaml-4.02.0

* Sun Aug 31 2014 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-14
- Bump release and rebuild.

* Sun Aug 31 2014 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-13
- ocaml-4.02.0 final rebuild.

* Sun Aug 24 2014 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-12
- ocaml-4.02.0+rc1 rebuild.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.0-10
- Long latency virtual-mmu operations are not preemptible
	[XSA-97, CVE-2014-5146]

* Thu Aug 07 2014 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-9
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 14 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.0-8
- rebuild for ocaml update

* Tue Jun 17 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.0-7
- Hypervisor heap contents leaked to guest [XSA-100, CVE-2014-4021]
	(#1110316) with extra patch to avoid regression

* Sun Jun 15 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.0-6
- Fix two %%if line typos in the spec file
- Vulnerabilities in HVM MSI injection [XSA-96, CVE-2014-3967,CVE-2014-3968]
	(#1104583)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.0-4
- add systemd preset support (#1094938)

* Wed Apr 30 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.0-3
- HVMOP_set_mem_type allows invalid P2M entries to be created
	[XSA-92, CVE-2014-3124] (#1093315)
- change -Wmaybe-uninitialized errors into warnings for gcc 4.9.0
- fix a couple of -Wmaybe-uninitialized cases

* Wed Mar 26 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.0-2
- HVMOP_set_mem_access is not preemptible [XSA-89, CVE-2014-2599] (#1080425)

* Sun Mar 23 2014 Michael Young <m.a.young@durham.ac.uk> - 4.4.0-1
- update to xen-4.4.0
- adjust xend.selinux.fixes.patch and xen-initscript.patch as xend has moved
- don't build xend unless --with xend is specified
- use --with-system-seabios option instead of xen.use.fedora.seabios.patch
- update xen.use.fedora.ipxe.patch patch
- replace qemu-xen.tradonly.patch with --with-system-qemu= option pointing
  to Fedora's qemu-system-i386
- adjust xen.xsm.enable.patch and remove bits that are are no longer needed
- blktapctrl is no longer built, remove related files
- adjust files to be packaged; xsview has gone, add xen-mfndump and
  xenstore man pages
- add another xenstore-write to xenstored.service and oxenstored.service
- Add xen.console.fix.patch to fix issues running pygrub

* Tue Feb 18 2014 Michael Young <m.a.young@durham.ac.uk> - 4.3.2-1
- update to xen-4.3.2
  includes fix for "Excessive time to disable caching with HVM guests with
    PCI passthrough" [XSA-60, CVE-2013-2212] (#987914)
- remove patches that are now included

* Wed Feb 12 2014 Michael Young <m.a.young@durham.ac.uk> - 4.3.1-10
- use-after-free in xc_cpupool_getinfo() under memory pressure [XSA-88,
    CVE-2014-1950] (#1064491)

* Thu Feb 06 2014 Michael Young <m.a.young@durham.ac.uk> - 4.3.1-9
- integer overflow in several XSM/Flask hypercalls [XSA-84, CVE-2014-1891,
    CVE-2014-1892, CVE-2014-1893, CVE-2014-1894]
  Off-by-one error in FLASK_AVC_CACHESTAT hypercall [XSA-85, CVE-2014-1895]
  libvchan failure handling malicious ring indexes [XSA-86, CVE-2014-1896]
    (#1062335)

* Fri Jan 24 2014 Michael Young <m.a.young@durham.ac.uk> - 4.3.1-8
- PHYSDEVOP_{prepare,release}_msix exposed to unprivileged pv guests
    [XSA-87, CVE-2014-1666] (#1058398)

* Thu Jan 23 2014 Michael Young <m.a.young@durham.ac.uk> - 4.3.1-7
- Out-of-memory condition yielding memory corruption during IRQ setup
    [XSA-83, CVE-2014-1642] (#1057142)

* Wed Dec 11 2013 Michael Young <m.a.young@durham.ac.uk> - 4.3.1-6
- Disaggregated domain management security status update [XSA-77]
- IOMMU TLB flushing may be inadvertently suppressed [XSA-80, CVE-2013-6400]
    (#1040024)

* Mon Dec 02 2013 Michael Young <m.a.young@durham.ac.uk> - 4.3.1-5
- HVM guest triggerable AMD CPU erratum may cause host hang
    [XSA-82, CVE-2013-6885]

* Tue Nov 26 2013 Michael Young <m.a.young@durham.ac.uk> - 4.3.1-4
- Lock order reversal between page_alloc_lock and mm_rwlock
    [XSA-74, CVE-2013-4553] (#1034925)
- Hypercalls exposed to privilege rings 1 and 2 of HVM guests
    [XSA-76, CVE-2013-4554] (#1034923)

* Thu Nov 21 2013 Michael Young <m.a.young@durham.ac.uk> - 4.3.1-3
- Insufficient TLB flushing in VT-d (iommu) code
    [XSA-78, CVE-2013-6375] (#1033149)

* Sat Nov 09 2013 Michael Young <m.a.young@durham.ac.uk> - 4.3.1-2
- Host crash due to HVM guest VMX instruction execution
    [XSA-75, CVE-2013-4551] (#1029055)

* Fri Nov 01 2013 Michael Young <m.a.young@durham.ac.uk> - 4.3.1-1
- update to xen-4.3.1
- Lock order reversal between page allocation and grant table locks
    [XSA-73, CVE-2013-4494] (#1026248)

* Tue Oct 29 2013 Michael Young <m.a.young@durham.ac.uk> - 4.3.0-10
- ocaml xenstored mishandles oversized message replies
    [XSA-72, CVE-2013-4416] (#1024450)

* Thu Oct 24 2013 Michael Young <m.a.young@durham.ac.uk> - 4.3.0-9
- systemd changes to allow oxenstored to be used instead of xenstored (#1022640)

* Thu Oct 10 2013 Michael Young <m.a.young@durham.ac.uk> - 4.3.0-8
- security fixes (#1017843)
  Information leak through outs instruction emulation in 64-bit PV guests
    [XSA-67, CVE-2013-4368]
  possible null dereference when parsing vif ratelimiting info
    [XSA-68, CVE-2013-4369]
  misplaced free in ocaml xc_vcpu_getaffinity stub
    [XSA-69, CVE-2013-4370]
  use-after-free in libxl_list_cpupool under memory pressure
    [XSA-70, CVE-2013-4371]
  qemu disk backend (qdisk) resource leak (Fedora doesn't build this qemu)
    [XSA-71, CVE-2013-4375]

* Wed Oct 02 2013 Michael Young <m.a.young@durham.ac.uk> - 4.3.0-7
- Set "Domain-0" label in xenstored.service systemd file to match
  xencommons init.d script.
- security fixes (#1013748)
  Information leaks to HVM guests through I/O instruction emulation
    [XSA-63, CVE-2013-4355]
  Memory accessible by 64-bit PV guests under live migration
    [XSA-64, CVE-2013-4356]
  Information leak to HVM guests through fbld instruction emulation
    [XSA-66, CVE-2013-4361]

* Wed Sep 25 2013 Michael Young <m.a.young@durham.ac.uk> - 4.3.0-6
- Information leak on AVX and/or LWP capable CPUs [XSA-62, CVE-2013-1442]
  (#1012056)

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 4.3.0-5
- Rebuild for OCaml 4.01.0.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Michael Young <m.a.young@durham.ac.uk> - 4.3.0-2 4.3.0-3
- build a 64-bit hypervisor on ix86

* Tue Jul 16 2013 Michael Young <m.a.young@durham.ac.uk> - 4.3.0-1
- update to xen-4.3.0
- rebase xen.use.fedora.ipxe.patch
- remove patches that are now included or no longer needed
- add polarssl source needed for stubdom build
- remove references to ia64 in spec file (dropped upstream)
- don't build hypervisor on ix86 (dropped upstream)
- tools want wget (or ftp) to build
- build XSM FLASK support into hypervisor with policy file
- add xencov_split and xencov to files packaged, remove pdf docs
- tidy up rpm scripts and stop enabling systemctl services on upgrade
  now sysv is gone from Fedora
- re-number patches

* Wed Jun 26 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.2-10
- XSA-45/CVE-2013-1918 breaks page reference counting [XSA-58,
  CVE-2013-1432] (#978383)
- let pygrub handle set default="${next_entry}" line in F19 (#978036)
- libxl: Set vfb and vkb devid if not done so by the caller (#977987)

* Mon Jun 24 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.2-9
- add upstream patch for PCI passthrough problems after XSA-46 (#977310)

* Fri Jun 21 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.2-8
- xenstore permissions not set correctly by libxl [XSA-57,
  CVE-2013-2211] (#976779)

* Fri Jun 14 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.2-7
- Revised fixes for [XSA-55, CVE-2013-2194 CVE-2013-2195
  CVE-2013-2196] (#970640)

* Tue Jun 04 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.2-6
- Information leak on XSAVE/XRSTOR capable AMD CPUs
  [XSA-52, CVE-2013-2076] (#970206)
- Hypervisor crash due to missing exception recovery on XRSTOR
  [XSA-53, CVE-2013-2077] (#970204)
- Hypervisor crash due to missing exception recovery on XSETBV
  [XSA-54, CVE-2013-2078] (#970202)
- Multiple vulnerabilities in libelf PV kernel handling
  [XSA-55] (#970640)

* Fri May 17 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.2-5
- xend toolstack doesn't check bounds for VCPU affinity
  [XSA-56, CVE-2013-2072] (#964241)

* Tue May 14 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.2-4
- xen-devel should require libuuid-devel (#962833)
- pygrub menu items can include too much text (#958524)

* Thu May 02 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.2-3
- PV guests can use non-preemptible long latency operations to
  mount a denial of service attack on the whole system
  [XSA-45, CVE-2013-1918] (#958918)
- malicious guests can inject interrupts through bridge devices to
  mount a denial of service attack on the whole system
  [XSA-49, CVE-2013-1952] (#958919)

* Fri Apr 26 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.2-2
- fix further man page issues to allow building on F19 and F20

* Thu Apr 25 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.2-1
- update to xen-4.2.2
  includes fixes for
  [XSA-48, CVE-2013-1922] (Fedora doesn't use the affected code)
  passed through IRQs or PCI devices might allow denial of service attack
    [XSA-46, CVE-2013-1919] (#953568)
  SYSENTER in 32-bit PV guests on 64-bit xen can crash hypervisor
    [XSA-44, CVE-2013-1917] (#953569)
- remove patches that are included in 4.2.2
- look for libxl-save-helper in the right place
- fix xl list -l output when built with yajl2
- allow xendomains to work with xl saved images

* Thu Apr 04 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.1-10
- make xendomains systemd script executable and update it from
  init.d version (#919705)
- Potential use of freed memory in event channel operations [XSA-47,
  CVE-2013-1920]

* Thu Feb 21 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.1-9
- patch for [XSA-36, CVE-2013-0153] can cause boot time crash

* Fri Feb 15 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.1-8
- patch for [XSA-38, CVE-2013-0215] was flawed

* Fri Feb 08 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.1-7
- BuildRequires for texlive-kpathsea-bin wasn't needed
- correct gcc 4.8 fixes and follow suggestions upstream

* Tue Feb 05 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.1-6
- guest using oxenstored can crash host or exhaust memory [XSA-38,
  CVE-2013-0215] (#907888)
- guest using AMD-Vi for PCI passthrough can cause denial of service
  [XSA-36, CVE-2013-0153] (#910914)
- add some fixes for code which gcc 4.8 complains about
- additional BuildRequires are now needed for pod2text and pod2man
  also texlive-kpathsea-bin for mktexfmt

* Wed Jan 23 2013 Michael Young <m.a.young@durham.ac.uk>
- correct disabling of xendomains.service on uninstall

* Tue Jan 22 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.1-5
- nested virtualization on 32-bit guest can crash host [XSA-34,
  CVE-2013-0151] also nested HVM on guest can cause host to run out
  of memory [XSA-35, CVE-2013-0152] (#902792)
- restore status option to xend which is used by libvirt (#893699)

* Thu Jan 17 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.1-4
- Buffer overflow when processing large packets in qemu e1000 device
  driver [XSA-41, CVE-2012-6075] (#910845)

* Thu Jan 10 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.1-3
- fix some format errors in xl.cfg.pod.5 to allow build on F19

* Wed Jan 09 2013 Michael Young <m.a.young@durham.ac.uk> - 4.2.1-2
- VT-d interrupt remapping source validation flaw [XSA-33,
    CVE-2012-5634] (#893568)
- pv guests can crash xen when xen built with debug=y (included for
    completeness - Fedora builds have debug=n) [XSA-37, CVE-2013-0154]

* Tue Dec 18 2012 Michael Young <m.a.young@durham.ac.uk> - 4.2.1-1
- update to xen-4.2.1
- remove patches that are included in 4.2.1
- rebase xen.fedora.efi.build.patch

* Thu Dec 13 2012 Richard W.M. Jones <rjones@redhat.com> - 4.2.0-7
- Rebuild for OCaml fix (RHBZ#877128).

* Mon Dec 03 2012 Michael Young <m.a.young@durham.ac.uk> - 4.2.0-6
- 6 security fixes
  A guest can cause xen to crash [XSA-26, CVE-2012-5510] (#883082)
  An HVM guest can cause xen to run slowly or crash [XSA-27, CVE-2012-5511]
    (#883084)
  A PV guest can cause xen to crash and might be able escalate privileges
    [XSA-29, CVE-2012-5513] (#883088)
  An HVM guest can cause xen to hang [XSA-30, CVE-2012-5514] (#883091)
  A guest can cause xen to hang [XSA-31, CVE-2012-5515] (#883092)
  A PV guest can cause xen to crash and might be able escalate privileges
    [XSA-32, CVE-2012-5525] (#883094)

* Sat Nov 17 2012 Michael Young <m.a.young@durham.ac.uk> - 4.2.0-5
- two build fixes for Fedora 19
- add texlive-ntgclass package to fix build

* Tue Nov 13 2012 Michael Young <m.a.young@durham.ac.uk> - 4.2.0-4
- 4 security fixes
  A guest can block a cpu by setting a bad VCPU deadline [XSA 20,
    CVE-2012-4535] (#876198)
  HVM guest can exhaust p2m table crashing xen [XSA 22, CVE-2012-4537] (#876203)
  PAE HVM guest can crash hypervisor [XSA-23, CVE-2012-4538] (#876205)
  32-bit PV guest on 64-bit hypervisor can cause an hypervisor infinite
    loop [XSA-24, CVE-2012-4539] (#876207)
- texlive-2012 is now in Fedora 18

* Sun Oct 28 2012 Michael Young <m.a.young@durham.ac.uk> - 4.2.0-3
- texlive-2012 isn't in Fedora 18 yet

* Fri Oct 26 2012 Michael Young <m.a.young@durham.ac.uk> - 4.2.0-2
- limit the size of guest kernels and ramdisks to avoid running out
  of memeory on dom0 during guest boot [XSA-25, CVE-2012-4544] (#870414)

* Thu Oct 25 2012 Michael Young <m.a.young@durham.ac.uk> - 4.2.0-1
- update to xen-4.2.0
- rebase xen-net-disable-iptables-on-bridge.patch pygrubfix.patch
- remove patches that are now upstream or with alternatives upstream
- use ipxe and seabios from seabios-bin and ipxe-roms-qemu packages
- xen tools now need ./configure to be run (x86_64 needs libdir set)
- don't build upstream qemu version
- amend list of files in package - relocate xenpaging
  add /etc/xen/xlexample* oxenstored.conf /usr/include/xenstore-compat/*
      xenstore-stubdom.gz xen-lowmemd xen-ringwatch xl.1.gz xl.cfg.5.gz
      xl.conf.5.gz xlcpupool.cfg.5.gz
- use a tmpfiles.d file to create /run/xen on boot
- add BuildRequires for yajl-devel and graphviz
- build an efi boot image where it is supported
- adjust texlive changes so spec file still works on Fedora 17

* Thu Oct 18 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.3-6
- add font packages to build requires due to 2012 version of texlive in F19
- use build requires of texlive-latex instead of tetex-latex which it
  obsoletes

* Wed Oct 17 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.3-5
- rebuild for ocaml update

* Thu Sep 06 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.3-4
- disable qemu monitor by default [XSA-19, CVE-2012-4411] (#855141)

* Wed Sep 05 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.3-3
- 5 security fixes
  a malicious 64-bit PV guest can crash the dom0 [XSA-12, CVE-2012-3494]
    (#854585)
  a malicious crash might be able to crash the dom0 or escalate privileges
    [XSA-13, CVE-2012-3495] (#854589)
  a malicious PV guest can crash the dom0 [XSA-14, CVE-2012-3496] (#854590)
  a malicious HVM guest can crash the dom0 and might be able to read
    hypervisor or guest memory [XSA-16, CVE-2012-3498] (#854593)
  an HVM guest could use VT100 escape sequences to escalate privileges to
    that of the qemu process [XSA-17, CVE-2012-3515] (#854599)

* Fri Aug 10 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.3-1 4.1.3-2
- update to 4.1.3
  includes fix for untrusted HVM guest can cause the dom0 to hang or
    crash [XSA-11, CVE-2012-3433] (#843582)
- remove patches that are now upstream
- remove some unnecessary compile fixes
- adjust upstream-23936:cdb34816a40a-rework for backported fix for
    upstream-23940:187d59e32a58
- replace pygrub.size.limits.patch with upstreamed version
- fix for (#845444) broke xend under systemd

* Tue Aug 07 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-25
- remove some unnecessary cache flushing that slow things down
- change python options on xend to reduce selinux problems (#845444)

* Thu Jul 26 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-24
- in rare circumstances an unprivileged user can crash an HVM guest
  [XSA-10,CVE-2012-3432] (#843766)

* Tue Jul 24 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-23
- add a patch to remove a dependency on PyXML and Require python-lxml
  instead of PyXML (#842843)

* Sun Jul 22 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-22
- adjust systemd service files not to report failures when running without
  a hypervisor or when xendomains.service doesn't find anything to start

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-20
- Apply three security patches
  64-bit PV guest privilege escalation vulnerability [CVE-2012-0217]
  guest denial of service on syscall/sysenter exception generation
    [CVE-2012-0218]
  PV guest host Denial of Service [CVE-2012-2934]

* Sat Jun 09 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-19
- adjust xend.service systemd file to avoid selinux problems

* Fri Jun 08 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-18
- Enable xenconsoled by default under systemd (#829732)

* Thu May 17 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-16 4.1.2-17
- make pygrub cope better with big files from guest (#818412 CVE-2012-2625)
- add patch from 4.1.3-rc2-pre to build on F17/8

* Sun Apr 15 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-15
- Make the udev tap rule more specific as it breaks openvpn (#812421)
- don't try setuid in xend if we don't need to so selinux is happier

* Sat Mar 31 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-14
- /var/lib/xenstored mount has wrong selinux permissions in latest Fedora
- load xen-acpi-processor module (kernel 3.4 onwards) if present

* Thu Mar 08 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-13
- fix a packaging error

* Thu Mar 08 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-12
- fix an error in an rpm script from the sysv configuration removal
- migrate xendomains script to systemd

* Wed Feb 29 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-11
- put the systemd files back in the right place

* Wed Feb 29 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-10
- clean up systemd and sysv configuration including removal of migrated
  sysv files for fc17+

* Sat Feb 18 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-9
- move xen-watchdog to systemd

* Wed Feb 08 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-8
- relocate systemd files for fc17+

* Tue Feb 07 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-7
- move xend and xenconsoled to systemd

* Thu Feb 02 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-6
- Fix buffer overflow in e1000 emulation for HVM guests [CVE-2012-0029]

* Sat Jan 28 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-5
- Start building xen's ocaml libraries if appropriate unless --without ocaml
  was specified
- add some backported patches from xen unstable (via Debian) for some
  ocaml tidying and fixes

* Sun Jan 15 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-4
- actually apply the xend-pci-loop.patch
- compile fixes for gcc-4.7

* Wed Jan 11 2012 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-3
- Add xend-pci-loop.patch to stop xend crashing with weird PCI cards (#767742)
- avoid a backtrace if xend can't log to the standard file or a 
  temporary directory (part of #741042)

* Mon Nov 21 2011 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-2
- Fix lost interrupts on emulated devices
- stop xend crashing if its state files are empty at start up
- avoid a python backtrace if xend is run on bare metal
- update grub2 configuration after the old hypervisor has gone
- move blktapctrl to systemd
- Drop obsolete dom0-kernel.repo file

* Fri Oct 21 2011 Michael Young <m.a.young@durham.ac.uk> - 4.1.2-1
- update to 4.1.2
  remove upstream patches xen-4.1-testing.23104 and xen-4.1-testing.23112

* Fri Oct 14 2011 Michael Young <m.a.young@durham.ac.uk> - 4.1.1-8
- more pygrub improvements for grub2 on guest

* Thu Oct 13 2011 Michael Young <m.a.young@durham.ac.uk> - 4.1.1-7
- make pygrub work better with GPT partitions and grub2 on guest

* Thu Sep 29 2011 Michael Young <m.a.young@durham.ac.uk> - 4.1.1-5 4.1.1-6
- improve systemd functionality

* Wed Sep 28 2011 Michael Young <m.a.young@durham.ac.uk> - 4.1.1-4
- lsb header fixes - xenconsoled shutdown needs xenstored to be running
- partial migration to systemd to fix shutdown delays
- update grub2 configuration after hypervisor updates

* Sun Aug 14 2011 Michael Young <m.a.young@durham.ac.uk> - 4.1.1-3
- untrusted guest controlling PCI[E] device can lock up host CPU [CVE-2011-3131]

* Wed Jul 20 2011 Michael Young <m.a.young@durham.ac.uk> - 4.1.1-2
- clean up patch to solve a problem with hvmloader compiled with gcc 4.6

* Wed Jun 15 2011 Michael Young <m.a.young@durham.ac.uk> - 4.1.1-1
- update to 4.1.1
  includes various bugfixes and fix for [CVE-2011-1898] guest with pci
  passthrough can gain privileged access to base domain
- remove upstream cve-2011-1583-4.1.patch 

* Mon May 09 2011 Michael Young <m.a.young@durham.ac.uk> - 4.1.0-2
- Overflows in kernel decompression can allow root on xen PV guest to gain
  privileged access to base domain, or access to xen configuration info.
  Lack of error checking could allow DoS attack from guest [CVE-2011-1583]
- Don't require /usr/bin/qemu-nbd as it isn't used at present.

* Fri Mar 25 2011 Michael Young <m.a.young@durham.ac.uk> - 4.1.0-1
- update to 4.1.0 final

* Tue Mar 22 2011 Michael Young <m.a.young@durham.ac.uk> - 4.1.0-0.1.rc8
- update to 4.1.0-rc8 release candidate
- create xen-4.1.0-rc8.tar.xz file from git/hg repositories
- rebase xen-initscript.patch xen-dumpdir.patch
  xen-net-disable-iptables-on-bridge.patch localgcc45fix.patch
  sysconfig.xenstored init.xenstored
- remove unnecessary or conflicting xen-xenstore-cli.patch localpy27fixes.patch
  xen.irq.fixes.patch xen.xsave.disable.patch xen.8259afix.patch
  localcleanups.patch libpermfixes.patch
- add patch to allow pygrub to work with single partitions with boot sectors
- create ipxe-git-v1.0.0.tar.gz from http://git.ipxe.org/ipxe.git
  to avoid downloading at build time
- no need to move udev rules or init scripts as now created in the right place
- amend list of files shipped - remove fs-backend
  add init.d scripts xen-watchdog xencommons
  add config files xencommons xl.conf cpupool
  add programs kdd tap-ctl xen-hptool xen-hvmcrash xenwatchdogd

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Michael Young <m.a.young@durham.ac.uk> - 4.0.1-9
- Make libraries executable so that rpm gets dependencies right

* Sat Jan 29 2011 Michael Young <m.a.young@durham.ac.uk> - 4.0.1-8
- Temporarily turn off some compile options so it will build on rawhide

* Fri Jan 28 2011 Michael Young <m.a.young@durham.ac.uk> - 4.0.1-7
- ghost directories in /var/run (#656724)
- minor fixes to /usr/share/doc/xen-doc-4.?.?/misc/network_setup.txt (#653159)
  /etc/xen/scripts/network-route, /etc/xen/scripts/vif-common.sh (#669747)
  and /etc/sysconfig/modules/xen.modules (#656536)

* Tue Oct 12 2010 Michael Young <m.a.young@durham.ac.uk> - 4.0.1-6
- add upstream xen patch xen.8259afix.patch to fix boot panic
  "IO-APIC + timer doesn't work!" (#642108)

* Thu Oct 07 2010 Michael Young <m.a.young@durham.ac.uk> - 4.0.1-5
- add ext4 support for pvgrub (grub-ext4-support.patch from grub-0.97-66.fc14)

* Wed Sep 29 2010 jkeating - 4.0.1-4
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Michael Young <m.a.young@durham.ac.uk> - 4.0.1-3
- create symlink for qemu-dm on x86_64 for compatibility with 3.4
- apply some patches destined for 4.0.2
    add some irq fixes
    disable xsave which causes problems for HVM

* Sun Aug 29 2010 Michael Young <m.a.young@durham.ac.uk> - 4.0.1-2
- fix compile problems on Fedora 15, I suspect due to gcc 4.5.1

* Wed Aug 25 2010 Michael Young <m.a.young@durham.ac.uk> - 4.0.1-1
- update to 4.0.1 release - many bug fixes
- xen-dev-create-cleanup.patch no longer needed
- remove part of localgcc45fix.patch no longer needed
- package new files /etc/bash_completion.d/xl.sh
  and /usr/sbin/gdbsx
- add patch to get xm and xend working with python 2.7

* Mon Aug 2 2010 Michael Young <m.a.young@durham.ac.uk> - 4.0.0-5
- add newer module names and xen-gntdev to xen.modules
- Update dom0-kernel.repo file to use repos.fedorapeople.org location

* Mon Jul 26 2010 Michael Young <m.a.young@durham.ac.uk>
- create a xen-licenses package to satisfy revised the Fedora
  Licensing Guidelines

* Sun Jul 25 2010 Michael Young <m.a.young@durham.ac.uk> - 4.0.0-4
- fix gcc 4.5 compile problems

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jun 20 2010 Michael Young <m.a.young@durham.ac.uk> - 4.0.0-2
- add patch to remove some old device creation code that doesn't
  work with the latest pvops kernels

* Mon Jun 7 2010 Michael Young <m.a.young@durham.ac.uk> - 4.0.0-1
- update to 4.0.0 release
- rebase xen-initscript.patch and xen-dumpdir.patch patches
- adjust spec file for files added to or removed from the packages
- add new build dependencies libuuid-devel and iasl

* Tue Jun 1 2010 Michael Young <m.a.young@durham.ac.uk> - 3.4.3-1
- update to 3.4.3 release including
    support for latest pv_ops kernels (possibly incomplete)
    should fix build problems (#565063) and crashes (#545307)
- replace Prereq: with Requires: in spec file
- drop static libraries (#556101)

* Thu Dec 10 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.4.2-2
- adapt module load script to evtchn.ko -> xen-evtchn.ko rename.

* Thu Dec 10 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.4.2-1
- update to 3.4.2 release.
- drop backport patches.

* Thu Oct 8 2009 Justin M. Forbes <jforbes@redhat.com> - 3.4.1-5
- add PyXML to dependencies. (#496135)
- Take ownership of {_libdir}/fs (#521806)

* Mon Sep 14 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.4.1-4
- add e2fsprogs-devel to build dependencies.

* Wed Sep 2 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.4.1-3
- swap bzip2+xz linux kernel compression support patches.
- backport one more bugfix (videoram option).

* Tue Sep 1 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.4.1-2
- backport bzip2+xz linux kernel compression support.
- backport a few bugfixes.

* Fri Aug 7 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.4.1-1
- update to 3.4.1 release.

* Wed Aug 5 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.4.0-4
- Kill info files.  No xen docs, just standard gnu stuff.
- kill -Werror in tools/libxc to fix build.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 28 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.4.0-2
- rename info files to fix conflict with binutils.
- add install-info calls for the doc subpackage.
- un-parallelize doc build.

* Wed May 27 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.4.0-1
- update to version 3.4.0.
- cleanup specfile, add doc subpackage.

* Tue Mar 10 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.3.1-11
- fix python 2.6 warnings.

* Fri Mar 6 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.3.1-9
- fix xen.modules init script for pv_ops kernel.
- stick rpm release tag into XEN_VENDORVERSION.
- use %%{ix86} macro in ExclusiveArch.
- keep blktapctrl turned off by default.

* Mon Mar 2 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.3.1-7
- fix xenstored init script for pv_ops kernel.

* Fri Feb 27 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.3.1-6
- fix xenstored crash.
- backport qemu-unplug patch.

* Tue Feb 24 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.3.1-5
- fix gcc44 build (broken constrain in inline asm).
- fix ExclusiveArch

* Tue Feb 3 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.3.1-3
- backport bzImage support for dom0 builder.

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 3.3.1-2
- rebuild with new openssl

* Thu Jan 8 2009 Gerd Hoffmann <kraxel@redhat.com> - 3.3.1-1
- update to xen 3.3.1 release.

* Wed Dec 17 2008 Gerd Hoffmann <kraxel@redhat.com> - 3.3.0-2
- build and package stub domains (pvgrub, ioemu).
- backport unstable fixes for pv_ops dom0.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.3.0-1.1
- Rebuild for Python 2.6

* Fri Aug 29 2008 Daniel P. Berrange <berrange@redhat.com> - 3.3.0-1.fc10
- Update to xen 3.3.0 release

* Wed Jul 23 2008 Mark McLoughlin <markmc@redhat.com> - 3.2.0-17.fc10
- Enable xen-hypervisor build
- Backport support for booting DomU from bzImage
- Re-diff all patches for zero fuzz

* Wed Jul  9 2008 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-16.fc10
- Remove bogus ia64 hypercall arg (rhbz #433921)

* Fri Jun 27 2008 Markus Armbruster <armbru@redhat.com> - 3.2.0-15.fc10
- Re-enable QEMU image format auto-detection, without the security
  loopholes

* Wed Jun 25 2008 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-14.fc10
- Rebuild for GNU TLS ABI change

* Fri Jun 13 2008 Markus Armbruster <armbru@redhat.com> - 3.2.0-13.fc10
- Correctly limit PVFB size (CVE-2008-1952)

* Tue Jun  3 2008 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-12.fc10
- Move /var/run/xend into xen-runtime for pygrub (rhbz #442052)

* Wed May 14 2008 Markus Armbruster <armbru@redhat.com> - 3.2.0-11.fc10
- Disable QEMU image format auto-detection (CVE-2008-2004)
- Fix PVFB to validate frame buffer description (CVE-2008-1943)

* Wed Feb 27 2008 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-10.fc9
- Fix block device checks for extendable disk formats

* Wed Feb 27 2008 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-9.fc9
- Let XenD setup QEMU logfile (rhbz #435164)
- Fix PVFB use of event channel filehandle

* Sat Feb 23 2008 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-8.fc9
- Fix block device extents check (rhbz #433560)

* Mon Feb 18 2008 Mark McLoughlin <markmc@redhat.com> - 3.2.0-7.fc9
- Restore some network-bridge patches lost during 3.2.0 rebase

* Wed Feb  6 2008 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-6.fc9
- Fixed xenstore-ls to automatically use xenstored socket as needed

* Sun Feb  3 2008 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-5.fc9
- Fix timer mode parameter handling for HVM
- Temporarily disable all Latex docs due to texlive problems (rhbz #431327)

* Fri Feb  1 2008 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-4.fc9
- Add a xen-runtime subpackage to allow use of Xen without XenD
- Split init script out to one script per daemon
- Remove unused / broken / obsolete tools

* Mon Jan 21 2008 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-3.fc9
- Remove legacy dependancy on python-virtinst

* Mon Jan 21 2008 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-2.fc9
- Added XSM header files to -devel RPM

* Fri Jan 18 2008 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-1.fc9
- Updated to 3.2.0 final release

* Thu Jan 10 2008 Daniel P. Berrange <berrange@redhat.com> - 3.2.0-0.fc9.rc5.dev16701.1
- Rebase to Xen 3.2 rc5 changeset 16701

* Thu Dec 13 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.2-3.fc9
- Re-factor to make it easier to test dev trees in RPMs
- Include hypervisor build if doing a dev RPM

* Fri Dec 07 2007 Release Engineering <rel-eng@fedoraproject.org> - 3.1.2-2.fc9
- Rebuild for deps

* Sat Dec  1 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.2-1.fc9
- Upgrade to 3.1.2 bugfix release

* Sat Nov  3 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-14.fc9
- Disable network-bridge script since it conflicts with NetworkManager
  which is now on by default

* Fri Oct 26 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-13.fc9
- Fixed xenbaked tmpfile flaw (CVE-2007-3919)

* Wed Oct 10 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-12.fc8
- Pull in QEMU BIOS boot menu patch from KVM package
- Fix QEMU patch for locating x509 certificates based on command line args
- Add XenD config options for TLS x509 certificate setup

* Wed Sep 26 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-11.fc8
- Fixed rtl8139 checksum calculation for Vista (rhbz #308201)

* Wed Sep 26 2007 Chris Lalancette <clalance@redhat.com> - 3.1.0-10.fc8
- QEmu NE2000 overflow check - CVE-2007-1321
- Pygrub guest escape - CVE-2007-4993

* Mon Sep 24 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-9.fc8
- Fix generation of manual pages (rhbz #250791)
- Really fix FC-6 32-on-64 guests

* Mon Sep 24 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-8.fc8
- Make 32-bit FC-6 guest PVFB work on x86_64 host

* Mon Sep 24 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-7.fc8
- Re-add support for back-compat FC6 PVFB support
- Fix handling of explicit port numbers (rhbz #279581)

* Wed Sep 19 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-6.fc8
- Don't clobber the VIF type attribute in FV guests (rhbz #296061)

* Tue Aug 28 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-5.fc8
- Added dep on openssl for blktap-qcow

* Tue Aug 28 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-4.fc8
- Switch PVFB over to use QEMU
- Backport QEMU VNC security patches for TLS/x509

* Wed Aug  1 2007 Markus Armbruster <armbru@redhat.com> - 3.1.0-3.fc8
- Put guest's native protocol ABI into xenstore, to provide for older
  kernels running 32-on-64.
- VNC keymap fixes
- Fix race conditions in LibVNCServer on client disconnect

* Tue Jun 12 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-2.fc8
- Remove patch which kills VNC monitor
- Fix HVM save/restore file path to be /var/lib/xen instead of /tmp
- Don't spawn a bogus xen-vncfb daemon for HVM guests
- Add persistent logging of hypervisor & guest consoles
- Add /etc/sysconfig/xen to allow admin choice of logging options
- Re-write Xen startup to use standard init script functions
- Add logrotate configuration for all xen related logs

* Fri May 25 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-1.fc8
- Updated to official 3.1.0 tar.gz
- Fixed data corruption from VNC client disconnect (bz 241303)

* Thu May 17 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-0.rc7.2.fc7
- Ensure xen-vncfb processes are cleanedup if guest quits (bz 240406)
- Tear down guest if device hotplug fails

* Thu May  3 2007 Daniel P. Berrange <berrange@redhat.com> - 3.1.0-0.rc7.1.fc7
- Updated to 3.1.0 rc7, changeset  15021 (upstream renumbered from 3.0.5)

* Tue May  1 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.5-0.rc4.4.fc7
- Fix op_save RPC API

* Mon Apr 30 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.5-0.rc4.3.fc7
- Added BR on gettext

* Mon Apr 30 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.5-0.rc4.2.fc7
- Redo failed build.

* Mon Apr 30 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.5-0.rc4.1.fc7
- Updated to 3.0.5 rc4, changeset 14993
- Reduce number of xenstore transactions used for listing domains
- Hack to pre-balloon 2 MB for PV guests as well as HVM

* Thu Apr 26 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.5-0.rc3.14934.2.fc7
- Fixed display of bootloader menu with xm create -c
- Added modprobe for both xenblktap & blktap to deal with rename issues
- Hack to pre-balloon 10 MB for HVM guests

* Thu Apr 26 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.5-0.rc3.14934.1.fc7
- Updated to 3.0.5 rc3, changeset 14934
- Fixed networking for service xend restart & minor IPv6 tweak

* Tue Apr 24 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.5-0.rc2.14889.2.fc7
- Fixed vfb/vkbd device startup race

* Tue Apr 24 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.5-0.rc2.14889.1.fc7
- Updated to xen 3.0.5 rc2, changeset 14889
- Remove use of netloop from network-bridge script
- Add backcompat support to vif-bridge script to translate xenbrN to ethN

* Wed Mar 14 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.4-9.fc7
- Disable access to QEMU monitor over VNC (CVE-2007-0998, bz 230295)

* Tue Mar  6 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.4-8.fc7
- Close QEMU file handles when running network script

* Fri Mar  2 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.4-7.fc7
- Fix interaction of bootloader with blktap (bz 230702)
- Ensure PVFB daemon terminates if domain doesn't startup (bz 230634)

* Thu Feb  8 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.4-6.fc7
- Setup readonly loop devices for readonly disks
- Extended error reporting for hotplug scripts
- Pass all 8 mouse buttons from VNC through to kernel

* Tue Jan 30 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.4-5.fc7
- Don't run the pvfb daemons for HVM guests (bz 225413)
- Fix handling of vnclisten parameter for HVM guests

* Tue Jan 30 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.4-4.fc7
- Fix pygrub memory corruption

* Tue Jan 23 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.4-3.fc7
- Added PVFB back compat for FC5/6 guests

* Mon Jan 22 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.4-2.fc7
- Ensure the arch-x86 header files are included in xen-devel package
- Bring back patch to move /var/xen/dump to /var/lib/xen/dump
- Make /var/log/xen mode 0700

* Thu Jan 11 2007 Daniel P. Berrange <berrange@redhat.com> - 3.0.4-1
- Upgrade to official xen-3.0.4_1 release tarball

* Thu Dec 14 2006 Jeremy Katz <katzj@redhat.com> - 3.0.3-3
- fix the build

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 3.0.3-2
- rebuild for python 2.5

* Tue Oct 24 2006 Daniel P. Berrange <berrange@redhat.com> - 3.0.3-1
- Pull in the official 3.0.3 tarball of xen (changeset 11774).
- Add patches for VNC password authentication (bz 203196)
- Switch /etc/xen directory to be mode 0700 because the config files
  can contain plain text passwords (bz 203196)
- Change the package dependency to python-virtinst to reflect the
  package name change.
- Fix str-2-int cast of VNC port for paravirt framebuffer (bz 211193)

* Wed Oct  4 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-44
- fix having "many" kernels in pygrub

* Wed Oct  4 2006 Stephen C. Tweedie <sct@redhat.com> - 3.0.2-43
- Fix SMBIOS tables for SVM guests [danpb] (bug 207501)

* Fri Sep 29 2006 Daniel P. Berrange <berrange@redhat.com> - 3.0.2-42
- Added vnclisten patches to make VNC only listen on localhost
  out of the box, configurable by 'vnclisten' parameter (bz 203196)

* Thu Sep 28 2006 Stephen C. Tweedie <sct@redhat.com> - 3.0.2-41
- Update to xen-3.0.3-testing changeset 11633

* Thu Sep 28 2006 Stephen C. Tweedie <sct@redhat.com> - 3.0.2-40
- Workaround blktap/xenstore startup race
- Add udev rules for xen blktap devices (srostedt)
- Add support for dynamic blktap device nodes (srostedt)
- Fixes for infinite dom0 cpu usage with blktap
- Fix xm not to die on malformed "tap:" blkif config string
- Enable blktap on kernels without epoll-for-aio support.
- Load the blktap module automatically at startup
- Reenable blktapctrl

* Wed Sep 27 2006 Daniel Berrange <berrange@redhat.com> - 3.0.2-39
- Disable paravirt framebuffer server side rendered cursor (bz 206313)
- Ignore SIGPIPE in paravirt framebuffer daemon to avoid terminating
  on client disconnects while writing data (bz 208025)

* Wed Sep 27 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-38
- Fix cursor in pygrub (#208041)

* Tue Sep 26 2006 Daniel P. Berrange <berrange@redhat.com> - 3.0.2-37
- Removed obsolete scary warnings in package description

* Thu Sep 21 2006 Stephen C. Tweedie <sct@redhat.com> - 3.0.2-36
- Add Requires: kpartx for dom0 access to domU data

* Wed Sep 20 2006 Stephen C. Tweedie <sct@redhat.com> - 3.0.2-35
- Don't strip qemu-dm early, so that we get proper debuginfo (danpb)
- Fix compile problem with latest glibc

* Wed Sep 20 2006 Stephen C. Tweedie <sct@redhat.com> - 3.0.2-34
- Update to xen-unstable changeset 11539
- Threading fixes for libVNCserver (danpb)

* Tue Sep  5 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-33
- update pvfb patch based on upstream feedback

* Tue Sep  5 2006 Juan Quintela <quintela@redhat.com> - 3.0.2-31
- re-enable ia64.

* Thu Aug 31 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-31
- update to changeset 11405

* Thu Aug 31 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-30
- fix pvfb for x86_64

* Wed Aug 30 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-29
- update libvncserver to hopefully fix problems with vnc clients disconnecting

* Tue Aug 29 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-28
- fix a typo

* Mon Aug 28 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-27
- add support for paravirt framebuffer

* Mon Aug 28 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-26
- update to xen-unstable cs 11251
- clean up patches some
- disable ia64 as it doesn't currently build 

* Tue Aug 22 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-25
- make initscript not spew on non-xen kernels (#202945)

* Mon Aug 21 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-24
- remove copy of xenguest-install from this package, require 
  python-xeninst (the new home of xenguest-install)

* Wed Aug  2 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-23
- add patch to fix rtl8139 in FV, switch it back to the default nic
- add necessary ia64 patches (#201040)
- build on ia64

* Fri Jul 28 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-22
- add patch to fix net devices for HVM guests 

* Fri Jul 28 2006 Rik van Riel <riel@redhat.com> - 3.0.2-21
- make sure disk IO from HVM guests actually hits disk (#198851)

* Fri Jul 28 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-20
- don't start blktapctrl for now
- fix HVM guest creation in xenguest-install
- make sure log files have the right SELinux label

* Tue Jul 25 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-19
- fix libblktap symlinks (#199820)
- make libxenstore executable (#197316)
- version libxenstore (markmc) 

* Fri Jul 21 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-18
- include /var/xen/dump in file list
- load blkbk, netbk and netloop when xend starts
- update to cs 10712
- avoid file conflicts with qemu (#199759)

* Wed Jul 19 2006 Mark McLoughlin <markmc@redhat.com> - 3.0.2-17
- libxenstore is unversioned, so make xen-libs own it rather
  than xen-devel

* Wed Jul 19 2006 Mark McLoughlin <markmc@redhat.com> 3.0.2-16
- Fix network-bridge error (#199414)

* Mon Jul 17 2006 Daniel Veillard <veillard@redhat.com> - 3.0.2-15
- desactivating the relocation server in xend conf by default and
  add a warning text about it.

* Thu Jul 13 2006 Stephen C. Tweedie <sct@redhat.com> - 3.0.2-14
- Compile fix: don't #include <linux/compiler.h>

* Thu Jul 13 2006 Stephen C. Tweedie <sct@redhat.com> - 3.0.2-13
- Update to xen-unstable cset 10675
- Remove internal libvncserver build, new qemu device model has its own one
  now.
- Change default FV NIC model from rtl8139 to ne2k_pci until the former works
  better

* Tue Jul 11 2006 Daniel Veillard <veillard@redhat.com> - 3.0.2-12
- bump libvirt requires to 0.1.2
- drop xend httpd localhost server and use the unix socket instead

* Mon Jul 10 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-11
- split into main packages + -libs and -devel subpackages for #198260
- add patch from jfautley to allow specifying other bridge for 
  xenguest-install (#198097)

* Mon Jul  3 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-10
- make xenguest-install work with relative paths to disk 
  images (markmc, #197518)

* Fri Jun 23 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-9
- own /var/run/xend for selinux (#196456, #195952)

* Tue Jun 13 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-8
- fix syntax error in xenguest-install

* Mon Jun 12 2006 Daniel Veillard <veillard@redhat.com> - 3.0.2-7
- more initscript patch to report status #184452

* Wed Jun  7 2006 Stephen C. Tweedie <sct@redhat.com> - 3.0.2-6
- Add BuildRequires: for gnu/stubs-32.h so that x86_64 builds pick up
  glibc32 correctly

* Wed Jun  7 2006 Stephen C. Tweedie <sct@redhat.com> - 3.0.2-5
- Rebase to xen-unstable cset 10278

* Fri May  5 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-4
- update to new snapshot (changeset 9925)

* Thu Apr 27 2006 Daniel Veillard <veillard@redhat.com> - 3.0.2-3
- xen.h now requires xen-compat.h, install it too

* Wed Apr 26 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-2
- -m64 patch isn't needed anymore either

* Tue Apr 25 2006 Jeremy Katz <katzj@redhat.com> - 3.0.2-1
- update to post 3.0.2 snapshot (changeset:   9744:1ad06bd6832d)
- stop applying patches that are upstreamed
- add patches for bootloader to run on all domain creations
- make xenguest-install create a persistent uuid
- use libvirt for domain creation in xenguest-install, slightly improve 
  error handling

* Tue Apr 18 2006 Daniel Veillard <veillard@redhat.com> - 3.0.1-5
- augment the close on exec patch with the fix for #188361

* Thu Mar  9 2006 Jeremy Katz <katzj@redhat.com> - 3.0.1-4
- add udev rule so that /dev/xen/evtchn gets created properly
- make pygrub not use /tmp for SELinux
- make xenguest-install actually unmount its nfs share.  also, don't use /tmp

* Tue Mar  7 2006 Jeremy Katz <katzj@redhat.com> - 3.0.1-3
- set /proc/xen/privcmd and /var/log/xend-debug.log as close on exec to avoid
  SELinux problems
- give better feedback on invalid urls (#184176)

* Mon Mar  6 2006 Stephen Tweedie <sct@redhat.com> - 3.0.1-2
- Use kva mmap to find the xenstore page (upstream xen-unstable cset 9130)

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 3.0.1-1
- fix xenguest-install so that it uses phy: for block devices instead of 
  forcing them over loopback.  
- change package versioning to be a little more accurate

* Thu Mar  2 2006 Stephen Tweedie <sct@redhat.com> - 3.0.1-0.20060301.fc5.3
- Remove unneeded CFLAGS spec file hack

* Thu Mar  2 2006 Rik van Riel <riel@redhat.com> - 3.0.1-0.20060301.fc5.2
- fix 64 bit CFLAGS issue with vmxloader and hvmloader

* Wed Mar  1 2006 Stephen Tweedie <sct@redhat.com> - 3.0.1-0.20060301.fc5.1
- Update to xen-unstable cset 9022

* Tue Feb 28 2006 Stephen Tweedie <sct@redhat.com> - 3.0.1-0.20060228.fc5.1
- Update to xen-unstable cset 9015

* Thu Feb 23 2006 Jeremy Katz <katzj@redhat.com> - 3.0.1-0.20060208.fc5.3
- add patch to ensure we get a unique fifo for boot loader (#182328)
- don't try to read the whole disk if we can't find a partition table 
  with pygrub 
- fix restarting of domains (#179677)

* Thu Feb  9 2006 Jeremy Katz <katzj@redhat.com> - 3.0.1-0.20060208.fc5.2
- fix -h conflict for xenguest-isntall

* Wed Feb  8 2006 Jeremy Katz <katzj@redhat.com> - 3.0.1-0.20060208.fc5.1
- turn on http listener so you can do things with libvir as a user

* Wed Feb  8 2006 Jeremy Katz <katzj@redhat.com> - 3.0.1-0.20060208.fc5
- update to current hg snapshot for HVM support
- update xenguest-install for hvm changes.  allow hvm on svm hardware
- fix a few little xenguest-install bugs

* Tue Feb  7 2006 Jeremy Katz <katzj@redhat.com> - 3.0-0.20060130.fc5.6
- add a hack to fix VMX guests with video to balloon enough (#180375)

* Tue Feb  7 2006 Jeremy Katz <katzj@redhat.com> - 3.0-0.20060130.fc5.5
- fix build for new udev

* Tue Feb  7 2006 Jeremy Katz <katzj@redhat.com> - 3.0-0.20060130.fc5.4
- patch from David Lutterkort to pass macaddr (-m) to xenguest-install
- rework xenguest-install a bit so that it can be used for creating 
  fully-virtualized guests as well as paravirt.  Run with --help for 
  more details (or follow the prompts)
- add more docs (noticed by Andrew Puch)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.0-0.20060130.fc5.3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb  2 2006 Bill Nottingham <notting@redhat.com> 3.0-0.20060130.fc5.3
- disable iptables/ip6tables/arptables on bridging when bringing up a
  Xen bridge. If complicated filtering is needed that uses this, custom
  firewalls will be needed. (#177794)

* Tue Jan 31 2006 Bill Nottingham <notting@redhat.com> 3.0-0.20060130.fc5.2
- use the default network device, don't hardcode eth0

* Tue Jan 31 2006  <sct@redhat.com> - 3.0-0.20060130.fc5.1
- Add xenguest-install.py in /usr/sbin

* Mon Jan 30 2006  <sct@redhat.com> - 3.0-0.20060130.fc5
- Update to xen-unstable from 20060130 (cset 8705)

* Wed Jan 25 2006 Jeremy Katz <katzj@redhat.com> - 3.0-0.20060110.fc5.5
- buildrequire dev86 so that vmx firmware gets built
- include a copy of libvncserver and build vmx device models against it 

* Tue Jan 24 2006 Bill Nottingham <notting@redhat.com> - 3.0-0.20060110.fc5.4
- only put the udev rules in one place

* Fri Jan 20 2006 Jeremy Katz <katzj@redhat.com> - 3.0-0.20060110.fc5.3
- move xsls to xenstore-ls to not conflict (#171863)

* Tue Jan 10 2006  <sct@redhat.com> - 3.0-0.20060110.fc5.1
- Update to xen-unstable from 20060110 (cset 8526)

* Thu Dec 22 2005 Jesse Keating <jkeating@redhat.com> - 3.0-0.20051206.fc5.2
- rebuilt

* Tue Dec  6 2005 Juan Quintela <quintela@trasno.org> - 3.0-0.20051206.fc5.1
- 20051206 version (should be 3.0.0).
- Remove xen-bootloader fixes (integrated upstream).

* Wed Nov 30 2005 Daniel Veillard <veillard@redhat.com> - 3.0-0.20051109.fc5.4
- adding missing headers for libxenctrl and libxenstore
- use libX11-devel build require instead of xorg-x11-devel

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> - 3.0-0.20051109.fc5.3
- change default dom0 min-mem to 256M so that dom0 will try to balloon down

* Sat Nov 12 2005 Jeremy Katz <katzj@redhat.com>
- buildrequire ncurses-devel (reported by Justin Dearing)

* Thu Nov 10 2005 Jeremy Katz <katzj@redhat.com> - 3.0-0.20051109.fc5.2
- actually enable the initscripts

* Wed Nov  9 2005 Jeremy Katz <katzj@redhat.com> - 3.0-0.20051109.fc5.1
- udev rules moved

* Wed Nov  9 2005 Jeremy Katz <katzj@redhat.com> - 3.0-0.20051109.fc5
- update to current -unstable
- add patches to fix pygrub 

* Wed Nov  9 2005 Jeremy Katz <katzj@redhat.com> - 3.0-0.20051108.fc5
- update to current -unstable

* Fri Oct 21 2005 Jeremy Katz <katzj@redhat.com> - 3.0-0.20051021.fc5
- update to current -unstable

* Thu Sep 15 2005 Jeremy Katz <katzj@redhat.com> - 3.0-0.20050912.fc5.1
- doesn't require twisted anymore

* Mon Sep 12 2005 Rik van Riel <riel@redhat.com> 3.0-0.20050912.fc5
- add /var/{lib,run}/xenstored to the %%files section (#167496, #167121)
- upgrade to today's Xen snapshot
- some small build fixes for x86_64
- enable x86_64 builds

* Thu Sep  8 2005 Rik van Riel <riel@redhat.com> 3.0-0.20050908
- explicitly call /usr/sbin/xend from initscript (#167407)
- add xenstored directories to spec file (#167496, #167121)
- misc gcc4 fixes 
- spec file cleanups (#161191)
- upgrade to today's Xen snapshot
- change the version to 3.0-0.<date> (real 3.0 release will be 3.0-1)

* Tue Aug 23 2005 Rik van Riel <riel@redhat.com> 2-20050823
- upgrade to today's Xen snapshot

* Mon Aug 15 2005 Rik van Riel <riel@redhat.com> 2-20050726
- upgrade to a known-working newer Xen, now that execshield works again

* Mon May 30 2005 Rik van Riel <riel@redhat.com> 2-20050530
- create /var/lib/xen/xen-db/migrate directory so "xm save" works (#158895)

* Mon May 23 2005 Rik van Riel <riel@redhat.com> 2-20050522
- change default display method for VMX domains to SDL

* Fri May 20 2005 Rik van Riel <riel@redhat.com> 2-20050520
- qemu device model for VMX

* Thu May 19 2005 Rik van Riel <riel@redhat.com> 2-20050519
- apply some VMX related bugfixes

* Mon Apr 25 2005 Rik van Riel <riel@redhat.com> 2-20050424
- upgrade to last night's snapshot

* Fri Apr 15 2005 Jeremy Katz <katzj@redhat.com>
- patch manpath instead of moving in specfile.  patch sent upstream
- install to native python path instead of /usr/lib/python
- other misc specfile duplication cleanup

* Sun Apr  3 2005 Rik van Riel <riel@redhat.com> 2-20050403
- fix context switch between vcpus in same domain, vcpus > cpus works again

* Sat Apr  2 2005 Rik van Riel <riel@redhat.com> 2-20050402
- move initscripts to /etc/rc.d/init.d (Florian La Roche) (#153188)
- ship only PDF documentation, not the PS or tex duplicates

* Thu Mar 31 2005 Rik van Riel <riel@redhat.com> 2-20050331
- upgrade to new xen hypervisor
- minor gcc4 compile fix

* Mon Mar 28 2005 Rik van Riel <riel@redhat.com> 2-20050328
- do not yet upgrade to new hypervisor ;)
- add barrier to fix SMP boot bug
- add tags target
- add zlib-devel build requires (#150952)

* Wed Mar  9 2005 Rik van Riel <riel@redhat.com> 2-20050308
- upgrade to last night's snapshot
- new compile fix patch

* Sun Mar  6 2005 Rik van Riel <riel@redhat.com> 2-20050305
- the gcc4 compile patches are now upstream
- upgrade to last night's snapshot, drop patches locally

* Fri Mar  4 2005 Rik van Riel <riel@redhat.com> 2-20050303
- finally got everything to compile with gcc4 -Wall -Werror

* Thu Mar  3 2005 Rik van Riel <riel@redhat.com> 2-20050303
- upgrade to last night's Xen-unstable snapshot
- drop printf warnings patch, which is upstream now

* Wed Feb 23 2005 Rik van Riel <riel@redhat.com> 2-20050222
- upgraded to last night's Xen snapshot
- compile warning fixes are now upstream, drop patch

* Sat Feb 19 2005 Rik van Riel <riel@redhat.com> 2-20050219
- fix more compile warnings
- fix the fwrite return check

* Fri Feb 18 2005 Rik van Riel <riel@redhat.com> 2-20050218
- upgrade to last night's Xen snapshot
- a kernel upgrade is needed to run this Xen, the hypervisor
  interface changed slightly
- comment out unused debugging function in plan9 domain builder
  that was giving compile errors with -Werror

* Tue Feb  8 2005 Rik van Riel <riel@redhat.com> 2-20050207
- upgrade to last night's Xen snapshot

* Tue Feb  1 2005 Rik van Riel <riel@redhat.com> 2-20050201.1
- move everything to /var/lib/xen

* Tue Feb  1 2005 Rik van Riel <riel@redhat.com> 2-20050201
- upgrade to new upstream Xen snapshot

* Tue Jan 25 2005 Jeremy Katz <katzj@redhat.com>
- add buildreqs on python-devel and xorg-x11-devel (strange AT nsk.no-ip.org)

* Mon Jan 24 2005 Rik van Riel <riel@redhat.com> - 2-20050124
- fix /etc/xen/scripts/network to not break with ipv6 (also sent upstream)

* Fri Jan 14 2005 Jeremy Katz <katzj@redhat.com> - 2-20050114
- update to new snap
- python-twisted is its own package now
- files are in /usr/lib/python now as well, ugh.

* Tue Jan 11 2005 Rik van Riel <riel@redhat.com>
- add segment fixup patch from xen tree
- fix %%files list for python-twisted

* Mon Jan 10 2005 Rik van Riel <riel@redhat.com>
- grab newer snapshot, that does start up
- add /var/xen/xend-db/{domain,vnet} to %%files section

* Thu Jan  6 2005 Rik van Riel <riel@redhat.com>
- upgrade to new snapshot of xen-unstable

* Mon Dec 13 2004 Rik van Riel <riel@redhat.com>
- build python-twisted as a subpackage
- update to latest upstream Xen snapshot

* Sun Dec  5 2004 Rik van Riel <riel@redhat.com>
- grab new Xen tarball (with wednesday's patch already included)
- transfig is a buildrequire, add it to the spec file

* Wed Dec  1 2004 Rik van Riel <riel@redhat.com>
- fix up Che's spec file a little bit
- create patch to build just Xen, not the kernels

* Wed Dec 01 2004 Che
- initial rpm release
