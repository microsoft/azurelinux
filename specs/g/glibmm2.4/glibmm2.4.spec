# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global apiver 2.4
# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

%global glib2_version 2.61.2
%global libsigc_version 2.9.1

Name:           glibmm2.4
Version:        2.66.8
Release: 3%{?dist}
Summary:        C++ interface for the GLib library

# Library sources are LGPL 2.1+, tools used to generate sources are GPL 2+.
License:        LGPL-2.1-or-later AND GPL-2.0-or-later
URL:            https://gtkmm.org/
Source0:        https://download.gnome.org/sources/glibmm/%{release_version}/glibmm-%{version}.tar.xz

Patch0:         glibmm24-gcc11.patch

BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  libxslt
BuildRequires:  m4
BuildRequires:  meson
BuildRequires:  mm-common
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Getopt::Long)
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(sigc++-2.0) >= %{libsigc_version}

Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       libsigc++20%{?_isa} >= %{libsigc_version}

# Renamed in F37
Obsoletes:      glibmm24 < %{version}-%{release}
Provides:       glibmm24 = %{version}-%{release}
Provides:       glibmm24%{?_isa} = %{version}-%{release}

# Do not export private Perl modules
%global __provides_exclude %{?__provides_exclude:%{__provides_exclude}|}^perl\\(
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((DocsParser|Enum|Function|FunctionBase|GtkDefs|Object|Output|Property|Util|WrapParser)\\)

%description
glibmm is the official C++ interface for the popular cross-platform
library GLib. It provides non-UI API that is not available in standard
C++ and makes it possible for gtkmm to wrap GObject-based APIs.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Renamed in F37
Obsoletes:      glibmm24-devel < %{version}-%{release}
Provides:       glibmm24-devel = %{version}-%{release}
Provides:       glibmm24-devel%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        API documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       libsigc++20-doc
# Renamed in F37
Obsoletes:      glibmm24-doc < %{version}-%{release}
Provides:       glibmm24-doc = %{version}-%{release}

%description    doc
This package contains the full API documentation for %{name}.


%prep
%autosetup -p1 -n glibmm-%{version}


%build
%meson -Dbuild-documentation=true
%meson_build


%install
%meson_install

chmod +x $RPM_BUILD_ROOT%{_libdir}/glibmm-%{apiver}/proc/generate_wrap_init.pl
chmod +x $RPM_BUILD_ROOT%{_libdir}/glibmm-%{apiver}/proc/gmmproc


%files
%license COPYING COPYING.tools
%doc NEWS README.md
%{_libdir}/libgiomm-%{apiver}.so.1*
%{_libdir}/libglibmm-%{apiver}.so.1*
%{_libdir}/libglibmm_generate_extra_defs-%{apiver}.so.1*

%files devel
%{_includedir}/glibmm-%{apiver}/
%{_includedir}/giomm-%{apiver}/
%{_libdir}/*.so
%{_libdir}/glibmm-%{apiver}/
%{_libdir}/giomm-%{apiver}/
%{_libdir}/pkgconfig/*.pc

%files doc
%doc %{_datadir}/devhelp/
%doc %{_docdir}/glibmm-%{apiver}/


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.66.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Mar 19 2025 nmontero <nmontero@redhat.com> - 2.66.8-1
- Update to 2.66.8

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.66.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.66.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar 26 2024 David King <amigadave@amigadave.com> - 2.66.7-1
- Update to 2.66.7

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.66.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.66.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.66.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Apr 25 2023 David King <amigadave@amigadave.com> - 2.66.6-1
- Update to 2.66.6

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.66.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Sep 23 2022 Kalev Lember <klember@redhat.com> - 2.66.5-2
- Rename from glibmm24 to glibmm2.4

* Mon Sep 19 2022 Kalev Lember <klember@redhat.com> - 2.66.5-1
- Update to 2.66.5

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.66.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 04 2022 David King <amigadave@amigadave.com> - 2.66.4-1
- Update to 2.66.4

* Tue May 03 2022 David King <amigadave@amigadave.com> - 2.66.3-1
- Update to 2.66.3

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.66.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 27 2021 Kalev Lember <klember@redhat.com> - 2.66.2-1
- Update to 2.66.2

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.66.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 26 2021 Kalev Lember <klember@redhat.com> - 2.66.1-1
- Update to 2.66.1

* Wed Apr 14 2021 Kalev Lember <klember@redhat.com> - 2.66.0-2
- Update generated header files for C++20 compatibility (#1947838)

* Tue Apr 13 2021 Kalev Lember <klember@redhat.com> - 2.66.0-1
- Update to 2.66.0
- Backport upstream fix for C++20 compatibility (#1947838)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.64.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Kalev Lember <klember@redhat.com> - 2.64.5-3
- Fix gmmproc and generate_wrap_init.pl to be executable (#1917035)

* Mon Dec 14 2020 Kalev Lember <klember@redhat.com> - 2.64.5-2
- Add missing dep for generating links to libstdc++ docs

* Tue Dec  1 2020 Kalev Lember <klember@redhat.com> - 2.64.5-1
- Update to 2.64.5

* Tue Nov 24 2020 Kalev Lember <klember@redhat.com> - 2.64.4-1
- Update to 2.64.4
- Switch to meson build system
- Tighten soname globs

* Sat Oct 31 2020 Jeff Law <law@redhat.com> - 2.64.2-5
- Fix bogus volatile caught by gcc-11

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.64.2-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.64.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 Petr Pisar <ppisar@redhat.com> - 2.64.2-2
- Do not export private Perl modules

* Fri Mar 27 2020 Kalev Lember <klember@redhat.com> - 2.64.2-1
- Update to 2.64.2

* Fri Mar 20 2020 Kalev Lember <klember@redhat.com> - 2.64.1-2
- Backport an upstream fix to fix ardour5 build (#1815144)

* Wed Mar 18 2020 Kalev Lember <klember@redhat.com> - 2.64.1-1
- Update to 2.64.1

* Tue Mar 17 2020 Kalev Lember <klember@redhat.com> - 2.64.0-1
- Update to 2.64.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.62.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 19 2019 Kalev Lember <klember@redhat.com> - 2.62.0-1
- Update to 2.62.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.60.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 19 2019 Kalev Lember <klember@redhat.com> - 2.60.0-1
- Update to 2.60.0

* Mon Mar 18 2019 Kalev Lember <klember@redhat.com> - 2.58.1-1
- Update to 2.58.1

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.58.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 01 2018 Kalev Lember <klember@redhat.com> - 2.58.0-1
- Update to 2.58.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.56.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 02 2018 Kalev Lember <klember@redhat.com> - 2.56.0-1
- Update to 2.56.0
- Remove ldconfig scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.54.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Kalev Lember <klember@redhat.com> - 2.54.1-2
- Backport a patch to fix invalid code in glibmm/threads.h (#1540795)

* Mon Sep 18 2017 Kalev Lember <klember@redhat.com> - 2.54.1-1
- Update to 2.54.1

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 2.54.0-1
- Update to 2.54.0

* Tue Sep 05 2017 Kalev Lember <klember@redhat.com> - 2.52.1-1
- Update to 2.52.1

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.52.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.52.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 23 2017 Kalev Lember <klember@redhat.com> - 2.52.0-1
- Update to 2.52.0

* Wed May 10 2017 Kalev Lember <klember@redhat.com> - 2.51.7-1
- Update to 2.51.7

* Mon Apr 03 2017 Kalev Lember <klember@redhat.com> - 2.51.6-1
- Update to 2.51.6

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.50.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 20 2016 Kalev Lember <klember@redhat.com> - 2.50.0-1
- Update to 2.50.0
- Use make_install macro

* Fri Sep 16 2016 Kalev Lember <klember@redhat.com> - 2.49.7-1
- Update to 2.49.7
- Don't set group tags

* Sun Aug 21 2016 Kalev Lember <klember@redhat.com> - 2.49.5-1
- Update to 2.49.5

* Tue Jul 26 2016 Kalev Lember <klember@redhat.com> - 2.49.4-1
- Update to 2.49.4

* Mon Jul 18 2016 Richard Hughes <rhughes@redhat.com> - 2.49.2-1
- Update to 2.49.2

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 2.49.1-1
- Update to 2.49.1

* Thu Mar 31 2016 Kalev Lember <klember@redhat.com> - 2.48.1-1
- Update to 2.48.1

* Wed Mar 30 2016 Kalev Lember <klember@redhat.com> - 2.48.0-1
- Update to 2.48.0

* Fri Mar 18 2016 Kalev Lember <klember@redhat.com> - 2.47.92-1
- Update to 2.47.92

* Wed Mar 02 2016 Richard Hughes <rhughes@redhat.com> - 2.47.6-1
- Update to 2.47.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.47.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 18 2015 Kalev Lember <klember@redhat.com> - 2.47.4-1
- Update to 2.47.4

* Sat Nov 28 2015 Kalev Lember <klember@redhat.com> - 2.47.3.1-1
- Update to 2.47.3.1

* Fri Nov 20 2015 Kalev Lember <klember@redhat.com> - 2.46.2-1
- Update to 2.46.2

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 2.46.1-1
- Update to 2.46.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 2.46.0-1
- Update to 2.46.0

* Tue Sep 15 2015 Richard Hughes <rhughes@redhat.com> - 2.45.80-1
- Update to 2.45.80

* Tue Jun 30 2015 Kalev Lember <klember@redhat.com> - 2.45.3-1
- Update to 2.45.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.45.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Kalev Lember <kalevlember@gmail.com> - 2.45.2-1
- Update to 2.45.2

* Fri Apr 24 2015 Nils Philippsen <nils@redhat.com> - 2.44.0-2
- rebuild for C++11 ABI
- fix bogus changelog dates

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 2.44.0-1
- Update to 2.44.0
- Use license macro for the COPYING file

* Fri Mar 06 2015 Kalev Lember <kalevlember@gmail.com> - 2.43.91-1
- Update to 2.43.91

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.43.90-1
- Update to 2.43.90

* Fri Feb 27 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.43.3-2
- Rebuild on F-23 for gcc5 ABI change

* Thu Jan 22 2015 Richard Hughes <rhughes@redhat.com> - 2.43.3-1
- Update to 2.43.3

* Thu Dec 18 2014 Richard Hughes <rhughes@redhat.com> - 2.43.2-1
- Update to 2.43.2

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.42.0-1
- Update to 2.42.0

* Mon Sep 15 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.4-1
- Update to 2.41.4

* Fri Aug 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.3-1
- Update to 2.41.3

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 29 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.2-1
- Update to 2.41.2

* Thu Jun 26 2014 Richard Hughes <rhughes@redhat.com> - 2.41.1-1
- Update to 2.41.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.41.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Kalev Lember <kalevlember@gmail.com> - 2.41.0-1
- Update to 2.41.0
- Tighten -devel requires with %%_isa

* Sun Apr 13 2014 Kalev Lember <kalevlember@gmail.com> - 2.40.0-1
- Update to 2.40.0

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 2.39.93-2
- Set minimum required glib version

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 2.39.93-1
- Update to 2.39.93

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 2.39.92-1
- Update to 2.39.92

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 2.39.91-1
- Update to 2.39.91

* Mon Feb 17 2014 Richard Hughes <rhughes@redhat.com> - 2.39.4-1
- Update to 2.39.4

* Tue Jan 21 2014 Richard Hughes <rhughes@redhat.com> - 2.39.3-1
- Update to 2.39.3

* Mon Nov 18 2013 Richard Hughes <rhughes@redhat.com> - 2.38.1-1
- Update to 2.38.1

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 2.38.0-1
- Update to 2.38.0

* Wed Sep 25 2013 Richard Hughes <rhughes@redhat.com> - 2.37.93-1
- Update to 2.37.93

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.7-1
- Update to 2.37.7

* Wed Aug 28 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.6-1
- Update to 2.37.6

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.5-1
- Update to 2.37.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.37.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.37.4-2
- Perl 5.18 rebuild

* Tue Jul 16 2013 Richard Hughes <rhughes@redhat.com> - 2.37.4-1
- Update to 2.37.4

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 2.36.2-2
- Don't install ChangeLog

* Thu May 02 2013 Kalev Lember <kalevlember@gmail.com> - 2.36.2-1
- Update to 2.36.2

* Mon Apr 29 2013 Kalev Lember <kalevlember@gmail.com> - 2.36.1-1
- Update to 2.36.1

* Wed Apr 17 2013 Kalev Lember <kalevlember@gmail.com> - 2.36.0-1
- Update to 2.36.0

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 2.35.9-1
- Update to 2.35.9

* Fri Feb 22 2013 Kalev Lember <kalevlember@gmail.com> - 2.35.8-1
- Update to 2.35.8

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.34.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 10 2012 Kalev Lember <kalevlember@gmail.com> - 2.34.1-1
- Update to 2.34.1

* Mon Oct 22 2012 Kalev Lember <kalevlember@gmail.com> - 2.34.0-1
- Update to 2.34.0

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 2.33.14-1
- Update to 2.33.14

* Wed Sep 26 2012 Kalev Lember <kalevlember@gmail.com> - 2.33.13-1
- Update to 2.33.13

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Kalev Lember <kalevlember@gmail.com> - 2.33.3-1
- Update to 2.33.3

* Thu Jun 21 2012 Kalev Lember <kalevlember@gmail.com> - 2.33.2-1
- Update to 2.33.2

* Tue Jun 12 2012 Kalev Lember <kalevlember@gmail.com> - 2.33.1-1
- Update to 2.33.1

* Wed Apr 11 2012 Kalev Lember <kalevlember@gmail.com> - 2.32.0-1
- Update to 2.32.0

* Wed Mar 07 2012 Kalev Lember <kalevlember@gmail.com> - 2.31.20-1
- Update to 2.31.20

* Mon Feb 27 2012 Kalev Lember <kalevlember@gmail.com> - 2.31.18.1-1
- Update to 2.31.18.1

* Sun Feb 26 2012 Kalev Lember <kalevlember@gmail.com> - 2.31.18-1
- Update to 2.31.18

* Tue Feb 07 2012 Kalev Lember <kalevlember@gmail.com> - 2.31.16-1
- Update to 2.31.16
- Drop upstreamed patches

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec  4 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.31.2-2
- close RHBZ #759644 (patch accepted upstream)

* Sat Dec  3 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.31.2-1
- upstream 2.31.2 (unstable)
- do not use glib deprecated API (RHBZ #759644)

* Thu Dec 01 2011 Dan Horák <dan[at]danny.cz> 2.30.1-1
- Update to 2.30.1 - fixes FTBFS with latest glib

* Wed Sep 28 2011 Ray Strode <rstrode@redhat.com> 2.30.0-1
- Update to 2.30.0

* Wed Sep 07 2011 Kalev Lember <kalevlember@gmail.com> - 2.29.13-1
- Update to 2.29.13

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 2.29.12-1
- Update to 2.29.12

* Mon Jul 25 2011 Kalev Lember <kalevlember@gmail.com> - 2.29.11-1
- Update to 2.29.11

* Sat Jul 09 2011 Kalev Lember <kalevlember@gmail.com> - 2.29.10-1
- Update to 2.29.10

* Tue Jun 14 2011 Kalev Lember <kalev@smartlink.ee> - 2.28.2-1
- Update to 2.28.2
- Use .xz compressed tarballs
- Clean up the spec file for modern rpmbuild

* Mon May 09 2011 Kalev Lember <kalev@smartlink.ee> - 2.28.1-1
- Update to 2.28.1

* Tue Apr 05 2011 Kalev Lember <kalev@smartlink.ee> - 2.28.0-1
- Update to 2.28.0

* Thu Mar 24 2011 Kalev Lember <kalev@smartlink.ee> - 2.27.99-1
- Update to 2.27.99
- Dropped BR mm-common which is no longer needed for tarball builds
- BR stable glib2 release

* Wed Mar 23 2011 Kalev Lember <kalev@smartlink.ee> - 2.27.98-1
- Update to 2.27.98

* Fri Mar 18 2011 Kalev Lember <kalev@smartlink.ee> - 2.27.97-1
- Update to 2.27.97
- BuildRequire mm-common as the doctools are no longer bundled
  with glibmm tarball.

* Tue Mar 01 2011 Kalev Lember <kalev@smartlink.ee> - 2.27.94-2
- Spec cleanup
- Actually co-own /usr/share/devhelp/ directory
- Require base package from -doc subpackage

* Mon Feb 21 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.27.94-1
- upstream 2.27.94
- fix documentation location
- co-own /usr/share/devhelp

* Thu Feb 03 2011 Kalev Lember <kalev@smartlink.ee> - 2.27.93-1
- Update to 2.27.93

* Thu Jan 13 2011 Kalev Lember <kalev@smartlink.ee> - 2.27.91-1
- Update to 2.27.91

* Fri Dec 03 2010 Kalev Lember <kalev@smartlink.ee> - 2.27.4-1
- Update to 2.27.4

* Thu Nov 11 2010 Kalev Lember <kalev@smartlink.ee> - 2.27.3-1
- Update to 2.27.3

* Tue Nov 02 2010 Kalev Lember <kalev@smartlink.ee> - 2.27.2-1
- Update to 2.27.2
- Use macro for automatically calculating ftp directory name with
  first two digits of tarball version.

* Mon Nov 01 2010 Kalev Lember <kalev@smartlink.ee> - 2.27.1-1
- Update to 2.27.1

* Wed Sep 29 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.25.5-1
- update to 2.25.5

* Wed Sep 29 2010 jkeating - 2.24.2-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Kalev Lember <kalev@smartlink.ee> - 2.24.2-1
- Update to 2.24.2
- Reworked description and summary
- Fixed macro-in-changelog rpmlint warning
- Build doc subpackage as noarch and require base package as
  per new licensing guidelines
- Co-own gtk-doc directory (#604169)

* Thu Apr 29 2010 Haikel Guémar <hguemar@fedoraproject.org> - 2.24.1-1
- Update to upstream 2.24.1

* Wed Apr  7 2010 Denis Leroy <denis@poolshark.org> - 2.24.0-1
- Update to stable 2.24.0

* Mon Mar  8 2010 Denis Leroy <denis@poolshark.org> - 2.23.3-1
- Update to upstream 2.23.3, several bug fixes

* Thu Feb 18 2010 Denis Leroy <denis@poolshark.org> - 2.23.2-1
- Update to upstream 2.23.2

* Sun Jan 17 2010 Denis Leroy <denis@poolshark.org> - 2.23.1-1
- Update to upstream 2.23.1, new unstable branch to follow glib2

* Fri Sep 25 2009 Denis Leroy <denis@poolshark.org> - 2.22.1-1
- Update to upstream 2.22.1

* Tue Sep 15 2009 Denis Leroy <denis@poolshark.org> - 2.21.5-2
- Better fix for devhelp file broken tags

* Mon Sep 14 2009 Denis Leroy <denis@poolshark.org> - 2.21.5-1
- Update to upstream 2.21.5
- Keep datadir/glibmm-2.4, for doc scripts

* Wed Sep  2 2009 Denis Leroy <denis@poolshark.org> - 2.21.4.2-1
- Update to upstream 2.21.4.2

* Sun Aug 30 2009 Denis Leroy <denis@poolshark.org> - 2.21.4-1
- Update to upstream 2.21.4

* Sun Aug 16 2009 Denis Leroy <denis@poolshark.org> - 2.21.3-1
- Update to upstream 2.21.3

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 Denis Leroy <denis@poolshark.org> - 2.21.1-1
- Update to upstream 2.21.1
- Switch to unstable branch, to follow glib2 version

* Sat Mar 21 2009 Denis Leroy <denis@poolshark.org> - 2.20.0-1
- Update to 2.20.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Denis Leroy <denis@poolshark.org> - 2.19.2-1
- Update to upstream 2.19.2
- Some new API, memory leak fix

* Wed Jan 14 2009 Denis Leroy <denis@poolshark.org> - 2.19.1-1
- Update to upstream 2.19.1

* Thu Dec 11 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.18.1-2
- Rebuild for pkgconfig provides

* Tue Oct 21 2008 Denis Leroy <denis@poolshark.org> - 2.18.1-1
- Update to upstream 2.18.1, many bug fixes
- Patch for define conflict upstreamed

* Sat Oct 11 2008 Denis Leroy <denis@poolshark.org> - 2.18.0-4
- Split documentation in new doc sub-package
- Fixed some devhelp documentation links

* Sun Oct 05 2008 Adel Gadllah <adel.gadllah@gmail.com> - 2.18.0-3
- Patch error.h directly rather than error.hg

* Sun Oct 05 2008 Adel Gadllah <adel.gadllah@gmail.com> - 2.18.0-2
- Backport upstream fix that resolves HOST_NOT_FOUND
  symbol conflicts (GNOME #529496)

* Tue Sep 23 2008 Denis Leroy <denis@poolshark.org> - 2.18.0-1
- Update to upstream 2.18.0

* Sun Aug 24 2008 Denis Leroy <denis@poolshark.org> - 2.17.2-1
- Update to upstream 2.17.2

* Wed Jul 23 2008 Denis Leroy <denis@poolshark.org> - 2.17.1-1
- Update to upstream 2.17.1

* Thu Jul  3 2008 Denis Leroy <denis@poolshark.org> - 2.17.0-1
- Update to unstable branch 2.17

* Sat May 17 2008 Denis Leroy <denis@poolshark.org> - 2.16.2-1
- Update to upstream 2.16.2

* Sat Apr 12 2008 Denis Leroy <denis@poolshark.org> - 2.16.1-1
- Update to upstream 2.16.1, filechooser refcount bugfix

* Wed Mar 12 2008 Denis Leroy <denis@poolshark.org> - 2.16.0-1
- Update to upstream 2.16.0, added --disable-fulldocs

* Tue Feb 12 2008 Denis Leroy <denis@poolshark.org> - 2.15.5-1
- Update to 2.15.5, skipping borked 2.15.4, CHANGES file gone

* Wed Jan 23 2008 Denis Leroy <denis@poolshark.org> - 2.15.2-1
- Update to upstream 2.15.2

* Tue Jan  8 2008 Denis Leroy <denis@poolshark.org> - 2.15.0-1
- Update to 2.15 branch, to follow up with glib2
- Now with giomm goodness

* Sun Nov  4 2007 Denis Leroy <denis@poolshark.org> - 2.14.2-1
- Update to 2.14.2, BRs update

* Fri Sep 14 2007 Denis Leroy <denis@poolshark.org> - 2.14.0-1
- Update to new stable tree 2.14.0

* Thu Sep  6 2007 Denis Leroy <denis@poolshark.org> - 2.13.9-3
- Removed Perl code autogeneration tools (#278191)

* Wed Aug 22 2007 Denis Leroy <denis@poolshark.org> - 2.13.9-2
- License tag update

* Wed Aug  1 2007 Denis Leroy <denis@poolshark.org> - 2.13.9-1
- Update to 2.13.9

* Tue Jul  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.13.6-3
- Rebuild against newest GLib (due to #245141, #245634)

* Fri Jun 22 2007 Denis Leroy <denis@poolshark.org> - 2.13.6-2
- Moved documentation to devhelp directory

* Thu Jun 21 2007 Denis Leroy <denis@poolshark.org> - 2.13.6-1
- Update to unstable 2.13 tree to follow glib2 version

* Mon Apr 30 2007 Denis Leroy <denis@poolshark.org> - 2.12.8-1
- Update to 2.12.8

* Thu Mar 15 2007 Denis Leroy <denis@poolshark.org> - 2.12.7-1
- Update to 2.12.7

* Sun Jan 28 2007 Denis Leroy <denis@poolshark.org> - 2.12.5-1
- Update to 2.12.5, some spec cleanups

* Tue Jan  9 2007 Denis Leroy <denis@poolshark.org> - 2.12.4-1
- Update to 2.12.4, number of bug fixes

* Mon Dec  4 2006 Denis Leroy <denis@poolshark.org> - 2.12.3-1
- Update to 2.12.3
- Added dist tag

* Mon Oct  2 2006 Denis Leroy <denis@poolshark.org> - 2.12.2-1
- Update to 2.12.2

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 2.12.0-2
- FE6 Rebuild

* Mon Aug 21 2006 Denis Leroy <denis@poolshark.org> - 2.12.0-1
- Update to 2.12.0

* Sun Jun 25 2006 Denis Leroy <denis@poolshark.org> - 2.10.4-1
- Update to 2.10.4

* Sun May  7 2006 Denis Leroy <denis@poolshark.org> - 2.10.1-1
- Update to 2.10.1

* Mon Mar 20 2006 Denis Leroy <denis@poolshark.org> - 2.10.0-1
- Update to 2.10.0, requires newer glib

* Tue Feb 28 2006 Denis Leroy <denis@poolshark.org> - 2.8.4-1
- Update to 2.8.4
- Added optional macro to enable static libs

* Sat Dec 17 2005 Denis Leroy <denis@poolshark.org> - 2.8.3-1
- Update to 2.8.3

* Fri Nov 25 2005 Denis Leroy <denis@poolshark.org> - 2.8.2-1
- Update to 2.8.2
- Disabled static libraries

* Mon Sep 19 2005 Denis Leroy <denis@poolshark.org> - 2.8.0-1
- Upgrade to 2.8.0
- Updated glib2 version dependency

* Fri Sep  2 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 2.6.1-2
- rebuild for gcc-c++-4.0.1-12
  result for GLIBMM_CXX_ALLOWS_STATIC_INLINE_NPOS check changed

* Sat Apr  9 2005 Denis Leroy <denis@poolshark.org> - 2.6.1-1
- Update to version 2.6.1

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Nov 17 2004 Denis Leroy <denis@poolshark.org> - 0:2.4.5-1
- Upgrade to glibmm 2.4.5

* Mon Jun 28 2004 Denis Leroy <denis@poolshark.org> - 0:2.4.4-0.fdr.1
- Upgrade to 2.4.4
- Moved docs to regular directory

* Fri Dec 6 2002 Gary Peck <gbpeck@sbcglobal.net> - 2.0.2-1
- Removed "--without docs" option and simplified the spec file since the
  documentation is included in the tarball now

* Thu Dec 5 2002 Walter H. van Holst <rpm-maintainer@fossiel.xs4all.nl> - 1.0.2
- Removed reference to patch
- Added the documentation files in %%files

* Thu Oct 31 2002 Gary Peck <gbpeck@sbcglobal.net> - 2.0.0-gp1
- Update to 2.0.0

* Wed Oct 30 2002 Gary Peck <gbpeck@sbcglobal.net> - 1.3.26-gp3
- Added "--without docs" option to disable DocBook generation

* Sat Oct 26 2002 Gary Peck <gbpeck@sbcglobal.net> - 1.3.26-gp2
- Update to 1.3.26
- Spec file cleanups
- Removed examples from devel package
- Build html documentation (including a Makefile patch)

* Mon Oct 14 2002 Gary Peck <gbpeck@sbcglobal.net> - 1.3.24-gp1
- Initial release of gtkmm2, using gtkmm spec file as base

