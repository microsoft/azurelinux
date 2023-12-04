%define bcond_meson() %{lua: do
  local option = rpm.expand("%{1}")
  local with = rpm.expand("%{?with_" .. option .. "}")
  local value = (with ~= '') and "enabled" or "disabled"
  option = option:gsub('_', '-')
  print(string.format("-D%s=%s", option, value))
end}
%define bcond_meson_tf() %{lua: do
  local option = rpm.expand("%{1}")
  local with = rpm.expand("%{?with_" .. option .. "}")
  local value = (with ~= '') and "true" or "false"
  option = option:gsub('_', '-')
  print(string.format("-D%s=%s", option, value))
end}
%bcond_without amdgpu
%bcond_without radeon
%bcond_without install_test_programs
%bcond_without man_pages
%bcond_without nouveau
%bcond_without udev
%bcond_without vmwgfx
%ifarch %{ix86} x86_64
%bcond_without intel
%else
%bcond_with    intel
%endif
%ifarch %{arm}
%bcond_without omap
%else
%bcond_with    omap
%endif
%ifarch %{arm} aarch64
%bcond_without etnaviv
%bcond_without exynos
%bcond_without freedreno
%bcond_without tegra
%bcond_without vc4
%else
%bcond_with    etnaviv
%bcond_with    exynos
%bcond_with    freedreno
%bcond_with    tegra
%bcond_with    vc4
%endif
%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with    valgrind
%endif
Summary:        Direct Rendering Manager runtime library
Name:           libdrm
Version:        2.4.116
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://dri.freedesktop.org
Source0:        %{url}/libdrm/%{name}-%{version}.tar.xz
Source1:        README.rst
Source2:        91-drm-modeset.rules
Source3:        LICENSE.PTR
# Hardcode the 666 instead of 660 for device nodes
Patch1001:      libdrm-make-dri-perms-okay.patch
# Remove backwards compat not needed on CBL-Mariner
Patch1002:      libdrm-2.4.0-no-bc.patch
BuildRequires:  chrpath
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  kernel-headers
BuildRequires:  libatomic_ops-devel
BuildRequires:  meson >= 0.43
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(cairo)
%if %{with intel}
BuildRequires:  pkgconfig(pciaccess) >= 0.10
%endif
%if %{with man_pages}
BuildRequires:  python3-docutils
%endif
%if %{with valgrind}
BuildRequires:  valgrind-devel
%endif
%if %{with udev}
BuildRequires:  systemd-devel
%endif

%description
Direct Rendering Manager runtime library

%package        devel
Summary:        Direct Rendering Manager development package
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kernel-headers

%description    devel
Direct Rendering Manager development package.

%if %{with install_test_programs}
%package -n drm-utils
Summary:        Direct Rendering Manager utilities
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n drm-utils
Utility programs for the kernel DRM interface.  Will void your warranty.
%endif

%prep
%autosetup -p1
cp %{SOURCE3} .

%build
%meson \
  %{bcond_meson intel}                 \
  %{bcond_meson radeon}                \
  %{bcond_meson amdgpu}                \
  %{bcond_meson nouveau}               \
  %{bcond_meson vmwgfx}                \
  %{bcond_meson omap}                  \
  %{bcond_meson exynos}                \
  %{bcond_meson freedreno}             \
  %{bcond_meson tegra}                 \
  %{bcond_meson vc4}                   \
  %{bcond_meson etnaviv}               \
  %{bcond_meson man_pages}             \
  %{bcond_meson valgrind}              \
  %{bcond_meson_tf install_test_programs} \
  %{bcond_meson_tf udev}                  \
  %{nil}
%meson_build

%install
%meson_install
%if %{with install_test_programs}
chrpath -d %{_vpath_builddir}/tests/drmdevice
install -Dpm0755 -t %{buildroot}%{_bindir} %{_vpath_builddir}/tests/drmdevice
%endif
%if %{with udev}
install -Dpm0644 -t %{buildroot}%{_udevrulesdir} %{SOURCE2}
%endif
mkdir -p %{buildroot}%{_docdir}/libdrm
cp %{SOURCE1} %{buildroot}%{_docdir}/libdrm

%ldconfig_scriptlets

%files
%doc README.rst
%license LICENSE.PTR
%{_libdir}/libdrm.so.2
%{_libdir}/libdrm.so.2.4.0
%dir %{_datadir}/libdrm

%if %{with intel}
%{_libdir}/libdrm_intel.so.1
%{_libdir}/libdrm_intel.so.1.0.0
%endif

%if %{with radeon}
%{_libdir}/libdrm_radeon.so.1
%{_libdir}/libdrm_radeon.so.1.0.1
%endif

%if %{with amdgpu}
%{_libdir}/libdrm_amdgpu.so.1
%{_libdir}/libdrm_amdgpu.so.1.0.0
%{_datadir}/libdrm/amdgpu.ids
%endif

%if %{with nouveau}
%{_libdir}/libdrm_nouveau.so.2
%{_libdir}/libdrm_nouveau.so.2.0.0
%endif

%if %{with omap}
%{_libdir}/libdrm_omap.so.1
%{_libdir}/libdrm_omap.so.1.0.0
%endif

%if %{with exynos}
%{_libdir}/libdrm_exynos.so.1
%{_libdir}/libdrm_exynos.so.1.0.0
%endif

%if %{with freedreno}
%{_libdir}/libdrm_freedreno.so.1
%{_libdir}/libdrm_freedreno.so.1.0.0
%endif

%if %{with tegra}
%{_libdir}/libdrm_tegra.so.0
%{_libdir}/libdrm_tegra.so.0.0.0
%endif

%if %{with etnaviv}
%{_libdir}/libdrm_etnaviv.so.1
%{_libdir}/libdrm_etnaviv.so.1.0.0
%endif

%if %{with udev}
%{_udevrulesdir}/91-drm-modeset.rules
%endif

%files devel
%dir %{_includedir}/libdrm
%{_includedir}/libdrm/drm.h
%{_includedir}/libdrm/drm_fourcc.h
%{_includedir}/libdrm/drm_mode.h
%{_includedir}/libdrm/drm_sarea.h
%{_includedir}/libdrm/*_drm.h
%{_includedir}/libsync.h
%{_includedir}/xf86drm.h
%{_includedir}/xf86drmMode.h
%{_libdir}/libdrm.so
%{_libdir}/pkgconfig/libdrm.pc
%if %{with intel}
%{_includedir}/libdrm/intel_*.h
%{_libdir}/libdrm_intel.so
%{_libdir}/pkgconfig/libdrm_intel.pc
%endif
%if %{with radeon}
%{_includedir}/libdrm/radeon_{bo,cs,surface}*.h
%{_includedir}/libdrm/r600_pci_ids.h
%{_libdir}/libdrm_radeon.so
%{_libdir}/pkgconfig/libdrm_radeon.pc
%endif
%if %{with amdgpu}
%{_includedir}/libdrm/amdgpu.h
%{_libdir}/libdrm_amdgpu.so
%{_libdir}/pkgconfig/libdrm_amdgpu.pc
%endif
%if %{with nouveau}
%{_includedir}/libdrm/nouveau/
%{_libdir}/libdrm_nouveau.so
%{_libdir}/pkgconfig/libdrm_nouveau.pc
%endif
%if %{with omap}
%{_includedir}/libdrm/omap_*.h
%{_includedir}/omap/
%{_libdir}/libdrm_omap.so
%{_libdir}/pkgconfig/libdrm_omap.pc
%endif
%if %{with exynos}
%{_includedir}/libdrm/exynos_*.h
%{_includedir}/exynos/
%{_libdir}/libdrm_exynos.so
%{_libdir}/pkgconfig/libdrm_exynos.pc
%endif
%if %{with freedreno}
%{_includedir}/freedreno/
%{_libdir}/libdrm_freedreno.so
%{_libdir}/pkgconfig/libdrm_freedreno.pc
%endif
%if %{with tegra}
%{_includedir}/libdrm/tegra.h
%{_libdir}/libdrm_tegra.so
%{_libdir}/pkgconfig/libdrm_tegra.pc
%endif
%if %{with vc4}
%{_includedir}/libdrm/vc4_*.h
%{_libdir}/pkgconfig/libdrm_vc4.pc
%endif
%if %{with etnaviv}
%{_includedir}/libdrm/etnaviv_*.h
%{_libdir}/libdrm_etnaviv.so
%{_libdir}/pkgconfig/libdrm_etnaviv.pc
%endif
%if %{with man_pages}
%{_mandir}/man3/drm*.3*
%{_mandir}/man7/drm*.7*
%endif

%if %{with install_test_programs}
%files -n drm-utils
%if %{with amdgpu}
%{_bindir}/amdgpu_stress
%endif
%{_bindir}/drmdevice
%if %{with etnaviv}
%exclude %{_bindir}/etnaviv_*
%endif
%if %{with exynos}
%exclude %{_bindir}/exynos_*
%endif
%if %{with tegra}
%exclude %{_bindir}/tegra-*
%endif
%{_bindir}/modeprint
%{_bindir}/modetest
%{_bindir}/proptest
%{_bindir}/vbltest
%endif

%changelog
* Mon Nov 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.116-1
- Auto-upgrade to 2.4.116 - Azure Linux 3.0 - package upgrades

* Fri Oct 27 2023 Xiaohong Deng <xiaohongdeng@microsoft.com> - 2.4.115-1
- Upgrade to 2.4.115

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.4.114-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon May 15 2023 Hideyuki Nagase <hideyukn@microsoft.com> - 2.4.114-1
- Updating to version 2.4.114 using Fedora 39 spec (license: MIT) for guidance.

* Fri Apr 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.4.102-5
- Remove explicit pkgconfig provides that are now automatically generated by RPM

* Mon Aug 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.102-4
- Removing BR on 'marinerui-rpm-macros'. Using macros from the build env.

* Fri Dec 18 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.102-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Added an explicit 'pkgconfig(libdrm)' for 'libdrm-devel'.
- Added build-time dependency on 'marinerui-rpm-macros'.
- Added the "LICENSE.PTR" file.
- Removed manual pages.
- Replaced ldconfig scriptlets with explicit calls to ldconfig.
- Removed sections related to %%bcond_with for 'cairo_tests' and 'freedreno_kgsl'.
- License verified.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.102-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 27 2020 Dave Airlie <airlied@redhat.com> - 2.4.102-1
- Update to 2.4.102

* Thu May 14 2020 Dave Airlie <airlied@redhat.com> - 2.4.101-1
- Update to 2.4.101

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.100-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 17 2019 Pete Walter <pwalter@fedoraproject.org> - 2.4.100-1
- Update to 2.4.100

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.99-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 04 2019 Dave Airlie <airlied@redhat.com> - 2.4.99-1
- Update to 2.4.99

* Tue Apr 30 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.98-1
- Update to 2.4.98

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Dave Airlie <airlied@redhat.com> - 2.4.97-1
- Update to 2.4.97

* Mon Nov 19 2018 Adam Jackson <ajax@redhat.com> - 2.4.96-2
- Strip RPATH from %%{_bindir}/drmdevice

* Sun Oct 28 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.96-1
- Update to 2.4.96

* Sun Oct  7 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.95-1
- Update to 2.4.95

* Tue Sep 18 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.94-1
- Update to 2.4.94

* Sat Aug 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.93-1
- Update to 2.4.93

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 10 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.92-1
- Update to 2.4.92

* Tue Mar 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.91-1
- Update to 2.4.91

* Thu Mar 01 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.90-2
- Backport fix for broken amdgpu

* Sun Feb 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.90-1
- Update to 2.4.90
- Switch to meson buildsystem

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.89-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.89-2
- Switch to %%ldconfig_scriptlets

* Mon Dec 18 2017 Dave Airlie <airlied@redhat.com> - 2.4.89-1
- Update to 2.4.89

* Sun Nov  5 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.88-1
- Update to 2.4.88

* Thu Nov 02 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.87-1
- Update to 2.4.87

* Sun Oct 22 2017 Dave Airlie <airlied@redhat.com> - 2.4.85-1
- Update to 2.4.85

* Tue Oct 17 2017 Ville Skyttä <ville.skytta@iki.fi> - 2.4.84-2
- Own the %%{_datadir}/libdrm dir

* Fri Oct 13 2017 Dave Airlie <airlied@redhat.com> - 2.4.84-1
- Update to 2.4.84

* Thu Aug 31 2017 Adam Jackson <ajax@redhat.com> - 2.4.83-3
- Also fix the udev rule install

* Wed Aug 30 2017 Adam Jackson <ajax@redhat.com> - 2.4.83-2
- Fix the check-programs install line to work with older libtool
- Seriously, libtool is awful

* Sun Aug 27 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.83-1
- Update to 2.4.83

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.82-1
- Update to 2.4.82

* Fri May 26 2017 Dave Airlie <airlied@redhat.com> - 2.4.81-1
- Update to 2.4.81

* Tue Apr 18 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.4.80-1
- Update to 2.4.80

* Tue Apr 11 2017 Dave Airlie <airlied@redhat.com> - 2.4.79-1
- Update to 2.4.79

* Fri Apr 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.4.78-1
- Update to 2.4.78

* Tue Apr 04 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.4.77-1
- Update to 2.4.77

* Thu Mar 30 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.4.76-1
- Update to 2.4.76

* Thu Mar 23 2017 Adam Jackson <ajax@redhat.com> - 2.4.75-3
- Fix pkg-config detection on non-Intel

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Dave Airlie <airlied@redhat.com> - 2.4.75-1
- Update to 2.4.75

* Sat Jan 21 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.74-2
- Enable etnaviv support on aarch64 too

* Thu Dec 01 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.4.74-1
- Update to 2.4.74 (RHBZ #1400154)

* Tue Nov 15 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.4.73-1
- Update to 2.4.73 (RHBZ #1394986)

* Wed Oct 05 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.4.71-2
- Enable etnaviv on ARM (RHBZ #1381898, billiboy@mt2015.com)

* Tue Oct 04 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.4.71-1
- Update to 2.4.71 (RHBZ #1381543)

* Thu Aug 11 2016 Michal Toman <mtoman@fedoraproject.org> - 2.4.70-2
- No valgrind on MIPS

* Sun Jul 24 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.4.70-1
- Update to 2.4.70 (RHBZ #1359449)

* Thu Jul 21 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.4.69-1
- Update to 2.4.69 (RHBZ #1358549)

* Thu Apr 28 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.4.68-1
- Update to 2.4.68

* Sat Apr  9 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.67-3
- Build some extra bits for aarch64

* Sun Feb 21 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.67-2
- Fix build on aarch64

* Fri Feb 19 2016 Dave Airlie <airlied@redhat.com> 2.4.67-2
- fix installing drm-utils properly - we were install libtool scripts

* Tue Feb 16 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.67-1
- Update to 2.4.67
- Enable VC4

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.66-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.4.66-1
- Update to 2.4.66 (RHBZ #1294382)

* Thu Sep 17 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.4.65-1
- Update to 2.4.65 (RHBZ #1263878)

* Tue Aug 25 2015 Dave Airlie <airlied@redhat.com> 2.4.64-1
- libdrm 2.4.64

* Mon Jul 13 2015 Dan Horák <dan[at]danny.cz> 2.4.62-2
- valgrind needs explicit disable if not available

* Sun Jul 12 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.62-1
- libdrm 2.4.62
- Minor spec cleanups

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.61-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 07 2015 Ben Skeggs <bskeggs@redhat.com> 2.4.61-3
- build needs xorg-x11-util-macros now...

* Thu May 07 2015 Ben Skeggs <bskeggs@redhat.com> 2.4.61-2
- fixup patch, don't ship extra tests

* Thu May 07 2015 Ben Skeggs <bskeggs@redhat.com> 2.4.61-1
- libdrm 2.4.61

* Mon Mar 23 2015 Dave Airlie <airlied@redhat.com> 2.4.60-1
- libdrm 2.4.60

* Fri Jan 23 2015 Rob Clark <rclark@redhat.com> 2.4.59-4
- No we don't actually want to install the exynos tests

* Fri Jan 23 2015 Rob Clark <rclark@redhat.com> 2.4.59-3
- Add test apps to drm-utils package

* Thu Jan 22 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.59-2
- Enable tegra

* Thu Jan 22 2015 Dave Airlie <airlied@redhat.com> 2.4.59-1
- libdrm 2.4.59

* Wed Nov 19 2014 Dan Horák <dan[at]danny.cz> 2.4.58-3
- valgrind available only on selected arches

* Tue Nov 18 2014 Adam Jackson <ajax@redhat.com> 2.4.58-2
- BR: valgrind-devel so we get ioctl annotations

* Thu Oct 02 2014 Adam Jackson <ajax@redhat.com> 2.4.58-1
- libdrm 2.4.58

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Dave Airlie <airlied@redhat.com> 2.4.56-1
- libdrm 2.4.56

* Mon Jul  7 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.54-3
- Build freedreno support on aarch64 too

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 03 2014 Dennis Gilmore <dennis@ausil.us> 2.4.54-1
- libdrm 2.4.54

* Sun Apr 13 2014 Dave Airlie <airlied@redhat.com> 2.4.53-1
- libdrm 2.4.53

* Sat Feb 08 2014 Adel Gadllah <adel.gadllah@gmail.com> 2.4.52-1
- libdrm 2.4.52

* Thu Dec 05 2013 Dave Airlie <airlied@redhat.com> 2.4.50-1
- libdrm 2.4.50

* Mon Dec 02 2013 Dave Airlie <airlied@redhat.com> 2.4.49-2
- backport two fixes from master

* Sun Nov 24 2013 Dave Airlie <airlied@redhat.com> 2.4.49-1
- libdrm 2.4.49

* Fri Nov 08 2013 Dave Airlie <airlied@redhat.com> 2.4.47-1
- libdrm 2.4.47
- add fix for nouveau with gcc 4.8

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 03 2013 Dave Airlie <airlied@redhat.com> 2.4.46-1
- libdrm 2.4.46

* Tue Jun 18 2013 Adam Jackson <ajax@redhat.com> 2.4.45-2
- Sync some Haswell updates from git

* Thu May 16 2013 Dave Airlie <airlied@redhat.com> 2.4.45-1
- libdrm 2.4.45

* Sun Apr 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.44-2
- enable freedreno support on ARM

* Fri Apr 19 2013 Jerome Glisse <jglisse@redhat.com> 2.4.44-1
- libdrm 2.4.44

* Fri Apr 12 2013 Adam Jackson <ajax@redhat.com> 2.4.43-1
- libdrm 2.4.43

* Tue Mar 12 2013 Dave Airlie <airlied@redhat.com> 2.4.42-2
- add qxl header file

* Tue Feb 05 2013 Adam Jackson <ajax@redhat.com> 2.4.42-1
- libdrm 2.4.42

* Tue Jan 22 2013 Adam Jackson <ajax@redhat.com> 2.4.41-2
- Fix directory ownership in -devel (#894468)

* Thu Jan 17 2013 Adam Jackson <ajax@redhat.com> 2.4.41-1
- libdrm 2.4.41 plus git.  Done as a git snapshot instead of the released
  2.4.41 since the release tarball is missing man/ entirely.
- Pre-F16 changelog trim

* Wed Jan 09 2013 Ben Skeggs <bskeggs@redhat.com> 2.4.40-2
- nouveau: fix bug causing kernel to reject certain command streams

* Tue Nov 06 2012 Dave Airlie <airlied@redhat.com> 2.4.40-1
- libdrm 2.4.40

* Thu Oct 25 2012 Adam Jackson <ajax@redhat.com> 2.4.39-4
- Rebuild to appease koji and get libkms on F18 again

* Mon Oct 08 2012 Adam Jackson <ajax@redhat.com> 2.4.39-3
- Add exynos to arm

* Mon Aug 27 2012 Dave Airlie <airlied@redhat.com> 2.4.39-1
- upstream 2.4.39 release

* Tue Aug 14 2012 Dave Airlie <airlied@redhat.com> 2.4.38-2
- add radeon prime support

* Sun Aug 12 2012 Dave Airlie <airlied@redhat.com> 2.4.38-1
- upstream 2.4.38 release

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.37-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 25 2012 Dave Airlie <airlied@redhat.com> 2.4.37-3
- add libdrm prime support for core, intel, nouveau

* Mon Jul 23 2012 Adam Jackson <ajax@redhat.com> 2.4.37-2
- libdrm-2.4.37-i915-hush.patch: Silence an excessive error message

* Fri Jul 13 2012 Dave Airlie <airlied@redhat.com> 2.4.37-1
- bump to libdrm 2.4.37

* Thu Jun 28 2012 Dave Airlie <airlied@redhat.com> 2.4.36-1
- bump to libdrm 2.4.36

* Mon Jun 25 2012 Adam Jackson <ajax@redhat.com> 2.4.35-2
- Drop libkms. Only used by plymouth, and even that's a mistake.

* Fri Jun 15 2012 Dave Airlie <airlied@redhat.com> 2.4.35-1
- bump to libdrm 2.4.35

* Tue Jun 05 2012 Adam Jackson <ajax@redhat.com> 2.4.34-2
- Rebuild for new libudev
- Conditional BuildReqs for {libudev,systemd}-devel

* Sat May 12 2012 Dave Airlie <airlied@redhat.com> 2.4.34-1
- libdrm 2.4.34

* Fri May 11 2012 Dennis Gilmore <dennis@ausil.us> 2.4.34-0.3
- enable libdrm_omap on arm arches

* Thu May 10 2012 Adam Jackson <ajax@redhat.com> 2.4.34-0.2
- Drop ancient kernel Requires.

* Tue Apr 24 2012 Richard Hughes <rhughes@redhat.com> - 2.4.34-0.1.20120424
- Update to a newer git snapshot

* Sat Mar 31 2012 Dave Airlie <airlied@redhat.com> 2.4.33-1
- libdrm 2.4.33
- drop libdrm-2.4.32-tn-surface.patch

* Wed Mar 21 2012 Adam Jackson <ajax@redhat.com> 2.4.32-1
- libdrm 2.4.32
- libdrm-2.4.32-tn-surface.patch: Sync with git.

* Sat Feb 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.31-4
- Add gem_ binaries to x86 only exclusion too

* Wed Feb 22 2012 Adam Jackson <ajax@redhat.com> 2.4.31-3
- Fix build on non-Intel arches

* Tue Feb 07 2012 Jerome Glisse <jglisse@redhat.com> 2.4.31-2
- Fix missing header file

* Tue Feb 07 2012 Jerome Glisse <jglisse@redhat.com> 2.4.31-1
- upstream 2.4.31 release

* Fri Jan 20 2012 Dave Airlie <airlied@redhat.com> 2.4.30-1
- upstream 2.4.30 release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Adam Jackson <ajax@redhat.com> 2.4.27-2
- Fix typo in udev rule

* Tue Nov 01 2011 Adam Jackson <ajax@redhat.com> 2.4.27-1
- libdrm 2.4.27

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.26-4
- Rebuilt for glibc bug#747377

* Tue Oct 25 2011 Adam Jackson <ajax@redhat.com> 2.4.26-3
- Fix udev rule matching and install location (#748205)

* Fri Oct 21 2011 Dave Airlie <airlied@redhat.com> 2.4.26-2
- fix perms on control node in udev rule

* Mon Jun 06 2011 Adam Jackson <ajax@redhat.com> 2.4.26-1
- libdrm 2.4.26 (#711038)
