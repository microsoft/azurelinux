#!/tools/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

#
# Initial filesystem setup in chroot
#

set -x

# Create standard directory tree in chroot

# 7.5. Creating Directories
mkdir -pv /{boot,home,mnt,opt,srv}
mkdir -pv /etc/{opt,sysconfig}
mkdir -pv /lib/firmware
mkdir -pv /media/{floppy,cdrom}
mkdir -pv /usr/{,local/}{include,src}
mkdir -pv /usr/local/{bin,lib,sbin}
mkdir -pv /usr/{,local/}share/{color,dict,doc,info,locale,man}
mkdir -pv /usr/{,local/}share/{misc,terminfo,zoneinfo}
mkdir -pv /usr/{,local/}share/man/man{1..8}
mkdir -pv /var/{cache,local,log,mail,opt,spool}
mkdir -pv /var/lib/{color,misc,locate}
ln -sfv /run /var/run
ln -sfv /run/lock /var/lock
install -dv -m 0750 /root
install -dv -m 1777 /tmp /var/tmp

install -vdm 755 /{dev,proc,run/{media/{floppy,cdrom},lock},sys}
install -vdm 755 /{boot,etc/{opt,sysconfig},home,mnt}
install -vdm 755 /var
install -dv -m 0750 /root
install -dv -m 1777 /tmp /var/tmp
install -vdm 755 /usr/{,local/}{bin,include,lib,sbin,src}
install -vdm 755 /usr/{,local/}share/{color,dict,doc,info,locale,man}
install -vdm 755 /usr/{,local/}share/{misc,terminfo,zoneinfo}
install -vdm 755 /usr/libexec
install -vdm 755 /usr/{,local/}share/man/man{1..8}
install -vdm 755 /etc/profile.d
install -vdm 755 /usr/lib/debug/{lib,bin,sbin,usr}

mkdir -pv /etc/{opt,sysconfig}
mkdir -pv /lib/firmware
mkdir -pv /media/{floppy,cdrom}
mkdir -pv /usr/{,local/}{include,src}
mkdir -pv /usr/local/{bin,lib,sbin}
mkdir -pv /usr/{,local/}share/{color,dict,doc,info,locale,man}
mkdir -pv /usr/{,local/}share/{misc,terminfo,zoneinfo}
mkdir -pv /usr/{,local/}share/man/man{1..8}
mkdir -pv /var/{cache,local,log,mail,opt,spool}
mkdir -pv /var/lib/{color,misc,locate}

ln -sfv /run /var/run
ln -sfv /run/lock /var/lock

install -dv -m 0750 /root
install -dv -m 1777 /tmp /var/tmp


# ????????
# ln -svfn usr/lib /lib
# ln -svfn usr/bin /bin
# ln -svfn usr/sbin /sbin
# ln -svfn run/media /media

# ln -svfn ../bin /usr/lib/debug/usr/bin
# ln -svfn ../sbin /usr/lib/debug/usr/sbin
# ln -svfn ../lib /usr/lib/debug/usr/lib

# ln -svfn usr/lib /lib64
# ln -svfn lib /usr/lib64
# ln -svfn lib /usr/local/lib64
# ln -svfn lib /usr/lib/debug/lib64
# ln -svfn ../lib /usr/lib/debug/usr/lib64
# install -vdm 755 /var/{log,mail,spool,mnt,srv}
# ln -svfn var/srv /srv
# ln -svfn ../run /var/run
# ln -svfn ../run/lock /var/lock
# install -vdm 755 /var/{opt,cache,lib/{color,misc,locate},local}
# install -vdm 755 /mnt/cdrom
# install -vdm 755 /mnt/hgfs

# # Create essential files and links
# # ln -sv /tools/bin/{bash,cat,chmod,dd,echo,ln,mkdir,pwd,rm,stty,touch} /bin
# # ln -sv /tools/bin/{env,install,perl,printf}         /usr/bin
# # ln -sv /tools/lib/libgcc_s.so{,.1}                  /usr/lib
# # ln -sv /tools/lib/libstdc++.{a,so{,.6}}             /usr/lib

# # ????????


ln -sv bash /bin/sh

ls -la /tools/bin
ls -la /tools/lib

# Create mtab
ln -sv /proc/self/mounts /etc/mtab

cat > /etc/hosts << EOF
127.0.0.1  localhost $(hostname)
::1        localhost
EOF

# Create files for root user in chroot
cat > /etc/passwd << "EOF"
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/dev/null:/usr/bin/false
daemon:x:6:6:Daemon User:/dev/null:/usr/bin/false
messagebus:x:18:18:D-Bus Message Daemon User:/run/dbus:/usr/bin/false
uuidd:x:80:80:UUID Generation Daemon User:/dev/null:/usr/bin/false
nobody:x:65534:65534:Unprivileged User:/dev/null:/usr/bin/false
EOF

cat > /etc/group << "EOF"
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
input:x:24:
mail:x:34:
kvm:x:61:
uuidd:x:80:
wheel:x:97:
users:x:999:
nogroup:x:65534:
EOF

touch /var/log/{btmp,lastlog,faillog,wtmp}
chgrp -v utmp /var/log/lastlog
chmod -v 664  /var/log/lastlog
chmod -v 600  /var/log/btmp

# Start a new shell
echo Finished with filesystem initial configuration, need to start a new shell
#exec /tools/bin/bash --login +h
#echo New shell running