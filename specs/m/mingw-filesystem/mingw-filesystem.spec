# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Define before mingw-binutils is build
%bcond_with bootstrap

%global debug_package %{nil}

# Place RPM macros in %%{_rpmconfigdir}/macros.d if it exists (RPM 4.11+)
# Otherwise, use %%{_sysconfdir}/rpm
# https://lists.fedoraproject.org/pipermail/devel/2014-January/195026.html
%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Name:           mingw-filesystem
Version:        151
Release:        1%{?dist}
Summary:        MinGW cross compiler base filesystem and environment

License:        GPL-2.0-or-later
URL:            http://fedoraproject.org/wiki/MinGW
BuildArch:      noarch

Source0:        COPYING
Source1:        macros.mingw
Source2:        macros.mingw32
Source3:        macros.mingw64
Source4:        macros.ucrt64
Source5:        mingw32.sh
Source6:        mingw64.sh
Source7:        ucrt64.sh
Source8:        mingw-find-debuginfo.sh
Source9:        mingw.req
Source10:       mingw.prov
Source11:       mingw-scripts.sh
Source12:       mingw-rpmlint.config
Source13:       toolchain-mingw32.cmake
Source14:       toolchain-mingw64.cmake
Source15:       toolchain-ucrt64.cmake
Source16:       mingw-find-lang.sh
Source17:       mingw32.attr
Source18:       mingw64.attr
Source19:       ucrt64.attr
Source20:       toolchain-mingw32.meson
Source21:       toolchain-mingw64.meson
Source22:       toolchain-ucrt64.meson
Source23:       pkgconf-personality-mingw32
Source24:       pkgconf-personality-mingw64
Source25:       pkgconf-personality-ucrt64
Source26:       mingw32-hostlib.conf
Source27:       mingw64-hostlib.conf

# Taken from the Fedora filesystem package
Source101:      https://fedorahosted.org/filesystem/browser/lang-exceptions
Source102:      iso_639.sed
Source103:      iso_3166.sed

BuildRequires:  make
BuildRequires:  iso-codes
BuildRequires:  pkgconf


%description
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW


%package base
Summary:        Generic files which are needed for {mingw32,mingw64,ucrt64}-filesystem

# We need this for cmake macros
Requires:       cmake-rpm-macros
Requires:       redhat-rpm-config
# Obsolete the packages from the test repo
Obsoletes:      cross-filesystem < 67-2
Obsoletes:      cross-filesystem-scripts < 67-2
Obsoletes:      mingw-filesystem < 75-2
Obsoletes:      mingw-filesystem-scripts < 75-2
# For using pkgconf with MinGW
Requires:       pkgconf

%description base
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW


%package -n mingw32-filesystem
Summary:        MinGW cross compiler base filesystem and environment for the win32 target
Requires:       %{name}-base = %{version}-%{release}
# Replace mingw32-pkg-config
Conflicts:      mingw32-pkg-config < 0.28-17
Obsoletes:      mingw32-pkg-config < 0.28-17
Provides:       mingw32-pkg-config = 0.28-17
%if %{without bootstrap}
Requires:       mingw-binutils-generic
%endif

%description -n mingw32-filesystem
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW


%package -n mingw64-filesystem
Summary:        MinGW cross compiler base filesystem and environment for the win64 target
Requires:       %{name}-base = %{version}-%{release}
# Replace mingw64-pkg-config
Conflicts:      mingw64-pkg-config < 0.28-17
Obsoletes:      mingw64-pkg-config < 0.28-17
Provides:       mingw64-pkg-config = 0.28-17
%if %{without bootstrap}
Requires:       mingw-binutils-generic
%endif

%description -n mingw64-filesystem
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW


%package -n ucrt64-filesystem
Summary:        MinGW cross compiler base filesystem and environment for the win64 UCRT target
Requires:       %{name}-base = %{version}-%{release}
# Replace ucrt64-pkg-config
Conflicts:      ucrt64-pkg-config < 0.28-17
Obsoletes:      ucrt64-pkg-config < 0.28-17
Provides:       ucrt64-pkg-config = 0.28-17
%if %{without bootstrap}
Requires:       mingw-binutils-generic
%endif

%description -n ucrt64-filesystem
This package contains the base filesystem layout, RPM macros and
environment for all Fedora MinGW packages.

This environment is maintained by the Fedora MinGW SIG at:

  http://fedoraproject.org/wiki/SIGs/MinGW


%prep
%setup -q -c -T
cp %{SOURCE0} COPYING


%build
# nothing


%install
mkdir -p %{buildroot}%{_libexecdir}
install -m 755 %{SOURCE11} %{buildroot}%{_libexecdir}/mingw-scripts

mkdir -p %{buildroot}%{_bindir}
pushd %{buildroot}%{_bindir}
for i in mingw32-configure mingw32-cmake mingw32-make mingw32-meson mingw32-pkg-config \
         mingw64-configure mingw64-cmake mingw64-make mingw64-meson mingw64-pkg-config \
         ucrt64-configure ucrt64-cmake ucrt64-make ucrt64-meson ucrt64-pkg-config ; do
  ln -s %{_libexecdir}/mingw-scripts $i
done
for i in i686-w64-mingw32-pkg-config  \
         x86_64-w64-mingw32-pkg-config \
         x86_64-w64-mingw32ucrt-pkg-config ; do
  ln -s %{_bindir}/pkgconf $i
done
popd

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/profile.d/
install -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/profile.d/
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/profile.d/

mkdir -p %{buildroot}%{macrosdir}
install -m 644 %{SOURCE1} %{buildroot}%{macrosdir}/macros.mingw
install -m 644 %{SOURCE2} %{buildroot}%{macrosdir}/macros.mingw32
install -m 644 %{SOURCE3} %{buildroot}%{macrosdir}/macros.mingw64
install -m 644 %{SOURCE4} %{buildroot}%{macrosdir}/macros.ucrt64

mkdir -p %{buildroot}%{_sysconfdir}/rpmlint
install -m 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/rpmlint/

for target in i686-w64-mingw32 x86_64-w64-mingw32 x86_64-w64-mingw32ucrt; do
  # Create the folders required for gcc and binutils
  mkdir -p %{buildroot}%{_prefix}/$target
  mkdir -p %{buildroot}%{_prefix}/$target/bin
  mkdir -p %{buildroot}%{_prefix}/$target/lib

  # The MinGW system root which will contain Windows native binaries
  # and Windows-specific header files, pkgconfig, etc.
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/bin
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/etc
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/include
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/include/sys
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/lib
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/lib/pkgconfig
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/lib/cmake
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/libexec
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/libexec/installed-tests
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/sbin

  # We don't normally package manual pages and info files, except
  # where those are not supplied by a Fedora native package.  So we
  # need to create the directories.
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share/doc
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share/info
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share/man
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share/man/man{1,2,3,4,5,6,7,8,l,n}
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share/aclocal
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share/themes
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share/cmake
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share/locale
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share/pkgconfig
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share/xml
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share/icons
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share/metainfo
  mkdir -p %{buildroot}%{_prefix}/$target/sys-root/mingw/share/installed-tests

  mkdir -p %{buildroot}%{_prefix}/lib/debug/%{_prefix}/$target
done

# Own folders for all locales
# Snippet taken from the Fedora filesystem package
sed -n -f %{SOURCE102} /usr/share/xml/iso-codes/iso_639.xml > %{buildroot}/iso_639.tab
sed -n -f %{SOURCE103} /usr/share/xml/iso-codes/iso_3166.xml > %{buildroot}/iso_3166.tab

grep -v "^$" %{buildroot}/iso_639.tab | grep -v "^#" | while read a b c d ; do
    [[ "$d" =~ "^Reserved" ]] && continue
    [[ "$d" =~ "^No linguistic" ]] && continue

    locale=$c
    if [ "$locale" = "XX" ]; then
        locale=$b
    fi
    echo "%lang(${locale}) %{_prefix}/i686-w64-mingw32/sys-root/mingw/share/locale/${locale}" >> filelist_mingw32
    echo "%lang(${locale}) %{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/locale/${locale}" >> filelist_mingw64
    echo "%lang(${locale}) %{_prefix}/x86_64-w64-mingw32ucrt/sys-root/mingw/share/locale/${locale}" >> filelist_ucrt
done

cat %{SOURCE101} | grep -v "^#" | grep -v "^$" | while read loc ; do
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
        grep -Eq "[[:space:]]${locale%%_*}[[:space:]]" %{buildroot}/iso_639.tab || continue
    fi
    echo "%lang(${locale}) %{_prefix}/i686-w64-mingw32/sys-root/mingw/share/locale/${loc}" >> filelist_mingw32
    echo "%lang(${locale}) %{_prefix}/x86_64-w64-mingw32/sys-root/mingw/share/locale/${loc}" >> filelist_mingw64
    echo "%lang(${locale}) %{_prefix}/x86_64-w64-mingw32ucrt/sys-root/mingw/share/locale/${loc}" >> filelist_ucrt
done

rm -f %{buildroot}/iso_639.tab
rm -f %{buildroot}/iso_3166.tab

cat filelist_mingw32 filelist_mingw64 filelist_ucrt | grep "locale" | while read a b ; do
    mkdir -p -m 755 %{buildroot}/$b/LC_MESSAGES
done

# NB. NOT _libdir
mkdir -p %{buildroot}/usr/lib/rpm
install -m 0755 %{SOURCE8} %{buildroot}%{_rpmconfigdir}
install -m 0755 %{SOURCE9} %{buildroot}%{_rpmconfigdir}
install -m 0755 %{SOURCE10} %{buildroot}%{_rpmconfigdir}
install -m 0755 %{SOURCE16} %{buildroot}%{_rpmconfigdir}

mkdir -p %{buildroot}/usr/lib/rpm/fileattrs
install -m 0644 %{SOURCE17} %{buildroot}%{_rpmconfigdir}/fileattrs/
install -m 0644 %{SOURCE18} %{buildroot}%{_rpmconfigdir}/fileattrs/
install -m 0644 %{SOURCE19} %{buildroot}%{_rpmconfigdir}/fileattrs/

mkdir -p %{buildroot}%{_datadir}/mingw
install -m 0644 %{SOURCE13} %{buildroot}%{_datadir}/mingw/
install -m 0644 %{SOURCE14} %{buildroot}%{_datadir}/mingw/
install -m 0644 %{SOURCE15} %{buildroot}%{_datadir}/mingw/
install -m 0644 %{SOURCE20} %{buildroot}%{_datadir}/mingw/
install -m 0644 %{SOURCE21} %{buildroot}%{_datadir}/mingw/
install -m 0644 %{SOURCE22} %{buildroot}%{_datadir}/mingw/

mkdir -p %{buildroot}%{pkgconfig_personalitydir}
install -m 0644 %{SOURCE23} %{buildroot}%{pkgconfig_personalitydir}/i686-w64-mingw32.personality
install -m 0644 %{SOURCE24} %{buildroot}%{pkgconfig_personalitydir}/x86_64-w64-mingw32.personality
install -m 0644 %{SOURCE25} %{buildroot}%{pkgconfig_personalitydir}/x86_64-w64-mingw32ucrt.personality

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -m 0644 %{SOURCE26} %{buildroot}%{_sysconfdir}/ld.so.conf.d/mingw32-hostlib.conf
install -m 0644 %{SOURCE27} %{buildroot}%{_sysconfdir}/ld.so.conf.d/mingw64-hostlib.conf

# Link mingw-pkg-config man pages to pkgconf(1)
mkdir -p %{buildroot}%{_mandir}/man1/
echo ".so man1/pkgconf.1" > %{buildroot}%{_mandir}/man1/i686-w64-mingw32-pkg-config.1
echo ".so man1/pkgconf.1" > %{buildroot}%{_mandir}/man1/x86_64-w64-mingw32-pkg-config.1
echo ".so man1/pkgconf.1" > %{buildroot}%{_mandir}/man1/x86_64-w64-mingw32ucrt-pkg-config.1


%files base
%doc COPYING
%dir %{_sysconfdir}/rpmlint/
%config(noreplace) %{_sysconfdir}/rpmlint/mingw-rpmlint.config
%{macrosdir}/macros.mingw
%{_libexecdir}/mingw-scripts
%{_rpmconfigdir}/mingw*
%dir %{_datadir}/mingw/

%files -n mingw32-filesystem
%{macrosdir}/macros.mingw32
%config(noreplace) %{_sysconfdir}/profile.d/mingw32.sh
%{_bindir}/mingw32-configure
%{_bindir}/mingw32-cmake
%{_bindir}/mingw32-make
%{_bindir}/mingw32-meson
%{_bindir}/mingw32-pkg-config
%{_bindir}/i686-w64-mingw32-pkg-config
%{_prefix}/i686-w64-mingw32
%{_rpmconfigdir}/fileattrs/mingw32.attr
%{_datadir}/mingw/toolchain-mingw32.cmake
%{_datadir}/mingw/toolchain-mingw32.meson
%{pkgconfig_personalitydir}/i686-w64-mingw32.personality
%{_mandir}/man1/i686-w64-mingw32-pkg-config.1*
%{_sysconfdir}/ld.so.conf.d/mingw32-hostlib.conf
%dir %{_prefix}/lib/debug/%{_prefix}
%dir %{_prefix}/lib/debug/%{_prefix}/i686-w64-mingw32


%files -n mingw64-filesystem
%{macrosdir}/macros.mingw64
%config(noreplace) %{_sysconfdir}/profile.d/mingw64.sh
%{_bindir}/mingw64-configure
%{_bindir}/mingw64-cmake
%{_bindir}/mingw64-make
%{_bindir}/mingw64-meson
%{_bindir}/mingw64-pkg-config
%{_bindir}/x86_64-w64-mingw32-pkg-config
%{_prefix}/x86_64-w64-mingw32
%{_rpmconfigdir}/fileattrs/mingw64.attr
%{_datadir}/mingw/toolchain-mingw64.cmake
%{_datadir}/mingw/toolchain-mingw64.meson
%{pkgconfig_personalitydir}/x86_64-w64-mingw32.personality
%{_mandir}/man1/x86_64-w64-mingw32-pkg-config.1*
%{_sysconfdir}/ld.so.conf.d/mingw64-hostlib.conf
%dir %{_prefix}/lib/debug/%{_prefix}
%dir %{_prefix}/lib/debug/%{_prefix}/x86_64-w64-mingw32


%files -n ucrt64-filesystem
%{macrosdir}/macros.ucrt64
%config(noreplace) %{_sysconfdir}/profile.d/ucrt64.sh
%{_bindir}/ucrt64-configure
%{_bindir}/ucrt64-cmake
%{_bindir}/ucrt64-make
%{_bindir}/ucrt64-meson
%{_bindir}/ucrt64-pkg-config
%{_bindir}/x86_64-w64-mingw32ucrt-pkg-config
%{_prefix}/x86_64-w64-mingw32ucrt
%{_rpmconfigdir}/fileattrs/ucrt64.attr
%{_datadir}/mingw/toolchain-ucrt64.cmake
%{_datadir}/mingw/toolchain-ucrt64.meson
%{pkgconfig_personalitydir}/x86_64-w64-mingw32ucrt.personality
%{_mandir}/man1/x86_64-w64-mingw32ucrt-pkg-config.1*
%dir %{_prefix}/lib/debug/%{_prefix}
%dir %{_prefix}/lib/debug/%{_prefix}/x86_64-w64-mingw32ucrt

%changelog
* Thu Jan 22 2026 Sandro Mani <manisandro@gmail.com> - 151-1
- Use relative cross compiler paths in cmake toolchain files (#2430586)

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 150-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Aug 20 2025 Marc-André Lureau <marcandre.lureau@redhat.com> - 150-3
- Own a few more directories.

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 150-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu May 29 2025 Sandro Mani <manisandro@gmail.com> - 150-1
- Re-add target bin dir to PATH

* Sun Mar 23 2025 Sandro Mani <manisandro@gmail.com> - 149-1
- Only add cross host tools bin dir to PATH

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 148-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Sep 07 2024 Zephyr Lykos <fedora@mochaa.ws> - 148-7
- Fix meson deprecation warnings

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 148-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Sandro Mani <manisandro@gmail.com> - 148-5
- Rust fixes

* Thu Jun 06 2024 Sandro Mani <manisandro@gmail.com> - 148-4
- Set __debug_package 1 in %mingw_debug_package (#2284193)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 148-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 148-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 13 2023 Orion Poplawski <orion@nwra.com> - 148-1
- Add pkgconfig provides

* Mon Sep 11 2023 Neal Gompa <ngompa@fedoraproject.org> - 147-3
- Add dependency on cmake-rpm-macros

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 147-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 07 2023 Sandro Mani <manisandro@gmail.com> - 147-1
- Set mingw_env before in run_mingw_make

* Wed Apr 05 2023 Sandro Mani <manisandro@gmail.com> - 146-1
- Set RUSTFLAGS in mingw env

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 145-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Sandro Mani <manisandro@gmail.com> - 145-1
- Fix mingw-find-lang.sh exit code

* Fri Dec 23 2022 Sandro Mani <manisandro@gmail.com> - 144-1
- Add mingw-qmake-qt6 macros, drop mingw-cmake-kde4 macros

* Fri Dec 09 2022 Sandro Mani <manisandro@gmail.com> - 143-1
- Prevent mingw-find-lang.sh from clobbering previous find-lang results

* Tue Oct 18 2022 Sandro Mani <manisandro@gmail.com> - 142-1
- Require mingw-binutils-generic

* Tue Sep 27 2022 Sandro Mani <manisandro@gmail.com> - 141-2
- Replace egrep with grep -E

* Sat Jul 30 2022 Sandro Mani <manisandro@gmail.com> - 141-1
- Revert unsetting _PREFIX

* Fri Jul 29 2022 Sandro Mani <manisandro@gmail.com> - 140-1
- Don't unset _PREFIX in mingw-env macro, it leads to ${_PREFIX}
  being empty when evaluated the lines above

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 139-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 139-1
- Set CMAKE_FIND_ROOT_PATH_MODE_PACKAGE in cmake toolchain files

* Wed May 11 2022 Sandro Mani <manisandro@gmail.com> - 138-1
- Drop CMAKE_INSTALL_LIBDIR from mingw-cmake macros

* Mon May 09 2022 Richard Hughes <richard@hughsie.com> 137-1
- Include glib-mkenums in the toolchain binaries to avoid installing host GLib for building.

* Tue May 03 2022 Sandro Mani <manisandro@gmail.com> - 136-1
- Drop standard DLL provides, moved to mingw-crt

* Tue May 03 2022 Sandro Mani <manisandro@gmail.com> - 135-1
- Add host lib dirs to ld.so.conf

* Thu Apr 28 2022 Sandro Mani <manisandro@gmail.com> - 134-1
- Regenerate standard-dlls

* Thu Feb 24 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 133-2
- Fix ucrt64 toolchain filenames.

* Tue Feb 22 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 133-1
- Add ucrt64 target. Related to rhbz#2055254.

* Mon Feb 21 2022 Sandro Mani <manisandro@gmail.com> - 132-1
- Create build_winXX directories with mkdir -p

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 131-2
- Bump release

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 131-1
- Move python dependency generation to mingw32/64_python3.attr in mingw-python3 package
- More generic mingw_pkg_name macros to also deduce mingw package name from native name

* Wed Feb 02 2022 Sandro Mani <manisandro@gmail.com> - 130-1
- Drop evaling $@ in mingw-scripts, ensure mingw macros invoked by mingw-scripts contain $@

* Sat Jan 22 2022 Sandro Mani <manisandro@gmail.com> - 129-1
- Also set FCFLAGS in mingw-env

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 08 2022 Sandro Mani <manisandro@gmail.com> - 128-1
- Add Boost_ARCHITECTURE to cmake toolchain file

* Sat Jan 08 2022 Sandro Mani <manisandro@gmail.com> - 127-1
- Correctly test whether CC/CXX/FC env-vars are set in cmake toolchain config

* Wed Dec 15 2021 Sandro Mani <manisandro@gmail.com> - 126-1
- Preserve CC/CXX/FC/RC set by ENV if set in cmake toolchain files

* Sat Nov 20 2021 Sandro Mani <manisandro@gmail.com> - 125-1
- Fix up debug dirs ownership

* Wed Nov 17 2021 Sandro Mani <manisandro@gmail.com> - 124-1
- Use relative paths in cmake/meson toolchain files to make ccache work if
  available

* Tue Sep 21 2021 Sandro Mani <manisandro@gmail.com> - 123-1
- Autogenerate mingw-python3 BR
- Fix mingw{32/64}.attr to also capture pyd, pc files

* Thu Sep 02 2021 Sandro Mani <manisandro@gmail.com> - 122-1
- Allow overriding CMake INCLUDE_INSTALL_DIR in MINGWXX_CMAKE_ARGS
- Drop evaling $@ in mingw-scripts, ensure mingw macros invoked by mingw-scripts contain $@

* Sun Aug 29 2021 Sandro Mani <manisandro@gmail.com> - 121-1
- Drop use of deprecated external dependency generator
- Fix file listed twice
- Fix copying minidebug symbols to binary in mingw-find-debuginfo.sh

* Fri Aug 27 2021 Sandro Mani <manisandro@gmail.com> - 120-1
- Adapt mingw-find-debuginfo.sh to store debug files below /usr/lib/debug
- See https://fedoraproject.org/wiki/Changes/F36MingwDebugLocation

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 12 2021 Neal Gompa <ngompa13@gmail.com> - 119-1
- Use pkgconf for pkgconfig

* Mon Jun 07 2021 Sandro Mani <manisandro@gmail.com> - 118-1
- Allow overriding CFLAGS/CXXFLAGS/LDFLAGS for %%mingw_meson

* Mon Feb 01 2021 Sandro Mani <manisandro@gmail.com> - 117-1
- Filter Windows API umbrella libraries from requires

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> 116-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Sandro Mani <manisandro@gmail.com> - 116-1
- Add -lssp to LDFLAGS

* Thu Jul 23 2020 Sandro Mani <manisandro@gmail.com> - 115-1
- Add -fstack-protector to LDFLAGS (since we carry -D_FORTIFY_SOURCE=2 in cflags, see https://sourceforge.net/p/mingw-w64/bugs/818/)

* Tue Jul 14 2020 Daniel P. Berrangé <berrange@redhat.com> - 114-1
- Add meson hint for libgcrypt-config on mingw cross builds (#1856446)

* Sat May 23 2020 Sandro Mani <manisandro@gmail.com> - 113-1
- Add %%mingw_make_build and %%mingw_make_install

* Fri May 22 2020 Sandro Mani <manisandro@gmail.com> - 112-1
- Fix %%mingw_meson resulting in ERROR: Unable to determine dynamic linker

* Fri May 01 2020 David Woodhouse <dwmw2@infradead.org> - 111-1
- Quote tr sequences like '[blank]' to prevent the shell from doing so (#1830233)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 07 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 110-1
- Add redhat-rpm-config dependency. Fixes rhbz#1769792

* Thu Aug 29 2019 Sandro Mani <manisandro@gmail.com> - 109-1
- Add dlltool to toolchain-mingw{32,64}.meson

* Mon Aug 12 2019 Sandro Mani <manisandro@gmail.com> - 108-1
- Fix mingw-find-debuginfo.sh to pick up strippable binaries also in %%{_prefix}/%%{mingw32,64_target}

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 19 2019 Fabiano Fidêncio <fidencio@redhat.com> - 107-1
- Add %%mingw_ninja_install macro

* Thu Feb 14 2019 Sandro Mani <manisandro@gmail.com> - 106-1
- Revert "Remove redundant $@ in mingw_cmake and mingw_meson", it causes no arguments at all to be passed to cmake

* Tue Feb 05 2019 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 105-1
- Remove redundant $@ in mingw_cmake and mingw_meson, breaking wrapper scripts

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Apr 20 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 104-1
- Add macros for meson and ninja

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Sep 10 2017 Sandro Mani <manisandro@gmail.com> - 103-1
- Add %%mingw_nm macro

* Sat Sep 09 2017 Sandro Mani <manisandro@gmail.com> - 102-1
- Also extract debuginfo data from pyd binaries

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May  8 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 101-1
- Update config.{guess,sub} in %%mingw_configure (#1288256)
- Regenerated list of default win32 DLL's

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 11 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 100-1
- Various CMake improvements:
  * The toolchain files /usr/share/data/mingw/toolchain-mingw32.cmake
    and /usr/share/data/mingw/toolchain-mingw64.cmake don't have
    an uppercase character in their file name any more
  * Add CMAKE_SYSTEM_PROCESSOR to the CMake toolchain files
  * Removed Boost_COMPILER from the CMake toolchain files as
    it was unused and broken anyway
  * Made the RPM macros mingw32_cmake, mingw32_cmake_kde4,
    mingw64_cmake and mingw64_cmake_kde4 more generic
  * Removed the rpath references as mingw doesn't support rpath
  * Allow verbose CMake output to be disabled by setting the
    environment variable MINGW_CMAKE_NO_VERBOSE (RHBZ #987644)
  * When calling the mingw32-cmake and mingw64-cmake wrapper
    scripts don't use verbose CMake output by default
  * When using the CMake wrappers, prevent CFLAGS and CXXFLAGS
    from being set unless they're already set in the current
    environment (RHBZ #1136069)
  * Don't set LIB_INSTALL_DIR any more in the CMake macros
    as it breaks CPack and isn't needed by any of the
    Fedora MinGW packages (RHBZ #1152696)
- Accept empty MINGW{32,64}_{C,CPP,CXX}FLAGS environment variables
- Removed old _mingw32 macros which have been deprecated since Fedora 17

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 99-4
- Place the RPM macros in /usr/lib/rpm/macros.d when using a modern RPM

* Sat Aug  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 99-3
- Own the folders %%{mingw32_libdir}/cmake and %%{mingw64_libdir}/cmake
- Own all the locale folders below %%{mingw32_datadir}/locale and %%{mingw64_datadir}/locale (RHBZ #798329)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 15 2013 Kalev Lember <kalevlember@gmail.com> - 99-1
- Remove invalid macros with '++' in the name

* Sun Jun  2 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 98-2
- Only set the environment variable PKG_CONFIG_LIBDIR when
  using the macros %%mingw32_cmake, %%mingw32_cmake_kde4,
  %%mingw64_cmake or %%mingw64_cmake_kde4
- Fixes FTBFS of the mingw-matahari package

* Sun May 12 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 98-1
- Removed the use of the environment variable PKG_CONFIG_LIBDIR
  While building binaries the tool {i686,x86_64}-w64-mingw32-pkg-config
  should be used to find out pkg-config information
  The environment variable PKG_CONFIG already automatically points
  to the right cross-compiler aware version of pkg-config when
  the mingw{32,64}-pkg-config packages are installed
- Fixes compilation of mingw-gtk3 3.9.0 (GNOME BZ #699690)
- Automatically add R: mingw{32,64}-pkg-config tags when .pc files
  are detected while building mingw packages
- Bumped the minimum required version of mingw{32,64}-filesystem
  to >= 95 in built mingw packages as this is the first version of
  which was introduced in Fedora with a stable interface
- Updated the list of DLLs which are part of the Win32 API with
  the libraries d3dcompiler_46.dll, d3dcsx_46.dll, davclnt.dll,
  devmgr.dll, devobj.dll and devrtl.dll

* Thu Feb 28 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 97-3
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).
- Minor spec fixes.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 16 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 97-1
- Added support for using the environment variables MINGW32_MAKE_ARGS and
  MINGW64_MAKE_ARGS. These environment variables can be used to  provide
  additional target-specific arguments when using the %%mingw_make macro

* Mon Dec  3 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 96-3
- Added support for RHEL6

* Sat Nov 10 2012 Kalev Lember <kalevlember@gmail.com> - 96-2
- Add provides for mscoree.dll and regenerate the standard-dlls file

* Mon Sep 17 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 96-1
- Added new macros for Qt5 support, %%mingw32_qmake_qt5, %%mingw64_qmake_qt5,
  %%mingw_qmake_qt4 and %%mingw_qmake_qt5
- It isn't necessary to call %%mingw32_env / %%mingw64_env any more
  in the %%mingw32_qmake_qt4 and %%mingw64_qmake_qt4 macros

* Mon Aug 13 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 95-14
- Fix the handling of quoted arguments in the cmake macros

* Tue Jul 24 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 95-13
- Make sure the %%mingw_cmake and %%mingw_cmake_kde4 macros respect the
  environment variable MINGW_BUILDDIR_SUFFIX

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 95-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Kalev Lember <kalevlember@gmail.com> - 95-11
- Fix syntax error in mingw64_env macro, thanks to Akira TAGOH (#831534)

* Wed Jun  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 95-10
- Prevent errors when the folders %%{mingw32_prefix} or %%{mingw64_prefix} are missing
- Fix parse error when -config files containing a . are available
  in %%{mingw32_bindir} or %%{mingw64_bindir} (RHBZ #657478)

* Thu Apr 19 2012 Kalev Lember <kalevlember@gmail.com> - 95-9
- Fix whitespace handling in %%mingw_configure and friends

* Sat Mar 17 2012 Kalev Lember <kalevlember@gmail.com> - 95-8
- Generate the list of mingw32(...) and mingw64(...) DLL name provides from
  mingw-crt import libraries

* Sat Mar 17 2012 Kalev Lember <kalevlember@gmail.com> - 95-7
- Define mingw_build_win32/win64 in system macros, so that each
  individual package wouldn't have to

* Fri Mar 16 2012 Kalev Lember <kalevlember@gmail.com> - 95-6
- Fix warnings during debuginfo generation

* Fri Mar 16 2012 Kalev Lember <kalevlember@gmail.com> - 95-5
- Simplify the mingw_make_install macro, also moving it to the deprecated
  section

* Mon Mar 12 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 95-4
- Added a manual provides for the native windows library ksuser.dll as
  wine doesn't have an implementation for this library at the moment

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 95-3
- Merge copy-n-paste duplicate %%mingw32_debug_package code
- Get rid of the USE_OLD_METHOD hack in mingw-find-debuginfo.sh
- Add missing %%mingw32_debug_install_post

* Tue Feb 28 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 95-2
- Fixed broken summary tags

* Sat Feb 25 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 95-1
- Added support for both win32 and win64 targets
- Fixed rpmlint issues
- Fixed permissions of the scripts (775 -> 755)
- Fixed description of the various subpackages
- Make the various macros compliant with the new packaging guidelines:
  https://fedorahosted.org/fpc/ticket/71
- Suppress arch-independent-package-contains-binary-or-object rpmlint
  errors for static libraries
- Improved the mingw_configure, mingw_make, mingw_make_install,
  mingw_cmake and mingw_cmake_kde4 RPM macros so packagers don't need
  to use quotes anymore when using arguments. Thanks to Kalev Lember
  for the initial proof of concept
- Dropped the -mms-bitfields argument from the default CFLAGS as
  it is enabled by default as of gcc 4.7
- Replaced the CMake defines QT_HEADERS_DIR and QT_LIBRARY_DIR
  with QT_BINARY_DIR which is a more proper method to make CMake
  aware of the location of Qt. Thx to Dominik Schmidt for the hint
- Make sure CMake can detect the qmake-qt4 binary in /usr/$target/bin
- Make sure CMake can also detect the (native) Qt tools
  qdbuscpp2xml and qdbusxml2cpp
- Added new RPM macros mingw_cmake_kde4, mingw32_cmake_kde4 and mingw64_cmake_kde4
- Added three new environment variables which can be set to
  influence the behaviour of the cmake macros:
  MINGW_CMAKE_ARGS, MINGW32_CMAKE_ARGS and MINGW64_CMAKE_ARGS
- Dropped the mingw32-qmake-qt4 and mingw64-qmake-qt4 wrapper scripts
  as they're now provided by the mingw{32,64}-qt-qmake packages
- Added a new RPM macro: %%{?mingw_package_header}
  Packagers can use this macro instead of the original boilerplate
  code which is needed for all mingw packages
- Made argument passing using the backwards compatibility macro %%{_mingw32_cmake} work
- Fixed an issue in the mingw_cmake macro where it could point to
  a non-existant CMakeLists.txt file
- Fixed a bug in the find-requires script which causes all packages to depend
  on both the mingw32 and the mingw64 toolchains
- Split out the RPM macros which require both the mingw{32,64}-filesystem
  packages in a new file and put it in the mingw-filesystem-base package
- Generate seperate debuginfo packages for mingw32 and mingw64
- Set the minimum version of R: mingw{32,64}-filesystem to 70
- Use the correct FSF-address in some scripts
- Thanks to all the contributors: Erik van Pienbroek, Kalev Lember, Levente
  Farkas, Marc-Andre Lureau.

* Thu Feb 23 2012 Kalev Lember <kalevlember@gmail.com> - 69-15
- Rename the source package to mingw-filesystem (#673784)

* Sun Feb  5 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-14
- Use a more complete list of Win32 default dlls based on the
  dlls exported by wine (thanks to Levente Farkas). RHBZ #787486

* Tue Jan 31 2012 Kalev Lember <kalevlember@gmail.com> - 69-13
- Remove the mingw32-pkg-config wrapper as well, now that we have separate
  mingw32-pkg-config package

* Tue Jan 31 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-12
- Don't provide the wrapper i686-pc-mingw32-pkg-config anymore as we now
  have a mingw32-pkg-config package

* Tue Jan 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-11
- Set Boost_COMPILER to -gcc47 in cmake toolchain file

* Tue Nov 22 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-10
- Fixed a small regression introduced by the previous release which caused an
  FTBFS for mingw32-matahari as indicated on the fedora-mingw mailing list

* Wed Nov 16 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-9
- Added various definitions to the CMake toolchain file (RHBZ #753906)

* Tue Aug 02 2011 Kalev Lember <kalevlember@gmail.com> - 69-8
- Added avicap32.dll and psapi.dll to the list of Win32 default DLLs
  (thanks to Farkas Levente)

* Wed Jul 13 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-7
- Added glu32.dll and wsock32.dll to the list of Win32 default dll's

* Wed Jul  6 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-6
- Use a more complete list of Win32 default dll's

* Wed Jul 06 2011 Kalev Lember <kalevlember@gmail.com> - 69-5
- Fixed dep gen with upper case dll names

* Fri Jul  1 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 69-4
- The %%{_mingw32_qmake_qt4} macro pointed to an invalid mkspecs name. Fixed

* Tue Jun 28 2011 Kalev Lember <kalev@smartlink.ee> - 69-3
- Set Boost_COMPILER to -gcc46 in cmake toolchain file

* Sun May 29 2011 Kalev Lember <kalev@smartlink.ee> - 69-2
- Make sure the -debuginfo subpackages are mingw32- prefixed
  even if the base package is mingw-

* Tue May 24 2011 Kalev Lember <kalev@smartlink.ee> - 69-1
- Adjusted PKG_CONFIG_LIBDIR to also search in _mingw32_datadir/pkgconfig/
- Own the sbin/ directory
- Fixed the -n option with _mingw32_debug_package macro

* Mon May 23 2011 Kalev Lember <kalev@smartlink.ee> - 68-3
- Own etc/, share/pkgconfig/, share/xml/ directories

* Sat May 21 2011 Kalev Lember <kalev@smartlink.ee> - 68-2
- Own the _mingw32_datadir/cmake/ directory

* Fri May 20 2011 Kalev Lember <kalev@smartlink.ee> - 68-1
- Support RPM 4.9 new "fileattr" dep extraction system
- Cleaned up the spec file from cruft not needed with latest rpm
- Generate versionless mingw32-filesystem Requires

* Sat May 14 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 67-1
- Don't unset PKG_CONFIG_PATH in the wrapper scripts
  mingw32-pkg-config and i686-pc-mingw32-pkg-config (BZ #688171)

* Sun May 01 2011 Kalev Lember <kalev@smartlink.ee> - 66-1
- Override boost library suffix in cmake toolchain file

* Thu Mar 17 2011 Kalev Lember <kalev@smartlink.ee> - 65-1
- Don't error out trying to set illegal LD.BFD variable name

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 64-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 64-2
- Own the directory %%{_mingw32_datadir}/themes

* Sun Nov 14 2010 Ivan Romanov <drizt@land.ru> - 64-1
- Removed -win32 option for mingw32-qmake-qt4 (is obsoletes since qt version 4.7.0)
- Using win32-g++-fedora-cross instead fedora-win32-cross spec file

* Thu Nov 11 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 63-1
- Set the CMAKE_RC_COMPILER variable in the CMake toolchain file (RHBZ #652435)

* Tue Oct 19 2010 Ivan Romanov <drizt@land.ru> - 62-2
- Added mingw32-qmake-qt4

* Mon Oct 11 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 62-1
- Provide mingw32(odbc32.dll) for Qt

* Sun Sep 12 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 61-1
- Provide mingw32(gdiplus.dll) for gdk-pixbuf

* Thu Sep  9 2010 Richard W.M. Jones <rjones@redhat.com> - 60-1
- Provide virtual mingw32(ws2_32.dll) for libvirt.

* Mon Sep 06 2010 Kalev Lember <kalev@smartlink.ee> - 59-1
- Own /etc/rpmlint/ dir instead of depending on rpmlint package (RHBZ#629791)

* Fri Sep  3 2010 Richard W.M. Jones <rjones@redhat.com> - 58-1
- Remove requires setup and rpm (RHBZ#629791).

* Tue Jun  8 2010 Richard W.M. Jones <rjones@redhat.com> - 57-1
- Add provides mingw32(rpcrt4.dll) (RHBZ#594581).

* Mon May 24 2010 Kalev Lember <kalev@smartlink.ee> - 56-2
- Work around cmake's Qt detection in the toolchain file

* Fri Sep 18 2009 Erik van Pienbroek <epienbro@fedoraproject.org. - 56-1
- Prevented a circular dependency which caused the i686-pc-mingw32-pkg-config
  script to be broken. Thanks to Kalev Lember for spotting this bug

* Tue Sep  1 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 55-1
- The wrapper scripts i686-pc-mingw32-pkg-config, mingw32-pkg-config,
  mingw32-configure, mingw32-make and mingw32-cmake had a bug where
  quoted arguments could get interpreted incorrect.
  Thanks to Michael Ploujnikov for helping out with this issue

* Sat Aug 29 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 54-1
- Added the file /usr/bin/i686-pc-mingw32-pkg-config which is a wrapper script
  which calls pkg-config with the right environment variables set (BZ #513825)

* Sun Aug 23 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 53-1
- Fixed a small rpmlint warning caused by the debuginfo generation macro
  Thanks to Kalev Lember for spotting this

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 52-2
- Updated ChangeLog comment from previous version as the RPM variable
  __debug_install_post needs to be overridden instead of __os_install_post
  for -debuginfo subpackage generation

* Mon Jun 22 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 52-1
- Add script to create -debuginfo subpackages
  This script was created by Fridrich Strba
- All mingw32 packages now need to add these lines to their .spec files:
  %%define __debug_install_post %%{_mingw32_debug_install_post}
  %%{_mingw32_debug_package}

* Thu Jun  4 2009 Adam Goode <adam@spicenitz.org> - 51-1
- Add CMake rules

* Tue Apr 21 2009 Richard W.M. Jones <rjones@redhat.com> - 50-4
- Fix dependency problem with + in DLL name (Thomas Sailer).

* Fri Mar 27 2009 Richard W.M. Jones <rjones@redhat.com> - 50-3
- Fix up and test mingw32-pkg-config changes.

* Thu Mar 26 2009 Levente Farkas <lfarkas@lfarkas.org> - 50-1
- Add mingw32-pkg-config.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 49-2
- Rebuild for mingw32-gcc 4.4

* Thu Feb 19 2009 Richard W.M. Jones <rjones@redhat.com> - 49-1
- Added virtual provides for mingw32(cfgmgr32.dll) and mingw32(setupapi.dll).

* Wed Feb 18 2009 Richard W.M. Jones <rjones@redhat.com> - 48-1
- Fix _mingw32_configure.

* Tue Feb 17 2009 Richard W.M. Jones <rjones@redhat.com> - 47-1
- Rename mingw32-COPYING to COPYING.
- Rename mingw32-macros.mingw32 to macros.mingw32.
- _mingw32_configure looks for configure in "." and ".." dirs.
- Added _mingw32_description.
- Added mingw32(version.dll) virtual provides (rhbz#485842).

* Sun Feb  1 2009 Richard W.M. Jones <rjones@redhat.com> - 46-1
- Unset PKG_CONFIG_PATH because /usr/lib/rpm/macros sets it (Erik van
  Pienbroek).

* Wed Jan 28 2009 Richard W.M. Jones <rjones@redhat.com> - 45-1
- Use PKG_CONFIG_LIBDIR instead of PKG_CONFIG_PATH so that native pkgconfig
  is never searched.

* Mon Jan 26 2009 Richard W.M. Jones <rjones@redhat.com> - 44-1
- Install rpmlint overrides file to suppress some rpmlint warnings.

* Sat Jan 24 2009 Richard W.M. Jones <rjones@redhat.com> - 43-6
- Don't claim C++ compiler exists if it's not installed, as this
  breaks autoconf and (in particular) libtool.

* Wed Jan 14 2009 Richard W.M. Jones <rjones@redhat.com> - 42-1
- Add pseudo-provides secur32.dll

* Wed Dec 17 2008 Levente Farkas <lfarkas@lfarkas.org> - 41-1
- Re-add mingw32-make

* Sat Dec  6 2008 Levente Farkas <lfarkas@lfarkas.org> - 40-2
- Rewrite mingw32-scripts to run in the current shell
- (Re-add mingw32-make) - Removed by RWMJ.
- Add mingw32-env to mingw32.sh

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 39-3
- Unify mingw32-filesystem packages from all three branches again, and test.
- Fix mingw32-scripts so it can handle extra parameters correctly.
- Remove mingw32-env & mingw32-make since neither of them actually work.

* Sun Nov 23 2008 Richard Jones <rjones@redhat.com> - 38-1
- Added mingw32(glut32.dll).

* Wed Nov 19 2008 Richard Jones <rjones@redhat.com> - 37-1
- Revert part of the 36-1 patch.  --build option to configure was wrong.

* Wed Nov 19 2008 Richard Jones <rjones@redhat.com> - 36-1
- Greatly improved macros (Levente Farkas).
- Added -mms-bitfields.

* Thu Nov 13 2008 Richard Jones <rjones@redhat.com> - 35-1
- Added mingw32(wldap32.dll) pseudo-provides.

* Wed Oct 29 2008 Richard Jones <rjones@redhat.com> - 34-1
- Set --prefix correctly.

* Wed Oct 29 2008 Richard Jones <rjones@redhat.com> - 33-1
- Remove mingw32.{sh,csh} which are unused.

* Mon Oct 27 2008 Richard Jones <rjones@redhat.com> - 32-1
- Add mingw32-configure script.

* Mon Oct 27 2008 Richard Jones <rjones@redhat.com> - 31-1
- Update the spec file with explanation of the 'Provides: mingw32(...)'
  lines for Windows system DLLs.

* Mon Oct  6 2008 Richard Jones <rjones@redhat.com> - 30-1
- Added _mingw32_cxx.

* Thu Sep 25 2008 Richard Jones <rjones@redhat.com> - 29-1
- Added _mingw32_as, _mingw32_dlltool, _mingw32_windres.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 27-1
- Begin the grand renaming of mingw -> mingw32.
- Added mingw32(mscoree.dll).

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 25-1
- Add shared aclocal directory.

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 24-1
- Remove mingw-defs, since no longer used.
- Add _mingw_infodir.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 23-1
- Add macros for find-provides/requires scripts

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 22-1
- Windows provides OLE32.DLL.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 21-1
- Allow '.' in dll names for find-requires
- Windows provides GDI32.DLL.

* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 20-1
- On 64 bit install in /usr/lib/rpm always.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 19-1
- 'user32.dll' is provided by Windows.
- Allow '-' in DLL names.
- More accurate detection of DLLs in requires/provides scripts.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 17-1
- Automatically add mingw-filesystem and mingw-runtime requires.
- Add --prefix to _mingw_configure macro.
- Three backslashes required on each continuation line in RPM macros.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 14-1
- Fix path to mingw-find-requires/provides scripts.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 12-1
- Put CFLAGS on a single line to avoid problems in some configure scripts.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 10-1
- Provides certain base Windows DLLs (not literally).

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 9-1
- Include RPM dependency generators and definitions.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4-1
- Add _mingw_cc/cflags/etc. and _mingw_configure macros.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3-1
- Add _mingw_host macro.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 2-1
- Add _mingw_sysroot macro.
- Add _mingw_target macro.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1-1
- Basic filesystem layout.
