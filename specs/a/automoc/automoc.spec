# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#define snaptag .20080527svn811390
%define beta 0.9.88
%define beta_tag rc3

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

Name:           automoc
Version:        1.0
Release:        0.51.%{?beta_tag}%{?dist}
Summary:        Automatic moc for Qt 4
License:        BSD-2-Clause
URL:            http://www.kde.org
Source0:        ftp://ftp.kde.org/pub/kde/stable/automoc4/%{beta}/automoc4-%{beta}.tar.bz2

## upstream patches
Patch1: 0001-fix-make-clean-it-s-SET_directory_properties-and-not.patch
Patch2: 0002-automoc-did-not-understand-.mm-files-objc.patch
Patch3: 0003-support-for-Objective-C-i.e.-mm-files-is-enough-to-i.patch
Patch4: 0004-auto-detect-case-insensitive-filesystem-on-OSX.patch
Patch5: 0005-add-a-ctest-config-file-see-http-my.cdash.org-index..patch
Patch6: 0006-support-for-nightly-builds-at-http-my.cdash.org-inde.patch
Patch7: 0007-rename-AutomocNightly.cmake-to-Automoc4Nightly-to-ma.patch
Patch8: 0008-chaneg-nightly-time.patch
Patch9: 0009-remove-the-warnings-again.patch
Patch10: 0010-add-some-comments.patch
Patch11: 0011-adapt-this-to-the-new-enhanced-KDECTestNightly.cmake.patch
Patch12: 0012-support-installing-in-the-nightly-build.patch
Patch13: 0013-add-documentation.patch
Patch14: 0014-first-attempt-at-cpack-ing-a-KDE-package-works-on-OS.patch
Patch15: 0015-put-the-apple-specific-stuff-in-here.patch
Patch16: 0016-move-the-cpack-bits-into-a-separate-cmake-file.patch
Patch17: 0017-Compile-and-link-on-Mac.patch
Patch18: 0018-Fix-framework-detection-on-Mac-where-Qt-is-installed.patch
Patch19: 0019-kdesupport-automoc-krazy2-fixes.patch
Patch20: 0020-Hack-the-hack.patch
Patch21: 0021-fix-stupid-typo.patch
Patch22: 0022-CMake-2.6.4-is-required-because-older-versions-don-t.patch
Patch23: 0023-Reverting-r1140777-as-causing-some-nasty-cmake-funky.patch
Patch24: 0024-add-cmake_policy-PUSH-POP-to-save-and-restore-the-or.patch
Patch25: 0025-allow-duplicate-target-names-also-in-the-automoc-mac.patch
Patch26: 0026-Fix-cmake_policy-call.patch
Patch27: 0027-add-some-changes-to-build-automoc-statically.patch
Patch28: 0028-AutoMoc-lazyInit-expects-the-app-to-get-6-parameter-.patch
Patch29: 0029-Fix-missing-include-dirs-current-source-and-build-di.patch
Patch30: 0030-Don-t-attempt-to-read-the-DEFINITIONS-property.patch
Patch31: 0031-Don-t-attempt-to-add-dependencies-which-do-not-exist.patch
Patch32: 0032-set-cmake_min_req-to-enable-newer-policies.patch
Patch33: 0033-cmake-2.8.9-sets-CMP0003-to-NEW-clean-up.patch

Provides: automoc4 = %{beta}

Requires:       cmake >= 2.8.9
BuildRequires:  cmake >= 2.8.9
Buildrequires:  gcc-c++
BuildRequires:  qt4-devel
BuildRequires:  kde4-macros(api)
BuildRequires: make

%description
This package contains the automoc4 binary which is used to run moc on the
right source files in a Qt 4 or KDE 4 application.
Moc is the meta object compiler which is a widely used tool with Qt and
creates standard C++ files to provide syntactic sugar of the signal/slots
mechanism.


%prep
%autosetup -p1 -n automoc4-%{beta}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

%make_build -C %{_target_platform}


%install
make install DESTDIR=%{buildroot} -C %{_target_platform}


%files
%{_bindir}/automoc4
%{_kde4_libdir}/automoc4/


%changelog
* Fri Jan 30 2026 Than Ngo <than@redhat.com> - 1.0-0.51.rc3
- Update License

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.50.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.49.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Alessandro Astone <ales.astone@gmail.com> - 1.0-0.48.rc3
- Fix build dependency on %cmake_kde4 macro

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 1.0-0.47.rc3
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.46.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.45.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.44.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.43.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.42.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.41.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.40.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.39.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.38.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.37.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.36.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.35.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 02 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.0-0.34.rc4
- rebuild, use %%make_build

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.33.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.32.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.0-0.31.rc3
- BR: gcc-c++, .spec cosmetics

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.30.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.29.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.28.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.27.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.0-0.26.fc3
- rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.25.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 01 2015 Rex Dieter <rdieter@fedoraproject.org> 1.0-0.24.rc3
- pull in latest upstream fixes

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.23.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.0-0.22.rc3
- Rebuilt for GCC 5 C++11 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.21.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.20.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.19.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.18.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.17.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.16.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.15.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 14 2010 Rex Dieter <rdieter@fedoraproject.org. - 1.0-0.14.rc3
- rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.13.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.12.rc3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Rex Dieter <rdieter@fedoraproject.org> 1.0-0.11.rc3
- automoc4-0.9.88 (1.0-rc3)

* Sat Nov 22 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 1.0-0.10.rc2
- fix package summary and descriptions (as requested by Richard Hughes)
- match cmake minimum required version with the contents of CMakeLists.txt
  (paranoid fix)

* Thu Sep  4 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 1.0-0.9.rc2
- automoc4-0.9.87 (1.0-rc2)

* Wed Jul 23 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0-0.8.rc1
- automoc4-0.9.84 (1.0-rc1)

* Mon Jun 30 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0-0.7.beta2
- automoc4-0.9.83 (1.0-beta2)
- drop lib64 patch

* Thu Jun 10 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 1.0-0.5.20080527svn811390
- Leave automoc4.files.in in _libdir
- Same applies to Automoc4Config.cmake

* Thu May 29 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 1.0-0.3.20080527svn811390
- Added 'cmake' to Requires

* Wed May 28 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 1.0-0.2.20080527svn811390
- Patched to make it build on other systems than i386 (thanks to Rex Dieter)

* Tue May 27 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 1.0-0.1.20080527svn811390
- Initial release
