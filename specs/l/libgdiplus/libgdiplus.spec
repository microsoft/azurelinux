# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#https://fedoraproject.org/wiki/Changes/Harden_All_Packages#Troubleshooting_steps_for_package_maintainers
%undefine _hardened_build

Name:           libgdiplus
Version:        6.1
Release: 11%{?dist}
Summary:        An Open Source implementation of the GDI+ API
License:        MIT
URL:            http://www.mono-project.com/Main_Page
Source0:        http://download.mono-project.com/sources/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  gcc gcc-c++
BuildRequires:  freetype-devel glib2-devel libjpeg-devel libtiff-devel
BuildRequires:  libpng-devel fontconfig-devel
BuildRequires:  cairo-devel giflib-devel libexif-devel
BuildRequires:  zlib-devel
BuildRequires: make

%description
An Open Source implementation of the GDI+ API, it is part of the Mono 
Project

%package devel
Summary: Development files for libgdiplus
Requires: %{name} = %{version}-%{release}

%description devel
Development files for libgdiplus

%prep
%setup -q

CFLAGS="$RPM_OPT_FLAGS -Wl,-z,lazy"
CXXFLAGS="$RPM_OPT_FLAGS -Wl,-z,lazy"

export CFLAGS
export CXXFLAGS

%build
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md TODO AUTHORS ChangeLog
%{_libdir}/lib*.so.*

%files devel
%{_libdir}/pkgconfig/*
%{_libdir}/lib*.so

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Nov 20 2021 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 6.1-1
- update to 6.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 04 2020 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 6.0.4-4
- add patch for drawing images

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov  8 2019 Tom Callaway <spot@fedoraproject.org> - 6.0.4-1
- update to 6.0.4

* Thu Aug 08 2019 Kentaro Ishii <sony.pcv.s520@gmail.com> - 5.6-5
- Fixes #1710587.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Apr 06 2018 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 5.6-1
- Updated to 5.6

* Sun Feb 11 2018 Sandro Mani <manisandro@gmail.com> - 4.2-7
- Rebuild (giflib)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 4.2-1
- Updated to 4.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 3.12-2
- Disable hardened_build that cause not build git, tiff and jpg support

* Tue Apr 14 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 3.12-1
- updated to 3.12
- Use %%license

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Dan Horák <dan[at]danny.cz> - 2.10.9-1
- updated to 2.10.9
- fix FTBFS (#1089734, #1037161)

* Mon Nov 25 2013 Björn Esser <bjoern.esser@gmail.com> - 2.10-11
- rebuilt for giflib-5.0.5 on rawhide
- removed BuildRequires: libungif-devel, since the package passed away
- fixed bogus date in %%changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.10-8
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.10-7
- rebuild against new libjpeg

* Fri Jul 27 2012 Christian Krause <chkr@fedoraproject.org> - 2.10-6
- Add patch to support linking against libpng 1.5 (BZ #843330)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.10-3
- Rebuild for new libpng

* Sun Mar 27 2011 Christian Krause <chkr@fedoraproject.org> - 2.10-2
- Update to official 2.10 release
- Move sources into lookaside cache

* Thu Feb 03 2011  Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.10-1
- Bump to 2.10 RC2

* Tue Nov 23 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.8.1-1
- Bump to bug fix release

* Thu Oct 14 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.8-2
- Correct URL
- Revert merge-review cleanup (#226009)

* Thu Oct 07 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.8-1.1
- Bump to full release

* Wed Sep 15 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.8-1
- Bump to review 3 of the 2.8 release
- Remove patch for CVE-2010-1526

* Tue Aug 24 2010 Christian Krause <chkr@fedoraproject.org> - 2.6.7-3
- Add upstream patch for CVE-2010-1526

* Sun Jul 25 2010 Christian Krause <chkr@fedoraproject.org> - 2.6.7-2
- Cleanup spec file

* Sat Jul 10 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6.7-1
- Update to 2.6.7 release candidate 1
- Add BR giflib-devel and libexif-devel

* Sun Jun 20 2010 Christian Krause <chkr@fedoraproject.org> - 2.6.4-2
- Cleanup spec file
- Remove removal of -Werror - not applicable anymore

* Tue Apr 27 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6.4-1
- Update to the 2.6.4 release
- URL and source locations fixed in spec file

* Wed Dec 16 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6-2
- Update to 2.6

* Wed Sep 30 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.6-1
- Update to 2.6 preview 1

* Mon Jun 22 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4,2-2
- bump to RC1

* Tue Jun 09 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4.2-1
- bump to 2.4.2 preview

* Thu Mar 26 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-5
- 2.4 release

* Tue Mar 17 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-4.RC3
- Bump to RC3

* Tue Mar 10 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-3.RC2
- Bump to RC2

* Fri Feb 27 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-2.RC1
- Bump to RC1 release
- Fixed source URL
- Returned from svn to official releases

* Mon Feb 02 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.4-1.pre1.20090202svn124838
- Update to svn
- retagged as 2.4 pre-release 1

* Sat Jan 10 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-4.RC1.20090104svn122354.1
- Rebuild

* Sun Jan 04 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-4.RC1.20090104svn122354
- Update to svn

* Wed Dec 24 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-4.RC1.20081224svn122059
- Bump to RC1 branched svn

* Wed Dec 10 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-3.pre2.20081012svn118228
- Update to svn

* Fri Dec 05 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-2.pre2
- Update to 2.2 preview 2

* Tue Nov 18 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.2-1.pre1
- Update to 2.2 preview 1

* Sat Oct 18 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-5
- fix the long standing symlink problem

* Fri Oct 03 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-4
- Bump to RC4

* Mon Sep 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-3
- Bump to RC3

* Tue Sep 09 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-2
- Bump to RC1

* Sat Aug 02 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 2.0-1
- Bump to preview 1
- Alter licence

* Thu Mar 06 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-4
- bump to preview 4

* Mon Feb 04 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.9-1
- bump to preview 1

* Tue Dec 11 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-2
- bump to preview 4

* Thu Nov 22 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.6-1
- bump to latest preview version

* Fri Oct 05 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.5-1
- bump to 1.2.5
- disabled static build
- added fontconfig-devel requirement

* Sat Apr 21 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.4-1
- bump

* Fri Jan 26 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.3-1
- bump

* Sat Dec 02 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.2-1
- bump

* Sat Nov 25 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.1-1
- bump

* Fri Nov 03 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2-1
- bump
- added post and postun
- put the .so file in the devel package

* Sat Sep 02 2006 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.1.17-1
- bump
- added devel package
- swapped the perl script into prep (where it should be!)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Jul  7 2006 Alexander Larsson <alexl@redhat.com> - 1.1.16-1
- update to 1.1.16

* Wed Jun  7 2006 Alexander Larsson <alexl@redhat.com> - 1.1.15-1
- Update to 1.1.15

* Wed Apr 26 2006 Alexander Larsson <alexl@redhat.com> - 1.1.13.6-2
- Upgrade to 1.1.13.6

* Fri Mar  3 2006 Christopher Aillon <caillon@redhat.com> - 1.1.13.4-1
- Update to 1.1.13.4

* Fri Feb 10 2006 Christopher Aillon <caillon@redhat.com> - 1.1.13.2-2
- Rebuild

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1.13.2-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Christopher Aillon <caillon@redhat.com> - 1.1.13.2-1
- Update to 1.1.13.2

* Fri Jan 13 2006 Alexander Larsson <alexl@redhat.com> - 1.1.13-1
- update to 1.1.13

* Wed Jan 11 2006 Alexander Larsson <alexl@redhat.com> 1.1.11-2
- Don't package debug info

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> - 1.1.11-1
- Update to 1.1.11

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> - 1.1.10-3
- Rebuild, fix gcc4 issue

* Thu Nov 17 2005 Alexander Larsson <alexl@redhat.com> 1.1.10-2
- Build on s390* also

* Thu Nov 17 2005 Alexander Larsson <alexl@redhat.com> - 1.1.10-1
- Initial version

