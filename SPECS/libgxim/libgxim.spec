Summary:        GObject-based XIM protocol library
Name:           libgxim
Version:        0.5.0
Release:        20%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://tagoh.bitbucket.org/libgxim/
Source0:        https://bitbucket.org/tagoh/%{name}/downloads/%{name}-%{version}.tar.bz2
Patch0:         %{name}-fix-build.patch
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glib2-devel >= 2.26
BuildRequires:  gtk2-devel
BuildRequires:  intltool
BuildRequires:  ruby
BuildRequires:  rubygems

%description
libgxim is a X Input Method protocol library that is implemented by GObject.
this library helps you to implement XIM servers or client applications to
communicate through XIM protocol without using Xlib API directly, particularly
if your application uses GObject-based main loop.

This package contains the shared library.

%package        devel
Summary:        Development files for libgxim
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel >= 2.26.0
Requires:       gtk2-devel
Requires:       pkg-config

%description	devel
libgxim is a X Input Method protocol library that is implemented by GObject.
this library helps you to implement XIM servers or client applications to
communicate through XIM protocol without using Xlib API directly, particularly
if your application uses GObject-based main loop.

This package contains the development files to make any applications with
libgxim.

%prep
%autosetup -p1


%build
%configure --disable-static --disable-rebuilds
%make_build


%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%doc AUTHORS ChangeLog README
%license COPYING
%{_libdir}/libgxim.so.*

%files devel
%doc AUTHORS ChangeLog README
%license COPYING
%{_libdir}/libgxim.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/libgxim
%{_datadir}/gtk-doc/html/libgxim

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.5.0-20
- License verified
- Lint spec

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.0-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Akira TAGOH <tagoh@redhat.com> - 0.5.0-14
- Use ldconfig rpm macro.

* Mon Feb 19 2018 Akira TAGOH <tagoh@redhat.com> - 0.5.0-13
- Add BR: gcc

* Wed Feb 14 2018 Akira TAGOH <tagoh@redhat.com> - 0.5.0-12
- Fix the build fail.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 13 2017 Akira TAGOH <tagoh@redhat.com> - 0.5.0-8
- Add rubygems to BR.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb  8 2013 Akira TAGOH <tagoh@redhat.com> - 0.5.0-1
- New upstream release.

* Fri Nov 23 2012 Akira TAGOH <tagoh@redhat.com> - 0.4.0-1
- New upstream release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.3.3-5
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr  3 2009 Akira TAGOH <tagoh@redhat.com> - 0.3.3-2
- Fix an error message about FontSet.

* Thu Apr  2 2009 Akira TAGOH <tagoh@redhat.com> - 0.3.3-1
- New upstream release.
  - partly including a fix of freeze issue with switching (#488877)

* Tue Mar  3 2009 Akira TAGOH <tagoh@redhat.com> - 0.3.2-4
- Fix destroying a window unexpectedly. (#488223)

* Mon Mar  2 2009 Akira TAGOH <tagoh@redhat.com> - 0.3.2-3
- Backport a patch to fix the unknown event issue.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 13 2009 Akira TAGOH <tagoh@redhat.com> - 0.3.2-1
- New upstream release.

* Thu Oct 23 2008 Akira TAGOH <tagoh@redhat.com> - 0.3.1-1
- New upstream release.

* Tue Oct 14 2008 Akira TAGOH <tagoh@redhat.com> - 0.3.0-1
- New upstream release.
  - Have a workaround to avoid the race condition issue. (#452849)
  - Fix a freeze issue with ibus. (#465431)

* Wed Sep 17 2008 Akira TAGOH <tagoh@redhat.com> - 0.2.0-1
- New upstream release.
  - Fix discarding some packets when reconnecting.
  - Fix invalid memory access.

* Fri Aug 29 2008 Akira TAGOH <tagoh@redhat.com> - 0.1.1-1
- New upstream release.

* Thu Aug 28 2008 Akira TAGOH <tagoh@redhat.com> - 0.1.0-2
- clean up the spec file a bit.

* Mon Aug 25 2008 Akira TAGOH <tagoh@redhat.com> - 0.1.0-1
- Initial package.
