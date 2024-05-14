Summary:        Lightweight library to easily extract data from zip files
Name:           zziplib
Version:        0.13.72
Release:        3%{?dist}
License:        LGPLv2+ OR MPLv1.1
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://zziplib.sourceforge.net/
Source:         https://github.com/gdraheim/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  SDL-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-interpreter
BuildRequires:  pkgconfig
BuildRequires:  python3
BuildRequires:  python3-rpm-macros
BuildRequires:  xmlto
BuildRequires:  zip
BuildRequires:  zlib-devel

%description
The zziplib library is intentionally lightweight, it offers the ability to
easily extract data from files archived in a single zip file. Applications
can bundle files into a single zip archive and access them. The implementation
is based only on the (free) subset of compression with the zlib algorithm
which is actually used by the zip/unzip tools.

%package utils
Summary:        Utilities for the zziplib library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
The zziplib library is intentionally lightweight, it offers the ability to
easily extract data from files archived in a single zip file. Applications
can bundle files into a single zip archive and access them. The implementation
is based only on the (free) subset of compression with the zlib algorithm
which is actually used by the zip/unzip tools.

This packages contains all the utilities that come with the zziplib library.

%package devel
Summary:        Development files for the zziplib library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       SDL-devel
Requires:       pkgconfig
Requires:       zlib-devel

%description devel
The zziplib library is intentionally lightweight, it offers the ability to
easily extract data from files archived in a single zip file. Applications
can bundle files into a single zip archive and access them. The implementation
is based only on the (free) subset of compression with the zlib algorithm
which is actually used by the zip/unzip tools.

This package contains files required to build applications that will use the
zziplib library.

%prep
%autosetup -p1

%build
%cmake -B "%{_vpath_builddir}"

%make_build -C "%{_vpath_builddir}"

%install
%make_install -C "%{_vpath_builddir}"

%check
make test -C "%{_vpath_builddir}"

%ldconfig_scriptlets

%files
%license docs/COPYING*
%doc ChangeLog README TODO
%{_libdir}/*.so.*

%files utils
%{_bindir}/*

%files devel
%doc docs/README.SDL docs/*.htm
%{_includedir}/*
%exclude %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4
%{_mandir}/man3/*

%changelog
* Wed Dec 14 2022 Sumedh Sharma <sumsharma@microsoft.com> - 0.13.72-3
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License Verified

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Feb 09 2022 Alexander Bokovoy <abokovoy@redhat.com> - 0.13.72-1
- 0.13.72
- Fixes CVE-2020-18442
- Resolves: rhbz#1973831
- Switch build to CMake, drop 32-bit patches as checks integrated in CMake already

* Sat Feb 05 2022 Leigh Scott <leigh123linux@gmail.com> - 0.13.71-7
- Fix pkgconfig files

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.71-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 01 2021 Jakub Martisko <jamartis@redhat.com> - 0.13.71-5
- Use the multilib patches from RHEL
- Resolves ftbfs
Resolves: rhbz#1988061
Related: rhbz#1915747

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.71-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 01 2021 Jakub Martisko <jamartis@redhat.com> - 0.13.71-3
- Use python3 (versioned) as buildrequires

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Jakub Martisko <jamartis@redhat.com> - 0.13.71-1
- Rebase to 0.13.71
- Drop the CVE patches, they are now part of the upstream package
- Build no longer requires python2
- Resolves: 1807565

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.69-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 0.13.69-8
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.69-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.69-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.69-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 24 2019 Jakub Martisko <jamartis@redhat.com> - 0.13.69-4
- Add the missing CVE-2018-17828.part2.patch file
- Fix Formating of the previous 2 changelog entries

* Thu Jan 24 2019 Jakub Martisko <jamartis@redhat.com> - 0.13.69-3
- Related: #1626202
- Resolves: CVE-2018-16548

* Thu Jan 24 2019 Jakub Martisko <jamartis@redhat.com> - 0.13.69-2
- Related: 1635890
- Resolves: CVE-2018-17828

* Mon Jul 23 2018 Alexander Bokovoy <abokovoy@redhat.com> - 0.13.69-1
- Update to 0.13.69 release
- Fixes: #1598246 (CVE-2018-6541)
- Fixes: #1554673 (CVE-2018-7727)
- Use versioned python executables everywhere

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.68-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar 18 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.13.68-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 14 2018 Alexander Bokovoy <abokovoy@redhat.com> - 0.13.68-1
- 0.13.68
- Fixes: #1543942 (CVE-2018-6484)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 01 2018 Alexander Bokovoy <abokovoy@redhat.com> - 0.13.67-1
- Update release
- CVE-2018-6381

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.62-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.62-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.62-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.62-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.62-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.62-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.62-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jan 30 2013 Jindrich Novy <jnovy@redhat.com> 0.13.62-2
- rebuild with -fno-strict-aliasing

* Wed Oct 10 2012 Matthias Saou <matthias@saou.eu> 0.13.62-1
- Update to 0.13.62.
- Remove no longer needed -Wl patch.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar  8 2012 Tom Callaway <spot@fedoraproject.org> - 0.13.60-1
- update to 0.13.60

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.59-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  9 2010 Hans de Goede <hdegoede@redhat.com> 0.13.59-2
- Fix broken zzip/_config.h which causes apps using zziplib to fail to compile

* Sat Dec  4 2010 Matthias Saou <https://freshrpms.net/> 0.13.59-1
- Update to 0.13.59.
- Remove no longer needed 'open' patch.
- Rebase the multilib patch, still required.
- Re-enable _smp_mflags, build works again with it apparently.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.49-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.49-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Matthias Saou <https://freshrpms.net/> 0.13.49-6
- Patch _config.h to make it identical for 32bit and 64bit archs (#343521).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Wed Aug  8 2007 Matthias Saou <https://freshrpms.net/> 0.13.49-4
- Include patch to fix fd.open calls with recent glibc.
- Disable _smp_mflags since the docs fail to build.

* Fri Aug  3 2007 Matthias Saou <https://freshrpms.net/> 0.13.49-3
- Update License field.

* Tue Jun 19 2007 Matthias Saou <https://freshrpms.net/> 0.13.49-2
- Disable static lib build instead of excluding it later.
- Remove rpath on 64bit archs.
- Switch to using DESTDIR install method.

* Mon Mar 26 2007 Matthias Saou <https://freshrpms.net/> 0.13.49-1
- Update to 0.13.49 to fix CVE-2007-1614 (rhbz #233700).
- Include new man3 pages to the devel sub-package.

* Mon Aug 28 2006 Matthias Saou <https://freshrpms.net/> 0.13.47-1
- Update to 0.13.47.
- FC6 rebuild.

* Mon Jul 24 2006 Matthias Saou <https://freshrpms.net/> 0.13.45-3
- Split off -utils sub-package (#199467). Could have been plain "zzip"?
- Have sub-packages require exact release too.
- Build require automake to make the aclocal-1.9 check happy.
- Use --enable-frame-pointer otherwise -g gets removed from the CFLAGS.

* Mon Mar  6 2006 Matthias Saou <https://freshrpms.net/> 0.13.45-2
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <https://freshrpms.net/> 0.13.45-1
- Update to 0.13.45.
- Exclude static library.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.13.38-2
- rebuild on all arches

* Tue Apr  5 2005 Matthias Saou <https://freshrpms.net/> 0.13.38-1
- Update to 0.13.38, fixes gcc4 compile issues (Adrian Reber).

* Tue Nov 16 2004 Matthias Saou <https://freshrpms.net/> 0.13.36-2
- Bump release to provide Extras upgrade path.

* Tue Jun  8 2004 Matthias Saou <https://freshrpms.net/> 0.13.36-1
- Initial RPM release.
