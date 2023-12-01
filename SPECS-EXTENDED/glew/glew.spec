Name:           glew
Version:        2.1.0
Release:        7%{?dist}
Summary:        The OpenGL Extension Wrangler Library
License:        BSD and MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://glew.sourceforge.net

Source0:        https://sourceforge.net/projects/glew/files/glew/%{version}/glew-%{version}.tgz
Patch0:         glew-2.1.0-install.patch
BuildRequires:  gcc
BuildRequires:  libGLU-devel

%description
The OpenGL Extension Wrangler Library (GLEW) is a cross-platform C/C++
extension loading library. GLEW provides efficient run-time mechanisms for
determining which OpenGL extensions are supported on the target platform.
OpenGL core and extension functionality is exposed in a single header file.
GLEW is available for a variety of operating systems, including Windows, Linux,
Mac OS X, FreeBSD, Irix, and Solaris.

This package contains the demo GLEW utilities.  The libraries themselves
are in libGLEW.

%package devel
Summary:        Development files for glew
Requires:       libGLEW%{?_isa} = %{version}-%{release}
Requires:       mesa-libGLU-devel%{?_isa}

%description devel
Development files for glew


%package -n libGLEW
Summary:        libGLEW

%description -n libGLEW
libGLEW

%prep
%autosetup -p1

%build
%make_build CFLAGS.EXTRA="$RPM_OPT_FLAGS -fPIC"\
     STRIP= \
     GLEW_PREFIX=%{_prefix} GLEW_DEST=%{_prefix} \
     includedir=%{_includedir} \
     BINDIR=%{_bindir} LIBDIR=%{_libdir} PKGDIR=%{_libdir}/pkgconfig

%install
make install.all DESTDIR="$RPM_BUILD_ROOT" \
     GLEW_PREFIX=%{_prefix} GLEW_DEST=%{_prefix} \
     includedir=%{_includedir} \
     BINDIR=%{_bindir} LIBDIR=%{_libdir} PKGDIR=%{_libdir}/pkgconfig
find $RPM_BUILD_ROOT -type f -name "*.a" -delete
# sigh
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/*.so*

%ldconfig_scriptlets -n libGLEW

%files
%license LICENSE.txt
%{_bindir}/*

%files -n libGLEW
%license LICENSE.txt
%{_libdir}/libGLEW.so.*

%files devel
%{_libdir}/libGLEW.so
%{_libdir}/pkgconfig//glew.pc
%{_includedir}/GL/*.h
%doc doc/*

%changelog
* Thu Jun 17 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.1.0-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove redhat-specific config.guess seeding

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep  6 2018 Owen Taylor <otaylor@redhat.com> - 2.1.0-3
- Fix installation with prefix=/app

* Thu Aug 23 2018 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-2
- Fix mesa-libGLU-devel isnt't arched

* Wed Aug 15 2018 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-1
- Update to 2.1.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.0-5
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 8 2017 Oded Gabbay <oded.gabbay@gmail.com> 2.0.0-1
- glew 2.0.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Adam Jackson <ajax@redhat.com> 1.13.0-1
- glew 1.13.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May  3 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.10.0-3
- Update config.guess for newer arch support
- Modernise spec file

* Mon Nov 18 2013 Dave Airlie <airlied@redhat.com> - 1.10.0-2
- rebuilt for GLEW 1.10

* Sun Nov 17 2013 Dave Airlie <airlied@redhat.com> 1.10.0-1
- glew 1.10.0 + build fix + makefile hacks

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 18 2012 Ville Skyttä <ville.skytta@iki.fi> - 1.9.0-2
- Prevent stripping binaries before rpmbuild does it.

* Thu Dec 13 2012 Adam Jackson <ajax@redhat.com> 1.9.0-1
- glew 1.9.0

* Sun Jul 22 2012 Ville Skyttä <ville.skytta@iki.fi> - 1.7.0-3
- Move/add ldconfig post(un)install scriptlets to appropriate subpackages.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 13 2012 Adam Jackson <ajax@redhat.com> 1.7.0-1
- glew 1.7.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Adam Jackson <ajax@redhat.com> 1.6.0-1
- glew 1.6.0 (#714763)

* Wed Mar 23 2011 Adam Williamson <awilliam@redhat.com> - 1.5.8-3
- instead of taking flags out in makefile.patch and adding them back
  in add-needed.patch, let's just not take them out...

* Wed Mar 23 2011 Adam Jackson <ajax@redhat.com> 1.5.8-2
- glew-1.5.8-glewmx.patch: Install libGLEWmx 0755 so autoprovs work
- Split runtime libraries to their own packages

* Wed Mar 23 2011 Adam Williamson <awilliam@redhat.com> - 1.5.8-1
- bump to 1.5.8
- add soname.patch to fix the internal SONAME of the MX library

* Wed Mar 23 2011 Adam Williamson <awilliam@redhat.com> - 1.5.7-3
- add glewmx.patch (upstream commit 302c224016, always build the
  MX-enabled version of the library as well as non-MX version, under
  a different name)
- revise add-needed.patch to change the LDFLAGS in a better place
  and add -lGLU as well as -lX11

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Dave Airlie <airlied@redhat.com> 1.5.7-1
- glew 1.5.7

* Wed Aug 25 2010 Adam Jackson <ajax@redhat.com> 1.5.5-1
- glew 1.5.5

* Fri Jul 30 2010 Dave Airlie <airlied@redhat.com> 1.5.4-2
- fix glew.pc file as pointed out by David Aguilar

* Sat May 29 2010 Dave Airlie <airlied@redhat.com> 1.5.4-1
- glew 1.5.4 - add glew.pc

* Tue Feb 09 2010 Adam Jackson <ajax@redhat.com> 1.5.2-2
- glew-1.5.2-add-needed.patch: Fix FTBFS from --no-add-needed

* Tue Feb 02 2010 Adam Jackson <ajax@redhat.com> 1.5.2-1
- glew 1.5.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 13 2008 Jochen Schmitt <Jochen herr-schmitt de> - 1.5.1-1
- New upstream release (#469639)
- Fix licenseing issue with developer documentation

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.0-2
- Autorebuild for GCC 4.3

* Mon Jan 21 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5.0-1
- New upstream version, now SGI licensed stuff free out of the box!
- Unfortunately some of the included docs are under a non free license,
  therefor this package is based on a modified tarbal with these files removed

* Sat Jan 12 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-4
- Add missing GL_FLOAT_MATXxX defines

* Sat Aug 18 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-3
- Fix multiple unused direct shlib dependencies in libGLEW.so
- Remove the "SGI Free Software License B" and "GLX Public License" tekst from
  the doc dir in the tarbal
- Patch credits.html to no longer refer to the 2 non free licenses, instead it
  now points to LICENSE-README.fedora
- Put API docs in -devel instead of main package

* Mon Aug  6 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.0-2
- Remove SGI encumbered files to make this ok to go into Fedora
- Replace some removed files with (modified) mesa files
- Regenerate some of the removed files using the mesa replacemenmt files
  and the scripts in the auto directory
- Readd wglew.h, some programs may need this to compile
- Update License tag for new Licensing Guidelines compliance

* Sun May 06 2007 Ian Chapman <packages@amiga-hardware.com> 1.4.0-1%{?dist}
- Updated to 1.4.0

* Sun Mar 04 2007 Ian Chapman <packages@amiga-hardware.com> 1.3.6-1%{?dist}
- Updated to 1.3.6
- Updated pathandstrip patch
- Dropped xlib patch - fixed upstream
- Dropped sed EOL replacements - fixed upstream
- Changed license to GPL

* Fri Dec 01 2006 Ian Chapman <packages@amiga-hardware.com> 1.3.5-1%{?dist}
- Updated to 1.3.5
- Fixed stripping of the binaries
- Reinstate parallel building, no longer appears broken
- Removed FC4 specifics from spec (no longer supported)

* Tue Jun 20 2006 Ian Chapman <packages@amiga-hardware.com> 1.3.4-3%{?dist}
- Added buildrequire macros to determine fc4, fc5, fc6 due to X modularisation

* Sun Jun 04 2006 Ian Chapman <packages@amiga-hardware.com> 1.3.4-2%{?dist}
- Replaced %%{_sed} macro with sed
- Replaced xorg-x11-devel (build)requires with libGLU-devel for compatibility
  with modular / non-modular X
- Replaced source URL to use primary sf site rather than a mirror
- Removed superfluous docs from devel package
- Removed wglew.h, seems to be only useful for windows platforms

* Thu May 11 2006 Ian Chapman <packages@amiga-hardware.com> 1.3.4-1.iss
- Initial Release
