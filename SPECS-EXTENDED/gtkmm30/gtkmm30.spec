Vendor:         Microsoft Corporation
Distribution:   Mariner
%global apiver 3.0
# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

%global atkmm_version 2.24.2
%global cairomm_version 1.12.0
%global gdk_pixbuf2_version 2.35.5
%global glibmm_version 2.49.1
%global gtk3_version 3.22.0
%global pangomm_version 2.38.2

Name:           gtkmm30
Version:        3.24.2
Release:        4%{?dist}
Summary:        C++ interface for the GTK+ library

License:        LGPLv2+
URL:            http://www.gtkmm.org/
Source0:        http://download.gnome.org/sources/gtkmm/%{release_version}/gtkmm-%{version}.tar.xz

BuildRequires:  gcc-c++
BuildRequires:  atkmm-devel >= %{atkmm_version}
BuildRequires:  cairomm-devel >= %{cairomm_version}
BuildRequires:  gdk-pixbuf2-devel >= %{gdk_pixbuf2_version}
BuildRequires:  glibmm-devel >= %{glibmm_version}
BuildRequires:  gtk3-devel >= %{gtk3_version}
BuildRequires:  pangomm-devel >= %{pangomm_version}

Requires:       atkmm%{?_isa} >= %{atkmm_version}
Requires:       cairomm%{?_isa} >= %{cairomm_version}
Requires:       gdk-pixbuf2%{?_isa} >= %{gdk_pixbuf2_version}
Requires:       glibmm%{?_isa} >= %{glibmm_version}
Requires:       gtk3%{?_isa} >= %{gtk3_version}
Requires:       pangomm%{?_isa} >= %{pangomm_version}

%description
gtkmm is the official C++ interface for the popular GUI library GTK+.
Highlights include type safe callbacks, and a comprehensive set of
widgets that are easily extensible via inheritance.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        API documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       glibmm-doc

%description    doc
This package contains the full API documentation for %{name}.


%prep
%setup -q -n gtkmm-%{version}

# Copy demos before build to avoid including built binaries in -doc package
mkdir -p _docs
cp -a demos/ _docs/


%build
%configure --disable-static

# fix lib64 rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# avoid unused direct dependencies
sed -i 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

make %{?_smp_mflags}


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%ldconfig_scriptlets


%files
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/*.so.*

%files devel
%{_includedir}/gtkmm-%{apiver}/
%{_includedir}/gdkmm-%{apiver}/
%{_libdir}/*.so
%{_libdir}/gtkmm-%{apiver}/
%{_libdir}/gdkmm-%{apiver}/
%{_libdir}/pkgconfig/*.pc

%files doc
%doc %{_docdir}/gtkmm-%{apiver}/
%doc %{_datadir}/devhelp/
%doc _docs/*


%changelog
* Tue Feb 15 2022 Cameron Baird <cameronbaird@microsoft.com> - 3.24.2-4
- Update Requires: to point at glibmm, rather than glibmm24 (removed)
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.24.2-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 24 2019 Kalev Lember <klember@redhat.com> - 3.24.2-1
- Update to 3.24.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 20 2019 Kalev Lember <klember@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Kalev Lember <klember@redhat.com> - 3.22.3-1
- Update to 3.22.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 3.22.2-1
- Update to 3.22.2

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 23 2017 Kalev Lember <klember@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 20 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Fri Sep 16 2016 Kalev Lember <klember@redhat.com> - 3.21.6-1
- Update to 3.21.6
- Don't set group tags

* Tue Jul 26 2016 Kalev Lember <klember@redhat.com> - 3.21.4-1
- Update to 3.21.4

* Mon Jul 18 2016 Richard Hughes <rhughes@redhat.com> - 3.21.3-1
- Update to 3.21.3

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 3.21.2-1
- Update to 3.21.2

* Thu Apr 14 2016 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Wed Mar 30 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Fri Mar 18 2016 Kalev Lember <klember@redhat.com> - 3.19.12-1
- Update to 3.19.12
- Disable failing tests

* Mon Mar 07 2016 Kalev Lember <klember@redhat.com> - 3.19.11-1
- Update to 3.19.11

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Richard Hughes <rhughes@redhat.com> - 3.19.6-1
- Update to 3.19.6

* Tue Dec 29 2015 Kalev Lember <klember@redhat.com> - 3.19.5-1
- Update to 3.19.5

* Mon Nov 30 2015 Kalev Lember <klember@redhat.com> - 3.19.3-1
- Update to 3.19.3

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0
- Use make_install macro

* Tue Sep 15 2015 Richard Hughes <rhughes@redhat.com> - 3.17.90-1
- Update to 3.17.90

* Tue Jun 30 2015 Kalev Lember <klember@redhat.com> - 3.17.4-1
- Update to 3.17.4

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.3-1
- Update to 3.17.3

* Fri May 01 2015 David Tardon <dtardon@redhat.com> - 3.16.0-2
- rebuild for yet another C++ ABI break

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Fri Mar 06 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.10-1
- Update to 3.15.10

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.9-1
- Update to 3.15.9
- Use the %%license macro for the COPYING file

* Sun Mar 01 2015 Kevin Fenzi <kevin@scrye.com> 3.15.4-2
- Rebuild for gcc5

* Thu Jan 22 2015 Richard Hughes <rhughes@redhat.com> - 3.15.4-1
- Update to 3.15.4

* Thu Dec 18 2014 Richard Hughes <rhughes@redhat.com> - 3.15.3-1
- Update to 3.15.3

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.8-1
- Update to 3.13.8

* Fri Aug 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.7-1
- Update to 3.13.7

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 30 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.5-1
- Update to 3.13.5

* Thu Jun 26 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-1
- Update to 3.13.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-1
- Update to 3.13.2

* Sun Apr 13 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0-1
- Update to 3.12.0

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.10-1
- Update to 3.11.10
- Specify minimum required glibmm24 and gtk3 versions
- Tighten -devel deps

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.9-1
- Update to 3.11.9

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 3.11.8-1
- Update to 3.11.8

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.7-1
- Update to 3.11.7

* Mon Feb 17 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Tue Jan 21 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Richard Hughes <rhughes@redhat.com> - 3.9.16-1
- Update to 3.9.16

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.14-1
- Update to 3.9.14

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.12-1
- Update to 3.9.12

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.10-1
- Update to 3.9.10

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Wed Apr 17 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.12-1
- Update to 3.7.12

* Mon Feb 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.10-1
- Update to 3.7.10

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 22 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Thu Sep 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.13-1
- Update to 3.5.13

* Wed Sep 05 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.12-1
- Update to 3.5.12

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.6-1
- Update to 3.5.6

* Tue Jun 12 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Wed Apr 11 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 07 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.18-1
- Update to 3.3.18

* Tue Feb 28 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.16-1
- Update to 3.3.16
- Remove manual Requires from -devel subpackage; these are automatically
  generated with rpm pkgconfig depgen

* Tue Feb 07 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.14-1
- Update to 3.3.14

* Sun Jan 22 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 3.3.2-1
- upstream 3.3.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Fri Sep 16 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.90-1
- Update to 3.1.90

* Wed Sep 07 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.18-1
- Update to 3.1.18

* Wed Aug 31 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.16-1
- Update to 3.1.16

* Thu Jul 28 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.10-1
- Update to 3.1.10

* Sat Jul 09 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.8-1
- Update to 3.1.8
- Use the xz compressed tarballs
- Clean up the spec file for modern rpmbuild

* Mon May 09 2011 Kalev Lember <kalev@smartlink.ee> - 3.0.1-1
- Update to 3.0.1

* Wed Apr 06 2011 Kalev Lember <kalev@smartlink.ee> - 3.0.0-1
- Update to 3.0.0

* Fri Mar 25 2011 Kalev Lember <kalev@smartlink.ee> - 2.99.8-1
- Update to 2.99.8
- Dropped BR mm-common which is no longer needed for tarball builds

* Fri Mar 18 2011 Kalev Lember <kalev@smartlink.ee> - 2.99.6-1
- Update to 2.99.6
- BuildRequire mm-common for doctools which are no longer in glibmm24-devel.

* Tue Mar 01 2011 Kalev Lember <kalev@smartlink.ee> - 2.99.5-2
- Spec cleanup
- Ship the source code for demos in -doc
- Require base package from -doc subpackage
- Actually co-own /usr/share/devhelp/ directory

* Sun Feb 27 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.99.5-1
- Update to 2.99.5

* Sun Feb 27 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.99.3-4
- fix documentation handling

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.99.3-3
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.99.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Kalev Lember <kalev@smartlink.ee> - 2.99.3-1
- Update to 2.99.3

* Thu Jan 13 2011 Kalev Lember <kalev@smartlink.ee> - 2.99.1-1
- Update to 2.99.1

* Fri Dec 03 2010 Kalev Lember <kalev@smartlink.ee> - 2.91.5.1-1
- Update to 2.91.5.1

* Tue Nov 02 2010 Kalev Lember <kalev@smartlink.ee> - 2.91.3-1
- Update to 2.91.3

* Mon Nov 01 2010 Kalev Lember <kalev@smartlink.ee> - 2.91.2-1
- Update to 2.91.2
- Removed no-application.patch as we now have new enough glibmm

* Sun Oct 03 2010 Kalev Lember <kalev@smartlink.ee> - 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.90.7-1
- 2.90.7
- no more "application" support in glib

* Wed Sep 29 2010 jkeating - 2.90.5-3
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Kalev Lember <kalev@smartlink.ee> - 2.90.5-2
- Co-own /usr/share/gtk-doc/ directory (#604169)

* Wed Jul 14 2010 Kalev Lember <kalev@smartlink.ee> - 2.90.5-1
- Update to 2.90.5

* Wed Jul 07 2010 Kalev Lember <kalev@smartlink.ee> - 2.90.4.0-3
- Avoid putting built demos in /usr/share (#608326)
- Moved demos to -doc package

* Tue Jul 06 2010 Kalev Lember <kalev@smartlink.ee> - 2.90.4.0-2
- Review fixes (#608326)
- Fixed lib64 rpaths
- Added %%check section
- Use %%define instead of %%global to set release_version macro, as the latter
  seems to confuse rpmlint
- Replaced hardcoded /usr/share with %%_datadir macro
- Updated description

* Mon Jul 05 2010 Kalev Lember <kalev@smartlink.ee> - 2.90.4.0-1
- Update to 2.90.4.0

* Sat Jun 26 2010 Kalev Lember <kalev@smartlink.ee> - 2.90.3.1-1
- Initial gtkmm30 spec based on gtkmm24 spec
