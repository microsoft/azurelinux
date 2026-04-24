# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define gitdate 20070827
%define gitrev 8ff7213f39edc1b2b8b60d6b0cc5d5f14ca1928d

Name:           pixman
Version:        0.46.2
Release: 3%{?dist}
Summary:        Pixel manipulation library

# SPDX
License:        MIT
URL:            https://gitlab.freedesktop.org/pixman/pixman
#VCS:           git:git://git.freedesktop.org/git/pixman
# To make git snapshots:
# ./make-pixman-snapshot.sh %{\?gitrev}
# if no revision specified, makes a new one from HEAD.
Source0:        https://xorg.freedesktop.org/archive/individual/lib/%{name}-%{version}.tar.xz
Source1:        make-pixman-snapshot.sh

BuildRequires:  gcc
BuildRequires:  meson

%description
Pixman is a pixel manipulation library for X and Cairo.

%package devel
Summary: Pixel manipulation library development package
Requires: %{name}%{?isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
Pixel manipulation library for X and Cairo development package.

%prep
%autosetup -p1

%build
%meson --auto-features=auto \
  %nil

%meson_build

%install
%meson_install

%check
%meson_test

%ldconfig_post
%ldconfig_postun

%files
%doc COPYING
%{_libdir}/libpixman-1*.so.*

%files devel
%dir %{_includedir}/pixman-1
%{_includedir}/pixman-1/pixman.h
%{_includedir}/pixman-1/pixman-version.h
%{_libdir}/libpixman-1*.so
%{_libdir}/pkgconfig/pixman-1.pc

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.46.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 10 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 0.46.2-1
- Update to 0.46.2

* Sun Jun 08 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 0.46.0-1
- Update to 0.46.0

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.44.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 05 2024 José Expósito <jexposit@redhat.com> - 0.44.2-1
- Update to 0.44.2

* Thu Nov 07 2024 José Expósito <jexposit@redhat.com> - 0.44.0-1
- Update to 0.44.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.43.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 01 2024 José Expósito <jexposit@redhat.com> - 0.43.4-1
- Update to 0.43.4

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.43.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.43.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 09 2024 José Expósito <jexposit@redhat.com> - 0.43.0-1
- Update to 0.43.0

* Thu Sep 07 2023 José Expósito <jexposit@redhat.com>
- SPDX migration: license is already SPDX compatible

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.42.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 21 2023 Petter Abrahamsson <pabraham@redhat.com> - 0.42.2-1
- Update to 0.42.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Kalev Lember <klember@redhat.com> - 0.40.0-1
- Update to 0.40.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 0.38.4-1
- Update to 0.38.4

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.38.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 12 2019 Kalev Lember <klember@redhat.com> - 0.38.0-1
- Update to 0.38.0
- Switch to the meson build system

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 29 2018 Adam Jackson <ajax@redhat.com> - 0.36.0-1
- pixman 0.36.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Adam Jackson <ajax@redhat.com> - 0.34.0-9
- Use ldconfig scriptlet macros

* Fri May 04 2018 Dan Horák <dan[at]danny.cz> - 0.34.0-8
- fix vector loads in VMX (ppc64le) (#1572540)

* Thu Apr 26 2018 Adam Jackson <ajax@redhat.com> - 0.34.0-7
- Enable %%check
- --disable-vmx to fix %%check failures with gcc8
- Remove stray --disable-ssse3

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 <oded.gabbay@gmail.com> - 0.34.0-1
- Update to 0.34.0 (#1249357)

* Tue Dec 22 2015 Oded Gabbay <oded.gabbay@gmail.com> 0.33.6-1
- pixman 0.33.6

* Fri Oct 23 2015 Oded Gabbay <oded.gabbay@gmail.com> 0.33.4-1
- pixman 0.33.4

* Sun Aug 09 2015 Oded Gabbay <oded.gabbay@gmail.com> 0.33.2-1
- pixman 0.33.2
- Enable VMX fast paths on ppc64le now that they are fixed

* Tue Jun 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.32.6-6
- revert cflag option added in -5 the broke building

* Mon May 11 2015 Adam Jackson <ajax@redhat.com> 0.32.6-5
- Fix devel's requirement on the base package to include %%{?isa}

* Mon Nov 10 2014 Adam Jackson <ajax@redhat.com> 0.32.6-4
- Disable (broken) VMX fast paths on ppc64le for now.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.32.6-2
- Enable make check but don't (currently) fail the build on failure
- Include COPYING as per packaging guidelines
- Minor spec cleanups

* Sun Jul 06 2014 Soren Sandmann <soren.sandmann@gmail.com> 0.32.6-1
- pixman 0.32.6
- drop SSSE3 patch

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 14 2013 Soren Sandmann <ssp@redhat.com> 0.32.0-2
- Add patch to fix SSSE3 detection

* Sun Nov 10 2013 Soren Sandmann <ssp@redhat.com> 0.32.0-1
- pixman 0.32.0

* Sat Nov 2 2013 Soren Sandmann <ssp@redhat.com> 0.31.2-1
- pixman 0.31.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 04 2013 Karsten Hopp <karsten@redhat.com> 0.30.0-2
- bump release and rebuild to fix dependencies on PPC

* Wed May 8 2013 Soren Sandmann <ssp@redhat.com> 0.30.0-1
- pixman 0.30.0
