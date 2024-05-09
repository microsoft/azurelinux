#
# spec file for package libva
#
# Copyright (c) 2023 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


#

%define build_gl 0
%define sover 2

Name:           libva
%define _name   libva
Version:        2.20.0
Release:        1%{?dist}
Summary:        Video Acceleration (VA) API
License:        MIT
Group:          Development/Libraries/C and C++
URL:            https://01.org/linuxmedia
Source0:        https://github.com/intel/libva/archive/%{version}.tar.gz#/libva-%{version}.tar.gz
Source2:        baselibs.conf
Patch0:         propagate-dpy.patch
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  meson
BuildRequires:  pkgconf-pkg-config
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(wayland-client) >= 1.11.0
BuildRequires:  pkgconfig(wayland-scanner) >= 1.11.0
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  libXv-devel
%if %{build_gl}
BuildRequires:  pkgconfig(gl)
%endif

%description
The libva library implements the Video Acceleration API.
The library loads a hardware dependendent driver.

%package -n libva-glx%{sover}
Summary:        GLX backend for the Video Acceleration API
Group:          System/Libraries
Supplements:    libva%{sover}

%description -n libva-glx%{sover}
The libva library implements the Video Acceleration API.
The library loads a hardware dependendent driver.

This is the VA/GLX runtime library.

%package -n libva-wayland%{sover}
Summary:        Wayland backend for the Video Acceleration API
Group:          System/Libraries

%description -n libva-wayland%{sover}
The libva library implements the Video Acceleration API.
The library loads a hardware dependendent driver.

%package devel
Summary:        Development files for the Video Acceleration API
Group:          Development/Languages/C and C++
%if 0%{?build_gl}
BuildRequires:  libva-devel = %{version}
Requires:       libva-glx%{sover} = %{version}
Requires:       pkgconfig(gl)
%else
Requires:       libva%{sover} = %{version}
Requires:       libva-drm%{sover} = %{version}
Requires:       libva-wayland%{sover} = %{version}
Requires:       libva-x11-%{sover} = %{version}
Requires:       pkgconfig(libdrm)
Requires:       pkgconfig(x11)
Requires:       pkgconfig(xfixes)
Recommends:     libva-gl-devel
%endif

%description devel
The libva library implements the Video Acceleration API.
The library loads a hardware dependendent driver.

%if 0%{?build_gl}
This package provides the development environment for libva gl packages.
%else
This package provides the development environment for libva packages.
%endif

%package -n libva%{sover}
Summary:        Video Acceleration API
Group:          System/Libraries

%description -n libva%{sover}
The libva library implements the Video Acceleration API.
The library loads a hardware dependendent driver.

This is the core runtime library.

%package -n libva-drm%{sover}
Summary:        DRM backend for the Video Acceleration API
Group:          System/Libraries
Supplements:    libva%{sover}

%description -n libva-drm%{sover}
The libva library implements the Video Acceleration API.
The library loads a hardware dependendent driver.

This is the VA/DRM runtime library.

%package -n libva-x11-%{sover}
Summary:        X11 backend for the Video Acceleration API
Group:          System/Libraries
Supplements:    libva%{sover}

%description -n libva-x11-%{sover}
The libva library implements the Video Acceleration API.
The library loads a hardware dependendent driver.

This is the VA/X11 runtime library.

%prep
%autosetup -n %{_name}-%{version} -p1

%build
%meson \
	-D driverdir=%{_libdir}/dri \
%if %{build_gl}
	-D with_glx=yes \
	-D with_x11=yes \
	-D disable_drm=true \
	-D with_wayland=no \
	-D with_win32=no \
%else
	-D with_glx=no \
%endif
	%{nil}
%meson_build

%install
%meson_install

%if %{build_gl}
# remove all files packaged during without gl mode
rm -rf `find %{buildroot}%{_includedir}/va/* | grep -v "glx"`
rm -rf `find %{buildroot}%{_libdir}/libva* | grep -v "glx"`
rm -rf `find %{buildroot}%{_libdir}/pkgconfig/libva*.pc | grep -v "glx"`
%endif

%ldconfig_scriptlets -n libva-glx%{sover}
%ldconfig_scriptlets -n libva-wayland%{sover}
%ldconfig_scriptlets -n libva%{sover}
%ldconfig_scriptlets -n libva-drm%{sover}
%ldconfig_scriptlets -n libva-x11-%{sover}

%if %{build_gl}
%files -n libva-glx%{sover}
%{_libdir}/libva-glx.so.%{sover}*

%files devel
%{_libdir}/libva-glx.so
%{_includedir}/va/va_glx.h
%{_includedir}/va/va_backend_glx.h
%{_libdir}/pkgconfig/libva-glx.pc
%else

%files -n libva%{sover}
%license COPYING
%{_libdir}/libva.so.*

%files -n libva-x11-%{sover}
%{_libdir}/libva-x11.so.*

%files -n libva-drm%{sover}
%{_libdir}/libva-drm.so.*

%files -n libva-wayland%{sover}
%{_libdir}/libva-wayland.so.%{sover}*

%files devel
%{_libdir}/libva.so
%{_libdir}/libva-x11.so
%{_libdir}/libva-drm.so
%{_libdir}/libva-wayland.so
%{_includedir}/va
%{_libdir}/pkgconfig/libva-drm.pc
%{_libdir}/pkgconfig/libva-x11.pc
%{_libdir}/pkgconfig/libva-wayland.pc
%{_libdir}/pkgconfig/libva.pc
%endif

%changelog
* Fri Mar 29 2024 Nan Liu <liunan@microsoft.com> - 2.20.0-1
- Upgrade to 2.20.0 using openSUSE Tumbleweed.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.11.0-143
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Apr 15 2021 Henry Li <lihl@microsoft.com> - 2.11.0-142.2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Change %makeinstall to the right installation command

* Wed Mar 24 2021 Dirk Müller <dmueller@suse.com>
- update to 2.11.0:
  * add: LibVA Protected Content API
  * add: Add a configuration attribute to advertise AV1d LST feature
  * fix: wayland: don't try to authenticate with render nodes
  * autotools: use shell grouping instead of sed to prepend a line
  * trace: Add details data dump for mpeg2 IQ matrix.
  * doc: update docs for VASurfaceAttribPixelFormat
  * doc: Libva documentation edit for AV1 reference frames
  * doc: Modify AV1 frame_width_minus1 and frame_height_minus1 comment
  * doc: Remove tile_rows and tile_cols restriction to match AV1 spec
  * doc: Format code for doxygen output
  * doc: AV1 decode documentation edit for superres_scale_denominator
  * ci: upgrade FreeBSD to 12.2
  * ci: disable travis build
  * ci: update cache before attempting to install packages
  * ci: avoid running workloads on other workloads changes
  * ci: enable github actions
* Wed Dec 16 2020 Aaron Stern <ukbeast89@protonmail.com>
- update to 2.10.0:
  * add: Pass offset and size of pred_weight_table
  * add: add vaCopy interface to copy surface and buffer
  * add: add definition for different execution
  * add: New parameters for transport controlled BRC were added
  * add: add FreeBSD support
  * add: add a bufer type to adjust context priority dynamically
  * fix: correct the api version in meson.build
  * fix: remove deprecated variable from va_trace.c
  * fix: Use va_deprecated for the deprecate variable
  * fix: Mark chroma_sample_position as deprecated
  * doc: va_dec_av1: clarifies CDEF syntax element packing
  * doc: [AV1] Update documented ranges for loop filter and quantization params.
  * doc: Update va.h for multi-threaded usages
  * trace: va/va_trace: ignore system gettid() on Linux
* Thu Nov 26 2020 Dirk Mueller <dmueller@suse.com>
- update to 2.9.1:
  * fix version mismatch between meson and autotools
* Mon Oct  5 2020 Aaron Stern <ukbeast89@protonmail.com>
- update to 2.9.0:
  * trace: Refine the va_TraceVAPictureParameterBufferAV1.
  * doc: Add comments for backward/forward reference to avoid confusion
  * doc: Modify comments in av1 decoder interfaces
  * doc: Update mailing list
  * Add SCC fields trace for HEVC SCC encoding.
  * Add FOURCC code for Y212 and Y412 format.
  * Add interpolation method for scaling.
  * add attributes for context priority setting
  * Add vaSyncBuffer for output buffers synchronization
  * Add vaSyncSurface2 with timeout
* Mon Aug 31 2020 Stefan Dirsch <sndirsch@suse.com>
- version 2.8.0 needed for jira#SLE/SLE-12712
* Sat Aug 15 2020 Dirk Mueller <dmueller@suse.com>
- update to 2.8.0:
  * trace: enable return value trace for successful function call
  * trace: divide va_TraceEndPicture to two seperate function
  * trace: add support for VAProfileHEVCSccMain444_10
  * fix:Fixes file descriptor leak
  * add fourcc code for P012 format
  * travis: Add a test that code files don't have the exec bit set
  * Remove the execute bit from all source code files
  * meson: Allow for libdir and includedir to be absolute paths
  * trace: Fix format string warnings
  * fix:Fix clang warning (reading garbage)
  * add definition to enforce both reflist not empty
  * trace: List correct field names in va_TraceVAPictureParameterBufferHEVC
  * change the return value to be UNIMPLEMENTED when the function pointer is NULL
  * remove check of vaPutSurface implementation
  * Add new slice structure flag for CAPS reporting
  * VA/X11: VAAPI driver mapping for iris DRI driver
  * VA/X11: enable driver candidate selection for DRI2
  * Add SCC flags to enable/disable features
  * fix: Fix HDR10 MaxCLL and MaxFALL documentation
  * Add VAProfileHEVCSccMain444_10 for HEVC
  * change the compatible list to be dynamic one
  * trace:Convert VAProfileAV1Profile0 VAProfileAV1Profile1 to string
* Fri Apr 10 2020 Stefan Dirsch <sndirsch@suse.com>
- Update to version 2.7.0
  * trace: av1 decode buffers trace
  * trace: Add HEVC REXT and SCC trace for decoding.
  * Add av1 decode interfaces
  * Fix crashes on system without supported hardware by PR #369.
  * Add 2 FourCC for 10bit RGB(without Alpha) format: X2R10G10B10
    and X2B10G10R10.
  * Fix android build issue #365 and remove some trailing
    whitespace
  * Adjust call sequence to ensure authenticate operation is
    executed to fix #355
* Fri Mar  6 2020 Stefan Dirsch <sndirsch@suse.com>
- cleanup in specfile: get rid of is_opensuse macro, which is no
  longer needed at all since sle15/Leap15, where we always enable
  wayland support (jira#PM-1623)
* Wed Feb 26 2020 Stefan Dirsch <sndirsch@suse.com>
- Update to version 2.6.1
  * adjust call sequence to ensure authenticate operation is
    executed this patch is not needed for media-driver, but
    needed for i965 driver which check authentication.
* Fri Jan 10 2020 Aaron Stern <ukbeast89@protonmail.com>
- Update to version 2.6.0:
  * enable the mutiple driver selection logic and enable it for DRM.
  * drm: Add iHD to driver_name_map
  * Add missed slice parameter 'slice_data_num_emu_prevn_bytes'
  * ensure that all meson files are part of the release tarball
  * configure: use correct comparison operator
  * trace: support VAConfigAttribMultipleFrame in trace
  * remove incorrect field of VAConfigAttribValDecJPEG
  * va/va_trace: Dump VP9 parameters for profile 1~3
  * add multiple frame capability report
  * add variable to indicate layer infromation
  * trace: fix memory leak on closing the trace
  * add prediction direction caps report
  * Add comments for colour primaries and transfer characteristics in VAProcColorProperties
* Thu Nov  7 2019 Stefan Dirsch <sndirsch@suse.com>
- This release is needed for latest intel-media-driver update
  (jsc#SLE-8838)
* Wed Aug 21 2019 Aaron Stern <ukbeast89@protonmail.com>
- Update to version 2.5.0:
  * Correct the comment of color_range.
  * Add VA_FOURCC_A2B10G10R10 for format a2b10g10r10.
  * Adjust VAEncMiscParameterQuantization structure to be align with VAEncMiscParameterBuffer(possible to impact BC)
  * Add attribute for max frame size
  * Add va_footer.html into distribution build
  * va_trace: hevc profiles added
  * Add new definition for input/output surface flag
  * va/va_trace: add trace support for VAEncMiscParameterTypeSkipFrame structure.
  * va/va_trace: add MPEG2 trace support for MiscParam and SequenceParam
  * va_openDriver: check strdup return value
  * Mark some duplicated field as deprecated
  * Add return value into logs
  * va/va_trace: add trace support for VAEncMiscParameterEncQuality structure.
  * Add newformat foucc defination
  * va_backend: remove unneeded linux/videodev2.h include
  * va_trace: add missing <sys/time.h> include
  * configure: don't build glx if VA/X11 isn't built
  * va/va_trace: unbreak with C89 after b369467
  * [common] Add A2RGB10 fourcc definition
  * build: meson: enables va messaging and visibility
  * va/va_trace: add trace support for RIR(rolling intra refresh).
  * va/va_trace: add trace support for ROI(region of interest)
* Sat Jul  6 2019 Bjørn Lie <bjorn.lie@gmail.com>
- Update to version 2.4.1:
  * [common] Add A2RGB10 fourcc definition.
  * build: meson: enables va messaging and visibility.
  * va/va_trace:
  - Add trace support for RIR(rolling intra refresh).
  - Add trace support for ROI(region of interest).
* Sat Jan 26 2019 bjorn.lie@gmail.com
- Update to version 2.4.0:
  * va_TraceSurface support for VA_FOURCC_P010
  * Add pointer to struct wl_interface for driver to use
  * (integrate) va: fix new line symbol in error message
  * av: avoid driver path truncation
  * Fix compilation warning (uninit and wrong variable types) for
    Android O MR1
  * Allow import of the DRM PRIME 2 memory type
  * android: ignore unimportant compile warnnings
  * compile: fix sign/unsign compare in va_trace.c
  * android: replace utils/Log.h with log/log.h
  * High Dynamic Range Tone Mapping: Add a new filter for input
    metadata and some comments
  * Remove restrictions on vaSetDriverName()
* Tue Oct 30 2018 chris@computersalat.de
- Update to 2.3.0
  * Bump VA-API version to 1.3.0 and libva to 2.3.0
  * Add max frame size parameters for multiple pass case in legacy mode
  * Add new BRC mode AVBR
  * Add new interface for High Dynamic Range tone mapping
  * Add missing enum to string conversions
  * Add hevc subsets parameters structure
  * Add Customized Noise Reduction (HVS) interfaces
  * Add new BRC mode definition QVBR
  * Add more complete colour properties for use in VPP
* Tue Jul 17 2018 tiwai@suse.de
- Update to 2.2.0:
  * Bump VA-API version to 1.2.0 and libva to 2.2.0
  * Add support for hevc range extension decoding
  * Add support for fast intra prediction in HEVC FEI
  * Add 10/12-bit YUV render target formats
  * Add fourcc code for Y210/Y216/Y410/Y416/RGB565/BGR565
  * Add VA_STATUS_ERROR_NOT_ENOUGH_BUFFER
  * Add VA_SURFACE_ATTRIB_USAGE_HINT_EXPORT
  * Improve documentation
- Use license tag
* Mon May  7 2018 sndirsch@suse.com
- Update to 2.1.0
  * Bump VA-API version to 1.1.0 and libva to 2.1.0
  * Add API for multi-frame processing
  * Add entrypoint VAEntrypointStats for Statistics
  * Add data structures for HEVC FEI support
  * Add new attributes for decoding/encoding/video processing
  * Add new VPP filter for Total Color Correction
  * Add blending interface in VPP
  * Add rotation interface in VPP
  * Add mirroring interface in VPP
  * Add Chroma siting flags in VPP
  * Add new color standard definitions
  * Add new interface for exporting surface
  * Add message callbacks for drivers to use
* Fri Nov 17 2017 zaitor@opensuse.org
- Drop erroneous --disable-wayland configure call passed when
  building gl part.
- Drop vaapi-wayland-tools sub-package, it does not contain any
  files.
- Clean up spec, explicitly list .pc files, ensure they go into the
  correct devel package, stop rm'ing binaries that no longer exist.
* Wed Nov  8 2017 alarrosa@suse.com
- Update to 2.0.0
  * Bump VA-API version to 1.0.0 and libva to 2.0.0
  * Add new API for H264 FEI support
  * Add definition of VA_FOURCC_I420
  * Add functions for converting common enums to strings
  * Deprecate H.264 baseline profile and FMO support
  * Deprecate packed misc packed header flag
  * Delete libva-tpi and libva-egl backends
  * Refine VASliceParameterBufferHEVC, VAEncMiscParameterBuffer
  * Fix errors in VAConfigAttribValEncROI, VAEncMacroblockParameterBufferH264
  * Fix race condition in wayland support
  * Rename vaMessageCallback to VAMessageCallback
  * Make logging callbacks library-safe
- Note libva 2.0.0 is not compatible with the old version of libva, but for
  most users, what you need to do is to rebuild your VA-API based application
  against libva 2.0.0.
- The soversion of the generated packages is increased to 2.
- Subpackage libva-egl1 is no longer generated since upstream removed support
  for the libva-egl backend.
- The libva2 package no longer includes the libva-tpi library since upstream
  removed support for the libva-tpi backend.
* Tue Aug 29 2017 jengelh@inai.de
- Fix RPM groups. Trim obvious "Linux" from description.
- Remove some %%if..%%endif blocks which are not necessary and
  which do not affect the build.
* Sat Aug 26 2017 zaitor@opensuse.org
- Move wayland to build_gl.
- Drop vaapi-dummy-driver Recommends, package does not exist
  anymore.
* Fri Aug 18 2017 sndirsch@suse.com
- fixed source URLs
* Wed Aug 16 2017 chris@computersalat.de
- Version 1.8.3 - 28.Jun.2017
  * Fix build issue on Android
  * Remove the dummy driver
  * Add traces for MB rate control / temporal layer
  * Set verbosity level between {0, 1, 2} by setting the variable
    LIBVA_MESSAGING_LEVEL in /etc/libva.conf or by setting the
    environment variable LIBVA_MESSAGING_LEVEL.
- remove subpkg vaapi-dummy-driver
* Wed Aug  9 2017 sndirsch@suse.com
- added COPYING as documentation file
* Fri Aug  4 2017 sndirsch@suse.com
- Version 1.8.2
  * Bump libva to 1.8.2
* Wed Apr 19 2017 chris@computersalat.de
- fix changes file
  * add missing changes for 1.8.1
  * fix Version string
* Tue Apr 18 2017 chris@computersalat.de
- Version 1.8.1 - 10.Apr.2017
  * Bump libva to 1.8.1
- add sha1sum file
* Sat Apr 15 2017 chris@computersalat.de
- Version 1.8.0 - 31.March.2017
  * Bump VA API version to 0.40
  * API: Change vaRenderPicture semantics that vaRenderPicture no
    longer deletes the input buffer automatically.
  * API: Add VA_FOURCC_I010 for 10bit surface
  * API: Add vaSetErrorCallback and vaSetInfoCallback for error
    and info message.
  * va/drm: Update the support for Mesa Gallium driver
  * va/drm: Fix authentication check for /dev/dri/card0
  * Move all utilities and tests to libva-utils
    (https://github.com/01org/libva-utils)
- disable obsolete vaapi-tools cause of move of all utilities to
  libva-utils
* Tue Apr 11 2017 sndirsch@suse.com
- SLE merge:
  * update to latest version, Intel Stack release 2016Q1
    (fate #315643-315645, 319159-319161, 319618)
  * latest updates for sle12 (fate #315643-315645, 319159-319161,
    319618)
* Tue Apr 11 2017 sndirsch@suse.com
- Removed libva-wayland1 from bqaselibs.conf; add it to
  baselibs.conf during a wayland build only; ugly I know ... This
  is needed since otherwise source validator
  ("osc service run source_validator") fails on sle
* Tue Apr 11 2017 sndirsch@suse.com
- sync openSUSE Leap/SLE build by making use of %%is_opensuse macro;
  we don't build wayland on SLE, but enable it on Leap
* Tue Jan 17 2017 sndirsch@suse.com
- N_libva_Fix_wayland-client.h_include-path.patch/
  N_libva_Fix_wayland-client.h_include-path_1320.patch no longer
  need after adjusting vaapi-intel-driver package
* Thu Jan 12 2017 chris@computersalat.de
- fix wayland-client.h include path
  * add N_libva_Fix_wayland-client.h_include-path.patch
  * add N_libva_Fix_wayland-client.h_include-path_1320.patch
* Sat Dec 31 2016 chris@computersalat.de
- Version 1.7.3 - 10.Nov.2016
  * Bump VA API version to 0.39.4
  * API: add support for bitrate control per temporal layer
  * API: update the usage for framerate in VAEncMiscParameterFrameRate
    to support non-integer frame-rate
  * Add has_prime_sharing flag in VADriverVTableWayland to indicate if
    buffer sharing with prime fd can be used in the backend driver
* Sat Oct 22 2016 chris@computersalat.de
- Version 1.7.2 - 05.Sep.2016
  * Bump VA API version to 0.39.3
  * API: add support for ROI
  * Add support for VP9 encoder in VA tracer
  * Refine test cases
  * Fix the issue of not properly terminating the parsed environment
    values with '\0'
    https://bugs.freedesktop.org/show_bug.cgi?id=96677
* Mon Jul  4 2016 sndirsch@suse.com
- Update to version 1.7.1
  * Bump VA API version to 0.39.2
  * API: add support for VP9 8bit encode
  * API: add support for low power/high performance encode
  * API: add support for encoding ROI attribute
  * API: add support for macroblock based rate control
  * Fix VA tracer to support multiple contexts in one instance
* Thu May 19 2016 zaitor@opensuse.org
- Add missing post/postun handling for libva-wayland1.
* Tue Apr 12 2016 sndirsch@suse.com
- Update to version 1.7.0
  * Bump VA API version to 0.39
  * Add support for VP9 10bit decode API
  * Allow libva to load the vaapi driver provided by Mesa Gallium
    for nouveau and radeon
  * Fix libva-glx against OpenGL 3.1 or above
* Wed Dec 30 2015 jimmy@boombatower.com
- Update baselibs.conf to work with new multi-spec file approach.
* Mon Dec 21 2015 dimstar@opensuse.org
- Use build_gl defines instead of build condition: libva-gl is
  never meant to be built --without=gl, so bcond is actually the
  wrong construct here.
- Add libva-gl.spec as a 2nd spec file to the package to keep them
  in sync (by means of pre_checkin.sh).
* Fri Dec 18 2015 jimmy@boombatower.com
- Bump up disable wayland support for 13.1 as 1.6.2 is incompatible
  with such old version of wayland.
* Thu Dec 17 2015 jimmy@boombatower.com
- Rework spec to either gl packages or everything else. By doing so
  libva-devel can be built without depending on Mesa and Mesa-libva
  can be build depending on libva-devel without introducing a
  dependency cycle. A linked package will then produce the libva
  gl packages.
* Thu Dec 17 2015 zaitor@opensuse.org
- Update to version 1.6.2:
  + Bump VA API version to 0.38.1.
  + Add new RT format for 16 bits per channel memory
    layout(P010,P016): VA_RT_FORMAT_YUV420_10BPP.
  + Add new fourcc codes: VA_FOURCC_P010, VA_FOURCC_P016,
    VA_FOURCC_YV16.
  + Fix crash if user doesn't have right to access the DRI device.
  + Fix uninitialized x11_screen driver context member for X11
    output (fdo#61603).
  + Fix the issue of not to use LIBVA_DRIVER_NAME (fdo#72822).
  + Fix build issue with wayland (fdo#79478).
  + vainfo: Add option '--display'.
* Thu Dec 17 2015 jimmy@boombatower.com
- Replace build requirement Mesa-devel with pkgconfig(egl) to
  narrow dependency and aid in avoiding cycle when building
  Mesa-libva.
* Mon Nov 23 2015 zaitor@opensuse.org
- Update to version 1.6.1:
  + Add support for VP9 decode and HEVC encode in VA trace module.
  + Add VP9 profile to vainfo.
  + Enhance VA trace to dump VP8 encode parameters.
- Add an explicit pkgconfig(wayland-scanner) BuildRequires:
  Configure looks for it, and we are already pulling it in
  automatically.
* Fri Jul 31 2015 zaitor@opensuse.org
- Update to version 1.6.0:
  + API:
  - Bump VA API version to 0.38.
  - Add support for HEVC Encode.
  - Add support for VP9 Decode.
  - Allow user to specify user preferred backend driver.
  - Add decode attribute to support decode normal and base modes.
  - Add encode attribute to support skip frame.
  + Fix quality issue in the JPEG encode demo.
* Mon Mar 30 2015 sndirsch@suse.com
- Update to version 1.5.1
  * API: correct the comment for num_token_partitions in struct
    _VAEncPictureParameterBufferVP8
  * VA/x11: fix double Unlocks/SyncHandle to avoid segmentation fault
* Sun Feb  8 2015 zaitor@opensuse.org
- Update to version 1.5.0:
  + API:
  - Add support for HEVC decoding.
  - Extend JPEG encoding data structures and add configuration
    attribute for JPEG encoding.
  + Add a unit test for JPEG encoding.
  + Add support for HEVC decoding and JPEG encoding in VA trace
    utility.
  + Fix out of tree builds.
  + VA/X11: fix BadDrawable issue when calling vaTerminate() after
    the pixmaps have been destroyed.
* Thu Oct 30 2014 sndirsch@suse.com
- added baselibs.conf as source to specfile in order to make factory
  happy
* Mon Oct 27 2014 sndirsch@suse.com
- update to version 1.4.1; most important features/changes since
  release 1.2.1:
  * API: add support for VP8 encoding
  * API: drop VAEntrypointMax enumeration
  * API: add STE filter to the VPP pipeline
  * API: add H.264 MVC profiles for decoding and encoding
  * API: add buffer export interfaces for interop with 3rdparty APIs (EGL, OCL)
  * API: add suppor for encoder quality level
  * API: add attribute usage hint flag
  * Enhancement for VA trace utility
  * Add support for DRM Render-Nodes (Andrey Larionov)
- removed obsolete patch libva-fix-rpmlint-error-no-return-in-non-void.patch
* Fri Sep 27 2013 dimstar@opensuse.org
- Introduce bcond_with wayland to easily control if the wayland
  support is to be built:
  + On openSUSE 13.1+ defaults to true
  + Create new subpackage vaapi-wayland-tools and libva-wayland1,
    containing the respective wayland support of libva.
  + BuilkdRequire pkgconfig(wayland-client).
  + Pass --enable/--disable-wayland to configure as appropriate.
* Wed Jul 10 2013 hrvoje.senjan@gmail.com
- updated to version 1.2.1:
  * fixed namespace issue with one of the new tools introduced as
    mpeg2enc. fdo#66221
  * API: new H.264 encoding API for Baseline, Main and High profiles
  * API: add support for MPEG-2 encoding
  * API: add video processing interfaces
  * API: add vaQuerySurfaceAttributes() to query surface attributes
    supported by the underlying drivers.
  * API: new version of vaCreateSurfaces(), the old version of
    vaCreateSurfaces() is still supported if including <va/va_compat.h>
  * API: add new surface attributes to enable VA surface creation
    from external buffer
  * API: add new RT formats and fourcc codes
  * Refine VA trace utility
  * Refine H.264 encoding test cases {avcenc, h264enc}
  * A new test case for MPEG-2 encoding
  * A lot of bug fixes
* Tue Mar 19 2013 kkhere.geo@gmail.com
- Version 1.1.1 - 18.Mar.2013
  This minor version brings the following changes:
  * Support wayland 1.0 protocol (Rob Bradford)
  * Automake 1.13 fixups (Armin K)
* Tue Nov 13 2012 guillaume@opensuse.org
- Remove Exclusive arch on x86*
* Thu Oct 18 2012 kkhere.geo@gmail.com
- fix rpmlint error no-return-in-nonvoid-function
* Thu Oct 18 2012 kkhere.geo@gmail.com
- packaging va backends seperately
* Thu Oct 18 2012 kkhere.geo@gmail.com
- previous bump to 1.1.0 was reverted upstream
- Version 1.1.0 - 04.Oct.2012
  * API: add Wayland support
  * API: add raw DRM support for headless pipelines
  * Fix generic VA/GLX implementation for newer cluttersink versions
  * Fix threading issues in VA objects reference code (+Krzysztof Kotlenga)
  * Fix build on Android Ice Cream Sandwich (+Haitao Huang, Daniel Charles)
* Tue May 29 2012 kkhere.geo@gmail.com
- get osc service localrun download_files to run
* Tue May 29 2012 tiwai@suse.de
- updated to version 1.1.0:
  * support of JPEG decoding
  * New hooks to create/free native pixmap
  * VA/EGL interfaces
  * Remove legacy DRI support
* Fri May 25 2012 kkhere.geo@gmail.com
- Remove nonexisting subpackage from baselibs.conf
* Wed May 23 2012 kkhere.geo@gmail.com
- Rename subpackage vaapi-drivers -> vaapi-dummy-driver
  since dummy is the only driver this package contains.
- Let the library recommend the dummy driver in case no other
  is present
* Tue May 22 2012 crrodriguez@opensuse.org
- Remove intel-driver, it has been packaged separately
  with proper hardware "Supplements" so it gets installed
  only when needed.
- Fix -devel package requires, otherwise dependant packages
  fail with missing headers wanted by files in /usr/include/va.
* Fri Apr 13 2012 kkhere.geo@gmail.com
- update intel driver to version 1.0.17
  Version 1.0.17 - 02.Apr.2012
  * Add support for IMC1/IMC3 surface formats
  * Fix rendering of interlaced surfaces
  * Fix MPEG-2 decoding of interlaced streams (SNB, IVB)
  * Fix H.264 weighted prediction indicator (SNB)
  * Fix and simplify calculation of H.264 macroblock bit offset (ILK, SNB, IVB)
  Version 1.0.16 - 14.Feb.2012
  * Fix VC-1 bitplane buffer size (SNB, IVB)
  * Fix VC-1 motion vector modes for Ivy Bridge
  * Fix MFX_QM_STATE for H.264 flat scaling lists (IVB)
  * Fix and simplify AVC_REF_IDX_STATE setup (ILK, SNB, IVB)
  * Fix memory leak of encoder buffers
  * Fix check for internal VA surface format prior to rendering
  * Add support for B43 chipset (Alexander Inyukhin)
* Wed Mar 21 2012 jengelh@medozas.de
- Remove redundant sections, compress filelist
- Enable parallel build
- Use pkgconfig symbols for deps
* Mon Feb 27 2012 dmueller@suse.de
- exclude from build on ARM
* Tue Feb 14 2012 sndirsch@suse.com
- Update package BuildRequires to use pkgconfig symbols
* Sat Nov 19 2011 coolo@suse.com
- add libtool as buildrequire to avoid implicit dependency
* Wed Nov  9 2011 kkhere.geo@gmail.com
- new version 1.0.15
  * API: make {Top,Bottom}FieldOrderCnt signed (Yi Wang)
  * Add auto-generated Debian packaging
  * Refine VA trace & VA fool utilities
  * Move i965 driver to a specific repository (vaapi/intel-driver)
  * Fix DSO link issue in tests
  * Fix fglrx driver name detection
  * Fix API vs. DSO vs. package versioning
- intel-driver has been split from the library, use separate tarball
- split the drivers into a separate package
* Tue Aug  9 2011 kkhere.geo@gmail.com
- new version 1.0.14
  no NEWS released; changelog in git https://cgit.freedesktop.org/libva/
* Tue May 31 2011 kkhere.geo@gmail.com
- new version 1.0.13
  * cleans up licensing issue
  * IvyBrigde video decoding support
  * thread safety
  * Encoding support in SandyBridge
* Fri Apr  1 2011 kkhere.geo@gmail.com
- new version 1.0.12
* Mon Mar 28 2011 kkhere.geo@gmail.com
- new version 1.0.11
  * obsoletes patch
  - i965_dri_video: don't try to render an invalid surface
* Thu Mar  3 2011 kkhere.geo@gmail.com
- patch: i965_dri_video: don't try to render an invalid surface
* Tue Feb 15 2011 kkhere.geo@gmail.com
- new version 1.0.10
* Mon Jan 10 2011 kkhere.geo@gmail.com
- new version 1.0.7
- support IA44 AI44 subpicture format in sandybridge
* Sun Dec 19 2010 lnussel@suse.de
- new version 1.0.6
* Fri Nov  5 2010 kkhere.geo@gmail.com
- update to version 1.0.6
* Thu Sep 30 2010 kkhere.geo@gmail.com
- update to version 1.0.5
  * add scaling flags for vaPutSurface()
  * i965_drv_video: add video processing kernels
  * i965_drv_video: deinterlacing & scaling
* Thu Sep  9 2010 kkhere.geo@gmail.com
- update to version 1.0.4
* Tue Jun  8 2010 dimstar@opensuse.org
- Split the library in libva1, the tools in vaapi-tools and the
  development in libva-devel. Both libraries can live in the same
  package as per policy: they are kept in sync with their soNUM.
* Mon Jun  7 2010 dominique-vlc.suse@leuenberger.net
- Initial package for VideoLAN repository, libva 1.0.1
