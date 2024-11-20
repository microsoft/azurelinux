Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# SPDX-License-Identifier: MIT

#
# spec file for package libvdpau
#
# Copyright (c) 2021 SUSE LLC
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

%if 0%{?suse_version} < 1550
  %define _distconfdir %{_prefix}%{_sysconfdir}
%endif
Name:           libvdpau
Version:        1.5
Release:        1%{?dist}
Summary:        VDPAU wrapper and trace libraries
License:        MIT
Group:          Development/Libraries/C and C++
URL:            https://www.freedesktop.org/wiki/Software/VDPAU/
Source0:        https://gitlab.freedesktop.org/vdpau/libvdpau/-/archive/%{version}/libvdpau-%{version}.tar.bz2

BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  graphviz
BuildRequires:  libtool
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  meson
BuildRequires:  xorg-x11-proto-devel

%description
VDPAU is the Video Decode and Presentation API for UNIX. It provides an
interface to video decode acceleration and presentation hardware present in
modern GPUs.

%package        trace
Summary:        Trace library for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} > 26 || 0%{?rhel} > 7
Supplements:    %{name}-debuginfo%{?_isa}
%endif

%description    trace
The %{name}-trace package contains trace library for %{name}.

%package        docs
Summary:        Documentation for %{name}
BuildArch:      noarch
Provides:       libvdpau-docs = %{version}-%{release}
Obsoletes:      libvdpau-docs < 0.6-2

%description    docs
The %{name}-docs package contains documentation for %{name}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
#Multilibs trace
Requires:       %{name}-trace%{?_isa} = %{version}-%{release}
Requires:       libX11-devel%{?_isa}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} -name '*.la' -delete
# Let %%doc macro create the correct location in the rpm file, creates a
# versioned docdir in <= f19 and an unversioned docdir in >= f20.
rm -fr %{buildroot}%{_docdir}
mv %{_vpath_builddir}/doc/html html

%ldconfig_scriptlets

%files
%doc AUTHORS
%license COPYING
%config(noreplace) %{_sysconfdir}/vdpau_wrapper.cfg
%{_libdir}/*.so.*
%dir %{_libdir}/vdpau/

%files trace
%{_libdir}/vdpau/%{name}_trace.so*

%files docs
%doc html

%files devel
%{_includedir}/vdpau/
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/vdpau.pc

%changelog
* Tue Nov 19 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 1.5-1
- Update Azure-Linux import from Fedora 41 (license: MIT).
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4-33
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Jan 14 2021 Dirk Müller <dmueller@suse.com>
- add c5a8e7c6c8b4b36a0e4c9a4369404519262a3256.patch
  e82dc4bdbb0db3ffa8c78275902738eb63aa5ca8.patch: upstream
  patches to include tracing info for VP9 and HEVC
* Fri Jul 31 2020 Stefan Dirsch <sndirsch@suse.com>
- n_UsrEtc.patch
  * switch to /usr/etc location for vdpau_wrapper.cfg, but first
    try /etc (boo#1173038)
* Sat Apr 11 2020 Stefan Dirsch <sndirsch@suse.com>
- Update libvdpau to version 1.4
  * adds 10,12-Bit decode support to VDPAU API
  * Adds HEVC Main 10/12 and HEVC Main 444 10/12 decode support in
    VDPAU API by Adding new profiles present in Range Extension
    profiles.Also Adds new VdpChromaTypes for 16bit.
- Updated vdpauinfo to version 1.3
  * Add names for the new 4:4:4 surface formats
  * Add support for VP9 in vdpauinfo
  * Depend on vdpau >= 1.3 for VP9 support
* Thu Aug 29 2019 Stefan Dirsch <sndirsch@suse.com>
- fixed source URL in specfile
* Thu Aug 29 2019 Stefan Dirsch <sndirsch@suse.com>
- Update libvdpau to version 1.3
  * This release of libvdpau switches the build system from
    automake & autoconf to meson and adds definitions to support
    decoding of the VP9 video format.
* Fri Mar  1 2019 Stefan Dirsch <sndirsch@suse.com>
- Update libvdpau to version 1.2
  * This version of libvdpau adds new chroma types defining whether
    surfaces contain frames or fields, and a new picture parameter
    structure that supports HEVC 4:4:4 pictures.
- supersedes U_Add_missing_include_of_config_h_to_define_GNU_SOURCE.patch
* Wed Dec 12 2018 Jan Engelhardt <jengelh@inai.de>
- Update RPM groups and %%make(_)install call.
* Wed Dec 12 2018 Dominique Leuenberger <dimstar@opensuse.org>
- Drop graphviz BuildRequires: we lose the doc with this, but
  manage to break a build cycle.
* Tue May 30 2017 sndirsch@suse.com
- includes everything needed for missing sle issue entries:
  * fate #315643-315645, 319159-319161, 319618 (bsc#1041623)
  * bnc#943967, bnc#943968, bnc#943969 (bsc#1041623)
  * CVE-2015-5198, CVE-2015-5199, CVE-2015-5200 (bsc#1041623)
* Mon Sep  7 2015 sndirsch@suse.com
- replaced u_src-mesa_dri2.c-define-_GNU_SOURCE.patch with upstream
  U_Add_missing_include_of_config_h_to_define_GNU_SOURCE.patch
* Wed Sep  2 2015 sndirsch@suse.com
- added missing BuildRequires for pkgconfig(dri2proto)
- u_src-mesa_dri2.c-define-_GNU_SOURCE.patch
  * Without having defined _GNU_SOURCE __USE_GNU isn't defined
    either. Though secure_getenv() in stdlib.h isn't declared.
* Tue Sep  1 2015 sndirsch@suse.com
- Update libvdpau to version 1.1.1 (bnc#943967,#943968,#943969)
  libvdpau versions 1.1 and earlier, when used in setuid or setgid
  applications, contain vulnerabilities related to environment
  variable handling that could allow an attacker to execute
  arbitrary code or overwrite arbitrary files.  See CVE-2015-5198,
  CVE-2015-5199, and CVE-2015-5200 for more details.
  This release uses the secure_getenv() function, when available,
  to fix these problems. The updated libvdpau will instead use a
  fallback implementation of secure_getenv() when the platform
  doesn't provide one.
  If you use the NVIDIA .run installer packages, please see
  https://devtalk.nvidia.com/default/topic/873035 for additional
  information.
  This release also adds tracing of HEVC picture structures to
  libvdpau_trace.
- supersedes patch: libvdpau-nopdftex.patch
* Tue Mar 17 2015 sndirsch@suse.com
- Update libvdpau to version 1.1
  * This release fixes a bug in the new VdpPictureInfoHEVC structure:
    the column_width_minus1 and row_height_minus1 arrays had the wrong
    dimensions. To avoid the incorrect structure being used, the profile
    numbers for the HEVC profiles have been changed. Please use the new
    profiles rather than the ones from libvdpau 1.0.
* Mon Mar 16 2015 sndirsch@suse.com
- Update libvdpau to version 1.0
  * This release adds support for the following HEVC / H.265 profiles:
    VDP_DECODER_PROFILE_HEVC_MAIN
    VDP_DECODER_PROFILE_HEVC_MAIN_10
    VDP_DECODER_PROFILE_HEVC_MAIN_STILL
    VDP_DECODER_PROFILE_HEVC_MAIN_12
    VDP_DECODER_PROFILE_HEVC_MAIN_444
- Updated vdpauinfo to version 0.9
  * This release adds support for querying the new profiles added in
    libvdpau 1.0 (see above)
- cleanup: removed empty patch 'vdpauinfo-missing-lX11.diff'
* Tue Dec 23 2014 jweberhofer@weberhofer.at
- Update libvpaud to version 0.9
  This release adds several new decoder profiles:
  - VDP_DECODER_PROFILE_H264_CONSTRAINED_BASELINE
  - VDP_DECODER_PROFILE_H264_EXTENDED
  - VDP_DECODER_PROFILE_H264_PROGRESSIVE_HIGH
  - VDP_DECODER_PROFILE_H264_CONSTRAINED_HIGH
  - VDP_DECODER_PROFILE_H264_HIGH_444_PREDICTIVE
  In addition, this release includes a number of packaging and compiler warning
  fixes and clarifies the ABI policy to include the size of the data structures
  defined in vdpau.h.  It also fixes a race condition that could be triggered
  when two threads call VdpDeviceCreateX11 simultaneously.
  * vdpau_x11.h: update stale comment about how libvdpau finds drivers
  * vdpau.h: define a more strict ABI policy
  * trace: properly annotate private functions as static
  * vdpau: do not export _vdp_DRI2* functions
  * Clarify type of source_surface as VDP_INVALID_HANDLE
  * vdpau_x11 - fix typo
  * Add support for H.264 Hi444PP in VDPAU API
  * vdpau_trace: Fix GCC 4.8 build warnings
  * vdpau_wrapper: remove unused parameter warnings
  * test: do not clobber CFLAGS
  * test: remove assignment-as-truth-value warning
  * test: fix incomplete prototype
  * vdpau.h: improve constant expansion safety
  * vdpau: define some more H.264/AVC decoding profiles
  * configure: add test for POSIX threads
  * vdpau_wrapper: make the fixes initialization thread-safe
  * vdpau_wrapper: make initialization of library handles thread-safe
  * vdpau_wrapper: protect concurrent access to _imp_get_proc_address
- Updated vdpauinfo to version 0.9
  This release adds support for the new profiles added in libvdpau 0.9.  It
  also adds the ability to display which indexed color formats are supported by
  the PutBits interface.
  Finally, it adds the command line options --display and --screen, which can
  be used to select which X server and screen to query rather than having to
  set the $DISPLAY environment variable.
  * Set the AM_INIT_AUTOMAKE foreign flag
  * vdpauinfo: add option processing
  * vdpauinfo: print supported PutBits indexed color formats
  * Support new H.264 profiles added in libvdpau 0.9
  * List profiles that are not supported as well
- rebased patches
* Wed Jul  2 2014 sndirsch@suse.com
- Update to v0.8
  * This release fixes an incorrect type for VdpPictureInfo and
    adds an environment variable, VDPAU_DRIVER_PATH, which can be
    used to override the default search path that the library uses
    to find its backend driver libraries.
* Sun Oct 27 2013 sndirsch@suse.com
- update to vdpauinfo 0.1
  * This release fixes a problem where ranges were queried for
    mixer parameters and attributes where ranges were not allowed.
* Mon Mar 25 2013 idonmez@suse.com
- Drop libvdpau-alway-workaround-libflash.patch: while this
  fixes flash plugin, it breaks all the other apps. (bnc#811360)
* Sun Feb  3 2013 hrvoje.senjan@gmail.com
- Update to v0.6
  * Make use of dri2proto_CFLAGS when building.
  * Fix leaked extension info on library unload
  * Use AC_CONFIG_HEADERS instead of AM_CONFIG_HEADER to appease
    automake 1.13
* Wed Sep  5 2012 idonmez@suse.com
- Update to v0.5
  * vdpau_wrapper.c: Track dynamic library handles and free them
    on exit
  * Implement workarounds for Adobe Flash bugs
- Add libvdpau-alway-workaround-libflash.patch: always enable
  Flash workarounds and not depend on kernel command line. Users
  can disable this in the /etc/vdpau_wrapper.cfg file.
* Tue Jun 26 2012 sndirsch@suse.com
- back to building the HTML documentation (instead of prebuilding
  and then extracting it during the build), but this time without
  requiring texlive, since pdftex apparently isn't used for this
  purpose anyway (libvdpau-nopdftex.patch)
* Mon Jun 25 2012 coolo@suse.com
- do not build the documentation but package a prebuilt tar of it
  to avoid huge build cycle
* Mon Aug 29 2011 sndirsch@suse.com
- fixes the build in a more correct way :-) Hopefully!
* Mon Aug 29 2011 sndirsch@suse.com
- vdpau needs an explicit "-lX11" with latest toolchain
* Wed Sep 22 2010 coolo@novell.com
- fix baselibs.conf
* Wed Sep  8 2010 sndirsch@novell.com
- libvdpau 0.4.1
  This minor update just changes a few small, but important,
  documentation details.
  * vdpau.h: Clarify video mixer field amount recommendation
  * vpdau.h: Fix typo and clarify wording.
  * More doc issues pointed out by Xine authors.
* Fri Jun 18 2010 sndirsch@suse.de
- renamed rpmlintrc to libvdpau-rpmlintrc
- added libvdpau-rpmlintrc as source to specfile
* Fri Jun  4 2010 sndirsch@suse.de
- fixed baselibs.conf (packages have been renamed)
* Sat Apr 24 2010 sndirsch@suse.de
- fixed libvdpau_trace1 package description
- added README for tracing VDPAU function calls
* Sat Apr 24 2010 sndirsch@suse.de
- added Wladimir J. van der Laan's vdpinfo tool, a command line
  utility for querying the capabilities of a VDPAU device.
* Thu Apr 22 2010 herbert@graeber-clan.de
- put libvdpau_trace into it's own package
* Thu Apr 22 2010 herbert@graeber-clan.de
- follow Shared Library Packaging Policy
- obsolete packman vdpau packages for proper update
* Thu Apr 22 2010 sndirsch@suse.de
- also build and package documentation
* Wed Apr 21 2010 sndirsch@suse.de
- created package (bnc #596481)
