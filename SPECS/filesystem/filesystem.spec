
Summary: The basic directory layout for a Linux system
Name: filesystem
Version: 3.18
Release: 9%{?dist}
License: LicenseRef-Fedora-Public-Domain
Vendor: Microsoft Corporation
Distribution: Azure Linux
URL: https://pagure.io/filesystem
Source1: https://pagure.io/filesystem/raw/master/f/lang-exceptions
Source2: iso_639.sed
Source3: iso_3166.sed
BuildRequires: iso-codes

# We don't order the same as Fedora here, although maybe we should.
# If ordering is changed, be sure to coordinate with setup
# package as well as package that provides system-release
%if ! 0%{?azl}
Requires(pre): setup
%endif

%description
The filesystem package is one of the basic packages that is installed
on a Linux system. Filesystem contains the basic directory layout
for a Linux operating system, including the correct permissions for
the directories.

%prep
rm -f $RPM_BUILD_DIR/filelist

%build

%install
rm -rf %{buildroot}
mkdir %{buildroot}
install -p -c -m755 %SOURCE2 %{buildroot}/iso_639.sed
install -p -c -m755 %SOURCE3 %{buildroot}/iso_3166.sed

cd %{buildroot}

Paths=(
        afs boot dev \
        etc/{X11/{applnk,fontpath.d,xinit/{xinitrc,xinput}.d},xdg/autostart,opt,pm/{config.d,power.d,sleep.d},skel,sysconfig,keys/ima,pki,bash_completion.d,rwtab.d,statetab.d} \
        home media mnt opt root run srv tmp \
        usr/{bin,games,include,%{_lib}/{bpf,games,X11,pm-utils/{module.d,power.d,sleep.d}},lib/{debug/{.dwz,usr},games,locale,modules,sysimage,systemd/{system,user},sysusers.d,tmpfiles.d},libexec,local/{bin,etc,games,lib,%{_lib}/bpf,sbin,src,share/{applications,man/man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x},info},libexec,include,},sbin,share/{aclocal,appdata,applications,augeas/lenses,backgrounds,bash-completion{,/completions,/helpers},desktop-directories,dict,doc,empty,fish/vendor_completions.d,games,gnome,help,icons,idl,info,licenses,man/man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x,0p,1p,3p},metainfo,mime-info,misc,omf,pixmaps,sounds,themes,xsessions,X11/fonts,wayland-sessions,zsh/site-functions},src,src/kernels,src/debug} \
        var/{adm,empty,ftp,lib/{games,misc,rpm-state},local,log,nis,preserve,spool/{mail,lpd},tmp,db,cache/bpf,opt,games,yp}
)
for i in "${Paths[@]}"; do
    mkdir -p "$i"
done

ln -snf ../var/tmp usr/tmp
ln -snf spool/mail var/mail
ln -snf usr/bin bin
ln -snf usr/sbin sbin
ln -snf usr/lib lib
ln -snf usr/%{_lib} %{_lib}
ln -snf ../run var/run
ln -snf ../run/lock var/lock
ln -snf usr/bin usr/lib/debug/bin
ln -snf usr/lib usr/lib/debug/lib
ln -snf usr/%{_lib} usr/lib/debug/%{_lib}
ln -snf ../.dwz usr/lib/debug/usr/.dwz
ln -snf usr/sbin usr/lib/debug/sbin

sed -n -f %{buildroot}/iso_639.sed /usr/share/xml/iso-codes/iso_639.xml \
  >%{buildroot}/iso_639.tab
sed -n -f %{buildroot}/iso_3166.sed /usr/share/xml/iso-codes/iso_3166.xml \
  >%{buildroot}/iso_3166.tab

grep -v "^$" %{buildroot}/iso_639.tab | grep -v "^#" | while read a b c d ; do
    [[ "$d" =~ "^Reserved" ]] && continue
    [[ "$d" =~ "^No linguistic" ]] && continue

    locale=$c
    if [ "$locale" = "XX" ]; then
        locale=$b
    fi
    echo "%lang(${locale})	/usr/share/locale/${locale}" >> $RPM_BUILD_DIR/filelist
    echo "%lang(${locale}) %ghost %config(missingok) /usr/share/man/${locale}" >>$RPM_BUILD_DIR/filelist
done
cat %{SOURCE1} | grep -v "^#" | grep -v "^$" | while read loc ; do
    locale=$loc
    locality=
    special=
    [[ "$locale" =~ "@" ]] && locale=${locale%%%%@*}
    [[ "$locale" =~ "_" ]] && locality=${locale##*_}
    [[ "$locality" =~ "." ]] && locality=${locality%%%%.*}
    [[ "$loc" =~ "_" ]] || [[ "$loc" =~ "@" ]] || special=$loc

    # If the locality is not official, skip it
    if [ -n "$locality" ]; then
        grep -q "^$locality" %{buildroot}/iso_3166.tab || continue
    fi
    # If the locale is not official and not special, skip it
    if [ -z "$special" ]; then
        egrep -q "[[:space:]]${locale%%_*}[[:space:]]" \
           %{buildroot}/iso_639.tab || continue
    fi
    echo "%lang(${locale})	/usr/share/locale/${loc}" >> $RPM_BUILD_DIR/filelist
    echo "%lang(${locale})  %ghost %config(missingok) /usr/share/man/${loc}" >> $RPM_BUILD_DIR/filelist
done

rm -f %{buildroot}/iso_639.tab
rm -f %{buildroot}/iso_639.sed
rm -f %{buildroot}/iso_3166.tab
rm -f %{buildroot}/iso_3166.sed

cat $RPM_BUILD_DIR/filelist | grep "locale" | while read a b ; do
    mkdir -p -m 755 %{buildroot}/$b/LC_MESSAGES
done

cat $RPM_BUILD_DIR/filelist | grep "/share/man" | while read a b c d; do
    mkdir -p -m 755 %{buildroot}/$d/man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x,0p,1p,3p}
done

for i in man{1,2,3,4,5,6,7,8,9,n,1x,2x,3x,4x,5x,6x,7x,8x,9x,0p,1p,3p}; do
   echo "/usr/share/man/$i" >>$RPM_BUILD_DIR/filelist
done

%pretrans -p <lua>
--# If we are running in pretrans in a fresh root, there is no /usr and
--# symlinks. We cannot be sure, to be the very first rpm in the
--# transaction list. Let's create the needed base directories and symlinks
--# here, to place the files from other packages in the right locations.
--# When our rpm is unpacked by cpio, it will set all permissions and modes
--# later.
posix.mkdir("/usr")
posix.mkdir("/usr/bin")
posix.mkdir("/usr/sbin")
posix.mkdir("/usr/lib")
posix.mkdir("/usr/lib/debug")
posix.mkdir("/usr/lib/debug/usr/")
posix.mkdir("/usr/lib/debug/usr/bin")
posix.mkdir("/usr/lib/debug/usr/sbin")
posix.mkdir("/usr/lib/debug/usr/lib")
posix.mkdir("/usr/lib/debug/usr/%{_lib}")
posix.mkdir("/usr/%{_lib}")
posix.symlink("usr/bin", "/bin")
posix.symlink("usr/sbin", "/sbin")
posix.symlink("usr/lib", "/lib")
posix.symlink("usr/bin", "/usr/lib/debug/bin")
posix.symlink("usr/lib", "/usr/lib/debug/lib")
posix.symlink("usr/%{_lib}", "/usr/lib/debug/%{_lib}")
posix.symlink("../.dwz", "/usr/lib/debug/usr/.dwz")
posix.symlink("usr/sbin", "/usr/lib/debug/sbin")
posix.symlink("usr/%{_lib}", "/%{_lib}")
posix.mkdir("/run")
posix.mkdir("/proc")
posix.mkdir("/sys")
posix.chmod("/proc", 0555)
posix.chmod("/sys", 0555)
st = posix.stat("/media")
if st and st.type == "link" then
  os.remove("/media")
end
posix.mkdir("/var")
posix.symlink("../run", "/var/run")
posix.symlink("../run/lock", "/var/lock")
return 0

%posttrans -p <lua>
--# we need to restorecon on some dirs created in %pretrans or by other packages
if posix.access ("/usr/sbin/restorecon", "x") then
  rpm.execute("/usr/sbin/restorecon", "/var", "/var/run", "/var/lock", "/sys", "/boot", "/dev", "/media", "/afs")
  rpm.execute("/usr/sbin/restorecon", "-r", "/usr/lib/debug")
end


%files -f filelist
%defattr(0755,root,root,0755)
%dir %attr(555,root,root) /
/bin
%attr(555,root,root) /boot
%attr(555,root,root) /afs
/dev
%dir /etc
/etc/X11
/etc/xdg
/etc/opt
/etc/pm
/etc/skel
/etc/sysconfig
/etc/keys
/etc/pki
/etc/bash_completion.d/
%dir /etc/rwtab.d
%dir /etc/statetab.d
/home
/lib
%ifarch x86_64 ppc64 sparc64 s390x aarch64 ppc64le mips64 mips64el riscv64
/%{_lib}
%endif
/media
%dir /mnt
%dir /opt
%ghost %attr(555,root,root) /proc
%attr(550,root,root) /root
/run
/sbin
/srv
%ghost %attr(555,root,root) /sys
%attr(1777,root,root) /tmp
%dir /usr
%attr(555,root,root) /usr/bin
/usr/games
/usr/include
%dir %attr(555,root,root) /usr/lib
%dir /usr/lib/sysimage
%dir /usr/lib/systemd
/usr/lib/systemd/system
/usr/lib/systemd/user
%dir /usr/lib/sysusers.d
%dir /usr/lib/tmpfiles.d
%dir /usr/lib/locale
%dir /usr/lib/modules
%dir /usr/lib/debug
%dir /usr/lib/debug/.dwz
%ghost /usr/lib/debug/bin
%ghost /usr/lib/debug/lib
%ghost /usr/lib/debug/%{_lib}
%ghost %dir /usr/lib/debug/usr
%ghost /usr/lib/debug/usr/bin
%ghost /usr/lib/debug/usr/sbin
%ghost /usr/lib/debug/usr/lib
%ghost /usr/lib/debug/usr/%{_lib}
%ghost /usr/lib/debug/usr/.dwz
%ghost /usr/lib/debug/sbin
%attr(555,root,root) /usr/lib/games
%ifarch x86_64 ppc64 sparc64 s390x aarch64 ppc64le mips64 mips64el riscv64
%attr(555,root,root) /usr/%{_lib}
%else
%attr(555,root,root) /usr/lib/bpf
%attr(555,root,root) /usr/lib/X11
%attr(555,root,root) /usr/lib/pm-utils
%endif
/usr/libexec
/usr/local
%attr(555,root,root) /usr/sbin
%dir /usr/share
/usr/share/aclocal
/usr/share/appdata
/usr/share/applications
/usr/share/augeas
/usr/share/backgrounds
%dir /usr/share/bash-completion
/usr/share/bash-completion/completions
/usr/share/bash-completion/helpers
/usr/share/desktop-directories
/usr/share/dict
/usr/share/doc
%attr(555,root,root) %dir /usr/share/empty
/usr/share/fish
/usr/share/games
/usr/share/gnome
/usr/share/help
/usr/share/icons
/usr/share/idl
/usr/share/info
%dir /usr/share/licenses
%dir /usr/share/locale
%dir /usr/share/man
/usr/share/metainfo
/usr/share/mime-info
/usr/share/misc
/usr/share/omf
/usr/share/pixmaps
/usr/share/sounds
/usr/share/themes
/usr/share/xsessions
%dir /usr/share/X11
/usr/share/X11/fonts
/usr/share/wayland-sessions
/usr/share/zsh
/usr/src
/usr/tmp
%dir /var
/var/adm
%dir /var/cache
/var/cache/bpf
/var/db
/var/empty
/var/ftp
/var/games
/var/lib
/var/local
%ghost /var/lock
/var/log
/var/mail
/var/nis
/var/opt
/var/preserve
%ghost /var/run
%dir /var/spool
%attr(755,root,root) /var/spool/lpd
%attr(775,root,mail) /var/spool/mail
%attr(1777,root,root) /var/tmp
/var/yp

%changelog
* Fri Mar 08 2024 Dan Streetman <ddstreet@microsoft.com> - 3.18-9
- Initial Azure Linux import from Fedora 40 (license: MIT).
- license verified

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 3.18-6
- Add /etc/keys for initrd/kernel related keys

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 21 2023 Than Ngo <than@redhat.com> - 3.18-4
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 09 2022 Martin Osvald <mosvald@redhat.com> - 3.18-2
- Filesystem has a dependency on /bin/sh (rhbz#1306489)

* Tue Jul 26 2022 Martin Osvald <mosvald@redhat.com> - 3.18-1
- Filesystem has a dependency on /bin/sh (#1306489)
- Add /usr/share/X11/fonts/ to default filesystem (#2107447)
- Remove obsolete and forbidden Group tag
- Own zsh and fish completions directories (rhbz#1312594)
- Improve directory creation to avoid 'Argument list too long' error

* Mon Jul 25 2022 Debarshi Ray <rishi@fedoraproject.org> - 3.17-1
- Assume ownership of /usr/lib/tmpfiles.d

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Petr Menšík <pemensik@redhat.com> - 3.16-3
- Include systemd directories for %unitdir and similar

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug  3 2021 Pavel Zhukov <pzhukov@redhat.com> - 3.15-1
- Move /afs into main package

* Fri Aug 07 2020 Pavel Raiskup <praiskup@redhat.com> - 3.14-4
- /proc and /sys made %%ghost to allow filesystem package updates in rootless
  container environments (rhbz#1548403)

* Mon Jan 27 2020 Ondrej Vasik <ovasik@redhat.com> - 3.14-1
- do not restore context of /proc (#1722766)

* Wed Dec 18 2019 Ondrej Vasik <ovasik@redhat.com> - 3.13-1
- add ownership for eBPF bytecode files directories (#1781646)

* Thu Jun 20 2019 David Howells <dhowells@redhat.com> - 3.12-1
- add new -afs supbackage for /afs directory (#FPC888,#1720232)

* Mon Apr 29 2019 Ondrej Vasik <ovasik@redhat.com> - 3.11-1
- drop ownership for /etc/xinet.d (#1691146)
- drop ownership for %{_libdir}/tls, %{_libdir}/sse2 (#1702329)

* Mon Feb 11 2019 Ondrej Vasik <ovasik@redhat.com> - 3.10-1
- drop legacy /var/gopher (#1667231)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 21 2018 Ondrej Vasik <ovasik@redhat.com> - 3.9-1
- add ownership of /etc/rwtab.d and /etc/statetab.d

* Tue Feb 20 2018 Adam Jackson <ajax@redhat.com> - 3.8-3
- own /etc/X11/xinit/{,{xinitrc,xinput}.d}

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 13 2018 Ondrej Vasik <ovasik@redhat.com> - 3.8-1
- drop the ownership of ghostscript dirs (#1533992)

* Thu Dec 14 2017 Ondrej Vasik <ovasik@redhat.com> - 3.7-1
- own /usr/share/locale and /usr/lib/modules
- own /usr/lib/sysimage
- improve filesystem content file to include symlinks and rootdir

* Mon Nov 20 2017 Ondrej Vasik <ovasik@redhat.com> - 3.6-1
- own /usr/share/bash-completion{,/completions,/helpers} (#1504616)
- create and own /usr/lib/debug/.dwz dir to prevent
  dangling symlink (#1508610)

* Thu Oct 12 2017 Ondrej Vasik <ovasik@redhat.com> - 3.5-1
- improve the content file creation

* Thu Oct 05 2017 Ondrej Vasik <ovasik@redhat.com> - 3.4-1
- create and own file with the content of filesystem package

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 21 2017 Ondrej Vasik <ovasik@redhat.com> - 3.3-1
- Move to Pagure.io
- add ownership for /usr/share/metainfo/ (#1434008)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Ondrej Vasik <ovasik@redhat.com> - 3.2-39
- refresh lang-exceptions list - /usr/share/locale ownerships
  (#1409402, #1313421)
- add ownership for /usr/share/help (#1357974)

* Tue Oct 11 2016 Richard W.M. Jones <rjones@redhat.com> - 3.2-38
- Add riscv64 to list of 64 bit architectures.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Ondrej Vasik <ovasik@redhat.com> - 3.2-36
- own /var/ftp - homedir for system default ftp user (#1302711)

* Fri Sep 04 2015 Michal Toman <mtoman@fedoraproject.org> - 3.2-35
- add mips64 and mips64el to the 64-bit arches

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Ondrej Vasik <ovasik@redhat.com> - 3.2-33
- prevent potentially broken symlinks in debuginfo dirs (#1195641)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Ondrej Vasik <ovasik@redhat.com> - 3.2-31
- revert /media -> /run/media change - as it is more fragile
  than useful (#965918)

* Wed Jul 30 2014 Ondrej Vasik <ovasik@redhat.com> - 3.2-30
- fix wrong redirection of restorecon stderr (#1124623)

* Tue Jul 29 2014 Ondrej Vasik <ovasik@redhat.com> - 3.2-29
- rename /media directory when replacing with symlinks
  to prevent potential data loss

* Mon Jul 28 2014 Ondrej Vasik <ovasik@redhat.com> - 3.2-28
- add ownership for /usr/share/licenses (#1121416)
- have /media as symlink to /run/media (#965918)

* Mon Jul 14 2014 Ondrej Vasik <ovasik@redhat.com> - 3.2-27
- add ownership for /usr/share/wayland-sessions (#1022423)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Ondrej Vasik <ovasik@redhat.com> - 3.2-25
- /var/run has incorrect selinux context after installation
  to disk image (#1034922)

* Fri Jan 10 2014 Ondrej Vasik <ovasik@redhat.com> - 3.2-24
- refresh the list of lang-exceptions from rawhide repo

* Fri Jan 10 2014 Ondrej Vasik <ovasik@redhat.com> - 3.2-23
- add ppc64 little endian to the 64-bit arches(#1051191)
- add bn_BD to lang exceptions (#1048327)

* Wed Dec 04 2013 Ondrej Vasik <ovasik@redhat.com> - 3.2-22
- change the permissions of the /sys directory to 555
  to match the kernel (#1037862)

* Mon Nov 18 2013 Ondrej Vasik <ovasik@redhat.com> - 3.2-21
- add ownership for the /usr/lib/debug subdirs(#1031136)

* Wed Sep 11 2013 Richard Hughes <rhughes@redhat.com> - 3.2-20
- Add /usr/share/appdata

* Wed Aug 07 2013 Ondrej Vasik <ovasik@redhat.com> - 3.2-19
- drop the ownership of /usr/etc

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 30 2013 Ondrej Vasik <ovasik@redhat.com> - 3.2-17
- .dwz symlink is needed as well (#974130)

* Thu Jun 20 2013 Ondrej Vasik <ovasik@redhat.com> - 3.2-16
- /var/run and /var/lock can't be in payload for some reason

* Wed Jun 19 2013 Ondrej Vasik <ovasik@redhat.com> - 3.2-15
- handle bin/lib/lib64 symlinks in /usr/lib/debug (#974130)

* Tue Jun 18 2013 Kay Sievers <kay@redhat.com> - 3.2-14
- fix yum installroot ending up with directories in /var
  instead of the expected symlinks to /run
- ship /var/run and /var/lock as plain symlinks
- do not handle /var/lock/subsys, it is always on tmpfs
- create all symlinked directories and their targets
  in pretrans to make sure other packages install into
  the right place, even if filesystem.rpm is not the
  first package installed in the transaction

* Sat May 11 2013 Ondrej Vasik <ovasik@redhat.com> 3.2-13
- move /var/spool/uucp to uucp package (#961952)

* Thu Apr 18 2013 Ondrej Vasik <ovasik@redhat.com> 3.2-12
- remove the rpmlib(X-CheckUnifiedSystemdir) requirement
  hack - no longer required

* Mon Apr 08 2013 Ondrej Vasik <ovasik@redhat.com> 3.2-11
- do not handle AArch64 differently (#917804)

* Mon Mar 18 2013 Ondrej Vasik <ovasik@redhat.com> 3.2-9
- revert the change for previous build, breaking koji
  builds

* Mon Mar 18 2013 Ondrej Vasik <ovasik@redhat.com> 3.2-8
- ship /var/run and /var/lock as symlinks in payload,
  don't handle them as part of post scriptlet (#919374)

* Tue Mar 05 2013 Ondrej Vasik <ovasik@redhat.com> 3.2-7
- add support for AArch64 architecture (#917804)

* Wed Feb 27 2013 Ondrej Vasik <ovasik@redhat.com> 3.2-6
- fix directory listed twice errors on 32bit secondary arches
  (#915947)

* Thu Feb 21 2013 Ondrej Vasik <ovasik@redhat.com> 3.2-5
- change the attributes of /usr/lib/debug to 0755 (#911831)

* Tue Feb 19 2013 Ondrej Vasik <ovasik@redhat.com> 3.2-4
- own /usr/lib/debug for consistency (#911831)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Ondrej Vasik <ovasik@redhat.com> 3.2-2
- defer the /etc/default ownership to resolve the build tree conflicts

* Sat Oct 27 2012 Ondrej Vasik <ovasik@redhat.com> 3.2-1
- own /etc/bash_completion.d (#870193)
- own /etc/default and create it as symlink do /etc/sysconfig (#797316)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 29 2012 Ondrej Vasik <ovasik@redhat.com> 3.1-1
- add brx and brx_IN from iso639-3 set to lang-exceptions
  file (#806328)

* Fri Feb  3 2012 Kay Sievers <kay@redhat.com> 3-2
- enable guard against unconverted /bin, /sbin, /lib*
  directories in the filesystem

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 3-1
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Thu Jan 12 2012 Ondrej Vasik <ovasik@redhat.com>  2.4.46-1
- own and create /var/lib/rpm-state (#771713)

* Fri Nov 11 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.45-1
- own and create /var/adm, /var/gopher and /var/spool/uucp
  as these are homedirs for default legacy system accounts
  (#752885)

* Fri Jul 29 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.44-1
- drop ownership of /selinux - moved to /sys/fs/selinux(#726528)

* Tue Jun 28 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.43-1
- add various languages to lang-exceptions(#620063)

* Wed May 18 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.42-1
- Pre: require setup again (#705443)

* Fri Apr 08 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.41-1
- drop filesystem.conf file (#694688)

* Tue Apr 05 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.40-1
- create /run/lock as 755 root:root (#693394)

* Thu Mar 31 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.39-1
- add /run to filesystem (#692124)
- minor spec file cleanup

* Fri Feb 25 2011 Ondrej Vasik <ovasik@redhat.com>  2.4.38-1
- do /var/lock/subsys directory systemd way via tmpfiles.d conf file
  (#656586)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Adam Jackson <ajax@redhat.com> 2.4.37-1
- Drop Prov/Obs: xorg-x11-filesystem and pm-utils-filesystem, both last seen
  in Fedora 11.
- Remove explicit BuildRoot.

* Fri Sep 25 2010 Ondrej Vasik <ovasik@redhat.com>  2.4.36-1
- own /usr/lib/sse2 even on 64-bit (#636748)

* Mon Apr 19 2010 Ondrej Vasik <ovasik@redhat.com>  2.4.35-1
- change permissions on /var/lock from 775 root:lock to
  755 root:root (#581884)

* Thu Apr 08 2010 Ondrej Vasik <ovasik@redhat.com>  2.4.34-1
- drop ownership for /mnt/{floppy,cdrom} subdirs(#173854)

* Thu Mar 04 2010 Ondrej Vasik <ovasik@redhat.com>  2.4.33-1
- do own /usr/share/aclocal (#533962)

* Tue Mar 02 2010 Ondrej Vasik <ovasik@redhat.com>  2.4.32-1
- added sr@ijekavian and sr@ijekavianlatin into lang
  exceptions

* Thu Oct 01 2009 Ondrej Vasik <ovasik@redhat.com>  2.4.31-1
- added zh_CN.GB2312 to lang exceptions(#487568)

* Tue Aug 25 2009 Karsten Hopp <karsten@redhat.com> 2.4.30-2
- fix typo in Provides

* Mon Aug 17 2009 Ondrej Vasik <ovasik@redhat.com> 2.4.30-1
- adjust directory rights for usage of capabilities(#517575)

* Mon Aug 10 2009 Ondrej Vasik <ovasik@redhat.com> 2.4.29-1
- iso_codes package no longer provides tab files, do generate
  them on fly with sed (thanks D. Tardon)

* Wed Aug 05 2009 Ondrej Vasik <ovasik@redhat.com> 2.4.28-1
- Provide/obsolete pm-utils-filesystem, own dirs for pm-utils
  hooks(#515362)
- Do own man sections for /usr/share/man/<locale> dirs (#220265)
- Do own /usr/share/sounds (#515485)

* Tue Aug 04 2009 Adam Jackson <ajax@redhat.com> 2.4.27-1
- Prov/Obs: xorg-x11-filesystem

* Mon Aug 03 2009 Ondrej Vasik <ovasik@redhat.com> 2.4.26-1
- Do own /usr/share/man/<locale> directories (ghosted, missingok) - #220265

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 2.4.25-1
- Remove explicit /usr/lib/X11, everything uses %%_libdir now.

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 2.4.24-1
- Added /usr/share/X11

* Thu Jul 09 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.23-1
- do own /usr/src/debug (#214983)

* Wed Jul 08 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.22-1
- do own interface description directory /usr/share/idl(#451719)
- add a few missing lang-exceptions to filelist(#508309)

* Wed Mar 04 2009 Phil Knirsch <pknirsch@redhat.com> - 2.4.21-1
- Added /usr/share/backgrounds (#487957)
- Added /usr/share/ghostscript/{conf.d} (#302521)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Phil Knirsch <pknirsch@redhat.com> - 2.4.20-1
- Removed ownership of fonts directories (#477046)

* Sat Sep 06 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.19-1
- Added augeas lenses dir (#461317)

* Tue Jun 24 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.18-1
- Added comment with raw format lang-exception URL

* Mon Jun 23 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.17-1
- Added URL for lang-exception source (#225752)

* Wed Jun 18 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.16-1
- Dropped /etc/news again as we're handling it now correctly (#437462)
- Filesystem is now an official fedorahosted project, part of the review
  changes (#225752)
- Removed duplicate entry in lang_exceptions for ca_ES@valencian (#225752)

* Tue May 27 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.15-1
- First round of Fedora package review changes (#225752)

* Tue May 20 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.14-1
- Added /usr/src/kernels to owned and created dirs (#442283)

* Mon Apr 07 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.13-1
- Added /etc/news to owned and created directories

* Thu Mar 27 2008 Phil Knirsch <pknirsch@redhat.com> - 2.4.12-1
- Added be@latin to lang-exceptions (#231737)
- Added /usr/share/man{0,1,3]p to owned files (#233879)
- Added /usr/share/fonts to owned files (#302141)
- Renamed sr@Latn to sr@latin (#436887)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.4.11-2
- Autorebuild for GCC 4.3

* Mon Aug 13 2007 Phil Knirsch <pknirsch@redhat.com> 2.4.11-1
- Added /etc/X11/fontpath.d and dropped /etc/X11/sysconfig /etc/X11/serverconfig
 (#251707)

* Wed Jul 18 2007 Phil Knirsch <pknirsch@redhat.com> 2.4.10-1
- Replaced gtk-doc with gnome (#247276)

* Tue May 29 2007 Phil Knirsch <pknirsch@redhat.com> 2.4.9-1
- Fixed nasty typo for /etc directories (#241525)

* Fri May 25 2007 Phil Knirsch <pknirsch@redhat.com> 2.4.8-1
- Fixed description to avoid trademark issues (#234093)

* Thu May 24 2007 Phil Knirsch <pknirsch@redhat.com> 2.4.7-1
- Added /etc/fonts/conf.d and /usr/share/themes (#239246)
- Removed /etc/xdg/menus, already owned by redhat-menus (#228779)

* Tue Apr 17 2007 Phil Knirsch <pknirsch@redhat.com> - 2.4.6-1
- Added several more /usr/share directories (#222905)

* Sat Mar 31 2007 Peter Jones <pjones@redhat.com> - 2.4.5-1
- add /usr/local/share/applications

* Fri Mar 30 2007 Jeremy Katz <katzj@redhat.com> - 2.4.4-1
- add /etc/xdg/autostart

* Thu Mar 15 2007 Phil Knirsch <pknirsch@redhat.com> - 2.4.3-1
- Fixed typo for new /etc/xdg entries (#224052)
- One more tiny specile cleanup

* Mon Feb 12 2007 Phil Knirsch <pknirsch@redhat.com> - 2.4.2-1
- Added several missing unowned directories (#224052)
- Tiny specfile cleanups

* Wed Dec 20 2006 Phil Knirsch <pknirsch@redhat.com> - 2.4.1-1
- Dropped the obsolete directories /usr/lib{,64}/gcc-lib (#220235)

* Tue Oct 10 2006 Bill Nottingham <notting@redhat.com> - 2.4.0-1
- create and own /usr/share/locale/*/LC_MESSAGES (#196669)

* Tue Oct 10 2006 Phil Knirsch <pknirsch@redhat.com> - 2.3.8-1
- Added the manXx directories to the ownership of filesystem (#208121)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.7-2.1
- rebuild

* Wed Jun 28 2006 Phil Knirsch <pknirsch@redhat.com> - 2.3.7-2
- Fixed games location according to FHS 2.1 (#165425)
- Added {_libdir}/sse2 to owned files (#192853)
- Added /dev to owned files (#192860)
- Added {_datadir}/icons to owned files (#195911)
- Dropped obsolete /etc/X11/starthere (#191163)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.3.7-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.3.7-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 17 2005 Bill Nottingham <notting@redhat.com> - 2.3.7-1
- actually, *do* package /usr/lib/X11, etc, but as directories
- remove /usr/X11R6 heirarchy

* Mon Nov  7 2005 Bill Nottingham <notting@redhat.com> - 2.3.6-1
- don't package /usr/lib/X11 or /usr/bin/X11 symlinks

* Fri Aug 19 2005 Bill Nottingham <notting@redhat.com> - 2.3.5-1
- package / (#165797)

* Mon May 23 2005 Bill Nottingham <notting@redhat.com> - 2.3.4-1
- ship /usr/share/games (#158433, <ville.skytta@iki.fi>)

* Thu May  5 2005 Peter Jones <pjones@redhat.com> - 2.3.3-1
- remove /initrd, since mkinitrd doesn't use it anymore by default

* Wed Apr 20 2005 John Dennis <jdennis@redhat.com> - 2.3.2-1
- add /etc/pki, a place to store keys and certificates

* Wed Mar  9 2005 Bill Nottingham <notting@redhat.com> 2.3.1-1
- don't ship /usr/lib64/X11 in general (#147077)

* Thu Aug 12 2004 Bill Nottingham <notting@redhat.com> 2.3.0-1
- add /media, /srv

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Mar 11 2004 Bill Nottingham <notting@redhat.com> 2.2.4-1
- move /selinux here from SysVinit

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 15 2004 Bill Nottingham <notting@redhat.com> 2.2.3-1
- move /usr/dict to /usr/share/dict (#113645)
- add /usr/lib/locale, /var/empty (#108686,#113036)
- add */%%{_lib}/tls (#113050)

* Fri Nov 21 2003 Bill Nottingham <notting@redhat.com> 2.2.2-1
- add /sys

* Tue Oct 07 2003 Than Ngo <than@redhat.com> 2.2.1-5
- add /usr/share/xsessions

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Dec  1 2002 Tim Waugh <twaugh@redhat.com> 2.2.1-2
- Really fix /var/mail

* Thu Nov 28 2002 Bill Nottingham <notting@redhat.com> 2.2.1-1
- fix /var/mail

* Wed Nov 20 2002 Bill Nottingham <notting@redhat.com>
- make arch specific, handle lib/lib64 stuff
- add /usr/libexec, /usr/share/applications

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Aug 20 2001 Bill Nottingham <notting@redhat.com>
- %%ghost /mnt/cdrom, /mnt/floppy (fixes #52046)

* Wed Aug 15 2001 Bill Nottingham <notting@redhat.com>
- add /usr/X11R6/share (#51830)

* Mon Aug 13 2001 Bill Nottingham <notting@redhat.com>
- prereq a particular version of the setup package

* Thu Aug  9 2001 Bill Nottingham <notting@redhat.com>
- remove /mnt/cdrom, /mnt/floppy (updfstab will create them if needed)
- make it noarch again

* Wed Aug  8 2001 Bill Nottingham <notting@redhat.com>
- /var/lock needs to be root.lock, not lock.lock

* Mon Aug  6 2001 Jeff Johnson <jbj@redhat.com>
- lock.lock ownership, 0775 permissions, for /var/lock.

* Tue Jul 17 2001 Bill Nottingham <notting@redhat.com>
- add /etc/sysconfig, /var/yp, /usr/share/pixmaps

* Tue Jul 10 2001 Bill Nottingham <notting@redhat.com>
- add stuff under /etc/X11
- remove extraneous /usr/X11R6/doc (#47490)

* Mon Jun 25 2001 Bill Nottingham <notting@redhat.com>
- don't conflict with rpm

* Fri Jun 22 2001 Bill Nottingham <notting@redhat.com>
- don't own /var/lib/rpm (#43315)
- add some stuff in /usr/local (#36522)

* Thu Jun 21 2001 Bill Nottingham <notting@redhat.com>
- add /initrd

* Thu Jun 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- remove noarch
- do not include /mnt/cdrom and /mnt/floppy for s390/s390x

* Mon Apr 16 2001 Bill Nottingham <notting@redhat.com>
- take the group write off of /var/lock

* Fri Jul 21 2000 Bill Nottingham <notting@redhat.com>
- add /usr/share/empty

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jun 28 2000 Preston Brown <pbrown@redhat.com>
- remove /usr/doc

* Thu Jun 22 2000 Preston Brown <pbrown@redhat.com>
- remove /usr/info

* Sun Jun 19 2000 Bill Nottingham <notting@redhat.com>
- remove /usr/man

* Sat Jun 17 2000 Bill Nottingham <notting@redhat.com>
- /var/spool/lpd should have normal perms (#12272)

* Tue Jun  6 2000 Bill Nottingham <notting@redhat.com>
- add /etc/skel

* Thu Jun 01 2000 Preston Brown <pbrown@redhat.com>
- add /var/spool/lpd to filesystem, owned by user/group lp, tight permissions

* Tue May 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Added /etc/xinetd.d

* Mon May 15 2000 Preston Brown <pbrown@redhat.com>
- /etc/opt, /usr/share/{info,man/man*,misc,doc} (FHS 2.1)
- added /var/games.  Data should move from /var/lib/games to there (FHS 2.1)
- bump version up to 2.0 already!

* Thu Apr 13 2000 Jakub Jelinek <jakub@redhat.com>
- removed /var/state, added /var/opt, /var/mail for FHS 2.1 compliance

* Mon Aug 28 1999 Preston Brown <pbrown@redhat.com>
- added /opt, /var/state, /var/cache for FHS compliance (#3966)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- don't carry X11R6.1 as directory on sparc.
- /var/tmp/build root (#811)

* Wed Jan 13 1999 Preston Brown <pbrown@redhat.com>
- font directory didn't belong, which I previously misunderstood.  removed.

* Fri Nov 13 1998 Preston Brown <pbrown@redhat.com>
- /usr/share/fonts/default added.

* Fri Oct  9 1998 Bill Nottingham <notting@redhat.com>
- put /mnt/cdrom back in

* Wed Oct  7 1998 Bill Nottingham <notting@redhat.com>
- Changed /root to 0750

* Wed Aug 05 1998 Erik Troan <ewt@redhat.com>
- added /var/db
- set attributes in the spec file; don't depend on the ones in the cpio
  archive
- use a tarball instead of a cpioball

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Sep 09 1997 Erik Troan <ewt@redhat.com>
- made a noarch package

* Wed Jul 09 1997 Erik Troan <ewt@redhat.com>
- added /

* Wed Apr 16 1997 Erik Troan <ewt@redhat.com>
- Changed /proc to 555
- Removed /var/spool/mqueue (which is owned by sendmail)
