# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           inotify-tools
Version:        4.23.9.0
Release: 6%{?dist}
Summary:        Command line utilities for inotify

# GPL-2.0-only: the project as a whole
# GPL-2.0-only WITH Linux-syscall-note: libinotifytools/src/inotifytools/fanotify-dfid-name.h
# LGPL-2.1-or-later: libinotifytools/src/redblack.{cpp,h}
License:        GPL-2.0-only AND GPL-2.0-only WITH Linux-syscall-note AND LGPL-2.1-or-later
URL:            https://github.com/inotify-tools/inotify-tools
Source0:        https://github.com/inotify-tools/inotify-tools/archive/%{version}/inotify-tools-%{version}.tar.gz
Patch0:         too-many-args.patch

BuildRequires:  gcc-c++
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  doxygen
BuildRequires:  make
BuildRequires:  libtool

%description
inotify-tools is a set of command-line programs for Linux providing
a simple interface to inotify. These programs can be used to monitor
and act upon filesystem events.

%package        devel
Summary:        Headers and libraries for building apps that use libinotifytools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains headers and libraries required to build applications
that use the libinotifytools library.

%prep
%autosetup -p1


%build
./autogen.sh
%configure \
        --disable-dependency-tracking \
        --disable-static \
        --enable-doxygen \
        --enable-fanotify

# Get rid of undesirable hardcoded rpaths; workaround libtool reordering
# -Wl,--as-needed after all the libraries.
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|CC="\(.*g..\)"|CC="\1 -Wl,--as-needed"|' \
    -i libtool

%make_build


%install
%make_install

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
# We'll install documentation in the proper place
rm -rf %{buildroot}/%{_datadir}/doc/



%ldconfig_scriptlets


%files
%doc AUTHORS COPYING ChangeLog NEWS README.md
%{_bindir}/fsnotifywait
%{_bindir}/fsnotifywatch
%{_bindir}/inotifywait
%{_bindir}/inotifywatch
%{_libdir}/libinotifytools.so.*
%{_mandir}/man1/inotifywait.1*
%{_mandir}/man1/inotifywatch.1*
%{_mandir}/man1/fsnotifywait.1*
%{_mandir}/man1/fsnotifywatch.1*

%files devel
%doc libinotifytools/src/doc/html/*
%dir %{_includedir}/inotifytools/
%{_includedir}/inotifytools/inotify.h
%{_includedir}/inotifytools/inotify-nosys.h
%{_includedir}/inotifytools/inotifytools.h
%{_includedir}/inotifytools/fanotify-dfid-name.h
%{_includedir}/inotifytools/fanotify.h
%{_libdir}/libinotifytools.so


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.23.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Feb 19 2025 Jan Kratochvil <jan@jankratochvil.net> - 4.23.9.0-4
- Fix memory corruption with too many arguments
  https://bugzilla.redhat.com/show_bug.cgi?id=2345921
- Use %%autosetup

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.23.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.23.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 22 2024 Jerry James <loganjerry@gmail.com> - 4.23.9.0-1
- Update to 4.23.9.0
- SPDX migration
- Enable fanotify support
- Minor spec file cleanups

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 22 2021 Eric Curtin <ecurtin@redhat.com> - 3.22.1.0-1
- Update to 3.22.1.0

* Wed Sep 22 2021 Eric Curtin <ecurtin@redhat.com> - 3.21.9.5-1
- Update to 3.21.9.5

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 06 2019 Jan Kratochvil <jan.kratochvil@redhat.com> - 3.14-19
- Fix source package URL (fix by Breno Brand Fernandes).

* Thu Sep 05 2019 Jan Kratochvil <jan.kratochvil@redhat.com> - 3.14-18
- Fix stack corruption on a moved directory, reproducible on aarch64.
  https://bugzilla.redhat.com/show_bug.cgi?id=1741472
  0006-Fix-buffer-overrun-in-inotifytools.c.patch
- Fix buffer overrun on -c|--csv with '"', ',' or '\n' in directory name.
  0005-Fix-segfault-with-csv-output-when-filename-contains-.patch
- Remove rpath to pass a rpmbuild check.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Nov 14 2010 Adel Gadllah <adel.gadllah@gmail.com> - 3.14-1
- Update to 3.14

* Sat Feb 13 2010 Adel Gadllah <adel.gadllah@gmail.com> - 3.13-4
- Don't run make check, it fails on the builders

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 11 2008 Adel Gadllah <adel.gadllah@gmail.com> 3.13-1
- Update to 3.13

* Mon Sep 24 2007 Dawid Gajownik <gajownik[AT]gmail.com> - 3.11-1
- Update to 3.11 (CVE-2007-5037, #299771)
- Fix License tag

* Sun Dec 17 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 3.6-1
- Update to 3.6

* Tue Oct 31 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 3.3-1
- Update to 3.3
- Add %%check stage

* Sat Oct 28 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 3.1-1
- Update to 3.1
- Add -devel subpackage

* Tue Oct  3 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 2.6-1
- Update to 2.6

* Mon Oct  2 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 2.5-1
- Update to 2.5

* Sat Sep  9 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 2.4-1
- Update to 2.4

* Tue Aug 15 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 2.3-1
- Update to 2.3
- Drop implicit_syscall patch (fixed upstream)

* Mon Jul 31 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 2.2-3
- Fix URL

* Thu Jul  6 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 2.2-2
- Fix compilation warnings

* Thu Jul  6 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 2.2-1
- New version 2.2
- Update URL and description
- Add man pages

* Wed Jul  5 2006 Dawid Gajownik <gajownik[AT]gmail.com> - 2.1-1
- Initial RPM release.
