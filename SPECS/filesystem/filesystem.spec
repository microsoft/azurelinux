Summary:      Default file system
Name:         filesystem
Version:      1.1
Release:      19%{?dist}
License:      GPLv3
Group:        System Environment/Base
Vendor:       Microsoft Corporation
URL:          http://www.linuxfromscratch.org
Distribution: Mariner

%description
The filesystem package is one of the basic packages that is installed
on a Linux system. Filesystem contains the basic directory
layout for a Linux operating system, including the correct permissions
for the directories. This version is for a system configured with systemd.

%package asc
Summary:        Provide with config files needed for Azure Security Baseline
Requires:       %{name} = %{version}-%{release}

%description    asc
Provide with multiple configuration files in /etc/modprobe.d/ to meet Azure Security Baseline

%prep
%build
%install
#
#	6.5.  Creating Directories
#
install -vdm 755 %{buildroot}/{dev,run/{media/{floppy,cdrom},lock}}
install -vdm 755 %{buildroot}/{etc/{opt,sysconfig},home,mnt}
install -vdm 700 %{buildroot}/boot
install -vdm 755 %{buildroot}/{var}
install -vdm 755 %{buildroot}/opt
install -vdm 755 %{buildroot}/media
install -dv -m 0750 %{buildroot}/root
install -dv -m 1777 %{buildroot}/tmp %{buildroot}/var/tmp
install -vdm 755 %{buildroot}/usr/{,local/}{bin,include,lib,sbin,src}
install -vdm 755 %{buildroot}/usr/{,local/}share/{color,dict,doc,info,locale,man}
install -vdm 755 %{buildroot}/usr/{,local/}share/{misc,terminfo,zoneinfo}
install -vdm 755 %{buildroot}/usr/libexec
install -vdm 755 %{buildroot}/usr/{,local/}share/man/man{1..8}
install -vdm 755 %{buildroot}/etc/profile.d
install -vdm 755 %{buildroot}/usr/lib/debug/{lib,bin,sbin,usr,.dwz}

ln -svfn usr/lib %{buildroot}/lib
ln -svfn usr/bin %{buildroot}/bin
ln -svfn usr/sbin %{buildroot}/sbin

ln -svfn ../bin %{buildroot}/usr/lib/debug/usr/bin
ln -svfn ../sbin %{buildroot}/usr/lib/debug/usr/sbin
ln -svfn ../lib %{buildroot}/usr/lib/debug/usr/lib

	ln -svfn usr/lib %{buildroot}/lib64
	ln -svfn lib %{buildroot}/usr/lib64
	ln -svfn lib %{buildroot}/usr/local/lib64
        ln -svfn lib %{buildroot}/usr/lib/debug/lib64
        ln -svfn ../lib %{buildroot}/usr/lib/debug/usr/lib64
        ln -svfn ../.dwz %{buildroot}/usr/lib/debug/usr/.dwz

install -vdm 755 %{buildroot}/var/{log,mail,spool,mnt,srv}

ln -svfn var/srv %{buildroot}/srv
ln -svfn ../run %{buildroot}/var/run
ln -svfn ../run/lock %{buildroot}/var/lock
install -vdm 755 %{buildroot}/var/{opt,cache,lib/{color,misc,locate},local}
install -vdm 755 %{buildroot}/mnt/cdrom
install -vdm 755 %{buildroot}/mnt/hgfs

#
#	6.6. Creating Essential Files and Symlinks
#
ln -svfn /proc/self/mounts %{buildroot}/etc/mtab
#touch -f %{buildroot}/etc/mtab

touch %{buildroot}/var/log/{btmp,lastlog,wtmp}
#
#	Configuration files
#
cat > %{buildroot}/etc/passwd <<- "EOF"
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/dev/null:/bin/false
daemon:x:6:6:Daemon User:/dev/null:/bin/false
messagebus:x:18:18:D-Bus Message Daemon User:/var/run/dbus:/bin/false
systemd-bus-proxy:x:72:72:systemd Bus Proxy:/:/bin/false
systemd-journal-gateway:x:73:73:systemd Journal Gateway:/:/bin/false
systemd-journal-remote:x:74:74:systemd Journal Remote:/:/bin/false
systemd-journal-upload:x:75:75:systemd Journal Upload:/:/bin/false
systemd-network:x:76:76:systemd Network Management:/:/bin/false
systemd-resolve:x:77:77:systemd Resolver:/:/bin/false
systemd-timesync:x:78:78:systemd Time Synchronization:/:/bin/false
systemd-coredump:x:79:79:systemd Core Dumper:/:/usr/bin/false
systemd-oom:x:80:80:systemd Userspace OOM Killer:/:/usr/bin/false
nobody:x:65534:65533:Unprivileged User:/dev/null:/bin/false
EOF
cat > %{buildroot}/etc/group <<- "EOF"
root:x:0:
bin:x:1:daemon
sys:x:2:
kmem:x:3:
tape:x:4:
tty:x:5:
daemon:x:6:
floppy:x:7:
disk:x:8:
lp:x:9:
dialout:x:10:
audio:x:11:
video:x:12:
utmp:x:13:
usb:x:14:
cdrom:x:15:
adm:x:16:
messagebus:x:18:
systemd-journal:x:23:
input:x:24:
mail:x:34:
lock:x:54:
dip:x:30:
render:x:31:
kvm:x:32:
systemd-bus-proxy:x:72:
systemd-journal-gateway:x:73:
systemd-journal-remote:x:74:
systemd-journal-upload:x:75:
systemd-network:x:76:
systemd-resolve:x:77:
systemd-timesync:x:78:
systemd-coredump:x:79:
systemd-oom:x:80:
nogroup:x:65533:
users:x:100:
sudo:x:27:
wheel:x:28:
EOF
#
#   Creating Proxy Configuration"
#
cat > %{buildroot}/etc/sysconfig/proxy <<- "EOF"
# Enable a generation of the proxy settings to the profile.
# This setting allows to turn the proxy on and off while
# preserving the particular proxy setup.
#
PROXY_ENABLED="no"

# Some programs (e.g. wget) support proxies, if set in
# the environment.
# Example: HTTP_PROXY="http://proxy.provider.de:3128/"
HTTP_PROXY=""

# Example: HTTPS_PROXY="https://proxy.provider.de:3128/"
HTTPS_PROXY=""

# Example: FTP_PROXY="http://proxy.provider.de:3128/"
FTP_PROXY=""

# Example: GOPHER_PROXY="http://proxy.provider.de:3128/"
GOPHER_PROXY=""

# Example: SOCKS_PROXY="socks://proxy.example.com:8080"
SOCKS_PROXY=""

# Example: SOCKS5_SERVER="office-proxy.example.com:8881"
SOCKS5_SERVER=""

# Example: NO_PROXY="www.me.de, do.main, localhost"
NO_PROXY="localhost, 127.0.0.1"
EOF
#
#	7.3. Customizing the /etc/hosts File"
#
cat > %{buildroot}/etc/hosts <<- "EOF"
# Begin /etc/hosts (network card version)

::1         ipv6-localhost ipv6-loopback
127.0.0.1   localhost.localdomain
127.0.0.1   localhost

# End /etc/hosts (network card version)
EOF
# and /etc/host.conf file
echo "multi on" > %{buildroot}/etc/host.conf
#
#	7.9. Configuring the setclock Script"
#
cat > %{buildroot}/etc/sysconfig/clock <<- "EOF"
# Begin /etc/sysconfig/clock

UTC=1

# Set this to any options you might need to give to hwclock,
# such as machine hardware clock type for Alphas.
CLOCKPARAMS=

# End /etc/sysconfig/clock
EOF
#
#	7.10. Configuring the Linux Console"
#
cat > %{buildroot}/etc/sysconfig/console <<- "EOF"
# Begin /etc/sysconfig/console
#       Begin /etc/sysconfig/console
#       KEYMAP="us"
#       FONT="lat1-16 -m utf8"
#       FONT="lat1-16 -m 8859-1"
#       KEYMAP_CORRECTIONS="euro2"
#       UNICODE="1"
#       LEGACY_CHARSET="iso-8859-1"
# End /etc/sysconfig/console
EOF
#
#	7.13. The Bash Shell Startup Files
#
cat > %{buildroot}/etc/profile <<- "EOF"
# Begin /etc/profile
# Written for Beyond Linux From Scratch
# by James Robertson <jameswrobertson@earthlink.net>
# modifications by Dagmar d'Surreal <rivyqntzne@pbzpnfg.arg>

# System wide environment variables and startup programs.

# System wide aliases and functions should go in /etc/bashrc.  Personal
# environment variables and startup programs should go into
# ~/.bash_profile.  Personal aliases and functions should go into
# ~/.bashrc.

# Functions to help us manage paths.  Second argument is the name of the
# path variable to be modified (default: PATH)
pathremove () {
        local IFS=':'
        local NEWPATH
        local DIR
        local PATHVARIABLE=${2:-PATH}
        for DIR in ${!PATHVARIABLE} ; do
                if [ "$DIR" != "$1" ] ; then
                  NEWPATH=${NEWPATH:+$NEWPATH:}$DIR
                fi
        done
        export $PATHVARIABLE="$NEWPATH"
}

pathprepend () {
        pathremove $1 $2
        local PATHVARIABLE=${2:-PATH}
        export $PATHVARIABLE="$1${!PATHVARIABLE:+:${!PATHVARIABLE}}"
}

pathappend () {
        pathremove $1 $2
        local PATHVARIABLE=${2:-PATH}
        export $PATHVARIABLE="${!PATHVARIABLE:+${!PATHVARIABLE}:}$1"
}

export -f pathremove pathprepend pathappend

# Set the initial path
# Block unnessary as this is set elsewhere.
# export PATH=$PATH:/bin:/usr/bin

# if [ $EUID -eq 0 ] ; then
#         pathappend /sbin:/usr/sbin
#         unset HISTFILE
# fi

# Setup some environment variables.
export HISTSIZE=1000
export HISTIGNORE="&:[bf]g:exit"

# Set some defaults for graphical systems
export XDG_DATA_DIRS=/usr/share/
export XDG_CONFIG_DIRS=/etc/xdg/

# Setup a red prompt for root and a green one for users.
NORMAL="\[\e[0m\]"
RED="\[\e[1;31m\]"
GREEN="\[\e[1;32m\]"
if [[ $EUID == 0 ]] ; then
  PS1="$RED\u@\h [ $NORMAL\w$RED ]# $NORMAL"
else
  PS1="$GREEN\u@\h [ $NORMAL\w$GREEN ]\$ $NORMAL"
fi

for script in /etc/profile.d/*.sh ; do
        if [ -r $script ] ; then
                . $script
        fi
done

unset script RED GREEN NORMAL
umask 027
# End /etc/profile
EOF
#
#   The Proxy Bash Shell Startup File
#
cat > %{buildroot}/etc/profile.d/proxy.sh <<- "EOF"
#
# proxy.sh:              Set proxy environment
#

sys=/etc/sysconfig/proxy
test -s $sys || exit 0
while read line ; do
    case "$line" in
    \#*|"") continue ;;
    esac
    eval val=${line#*=}
    case "$line" in
    PROXY_ENABLED=*)
        PROXY_ENABLED="${val}"
        ;;
    HTTP_PROXY=*)
        test "$PROXY_ENABLED" = "yes" || continue
        http_proxy="${val}"
        export http_proxy
        ;;
    HTTPS_PROXY=*)
        test "$PROXY_ENABLED" = "yes" || continue
        https_proxy="${val}"
        export https_proxy
        ;;
    FTP_PROXY=*)
        test "$PROXY_ENABLED" = "yes" || continue
        ftp_proxy="${val}"
        export ftp_proxy
        ;;
    GOPHER_PROXY=*)
        test "$PROXY_ENABLED" = "yes" || continue
        gopher_proxy="${val}"
        export gopher_proxy
        ;;
    SOCKS_PROXY=*)
        test "$PROXY_ENABLED" = "yes" || continue
        socks_proxy="${val}"
        export socks_proxy
        SOCKS_PROXY="${val}"
        export SOCKS_PROXY
        ;;
    SOCKS5_SERVER=*)
        test "$PROXY_ENABLED" = "yes" || continue
        SOCKS5_SERVER="${val}"
        export SOCKS5_SERVER
        ;;
    NO_PROXY=*)
        test "$PROXY_ENABLED" = "yes" || continue
        no_proxy="${val}"
        export no_proxy
        NO_PROXY="${val}"
        export NO_PROXY
    esac
done < $sys
unset sys line val

if test "$PROXY_ENABLED" != "yes" ; then
    unset http_proxy https_proxy ftp_proxy gopher_proxy no_proxy NO_PROXY socks_proxy SOCKS_PROXY SOCKS5_SERVER
fi
unset PROXY_ENABLED
#
# end of proxy.sh
EOF
#
#	7.14. Creating the /etc/inputrc File
#
cat > %{buildroot}/etc/inputrc <<- "EOF"
# Begin /etc/inputrc
# Modified by Chris Lynn <roryo@roryo.dynup.net>

# Allow the command prompt to wrap to the next line
set horizontal-scroll-mode Off

# Enable 8bit input
set meta-flag On
set input-meta On

# Turns off 8th bit stripping
set convert-meta Off

# Keep the 8th bit for display
set output-meta On

# none, visible or audible
set bell-style none

# All of the following map the escape sequence of the value
# contained in the 1st argument to the readline specific functions
"\eOd": backward-word
"\eOc": forward-word

# for linux console
"\e[1~": beginning-of-line
"\e[4~": end-of-line
# page up - history search backward
"\e[5~": history-search-backward
# page down - history search forward
"\e[6~": history-search-forward
"\e[3~": delete-char
"\e[2~": quoted-insert

# for xterm
"\eOH": beginning-of-line
"\eOF": end-of-line

# for Konsole
"\e[H": beginning-of-line
"\e[F": end-of-line

# ctrl + left/right arrow to jump words
"\e[1;5C": forward-word
"\e[1;5D": backward-word

# End /etc/inputrc
EOF
#
#	8.2. Creating the /etc/fstab File
#
touch %{buildroot}/etc/fstab

#
#	8.3.2. Configuring Linux Module Load Order
#
install -vdm 755 %{buildroot}/etc/modprobe.d
cat > %{buildroot}/etc/modprobe.d/usb.conf <<- "EOF"
# Begin /etc/modprobe.d/usb.conf

install ohci_hcd /sbin/modprobe ehci_hcd ; /sbin/modprobe -i ohci_hcd ; true
install uhci_hcd /sbin/modprobe ehci_hcd ; /sbin/modprobe -i uhci_hcd ; true

# End /etc/modprobe.d/usb.conf
EOF

# Security patch for CCE-14118-4, msid: 6.6 
# Disable the installation and use of file systems that are not required (squashfs)
cat > %{buildroot}/etc/modprobe.d/squashfs.conf <<- "EOF"
# Begin /etc/modprobe.d/squashfs.conf

install squashfs /bin/true

# End /etc/modprobe.d/squashfs.conf
EOF

# Security patch for msid: 1.1.21.1 
# Ensure mounting of USB storage devices is disabled
cat > %{buildroot}/etc/modprobe.d/usb-storage.conf <<- "EOF"
# Begin /etc/modprobe.d/usb-storage.conf

install usb-storage /bin/true

# End /etc/modprobe.d/usb-storage.conf
EOF

# Security patch for msid: 6.1 
# Disable the installation and use of file systems that are not required (cramfs)
cat > %{buildroot}/etc/modprobe.d/cramfs.conf <<- "EOF"
# Begin /etc/modprobe.d/cramfs.conf

install cramfs /bin/true

# End /etc/modprobe.d/cramfs.conf
EOF

# Security patch for msid: 6.2 
# Disable the installation and use of file systems that are not required (freevxfs)
cat > %{buildroot}/etc/modprobe.d/freevxfs.conf <<- "EOF"
# Begin /etc/modprobe.d/freevxfs.conf

install freevxfs /bin/true

# End /etc/modprobe.d/freevxfs.conf
EOF

# Security patch for msid: 6.3 
# Disable the installation and use of file systems that are not required (hfs)
cat > %{buildroot}/etc/modprobe.d/hfs.conf <<- "EOF"
# Begin /etc/modprobe.d/hfs.conf

install hfs /bin/true

# End /etc/modprobe.d/hfs.conf
EOF

# Security patch for msid: 6.4 
# Disable the installation and use of file systems that are not required (hfsplus)
cat > %{buildroot}/etc/modprobe.d/hfsplus.conf <<- "EOF"
# Begin /etc/modprobe.d/hfsplus.conf

install hfsplus /bin/true

# End /etc/modprobe.d/hfsplus.conf
EOF

# Security patch for msid: 6.5 
# Disable the installation and use of file systems that are not required (jffs2)
cat > %{buildroot}/etc/modprobe.d/jffs2.conf <<- "EOF"
# Begin /etc/modprobe.d/jffs2.conf

install jffs2 /bin/true

# End /etc/modprobe.d/jffs2.conf
EOF

# Security patch for msid: 54
# Ensure DCCP is disabled
cat > %{buildroot}/etc/modprobe.d/dccp.conf <<- "EOF"
# Begin /etc/modprobe.d/dccp.conf

install dccp /bin/true

# End /etc/modprobe.d/dccp.conf
EOF

# Security patch for msid: 55
# Ensure SCTP is disabled
cat > %{buildroot}/etc/modprobe.d/sctp.conf <<- "EOF"
# Begin /etc/modprobe.d/sctp.conf

install sctp /bin/true

# End /etc/modprobe.d/sctp.conf
EOF

# Security patch for msid: 56
# Disable support for RDS
cat > %{buildroot}/etc/modprobe.d/rds.conf <<- "EOF"
# Begin /etc/modprobe.d/rds.conf

install rds /bin/true

# End /etc/modprobe.d/rds.conf
EOF

# Security patch for msid: 57
# Ensure TIPC is disabled
cat > %{buildroot}/etc/modprobe.d/tipc.conf <<- "EOF"
# Begin /etc/modprobe.d/tipc.conf

install tipc /bin/true

# End /etc/modprobe.d/tipc.conf
EOF
#
#		chapter 9.1. The End
#

# Since these following symlinks are ghosted entries, create them manually upon
# package installation.

# Use Lua to achieve this since when filesystem installs, there may not be any
# other packages installed if this is a new environment.
%post -p <lua>
posix.symlink("lib", "/usr/lib/debug/lib64")
posix.symlink("../bin", "/usr/lib/debug/usr/bin")
posix.symlink("../sbin", "/usr/lib/debug/usr/sbin")
posix.symlink("../lib", "/usr/lib/debug/usr/lib")
posix.symlink("../lib", "/usr/lib/debug/usr/lib64")
posix.symlink("../.dwz", "/usr/lib/debug/usr/.dwz")
return 0

%pretrans -p <lua>
posix.mkdir("/proc")
posix.mkdir("/sys")
posix.chmod("/proc", 0555)
posix.chmod("/sys", 0555)

-- Prior to filesystem-1.1-16, /media used to be a symlink to /run/media but this was
-- replaced with a directory. The RPM upgrade operation generally worked when the /media
-- symlink is a dangling link, which is commonly the case, however not always the case.
--
-- And when the /media symlink is indeed properly pointing to a real /run/media, RPM has a
-- known limitation where it is not possible to replace an active symlink with a directory,
-- and thus the RPM transation fails.
--
-- To workaround this, a %pretrans scriptlet must run to test and remove the symlink
-- before RPM attempts to install the new directory.
--
-- https://docs.fedoraproject.org/en-US/packaging-guidelines/Directory_Replacement
path = "/media"
st = posix.stat(path)
if st and st.type == "link" then
  os.remove(path)
end
return 0

%files
%defattr(-,root,root)
#	Root filesystem
/bin
%dir /boot
%dir /dev
%dir /etc
%dir /home
/lib
%dir /opt

/media
%dir /mnt
%ghost %attr(555,root,root) /proc
%dir /root
%dir /run
/sbin
/srv
%ghost %attr(555,root,root) /sys
%dir /tmp
%dir /usr
%dir /var
#	etc fileystem
%dir /etc/opt
%config(noreplace) /etc/fstab
%config(noreplace) /etc/group
%config(noreplace) /etc/hosts
%config(noreplace) /etc/host.conf
%config(noreplace) /etc/inputrc
%config(noreplace) /etc/mtab
%config(noreplace) /etc/passwd
%config(noreplace) /etc/profile
%dir /etc/modprobe.d
%config(noreplace) /etc/modprobe.d/usb.conf
%dir /etc/sysconfig
%config(noreplace) /etc/sysconfig/clock
%config(noreplace) /etc/sysconfig/console
%config(noreplace) /etc/sysconfig/proxy
%dir /etc/profile.d
%config(noreplace) /etc/profile.d/proxy.sh
#	media filesystem
%dir /run/media/cdrom
%dir /run/media/floppy
#	run filesystem
%dir /run/lock
#	usr filesystem
%dir /mnt/cdrom
%dir /mnt/hgfs
%dir /usr/bin
%dir /usr/include
%dir /usr/lib
%dir /usr/lib/debug
%dir /usr/lib/debug/bin
%dir /usr/lib/debug/lib
%dir /usr/lib/debug/sbin
%dir /usr/lib/debug/usr
%dir /usr/lib/debug/.dwz
%dir /usr/libexec
%dir /usr/local
%dir /usr/local/bin
%dir /usr/local/include
%dir /usr/local/lib
%dir /usr/local/sbin
%dir /usr/local/share
%dir /usr/local/share/color
%dir /usr/local/share/dict
%dir /usr/local/share/doc
%dir /usr/local/share/info
%dir /usr/local/share/locale
%dir /usr/local/share/man
%dir /usr/local/share/man/man1
%dir /usr/local/share/man/man2
%dir /usr/local/share/man/man3
%dir /usr/local/share/man/man4
%dir /usr/local/share/man/man5
%dir /usr/local/share/man/man6
%dir /usr/local/share/man/man7
%dir /usr/local/share/man/man8
%dir /usr/local/share/misc
%dir /usr/local/share/terminfo
%dir /usr/local/share/zoneinfo
%dir /usr/local/src
%dir /usr/sbin
%dir /usr/share
%dir /usr/share/color
%dir /usr/share/dict
%dir /usr/share/doc
%dir /usr/share/info
%dir /usr/share/locale
%dir /usr/share/man
%dir /usr/share/man/man1
%dir /usr/share/man/man2
%dir /usr/share/man/man3
%dir /usr/share/man/man4
%dir /usr/share/man/man5
%dir /usr/share/man/man6
%dir /usr/share/man/man7
%dir /usr/share/man/man8
%dir /usr/share/misc
%dir /usr/share/terminfo
%dir /usr/share/zoneinfo
%dir /usr/src

# 	ghosted /usr/lib/debug symlinks.
#
#   Ghost them to allow others packages to create/provide files
#   inside the symlinks without conflicting with this package. 
%ghost /usr/lib/debug/lib64
%ghost /usr/lib/debug/usr/bin
%ghost /usr/lib/debug/usr/lib
%ghost /usr/lib/debug/usr/lib64
%ghost /usr/lib/debug/usr/sbin
%ghost /usr/lib/debug/usr/.dwz

#	var filesystem
%dir /var/cache
%dir /var/lib
%dir /var/lib/color
%dir /var/lib/locate
%dir /var/lib/misc
%dir /var/local
%dir /var/log
%dir /var/mail
%dir /var/mnt
%dir /var/srv
%dir /var/opt
%dir /var/spool
%dir /var/tmp
%attr(-,root,root) 	/var/log/wtmp
%attr(664,root,utmp)	/var/log/lastlog
%attr(600,root,root)	/var/log/btmp
/var/lock
/var/run

/lib64
/usr/lib64
/usr/local/lib64

%files asc
%config(noreplace) /etc/modprobe.d/squashfs.conf
%config(noreplace) /etc/modprobe.d/usb-storage.conf
%config(noreplace) /etc/modprobe.d/cramfs.conf
%config(noreplace) /etc/modprobe.d/freevxfs.conf
%config(noreplace) /etc/modprobe.d/hfs.conf
%config(noreplace) /etc/modprobe.d/hfsplus.conf
%config(noreplace) /etc/modprobe.d/jffs2.conf
%config(noreplace) /etc/modprobe.d/dccp.conf
%config(noreplace) /etc/modprobe.d/sctp.conf
%config(noreplace) /etc/modprobe.d/rds.conf
%config(noreplace) /etc/modprobe.d/tipc.conf

%changelog
* Fri Dec 08 2023 Chris Co <chrco@microsoft.com> - 1.1-19
- Add scriptlet to handle /media symlink failed upgrade issue

* Thu Dec 07 2023 Dan Streetman <ddstreet@ieee.org> - 1.1-18
- Add /etc/host.conf with multi enabled

* Thu Oct 12 2023 Chris PeBenito <chpebeni@microsoft.com> - 1.1-17
- Restore the /opt directory.

* Mon Oct 09 2023 Chris Co <chrco@microsoft.com> - 1.1-16
- Make /media a proper directory

* Thu Jun 29 2023 Tobias Brick <tobiasb@microsoft.com> - 1.1-15
- Revert: Remove setting umask from /etc/profile and add it to a separate file in /etc/profile.d

* Tue Jun 13 2023 Andy Zaugg <azaugg@linkedin.com> - 1.1-14
- Adding /usr/local/sbin as per FHS

* Thu May 18 2023 Tobias Brick <tobiasb@microsoft.com> - 1.1-13
- Remove setting umask from /etc/profile and add it to a separate file in /etc/profile.d

* Thu Sep 14 2022 Thara Gopinath <tgopinath@microsoft.com> - 1.1-12
- Add the 'systemd-coredump' and 'systemd-oom' user and group accounts.

* Mon Jul 18 2022 Minghe Ren <mingheren@microsoft.com> - 1.1-11
- Update etc/modprobe.d/ folder to include new multiple config files and improve security
- Add subpackage asc to include all the new config files

* Thu Jun 16 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.1-10
- Mark /proc and /sys as %%ghost
- Create /proc and /sys as a pretransaction step

*   Wed May 18 2022 Brendan Kerrigan <bkerrigan@microsoft.com> 1.1-9
-   Update /etc/inputrc to enable Ctrl+LeftArrow and Ctrl+RightArrow word jumping binds.
-   License Verified.
*   Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 1.1-8
-   Add folders and symlinks for .dwz files.
*   Mon Jun 15 2020 Joe Schmitt <joschmit@microsoft.com> 1.1-7
-   Use ghost directive for /usr/lib/debug/* symlinks to avoid conflicting with debuginfo packages.
*   Wed May 20 2020 Emre Girgin <mrgirgin@microsoft.com> 1.1-6
-   Change /boot directory permissions to 600.
*   Wed May 20 2020 Joe Schmitt <joschmit@microsoft.com> 1.1-5
-   Add render and kvm group by default.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.1-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed May 8 2019 Alexey Makhalov <amakhalov@vmware.com> 1.1-3
-   Set 'x' as a root password placeholder
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.1-2
-   Aarch64 support
*   Fri Sep 15 2017 Anish Swaminathan <anishs@vmware.com>  1.1-1
-   Move network file from filesystem package
*   Fri Apr 21 2017 Alexey Makhalov <amakhalov@vmware.com> 1.0-13
-   make /var/run symlink to /run and keep it in rpm
*   Thu Apr 20 2017 Bo Gan <ganb@vmware.com> 1.0-12
-   Fix /usr/local/lib64 symlink
*   Wed Mar 08 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.0-11
-   Create default DHCP net config in 99-dhcp-en.network instead of 10-dhcp-en.network
*   Wed Aug 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0-10
-   /etc/inputrc PgUp/PgDown for history search
*   Tue Jul 12 2016 Divya Thaluru <dthaluru@vmware.com> 1.0-9
-   Added filesystem for debug libraries and binaries
*   Fri Jul 8 2016 Divya Thaluru <dthaluru@vmware.com> 1.0-8
-   Removing multiple entries of localhost in /etc/hosts file
*   Fri May 27 2016 Divya Thaluru <dthaluru@vmware.com> 1.0-7
-   Fixed nobody user uid and group gid
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-6
-   GA - Bump release of all rpms
*   Wed May 4 2016 Divya Thaluru <dthaluru@vmware.com> 1.0-5
-   Removing non-existent users from /etc/group file
*   Fri Apr 29 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 1.0-4
-   Updating the /etc/hosts file
*   Fri Apr 22 2016 Divya Thaluru <dthaluru@vmware.com> 1.0-3
-   Setting default umask value to 027
*   Thu Apr 21 2016 Anish Swaminathan <anishs@vmware.com> 1.0-2
-   Version update for network file change
*   Mon Jan 18 2016 Anish Swaminathan <anishs@vmware.com> 1.0-1
-   Reset version to match with Photon version
*   Wed Jan 13 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 7.5-13
-   Support to set proxy configuration file - SLES proxy configuration implementation.
*   Thu Jan 7 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 7.5-12
-   Removing /etc/sysconfig/network file.
*   Mon Nov 16 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 7.5-11
-   Removing /etc/fstab mount entries.
*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 7.5-10
-   Removint /opt from filesystem.
*   Fri Oct 02 2015 Vinay Kulkarni <kulkarniv@vmware.com> 7.5-9
-   Dump build-number and release version from macros.
*   Fri Aug 14 2015 Sharath George <sharathg@vmware.com> 7.5-8
-   upgrading release to TP2
*   Tue Jun 30 2015 Alexey Makhalov <amakhalov@vmware.com> 7.5-7
-   /etc/profile.d permission fix
*   Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 7.5-6
-   Adding group dip
*   Mon Jun 22 2015 Divya Thaluru <dthaluru@vmware.com> 7.5-5
-   Fixing lsb-release file
*   Tue Jun 16 2015 Alexey Makhalov <amakhalov@vmware.com> 7.5-4
-   Change users group id to 100.
-   Add audio group to users group.
*   Mon Jun 15 2015 Sharath George <sharathg@vmware.com> 7.5-3
-   Change the network match for dhcp.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 7.5-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 7.5-1
-   Initial build. First version
