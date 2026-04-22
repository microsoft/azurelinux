# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: SDL graphics drawing primitives and other support functions
Name: SDL_gfx
Version: 2.0.27
Release: 7%{?dist}
License: Zlib
URL: http://www.ferzkopp.net/Software/SDL_gfx-2.0/
Source: http://www.ferzkopp.net/Software/SDL_gfx-2.0/SDL_gfx-%{version}.tar.gz
Patch0: SDL_gfx-2.0.13-ppc.patch
BuildRequires: make
BuildRequires:  gcc
BuildRequires: SDL-devel
BuildRequires: libXt-devel

%description
Library providing SDL graphics drawing primitives and other support functions
wrapped up in an addon library for the Simple Direct Media (SDL) cross-platform
API layer.


%package devel
Summary: Development files for SDL_gfx
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: SDL-devel

%description devel
This package contains the files required to develop programs which use SDL_gfx.


%prep
%setup -q
%patch -P 0 -p1 -b .ppc


%build
%configure \
%ifnarch %{ix86} x86_64
    --disable-mmx \
%endif
    --disable-static
make %{?_smp_mflags}


%install
%make_install


%ldconfig_scriptlets


%files
%doc LICENSE README AUTHORS COPYING
%{_libdir}/*.so.*

%files devel
%{_includedir}/SDL/*.h
%exclude %{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.0.27-1
- 2.0.27

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.26-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Mar 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 2.0.26-9
- migrated to SPDX license

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.26-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.26-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 05 2020 Gwyn Ciesla <gwync@protonmail.com> = 2.0.26-1
- 2.0.26

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Hans de Goede <hdegoede@redhat.com> - 2.0.25-1
- Update to 2.0.25 (related rhbz#1106197)

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 09 2013 Lubomir Rintel <lkundrak@v3.sk> - 2.0.24-1
- Bump version

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 13 2011 Matthias Saou <http://freshrpms.net/> 2.0.22-1
- Update to 2.0.22.
- Include new pkgconfig file.
- Update descriptions and summaries.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Matthias Saou <http://freshrpms.net/> 2.0.17-1
- Update to 2.0.17.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Matthias Saou <http://freshrpms.net/> 2.0.16-4
- Rebuild for new BuildID feature.

* Fri Aug  3 2007 Matthias Saou <http://freshrpms.net/> 2.0.16-3
- Update License field.

* Tue Jun 19 2007 Matthias Saou <http://freshrpms.net/> 2.0.16-2
- Minor cleanups.

* Mon May  7 2007 Matthias Saou <http://freshrpms.net/> 2.0.16-1
- Update to 2.0.16.
- Remove no longer needed semicolon patch.
- Add libXt-devel BR to make configure happy (seems unused, though).
- Remove no longer needed autotools BR.

* Mon May  7 2007 Matthias Saou <http://freshrpms.net/> 2.0.13-8
- Include ppc patch (#239130, Bill Nottingham).
- Too late to update to 2.0.16 for F7 (freeze, and soname change).

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 2.0.13-7
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Matthias Saou <http://freshrpms.net/> 2.0.13-6
- Fix semicolons in header files (#207665).

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 2.0.13-5
- FC6 rebuild.
- Remove gcc-c++ and perl build requirements, they're defaults.
- Add release to the devel sub-package requirement.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 2.0.13-4
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 2.0.13-3
- Rebuild for new gcc/glibc.
- Update URLs.
- Exclude the static library.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Jan 28 2005 Matthias Saou <http://freshrpms.net/> 2.0.13-1
- Initial Extras import, minor spec tweaks.

* Tue Dec 21 2004 Dries Verachtert <dries@ulyssis.org> 2.0.13-1
- Updated to release 2.0.13 and removed the patch (has been
  applied upstream)

* Thu Nov 11 2004 Matthias Saou <http://freshrpms.net/> 2.0.12-3
- Explicitly disable mmx for non-ix86 to fix build on x86_64.

* Fri Oct 22 2004 Dries Verachtert <dries@ulyssis.org> 2.0.12-3
- fixed some buildrequirements so the correct version of libSDL_gfx.so
  can be found in the list of provides.

* Fri Oct 22 2004 Dries Verachtert <dries@ulyssis.org> 2.0.12-2
- rebuild

* Wed Sep 01 2004 Dries Verachtert <dries@ulyssis.org> 2.0.12-1
- Update to version 2.0.12.

* Mon Apr 26 2004 Dries Verachtert <dries@ulyssis.org> 2.0.10-1
- Initial package
