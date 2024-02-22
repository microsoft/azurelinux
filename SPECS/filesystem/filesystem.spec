Summary:      Default file system
Name:         filesystem
Version:      1.1
Release:      20%{?dist}
License:      GPLv3
Group:        System Environment/Base
Vendor:       Microsoft Corporation
URL:          http://www.linuxfromscratch.org
Distribution:   Azure Linux

# We don't order the same as Fedora here, although maybe we should.
# If ordering is changed, be sure to coordinate with setup
# package as well as package that provides system-release
%if ! 0%{?azl}
Requires(pre): setup
%endif

%description
The filesystem package is one of the basic packages that is installed
on a Linux system. Filesystem contains the basic directory
layout for a Linux operating system, including the correct permissions
for the directories. This version is for a system configured with systemd.

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
%dir /etc/sysconfig
%dir /etc/profile.d
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
/var/lock
/var/run

/lib64
/usr/lib64
/usr/local/lib64

%changelog
* Mon Mar 04 2024 Dan Streetman <ddstreet@microsoft.com> - 1.1-20
- move filesystem-asc stuff into asc
- move /etc/modprobe.d into kmod package
- move /etc/mtab from filesystem to util-linux package
- move /var/log/* files from filesystem to systemd package
- remove opensuse-style 'proxy' config file
- remove unused /etc/sysconfig/clock file
- remove unused opensuse-style /etc/sysconfig/console file
- move some files into setup package

* Wed Feb 28 2024 Dan Streetman <ddstreet@microsoft.com> - 1.1-19
- fix /etc/hosts
- add /etc/host.conf to enable multi

* Thu Nov 30 2023 Dan Streetman <ddstreet@ieee.org> - 1.1-18
- Remove umask 027

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
