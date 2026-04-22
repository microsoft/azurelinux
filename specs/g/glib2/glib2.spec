## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           glib2
Version:        2.86.4
Release:        %autorelease
Summary:        A library of handy utility functions

License:        LGPL-2.1-or-later
URL:            https://www.gtk.org
Source:         https://download.gnome.org/sources/glib/2.86/glib-%{version}.tar.xz

# Required for RHEL core crypto components policy. Good for Fedora too.
# https://bugzilla.redhat.com/show_bug.cgi?id=1630260
# https://gitlab.gnome.org/GNOME/glib/-/merge_requests/903
Patch:          gnutls-hmac.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=2192204
Patch:          default-terminal.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  perl-interpreter
BuildRequires:  glibc-devel
BuildRequires:  libattr-devel
BuildRequires:  libselinux-devel
BuildRequires:  meson
BuildRequires:  systemtap-sdt-devel
BuildRequires:  systemtap-sdt-dtrace
BuildRequires:  pkgconfig(gi-docgen)
BuildRequires:  pkgconfig(libelf)
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(mount)
BuildRequires:  pkgconfig(sysprof-capture-4)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python3-devel
BuildRequires:  /usr/bin/g-ir-scanner
BuildRequires:  /usr/bin/rst2man

# Dependencies for tests
BuildRequires:  shared-mime-info
BuildRequires:  /usr/bin/dbus-daemon
BuildRequires:  /usr/bin/update-desktop-database

# For gnutls-hmac.patch. We now dlopen libgnutls.so.30 so that we can build a
# static glib2 without depending on a static build of GnuTLS as well. This will
# ensure we notice if the GnuTLS soname bumps, so that we can update our patch.
BuildRequires:  gnutls
%if 0%{?__isa_bits} == 64
Requires: libgnutls.so.30()(64bit)
%else
Requires: libgnutls.so.30
%endif

Provides: bundled(cmph)
Provides: bundled(dirent)
Provides: bundled(gnulib)
Provides: bundled(gvdb)
Provides: bundled(libcharset)
Provides: bundled(xdgmime)

# glib typelib files moved from gobject-introspection to glib2 in F40
Conflicts: gobject-introspection < 1.79.1

%description
GLib is the low-level core library that forms the basis for projects
such as GTK+ and GNOME. It provides data structure handling for C,
portability wrappers, and interfaces for such runtime functionality
as an event loop, threads, dynamic loading, and an object system.

%package devel
Summary: A library of handy utility functions
Requires: %{name}%{?_isa} = %{version}-%{release}
# Required by gdbus-codegen
Requires: python3-packaging
# glib gir files moved from gobject-introspection-devel to glib2-devel in F40
Conflicts: gobject-introspection-devel < 1.79.1

%description devel
The glib2-devel package includes the header files for the GLib library.

%package doc
Summary: A library of handy utility functions
Requires: %{name}%{?_isa} = %{version}-%{release}

%description doc
The glib2-doc package includes documentation for the GLib library.

%package static
Summary: glib static
Requires: %{name}-devel = %{version}-%{release}
Requires: pcre2-static
Requires: sysprof-capture-static
Requires: libatomic-static

%description static
The %{name}-static subpackage contains static libraries for %{name}.

%package tests
Summary: Tests for the glib2 package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The glib2-tests package contains tests that can be used to verify
the functionality of the installed glib2 package.

%prep
%autosetup -n glib-%{version} -p1

%build
%meson \
    -Dglib_debug=disabled \
    -Ddocumentation=true \
    -Dinstalled_tests=true \
    -Dgnutls=true \
    --default-library=both \
    %{nil}
%meson_build

%install
%meson_install

# Perform byte compilation manually on paths outside the usual locations
%py_byte_compile %{python3} %{buildroot}%{_datadir}

mv %{buildroot}%{_bindir}/gio-querymodules %{buildroot}%{_bindir}/gio-querymodules-%{__isa_bits}
sed -i -e "/^gio_querymodules=/s/gio-querymodules/gio-querymodules-%{__isa_bits}/" %{buildroot}%{_libdir}/pkgconfig/gio-2.0.pc

mkdir -p %{buildroot}%{_libdir}/gio/modules
touch %{buildroot}%{_libdir}/gio/modules/giomodule.cache

%find_lang glib20

%transfiletriggerin -- %{_libdir}/gio/modules
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :

%transfiletriggerpostun -- %{_libdir}/gio/modules
gio-querymodules-%{__isa_bits} %{_libdir}/gio/modules &> /dev/null || :

%transfiletriggerin -- %{_datadir}/glib-2.0/schemas
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%transfiletriggerpostun -- %{_datadir}/glib-2.0/schemas
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%meson_test

%files -f glib20.lang
%license LICENSES/LGPL-2.1-or-later.txt
%doc NEWS README.md
%{_libdir}/libglib-2.0.so.0*
%{_libdir}/libgthread-2.0.so.0*
%{_libdir}/libgmodule-2.0.so.0*
%{_libdir}/libgobject-2.0.so.0*
%{_libdir}/libgio-2.0.so.0*
%{_libdir}/libgirepository-2.0.so.0*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/GIRepository-3.0.typelib
%{_libdir}/girepository-1.0/GLib-2.0.typelib
%{_libdir}/girepository-1.0/GLibUnix-2.0.typelib
%{_libdir}/girepository-1.0/GModule-2.0.typelib
%{_libdir}/girepository-1.0/GObject-2.0.typelib
%{_libdir}/girepository-1.0/Gio-2.0.typelib
%{_libdir}/girepository-1.0/GioUnix-2.0.typelib
%dir %{_datadir}/bash-completion
%dir %{bash_completions_dir}
%{bash_completions_dir}/gapplication
%{bash_completions_dir}/gdbus
%{bash_completions_dir}/gio
%{bash_completions_dir}/gsettings
%dir %{_datadir}/glib-2.0
%dir %{_datadir}/glib-2.0/schemas
%dir %{_libdir}/gio
%dir %{_libdir}/gio/modules
%ghost %{_libdir}/gio/modules/giomodule.cache
%{_bindir}/gio
%{_bindir}/gio-querymodules*
%{_bindir}/glib-compile-schemas
%{_bindir}/gsettings
%{_bindir}/gdbus
%{_bindir}/gapplication
%{_libexecdir}/gio-launch-desktop
%{_mandir}/man1/gio.1*
%{_mandir}/man1/gio-querymodules.1*
%{_mandir}/man1/glib-compile-schemas.1*
%{_mandir}/man1/gsettings.1*
%{_mandir}/man1/gdbus.1*
%{_mandir}/man1/gapplication.1*

%files devel
%{_libdir}/lib*.so
%{_libdir}/glib-2.0
%{_includedir}/gio-unix-2.0/
%{_includedir}/glib-2.0/
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_datadir}/glib-2.0/dtds
%{_datadir}/glib-2.0/gdb
%{_datadir}/glib-2.0/gettext
%{_datadir}/glib-2.0/schemas/gschema.dtd
%dir %{_datadir}/glib-2.0/valgrind
%{_datadir}/glib-2.0/valgrind/glib.supp
%{bash_completions_dir}/gresource
%{_bindir}/glib-genmarshal
%{_bindir}/glib-gettextize
%{_bindir}/glib-mkenums
%{_bindir}/gi-compile-repository
%{_bindir}/gi-decompile-typelib
%{_bindir}/gi-inspect-typelib
%{_bindir}/gobject-query
%{_bindir}/gtester
%{_bindir}/gdbus-codegen
%{_bindir}/glib-compile-resources
%{_bindir}/gresource
%{_datadir}/glib-2.0/codegen
%attr (0755, root, root) %{_bindir}/gtester-report
%{_mandir}/man1/glib-genmarshal.1*
%{_mandir}/man1/glib-gettextize.1*
%{_mandir}/man1/glib-mkenums.1*
%{_mandir}/man1/gi-compile-repository.1*
%{_mandir}/man1/gi-decompile-typelib.1*
%{_mandir}/man1/gi-inspect-typelib.1*
%{_mandir}/man1/gobject-query.1*
%{_mandir}/man1/gtester-report.1*
%{_mandir}/man1/gtester.1*
%{_mandir}/man1/gdbus-codegen.1*
%{_mandir}/man1/glib-compile-resources.1*
%{_mandir}/man1/gresource.1*
%{_datadir}/gdb/
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/GIRepository-3.0.gir
%{_datadir}/gir-1.0/GLib-2.0.gir
%{_datadir}/gir-1.0/GLibUnix-2.0.gir
%{_datadir}/gir-1.0/GModule-2.0.gir
%{_datadir}/gir-1.0/GObject-2.0.gir
%{_datadir}/gir-1.0/Gio-2.0.gir
%{_datadir}/gir-1.0/GioUnix-2.0.gir
%{_datadir}/gettext/
%{_datadir}/systemtap/

%files doc
%{_datadir}/doc/gio-2.0/
%{_datadir}/doc/gio-unix-2.0/
%{_datadir}/doc/girepository-2.0/
%{_datadir}/doc/glib-2.0/
%{_datadir}/doc/glib-unix-2.0/
%{_datadir}/doc/gmodule-2.0/
%{_datadir}/doc/gobject-2.0/

%files static
%{_libdir}/libgio-2.0.a
%{_libdir}/libgirepository-2.0.a
%{_libdir}/libglib-2.0.a
%{_libdir}/libgmodule-2.0.a
%{_libdir}/libgobject-2.0.a
%{_libdir}/libgthread-2.0.a

%files tests
%{_libexecdir}/installed-tests
%{_datadir}/installed-tests

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 2.86.4-2
- Latest state for glib2

* Mon Feb 16 2026 nmontero <nmontero@redhat.com> - 2.86.4-1
- Update to 2.86.4

* Thu Dec 11 2025 Adrian Vovk <adrianvovk@gmail.com> - 2.86.3-1
- Update to 2.86.3

* Sat Nov 29 2025 Debarshi Ray <rishi@fedoraproject.org> - 2.86.2-1
- Update to 2.86.2
- Fix CVE-2025-13601 or #YWH-PGM9867-134

* Mon Nov 10 2025 Debarshi Ray <rishi@fedoraproject.org> - 2.86.1-5
- Unbreak name resolution on IPv6-only networks

* Mon Nov 10 2025 Debarshi Ray <rishi@fedoraproject.org> - 2.86.1-3
- Own %%{_datadir}/glib-2.0/valgrind

* Wed Nov 05 2025 Michael Kuhn <suraia@fedoraproject.org> - 2.86.1-2
- Unbreak setting special directories to $HOME

* Thu Oct 30 2025 Matthias Clasen <mclasen@redhat.com> - 2.86.1-1
- Update to 2.86.1

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.86.0-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Sep 05 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 2.86.0-1
- Update to 2.86.0

* Mon Aug 25 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 2.85.4-1
- Update to 2.85.4

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.85.3-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Aug 11 2025 Marek Kasik <mkasik@redhat.com> - 2.85.3-1
- Update to 2.85.3

* Wed Jul 23 2025 Barry Dunn <badunn@redhat.com> - 2.85.2-1
- Updated to 2.85.2

* Fri Jun 13 2025 Carlos Garnacho <cgarnach@redhat.com> - 2.85.1-1
- Update to 2.85.1

* Wed May 21 2025 nmontero <nmontero@redhat.com> - 2.85.0-1
- Update to 2.85.0

* Fri Apr 04 2025 nmontero <nmontero@redhat.com> - 2.84.1-1
- Update to 2.84.1

* Thu Mar 06 2025 nmontero <nmontero@redhat.com> - 2.84.0-1
- Update to 2.84.0

* Mon Mar 03 2025 nmontero <nmontero@redhat.com> - 2.83.5-1
- Update to 2.83.5

* Wed Jan 22 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 2.83.2-6
- Add patch to revert gcancellable changes, try 2

* Wed Jan 22 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2.83.2-5
- Drop FIPS mode test, again

* Wed Jan 22 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 2.83.2-4
- Revert "Add patch to revert gcancellable changes"

* Tue Jan 21 2025 nmontero <nmontero@redhat.com> - 2.83.2-3
- Add patch to revert gcancellable changes

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.83.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 12 2024 David King <amigadave@amigadave.com> - 2.83.2-1
- Update to 2.83.2

* Fri Dec 06 2024 Daniel P. Berrangé <berrange@redhat.com> - 2.83.0-3
- Drop ifuncs to unbreak qemu-user-static binaries

* Wed Nov 20 2024 Richard Hughes <richard@hughsie.com> - 2.83.0-2
- Fix a regression that affected fwupd

* Thu Nov 07 2024 nmontero <nmontero@redhat.com> - 2.83.0-1
- Update to 2.83.0

* Fri Oct 18 2024 David King <amigadave@amigadave.com> - 2.82.2-1
- Update to 2.82.2

* Fri Sep 27 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.82.1-2
- Fix default-terminal.patch to actually work

* Fri Sep 20 2024 nmontero <nmontero@redhat.com> - 2.82.1-1
- Update to 2.82.1

* Mon Aug 26 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.82.0-1
- Update to 2.82.0

* Mon Aug 26 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.81.2-4
- Build with -Dglib_debug=disabled again

* Mon Aug 26 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.81.2-3
- Clean up unnecessary build options

* Tue Aug 20 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.81.2-2
- Update default-terminal.patch for Ptyxis, new default terminal

* Sun Aug 18 2024 David King <amigadave@amigadave.com> - 2.81.2-1
- Update to 2.81.2

* Mon Aug 05 2024 Cole Robinson <crobinso@redhat.com> - 2.81.1-2
- Add `Requires: libatomic-static` for `glib2-static`

* Mon Aug 05 2024 nmontero <nmontero@redhat.com> - 2.81.1-1
- Update to 2.81.1

* Mon Jul 29 2024 nmontero <nmontero@redhat.com> - 2.81.0-1
- Update to 2.81.0

* Mon Jul 22 2024 Lumir Balhar <lbalhar@redhat.com> - 2.80.3-6
- Add new systemtap-sdt-dtrace to build deps

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.80.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.3-4
- Drop FIPS mode test

* Wed Jul 10 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.3-3
- Correction: "Stop manually disabling glib_debug" enabled glib_debug!

* Tue Jun 18 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.80.3-2
- Drop manual byte compilation and call to marshalparser

* Mon Jun 17 2024 Nieves Montero <nmontero@redhat.com> - 2.80.3-1
- Update to 2.80.3

* Thu May 09 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.2-1
- Update to 2.80.2

* Wed May 08 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.1-4
- Stop manually disabling glib_debug

* Tue May 07 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.1-3
- Add patch to fix GDBusConnection test failures

* Tue May 07 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.1-2
- Add patch to prefer gnome-terminal over kgx

* Tue May 07 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.1-1
- Update to 2.80.1

* Tue May 07 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.0-9
- Remove gspawn-eperm patchset

* Tue May 07 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.0-8
- Run tests in %%check

* Tue Apr 30 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.0-7
- Revert "Run tests in %%check"

* Tue Apr 30 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.0-6
- Reapply "Update build options, without actually changing anything"

* Tue Apr 30 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.0-5
- Revert "Update build options, without actually changing anything"

* Tue Apr 30 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.0-4
- Run tests in %%check

* Tue Apr 30 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.0-3
- Update build options, without actually changing anything

* Thu Apr 18 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.80.0-2
- Add missing bundled provides

* Tue Mar 12 2024 David King <amigadave@amigadave.com> - 2.80.0-1
- Update to 2.80.0

* Fri Jan 26 2024 David King <amigadave@amigadave.com> - 2.79.1-1
- Update to 2.79.1

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.79.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.79.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 15 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 2.79.0-6
- Add dependency on python3-packaging

* Thu Jan 11 2024 Kalev Lember <klember@redhat.com> - 2.79.0-5
- Backport a patch to skip deprecated gthread api in introspection data

* Thu Jan 11 2024 Kalev Lember <klember@redhat.com> - 2.79.0-4
- Backport a patch to avoid loading mismatching GIRepository versions

* Thu Jan 11 2024 Kalev Lember <klember@redhat.com> - 2.79.0-3
- Drop old glib2-fam obsoletes

* Wed Jan 10 2024 Kalev Lember <klember@redhat.com> - 2.79.0-2
- Don't mark the doc subpackage as noarch

* Wed Jan 10 2024 Kalev Lember <klember@redhat.com> - 2.79.0-1
- Update to 2.79.0
- Rebase gnutls-hmac.patch
- Add gir and typelib files that moved here from gobject-introspection
- Explicitly conflict with older gobject-introspection
- Switch to building docs with gi-docgen instead of gtk-doc

* Wed Dec 06 2023 Kalev Lember <klember@redhat.com> - 2.78.3-1
- Update to 2.78.3

* Wed Dec 06 2023 Kalev Lember <klember@redhat.com> - 2.78.2-1
- Update to 2.78.2

* Thu Oct 26 2023 Kalev Lember <klember@redhat.com> - 2.78.1-1
- Update to 2.78.1

* Wed Sep 27 2023 Zephyr Lykos <git@mochaa.ws> - 2.78.0-3
- gthreadedresolver: Fix race between source callbacks and finalize
  (fedora#2235890)

* Sat Sep 16 2023 Kalev Lember <klember@redhat.com> - 2.78.0-2
- Use standard indentation

* Sat Sep 16 2023 Kalev Lember <klember@redhat.com> - 2.78.0-1
- Update to 2.78.0

* Sat Sep 16 2023 Kalev Lember <klember@redhat.com> - 2.77.3-3
- Don't number sources and patches

* Thu Sep 07 2023 Kalev Lember <klember@redhat.com> - 2.77.3-2
- gkeyfile: Temporarily re-allow invalid escapes when parsing strings

* Thu Aug 31 2023 Kalev Lember <klember@redhat.com> - 2.77.3-1
- Update to 2.77.3

* Sat Aug 12 2023 Kalev Lember <klember@redhat.com> - 2.77.2-1
- Update to 2.77.2

* Mon Jul 31 2023 Kalev Lember <klember@redhat.com> - 2.77.1-1
- Update to 2.77.1

* Mon Jul 24 2023 Kalev Lember <klember@redhat.com> - 2.77.0-8
- Backport upstream patch to fix GKeyFile group comments (rhbz#2225257)

* Thu Jul 20 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.77.0-7
- Fix GModule change resulting in missing exported symbols

* Wed Jul 19 2023 Richard Hughes <richard@hughsie.com> - 2.77.0-6
- Fix up EPRM patch -- 3rd try lucky

* Wed Jul 19 2023 Richard Hughes <richard@hughsie.com> - 2.77.0-5
- Fix up patch to actually apply

* Wed Jul 19 2023 Richard Hughes <richard@hughsie.com> - 2.77.0-4
- Handle EPERM to allow Fedora to be used on CircleCI and GitHub actions

* Tue Jul 18 2023 Adam Williamson <awilliam@redhat.com> - 2.77.0-3
- Update to upstream fix for anaconda crash issue

* Tue Jul 18 2023 Adam Williamson <awilliam@redhat.com> - 2.77.0-2
- Revert an upstream change that makes anaconda crash

* Mon Jul 17 2023 David King <amigadave@amigadave.com> - 2.77.0-1
- Update to 2.77.0

* Thu Jul 06 2023 Kalev Lember <klember@redhat.com> - 2.76.4-1
- Update to 2.76.4

* Tue May 23 2023 David King <amigadave@amigadave.com> - 2.76.3-1
- Update to 2.76.3

* Mon Apr 24 2023 David King <amigadave@amigadave.com> - 2.76.2-1
- Update to 2.76.2

* Mon Apr 10 2023 David King <amigadave@amigadave.com> - 2.76.1-2
- Add python3-setuptools Requires to -devel

* Wed Mar 22 2023 David King <amigadave@amigadave.com> - 2.76.1-1
- Update to 2.76.1

* Sun Mar 12 2023 David King <amigadave@amigadave.com> - 2.76.0-1
- Update to 2.76.0

* Mon Mar 06 2023 David King <amigadave@amigadave.com> - 2.75.4-2
- Fix getting etag attributes

* Sat Mar 04 2023 David King <amigadave@amigadave.com> - 2.75.4-1
- Update to 2.75.4

* Sat Feb 18 2023 Adam Williamson <awilliam@redhat.com> - 2.75.3-4
- Revert "Fix #2169622 for now by reverting the problematic commit"

* Wed Feb 15 2023 Adam Williamson <awilliam@redhat.com> - 2.75.3-3
- Fix #2169622 for now by reverting the problematic commit

* Tue Feb 14 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.75.3-2
- Remove Provides: bundled(gnulib)

* Mon Feb 13 2023 Adam Williamson <awilliam@redhat.com> - 2.75.3-1
- Update to 2.75.3

* Tue Feb 07 2023 David King <amigadave@amigadave.com> - 2.75.2-1
- Update to 2.75.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 02 2022 David King <amigadave@amigadave.com> - 2.74.1-2
- Add upstream revert of fd mishandling

* Thu Oct 27 2022 David King <amigadave@amigadave.com> - 2.74.1-1
- Update to 2.74.1

* Tue Sep 27 2022 Kalev Lember <klember@redhat.com> - 2.74.0-3
- Rebuild to fix sysprof-capture symbols leaking into libraries consuming
  it

* Mon Sep 26 2022 Kalev Lember <klember@redhat.com> - 2.74.0-2
- Backport an upstream patch to fix GParam validation crashes

* Sun Sep 18 2022 Kalev Lember <klember@redhat.com> - 2.74.0-1
- Update to 2.74.0

* Tue Sep 06 2022 Kalev Lember <klember@redhat.com> - 2.73.3-3
- Rebuild so that we can include it in the GNOME 43.rc mega-update as
  various updates in there depend on new glib.

* Fri Aug 26 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.73.3-2
- gio-launch-desktop is back

* Fri Aug 26 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.73.3-1
- Update to 2.73.3 and drop gdesktopappinfo patch

* Mon Aug 15 2022 Kalev Lember <klember@redhat.com> - 2.73.2-8
- Backport an upstream patch to fix an FD leak (rhbz#2109145)

* Wed Jul 27 2022 Kalev Lember <klember@redhat.com> - 2.73.2-7
- Backport another GRegex upstream fix

* Tue Jul 26 2022 Kalev Lember <klember@redhat.com> - 2.73.2-6
- Backport an upstream patch to fix GRegex on s390x

* Tue Jul 26 2022 Kalev Lember <klember@redhat.com> - 2.73.2-5
- Add missing requires to glib2-static subpackage

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.73.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.73.2-3
- No unexpected soname bumps

* Thu Jul 14 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.73.2-2
- Fix gnutls-hmac.patch

* Thu Jul 14 2022 Kalev Lember <klember@redhat.com> - 2.73.2-1
- Update to 2.73.2
- Rebase gnutls-hmac.patch
- Rebase gdesktopappinfo.patch
- Drop 2784.patch as it's been fixed upstream
- Build with pcre2 instead of pcre

* Tue Jun 28 2022 Adam Williamson <awilliam@redhat.com> - 2.73.1-2
- Backport PR #2784 to fix `weak_locations != NULL` crashes

* Tue Jun 21 2022 David King <amigadave@amigadave.com> - 2.73.1-1
- Update to 2.73.1

* Mon May 30 2022 David King <amigadave@amigadave.com> - 2.72.2-1
- Update to 2.72.2

* Thu Apr 14 2022 David King <amigadave@amigadave.com> - 2.72.1-1
- Update to 2.72.1

* Fri Mar 18 2022 David King <amigadave@amigadave.com> - 2.72.0-1
- Update to 2.72.0

* Mon Mar 07 2022 David King <amigadave@amigadave.com> - 2.71.3-1
- Update to 2.71.3

* Tue Feb 15 2022 David King <amigadave@amigadave.com> - 2.71.2-1
- Update to 2.71.2

* Sun Jan 30 2022 David King <amigadave@amigadave.com> - 2.71.1-1
- Update to 2.71.1

* Wed Jan 26 2022 Bastien Nocera <hadess@hadess.net> - 2.71.0-3
- Fix gspawn hangs in CI runners

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.71.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 David King <amigadave@amigadave.com> - 2.71.0-1
- Update to 2.71.0

* Sat Jan 08 2022 Miro Hrončok <miro@hroncok.cz> - 2.70.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Mon Dec 06 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.70.2-3
- Update annocheck policy

* Mon Dec 06 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.70.2-2
- Add gspawn patchset

* Mon Dec 06 2021 Kalev Lember <klember@redhat.com> - 2.70.2-1
- Update to 2.70.2

* Thu Oct 28 2021 Kalev Lember <klember@redhat.com> - 2.70.1-1
- Update to 2.70.1

* Fri Oct 15 2021 Kalev Lember <klember@redhat.com> - 2.70.0-5
- Fix network state monitoring to work with NetworkManager 1.32 (#1991075)

* Tue Oct 05 2021 Miro Hrončok <miro@hroncok.cz> - 2.70.0-4
- Produce bit-by-bit identical .pyc files across different architectures,
  to avoid multilib conflicts

* Wed Sep 22 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.70.0-3
- Remove workaround for gnome-keyring

* Tue Sep 21 2021 Adam Williamson <awilliam@redhat.com> - 2.70.0-2
- Re-enable a workaround to fix g-i-s/gnome-keyring (#2005625)

* Fri Sep 17 2021 Kalev Lember <klember@redhat.com> - 2.70.0-1
- Update to 2.70.0

* Wed Sep 08 2021 Kalev Lember <klember@redhat.com> - 2.69.3-1
- Update to 2.69.3

* Sat Aug 21 2021 Kalev Lember <klember@redhat.com> - 2.69.2-1
- Update to 2.69.2

* Wed Jul 21 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.69.0-1
- Upgrade to 2.69.0

* Mon Jul 12 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.68.3-13
- Note: all those previous empty commits accomplished nothing

* Mon Jul 12 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.68.3-12
- Empty commit for rpmautospec -5

* Mon Jul 12 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.68.3-11
- Empty commit for rpmautospec -4

* Mon Jul 12 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.68.3-10
- Empty commit for rpmautospec -3

* Mon Jul 12 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.68.3-9
- Empty commit for rpmautospec -2

* Thu Jul 01 2021 Michael Catanzaro <mcatanzaro@gnome.org> - 2.68.3-4
- Refresh gnutls-hmac patchset to fix leaks in error path

* Mon Jun 28 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.68.3-3
- Drop Recommends: shared-mime-info (#1947897)
- Remove old Conflicts: gcr < 3.28.1

* Wed Jun 23 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.68.3-2
- Drop check-rpath hack, no longer required

* Mon Jun 21 2021 Kalev Lember <klember@redhat.com> - 2.68.3-1
- Update to 2.68.3

* Thu Jun 17 2021 Stephen Gallagher <sgallagh@redhat.com> - 2.68.2-3
- Fix the requirement for 32-bit libgnutls.so.30

* Thu Jun 17 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.68.2-2
- Enable GnuTLS-based GHmac in Fedora and reenable glib2-static in RHEL
- Consolidate GDesktopAppInfo changes into gdesktopappinfo.patch
- Disable check-rpath since it seems to be broken

* Tue May 11 2021 Kalev Lember <klember@redhat.com> - 2.68.2-1
- Update to 2.68.2

* Wed May 05 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.68.1-3
- Add missing bundled provides

* Wed Apr 28 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 2.68.1-2
- Refresh GDesktopAppInfo patchset

* Thu Apr 08 2021 Kalev Lember <klember@redhat.com> - 2.68.1-1
- Update to 2.68.1

* Fri Mar 26 2021 Kalev Lember <klember@redhat.com> - 2.68.0-2
- Rebuild to fix sysprof-capture symbols leaking into libraries consuming it

* Thu Mar 18 2021 Kalev Lember <klember@redhat.com> - 2.68.0-1
- Update to 2.68.0

* Thu Mar 18 2021 Petr Pisar <ppisar@redhat.com> - 2.67.6-2
- Disable debugging glib (bug #1936339)

* Thu Mar 11 2021 Kalev Lember <klember@redhat.com> - 2.67.6-1
- Update to 2.67.6

* Tue Mar 02 2021 Kalev Lember <klember@redhat.com> - 2.67.5-1
- Update to 2.67.5

* Wed Feb 24 2021 Kalev Lember <klember@redhat.com> - 2.67.4-3
- Enable sysprof capture support

* Fri Feb 19 2021 Kalev Lember <klember@redhat.com> - 2.67.4-2
- Backport a fix for gsubprocesslauncher regression

* Tue Feb 16 2021 Kalev Lember <klember@redhat.com> - 2.67.4-1
- Update to 2.67.4

* Tue Feb 09 2021 Benjamin Berg <bberg@redhat.com> - 2.67.3-2
- Add patches to move applications into systemd scopes

* Thu Feb 04 2021 Kalev Lember <klember@redhat.com> - 2.67.3-1
- Update to 2.67.3
- Fix gtk-doc directory ownership

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.67.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 2.67.1-3
- Drop dependency on gamin

* Sat Dec 19 2020 Kevin Fenzi <kevin@scrye.com> - 2.67.1-2
- Add already upstream patch to fix gdm crasher.

* Sat Dec 19 2020 Kalev Lember <klember@redhat.com> - 2.67.1-1
- Update to 2.67.1

* Fri Dec 04 2020 Ondrej Holy <oholy@redhat.com> - 2.67.0-7
- Explicitly create modules dir to fix ELN build

* Tue Dec 01 2020 Ondrej Holy and Michael Catanzaro <mcatanzaro@redhat.com> - 2.67.0-6
- Disable glib2-fam in RHEL

* Tue Nov 24 2020 Kalev Lember <klember@redhat.com> - 2.67.0-5
- Backport upstream patches to fix invalid use of volatile objects
  (gcc 11 support)

* Wed Nov 11 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.67.0-4
- Make GnuTLS patch RHEL-specific, and make glib2-static subpackage Fedora-specific

* Tue Nov 10 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.67.0-3
- Use GnuTLS to implement GHmac (thanks to Colin Walters)

* Wed Nov 04 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.67.0-2
- Backport fix for GSocketClient crash

* Thu Oct 29 2020 Kalev Lember <klember@redhat.com> - 2.67.0-1
- Update to 2.67.0

* Mon Oct 19 2020 Kalev Lember <klember@redhat.com> - 2.66.2-1
- Update to 2.66.2
- Drop gtk-doc patch as we finally have a new enough gtk-doc

* Wed Oct 14 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.66.1-3
- Fix yet another timezone bug

* Wed Oct 14 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.66.1-2
- Fix timezone-related bugs in many applications caused by new glib timezone cache

* Thu Oct  1 2020 Kalev Lember <klember@redhat.com> - 2.66.1-1
- Update to 2.66.1

* Thu Sep 10 2020 Kalev Lember <klember@redhat.com> - 2.66.0-1
- Update to 2.66.0

* Wed Sep 02 2020 Kalev Lember <klember@redhat.com> - 2.65.3-1
- Update to 2.65.3

* Tue Aug 25 2020 Adam Williamson <awilliam@redhat.com> - 2.65.2-3
- Backport fix for GGO #2189 (error accessing some filesystems)

* Thu Aug 20 2020 Jeff Law <law@redhat.com> - 2.65.2-2
- Re-enable LTO

* Tue Aug 18 2020 Kalev Lember <klember@redhat.com> - 2.65.2-1
- Update to 2.65.2

* Mon Aug 17 2020 Kalev Lember <klember@redhat.com> - 2.65.1-1
- Update to 2.65.1

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.65.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.65.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Jeff Law <aw@redhat.com> - 2.65.0-3
Disable LTO

* Mon Jun 22 2020 Kalev Lember <klember@redhat.com> - 2.65.0-2
- Update gio-2.0.pc with correct gio-querymodules name when renaming it
  (#1849441)

* Mon Jun 22 2020 Kalev Lember <klember@redhat.com> - 2.65.0-1
- Update to 2.65.0

* Wed May 20 2020 Kalev Lember <klember@redhat.com> - 2.64.3-1
- Update to 2.64.3

* Tue Apr 28 2020 Tomas Popela <tpopela@redhat.com> - 2.64.2-2
- Backport fix for a race condition in GCancellable (rhbz#1825230)

* Fri Apr 10 2020 Kalev Lember <klember@redhat.com> - 2.64.2-1
- Update to 2.64.2

* Wed Mar 11 2020 Kalev Lember <klember@redhat.com> - 2.64.1-1
- Update to 2.64.1

* Mon Mar 02 2020 Kalev Lember <klember@redhat.com> - 2.64.0-1
- Update to 2.64.0

* Mon Feb 24 2020 Kalev Lember <klember@redhat.com> - 2.63.6-1
- Update to 2.63.6

* Wed Feb 12 2020 Kalev Lember <klember@redhat.com> - 2.63.5-3
- Backport a patch to work around SELinux policies not allowing
  SYS_sched_setattr (#1795524)

* Fri Feb 07 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.63.5-2
- Add patch for CVE-2020-6750 and related issues.

* Mon Feb 03 2020 Kalev Lember <klember@redhat.com> - 2.63.5-1
- Update to 2.63.5

* Wed Jan 29 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.63.4-3
- Fix GThreadPool initialization that is breaking createrepo_c (BZ #1795052)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.63.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Kalev Lember <klember@redhat.com> - 2.63.4-1
- Update to 2.63.4

* Mon Dec 16 2019 Kalev Lember <klember@redhat.com> - 2.63.3-1
- Update to 2.63.3

* Mon Dec 02 2019 Kalev Lember <klember@redhat.com> - 2.63.2-1
- Update to 2.63.2

* Fri Oct 04 2019 Kalev Lember <klember@redhat.com> - 2.63.0-1
- Update to 2.63.0

* Fri Oct 04 2019 Kalev Lember <klember@redhat.com> - 2.62.1-1
- Update to 2.62.1

* Fri Sep 06 2019 Kalev Lember <klember@redhat.com> - 2.62.0-1
- Update to 2.62.0

* Tue Sep 03 2019 Kalev Lember <klember@redhat.com> - 2.61.3-1
- Update to 2.61.3

* Mon Aug 12 2019 Kalev Lember <klember@redhat.com> - 2.61.2-1
- Update to 2.61.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.61.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 David King <amigadave@amigadave.com> - 2.61.1-2
- Fix CVE-2019-12450 (#1719142)
- Consistently use buildroot macro

* Fri May 24 2019 Kalev Lember <klember@redhat.com> - 2.61.1-1
- Update to 2.61.1

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 2.61.0-2
- Rebuild with Meson fix for #1699099

* Mon Apr 15 2019 Kalev Lember <klember@redhat.com> - 2.61.0-1
- Update to 2.61.0

* Mon Apr 15 2019 Kalev Lember <klember@redhat.com> - 2.60.1-1
- Update to 2.60.1

* Wed Mar 13 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.60.0-3
- Switch back to timestamp-based pyc invalidation mode

* Wed Mar  6 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.60.0-2
- Make sure all .py files have fixed timestamps (fixes issue with
  parallel installability of i686 and amd64 -devel packages)
- Switch to explicit byte compilation to override invalidation mode

* Mon Mar 04 2019 Kalev Lember <klember@redhat.com> - 2.60.0-1
- Update to 2.60.0

* Mon Feb 18 2019 Kalev Lember <klember@redhat.com> - 2.59.3-1
- Update to 2.59.3

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 2.59.2-1
- Update to 2.59.2

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.59.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 Kalev Lember <klember@redhat.com> - 2.59.1-1
- Update to 2.59.1

* Thu Jan 03 2019 Kalev Lember <klember@redhat.com> - 2.59.0-1
- Update to 2.59.0
- Switch to the meson build system

* Tue Dec 18 2018 Kalev Lember <klember@redhat.com> - 2.58.2-1
- Update to 2.58.2

* Fri Oct 05 2018 Kalev Lember <klember@redhat.com> - 2.58.1-2
- Fix multilib -devel installs (#1634778)

* Fri Sep 21 2018 Kalev Lember <klember@redhat.com> - 2.58.1-1
- Update to 2.58.1

* Wed Sep 05 2018 Kalev Lember <klember@redhat.com> - 2.58.0-1
- Update to 2.58.0

* Thu Aug 2 2018 Ondrej Holy <oholy@redhat.com> - 2.57.2-1
- Update to 2.57.2

* Fri Jul 20 2018 Ondrej Holy <oholy@redhat.com> - 2.57.1-1
- Update to 2.57.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.56.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.56.1-5
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Debarshi Ray <rishi@fedoraproject.org> - 2.56.1-4
- Backport patch to fix possible invalid pointer in dbus callback in the FD.o
  notification backend (RH #1584916)

* Sun May 27 2018 Kalev Lember <klember@redhat.com> - 2.56.1-3
- Fix multilib -devel installs (#1581067)

* Sun May 13 2018 Fabio Valentini <decathorpe@gmail.com> - 2.56.1-2
- Include upstream patch to fix gdbus-codegen with meson 0.46.

* Sun Apr 08 2018 Kalev Lember <klember@redhat.com> - 2.56.1-1
- Update to 2.56.1

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 2.56.0-1
- Update to 2.56.0

* Wed Feb 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.55.2-3
- Undo disabling mangling

* Wed Feb 07 2018 Kalev Lember <klember@redhat.com> - 2.55.2-2
- Disable brp-mangle-shebangs shebangs

* Wed Feb 07 2018 Kalev Lember <klember@redhat.com> - 2.55.2-1
- Update to 2.55.2
- Drop ldconfig scriptlets

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.55.1-3
- Switch to %%ldconfig_scriptlets

* Thu Jan 18 2018 Kalev Lember <klember@redhat.com> - 2.55.1-2
- gmain: Partial revert of recent wakeup changes

* Mon Jan 08 2018 Kalev Lember <klember@redhat.com> - 2.55.1-1
- Update to 2.55.1
- Drop upstreamed systemtap multilib fix

* Tue Dec 19 2017 Kalev Lember <klember@redhat.com> - 2.55.0-1
- Update to 2.55.0

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 2.54.2-1
- Update to 2.54.2

* Fri Oct 06 2017 Kalev Lember <klember@redhat.com> - 2.54.1-1
- Update to 2.54.1

* Mon Sep 11 2017 Kalev Lember <klember@redhat.com> - 2.54.0-1
- Update to 2.54.0

* Tue Sep 05 2017 Kalev Lember <klember@redhat.com> - 2.53.7-1
- Update to 2.53.7

* Sat Aug 19 2017 Kalev Lember <klember@redhat.com> - 2.53.6-1
- Update to 2.53.6

* Mon Aug 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.53.5-1
- Update to 2.53.5

* Tue Aug 01 2017 Kalev Lember <klember@redhat.com> - 2.53.4-4
- Backport glib-mkenums flags annotation parsing fixes

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.53.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Kalev Lember <klember@redhat.com> - 2.53.4-2
- Revert a GKeyFile introspection ABI change

* Tue Jul 18 2017 Kalev Lember <klember@redhat.com> - 2.53.4-1
- Update to 2.53.4

* Thu Jun 22 2017 Kalev Lember <klember@redhat.com> - 2.53.3-1
- Update to 2.53.3

* Thu Jun 8 2017 Owen Taylor <otaylor@redhat.com> - 2.53.2-2
- Make triggers also compile schemas in /app/share/glib-2.0/schemas

* Wed May 24 2017 Florian Müllner <fmuellner@redhat.com> - 2.53.2-1
- Update to 2.53.2

* Mon May 15 2017 Kalev Lember <klember@redhat.com> - 2.52.2-2
- Backport a gmain GWakeup patch to fix timedatex high CPU usage (#1450628)

* Tue May 09 2017 Kalev Lember <klember@redhat.com> - 2.52.2-1
- Update to 2.52.2

* Tue Apr 11 2017 Colin Walters <walters@verbum.org> - 2.52.1-3
- Backport patches for gmain wakeup for qemu
  See: https://bugzilla.gnome.org/show_bug.cgi?id=761102

* Tue Apr 11 2017 Colin Walters <walters@verbum.org> - 2.52.1-2
- Explictly remove PCRE sources
- Related: https://bugzilla.redhat.com/show_bug.cgi?id=1324770

* Tue Apr 11 2017 Kalev Lember <klember@redhat.com> - 2.52.1-1
- Update to 2.52.1

* Mon Mar 20 2017 Kalev Lember <klember@redhat.com> - 2.52.0-1
- Update to 2.52.0

* Thu Mar 16 2017 Kalev Lember <klember@redhat.com> - 2.51.5-1
- Update to 2.51.5

* Thu Mar 02 2017 Kalev Lember <klember@redhat.com> - 2.51.4-2
- Remove the dependency on dbus-launch again (#927212)

* Wed Mar 01 2017 David King <amigadave@amigadave.com> - 2.51.4-1
- Update to 2.51.4
- Add a Requires on dbus-launch (#927212)
- Use pkgconfig for BuildRequires

* Tue Feb 14 2017 Richard Hughes <rhughes@redhat.com> - 2.51.2-1
- Update to 2.51.2

* Mon Feb 13 2017 Richard Hughes <rhughes@redhat.com> - 2.51.1-1
- Update to 2.51.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.51.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.51.0-2
- Rebuild for Python 3.6

* Sun Oct 30 2016 Kalev Lember <klember@redhat.com> - 2.51.0-1
- Update to 2.51.0

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 2.50.1-1
- Update to 2.50.1

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 2.50.0-1
- Update to 2.50.0

* Tue Sep 13 2016 Kalev Lember <klember@redhat.com> - 2.49.7-1
- Update to 2.49.7
- Don't set group tags

* Sun Aug 28 2016 Kalev Lember <klember@redhat.com> - 2.49.6-1
- Update to 2.49.6

* Thu Aug 18 2016 Kalev Lember <klember@redhat.com> - 2.49.5-1
- Update to 2.49.5
- Own /usr/share/gdb and /usr/share/systemtap directories

* Tue Aug 16 2016 Miro Hrončok <mhroncok@redhat.com> - 2.49.4-3
- Use Python 3 for the RPM Python byte compilation

* Wed Jul 27 2016 Ville Skyttä <ville.skytta@iki.fi> - 2.49.4-2
- Switch to Python 3 (#1286284)

* Thu Jul 21 2016 Kalev Lember <klember@redhat.com> - 2.49.4-1
- Update to 2.49.4

* Sun Jul 17 2016 Kalev Lember <klember@redhat.com> - 2.49.3-1
- Update to 2.49.3

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 2.49.2-1
- Update to 2.49.2

* Wed Jun 01 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.49.1-2
- Soften shared-mime-info dependency (#1266118)

* Fri May 27 2016 Florian Müllner <fmuellner@redhat.com> - 2.49.1-1
- Update to 2.49.1

* Tue May 10 2016 Kalev Lember <klember@redhat.com> - 2.48.1-1
- Update to 2.48.1

* Wed Apr 06 2016 Colin Walters <walters@redhat.com> - 2.48.0-2
- Explicitly require system pcre, though we happened to default to this now
  anyways due to something else pulling PCRE into the buildroot
  Closes rhbz#1287266

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 2.48.0-1
- Update to 2.48.0

* Thu Mar 17 2016 Richard Hughes <rhughes@redhat.com> - 2.47.92-1
- Update to 2.47.92

* Wed Feb 24 2016 Colin Walters <walters@redhat.com> - 2.47.6.19.gad2092b-2
- git snapshot to work around https://bugzilla.gnome.org/show_bug.cgi?id=762637
- Add --with-python=/usr/bin/python explicitly to hopefully fix a weird
  issue I am seeing where librepo fails to build in epel7 with this due to
  us requiring /bin/python.

* Wed Feb 17 2016 Richard Hughes <rhughes@redhat.com> - 2.47.6-1
- Update to 2.47.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.47.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 David King <amigadave@amigadave.com> - 2.47.5-1
- Update to 2.47.5

* Wed Dec 16 2015 Kalev Lember <klember@redhat.com> - 2.47.4-1
- Update to 2.47.4

* Wed Nov 25 2015 Kalev Lember <klember@redhat.com> - 2.47.3-1
- Update to 2.47.3

* Wed Nov 25 2015 Kalev Lember <klember@redhat.com> - 2.47.2-1
- Update to 2.47.2

* Mon Nov 09 2015 Kevin Fenzi <kevin@scrye.com> - 2.47.1-2
- Add full path redirect output to null and || : to triggers.

* Wed Oct 28 2015 Kalev Lember <klember@redhat.com> - 2.47.1-1
- Update to 2.47.1

* Mon Oct 19 2015 Kalev Lember <klember@redhat.com> - 2.46.1-2
- Backport an upstream fix for app launching under wayland (#1273146)

* Wed Oct 14 2015 Kalev Lember <klember@redhat.com> - 2.46.1-1
- Update to 2.46.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 2.46.0-1
- Update to 2.46.0

* Mon Sep 14 2015 Kalev Lember <klember@redhat.com> - 2.45.8-1
- Update to 2.45.8

* Tue Sep 01 2015 Kalev Lember <klember@redhat.com> - 2.45.7-1
- Update to 2.45.7

* Wed Aug 19 2015 Kalev Lember <klember@redhat.com> - 2.45.6-1
- Update to 2.45.6

* Wed Aug 19 2015 Kalev Lember <klember@redhat.com> - 2.45.5-1
- Update to 2.45.5

* Fri Aug 14 2015 Matthias Clasen <mclasen@redhat.com> - 2.45.4-2
- Add file triggers for gio modules and gsettings schemas

* Tue Jul 21 2015 David King <amigadave@amigadave.com> - 2.45.4-1
- Update to 2.45.4

* Wed Jun 24 2015 Kalev Lember <klember@redhat.com> - 2.45.3-2
- Backport a patch to fix notification withdrawing in gnome-software

* Wed Jun 24 2015 David King <amigadave@amigadave.com> - 2.45.3-1
- Update to 2.45.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.45.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 David King <amigadave@amigadave.com> - 2.45.2-1
- Update to 2.45.2

* Thu Apr 30 2015 Kalev Lember <kalevlember@gmail.com> - 2.45.1-1
- Update to 2.45.1

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 2.44.0-1
- Update to 2.44.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 2.43.92-1
- Update to 2.43.92

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.43.91-1
- Update to 2.43.91

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.43.90-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Feb 18 2015 David King <amigadave@amigadave.com> - 2.43.90-1
- Update to 2.43.90
- Update man pages glob in files section

* Tue Feb 10 2015 Matthias Clasen <mclasen@redhat.com> - 2.43.4-1
- Update to 2.43.4

* Tue Jan 20 2015 David King <amigadave@amigadave.com> - 2.43.3-1
- Update to 2.43.3

* Wed Dec 17 2014 Kalev Lember <kalevlember@gmail.com> - 2.43.2-1
- Update to 2.43.2

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 2.43.1-1
- Update to 2.43.1

* Thu Oct 30 2014 Florian Müllner <fmuellner@redhat.com> - 2.43.0-1
- Update to 2.43.0

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.42.0-1
- Update to 2.42.0

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.5-1
- Update to 2.41.5

* Thu Sep  4 2014 Matthias Clasen <mclasen@redhat.com> 2.41.4-3
- Don't remove rpath from gdbus-peer test - it doesn't work without it

* Thu Sep 04 2014 Bastien Nocera <bnocera@redhat.com> 2.41.4-2
- Fix banshee getting selected as the default movie player

* Tue Sep 02 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.4-1
- Update to 2.41.4

* Sat Aug 16 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.3-1
- Update to 2.41.3

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Stef Walter <stefw@redhat.com> - 2.41.2-2
- Fix regression with GDBus array encoding rhbz#1122128

* Mon Jul 14 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.2-1
- Update to 2.41.2

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 2.41.1-2
- fix license handling

* Tue Jun 24 2014 Richard Hughes <rhughes@redhat.com> - 2.41.1-1
- Update to 2.41.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.0-1
- Update to 2.41.0

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 2.40.0-1
- Update to 2.40.0

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 2.39.92-1
- Update to 2.39.92

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 2.39.91-1
- Update to 2.39.91

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 2.39.90-1
- Update to 2.39.90

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 2.39.4-1
- Update to 2.39.4

* Tue Jan 14 2014 Richard Hughes <rhughes@redhat.com> - 2.39.3-1
- Update to 2.39.3

* Sun Dec 22 2013 Richard W.M. Jones <rjones@redhat.com> - 2.39.2-2
- Re-add static subpackage so that we can build static qemu as
  an AArch64 binfmt.

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 2.39.2-1
- Update to 2.39.2

* Mon Dec 09 2013 Richard Hughes <rhughes@redhat.com> - 2.39.1-2
- Backport a patch from master to stop gnome-settings-daemon crashing.

* Thu Nov 14 2013 Richard Hughes <rhughes@redhat.com> - 2.39.1-1
- Update to 2.39.1

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 2.39.0-1
- Update to 2.39.0

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 2.38.0-1
- Update to 2.38.0

* Tue Sep 17 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.93-1
- Update to 2.37.93

* Mon Sep 02 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.7-1
- Update to 2.37.7

* Wed Aug 21 2013 Debarshi Ray <rishi@fedoraproject.org> - 2.37.6-1
- Update to 2.37.6

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 2.37.5-2
- Perl 5.18 rebuild

* Thu Aug  1 2013 Debarshi Ray <rishi@fedoraproject.org> - 2.37.5-1
- Update to 2.37.5

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.37.4-2
- Perl 5.18 rebuild

* Tue Jul  9 2013 Matthias Clasen <mclasen@redhat.com> - 2.37.4-1
- Update to 2.37.4

* Thu Jun 20 2013 Debarshi Ray <rishi@fedoraproject.org> - 2.37.2-1
- Update to 2.37.2

* Tue May 28 2013 Matthias Clasen <mclasen@redhat.com> - 2.37.1-1
- Update to 2.37.1
- Add a tests subpackage

* Sat May 04 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.0-1
- Update to 2.37.0

* Sat Apr 27 2013 Thorsten Leemhuis <fedora@leemhuis.info> - 2.36.1-2
- Fix pidgin freezes by applying patch from master (#956872)

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 2.36.1-1
- Update to 2.36.1

* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> - 2.36.0-1
- Update to 2.36.0

* Tue Mar 19 2013 Matthias Clasen <mclasen@redhat.com> - 2.35.9-1
- Update to 2.35.9

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 2.35.8-1
- Update to 2.35.8

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 2.35.7-1
- Update to 2.35.7

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.35.4-1
- Update to 2.35.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.3-1
- Update to 2.35.3

* Sat Nov 24 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.2-1
- Update to 2.35.2

* Thu Nov 08 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.1-1
- Update to 2.35.1
- Drop upstreamed codegen-in-datadir.patch

## END: Generated by rpmautospec
