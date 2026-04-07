# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Drop this when EL7 is EOL
%{!?ruby_vendorlibdir: %global ruby_vendorlibdir %(ruby -r rbconfig -e 'print RbConfig::CONFIG["vendorlibdir"]')}
%{!?ruby_vendorarchdir: %global ruby_vendorarchdir %(ruby -r rbconfig -e 'print RbConfig::CONFIG["vendorarchdir"]')}

%if 0%{?el9}
%bcond_with    gl
%else
%bcond_without gl
%endif

%if 0%{?fedora} >= 40 || 0%{?rhel} > 9
%bcond_with    ruby
%else
%bcond_without ruby
%endif

%define beta beta20

Summary: Library for Colour AsCii Art, text mode graphics
Name: libcaca
Version: 0.99
Release: 0.80.%{beta}%{?dist}
License: WTFPL
URL: http://caca.zoy.org/wiki/libcaca

Source0: https://github.com/cacalabs/libcaca/releases/download/v%{version}.%{beta}/%{name}-%{version}.%{beta}.tar.bz2
Patch0: libcaca-0.99.beta16-multilib.patch
Patch1: libcaca-0.99.beta20-c99.patch
# https://github.com/cacalabs/libcaca/pull/66
Patch2: libcaca-0.99.beta20-CVE-2022-0856.patch

Buildrequires: doxygen
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: slang-devel
BuildRequires: libX11-devel
BuildRequires: ncurses-devel
BuildRequires: pkgconfig(imlib2)
BuildRequires: pkgconfig(pangoft2)
BuildRequires: python3-devel
BuildRequires: python3-setuptools
%if %{with ruby}
BuildRequires: ruby
BuildRequires: ruby-devel
%endif
Buildrequires: texlive-dvips
Buildrequires: texlive-latex
%if %{with gl}
BuildRequires: freeglut-devel
BuildRequires: mesa-libGLU-devel
%endif

%description
libcaca is the Colour AsCii Art library. It provides high level functions for
color text drawing, simple primitives for line, polygon and ellipse drawing, as
well as powerful image to text conversion routines.

%package devel
Summary: Development files for libcaca, the library for Colour AsCii Art
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: imlib2-devel
Requires: libX11-devel
Requires: ncurses-devel
Requires: pango-devel
Requires: slang-devel
%if %{with gl}
Requires: freeglut-devel
Requires: mesa-libGLU-devel
%endif

%description devel
libcaca is the Colour AsCii Art library. It provides high level functions for
color text drawing, simple primitives for line, polygon and ellipse drawing, as
well as powerful image to text conversion routines.

This package contains the header files needed to compile applications or shared
objects that use libcaca.


%package -n caca-utils
Summary: Colour AsCii Art Text mode graphics utilities based on libcaca
Requires: toilet

%description -n caca-utils
This package contains utilities and demonstration programs for libcaca, the
Colour AsCii Art library.

cacaview is a simple image viewer for the terminal. It opens most image formats
such as JPEG, PNG, GIF etc. and renders them on the terminal using ASCII art.
The user can zoom and scroll the image, set the dithering method or enable
anti-aliasing.

cacaball is a tiny graphic program that renders animated ASCII metaballs on the
screen, cacafire is a port of AALib's aafire and displays burning ASCII art
flames, and cacademo is a simple application that shows the libcaca rendering
features such as line and ellipses drawing, triangle filling and sprite
blitting.


%package -n python3-caca
Summary: Python bindings for libcaca

%description -n python3-caca
This package contains the python bindings for using libcaca from python.


%if %{with ruby}
%package -n ruby-caca
Summary: Ruby bindings for libcaca
Requires: ruby(release)
Provides: ruby(caca) = %{version}-%{release}

%description -n ruby-caca
This package contains the ruby bindings for using libcaca from ruby.
%endif


%prep
%autosetup -p1 -n libcaca-%{version}.%{beta}

for file in python/examples/*.py; do
  sed -e 's|/usr/bin/env python$|%{__python3}|g' ${file} > ${file}.tmp
  touch -r ${file} ${file}.tmp
  mv -f ${file}.tmp ${file}
done

%build
# This package has a configure test which uses ASMs, but does not link the
# resultant .o files.  As such the ASM test is always successful, even on
# architectures were the ASM is not valid when compiling with LTO.
#
# -ffat-lto-objects is sufficient to address this issue.  It is the default
# for F33, but is expected to only be enabled for packages that need it in
# F34, so we use it here explicitly
%define _lto_cflags -flto=auto -ffat-lto-objects

export LDFLAGS="$(pkg-config --libs gio-2.0) $LDFLAGS"

sed -i -e 's/sitearchdir/vendorarchdir/g' -e 's/sitelibdir/vendorlibdir/g' configure

%configure \
  --disable-static \
  --disable-csharp \
  --disable-java

%make_build


%install
%make_install
find %{buildroot} -name "*.la" -delete

# We want to include the docs ourselves from the source directory
mv %{buildroot}%{_docdir}/libcaca-dev libcaca-dev-docs


# Drop this when EL7 is EOL
%{?ldconfig_scriptlets}


%files
%license COPYING
%{_libdir}/*.so.0*

%files devel
%doc libcaca-dev-docs/html/
%{_bindir}/caca-config
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_mandir}/man1/caca-config.1*
%{_mandir}/man3/*

%files -n caca-utils
%license COPYING*
%doc AUTHORS NEWS NOTES README THANKS
%{_bindir}/cacaclock
%{_bindir}/cacademo
%{_bindir}/cacafire
%{_bindir}/cacaplay
%{_bindir}/cacaserver
%{_bindir}/cacaview
%{_bindir}/img2txt
%{_datadir}/libcaca/
%{_mandir}/man1/cacademo.1*
%{_mandir}/man1/cacafire.1*
%{_mandir}/man1/cacaplay.1*
%{_mandir}/man1/cacaserver.1*
%{_mandir}/man1/cacaview.1*
%{_mandir}/man1/img2txt.1*

%files -n python3-caca
%doc python/examples
%{python3_sitelib}/caca/

%if %{with ruby}
%files -n ruby-caca
%doc ruby/README
%{ruby_vendorlibdir}/caca.rb
%{ruby_vendorarchdir}/caca.so
%endif


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.99-0.80.beta20
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.99-0.79.beta20
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.78.beta20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.99-0.77.beta20
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.76.beta20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.75.beta20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.99-0.74.beta20
- Rebuilt for Python 3.13

* Wed Mar 20 2024 Xavier Bachelot <xavier@bachelot.org> - 0.99-0.73.beta20
- Disable ruby bindings on F40+ (workaround RHBZ#2261303)
- Disable ruby bindings on eln

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.72.beta20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.71.beta20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.99-0.70.beta20
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.3

* Sun Sep 24 2023 Xavier Bachelot <xavier@bachelot.org> - 0.99-0.69.beta20
- Fix CVE-2022-0856 (RHBZ#2081750)
- Add missing Requires: for caca-utils (RHBZ#1701685)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.68.beta20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.99-0.67.beta20
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Leigh Scott <leigh123linux@gmail.com> - 0.99-0.66.beta20
- Rebuild fo new imlib2

* Fri Jan 20 2023 Peter Fordham <peter.fordham@gmail.com> - 0.99-0.65.beta20
- Port code to C99.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.64.beta20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.99-0.63.beta20
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_3.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.62.beta20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.99-0.61.beta20
- Rebuilt for Python 3.11

* Tue Mar 15 2022 Xavier Bachelot <xavier@bachelot.org> - 0.99-0.60.beta20
- Spec cleanup
- Disable GL support on EL9

* Mon Mar 14 2022 Simone Caronni <negativo17@gmail.com> - 0.99-0.59.beta20
- Clean up SPEC file.

* Wed Jan 26 2022 Vít Ondruch <vondruch@redhat.com> - 0.99-0.58.beta20
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_3.1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.57.beta20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 08 2021 Xavier Bachelot <xaver@bachelot.org> - 0.99-0.56.beta20
- Update to 0.99.beta20. Fixes :
  - CVE-2018-20544, CVE-2018-20545, CVE-2018-20546, CVE-2018-20547,
    CVE-2018-20548, CVE-2018-20549 (RHBZ#1687860)
  - CVE-2021-3410 (RHBZ#1928437)
  - CVE-2021-30498 (RHBZ#1948676, RHBZ#1948677)
  - CVE-2021-30499 (RHBZ#1948680, RHBZ#1948681)
- Update Source0 to github
- Don't glob soname to avoid spurious bump
- Fix bogus date in changelog

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.55.beta19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.99-0.54.beta19
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.53.beta19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.99-0.52.beta19
- F-34: rebuild against ruby 3.0

* Fri Aug 21 2020 Jeff Law <aw@redhat.com> - 0.99-0.51.beta19
- Re-enable LTO

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.50.beta19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Jeff Law <aw@redhat.com> - 0.99-0.49.beta19
- Disable LTO

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.99-0.48.beta19
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.47.beta19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.99-0.46.beta19
- F-32: rebuild against ruby27

* Fri Oct 04 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.99-0.45.beta19
- Rebuilt for new freeglut

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.99-0.44.beta19
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.99-0.43.beta19
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.42.beta19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.41.beta19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Matthias Saou <matthias@saou.eu> 0.99-0.40.beta19
- Update tetex to texlive in BR.
- Re-add python sub-package, but python3 (#1323249).

* Mon Jan 21 2019 Vít Ondruch <vondruch@redhat.com> - 0.99-0.39.beta19
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.6

* Thu Jan 10 2019 Miro Hrončok <mhroncok@redhat.com> - 0.99-0.38.beta19
- Remove Python 2 subpackage

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.37.beta19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.36.beta19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.99-0.35.beta19
- F-28: rebuild for ruby25

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.99-0.34.beta19
- Python 2 binary package renamed to python2-caca
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.33.beta19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.32.beta19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.31.beta19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Vít Ondruch <vondruch@redhat.com> - 0.99-0.30.beta19
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.4

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.29.beta19
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.99-0.28.beta19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Vít Ondruch <vondruch@redhat.com> - 0.99-0.27.beta19
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.3

* Mon Nov  9 2015 Matthias Saou <matthias@saou.eu> 0.99-0.26.beta19
- Update to 0.99.beta19.
- Remove upstreamed ruby patch, fixed in November 2012 (commit 36990e1).

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.25.beta18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.99-0.24.beta18
- Rebuilt for GCC 5 C++11 ABI change

* Sat Jan 17 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.99-0.23.beta18
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.22.beta18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.21.beta18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Vít Ondruch <vondruch@redhat.com> - 0.99-0.20.beta18
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Tue Mar 11 2014 Matthias Saou <matthias@saou.eu> 0.99-0.19.beta18
- Update to 0.99.beta18 (#1062632).
- Add python-caca sub-package with python bindings.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.18.beta17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 19 2013 Vít Ondruch <vondruch@redhat.com> - 0.99-0.17.beta17
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.16.beta17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.15.beta17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 29 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.99-0.14.beta17
- Rebuilt and patched for Ruby 1.9.3.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.13.beta17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 11 2011 Matthias Saou <http://freshrpms.net/> 0.99-0.12.beta17
- Explicitly disable building csharp and java bindings (#671206).

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.11.beta17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Apr 28 2010 Matthias Saou <http://freshrpms.net/> 0.99-0.10.beta17
- Update to 0.99.0beta17.
- Update spec file URLs.
- Switch to using DESTDIR for install, which is the preferred method.
- Remove the static library (#556062).
- Remove no longer needed libGLU patch.
- Enable new ruby bindings.
- Leave C# and Java disabled, I hope no one will ever ask to have them enabled.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-0.9.beta16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 11 2009 Matthias Saou <http://freshrpms.net/> 0.99-0.8.beta16
- Fix build now that glut no longer links against libGLU (#502296).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 21 2008 Matthias Saou <http://freshrpms.net/> 0.99-0.6.beta16
- Add patch to share the same caca-config for 32 and 64bit (#341951).
- Don't include the pdf devel doc, only html (again, fixed multilib conflict).

* Mon Oct 27 2008 Matthias Saou <http://freshrpms.net/> 0.99-0.5.beta16
- Update to 0.99beta16.
- Update Source URL.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.99-0.4.beta11
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 0.99-0.3.beta11
- Rebuild for new BuildID feature.

* Mon Aug  6 2007 Matthias Saou <http://freshrpms.net/> 0.99-0.2.beta11
- Update License field.

* Thu Mar 29 2007 Matthias Saou <http://freshrpms.net/> 0.99-0.1.beta11
- Update to 0.99beta11.
- We now have a main libcaca package with just the shared lib (built by default
  now), so make the devel sub-package require it too. Leave static lib for now.
- Enable opengl and pango support.
- Remove useless rpath.
- Remove no longer needed man3 patch.
- Remove all configure options, they're autodetected.

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 0.9-11
- FC6 rebuild.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 0.9-10
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 0.9-9
- Rebuild for new gcc/glibc.

* Mon Jan  2 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.9-8
- Include unpackaged man page symlinks.
- Rebuild against new slang.

* Thu Nov 17 2005 Matthias Saou <http://freshrpms.net/> 0.9-7
- Change XFree86-devel requirements to libX11-devel.
- Force --x-includes= and --x-libraries=, otherwise -L gets passed empty.

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.9-6
- Include libcaca datadir.

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 0.9-5
- Bump release to provide Extras upgrade path.

* Wed Nov  3 2004 Matthias Saou <http://freshrpms.net/> 0.9-4
- Disable man3 pages, they don't build on FC3, this needs fixing.
- Fix to not get the debuginfo files go into the devel package.

* Wed May 19 2004 Matthias Saou <http://freshrpms.net/> 0.9-3
- Rebuild for Fedora Core 2.

* Tue Feb 24 2004 Matthias Saou <http://freshrpms.net/> 0.9-2
- Fix License tag from GPL to LGPL.

* Mon Feb  9 2004 Matthias Saou <http://freshrpms.net/> 0.9-1
- Update to 0.9.
- Added cacamoir and cacaplas.

* Fri Jan  9 2004 Matthias Saou <http://freshrpms.net/> 0.7-1
- Spec file cleanup for Fedora Core 1.

* Wed Jan 7 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.7-1
- new release

* Sun Jan 4 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.6-2
- install documentation into {doc}/package-version instead of {doc}/package
- added tetex-dvips to the build dependencies

* Sat Jan 3 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.6-1
- new release
- more detailed descriptions
- split the RPM into libcaca-devel and caca-utils
- packages are rpmlint clean

* Mon Dec 29 2003 Richard Zidlicky <rz@linux-m68k.org> 0.5-1
- created specfile

