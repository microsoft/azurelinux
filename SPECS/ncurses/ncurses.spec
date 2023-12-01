%global patchlevel     20231125

Summary:        Libraries for terminal handling of character screens
Name:           ncurses
Version:        6.4
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://invisible-island.net/ncurses/
#
# Please note that it is very important to select the ncurses package
# with the highest available patch level in the name when fixing CVE's
#
# For example, the original 6.3 ncurses release is available here:
# https://invisible-mirror.net/archives/ncurses/ncurses-6.3.tar.gz
#
# However there are rollling patch versions of the package available under this folder:
# https://invisible-mirror.net/archives/ncurses/current/
#
# So, when upgrading choose the appropriate patch version
# Also note that at least one CVE on NIST had unusual matching rules
# where the patch number is not specified in the version,
# but was described in the textual description.
#
# Description showed:
#   ncurses 6.3 before patch 20220416 has an out-of-bounds....
#
# Matching rules showed:
#   cpe:2.3:a:gnu:ncurses:*:*:*:*:*:*:*:*  	    Up to (excluding)  6.3
#   cpe:2.3:a:gnu:ncurses:6.3:-:*:*:*:*:*:*     [and this line says including 6.3?!]
#
# Use a nopatch file to clear the CVE after choosing the correct patch level
#
Source0:        https://invisible-mirror.net/archives/%{name}/current/%{name}-%{version}-%{patchlevel}.tgz
Requires:       %{name}-libs = %{version}-%{release}


%description
The Ncurses package contains libraries for terminal-independent
handling of character screens.

%package        libs
Summary:        Ncurses Libraries
Group:          System Environment/Libraries

%description libs
This package contains ncurses libraries

%package        compat
Summary:        Ncurses compatibility libraries
Group:          System Environment/Libraries

%description    compat
This package contains the ABI version 5 of the ncurses libraries for
compatibility.

%package        devel
Summary:        Header and development files for ncurses
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%package        term
Summary:        terminfo files for ncurses
Requires:       %{name} = %{version}-%{release}

%description    term
It contains all terminfo files

%prep
%autosetup -p1 -n %{name}-%{version}-%{patchlevel}

%build
common_options="\
    --enable-colorfgbg \
    --enable-hard-tabs \
    --enable-overwrite \
    --enable-pc-files \
    --enable-xmc-glitch \
    --disable-stripping \
    --disable-wattr-macros \
    --with-cxx-shared \
    --with-ospeed=unsigned \
    --with-pkg-config-libdir=%{_libdir}/pkgconfig \
    --with-shared \
    --with-terminfo-dirs=%{_sysconfdir}/terminfo:%{_datadir}/terminfo \
    --with-termlib=tinfo \
    --with-ticlib=tic \
    --with-xterm-kbs=DEL \
    --without-ada"
abi5_options="--with-chtype=long"

for abi in 5 6; do
    for char in narrowc widec; do
        mkdir $char$abi
        pushd $char$abi
        ln -s ../configure .

        [ $abi = 6 -a $char = widec ] && progs=yes || progs=no

        %configure $(
            echo $common_options --with-abi-version=$abi
            [ $abi = 5 ] && echo $abi5_options
            [ $char = widec ] && echo --enable-widec
            [ $progs = yes ] || echo --without-progs
        )

        make %{?_smp_mflags} libs
        [ $progs = yes ] && make %{?_smp_mflags} -C progs

        popd
    done
done

%install
make -C narrowc5 DESTDIR=%{buildroot} install.libs
rm %{buildroot}%{_libdir}/lib{tic,tinfo}.so.5*
make -C widec5 DESTDIR=%{buildroot} install.libs
make -C narrowc6 DESTDIR=%{buildroot} install.libs
rm %{buildroot}%{_libdir}/lib{tic,tinfo}.so.6*
make -C widec6 DESTDIR=%{buildroot} install.{libs,progs,data,includes,man}

chmod 755 %{buildroot}%{_libdir}/lib*.so.*.*
chmod 644 %{buildroot}%{_libdir}/lib*.a

mkdir -p %{buildroot}%{_sysconfdir}/terminfo

baseterms=

# prepare -base and -term file lists
for termname in \
    ansi dumb linux vt100 vt100-nav vt102 vt220 vt52 \
    Eterm\* aterm bterm cons25 cygwin eterm\* gnome gnome-256color hurd jfbterm \
    konsole konsole-256color mach\* mlterm mrxvt nsterm putty{,-256color} pcansi \
    rxvt{,-\*} screen{,-\*color,.[^mlp]\*,.linux,.mlterm\*,.putty{,-256color},.mrxvt} \
    st{,-\*color} sun teraterm teraterm2.3 tmux{,-\*} vte vte-256color vwmterm \
    wsvt25\* xfce xterm xterm-\*
do
    for i in %{buildroot}%{_datadir}/terminfo/?/$termname; do
        for t in $(find %{buildroot}%{_datadir}/terminfo -samefile $i); do
            baseterms="$baseterms $(basename $t)"
        done
    done
done 2> /dev/null
for t in $baseterms; do
    echo "%dir %{_datadir}/terminfo/${t::1}"
    echo %{_datadir}/terminfo/${t::1}/$t
done 2> /dev/null | sort -u > terms.base
find %{buildroot}%{_datadir}/terminfo \! -type d | \
    sed "s|^%{buildroot}||" | while read t
do
    echo "%dir $(dirname $t)"
    echo $t
done 2> /dev/null | sort -u | comm -2 -3 - terms.base > terms.term

# can't replace directory with symlink (rpm bug), symlink all headers
mkdir %{buildroot}%{_includedir}/ncurses{,w}
for l in %{buildroot}%{_includedir}/*.h; do
    ln -s ../$(basename $l) %{buildroot}%{_includedir}/ncurses
    ln -s ../$(basename $l) %{buildroot}%{_includedir}/ncursesw
done

# don't require -ltinfo when linking with --no-add-needed
for l in %{buildroot}%{_libdir}/libncurses{,w}.so; do
    soname=$(basename $(readlink $l))
    rm -f $l
    echo "INPUT($soname -ltinfo)" > $l
done

rm -f %{buildroot}%{_libdir}/libcurses{,w}.so
echo "INPUT(-lncurses)" > %{buildroot}%{_libdir}/libcurses.so
echo "INPUT(-lncursesw)" > %{buildroot}%{_libdir}/libcursesw.so

echo "INPUT(-ltinfo)" > %{buildroot}%{_libdir}/libtermcap.so

rm -f %{buildroot}%{_bindir}/ncurses*5-config
rm -f %{buildroot}%{_libdir}/terminfo
rm -f %{buildroot}%{_libdir}/pkgconfig/*_g.pc

xz NEWS

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post compat -p /sbin/ldconfig
%postun compat -p /sbin/ldconfig

%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%doc ANNOUNCE AUTHORS NEWS.xz README TO-DO
%{_bindir}/[cirt]*
%{_mandir}/man1/[cirt]*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files libs -f terms.base
%{!?_licensedir:%global license %%doc}
%doc README
%license COPYING
%{_datadir}/terminfo/l/linux
%dir %{_sysconfdir}/terminfo
%{_datadir}/tabset
%dir %{_datadir}/terminfo
%{_libdir}/lib*.so.6*

%files compat
%{_libdir}/lib*.so.5*

%files devel
%doc doc/html/hackguide.html
%doc doc/html/ncurses-intro.html
%doc c++/README*
%doc misc/ncurses.supp
%{_bindir}/ncurses*-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/ncurses
%dir %{_includedir}/ncursesw
%{_includedir}/ncurses/*.h
%{_includedir}/ncursesw/*.h
%{_includedir}/*.h
%{_mandir}/man1/ncurses*-config*
%{_mandir}/man1/description.1m.gz
%{_mandir}/man3/*
%{_libdir}/lib*.a

%files term -f terms.term

%changelog
* Tue Nov 28 2023 Andrew Phelps <anphel@microsoft.com> - 6.4-2
- Update to version 6.4-20231125

* Wed Apr 26 2023 Sindhu Karri <lakarri@microsoft.com> - 6.4-1
- Update to version 6.4-20230408 to fix CVE-2023-29491

* Tue Sep 20 2022 Jon Slobodzian <joslobo@microsoft.com> - 6.3-2
- Update to version 6.3-20220612 to fix CVE-2022-29458
- Cherry-picked from Mariner 1.0

* Mon Jun 13 2022 Andrew Phelps <anphel@microsoft.com> - 6.3-1
- Update to version 6.3

* Wed Apr 20 2022 Olivia Crain <oliviacrain@microsoft.com> - 6.2-6
- Patch CVE-2021-39537
- Change FTP source url to HTTPS mirror
- Lint spec

* Tue Feb 08 2022 Olivia Crain <oliviacrain@microsoft.com> - 6.2-5
- Remove manual pkgconfig(*) provides in toolchain specs

* Thu Aug 06 2020 Mateusz Malisz <mamalisz@microsoft.com> - 6.2-4
- Sync build process with Fedora 32.
- Add libtinfo

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 6.2-3
- Added %%license line automatically

* Mon Apr 27 2020 Emre Girgin <mrgirgin@microsoft.com> - 6.2-2
- Rename ncurses-terminfo to ncurses-term.

* Thu Apr 23 2020 Andrew Phelps <anphel@microsoft.com> - 6.2-1
- Update to version 6.2. Verified license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 6.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 12 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 6.1-1
- Update to version 6.1.

* Tue Jul 17 2018 Tapas Kundu <tkundu@vmware.com> - 6.0-14
- Fix for CVE-2018-10754

* Wed Dec 06 2017 Xiaolin Li <xiaolinl@vmware.com> - 6.0-13
- version bump to 20171007, fix CVE-2017-16879

* Tue Oct 10 2017 Bo Gan <ganb@vmware.com> - 6.0-12
- version bump to 20171007
- Fix for CVE-2017-11112, CVE-2017-11113 and CVE-2017-13728

* Fri Sep 15 2017 Xiaolin Li <xiaolinl@vmware.com> - 6.0-11
- ncurses-devel provides pkgconfig(ncurses)

* Thu Aug 10 2017 Bo Gan <ganb@vmware.com> - 6.0-10
- Move ncursesw6-config to devel

* Thu Jul 06 2017 Dheeraj Shetty <dheerajs@vmware.com> - 6.0-9
- Fix for CVE-2017-10684 and CVE-2017-10685

* Mon Jun 05 2017 Bo Gan <ganb@vmware.com> - 6.0-8
- Fix bash dependency

* Sun Jun 04 2017 Bo Gan <ganb@vmware.com> - 6.0-7
- Fix symlink

* Wed Mar 29 2017 Alexey Makhalov <amakhalov@vmware.com> - 6.0-6
- --with-chtype=long --with-mmask-t=long to avoid type clashes (1838226)

* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> - 6.0-5
- Add -terminfo subpackage. Main package carries only 'linux' terminfo

* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> - 6.0-4
- Move doc and man3 to the devel package

* Fri Oct 07 2016 ChangLee <changlee@vmware.com> - 6.0-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 6.0-2
- GA - Bump release of all rpms

* Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> - 6.0-1
- Update to version 6.0.

* Wed Nov 18 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> - 5.9-4
- Package provides libncurses.so.5()(64bit)

* Tue Nov 10 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> - 5.9-3
- Add libncurses.so.5, and minor fix in the devel package

* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> - 5.9-2
- Update according to UsrMove.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 5.9-1
- Initial build. First version
