## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:          notcurses
Version:       3.0.17
Release:       %autorelease
Summary:       Character graphics and TUI library
License:       Apache-2.0
URL:           https://nick-black.com/dankwiki/index.php/Notcurses
Source0:       https://github.com/dankamongmen/%{name}/releases/download/v%{version}/notcurses_%{version}+dfsg.orig.tar.xz
Source1:       https://github.com/dankamongmen/%{name}/releases/download/v%{version}/notcurses_%{version}+dfsg.orig.tar.xz.asc
Source2:       https://nick-black.com/dankamongmen.gpg

BuildRequires: gnupg2
BuildRequires: cmake
BuildRequires: doctest-devel
BuildRequires: gcc-c++
BuildRequires: gpm-devel
BuildRequires: libdeflate-devel
BuildRequires: libqrcodegen-devel
BuildRequires: libunistring-devel
BuildRequires: ffmpeg-free-devel
BuildRequires: ncurses-devel
BuildRequires: pkgconfig(zlib)
BuildRequires: pandoc
BuildRequires: python3-devel
# for en_US.UTF-8 locale (we just want *some* UTF-8 one)
BuildRequires: glibc-langpack-en

%generate_buildrequires
cd cffi
%pyproject_buildrequires

%description
Notcurses facilitates the creation of modern TUI programs,
making full use of Unicode and 24-bit TrueColor. It presents
an API similar to that of Curses, and rides atop Terminfo.
This package includes C and C++ shared libraries.

%package devel
Summary:       Development files for the Notcurses library
License:       Apache-2.0
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for the notcurses library.

%package static
Summary:       Static library for the Notcurses library
License:       Apache-2.0
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description static
A statically-linked version of the notcurses library.

%package utils
Summary:       Binaries from the Notcurses project
License:       Apache-2.0
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description utils
Binaries from Notcurses, and multimedia content used thereby.

%package -n python3-%{name}
Summary:       Python wrappers for notcurses
License:       Apache-2.0
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
Python wrappers and a demonstration script for the notcurses library.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%define __cmake_in_source_build 1

%build
# fedora requires -fPIC for static libraries
%cmake -DUSE_QRCODEGEN=on -DDFSG_BUILD=on -DUSE_GPM=on \
 -DCMAKE_POSITION_INDEPENDENT_CODE=ON
%cmake_build
cd cffi
CFLAGS="-I../include -L../" %pyproject_wheel

%check
#ctest -V %{?_smp_mflags}

%install
%cmake_install
cd cffi
%pyproject_install

%files
%doc CONTRIBUTING.md doc/CURSES.md doc/HACKING.md doc/HISTORY.md INSTALL.md doc/OTHERS.md README.md USAGE.md NEWS.md TERMINALS.md
%license COPYRIGHT
%{_libdir}/libnotcurses-core.so.%{version}
%{_libdir}/libnotcurses-core.so.3
%{_libdir}/libnotcurses-ffi.so.%{version}
%{_libdir}/libnotcurses-ffi.so.3
%{_libdir}/libnotcurses.so.%{version}
%{_libdir}/libnotcurses.so.3
%{_libdir}/libnotcurses++.so.3
%{_libdir}/libnotcurses++.so.%{version}

%files devel
%{_includedir}/notcurses/
%{_includedir}/ncpp/
%{_libdir}/libnotcurses-core.so
%{_libdir}/libnotcurses-ffi.so
%{_libdir}/libnotcurses.so
%{_libdir}/libnotcurses++.so
%{_libdir}/cmake/Notcurses
%{_libdir}/cmake/Notcurses++
%{_libdir}/cmake/NotcursesCore
%{_libdir}/pkgconfig/notcurses-core.pc
%{_libdir}/pkgconfig/notcurses-ffi.pc
%{_libdir}/pkgconfig/notcurses.pc
%{_libdir}/pkgconfig/notcurses++.pc
%{_mandir}/man3/*.3*

%files static
%{_libdir}/libnotcurses-core.a
%{_libdir}/libnotcurses.a
%{_libdir}/libnotcurses++.a

%files utils
# Don't use a wildcard, lest we pull in notcurses-*pydemo.1.
%{_bindir}/ncls
%{_bindir}/ncneofetch
%{_bindir}/ncplayer
%{_bindir}/nctetris
%{_bindir}/notcurses-demo
%{_bindir}/notcurses-info
%{_bindir}/notcurses-input
%{_bindir}/notcurses-tester
%{_bindir}/tfman
%{_mandir}/man1/ncls.1*
%{_mandir}/man1/ncneofetch.1*
%{_mandir}/man1/ncplayer.1*
%{_mandir}/man1/nctetris.1*
%{_mandir}/man1/notcurses-demo.1*
%{_mandir}/man1/notcurses-info.1*
%{_mandir}/man1/notcurses-input.1*
%{_mandir}/man1/notcurses-tester.1*
%{_mandir}/man1/tfman.1*
%{_datadir}/%{name}

%files -n python3-%{name}
%{_bindir}/notcurses-pydemo
%{_bindir}/ncdirect-pydemo
%{_mandir}/man1/notcurses-pydemo.1*
%{_mandir}/man1/ncdirect-pydemo.1*
%{python3_sitearch}/notcurses-%{version}.dist-info/
%{python3_sitearch}/notcurses/
%attr(0755, -, -) %{python3_sitearch}/notcurses/notcurses.py
%{python3_sitearch}/*.so

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 3.0.17-3
- Latest state for notcurses

* Sat Nov 01 2025 Nick Black <dankamongmen@gmail.com> - 3.0.17-2
- remove patch applied upstream

* Sat Nov 01 2025 Nick Black <dankamongmen@gmail.com> - 3.0.17-1
- new upstream 3.0.17

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.0.16-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.0.16-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Aug 05 2025 Miro Hrončok <miro@hroncok.cz> - 3.0.16-5
- Install manual pages to the correct location

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Nick Black <dankamongmen@gmail.com> - 3.0.16-3
- move to new python packaging, closes #2377345

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.0.16-2
- Rebuilt for Python 3.14

* Sun May 04 2025 Nick Black <dankamongmen@gmail.com> - 3.0.16-1
- new upstream 3.0.16

* Mon Apr 28 2025 Nick Black <dankamongmen@gmail.com> - 3.0.14-1
- new upstream 3.0.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Nick Black <dankamongmen@gmail.com> - 3.0.13-1
- new upstream 3.0.13, new upstream naming

* Thu Jan 09 2025 Nick Black <dankamongmen@gmail.com> - 3.0.12-1
- new upstream 3.0.12

* Mon Oct 07 2024 Nick Black <dankamongmen@gmail.com> - 3.0.11-1
- new upstream 3.0.11, drop patch

* Mon Sep 23 2024 Fabio Valentini <decathorpe@gmail.com> - 3.0.9-6
- Rebuild for ffmpeg 7

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 3.0.9-5
- convert ASL 2.0 license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 3.0.9-3
- Rebuilt for Python 3.13

* Sat May 04 2024 Robert-André Mauchin <zebob.m@gmail.com> - 3.0.9-2
- Add compatibility with FFMPEG 7.0

* Sat Mar 23 2024 Nick Black <dankamongmen@gmail.com> - 3.0.9-1
- new upstream 3.0.9

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 3.0.8-7
- Rebuilt for Python 3.12

* Sun Mar 12 2023 Neal Gompa <ngompa@fedoraproject.org> - 3.0.8-6
- Rebuild for ffmpeg 6.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Aug 29 2022 Neal Gompa <ngompa@fedoraproject.org> - 3.0.8-4
- Rebuild for ffmpeg 5.1 (#2121070)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.0.8-2
- Rebuilt for Python 3.11

* Wed Apr 06 2022 Nick Black <dankamongmen@gmail.com> - 3.0.8-1
- new upstream 3.0.8

* Tue Mar 08 2022 Nick Black <dankamongmen@gmail.com> - 3.0.7-7
- disable tests for a minute

* Tue Mar 08 2022 Nick Black <dankamongmen@gmail.com> - 3.0.7-6
- use ffmpeg rather than openimageio

* Tue Mar 08 2022 Nick Black <dankamongmen@gmail.com> - 3.0.7-5
- erp

* Tue Mar 08 2022 Nick Black <dankamongmen@gmail.com> - 3.0.7-4
- patch up to only use free videos

* Tue Mar 08 2022 Nick Black <dankamongmen@gmail.com> - 3.0.7-3
- replace OIIO with ffmpeg-free-devel

* Mon Feb 21 2022 Nick Black <dankamongmen@gmail.com> - 3.0.7-2
- patch for big-endian unit tests

* Mon Feb 21 2022 Nick Black <dankamongmen@gmail.com> - 3.0.7-1
- new upstream 3.0.7

* Thu Feb 10 2022 Nick Black <dankamongmen@gmail.com> - 3.0.6-1
- new upstream 3.0.6

* Fri Jan 21 2022 Nick Black <dankamongmen@gmail.com> - 3.0.5-1
- new upstream 3.0.5

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Nick Black <dankamongmen@gmail.com> - 3.0.4-1
- update to new upstream 3.0.4

* Sun Jan 02 2022 Nick Black <dankamongmen@gmail.com> - 3.0.3-3
- install ffi pkgconfig

* Sun Jan 02 2022 Nick Black <dankamongmen@gmail.com> - 3.0.3-2
- install libnotcurses-ffi files

* Sun Jan 02 2022 Nick Black <dankamongmen@gmail.com> - 3.0.3-1
- new upstream 3.0.3

* Tue Dec 21 2021 Nick Black <dankamongmen@gmail.com> - 3.0.2-1
- new upstream 3.0.2

* Sun Dec 12 2021 Nick Black <dankamongmen@gmail.com> - 3.0.1-1
- new upstream 3.0.1

* Fri Dec 03 2021 Nick Black <dankamongmen@gmail.com> - 3.0.0-2
- upload 3.0.0 sources

* Fri Dec 03 2021 Nick Black <dankamongmen@gmail.com> - 3.0.0-1
- new upstream 3.0.0, API3/ABI3

* Thu Nov 11 2021 Nick Black <dankamongmen@gmail.com> - 2.4.9-1
- new upstream 2.4.9

* Mon Oct 25 2021 Nick Black <dankamongmen@gmail.com> - 2.4.8-1
- new upstream 2.4.8

* Sun Oct 17 2021 Nick Black <dankamongmen@gmail.com> - 2.4.7-1
- new upstream 2.4.7

* Thu Oct 07 2021 Nick Black <dankamongmen@gmail.com> - 2.4.5-1
- new upstream 2.4.5

* Tue Oct 05 2021 Richard Shaw <hobbes1069@gmail.com> - 2.4.4-2
- Rebuild for OpenImageIO 2.3.8.0.

* Sun Oct 03 2021 Nick Black <dankamongmen@gmail.com> - 2.4.4-1
- new upstream 2.4.4

* Sun Sep 26 2021 Nick Black <dankamongmen@gmail.com> - 2.4.3-1
- new upstream 2.4.3

* Mon Sep 20 2021 Nick Black <dankamongmen@gmail.com> - 2.4.2-1
- new upstream 2.4.2

* Mon Sep 13 2021 Nick Black <dankamongmen@gmail.com> - 2.4.1-1
- new upstream 2.4.1

* Mon Sep 06 2021 Nick Black <dankamongmen@gmail.com> - 2.4.0-1
- new upstream 2.4.0

* Wed Sep 01 2021 Nick Black <dankamongmen@gmail.com> - 2.3.18-2
- add sources erp

* Wed Sep 01 2021 Nick Black <dankamongmen@gmail.com> - 2.3.18-1
- new upstream version 2.3.18

* Mon Aug 30 2021 Nick Black <dankamongmen@gmail.com> - 2.3.17-2
- add gpm-devel dep and cmake def for next release

* Mon Aug 23 2021 Nick Black <dankamongmen@gmail.com> - 2.3.17-1
- new upstream 2.3.17

* Fri Aug 20 2021 Nick Black <dankamongmen@gmail.com> - 2.3.16-1
- new upstream 2.3.16

* Wed Aug 18 2021 Nick Black <dankamongmen@gmail.com> - 2.3.15-1
- new upstream 2.3.15

* Thu Aug 05 2021 Nick Black <dankamongmen@gmail.com> - 2.3.13-1
- new upstream 2.3.13

* Thu Jul 29 2021 Nick Black <dankamongmen@gmail.com> - 2.3.12-2
- replace zlib-devel with pkgconfig(zlib)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Nick Black <dankamongmen@gmail.com> - 2.3.11-1
- New upstream release, add zlib-devel dep

* Mon Jul 12 2021 Nick Black <dankamongmen@gmail.com> - 2.3.9-1
- New upstream release, bugfix-oriented

* Tue Jun 29 2021 Nick Black <dankamongmen@gmail.com> - 2.3.7-1
- New upstream release

* Wed Jun 23 2021 Nick Black <dankamongmen@gmail.com> - 2.3.6-1
- New upstream release

* Sat Jun 12 2021 Nick Black <dankamongmen@gmail.com> - 2.3.4-1
- New upstream release, new notcurses-info binary

* Mon Jun 07 2021 Python Maint <python-maint@redhat.com> - 2.3.2-2
- Rebuilt for Python 3.10

* Sun Jun 06 2021 Nick Black <dankamongmen@gmail.com> - 2.3.2-1
- New upstream release

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.3.1-3
- Rebuilt for Python 3.10

* Wed May 19 2021 Nick Black <dankamongmen@gmail.com> - 2.3.1-2
- Apply patch from @scauligi for cffi on arch

* Tue May 18 2021 Nick Black <dankamongmen@gmail.com> - 2.3.1-1
- New upstream

* Sun May 09 2021 Nick Black <dankamongmen@gmail.com> - 2.3.0-1
- New upstream

* Wed May 05 2021 Nick Black <dankamongmen@gmail.com> - 2.2.10-1
- New upstream, brown-bagger fixes assert failures

* Mon May 03 2021 Nick Black <dankamongmen@gmail.com> - 2.2.9-1
- New upstream

* Sun Apr 18 2021 Nick Black <dankamongmen@gmail.com> - 2.2.8-1
- New upstream

* Mon Apr 12 2021 Nick Black <dankamongmen@gmail.com> - 2.2.6-3
- New upstream, add explicit -DUSE_QRCODEGEN=ON

* Tue Mar 09 2021 Nick Black <dankamongmen@gmail.com> - 2.2.3-2
- New upstream, add CMAKE_POSITION_INDEPENDENT_CODE=ON

* Thu Feb 18 2021 Nick Black <dankamongmen@gmail.com> - 2.2.2-1
- New upstream

* Tue Feb 09 2021 Nick Black <dankamongmen@gmail.com> - 2.2.1-1
- New upstream, fixes Direct Mode UTF8 detection brown-bagger

* Mon Feb 08 2021 Nick Black <dankamongmen@gmail.com> - 2.2.0-1
- New upstream

* Wed Feb 03 2021 Nick Black <dankamongmen@gmail.com> - 2.1.8-1
- New upstream

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Nick Black <dankamongmen@gmail.com> - 2.1.7-1
- New upstream, split notcurses and notcurses-core

* Fri Jan 15 2021 Nick Black <dankamongmen@gmail.com> - 2.1.5-1
- New upstream version, add readline-dev dep

* Sun Jan 03 2021 Nick Black <dankamongmen@gmail.com> - 2.1.4-1
- New upstream version

* Thu Dec 31 2020 Nick Black <dankamongmen@gmail.com> - 2.1.3-1
- New upstream version, fixes crash in notcurses-demo

* Sat Dec 26 2020 Nick Black <dankamongmen@gmail.com> - 2.1.2-1
- New upstream version, sexblitter by default on some terms

* Wed Dec 16 2020 Nick Black <dankamongmen@gmail.com> - 2.1.1-1
- New upstream version, progress bar widget

* Sun Dec 13 2020 Nick Black <dankamongmen@gmail.com> - 2.1.0-1
- New upstream version, fixes resize cascade

* Wed Dec 09 2020 Nick Black <dankamongmen@gmail.com> - 2.0.11-1
- New upstream version, fixes many big-endian issues

* Sun Dec 06 2020 Nick Black <dankamongmen@gmail.com> - 2.0.10-1
- New upstream version

* Tue Dec 01 2020 Nick Black <dankamongmen@gmail.com> - 2.0.9-1
- New upstream version, several important bugfixes, add "ncls"

* Fri Nov 27 2020 Nick Black <dankamongmen@gmail.com> - 2.0.8-1
- New upstream version, relaxes pypandoc depend version

* Sat Nov 21 2020 Nick Black <dankamongmen@gmail.com> - 2.0.7-1
- New upstream version

* Tue Nov 10 2020 Nick Black <dankamongmen@gmail.com> - 2.0.4-1
- New upstream version, fixes unit tests for non-UTF8

* Mon Nov 9 2020 Nick Black <dankamongmen@gmail.com> - 2.0.3-1
- New upstream version including sexblitter, keller demo

* Sun Oct 25 2020 Nick Black <dankamongmen@gmail.com> - 2.0.2-1
- New upstream version, ncvisual_decode_loop()

* Mon Oct 19 2020 Nick Black <dankamongmen@gmail.com> - 2.0.1-1
- New upstream version, quadblitter perf+transparency improvements

* Tue Oct 13 2020 Nick Black <dankamongmen@gmail.com> - 2.0.0-1
- New upstream version, stable API!

* Sat Oct 10 2020 Nick Black <dankamongmen@gmail.com> - 1.7.6-1
- New upstream version

* Tue Sep 29 2020 Nick Black <dankamongmen@gmail.com> - 1.7.5-1
- New upstream version, drop notcurses-ncreel binary

* Sun Sep 20 2020 Nick Black <dankamongmen@gmail.com> - 1.7.4-1
- New upstream version

* Sat Sep 19 2020 Nick Black <dankamongmen@gmail.com> - 1.7.3-1
- New upstream version

* Fri Sep 11 2020 Nick Black <dankamongmen@gmail.com> - 1.7.2-1
- New upstream version

* Thu Aug 27 2020 Nick Black <dankamongmen@gmail.com> - 1.6.19-1
- New upstream version, reenable unit tests for s390

* Wed Aug 12 2020 Nick Black <dankamongmen@gmail.com> - 1.6.12-1
- New upstream version, many small bugfixes

* Mon Aug 03 2020 Nick Black <dankamongmen@gmail.com> - 1.6.11-1
- New upstream version with new 'zoo' demo

* Sun Aug 02 2020 Nick Black <dankamongmen@gmail.com> - 1.6.10-1
- New upstream version with Linux console font reprogramming

* Sun Jul 12 2020 Nick Black <dankamongmen@gmail.com> - 1.6.1-1
- New upstream version, purge vt100 patch (applied upstream), install TERMS.md

* Sat Jul 04 2020 Nick Black <dankamongmen@gmail.com> - 1.6.0-1
- New upstream version, backport patch to work on vt100 autobuilder, enable all tests

* Sun Jun 28 2020 Nick Black <dankamongmen@gmail.com> - 1.5.3-1
- New upstream version

* Fri Jun 19 2020 Nick Black <dankamongmen@gmail.com> - 1.5.2-1
- New upstream version, new binary 'ncneofetch'

* Sun Jun 14 2020 Nick Black <dankamongmen@gmail.com> - 1.5.1-1
- New upstream version

* Mon Jun 08 2020 Nick Black <dankamongmen@gmail.com> - 1.5.0-1
- New upstream version

* Sat Jun 06 2020 Nick Black <dankamongmen@gmail.com> - 1.4.5-1
- New upstream version, disable Ncpp,Exceptions unit tests for now

* Tue Jun 02 2020 Nick Black <dankamongmen@gmail.com> - 1.4.4.1-1
- New upstream version

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4.3-3
- Rebuilt for Python 3.9

* Sun May 24 2020 Nick Black <dankamongmen@gmail.com> - 1.4.3-2
- Dep on doctest-devel, run tests, use _target_platform in place of "build"

* Fri May 22 2020 Nick Black <dankamongmen@gmail.com> - 1.4.3-1
- New upstream version

* Wed May 20 2020 Nick Black <dankamongmen@gmail.com> - 1.4.2.4-1
- New upstream version, add python3-setuptools dep

* Sun May 17 2020 Nick Black <dankamongmen@gmail.com> - 1.4.2.3-1
- New upstream version

* Sat Apr 25 2020 Nick Black <dankamongmen@gmail.com> - 1.4.1-1
- New upstream version, incorporate review feedback
- Build against OpenImageIO, install notcurses-view and data

* Tue Apr 07 2020 Nick Black <dankamongmen@gmail.com> - 1.3.3-1
- Initial Fedora packaging

## END: Generated by rpmautospec
