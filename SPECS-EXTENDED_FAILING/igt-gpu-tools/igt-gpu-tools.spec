%global gitdate 20201203

Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           igt-gpu-tools
Version:        1.25
Release:        3%{?dist}
Summary:        Test suite and tools for DRM drivers

License:        MIT
URL:            https://gitlab.freedesktop.org/drm/igt-gpu-tools

%if 0%{?gitdate}
Source0:        igt-gpu-tools-%{gitdate}.tar.bz2
%else
Source0:        https://gitlab.freedesktop.org/drm/igt-gpu-tools/-/archive/igt-gpu-tools-%{version}/igt-gpu-tools-igt-gpu-tools-%{version}.tar.bz2
%endif
Source1:        make-git-snapshot.sh

%global provobs_version 2.99.917-42.20180618
Provides:       xorg-x11-drv-intel-devel = %{provobs_version}
Provides:       intel-gpu-tools = %{provobs_version}
Obsoletes:      xorg-x11-drv-intel-devel < %{provobs_version}
Obsoletes:      intel-gpu-tools < %{provobs_version}

BuildRequires:  meson >= 0.51.0
BuildRequires:  gcc
BuildRequires:  flex bison
BuildRequires:  pkgconfig(libdrm) >= 2.4.82
BuildRequires:  pkgconfig(pciaccess) >= 0.10
BuildRequires:  pkgconfig(libkmod)
BuildRequires:  pkgconfig(libprocps)
BuildRequires:  pkgconfig(libdw)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(valgrind)
BuildRequires:  pkgconfig(cairo) > 1.12.0
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gsl)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(xmlrpc)
BuildRequires:  pkgconfig(xmlrpc_util)
BuildRequires:  pkgconfig(xmlrpc_client)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(liboping)
BuildRequires:  kernel-headers
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  python3-docutils
BuildRequires:  alsa-lib-devel

# libunwind 1.4.0+ supports s390x
%ifnarch s390x
BuildRequires:  pkgconfig(libunwind)
%endif

%description
igt-gpu-tools (formerly known as intel-gpu-tools) is the standard for writing
test cases for DRM drivers. It also includes a handful of useful tools for
various drivers, such as Intel's GPU tools for i915.

%package docs
Summary:        Documentation for igt-gpu-tools

%description docs
gtk-doc generated documentation package for igt-gpu-tools.

%package devel
Summary:        Development files for igt-gpu-tools

%description devel
Development files for compiling against certain tools provided by
igt-gpu-tools, such as i915-perf.

%prep
%autosetup -c -p1

%build


%global with_libunwind disabled

# Mariner python3-doctuils does not ship with rst2man which is required for docs.
# Add a symbolic link to appease the build.

ln -s %{_bindir}/rst2man3 %{_bindir}/rst2man


# gcc-11 issues a false positive for accesses to hdmi_vsdb in
# cea_vsdb_get_hdmi_default
CFLAGS="%{build_cflags} -Wno-array-bounds"

# Some explanations here
# - We don't build overlay yet due to Fedora not shipping /usr/bin/leg, but we
#   probably don't care about that anyway
# - We specify -Db_ndebug=false because upstream has explicitly stated that
#   anything else is officially unsupported
# - Attempting to resolve all of the symbols within IGT at executable start
#   causes some of igt's symbols to be resolved in the wrong order, resulting in
#   certain runtime function resolvers (e.g. __attribute__((ifunc))) attempting
#   to call functions which have not been resolved yet - causing everything to
#   segfault. Because of this, we specify "-Dc_link_args=-z lazy" to force lazy
#   symbol resolution.
%meson \
        -Db_ndebug=false \
        -Dc_link_args="-z lazy" \
        -Doverlay=disabled \
        -Dlibunwind=%{with_libunwind}
%meson_build

%install
%meson_install

%ifarch %{ix86} x86_64
rm %{buildroot}/%{_libdir}/pkgconfig/intel-gen4asm.pc
%endif

# Remove the unversioned libigt symlinks
rm %{buildroot}/%{_libdir}/libigt.so

%check
# The timeout multiplier here is required due to certain tests timing out on
# koji builders that are under heavy load.
%meson_test --timeout-multiplier 16

%files
%license COPYING
%ifarch %{ix86} x86_64
%{_bindir}/intel-gen4asm
%{_bindir}/intel-gen4disasm
%{_bindir}/intel_dump_decode
%{_bindir}/intel_error_decode
%{_bindir}/intel_framebuffer_dump
%{_bindir}/intel_perf_counters
%endif
%{_libdir}/libigt.so.0
%{_libdir}/libi915_perf.so.*
%{_libexecdir}/igt-gpu-tools/*
%{_datadir}/igt-gpu-tools/*
%{_bindir}/dpcd_reg
%{_bindir}/igt_*
%{_bindir}/i915-perf-*
%{_bindir}/intel_audio_dump
%{_bindir}/intel_backlight
%{_bindir}/intel_bios_dumper
%{_bindir}/intel_display_crc
%{_bindir}/intel_display_poller
%{_bindir}/intel_dp_compliance
%{_bindir}/intel_firmware_decode
%{_bindir}/intel_forcewaked
%{_bindir}/intel_gem_info
%{_bindir}/intel_gpu_abrt
%{_bindir}/intel_gpu_frequency
%{_bindir}/intel_gpu_time
%{_bindir}/intel_gpu_top
%{_bindir}/intel_gtt
%{_bindir}/intel_guc_logger
%{_bindir}/intel_gvtg_test
%{_bindir}/intel_infoframes
%{_bindir}/intel_l3_parity
%{_bindir}/intel_lid
%{_bindir}/intel_opregion_decode
%{_bindir}/intel_panel_fitter
%{_bindir}/intel_reg
%{_bindir}/intel_reg_checker
%{_bindir}/intel_residency
%{_bindir}/intel_stepping
%{_bindir}/intel_vbt_decode
%{_bindir}/intel_watermark
%{_bindir}/amd_hdmi_compliance
%{_bindir}/msm_dp_compliance
%{_bindir}/lsgpu
%{_mandir}/man1/intel_*.1*

%files devel
%license COPYING
%{_includedir}/i915-perf/*
%{_libdir}/pkgconfig/i915-perf.pc
%{_libdir}/libi915_perf.so

%files docs
%license COPYING
%{_datadir}/gtk-doc/html/igt-gpu-tools/*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.25-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Sep 16 2021 Muhammad Falak <mwani@microsoft.com> - 1.25-2.20201203gitd67bad6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add explicit BR on `alsa-lib-devel`
- Add a symbolic link `rst2man` -> `rst2man3` which is needed for docs. Mariner python3-docutils does not ship with `rst2man`
- Disable `libunwind` support which conflicts while linking the library

* Thu Dec  3 18:41:08 EST 2020 Lyude Paul <lyude@redhat.com> - 1.25-1.20201203gitd67bad6
- New git snapshot

* Tue Dec  1 12:52:05 EST 2020 Lyude Paul <lyude@redhat.com> - 1.25-1.20201201gitc36f797
- New git snapshot

* Sun Nov  8 13:16:16 EST 2020 Lyude Paul <lyude@redhat.com> - 1.25-1.20201108git80435e0
- New git snapshot
- Fixes broken automatic device selection in intel_gpu_top (#1893536)

* Mon Oct 26 2020 Lyude Paul <lyude@redhat.com> - 1.25-1.20201026git7fd7e3f
- New git snapshot

* Thu Oct 15 2020 Jeff Law <law@redhat.com> - 1.25-2.20201012gitd5f40f0
- Work around false positive diagnostic with gcc-11

* Mon Oct 12 2020 Lyude Paul <lyude@redhat.com> - 1.25-1.20201012gitd5f40f0
- New git snapshot
- Also fixes potential crash in intel_gpu_top when no devices are found

* Sat Sep 26 2020 Lyude Paul <lyude@redhat.com> - 1.25-1.20200926gitebc9ca5
- New git snapshot

* Sun Sep 20 2020 Lyude Paul <lyude@redhat.com> - 1.25-1.20200920git0ec9620
- New git snapshot

* Thu Sep 03 2020 Lyude Paul <lyude@redhat.com> - 1.25-1.20200903gitc240b5c
- New git snapshot

* Tue Aug 25 2020 Lyude Paul <lyude@redhat.com> - 1.25-1.20200825gitf1d0c24
- New git snapshot

* Tue Aug 18 2020 Lyude Paul <lyude@redhat.com> - 1.25-1.20200818git4e5f76b
- New git snapshot

* Sat Aug 08 2020 Lyude Paul <lyude@redhat.com> - 1.25-1.20200808git9f09772
- New git snapshot

* Sun Jul 19 2020 Lyude Paul <lyude@redhat.com> - 1.25-1.20200719git9b964d7
- New git snapshot

* Sat Jul 04 2020 Lyude Paul <lyude@redhat.com> - 1.25-1.20200704git75bcaf7
- New git snapshot

* Tue Apr 21 2020 Björn Esser <besser82@fedoraproject.org> - 1.24-4.20191213git048f585
- Rebuild (json-c)

* Mon Apr 13 2020 Björn Esser <besser82@fedoraproject.org> - 1.24-3.20191213git048f585
- Add patch to fix build with GCC-10

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-2.20191213git048f585
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 13 2019 Lyude Paul <lyude@redhat.com> - 1.24-1.20191213git048f585
- New git snapshot

* Mon Dec 02 2019 Lyude Paul <lyude@redhat.com> - 1.24-1.20191202git9df50ae
- New git snapshot

* Fri Nov 01 2019 Lyude Paul <lyude@redhat.com> - 1.24-1.20191101gitc8a88b6
- New git snapshot

* Tue Oct 08 2019 Lyude Paul <lyude@redhat.com> - 1.24-1.20191008git869ed1e
- New git snapshot

* Fri Sep 27 2019 Lyude Paul <lyude@redhat.com> - 1.24-1.20190927git5a6c685
- New git snapshot

* Tue Sep 17 2019 Lyude Paul <lyude@redhat.com> - 1.24-2.20190917gitc78b995
- Increase meson_test timeout, again, so that tests don't time out on s390x

* Tue Sep 17 2019 Lyude Paul <lyude@redhat.com> - 1.24-1.20190917gitc78b995
- Add new liboping dependency
- New git snapshot

* Fri Sep 06 2019 Lyude Paul <lyude@redhat.com> - 1.24-1.20190906git3fb0f22
- New git snapshot

* Fri Aug 30 2019 Lyude Paul <lyude@redhat.com> - 1.24-1.20190830gite62ea30
- New git snapshot

* Thu Aug 29 2019 Lyude Paul <lyude@redhat.com> - 1.24-1.20190829gitd38950f
- New git snapshot

* Wed Aug 21 2019 Lyude Paul <lyude@redhat.com> - 1.24-1.20190821git357dbe1
- New git snapshot
- New release version

* Tue Aug 20 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.23-2.20190811gitf43f5fa
- Rebuilt for GSL 2.6.

* Sun Aug 11 2019 Lyude Paul <lyude@redhat.com> - 1.23-1.20190811gitf43f5fa
- New git snapshot

* Thu Aug 01 2019 Lyude Paul <lyude@redhat.com> - 1.23-1.20190801gitb3138fb
- New git snapshot

* Thu Jul 25 2019 Lyude Paul <lyude@redhat.com> - 1.23-1.20190725git7e4d105
- New git snapshot

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-2.20190722gitf3b3f93
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Lyude Paul <lyude@redhat.com> - 1.23-1.20190722gitf3b3f93
- New git snapshot

* Fri Jul 12 2019 Lyude Paul <lyude@redhat.com> - 1.23-1.20190712git549e1cd
- New git snapshot

* Tue Jul 09 2019 Lyude Paul <lyude@redhat.com> - 1.23-1.20190709git2a66ae6
- New git snapshot

* Fri Jun 28 2019 Lyude Paul <lyude@redhat.com> - 1.23-1.20190628git03779dd
- New git snapshot

* Wed Jun 26 2019 Lyude Paul <lyude@redhat.com> - 1.23-1.20190626git15ad664
- New git snapshot

* Fri Jun 21 2019 Lyude Paul <lyude@redhat.com> - 1.23-1.20190621git22850c1
- New git snapshot

* Wed Jun 19 2019 Lyude Paul <lyude@redhat.com> - 1.23-1.20190619gitc88ced7
- New git snapshot

* Fri May 31 2019 Lyude Paul <lyude@redhat.com> - 1.23-1.20190531git4108c74
- New git snapshot

* Wed May 22 2019 Lyude Paul <lyude@redhat.com> - 1.23-1.20190522gitadf9f43
- New git snapshot

* Thu May 16 2019 Lyude Paul <lyude@redhat.com> - 1.23-1.20190516git555019f
- Initial package

# vim: expandtab
