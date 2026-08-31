# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: epoxy runtime library
Name: libepoxy
Version: 1.5.10
Release: 11%{?dist}
# SPDX
License: MIT
URL: https://github.com/anholt/libepoxy
Source0: https://download.gnome.org/sources/%{name}/1.5/%{name}-%{version}.tar.xz

# https://github.com/anholt/libepoxy/pull/270
Patch0: Fix-dlwrap-on-riscv64.patch

BuildRequires: meson
BuildRequires: gcc
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(egl)
BuildRequires: libGL-devel
BuildRequires: libEGL-devel
BuildRequires: libX11-devel
BuildRequires: pkgconfig(glesv2)
BuildRequires: python3
BuildRequires: mesa-dri-drivers
BuildRequires: mutter
BuildRequires: xwayland-run

%description
A library for handling OpenGL function pointer management.

%package devel
Summary: Development files for libepoxy
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%check
# this should be %%meson_test but the macro expands with a bajillion
# embedded newlines for no obvious reason
xwfb-run -c mutter -- ninja -C %{_vpath_builddir} test || \
    (cat %{_vpath_builddir}/meson-logs/testlog.txt ; exit 1)

%files
%license COPYING
%doc README.md
%{_libdir}/libepoxy.so.0*

%files devel
%{_includedir}/epoxy/
%{_libdir}/libepoxy.so
%{_libdir}/pkgconfig/epoxy.pc

%changelog
* Thu Sep 25 2025 Songsong Zhang <U2FsdGVkX1@gmail.com> - 1.5.10-11
- Backport upstream fix for dlwrap on riscv64

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Niels De Graef  <ndegraef@redhat.com> - 1.5.10-7
- Move away from xvfb-run

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 07 2023 José Expósito <jexposit@redhat.com>
- SPDX migration: license is already SPDX compatible

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 18 2022 David King <amigadave@amigadave.com> - 1.5.10-1
- Update to 1.5.10

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Aug 15 2021 Kalev Lember <klember@redhat.com> - 1.5.9-1
- Update to 1.5.9

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 26 2021 Kalev Lember <klember@redhat.com> - 1.5.8-1
- Update to 1.5.8

* Fri Apr 30 2021 Kalev Lember <klember@redhat.com> - 1.5.7-1
- Update to 1.5.7

* Fri Apr 30 2021 Kalev Lember <klember@redhat.com> - 1.5.6-1
- Update to 1.5.6
- Remove ldconfig_scriptlets use

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 05 2021 Kalev Lember <klember@redhat.com> - 1.5.5-1
- Update to 1.5.5

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 27 2019 Kalev Lember <klember@redhat.com> - 1.5.4-1
- Update to 1.5.4

* Fri Oct 25 2019 Peter Robinson <pbrobinson@gmail.com> - 1.5.3-5
- Rebuild for libglvnd 1.2, drop work-arounds

* Thu Aug 22 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.5.3-4
- epoxy.pc: -Requires.private: gl egl (#1744320)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 05 2018 Kalev Lember <klember@redhat.com> - 1.5.3-1
- Update to 1.5.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun May 20 2018 Kalev Lember <klember@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Wed Apr 25 2018 Adam Jackson <ajax@redhat.com> - 1.5.1-2
- Enable tests for all arches
- Run tests against Xvfb so we get plausible amounts of coverage

* Wed Apr 25 2018 Kalev Lember <klember@redhat.com> - 1.5.1-1
- Update to 1.5.1

* Wed Feb 28 2018 Kalev Lember <klember@redhat.com> - 1.5.0-1
- Update to 1.5.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.3-5
- Switch to %%ldconfig_scriptlets

* Fri Sep 22 2017 Adam Jackson <ajax@redhat.com> - 1.4.3-4
- Backport some useful bits from master

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Adam Jackson <ajax@redhat.com> - 1.4.3-1
- libepoxy 1.4.3

* Thu Mar 09 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.4.1-2
- Switch to meson
- Add license file
- Simplify spec

* Thu Mar 09 2017 Dave Airlie <airlied@redhat.com> - 1.4.1-1
- libepoxy 1.4.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 23 2016 Adam Jackson <ajax@redhat.com> - 1.3.1-3
- Fix detection of EGL client extensions

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 05 2015 Adam Jackson <ajax@redhat.com> 1.3.1-1
- libepoxy 1.3.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 05 2015 Dave Airlie <airlied@redhat.com> 1.2-3
- update GL registry files (add new EGL extension)

* Wed Mar 25 2015 Adam Jackson <ajax@redhat.com> 1.2-2
- Fix description to not talk about DRM
- Sync some small bugfixes from git

* Mon Oct 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.0-1
- Update to 1.2 GA
- Don't fail build on make check failure for some architectures

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.4.20140411git6eb075c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.3.20140411git6eb075c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Dave Airlie <airlied@redhat.com> 1.2-0.2.20140411git6eb075c
- update to latest git snapshot

* Thu Mar 27 2014 Dave Airlie <airlied@redhat.com> 1.2-0.1.20140307gitd4ad80f
- initial git snapshot

