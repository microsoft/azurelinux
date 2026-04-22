# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global 	api_ver 2.6
# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           libxml++
Version:        2.42.3
Release: 8%{?dist}
Summary:        C++ wrapper for the libxml2 XML parser library

License:        LGPL-2.1-or-later
URL:            https://libxmlplusplus.sourceforge.net/
Source0:        https://download.gnome.org/sources/libxml++/%{release_version}/libxml++-%{version}.tar.xz

BuildRequires:  docbook-style-xsl
BuildRequires:  doxygen, graphviz
BuildRequires:  gcc-c++
BuildRequires:  glibmm24-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt
BuildRequires:  meson

%description
libxml++ is a C++ wrapper for the libxml2 XML parser library. Its original
author is Ari Johnson and it is currently maintained by Christophe de Vienne
and Murray Cumming.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libxml2-devel
Requires:       glibmm24-devel

%description devel
This package contains the headers and libraries for libxml++ development.

%package        doc
Summary:        Documentation for %{name}, includes full API docs
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       glibmm24-doc

%description    doc
This package contains the full API documentation for %{name}.


%prep
%setup -q
sed -i s'#\r##' examples/dom_parser/example_with_namespace.xml

%build
%meson -Dbuild-documentation=true
%meson_build

%install
%meson_install


%files
%license COPYING
%doc NEWS README.md
%{_libdir}/%{name}-%{api_ver}.so.2*


%files devel
%{_includedir}/%{name}-%{api_ver}/
%{_libdir}/%{name}-%{api_ver}/
%{_libdir}/%{name}-%{api_ver}.so
%{_libdir}/pkgconfig/%{name}-%{api_ver}.pc


%files doc
%doc %{_datadir}/devhelp/books/%{name}-%{api_ver}
%doc %{_docdir}/%{name}-%{api_ver}


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Kalev Lember <klember@redhat.com> - 2.42.3-1
- Update to 2.42.3

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 19 2022 Kalev Lember <klember@redhat.com> - 2.42.2-1
- Update to 2.42.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 27 2021 Kalev Lember <klember@redhat.com> - 2.42.1-1
- Update to 2.42.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct  5 2020 Kalev Lember <klember@redhat.com> - 2.42.0-1
- Update to 2.42.0
- Switch to meson build system
- Tighten soname globs

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 01 2015 Kalev Lember <klember@redhat.com> - 2.40.1-1
- Update to 2.40.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 2.40.0-1
- Update to 2.40.0
- Tighten -devel subpackage deps with _isa macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Kalev Lember <kalevlember@gmail.com> - 2.38.1-1
- Update to 2.38.1
- Use license macro for the COPYING file
- Drop large ChangeLog file

* Wed Apr 29 2015 Kalev Lember <kalevlember@gmail.com> - 2.38.0-2
- Rebuilt for GCC 5 ABI change

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.38.0-1
- Update to 2.38.0

* Mon Mar 02 2015 Kevin Fenzi <kevin@scrye.com> 2.37.2-2
- Rebuild for new gcc

* Wed Nov 26 2014 Kalev Lember <kalevlember@gmail.com> - 2.37.2-1
- Update to 2.37.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.37.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.37.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Kalev Lember <kalevlember@gmail.com> - 2.37.1-1
- Update to 2.37.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.36.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 10 2012 Kalev Lember <kalevlember@gmail.com> - 2.36.0-1
- Update to 2.36.0

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 2.35.4-1
- Update to 2.35.4

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.34.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.34.2-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.34.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 07 2011 Kalev Lember <kalevlember@gmail.com> - 2.34.2-1
- Update to 2.34.2

* Tue Jun 14 2011 Kalev Lember <kalev@smartlink.ee> - 2.34.1-1
- Update to 2.34.1
- Dropped upstreamed patches
- Require base package from -doc subpackage
- Clean up the spec file for modern rpmbuild

* Fri Jun 10 2011 Karsten Hopp <karsten@redhat.com> 2.33.2-2
- buildrequire mm-common for doc-install.pl
- fix configure and aclocal to check for mm-common-util before trying glibmm-2.4

* Tue Feb 22 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.33.2-1
- Update to upstream 2.33.2
- split doc into sub-package

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 2.33.1-1
- Update to upstream 2.33.1

* Fri Nov 05 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 2.32.0-1
- Update to upstream 2.32.0

* Thu Sep 30 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 2.30.1-1
- Update to upstream 2.30.1

* Fri Apr 09 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 2.30.0-1
- Update to upstream 2.30.0

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Denis Leroy <denis@poolshark.org> - 2.26.0-1
- Update to upstream 2.26.0 (to match Gnome release)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Denis Leroy <denis@poolshark.org> - 2.24.2-1
- Update to 2.24.2 (memleak fixes)
- Fixed Gnome FTP URL

* Fri Aug 29 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 2.23.2-2
- Include unowned directories

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.23.2-1
- update to 2.23.2

* Tue May 13 2008 Denis Leroy <denis@poolshark.org>
- Removed unneeded example binaries from devel package

* Thu Mar 13 2008 Denis Leroy <denis@poolshark.org> - 2.22.0-1
- Update to upstream 2.22.0
- GCC 4.3 patch upstreamed

* Sun Feb 17 2008 Denis Leroy <denis@poolshark.org> - 2.20.0-2
- Added patch for gcc 4.3 rebuild

* Thu Sep 20 2007 Denis Leroy <denis@poolshark.org> - 2.20.0-1
- Update to new 2.20 stable branch

* Thu Aug 16 2007 Denis Leroy <denis@poolshark.org> - 2.18.2-2
- Update to upstream 2.18.2 (mem leak fix)
- Fixed License tag

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 2.18.1-2
- Rebuild for RH #249435

* Tue Jul 24 2007 Denis Leroy <denis@poolshark.org> - 2.18.1-1
- Update to version 2.18.1

* Sun Sep 03 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.14.0-1.1
- FC6 rebuild

* Tue May 02 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.14.0-1
- Version 2.14.0

* Mon Feb 13 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.12.0-2.1
- FC5 Rebuild

* Thu Jan 26 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 2.12.0-2
- Rebuilt to address RH #178592

* Thu Sep 08 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 2.12.0-1
- Version 2.12.0
- Use --disable-static for configure.

* Thu Jul 21 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 2.10.0-1
- Version 2.10.0
- Rearrange and conform to new FE standards
- Buildrequire glibmm24-devel
- Add devel requires to -devel

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.26.0-5
- rebuild on all arches

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Nov 04 2003 Panu Matilainen <pmatilai@welho.com> - 0:0:26.0-0.fdr.3
- remove empty .libs directories

* Mon Nov  3 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.26.0-0.fdr.2
- buildrequires graphviz
- devel package requires main package and pkgconfig
- own %%_includedir/libxml++-1.0
- clean up examples tree

* Tue Oct 21 2003 Panu Matilainen <pmatilai@welho.com>
- Initial Fedora packaging

