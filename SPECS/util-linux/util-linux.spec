## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
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
* Mon Apr 06 2026 azldev <> - 2.41.3-10
- Latest state for util-linux

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
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
