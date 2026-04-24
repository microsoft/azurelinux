# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# ifdef'd in source code but runtime dep will be made for FT_Done_MM_Var symbol in freetype-2.9.1
# so update the build deps as well to keep deps consistency between runtime and build time.
%global freetype_version 2.9.1

Summary:	Font configuration and customization library
Name:		fontconfig
Version:	2.17.0
Release: 4%{?dist}
# src/ftglue.[ch] is in Public Domain
# src/fccache.c contains Public Domain code
## https://gitlab.com/fedora/legal/fedora-license-data/-/issues/177
# fc-case/CaseFolding.txt is in the UCD
# otherwise MIT
License:	HPND AND LicenseRef-Fedora-Public-Domain AND Unicode-DFS-2016
Source:		http://fontconfig.org/release/%{name}-%{version}.tar.xz
URL:		http://fontconfig.org
Source1:	25-no-bitmap-fedora.conf
Source2:	fc-cache

# https://bugzilla.redhat.com/show_bug.cgi?id=140335
Patch0:		%{name}-sleep-less.patch
Patch4:		%{name}-drop-lang-from-pkgkit-format.patch
Patch5:		%{name}-disable-network-required-test.patch
Patch6:		%{name}-lower-nonlatin-conf.patch
Patch7:		%{name}-fix-crash.patch

BuildRequires:	libxml2-devel
BuildRequires:	freetype-devel >= %{freetype_version}
BuildRequires:	fontpackages-devel
BuildRequires:	gettext
BuildRequires:	gperf
BuildRequires:  docbook-utils docbook-utils-pdf
BuildRequires:  meson ninja-build gcc

Requires:	fonts-filesystem freetype
# Register DTD system-wide to make validation work by default
# (used by fonts-rpm-macros)
Requires(pre):    xml-common
Requires(postun): xml-common
PreReq:		freetype >= 2.9.1-6
Requires(post):	grep coreutils
Requires:	font(:lang=en)
Suggests:	font(notosans)

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by 
applications.

%package	devel
Summary:	Font configuration and customization library
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	freetype-devel >= %{freetype_version}
Requires:	pkgconfig
Requires:	gettext

%description	devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which 
will use fontconfig.

%package	devel-doc
Summary:	Development Documentation files for fontconfig library
BuildArch:	noarch
Requires:	%{name}-devel = %{version}-%{release}

%description	devel-doc
The fontconfig-devel-doc package contains the documentation files
which is useful for developing applications that uses fontconfig.

%prep
%autosetup -p1
# To reduce a maintenance cost of fontconfig-lower-nonlatin-conf.patch
mv conf.d/65-nonlatin.conf conf.d/69-nonlatin.conf

%build
%meson -Ddoc=disabled -Dcache-build=disabled -Dxml-backend=libxml2 \
       -Dadditional-fonts-dirs=/usr/share/X11/fonts/Type1,/usr/share/X11/fonts/TTF,/usr/local/share/fonts \
       -Dcache-dir=/usr/lib/fontconfig/cache \
       --default-library=shared
%meson_build

%install
%meson_install

install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s %{_fontconfig_templatedir}/25-unhint-nonlatin.conf $RPM_BUILD_ROOT%{_fontconfig_confdir}/

# Use implied value to allow the use of conditional conf
rm $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d/10-sub-pixel-*.conf

# Do not enable bitmap-related conf
rm $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d/70-*bitmaps*.conf

# Install docs manually
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -d $RPM_BUILD_ROOT%{_mandir}/man3
install -d $RPM_BUILD_ROOT%{_mandir}/man5
for f in doc/*.1; do
  install -p -m 0644 $f $RPM_BUILD_ROOT%{_mandir}/man1
done
for f in doc/*.3; do
  install -p -m 0644 $f $RPM_BUILD_ROOT%{_mandir}/man3
done
for f in doc/*.5; do
  install -p -m 0644 $f $RPM_BUILD_ROOT%{_mandir}/man5
done
for f in doc/*.txt doc/*.pdf doc/*.html; do
  install -p -m 0644 $f .
done

# adjust the timestamp to avoid conflicts for multilib
touch -r doc/fontconfig-user.sgml fontconfig-user.txt
touch -r doc/fontconfig-user.sgml fontconfig-user.html
touch -r doc/fontconfig-devel.sgml fontconfig-devel.txt
touch -r doc/fontconfig-devel.sgml fontconfig-devel.html

# rename fc-cache binary
mv $RPM_BUILD_ROOT%{_bindir}/fc-cache $RPM_BUILD_ROOT%{_bindir}/fc-cache-%{__isa_bits}

# create link to man page
echo ".so man1/fc-cache.1" > $RPM_BUILD_ROOT%{_mandir}/man1/fc-cache-%{__isa_bits}.1

install -p -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/fc-cache

%find_lang %{name}
%find_lang %{name}-conf
cat %{name}-conf.lang >> %{name}.lang

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%meson_test

%post
umask 0022

mkdir -p /usr/lib/fontconfig/cache

[[ -d %{_localstatedir}/cache/fontconfig ]] && rm -rf %{_localstatedir}/cache/fontconfig/* 2> /dev/null || :

# Force regeneration of all fontconfig cache files
# The check for existance is needed on dual-arch installs (the second
#  copy of fontconfig might install the binary instead of the first)
# The HOME setting is to avoid problems if HOME hasn't been reset
if [ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache --version 2>&1 | grep -q %{version} ; then
  HOME=/root /usr/bin/fc-cache -f
fi

%transfiletriggerin -- /usr/share/fonts /usr/share/X11/fonts/Type1 /usr/share/X11/fonts/TTF /usr/local/share/fonts
HOME=/root /usr/bin/fc-cache -s

%transfiletriggerpostun -- /usr/share/fonts /usr/share/X11/fonts/Type1 /usr/share/X11/fonts/TTF /usr/local/share/fonts
HOME=/root /usr/bin/fc-cache -s

%posttrans
if [ -e %{_sysconfdir}/xml/catalog ]; then
  %{_bindir}/xmlcatalog --noout --add system \
                        "urn:fontconfig:fonts.dtd" \
                        "file://%{_datadir}/xml/fontconfig/fonts.dtd" \
                        %{_sysconfdir}/xml/catalog
fi

%postun
if [ $1 == 0 ] && [ -e %{_sysconfdir}/xml/catalog ]; then
  %{_bindir}/xmlcatalog --noout --del "urn:fontconfig:fonts.dtd" %{_sysconfdir}/xml/catalog
fi

%files -f %{name}.lang
%doc README.md AUTHORS
%doc fontconfig-user.txt fontconfig-user.html
%doc %{_fontconfig_confdir}/README
%license COPYING
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-cache*
%{_bindir}/fc-cat
%{_bindir}/fc-conflist
%{_bindir}/fc-list
%{_bindir}/fc-match
%{_bindir}/fc-pattern
%{_bindir}/fc-query
%{_bindir}/fc-scan
%{_bindir}/fc-validate
%{_fontconfig_templatedir}/*.conf
%{_datadir}/xml/fontconfig
# fonts.conf is not supposed to be modified.
# If you want to do so, you should use local.conf instead.
%config %{_fontconfig_masterdir}/fonts.conf
%config(noreplace) %{_fontconfig_confdir}/*.conf
%dir /usr/lib/fontconfig
%dir /usr/lib/fontconfig/cache
%{_mandir}/man1/*
%{_mandir}/man5/*

%files devel
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig
%{_mandir}/man3/*
%{_datadir}/gettext/its/fontconfig.its
%{_datadir}/gettext/its/fontconfig.loc

%files devel-doc
%doc fontconfig-devel.txt fontconfig-devel.html

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 30 2025 Akira TAGOH <tagoh@redhat.com> - 2.17.0-2
- Backport a patch to fix a crash with Graphite fonts
- Drop 70-*bitmaps*.conf from /etc/fonts/conf.d so far.
  Resolves: rhbz#2375426

* Fri Jun 27 2025 Akira TAGOH <tagoh@redhat.com> - 2.17.0-1
- New upstream release.
  Resolves: rhbz#2375126

* Fri Apr 11 2025 Akira TAGOH <tagoh@redhat.com> - 2.16.2-1
- New upstream release.

* Thu Mar 13 2025 Akira TAGOH <tagoh@redhat.com> - 2.16.1-1
- New upstream release.

* Mon Jan 27 2025 Akira TAGOH <tagoh@redhat.com> - 2.16.0-2
- Fix endian detection.
  Resolves: rhbz#2341757

* Sat Jan 18 2025 Akira TAGOH <tagoh@redhat.com> - 2.16.0-1
- New upstream release.
  Resolves: rhbz#2338618
- Use meson instead of autotools to build.
- Disable meson test on s390x temporarily.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug  1 2024 Akira TAGOH <tagoh@redhat.com> - 2.15.0-8
- Fix a memory leak and potentially uninitialized values.

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun  7 2024 Akira TAGOH <tagoh@redhat.com> - 2.15.0-6
- Own /usr/lib/fontconfig
  Resolves: rhbz#2284076

* Mon Apr 29 2024 Michael Kuhn <suraia@fedoraproject.org> - 2.15.0-5
- Fix emoji fonts being disabled when bitmap fonts were disabled

* Sat Feb 10 2024 Akira TAGOH <tagoh@redhat.com> - 2.15.0-4
- Delete .uuid with fc-cache -f.
  Resolves: rhbz#1761885

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 22 2023 Akira TAGOH <tagoh@redhat.com> - 2.15.0-1
- New upstream release.
  Resolves: rhbz#2255623

* Thu Aug 17 2023 Akira TAGOH <tagoh@redhat.com> - 2.14.2-5
- Update 65-nonlatin.conf to 69-nonlatin.conf
  This basically provides substitutes for certain languages and is helpful
  to determine default behavior though, we have per-package config for similar purpose.
  Since 65 is mostly used for default fonts and this config prevents some behavior for
  packages named something coming later than "nonlatin" in the alphabetical order.
  So moving this to the safer priority.
  This would fixes an issue, particularly Lohit Marathi vs Lohit Devanagari after
  updating their priorities from 65 to 66.

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Akira TAGOH <tagoh@redhat.com> - 2.14.2-3
- Drop 10-sub-pixel-rgb-for-kde.conf
  Resolves: rhbz#2212512

* Tue Apr  4 2023 Akira TAGOH <tagoh@redhat.com> - 2.14.2-2
- Migrated license tag to SPDX.

* Fri Jan 27 2023 Akira TAGOH <tagoh@redhat.com> - 2.14.2-1
- New upstream release.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Nov 26 2022 Akira TAGOH <tagoh@redhat.com> - 2.14.1-2
- Enable RGB stripes layout for sub-pixel rendering on KDE only.
  Resolves: rhbz#2137825

* Fri Oct 21 2022 Akira TAGOH <tagoh@redhat.com> - 2.14.1-1
- New upstream release.

* Wed Sep 28 2022 Akira TAGOH <tagoh@redhat.com> - 2.14.0-3
- Remap font paths to other place properly.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Mar 31 2022 Akira TAGOH <tagoh@redhat.com> - 2.14.0-1
- New upstream release.

* Fri Feb  4 2022 Akira TAGOH <tagoh@redhat.com> - 2.13.96-1
- New upstream release.
- Fix missing a file in the archive.
  Resolves: rhbz#2050478

* Tue Feb  1 2022 Akira TAGOH <tagoh@redhat.com> - 2.13.95-1
- New upstream release.
- Update deps to font(notosans)
  https://fedoraproject.org/wiki/Changes/DefaultToNotoFonts

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.94-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.94-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Akira TAGOH <tagoh@redhat.com> - 2.13.94-2
- Fix the score calculation on matching for multiple values.
- Enable 11-lcdfilter-default.conf.
  Resolves: rhbz#1965684

* Tue Jun 29 2021 Akira TAGOH <tagoh@redhat.com> - 2.13.94-1
- New upstream release.

* Thu Mar 25 2021 Akira TAGOH <tagoh@redhat.com> - 2.13.93-6
- Fix postun scriptlet to remove the entry from xml catalog.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.93-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 23 2020 Akira TAGOH <tagoh@redhat.com> - 2.13.93-4
- cherry pick some upstream patches
  - Skip leading white space in style.
  - Remove abort from FcCompareSize.
  - Fix memory leaks
  - Check qual and compare for family tests.
- 
* Thu Dec  3 2020 Akira TAGOH <tagoh@redhat.com> - 2.13.93-3
- Add back fullname property at the scan matching phase for the backward compatibility.
  Resolves: rhbz#1902881

* Mon Nov 30 2020 Akira TAGOH <tagoh@redhat.com> - 2.13.93-2
- Fix file conflicts.

* Sat Nov 28 2020 Akira TAGOH <tagoh@redhat.com> - 2.13.93-1
- New upstream release.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.92-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 23 2020 Akira TAGOH <tagoh@redhat.com> - 2.13.92-11
- deal with system caches as always latest on Silverblue. (#1750891)

* Thu Apr 02 2020 Akira TAGOH <tagoh@redhat.com> - 2.13.92-10
- Build against libxml2 instead of expat.

* Sat Mar 28 2020 Nicolas Mailhot <nim@fedoraproject.org> - 2.13.92-9
- Fix DTD declaration and registration so users and Fedora automation can
  easily validate new configuration files

* Mon Mar 23 2020 Akira TAGOH <tagoh@redhat.com> - 2.13.92-8
- Fix assertion in FcCacheFini() again.
  Resolves: rhbz#1815684

* Wed Feb 26 2020 Akira TAGOH <tagoh@redhat.com> - 2.13.92-7
- Fix assertion in FcCacheFini().

* Thu Jan 30 2020 Akira TAGOH <tagoh@redhat.com> - 2.13.92-6
- Fix some wrong behavior with sysroot option.
- Fix reading the outdated caches.
- Apply a patch to make it MT-safe more.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.92-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Akira TAGOH <tagoh@redhat.com> - 2.13.92-4
- Drop font(:lang=...) from %%{=pkgkit} format.
  Reference: rhbz#1792463

* Wed Aug 28 2019 Akira TAGOH <tagoh@redhat.com> - 2.13.92-3
- Do not return false on FcConfigParseAndLoad*() if complain is set to false.
  Resolves: rhbz#1744377

* Fri Aug  9 2019 Akira TAGOH <tagoh@redhat.com> - 2.13.92-2
- Fix to affect fonthashint property for score on match.

* Fri Aug  9 2019 Akira TAGOH <tagoh@redhat.com> - 2.13.92-1
- New upstream release.

* Wed Jul 31 2019 Akira TAGOH <tagoh@redhat.com> - 2.13.91-4
- Fix make check fails.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 16 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 2.13.91-2
- Remove calls to ldconfig from scriptlets
- Use "PreReq" instead of "Requires(pre)" for freetype

* Mon Jun 10 2019 Akira TAGOH <tagoh@redhat.com> - 2.13.91-1
- New upstream release.

* Fri Feb 22 2019 Akira TAGOH <tagoh@redhat.com> - 2.13.1-6
- Update freetype version for runtime dependency to ensure
  they have FT_Done_MM_Var symbol certainly. (#1679619)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 13 2018 Akira TAGOH <tagoh@redhat.com> - 2.13.1-4
- Use Rachana instead of Meera for serif subsitution. (#1649184)

* Wed Nov 07 2018 Akira TAGOH <tagoh@redhat.com> - 2.13.1-3
- Stop cleaning up .uuid file even when a directory is empty.

* Wed Sep 26 2018 Akira TAGOH <tagoh@redhat.com> - 2.13.1-2
- Add man page for fc-cache-* links to fc-cache.
- Drop unnecessary BR.

* Thu Aug 30 2018 Akira TAGOH <tagoh@redhat.com> - 2.13.1-1
- New upstream release.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Akira TAGOH <tagoh@redhat.com> - 2.13.0-7
- Use ldconfig rpm macro.

* Thu Jun 07 2018 Akira TAGOH <tagoh@redhat.com> - 2.13.0-6
- Add Suggests: dejavu-sans-fonts to address pulling the unpredicted
  font package as dependency. (#1321551)

* Wed Jun 06 2018 Akira TAGOH <tagoh@redhat.com> - 2.13.0-5
- Update the version deps of freetype to resolve FT_Done_MM_Var symbol. (#1579464)

* Fri May 11 2018 Akira TAGOH <tagoh@redhat.com> - 2.13.0-4
- Fix the emboldening logic. (#1575649)

* Thu Mar 15 2018 Akira TAGOH <tagoh@redhat.com> - 2.13.0-3
- Another fix to accept the const names in param.
- Fix locale issue.

* Mon Mar 12 2018 Akira TAGOH <tagoh@redhat.com> - 2.13.0-2
- Allow the const names in the range.

* Tue Mar 06 2018 Akira TAGOH <tagoh@redhat.com> - 2.13.0-1
- New upstream release.

* Thu Feb 15 2018 Akira TAGOH <tagoh@redhat.com> - 2.12.93-1
- New upstream release.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan  4 2018 Akira TAGOH <tagoh@redhat.com> - 2.12.92-1
- New upstream release.
- Fix the mis-ordering of evaluating config. (#1530211)

* Sat Dec 23 2017 Akira TAGOH <tagoh@redhat.com> - 2.12.91-2
- Fix crash (#1528706)

* Thu Dec 14 2017 Akira TAGOH <tagoh@redhat.com> - 2.12.91-1
- New upstream release.

* Wed Nov  8 2017 Akira TAGOH <tagoh@redhat.com> - 2.12.6-4
- Remove the debug print in fc-query. (#1509790)

* Thu Oct  5 2017 Akira TAGOH <tagoh@redhat.com> - 2.12.6-3
- Backport a patch to change the order of the emoji fonts. (#1496761)

* Tue Oct  3 2017 Akira TAGOH <tagoh@redhat.com> - 2.12.6-2
- Bump the release to address the upgrade path issue.

* Thu Sep 21 2017 Akira TAGOH <tagoh@redhat.com> - 2.12.6-1
- New upstream release.

* Sat Sep  9 2017 Akira TAGOH <tagoh@redhat.com> - 2.12.5-1
- New upstream release.

* Mon Jul 31 2017 Akira TAGOH <tagoh@redhat.com> - 2.12.4-4
- Fix exiting with 1 on 32bit arch. (#1476831)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Akira TAGOH <tagoh@redhat.com> - 2.12.4-2
- Allow installing 32/64 bit version of fc-cache at the same time. (#1474257)
- Add fc-cache script to invoke both version of fc-cache if available.

* Wed Jul  5 2017 Akira TAGOH <tagoh@redhat.com> - 2.12.4-1
- New upstream release.

* Wed May 31 2017 Akira TAGOH <tagoh@redhat.com> - 2.12.3-1
- New upstream release.

* Thu Feb 23 2017 Akira TAGOH <tagoh@redhat.com> - 2.12.1-4
- Move the cache files into /usr/lib/fontconfig/cache (#1377367, #1416380)

* Wed Feb 22 2017 Akira TAGOH <tagoh@redhat.com> - 2.12.1-3
- Fix FTBFS (#1423570)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug  5 2016 Akira TAGOH <tagoh@redhat.com> - 2.12.1-1
- New upstream release.

* Wed Jun 15 2016 Akira TAGOH <tagoh@redhat.com> - 2.12.0-1
- New upstream release.

* Tue Apr 12 2016 Akira TAGOH <tagoh@redhat.com> - 2.11.95-1
- New upstream release. (#1325560)

* Mon Mar 28 2016 Akira TAGOH <tagoh@redhat.com> - 2.11.94-7
- Add Requires: freetype.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.94-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep  7 2015 Akira TAGOH <tagoh@redhat.com> - 2.11.94-5
- Add file triggers for fonts.

* Fri Aug 14 2015 Akira TAGOH <tagoh@redhat.com> - 2.11.94-4
- Revise the patch. (#1236034)

* Wed Aug 12 2015 Akira TAGOH <tagoh@redhat.com> - 2.11.94-3
- Lock the cache file until scanning and writing finished. (#1236034)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.94-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  2 2015 Akira TAGOH <tagoh@redhat.com> - 2.11.94-1
- New upstream release.
  - Fix bitmap scaling. (#1187528, #1226433, 1226522, #1226722)

* Mon Mar 30 2015 Akira TAGOH <tagoh@redhat.com> - 2.11.93-2
- Fix SIGFPE (#1203118)

* Mon Mar  9 2015 Akira TAGOH <tagoh@redhat.com> - 2.11.93-1
- New upstream release.

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.11.92-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Jan 13 2015 Akira TAGOH <tagoh@redhat.com> - 2.11.92-1
- New upstream release.

* Thu Dec 25 2014 Akira TAGOH <tagoh@redhat.com> - 2.11.91-1
- New upstream release.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun  5 2014 Akira TAGOH <tagoh@redhat.com> - 2.11.1-3
- Workaround that the cache isn't updated properly. (#921706)

* Fri Apr 11 2014 Akira TAGOH <tagoh@redhat.com> - 2.11.1-2
- Fix failing on updating cache with --really-force.

* Mon Mar 24 2014 Akira TAGOH <tagoh@redhat.com> - 2.11.1-1
- New upstream release.

* Fri Jan 24 2014 Akira TAGOH <tagoh@redhat.com> - 2.11.0-2
- Add Requires: font(:lang=en) (#1025331, #845712)

* Fri Oct 11 2013 Akira TAGOH <tagoh@redhat.com> - 2.11.0-1
- New upstream release.

* Fri Sep 13 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.95-4
- Fix memory leaks in FcFreeTypeQueryFace().

* Mon Sep  2 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.95-3
- Do not create a directory for migration when no old config file and directory.
  (#1003495)

* Sat Aug 31 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.95-1
- Fix a crash issue (#1003069)

* Fri Aug 30 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.94-1
- New upstream release.
- migrate the configuration for XDG Base Directory spec automatically (#882267)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.93-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 20 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.93-1
- New upstream release.

* Thu Apr 11 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.92-3
- Fix a web font issue in firefox. (#946859)

* Mon Apr  1 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.92-2
- Fix font matching issue. (#929372)

* Fri Mar 29 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.92-1
- New upstream release.

* Tue Feb 12 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.91-3
- Improve the spec to meet the latest packaging guidelines (#225759)
  - add -devel-doc subpackage.
- Fix a build issue with automake 1.13

* Fri Feb  8 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.10.91-2
- Own the %%{_datadir}/xml/fontconfig dir.
- Fix bogus dates in %%changelog.

* Fri Jan 11 2013 Akira TAGOH <tagoh@redhat.com> - 2.10.91-1
- New upstream release (#894109)
  - threadsafe
  - new tool to validate the glyph coverage
  - add new rule to scale the bitmap font.

* Mon Nov 26 2012 Akira TAGOH <tagoh@redhat.com> - 2.10.2-1
- New upstream release.
  - Fix an regression on FcFontMatch with namelang. (#876970)

* Thu Oct 25 2012 Akira TAGOH <tagoh@redhat.com> - 2.10.1-2
- Update License field (#869614)

* Fri Jul 27 2012 Akira TAGOH <tagoh@redhat.com> - 2.10.1-1
- New upstream release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Akira TAGOH <tagoh@redhat.com> - 2.10.0-1
- New upstream release.

* Mon Jun 25 2012 Akira TAGOH <tagoh@redhat.com> - 2.9.92-1
- New upstream release.

* Mon Jun 11 2012 Akira TAGOH <tagoh@redhat.com> - 2.9.91-1
- New upstream release.
  - docs are generated with the fixed docbook (#826145)
  - handle whitespace in family name correctly (#468565, #591634)
  - Updated ne.orth. (#586763)

* Wed May 16 2012 Akira TAGOH <tagoh@redhat.com> - 2.9.0-2
- Add grep and coreutils to Requires(post). (#821957)

* Fri Mar 23 2012 Akira TAGOH <tagoh@redhat.com>
- backport patch to make 'result' from FcFontMatch() and FcFontSort()
  more reliable.

* Wed Mar 21 2012 Akira TAGOH <tagoh@redhat.com> - 2.9.0-1
- New upstream release (#803559)
  - Update ks.orth (#790471)
  - Add brx.orth (#790460)
  - Update ur.orth (#757985)
  - No Apple Roman cmap support anymore. should works. (#681808)
  - Update ne.orth (#586763)
  - Add a workaround for ZapfDingbats. (#562952, #497648, #468565)
- clean up the spec file.
- Add BR: fontpackages-devel.
- Add R: fontpackages-filesystem.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May 31 2011 Adam Jackson <ajax@redhat.com> 2.8.0-4
- fontconfig-2.8.0-dingbats.patch: Hack for dingbats font matching. (#468565)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jun 24 2010 Adam Jackson <ajax@redhat.com> 2.8.0-2
- fontconfig-2.8.0-sleep-less.patch: Make a stupid sleep() in fc-cache
  slightly less stupid.

* Thu Dec  3 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Tue Sep  8 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.7.3-1
- Update to 2.7.3

* Mon Aug 31 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.7.2-1
- Update to 2.7.2

* Mon Jul  27 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.7.1-1
- Update to 2.7.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.7.0
- Update to 2.7.0

* Mon Jun  1 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad.20090601-1
- Update to 2.6.99.behdad.20090601

* Fri May  8 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad.20090508-1
- Update to 2.6.99.behdad.20090508
- Resolves #497984

* Wed Mar 18 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad.20090318-1
- Update to 2.6.99.behdad.20090318
- Resolves #490888

* Tue Mar 17 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad.20090317-1
- Update to 2.6.99.behdad.20090317
- Resolves #485685

* Sat Mar 14 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad-3
- New tarball with version fixed in the header

* Fri Mar 13 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad-2
- Previous tarball was broken.  Rebuild with respinned ball.

* Fri Mar 13 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.99.behdad-1
- Update to 2.6.99.behdad

* Tue Mar 10 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.98-1.gb39c36a
- Update to 2.6.98-1.gb39c36a

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.97-5.g945d6a4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 2.6.97-4.g945d6a4
— global-ization

* Mon Feb 16 2009 Richard Hughes <rhughes@redhat.com> - 2.6.97-3.g945d6a4
- Correct the rpm provide name to be font(), not Font().

* Sun Feb 15 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.97-2.g945d6a4
- Another try.

* Sun Feb 15 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.97-1.g945d6a4
- Update to 2.6.97-1.g945d6a4

* Sun Feb 15 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.96-1.g0b290a6
- Update to 2.6.96-1.g0b290a6

* Tue Jan 27 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.95-1.git.66.gb162bfb
- Update to 2.6.95-1.git.66.gb162bfb

* Fri Jan 23 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.94-1.git.65.g628ee83
- Update to 2.6.94-1.git.65.g628ee83

* Wed Jan 21 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.93-1.git.64.g6aa4dce
- Update to 2.6.93-1.git.64.g6aa4dce

* Mon Jan 19 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.92-1.git.64.g167bb82
- Update to 2.6.92-1.git.64.g167bb82

* Mon Jan 19 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.91-1.git.64.g9feaf34
- Update to 2.6.91-1.git.64.g9feaf34

* Fri Jan 16 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.90-3.git.63.g6bb4b9a
- Install fc-scan and fc-query

* Fri Jan 16 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.90-2.git.63.g6bb4b9a
- Update to 2.6.90-1.git.63.g6bb4b9a
- Remove upstreamed patch

* Mon Oct 20 2008 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.0-3
- Add fontconfig-2.6.0-indic.patch
- Resolves: #464470

* Sun Jun 01 2008 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.0-2
- Fix build.

* Sat May 31 2008 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.0-1
- Update to 2.6.0.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.5.0-2
- Autorebuild for GCC 4.3

* Wed Nov 14 2007 Behdad Esfahbod <besfahbo@redhat.com> - 2.5.0-1
- Update to 2.5.0.

* Tue Nov 06 2007 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.92-1
- Update to 2.4.92.
- Mark /etc/fonts/conf.d/* as config(noreplace).
- Remove most of our conf file, all upstreamed except for
  75-blacklist-fedora.conf that I'm happily dropping.  Who has
  Hershey fonts these days...
- ln upstream'ed 25-unhint-nonlatin.conf from conf.avail in conf.d
- Add 25-no-bitmap-fedora.conf which is the tiny remaining bit
  of conf that didn't end up upstream.  Can get rid of it in the
  future, but not just yet.

* Thu Oct 25 2007 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.91-1
- Update to 2.4.91.
- Add /usr/local/share/fonts to default config. (#147004)
- Don't rebuild docs, to fix multilib conflicts. (#313011)
- Remove docbook and elinks BuildRequires and stuff as we don't
  rebuild docs.

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 2.4.2-5
- Rebuild for PPC toolchain bug
- Add BuildRequires: gawk

* Sun Jun 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.4.2-4
- /etc/fonts/conf.d is now owned by filesystem

* Fri May 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.4.2-3
- Add Liberation fonts to 30-aliases-fedora.conf

* Fri Jan 12 2007 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.2-2
- Change /usr/share/X11/fonts/OTF to /usr/share/X11/fonts/TTF
- Resolves: #220809

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.4.2-1
- Update to 2.4.2

* Wed Oct  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.4.1-4
- Fix a multilib upgrade problem (#208151)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.4.1-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.1-2
- Update 30-aliases-fedora.conf to correctly alias MS and StarOffice
  fonts. (#207460)

* Fri Sep 15 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.1-1
- Update to 2.4.1, a public API was dropped from 2.4.0
- Remove upstreamed patch

* Mon Sep 11 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.0-1
- Update to 2.4.0
- Rename/order our configuration stuff to match the new scheme.
  Breaks expected :-(

* Thu Sep 07 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.97-3
- Add missing file.  Previous update didn't go through

* Thu Sep 07 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.97-2
- Add fontconfig-2.3.97-ppc64.patch, for ppc64 arch signature

* Thu Sep 07 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.97-1
- update to 2.3.97
- Drop upstreamed patches
- Regenerate defaultconfig patch
- Don't touch stamp as it was not ever needed

* Thu Aug 17 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.95-11
- inclusion of zhong yi font and rearranged font prefer list. (bug# 201300)

* Fri Aug 11 2006 Ray Strode <rstrode@redhat.com> - 2.3.95-10
- use "%%5x" instead of " %%4x" to support 64k instead of
  clamping.  Idea from Behdad.

* Fri Aug 11 2006 Ray Strode <rstrode@redhat.com> - 2.3.95-9
- tweak last patch to give a more reasonable page size
  value if 64k page size is in effect.

* Fri Aug 11 2006 Ray Strode <rstrode@redhat.com> - 2.3.95-8
- maybe fix buffer overflow (bug 202152).

* Fri Aug 11 2006 Ray Strode <rstrode@redhat.com> - 2.3.95-7
- Update configs to provide better openoffice/staroffice
  compatibility (bug 200723)

* Thu Jul 27 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.95-6
- Do umask 0022 in post
- Update configs to reflect addition of new Indic fonts (#200381, #200397)

* Tue Jul 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.95-5
- Plug a small memory leak

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.95-4.1.1
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.95-4.1
- rebuild

* Fri Jun  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.95-4
- Fix the handling of TTF font collections

* Thu May 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.95-3
- Apply a patch by David Turner to speed up cache generation

* Wed Apr 26 2006 Bill Nottingham <notting@redhat.com> - 2.3.95-2
- fix fonts.conf typo

* Wed Apr 26 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.95-1
- Update to 2.3.95

* Fri Feb 24 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.94-1
- Update to 2.3.94

* Sat Feb 11 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060211-1
- Newer cvs snapshot

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.3.93.cvs20060208-1.1
- bump again for double-long bug on ppc(64)

* Wed Feb  8 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060208-1
- Newer cvs snapshot

* Tue Feb  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060207-1
- Newer cvs snapshot
- Drop upstreamed patches, pick up some new ones

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.3.93.cvs20060131-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb  2 2006 Ray Strode <rstrode@redhat.com> - 2.3.93.cvs20060131-3
- Move user cache to a subdirectory (bug 160275)

* Thu Feb  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060131-2
- Accumulated patches

* Tue Jan 31 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060131-1
- Newer cvs snapshot

* Tue Jan 24 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060124-1
- Newer cvs snapshot

* Tue Jan 17 2006 Ray Strode <rstrode@redhat.com> - 2.3.93-4
- apply patch from Tim Mayberry to correct aliasing and disable
  hinting for the two Chinese font names AR PL ShanHeiSun Uni 
  and AR PL Zenkai Uni

* Tue Jan 10 2006 Bill Nottingham <notting@redhat.com> - 2.3.93-3
- prereq coreutils for mkdir/touch in %%post

* Wed Dec 21 2005 Carl Worth <cworth@redhat.com> - 2.3.93-2
- Fix to create /var/cache/fontconfig/stamp in the post install stage.

* Wed Dec 21 2005 Carl Worth <cworth@redhat.com> - 2.3.93-1
- New upstream version.

* Tue Dec 13 2005 Carl Worth <cworth@redhat.com> - 2.3.92.cvs20051129-3
- Disable hinting for Lohit Gujarati

* Fri Dec  9 2005 Carl Worth <cworth@redhat.com> - 2.3.92.cvs20051129-2
- Add two new Chinese font names to the default fonts.conf file:
    AR PL ShanHeiSun Uni
    AR PL Zenkai Uni

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 29 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.92.cvs20051129-1
- Update to a newer cvs snapshot

* Sat Nov 19 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.92.cvs20051119-1
- Update to a newer cvs snapshot

* Wed Nov 16 2005 Bill Nottingham <notting@redhat.com> - 2.3.93-3
- modular X moved fonts from /usr/X11R6/lib/X11/fonts to
  /usr/share/X11/fonts, adjust %%configure accordingly and 
  conflict with older font packages

* Wed Nov  9 2005 Carl Worth <cworth@redhat.com> - 2.3.92-2
- Remove inadvertent rejection of Luxi Mono from 40-blacklist-fonts.conf.
  Fixes #172437

* Fri Nov  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.92-1
- Update to 2.3.92

* Mon Oct 31 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.91.cvs20051031-1
- Update to a newer cvs snapshot
- Add a patch which should help to understand broken cache problems

* Fri Oct 21 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.91.cvs20051017-2
- Add new Chinese fonts
- Fix the 40-blacklist-fonts.conf file to use the documented
  fonts.conf syntax, and exclude the Hershey fonts by family
  name.

* Fri Oct 14 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.91.cvs20051017-1
- Update to the mmap branch of fontconfig

* Fri Jul 22 2005 Kristian Høgsberg <krh@redhat.com> - 2.3.2-1
- Update to fontconfig-2.3.2.  Drop

	fontconfig-2.1-slighthint.patch,
	fontconfig-2.2.3-timestamp.patch,
	fontconfig-2.2.3-names.patch,
	fontconfig-2.2.3-ta-pa-orth.patch, and
	fontconfig-2.2.3-timestamp.patch,

  as they are now merged upstream.

- Fold fontconfig-2.2.3-add-sazanami.patch into
  fontconfig-2.3.2-defaultconfig.patch and split rules to disable CJK
  hinting out into /etc/fonts/conf.d/50-no-hint-fonts.conf.

- Drop fontconfig-0.0.1.020826.1330-blacklist.patch and use the new
  rejectfont directive to reject those fonts in 40-blacklist-fonts.conf.

- Add fontconfig-2.3.2-only-parse-conf-files.patch to avoid parsing
  .rpmsave files.

- Renable s390 documentation now that #97079 has been fixed and add
  BuildRequires: for docbook-utils and docbook-utils-pdf.

- Drop code to iconv and custom install man pages, upstream does the
  right thing now.

- Add workaround from hell to make elinks cooperate so we can build
  txt documentation.

* Tue Apr 19 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-13
- Add another font family name Sazanami Gothic/Mincho (#148748)

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-12
- Rebuild

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-11
- Rebuild

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-10
- Rebuild

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-9
- Disable docs for s390 for now

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-8
- Rebuild

* Wed Dec  1 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-6
- Sleep a second before the exit of fc-cache to fix problems with fast 
  serial installs of fonts (#140335)
- Turn off hinting for Lohit Hindi/Bengali/Punjabi (#139816)

* Tue Oct 19 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-5
- Add Lohit fonts for Indic languages (#134492)
- Add Punjabi converage, fix Tamil coverage

* Wed Sep 22 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-4
- Update fonts-hebrew names to include CLM suffix

* Thu Sep  2 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-3
- Backport code from head branch of fontconfig CVS to parse names 
  for postscript fonts (fixes #127500, J. J. Ramsey)
- Own /usr/share/fonts (#110956, David K. Levine)
- Add KacstQura to serif/sans-serif/monospace aliases (#101182)

* Mon Aug 16 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-2
- Don't run fc-cache if the binary isn't there (#128072, tracked
  down by Jay Turner)

* Tue Aug  3 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-1
- Upgrade to 2.2.3
- Convert man pages to UTF-8 (#108730, Peter van Egdom)
- Renable docs on s390

* Mon Jul 26 2004 Owen Taylor <otaylor@redhat.com> - 2.2.1-12
- Rebuild for RHEL
- Back freetype required version down to 2.1.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 19 2004 Owen Taylor <otaylor@redhat.com> 2.2.1-10
- Require recent freetype (#109592, Peter Oliver)
- Remove fonts.conf timestamp to fix multiarch conflict (#118182)
- Disable hinting for Mukti Narrow (#120915, Sayamindu Dasgupta)

* Wed Mar 10 2004 Owen Taylor <otaylor@redhat.com> 2.2.1-8.1
- Rebuild

* Wed Mar 10 2004 Owen Taylor <otaylor@redhat.com> 2.2.1-8.0
- Add Albany/Cumberland/Thorndale as fallbacks for Microsoft core fonts and 
  as non-preferred alternatives for Sans/Serif/Monospace
- Fix FreeType includes for recent FreeType

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Sep 22 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-6.0
- Should have been passing --with-add-fonts, not --with-add-dirs to 
  configure ... caused wrong version of Luxi to be used. (#100862)

* Fri Sep 19 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-5.0
- Tweak fonts.conf to get right hinting for CJK fonts (#97337)

* Tue Jun 17 2003 Bill Nottingham <notting@redhat.com> 2.2.1-3
- handle null config->cache correctly

* Thu Jun 12 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-2
- Update default config to include Hebrew fonts (#90501, Dov Grobgeld)

* Tue Jun 10 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-2
- As a workaround disable doc builds on s390

* Mon Jun  9 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-1
- Version 2.2.1

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Mon Feb 24 2003 Owen Taylor <otaylor@redhat.com> 2.1-8
- Fix segfault in fc-cache from .dircache patch

* Mon Feb 24 2003 Owen Taylor <otaylor@redhat.com>
- Back out patch that wrote fonts.conf entries that crash RH-8.0 
  gnome-terminal, go with patch from fontconfig CVS instead.
  (#84863)

* Tue Feb 11 2003 Owen Taylor <otaylor@redhat.com>
- Move fontconfig man page to main package, since it contains non-devel 
  information (#76189)
- Look in the OTF subdirectory of /usr/X11R6/lib/fonts as well
  so we find Syriac fonts (#82627)

* Thu Feb  6 2003 Matt Wilson <msw@redhat.com> 2.1-5
- modified fontconfig-0.0.1.020626.1517-fontdir.patch to hard code
  /usr/X11R6/lib/X11/fonts instead of using $(X_FONT_DIR).  This is
  because on lib64 machines, fonts are not in /usr/X11R6/lib64/....

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Owen Taylor <otaylor@redhat.com>
- Try a different tack when fixing cache problem

* Tue Jan 14 2003 Owen Taylor <otaylor@redhat.com>
- Try to fix bug where empty cache entries would be found in 
  ~/.fonts.cache-1 during scanning (#81335)

* Thu Nov 21 2002 Mike A. Harris <mharris@redhat.com> 2.1-1
- Updated to version 2.1
- Updated slighthint patch to fontconfig-2.1-slighthint.patch
- Updated freetype version required to 2.1.2-7

* Mon Sep  2 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.0
- Correct capitalization/spacing for ZYSong18030 name (#73272)

* Fri Aug 30 2002 Owen Taylor <otaylor@redhat.com>
- Blacklist fonts from ghostscript-fonts that don't render correctly

* Mon Aug 26 2002 Owen Taylor <otaylor@redhat.com>
- Upgrade to fcpackage rc3
- Fix bug in comparisons for xx_XX language tags
- Compensate for a minor config file change in rc3

* Wed Aug 21 2002 Owen Taylor <otaylor@redhat.com>
- Add an explicit PreReq for freetype
- Move fonts we don't ship to the end of the fonts.conf aliases so
  installing them doesn't change the look.

* Wed Aug 21 2002 Owen Taylor <otaylor@redhat.com>
- Memory leak fix when parsing config files
- Set rh_prefer_bitmaps for .ja fonts to key off of in Xft
- Fix some groff warnings for fontconfig.man (#72138)

* Thu Aug 15 2002 Owen Taylor <otaylor@redhat.com>
- Try once more to get the right default Sans-serif font :-(
- Switch the Sans/Monospace aliases for Korean to Gulim, not Dotum

* Wed Aug 14 2002 Owen Taylor <otaylor@redhat.com>
- Fix %%post

* Tue Aug 13 2002 Owen Taylor <otaylor@redhat.com>
- Fix lost Luxi Sans default

* Mon Aug 12 2002 Owen Taylor <otaylor@redhat.com>
- Upgrade to rc2
- Turn off hinting for all CJK fonts
- Fix typo in %%post
- Remove the custom language tag stuff in favor of Keith's standard 
  solution.

* Mon Jul 15 2002 Owen Taylor <otaylor@redhat.com>
- Prefer Luxi Sans to Nimbus Sans again

* Fri Jul 12 2002 Owen Taylor <otaylor@redhat.com>
- Add FC_HINT_STYLE to FcBaseObjectTypes
- Switch Chinese fonts to always using Sung-ti / Ming-ti, and never Kai-ti
- Add ZYSong18030 to aliases (#68428)

* Wed Jul 10 2002 Owen Taylor <otaylor@redhat.com>
- Fix a typo in the langtag patch (caught by Erik van der Poel)

* Wed Jul  3 2002 Owen Taylor <otaylor@redhat.com>
- Add FC_HINT_STYLE tag

* Thu Jun 27 2002 Owen Taylor <otaylor@redhat.com>
- New upstream version, with fix for problems with
  ghostscript-fonts (Fonts don't work for Qt+CJK,
  etc.)

* Wed Jun 26 2002 Owen Taylor <otaylor@redhat.com>
- New upstream version, fixing locale problem

* Mon Jun 24 2002 Owen Taylor <otaylor@redhat.com>
- Add a hack where we set the "language" fontconfig property based on the locale, then 
  we conditionalize base on that in the fonts.conf file.

* Sun Jun 23 2002 Owen Taylor <otaylor@redhat.com>
- New upstream version

* Tue Jun 18 2002 Owen Taylor <otaylor@redhat.com>
- Fix crash from FcObjectSetAdd

* Tue Jun 11 2002 Owen Taylor <otaylor@redhat.com>
- make fonts.conf %%config, not %%config(noreplace)
- Another try at the CJK aliases
- Add some CJK fonts to the config
- Prefer Luxi Mono to Nimbus Mono

* Mon Jun 10 2002 Owen Taylor <otaylor@redhat.com>
- New upstream version
- Fix matching for bitmap fonts

* Mon Jun  3 2002 Owen Taylor <otaylor@redhat.com>
- New version, new upstream mega-tarball

* Tue May 28 2002 Owen Taylor <otaylor@redhat.com>
- Fix problem with FcConfigSort

* Fri May 24 2002 Owen Taylor <otaylor@redhat.com>
- Initial specfile

