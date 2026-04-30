## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

### Header
Summary: Collection of basic system utilities
Name: util-linux
Version: 2.41.3
# -p -e rc1
Release: %autorelease -b7
License: GPL-1.0-or-later AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-3.0-or-later AND LGPL-2.1-or-later AND BSD-2-Clause AND BSD-3-Clause AND BSD-4-Clause-UC AND LicenseRef-Fedora-Public-Domain
URL: https://en.wikipedia.org/wiki/Util-linux

### Macros
%global upstream_version %{version}
%global upstream_major %(eval echo %{version} | sed -e 's/\([[:digit:]]*\)\.\([[:digit:]]*\)\.[[:digit:]]*$/\1.\2/')

%global compldir %{_datadir}/bash-completion/completions/

%global pypkg python3
%global pyver 3

### Dependencies
BuildRequires: make
BuildRequires: audit-libs-devel >= 1.0.6
BuildRequires: gettext-devel
BuildRequires: libselinux-devel
BuildRequires: libxcrypt-devel
BuildRequires: ncurses-devel
BuildRequires: readline-devel
BuildRequires: pam-devel
BuildRequires: zlib-devel
BuildRequires: popt-devel
BuildRequires: libutempter-devel
BuildRequires: systemd-devel
BuildRequires: systemd
BuildRequires: libcap-ng-devel
BuildRequires: %{pypkg}-devel
BuildRequires: gcc
BuildRequires: rubygem-asciidoctor
BuildRequires: po4a
BuildRequires: sqlite-devel
%ifarch ppc64le
BuildRequires: librtas-devel
%endif

# enable if make changes to build-system
#BuildRequires: autoconf
#BuildRequires: automake
#BuildRequires: libtool
BuildRequires: bison
BuildRequires: flex

### Sources
Source0: https://www.kernel.org/pub/linux/utils/util-linux/v%{upstream_major}/util-linux-%{upstream_version}.tar.xz
Source1: util-linux-login.pamd
Source2: util-linux-remote.pamd
Source3: util-linux-chsh-chfn.pamd
Source5: adjtime
Source12: util-linux-su.pamd
Source13: util-linux-su-l.pamd
Source14: util-linux-runuser.pamd
Source15: util-linux-runuser-l.pamd

### Obsoletes & Conflicts & Provides
Conflicts: initscripts < 9.79-4
Conflicts: bash-completion < 1:2.1-1
# su(1) and runuser(1) merged into util-linux v2.22
Conflicts: coreutils < 8.20
# eject has been merged into util-linux v2.22
Obsoletes: eject <= 2.1.5
Provides: eject = 2.1.6
# rfkill has been merged into util-linux v2.31
Obsoletes: rfkill <= 0.5
Provides: rfkill = 0.5
# sulogin, utmpdump merged into util-linux v2.22;
# last, lastb merged into util-linux v2.24
Conflicts: sysvinit-tools < 2.88-14
# rename from util-linux-ng back to util-linux
Obsoletes: util-linux-ng < 2.19
Provides: util-linux-ng = %{version}-%{release}
Conflicts: filesystem < 3
Provides: /sbin/nologin
Provides: /sbin/findfs
# util-linux-user was dropped in 2.39-1 and its contents moved back
# to util-linux
Obsoletes: util-linux-user < 2.39-1
Provides: util-linux-user = %{version}-%{release}

Requires(post): coreutils
Requires: (pam >= 1.1.3-7 if systemd)
Requires: (/etc/pam.d/system-auth if systemd)
Requires: audit-libs >= 1.0.6
Requires: libuuid = %{version}-%{release}
Requires: libblkid = %{version}-%{release}
Requires: libmount = %{version}-%{release}
Requires: libsmartcols = %{version}-%{release}
Requires: libfdisk = %{version}-%{release}
Requires: liblastlog2 = %{version}-%{release}
Requires: util-linux-core = %{version}-%{release}

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/runuser
Provides:       /usr/sbin/sfdisk
%endif

### Ready for upstream?
###
# 151635 - makeing /var/log/lastlog
Patch0: login-lastlog-create.patch
# Add `/run/motd.d` to the hardcoded MOTD_FILE
# https://github.com/coreos/console-login-helper-messages/issues/60
Patch1: login-default-motd-file.patch

# https://github.com/dracut-ng/dracut-ng/issues/1384
# 2367956 - EROFS vs. the latest util-linux and kernel
Patch2: 0001-libmount-disable-EROFS-backing-file-support.patch


# Upstream backports
Patch3: 0003-build-sys-gcc-ignore-Wunused-but-set-variable-for-bi.patch
Patch4: 0004-blkid-Drop-const-from-blkid_partitions_get_name.patch


%description
The util-linux package contains a large variety of low-level system
utilities that are necessary for a Linux system to function. Among
others, util-linux contains the fdisk configuration tool and the login
program.


%package -n util-linux-core
Summary: The most essential utilities from the util-linux suite
License: GPL-2.0-only AND GPL-2.0-or-later AND BSD-2-Clause AND BSD-3-Clause AND BSD-4-Clause-UC AND LicenseRef-Fedora-Public-Domain

Provides: /bin/dmesg
Provides: /bin/kill
Provides: /bin/more
Provides: /bin/mount
Provides: /bin/umount
Provides: /sbin/blkid
Provides: /sbin/blockdev
Provides: /sbin/fsck
# hardlink has been merged into util-linux v2.34
Obsoletes: hardlink <= 1:1.3-9
Provides: hardlink = 1:1.3-9
Requires: libuuid = %{version}-%{release}
Requires: libblkid = %{version}-%{release}
Requires: libmount = %{version}-%{release}
Requires: libsmartcols = %{version}-%{release}
# old versions of e2fsprogs contain fsck, uuidgen
Conflicts: e2fsprogs < 1.41.8-5

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/fsck
%endif

%description -n util-linux-core
This is a very basic set of Linux utilities that is necessary on
minimal installations.


%package -n libfdisk
Summary: Partitioning library for fdisk-like programs
License: LGPL-2.1-or-later

%description -n libfdisk
This is library for fdisk-like programs, part of util-linux.


%package -n libfdisk-devel
Summary:  Partitioning library for fdisk-like programs
License: LGPL-2.1-or-later
Requires: libfdisk%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n libfdisk-devel
This is development library and headers for fdisk-like programs,
part of util-linux.


%package -n libsmartcols
Summary: Formatting library for ls-like programs
License: LGPL-2.1-or-later

%description -n libsmartcols
This is library for ls-like terminal programs, part of util-linux.


%package -n libsmartcols-devel
Summary: Formatting library for ls-like programs
License: LGPL-2.1-or-later
Requires: libsmartcols%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n libsmartcols-devel
This is development library and headers for ls-like terminal programs,
part of util-linux.


%package -n libmount
Summary: Device mounting library
License: LGPL-2.1-or-later
Requires: libblkid%{?_isa} = %{version}-%{release}
Requires: libuuid%{?_isa} = %{version}-%{release}
Conflicts: filesystem < 3

%description -n libmount
This is the device mounting library, part of util-linux.


%package -n libmount-devel
Summary: Device mounting library
License: LGPL-2.1-or-later
Requires: libmount%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n libmount-devel
This is the device mounting development library and headers,
part of util-linux.


%package -n liblastlog2
Summary: lastlog database library and PAM module
License: BSD-2-Clause

%description -n liblastlog2
This is the lastlog database library and PAM module, part of util-linux.


%package -n liblastlog2-devel
Summary: lastlog database library
License: BSD-2-Clause
Requires: liblastlog2%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n liblastlog2-devel
This is the lastlog database development library and headers,
part of util-linux.


%package -n libblkid
Summary: Block device ID library
License: LGPL-2.1-or-later
Requires: libuuid%{?_isa} = %{version}-%{release}
Conflicts: filesystem < 3

%description -n libblkid
This is block device identification library, part of util-linux.


%package -n libblkid-devel
Summary: Block device ID library
License: LGPL-2.1-or-later
Requires: libblkid%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n libblkid-devel
This is the block device identification development library and headers,
part of util-linux.


%package -n libuuid
Summary: Universally unique ID library
License: BSD-3-Clause
Conflicts: filesystem < 3

%description -n libuuid
This is the universally unique ID library, part of util-linux.

The libuuid library generates and parses 128-bit universally unique
id's (UUID's).  A UUID is an identifier that is unique across both
space and time, with respect to the space of all UUIDs.  A UUID can
be used for multiple purposes, from tagging objects with an extremely
short lifetime, to reliably identifying very persistent objects
across a network.

See also the "uuid" package, which is a separate implementation.

%package -n libuuid-devel
Summary: Universally unique ID library
License: BSD-3-Clause AND LGPL-2.1-or-later
Requires: libuuid%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n libuuid-devel
This is the universally unique ID development library and headers,
part of util-linux.

The libuuid library generates and parses 128-bit universally unique
id's (UUID's).  A UUID is an identifier that is unique across both
space and time, with respect to the space of all UUIDs.  A UUID can
be used for multiple purposes, from tagging objects with an extremely
short lifetime, to reliably identifying very persistent objects
across a network.

See also the "uuid-devel" package, which is a separate implementation.


%package -n uuidd
Summary: Helper daemon to guarantee uniqueness of time-based UUIDs
Requires: libuuid = %{version}-%{release}
License: GPL-2.0-only
Requires(pre): shadow-utils
%{?systemd_ordering}

%description -n uuidd
The uuidd package contains a userspace daemon (uuidd) which guarantees
uniqueness of time-based UUID generation even at very high rates on
SMP systems.


%package -n %{pypkg}-libmount
Summary: Python bindings for the libmount library
Requires: libmount%{?_isa} = %{version}-%{release}
License: LGPL-2.1-or-later

%description -n %{pypkg}-libmount
The libmount-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libmount library to work with mount tables (fstab,
mountinfo, etc) and mount filesystems.


%package -n util-linux-i18n
Summary: Internationalization pack for util-linux
Requires: util-linux = %{version}-%{release}
License: GPL-2.0-or-later

%description -n util-linux-i18n
Internationalization pack with translated messages and manual pages for
util-linux commands.

%package -n util-linux-script
Summary: Utilities for creating and replaying typescripts of terminal session
Requires: util-linux = %{version}-%{release}

%description -n util-linux-script
The utilities scripts, scriptreplay, and scriptlive are used to create and replay terminal sessions.

%prep
%autosetup -p1 -n %{name}-%{upstream_version}

%build
unset LINGUAS || :

# enable only when make a change to the build-system
#./autogen.sh


export CFLAGS="-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64 $RPM_OPT_FLAGS"
export SUID_CFLAGS="-fpie"
export SUID_LDFLAGS="-pie -Wl,-z,relro -Wl,-z,now"
export DAEMON_CFLAGS="$SUID_CFLAGS"
export DAEMON_LDFLAGS="$SUID_LDFLAGS"
%configure \
	--with-systemdsystemunitdir=%{_unitdir} \
	--without-user \
	--disable-silent-rules \
	--disable-bfs \
	--disable-pg \
	--enable-chfn-chsh \
	--enable-usrdir-path \
	--enable-write \
	--disable-raw \
	--enable-hardlink \
	--enable-fdformat \
	--enable-asciidoc \
	--with-python=%{pyver} \
	--with-systemd \
	--with-udev \
	--with-selinux \
	--with-audit \
	--with-utempter \
	--disable-makeinstall-chown \
%ifarch s390 s390x
	--disable-hwclock \
	--disable-fdformat
%endif

# build util-linux
%make_build

%check
#to run tests use "--with check"
%if %{?_with_check:1}%{!?_with_check:0}
make check
%endif


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man{1,6,8,5}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/{pam.d,security/console.apps}

# install util-linux
%make_install

# And a dirs that the makefiles don't create
install -d %{buildroot}%{_rundir}/uuidd
install -d %{buildroot}%{_sharedstatedir}/libuuid
install -d %{buildroot}%{_sharedstatedir}/lastlog

# /etc/adjtime
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/adjtime

# libtool junk
rm -rf %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.la
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.a

%ifarch %{sparc}
rm -rf %{buildroot}%{_bindir}/sunhostid
cat << E-O-F > %{buildroot}%{_bindir}/sunhostid
#!/bin/sh
# this should be _bindir/sunhostid or somesuch.
# Copyright 1999 Peter Jones, <pjones@redhat.com> .
# GPL and all that good stuff apply.
(
idprom=\`cat /proc/openprom/idprom\`
echo \$idprom|dd bs=1 skip=2 count=2
echo \$idprom|dd bs=1 skip=27 count=6
echo
) 2>/dev/null
E-O-F
chmod 755 %{buildroot}%{_bindir}/sunhostid
%endif

# PAM settings
{
	pushd %{buildroot}%{_sysconfdir}/pam.d
	install -m 644 %{SOURCE1} ./login
	install -m 644 %{SOURCE2} ./remote
	install -m 644 %{SOURCE3} ./chsh
	install -m 644 %{SOURCE3} ./chfn
	install -m 644 %{SOURCE12} ./su
	install -m 644 %{SOURCE13} ./su-l
	install -m 644 %{SOURCE14} ./runuser
	install -m 644 %{SOURCE15} ./runuser-l
	popd
}

%ifnarch s390 s390x
ln -sf hwclock %{buildroot}%{_sbindir}/clock
echo ".so man8/hwclock.8" > %{buildroot}%{_mandir}/man8/clock.8
%endif

# unsupported on SPARCs
%ifarch %{sparc}
rm -f %{buildroot}/sbin/sfdisk \
      %{buildroot}%{_mandir}/man8/sfdisk.8* \
      %{buildroot}/sbin/cfdisk \
      %{buildroot}%{_mandir}/man8/cfdisk.8*
%endif

# we install getopt-*.{bash,tcsh} by doc directive
#chmod 644 misc-utils/getopt-*.{bash,tcsh}
#rm -f %{buildroot}%{_datadir}/doc/util-linux/getopt/*
#rmdir %{buildroot}%{_datadir}/doc/util-linux/getopt

ln -sf ../proc/self/mounts %{buildroot}/etc/mtab

# remove static libs
rm -f %{buildroot}%{_libdir}/lib{uuid,blkid,mount,smartcols,fdisk,lastlog2}.a

# temporary remove to avoid conflicts with bash-completion pkg
rm -f %{buildroot}%{compldir}/{mount,umount}

# remove unvanted translations (conflicts with shadow-utils)
rm -f %{buildroot}%{_mandir}/*/man1/newgrp.*
rm -f %{buildroot}%{_mandir}/*/man8/vigr.*
rm -f %{buildroot}%{_mandir}/*/man8/vipw.*


# find MO files
%find_lang %{name} --all-name --with-man

touch %{name}.files

# create list of setarch(8) symlinks
find  %{buildroot}%{_bindir}/ -regextype posix-egrep -type l \
	-regex ".*(linux32|linux64|s390|s390x|i386|ppc|ppc64|ppc32|sparc|sparc64|sparc32|sparc32bash|mips|mips64|mips32|ia64|x86_64|uname26)$" \
	-printf "%{_bindir}/%f\n" >> %{name}.files

find  %{buildroot}%{_mandir}/man8 -regextype posix-egrep  \
	-regex ".*(linux32|linux64|s390|s390x|i386|ppc|ppc64|ppc32|sparc|sparc64|sparc32|sparc32bash|mips|mips64|mips32|ia64|x86_64|uname26)\.8.*" \
	-printf "%{_mandir}/man8/%f*\n" >> %{name}.files

%if "%{_sbindir}" == "%{_bindir}"
# Autotools installation script gets the location wrong :(
mv -v %{buildroot}/usr/sbin/* %{buildroot}/usr/bin/
%endif


%post
%systemd_post fstrim.{service,timer}

%post -n liblastlog2
%systemd_post lastlog2-import.service


%preun
%systemd_preun fstrim.{service,timer}


%postun
%systemd_postun_with_restart fstrim.timer
%systemd_postun fstrim.service

%postun -n liblastlog2
%systemd_postun lastlog2-import.service


# Please, keep uuidd running after installation! Note that systemd_post is
# "systemctl preset" and it enable/disable service only.
%post -n uuidd
%systemd_post uuidd.service
if [ $1 -eq 1 ] && [ -x /usr/bin/systemctl ]; then
	# install
	/usr/bin/systemctl start uuidd.service > /dev/null 2>&1 || :
fi

%preun -n uuidd
%systemd_preun uuidd.socket uuidd.service

%postun -n uuidd
%systemd_postun_with_restart uuidd.socket uuidd.service

%triggerpostun -- util-linux < 2.40-0.2
if [ $1 -gt 1 ] && [ -x /usr/bin/systemctl ] ; then
        # Enable fstrim.timer for upgrades from older versions
        /usr/bin/systemctl --no-reload preset fstrim.timer || :
fi

%files -f %{name}.files
%doc README NEWS AUTHORS
%doc Documentation/deprecated.txt
%license Documentation/licenses/*
%doc misc-utils/getopt-*.{bash,tcsh}

%config(noreplace)	%{_sysconfdir}/pam.d/login
%config(noreplace)	%{_sysconfdir}/pam.d/remote
%config(noreplace)	%{_sysconfdir}/pam.d/su
%config(noreplace)	%{_sysconfdir}/pam.d/su-l
%config(noreplace)	%{_sysconfdir}/pam.d/runuser
%config(noreplace)	%{_sysconfdir}/pam.d/runuser-l
%config(noreplace)	%{_sysconfdir}/pam.d/chfn
%config(noreplace)	%{_sysconfdir}/pam.d/chsh

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/adjtime

%attr(4755,root,root)	%{_bindir}/su
%attr(755,root,root)	%{_bindir}/login
%attr(4711,root,root)	%{_bindir}/chfn
%attr(4711,root,root)	%{_bindir}/chsh

%{_unitdir}/fstrim.*

%{_bindir}/bits
%{_bindir}/cal
%{_bindir}/chmem
%{_bindir}/choom
%{_bindir}/col
%{_bindir}/colcrt
%{_bindir}/colrm
%{_bindir}/column
%{_bindir}/coresched
%{_bindir}/eject
%{_bindir}/enosys
%{_bindir}/exch
%{_bindir}/fallocate
%{_bindir}/fincore
%{_bindir}/fadvise
%{_bindir}/getopt
%{_bindir}/hexdump
%{_bindir}/irqtop
%{_bindir}/isosize
%{_bindir}/last
%{_bindir}/lastb
%{_bindir}/lastlog2
%{_bindir}/look
%{_bindir}/lsblk
%{_bindir}/lscpu
%{_bindir}/lsclocks
%{_bindir}/lsfd
%{_bindir}/lsipc
%{_bindir}/lsirq
%{_bindir}/lslocks
%{_bindir}/lslogins
%{_bindir}/lsmem
%{_bindir}/lsns
%{_bindir}/mcookie
%{_bindir}/mesg
%{_bindir}/namei
%{_bindir}/pipesz
%{_bindir}/prlimit
%{_bindir}/rename
%{_bindir}/rev
%{_bindir}/setarch
%{_bindir}/setpgid
%{_bindir}/setpriv
%{_bindir}/setterm
%{_bindir}/uclampset
%{_bindir}/ul
%{_bindir}/utmpdump
%{_bindir}/uuidgen
%{_bindir}/uuidparse
%{_bindir}/waitpid
%{_bindir}/wall
%{_bindir}/wdctl
%{_bindir}/whereis
%{_bindir}/write

%{_mandir}/man1/bits.1*
%{_mandir}/man1/cal.1*
%{_mandir}/man1/chfn.1*
%{_mandir}/man1/choom.1*
%{_mandir}/man1/chsh.1*
%{_mandir}/man1/col.1*
%{_mandir}/man1/colcrt.1*
%{_mandir}/man1/colrm.1*
%{_mandir}/man1/column.1*
%{_mandir}/man1/coresched.1.*
%{_mandir}/man1/eject.1*
%{_mandir}/man1/enosys.1*
%{_mandir}/man1/exch.1*
%{_mandir}/man1/fadvise.1*
%{_mandir}/man1/fallocate.1*
%{_mandir}/man1/fincore.1*
%{_mandir}/man1/getopt.1*
%{_mandir}/man1/hexdump.1*
%{_mandir}/man1/irqtop.1*
%{_mandir}/man1/last.1*
%{_mandir}/man1/lastb.1*
%{_mandir}/man1/login.1*
%{_mandir}/man1/look.1*
%{_mandir}/man1/lscpu.1*
%{_mandir}/man1/lsclocks.1*
%{_mandir}/man1/lsfd.1*
%{_mandir}/man1/lsipc.1*
%{_mandir}/man1/lsirq.1*
%{_mandir}/man1/lslogins.1*
%{_mandir}/man1/lsmem.1*
%{_mandir}/man1/mcookie.1*
%{_mandir}/man1/mesg.1*
%{_mandir}/man1/namei.1*
%{_mandir}/man1/pipesz.1.*
%{_mandir}/man1/prlimit.1*
%{_mandir}/man1/rename.1*
%{_mandir}/man1/rev.1*
%{_mandir}/man1/runuser.1*
%{_mandir}/man1/setpgid.1*
%{_mandir}/man1/setpriv.1*
%{_mandir}/man1/setterm.1*
%{_mandir}/man1/su.1*
%{_mandir}/man1/uclampset.1.*
%{_mandir}/man1/ul.1*
%{_mandir}/man1/utmpdump.1.gz
%{_mandir}/man1/uuidgen.1*
%{_mandir}/man1/uuidparse.1*
%{_mandir}/man1/waitpid.1.*
%{_mandir}/man1/wall.1*
%{_mandir}/man1/whereis.1*
%{_mandir}/man1/write.1*
%{_mandir}/man5/fstab.5*
%{_mandir}/man5/scols-filter.5*
%{_mandir}/man5/terminal-colors.d.5*
%{_mandir}/man8/addpart.8*
%{_mandir}/man8/blkdiscard.8*
%{_mandir}/man8/blkpr.8.*
%{_mandir}/man8/blkzone.8*
%{_mandir}/man8/chcpu.8*
%{_mandir}/man8/chmem.8*
%{_mandir}/man8/ctrlaltdel.8*
%{_mandir}/man8/delpart.8*
%{_mandir}/man8/fdisk.8*
%{_mandir}/man8/findfs.8*
%{_mandir}/man8/fsck.cramfs.8*
%{_mandir}/man8/fsck.minix.8*
%{_mandir}/man8/fsfreeze.8*
%{_mandir}/man8/fstrim.8*
%{_mandir}/man8/isosize.8*
%{_mandir}/man8/lastlog2.8*
%{_mandir}/man8/ldattach.8*
%{_mandir}/man8/lsblk.8*
%{_mandir}/man8/lslocks.8*
%{_mandir}/man8/lsns.8*
%{_mandir}/man8/mkfs.8*
%{_mandir}/man8/mkfs.cramfs.8*
%{_mandir}/man8/mkfs.minix.8*
%{_mandir}/man8/nologin.8*
%{_mandir}/man8/pivot_root.8*
%{_mandir}/man8/readprofile.8*
%{_mandir}/man8/resizepart.8*
%{_mandir}/man8/rfkill.8*
%{_mandir}/man8/rtcwake.8*
%{_mandir}/man8/setarch.8*
%{_mandir}/man8/swaplabel.8*
%{_mandir}/man8/wdctl.8.gz
%{_mandir}/man8/wipefs.8*
%{_mandir}/man8/zramctl.8*
%{_sbindir}/addpart
%{_sbindir}/blkdiscard
%{_sbindir}/blkpr
%{_sbindir}/blkzone
%{_sbindir}/chcpu
%{_sbindir}/ctrlaltdel
%{_sbindir}/delpart
%{_sbindir}/fdisk
%{_sbindir}/findfs
%{_sbindir}/fsck.cramfs
%{_sbindir}/fsck.minix
%{_sbindir}/fsfreeze
%{_sbindir}/fstrim
%{_sbindir}/ldattach
%{_sbindir}/mkfs
%{_sbindir}/mkfs.cramfs
%{_sbindir}/mkfs.minix
%{_sbindir}/nologin
%{_sbindir}/pivot_root
%{_sbindir}/readprofile
%{_sbindir}/resizepart
%{_sbindir}/rfkill
%{_sbindir}/rtcwake
%{_sbindir}/runuser
%{_sbindir}/swaplabel
%{_sbindir}/wipefs
%{_sbindir}/zramctl

%{compldir}/addpart
%{compldir}/blkdiscard
%{compldir}/blkzone
%{compldir}/bits
%{compldir}/blkpr
%{compldir}/cal
%{compldir}/chcpu
%{compldir}/chfn
%{compldir}/chmem
%{compldir}/chsh
%{compldir}/col
%{compldir}/choom
%{compldir}/colcrt
%{compldir}/colrm
%{compldir}/column
%{compldir}/coresched
%{compldir}/ctrlaltdel
%{compldir}/delpart
%{compldir}/eject
%{compldir}/enosys
%{compldir}/exch
%{compldir}/fadvise
%{compldir}/fallocate
%{compldir}/fdisk
%{compldir}/fincore
%{compldir}/findfs
%{compldir}/fsck.cramfs
%{compldir}/fsck.minix
%{compldir}/fsfreeze
%{compldir}/fstrim
%{compldir}/getopt
%{compldir}/hexdump
%{compldir}/irqtop
%{compldir}/isosize
%{compldir}/last
%{compldir}/lastb
%{compldir}/lastlog2
%{compldir}/ldattach
%{compldir}/look
%{compldir}/lsblk
%{compldir}/lscpu
%{compldir}/lsclocks
%{compldir}/lsfd
%{compldir}/lsipc
%{compldir}/lsirq
%{compldir}/lslocks
%{compldir}/lslogins
%{compldir}/lsmem
%{compldir}/lsns
%{compldir}/mcookie
%{compldir}/mesg
%{compldir}/mkfs
%{compldir}/mkfs.cramfs
%{compldir}/mkfs.minix
%{compldir}/namei
%{compldir}/pipesz
%{compldir}/pivot_root
%{compldir}/prlimit
%{compldir}/readprofile
%{compldir}/rename
%{compldir}/resizepart
%{compldir}/rev
%{compldir}/rfkill
%{compldir}/rtcwake
%{compldir}/runuser
%{compldir}/setarch
%{compldir}/setpriv
%{compldir}/setpgid
%{compldir}/setterm
%{compldir}/su
%{compldir}/swaplabel
%{compldir}/uclampset
%{compldir}/ul
%{compldir}/utmpdump
%{compldir}/uuidgen
%{compldir}/uuidparse
%{compldir}/wall
%{compldir}/waitpid
%{compldir}/wdctl
%{compldir}/whereis
%{compldir}/wipefs
%{compldir}/write
%{compldir}/zramctl

%ifnarch s390 s390x
%{_sbindir}/clock
%{_sbindir}/fdformat
%{_sbindir}/hwclock
%{_mandir}/man8/fdformat.8*
%{_mandir}/man8/hwclock.8*
%{_mandir}/man8/clock.8*
%{_mandir}/man5/adjtime_config.5*
%{compldir}/fdformat
%{compldir}/hwclock
%endif

%ifnarch %{sparc}
%{_sbindir}/cfdisk
%{_sbindir}/sfdisk
%{_mandir}/man8/cfdisk.8*
%{_mandir}/man8/sfdisk.8*
%{compldir}/cfdisk
%{compldir}/sfdisk
%endif

%ifarch %{sparc}
%{_bindir}/sunhostid
%endif


%files -n util-linux-core
%license Documentation/licenses/*
%attr(4755,root,root)	%{_bindir}/mount
%attr(4755,root,root)	%{_bindir}/umount
%{_bindir}/chrt
%{_bindir}/dmesg
%{_bindir}/findmnt
%{_bindir}/flock
%{_bindir}/hardlink
%{_bindir}/ionice
%{_bindir}/ipcmk
%{_bindir}/ipcrm
%{_bindir}/ipcs
%{_bindir}/kill
%{_bindir}/logger
%{_bindir}/more
%{_bindir}/mountpoint
%{_bindir}/nsenter
%{_bindir}/renice
%{_bindir}/setsid
%{_bindir}/taskset
%{_bindir}/unshare
%{compldir}/blkid
%{compldir}/blockdev
%{compldir}/chrt
%{compldir}/dmesg
%{compldir}/findmnt
%{compldir}/flock
%{compldir}/hardlink
%{compldir}/fsck
%{compldir}/ionice
%{compldir}/ipcmk
%{compldir}/ipcrm
%{compldir}/ipcs
%{compldir}/logger
%{compldir}/losetup
%{compldir}/mkswap
%{compldir}/more
%{compldir}/mountpoint
%{compldir}/nsenter
%{compldir}/partx
%{compldir}/renice
%{compldir}/setsid
%{compldir}/swapoff
%{compldir}/swapon
%{compldir}/taskset
%{compldir}/unshare
%{_mandir}/man1/chrt.1*
%{_mandir}/man1/dmesg.1*
%{_mandir}/man1/flock.1*
%{_mandir}/man1/hardlink.1*
%{_mandir}/man1/ionice.1*
%{_mandir}/man1/ipcmk.1*
%{_mandir}/man1/ipcrm.1*
%{_mandir}/man1/ipcs.1*
%{_mandir}/man1/kill.1*
%{_mandir}/man1/logger.1*
%{_mandir}/man1/more.1*
%{_mandir}/man1/mountpoint.1*
%{_mandir}/man1/nsenter.1*
%{_mandir}/man1/renice.1*
%{_mandir}/man1/setsid.1*
%{_mandir}/man1/taskset.1*
%{_mandir}/man1/unshare.1*
%{_mandir}/man8/agetty.8*
%{_mandir}/man8/blkid.8*
%{_mandir}/man8/blockdev.8*
%{_mandir}/man8/findmnt.8*
%{_mandir}/man8/fsck.8*
%{_mandir}/man8/losetup.8*
%{_mandir}/man8/mkswap.8*
%{_mandir}/man8/mount.8*
%{_mandir}/man8/partx.8*
%{_mandir}/man8/sulogin.8*
%{_mandir}/man8/swapoff.8*
%{_mandir}/man8/swapon.8*
%{_mandir}/man8/switch_root.8*
%{_mandir}/man8/umount.8*
%{_sbindir}/agetty
%{_sbindir}/blkid
%{_sbindir}/blockdev
%{_sbindir}/fsck
%{_sbindir}/losetup
%{_sbindir}/mkswap
%{_sbindir}/partx
%{_sbindir}/sulogin
%{_sbindir}/swapoff
%{_sbindir}/swapon
%{_sbindir}/switch_root
/etc/mtab


%files -n uuidd
%license Documentation/licenses/COPYING.GPL-2.0-only
%{_mandir}/man8/uuidd.8*
%{_sbindir}/uuidd
%{_unitdir}/uuidd.*
%dir %attr(2775, uuidd, uuidd) %{_sharedstatedir}/libuuid
%dir %attr(2775, uuidd, uuidd) %{_rundir}/uuidd
%{compldir}/uuidd
%{_tmpfilesdir}/uuidd-tmpfiles.conf
%{_sysusersdir}/uuidd-sysusers.conf


%files -n libfdisk
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libfdisk.so.*

%files -n libfdisk-devel
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libfdisk.so
%{_includedir}/libfdisk
%{_libdir}/pkgconfig/fdisk.pc


%files -n libsmartcols
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libsmartcols.so.*

%files -n libsmartcols-devel
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libsmartcols.so
%{_includedir}/libsmartcols
%{_libdir}/pkgconfig/smartcols.pc


%files -n libmount
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libmount.so.*

%files -n libmount-devel
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libmount.so
%{_includedir}/libmount
%{_libdir}/pkgconfig/mount.pc


%files -n liblastlog2
%license Documentation/licenses/COPYING.BSD-2-Clause
%dir %{_sharedstatedir}/lastlog
%{_libdir}/liblastlog2.so.*
%{_pam_moduledir}/pam_lastlog2.so
%{_tmpfilesdir}/lastlog2-tmpfiles.conf
%{_unitdir}/lastlog2*
%{_mandir}/man8/pam_lastlog2.8*

%files -n liblastlog2-devel
%license Documentation/licenses/COPYING.BSD-2-Clause
%{_libdir}/liblastlog2.so
%{_includedir}/liblastlog2
%{_libdir}/pkgconfig/lastlog2.pc
%{_mandir}/man3/lastlog2.3.*
%{_mandir}/man3/ll2_import_lastlog.3*
%{_mandir}/man3/ll2_read_all.3*
%{_mandir}/man3/ll2_read_entry.3*
%{_mandir}/man3/ll2_remove_entry.3*
%{_mandir}/man3/ll2_rename_user.3*
%{_mandir}/man3/ll2_update_login_time.3*
%{_mandir}/man3/ll2_write_entry.3*


%files -n libblkid
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libblkid.so.*

%files -n libblkid-devel
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libblkid.so
%{_includedir}/blkid
%{_mandir}/man3/libblkid.3*
%{_libdir}/pkgconfig/blkid.pc


%files -n libuuid
%license Documentation/licenses/COPYING.BSD-3-Clause
%{_libdir}/libuuid.so.*

%files -n libuuid-devel
%license Documentation/licenses/COPYING.BSD-3-Clause Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/libuuid.so
%{_includedir}/uuid
%{_mandir}/man3/uuid.3*
%{_mandir}/man3/uuid_clear.3*
%{_mandir}/man3/uuid_compare.3*
%{_mandir}/man3/uuid_copy.3*
%{_mandir}/man3/uuid_generate.3*
%{_mandir}/man3/uuid_generate_random.3*
%{_mandir}/man3/uuid_generate_time.3*
%{_mandir}/man3/uuid_generate_time_safe.3*
%{_mandir}/man3/uuid_is_null.3*
%{_mandir}/man3/uuid_parse.3*
%{_mandir}/man3/uuid_time.3*
%{_mandir}/man3/uuid_unparse.3*
%{_libdir}/pkgconfig/uuid.pc

%files -n %{pypkg}-libmount
%license Documentation/licenses/COPYING.LGPL-2.1-or-later
%{_libdir}/python*/site-packages/libmount/

%files -n util-linux-i18n -f %{name}.lang
%license Documentation/licenses/COPYING.GPL-2.0-or-later

%files -n util-linux-script
%{_bindir}/script
%{_bindir}/scriptlive
%{_bindir}/scriptreplay
%{_mandir}/man1/script.1*
%{_mandir}/man1/scriptlive.1*
%{_mandir}/man1/scriptreplay.1*
%{compldir}/script
%{compldir}/scriptlive
%{compldir}/scriptreplay

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2.41.3-10
- test: add initial lock files

* Mon Jan 12 2026 Karel Zak <kzak@redhat.com> - 2.41.3-9
- enable BuildRequires for parsers

* Mon Jan 12 2026 Karel Zak <kzak@redhat.com> - 2.41.3-8
- fix built on new gcc (bison based code and libblkid API)

* Mon Dec 15 2025 Karel Zak <kzak@redhat.com> - 2.41.3-7
- upgrade to upstream release v2.41.3

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.41.1-17
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.41.1-16
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Aug 05 2025 Karel Zak <kzak@redhat.com> - 2.41.1-15
- use RPM macros for /var/lib and /run

* Tue Aug 05 2025 Karel Zak <kzak@redhat.com> - 2.41.1-14
- add /var/lib/liblastlog to files list

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.41.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Karel Zak <kzak@fedoraproject.org> - 2.41.1-12
- Merge #24 `tests: migrate from STI to TMT`

* Tue Jul 15 2025 Karel Zak <kzak@redhat.com> - 2.41.1-11
- enable lastlog2-import.service

* Tue Jun 24 2025 Karel Zak <kzak@redhat.com> - 2.41.1-10
- Fix ldattach build on recent glibc headers.

* Tue Jun 24 2025 Karel Zak <kzak@redhat.com> - 2.41.1-9
- Temporarily disable support for EROFS backing files.

* Tue Jun 24 2025 Karel Zak <kzak@redhat.com> - 2.41.1-8
- remove obsolete patch

* Tue Jun 24 2025 Karel Zak <kzak@redhat.com> - 2.41.1-7
- upgrade to upstream release v2.41.1
  https://www.kernel.org/pub/linux/utils/util-
  linux/v2.41/v2.41-ReleaseNotes
- add lastlog2 library and PAM module
- add new utils bits, coresched and lastlog2

* Mon Jun 09 2025 Python Maint <python-maint@redhat.com> - 2.40.4-8
- Rebuilt for Python 3.14

* Mon Jun 09 2025 Miro Hrončok <miro@hroncok.cz> - 2.40.4-7
- Revert to util-linux-2.40.4-7 to rebuild it for Python 3.14

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.41-3
- Rebuilt for Python 3.14

* Mon May 12 2025 Karel Zak <kzak@redhat.com> - 2.41-2
- add BuildRequires for lastlog2

* Mon May 12 2025 Karel Zak <kzak@redhat.com> - 2.41-1
- upgrade to upstream release v2.41
  https://www.kernel.org/pub/linux/utils/util-
  linux/v2.41/v2.41-ReleaseNotes
- add lastlog2 library and PAM module
- add new utils bits, coresched and lastlog2

* Wed Feb 19 2025 Dusty Mabe <dusty@dustymabe.com> - 2.40.4-7
- backport blkid: allow up to 64k erofs block sizes

* Wed Feb 12 2025 Karel Zak <kzak@redhat.com> - 2.40.4-6
- remove useradd (replaced by sysusers config)

* Tue Feb 04 2025 Karel Zak <kzak@fedoraproject.org> - 2.40.4-5
- Merge #20 `Conditionalize pam dependency`

* Tue Feb 04 2025 Karel Zak <kzak@redhat.com> - 2.40.4-4
- add sysusers config for uuidd

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 2.40.4-3
- Add explicit BR: libxcrypt-devel

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Karel Zak <kzak@redhat.com> - 2.40.4-1
- upgrade to v2.40.4

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.40.2-9
- Rebuilt for the bin-sbin merge (2nd attempt)

* Tue Sep 03 2024 Karel Zak <kzak@redhat.com> - 2.40.2-8
- improve util-linux-script subpackage

* Fri Aug 23 2024 Daan De Meyer <daan.j.demeyer@gmail.com> - 2.40.2-7
- Move script utilities to util-linux-script subpackage

* Wed Aug 14 2024 Daan De Meyer <daan.j.demeyer@gmail.com> - 2.40.2-6
- Remove setgid and tty group from /usr/bin/write

* Wed Aug 14 2024 Daan De Meyer <daan.j.demeyer@gmail.com> - 2.40.2-5
- Fix whitespace issues

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.40.2-3
- Add compat Providess for binaries under /usr/sbin

* Thu Jul 04 2024 Karel Zak <kzak@redhat.com> - 2.40.2-1
- upgrade from v2.40.1 to v2.40.2

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.40.1-2
- Rebuilt for Python 3.13

* Mon May 06 2024 Karel Zak <kzak@redhat.com> - 2.40.1-1
- upgrade to stable v2.40.1

* Mon Apr 08 2024 Karel Zak <kzak@redhat.com> - 2.40-13
- remove pre-release option

* Fri Mar 29 2024 Karel Zak <kzak@redhat.com> - 2.40-0.12
- upgrade to v2.40

* Wed Feb 28 2024 Karel Zak <kzak@redhat.com> - 2.40-0.11.rc1
- fix license related stuff

* Wed Feb 21 2024 Karel Zak <kzak@redhat.com> - 2.40-0.10.rc1
- use SPDX based identifiers for license field

* Thu Feb 15 2024 Colin Walters <walters@verbum.org> - 2.40-0.9.rc1
- Backport https://github.com/util-linux/util-
  linux/commit/211a9da0b4e9704eea210d7944b723fa78272c79

* Wed Feb  7 2024 Karel Zak <kzak@redhat.com> - 2.40-0.8
- add autorelease and autochangelog

* Fri Feb  2 2024 Karel Zak <kzak@redhat.com> - 2.40-0.1
- upgrade to v2.40-rc1
- add setpgid, enosys, exch and lsclocks commands

* Thu Jan 25 2024 Karel Zak <kzak@redhat.com> - 2.39.3-4
- improve fix for #2256391 (util-linux-i18n conflicts)

* Thu Jan 25 2024 Karel Zak <kzak@redhat.com> - 2.39.3-3
- fix #2258501 - dnf5 unusable with libsmartcols

* Thu Jan 11 2024 Karel Zak <kzak@redhat.com> - 2.39.3-2
- fix #2256391 util-linux-i18n conflicts with file from package shadow-utils

* Sun Dec 31 2023 Karel Zak <kzak@redhat.com> - 2.39.3-1
- upgrade to v2.39.3
  https://kernel.org/pub/linux/utils/util-linux/v2.39/v2.39.3-ReleaseNotes

* Sat Dec  2 2023 Daan De Meyer <daandemeyer@gmail.com> - 2.39.2-2
- Move sulogin to util-linux-core

* Thu Aug 17 2023 Karel Zak <kzak@redhat.com> - 2.39.2-1
- fix libmount atime regression
- upgrade to v2.39.2
  https://kernel.org/pub/linux/utils/util-linux/v2.39/v2.39.2-ReleaseNotes

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.39.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 2.39.1-2
- Rebuilt for Python 3.12

* Wed Jun 28 2023 Karel Zak <kzak@redhat.com> - 2.39.1-1
- upgrade to v2.39.1
  https://kernel.org/pub/linux/utils/util-linux/v2.39/v2.39.1-ReleaseNotes

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.39-5
- Rebuilt for Python 3.12

* Thu May 25 2023 Karel Zak <kzak@redhat.com> - 2.39-4
- fix mount when /sbin/mount.<type> executed

* Mon May 22 2023 Karel Zak <kzak@redhat.com> - 2.39-3
- fix mount options prepend/insert and merging (upstream)

* Thu May 18 2023 Adam Williamson <awilliam@redhat.com> - 2.39-2
- Have util-linux obsolete and provide util-linux-user

* Thu May 18 2023 Karel Zak <kzak@redhat.com> - 2.39-1
- upgrade to v2.39
- remove dependence on libuser
- remove util-linux-user subpackage
- enable translated man pages
- add util-linux-i18n subpackage

* Wed Apr 19 2023 Karel Zak <kzak@redhat.com> - 2.39-0.5
- upgrade to v2.39-rc3 (fixes XFS and rw/ro issues)

* Wed Apr  5 2023 Karel Zak <kzak@redhat.com> - 2.39-0.4
- fix #2180593 (superblock reconfiguration libmount issue)

* Tue Apr  4 2023 Karel Zak <kzak@redhat.com> - 2.39-0.3
- fix spec file

* Tue Apr  4 2023 Karel Zak <kzak@redhat.com> - 2.39-0.2
- upgrade to v2.39-rc2

* Mon Mar 20 2023 Karel Zak <kzak@redhat.com> - 2.39-0.1
- upgrade to v2.39-rc1
  https://kernel.org/pub/linux/utils/util-linux/v2.39/v2.39-ReleaseNotes

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 17 2022 Florian Weimer <fweimer@redhat.com> - 2.38.1-3
- Backport upstream patch to fix C99 issue in kill

* Mon Aug 22 2022 Karel Zak <kzak@redhat.com> - 2.38.1-2
- improve tmpfiles.d use in spec file

* Thu Aug 4 2022 Karel Zak <kzak@redhat.com> - 2.38.1-1
- upgrade to v2.38.1
  https://kernel.org/pub/linux/utils/util-linux/v2.38/v2.38.1-ReleaseNotes

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.38-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.38-4
- Rebuilt for Python 3.11

* Wed Apr 13 2022 Karel Zak <kzak@redhat.com> - 2.38-3
- fix spec file changelog order

* Wed Mar 30 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.38-2
- simplify creation of /etc/mtab symlink

* Wed Mar 30 2022 Karel Zak <kzak@redhat.com> - 2.38-1
- upgrade to v2.38
- don't (re)generate build-system
- modernize spec file style (thanks to Zbigniew)

* Thu Mar 17 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.38-0.5
- Drop very old upgrade scriptlet for libblkid

* Wed Mar 16 2022 Karel Zak <kzak@redhat.com> - 2.38-0.4
- upgrade to v2.38-rc3
  https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/v2.38/v2.38-ReleaseNotes

* Wed Feb  2 2022 Karel Zak <kzak@redhat.com> - 2.38-0.3
- add /usr/lib/tmpfiles.d/uuidd.conf (based on #2047952)

* Wed Feb  2 2022 Karel Zak <kzak@redhat.com> - 2.38-0.2
- release ownership of /var/log/lastlog

* Mon Jan 31 2022 Karel Zak <kzak@redhat.com> - 2.38-0.1
- upgrade to v2.38-rc1

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.37.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 17 2021 Karel Zak <kzak@redhat.com> - 2.37.2-1
* upgrade to v2.37.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Karel Zak <kzak@redhat.com> - 2.37-5
- remove unused util-linux-60-raw.rules

* Wed Jul 14 2021 Karel Zak <kzak@redhat.com> - 2.37-4
- disable raw(8) - no more supported since Linux v5.14 (commit 03e4922f1c81fc2ed3a87b4f91a8d3aafc7e093)
- remove dependence on deprecated pcre2posix.h
- fix #1981729 - close_range() 3rd argument

* Wed Jun 16 2021 Richard W.M. Jones <rjones@redhat.com> - 2.37-3
- Rebuild for updated pcre2

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.37-2
- Rebuilt for Python 3.10

* Tue Jun  1 2021 Karel Zak <kzak@redhat.com> - 2.37-1
- upgrade to v2.37
- introduce util-linux-core subpackage

* Fri May 14 2021 Karel Zak <kzak@redhat.com> - 2.37-0.1
- upgrade to v2.37-rc2
  https://kernel.org/pub/linux/utils/util-linux/v2.37/v2.37-ReleaseNotes

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.36.2-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Mar  2 2021 Karel Zak <kzak@redhat.com> - 2.36.2-2
- spec file cleanup https://src.fedoraproject.org/rpms/util-linux/pull-request/9

* Fri Feb 12 2021 Karel Zak <kzak@redhat.com> - 2.36.2-1
- upgrade to stable upstream 2.36.2
  https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/v2.36/v2.36.2-ReleaseNotes

* Wed Jan 27 2021 Kelvin Fan <kfan@redhat.com> - 2.36.1-4
- Add patch to add /run/motd.d to default MOTD_FILE in login(1)

* Thu Jan 14 2021 Karel Zak <kzak@redhat.com> - 2.36.1-3
- improve uuidd scriptlets (fix #1767553)

* Thu Nov 19 2020 Karel Zak <kzak@redhat.com> - 2.36.1-2
- remove unused patches
- remove versions and seq.numbers from patch names
- fix mount "symfollow" issue (upstream patch)

* Mon Nov 16 2020 Karel Zak <kzak@redhat.com> - 2.36.1-1
- upgrade to stable upstream 2.36.1

* Thu Nov 12 2020 Tom Stellard <tstellar@redhat.com> - 2.36-4
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Sep 01 2020 Karel Zak <kzak@redhat.com> - 2.36-3
- remove mountinfo workaround (unnecessary for kernel 5.8)
- fix #1860461 - sfdisk regression creating simple 3 partition MBR disk

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Karel Zak <kzak@redhat.com> - 2.36-1
- upgrade to upstream release v2.36
  https://www.kernel.org/pub/linux/utils/util-linux/v2.36/v2.36-ReleaseNotes
- add irqtop and lsirq commands

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.35.2-2
- Rebuilt for Python 3.9

* Wed May 20 2020 Karel Zak <kzak@redhat.com> - 2.35.2-1
- upgrade to upstream bug fix release 2.35.2
  https://www.kernel.org/pub/linux/utils/util-linux/v2.35/v2.35.2-ReleaseNotes

* Wed Apr 15 2020 Karel Zak <kzak@redhat.com> - 2.35.1-9
- fix copy & past bug in specfile changelog

* Wed Apr 15 2020 Karel Zak <kzak@redhat.com> - 2.35.1-8
- fix #1822226 - remove pam_console dependency
- fix #1823463 - hwclock unable to set system time

* Tue Mar 24 2020 Kalev Lember <klember@redhat.com> - 2.35.1-7
- Another attempt at enabling fstrim.timer on F32 upgrades (#1811506)

* Thu Mar 19 2020 Karel Zak <kzak@redhat.com> - 2.35.1-6
- fix #1811506 (triggerpostun)

* Tue Feb 25 2020 Karel Zak <kzak@redhat.com> - 2.35.1-5
- fix lsblk -P output for RAIDs, etc.

* Thu Feb 06 2020 Karel Zak <kzak@redhat.com> - 2.35.1-4
- add triggerpostun for fstrim.timer (#1785041, FESCo #2309)

* Tue Feb 04 2020 Karel Zak <kzak@redhat.com> - 2.35.1-3
- fix fstrim.service (util-linux github #948)

* Tue Feb 04 2020 Karel Zak <kzak@redhat.com> - 2.35.1-2
- fix sfdisk dump issue (util-linux github #949)

* Mon Feb 03 2020 Karel Zak <kzak@redhat.com> - 2.35.1-1
- upgrade to upstream bug fix release 2.35.1

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Karel Zak <kzak@redhat.com> - 2.35-1
- upgrade to v2.35

* Thu Jan 9 2020 Karel Zak <kzak@redhat.com> - 2.35-0.5
- upgrade to v2.35-rc2

* Fri Dec 20 2019 Karel Zak <kzak@redhat.com> - 2.35-0.4
- fix #1784536 - Segfaults in agetty during Cloud image testing

* Fri Dec 20 2019 Karel Zak <kzak@redhat.com> - 2.35-0.3
- upgrade to the upstream git snapshot (v2.35-rc1-20-g63f8c66af)
- fix #1783066 - Fedora-Rawhide images do not boot

* Thu Dec 12 2019 Adam Williamson <awilliam@redhat.com> - 2.35-0.2
- Revert upstream commit 7ef86a0 to fix RHBZ #1783066

* Wed Dec 11 2019 Karel Zak <kzak@redhat.com> - 2.35-0.1
- upgrade to v2.35-rc1
  https://www.kernel.org/pub/linux/utils/util-linux/v2.35/v2.35-ReleaseNotes

* Fri Sep 13 2019 Karel Zak <kzak@redhat.com> - 2.34-6
- fix https://github.com/systemd/systemd/issues/10872

* Thu Sep 12 2019 Karel Zak <kzak@redhat.com> - 2.34-5
- fix #1751290 - regression: lsblk not showing PKNAME in f31+

* Thu Sep 05 2019 Karel Zak <kzak@redhat.com> - 2.34-4
- add BuildRequires: readline for fdisks

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.34-3
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Karel Zak <kzak@redhat.com> - 2.34-2
- fix lscpu compilation on ppc

* Fri Jun 14 2019 Karel Zak <kzak@redhat.com> - 2.34-1
- upgrade to v2.34

* Thu May 30 2019 Karel Zak <kzak@redhat.com> - 2.34-0.2
- upgrade to v2.34-rc2

* Tue Apr 30 2019 Karel Zak <kzak@redhat.com> - 2.34-0.1
- add command hardlink(1) (merged into util-linux upstream)
- upgrade to v2.34-rc1
  http://www.kernel.org/pub/linux/utils/util-linux/v2.34/v2.34-ReleaseNotes

* Tue Apr  9 2019 Karel Zak <kzak@redhat.com> - 2.33.2-1
- upgrade to v2.33.2
  https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/v2.33/v2.33.2-ReleaseNotes

* Thu Mar 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.33.1-4
- Remove obsolete scriptlets

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.33.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 2.33.1-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Wed Jan  9 2019 Karel Zak <kzak@redhat.com> - 2.33.1-1
- upgrade to v2.33.1
  https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/v2.33/v2.33.1-ReleaseNotes

* Thu Nov  1 2018 Karel Zak <kzak@redhat.com> - 2.33-0.1
- Remove ldconfig scriptlet, now done via. transfiletrigger in glibc [James Antill]
- upgrade to v2.33-rc2
  http://www.kernel.org/pub/linux/utils/util-linux/v2.33/v2.33-ReleaseNotes

* Mon Jul 16 2018 Karel Zak <kzak@redhat.com> - 2.32.1-1
- upgrade to v2.32.1
  http://www.kernel.org/pub/linux/utils/util-linux/v2.32/v2.32.1-ReleaseNotes

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.32-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.32-6
- Rebuilt for Python 3.7

* Fri May 18 2018 Karel Zak <kzak@redhat.com> - 2.32-5
- move /etc/adjtime config from initscripts to util-linux

* Wed Apr 11 2018 Karel Zak <kzak@redhat.com> - 2.32-4
- fix #1560642 - uuidd.service does not start

* Tue Apr 10 2018 Karel Zak <kzak@redhat.com> - 2.32-3
- remove unused build option --enable-libmount-force-mountinfo (it's default now)

* Tue Mar 27 2018 Karel Zak <kzak@redhat.com> - 2.32-2
- fix #1560283 - column does not properly handle spaces at beginning of tab-separated table columns

* Wed Mar 21 2018 Karel Zak <kzak@redhat.com> - 2.32-1
- upgrade to v2.32

* Tue Feb 20 2018 Karel Zak <kzak@redhat.com> - 2.32-0.2
- add BuildRequires gcc

* Tue Feb 13 2018 Karel Zak <kzak@redhat.com> - 2.32-0.1
- upgrade to v2.32-rc1
  http://www.kernel.org/pub/linux/utils/util-linux/v2.32/v2.32-ReleaseNotes

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.31-4
- Rebuilt for switch to libxcrypt

* Wed Jan 03 2018 Lumír Balhar <lbalhar@redhat.com> - 2.31-3
- Fix directory ownership in python subpackage

* Mon Oct 30 2017 Karel Zak <kzak@redhat.com> - 2.31-2
- fix dmesg for multi-line records

* Mon Oct 23 2017 Karel Zak <kzak@redhat.com> - 2.31-1
- upgrade to final v2.31
- move rfkill to sbin (for backward compatibility)

* Mon Oct  9 2017 Karel Zak <kzak@redhat.com> - 2.31-0.4
- fix build error

* Mon Oct  9 2017 Karel Zak <kzak@redhat.com> - 2.31-0.3
- upgrade to v2.31-rc2
- enable rfkill

* Mon Sep 25 2017 Karel Zak <kzak@redhat.com> - 2.31-0.2
- temporary disable rfkill (fix #1494855)

* Fri Sep 22 2017 Karel Zak <kzak@redhat.com> - 2.31-0.1
- upgrade to v2.31-rc1
  http://ftp.kernel.org/pub/linux/utils/util-linux/v2.31/v2.31-ReleaseNotes

* Fri Sep 22 2017 Karel Zak <kzak@redhat.com> - 2.30.2-1
- upgrade to v2.30.2
  http://ftp.kernel.org/pub/linux/utils/util-linux/v2.30/v2.30.2-ReleaseNotes

* Mon Aug 14 2017 Karel Zak <kzak@redhat.com> - 2.30.1-5
- make ln-s usage more robust

* Fri Aug  4 2017 Karel Zak <kzak@redhat.com> - 2.30.1-4
- fix post install script

* Wed Aug  2 2017 Karel Zak <kzak@redhat.com> - 2.30.1-3
- fix #1390191 - systemd read-only container produces errors

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Karel Zak <kzak@redhat.com> - 2.30.1-1
- upgrade to v2.30.1
  http://ftp.kernel.org/pub/linux/utils/util-linux/v2.30/v2.30.1-ReleaseNotes

* Fri Jun  2 2017 Karel Zak <kzak@redhat.com> - 2.30-1
- upgrade to v2.30

* Wed May 17 2017 Karel Zak <kzak@redhat.com> - 2.30-0.1
- upgrade to v2.30-rc1
  http://ftp.kernel.org/pub/linux/utils/util-linux/v2.30/v2.30-ReleaseNotes

* Fri Feb 24 2017 Karel Zak <kzak@redhat.com> - 2.29.2-1
- upgrade to v2.29.2
  http://ftp.kernel.org/pub/linux/utils/util-linux/v2.29/v2.29.2-ReleaseNotes

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.29.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 20 2017 Karel Zak <kzak@redhat.com> - 2.29.1-1
- upgrade to v2.29.1
  http://ftp.kernel.org/pub/linux/utils/util-linux/v2.29/v2.29.1-ReleaseNotes

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.29-2
- Rebuild for Python 3.6

* Tue Nov  8 2016 Karel Zak <kzak@redhat.com> - 2.29-1
- upgrade to v2.29

* Wed Oct 19 2016 Karel Zak <kzak@redhat.com> - 2.29-0.2
- upgrade to v2.29-rc2

* Fri Sep 30 2016 Karel Zak <kzak@redhat.com> - 2.29-0.1
- upgrade to v2.29-rc1
  http://ftp.kernel.org/pub/linux/utils/util-linux/v2.29/v2.29-ReleaseNotes

* Wed Sep  7 2016 Karel Zak <kzak@redhat.com> - 2.28.2-1
- upgrade to stable 2.28.2
  http://ftp.kernel.org/pub/linux/utils/util-linux/v2.28/v2.28.2-ReleaseNotes

* Thu Aug 18 2016 Karel Zak <kzak@redhat.com> - 2.28.1-1
- upgrade to stable 2.28.1
  http://ftp.kernel.org/pub/linux/utils/util-linux/v2.28/v2.28.1-ReleaseNotes

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jun 13 2016 Karel Zak <kzak@redhat.com> - 2.28-3
- fix #1234317 - CD / DVD are rarely automounted

* Tue Apr 26 2016 Karel Zak <kzak@redhat.com> - 2.28-2
- refresh login-lastlog-create.patch

* Tue Apr 12 2016 Karel Zak <kzak@redhat.com> - 2.28-1
- upgrade to stable v2.28

* Wed Mar 30 2016 Karel Zak <kzak@redhat.com> - 2.28-0.3
- fix libblkid

* Tue Mar 29 2016 Karel Zak <kzak@redhat.com> - 2.28-0.2
- upgrade to v2.28-rc2

* Tue Mar 22 2016 Karel Zak <kzak@redhat.com> - 2.28-0.1
- upgrade to v2.28-rc1
  http://ftp.kernel.org/pub/linux/utils/util-linux/v2.28/v2.28-ReleaseNotes
- add patch to fix broken swapon
- add subpackage util-linux-user (utils with dependence on libuser)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.27.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Karel Zak <kzak@redhat.com> - 2.27.1-4
- fix #1299255 - boot.iso (from 20160117 Rawhide compose) incorrectly detected as minix FS

* Wed Nov 18 2015 Karel Zak <kzak@redhat.com> - 2.27.1-3
- fix #1259745 - Can't start installation in Rawhide or F23 recent development images

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov  2 2015 Karel Zak <kzak@redhat.com> - 2.27.1
- upgrade to v2.27.1
  http://ftp.kernel.org/pub/linux/utils/util-linux/v2.27/v2.27.1-ReleaseNotes

* Mon Sep  7 2015 Karel Zak <kzak@redhat.com> - 2.27
- upgrade to v2.27

* Mon Aug 24 2015 Karel Zak <kzak@redhat.com> - 2.27-0.4
- upgrade to v2.27-rc2

* Thu Aug 13 2015 Karel Zak <kzak@redhat.com> - 2.27-0.3
- improve version usage in source url

* Wed Aug 12 2015 Karel Zak <kzak@redhat.com> - 2.27-0.2
- fix #1251320 - rfe: please change login to not add /bin:/sbin to $PATH
- apply patches from Lokesh Mandvekar to make spec file more portable

* Fri Jul 31 2015 Karel Zak <kzak@redhat.com> - 2.27-0.1
- upgrade to v2.27-rc1
  http://ftp.kernel.org/pub/linux/utils/util-linux/v2.27/v2.27-ReleaseNotes
- add lsipc

* Thu Jul 16 2015 Karel Zak <kzak@redhat.com> - 2.26.2-3
- fix dates in the spec file

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 30 2015 Karel Zak <kzak@redhat.com> - 2.26.2-1
- upgrade to stable release 2.26.2
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.26/v2.26.2-ReleaseNotes

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.26-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Feb 19 2015 Karel Zak <kzak@redhat.com> 2.26-1
- upgrade to stable release 2.26

* Tue Feb 10 2015 Karel Zak <kzak@redhat.com> 2.26-0.4
- fix setarch build on PPC

* Thu Feb 5 2015 Karel Zak <kzak@redhat.com> 2.26-0.3
- upgrade to 2.26-rc2

* Fri Jan 16 2015 Karel Zak <kzak@redhat.com> 2.26-0.2
- fix 1182778 - remount causes ro / and /home on boot

* Thu Jan 15 2015 Karel Zak <kzak@redhat.com> 2.26-0.1
- upgrade to 2.26-rc1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.26/v2.26-ReleaseNotes
- build with -pie for uuidd
- new command zramctl

* Thu Nov 27 2014 Karel Zak <kzak@redhat.com> 2.25.2-2
- fix #1168490 - CVE-2014-9114 util-linux: command injection flaw in blkid

* Fri Oct 24 2014 Karel Zak <kzak@redhat.com> 2.25.2-1
- upgrade to stable 2.25.2
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.25/v2.25.2-ReleaseNotes

* Wed Sep  3 2014 Karel Zak <kzak@redhat.com> 2.25.1-1
- upgrade to stable 2.25.1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.25/v2.25.1-ReleaseNotes

* Wed Aug 27 2014 Karel Zak <kzak@redhat.com> 2.25.1-0.1
- upgrade to release 2.25.1-rc1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.25/v2.25.1-ReleaseNotes

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug  6 2014 Tom Callaway <spot@fedoraproject.org> 2.25-3
- fix license handling

* Thu Jul 24 2014 Karel Zak <kzak@redhat.com> 2.25-2
- remove fstrim unit files from uuidd subpackage

* Tue Jul 22 2014 Karel Zak <kzak@redhat.com> 2.25-1
- upgrade to stable release 2.25

* Wed Jul 02 2014 Karel Zak <kzak@redhat.com> 2.25-0.3
- upgrade to release 2.25-rc2

* Wed Jun 25 2014 Peter Jones <pjones@redhat.com> - 2.25-0.2
- Fix libblkid's squashfs probe return checking.
  Related: rhbz#1112315

* Thu Jun 19 2014 Karel Zak <kzak@redhat.com> 2.25-0.1
- upgrade to release 2.25-rc1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.25/v2.25-ReleaseNotes

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.24.2-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon May 12 2014 Karel Zak <kzak@redhat.com> 2.24.2-4
- fix #1094935 - script and/or trigger should not directly enable systemd units

* Mon May 12 2014 Karel Zak <kzak@redhat.com> 2.24.2-3
- fix #1090638 - remove pam_securetty.so from .pamd files

* Wed May  7 2014 Karel Zak <kzak@redhat.com> 2.24.2-2
- use systemd macroized scriptlets (#850355)

* Thu Apr 24 2014 Karel Zak <kzak@redhat.com> 2.24.2-1
- upgrade to stable release 2.24.2
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.24/v2.24.2-ReleaseNotes

* Thu Jan 30 2014 Karel Zak <kzak@redhat.com> 2.24.1-2
- use rpm autosetup

* Mon Jan 20 2014 Karel Zak <kzak@redhat.com> 2.24.1-1
- upgrade to stable release 2.24.1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.24/v2.24.1-ReleaseNotes

* Mon Nov 18 2013 Karel Zak <kzak@redhat.com> 2.24-2
- fix #1031262 - lsblk -D segfault

* Wed Oct 23 2013 Karel Zak <kzak@redhat.com> 2.24-1
- upgrade to upstream release v2.24
- remove nologin (merged upstream)
- fix #1022217 - fdisk mishandles GPT corruption

* Fri Sep 27 2013 Karel Zak <kzak@redhat.com> 2.24-0.1
- upgrade to upstream release v2.24-rc1
- add python3 libmount binding

* Mon Sep  9 2013 Karel Zak <kzak@redhat.com> 2.23.2-4
- fix #1005566 - recount_geometry: Process /usr/sbin/fdisk was killed by signal 8 (SIGFPE)
- fix #1005194 - su generates incorrect log entries

* Mon Sep  9 2013 Karel Zak <kzak@redhat.com> 2.23.2-3
- refresh and rename patches
- fix #987787 - Remove lastlogin from su
- fix #950497 - problem umounting loop device
- fix #921498 - multiple internal testsuite failures

* Thu Aug  1 2013 Karel Zak <kzak@redhat.com> 2.23.2-2
- fix 990083 - su doesn't work with pam_ecryptfs

* Wed Jul 31 2013 Karel Zak <kzak@redhat.com> 2.23.2-1
- upgrade to stable release 2.23.2
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.23/v2.23.2-ReleaseNotes

* Thu Jun 13 2013 Karel Zak <kzak@redhat.com> 2.23.1-3
- fix #972457 - agetty idle I/O polling causes elevated CPU usage

* Wed Jun  5 2013 Karel Zak <kzak@redhat.com> 2.23.1-2
- fix #962145 - in.telnetd immediately closes connection

* Tue May 28 2013 Karel Zak <kzak@redhat.com> 2.23.1-1
- upgrade to 2.23.1
- backport agetty --local-line path

* Thu Apr 25 2013 Karel Zak <kzak@redhat.com> 2.23-1
- upgrade to 2.23
- add --with check to call make check

* Mon Apr 15 2013 Karel Zak <kzak@redhat.com> 2.23-0.7
- remove unused patches

* Mon Apr 15 2013 Karel Zak <kzak@redhat.com> 2.23-0.6
- remove floppy from util-linux

* Fri Apr 12 2013 Karel Zak <kzak@redhat.com> 2.23-0.5
- fix #948274 - interruption code 0x4003B in libmount.so.1.1.0

* Wed Apr 10 2013 Karel Zak <kzak@redhat.com> 2.23-0.4
- upgrade to the release 2.23-rc2

* Wed Mar 27 2013 Karel Zak <kzak@redhat.com> 2.23-0.3
- libblkid ntfs bugfix for build on s390

* Wed Mar 27 2013 Karel Zak <kzak@redhat.com> 2.23-0.2
- add upstream patches for to fix umount and mount.<type>

* Fri Mar 22 2013 Karel Zak <kzak@redhat.com> 2.23-0.1
- upgrade to the release 2.23-rc1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.23/v2.23-ReleaseNotes
- add nsenter and blkdiscard
- remove tunelp

* Wed Feb 20 2013 Karel Zak <kzak@redhat.com> 2.22.2-6
- fix  #912778 - "runuser -l" doesn't register session to systemd

* Tue Feb 19 2013 Karel Zak <kzak@redhat.com> 2.22.2-5
- fix #902512 - Dependency failed for /home (and blkid fails to tell UUID)
- refresh old patches

* Wed Feb  6 2013 Karel Zak <kzak@redhat.com> 2.22.2-4
- improve convertion to mtab symlink in post script
- spec file cleanup (based on #894199)

* Sun Feb  3 2013 Karel Zak <kzak@redhat.com> 2.22.2-3
- fix #882305 - agetty: unstable /dev/tty* permissions
- fix #885314 - hexdump segfault
- fix #896447 - No newlines in piped "cal" command
- fix libblkid cache usage (upstream patch)
- fix #905008 - uuidd: /usr/sbin/uuidd has incorrect file permissions

* Tue Jan 15 2013 Karel Zak <kzak@redhat.com> 2.22.2-2
- fix #889888 - wipefs does not completely wipe btrfs volume

* Thu Dec 13 2012 Karel Zak <kzak@redhat.com> 2.22.2-1
- upgrade to upstream maintenance release 2.22.2

* Mon Nov 19 2012 Karel Zak <kzak@redhat.com> 2.22.1-5
- sources cleanup

* Fri Nov 16 2012 Karel Zak <kzak@redhat.com> 2.22.1-4
- fix #872787 - su: COMMAND not specified

* Thu Nov  1 2012 Karel Zak <kzak@redhat.com> 2.22.1-3
- backport upstream runuser(1)
- enable su(1)

* Thu Nov  1 2012 Karel Zak <kzak@redhat.com> 2.22.1-2
- apply pathes from upstream stable/v2.22 branch
- fix #865961 - wipefs -a should use O_EXCL

* Wed Oct 10 2012 Karel Zak <kzak@redhat.com> 2.22.1-1
- upgrade to the release 2.22.1

* Wed Oct  3 2012 Karel Zak <kzak@redhat.com> 2.22-2
- remove obsolete references to e2fsprogs

* Thu Sep  6 2012 Karel Zak <kzak@redhat.com> 2.22-1
- upgrade to the release 2.22
- enable eject(1) from util-linux, obsolete original eject package
- fix #853164 - setuid program should have full RELRO
- fix #851230 - probe_ntfs: /usr/sbin/blkid was killed by SIGSEGV

* Thu Aug 16 2012 Karel Zak <kzak@redhat.com> 2.22-0.1
- upgrade to the release 2.22-rc2
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.22/v2.22-ReleaseNotes
- add sulogin, utmpdump, lslocks, wdctl

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Karel Zak <kzak@redhat.com> 2.21.2-2
- replace udev dependenceis with systemd

* Fri May 25 2012 Karel Zak <kzak@redhat.com> 2.21.2-1
- upgrade to bugfix release 2.21.2
- fix #814699 - namei(1) incorrectly resolves relative symlinks
- fix #820707 - Impossible to unmount nfsv4/krb5 mounts after network disconnect
- fix #816877 - libmount does not close device fd before mount(2)
- fix #822705 - unable to login after installing

* Fri Mar 30 2012 Karel Zak <kzak@redhat.com> 2.21.1-1
- upgrade to bugfix release 2.21.1

* Fri Feb 24 2012 Karel Zak <kzak@redhat.com> 2.21-1
- upgrade to release 2.21

* Thu Feb 09 2012 Karel Zak <kzak@redhat.com> 2.21-0.2
- fix #788703 - /run/blkid does not exist

* Tue Feb 07 2012 Karel Zak <kzak@redhat.com> 2.21-0.1
- upgrade to the release 2.21-rc2
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.21/v2.21-ReleaseNotes
- add {fsck,mkfs}.minix
- add new command chcpu(8)
- add new command prlimit(1)
- enable raw(8) command
- move 60-raw.rules from /etc from /usr/lib/udev/rules.d
- move blkid cache from etc to /run/blkid

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 2.20.1-5
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Karel Zak <kzak@redhat.com> 2.20.1-3
- fix #748216 - util-linux requires pam >= 1.1.3-7
- remove ddate(1)

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20.1-2
- Rebuilt for glibc bug#747377

* Thu Oct 20 2011 Karel Zak <kzak@redhat.com> 2.20.1-1
- upgrade to the release 2.20.1
  ftp://ftp.infradead.org/pub/util-linux/v2.20/v2.20.1-ReleaseNotes

* Mon Aug 29 2011 Karel Zak <kzak@redhat.com> 2.20-1
- upgrade to the release 2.20

* Wed Aug 17 2011 Karel Zak <kzak@redhat.com> 2.20-0.2
- upgrade to the release 2.20-rc2
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.20/v2.20-rc2-ChangeLog

* Tue Aug  2 2011 Karel Zak <kzak@redhat.com> 2.20-0.1
- upgrade to the release 2.20-rc1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.20/v2.20-ReleaseNotes

* Mon Jul  4 2011 Karel Zak <kzak@redhat.com> 2.19.1-2
- fix #716483 - /var/tmp --(BIND-mounted)--> /tmp disrupts/hangs bootup
- fix #709681 - failure to mount if a mount point ends with a slash in /etc/fstab
- fix #709319 - 'mount -a' mounts already mounted directories
- fix kernel version parsing

* Fri May  6 2011 Karel Zak <kzak@redhat.com> 2.19.1-1
- upgrade to the release 2.19.1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.19/v2.19.1-ReleaseNotes

* Wed Apr 20 2011 Karel Zak <kzak@redhat.com> 2.19.1-0.1
- upgrade to the release 2.19.1-rc1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.19/v2.19.1-rc1-ChangeLog

* Mon Mar  7 2011 Karel Zak <kzak@redhat.com> 2.19-2
- fix #682502 - Broken source URL to floppy tarball, new version available
- upgrade to floppy-0.18

* Thu Feb 10 2011 Karel Zak <kzak@redhat.com> 2.19-1
- upgrade to the release 2.19
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.19/v2.19-ReleaseNotes
- remove /sbin/mount.tmpfs -- integrated to mount(8)

* Tue Feb  8 2011 Karel Zak <kzak@redhat.com> 2.19-0.6
- fix #665062 - add support for the postlogin PAM stack to util-linux-ng

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Karel Zak <kzak@redhat.com> 2.19-0.4
- upgrade to the release 2.19-rc3
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.19/v2.19-rc3-ChangeLog

* Tue Jan 25 2011 Karel Zak <kzak@redhat.com> 2.19-0.3
- upgrade to the release 2.19-rc2
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.19/v2.19-rc2-ChangeLog
- fix #671893 - SELinux is preventing /bin/chown from 'setattr' accesses
  on the file mounts.

* Wed Jan 19 2011 Karel Zak <kzak@redhat.com> 2.19-0.2
- clean up specfile (review #667416)

* Wed Jan  5 2011 Karel Zak <kzak@redhat.com> 2.19-0.1
- upgrade to the release 2.19-rc1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux/v2.19/v2.19-ReleaseNotes

* Tue Oct 26 2010 Karel Zak <kzak@redhat.com> 2.18-5
- fix #645640 - new "-s" parameter parsing in agetty does not work
- add -l (lock) support to fsck

* Wed Aug 18 2010 Karel Zak <kzak@redhat.com> 2.18-4
- fix #623685 - please extend agetty to not require a baud rate to be specified

* Thu Aug  5 2010 Karel Zak <kzak@redhat.com> 2.18-3
- fix #620924 - /sbin/mount.tmpfs uses not available /usr/bin/id

* Mon Aug  2 2010 Karel Zak <kzak@redhat.com> 2.18-2
- fix #615719 - tmpfs mount fails with 'user' option.
- fix #598631 - shutdown, reboot, halt and C-A-D don't work
- fix #618957 - ISO images listed in fstab are mounted twice at boot

* Wed Jun 30 2010 Karel Zak <kzak@redhat.com> 2.18-1
- upgrade to the final 2.18
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.18/v2.18-ReleaseNotes
 
* Fri Jun 18 2010 Karel Zak <kzak@redhat.com> 2.18-0.2
- upgrade to 2.18-rc2
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.18/v2.18-rc2-ChangeLog

* Tue Jun  8 2010 Karel Zak <kzak@redhat.com> 2.18-0.1
- upgrade to the release 2.18-rc1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.18/v2.18-ReleaseNotes
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.18/v2.18-rc1-ChangeLog

* Mon Apr 12 2010 Karel Zak <kzak@redhat.com> 2.17.2-1
- fix #581252 - remounting tmpfs fails because of hidden rootcontext=
- fix #580296 - "rtcwake" does miss the "off" option
- fix #575734 - use microsecond resolution for blkid cache entries
- upgrade to the bugfix release 2.17.2
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.17/v2.17.2-ReleaseNotes
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.17/v2.17.2-ChangeLog
- minor fixed in spec file

* Thu Mar 11 2010 Karel Zak <kzak@redhat.com> 2.17.1-2
- fix #533874 - libblkid should allow scanning of slow devices (eg. cdroms)

* Mon Feb 22 2010 Karel Zak <kzak@redhat.com> 2.17.1-1
- upgrade to the final 2.17.1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.17/v2.17.1-ReleaseNotes
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.17/v2.17.1-ChangeLog

* Tue Feb 16 2010 Karel Zak <kzak@redhat.com> 2.17.1-0.1
- upgrade to 2.17.1-rc1

* Tue Feb 16 2010 Karel Zak <kzak@redhat.com> 2.17-4
- fix uuidd init script

* Fri Feb 12 2010 Karel Zak <kzak@redhat.com> 2.17-3
- fix #541402 - uuidd initscript lsb compliance

* Fri Jan  8 2010 Karel Zak <kzak@redhat.com> 2.17-2
- remove Provides: lib{uuid,blkid}-static (thanks to Michael Schwendt)
- remove useless URL to sf.net

* Fri Jan  8 2010 Karel Zak <kzak@redhat.com> 2.17-1
- upgrade to the final 2.17
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.17/v2.17-ReleaseNotes
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.17/v2.17-ChangeLog
- fix #545147 - util-linux-ng : Violation of the Packaging Guidelines
  (remove uuid and blkid static libs)

* Mon Dec 14 2009 Karel Zak <kzak@redhat.com> 2.17-0.6
- minor fixes in spec file (fix URL, add Requires, add LGPLv2+)

* Wed Dec  9 2009 Karel Zak <kzak@redhat.com> 2.17-0.5
- upgrade to 2.17-rc2
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.17/v2.17-rc2-ChangeLog

* Mon Dec  7 2009 Karel Zak <kzak@redhat.com> 2.17-0.4
- add clock.8 man page (manlink to hwclock)
- add --help to mount.tmpfs

* Mon Nov 23 2009 Karel Zak <kzak@redhat.com> 2.17-0.3
- upgrade to 2.17-rc1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.17/v2.17-rc1-ChangeLog

* Tue Nov 10 2009 Karel Zak <kzak@redhat.com> 2.17-0.2.git10dfc39
- upgrade to pre-release snapshot (official changelog not available yet, see
  http://git.kernel.org/?p=utils/util-linux-ng/util-linux-ng.git for now)

* Mon Oct 19 2009 Karel Zak <kzak@redhat.com> 2.17-0.1.git5e51568
- upgrade to pre-release snapshot (official changelog not available yet, see
  http://git.kernel.org/?p=utils/util-linux-ng/util-linux-ng.git for now)  
- new commands: fallocate, unshare, wipefs
- libblkid supports topology and partitions probing
- remove support for --rmpart[s] from blockdev(8) (util-linux-ng-2.14-blockdev-rmpart.patch)
- merged upstream:
  util-linux-ng-2.14-sfdisk-dump.patch
  util-linux-ng-2.16-blkid-swsuspend.patch
  util-linux-ng-2.16-libblkid-compression.patch
  util-linux-ng-2.16-libblkid-ext2.patch
  util-linux-ng-2.16-switchroot-tty.patch

* Mon Oct  5 2009 Karel Zak <kzak@redhat.com> 2.16-13
- fix spec file

* Fri Oct  2 2009 Karel Zak <kzak@redhat.com> 2.16-12
- release++

* Thu Oct  1 2009 Karel Zak <kzak@redhat.com> 2.16-11
- fix #519237 - bash: cannot set terminal process group (-1): Inappropriate ioctl for device

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 2.16-10
- use password-auth common PAM configuration instead of system-auth and
  drop pam_console.so call from the remote PAM config file

* Mon Sep 14 2009 Karel Zak <kzak@redhat.com> 2.16-9
- fix #522718 - sfdisk -d /dev/xxx | sfdisk --force /dev/yyy fails when LANG is set
- fix typo in swsuspend detection

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> - 2.16-8
- rebuilt with new audit

* Sun Aug 23 2009 Karel Zak <kzak@redhat.com> 2.16-7
- fix #518572 - blkid requires ext2.ko to be decompressed on installation media

* Thu Aug 13 2009 Karel Zak <kzak@redhat.com> 2.16-5
- fix #513104 - blkid returns no fstype for ext2 device when ext2 module not loaded

* Wed Aug  5 2009 Stepan Kasal <skasal@redhat.com> 2.16-4
- set conflict with versions of e2fsprogs containing fsck

* Thu Jul 30 2009 Karel Zak <kzak@redhat.com> 2.16-3
- remove the mount.conf support (see #214891)

* Mon Jul 27 2009 Karel Zak <kzak@redhat.com> 2.16-2
- fix #214891 - add mount.conf and MTAB_LOCK_DIR= option

* Sat Jul 25 2009 Karel Zak <kzak@redhat.com> 2.16-1
- upgrade to 2.16
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.16/v2.16-ReleaseNotes
- enable built-in libuuid (replacement for the old uuid stuff from e2fsprogs)
- new commands switch_root, uuidgen and uuidd (subpackage)

* Wed Jun 10 2009 Karel Zak <kzak@redhat.com> 2.15.1-1
- upgrade to 2.15.1

* Mon Jun  8 2009 Karel Zak <kzak@redhat.com> 2.15.1-0.2
- set BuildRequires: e2fsprogs-devel
- add Requires: e2fsprogs-devel to libblkid-devel

* Thu Jun  4 2009 Karel Zak <kzak@redhat.com> 2.15.1-0.1
- upgrade to 2.15.1-rc1
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.15/v2.15-ReleaseNotes
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.15/v2.15.1-rc1-ChangeLog 
- merged patches:
  util-linux-ng-2.14-login-remote.patch
  util-linux-ng-2.14-fdisk-4k-I.patch
  util-linux-ng-2.14-fdisk-4k-II.patch
  util-linux-ng-2.14-fdisk-4k-III.patch
  util-linux-ng-2.14-dmesg-r.patch
  util-linux-ng-2.14-flock-segfaults.patch
  util-linux-ng-2.14-renice-n.patch
- new commands: lscpu, ipcmk
- remove support for "managed" and "kudzu" mount options
- cleanup spec file
- enable built-in libblkid (replacement for the old blkid from e2fsprogs)

* Thu Apr  2 2009 Karel Zak <kzak@redhat.com> 2.14.2-8
- fix #490769 - post scriptlet failed (thanks to Dan Horak)
 
* Fri Mar 20 2009 Karel Zak <kzak@redhat.com> 2.14.2-7
- fix some nits in mount.tmpfs

* Fri Mar 20 2009 Karel Zak <kzak@redhat.com> 2.14.2-6
- fix #491175 - mount of tmpfs FSs fail at boot

* Thu Mar 19 2009 Karel Zak <kzak@redhat.com> 2.14.2-5
- fix #489672 - flock segfaults when file name is not given (upstream)
- fix #476964 - Mount /var/tmp with tmpfs creates denials
- fix #487227 - fdisk 4KiB hw sectors support (upstream)
- fix #477303 - renice doesn't support -n option (upstream)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Karel Zak <kzak@redhat.com> 2.14.2-3
- add -r option to dmesg(1)

* Mon Feb  9 2009 Karel Zak <kzak@redhat.com> 2.14.2-2
- fix typo in spec file

* Mon Feb  9 2009 Karel Zak <kzak@redhat.com> 2.14.2-1
- upgrade to stable 2.14.2
  ftp://ftp.kernel.org/pub/linux/utils/util-linux-ng/v2.14/v2.14.2-ReleaseNotes

* Thu Jan 22 2009 Karel Zak <kzak@redhat.com> 2.14.2-0.2
- fix #480413 - util-linux-ng doesn't include scriptreplay
- fix #479002 - remove dependency on ConsoleKit-libs
- upgrade to 2.14.2-rc2

* Mon Dec 22 2008 Karel Zak <kzak@redhat.com> 2.14.2-0.1
- upgrade to 2.14.2-rc1
- refresh old patches

* Fri Nov 21 2008 Karel Zak <kzak@redhat.com> 2.14.1-5
- fix #472502 - problem with fdisk and use +sectors for the end of partition

* Mon Oct  6 2008 Karel Zak <kzak@redhat.com> 2.14.1-3
- fix #465761 -  mount manpage is missing uid/gid mount options for tmpfs
- refresh util-linux-ng-2.14-mount-file_t.patch (fuzz=0)

* Wed Sep 10 2008 Karel Zak <kzak@redhat.com> 2.14.1-2
- remove obsolete pam-console support

* Wed Sep 10 2008 Karel Zak <kzak@redhat.com> 2.14.1-1
- upgrade to stable 2.14.1

* Thu Aug 14 2008 Karel Zak <kzak@redhat.com> 2.14.1-0.1
- upgrade to 2.14.1-rc1
- refresh old patches

* Thu Jul 24 2008 Karel Zak <kzak@redhat.com> 2.14-3
- update util-linux-ng-2.14-mount-file_t.patch to make
  the SELinux warning optional (verbose mode is required)

* Tue Jul  1 2008 Karel Zak <kzak@redhat.com> 2.14-2
- fix #390691 - mount should check selinux context on mount, and warn on file_t

* Mon Jun  9 2008 Karel Zak <kzak@redhat.com> 2.14-1
- upgrade to stable util-linux-ng release

* Mon May 19 2008 Karel Zak <kzak@redhat.com> 2.14-0.1
- upgrade to 2.14-rc3
- remove arch(8) (deprecated in favor of uname(1) or arch(1) from coreutils)
- add a new command ldattach(8)
- cfdisk(8) linked with libncursesw

* Tue Apr 22 2008 Karel Zak <kzak@redhat.com> 2.13.1-9
- fix audit log injection attack via login

* Thu Apr 17 2008 Karel Zak <kzak@redhat.com> 2.13.1-8
- fix location of the command raw(8)

* Tue Apr 15 2008 Karel Zak <kzak@redhat.com> 2.13.1-7
- fix 244383 - libblkid uses TYPE="swsuspend" for S1SUSPEND/S2SUSPEND

* Wed Apr  2 2008 Karel Zak <kzak@redhat.com> 2.13.1-6
- fix 439984 - backport mkswap -U

* Wed Mar 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.13.1-5
- clean up sparc conditionals

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.13.1-4
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Karel Zak <kzak@redhat.com> 2.13.1-3
- upgrade to new upstream release
- fix #427874 - util-linux-ng gets "excess command line argument" on update

* Wed Jan  2 2008 Karel Zak <kzak@redhat.com> 2.13.1-2
- update to upstream 2.13.1-rc2

* Wed Dec 12 2007 Dan Walsh <dwalsh@redhat.com> 2.13.1-1
- Fix pam files so that pam_keyinit happens after pam_selinux.so

* Wed Dec 12 2007 Karel Zak <kzak@redhat.com> 2.13.1-0.2
- remove viwp and vigr (in favour of shadow-utils)

* Sun Dec  9 2007 Karel Zak <kzak@redhat.com> 2.13.1-0.1
- update to the latest upstream stable branch
  (commit: fda9d11739ee88c3b2f22a73f12ec019bd3b8335)

* Wed Oct 31 2007 Karel Zak <kzak@redhat.com> 2.13-4
- fix #354791 - blockdev command calls the blkpg ioctl with a wrong data structure

* Tue Oct 16 2007 Karel Zak <kzak@redhat.com> 2.13-3
- fix mount -L | -U segfault
- fix script die on SIGWINCH

* Thu Oct  4 2007 Karel Zak <kzak@redhat.com> 2.13-2
- update to the latest upstream stable branch

* Tue Aug 28 2007 Karel Zak <kzak@redhat.com> 2.13-1
- upgrade to stable util-linux-ng release

* Fri Aug 24 2007 Karel Zak <kzak@redhat.com> 2.13-0.59
- add release number to util-linux Provides and increment setarch Obsoletes
- fix #254114 - spec typo
- upgrade to floppy-0.16
- add BuildRequires: popt-devel

* Wed Aug 22 2007 Jesse Keating <jkeating@redhat.com>  2.13-0.58
- Obsolete a sufficiently high enough version of setarch

* Mon Aug 20 2007 Karel Zak <kzak@redhat.com>  2.13-0.57
- fix #253664 - util-linux-ng fails to build on sparc (patch by Dennis Gilmore)
- rebase to new GIT snapshot

* Mon Aug 20 2007 Karel Zak <kzak@redhat.com> 2.13-0.56
- fix obsoletes field

* Mon Aug 20 2007 Karel Zak <kzak@redhat.com> 2.13-0.55
- util-linux-ng includes setarch(1), define relevat Obsoletes+Provides

* Mon Aug 20 2007 Karel Zak <kzak@redhat.com> 2.13-0.54
- port "blockdev --rmpart" patch from util-linux
- use same Provides/Obsoletes setting like in util-linux

* Wed Aug 15 2007 Karel Zak <kzak@redhat.com> 2.13-0.53
- fix #252046 - review Request: util-linux-ng (util-linux replacement)

* Mon Aug 13 2007 Karel Zak <kzak@redhat.com> 2.13-0.52
- rebase to util-linux-ng (new util-linux upstream fork,
		based on util-linux 2.13-pre7)
- more than 70 Fedora/RHEL patches have been merged to upstream code

* Fri Apr  6 2007 Karel Zak <kzak@redhat.com> 2.13-0.51
- fix #150493 - hwclock --systohc sets clock 0.5 seconds slow
- fix #220873 - starting RPC idmapd: Error: RPC MTAB does not exist.
		(added rpc_pipefs to util-linux-2.13-umount-sysfs.patch)
- fix #227903 - mount -f does not work with NFS-mounted

* Sat Mar  3 2007 David Zeuthen <davidz@redhat.com> 2.13-0.50
- include ConsoleKit session module by default (#229172)

* Thu Jan 11 2007 Karel Zak <kzak@redhat.com> 2.13-0.49
- fix #222293 - undocumented partx,addpart, delpart

* Sun Dec 17 2006 Karel Zak <kzak@redhat.com> 2.13-0.48
- fix paths in po/Makefile.in.in

* Fri Dec 15 2006 Karel Zak <kzak@redhat.com> 2.13-0.47
- fix #217240 - namei ignores non-directory components instead of saying "Not a directory"
- fix #217241 - namei enforces symlink limits inconsistently

* Thu Dec 14 2006 Karel Zak <kzak@redhat.com> 2.13-0.46
- fix leaking file descriptor in the more command (patch by Steve Grubb)

* Wed Dec 13 2006 Karel Zak <kzak@redhat.com> 2.13-0.45
- use ncurses only
- fix #218915 - fdisk -b 4K
- upgrade to -pre7 release
- fix building problem with raw0 patch
- fix #217186 - /bin/sh: @MKINSTALLDIRS@: No such file or directory 
  (port po/Makefile.in.in from gettext-0.16)
- sync with FC6 and RHEL5:
- fix #216489 - SCHED_BATCH option missing in chrt
- fix #216712 - issues with raw device support ("raw0" is wrong device name)
- fix #216760 - mount with context or fscontext option fails
  (temporarily disabled the support for additional contexts -- not supported by kernel yet)
- fix #211827 - Can't mount with additional contexts
- fix #213127 - mount --make-unbindable does not work
- fix #211749 - add -r option to losetup to create a read-only loop

* Thu Oct 12 2006 Karel Zak <kzak@redhat.com> 2.13-0.44
- fix #209911 - losetup.8 updated (use dm-crypt rather than deprecated cryptoloop)
- fix #210338 - spurious error from '/bin/login -h $PHONENUMBER' (bug in IPv6 patch)
- fix #208634 - mkswap "works" without warning on a mounted device

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.13-0.43
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Karel Zak <kzak@redhat.com> 2.13-0.42
- remove obsolete NFS code and patches (we use /sbin/mount.nfs
  and /sbin/umount.nfs from nfs-utils now)
- move nfs.5 to nfs-utils

* Fri Sep 15 2006 Karel Zak <kzak@redhat.com> 2.13-0.41
- fix #205038 - mount not allowing sloppy option (exports "-s"
  to external /sbin/mount.nfs(4) calls) 
- fix minor bug in util-linux-2.13-mount-twiceloop.patch
- fix #188193- util-linux should provide plugin infrastructure for HAL

* Mon Aug 21 2006 Karel Zak <kzak@redhat.com> 2.13-0.40
- fix Makefile.am in util-linux-2.13-mount-context.patch
- fix #201343 - pam_securetty requires known user to work
		(split PAM login configuration to two files)
- fix #203358 - change location of taskset binary to allow for early affinity work

* Fri Aug 11 2006 Karel Zak <kzak@redhat.com> 2.13-0.39
- fix #199745 - non-existant simpleinit(8) mentioned in ctrlaltdel(8)

* Thu Aug 10 2006 Dan Walsh <dwalsh@redhat.com> 2.13-0.38
- Change keycreate line to happen after pam_selinux open call so it gets correct context

* Thu Aug 10 2006 Karel Zak <kzak@redhat.com> 2.13-0.37
- fix #176494 - last -i returns strange IP addresses (patch by Bill Nottingham)

* Thu Jul 27 2006 Karel Zak <kzak@redhat.com> 2.13-0.36
- fix #198300, #199557 - util-linux "post" scriptlet failure

* Thu Jul 27 2006 Steve Dickson <steved@redhat.com> 2.13-0.35
- Added the -o fsc flag to nfsmount.

* Wed Jul 26 2006 Karel Zak <kzak@redhat.com> 2.13-0.34
- rebuild

* Tue Jul 18 2006 Karel Zak <kzak@redhat.com> 2.13-0.33
- add Requires(post): libselinux

* Mon Jul 17 2006 Karel Zak <kzak@redhat.com> 2.13-0.32
- add IPv6 support to the login command (patch by Milan Zazrivec)
- fix #198626 - add keyinit instructions to the login PAM script 
  (patch by David Howells) 

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.13-0.31.1
- rebuild

* Tue Jul 11 2006 Karel Zak <kzak@redhat.com> 2.13-0.31
- cleanup dependences for post and preun scriptlets

* Mon Jul 10 2006 Karsten Hopp <karsten@redhat.de> 2.13-0.30
- silence install in minimal buildroot without /var/log

* Fri Jul  7 2006 Karel Zak <kzak@redhat.com> 2.13-0.29 
- include the raw command for RHELs

* Mon Jun 26 2006 Florian La Roche <laroche@redhat.com> 2.13-0.28
- move install-info parts from postun to preun

* Wed Jun 21 2006 Dan Walsh <dwalsh@RedHat.com> 2.13-0.27
- Only execute chcon on machines with selinux enabled

* Wed Jun 14 2006 Steve Dickson <steved@redhat.com> 2.13-0.26
- Remove unneeded header files from nfsmount.c

* Mon Jun 12 2006 Karel Zak <kzak@redhat.com> 2.13-0.25
- fix #187014 - umount segfaults for normal user
- fix #183446 - cal not UTF-8-aware
- fix #186915 - mount does not translate SELIinux context options though libselinux
- fix #185500 - Need man page entry for -o context= mount option
- fix #152579 - missing info about /etc/mtab and /proc/mounts mismatch
- fix #183890 - missing info about possible ioctl() and fcntl() problems on NFS filesystem
- fix #191230 - using mount --move results in wrong data in /etc/mtab
- added mount subtrees support
- fdisk: wrong number of sectors for large disks (suse#160822)
- merge fdisk-xvd (#182553) with new fdisk-isfull (#188981) patch 
- fix #181549 - raw(8) manpage has old information about dd
- remove asm/page.h usage

* Wed May 24 2006 Dan Walsh <dwalsh@RedHat.com> 2.13-0.24
- Remove requirement on restorecon, since we can do the same thing
- with chcon/matchpathcon, and not add requirement on policycoreutils

* Wed May 24 2006 Steve Dickson <steved@redhat.com> 2.13-0.23
- Fixed bug in patch for bz183713 which cause nfs4 mounts to fail.

* Tue May  2 2006 Steve Dickson <steved@redhat.com> 2.13-0.22
- Added syslog logging to background mounts as suggested
  by a customer.

* Mon May  1 2006 Steve Dickson <steved@redhat.com> 2.13-0.21
- fix #183713 - foreground mounts are not retrying as advertised
- fix #151549 - Added 'noacl' mount flag
- fix #169042 - Changed nfsmount to try udp before using tcp when rpc-ing
		the remote rpc.mountd (iff -o tcp is not specified).
		This drastically increases the total number of tcp mounts
		that can happen at once (ala autofs).

* Thu Mar  9 2006 Jesse Keating <jkeating@redhat.com> 2.13-0.20
- Better calling of restorecon as suggested by Bill Nottingham
- prereq restorecon to avoid ordering issues

* Thu Mar  9 2006 Jesse Keating <jkeating@redhat.com> 2.13-0.19
- restorecon /var/log/lastlog

* Wed Mar  8 2006 Karel Zak <kzak@redhat.com> 2.13-0.17
- fix #181782 - mkswap selinux relabeling (fix util-linux-2.13-mkswap-selinux.patch)

* Wed Feb 22 2006 Karel Zak <kzak@redhat.com> 2.13-0.16
- fix #181782 - mkswap should automatically add selinux label to swapfile
- fix #180730 - col is exiting with 1 (fix util-linux-2.12p-col-EILSEQ.patch)
- fix #181896 - broken example in schedutils man pages
- fix #177331 - login omits pam_acct_mgmt & pam_chauthtok when authentication is skipped.
- fix #177523 - umount -a should not unmount sysfs
- fix #182553 - fdisk -l inside xen guest shows no disks

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13-0.15.1
- bump again for double-long bug on ppc(64)

* Wed Feb  8 2006 Peter Jones <pjones@redhat.com> 2.13-0.15
- add "blockdev --rmpart N <device>" and "blockdev --rmparts <device>"

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13-0.14.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 19 2006 Steve Dickson <steved@redhat.com> 2.13-0.14
- Updated the gssd_check() and idmapd_check(), used with
  nfsv4 mounts, to looked for the correct file in /var/lock/subsys
  which stops bogus warnings. 

* Tue Jan  3 2006 Karel Zak <kzak@redhat.com> 2.13-0.13
- fix #174676 - hwclock audit return code mismatch
- fix #176441: col truncates data
- fix #174111 - mount allows loopback devices to be mounted more than once to the same mount point
- better wide chars usage in the cal command (based on the old 'moremisc' patch)

* Mon Dec 12 2005 Karel Zak <kzak@redhat.com> 2.13-0.12
- rebuilt

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 25 2005 Karel Zak <kzak@redhat.com> 2.13-0.11.pre6
- update to upstream version 2.13-pre6
- fix #172203 - mount man page in RHEL4 lacks any info on cifs mount options

* Mon Nov  7 2005 Karel Zak <kzak@redhat.com> 2.13-0.10.pre5
- fix #171337 - mkfs.cramfs doesn't work correctly with empty files

* Fri Oct 28 2005 Karel Zak <kzak@redhat.com> 2.13-0.9.pre5
- rebuild

* Wed Oct 26 2005 Karel Zak <kzak@redhat.com> 2.13-0.8.pre5
- updated version of the patch for hwclock audit

* Thu Oct 20 2005 Karel Zak <kzak@redhat.com> 2.13-0.7.pre5
- fix #171337 - mkfs.cramfs dies creating installer image

* Thu Oct 20 2005 Karel Zak <kzak@redhat.com> 2.13-0.6.pre5
- update to upstream 2.13pre5
- remove separated cramfs1.1 (already in upstream package)
- remove odd symlink /usr/bin/mkcramfs -> ../../sbin/mkfs.cramfs
- fix #170171 - ipcs -lm always report "max total shared memory (kbytes) = 0"

* Mon Oct 17 2005 Karel Zak <kzak@redhat.com> 2.13-0.5.pre4
* fix #170564 - add audit message to login

* Fri Oct  7 2005 Karel Zak <kzak@redhat.com> 2.13-0.4.pre4
- fix #169628 - /usr/bin/floppy doesn't work with /dev/fd0
- fix #168436 - login will attempt to run if it has no read/write access to its terminal
- fix #168434 - login's timeout can fail - needs to call siginterrupt(SIGALRM,1)
- fix #165253 - losetup missing option -a [new feature]
- update PAM files (replace pam_stack with new "include" PAM directive)
- remove kbdrate from src.rpm
- update to 2.13pre4

* Fri Oct  7 2005 Steve Dickson <steved@redhat.com> 2.13-0.3.pre3
- fix #170110 - Documentation for 'rsize' and 'wsize' NFS mount options
		is misleading

* Fri Sep  2 2005 Karel Zak <kzak@redhat.com> 2.13-0.3.pre2
- fix #166923 - hwclock will not run on a non audit-enabled kernel
- fix #159410 - mkswap(8) claims max swap area size is 2 GB
- fix #165863 - swsusp swaps should be reinitialized
- change /var/log/lastlog perms to 0644

* Tue Aug 16 2005 Karel Zak <kzak@redhat.com> 2.13-0.2.pre2
- /usr/share/misc/getopt/* -move-> /usr/share/doc/util-linux-2.13/getopt-*
- the arch command marked as deprecated
- removed: elvtune, rescuept and setfdprm
- removed: man8/sln.8 (moved to man-pages, see #10601)
- removed REDAME.pg and README.reset
- .spec file cleanup
- added schedutils (commands: chrt, ionice and taskset)

* Tue Jul 12 2005 Karel Zak <kzak@redhat.com> 2.12p-9.7
- fix #159339 - util-linux updates for new audit system
- fix #158737 - sfdisk warning for large partitions, gpt
- fix #150912 - Add ocfs2 support
- NULL is better than zero at end of execl()

* Thu Jun 16 2005 Karel Zak <kzak@redhat.com> 2.12p-9.5
- fix #157656 - CRM 546998: Possible bug in vipw, changes permissions of /etc/shadow and /etc/gshadow
- fix #159339 - util-linux updates for new audit system (pam_loginuid.so added to util-linux-selinux.pamd)
- fix #159418 - sfdisk unusable - crashes immediately on invocation
- fix #157674 - sync option on VFAT mount destroys flash drives
- fix .spec file /usr/sbin/{hwclock,clock} symlinks

* Wed May  4 2005 Jeremy Katz <katzj@redhat.com> - 2.12p-9.3
- rebuild against new libe2fsprogs (and libblkid) to fix cramfs auto-detection

* Mon May  2 2005 Karel Zak <kzak@redhat.com> 2.12p-9.2
- rebuild

* Mon May  2 2005 Karel Zak <kzak@redhat.com> 2.12p-9
- fix #156597 - look - doesn't work with separators

* Mon Apr 25 2005 Karel Zak <kzak@redhat.com> 2.12p-8
- fix #154498 - util-linux login & pam session
- fix #155293 - man 5 nfs should include vers as a mount option
- fix #76467 - At boot time, fsck chokes on LVs listed by label in fstab
- new Source URL
- added note about ATAPI IDE floppy to fdformat.8
- fix #145355 - Man pages for fstab and fstab-sync in conflict

* Tue Apr  5 2005 Karel Zak <kzak@redhat.com> 2.12p-7
- enable build with libblkid from e2fsprogs-devel
- remove workaround for duplicated labels

* Thu Mar 31 2005 Steve Dickson <SteveD@RedHat.com> 2.12p-5
- Fixed nfs mount to rollback correctly.

* Fri Mar 25 2005 Karel Zak <kzak@redhat.com> 2.12p-4
- added /var/log/lastlog to util-linux (#151635)
- disabled 'newgrp' in util-linux (enabled in shadow-utils) (#149997, #151613)
- improved mtab lock (#143118)
- fixed ipcs typo (#151156)
- implemented mount workaround for duplicated labels (#116300)

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com> 2.12p-3
- rebuilt

* Fri Feb 25 2005 Steve Dickson <SteveD@RedHat.com> 2.12p-2
- Changed nfsmount to only use reserve ports when necessary
  (bz# 141773) 

* Thu Dec 23 2004 Elliot Lee <sopwith@redhat.com> 2.12p-1
- Update to util-linux-2.12p. This changes swap header format
  from - you may need to rerun mkswap if you did a clean install of
  FC3.

* Fri Dec 10 2004 Elliot Lee <sopwith@redhat.com> 2.12j-1
- Update to util-linux-2.12j

* Tue Dec  7 2004 Steve Dickson <SteveD@RedHat.com> 2.12a-20
- Corrected a buffer overflow problem with nfs mounts.
  (bz# 141733) 

* Wed Dec 01 2004 Elliot Lee <sopwith@redhat.com> 2.12a-19
- Patches for various bugs.

* Mon Nov 29 2004 Steve Dickson <SteveD@RedHat.com> 2.12a-18
- Made NFS mounts adhere to the IP protocol if specified on
  command line as well as made NFS umounts adhere to the
  current IP protocol. Fix #140016

* Thu Oct 14 2004 Elliot Lee <sopwith@redhat.com> 2.12a-16
- Add include_raw macro, build with it off for Fedora

* Wed Oct 13 2004 Stephen C. Tweedie <sct@redhat.com> - 2.12a-15
- Add raw patch to allow binding of devices not yet in /dev

* Wed Oct 13 2004 John (J5) Palmieri <johnp@redhat.com> 2.12a-14
- Add David Zeuthen's patch to enable the pamconsole flag #133941

* Wed Oct 13 2004 Stephen C. Tweedie <sct@redhat.com> 2.12a-13
- Restore raw utils (bugzilla #130016)

* Mon Oct 11 2004 Phil Knirsch <pknirsch@redhat.com> 2.12a-12
- Add the missing remote entry in pam.d

* Wed Oct  6 2004 Steve Dickson <SteveD@RedHat.com>
- Rechecked in some missing NFS mounting code.

* Wed Sep 29 2004 Elliot Lee <sopwith@redhat.com> 2.12a-10
- Make swaplabel support work with swapon -a -e

* Tue Sep 28 2004 Steve Dickson <SteveD@RedHat.com>
- Updated the NFS and NFS4 code to the latest CITI patch set
  (in which they incorporate a number of our local patches).

* Wed Sep 15 2004 Nalin Dahybhai <nalin@redhat.com> 2.12a-8
- Fix #132196 - turn on SELinux support at build-time.

* Wed Sep 15 2004 Phil Knirsch <pknirsch@redhat.com> 2.12a-7
- Fix #91174 with pamstart.patch

* Tue Aug 31 2004 Elliot Lee <sopwith@redhat.com> 2.12a-6
- Fix #16415, #70616 with rdevman.patch
- Fix #102566 with loginman.patch
- Fix #104321 with rescuept.patch (just use plain lseek - we're in _FILE_OFFSET_BITS=64 land now)
- Fix #130016 - remove raw.
- Re-add agetty (replacing it with mgetty is too much pain, and mgetty is much larger)

* Thu Aug 26 2004 Steve Dickson <SteveD@RedHat.com>
- Made the NFS security checks more explicit to avoid confusion
  (an upstream fix)
- Also removed a compilation warning

* Wed Aug 11 2004 Alasdair Kergon <agk@redhat.com>
- Remove unused mount libdevmapper inclusion.

* Wed Aug 11 2004 Alasdair Kergon <agk@redhat.com>
- Add device-mapper mount-by-label support
- Fix segfault in mount-by-label when a device without a label is present.

* Wed Aug 11 2004 Steve Dickson <SteveD@RedHat.com>
- Updated nfs man page to show that intr are on by
  default for nfs4

* Thu Aug 05 2004 Jindrich Novy <jnovy@redhat.com>
- modified warning causing heart attack for >16 partitions, #107824

* Fri Jul 09 2004 Elliot Lee <sopwith@redhat.com> 2.12a-3
- Fix #126623, #126572
- Patch cleanup
- Remove agetty (use mgetty, agetty is broken)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun 03 2004 Elliot Lee <sopwith@redhat.com> 2.12a-1
- Update to 2.12a
- Fix #122448

* Thu May 13 2004 Dan Walsh <dwalsh@RedHat.com> 2.12-19
- Change pam_selinux to run last

* Tue May 04 2004 Elliot Lee <sopwith@redhat.com> 2.12-18
- Fix #122448 (autofs issues)

* Fri Apr 23 2004 Elliot Lee <sopwith@redhat.com> 2.12-17
- Fix #119157 by editing the patch
- Add patch145 to fix #119986

* Fri Apr 16 2004 Elliot Lee <sopwith@redhat.com> 2.12-16
- Fix #118803

* Tue Mar 23 2004 Jeremy Katz <katzj@redhat.com> 2.12-15
- mkcramfs: use PAGE_SIZE for default blocksize (#118681)

* Sat Mar 20 2004 <SteveD@RedHat.com>
- Updated the nfs-mount.patch to correctly 
  handle the mounthost option and to ignore 
  servers that do not set auth flavors

* Tue Mar 16 2004 Dan Walsh <dwalsh@RedHat.com> 2.12-13
- Fix selinux ordering or pam for login

* Tue Mar 16 2004 <SteveD@RedHat.com>
- Make RPC error messages displayed with -v argument
- Added two checks to the nfs4 path what will print warnings
  when rpc.idmapd and rpc.gssd are not running
- Ping NFS v4 servers before diving into kernel
- Make v4 mount interruptible which also make the intr option on by default 

* Sat Mar 13 2004  <SteveD@RedHat.com>
- Reworked how the rpc.idmapd and rpc.gssd checks were
  done due to review comments from upstream.
- Added rpc_strerror() so the '-v' flag will show RPC errors.

* Sat Mar 13 2004  <SteveD@RedHat.com>
- Added two checks to the nfs4 path what will print warnings
  when rpc.idmapd and rpc.gssd are not running.

* Thu Mar 11 2004 <SteveD@RedHat.com>
- Reworked and updated the nfsv4 patches.

* Wed Mar 10 2004 Dan Walsh <dwalsh@RedHat.com>
- Bump version

* Wed Mar 10 2004 Steve Dickson <SteveD@RedHat.com>
- Tried to make nfs error message a bit more meaninful
- Cleaned up some warnings

* Sun Mar  7 2004 Steve Dickson <SteveD@RedHat.com> 
- Added pesudo flavors for nfsv4 mounts.
- Added BuildRequires: libselinux-devel and Requires: libselinux
  when WITH_SELINUX is set. 

* Fri Feb 27 2004 Dan Walsh <dwalsh@redhat.com> 2.12-5
- check for 2.6.3 kernel in mount options

* Mon Feb 23 2004 Elliot Lee <sopwith@redhat.com> 2.12-4
- Remove /bin/kill for #116100

* Fri Feb 20 2004 Dan Walsh <dwalsh@redhat.com> 2.12-3
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 12 2004 Elliot Lee <sopwith@redhat.com> 2.12-1
- Final 2.12 has been out for ages - might as well use it.

* Wed Jan 28 2004 Steve Dickson <SteveD@RedHat.com> 2.12pre-4
- Added mount patches that have NFS version 4 support

* Mon Jan 26 2004 Elliot Lee <sopwith@redhat.com> 2.12pre-3
- Provides: mount losetup

* Mon Jan 26 2004 Dan Walsh <dwalsh@redhat.com> 2.12pre-2
- Add multiple to /etc/pam.d/login for SELinux

* Thu Jan 15 2004 Elliot Lee <sopwith@redhat.com> 2.12pre-1
- 2.12pre-1
- Merge mount/losetup packages into the main package (#112324)
- Lose separate 

* Mon Nov 3 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-35.sel
- remove selinux code from login and use pam_selinux

* Thu Oct 30 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-34.sel
- turn on selinux

* Fri Oct 24 2003 Elliot Lee <sopwith@redhat.com> 2.11y-34
- Add BuildRequires: texinfo (from a bug# I don't remember)
- Fix #90588 with mountman patch142.

* Mon Oct 6 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-33
- turn off selinux

* Thu Sep 25 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-32.sel
- turn on selinux
- remove context selection

* Fri Sep 19 2003 Elliot Lee <sopwith@redhat.com> 2.11y-31
- Add patch140 (alldevs) to fix #101772. Printing the total size of
  all devices was deemed a lower priority than having all devices
  (e.g. /dev/ida/c0d9) displayed.

* Fri Sep 12 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-31
- turn off selinux

* Fri Sep 12 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-30.sel
- turn on selinux

* Fri Sep 5 2003 Elliot Lee <sopwith@redhat.com> 2.11y-28
- Fix #103004, #103954

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-27
- turn off selinux

* Thu Sep 4 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-26.sel
- build with selinux

* Mon Aug 11 2003 Elliot Lee <sopwith@redhat.com> 2.11y-25
- Use urandom instead for mkcramfs

* Tue Jul 29 2003 Dan Walsh <dwalsh@redhat.com> 2.11y-24
- add SELINUX 2.5 support

* Wed Jul 23 2003 Elliot Lee <sopwith@redhat.com> 2.11y-22
- #100433 patch

* Sat Jun 14 2003 Elliot Lee <sopwith@redhat.com> 2.11y-20
- #97381 patch

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 21 2003 Elliot Lee <sopwith@redhat.com> 2.11y-17
- Change patch128 to improve ipcs -l

* Fri Apr 11 2003 Elliot Lee <sopwith@redhat.com> 2.11y-16
- Fix #85407

* Fri Apr 11 2003 Elliot Lee <sopwith@redhat.com> 2.11y-15
- Change patch128 to util-linux-2.11f-ipcs-84243-86285.patch to get all
ipcs fixes

* Thu Apr 10 2003 Matt Wilson <msw@redhat.com> 2.11y-14
- fix last login date display on AMD64 (#88574)

* Mon Apr  7 2003 Jeremy Katz <katzj@redhat.com> 2.11y-13
- include sfdisk on ppc

* Fri Mar 28 2003 Jeremy Katz <katzj@redhat.com> 2.11y-12
- add patch from msw to change mkcramfs blocksize with a command line option

* Tue Mar 25 2003 Phil Knirsch <pknirsch@redhat.com> 2.11y-11
- Fix segfault on s390x due to wrong usage of BLKGETSIZE.

* Thu Mar 13 2003 Elliot Lee <sopwith@redhat.com> 2.11y-10
- Really apply the ipcs patch. Doh.

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 19 2003 Elliot Lee <sopwith@redhat.com> 2.11y-8
- ipcs-84243.patch to fix #84243

* Thu Feb 13 2003 Yukihiro Nakai <ynakai@redhat.com> 2.11y-7
- Update moremisc patch to fix swprintf()'s minimum field (bug #83361).

* Mon Feb 03 2003 Elliot Lee <sopwith@redhat.com> 2.11y-6
- Fix mcookie segfault on many 64-bit architectures (bug #83345).

* Mon Feb 03 2003 Tim Waugh <twaugh@redhat.com> 2.11y-5
- Fix underlined multibyte characters (bug #83376).

* Sun Feb 02 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuild to have again a s390 rpm
- disable some more apps for mainframe

* Wed Jan 29 2003 Elliot Lee <sopwith@redhat.com> 2.11y-4
- util-linux-2.11y-umask-82552.patch

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Elliot Lee <sopwith@redhat.com> 2.11y-2
- Fix #81069, #75421

* Mon Jan 13 2003 Elliot Lee <sopwith@redhat.com> 2.11y-1
- Update to 2.11y
- Fix #80953
- Update patch0, patch107, patch117, patch120 for 2.11y
- Remove patch60, patch61, patch207, patch211, patch212, patch119, patch121
- Remove patch122, patch200

* Wed Oct 30 2002 Elliot Lee <sopwith@redhat.com> 2.11w-2
- Remove some crack/unnecessary patches while submitting stuff upstream.
- Build with -D_FILE_OFFSET_BITS=64

* Tue Oct 29 2002 Elliot Lee <sopwith@redhat.com> 2.11w-1
- Update to 2.11w, resolve patch conflicts

* Tue Oct 08 2002 Phil Knirsch <pknirsch@redhat.com> 2.11r-10hammer.3
- Extended util-linux-2.11b-s390x patch to work again.

* Thu Oct 03 2002 Elliot Lee <sopwith@redhat.com> 2.11r-10hammer.2
- Add patch122 for hwclock on x86_64

* Thu Sep 12 2002 Than Ngo <than@redhat.com> 2.11r-10hammer.1
- Fixed pam config files

* Wed Sep 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.11r-10hammer
- Port to hammer

* Fri Aug 30 2002 Elliot Lee <sopwith@redhat.com> 2.11r-10
- Patch120 (hwclock) to fix #72140
- Include isosize util

* Wed Aug 7 2002  Elliot Lee <sopwith@redhat.com> 2.11r-9
- Patch120 (skipraid2) to fix #70353, because the original patch was 
totally useless.

* Fri Aug 2 2002  Elliot Lee <sopwith@redhat.com> 2.11r-8
- Patch119 (fdisk-add-primary) from #67898

* Wed Jul 24 2002 Elliot Lee <sopwith@redhat.com> 2.11r-7
- Really add the gptsize patch, instead of what I think the patch says.
(+1)

* Tue Jul 23 2002 Elliot Lee <sopwith@redhat.com> 2.11r-6
- Add the sp[n].size part of the patch from #69603

* Mon Jul 22 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- adjust mainframe patches

* Tue Jul  2 2002 Bill Nottingham <notting@redhat.com> 2.11r-4
- only require usermode if we're shipping kbdrate here

* Fri Jun 28 2002 Trond Eivind Glomsrod <teg@redhat.com> 2.11r-3
- Port the large swap patch to new util-linux... the off_t changes 
  now in main aren't sufficient

* Thu Jun 27 2002 Elliot Lee <sopwith@redhat.com> 2.11r-2
- Remove swapondetect (patch301) until it avoids possible false positives.

* Thu Jun 27 2002 Elliot Lee <sopwith@redhat.com> 2.11r-1
- Update to 2.11r, wheeee
- Remove unused patches

* Thu Jun 27 2002 Elliot Lee <sopwith@redhat.com> 2.11n-19
- Make a note here that this package was the source of the single change 
contained in util-linux-2.11f-18 (in 7.2/Alpha), and also contains the 
rawman patch from util-linux-2.11f-17.1 (in 2.1AS).
- Package has no runtime deps on slang, so remove the BuildRequires: 
slang-devel.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 20 2002 Elliot Lee <sopwith@redhat.com> 2.11n-17
- Fix teg's swapondetect patch to not print out the usage message when 
'swapon -a -e' is run. (#66690) (edit existing patch)
- Apply hjl's utmp handling patch (#66950) (patch116)
- Fix fdisk man page notes on IDE disk partition limit (#64013) (patch117)
- Fix mount.8 man page notes on vfat shortname option (#65628) (patch117)
- Fix possible cal overflow with widechars (#67090) (patch117)

* Tue Jun 11 2002 Trond Eivind Glomsrod <teg@redhat.com> 2.11n-16
- support large swap partitions
- add '-d' option to autodetect available swap partitions

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 15 2002 Elliot Lee <sopwith@redhat.com> 2.11n-14
- Remove kbdrate (again).

* Mon Apr 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- adjust mainframe patches to apply to current rpm
- do not include fdisk until it is fixed to work on mainframe

* Mon Apr 01 2002 Elliot Lee <sopwith@redhat.com> 2.11n-12
- Don't strip binaries - rpm does it for us.

* Sun Mar 31 2002 Elliot Lee <sopwith@redhat.com> 2.11n-11
- Apply patch115 from ejb@ql.org for bug #61868

* Wed Mar 27 2002 Elliot Lee <sopwith@redhat.com> 2.11n-10
- Finish fixing #60675 (ipcrm man page), updated the patch.
- Fix #61203 (patch114 - dumboctal.patch).

* Tue Mar 12 2002 Elliot Lee <sopwith@redhat.com> 2.11n-9
- Update ctty3 patch to ignore SIGHUP while dropping controlling terminal

* Fri Mar 08 2002 Elliot Lee <sopwith@redhat.com> 2.11n-8
- Update ctty3 patch to drop controlling terminal before forking.

* Fri Mar 08 2002 Elliot Lee <sopwith@redhat.com> 2.11n-7
  Fix various bugs:
- Add patch110 (skipraid) to properly skip devices that are part of a RAID array.
- Add patch111 (mkfsman) to update the mkfs man page's "SEE ALSO" section.
- remove README.cfdisk
- Include partx
- Fix 54741 and related bugs for good(hah!) with patch113 (ctty3)

* Wed Mar 06 2002 Elliot Lee <sopwith@redhat.com> 2.11n-6
- Put kbdrate in, add usermode dep.

* Tue Feb 26 2002 Elliot Lee <sopwith@redhat.com> 2.11n-5
- Fix #60363 (tweak raw.8 man page, make rawdevices.8 symlink).

* Mon Jan 28 2002 Bill Nottingham <notting@redhat.com> 2.11n-4
- remove kbdrate (fixes kbd conflict)

* Fri Dec 28 2001 Elliot Lee <sopwith@redhat.com> 2.11n-3
- Add util-linux-2.11n-ownerumount.patch (#56593)
- Add patch102 (util-linux-2.11n-colrm.patch) to fix #51887
- Fix #53452 nits.
- Fix #56953 (remove tunelp on s390)
- Fix #56459, and in addition switch to using sed instead of perl.
- Fix #58471
- Fix #57300
- Fix #37436
- Fix #32132

* Wed Dec 26 2001 Elliot Lee <sopwith@redhat.com> 2.11n-1
- Update to 2.11n
- Merge mount/losetup back in.

* Tue Dec 04 2001 Elliot Lee <sopwith@redhat.com> 2.11f-17
- Add patch38 (util-linux-2.11f-ctty2.patch) to ignore SIGINT/SIGTERM/SIGQUIT in the parent, so that ^\ won't break things.

* Fri Nov 09 2001 Elliot Lee <sopwith@redhat.com> 2.11f-16
- Merge patches 36, 75, 76, and 77 into patch #37, to attempt resolve all the remaining issues with #54741.

* Wed Oct 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add nologin man-page for s390/s390x

* Wed Oct 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.11f-14
- Don't build kbdrate on s390/s390x
- Don't make the pivot_root.8 man page executable(!)

* Tue Oct 23 2001 Elliot Lee <sopwith@redhat.com> 2.11f-13
- Patch/idea #76 from HJL, fixes bug #54741 (race condition in login 
acquisition of controlling terminal).

* Thu Oct 11 2001 Bill Nottingham <notting@redhat.com>
- fix permissions problem with vipw & shadow files, again (doh!)

* Tue Oct 09 2001 Erik Troan <ewt@redhat.com>
- added patch from Olaf Kirch to fix possible pwent structure overwriting

* Fri Sep 28 2001 Elliot Lee <sopwith@redhat.com> 2.11f-10
- fdisk patch from arjan

* Sun Aug 26 2001 Elliot Lee <sopwith@redhat.com> 2.11f-9
- Don't include cfdisk, since it appears to be an even bigger pile of junk than fdisk? :)

* Wed Aug  1 2001 Tim Powers <timp@redhat.com>
- don't require usermode

* Mon Jul 30 2001 Elliot Lee <sopwith@redhat.com> 2.11f-7
- Incorporate kbdrate back in.

* Mon Jul 30 2001 Bill Nottingham <notting@redhat.com>
- revert the patch that calls setsid() in login that we had reverted
  locally but got integrated upstream (#46223)

* Tue Jul 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- correct s390x patch

* Mon Jul 23 2001 Elliot Lee <sopwith@redhat.com>
- Add my megapatch (various bugs)
- Include pivot_root (#44828)

* Thu Jul 12 2001 Bill Nottingham <notting@redhat.com>
- make shadow files 0400, not 0600

* Wed Jul 11 2001 Bill Nottingham <notting@redhat.com>
- fix permissions problem with vipw & shadow files

* Mon Jun 18 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.11f, remove any merged patches
- add s390x patches for somewhat larger swap

* Thu Jun 14 2001 Erik Troan <ewt@redhat.com>
- added --verbose patch to mkcramfs; it's much quieter by default now

* Tue May 22 2001 Erik Troan <ewt@redhat.com>
- removed warning about starting partitions on cylinder 0 -- swap version2
  makes it unnecessary

* Wed May  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.11b-2
- Fix up s390x support

* Mon May  7 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.11b-1
- Fix up login for real (a console session should be the controlling tty)
  by reverting to 2.10s code (#36839, #36840, #39237)
- Add man page for agetty (#39287)
- 2.11b, while at it

* Fri Apr 27 2001 Preston Brown <pbrown@redhat.com> 2.11a-4
- /sbin/nologin from OpenBSD added.

* Fri Apr 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.11a-3
- Fix up login - exiting immediately even if the password is correct
  is not exactly a nice feature.
- Make definite plans to kill people who update login without checking
  if the new version works ;)

* Tue Apr 17 2001 Erik Troan <ewt@redhat.com>
- upgraded to 2.11a (kbdrate moved to kbd, among other things)
- turned off ALLOW_VCS_USE
- modified mkcramfs to not use a large number of file descriptors
- include mkfs.bfs

* Sun Apr  8 2001 Matt Wilson <msw@redhat.com>
- changed Requires: kernel >= 2.2.12-7 to Conflicts: kernel < 2.2.12-7
  (fixes a initscripts -> util-linux -> kernel -> initscripts prereq loop)

* Tue Mar 20 2001 Matt Wilson <msw@redhat.com>
- patched mkcramfs to use the PAGE_SIZE from asm/page.h instead of hard
  coding 4096 (fixes mkcramfs on alpha...)

* Mon Mar 19 2001 Matt Wilson <msw@redhat.com>
- added mkcramfs (from linux/scripts/mkcramfs)

* Mon Feb 26 2001 Tim Powers <timp@redhat.com>
- fixed bug #29131, where ipc.info didn't have an info dir entry,
  added the dir entry to ipc.texi (Patch58)

* Fri Feb 23 2001 Preston Brown <pbrown@redhat.com>
- use lang finder script
- install info files

* Thu Feb 08 2001 Erik Troan <ewt@redhat.com>
- reverted login patch; seems to cause problems
- added agetty

* Wed Feb 07 2001 Erik Troan <ewt@redhat.com>
- updated kill man page
- added patch to fix vipw race
- updated vipw to edit /etc/shadow and /etc/gshadow, if appropriate
- added patch to disassociate login from tty, session, and pgrp

* Tue Feb 06 2001 Erik Troan <ewt@redhat.com>
- fixed problem w/ empty extended partitions
- added patch to fix the date in the more man page
- set OPT to pass optimization flags to make rather then RPM_OPT_FLAG
- fixed fdisk -l /Proc/partitions parsing
- updated to 2.10s

* Tue Jan 23 2001 Preston Brown <pbrown@redhat.com>
- danish translations added

* Mon Jan 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix segfault in login in btmp patch (#24025)

* Mon Dec 11 2000 Oliver Paukstadt <oliver.paukstadt@millenux.com>
- ported to s390

* Wed Nov 01 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.10p
- update patch37 to newer fdisk version

* Mon Oct  9 2000 Jeff Johnson <jbj@redhat.com>
- update to 2.10o
-  fdformat: fixed to work with kernel 2.4.0test6 (Marek Wojtowicz)
-  login: not installed suid
-  getopt: by default install aux files in /usr/share/misc
- update to 2.10n:
-  added blockdev.8
-  change to elvtune (andrea)
-  fixed overrun in agetty (vii@penguinpowered.com)
-  shutdown: prefer umounting by mount point (rgooch)
-  fdisk: added plan9
-  fdisk: remove empty links in chain of extended partitions
-  hwclock: handle both /dev/rtc and /dev/efirtc (Bill Nottingham)
-  script: added -f (flush) option (Ivan Schreter)
-  script: added -q (quiet) option (Per Andreas Buer)
-  getopt: updated to version 1.1.0 (Frodo Looijaard)
-  Czech messages (Jiri Pavlovsky)
- login.1 man page had not /var/spool/mail path (#16998).
- sln.8 man page (but not executable) included (#10601).
- teach fdisk 0xde(Dell), 0xee(EFI GPT), 0xef(EFI FAT) partitions (#17610).

* Wed Aug 30 2000 Matt Wilson <msw@redhat.com>
- rebuild to cope with glibc locale binary incompatibility, again

* Mon Aug 14 2000 Jeff Johnson <jbj@redhat.com>
- setfdprm should open with O_WRONLY, not 3.

* Fri Aug 11 2000 Jeff Johnson <jbj@redhat.com>
- fdformat should open with O_WRONLY, not 3.

* Fri Jul 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- make 'look' look in /usr/share/dict

* Fri Jul 21 2000 Bill Nottingham <notting@redhat.com>
- put /usr/local/sbin:/usr/local/bin in root's path

* Wed Jul 19 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild to cope with glibc locale binary incompatibility

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Bill Nottingham <notting@redhat.com>
- enable hwclock to use /dev/efirtc on ia64 (gettext is fun. :( )

* Mon Jul  3 2000 Bill Nottingham <notting@redhat.com>
- move cfdisk to /usr/sbin, it depends on /usr stuff
- add rescuept

* Fri Jun 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- point more at the correct path to vi (for "v"), Bug #10882

* Sun Jun  4 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging changes.

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- modify PAM setup to use system-auth

* Mon May  1 2000 Bill Nottingham <notting@redhat.com>
- eek, where did login go? (specfile tweaks)

* Mon Apr 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.10k
- fix compilation with current glibc

* Tue Mar 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.10h

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Sat Mar  4 2000 Matt Wilson <msw@redhat.com>
- use snprintf - not sprintf - when doing
  sprintf ("%%s\n", _("Some string")) to avoid overflows and
  segfaults.

* Mon Feb 21 2000 Jeff Johnson <jbj@redhat.com>
- raw control file was /dev/raw, now /dev/rawctl.
- raw access files were /dev/raw*, now /dev/raw/raw*.

* Thu Feb 17 2000 Erik Troan <ewt@redhat.com>
- -v argument to mkswap wasn't working

* Thu Feb 10 2000 Jakub Jelinek <jakub@redhat.com>
- Recognize 0xfd on Sun disklabels as RAID

* Tue Feb  8 2000 Bill Nottingham <notting@redhat.com>
- more lives in /bin, and was linked against /usr/lib/libnurses. Bad.

* Thu Feb 03 2000 Jakub Jelinek <jakub@redhat.com>
- update to 2.10f
- fix issues in the new realpath code, avoid leaking memory

* Tue Feb 01 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies
- add NFSv3 patches

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- don't require csh

* Mon Jan 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.10e
- add rename

* Thu Jan 20 2000 Jeff Johnson <jbj@redhat.com>
- strip newlines in logger input.

* Mon Jan 10 2000 Jeff Johnson <jbj@redhat.com>
- rebuild with correct ncurses libs.

* Tue Dec  7 1999 Matt Wilson <msw@redhat.com>
- updated to util-linux 2.10c
- deprecated IMAP login mail notification patch17
- deprecated raw patch22
- depricated readprofile patch24

* Tue Dec  7 1999 Bill Nottingham <notting@redhat.com>
- add patch for readprofile

* Thu Nov 18 1999 Michael K. Johnson <johnsonm@redhat.com>
- tunelp should come from util-linux

* Tue Nov  9 1999 Jakub Jelinek <jakub@redhat.com>
- kbdrate cannot use /dev/port on sparc.

* Wed Nov  3 1999 Jakub Jelinek <jakub@redhat.com>
- fix kbdrate on sparc.

* Wed Oct 27 1999 Bill Nottingham <notting@redhat.com>
- ship hwclock on alpha.

* Tue Oct  5 1999 Bill Nottingham <notting@redhat.com>
- don't ship symlinks to rdev if we don't ship rdev.

* Tue Sep 07 1999 Cristian Gafton <gafton@redhat.com>
- add rawIO support from sct

* Mon Aug 30 1999 Preston Brown <pbrown@redhat.com>
- don't display "new mail" message when the only piece of mail is from IMAP

* Fri Aug 27 1999 Michael K. Johnson <johnsonm@redhat.com>
- kbdrate is now a console program

* Thu Aug 26 1999 Jeff Johnson <jbj@redhat.com>
- hostid is now in sh-utils. On sparc, install hostid as sunhostid (#4581).
- update to 2.9w:
-  Updated mount.8 (Yann Droneaud)
-  Improved makefiles
-  Fixed flaw in fdisk

* Tue Aug 10 1999 Jeff Johnson <jbj@redhat.com>
- tsort is now in textutils.

* Wed Aug  4 1999 Bill Nottingham <notting@redhat.com>
- turn off setuid bit on login. Again. :(

* Tue Aug  3 1999 Peter Jones, <pjones@redhat.com>
- hostid script for sparc (#3803).

* Tue Aug 03 1999 Christian 'Dr. Disk' Hechelmann <drdisk@tc-gruppe.de>
- added locale message catalogs to %%file
- added patch for non-root build
- vigr.8 and /usr/lib/getopt  man-page was missing from file list
- /etc/fdprm really is a config file

* Fri Jul 23 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.9v:
- cfdisk no longer believes the kernel's HDGETGEO
	(and may be able to partition a 2 TB disk)

* Fri Jul 16 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.9u:
- Czech more.help and messages (Jiri Pavlovsky)
- Japanese messages (Daisuke Yamashita)
- fdisk fix (Klaus G. Wagner)
- mount fix (Hirokazu Takahashi)
- agetty: enable hardware flow control (Thorsten Kranzkowski)
- minor cfdisk improvements
- fdisk no longer accepts a default device
- Makefile fix

* Tue Jul  6 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.9t:
- national language support for hwclock
- Japanese messages (both by Daisuke Yamashita)
- German messages and some misc i18n fixes (Elrond)
- Czech messages (Jiri Pavlovsky)
- wall fixed for /dev/pts/xx ttys
- make last and wall use getutent() (Sascha Schumann)
	[Maybe this is bad: last reading all of wtmp may be too slow.
	Revert in case people complain.]
- documented UUID= and LABEL= in fstab.5
- added some partition types
- swapon: warn only if verbose

* Fri Jun 25 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.9s.

* Sat May 29 1999 Jeff Johnson <jbj@redhat.com>
- fix mkswap sets incorrect bits on sparc64 (#3140).

* Thu Apr 15 1999 Jeff Johnson <jbj@redhat.com>
- on sparc64 random ioctls on clock interface cause kernel messages.

* Thu Apr 15 1999 Jeff Johnson <jbj@redhat.com>
- improved raid patch (H.J. Lu).

* Wed Apr 14 1999 Michael K. Johnson <johnsonm@redhat.com>
- added patch for smartraid controllers

* Sat Apr 10 1999 Cristian Gafton <gafton@redhat.com>
- fix logging problems caused by setproctitle and PAM interaction
  (#2045)

* Wed Mar 31 1999 Jeff Johnson <jbj@redhat.com>
- include docs and examples for sfdisk (#1164)

* Mon Mar 29 1999 Matt Wilson <msw@redhat.com>
- rtc is not working properly on alpha, we can't use hwclock yet.

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- add patch to make mkswap more 64 bit friendly... Patch from
  eranian@hpl.hp.com (ahem!)

* Thu Mar 25 1999 Jeff Johnson <jbj@redhat.com>
- include sfdisk (#1164)
- fix write (#1784)
- use positive logic in spec file (ifarch rather than ifnarch).
- (re)-use 1st matching utmp slot if search by mypid not found.
- update to 2.9o
- lastb wants bad logins in wtmp clone /var/run/btmp (#884)

* Thu Mar 25 1999 Jakub Jelinek <jj@ultra.linux.cz>
- if hwclock is to be compiled on sparc,
  it must actually work. Also, it should obsolete
  clock, otherwise it clashes.
- limit the swap size in mkswap for 2.2.1+ kernels
  by the actual maximum size kernel can handle.
- fix kbdrate on sparc, patch by J. S. Connell
  <ankh@canuck.gen.nz>

* Wed Mar 24 1999 Matt Wilson <msw@redhat.com>
- added pam_console back into pam.d/login

* Tue Mar 23 1999 Matt Wilson <msw@redhat.com>
- updated to 2.9i
- added hwclock for sparcs and alpha

* Mon Mar 22 1999 Erik Troan <ewt@redhat.com>
- added vigr to file list

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- remove most of the ifnarch arm stuff

* Mon Mar 15 1999 Michael Johnson <johnsonm@redhat.com>
- added pam_console.so to /etc/pam.d/login

* Thu Feb  4 1999 Michael K. Johnson <johnsonm@redhat.com>
- .perms patch to login to make it retain root in parent process
  for pam_close_session to work correctly

* Tue Jan 12 1999 Jeff Johnson <jbj@redhat.com>
- strip fdisk in buildroot correctly (#718)

* Mon Jan 11 1999 Cristian Gafton <gafton@redhat.com>
- have fdisk compiled on sparc and arm

* Mon Jan 11 1999 Erik Troan <ewt@redhat.com>
- added beos partition type to fdisk

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- incorporate fdisk on all arches

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- restore PAM functionality at end of login (Bug #201)

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch top build on the arm without PAM and related utilities, for now.
- build hwclock only on intel

* Wed Nov 18 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to version 2.9

* Thu Oct 29 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide (slang-1.2.2)
- patch kbdrate wackiness so it builds with egcs

* Tue Oct 13 1998 Erik Troan <ewt@redhat.com>
- patched more to use termcap

* Mon Oct 12 1998 Erik Troan <ewt@redhat.com>
- added warning about alpha/bsd label starting cylinder

* Mon Sep 21 1998 Erik Troan <ewt@redhat.com>
- use sigsetjmp/siglongjmp in more rather then sig'less versions

* Fri Sep 11 1998 Jeff Johnson <jbj@redhat.com>
- explicit attrs for setuid/setgid programs

* Thu Aug 27 1998 Cristian Gafton <gafton@redhat.com>
- sln is now included in glibc

* Sun Aug 23 1998 Jeff Johnson <jbj@redhat.com>
- add cbm1581 floppy definitions (problem #787)

* Mon Jun 29 1998 Jeff Johnson <jbj@redhat.com>
- remove /etc/nologin at end of shutdown/halt.

* Fri Jun 19 1998 Jeff Johnson <jbj@redhat.com>
- add mount/losetup.

* Thu Jun 18 1998 Jeff Johnson <jbj@redhat.com>
- update to 2.8 with 2.8b clean up. hostid now defunct?

* Mon Jun 01 1998 David S. Miller <davem@dm.cobaltmicro.com>
- "more" now works properly on sparc

* Sat May 02 1998 Jeff Johnson <jbj@redhat.com>
- Fix "fdisk -l" fault on mounted cdrom. (prob #513)

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 11 1998 Cristian Gafton <gafton@redhat.com>
- manhattan rebuild

* Mon Dec 29 1997 Erik Troan <ewt@redhat.com>
- more didn't suspend properly on glibc
- use proper tc*() calls rather then ioctl's

* Sun Dec 21 1997 Cristian Gafton <gafton@redhat.com>
- fixed a security problem in chfn and chsh accepting too 
  long gecos fields

* Fri Dec 19 1997 Mike Wangsmo <wanger@redhat.com>
- removed "." from default path

* Tue Dec 02 1997 Cristian Gafton <gafton@redhat.com>
- added (again) the vipw patch

* Wed Oct 22 1997 Michael Fulbright <msf@redhat.com>
- minor cleanups for glibc 2.1

* Fri Oct 17 1997 Michael Fulbright <msf@redhat.com>
- added vfat32 filesystem type to list recognized by fdisk

* Fri Oct 10 1997 Erik Troan <ewt@redhat.com>
- don't build clock on the alpha 
- don't install chkdupexe

* Thu Oct 02 1997 Michael K. Johnson <johnsonm@redhat.com>
- Update to new pam standard.
- BuildRoot.

* Thu Sep 25 1997 Cristian Gafton <gafton@redhat.com>
- added rootok and setproctitle patches
- updated pam config files for chfn and chsh

* Tue Sep 02 1997 Erik Troan <ewt@redhat.com>
- updated MCONFIG to automatically determine the architecture
- added glibc header hacks to fdisk code
- rdev is only available on the intel

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- update to util-linux 2.7, fixed login problems

* Wed Jun 25 1997 Erik Troan <ewt@redhat.com>
- Merged Red Hat changes into main util-linux source, updated package to
  development util-linux (nearly 2.7).

* Tue Apr 22 1997 Michael K. Johnson <johnsonm@redhat.com>
- LOG_AUTH --> LOG_AUTHPRIV in login and shutdown

* Mon Mar 03 1997 Michael K. Johnson <johnsonm@redhat.com>
- Moved to new pam and from pam.conf to pam.d

* Tue Feb 25 1997 Michael K. Johnson <johnsonm@redhat.com>
- pam.patch differentiated between different kinds of bad logins.
  In particular, "user does not exist" and "bad password" were treated
  differently.  This was a minor security hole.

## END: Generated by rpmautospec
