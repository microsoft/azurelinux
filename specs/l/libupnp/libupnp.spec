# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Version: 1.14.30
Summary: Universal Plug and Play (UPnP) SDK
Name: libupnp
Release: 1%{?dist}
# Automatically converted from old format: BSD - review is highly recommended.
License: LicenseRef-Callaway-BSD
URL: https://github.com/pupnp/pupnp
Source: %{url}/archive/release-%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: make
BuildRequires: libtool


%description
The Universal Plug and Play (UPnP) SDK for Linux provides 
support for building UPnP-compliant control points, devices, 
and bridges on Linux.

%package devel
Summary: Include files needed for development with libupnp
Requires: libupnp%{?_isa} = %{version}-%{release}

%description devel
The libupnp-devel package contains the files necessary for development with
the UPnP SDK libraries.

%prep
%autosetup -p1 -n pupnp-release-%{version}


%build
autoreconf -vif
%configure \
  --enable-static=no \
  --enable-ipv6

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install

%{__rm} %{buildroot}%{_libdir}/{libixml.la,libupnp.la}

%ldconfig_scriptlets

%files
%license COPYING
%doc THANKS
%{_libdir}/libixml.so.11*
%{_libdir}/libupnp.so.17*

%files devel
%{_includedir}/upnp/
%{_libdir}/libixml.so
%{_libdir}/libupnp.so
%{_libdir}/pkgconfig/libupnp.pc

%changelog
* Tue Feb 10 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.14.30-1
- 1.14.30

* Mon Feb 09 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.14.29-1
- 1.14.29

* Fri Feb 06 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.14.26-1
- 1.14.26

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Sep 22 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.14.25-1
- 1.14.25

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 12 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.14.24-1
- 1.14.24

* Sat Jun 07 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.14.23-1
- 1.14.23

* Tue Jun 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.14.22-1
- 1.14.22

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 08 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.14.20-1
- 1.14.20

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.14.19-3
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 23 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.14.19-1
- 1.14.19

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 23 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.14.18-1
- 1.14.18

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.14.17-1
- 1.14.17

* Thu Mar 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.14.16-1
- 1.14.16

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.14.15-1
- 1.14.15

* Wed Oct 05 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.14.14-1
- 1.14.14

* Thu Aug 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.14.13-1
- 1.14.13

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 04 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.14.12-1
- Update to 1.14.12

* Thu Aug 19 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.14.10-1
- Update to 1.14.10

* Mon Aug 16 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.14.9-1
- Update to 1.14.9

* Mon Aug 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.14.7-3
- Upstream patch to fix FTBFS.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.14.7-1
- Update to 1.14.7

* Wed Apr 21 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.14.6-1
- Update to 1.14.6

* Tue Apr 06 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.14.5-1
- Update to 1.14.5

* Tue Mar 30 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.14.4-1
- Update to 1.14.4

* Mon Mar 01 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.14.2-1
- Update to 1.14.2

* Tue Feb 09 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.14.1-1
- Update to 1.14.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.12.1-1
- 1.12.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 08 2019 Nicolas Chauvet <kwizart@gmail.com> - 1.8.4-1
- Update to 1.8.4
- Revert the ABI bump since it's the same as 1.8.3
- Add back patch for largefile support

* Thu Dec 13 2018 Dennis Gilmore <dennis@ausil.us> - 1.8.3-4
- pull in patch from upstream so that samples will build on 32 bit arches with
- largefile support, enables gerbera to run on armv7hl and i686

* Fri Jul 20 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.8.3-3
- Add missng cc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Apr 13 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.8.3-1
- Update to 1.8.3
- Drop libthreadutil

* Fri Apr 13 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.6.25-1
- Update to 1.6.25
- Spec file clean-up
- Avoid rpath

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 07 2017 Michael Cronenworth <mike@cchtml.com> - 1.6.21-1
- libupnp 1.6.21

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jul 18 2016 Adam Jackson <ajax@redhat.com> - 1.6.20-1
- libupnp 1.6.20
- Don't write to the filesystem on unhandled POST requests

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 09 2013 Adam Jackson <ajax@redhat.com> 1.6.19-1
- libupnp 1.6.19
- Build with --enable-ipv6 (#917210)

* Sun Oct 27 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.6.18-4
- Adapt to possibly unversioned doc dirs.
- Include LICENSE and THANKS in main package.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jan 29 2013 Adam Jackson <ajax@redhat.com> 1.6.18-1
- libupnp 1.6.18 (#905577)

* Tue Oct 16 2012 Adam Jackson <ajax@redhat.com> 1.6.17-1
- libupnp 1.6.17

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jul 30 2011 Matěj Cepl <mcepl@redhat.com> - 1.6.13-2
- Rebuilt against new libraries.

* Tue May 31 2011 Adam Jackson <ajax@redhat.com> 1.6.13-1
- libupnp 1.6.13

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 01 2008 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.6.6-1
- Update to version 1.6.6

* Sun Feb 03 2008 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.6.5-1
- Update to version 1.6.5

* Sun Jan 27 2008 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.6.4-1
- Update to version 1.6.4

* Fri Jan 04 2008 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.6.3-3
- No more building static library

* Sun Dec 30 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.6.3-2
- Spec file cleanup

* Sun Dec 30 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.6.3-1
- Update to version 1.6.3

* Thu Dec 13 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.6.2-1
- Update to version 1.6.2

* Sun Nov 18 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.6.1-1
- Update to version 1.6.1

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.6.0-2
- Rebuild for selinux ppc32 issue.

* Wed Jun 13 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.6.0-1
- Update to version 1.6.0

* Tue May 01 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.4.6-1
- Update to version 1.4.6

* Sat Apr 21 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.4.4-1
- Update to version 1.4.4

* Tue Mar 06 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.4.3-1
- Update to version 1.4.3

* Fri Feb 02 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.4.2-1
- Update to version 1.4.2

* Wed Jul 05 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.4.1-1
- Update to version 1.4.1

* Fri Jun 23 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.4.0-3
- modified patch for x86_64 arch

* Fri Jun 23 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.4.0-2
- Add a patch for x86_64 arch

* Sun Jun 11 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.4.0-1
- Update to 1.4.0

* Sun Mar 05 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.3.1-1
- Update to 1.3.1

* Tue Feb 14 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.2.1a-6
- Rebuild for FC5

* Fri Feb 10 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.2.1a-5
- Rebuild for FC5

* Mon Jan  9 2006 Eric Tanguy 1.2.1a-4
- Include libupnp.so symlink in package to take care of non versioning of libupnp.so.1.2.1

* Sun Jan  8 2006 Paul Howarth 1.2.1a-3
- Disable stripping of object code for sane debuginfo generation
- Edit makefiles to hnnor RPM optflags
- Install libraries in %%{_libdir} rather than hardcoded /usr/lib
- Fix libupnp.so symlink
- Own directory %%{_includedir}/upnp
- Fix permissions in -devel package

* Fri Jan 06 2006 Eric Tanguy 1.2.1a-2
- Use 'install -p' to preserve timestamps
- Devel now require full version-release of main package

* Thu Dec 22 2005 Eric Tanguy 1.2.1a-1
- Modify spec file from 
http://rpm.pbone.net/index.php3/stat/4/idpl/2378737/com/libupnp-1.2.1a_DSM320-3.i386.rpm.html
