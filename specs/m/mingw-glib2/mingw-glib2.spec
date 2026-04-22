# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-glib2
Version:        2.86.3
Release: 4%{?dist}
Summary:        MinGW Windows GLib2 library

License:        LGPL-2.0-or-later
URL:            http://www.gtk.org
# first two digits of version
%global release_version %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.gnome.org/sources/glib/%{release_version}/glib-%{version}.tar.xz

# Backport fix for CVE-2026-0988
Patch0:         https://gitlab.gnome.org/GNOME/glib/-/commit/c5766cff61ffce0b8e787eae09908ac348338e5f.patch
# https://gitlab.gnome.org/GNOME/glib/-/merge_requests/4978
Patch1:         CVE-2026-1484.patch
# https://gitlab.gnome.org/GNOME/glib/-/merge_requests/4980
Patch2:         CVE-2026-1485.patch
# https://gitlab.gnome.org/GNOME/glib/-/merge_requests/4983
Patch3:         CVE-2026-1489.patch

BuildArch:      noarch

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  gcc-c++

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-win-iconv
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-libffi
BuildRequires:  mingw32-pcre2
BuildRequires:  mingw32-zlib

BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-win-iconv
BuildRequires:  mingw64-gettext
BuildRequires:  mingw64-libffi
BuildRequires:  mingw64-pcre2
BuildRequires:  mingw64-zlib

# Native version required for msgfmt use in build
BuildRequires:  gettext
# Native version required for glib-genmarshal
BuildRequires:  glib2-devel >= 2.45.3
BuildRequires:  python3-devel

# Prefer the use of GCC constructors over DllMain
# This prevents having to depend on DllMain in static libraries
# http://lists.fedoraproject.org/pipermail/mingw/2013-March/006429.html
# http://lists.fedoraproject.org/pipermail/mingw/2013-March/006469.html
# https://bugzilla.gnome.org/show_bug.cgi?id=698118
#Patch5:         glib-prefer-constructors-over-DllMain.patch

%description
MinGW Windows Glib2 library.

# Win32
%package -n mingw32-glib2
Summary:        MinGW Windows Glib2 library for the win32 target
# glib-genmarshal and glib-mkenums are written in Python
Requires:       python3

%description -n mingw32-glib2
MinGW Windows Glib2 library.

%package -n mingw32-glib2-static
Summary:        Static version of the MinGW Windows GLib2 library
Requires:       mingw32-glib2 = %{version}-%{release}
Requires:       mingw32-gettext-static

%description -n mingw32-glib2-static
Static version of the MinGW Windows GLib2 library.

# Win64
%package -n mingw64-glib2
Summary:        MinGW Windows Glib2 library for the win64 target
# glib-genmarshal and glib-mkenums are written in Python
Requires:       python3

%description -n mingw64-glib2
MinGW Windows Glib2 library.

%package -n mingw64-glib2-static
Summary:        Static version of the MinGW Windows GLib2 library
Requires:       mingw64-glib2 = %{version}-%{release}
Requires:       mingw64-gettext-static

%description -n mingw64-glib2-static
Static version of the MinGW Windows GLib2 library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n glib-%{version}

%build
export MINGW_BUILDDIR_SUFFIX=static
%mingw_meson --default-library=static
%mingw_ninja
export MINGW_BUILDDIR_SUFFIX=shared
%mingw_meson --default-library=shared
%mingw_ninja

%install
export MINGW_BUILDDIR_SUFFIX=static
%mingw_ninja_install
export MINGW_BUILDDIR_SUFFIX=shared
%mingw_ninja_install

# There's a small difference in the file glibconfig.h between the
# shared and the static build:
#
#diff -ur shared/usr/i686-pc-mingw32/sys-root/mingw/lib/glib-2.0/include/glibconfig.h static/usr/i686-pc-mingw32/sys-root/mingw/lib/glib-2.0/include/glibconfig.h
#--- shared/usr/i686-pc-mingw32/sys-root/mingw/lib/glib-2.0/include/glibconfig.h	2009-02-20 17:34:35.735677022 +0100
#+++ static/usr/i686-pc-mingw32/sys-root/mingw/lib/glib-2.0/include/glibconfig.h	2009-02-20 17:33:35.498932269 +0100
#@@ -92,7 +92,8 @@
# 
# #define G_OS_WIN32
# #define G_PLATFORM_WIN32
#-
#+#define GLIB_STATIC_COMPILATION 1
#+#define GOBJECT_STATIC_COMPILATION 1
# 
# #define G_VA_COPY	va_copy
#
# However, we can't merge this change as it is situation-dependent...
#
# Developers using the static build of GLib need to add -DGLIB_STATIC_COMPILATION
# and -DGOBJECT_STATIC_COMPILATION to their CFLAGS to avoid compile failures

# Drop the folder which was temporary used for installing the static bits
rm -f %{buildroot}/%{mingw32_libdir}/charset.alias
rm -f %{buildroot}/%{mingw64_libdir}/charset.alias

# Drop the GDB helper files as we can't use the native Fedora GDB to debug Win32 programs
rm -rf %{buildroot}%{mingw32_datadir}/gdb
rm -rf %{buildroot}%{mingw64_datadir}/gdb

# Remove the gtk-doc documentation and manpages which duplicate Fedora native
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw32_datadir}/gtk-doc

rm -rf %{buildroot}%{mingw64_mandir}
rm -rf %{buildroot}%{mingw64_datadir}/gtk-doc

# Bash-completion files aren't interesting for mingw
rm -rf %{buildroot}%{mingw32_datadir}/bash-completion
rm -rf %{buildroot}%{mingw64_datadir}/bash-completion

# The .def files are also of no use to other binaries
rm -f %{buildroot}%{mingw32_libdir}/*.def
rm -f %{buildroot}%{mingw64_libdir}/*.def

# The gdbus-codegen pieces are already in the native glib2 package
rm -f %{buildroot}%{mingw32_bindir}/gdbus-codegen
rm -rf %{buildroot}%{mingw32_libdir}/gdbus-2.0
sed -i 's|gdbus_codegen=.*|gdbus_codegen=%{_bindir}/gdbus-codegen|g' %{buildroot}%{mingw32_libdir}/pkgconfig/gio-2.0.pc

rm -f %{buildroot}%{mingw64_bindir}/gdbus-codegen
rm -rf %{buildroot}%{mingw64_libdir}/gdbus-2.0
sed -i 's|gdbus_codegen=.*|gdbus_codegen=%{_bindir}/gdbus-codegen|g' %{buildroot}%{mingw64_libdir}/pkgconfig/gio-2.0.pc

# Delete installed tests
rm -rf %{buildroot}%{mingw32_libexecdir}/installed-tests/
rm -rf %{buildroot}%{mingw64_libexecdir}/installed-tests/

# Drop all .la files
find %{buildroot} -name "*.la" -delete

%mingw_find_lang glib20

# Manually invoke the python byte compile macro for each path that needs byte
# compilation.
%py_byte_compile %{__python3} %{buildroot}%{mingw32_datadir}/glib-2.0/gdb
%py_byte_compile %{__python3} %{buildroot}%{mingw32_datadir}/glib-2.0/codegen
%py_byte_compile %{__python3} %{buildroot}%{mingw64_datadir}/glib-2.0/gdb
%py_byte_compile %{__python3} %{buildroot}%{mingw64_datadir}/glib-2.0/codegen


# Win32
%files -n mingw32-glib2 -f mingw32-glib20.lang
%license LICENSES/LGPL-2.1-or-later.txt
%{mingw32_bindir}/gdbus.exe
%{mingw32_bindir}/gi-compile-repository.exe
%{mingw32_bindir}/gi-decompile-typelib.exe
%{mingw32_bindir}/gi-inspect-typelib.exe
%{mingw32_bindir}/gio.exe
%{mingw32_bindir}/gio-querymodules.exe
%{mingw32_bindir}/glib-compile-resources.exe
%{mingw32_bindir}/glib-compile-schemas.exe
%{mingw32_bindir}/glib-genmarshal
%{mingw32_bindir}/glib-gettextize
%{mingw32_bindir}/glib-mkenums
%{mingw32_bindir}/gobject-query.exe
%{mingw32_bindir}/gresource.exe
%{mingw32_bindir}/gsettings.exe
%{mingw32_bindir}/gspawn-win32-helper-console.exe
%{mingw32_bindir}/gspawn-win32-helper.exe
%{mingw32_bindir}/gtester-report
%{mingw32_bindir}/libgio-2.0-0.dll
%{mingw32_bindir}/libglib-2.0-0.dll
%{mingw32_bindir}/libgmodule-2.0-0.dll
%{mingw32_bindir}/libgobject-2.0-0.dll
%{mingw32_bindir}/libgirepository-2.0-0.dll
%{mingw32_bindir}/libgthread-2.0-0.dll
%{mingw32_includedir}/glib-2.0/
%{mingw32_includedir}/gio-win32-2.0/
%{mingw32_libdir}/glib-2.0/
%{mingw32_libdir}/libgio-2.0.dll.a
%{mingw32_libdir}/libglib-2.0.dll.a
%{mingw32_libdir}/libgmodule-2.0.dll.a
%{mingw32_libdir}/libgobject-2.0.dll.a
%{mingw32_libdir}/libgirepository-2.0.dll.a
%{mingw32_libdir}/libgthread-2.0.dll.a
%{mingw32_libdir}/pkgconfig/gio-2.0.pc
%{mingw32_libdir}/pkgconfig/gio-windows-2.0.pc
%{mingw32_libdir}/pkgconfig/girepository-2.0.pc
%{mingw32_libdir}/pkgconfig/glib-2.0.pc
%{mingw32_libdir}/pkgconfig/gmodule-2.0.pc
%{mingw32_libdir}/pkgconfig/gmodule-export-2.0.pc
%{mingw32_libdir}/pkgconfig/gmodule-no-export-2.0.pc
%{mingw32_libdir}/pkgconfig/gobject-2.0.pc
%{mingw32_libdir}/pkgconfig/gthread-2.0.pc
%{mingw32_datadir}/aclocal/glib-2.0.m4
%{mingw32_datadir}/aclocal/glib-gettext.m4
%{mingw32_datadir}/aclocal/gsettings.m4
%{mingw32_datadir}/gettext/its/
%{mingw32_datadir}/glib-2.0/

%files -n mingw32-glib2-static
%{mingw32_libdir}/libgio-2.0.a
%{mingw32_libdir}/libgirepository-2.0.a
%{mingw32_libdir}/libglib-2.0.a
%{mingw32_libdir}/libgmodule-2.0.a
%{mingw32_libdir}/libgobject-2.0.a
%{mingw32_libdir}/libgthread-2.0.a

# Win64
%files -n mingw64-glib2 -f mingw64-glib20.lang
%license LICENSES/LGPL-2.1-or-later.txt
%{mingw64_bindir}/gdbus.exe
%{mingw64_bindir}/gi-compile-repository.exe
%{mingw64_bindir}/gi-decompile-typelib.exe
%{mingw64_bindir}/gi-inspect-typelib.exe
%{mingw64_bindir}/gio.exe
%{mingw64_bindir}/gio-querymodules.exe
%{mingw64_bindir}/glib-compile-resources.exe
%{mingw64_bindir}/glib-compile-schemas.exe
%{mingw64_bindir}/glib-genmarshal
%{mingw64_bindir}/glib-gettextize
%{mingw64_bindir}/glib-mkenums
%{mingw64_bindir}/gobject-query.exe
%{mingw64_bindir}/gresource.exe
%{mingw64_bindir}/gsettings.exe
%{mingw64_bindir}/gspawn-win64-helper-console.exe
%{mingw64_bindir}/gspawn-win64-helper.exe
%{mingw64_bindir}/gtester-report
%{mingw64_bindir}/libgio-2.0-0.dll
%{mingw64_bindir}/libglib-2.0-0.dll
%{mingw64_bindir}/libgmodule-2.0-0.dll
%{mingw64_bindir}/libgobject-2.0-0.dll
%{mingw64_bindir}/libgirepository-2.0-0.dll
%{mingw64_bindir}/libgthread-2.0-0.dll
%{mingw64_includedir}/glib-2.0/
%{mingw64_includedir}/gio-win32-2.0/
%{mingw64_libdir}/glib-2.0/
%{mingw64_libdir}/libgio-2.0.dll.a
%{mingw64_libdir}/libglib-2.0.dll.a
%{mingw64_libdir}/libgmodule-2.0.dll.a
%{mingw64_libdir}/libgobject-2.0.dll.a
%{mingw64_libdir}/libgirepository-2.0.dll.a
%{mingw64_libdir}/libgthread-2.0.dll.a
%{mingw64_libdir}/pkgconfig/gio-2.0.pc
%{mingw64_libdir}/pkgconfig/gio-windows-2.0.pc
%{mingw64_libdir}/pkgconfig/girepository-2.0.pc
%{mingw64_libdir}/pkgconfig/glib-2.0.pc
%{mingw64_libdir}/pkgconfig/gmodule-2.0.pc
%{mingw64_libdir}/pkgconfig/gmodule-export-2.0.pc
%{mingw64_libdir}/pkgconfig/gmodule-no-export-2.0.pc
%{mingw64_libdir}/pkgconfig/gobject-2.0.pc
%{mingw64_libdir}/pkgconfig/gthread-2.0.pc
%{mingw64_datadir}/aclocal/glib-2.0.m4
%{mingw64_datadir}/aclocal/glib-gettext.m4
%{mingw64_datadir}/aclocal/gsettings.m4
%{mingw64_datadir}/gettext/its/
%{mingw64_datadir}/glib-2.0/

%files -n mingw64-glib2-static
%{mingw64_libdir}/libgio-2.0.a
%{mingw64_libdir}/libgirepository-2.0.a
%{mingw64_libdir}/libglib-2.0.a
%{mingw64_libdir}/libgmodule-2.0.a
%{mingw64_libdir}/libgobject-2.0.a
%{mingw64_libdir}/libgthread-2.0.a


%changelog
* Thu Jan 29 2026 Sandro Mani <manisandro@gmail.com> - 2.86.3-3
- Backport fixes for CVE-2026-1484, CVE-2026-1485, CVE-2026-1489
- Remove ancient, obsolete downstream patch from 2012 (RHBZ#2431179)

* Sat Jan 17 2026 Sandro Mani <manisandro@gmail.com> - 2.86.3-2
- Backport fix for CVE-2026-0988

* Sun Dec 14 2025 Sandro Mani <manisandro@gmail.com> - 2.86.3-1
- Update to 2.86.3

* Sat Nov 15 2025 Sandro Mani <manisandro@gmail.com> - 2.87.0-1
- Update to 2.87.0

* Thu Oct 30 2025 Sandro Mani <manisandro@gmail.com> - 2.86.1-1
- Update to 2.86.1

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.86.0-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Thu Sep 18 2025 Sandro Mani <manisandro@gmail.com> - 2.86.0-1
- Update to 2.86.0

* Wed Aug 27 2025 Sandro Mani <manisandro@gmail.com> - 2.85.4-1
- Update to 2.85.4

* Sat Aug 16 2025 Sandro Mani <manisandro@gmail.com> - 2.85.3-1
- Update to 2.85.3

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.85.2-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Sun Jul 27 2025 Sandro Mani <manisandro@gmail.com> - 2.85.2-1
- Update to 2.85.2

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.85.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Sandro Mani <manisandro@gmail.com> - 2.85.1-2
- Fix incorrectly installed license file

* Sun Jun 15 2025 Sandro Mani <manisandro@gmail.com> - 2.85.1-1
- Update to 2.85.1

* Thu May 29 2025 Sandro Mani <manisandro@gmail.com> - 2.85.0-1
- Update to 2.85.0

* Sat Apr 05 2025 Sandro Mani <manisandro@gmail.com> - 2.84.1-1
- Update to 2.84.1

* Tue Mar 11 2025 Sandro Mani <manisandro@gmail.com> - 2.84.0-1
- Update to 2.84.0

* Wed Mar 05 2025 Sandro Mani <manisandro@gmail.com> - 2.83.5-1
- Update to 2.83.5

* Sat Jan 25 2025 Sandro Mani <manisandro@gmail.com> - 2.83.3-1
- Update to 2.83.3

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.83.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Nov 09 2024 Sandro Mani <manisandro@gmail.com> - 2.83.0-1
- Update to 2.83.0

* Mon Oct 21 2024 Sandro Mani <manisandro@gmail.com> - 2.82.2-1
- Update to 2.82.2

* Mon Sep 23 2024 Sandro Mani <manisandro@gmail.com> - 2.82.1-1
- Update to 2.82.1

* Tue Aug 27 2024 Sandro Mani <manisandro@gmail.com> - 2.82.0-1
- Update to 2.82.0

* Mon Aug 19 2024 Sandro Mani <manisandro@gmail.com> - 2.81.2-1
- Update to 2.81.2

* Tue Aug 06 2024 Sandro Mani <manisandro@gmail.com> - 2.81.1-1
- Update to 2.81.1

* Tue Jul 30 2024 Sandro Mani <manisandro@gmail.com> - 2.81.0-1
- Update to 2.81.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.80.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 15 2024 Sandro Mani <manisandro@gmail.com> - 2.80.3-1
- Update to 2.80.3

* Fri May 10 2024 Sandro Mani <manisandro@gmail.com> - 2.80.2-1
- Update to 2.80.2

* Tue May 07 2024 Sandro Mani <manisandro@gmail.com> - 2.80.1-1
- Update to 2.80.1

* Sat Mar 23 2024 Sandro Mani <manisandro@gmail.com> - 2.80.0-1
- Update to 2.80.0

* Fri Jan 26 2024 Sandro Mani <manisandro@gmail.com> - 2.79.1-1
- Update to 2.79.1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.79.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.79.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Sandro Mani <manisandro@gmail.com> - 2.79.0-1
- Update to 2.79.0

* Thu Dec 07 2023 Sandro Mani <manisandro@gmail.com> - 2.78.3-1
- Update to 2.78.3

* Sat Oct 28 2023 Sandro Mani <manisandro@gmail.com> - 2.78.1-1
- Update to 2.78.1

* Tue Sep 19 2023 Sandro Mani <manisandro@gmail.com> - 2.78.0-1
- Update to 2.78.0

* Sat Sep 02 2023 Sandro Mani <manisandro@gmail.com> - 2.77.3-1
- Update to 2.77.3

* Tue Aug 15 2023 Sandro Mani <manisandro@gmail.com> - 2.77.2-1
- Update to 2.77.2

* Fri Aug 04 2023 Sandro Mani <manisandro@gmail.com> - 2.77.1-1
- Update to 2.77.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.77.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Sandro Mani <manisandro@gmail.com> - 2.77.0-1
- Update to 2.77.0

* Mon Jul 10 2023 Sandro Mani <manisandro@gmail.com> - 2.76.4-1
- Update to 2.76.4

* Wed May 24 2023 Sandro Mani <manisandro@gmail.com> - 2.76.3-1
- Update to 2.76.3

* Mon Apr 24 2023 Sandro Mani <manisandro@gmail.com> - 2.76.2-1
- Update to 2.76.2

* Thu Mar 23 2023 Sandro Mani <manisandro@gmail.com> - 2.76.1-1
- Update to 2.76.1

* Sun Mar 19 2023 Sandro Mani <manisandro@gmail.com> - 2.76.0-1
- Update to 2.76.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.74.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 14 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 2.74.1-2
- Set gio-2.0.pc gdbus_codegen variable to system path.

* Sun Oct 30 2022 Sandro Mani <manisandro@gmail.com> - 2.74.1-1
- Update to 2.74.1

* Wed Sep 21 2022 Sandro Mani <manisandro@gmail.com> - 2.74.0-1
- Update to 2.74.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.72.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Sandro Mani <manisandro@gmail.com> - 2.72.3-1
- Update to 2.72.3

* Tue May 31 2022 Sandro Mani <manisandro@gmail.com> - 2.72.2-1
- Update to 2.72.2

* Sun Apr 17 2022 Sandro Mani <manisandro@gmail.com> - 2.72.1-1
- Update to 2.72.1

* Mon Mar 28 2022 Sandro Mani <manisandro@gmail.com> - 2.72.0-1
- Update to 2.72.0

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 2.71.3-2
- Rebuild with mingw-gcc-12

* Mon Mar 07 2022 Sandro Mani <manisandro@gmail.com> - 2.71.3-1
- Update to 2.71.3

* Tue Feb 15 2022 Sandro Mani <manisandro@gmail.com> - 2.71.2-1
- Update to 2.71.2

* Sun Jan 30 2022 Sandro Mani <manisandro@gmail.com> - 2.71.1-1
- Update to 2.71.1

* Tue Jan 25 2022 Sandro Mani <manisandro@gmail.com> - 2.71.0-1
- Update to 2.71.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.70.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 07 2021 Sandro Mani <manisandro@gmail.com> - 2.70.2-1
- Update to 2.70.2

* Mon Nov 01 2021 Sandro Mani <manisandro@gmail.com> - 2.70.1-1
- Update to 2.70.1

* Tue Sep 21 2021 Sandro Mani <manisandro@gmail.com> - 2.70.0-1
- Update to 2.70.0

* Fri Sep 10 2021 Sandro Mani <manisandro@gmail.com> - 2.69.3-1
- Update to 2.69.3

* Sat Aug 28 2021 Sandro Mani <manisandro@gmail.com> - 2.69.2-1
- Update to 2.69.2

* Fri Jul 30 2021 Sandro Mani <manisandro@gmail.com> - 2.69.0-2
- Rebuild (libffi)

* Sat Jul 24 2021 Sandro Mani <manisandro@gmail.com> - 2.69.0-1
- Update to 2.69.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.68.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Sandro Mani <manisandro@gmail.com> - 2.68.3-1
- Update to 2.68.3

* Thu May 20 2021 Sandro Mani <manisandro@gmail.com> - 2.68.2-1
- Update to 2.68.2

* Mon Apr 12 2021 Sandro Mani <manisandro@gmail.com> - 2.68.1-1
- Update to 2.68.1

* Mon Mar 29 2021 Sandro Mani <manisandro@gmail.com> - 2.68.0-1
- Update to 2.68.0

* Fri Mar 05 2021 Sandro Mani <manisandro@gmail.com> - 2.66.7-1
- Update to 2.66.7

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.66.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 19 2020 Sandro Mani <manisandro@gmail.com> - 2.66.2-1
- Update to 2.66.2

* Mon Oct 05 2020 Sandro Mani <manisandro@gmail.com> - 2.66.1-1
- Update to 2.66.1

* Tue Sep 15 2020 Sandro Mani <manisandro@gmail.com> - 2.66.0-1
- Update to 2.66.0

* Wed Aug 12 13:36:55 GMT 2020 Sandro Mani <manisandro@gmail.com> - 2.64.3-3
- Rebuild (mingw-gettext)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.64.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Sandro Mani <manisandro@gmail.com> - 2.64.3-1
- Update to 2.64.3

* Mon Apr 20 2020 Sandro Mani <manisandro@gmail.com> - 2.64.2-2
- Rebuild (gettext)

* Sat Apr 11 2020 Sandro Mani <manisandro@gmail.com> - 2.64.2-1
- Update to 2.64.2

* Thu Mar 12 2020 Sandro Mani <manisandro@gmail.com> - 2.64.1-1
- Update to 2.64.1

* Fri Mar 06 2020 Sandro Mani <manisandro@gmail.com> - 2.64.0-1
- Update to 2.64.0

* Tue Feb 25 2020 Sandro Mani <manisandro@gmail.com> - 2.63.6-1
- Update to 2.63.6

* Tue Feb 11 2020 Sandro Mani <manisandro@gmail.com> - 2.63.5-2
- Backport proposed patch for CVE-2020-6750

* Mon Feb 03 2020 Sandro Mani <manisandro@gmail.com> - 2.63.5-1
- Update to 2.63.5

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.63.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Sandro Mani <manisandro@gmail.com> - 2.63.4-1
- Update to 2.63.4

* Mon Dec 16 2019 Sandro Mani <manisandro@gmail.com> - 2.63.3-1
- Update to 2.63.3

* Tue Dec 03 2019 Sandro Mani <manisandro@gmail.com> - 2.63.2-1
- Update to 2.63.2

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 2.63.0-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Fri Oct 04 2019 Sandro Mani <manisandro@gmail.com> - 2.63.0-1
- Update to 2.63.0

* Mon Sep 16 2019 Sandro Mani <manisandro@gmail.com> - 2.62.0-1
- Update to 2.62.0

* Wed Sep 04 2019 Sandro Mani <manisandro@gmail.com> - 2.61.3-1
- Update to 2.61.3

* Thu Aug 15 2019 Fabiano Fidêncio <fidencio@redhat.com> - 2.61.2-1
- Update to 2.61.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.58.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.58.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Kalev Lember <klember@redhat.com> - 2.58.3-1
- Update to 2.58.3

* Tue Jan 08 2019 Kalev Lember <klember@redhat.com> - 2.58.2-1
- Update to 2.58.2

* Fri Sep 21 2018 Kalev Lember <klember@redhat.com> - 2.58.1-1
- Update to 2.58.1

* Thu Aug 02 2018 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.57.2-1
- Update to 2.57.2

* Thu Aug 02 2018 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.57.1-1
- Update to 2.57.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.56.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.56.1-2
- Rebuilt for Python 3.7

* Mon May 28 2018 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.56.1-1
- Update to 2.56.1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.54.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 15 2017 Kalev Lember <klember@redhat.com> - 2.54.1-1
- Update to 2.54.1

* Mon Aug 21 2017 Kalev Lember <klember@redhat.com> - 2.53.6-1
- Update to 2.53.6

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.52.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 2.52.2-2
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Mon Jun 19 2017 Kalev Lember <klember@redhat.com> - 2.52.2-1
- Update to 2.52.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.50.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 2.50.1-1
- Update to 2.50.1

* Fri Sep 23 2016 Kalev Lember <klember@redhat.com> - 2.50.0-1
- Update to 2.50.0

* Fri Sep 16 2016 Kalev Lember <klember@redhat.com> - 2.48.2-2
- Add missing perl dep for glib-mkenums
- Don't set group tags

* Thu Aug 18 2016 Kalev Lember <klember@redhat.com> - 2.48.2-1
- Update to 2.48.2

* Tue May 10 2016 Kalev Lember <klember@redhat.com> - 2.48.1-1
- Update to 2.48.1

* Mon May  2 2016 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.48.0-1
- update to 2.48.0

* Sun Feb  7 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.47.5-1
- Update to 2.47.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.47.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Richard Jones <rjones@redhat.com> - 2.47.4-2
- Use global instead of define.

* Tue Dec 29 2015 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.47.4-1
- Update to 2.47.4

* Wed Nov 18 2015 Kalev Lember <klember@redhat.com> - 2.46.2-1
- Update to 2.46.2

* Fri Oct 16 2015 Kalev Lember <klember@redhat.com> - 2.46.1-1
- Update to 2.46.1

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 2.46.0-1
- Update to 2.46.0

* Sat Aug 22 2015 Kalev Lember <klember@redhat.com> - 2.45.6-1
- Update to 2.45.6

* Thu Jul  2 2015 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.45.3-1
- Update to 2.45.3

* Tue Jun 23 2015 Fabiano Fidêncio <fidencio@redhat.com> - 2.44.0-4
- gio/ginetaddress.c: Fix Windows XP inet_pton() Emulation
  (https://bugzilla.gnome.org/show_bug.cgi?id=730352#c24)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.44.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 20 2015 Kalev Lember <kalevlember@gmail.com> - 2.44.0-2
- Add back two accidentally dropped GNetworkMonitor crasher fixes
  (GNOME BZ #733338)

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 2.44.0-1
- Update to 2.44.0
- Use license macro for the COPYING file

* Mon Jan 26 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.43.3-1
- Update to 2.43.3

* Sat Nov 15 2014 Kalev Lember <kalevlember@gmail.com> - 2.42.1-1
- Update to 2.42.1

* Tue Sep 23 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.42.0-1
- Update to 2.42.0

* Sat Sep 20 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.41.5-1
- Update to 2.41.5

* Fri Sep 12 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.41.4-1
- Update to 2.41.4

* Tue Jul 22 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.41.2-1
- Update to 2.41.2

* Sat Jun 14 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.41.0-3
- Prevent an invalid @CARBON_LIBS@ from appearing in the .pc files (GNOME BZ #731657)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jun  1 2014 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.41.0-1
- update to 2.41.0

* Thu May 15 2014 Richard W.M. Jones <rjones@redhat.com> - 2.40.0-3
- Fix valgrind support (RHBZ#1095664, GNOME bug 730198).
- Include <stdint.h>, required by valgrind.h only on Rawhide.

* Sat Mar 29 2014 Kalev Lember <kalevlember@gmail.com> - 2.40.0-1
- Update to 2.40.0

* Thu Mar  6 2014 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.39.91-1
- Update to 2.39.91

* Sat Mar  1 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.39.90-1
- Update to 2.39.90

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.39.4-1
- Update to 2.39.4

* Tue Dec 17 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.39.2-1
- Update to 2.39.2

* Wed Nov 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.39.1-1
- Update to 2.39.1

* Wed Nov 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.38.2-1
- Update to 2.38.2

* Tue Sep 24 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.38.0-1
- Update to 2.38.0

* Wed Sep  4 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.37.7-1
- Update to 2.37.7

* Thu Aug  1 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.37.5-1
- Update to 2.37.5

* Wed Jul 10 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.37.4-1
- Update to 2.37.4

* Thu Jun 27 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.3-2
- Include the COPYING file in %%doc (thanks daumas for noticing it!)

* Wed Jun 26 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.37.3-1
- Update to 2.37.3

* Sun Jun 16 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.37.1-2
- Rebuild to resolve InterlockedCompareExchange regression in mingw32 libraries

* Fri May 31 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.37.1-1
- Update to 2.37.1

* Sun May  5 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.37.0-1
- Update to 2.37.0

* Tue Apr 16 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.36.1-1
- Update to 2.36.1
- Dropped upstreamed patches

* Mon Apr 15 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.36.0-3
- Revert unintended ABI break on win64 (RHBZ #951588, GNOME BZ #697879)

* Fri Mar 29 2013 Kalev Lember <kalevlember@gmail.com> - 2.36.0-2
- Drop two patches that have been fixed upstream

* Tue Mar 26 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.36.0-1
- Update to 2.36.0

* Sat Mar 23 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.35.9-1
- Update to 2.35.9
- Added R: mingw{32,64}-gettext-static to the -static subpackages
- Prefer the use of GCC constructors over DllMain
  This removes the DllMain symbol from the static libraries

* Fri Feb 22 2013 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.35.8-1
- update to 2.35.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.35.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.35.4-3
- Replaced the gcc 4.8 workaround with a more proper fix (GNOME BZ #692079)

* Sat Jan 19 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.35.4-2
- Work around more strict behaviour of gcc 4.8, GNOME BZ #692079
- Use verbose make

* Wed Jan 16 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.35.4-1
- Update to 2.35.4

* Thu Jan  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.35.3-3
- Resolve regression regarding linking against C++ code (GNOME BZ #690902)

* Tue Jan  1 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.35.3-2
- Make sure g_log_default_handler uses the correct file descriptors for stdout and stderr

* Tue Jan  1 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.35.3-1
- Update to 2.35.3

* Fri Nov  9 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.35.1-1
- Update to 2.35.1

* Sat Oct 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.34.1-1
- Update to 2.34.1

* Fri Oct  5 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.34.0-1
- Update to 2.34.0

* Mon Aug 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.33.10-2
- Use CreateFile on Win32 to make sure g_unlink always works (GNOME BZ #674214)
- Fixed typo's in description

* Sat Aug 25 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.33.10-1
- Update to 2.33.10

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 05 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.33.1-1
- Update to 2.33.1

* Sat May 05 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.32.2-2
- Fix compile failure while building static library (GNOME BZ #675516)

* Tue May 01 2012 Kalev Lember <kalevlember@gmail.com> - 2.32.2-1
- Update to 2.32.2
- Dropped upstreamed patches

* Sat Apr 14 2012 Kalev Lember <kalevlember@gmail.com> - 2.32.1-1
- Update to 2.32.1
- Dropped an upstreamed patch
- Added two new patches to fix build

* Wed Mar 28 2012 Kalev Lember <kalevlember@gmail.com> - 2.32.0-2
- Add a patch to fix alignment tests when cross compiling

* Mon Mar 26 2012 Kalev Lember <kalevlember@gmail.com> - 2.32.0-1
- Update to 2.32.0
- Dropped upstreamed patch

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.31.20-2
- Added win64 support

* Thu Mar 08 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.31.20-1
- Update to 2.31.20
- Dropped unneeded BR: mingw32-dlfcn
- Dropped .la files

* Tue Mar 06 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.31.18-2
- Renamed the source package to mingw-glib2 (RHBZ #800389)
- Use mingw macros without leading underscore

* Tue Feb 28 2012 Kalev Lember <kalevlember@gmail.com> - 2.31.18-1
- Update to 2.31.18

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.31.16-2
- Rebuild against the mingw-w64 toolchain

* Tue Feb 07 2012 Kalev Lember <kalevlember@gmail.com> - 2.31.16-1
- Update to 2.31.16

* Thu Jan 12 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.31.8-1
- Update to 2.31.8

* Tue Nov 22 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.31.2-1
- Update to 2.31.2

* Tue Oct 18 2011 Kalev Lember <kalevlember@gmail.com> - 2.30.1-1
- Update to 2.30.1

* Fri Sep 30 2011 Kalev Lember <kalevlember@gmail.com> - 2.30.0-1
- Update to 2.30.0

* Tue Aug 30 2011 Kalev Lember <kalevlember@gmail.com> - 2.29.18-1
- Update to 2.29.18

* Sun Jul 10 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.29.10-2
- Dropped the gdbus-codegen pieces as they match the native glib2 package

* Fri Jul 08 2011 Kalev Lember <kalevlember@gmail.com> - 2.29.10-1
- Update to 2.29.10
- Switch to xz compressed tarballs

* Wed Jul 06 2011 Kalev Lember <kalevlember@gmail.com> - 2.28.6-4
- Rebuilt against win-iconv

* Thu Apr 28 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.28.6-3
- Own the folders %%{_mingw32_libdir}/gio and %%{_mingw32_libdir}/gio/modules
- Dropped the .def files as they aren't useful for other binaries

* Wed Apr 27 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.28.6-2
- Dropped the proxy-libintl pieces

* Sat Apr 23 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.28.6-1
- Update to 2.28.6
- Dropped the ugly build hack as it isn't needed anymore (the
  broken mingw32-runtime has been fixed by now)
- Made the pkgconfig LDFLAGS libtool friendly (fixes compilation for
  non-libtool based projects such as midori)

* Sun Feb 13 2011 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.28.0-1
- update to 2.28.0

* Sun Feb 13 2011 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.27.93-1
- update to 2.27.93

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec  6 2010 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.27.4-1
- update to 2.27.4

* Sun Nov  7 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.26.0-4
- Fix a build failure in mingw32-libsoup and mingw32-webkitgtk

* Sun Oct 17 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.26.0-3
- Let binaries depending on GLib link against the libintl wrapper library
  in a way that libtool doesn't refuse

* Sat Oct 16 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.26.0-2
- Rebuild in order to make libintl-8.dll a soft dependency

* Mon Oct 11 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.26.0-1
- Update to 2.26.0

* Thu Sep 23 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.25.17-1
- Update to 2.25.17

* Sun Sep 12 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.25.15-1
- Update to 2.25.15

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 2.25.12-2
- recompiling .py files against Python 2.7 (rhbz#623338)

* Thu Aug  5 2010 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.25.12-1
- update to 2.25.12

* Fri Jun 11 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.24.1-1
- Update to 2.24.1

* Wed Feb 24 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.23.4-1
- Update to 2.23.4

* Sun Jan 31 2010 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.23.2-1
- Update to 2.23.2

* Wed Dec  2 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.23.0-1
- Update to 2.23.0
- Added BR: mingw32-zlib

* Fri Oct  9 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.2-1
- Update to 2.22.2

* Wed Sep 23 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.22.0-1
- Update to 2.22.0

* Fri Sep 18 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.6-2
- Rebuild because of broken mingw32-gcc/mingw32-binutils

* Sat Sep  5 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.6-1
- Update to 2.21.6

* Mon Aug 24 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.5-1
- Update to 2.21.5

* Thu Aug 13 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.4-1
- Update to 2.21.4

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.3-1
- Update to 2.21.3
- Drop upstreamed patch

* Mon Jun 22 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.2-2
- The wrong RPM variable was overriden for -debuginfo support. Should be okay now

* Mon Jun 22 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.2-1
- Update to 2.21.2
- Split out debug symbols to a -debuginfo subpackage

* Wed Jun 10 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21.1-1
- Update to 2.21.1
- Use %%global instead of %%define
- Dropped the glib-i386-atomic.patch as it doesn't have any effect (the mingw32
  toolchain is called i686-pc-mingw32, not i386-pc-mingw32)

* Thu Apr 16 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 2.20.1-1
- Update to 2.20.1

* Thu Mar 5 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.19.10-1
- Update to 2.19.10
- Dropped the gtk-doc documentation as it's identical to the base glib2 package

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Erik van Pienbroek <info@nntpgrab.nl> - 2.19.5-4
- Added -static subpackage
- Developers using the static build of GLib need to add
  -DGLIB_STATIC_COMPILATION and -DGOBJECT_STATIC_COMPILATION to
  their CFLAGS to avoid compile failures
- Fixed the %%defattr line
- Rebuild for mingw32-gcc 4.4 (RWMJ)

* Fri Jan 30 2009 Richard W.M. Jones <rjones@redhat.com> - 2.19.5-3
- Requires pkgconfig.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.19.5-2
- Rebase to native Fedora version 2.19.5.
- Use _smp_mflags.
- Use find_lang.
- Don't build static libraries.
- +BR dlfcn.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.1-2
- Rename mingw -> mingw32.

* Mon Sep 22 2008 Daniel P. Berrange <berrange@redhat.com> - 2.18.1-1
- Update to 2.18.1 release

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 2.18.0-3
- Remove manpages which duplicate Fedora native.

* Thu Sep 11 2008 Daniel P. Berrange <berrange@redhat.com> - 2.18.0-2
- Add BR on pkgconfig, gettext and glib2 (native)

* Tue Sep  9 2008 Daniel P. Berrange <berrange@redhat.com> - 2.18.0-1
- Initial RPM release
