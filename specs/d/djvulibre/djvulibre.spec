# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define         _hardened_build 1

%if 0%{?el10}
%bcond_with inkscape
%else
%bcond_without inkscape
%endif

Summary: DjVu viewers, encoders, and utilities
Name: djvulibre
Version: 3.5.28
Release: 14%{?dist}
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License: GPL-2.0-or-later
URL: http://djvu.sourceforge.net/
Source0: http://downloads.sourceforge.net/djvu/%{name}-%{version}.tar.gz
Patch0: djvulibre-3.5.22-cdefs.patch
#Patch1: djvulibre-3.5.25.3-cflags.patch
Patch6: djvulibre-3.5.27-export-file.patch
Patch8: djvulibre-3.5.27-check-image-size.patch
Patch9: djvulibre-3.5.27-integer-overflow.patch
Patch10: djvulibre-3.5.27-check-input-pool.patch
Patch11: djvulibre-3.5.27-djvuport-stack-overflow.patch
Patch12: djvulibre-3.5.27-unsigned-short-overflow.patch
Patch14: djvulibre-3.5.27-out-of-bound-write-2.patch
Patch15: 0001-Check-for-zero-width-and-height.patch

Requires(post): xdg-utils
Requires(preun): xdg-utils
BuildRequires: chrpath
BuildRequires: gcc-c++
BuildRequires: hicolor-icon-theme
%if %{with inkscape}
BuildRequires: inkscape
%endif
BuildRequires: libjpeg-turbo-devel
BuildRequires: libtiff-devel
BuildRequires: make
BuildRequires: xdg-utils

Provides: %{name}-mozplugin = %{version}
Obsoletes: %{name}-mozplugin < 3.5.24

%description
DjVu is a web-centric format and software platform for distributing documents
and images. DjVu can advantageously replace PDF, PS, TIFF, JPEG, and GIF for
distributing scanned documents, digital documents, or high-resolution pictures.
DjVu content downloads faster, displays and renders faster, looks nicer on a
screen, and consume less client resources than competing formats. DjVu images
display instantly and can be smoothly zoomed and panned with no lengthy
re-rendering.

DjVuLibre is a free (GPL'ed) implementation of DjVu, including viewers,
decoders, simple encoders, and utilities. The browser plugin is in its own
separate sub-package.


%package libs
Summary: Library files for DjVuLibre

%description libs
Library files for DjVuLibre.


%package devel
Summary: Development files for DjVuLibre
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig

%description devel
Development files for DjVuLibre.


%prep
%setup -q 
%patch -P0 -p1 -b .cdefs
#%patch1 -p1 -b .cflags
%patch -P6 -p1 -b .export-file
%patch -P8 -p1 -b .check-image-size
%patch -P9 -p1 -b .integer-overflow
%patch -P10 -p1 -b .check-input-pool
%patch -P11 -p1 -b .djvuport-stack-overflow
%patch -P12 -p1 -b .unsigned-short-overflow
%patch -P14 -p1 -b .out-of-bound-write-2
%patch -P15 -p1 -b .zero-size-image


%build 
%configure --with-qt=%{_libdir}/qt-3.3 --enable-threads
# Disable rpath on 64bit - NOT! It makes the build fail (still as of 3.5.20-2)
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install

# Fix for the libs to get stripped correctly (still required in 3.5.20-2)
find %{buildroot}%{_libdir} -name '*.so*' | xargs %{__chmod} +x

# Remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvutoxml
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvused
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/cjb2
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/csepdjvu
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvuserve
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvm
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvuxmlparser
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvutxt
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/ddjvu
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvumake
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/cpaldjvu
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvuextract
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/c44
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvups
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvudump
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/djvmcvt
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/bzz

# This XML file does not differentiate between DjVu Image and DjVu Document
# MIME types, the default one in shared-mime-info does.
rm -f $RPM_BUILD_ROOT%{_datadir}/mime/packages/djvulibre-mime.xml

# MIME types (icons and desktop file) - this installs icon files under
# /usr/share/icons/hicolor/ and an xml file under /usr/share/mime/image/
# Taken from {_datadir}/djvu/osi/desktop/register-djvu-mime install
# See also the README file in the desktopfiles directory of the source distribution
pushd desktopfiles
for i in 22 32 48 64 ; do
    install -d $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/
    cp -a ./prebuilt-hi${i}-djvu.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/image-vnd.djvu.mime.png
#    cp -a ./hi${i}-djvu.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${i}x${i}/mimetypes/gnome-mime-image-vnd.djvu.png
done
popd


%post
# Unregister menu entry for djview3 if it is present as we no longer
# ship this in favour of the djview4 package. These files were
# installed in %post by the older djvulibre packages, but not actually
# owned by the package (packaging bug)
rm -f %{_datadir}/applications/djvulibre-djview3.desktop || :
rm -f %{_datadir}/icons/hicolor/32x32/apps/djvulibre-djview3.png || :


%preun
# This is the legacy script, not compliant with current packaging
# guidelines. However, we leave it in, as the old packages didn't own
# the icon and xml files, so we want to be sure we remove them
if [ $1 -eq 0 ]; then
    # MIME types (icons and desktop file)
    %{_datadir}/djvu/osi/desktop/register-djvu-mime uninstall || :
fi


%ldconfig_scriptlets libs


%files
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/djvu/
%{_datadir}/icons/hicolor/16x16/mimetypes/*
%{_datadir}/icons/hicolor/20x20/mimetypes/*
%{_datadir}/icons/hicolor/22x22/mimetypes/*
%{_datadir}/icons/hicolor/24x24/mimetypes/*
%{_datadir}/icons/hicolor/32x32/mimetypes/*
%{_datadir}/icons/hicolor/48x48/mimetypes/*
%{_datadir}/icons/hicolor/64x64/mimetypes/*
%{_datadir}/icons/hicolor/72x72/mimetypes/*
%{_datadir}/icons/hicolor/96x96/mimetypes/*
%{_datadir}/icons/hicolor/128x128/mimetypes/*
%{_datadir}/icons/hicolor/scalable/mimetypes/*
%{_datadir}/icons/hicolor/256x256/mimetypes/*


%files libs
%license COPYING
%doc README COPYRIGHT NEWS
%{_libdir}/libdjvulibre.so.21*


%files devel
%doc doc/
%{_includedir}/libdjvu/
%{_libdir}/pkgconfig/ddjvuapi.pc
%{_libdir}/libdjvulibre.so


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.28-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.28-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 04 2024 Xavier Bachelot <xavier@bachelot.org> - 3.5.28-12
- Do not BuildRequires: inkscape on EL10
- Sort BuildRequires:
- Use %%make_build, %%make_install and %%license macros
- Improve %%files section

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 3.5.28-11
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.28-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue May 07 2024 Marek Kasik <mkasik@redhat.com> - 3.5.28-9
- Check for zero-size image when allocating GBuffer
- Resolves: #2234738

* Tue May 07 2024 Marek Kasik <mkasik@redhat.com> - 3.5.28-8
- Improve image size fix
- Resolves: #2234741

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Marek Kasik <mkasik@redhat.com> - 3.5.28-1
- Rebase to 3.5.28

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.27-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 02 2021 Marek Kasik <mkasik@redhat.com> - 3.5.27-30
- Improve previous commit
- Resolves: #1977428

* Fri Jul 02 2021 Marek Kasik <mkasik@redhat.com> - 3.5.27-29
- Fix out-of-bounds write in djvutext
- Resolves: #1977428

* Mon May 03 2021 Marek Kasik <mkasik@redhat.com> - 3.5.27-28
- Avoid unsigned short overflow in GBitmap when allocating row buffer
- Resolves: #1943424

* Mon May 03 2021 Marek Kasik <mkasik@redhat.com> - 3.5.27-27
- Avoid stack overflow in DjVuPort by remembering which file we are opening
- Resolves: #1943411, #1943685

* Mon May 03 2021 Marek Kasik <mkasik@redhat.com> - 3.5.27-26
- Check input pool for NULL
- Resolves: #1943410

* Mon May 03 2021 Marek Kasik <mkasik@redhat.com> - 3.5.27-25
- Avoid integer overflow when allocating bitmap
- Resolves: #1943409

* Mon May 03 2021 Marek Kasik <mkasik@redhat.com> - 3.5.27-24
- Check image size for 0
- Resolves: #1943408

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.27-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 04 2020 Marek Kasik <mkasik@redhat.com> - 3.5.27-22
- Fix exporting of djvu icons with Inkscape
- Resolves: #1863428

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.27-21
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.27-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.27-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 22 2019 Marek Kasik <mkasik@redhat.com> - 3.5.27-18
- Fix a NULL pointer dereference in DJVU::filter_fv()
- Resolves: #1771267

* Fri Nov  8 2019 Marek Kasik <mkasik@redhat.com> - 3.5.27-17
- Use Inkscape's "--export-file" option replacing "--export-png"
- Related: #1767921

* Thu Nov  7 2019 Marek Kasik <mkasik@redhat.com> - 3.5.27-16
- Fix a crash due to missing zero-bytes check
- Resolves: #1767921

* Thu Nov  7 2019 Marek Kasik <mkasik@redhat.com> - 3.5.27-15
- Fix a stack overflow
- Resolves: #1767868

* Wed Nov  6 2019 Marek Kasik <mkasik@redhat.com> - 3.5.27-14
- Break an infinite loop
- Resolves: #1767857

* Wed Nov  6 2019 Marek Kasik <mkasik@redhat.com> - 3.5.27-13
- Fix a buffer overflow
- Resolves: #1767842

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.27-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.27-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Marek Kasik <mkasik@redhat.com> - 3.5.27-10
- Add BuildRequires of gcc-c++
- Resolves: #1603796

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.27-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 14 2018 Marek Kasik <mkasik@redhat.com> - 3.5.27-8
- Remove XML file defining DjVu MIME type because it does not differentiate
- between DjVu Image and DjVu Document (the default one in shared-mime-info does)
- Resolves: #1513188

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.5.27-7
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.5.27-5
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Mar 28 2016 François Cami <fcami@fedoraproject.org> - 3.5.27-1
- Update to latest upstream.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.25.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.25.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.5.25.3-16
- Rebuilt for GCC 5 C++11 ABI change

* Fri Jan 09 2015 François Cami <fcami@fedoraproject.org> - 3.5.25.3-15
- Fix bogus date in changelog + use PIC.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.25.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.25.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May  5 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.5.25.3-12
- Remove autoconf requirement, it's not needed even for aarch64
  it's handled in the %%configure macro

* Tue Dec 17 2013 Jonathan Underwood <jonathan.underwood@gmail.com> - 3.5.25.3-11
- Only call autoreconf for Fedora 19 and higher, and not RHEL

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.25.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 23 2013 François Cami <fcami@fedoraproject.org> - - 3.5.25.3-9
- Fix #729469 again.

* Thu May 23 2013 François Cami <fcami@fedoraproject.org> - - 3.5.25.3-8
- Add autoreconf to BuildRequires.

* Thu May 23 2013 François Cami <fcami@fedoraproject.org> - - 3.5.25.3-7
- Call autoreconf in %%build (#925264).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.25.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 31 2013 François Cami <fcami@fedoraproject.org> - 3.5.25.3-5
- fix source URL (#905953).

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 3.5.25.3-4
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 3.5.25.3-3
- rebuild against new libjpeg

* Tue Oct  9 2012 Ville Skyttä <ville.skytta@iki.fi> - 3.5.25.3-2
- Build with $RPM_OPT_FLAGS (#729469).

* Wed Oct  3 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 3.5.25.3-1
- Update to version 3.5.25.3
- Add BuildRequires for inkscape

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May  8 2012 Jonathan G. Underwood <rpmb@mia.theory.phys.ucl.ac.uk> - 3.5.24-4
- Properly remove the djview3 menu entries
- Correctly package the icon files

* Sat May  5 2012 Jonathan G. Underwood <rpmb@mia.theory.phys.ucl.ac.uk> - 3.5.24-4
- Merge in changes from Fedora master branch to el6 branch to bring version 3.5.24
- Unregister djview3 menu/desktop entry on install if present
- Replace BuildRequire for libjpeg-turbo-devel with libjpeg-devel
  depending on fedora/rhel version

* Fri Feb 17 2012 Orion Poplawski <orion@cora.nwra.com> - 3.5.24-3
- Don't call register-djview-menu since we don't build djview3 anymore (bug 734856)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug  8 2011 Peter Robinson <pbrobinson@gmail.com> 3.5.24-1
- 3.5.24
- Obsolete mozplugin, dropped upstream
- Dropped djview3, use djview4

* Mon Jan 31 2011 Karsten Hopp <karsten@redhat.com> 3.5.22-2
- add include cstddefs for size_t

* Mon Nov 30 2009 Ralesh Pandit  <rakesh@fedoraproject.org> 3.5.22-1
- Updated to 3.5.22 (#542221) (Spec patch by Michal Schmidt)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Rakesh Pandit <rakesh@fedoraproject.org> 3.5.21-1
- Updated to 3.5.21

* Fri Jun 06 2008 Dennis Gilmore <dennis@ausil.us> 3.5.20-3
- BR qt3-devel

* Sun Feb  3 2008 Matthias Saou <http://freshrpms.net/> 3.5.20-2
- Update to 3.5.20-2 (#431025).
- Split off a -libs sub-package (#391201).
- Split off a -mozplugin sub-package.

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 3.5.19-4
- Rebuild for new BuildID feature.

* Mon Aug  6 2007 Matthias Saou <http://freshrpms.net/> 3.5.19-3
- Update License field.

* Mon Jun 11 2007 Matthias Saou <http://freshrpms.net/> 3.5.19-2
- Include patch to remove LC_CTYPE for ja man pages, fixes sed 100% CPU issue.

* Fri Jun  8 2007 Matthias Saou <http://freshrpms.net/> 3.5.19-1
- Update to 3.5.19.
- Disable rpath on 64bit... not.
- Convert ja man pages to UTF-8.

* Tue Feb 13 2007 Matthias Saou <http://freshrpms.net/> 3.5.18-2
- Include man page patch to have man pages be identical across archs (#228359).

* Mon Feb  5 2007 Matthias Saou <http://freshrpms.net/> 3.5.18-1
- Update to 3.5.18.
- Remove no longer needed /usr/include/qt3 replacing.
- Replace desktop build requirements and scriplets with new xdg utils way.
- Include new de and fr man page translations... not! Directories are empty.
- Split -devel sub-package, as the new djview4 should build require it.
- No longer build require a web browser, the plugin always gets built now.

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 3.5.17-2
- FC6 rebuild.
- Use mozilla up to FC5, and seamonkey for FC6+ and non-Fedora.
- Build require gnome-mime-data to get build time detected dirs in place.

* Sun Jul  2 2006 Matthias Saou <http://freshrpms.net/> 3.5.17-1
- Update to 3.5.17.

* Tue Mar 14 2006 Matthias Saou <http://freshrpms.net/> 3.5.16-3
- Update to CVS snapshot, fixes the build with gcc 4.1 (sf.net #1420522).. NOT!
- Include workaround for wrong qt3 includes in gui/djview/Makefile.dep.
- Add new pkgconfig ddjvuapi.pc file.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 3.5.16-2
- FC5 rebuild... nope.

* Mon Jan 30 2006 Matthias Saou <http://freshrpms.net/> 3.5.16-1
- Update to 3.5.16.
- Add conditional to build with/without modular X depending on FC version.
- Remove no longer needed gcc4 patch.
- Add extra qualification patch.

* Thu Aug  4 2005 Matthias Saou <http://freshrpms.net/> 3.5.15-2
- Include djvulibre-3.5.15-gcc401.patch to fix compilation with gcc 4.0.1.
- Add hicolor-icon-theme build req for /usr/share/icons/hicolor/48x48/mimetypes
  to exist.

* Thu Aug  4 2005 Matthias Saou <http://freshrpms.net/> 3.5.15-1
- Update to 3.5.15.
- Move desktop icon to datadir/icons/hicolor.
- Add gtk-update-icon-cache calls for the new icon.
- Move browser plugin from netscape to mozilla directory instead of symlinking.
- Clean build requirements and add libtiff-devel.
- Add redhat-menus build req since it owns /etc/xdg/menus/applications.menu,
  which the configure script checks to install the desktop file.
- Add OPTS to the make line (#156208 - Michael Schwendt).

* Tue May  3 2005 David Woodhouse <dwmw2@infradead.org> 3.5.14-6
- Remove files that were installed only for older KDE versions.

* Mon Feb 14 2005 David Woodhouse <dwmw2@infradead.org> 3.5.14-4
- Include %%{_datadir}/mimelnk/image/x-djvu.desktop

* Tue Nov 16 2004 Matthias Saou <http://freshrpms.net/> 3.5.14-3
- Bump release to provide Extras upgrade path.

* Fri Nov  5 2004 Matthias Saou <http://freshrpms.net/> 3.5.14-2
- Re-enable the lib/mozilla/ symlink to the plugin.
- Add source of /etc/profile.d/qt.sh to fix weird detection problem on FC3...
  ...doesn't fix it, some lib required by qt is probably installed after and
  ldconfig not run.
- Added lib +x chmod'ing to get proper stripping and debuginfo package.

* Sat Oct 16 2004 Matthias Saou <http://freshrpms.net/> 3.5.14-2
- Added update-desktop-database scriplet calls.

* Mon Aug 16 2004 Matthias Saou <http://freshrpms.net/> 3.5.14-1
- Update to 3.5.14.
- Added newly introduced files to the package.

* Mon May 17 2004 Matthias Saou <http://freshrpms.net/> 3.5.13-1
- Update to 3.5.13.
- Added new Japanese man pages.

* Wed May  5 2004 Matthias Saou <http://freshrpms.net/> 3.5.12-4
- Changed the plugin directory for mozilla to %%{_libdir}/mozilla,
  as suggested by Matteo Corti.
- Shortened the description.

* Wed Jan 14 2004 Matthias Saou <http://freshrpms.net/> 3.5.12-3
- Added XFree86-devel and libjpeg-devel build requirements.

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 3.5.12-2
- Rebuild for Fedora Core 1.

* Mon Sep  1 2003 Matthias Saou <http://freshrpms.net/>
- Update to 3.5.12.

* Thu May  1 2003 Matthias Saou <http://freshrpms.net/>
- Update to 3.5.11.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.

* Thu Mar 20 2003 Matthias Saou <http://freshrpms.net/>
- Update to 3.5.10.

* Wed Jul 24 2002 Matthias Saou <http://freshrpms.net/>
- Update to 3.5.7.

* Fri Jul 19 2002 Matthias Saou <http://freshrpms.net/>
- Spec file cleanup and fixes.

* Wed May 29 2002 Leon Bottou <leon@bottou.org>
- bumped to version 3.5.6-1

* Mon Apr 1 2002 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.5-2
- changed group to Applications/Publishing

* Mon Mar 25 2002 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.5-2

* Tue Jan 22 2002 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.4-1.
- fixed for properly locating the man directory.
- bumped to version 3.5.4-2.

* Wed Jan 16 2002 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.3-1

* Fri Dec  7 2001 Leon Bottou <leonb@users.sourceforge.net>
- bumped to version 3.5.2-1.

* Wed Dec  5 2001 Leon Bottou <leonb@users.sourceforge.net>
- created spec file for rh7.x.

