# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global expat_version 1.95.5
%global glib2_version 2.40.0
%global dbus_version 1.8

Name:    dbus-glib
Version: 0.112
Release: 11%{?dist}
Summary: GLib bindings for D-Bus

# dbus/dbus-bash-completion-helper.c is GPL-2.0-or-later
# some tests are (LGPL-2.1-or-later OR MIT) AND MIT, but not included in rpm
License: (AFL-2.1 OR GPL-2.0-or-later) AND GPL-2.0-or-later
URL:     https://www.freedesktop.org/software/dbus/
#VCS:    git:https://gitlab.freedesktop.org/dbus/dbus-glib.git
Source0: https://dbus.freedesktop.org/releases/dbus-glib/%{name}-%{version}.tar.gz
Source1: https://dbus.freedesktop.org/releases/dbus-glib/%{name}-%{version}.tar.gz.asc
# gpg --keyserver keyring.debian.org --recv-keys 36EC5A6448A4F5EF79BEFE98E05AE1478F814C4F
# gpg --export --export-options export-minimal 0x36EC5A6448A4F5EF79BEFE98E05AE1478F814C4F > gpgkey-36EC5A6448A4F5EF79BEFE98E05AE1478F814C4F.gpg
Source2: gpgkey-36EC5A6448A4F5EF79BEFE98E05AE1478F814C4F.gpg

BuildRequires: pkgconfig(dbus-1) >= %{dbus_version}
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: expat-devel >= %{expat_version}
BuildRequires: /usr/bin/chrpath
BuildRequires: dbus-daemon
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: gnupg2
BuildRequires: make

%description

D-Bus add-on library to integrate the standard D-Bus library with
the GLib thread abstraction and main loop.

%package devel
Summary: Libraries and headers for the D-Bus GLib bindings
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel

Headers and static libraries for the D-Bus GLib bindings

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
%set_build_flags
export CFLAGS="$CFLAGS -std=gnu17"
%configure --enable-tests=yes \
	--enable-asserts=yes \
	--disable-gtk-doc

%make_build

%check
%make_build check


%install
%make_install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

chrpath --delete $RPM_BUILD_ROOT%{_bindir}/dbus-binding-tool
chrpath --delete $RPM_BUILD_ROOT%{_libexecdir}/dbus-bash-completion-helper

# Scripts that are sourced should not be executable.
chmod -x $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/dbus-bash-completion.sh


%ldconfig_scriptlets

%files
%doc NEWS
%license COPYING
%{_libdir}/libdbus-glib-1.so.*
%{_bindir}/dbus-binding-tool
%{_mandir}/man1/dbus-binding-tool.1*

%files devel
%{_libdir}/libdbus-glib-1.so
%{_libdir}/pkgconfig/dbus-glib-1.pc
%{_includedir}/dbus-1.0/dbus/*
%{_datadir}/gtk-doc/html/dbus-glib
%{_sysconfdir}/bash_completion.d/dbus-bash-completion.sh
%{_libexecdir}/dbus-bash-completion-helper


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.112-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Mar 26 2021 David King <amigadave@amigadave.com> - 0.112-1
- Update to 0.112

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 0.110-8
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 10 2019 Scott Talbert <swt@techie.net> - 0.110-5
- Add dbus-daemon to BRs to fix FTBFS (#1674792)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.110-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 David King <amigadave@amigadave.com> - 0.110-1
- Update to 0.110

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.108-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.108-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.108-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 09 2016 David King <amigadave@amigadave.com> - 0.108-1
- Update to 0.108
- Enable tests
- Remove obsolete Requires and Obsoletes

* Tue Feb 02 2016 David King <amigadave@amigadave.com> - 0.106-1
- Update to 0.106

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.104-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.104-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Feb 09 2015 David King <amigadave@amigadave.com> - 0.104-1
- Update to 0.104
- Remove RPATH
- Remove executable bit from sourced script
- Move man page to main package and update glob
- Make the build output more verbose

* Sat Feb 07 2015 David King <amigadave@amigadave.com> - 0.102-1
- Update to 0.102
- Use pkgconfig for BuildRequires
- Remove outdated gtk subpackage
- Use license for COPYING
- Tighten subpackage dependencies with the isa macro
- Tidy spec file
- Preserve timestamps during install

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 01 2013 Colin Walters <walters@redhat.com> - 0.100.2
- New upstream version

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 0.100-4
- Don't install ChangeLog (need to save space on the live image)

* Wed Feb 20 2013 Colin Walters <walters@redhat.com> - 0.100-3
- CVE-2013-0292
  Resolves: #911714

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 17 2012 Colin Walters <walters@verbum.org> - 0.100-1
- Update to 0.100

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Christopher Aillon <caillon@redhat.com> - 0.92-1
- Update to 0.92

* Wed Sep 29 2010 jkeating - 0.88-3
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Colin Walters <walters@verbum.org> - 0.88-2
- Drop .gir file, it's now in gobject-introspection

* Thu Aug 12 2010 Colin Walters <walters@verbum.org> - 0.88-1
- New upstream version
- drop now-merged shadow props patch

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 0.86-4
- Rebuild against new gobject-introspection

* Tue Jun 29 2010 Dan Williams <dcbw@redhat.com> - 0.86-3
- Fix shadow property access (fdo #28835)

* Tue Jun 29 2010 Bastien Nocera <bnocera@redhat.com> 0.86-2
- Add introspection data from gir-repository
- Remove unneeded autotools calls

* Thu Mar 18 2010 Colin Walters <walters@verbum.org> - 0.86-1
- New upstream
  Drop upstreamed patch

* Tue Mar 02 2010 Colin Walters <walters@verbum.org> - 0.84-3
- Revert previous broken patch for error names, add better fix

* Mon Feb 15 2010 Colin Walters <walters@verbum.org> - 0.84-2
- Add patch to avoid assertions when setting a GError that
  includes a '-' in the enumeration value.  Should fix #528897

* Wed Jan 27 2010 Colin Walters <walters@verbum.org> - 0.84-1
- New upstream
  Has introspect.xml internally, drop it from here

* Fri Jan 15 2010 Colin Walters <walters@verbum.org> - 0.82-3
- Add ListActivatableNames to dbus-bus-introspect.xml to help tracker build

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Colin Walters <walters@verbum.org> - 0.82-1
- New upstream 0.82
- Remove mclasen accidental commit of CFLAGS="-O0 -g3"

* Sun Jun 14 2009 Matthias Clasen <mclasen@redhat.com> - 0.80-3
- Minor directory ownership cleanup

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Colin Walters <walters@verbum.org> - 0.80-1
- New upstream release
- Adjust to new bash completion dir
- Includes patch noreply patch

* Wed Jan 07 2009 Colin Walters <walters@verbum.org> - 0.78-2
- Add patch to avoid sending reply to noreply messages; this avoids
  some spurious dbus denial logs during system startup from NM

* Thu Dec 04 2008 Colin Walters <walters@verbum.org> - 0.78-1
- New upstream release, drop upstreamed patches

* Tue Nov 25 2008 Matthias Clasen <mclasen@redhat.com> - 0.76-4
- Avoid some spurious linkage

* Mon Nov 17 2008 Dan Williams <dcbw@redhat.com> - 0.76-3
- Fix crashes when a tracked service restarts too quickly (fdo #18573)

* Thu Jul 31 2008 David Zeuthen <davidz@redhat.com> - 0.76-2
- Add bash completion for dbus-send(1)

* Thu Jun 05 2008 Colin Walters <walters@redhat.com> - 0.76-1
- New upstream 0.76
- Drop all upstreamed patches

* Tue May 27 2008 Dan Williams <dcbw@redhat.com> - 0.74-9
- Handle unknown object properties without asserting (fdo #16079)
- Handle GetAll() property names correctly (fdo #16114)
- Enable the freeze-abi patch
- Cherry-pick some fixes from upstream git

* Thu May  8 2008 Matthias Clasen <mclasen@redhat.com> - 0.74-8
- Fix license field

* Tue Apr 15 2008 Colin Walters <walters@redhat.com> - 0.74-7
- Ensure ABI is frozen as it stands now

* Fri Apr  4 2008 David Zeuthen <davidz@redhat.com> - 0.74-6
- Add another upstreamed patch for setting the default timeout
  on a proxy

* Fri Apr  4 2008 David Zeuthen <davidz@redhat.com> - 0.74-5
- Add an already upstreamed patch to export the GetAll() method on
  the org.freedesktop.DBus.Properties interface

* Wed Mar 19 2008 Dan Williams <dcbw@redhat.com> - 0.74-4
- Ignore children of namespaced nodes too

* Tue Feb 12 2008 Dan Williams <dcbw@redhat.com> - 0.74-3
- Ignore namespaces in introspection XML

* Sun Nov 18 2007 Dan Williams <dcbw@redhat.com> - 0.74-2
- Actually apply the patch for fdo #12505

* Mon Oct 22 2007 Ray Strode <rstrode@redhat.com> - 0.74-1
- Update to 0.74

* Mon Sep 24 2007 Dan Williams <dcbw@redhat.com> - 0.73-4
- Dispatch NameOwnerChanged signals to proxies only once (fdo #12505)

* Sat Sep 15 2007 Matthias Clasen <mclasen@redhat.com> - 0.73-3
- Rebuild against new expat

* Wed Aug  1 2007 Matthias Clasen <mclasen@redhat.com> - 0.73-2
- Fix a bug in introspection support (#248150)

* Wed Apr  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.73-1
- Update to 0.73 (#233631)
- Drop upstreamed patches

* Tue Dec 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.71-4
- Add dbus-glib-0.70-use-default-threads.patch
- Partial fix to #219257

* Wed Nov 29 2006 David Zeuthen <davidz@redhat.com> - 0.71-3%{?dist}
- Add dbus-glib-0.70-fix-info-leak.patch
- Resolves: #216034

* Sun Nov  5 2006 Matthias Clasen <mclasen@redhat.com> - 0.71-2
- Fix up Requires for the -devel package

* Mon Oct 23 2006 Matthias Clasen <mclasen@redhat.com> - 0.71-1
- Update to 0.71

* Thu Jul 20 2006 Jesse Keating <jkeating@redhat.com> - 0.70-4
- remove improper obsoletes

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-3
- Pregenerate the xml introspect file so you don't need dbus running during
  the build 

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-2
- Spec file cleanups

* Mon Jul 17 2006 John (J5) Palmieri <johnp@redhat.com> - 0.70-1
- Initial dbus-glib package
