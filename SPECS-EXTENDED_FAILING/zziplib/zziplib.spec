Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: Lightweight library to easily extract data from zip files
Name: zziplib
Version: 0.13.69
Release: 8%{?dist}
License: LGPLv2+ or MPLv1.1
URL: http://zziplib.sourceforge.net/
Source: https://github.com/gdraheim/zziplib/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0: zziplib-0.13.69-multilib.patch

Patch1: CVE-2018-17828.patch
Patch2: CVE-2018-17828.part2.patch
Patch3: CVE-2018-16548.part1.patch
Patch4: CVE-2018-16548.part2.patch
Patch5: CVE-2018-16548.part3.patch

BuildRequires:  gcc
BuildRequires: perl-interpreter
BuildRequires: python2
BuildRequires: python2-rpm-macros
BuildRequires: zip
BuildRequires: xmlto
BuildRequires: zlib-devel
BuildRequires: SDL-devel
BuildRequires: pkgconfig
#BuildRequires: autoconf
#BuildRequires: automake

%description
The zziplib library is intentionally lightweight, it offers the ability to
easily extract data from files archived in a single zip file. Applications
can bundle files into a single zip archive and access them. The implementation
is based only on the (free) subset of compression with the zlib algorithm
which is actually used by the zip/unzip tools.

%package utils
Summary: Utilities for the zziplib library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
The zziplib library is intentionally lightweight, it offers the ability to
easily extract data from files archived in a single zip file. Applications
can bundle files into a single zip archive and access them. The implementation
is based only on the (free) subset of compression with the zlib algorithm
which is actually used by the zip/unzip tools.

This packages contains all the utilities that come with the zziplib library.

%package devel
Summary: Development files for the zziplib library
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: zlib-devel
Requires: SDL-devel

%description devel
The zziplib library is intentionally lightweight, it offers the ability to
easily extract data from files archived in a single zip file. Applications
can bundle files into a single zip archive and access them. The implementation
is based only on the (free) subset of compression with the zlib algorithm
which is actually used by the zip/unzip tools.

This package contains files required to build applications that will use the
zziplib library.

%prep
%setup -q

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# Force py2 for the build
find . -name '*.py' | xargs sed -i 's@#! /usr/bin/python@#! %__python2@g;s@#! /usr/bin/env python@#! %__python2@g'

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export PYTHON=%__python2
%configure \
    --disable-static \
    --enable-sdl \
    --enable-frame-pointer \
    --enable-builddir=_builddir
# Remove rpath on 64bit archs
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' */libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' */libtool
# Only patch generated _config.h on non-i686 and armv7hl
# These platforms have a correct _config.h already
%ifnarch i686 armv7hl
cd _builddir
%apply_patch %{PATCH0} -p2
cd ..
%endif

%{__make} %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%ldconfig_scriptlets

%files
%doc docs/COPYING* ChangeLog README TODO
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
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.13.69-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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

* Sat Dec  4 2010 Matthias Saou <http://freshrpms.net/> 0.13.59-1
- Update to 0.13.59.
- Remove no longer needed 'open' patch.
- Rebase the multilib patch, still required.
- Re-enable _smp_mflags, build works again with it apparently.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.49-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.49-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 Matthias Saou <http://freshrpms.net/> 0.13.49-6
- Patch _config.h to make it identical for 32bit and 64bit archs (#343521).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Wed Aug  8 2007 Matthias Saou <http://freshrpms.net/> 0.13.49-4
- Include patch to fix fd.open calls with recent glibc.
- Disable _smp_mflags since the docs fail to build.

* Fri Aug  3 2007 Matthias Saou <http://freshrpms.net/> 0.13.49-3
- Update License field.

* Tue Jun 19 2007 Matthias Saou <http://freshrpms.net/> 0.13.49-2
- Disable static lib build instead of excluding it later.
- Remove rpath on 64bit archs.
- Switch to using DESTDIR install method.

* Mon Mar 26 2007 Matthias Saou <http://freshrpms.net/> 0.13.49-1
- Update to 0.13.49 to fix CVE-2007-1614 (rhbz #233700).
- Include new man3 pages to the devel sub-package.

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 0.13.47-1
- Update to 0.13.47.
- FC6 rebuild.

* Mon Jul 24 2006 Matthias Saou <http://freshrpms.net/> 0.13.45-3
- Split off -utils sub-package (#199467). Could have been plain "zzip"?
- Have sub-packages require exact release too.
- Build require automake to make the aclocal-1.9 check happy.
- Use --enable-frame-pointer otherwise -g gets removed from the CFLAGS.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 0.13.45-2
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 0.13.45-1
- Update to 0.13.45.
- Exclude static library.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.13.38-2
- rebuild on all arches

* Tue Apr  5 2005 Matthias Saou <http://freshrpms.net/> 0.13.38-1
- Update to 0.13.38, fixes gcc4 compile issues (Adrian Reber).

* Tue Nov 16 2004 Matthias Saou <http://freshrpms.net/> 0.13.36-2
- Bump release to provide Extras upgrade path.

* Tue Jun  8 2004 Matthias Saou <http://freshrpms.net/> 0.13.36-1
- Initial RPM release.

