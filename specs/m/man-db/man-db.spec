# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global cache /var/cache/man

Summary: Tools for searching and reading man pages
Name: man-db
Version: 2.13.1
Release: 3%{?dist}
# GPLv2+ .. man-db
# GPLv3+ .. gnulib
License: GPL-2.0-or-later AND GPL-3.0-or-later
URL: http://www.nongnu.org/man-db/

Source0: http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.xz
Source1: http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.xz.asc
# Man-db GPG key is stored in a different name which makes it hard to fetch
# It was downloaded here: https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xac0a4ff12611b6fccf01c111393587d97d86500b
Source2: 0xac0a4ff12611b6fccf01c111393587d97d86500b

Source3: man-db.crondaily
Source4: man-db.sysconfig
Source5: man-db-cache-update.service
Source6: man-db-restart-cache-update.service

Obsoletes: man < 2.0
Provides: man = %{version}
Provides: man-pages-reader = %{version}
# FPC exception for gnulib - copylib - https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib)

Requires: coreutils, grep, groff-base, gzip, less
BuildRequires: make
BuildRequires: gcc
BuildRequires: systemd
BuildRequires: gdbm-devel, gettext, groff, less, libpipeline-devel, zlib-devel
BuildRequires: po4a, perl-interpreter, perl-version
BuildRequires: gnupg2
Recommends: glibc-gconv-extra

Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Requires(preun): %{_sbindir}/update-alternatives

%description
The man-db package includes five tools for browsing man-pages:
man, whatis, apropos, manpath and lexgrog. man formats and displays
manual pages. whatis searches the manual page names. apropos searches the
manual page names and descriptions. manpath determines search path
for manual pages. lexgrog directly reads header information in
manual pages.

%package cron
Summary: Periodic update of man-db cache

Requires: %{name} = %{version}-%{release}
Requires: crontabs

BuildArch: noarch

%description cron
This package provides periodic update of man-db cache.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
%configure \
    --with-sections="1 1p 8 2 3 3p 3pm 4 5 6 7 9 0p n l p o 1x 2x 3x 4x 5x 6x 7x 8x" \
    --disable-setuid --disable-cache-owner \
    --with-systemdsystemunitdir=no \
    --with-browser=elinks --with-lzip=lzip \
    --with-snapdir=/var/lib/snapd/snap \
    --with-override-dir=overrides
%make_build CC="%{__cc} %{optflags}"

%check
make check

%install
%make_install prefix=%{_prefix}

# rename files for alternative usage
for f in man apropos whatis; do
    mv %{buildroot}%{_bindir}/$f %{buildroot}%{_bindir}/$f.%{name}
    touch %{buildroot}%{_bindir}/$f
    mv %{buildroot}%{_mandir}/man1/$f.1 %{buildroot}%{_mandir}/man1/$f.%{name}.1
    touch %{buildroot}%{_mandir}/man1/$f.1
done

# move the documentation to the relevant place
mv $RPM_BUILD_ROOT%{_datadir}/doc/man-db/* ./

# remove zsoelim man page - part of groff package
rm $RPM_BUILD_ROOT%{_datadir}/man/man1/zsoelim.1

# remove libtool archives
rm $RPM_BUILD_ROOT%{_libdir}/man-db/*.la

# install cache directory
install -d -m 0755  $RPM_BUILD_ROOT%{cache}

# install cron script for man-db creation/update
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
install -D -p -m 0755 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/man-db.cron

# config for cron script
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -D -p -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/man-db

# config for tmpfiles.d
install -D -p -m 0644 init/systemd/man-db.conf $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/.

# man-db-cache-update.service and man-db-restart-cache-update.service
install -D -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_unitdir}/man-db-cache-update.service
install -D -p -m 0644 %{SOURCE6} $RPM_BUILD_ROOT%{_unitdir}/man-db-restart-cache-update.service

%find_lang %{name}
%find_lang %{name}-gnulib

%pre
# remove alternativized files if they are not symlinks
for f in man apropos whatis; do
    [ -L %{_bindir}/$f ] || %{__rm} -f %{_bindir}/$f >/dev/null 2>&1 || :
    [ -L %{_mandir}/man1/$f.1.gz ] || %{__rm} -f %{_mandir}/man1/$f.1.gz >/dev/null 2>&1 || :
done

# stop and disable timer from previous builds
if [ -e /usr/lib/systemd/system/mandb.timer ]; then
    if test -d /run/systemd; then
        systemctl stop man-db.timer >/dev/null 2>&1 || :
        systemctl -q disable man-db.timer >/dev/null 2>&1 || :
    fi
fi

%post
# set up the alternatives files
%{_sbindir}/update-alternatives --install %{_bindir}/man man %{_bindir}/man.%{name} 300 \
    --slave %{_bindir}/apropos apropos %{_bindir}/apropos.%{name} \
    --slave %{_bindir}/whatis whatis %{_bindir}/whatis.%{name} \
    --slave %{_mandir}/man1/man.1.gz man.1.gz %{_mandir}/man1/man.%{name}.1.gz \
    --slave %{_mandir}/man1/apropos.1.gz apropos.1.gz %{_mandir}/man1/apropos.%{name}.1.gz \
    --slave %{_mandir}/man1/whatis.1.gz whatis.1.gz %{_mandir}/man1/whatis.%{name}.1.gz \
    >/dev/null 2>&1 || :

# clear the old cache
%{__rm} -rf %{cache}/* >/dev/null 2>&1 || :

%preun
if [ $1 -eq 0 ]; then
    %{_sbindir}/update-alternatives --remove man %{_bindir}/man.%{name} >/dev/null 2>&1 || :
fi

%postun
if [ $1 -ge 1 ]; then
    if [ "$(readlink %{_sysconfdir}/alternatives/man)" == "%{_bindir}/man.%{name}" ]; then
        %{_sbindir}/update-alternatives --set man %{_bindir}/man.%{name} >/dev/null 2>&1 || :
    fi
fi

%transfiletriggerin -- %{_mandir}
# update cache
if [ -x /usr/bin/systemd-run -a -x /usr/bin/systemctl ]; then
    /usr/bin/systemd-run /usr/bin/systemctl start man-db-cache-update >/dev/null 2>&1 || :
fi

%transfiletriggerpostun -- %{_mandir}
# update cache
if [ -x /usr/bin/systemd-run -a -x /usr/bin/systemctl ]; then
    /usr/bin/systemd-run /usr/bin/systemctl start man-db-cache-update >/dev/null 2>&1 || :
fi

%files -f %{name}.lang -f %{name}-gnulib.lang
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README.md man-db-manual.txt man-db-manual.ps ChangeLog NEWS.md
%config(noreplace) %{_sysconfdir}/man_db.conf
%config(noreplace) %{_sysconfdir}/sysconfig/man-db
%config(noreplace) %{_tmpfilesdir}/man-db.conf
%{_unitdir}/man-db-cache-update.service
%{_unitdir}/man-db-restart-cache-update.service
%{_sbindir}/accessdb
%ghost %{_bindir}/man
%ghost %{_bindir}/apropos
%ghost %{_bindir}/whatis
%{_bindir}/man.%{name}
%{_bindir}/apropos.%{name}
%{_bindir}/whatis.%{name}
%{_bindir}/man-recode
%{_bindir}/manpath
%{_bindir}/lexgrog
%{_bindir}/catman
%{_bindir}/mandb
%dir %{_libdir}/man-db
%{_libdir}/man-db/*.so
%dir %{_libexecdir}/man-db
%{_libexecdir}/man-db/globbing
%{_libexecdir}/man-db/manconv
%{_libexecdir}/man-db/zsoelim
%verify(not mtime) %dir %{cache}
# documentation and translation
%ghost %{_mandir}/man1/man.1*
%ghost %{_mandir}/man1/apropos.1*
%ghost %{_mandir}/man1/whatis.1*
%{_mandir}/man1/man.%{name}.1*
%{_mandir}/man1/apropos.%{name}.1*
%{_mandir}/man1/whatis.%{name}.1*
%{_mandir}/man1/man-recode.1*
%{_mandir}/man1/lexgrog.1*
%{_mandir}/man1/manconv.1*
%{_mandir}/man1/manpath.1*
%{_mandir}/man5/manpath.5*
%{_mandir}/man8/accessdb.8*
%{_mandir}/man8/catman.8*
%{_mandir}/man8/mandb.8*
%lang(da)       %{_datadir}/man/da/man*/*
%lang(de)       %{_datadir}/man/de/man*/*
%lang(es)       %{_datadir}/man/es/man*/*
%lang(fr)       %{_datadir}/man/fr/man*/*
%lang(id)       %{_datadir}/man/id/man*/*
%lang(it)       %{_datadir}/man/it/man*/*
%lang(ja)       %{_datadir}/man/ja/man*/*
%lang(ko)	%{_datadir}/man/ko/man*/*
%lang(nl)       %{_datadir}/man/nl/man*/*
%lang(pl)       %{_datadir}/man/pl/man*/*
%lang(pt)       %{_datadir}/man/pt/man*/*
%lang(pt_BR)    %{_datadir}/man/pt_BR/man*/*
%lang(ro)       %{_datadir}/man/ro/man*/*
%lang(ru)       %{_datadir}/man/ru/man*/*
%lang(sr)       %{_datadir}/man/sr/man*/*
%lang(sv)       %{_datadir}/man/sv/man*/*
%lang(tr)       %{_datadir}/man/tr/man*/*
%lang(zh_CN)    %{_datadir}/man/zh_CN/man*/*
%lang(uk)	%{_datadir}/man/uk/man*/*

%files cron
%config(noreplace) %{_sysconfdir}/cron.daily/man-db.cron

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 05 2025 Lukas Javorsky <ljavorsk@redhat.com> - 2.13.1-1
- Rebase to version 2.13.1

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 29 2024 Packit <hello@packit.dev> - 2.13.0-1
- Update to version 2.13.0
- Resolves: rhbz#2308476

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 08 2024 Lukas Javorsky <ljavorsk@redhat.com> - 2.12.1-1
- Rebase to version 2.12.1

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 10 2023 Lukas Javorsky <ljavorsk@redhat.com> - 2.12.0-3
- Fix the Source numbering in installation
- Resolves: BZ#2242757

* Fri Sep 29 2023 Lukas Javorsky <ljavorsk@redhat.com> - 2.12.0-2
- Add GPG verify on the package

* Wed Sep 27 2023 Lukas Javorsky <ljavorsk@redhat.com> - 2.12.0-1
- Rebase to version 2.12.0
- Patch0 was upstreamed

* Tue Jul 25 2023 Lukas Javorsky <ljavorsk@redhat.com> - 2.11.2-5
- Release bump after added Patch0 from yselkowitz

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Lukas Javorsky <ljavorsk@redhat.com> - 2.11.2-3
- Add Recommends to package glibc-gconv-extra
- Justification in BZ#2182414

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Lukas Javorsky <ljavorsk@redhat.com> - 2.11.2-1
- Rebase to version 2.11.2

* Fri Nov 18 2022 Lukas Javorsky <ljavorsk@redhat.com> - 2.11.1-1
- Rebase to version 2.11.1
- Add Korean translations
- Resolves: #2142761

* Fri Oct 14 2022 Lukas Javorsky <ljavorsk@redhat.com> - 2.11.0-1
- Rebase to version 2.11.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 18 2022 Nikola Forró <nforro@redhat.com> - 2.10.2-1
- update to 2.10.2
  resolves: #2065447

* Fri Feb 11 2022 Nikola Forró <nforro@redhat.com> - 2.10.1-1
- update to 2.10.1
  resolves #2053020

* Tue Feb 08 2022 Nikola Forró <nforro@redhat.com> - 2.10.0-3
- backport upstream fixes for the unstable test

* Tue Feb 08 2022 Nikola Forró <nforro@redhat.com> - 2.10.0-2
- skip unstable test

* Sun Feb 06 2022 Nikola Forró <nforro@redhat.com> - 2.10.0-1
- update to 2.10.0
  resolves #2050778

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 11 2021 Nikola Forró <nforro@redhat.com> - 2.9.4-1
- update to 2.9.4
  resolves #1926527

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 09 2020 Jeff Law <law@redhat.com> - 2.9.3-2
- Re-enable LTO

* Tue Oct 06 2020 Nikola Forró <nforro@redhat.com> - 2.9.3-1
- update to 2.9.3
  resolves #1849809

* Thu Sep 03 2020 Nikola Forró <nforro@redhat.com> - 2.9.2-6
- disable LTO to workaround a possible linker bug
  related to #1871971

* Tue Aug 04 2020 Nikola Forró <nforro@redhat.com> - 2.9.2-5
- reenable LTO

* Tue Jul 28 2020 Nikola Forró <nforro@redhat.com> - 2.9.2-4
- disable LTO to avoid linker bug

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 2.9.2-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jun 02 2020 Nikola Forró <nforro@redhat.com> - 2.9.2-1
- update to 2.9.2
  resolves #1842624

* Sun Mar 01 2020 Nikola Forró <nforro@redhat.com> - 2.9.1-6
- fix %pre scriptlet

* Fri Feb 28 2020 Nikola Forró <nforro@redhat.com> - 2.9.1-5
- fix upgrades from non-alternativized versions properly

* Fri Feb 28 2020 Nikola Forró <nforro@redhat.com> - 2.9.1-4
- fix upgrades from non-alternativized versions

* Wed Feb 26 2020 Nikola Forró <nforro@redhat.com> - 2.9.1-3
- fix %postun scriptlet

* Wed Feb 26 2020 Nikola Forró <nforro@redhat.com> - 2.9.1-2
- use alternatives for man, apropos and whatis

* Wed Feb 26 2020 Nikola Forró <nforro@redhat.com> - 2.9.1-1
- update to 2.9.1
  resolves #1807144

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Nikola Forró <nforro@redhat.com> - 2.9.0-1
- update to 2.9.0
  resolves #1764582

* Fri Sep 27 2019 Nikola Forró <nforro@redhat.com> - 2.8.7-2
- schedule interrupted cache update for the next boot, instead of blocking
  system reboot/shutdown
  resolves #1678464

* Fri Aug 30 2019 Nikola Forró <nforro@redhat.com> - 2.8.7-1
- update to 2.8.7
  resolves #1747042

* Tue Aug 27 2019 Nikola Forró <nforro@redhat.com> - 2.8.6.1-1
- update to 2.8.6.1
  resolves #1742475

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 07 2019 Nikola Forró <nforro@redhat.com> - 2.8.4-3
- prioritize POSIX man pages over perl manuals
  resolves #1663919

* Wed Nov 07 2018 Nikola Forró <nforro@redhat.com> - 2.8.4-2
- get rid of hardcoded path

* Mon Jul 30 2018 Nikola Forró <nforro@redhat.com> - 2.8.4-1
- update to 2.8.4
  resolves #1609438

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.8.3-3
- Rebuild for new gdbm

* Fri Apr 06 2018 Nikola Forró <nforro@redhat.com> - 2.8.3-2
- fix version in the name of change-owner-of-man-cache patch

* Fri Apr 06 2018 Nikola Forró <nforro@redhat.com> - 2.8.3-1
- update to 2.8.3
  resolves #1564220

* Tue Feb 20 2018 Nikola Forró <nforro@redhat.com> - 2.7.6.1-15
- add missing gcc build dependency

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Todd Zullinger <tmz@pobox.com> - 2.7.6.1-13
- Avoid noisy output from man-db-cache-update triggers

* Tue Jan 16 2018 Jiri Kucera <jkucera@redhat.com> - 2.7.6.1-12
- fix segmentation fault caused by 'man -D?'
  resolves: #1495507

* Tue Jan 16 2018 Nikola Forró <nforro@redhat.com> - 2.7.6.1-11
- rebuild with gdbm-1.14

* Tue Dec 19 2017 Nikola Forró <nforro@redhat.com> - 2.7.6.1-10
- fix failure of man-db-cache-update service when configured not to run
  resolves: #1526715

* Tue Nov 21 2017 Nikola Forró <nforro@redhat.com> - 2.7.6.1-9
- allow configuration of man-db-cache-update service through sysconfig
  resolves: #1514909

* Tue Nov 21 2017 Nikola Forró <nforro@redhat.com> - 2.7.6.1-8
- set group of /var/cache/man to root and drop setgid bit
  resolves: #1515823

* Thu Nov 16 2017 Nikola Forró <nforro@redhat.com> - 2.7.6.1-7
- make file trigger scriptlets not to fail in case systemd is unavailable
- drop systemd dependency

* Wed Nov 08 2017 Nikola Forró <nforro@redhat.com> - 2.7.6.1-6
- run cache update in a transient service using systemd-run
  resolves #1318058

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Nikola Forró <nforro@redhat.com> - 2.7.6.1-2
- set owner of man cache to root instead of man

* Thu Jan 19 2017 Nikola Forró <nforro@redhat.com> - 2.7.6.1-1
- update to 2.7.6.1
  resolves #1403618

* Mon Mar 14 2016 Nikola Forró <nforro@redhat.com> - 2.7.5-3
- suppress potential locale warning when installing with glibc-minimal-langpack
  resolves #1314633

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Nikola Forró <nforro@redhat.com> - 2.7.5-1
- update to 2.7.5
  resolves #1279867

* Tue Oct 13 2015 Nikola Forró <nforro@redhat.com> - 2.7.4-2
- add cron subpackage

* Tue Oct 13 2015 Nikola Forró <nforro@redhat.com> - 2.7.4-1
- update to 2.7.4
  resolves #1270078

* Mon Sep 21 2015 Nikola Forró <nforro@redhat.com> - 2.7.3-3
- fix replace.sed prerequisite syntax
  resolves #1263930

* Thu Sep 10 2015 Nikola Forró <nforro@redhat.com> - 2.7.3-2
- use file triggers instead of crontabs for updating cache

* Thu Sep 10 2015 Nikola Forró <nforro@redhat.com> - 2.7.3-1
- update to 2.7.3
  resolves #1261678

* Mon Aug 24 2015 Nikola Forró <nforro@redhat.com> - 2.7.2-3
- try to get terminal width from /dev/tty
  resolves #1255930

* Mon Aug 24 2015 Nikola Forró <nforro@redhat.com> - 2.7.2-2
- rebuilt with latest libpipeline

* Mon Aug 24 2015 Nikola Forró <nforro@redhat.com> - 2.7.2-1
- update to 2.7.2
  resolves #1256177

* Tue Aug 04 2015 Nikola Forró <nforro@redhat.com> - 2.7.1-8
- fix inaccurate description of "man -f"
  resolves #1249377

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 jchaloup <jchaloup@redhat.com> - 2.7.1-6
- Test for /run/systemd only if mandb.timer is actually installed
  resolves: #1223244

* Tue May 12 2015 Colin Walters <walters@redhat.com> - 2.7.1-5
- Test for /run/systemd to detect systemd state rather than invoking
  rpm in % pre - it is not really supported by rpm.

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.7.1-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Jan 02 2015 jchaloup <jchaloup@redhat.com> - 2.7.1-3
- switching back to crontabs
  resolves: #1177993
  resolves: #1171450
- rpm verify reports for /var/cache/man
  resolves: #1173496

* Thu Nov 13 2014 jchaloup <jchaloup@redhat.com> - 2.7.1-2
- src/man.c (do_extern): Pass the -l option through
  resolves: #1161747

* Wed Nov 12 2014 jchaloup <jchaloup@redhat.com> - 2.7.1-1
- update to 2.7.1
  resolves: #1163167

* Wed Oct 15 2014 jchaloup <jchaloup@redhat.com> - 2.7.0.2-5
- switch man and root in init/systemd/man-db.conf
  related: #1151558

* Mon Oct 13 2014 jchaloup <jchaloup@redhat.com> - 2.7.0.2-4
- preun missing condition on number of man-db packages installed
  related: #1151558

* Sun Oct 12 2014 jchaloup <jchaloup@redhat.com> - 2.7.0.2-3
- remove executable flag for *.service and *.timer file
  resolves: #1151558

* Wed Oct 08 2014 jchaloup <jchaloup@redhat.com> - 2.7.0.2-2
- replacing cron with systemd.timer
  resolves: #1148559
- adding zsoelim to {_libexecdir}/man-db/zsoelim
  related: #1145493

* Wed Oct 08 2014 jchaloup <jchaloup@redhat.com> - 2.7.0.2-1
- Update to 2.7.0.2
  resolves: #1145493

* Thu Sep 18 2014 jchaloup <jchaloup@redhat.com> - 2.6.7.1-7
- resolves: #1043401
  Don't store canonicalised versions of manpath elements

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.6.7.1-5
- fix license handling

* Tue Jul 01 2014 jchaloup <jchaloup@redhat.com> - 2.6.7.1-4
- related: #1110274
  swapping root for man in man-db.conf

* Wed Jun 25 2014 jchaloup <jchaloup@redhat.com> - 2.6.7.1-3
- resolves: #1110274
  Add systemd tmpfiles snippet to clean up old cat files after (upstream patch)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Peter Schiffer <pschiffe@redhat.com> - 2.6.7.1-1
- resolves: #1087279
  updated to 2.6.7.1

* Wed Feb 19 2014 Peter Schiffer <pschiffe@redhat.com> - 2.6.6-1
- resolves: #1057495
  updated to 2.6.6

* Wed Aug 07 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 2.6.5-3
- Add a missing requirement on crontabs to spec file
- Mark the cron job as config(noreplace)
- Fix RHBZ#989077

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 27 2013 Peter Schiffer <pschiffe@redhat.com> - 2.6.5-1
- updated to 2.6.5

* Tue Jun 25 2013 Peter Schiffer <pschiffe@redhat.com> - 2.6.4-1
- resolves: #977255
  updated to 2.6.4

* Mon Apr  8 2013 Peter Schiffer <pschiffe@redhat.com> - 2.6.3-6
- resolves: #948695
  fixed double free
- fixed certain man pages to match options with --help and --usage

* Thu Mar 21 2013 Peter Schiffer <pschiffe@redhat.com> - 2.6.3-5
- temporarily disabled one unstable unit test

* Thu Mar 21 2013 Peter Schiffer <pschiffe@redhat.com> - 2.6.3-4
- fixed some compiler warnings and memory leaks

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.3-2
- resolves: #870680
  use less as the default pager

* Wed Oct 24 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.3-1
- resolves: #858577
  updated to 2.6.3
- cleaned .spec file
- resolves: #855632
  fixed SIGABRT crash
- adds support for man-pages-overrides

* Tue Jul 31 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.2-5
- resolves: #841431
  ignore cached man pages if they don't exist anymore

* Fri Jul 20 2012 Dan Horák <dan[at]danny.cz> - 2.6.2-4
- fully patch the autotools files, fixes FTBFS due updated automake

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.2-2
- resolves: #829553
  clear the old man cache on install or update

* Tue Jul 10 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.2-1
- resolves: #833312
  update to 2.6.2
- resolves: #657409
  fixed warning when invoking col by the mandb program in cron
- resolves: #829935
  enabled support for man pages compressed with lzip
- resolves: #821778
  added virtual provides for bundled gnulib library
- resolves: #824825
  apropos returns correct exit code for invalid man page

* Tue Apr 24 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.1-4
- related: #693458
  updated patch for .so links because previous one wasn't working very well

* Tue Apr 24 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.1-3
- added autoconf, automake, libtool and gettext-devel to the build requires

* Tue Apr 24 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.1-2
- resolves: #677669
  added support for wildcards in path
- resolves: #693458
  fixed error with .so links

* Thu Apr 05 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.1-1
- resolves: #790771
  update to 2.6.1
- resolves: #806086
  removed hard-dependency on cron, update man db after install or update

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 05 2011 Peter Schiffer <pschiffe@redhat.com> - 2.6.0.2-3
- resolves: #702904
  fixed double free or corruption issue
- resolves: #739207
  require groff-base instead of groff
- rebuilt for gdbm-1.9.1-1

* Sun May 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.6.0.2-2
- Own the %%{_libdir}/man-db dir.

* Thu Apr 21 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 2.6.0.2-1
- update to 2.6.0.2
- remove obsolete patches
- add libpipe dependency

* Wed Mar 23 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.9-6
- Build with zlib support.
- Use elinks as default HTML browser.
   thanks Ville Skyttä

* Wed Mar 23 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.9-5
* Resolves: #684977
  backport upstream patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.9-3
- Resolves: #659292
  use ionice in man cron job

* Wed Nov 24 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.9-2
- Resolves: #655385 - use old format of nroff output

* Mon Nov 22 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.9-1
- update to 2.5.9

* Fri Oct  1 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.7-8
- add less buildrequire

* Wed Sep 29 2010 jkeating - 2.5.7-7
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.7-6
- Resolves: #630506 (change the description)
- minor spec file changes

* Mon Aug 30 2010 Dennis Gilmore <dennis@ausil.us> - 2.5.7-5
- Provide Versioned man

* Mon Aug 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.7-4
- remove obsolete conflict flag

* Mon Aug 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.7-3
- provides man tag
- resolves: #621688
  remove problematic man-pages (now in man-pages-de package)

* Fri Apr 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.7-2
- add conflicts tag

* Wed Feb 17 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.7-1
- initial build
