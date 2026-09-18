# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%ifarch x86_64
%global archs %{ix86} x86_64
%else
%ifarch %{ix86}
%global archs %{ix86}
%else
%global archs %{_target_cpu}
%endif
%endif

%define abs2rel() perl -MFile::Spec -e 'print File::Spec->abs2rel(@ARGV)' %1 %2
%global relccache %(%abs2rel %{_bindir}/ccache %{_libdir}/ccache)

Name:           ccache
Version:        4.11.3
Release:        2%{?dist}
Summary:        C/C++ compiler cache

# See LICENSE.adoc for licenses of bundled codes
# blake3 is Apache-2.0
# span.hpp is BSL-1.0
# url.cpp/hpp is MIT
License:        GPL-3.0-or-later AND Apache-2.0 AND BSL-1.0 AND MIT
URL:            http://ccache.dev/
Source0:        https://github.com/ccache/ccache/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.sh.in
Source2:        %{name}.csh.in

BuildRequires:  /usr/bin/asciidoctor
BuildRequires:  cmake
# Uses a patched version and is missing on i686 in Fedora
#BuildRequires:  blake3-devel
BuildRequires:  cpp-httplib-devel
BuildRequires:  doctest-devel
BuildRequires:  expected-devel
BuildRequires:  fmt-devel
BuildRequires:  hiredis-devel
BuildRequires:  libzstd-devel
BuildRequires:  perl perl(File::Spec)
BuildRequires:  xxhash-devel
# clang for additional tests
BuildRequires:  clang clang-tools-extra
# coreutils for triggerin, triggerpostun
Requires:       coreutils
# For groupadd
Provides:       bundled(blake3) = 1.5.1
Provides:       bundled(span-lite) = 0.11.0
Provides:       bundled(cxxurl)

%description
ccache is a compiler cache.  It speeds up recompilation of C/C++ code
by caching previous compiles and detecting when the same compile is
being done again.  The main focus is to handle the GNU C/C++ compiler
(GCC), but it may also work with compilers that mimic GCC good enough.


%prep
%autosetup -p1
# win32-compat gets imported, but not used
rm -r src/third_party/{[ad-lo-tvy-z]*,cpp-httplib}
sed -e 's|@LIBDIR@|%{_libdir}|g' -e 's|@CACHEDIR@|%{_var}/cache/ccache|g' \
    %{SOURCE1} > %{name}.sh
sed -e 's|@LIBDIR@|%{_libdir}|g' -e 's|@CACHEDIR@|%{_var}/cache/ccache|g' \
    %{SOURCE2} > %{name}.csh

# Create a sysusers.d config file
cat >ccache.sysusers.conf <<EOF
g ccache -
EOF


%build
%cmake
%cmake_build
%cmake_build --target doc


%install
%cmake_install

install -Dpm 644 %{__cmake_builddir}/doc/ccache.1 $RPM_BUILD_ROOT%{_mandir}/man1/ccache.1

install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -pm 644 %{name}.sh %{name}.csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

install -dm 770 $RPM_BUILD_ROOT%{_var}/cache/ccache

# %%ghost files for ownership, keep in sync with triggers
install -dm 755 $RPM_BUILD_ROOT%{_libdir}/ccache
for n in cc gcc g++ c++ ; do
    ln -s %{relccache} $RPM_BUILD_ROOT%{_libdir}/ccache/$n
    for p in avr arm-gp2x-linux arm-none-eabi msp430 ; do
        ln -s %{relccache} $RPM_BUILD_ROOT%{_libdir}/ccache/$p-$n
    done
    for p in aarch64 alpha arm avr32 bfin c6x cris frv h8300 hppa hppa64 ia64 m32r \
        m68k microblaze mips64 mn10300 nios2 powerpc64 powerpc64le ppc64 ppc64le \
        s390x sh sh64 sparc64 tile x86_64 xtensa ; do
        ln -s %{relccache} $RPM_BUILD_ROOT%{_libdir}/ccache/$p-linux-gnu-$n
    done
    for s in 32 34 4 44 ; do
        ln -s %{relccache} $RPM_BUILD_ROOT%{_libdir}/ccache/$n$s
    done
    for a in %{archs} ; do
        ln -s %{relccache} \
            $RPM_BUILD_ROOT%{_libdir}/ccache/$a-%{_vendor}-%{_target_os}-$n
    done
done
for n in clang clang++ ; do
    ln -s %{relccache} $RPM_BUILD_ROOT%{_libdir}/ccache/$n
done
find $RPM_BUILD_ROOT%{_libdir}/ccache -type l | \
    sed -e "s|^$RPM_BUILD_ROOT|%%ghost |" > %{name}-%{version}.compilers

install -m0644 -D ccache.sysusers.conf %{buildroot}%{_sysusersdir}/ccache.conf


%check
%ctest


%define ccache_trigger(p:) \
%triggerin -- %{-p*}\
for n in %* ; do\
    [ ! -x %{_bindir}/$n ] || ln -sf %{relccache} %{_libdir}/ccache/$n\
    for a in %{archs} ; do\
        [ ! -x %{_bindir}/$a-%{_vendor}-%{_target_os}-$n ] || \\\
          ln -sf %{relccache} %{_libdir}/ccache/$a-%{_vendor}-%{_target_os}-$n\
    done\
done\
:\
%triggerpostun -- %{-p*}\
for n in %* ; do\
    [ -x %{_bindir}/$n ] || rm -f %{_libdir}/ccache/$n\
    for a in %{archs} ; do\
        [ -x %{_bindir}/$a-%{_vendor}-%{_target_os}-$n ] || \\\
            rm -f %{_libdir}/ccache/$a-%{_vendor}-%{_target_os}-$n\
    done\
done\
:\
%{nil}

%ccache_trigger -p arm-gp2x-linux-gcc arm-gp2x-linux-cc arm-gp2x-linux-gcc
%ccache_trigger -p arm-gp2x-linux-gcc-c++ arm-gp2x-linux-c++ arm-gp2x-linux-g++
%ccache_trigger -p arm-none-eabi-gcc-cs arm-none-eabi-gcc
%ccache_trigger -p avr-gcc avr-cc avr-gcc
%ccache_trigger -p avr-gcc-c++ avr-c++ avr-g++
%ccache_trigger -p clang clang clang++
%ccache_trigger -p compat-gcc-32 cc32 gcc32
%ccache_trigger -p compat-gcc-32-c++ c++32 g++32
%ccache_trigger -p compat-gcc-34 cc34 gcc34
%ccache_trigger -p compat-gcc-34-c++ c++34 g++34
%ccache_trigger -p compat-gcc-34-g77 f77 g77
%ccache_trigger -p gcc cc gcc
%ccache_trigger -p gcc-c++ c++ g++
%ccache_trigger -p gcc4 cc4 gcc4
%ccache_trigger -p gcc4-c++ c++4 g++4
%ccache_trigger -p gcc44 cc4 gcc44
%ccache_trigger -p gcc44-c++ c++44 g++44
%ccache_trigger -p mingw32-gcc i686-pc-mingw32-cc i686-pc-mingw32-gcc i686-w64-mingw32-gcc
%ccache_trigger -p mingw32-gcc-c++ i686-pc-mingw32-c++ i686-pc-mingw32-g++ i686-w64-mingw32-c++ i686-w64-mingw32-g++
%ccache_trigger -p mingw64-gcc i686-w64-mingw32-gcc x86_64-w64-mingw32-gcc
%ccache_trigger -p mingw64-gcc-c++ i686-w64-mingw32-c++ i686-w64-mingw32-g++ x86_64-w64-mingw32-c++ x86_64-w64-mingw32-g++
%ccache_trigger -p msp430-gcc msp430-cc msp430-gcc
%ccache_trigger -p nacl-arm-gcc arm-nacl-gcc
%ccache_trigger -p nacl-gcc nacl-gcc nacl-c++ nacl-g++
# cross-gcc
%ccache_trigger -p gcc-aarch64-linux-gnu aarch64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-aarch64-linux-gnu aarch64-linux-gnu-c++ aarch64-linux-gnu-g++
%ccache_trigger -p gcc-alpha-linux-gnu alpha-linux-gnu-gcc
%ccache_trigger -p gcc-c++-alpha-linux-gnu alpha-linux-gnu-c++ alpha-linux-gnu-g++
%ccache_trigger -p gcc-arm-linux-gnu arm-linux-gnu-gcc
%ccache_trigger -p gcc-c++-arm-linux-gnu arm-linux-gnu-c++ arm-linux-gnu-g++
%ccache_trigger -p gcc-avr32-linux-gnu avr32-linux-gnu-gcc
%ccache_trigger -p gcc-c++-avr32-linux-gnu avr32-linux-gnu-c++ avr32-linux-gnu-g++
%ccache_trigger -p gcc-bfin-linux-gnu bfin-linux-gnu-gcc
%ccache_trigger -p gcc-c++-bfin-linux-gnu bfin-linux-gnu-c++ bfin-linux-gnu-g++
%ccache_trigger -p gcc-c6x-linux-gnu c6x-linux-gnu-gcc
%ccache_trigger -p gcc-c++-c6x-linux-gnu c6x-linux-gnu-c++ c6x-linux-gnu-g++
%ccache_trigger -p gcc-cris-linux-gnu cris-linux-gnu-gcc
%ccache_trigger -p gcc-c++-cris-linux-gnu cris-linux-gnu-c++ cris-linux-gnu-g++
%ccache_trigger -p gcc-frv-linux-gnu frv-linux-gnu-gcc
%ccache_trigger -p gcc-c++-frv-linux-gnu frv-linux-gnu-c++ frv-linux-gnu-g++
%ccache_trigger -p gcc-h8300-linux-gnu h8300-linux-gnu-gcc
%ccache_trigger -p gcc-hppa-linux-gnu hppa-linux-gnu-gcc
%ccache_trigger -p gcc-c++-hppa-linux-gnu hppa-linux-gnu-c++ hppa-linux-gnu-g++
%ccache_trigger -p gcc-hppa64-linux-gnu hppa64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-hppa64-linux-gnu hppa64-linux-gnu-c++ hppa64-linux-gnu-g++
%ccache_trigger -p gcc-ia64-linux-gnu ia64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-ia64-linux-gnu ia64-linux-gnu-c++ ia64-linux-gnu-g++
%ccache_trigger -p gcc-m32r-linux-gnu m32r-linux-gnu-gcc
%ccache_trigger -p gcc-c++-m32r-linux-gnu m32r-linux-gnu-c++ m32r-linux-gnu-g++
%ccache_trigger -p gcc-m68k-linux-gnu m68k-linux-gnu-gcc
%ccache_trigger -p gcc-c++-m68k-linux-gnu m68k-linux-gnu-c++ m68k-linux-gnu-g++
%ccache_trigger -p gcc-microblaze-linux-gnu microblaze-linux-gnu-gcc
%ccache_trigger -p gcc-c++-microblaze-linux-gnu microblaze-linux-gnu-c++ microblaze-linux-gnu-g++
%ccache_trigger -p gcc-mips64-linux-gnu mips64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-mips64-linux-gnu mips64-linux-gnu-c++ mips64-linux-gnu-g++
%ccache_trigger -p gcc-mn10300-linux-gnu mn10300-linux-gnu-gcc
%ccache_trigger -p gcc-c++-mn10300-linux-gnu mn10300-linux-gnu-c++ mn10300-linux-gnu-g++
%ccache_trigger -p gcc-nios2-linux-gnu nios2-linux-gnu-gcc
%ccache_trigger -p gcc-c++-nios2-linux-gnu nios2-linux-gnu-c++ nios2-linux-gnu-g++
%ccache_trigger -p gcc-powerpc64-linux-gnu powerpc64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-powerpc64-linux-gnu powerpc64-linux-gnu-c++ powerpc64-linux-gnu-g++
%ccache_trigger -p gcc-powerpc64le-linux-gnu powerpc64le-linux-gnu-gcc
%ccache_trigger -p gcc-c++-powerpc64le-linux-gnu powerpc64le-linux-gnu-c++ powerpc64le-linux-gnu-g++
%ccache_trigger -p gcc-ppc64-linux-gnu ppc64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-ppc64-linux-gnu ppc64-linux-gnu-c++ ppc64-linux-gnu-g++
%ccache_trigger -p gcc-ppc64le-linux-gnu ppc64le-linux-gnu-gcc
%ccache_trigger -p gcc-c++-ppc64le-linux-gnu ppc64le-linux-gnu-c++ ppc64le-linux-gnu-g++
%ccache_trigger -p gcc-s390x-linux-gnu s390x-linux-gnu-gcc
%ccache_trigger -p gcc-c++-s390x-linux-gnu s390x-linux-gnu-c++ s390x-linux-gnu-g++
%ccache_trigger -p gcc-sh-linux-gnu sh-linux-gnu-gcc
%ccache_trigger -p gcc-c++-sh-linux-gnu sh-linux-gnu-c++ sh-linux-gnu-g++
%ccache_trigger -p gcc-sh64-linux-gnu sh64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-sh64-linux-gnu sh64-linux-gnu-c++ sh64-linux-gnu-g++
%ccache_trigger -p gcc-sparc64-linux-gnu sparc64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-sparc64-linux-gnu sparc64-linux-gnu-c++ sparc64-linux-gnu-g++
%ccache_trigger -p gcc-tile-linux-gnu tile-linux-gnu-gcc
%ccache_trigger -p gcc-c++-tile-linux-gnu tile-linux-gnu-c++ tile-linux-gnu-g++
%ccache_trigger -p gcc-x86_64-linux-gnu x86_64-linux-gnu-gcc
%ccache_trigger -p gcc-c++-x86_64-linux-gnu x86_64-linux-gnu-c++ x86_64-linux-gnu-g++
%ccache_trigger -p gcc-xtensa-linux-gnu xtensa-linux-gnu-gcc
%ccache_trigger -p gcc-c++-xtensa-linux-gnu xtensa-linux-gnu-c++ xtensa-linux-gnu-g++



%files -f %{name}-%{version}.compilers
%license GPL-3.0.txt LICENSE.*
%doc doc/AUTHORS.*  doc/MANUAL.* doc/NEWS.* README.md
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%{_bindir}/ccache
%dir %{_libdir}/ccache/
%attr(2770,root,ccache) %dir %{_var}/cache/ccache/
%{_mandir}/man1/ccache.1*
%{_sysusersdir}/ccache.conf


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri May 09 2025 Orion Poplawski <orion@nwra.com> - 4.11.3-1
- Update to 4.11.3

* Tue Mar 25 2025 Orion Poplawski <orion@nwra.com> - 4.11.2-1
- Update to 4.11.2

* Tue Mar 18 2025 Orion Poplawski <orion@nwra.com> - 4.11.1-1
- Update to 4.11.1

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.10.2-3
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 31 2024 Orion Poplawski <orion@nwra.com> - 4.10.2-1
- Update to 4.10.2

* Fri Jul 26 2024 Kefu Chai <tchaikov@gmail.com> - 4.10.1-3
- Rebuilt for fmt 11

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 12 2024 Orion Poplawski <orion@nwra.com> - 4.10.1-1
- Update to 4.10.1

* Sun Jun 02 2024 Orion Poplawski <orion@nwra.com> - 4.10-1
- Update to 4.10

* Sat May 11 2024 Kevin Fenzi <kevin@scrye.com> - 4.9.1-2
- rebuild for hiredis soname bump

* Tue Feb 06 2024 Orion Poplawski <orion@nwra.com> - 4.9.1-1
- Update to 4.9.1
- Unbundle some libraries
- Use SPDX license
- Add licenses for bundled code

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 01 2023 Orion Poplawski <orion@nwra.com> - 4.8.3-1
- Update to 4.8.3

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Orion Poplawski <orion@nwra.com> - 4.8.2-1
- Update to 4.8.2

* Wed Apr 05 2023 Orion Poplawski <orion@nwra.com> - 4.8-1
- Update to 4.8 (fixes bz#2160275)

* Wed Mar 22 2023 Orion Poplawski <orion@nwra.com> - 4.7.5-1
- Update to 4.7.5

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 10 2022 Orion Poplawski <orion@nwra.com> - 4.7.4-1
- Update to 4.7.4

* Mon Nov 07 2022 Orion Poplawski <orion@nwra.com> - 4.7.3-1
- Update to 4.7.3

* Sat Oct 01 2022 Orion Poplawski <orion@nwra.com> - 4.6.3-1
- Update to 4.6.3

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 16 2022 Orion Poplawski <orion@nwra.com> - 4.6.1-1
- Update to 4.6.1

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 Kevin Fenzi <kevin@scrye.com> - 4.5.1-2
- Rebuild for hiredis 1.0.2

* Sun Dec 05 2021 Orion Poplawski <orion@nwra.com> - 4.5.1-1
- Update to 4.5.1

* Wed Oct 27 2021 Orion Poplawski <orion@nwra.com> - 4.4.2-1
- Update to 4.4.2

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 02 2021 Orion Poplawski <orion@nwra.com> - 4.2.1-1
- Update to 4.2.1

* Wed Feb 03 2021 Orion Poplawski <orion@nwra.com> - 4.2-1
- Update to 4.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 02 2021 Łukasz Patron <priv.luk@gmail.com> - 4.1-1
- Update to 4.1

* Tue Oct 27 2020 Łukasz Patron <priv.luk@gmail.com> - 4.0-1
- Update to 4.0

* Thu Oct  1 2020 Orion Poplawski <orion@nwra.com> - 3.7.12-1
- Update to 3.7.12

* Sat Aug 15 2020 Orion Poplawski <orion@nwra.com> - 3.7.11-1
- Update to 3.7.11

* Fri Aug 07 2020 Jeff Law <law@redhat.com> - 3.7.9-4
- Depend on perl

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.9-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 30 2020 LuK1337 <priv.luk@gmail.com> - 3.7.9-1
- Update to 3.7.9

* Thu Mar 26 2020 LuK1337 <priv.luk@gmail.com> - 3.7.8-1
- Update to 3.7.8

* Tue Feb 18 2020 Orion Poplawski <orion@nwra.com> - 3.7.7-1
- Update to 3.7.7

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 21 2019 LuK1337 <priv.luk@gmail.com> - 3.7.6-1
- Updated to 3.7.6

* Thu Oct 24 2019 Michael Cullen <mich181189@fedoraproject.org> - 3.7.5-1
- Updated to 3.7.5
- Updated upstream URL

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 20 2019 Michael Cullen <mich181189@fedoraproject.org> - 3.7.1-1
- Updated to 3.7.1

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 24 2018 Michael Cullen <mich181189@fedoraproject.org> - 3.4.3-1
- Update to 3.4.3 (bugfix release)

* Tue Aug 28 2018 Major Hayden <major@redhat.com> - 3.4.2-4
- Added powerpc64le/ppc64le to ccache_trigger list

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 16 2018 Michael Cullen <mich181189@fedoraproject.org> - 3.4.2-2
- Fix i386 build error

* Wed Apr 11 2018 Michael Cullen <mich181189@fedoraproject.org> - 3.4.2-1
- Update to new version

* Fri Feb 16 2018 Michael Cullen <mich181189@fedoraproject.org> - 3.4.1-1
- Update to new version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 14 2018 Michael Cullen <mich181189@fedoraproject.org> - 3.3.5-1
- Update to new version

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 18 2017 Ville Skyttä <ville.skytta@iki.fi> - 3.3.4-1
- Update to 3.3.4

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 28 2016 Ville Skyttä <ville.skytta@iki.fi> - 3.3.3-1
- Update to 3.3.3

* Thu Sep 29 2016 Ville Skyttä <ville.skytta@iki.fi> - 3.3.2-1
- Update to 3.3.2

* Thu Sep  8 2016 Ville Skyttä <ville.skytta@iki.fi> - 3.3.1-1
- Update to 3.3.1, fixes #1373295

* Sun Aug 28 2016 Ville Skyttä <ville.skytta@iki.fi> - 3.3-1
- Update to 3.3
- Run tests with clang too

* Wed Aug 10 2016 Orion Poplawski <orion@cora.nwra.com> - 3.2.7-3
- Add needed requires for groupadd

* Tue Jul 26 2016 Ville Skyttä <ville.skytta@iki.fi> - 3.2.7-2
- Turn on CCACHE_CPP2 by default, fixes #1350086

* Wed Jul 20 2016 Ville Skyttä <ville.skytta@iki.fi> - 3.2.7-1
- Update to 3.2.7, fixes #1307367
- Add nacl*-gcc symlink triggers

* Thu Jul 14 2016 Ville Skyttä <ville.skytta@iki.fi> - 3.2.6-1
- Update to 3.2.6

* Mon Apr 18 2016 Ville Skyttä <ville.skytta@iki.fi> - 3.2.5-1
- Update to 3.2.5

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Ville Skyttä <ville.skytta@iki.fi> - 3.2.4-2
- Remove unnecessary %%defattr

* Fri Oct  9 2015 Ville Skyttä <ville.skytta@iki.fi> - 3.2.4-1
- Update to 3.2.4

* Mon Aug 17 2015 Ville Skyttä <ville.skytta@iki.fi> - 3.2.3-1
- Update to 3.2.3, fixes #1227819 and #1247493

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Ville Skyttä <ville.skytta@iki.fi> - 3.2.2-1
- Update to 3.2.2
- Add bunch of missing cross-gcc and c++ symlink triggers (#1205187)
- Fix cross-gcc symlink ownerships

* Fri Dec 12 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.2.1-1
- Update to 3.2.1

* Sun Nov 30 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.2-1
- Update to 3.2

* Mon Oct 20 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.1.10-1
- Update to 3.1.10

* Wed Sep 10 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.1.9-7
- Add clang and clang++ symlink triggers (#1140349, Jan Kratochvil)
- Mark license files as %%license where applicable

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 31 2013 Ville Skyttä <ville.skytta@iki.fi> - 3.1.9-3
- Apply upstream fix for gcc 4.8 test suite failure (#913915).
- Add arm-none-eabi and cross-gcc symlink triggers.
- Fix bogus dates in %%changelog.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  9 2013 Ville Skyttä <ville.skytta@iki.fi> - 3.1.9-1
- Update to 3.1.9.

* Sat Aug 18 2012 Ville Skyttä <ville.skytta@iki.fi> - 3.1.8-1
- Update to 3.1.8, fixes #783971.
- Update mingw* symlink triggers.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan  8 2012 Ville Skyttä <ville.skytta@iki.fi> - 3.1.7-1
- Update to 3.1.7.

* Sun Dec  4 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.1.6-2
- Turn on CCACHE_HASHDIR by default (#759592, Jan Kratochvil).

* Mon Aug 22 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.1.6-1
- Update to 3.1.6.

* Mon May 30 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.1.5-1
- Update to 3.1.5.

* Sat Apr  2 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.1.4-4
- Replace Requires(trigger*) with plain requires to appease rpmbuild >= 4.9.

* Sat Apr  2 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.1.4-3
- Reset non-working cache dir related env settings on user switch (#651023).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.1.4-1
- Update to 3.1.4.

* Sun Dec  5 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.1.3-2
- Update compiler executable lists, make their package triggers more targeted.
- Auto-symlink mingw32-gcc(-c++) compilers.

* Sun Nov 28 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.1.3-1
- Update to 3.1.3, fixes #657857.

* Tue Nov 23 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.1.2-1
- Update to 3.1.2.

* Thu Nov 18 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.1.1-1
- Update to 3.1.1.

* Sat Sep 18 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.1-1
- Update to 3.1, fixes #610853.
- Make sh profile script "nounset" clean.

* Fri Jul 16 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.0.1-1
- Update to 3.0.1.

* Sat Jul  3 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.0-1
- Update to 3.0, no-strip patch no longer needed.

* Fri Jun  4 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.0-0.2.pre1
- Reintroduce minor profile.d script performance improvements.

* Thu May 13 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.0-0.1.pre1
- Update to 3.0pre1 (#591040), license changed to GPLv3+.

* Mon Mar  1 2010 Ville Skyttä <ville.skytta@iki.fi> - 3.0-0.1.pre0
- Update to 3.0pre0, all old patches applied/superseded upstream.
  Note: old caches will no longer be used, see NEWS for details.
- Don't use "pathmunge" in the profile.d sh script to work around #548960.
- Patch to avoid stripping the binary during build.
- Add auto-symlink support for gcc44(-c++) and msp430-gcc.
- Run test suite during build.
- Update description.

* Sat Dec 19 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.4-17
- Minor profile.d script performance improvements.
- Fix hardcoded /var/cache/ccache in profile.d scripts.

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.4-16
- Switch #438201 patch URL to Debian patch tracking (original is MIA).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 19 2008 Ville Skyttä <ville.skytta@iki.fi> - 2.4-13
- Apply patch to fix path to saved dependency files (#438201).

* Sat Feb  9 2008 Ville Skyttä <ville.skytta@iki.fi> - 2.4-12
- Rebuild.

* Tue Oct  2 2007 Ville Skyttä <ville.skytta@iki.fi> - 2.4-11
- Apply upstream fix for problems when $HOME is not set (#315441).

* Wed Aug 22 2007 Ville Skyttä <ville.skytta@iki.fi>
- Fix URL to upstream tarball.

* Sun Aug 19 2007 Ville Skyttä <ville.skytta@iki.fi> - 2.4-10
- License: GPLv2+
- Make compiler symlinks relative.
- Make profile.d scripts noreplace.

* Mon Jul 30 2007 Ville Skyttä <ville.skytta@iki.fi> - 2.4-9
- Use shared cache dir for users in the ccache group by default
  (#247760, based on Andy Shevchenko's work).
- Fix outdated hardlink info in cache sharing docs.
- Add auto-symlink support for avr-gcc(-c++) and arm-gp2x-linux-gcc(-c++).
- Make triggers always exit with a zero exit status.

* Thu Mar 15 2007 Ville Skyttä <ville.skytta@iki.fi> - 2.4-8
- Bypass cache with --coverage, -fprofile-arcs and -ftest-coverage
  (upstream CVS and Matt Fago, #231462).

* Fri Nov 10 2006 Ville Skyttä <ville.skytta@iki.fi> - 2.4-7
- Require coreutils for triggers (#215030).

* Wed Aug  9 2006 Ville Skyttä <ville.skytta@iki.fi> - 2.4-6
- Add auto-symlink support for compat-gcc-34(-c++).
- Untabify, escape macros in changelog.

* Tue May 16 2006 Ville Skyttä <ville.skytta@iki.fi> - 2.4-5
- Add auto-symlink support for g++-libstdc++-so_7.

* Sat Nov 26 2005 Ville Skyttä <ville.skytta@iki.fi> - 2.4-4
- Drop "bin" from compiler symlink path.
- Make profile.d snippets non-executable (#35714).

* Sun May  1 2005 Ville Skyttä <ville.skytta@iki.fi> - 2.4-3
- Auto-symlink update: add compat-gcc-32 and compat-gcc-32-c++, drop
  bunch of no longer relevant compilers.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.4-2
- rebuilt

* Sun Sep 26 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:2.4-0.fdr.1
- Update to 2.4.
- Add symlinking support for gcc4 and gcc4-c++.
- Move the ccache executable to %%{_bindir}.
- Include more docs.

* Fri Jun 25 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:2.3-0.fdr.5
- Add support for gcc33 and g++33.

* Thu Jun 10 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:2.3-0.fdr.4
- Fix hardcoded lib path in profile.d scriptlets (bug 1558).

* Mon May  3 2004 Ville Skyttä <ville.skytta@iki.fi> - 0:2.3-0.fdr.3
- Add support for gcc34 and g++34, and
  %%{_target_cpu}-%%{_vendor}-%%{_target_os}-* variants.

* Thu Nov 13 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:2.3-0.fdr.2
- Add overriding symlinks for gcc-ssa and g++-ssa (bug 963).

* Tue Nov 11 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:2.3-0.fdr.1
- Update to 2.3.
- Implement triggers to keep list of "aliased" compilers up to date on the fly.
- Add gcc32 and a bunch of legacy packages to the list of overridden compilers.

* Sat Aug  2 2003 Ville Skyttä <ville.skytta@iki.fi> - 0:2.2-0.fdr.6
- Add c++ to the list of overridden compilers (bug 548).
- Own everything including dirs under %%{_libdir}/ccache (bug 529).
- %%{buildroot} -> $RPM_BUILD_ROOT.
- Fix man page permissions.
- Use %%{?_smp_mflags}.
- Other cosmetic specfile tweaks.

* Sat Mar 29 2003 Warren Togami <warren@togami.com> 2.2-0.fdr.5
- Epoch: 0
- Remove /usr/lib/ccache/sbin from PATH

* Fri Mar 28 2003 Warren Togami <warren@togami.com> 2.2-0.fdr.4
- Add BuildRequires: autoconf >= 0:2.52
- Add Requires: gcc, gcc-c++ (minimal expectation of compilers)

* Fri Mar 28 2003 Warren Togami <warren@togami.com> 2.2-0.fdr.3
- No longer use %%ghost, symlinks always exist

* Thu Mar 27 2003 Warren Togami <warren@togami.com> 2.2-0.fdr.2
- Move symlinks to /usr/lib/ccache/bin
- Use /etc/profile.d/ccache.* scripts to add it to PATH
  As long as it is before /usr/bin it is good.

* Thu Mar 27 2003 Warren Togami <warren@togami.com> 2.2-0.fdr.1
- Move symlinks to /bin since it seems to be at the beginning of PATH of all users
    before /usr/bin, the location of the real compiler.
- Package symlinks rather than create and remove during %%post and %%postun

* Thu Feb 20 2003 Warren Togami <warren@togami.com> 2.2-4.fedora.1
- Fedora

* Thu Feb 20 2003 Samir M. Nassar <rpm@redconcepts.net> 2.2-3.redconcepts
- Added symlinks to g++
- Removed symlink removal in post

* Thu Feb 20 2003 Samir M. Nassar <rpm@redconcepts.net> 2.2-2.redconcepts
- Cleans symlinks if present to make upgrades easier

* Thu Feb 20 2003 Samir M. Nassar <rpm@redconcepts.net> 2.2-1.redconcepts
- Upgraded to ccache 2.2

* Tue Feb 04 2003 Samir M. Nassar <rpm@redconcepts.net> 2.1.1-4.redconcepts
- Using %%post to create the soft symlinks
- Using %%postun to remove the soft symlinks
- Thanks to Che <che666@uni.de> for the help
- Packaged as user

* Sun Jan 19 2003 Samir M. Nassar <rpm@redconcepts.net> 2.1.1-3.redconcepts
- make a soft symlink between ccache and gcc
- make a soft symlink between ccache and cc

* Thu Jan 16 2003 Samir M. Nassar <rpm@redconcepts.net> 2.1.1-2.redconcepts
- Normalized spec file.

* Wed Jan 15 2003 Samir M, Nassar <rpm@redconcepts.net> 2.1.1-1.redconcepts
- Using ccache 2.2.1 sources
- Changed release to redconcepts for consistency

* Tue Oct 22 2002 Samir M. Nassar <rpm.redconcepts.net> 1.9-1.rcn
- Initial RedConcepts.NET (rcn) build for Red Hat Linux 8.0
