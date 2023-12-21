%define xfceversion %(echo %{version} | cut -d. -f1-2)
Summary:        Utility library for the Xfce4 desktop environment
Name:           libxfce4util
Version:        4.19.2
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.xfce.org/
Source0:        https://archive.xfce.org/src/xfce/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  intltool
BuildRequires:  pkg-config
BuildRequires:  vala
BuildRequires:  pkgconfig(glib-2.0) >= 2.24.0

%description
This package includes basic utility non-GUI functions for Xfce4.

%package        devel
Summary:        Developpment tools for libxfce4util library
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel
Requires:       gtk2-devel
Requires:       pkg-config

%description devel
This package includes static libraries and header files for the
libxfce4util library.

%prep
%autosetup

%build
%configure --disable-static
# Remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
export LD_LIBRARY_PATH="`pwd`/libxfce4util/.libs"
%make_build

%install
%make_install
chmod 755 %{buildroot}/%{_libdir}/*.so
find %{buildroot} -type f -name "*.la" -delete -print

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS
%{_libdir}/lib*.so.*
%{_sbindir}/xfce4-kiosk-query
%{_libdir}/girepository-1.0/Libxfce4util-1.0.typelib
%{_datadir}/gir-1.0/Libxfce4util-1.0.gir
%{_datadir}/vala/vapi/%{name}-1.0.vapi

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/xfce4
%doc %{_datadir}/gtk-doc/

%changelog
* Wed Dec 20 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 4.19.2-1
- Update to v4.19.2

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 4.14.0-5
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Dec 08 2021 Thomas Crain <thcrain@microsoft.com> - 4.14.0-4
- License verified
- Lint spec

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.14.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 12 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.14.0-1
- Update to 4.14.0

* Mon Jul 29 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.13.5-1
- Update to 4.13.5
- Enable vala

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 01 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.13.4-3
- add export ld-path

* Mon Jul 01 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.13.4-2
- Enable gobject instrospection

* Mon Jul 01 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.13.4-1
- Update to 4.13.4

* Thu May 16 2019 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.13.3-1
- Update to 4.13.3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Aug 11 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.13.2-20
- Update to 4.13.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 28 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.12.1-9
- Add BR:gcc-c++

* Sun May 27 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.12.1-8
- Drop gtk-doc building (fixes bug# 1582901)
- Modernize spec

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 28 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.12.1-1
- Update to 4.12.1
- Fixes permissions problems in installing libraries
- Fixes xfce_version_string 

* Sat Feb 28 2015 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 4.12.0-1
- Update to stable release 4.12.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 05 2013 Kevin Fenzi <kevin@scrye.com> 4.10.1-1
- Update to 4.10.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 4.10.0 final
- Make build verbose
- Add VCS key

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.1-1
- Update to 4.9.1 (Xfce 4.10pre2)

* Sun Apr 01 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.0-1
- Update to 4.9.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 12 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.2-1
- Update to 4.8.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.1-1
- Update to 4.8.1

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0 final 

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.5-1
- Update to 4.7.5

* Fri Dec 03 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.4-1
- Update to 4.7.4

* Sun Nov 07 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.3-1
- Update to 4.7.3

* Sun Sep 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.2-1
- Update to 4.7.2

* Mon Aug 23 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.2-2
- Remove unneeded gtk-doc dep. Fixes bug #604400

* Fri May 21 2010 Kevin Fenzi <kevin@tummy.com> - 4.6.2-1
- Update to 4.6.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 19 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.1-1
- Update to 4.6.1

* Mon Mar 02 2009 Christoph Wickert <cwickert@fedoraproject.org> - 4.6.0-2
- Make devel package require pkgconfig and gtk-doc
- Mark gtk-doc files as %%doc

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.6.0-1
- Update to 4.6.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.99.1-1
- Update to 4.5.99.1

* Tue Jan 13 2009 Kevin Fenzi <kevin@tummy.com> - 4.5.93-1
- Update to 4.5.93

* Sun Dec 21 2008 Kevin Fenzi <kevin@tummy.com> - 4.5.92-1
- Update to 4.5.92

* Mon Oct 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 4.4.3-1
- Update to 4.4.3

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 4.4.2-2
- Rebuild for gcc43

* Sun Dec  2 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.2-1
- Update to 4.4.2

* Sun Aug 26 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-3
- Update License tag

* Mon Apr 16 2007 Christoph Wickert <fedora@christoph-wickert.de> - 4.4.1-2
- BuildRequire gettext and include locales

* Wed Apr 11 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.1-1
- Update to 4.4.1

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 4.4.0-1
- Update to 4.4.0

* Thu Nov  9 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.2-1
- Update to 4.3.99.2

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-3
- Fix defattr

* Wed Oct  4 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-2
- Bump release for devel checkin

* Sun Sep  3 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.99.1-1
- Upgrade to 4.4rc1/4.3.99.1
- Remove unneeded PreReq
- Added doc files

* Sun Aug 27 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.2-2
- Make devel package own includedir/xfce4 (fixes #203644)

* Tue Jul 11 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.2-1
- Update to 4.3.90.2

* Thu Apr 27 2006 Kevin Fenzi <kevin@tummy.com> - 4.3.90.1-1
- upgrade to 4.3.90.1

* Thu Feb 16 2006 Kevin Fenzi <kevin@tummy.com> - 4.2.3.2-2.fc5
- Rebuild for fc5

* Wed Nov 16 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3.2-1.fc5
- Update to 4.2.3.2

* Thu Nov 10 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3.1-4.fc5
- bump release for rebuild

* Thu Nov 10 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3.1-3.fc5
- disable-static instead of removing .a files. 
- sync release with FC-4 branch

* Mon Nov  7 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.3.1-1.fc5
- Update to 4.2.3.1
- Added dist tag
- Removed .la files. Fixes bug 172645
- Removed .a files. 

* Tue May 17 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.2-1.fc4
- Update to 4.2.2

* Fri Mar 25 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-3.fc4
- lowercase Release

* Sat Mar 19 2005 Warren Togami <wtogami@redhat.com> - 4.2.1-2
- remove stuff 

* Tue Mar 15 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.1-1
- Updated to 4.2.1 version

* Tue Mar  8 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-3
- Fixed License to be BSD and LGPL
- Fixed case on Xfce

* Sun Mar  6 2005 Kevin Fenzi <kevin@tummy.com> - 4.2.0-2
- Inital Fedora Extras version
- Capitalized first letter of Summary in devel section to quiet rpmlint
- Added LGPL to License as 2 files are under LGPL, the rest BSD

* Sun Jan 23 2005 Than Ngo <than@redhat.com> 4.2.0-1
- update to 4.2.0 release

* Wed Dec 08 2004 Than Ngo <than@redhat.com> 4.1.99.1-1
- update to 4.2 rc1

* Mon Jul 19 2004 Than Ngo <than@redhat.com> 4.0.6-1
- update to 4.0.6
- add requires on glib2-devel, bug #124200
- remove unneeded patch file, which is included in new upstream

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr 15 2004 Than Ngo <than@redhat.com> 4.0.5-1
- update to 4.0.5

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Than Ngo <than@redhat.com> 4.0.3-2
- fixed dependant libraries check on x86_64

* Fri Jan 09 2004 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3

* Thu Dec 25 2003 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2

* Tue Dec 16 2003 Than Ngo <than@redhat.com> 4.0.1-1
- initial build
