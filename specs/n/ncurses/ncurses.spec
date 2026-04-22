# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?rhel} >= 10
%bcond_with compat_libs
%bcond_with gpm
%else
%bcond_without compat_libs
%bcond_without gpm
%endif
%global revision 20250614
Summary: Ncurses support utilities
Name: ncurses
Version: 6.5
Release: 8.%{revision}%{?dist}
License: MIT-open-group
URL: https://invisible-island.net/ncurses/ncurses.html
Source0: https://invisible-mirror.net/archives/ncurses/current/ncurses-%{version}-%{revision}.tgz
Source1: https://invisible-mirror.net/archives/ncurses/current/ncurses-%{version}-%{revision}.tgz.asc
Source2: https://invisible-island.net/public/dickey@invisible-island.net-rsa3072.asc

Patch8: ncurses-config.patch
Patch9: ncurses-libs.patch
Patch11: ncurses-urxvt.patch
BuildRequires: gcc gcc-c++ gnupg2 make pkgconfig
%{?with_gpm:BuildRequires: gpm-devel}

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains support utilities, including a terminfo compiler
tic, a decompiler infocmp, clear, tput, tset, and a termcap conversion
tool captoinfo.

%package libs
Summary: Ncurses libraries
Requires: %{name}-base = %{version}-%{release}

%description libs
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains the ncurses libraries.

%if %{with compat_libs}
%package compat-libs
Summary: Ncurses compatibility libraries
Requires: %{name}-base = %{version}-%{release}

%description compat-libs
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains the ABI version 5 of the ncurses libraries for
compatibility.
%endif

%package c++-libs
Summary: Ncurses C++ bindings
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description c++-libs
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains C++ bindings of the ncurses ABI version 6 libraries.

%package base
Summary: Descriptions of common terminals
# rxvt-unicode-256color entry used to be in rxvt-unicode and briefly
# in rxvt-unicode-terminfo
Conflicts: rxvt-unicode < 9.22-15
Obsoletes: rxvt-unicode-terminfo < 9.22-18
BuildArch: noarch

%description base
This package contains descriptions of common terminals. Other terminal
descriptions are included in the ncurses-term package.

%package term
Summary: Terminal descriptions
Requires: %{name}-base = %{version}-%{release}
BuildArch: noarch

%description term
This package contains additional terminal descriptions not found in
the ncurses-base package.

%package devel
Summary: Development files for the ncurses library
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-c++-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
The header files and libraries for developing applications that use
the ncurses terminal handling library.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.

%package static
Summary: Static libraries for the ncurses library
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The ncurses-static package includes static libraries of the ncurses library.

%prep
%{gpgverify} --keyring=%{SOURCE2} --signature=%{SOURCE1} --data=%{SOURCE0}

%setup -q -n %{name}-%{version}-%{revision}

%patch -P8 -p1 -b .config
%patch -P9 -p1 -b .libs
%patch -P11 -p1 -b .urxvt

for f in ANNOUNCE; do
    iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
        touch -r ${f}{,_} && mv -f ${f}{_,}
done

%build
common_options="\
    --enable-colorfgbg \
    --enable-hard-tabs \
    --enable-overwrite \
    --enable-pc-files \
    --enable-xmc-glitch \
    --disable-root-access \
    --disable-setuid-environ \
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
%{!?with_gpm:--without-gpm} \
    --without-ada"
abi5_options="--with-chtype=long"

for abi in %{?with_compat_libs:5} 6; do
    for char in narrowc widec; do
        mkdir $char$abi
        pushd $char$abi
        ln -s ../configure .

        [ $abi = 6 -a $char = widec ] && progs=yes || progs=no

        %configure $(
            echo $common_options --with-abi-version=$abi
            [ $abi = 5 ] && echo $abi5_options
            [ $char = widec ] && echo --enable-widec || echo --disable-widec
            [ $progs = yes ] || echo --without-progs
        )

        %make_build libs
        [ $progs = yes ] && %make_build -C progs

        # force use of stdbool.h for compatibility with older standards
        sed -i '/^#define NCURSES_ENABLE_STDBOOL_H/s/0/1/' include/curses.h

        popd
    done
done

%install
%if %{with compat_libs}
make -C narrowc5 DESTDIR=$RPM_BUILD_ROOT install.libs
rm ${RPM_BUILD_ROOT}%{_libdir}/lib{tic,tinfo}.so.5*
make -C widec5 DESTDIR=$RPM_BUILD_ROOT install.libs
%endif
make -C narrowc6 DESTDIR=$RPM_BUILD_ROOT install.libs
rm ${RPM_BUILD_ROOT}%{_libdir}/lib{tic,tinfo}.so.6*
make -C widec6 DESTDIR=$RPM_BUILD_ROOT install.{libs,progs,data,includes,man}

chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/lib*.so.*.*
chmod 644 ${RPM_BUILD_ROOT}%{_libdir}/lib*.a

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/terminfo

baseterms=

# prepare -base and -term file lists
for termname in \
    alacritty ansi dumb foot\* linux vt100 vt100-nav vt102 vt220 vt52 \
    Eterm\* aterm bterm cons25 cygwin eterm\* gnome gnome-256color hurd jfbterm \
    kitty konsole konsole-256color mach\* mlterm mrxvt nsterm putty{,-256color} pcansi \
    rxvt{,-\*} screen{,-\*color,.[^mlp]\*,.linux,.mlterm\*,.putty{,-256color},.mrxvt} \
    st{,-\*color} sun teraterm teraterm2.3 tmux{,-\*} vte vte-256color vwmterm \
    wsvt25\* xfce xterm xterm-\*
do
    for i in $RPM_BUILD_ROOT%{_datadir}/terminfo/?/$termname; do
        for t in $(find $RPM_BUILD_ROOT%{_datadir}/terminfo -samefile $i); do
            baseterms="$baseterms $(basename $t)"
        done
    done
done 2> /dev/null
for t in $baseterms; do
    echo "%dir %{_datadir}/terminfo/${t::1}"
    echo %{_datadir}/terminfo/${t::1}/$t
done 2> /dev/null | sort -u > terms.base
find $RPM_BUILD_ROOT%{_datadir}/terminfo \! -type d | \
    sed "s|^$RPM_BUILD_ROOT||" | while read t
do
    echo "%dir $(dirname $t)"
    echo $t
done 2> /dev/null | sort -u | comm -2 -3 - terms.base > terms.term

# can't replace directory with symlink (rpm bug), symlink all headers
mkdir $RPM_BUILD_ROOT%{_includedir}/ncurses{,w}
for l in $RPM_BUILD_ROOT%{_includedir}/*.h; do
    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncurses
    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncursesw
done

# don't require -ltinfo when linking with --no-add-needed
for l in $RPM_BUILD_ROOT%{_libdir}/libncurses{,w}.so; do
    soname=$(basename $(readlink $l))
    rm -f $l
    echo "INPUT($soname -ltinfo)" > $l
done

rm -f $RPM_BUILD_ROOT%{_libdir}/libcurses{,w}.so
echo "INPUT(-lncurses)" > $RPM_BUILD_ROOT%{_libdir}/libcurses.so
echo "INPUT(-lncursesw)" > $RPM_BUILD_ROOT%{_libdir}/libcursesw.so

echo "INPUT(-ltinfo)" > $RPM_BUILD_ROOT%{_libdir}/libtermcap.so

rm -f $RPM_BUILD_ROOT%{_bindir}/ncurses*5-config
rm -f $RPM_BUILD_ROOT{%{_libdir},/usr/lib}/terminfo
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/*_g.pc

xz NEWS

%ldconfig_scriptlets libs

%ldconfig_scriptlets c++-libs

%if %{with compat_libs}
%ldconfig_scriptlets compat-libs
%endif

%files
%doc ANNOUNCE AUTHORS NEWS.xz README TO-DO
%{_bindir}/[cirt]*
%{_mandir}/man1/[cirt]*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files libs
%exclude %{_libdir}/libncurses++*.so.6*
%{_libdir}/lib*.so.6*

%if %{with compat_libs}
%files compat-libs
%{_libdir}/lib*.so.5*
%endif

%files c++-libs
%{_libdir}/libncurses++*.so.6*

%files base -f terms.base
%license COPYING
%doc README
%dir %{_sysconfdir}/terminfo
%{_datadir}/tabset
%dir %{_datadir}/terminfo

%files term -f terms.term

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
%{_mandir}/man3/*

%files static
%{_libdir}/lib*.a

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.5-7.20250614
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 17 2025 Miroslav Lichvar <mlichvar@redhat.com> 6.5-6.20250614
- update to 6.5-20250614 (CVE-2025-6141)

* Tue Jan 28 2025 Miroslav Lichvar <mlichvar@redhat.com> 6.5-5.20250125
- update to 6.5-20250125
- force use of stdbool.h for compatibility with older standards (#2342514)

* Thu Jan 23 2025 Miroslav Lichvar <mlichvar@redhat.com> 6.5-4.20250118
- update to 6.5-20250118 (#2340910)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.5-3.20240629
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.5-2.20240629
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Miroslav Lichvar <mlichvar@redhat.com> 6.5-1.20240629
- update to 6.5-20240629

* Thu Feb 01 2024 Miroslav Lichvar <mlichvar@redhat.com> 6.4-12.20240127
- update to 6.4-20240127
- disable gpm on RHEL >= 10 (RHEL-23679)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-11.20240113
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-10.20240113
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Miroslav Lichvar <mlichvar@redhat.com> 6.4-9.20240113
- update to 6.4-20240113
- disable compat libs on RHEL >= 10
- drop kbs patch

* Wed Oct 04 2023 Miroslav Lichvar <mlichvar@redhat.com> 6.4-8.20231001
- update to 6.4-20231001
- convert license tag to SPDX
- switch from patchX to patch -PX

* Tue Aug 22 2023 Miroslav Lichvar <mlichvar@redhat.com> 6.4-7.20230520
- ignore TERMINFO and HOME only if setuid/setgid/capability

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-6.20230520
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Debarshi Ray <rishi@fedoraproject.org> 6.4-5.20230520
- move foot entries to -base (#2217982)

* Mon May 22 2023 Miroslav Lichvar <mlichvar@redhat.com> 6.4-4.20230520
- update to 6.4-20230520
- build with options disabling root file access and environment

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.4-3.20230114
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Miroslav Lichvar <mlichvar@redhat.com> 6.4-2.20230114
- update to 6.4-20230114 (#2160276)

* Mon Jan 09 2023 Miroslav Lichvar <mlichvar@redhat.com> 6.4-1.20230107
- update to 6.4-20230107
- restore compat-libs (ABI 5) subpackage (#2129865)

* Fri Dec 16 2022 Miroslav Lichvar <mlichvar@redhat.com> 6.3-5.20221126
- revert "enable symbol versioning for dynamic linker (#1875587)"

* Thu Dec 01 2022 Miroslav Lichvar <mlichvar@redhat.com> 6.3-4.20221126
- update to 6.3-20221126
- enable symbol versioning for dynamic linker (#1875587)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.3-3.20220501
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 04 2022 Miroslav Lichvar <mlichvar@redhat.com> 6.3-2.20220501
- update to 6.3-20220501

* Tue Apr 19 2022 Miroslav Lichvar <mlichvar@redhat.com> 6.3-1.20220416
- update to 6.3-20220416 (CVE-2022-29458)
- drop compat-libs (ABI 5) subpackage

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-9.20210508
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-8.20210508
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 10 2021 Miroslav Lichvar <mlichvar@redhat.com> 6.2-7.20210508
- update to 6.2-20210508

* Tue May 04 2021 Miroslav Lichvar <mlichvar@redhat.com> 6.2-6.20210501
- update to 6.2-20210501

* Thu Mar 11 2021 Miroslav Lichvar <mlichvar@redhat.com> 6.2-5.20210306
- update to 6.2-20210306

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-4.20200222
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
- Use make macros
- Remove %license definition
- Add BuildRequires: make

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-3.20200222
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Miroslav Lichvar <mlichvar@redhat.com> 6.2-2.20200222
- move alacritty and kitty entries to -base (#1849974)

* Wed Feb 26 2020 Miroslav Lichvar <mlichvar@redhat.com> 6.2-1.20200222
- update to 6.2-20200222

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-15.20191109
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Miroslav Lichvar <mlichvar@redhat.com> 6.1-14.20191109
- update to 6.1-20191109
- remove LDFLAGS from pkgconfig files and ncurses-config scripts (#1771137)

* Thu Oct 31 2019 Miroslav Lichvar <mlichvar@redhat.com> 6.1-13.20191026
- update to 6.1-20191026 (CVE-2019-17594 CVE-2019-17595)
- restore rxvt-unicode-256color terminfo (Robbie Harwood) (#1430935)
- conflict/obsolete rxvt-unicode (sub)packages with terminfo (#1430935)
- drop old obsoletes and conflicts

* Wed Aug 07 2019 Miroslav Lichvar <mlichvar@redhat.com> 6.1-12.20190803
- update to 6.1-20190803
- verify upstream signatures
- compress NEWS by xz

* Wed Jul 24 2019 Miroslav Lichvar <mlichvar@redhat.com> 6.1-11.20190720
- update to 6.1-20190720

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-10.20180923
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Miroslav Lichvar <mlichvar@redhat.com> 6.1-9.20180923
- disable stripping on program installation

* Mon Sep 24 2018 Miroslav Lichvar <mlichvar@redhat.com> 6.1-8.20180923
- update to 6.1-20180923

* Mon Jul 16 2018 Miroslav Lichvar <mlichvar@redhat.com> 6.1-7.20180714
- update to 6.1-20180714
- add gcc-c++ to build requirements

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-6.20180224
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 09 2018 Miroslav Lichvar <mlichvar@redhat.com> 6.1-5.20180224
- fix crash in parsing of terminfo use capability (CVE-2018-10754)

* Mon Feb 26 2018 Miroslav Lichvar <mlichvar@redhat.com> 6.1-4.20180224
- update to 6.1-20180224
- add gcc to build requirements

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-3.20180129
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Miroslav Lichvar <mlichvar@redhat.com> 6.1-2.20180129
- update to 6.1-20180129
- use macro for ldconfig scriptlets

* Mon Jan 29 2018 Miroslav Lichvar <mlichvar@redhat.com> 6.1-1.20180127
- update to 6.1-20180127

* Thu Nov 30 2017 Miroslav Lichvar <mlichvar@redhat.com> 6.0-15.20171125
- update to 6.0-20171125 (CVE-2017-16879)

* Wed Sep 20 2017 Miroslav Lichvar <mlichvar@redhat.com> 6.0-14.20170916
- update to 6.0-20170916 (CVE-2017-13728 CVE-2017-13729 CVE-2017-13730
  CVE-2017-13731 CVE-2017-13732 CVE-2017-13733 CVE-2017-13734)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-13.20170722
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 6.0-12.20170722
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Miroslav Lichvar <mlichvar@redhat.com> 6.0-11.20170722
- update to 6.0-20170722 (CVE-2017-10684 CVE-2017-10685 CVE-2017-11112
  CVE-2017-11113)

* Mon May 29 2017 Miroslav Lichvar <mlichvar@redhat.com> 6.0-10.20170520
- fix compatibility between libtinfo and libncurses (#1456340)

* Fri May 26 2017 Miroslav Lichvar <mlichvar@redhat.com> 6.0-9.20170520
- update to 6.0-20170520

* Tue Feb 14 2017 Miroslav Lichvar <mlichvar@redhat.com> 6.0-8.20170212
- update to 6.0-20170212

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-7.20160709
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Miroslav Lichvar <mlichvar@redhat.com> 6.0-6.20160709
- update to 6.0-20160709

* Fri Apr 08 2016 Yaakov Selkowitz <yselkowi@redhat.com> 6.0-5.20160116
- separate ncurses-c++-libs subpackage (#1324575)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-4.20160116
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Miroslav Lichvar <mlichvar@redhat.com> 6.0-3.20160116
- make installed ncurses.h compatible with narrow-char libncurses (#1270534)

* Mon Jan 18 2016 Miroslav Lichvar <mlichvar@redhat.com> 6.0-2.20160116
- update to 6.0-20160116

* Thu Aug 13 2015 Miroslav Lichvar <mlichvar@redhat.com> 6.0-1.20150810
- update to 6.0-20150810
- build ABI 5 and ABI 6 libraries
- add compat-libs subpackage for ABI 5 libraries
- update rxvt-unicode terminfo
- don't include tests in devel documentation

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9-21.20150214
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.9-20.20150214
- Rebuilt for GCC 5 C++11 ABI change

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 5.9-19.20150214
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Feb 20 2015 Miroslav Lichvar <mlichvar@redhat.com> 5.9-18.20150214
- update to 5.9-20150214

* Fri Sep 12 2014 Miroslav Lichvar <mlichvar@redhat.com> 5.9-17.20140906
- update to 5.9-20140906

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9-16.20140323
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 5.9-15.20140323
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9-14.20140323
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 26 2014 Miroslav Lichvar <mlichvar@redhat.com> 5.9-13.20140323
- update to 20140323

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9-12.20130511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Miroslav Lichvar <mlichvar@redhat.com> 5.9-11.20130511
- update to 20130511

* Mon Apr 15 2013 Miroslav Lichvar <mlichvar@redhat.com> 5.9-10.20130413
- update to 20130413

* Mon Mar 18 2013 Miroslav Lichvar <mlichvar@redhat.com> 5.9-9.20130316
- update to 20130316
- include shared ncurses C++ libraries (#911540)

* Wed Jan 30 2013 Miroslav Lichvar <mlichvar@redhat.com> 5.9-8.20130126
- update to 20130126
- clear scrollback buffer in clear (#815790)
- make -base and -term subpackages noarch
- make some dependencies arch-specific

* Thu Oct 18 2012 Miroslav Lichvar <mlichvar@redhat.com> 5.9-7.20121017
- update to 20121017

* Mon Oct 15 2012 Miroslav Lichvar <mlichvar@redhat.com> 5.9-6.20121013
- update to 20121013
- move st entries to -base
- remove obsolete macros

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9-5.20120204
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 08 2012 Miroslav Lichvar <mlichvar@redhat.com> 5.9-4.20120204
- move libs and terms to /usr
- update to patch 20120204

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9-3.20110716
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Miroslav Lichvar <mlichvar@redhat.com> 5.9-2.20110716
- update to patch 20110716
- update rxvt-unicode entry

* Tue Apr 05 2011 Miroslav Lichvar <mlichvar@redhat.com> 5.9-1
- update to 5.9

* Tue Mar 22 2011 Miroslav Lichvar <mlichvar@redhat.com> 5.8-2.20110319
- update to patch 20110319

* Wed Mar 02 2011 Miroslav Lichvar <mlichvar@redhat.com> 5.8-1
- update to 5.8

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-11.20101211
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-10.20101211
- update to patch 20101211

* Mon Nov 29 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-9.20101128
- update to patch 20101128
- update rxvt-unicode entry (#653081)

* Wed Jul 14 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-8.20100703
- update to patch 20100703
- add README to base subpackage

* Wed Feb 03 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-7.20100130
- update to patch 20100130
- fix ncursesw5-config and pc files to use correct tinfo

* Mon Jan 25 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-6.20100123
- update to patch 20100123
- remove AS_NEEDED from linker scripts

* Wed Jan 20 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-5.20100116
- fix narrow/wide libtinfo compatibility
- fix wattrset macro to not produce warning with current gcc (#556645)

* Mon Jan 18 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-4.20100116
- update to patch 20100116
- don't require -ltinfo when linking with --no-add-needed

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-3.20090207
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-2.20090207
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Miroslav Lichvar <mlichvar@redhat.com> 5.7-1.20090207
- update to 5.7, patch 20090207
- use default pcf in xterm description
- include NEWS

* Thu Oct 02 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-20.20080927
- update to patch 20080927

* Wed Jul 23 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-19.20080628
- rebuild with new gpm

* Mon Jul 07 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-18.20080628
- update to patch 20080628
- move mlterm and screen.* entries to -base
- change kbs to ^? in rxvt and screen entries

* Mon May 26 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-17.20080524
- update to patch 20080524
- force installing wide libtinfo

* Fri Mar 07 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-16.20080301
- update to patch 20080301
- provide libtermcap.so (#428898)
- move all headers to /usr/include
- move libncursesw out of /usr
- make examples in documentation compilable (#436355)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.6-15.20080112
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-14.20080112
- obsolete libtermcap-devel (#428898)

* Mon Jan 14 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-13.20080112
- update to patch 20080112
- make -libs, -base, -term subpackages
- obsolete termcap and libtermcap
- update urxvt entry

* Tue Oct 16 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-12.20070812
- allocate additional working buffers in new_field (#310071)

* Wed Oct 10 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-11.20070812
- don't write beyond field buffer in form driver (#310071)

* Thu Oct 04 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-10.20070812
- fix comp_hash string output
- avoid comparing padding in cchar_t structure
- remove gawk from buildrequires

* Thu Aug 23 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-9.20070812
- rebuild
- buildrequire gawk

* Mon Aug 13 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-8.20070812
- update to patch 20070812

* Wed Jun 13 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-7.20070612
- update to patch 20070612

* Thu Mar 08 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-6.20070303
- update to patch 20070303
- use one libtinfo for both libncurses and libncursesw
- shorten -devel description

* Mon Feb 19 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-5.20070217
- update to patch 20070217
- replace libcurses.so symlink with linker script (#228891)

* Mon Feb 12 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-4.20070210
- update to patch 20070210
- generate separate terminfo library
- move static libraries to -static subpackage
- avoid unnecessary linking with libdl 

* Tue Feb 06 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-3.20070203
- update to patch 20070203
- spec cleanup (#226188)

* Sun Jan 21 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-2.20070120
- update to patch 20070120
- don't depend on bash, drop resetall script
- include rxvt-unicode description

* Wed Jan 10 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-1.20070106
- update to 5.6, patch 20070106

* Mon Dec 11 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-27.20061209
- update to patch 20061209
- strip large tables from shared libraries, reduce number of relocations
- package utils linked with libncurses instead of libncursesw
- package only wide-character headers

* Thu Nov 30 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-26.20060715
- move also hardlinked entries (#217750)
- search /etc/terminfo for local terminfo entries

* Mon Nov 27 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-25.20060715
- move libncurses and some terminfo entries out of /usr
- drop console symlink and sparc terminfo entries

* Thu Aug 31 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-24.20060715
- modify tgetstr to make screen happy (#202480)
- use CFLAGS when linking (#199369)
- change BuildRoot tag to comply with Fedora packaging guidelines

* Wed Aug 16 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-23.20060715
- fix another crash in tgetent (#202480)

* Mon Jul 17 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-22.20060715
- update to patch 20060715
- fix package summary (#197655)

* Sat Jul 08 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-21
- fix crash in tgetent (#198032)

* Fri Jul 07 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-20
- update to patch 20060701
- don't strip libraries, chmod +x them
- move .so links to devel package
- add gpm-devel to buildrequires
- spec cleanup

* Mon Feb 27 2006 Miroslav Lichvar <mlichvar@redhat.com> - 5.5-19
- avoid comparing padding in cchar_t structure (#182024)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.5-18.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.5-18.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Jindrich Novy <jnovy@redhat.com> 5.5-18
- add --with-chtype=long to avoid type clashes on x86_64 (#178824)
- spec cleanup

* Fri Jan 27 2006 Petr Raszyk <praszyk@redhat.com> 5.5-17
- Rebuild.

* Fri Jan 27 2006 Petr Raszyk <praszyk@redhat.com> 5.5-11
- According Henrik Nordstrom (hno@squid-cache.org)
  Diff between the two versions of curses.h on x86_64
  Patch ncurses-5.5-chtypeaslong2.patch
  See #178824

* Fri Dec 23 2005 Petr Raszyk <praszyk@redhat.com> 5.5-10
- Rebuild.

* Thu Dec 22 2005 Jindrich Novy <jnovy@redhat.com> 5.5-9
- helped Petr to strip libs. 

* Thu Dec 22 2005 Petr Raszyk <praszyk@redhat.com> 5.5-8
- Strip *.so libs.

* Wed Dec 21 2005 Petr Raszyk <praszyk@redhat.com> 5.5-1
- Upgrade to ncurses 5.5

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Dec 1 2005 Petr Raszyk <praszyk@redhat.com> 5.4-23
- Rebuild.

* Thu Dec 1 2005 Petr Raszyk <praszyk@redhat.com> 5.4-22
- Rebuild.

* Thu Dec 1 2005 Petr Raszyk <praszyk@redhat.com> 5.4-21
- Clear window after: filter()+'terminal-resizing'+endwin()
  doupdate()+endwin()
  See bug #174498, patch ncurses-5.4-endwinfilter.patch

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com> 5.4-20
- fix location for resize in ncurses-resetall.sh

* Fri Sep 30 2005 5.4-19 <praszyk@redhat.com> 5.4-19
- Clear window after: filter()+initscr()+endwin()+refresh()
  See bug #2966, patch ncurses-5.4-filter.patch

* Wed Aug 03 2005 Karsten Hopp <karsten@redhat.de> 5.4-18
- rebuild with new rpm

* Wed Apr 27 2005 Petr Rockai <prockai@redhat.com> - 5.4-17
- apply patch from Hans de Goede, fixing BR142659 [The
  terminfo data for kbs changed from \177 to ^H]

* Sun Mar 06 2005 Petr Rockai <prockai@redhat.com>
- rebuild

* Thu Jan 27 2005 Adrian Havill <havill@redhat.com> 5.4-15
- update to newest jumbo monthly patch + weeklies, fixing
  new line cursor move problem (#140326)

* Thu Oct 21 2004 Adrian Havill <havill@redhat.com> 5.4-14
- escape rpm macros in the changelog (#135408)

* Tue Aug 31 2004 Adrian Havill <havill@redhat.com> 5.4-13
- term.sh can't detect CJK environment; revert
- gt 2.7 behaves better with xterm-new

* Tue Aug  3 2004 Adrian Havill <havill@redhat.com> 5.4-12
- make xterm same as xterm-r6
- detect for "dumb" in term.sh

* Thu Jul 29 2004 Adrian Havill <havill@redhat.com> 5.4-11
- add latest rollup patches and weekly patches
- remove home/end patch, which is now included in latest
  terminfo.src and termcap.src
- add term.sh to /etc/profile.d, reference in /etc/bashrc
- modify term.sh to support rxvt (#122815 comment 93)

* Thu Jul 08 2004 Adrian Havill <havill@redhat.com> 5.4-10
- add home/end mappings to gnome definition (#122815)

* Tue Jul 06 2004 Adrian Havill <havill@redhat.com> 5.4-9.fc3
- n-v-r

* Tue Jul 06 2004 Adrian Havill <havill@redhat.com> 5.4-9.fc2
- n-v-r

* Tue Jul 06 2004 Adrian Havill <havill@redhat.com> 5.4-9
- remove terminfo try-to-please-all xterm hackery; it's now ptty
  and profile's job to point to the correct terminal. (#122815)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun May 30 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- remove ncurses-c++-devel rpm, all files are also part of ncurses-devel

* Sat May 29 2004 Joe Orton <jorton@redhat.com> 5.4-6
- fix xterm terminfo entry (Hans de Geode, #122815)

* Thu May 06 2004 Adrian Havill <havill@redhat.com> 5.4-5
- remove --with-gpm from configure, as it adds a pkg
  dependency (#122336) and causes too many problems vs its benefits

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Adrian Havill <havill@redhat.com> 5.4-3
- xterm-color is wrong for rh; inverted bs/del (#115499)

* Wed Feb 25 2004 Adrian Havill <havill@redhat.com> 5.4-3
- link "xterm" to "xterm-color" as temp fix for escape problem (#115448)
- remove old zcat for PATCH1

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 10 2004 Adrian Havill <havill@redhat.com> 5.4-1
- version update to 5.4

* Thu Jan 29 2004 Adrian Havill <havill@redhat.com> 5.3-10
- add /usr/include/ncursesw (#112979)
- allow for non-gzipped man pages during the build process

* Sun Sep 21 2003 Matt Wilson <msw@redhat.com> 5.3-9.3
- remove the elf32/elf64 provides/obsoletes

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 5.3-9.2
- rebuild to fix gzipped file md5sums (#91211)

* Thu Sep 11 2003 Adrian Havill <havill@redhat.com> 5.3-9.1
- RHEL bump

* Thu Sep 11 2003 Adrian Havill <havill@redhat.com> 5.3-9
- remove not-so safe-sprintf configure option because the code does
  not appear to be stable enough for some apps. (#103790)

* Wed Aug 20 2003 Adrian Havill <havill@redhat.com> 5.3-8.1
- RHEL bump

* Wed Aug 20 2003 Adrian Havill <havill@redhat.com> 5.3-8
- multilib patch (#91211)

* Mon Aug 11 2003 Adrian Havill <havill@redhat.com> 5.3-7
- fixed the safe sprintf code that was enabled in the previous release
  by the configure parameter. (#101486)

* Mon Jun 16 2003 Elliot Lee <sopwith@redhat.com> 5.3-6.1
- Fix ac25 patch, make it easy to turn off GPM support

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 22 2003 Adrian Havill <havill@redhat.com> 5.3-5
- added latest rollup patch with widec/UTF8 centric weekly (20030517)
- added --enable-widec to configure (#86311)
  original work done by Mr. Sam <sam@email-scan.com>
- require sharutils (#86605)
- add gpm, xmc support
- add debug syms back into package
- updated autoconf/configure patch

* Thu Feb  6 2003 Bill Nottingham <notting@redhat.com> 5.3-4
- fix debuginfo package

* Fri Jan 31 2003 Adrian Havill <havill@redhat.com> 5.3-3
- remunged xterm changes from 5.2 patch for 5.3
- updated screen entry (#82951)
- fixed ka3, kb2 and kf0 entries (#77506)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Adrian Havill <havill@redhat.com> 5.3-1
- upgrade to 5.3 for sake of utf-8, wide chars (#77585 ...)
- spec file summary/desc grammar (#73583)
- add Requires: for c++ devel subpkg (#74002)
- terminfo.src patches no longer needed
- adjust autoconf patch

* Thu Dec 05 2002 Elliot Lee <sopwith@redhat.com> 5.2-29
- Merge in multilib fixes

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr  8 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-26
- Remove duplicated files (#62752)
- Don't strip libraries (#60398)
- Remove cbt capability from xterm description (#61077)

* Mon Feb 25 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-25
- Remove bogus man pages
- Remove bool hack, it breaks make menuconfig

* Fri Feb 22 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-24
- Rebuild for glibc 2.3/gcc 3.1

* Fri Feb 22 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-23
- Put the bool type back in for !c++, but leave TRUE/FALSE out

* Thu Feb 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-21
- Don't define TRUE/FALSE etc., we don't care about SVR4 compliance and
  it breaks building gdb

* Thu Feb 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-20
- Rebuild for glibc 2.3/gcc 3.1

* Thu Feb 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-19
- Patchlevel 20020218
- Re-add %%{_includedir}/ncurses.h (#60169)

* Tue Feb 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-18
- Add C++ bindings (#59751)

* Tue Feb 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-17
- Patchlevel 20020209
- Fix zero-substitution of cf_cv_type_of_bool (#59450)
- Fix rebuilding of configure script with autoconf 2.5x

* Thu Jan 31 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-16
- Patchlevel 20020127

* Tue Nov 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-14
- Patchlevel 20011124

* Thu Sep 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-13
- Sync with patchlevel 20010908

* Fri Jul 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-12
- Sync terminfo with termcap 11.0.1-10

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-11
- Update to patchlevel 20010623, fixes some lynx issues

* Mon Jun 18 2001 Helge Deller <hdeller@redhat.de>
- fixed tput -S segfaulting bug (#44669)
- use _tmppath for BuildRoot:
- Copyright -> License

* Sun Apr 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to patchlevel 20010407

* Tue Mar  6 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up some terminfo entries containing includes to
  "/var/tmp/ncurses-root/something" (#30771)

* Thu Feb 22 2001 Harald Hoyer <harald@redhat.de>
- fixed rxvt backspace setting

* Fri Feb  9 2001 Yukihiro Nakai <ynakai@redhat.com>
- Update Japanese kterm patch

* Mon Jan 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update
- Add japanese patch from termcap
- Fix ospeed handling

* Mon Jan  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add libcurses.a -> libncurses.a symlink (RFE #23023)

* Tue Dec 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Use --with-ospeed='unsigned int'

* Fri Nov 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix alpha and ia64
- Rebuild with gcc 2.96-64

* Thu Nov  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.2
- Fix typo in man page (Bug #20205)
- update the "screen" terminfo entries to the version supplied with
  screen 3.9.8

* Mon Oct  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update (fixes the "make menuconfig" bug introduced by the security fix)

* Tue Oct  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix security problem (possible buffer overrun)

* Fri Aug  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add the bugfix patches from the ncurses maintainer

* Thu Jul 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.1

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Matt Wilson <msw@redhat.com>
- *don't ship symlinks from lib*.so.5 to lib*.so.4!
- use FHS macros

* Fri Jun  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild for 7.0
- /usr/share/man
- update URL for patches
- misc. fixes to spec file

* Mon Mar 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- use the real library version number
- update to 20000319

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Fri Feb 18 2000 Preston Brown <pbrown@redhat.com>
- xterm terminfo entries from XFree86 3.3.6
- final round of xterm fixes, follow debian policy.

* Sat Feb  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- strip libraries

* Thu Feb  3 2000 Bernhard Rosenkränzer <bero@redhat.com>
- More xterm fixes (Bug #9087)

* Thu Jan 27 2000 Bernhard Rosenkränzer <bero@redhat.com>
- More xterm fixes from Hans de Goede (Bug #8633)

* Sat Jan 15 2000 Bernhard Rosenkränzer <bero@redhat.com>
- remove some broken symlinks (leftovers from libncurses.so.5)
- Use %%configure (Bug #8484)

* Tue Jan 11 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Add xterm patch from Hans de Goede <hans@highrise.nl>
- Patch 20000108, this fixes a problem with a header file.

* Wed Jan  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Add 20000101 patch, hopefully finally fixing the xterm description

* Wed Dec 22 1999 Cristian Gafton <gafton@redhat.com>
- revert to the old major number - because the ABI is not changed (and we
  should be handling the changes via symbol versioning anyway)

* Fri Nov 12 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix a typo in spec
- Add the 19991006 patch, fixing some C++ STL compatibility problems.
- get rid of profiling and debugging versions - we need to save space...

* Thu Nov  4 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.0
- some spec cleanups to make updating easier
- add links *.so.5 to *.so.4 - they are fully binary compatible.
  (Why did they change the invocation number???)

* Wed Sep 22 1999 Cristian Gafton <gafton@redhat.com>
- make clean in the test dir - don't ship any binaries at all.

* Mon Sep 13 1999 Preston Brown <pbrown@redhat.com>
- fixed stripping of test programs.

* Sun Aug 29 1999 Preston Brown <pbrown@redhat.com>
- removed 'flash' capability for xterm; see bug #2820 for details.

* Fri Aug 27 1999 Cristian Gafton <gafton@redhat.com>
- add the resetall script from Marc Merlin <marc@merlins.org>

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- added iris-ansi-net as alias for iris-ansi (bug #2561)

* Fri Jul 30 1999 Michael K. Johnson <johnsonm@redhat.com>
- added ncurses-intro.hmtl and hackguide.html to -devel package [bug #3929]

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- make sure ALL binaries are stripped (incl. test binaries)

* Thu Mar 25 1999 Preston Brown <pbrown@redhat.com>
- made xterm terminfo stuff MUCH better.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 16)

* Sat Mar 13 1999 Cristian Gafton <gafton@redhat.com>
- fixed header for C++ compiles

* Fri Mar 12 1999 Jeff Johnson <jbj@redhat.com>
- add terminfo entries for linux/linux-m on sparc (obsolete termfile_sparc).

* Thu Feb 18 1999 Cristian Gafton <gafton@redhat.com>
- updated patchset from original site

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- don't build the C++ demo code
- update patch set to the current as of today (redid all the individual
  patches in a single one)

* Wed Oct 14 1998 Cristian Gafton <gafton@redhat.com>
- make sure to strip the binaries

* Wed Sep 23 1998 Cristian Gafton <gafton@redhat.com>
- added another zillion of patches. The spec file *is* ugly
- defattr

* Mon Jul 20 1998 Cristian Gafton <gafton@redhat.com>
- added lots of patches. This spec file is starting to look ugly

* Wed Jul 01 1998 Alan Cox <alan@redhat.com>
- Fix setuid trusting. Open termcap/info files as the real user.

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- added terminfo entry for the poor guys using lat1 and/or lat-2 on their
  consoles... Enjoy linux-lat ! Thanks, Erik !

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- new patch to get xterm-color and nxterm terminfo entries
- aliased them to rxvt, as that seems to satisfy everybody

* Sun Apr 12 1998 Cristian Gafton <gafton@redhat.com>
- added %%clean section

* Tue Apr 07 1998 Cristian Gafton <gafton@redhat.com>
- removed /usr/lib/terminfo symlink - we shouldn't need that

* Mon Apr 06 1998 Cristian Gafton <gafton@redhat.com>
- updated to 4.2 + patches
- added BuildRoot

* Sat Apr 04 1998 Cristian Gafton <gafton@redhat.com>
- rebuilt with egcs on alpha

* Wed Dec 31 1997 Erik Troan <ewt@redhat.com>
- version 7 didn't rebuild properly on the Alpha somehow -- no real changes
  are in this version

* Tue Dec 09 1997 Erik Troan <ewt@redhat.com>
- TIOCGWINSZ wasn't used properly

* Tue Jul 08 1997 Erik Troan <ewt@redhat.com>
- built against glibc, linked shared libs against -lc

