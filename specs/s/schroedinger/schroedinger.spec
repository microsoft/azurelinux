# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define abi 1.0

Name:           schroedinger
Version:        1.0.11
Release:        34%{?dist}
Summary:        Portable libraries for the high quality Dirac video codec

# No version is given for the GPL or the LGPL
# Automatically converted from old format: GPL+ or LGPLv2+ or MIT or MPLv1.1 - review is highly recommended.
License:        GPL-1.0-or-later OR LicenseRef-Callaway-LGPLv2+ OR LicenseRef-Callaway-MIT OR LicenseRef-Callaway-MPLv1.1
URL:            http://schrodinger.sourceforge.net/schrodinger_faq.php
Source0:        http://www.diracvideo.org/download/schroedinger/schroedinger-%{version}.tar.gz

BuildRequires: make
BuildRequires:  gcc gcc-c++
BuildRequires:  orc-devel >= 0.4.16
BuildRequires:  glew-devel >= 1.5.1
BuildRequires:  gtk-doc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool


%description
The Schrödinger project will implement portable libraries for the high
quality Dirac video codec created by BBC Research and
Development. Dirac is a free and open source codec producing very high
image quality video.

The Schrödinger project is a project done by BBC R&D and Fluendo in
order to create a set of high quality decoder and encoder libraries
for the Dirac video codec.

%package devel
Summary:        Development files for schroedinger
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       orc-devel%{?_isa} >= 0.4.10

%description devel
Development files for schroedinger


%prep
%setup -q
# fix compatibility with gtk-doc 1.26
gtkdocize
autoreconf -fiv


%build
%configure --disable-static --enable-gtk-doc

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install
find %{buildroot} -name \*.la -delete


%ldconfig_scriptlets


%files
%doc NEWS TODO
%license COPYING*
%{_libdir}/libschroedinger-%{abi}.so.*


%files devel
%doc %{_datadir}/gtk-doc/html/schroedinger
%{_includedir}/schroedinger-%{abi}
%{_libdir}/*.so
%{_libdir}/pkgconfig/schroedinger-%{abi}.pc


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1.0.11-32
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 27 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.0.11-19
- Revert wrong workaround

* Sat Jul 21 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.0.11-18
- Add missing cc

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Merlin Mathesius <mmathesi@redhat.com> - 1.0.11-15
- Fix FTBFS in a better way by updating for compatibility with gtk-doc-1.26.

* Wed Jan 24 2018 Merlin Mathesius <mmathesi@redhat.com> - 1.0.11-14
- Fix FTBFS by disabling regeneration of documentation at build time
  and using pregenerated docs included in upstream source. This is
  because gtkdoc-mktmpl has been removed as of gtk-doc-1.26.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.11-8
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 27 2012 Fabian Deutsch <fabiand@fedoraproject.org> - 1.0.11-2
- Bump required orc version to 0.4.16

* Mon Jan 23 2012 Fabian Deutsch <fabiand@fedoraproject.org> - 1.0.11-1
- Update to 1.0.11

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 24 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 1.0.10-1
- Update to 1.0.10

* Thu Apr 22 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 1.0.9-2
- Added dependency on gtk-doc

* Fri Mar 05 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 1.0.9-1
- Update to 1.0.9
- Dropped dependency on liboil
- Added dependency on orc

* Mon Feb  1 2010 Nicolas CHauvet <kwizart@fedoraproject.org> - 1.0.8-4
- Remove gstreamer-plugins-schroedinger 
  Obsoleted by gst-plugins-bad-free introduction in Fedora.

* Sun Oct 25 2009 kwizart < kwizart at gmail.com > - 1.0.8-3
- Re-introduce gstreamer sub-package until seen in -good

* Tue Oct 20 2009 kwizart < kwizart at gmail.com > - 1.0.8-2
- Update to 1.0.8
- gstreamer-plugins-schroedinger is now in bad.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 24 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.7-1
- Update to 1.0.7

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 29 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.5-4
- Fix some typos [BZ#469133]

* Fri Sep 12 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.5-3
- Bump release and rebuild against latest gstreamer-* packages to pick
- up special gstreamer codec provides.

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.5-2
- fix license tag

* Wed Aug 27 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.5-1
- Update to 1.0.5

* Wed Jul  2 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.3-2
- Devel subpackage needs to require liboil-devel.

* Fri Jun 27 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.3-1
- Update to 1.0.3.
- Update URLs.

* Fri Feb 22 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.0-1
- Update to 1.0.0

* Mon Feb 11 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.0-2
- Rebuild for GCC 4.3

* Mon Nov 12 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.0-1
- Update to 0.9.0

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.6.1-3
- Rebuild for selinux ppc32 issue.

* Wed Jun 20 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.6.1-2
- Fix license field
- Add pkgconfig as a requirement for the devel subpackage

* Sun Jun 10 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.6.1-1
- First version for Fedora
