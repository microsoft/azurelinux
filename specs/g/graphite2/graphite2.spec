# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           graphite2
Version:        1.3.14
Release: 20%{?dist}
Summary:        Font rendering capabilities for complex non-Roman writing systems

# As per COPYING file this library is tri-licensed
License:        LGPL-2.1-or-later OR MPL-2.0 OR GPL-2.0-or-later

URL:            https://sourceforge.net/projects/silgraphite/
Source0:        https://downloads.sourceforge.net/project/silgraphite/graphite2//%{name}-%{version}.tgz

Patch0:         graphite-arm-nodefaultlibs.patch
Patch1:         graphite2-1.2.0-cmakepath.patch
# This fixes compilation with gcc15
Patch2:         graphite2-1.3.14-gcc15.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  freetype-devel

# needed for running the test suite
BuildRequires:  python3-fonttools

%description
Graphite2 is a project within SIL’s Non-Roman Script Initiative and Language
Software Development groups to provide rendering capabilities for complex
non-Roman writing systems. Graphite can be used to create “smart fonts” capable
of displaying writing systems with various complex behaviors. With respect to
the Text Encoding Model, Graphite handles the "Rendering" aspect of writing
system implementation.


%package devel
Summary:        Files for developing with graphite2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Includes and definitions for developing with graphite2.


%prep
%autosetup -p1


%build
%cmake -DGRAPHITE2_COMPARE_RENDERER=OFF
%cmake_build


%install
%cmake_install

find %{buildroot} -type f -name "*.la" -print -delete


%check
%ctest -E 'nametabletest'


%files
%license LICENSE COPYING
%doc ChangeLog README.md

%{_bindir}/gr2fonttest

%{_libdir}/libgraphite2.so.3*


%files devel
%{_includedir}/%{name}/

%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/graphite2-release.cmake
%{_libdir}/%{name}/graphite2.cmake

%{_libdir}/libgraphite2.so
%{_libdir}/pkgconfig/graphite2.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 23 2025 Parag Nemade <pnemade AT redhat DOT com> - 1.3.14-18
- Fix to build against GCC 15 (#2340572)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 06 2023 Parag Nemade <pnemade AT redhat DOT com> - 1.3.14-13
- Migrate to SPDX license expression
- Drop Netscape license reference as no test file using it in 1.3.x releases

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 30 2020 Fabio Valentini <decathorpe@gmail.com> - 1.3.14-6
- Stop building the HTML manual, texlive is breaking things too frequently.

* Sat Aug 01 2020 Fabio Valentini <decathorpe@gmail.com> - 1.3.14-5
- Adapt to new cmake macros.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Fabio Valentini <decathorpe@gmail.com> - 1.3.14-2
- Add missing build dependencies for building the manual with TeXLive 2020.

* Wed Apr 08 2020 Fabio Valentini <decathorpe@gmail.com> - 1.3.14-1
- Update to version 1.3.14.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 22 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.3.13-1
- New upstream 1.3.13 release
- Move to python3 for tests
- Fix CVE-2018-7999 (rhbz 1554383)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.10-4
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 23 2017 Michael Cronenworth <mike@cchtml.com> - 1.3.10-1
- New upstream release
- Resolves CVE-2017-7778

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 29 2016 Caolán McNamara <caolanm@redhat.com> - 1.3.6-1
- update to latest release

* Wed Feb 17 2016 Caolán McNamara <caolanm@redhat.com> - 1.3.5-1
- Resolves: rhbz#1305806 CVE-2016-1521 CVE-2016-1522 CVE-2016-1523 CVE-2016-1526

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.2.4-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 03 2014 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.2.4-1
- New upstream release

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.2.2-5
- Move *.so.major symlink to main package.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Caolán McNamara <caolanm@redhat.com> - 1.2.2-3
- clarify licenses

* Wed Jun 19 2013 Karsten Hopp <karsten@redhat.com> 1.2.2-2
- use minimum texlive buildrequires, Than Ngo, rhbz#975843 

* Thu May 30 2013 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.2.2-1
- New upstream release

* Tue Jan 29 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.2.0-4
- Drop refman.pdf as its same as manual.html
- patch install path for cmake files as they are arch dependent

* Tue Jan 29 2013 Kalev Lember <kalevlember@gmail.com> - 1.2.0-3
- Move manual.html to -devel subpackage

* Tue Jan 29 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.2.0-2
- revert the wrongly committed f18 spec to f19
- spec file cleanup
- thanks to jnovy for finding me minimum texlive BR
- partial multilib fix for manual.html

* Fri Nov 9 2012 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.2.0-1
- New upstream release

* Wed Oct 3 2012 Caolán McNamara <caolanm@redhat.com> - 1.1.1-4
- expand license field to cover tri-licenced GrUtfTextSrc test

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.1.1-2
- Fix FTBFS on ARM

* Mon Feb 27 2012 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.1.1-1
- New upstream release

* Wed Feb 8 2012 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.1.0-1
- New upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 23 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.3-1
- New upstream release

* Fri Aug 26 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.2-3
- Obsolete silgraphite

* Fri Aug 26 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.2-2
- Removed dependency on silgraphite-devel
- Stopped building comparerenderer - the only thing that depended on silgraphite

* Fri Aug 19 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.2-1
- Rebase to new release
- SPEC Cleanup
- Documentation is now properly installed

* Wed Aug 17 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.1-2
- Added some necessary requires

* Wed Aug 10 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.1-1
- Initial build of graphite2

