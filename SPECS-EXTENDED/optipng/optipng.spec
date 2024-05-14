Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           optipng
Version:        0.7.7
Release:        7%{?dist}
Summary:        PNG optimizer and converter

License:        zlib
URL:            https://optipng.sourceforge.net/
Source0:        https://downloads.sourceforge.net/optipng/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  zlib-devel libpng-devel

%description
OptiPNG is a PNG optimizer that recompresses image files to a smaller size,
without losing any information. This program also converts external formats
(BMP, GIF, PNM and TIFF) to optimized PNG, and performs PNG integrity checks
and corrections.


%prep
%setup -q
for f in AUTHORS.txt doc/history.txt ; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f
done

# Ensure system libs and headers are used; as of 0.6.3 pngxtern will use
# the bundled headers if present even with -with-system-*, causing failures.
rm -rf src/libpng src/zlib


%build
%set_build_flags
./configure -prefix=%{_prefix} -mandir=%{_mandir} \
    -with-system-zlib -with-system-libpng
%make_build


%install
rm -rf $RPM_BUILD_ROOT
%make_install
chmod -c 755 $RPM_BUILD_ROOT%{_bindir}/optipng


%check
%__make test


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc AUTHORS.txt README.txt doc/*
%{_bindir}/optipng
%{_mandir}/man1/optipng.1*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.7-7
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Thu Dec 10 2020 Peter Hanecak <hany@hany.sk> - 0.7.7-6
- Use make macros (PR from  tbaeder)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Peter Hanecak <hany@hany.sk> - 0.7.7-1
- Update to 0.7.7
- Dropped pathes (both CVEs fixed in 0.7.7)
- Added BuildRequires: gcc
  (https://fedoraproject.org/wiki/Changes/Remove_GCC_from_BuildRoot)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 04 2017 Till Maas <opensource@till.name> - 0.7.6-6
- Actually apply patches

* Mon Dec 04 2017 Till Maas <opensource@till.name> - 0.7.6-5
- Add patches for CVE-2017-1000229 and CVE-2017-16938
- Cleanup spec

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Apr  5 2016 Ville Skyttä <ville.skytta@iki.fi> - 0.7.6-1
- Update to 0.7.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Ville Skyttä <ville.skytta@iki.fi> - 0.7.5-6
- Remove unnecessary %%defattr

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 31 2015 Ville Skyttä <ville.skytta@iki.fi> - 0.7.5-4
- Ship LICENSE.txt as %%license where available

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 26 2014 Ville Skyttä <ville.skytta@iki.fi> - 0.7.5-1
- Update to 0.7.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 22 2012 Ville Skyttä <ville.skytta@iki.fi> - 0.7.4-1
- Update to 0.7.4.

* Mon Sep 17 2012 Ville Skyttä <ville.skytta@iki.fi> - 0.7.3-1
- Update to 0.7.3.

* Sat Aug 25 2012 Ville Skyttä <ville.skytta@iki.fi> - 0.7.2-1
- Update to 0.7.2.
- Build unit test code with $RPM_(OPT|LD)_FLAGS.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 24 2012 Ville Skyttä <ville.skytta@iki.fi> - 0.7.1-1
- Update to 0.7.1.

* Fri Mar  2 2012 Ville Skyttä <ville.skytta@iki.fi> - 0.7-1
- Update to 0.7.
- Build with $RPM_LD_FLAGS.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.6.5-2
- Rebuild for new libpng

* Thu Apr 28 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.6.5-1
- Update to 0.6.5.
- Patch to fix setjmp.h duplicate inclusion with system libpng.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat May 15 2010 Till Maas <opensource@till.name> - 0.6.4-1
- update to new release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 19 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.6.3-1
- Update to 0.6.3.
- Use %%global instead of %%define.

* Wed Feb 25 2009 Till Maas <opensource@till.name> - 0.6.2.1-1
- Update to new release to fix array overflow
- Red Hat Bugzilla #487364

* Wed Nov 12 2008 Till Maas <opensource@till.name> - 0.6.2-1
- Update to new release to fix buffer overflow
- Red Hat Bugzilla #471206

* Thu Aug 28 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.6.1-1
- 0.6.1.

* Thu Feb 14 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.5.5-4
- Apply sf.net patch #1790969 to fix crash with -log.
- Cosmetic specfile changes.

* Thu Aug 02 2007 Till Maas <opensource till name> - 0.5.5-3
- update License: Tag according to new Guidelines

* Wed Feb 14 2007 Till Maas <opensource till name> - 0.5.5-2
- rebuild because of new libpng

* Tue Feb 06 2007 Till Maas <opensource till name> - 0.5.5-1
- Version bump

* Wed Nov 29 2006 Till Maas <opensource till name> - 0.5.4-4
- splitting makefile patches
- make LDFLAGS=$RPM_OPT_FLAGS
- Use own makefile define
- Fixing 216784 with upstream patch

* Wed Oct 11 2006 Till Maas <opensource till name> - 0.5.4-3
- bumping release because of errors while importing to extras

* Tue Oct 10 2006 Till Maas <opensource till name> - 0.5.4-2
- shortening Summary

* Thu Sep 14 2006 Till Maas <opensource till name> - 0.5.4-1
- version bump
- use system zlib and libpng
- link without "-s" flag for non-empty debuginfo
- use DESTDIR

* Fri Jul 28 2006 Till Maas <opensource till name> - 0.5.3-1
- version bump
- Changed license tag back to zlib/libpng (#198616 rpmlint) 
- use $RPM_OPT_FLAGS instead of %%{optflags}

* Thu Jul 06 2006 Till Maas <opensource till name> - 0.5.2-2
- Changed license tag from zlib/libpng to zlib

* Tue Jul 04 2006 Till Maas <opensource till name> - 0.5.2-1
- Created from scratch for fedora extras
