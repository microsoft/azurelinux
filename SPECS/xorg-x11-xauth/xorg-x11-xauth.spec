%global pkgname xauth

Summary:        X.Org X11 X authority utilities
Name:           xorg-x11-%{pkgname}
Version:        1.1
Release:        7%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.x.org
Source0:        https://www.x.org/pub/individual/app/%{pkgname}-%{version}.tar.bz2

BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXau-devel
BuildRequires:  libXext-devel
BuildRequires:  libXmu-devel
BuildRequires:  pkg-config

Provides:       xauth = %{version}-%{release}

%description
xauth is used to edit and display the authorization information
used in connecting to an X server.

%prep
%autosetup -n %{pkgname}-%{version}

%build
%configure
%make_build

%install
%make_install

# Removing documentation.
rm -r %{buildroot}%{_mandir}/man1/xauth.1*

%files
%license COPYING
%doc README.md
%{_bindir}/xauth

%changelog
* Wed Oct 27 2021 Muhammad Falak <mwani@microsft.com> - 1.1-7
- Remove epoch

* Mon Jan 25 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:1.1-6
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- License verified.
- Removed documentation.
- Removed the %%check section as it depended on a dead/orphaned 'cmdtest' package.
  See here for details: https://src.fedoraproject.org/rpms/cmdtest/tree/master.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 1:1.1-4
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Adam Jackson <ajax@redhat.com> - 1:1.1-1
- xauth 1.1

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 19 2018 Adam Jackson <ajax@redhat.com> - 1.0.9-12
- Nerf the python-related BuildRequires. They're only needed for 'make check',
  and cmdtest is not yet a python3 package.

* Mon Feb 19 2018 Peter Hutterer <peter.hutterer@redhat.com> 1:1.0.9-11
- Add BR for automake and gcc

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 08 2017 Adam Jackson <ajax@redhat.com> - 1.0.9-9
- BuildRequires: python-markdown to fix 'make check'

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1:1.0.9-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul  3 2014 Hans de Goede <hdegoede@redhat.com> - 1:1.0.9-1
- Rebase to 1.0.9 (rhbz#1018603)
- Fixes ssh -Y failure from remote GDM session (rhbz#505545)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 11 2012 Adam Jackson <ajax@redhat.com> 1.0.7-1
- xauth 1.0.7 (#806308)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 11 2011 Matěj Cepl <mcepl@redhat.com> - 1.0.6-2
- Removed mkxauth with an extreme prejudice.

* Tue Jun 21 2011 Adam Jackson <ajax@redhat.com> 1.0.6-1
- xauth 1.0.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 30 2010 Adam Jackson <ajax@redhat.com> 1.0.2-8
- Merge review cleanups (#226648)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.2-5
- Fix license tag

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.0.2-4
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1:1.0.2-3
- Rebuild for build id

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> 1:1.0.2-2
- Don't install INSTALL

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1:1.0.2-1.fc7
- Update to 1.0.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-2
- Add missing documentation to doc manifest.
- Use "make install" instead of makeinstall macro.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1:1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1:1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-1
- Updated to xauth 1.0.1 from X11R7.0

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1:1.0.0-1
- Updated to xauth 1.0.0 from X11R7 RC4
- Changed manpage dir from man1x to man1 to match upstream default.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 1:0.99.2-1
- Updated to xauth 0.99.2 from X11R7 RC2
- Added Epoch 1 to package, to be able to change the version number from the
  X11R7 release number to the actual twm version.
- Rename mkxauth manpage to mkxauth.1x

* Mon Oct 31 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.0-3
- Updated to xauth 0.99.1 from X11R7 RC1
- Change manpage location to 'man1x' in file manifest

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.0-2
- Use Fedora-Extras style BuildRoot tag
- Update BuildRequires to use new library package names

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.0-1
- Initial build.
