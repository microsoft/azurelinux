Summary:        Color Management Engine
Name:           lcms2
Version:        2.13.1
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.littlecms.com/
Source0:        https://github.com/mm2/Little-CMS/archive/refs/tags/lcms%{version}.tar.gz#/Little-CMS-lcms%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  zlib-devel

%description
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form. LCMS2 is the current version of LCMS, and can be
parallel installed with the original (deprecated) lcms.

%package        utils
Summary:        Utility applications for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    utils
The %{name}-utils package contains utility applications for %{name}.

%package        devel
Summary:        Development files for LittleCMS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       littlecms-devel = %{version}-%{release}

%description    devel
Development files for LittleCMS.

%prep
%autosetup -p1 -n Little-CMS-lcms%{version}

%build
%configure \
  --disable-static \
  --program-suffix=2

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install

find %{buildroot} -type f -name "*.la" -delete -print

%check
%make_build check -k ||:

%ldconfig_scriptlets

%files
%doc AUTHORS
%license COPYING
%{_libdir}/liblcms2.so.2*

%files utils
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%{_includedir}/lcms2*.h
%{_libdir}/liblcms2.so
%{_libdir}/pkgconfig/lcms2.pc

%changelog
* Fri Mar 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.13.1-2
- Bumping release to re-build with newer 'libtiff' libraries.

* Wed Apr 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.13.1-1
- Updating to 2.13.1.
- Fixing source URL.

* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.9-9
- License verified
- Lint spec

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.9-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 18 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.9-4
- CVE-2018-16435 lcms2: heap-based buffer overflow in SetData function in cmsIT8LoadFromFile (#1628969)
- .spec cosmetics, use %%make_build %%make_install %%ldconfig_scriptlets

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.9-1
- lcms2-2.9 (#1512518), .spec cosmetics/modernization

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.8-2
- lcms2: Out-of-bounds read in Type_MLU_Read() (#1367357)

* Mon Jul 25 2016 Richard Hughes <richard@hughsie.com> - 2.8-1
- Update to new upstream version.

* Wed Mar 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.7-4
- %%files: less globs, use %%license
- tighten subpkg deps
- -devel: use %%doc
- use %%version in Source URL
- simplify %%setup
- %%check: make check

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 22 2015 Richard Hughes <richard@hughsie.com> - 2.7-1
- Update to new upstream version.

* Tue Mar 17 2015 Richard Hughes <richard@hughsie.com> - 2.7-0.1rc3
- Update to new upstream RC version.

* Thu Feb 05 2015 Richard Hughes <richard@hughsie.com> - 2.7-0.1rc1
- Update to new upstream version.
- Added a flag  to clip negative values in unbounded transforms
- Added a global optimization that merges consecutive matrices in pipelines.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Brent Baude <baude@us.ibm.com> - 2.6-2
- Correct assumption about ppc64 endianess

* Mon Mar 17 2014 Richard Hughes <richard@hughsie.com> 2.6-1
- Update to new upstream version.
- Added a way to retrieve matrix shaper always, no matter LUT is present
- Added pthread dependency
- Big revamp on Contexts, from Artifex
- Fixed a bug in PCS/Colorspace order when reading V2 Lab devicelinks
- Fixed some indexing out of bounds in floating point interpolation
- Fix for delete tag memory corruption
- New locking plug-in, from Artifex

* Wed Feb 19 2014 Richard Hughes <richard@hughsie.com> 2.6-0.1.rc3
- Update to new prerelease upstream version.

* Fri Feb 14 2014 Richard Hughes <richard@hughsie.com> 2.6-0.1.rc1
- Update to new prerelease upstream version.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 01 2013 Richard Hughes <richard@hughsie.com> 2.5-1
- Update to new upstream version.
- Added a reference for Mac MLU tag
- Added a way to read the profile creator from header
- Added error descriptions on cmsSmoothToneCurve
- Added identity curves support for write V2 LUT
- Added new cmsPlugInTHR() and fixed some race conditions
- Added TIFF Lab16 handling on tifficc
- Fixed a bug on big endian platforms not supporting uint64 or long long.
- Fixed a multithead bug on optimization
- Fixed devicelink generation for 8 bits
- Fixed some 64 bit warnings on size_t to uint32 conversions
- Rendering intent used when creating the transform is now propagated to profile
- RGB profiles store only one copy of the curve to save space
- Transform2Devicelink now keeps white point when guessing deviceclass is enabled
- Update black point detection algorithm to reflect ICC changes
- User defined parametric curves can now be saved in ICC profiles

* Thu Jun 27 2013 Richard Hughes <richard@hughsie.com> 2.5-0.2
- Update to new release candidate version.

* Thu May 30 2013 Richard Hughes <richard@hughsie.com> 2.5-0.1
- Update to new release candidate version.

* Thu Apr 25 2013 Tim Waugh <twaugh@redhat.com> - 2.4-6
- Applied upstream fixes for threading (bug #951984).

* Thu Mar  7 2013 Tim Waugh <twaugh@redhat.com> - 2.4-5
- Added upstream fix for threading issue with plugin registration
  (bug #912307).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.4-3
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.4-2
- rebuild against new libjpeg

* Sat Sep 15 2012 Richard Hughes <richard@hughsie.com> 2.4-1
- Update to new upstream version.
- Black point detection from the algorithm disclosed by Adobe
- Added support for transforms on planar data with different stride
- Added a new plug-in type for optimizing full transforms
- Linear (gamma 1.0) profiles can now operate in unbounded mode
- Added "half" float support

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 10 2011 Richard Hughes <richard@hughsie.com> 2.3-1
- Update to new upstream version which incorporates many bugfixes.

* Fri Jun 10 2011 Richard Hughes <richard@hughsie.com> 2.2-2
- Actually update the sources...

* Fri Jun 10 2011 Richard Hughes <richard@hughsie.com> 2.2-1
- Update to new upstream version
- Stability and efficienty fixes
- Adds support for dictionary metatag

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 01 2010 Richard Hughes <richard@hughsie.com> 2.1-1
- Update to new upstream version.

* Fri Jun 18 2010 Richard Hughes <richard@hughsie.com> 2.0a-3
- Address some more review comments.
- Resolves #590387

* Fri Jun 18 2010 Richard Hughes <richard@hughsie.com> 2.0a-2
- Address some review comments.
- Resolves #590387

* Fri Jun 18 2010 Richard Hughes <richard@hughsie.com> 2.0a-1
- Initial package for Fedora review
