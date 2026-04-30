## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit f1c79c02822848a9bed4315b12c8c8f3761e1296
%global snapdate 20251025

# We choose not to package the “stb_include” library (stb_include.h) because,
# during the package review, it was observed that it follows coding practices
# that make it dangerous to use on untrusted inputs, including but not limited
# to:
#
# - It uses of strcat/strcpy into a fixed-length buffer that is assumed (but
#   not proven) to be large enough for all possible uses
# - It ignores I/O errors (possibly leading to undefined behavior from reading
#   uninitialized memory), and so on.
#
# A substantial rewrite would be required to mitigate these concerns. If a
# request for this library arises, this decision may be revisited, or the
# necessary rewrite may be done and offered upstream. For now, we omit the
# library and expect it will not be missed.
%bcond stb_include 0

Name:           stb
# While the individual header-only libraries are versioned, the overall
# collection is not, and there are no releases. See:
#   https://github.com/nothings/stb/issues/359
#   https://github.com/nothings/stb/issues/1101
%global snapinfo ^%{snapdate}git%{sub %{commit} 1 7}
Version:        0%{snapinfo}
Release:        %autorelease
Summary:        Single-file public domain libraries for C/C++

# See LICENSE.
License:        MIT OR Unlicense
# Additionally, the following are under different terms, but are not used; to
# make certain, they are removed in %%prep.
#
# - deprecated/rrsprintf.h, tests/caveview/stb_gl.h, and
#   tests/caveview/win32/SDL_windows_main.c are
#   LicenseRef-Fedora-Public-Domain:
#   https://gitlab.com/fedora/legal/fedora-license-data/-/issues/620
# - tests/caveview/glext.h is MIT (only)
SourceLicense:  (%{license}) AND LicenseRef-Fedora-Public-Domain AND MIT
URL:            https://github.com/nothings/stb
Source:         %{url}/archive/%{commit}/stb-%{commit}.tar.gz

# Fix undefined behavior from array “shape-punning”
# https://github.com/nothings/stb/pull/1194
Patch:          %{url}/pull/1194.patch

# Fix misleading indentation in stb_divide.h
# https://github.com/nothings/stb/pull/1195
Patch:          %{url}/pull/1195.patch

# Trivial fix for array-in-structure initialization (missing braces warning)
# https://github.com/nothings/stb/pull/1196
Patch:          %{url}/pull/1196.patch

# Fix signature of dummy realloc() for STB_VORBIS_NO_CRT
# https://github.com/nothings/stb/pull/1198
Patch:          %{url}/pull/1198.patch

# Forward declare stbhw__process struct to fix warnings
# https://github.com/nothings/stb/pull/1236
#
# We don’t see these warnings in the “compile tests”, but we can reproduce them
# by manually compiling tests/herringbone_map.c; a real user of the
# stb_herringbone_wang_tile library would encounter them; and inspection of the
# patch shows it to be correct.
Patch:          %{url}/pull/1236.patch

# Fixes null pointer dereference in https://github.com/nothings/stb/issues/1452
# https://github.com/nothings/stb/pull/1454
#
# Fixes:
#
# NULL pointer dereference in the stb_image.h
# https://github.com/nothings/stb/issues/1452
# NULL pointer derefence in PIC loading (CVE-2023-43898)
# https://github.com/nothings/stb/issues/1521
# Null pointer dereference in stbi__convert_format (GHSL-2023-149)
# https://github.com/nothings/stb/issues/1546
#
# An alternative and equivalent patch is:
#
# Fix Null pointer dereference in stbi__convert_format
# https://github.com/nothings/stb/pull/1547
Patch:          %{url}/pull/1454.patch

# Fix integer overflow
# https://github.com/nothings/stb/pull/1530
#
# Fixes:
#
# Integer overflow in stbi__convert_8_to_16
# https://github.com/nothings/stb/issues/1529
Patch:          %{url}/pull/1530.patch

# Add overflow checks
# https://github.com/nothings/stb/pull/1532
#
# Fixes:
#
# Integer overflow in stbi__load_gif_main
# https://github.com/nothings/stb/issues/1531
Patch:          %{url}/pull/1532.patch

# Fix int overflow
# https://github.com/nothings/stb/pull/1534
#
# Fixes:
#
# Integer overflow in stbi__jpeg_decode_block
# https://github.com/nothings/stb/pull/1533
Patch:          %{url}/pull/1534.patch

# Fix wild address read in stbi__gif_load_next
# https://github.com/nothings/stb/pull/1539
#
# Fixes:
#
# Wild address read in stbi__gif_load_next (GHSL-2023-145/CVE-2023-45661)
# https://github.com/nothings/stb/issues/1538
Patch:          %{url}/pull/1539.patch

# Fix multi-byte read heap buffer overflow in stbi__vertical_flip
# https://github.com/nothings/stb/pull/1541
#
# Fixes:
#
# Multi-byte read heap buffer overflow in stbi__vertical_flip
# (GHSL-2023-146/CVE-2023-45662)
# https://github.com/nothings/stb/issues/1540
Patch:          %{url}/pull/1541.patch

# Fix disclosure of uninitialized memory in stbi__tga_load
# https://github.com/nothings/stb/pull/1543
#
# Fixes:
#
# Disclosure of uninitialized memory in stbi__tga_load
# (GHSL-2023-147/CVE-2023-45663)
# https://github.com/nothings/stb/issues/1542
Patch:          %{url}/pull/1543.patch

# Fix double-free in stbi__load_gif_main_outofmem
# https://github.com/nothings/stb/pull/1545
#
# Fixes:
#
# Double-free in stbi__load_gif_main_outofmem (GHSL-2023-148/CVE-2023-45664)
# https://github.com/nothings/stb/issues/1544
#
# Rebased on top of https://github.com/nothings/stb/pull/1539.
Patch:          0001-Fix-double-free-in-stbi__load_gif_main_outofmem.patch

# Fix possible double-free or memory leak in stbi__load_gif_main
# https://github.com/nothings/stb/pull/1549
#
# Fixes:
#
# Possible double-free or memory leak in stbi__load_gif_main
# (GHSL-2023-150/CVE-2023-45666)
# https://github.com/nothings/stb/issues/1548
#
# Rebased on top of https://github.com/nothings/stb/pull/1539 and
# https://github.com/nothings/stb/pull/1545.
Patch:          0002-Fix-possible-double-free-or-memory-leak-in-stbi__loa.patch

# Fix Null pointer dereference because of an uninitialized variable
# https://github.com/nothings/stb/pull/1551
#
# Fixes:
#
# Null pointer dereference because of an uninitialized variable
# (GHSL-2023-151/CVE-2023-45667)
# https://github.com/nothings/stb/issues/1550
#
# Rebased on top of https://github.com/nothings/stb/pull/1541.
Patch:          0001-Fix-Null-pointer-dereference-because-of-an-uninitial.patch

# Fix 0 byte write heap buffer overflow in start_decoder
# https://github.com/nothings/stb/pull/1553
#
# Fixes:
#
# 0 byte write heap buffer overflow in start_decoder
# (GHSL-2023-165/CVE-2023-45675)
# https://github.com/nothings/stb/issues/1552
Patch:          %{url}/pull/1553.patch

# riscv64 compile fix
# https://github.com/nothings/stb/pull/1610
Patch: fix-riscv64-compile-uintptr.patch

# Out of bounds heap buffer write (GHSL-2023-171/CVE-2023-45681)
# https://github.com/nothings/stb/pull/1559
# Fixes CVE-2023-45681 and duplicate CVE-2023-47212
# https://bugzilla.redhat.com/show_bug.cgi?id=2278402
Patch:          %{url}/pull/1559.patch

# Fix root-cause of CVE-2021-45340 : dereference of NULL ptr.
# https://github.com/nothings/stb/pull/1736
Patch:          %{url}/pull/1736.patch

# Add fix for https://github.com/nothings/stb/issues/1860 by checking malloc
# multiplication before allocating
# https://github.com/nothings/stb/pull/1862
#
# Fixes:
#
# Heap Buffer overflow in stbi__convert_format16
# https://github.com/nothings/stb/issues/1860
#
# Re-crated on top of all of the above patches.
Patch:          pr-1862.patch

#  Fixes issue #1861 by zero-initializing palette.
# https://github.com/nothings/stb/pull/1863
#
# Fixes:
#
# Out-of-bounds read in PNG palette expansion
# https://github.com/nothings/stb/issues/1861
Patch:          %{url}/pull/1863.patch

%global stb_c_lexer_version 0.12
%global stb_connected_components_version 0.96
%global stb_divide_version 0.94
%global stb_ds_version 0.67
%global stb_dxt_version 1.12
%global stb_easy_font_version 1.1
%global stb_herringbone_wang_tile_version 0.7
%global stb_hexwave_version 0.5
%global stb_image_version 2.30
%global stb_image_resize_version 0.97
%global stb_image_resize2_version 2.17
%global stb_image_write_version 1.16
%global stb_include_version 0.2
%global stb_leakcheck_version 0.6
%global stb_perlin_version 0.5
%global stb_rect_pack_version 1.1
%global stb_sprintf_version 1.10
%global stb_textedit_version 1.14
%global stb_tilemap_editor_version 0.42
%global stb_truetype_version 1.26
%global stb_vorbis_version 1.22
%global stb_voxel_render_version 0.89

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

BuildRequires:  /usr/bin/convert

# No compiled binaries are installed, so this would be empty.
%global debug_package %{nil}

%description
%{summary}.


%package devel
Summary:        Development files for stb

# Dependent packages should prefer to BuildRequire the -static packages for the
# specific stb libraries they use.
Provides:       stb-static = %{version}-%{release}

Requires:       stb_c_lexer-devel%{?_isa} = %{stb_c_lexer_version}%{snapinfo}-%{release}
Requires:       stb_c_lexer-static = %{stb_c_lexer_version}%{snapinfo}-%{release}
Requires:       stb_connected_components-devel%{?_isa} = %{stb_connected_components_version}%{snapinfo}-%{release}
Requires:       stb_connected_components-static = %{stb_connected_components_version}%{snapinfo}-%{release}
Requires:       stb_divide-devel%{?_isa} = %{stb_divide_version}%{snapinfo}-%{release}
Requires:       stb_divide-static = %{stb_divide_version}%{snapinfo}-%{release}
Requires:       stb_ds-devel%{?_isa} = %{stb_ds_version}%{snapinfo}-%{release}
Requires:       stb_ds-static = %{stb_ds_version}%{snapinfo}-%{release}
Requires:       stb_dxt-devel%{?_isa} = %{stb_dxt_version}%{snapinfo}-%{release}
Requires:       stb_dxt-static = %{stb_dxt_version}%{snapinfo}-%{release}
Requires:       stb_easy_font-devel%{?_isa} = %{stb_easy_font_version}%{snapinfo}-%{release}
Requires:       stb_easy_font-static = %{stb_easy_font_version}%{snapinfo}-%{release}
Requires:       stb_herringbone_wang_tile-devel%{?_isa} = %{stb_herringbone_wang_tile_version}%{snapinfo}-%{release}
Requires:       stb_herringbone_wang_tile-static = %{stb_herringbone_wang_tile_version}%{snapinfo}-%{release}
Requires:       stb_hexwave-devel%{?_isa} = %{stb_hexwave_version}%{snapinfo}-%{release}
Requires:       stb_hexwave-static = %{stb_hexwave_version}%{snapinfo}-%{release}
Requires:       stb_image-devel%{?_isa} = %{stb_image_version}%{snapinfo}-%{release}
Requires:       stb_image-static = %{stb_image_version}%{snapinfo}-%{release}
# For compatibility, we still depend on the subpackages for the original,
# deprecated-upstream stb_image_library in existing stable releases, but we
# drop the dependendency going forward as an acknowledgement of its status.
%if 0%{?el9} || 0%{?el8}
Requires:       stb_image_resize-devel%{?_isa} = %{stb_image_resize_version}%{snapinfo}-%{release}
Requires:       stb_image_resize-static = %{stb_image_resize_version}%{snapinfo}-%{release}
%endif
Requires:       stb_image_resize2-devel%{?_isa} = %{stb_image_resize2_version}%{snapinfo}-%{release}
Requires:       stb_image_resize2-static = %{stb_image_resize2_version}%{snapinfo}-%{release}
Requires:       stb_image_write-devel%{?_isa} = %{stb_image_write_version}%{snapinfo}-%{release}
Requires:       stb_image_write-static = %{stb_image_write_version}%{snapinfo}-%{release}
%if %{with stb_include}
Requires:       stb_include-devel%{?_isa} = %{stb_include_version}%{snapinfo}-%{release}
Requires:       stb_include-static = %{stb_include_version}%{snapinfo}-%{release}
%endif
Requires:       stb_leakcheck-devel%{?_isa} = %{stb_leakcheck_version}%{snapinfo}-%{release}
Requires:       stb_leakcheck-static = %{stb_leakcheck_version}%{snapinfo}-%{release}
Requires:       stb_perlin-devel%{?_isa} = %{stb_perlin_version}%{snapinfo}-%{release}
Requires:       stb_perlin-static = %{stb_perlin_version}%{snapinfo}-%{release}
Requires:       stb_rect_pack-devel%{?_isa} = %{stb_rect_pack_version}%{snapinfo}-%{release}
Requires:       stb_rect_pack-static = %{stb_rect_pack_version}%{snapinfo}-%{release}
Requires:       stb_sprintf-devel%{?_isa} = %{stb_sprintf_version}%{snapinfo}-%{release}
Requires:       stb_sprintf-static = %{stb_sprintf_version}%{snapinfo}-%{release}
Requires:       stb_textedit-devel%{?_isa} = %{stb_textedit_version}%{snapinfo}-%{release}
Requires:       stb_textedit-static = %{stb_textedit_version}%{snapinfo}-%{release}
Requires:       stb_tilemap_editor-devel%{?_isa} = %{stb_tilemap_editor_version}%{snapinfo}-%{release}
Requires:       stb_tilemap_editor-static = %{stb_tilemap_editor_version}%{snapinfo}-%{release}
Requires:       stb_truetype-devel%{?_isa} = %{stb_truetype_version}%{snapinfo}-%{release}
Requires:       stb_truetype-static = %{stb_truetype_version}%{snapinfo}-%{release}
Requires:       stb_vorbis-devel%{?_isa} = %{stb_vorbis_version}%{snapinfo}-%{release}
Requires:       stb_vorbis-static = %{stb_vorbis_version}%{snapinfo}-%{release}
Requires:       stb_voxel_render-devel%{?_isa} = %{stb_voxel_render_version}%{snapinfo}-%{release}
Requires:       stb_voxel_render-static = %{stb_voxel_render_version}%{snapinfo}-%{release}

%description devel
The stb-devel package contains libraries and header files for developing
applications that use stb.

This is a metapackage that requires the -devel packages for all stb libraries.


%package -n stb_c_lexer-devel
Summary:        Simplify writing parsers for C-like languages
Version:        %{stb_c_lexer_version}%{snapinfo}

Provides:       stb_c_lexer-static = %{stb_c_lexer_version}%{snapinfo}-%{release}

%description -n stb_c_lexer-devel
Lexer for making little C-like languages with recursive-descent parsers.


%package -n stb_connected_components-devel
Summary:        Incrementally compute reachability on grids
Version:        %{stb_connected_components_version}%{snapinfo}

Provides:       stb_connected_components-static = %{stb_connected_components_version}%{snapinfo}-%{release}

%description -n stb_connected_components-devel
Finds connected components on 2D grids for testing reachability between two
points, with fast updates when changing reachability (e.g. on one machine it
was typically 0.2ms w/ 1024x1024 grid). Each grid square must be “open” or
“closed” (traversable or untraversable), and grid squares are only connected to
their orthogonal neighbors, not diagonally.


%package -n stb_divide-devel
Summary:        More useful 32-bit modulus e.g. “Euclidean divide”
Version:        %{stb_divide_version}%{snapinfo}

Provides:       stb_divide-static = %{stb_divide_version}%{snapinfo}-%{release}

%description -n stb_divide-devel
This file provides three different consistent divide/mod pairs
implemented on top of arbitrary C/C++ division, including correct
handling of overflow of intermediate calculations:

    trunc:   a/b truncates to 0,           a%b has same sign as a
    floor:   a/b truncates to -inf,        a%b has same sign as b
    eucl:    a/b truncates to sign(b)*inf, a%b is non-negative


%package -n stb_ds-devel
Summary:        Typesafe dynamic array and hash tables for C, will compile in C++
Version:        %{stb_ds_version}%{snapinfo}

Provides:       stb_ds-static = %{stb_ds_version}%{snapinfo}-%{release}

%description -n stb_ds-devel
This is a single-header-file library that provides easy-to-use dynamic arrays
and hash tables for C (also works in C++).

For a gentle introduction: https://nothings.org/stb_ds


%package -n stb_dxt-devel
Summary:        Fabian “ryg” Giesen’s real-time DXT compressor
Version:        %{stb_dxt_version}%{snapinfo}

Provides:       stb_dxt-static = %{stb_dxt_version}%{snapinfo}-%{release}

%description -n stb_dxt-devel
DXT1/DXT5 compressor.


%package -n stb_easy_font-devel
Summary:        Quick-and-dirty easy-to-deploy bitmap font for printing frame rate, etc
Version:        %{stb_easy_font_version}%{snapinfo}

Provides:       stb_easy_font-static = %{stb_easy_font_version}%{snapinfo}-%{release}

%description -n stb_easy_font-devel
   Easy-to-deploy,
   reasonably compact,
   extremely inefficient performance-wise,
   crappy-looking,
   ASCII-only,
   bitmap font for use in 3D APIs.

Intended for when you just want to get some text displaying in a 3D app as
quickly as possible.

Doesn’t use any textures, instead builds characters out of quads.


%package -n stb_herringbone_wang_tile-devel
Summary:        Herringbone Wang tile map generator
Version:        %{stb_herringbone_wang_tile_version}%{snapinfo}

Provides:       stb_herringbone_wang_tile-static = %{stb_herringbone_wang_tile_version}%{snapinfo}-%{release}

%description -n stb_herringbone_wang_tile-devel
This library is an SDK for Herringbone Wang Tile generation:

     http://nothings.org/gamedev/herringbone

The core design is that you use this library offline to generate a “template”
of the tiles you’ll create. You then edit those tiles, then load the created
tile image file back into this library and use it at runtime to generate
“maps”.

You cannot load arbitrary tile image files with this library; it is only
designed to load image files made from the template it created. It stores a
binary description of the tile sizes & constraints in a few pixels, and uses
those to recover the rules, rather than trying to parse the tiles themselves.

You *can* use this library to generate from arbitrary tile sets, but only by
loading the tile set and specifying the constraints explicitly yourself.


%package -n stb_hexwave-devel
Summary:        Audio waveform synthesizer
Version:        %{stb_hexwave_version}%{snapinfo}

Provides:       stb_hexwave-static = %{stb_hexwave_version}%{snapinfo}-%{release}

%description -n stb_hexwave-devel
A flexible anti-aliased (bandlimited) digital audio oscillator.

This library generates waveforms of a variety of shapes made of line segments.
It does not do envelopes, LFO effects, etc.; it merely tries to solve the
problem of generating an artifact-free morphable digital waveform with a
variety of spectra, and leaves it to the user to rescale the waveform and mix
multiple voices, etc.


%package -n stb_image-devel
Summary:        Image loading/decoding from file/memory: JPG, PNG, TGA, BMP, PSD, GIF, HDR, PIC
Version:        %{stb_image_version}%{snapinfo}

Provides:       stb_image-static = %{stb_image_version}%{snapinfo}-%{release}

%description -n stb_image-devel
%{summary}.

Primarily of interest to game developers and other people who can avoid
problematic images and only need the trivial interface.


# We still package (and have chosen not to deprecate) the original
# stb_image_resize even though upstream has deprecated it. We do not want to
# drive dependent packages back to bundling.
%package -n stb_image_resize-devel
Summary:        Resize images larger/smaller with good quality (original version)
Version:        %{stb_image_resize_version}%{snapinfo}

Provides:       stb_image_resize-static = %{stb_image_resize_version}%{snapinfo}-%{release}

%description -n stb_image_resize-devel
Image resizing.

Written with emphasis on usability, portability, and efficiency. (No SIMD or
threads, so it be easily outperformed by libs that use those.) Only scaling and
translation is supported, no rotations or shears. Easy API downsamples
w/Mitchell filter, upsamples w/cubic interpolation.

This is the original version of the stb_image_resize library. It has been
deprecated by its developer; consider porting to stb_image_resize2 instead.


%package -n stb_image_resize2-devel
Summary:        Resize images larger/smaller with good quality
Version:        %{stb_image_resize2_version}%{snapinfo}

Provides:       stb_image_resize2-static = %{stb_image_resize2_version}%{snapinfo}-%{release}

%description -n stb_image_resize2-devel
Image resizing.


%package -n stb_image_write-devel
Summary:        Image writing to disk: PNG, TGA, BMP
Version:        %{stb_image_write_version}%{snapinfo}

Provides:       stb_image_write-static = %{stb_image_write_version}%{snapinfo}-%{release}

%description -n stb_image_write-devel
This header file is a library for writing images to C stdio or a callback.

The PNG output is not optimal; it is 20-50%% larger than the file written by a
decent optimizing implementation; though providing a custom zlib compress
function (see STBIW_ZLIB_COMPRESS) can mitigate that. This library is designed
for source code compactness and simplicity, not optimal image file size or
run-time performance.


%if %{with stb_include}
%package -n stb_include-devel
Summary:        Implement recursive #include support, particularly for GLSL
Version:        %{stb_include_version}%{snapinfo}

Provides:       stb_include-static = %{stb_include_version}%{snapinfo}-%{release}

%description -n stb_include-devel
This program parses a string and replaces lines of the form
        #include "foo"
with the contents of a file named "foo". It also embeds the appropriate #line
directives. Note that all include files must reside in the location specified
in the path passed to the API; it does not check multiple directories.

If the string contains a line of the form
        #inject
then it will be replaced with the contents of the string ‘inject’ passed to the
API.
%endif


%package -n stb_leakcheck-devel
Summary:        Quick-and-dirty malloc/free leak-checking
Version:        %{stb_leakcheck_version}%{snapinfo}

Provides:       stb_leakcheck-static = %{stb_leakcheck_version}%{snapinfo}-%{release}

%description -n stb_leakcheck-devel
%{summary}.


%package -n stb_perlin-devel
Summary:        Perlin’s revised simplex noise w/ different seeds
Version:        %{stb_perlin_version}%{snapinfo}

Provides:       stb_perlin-static = %{stb_perlin_version}%{snapinfo}-%{release}

%description -n stb_perlin-devel
%{summary}.


%package -n stb_rect_pack-devel
Summary:        Simple 2D rectangle packer with decent quality
Version:        %{stb_rect_pack_version}%{snapinfo}

Provides:       stb_rect_pack-static = %{stb_rect_pack_version}%{snapinfo}-%{release}

%description -n stb_rect_pack-devel
Useful for e.g. packing rectangular textures into an atlas. Does not do
rotation.

Not necessarily the awesomest packing method, but better than the totally naive
one in stb_truetype (which is primarily what this is meant to replace).

No memory allocations; uses qsort() and assert() from stdlib. Can override
those by defining STBRP_SORT and STBRP_ASSERT.

This library currently uses the Skyline Bottom-Left algorithm.

Please note: better rectangle packers are welcome! Please implement them to the
same API, but with a different init function.


%package -n stb_sprintf-devel
Summary:        Fast sprintf, snprintf for C/C++
Version:        %{stb_sprintf_version}%{snapinfo}

Provides:       stb_sprintf-static = %{stb_sprintf_version}%{snapinfo}-%{release}

%description -n stb_sprintf-devel
This is a full sprintf replacement that supports everything that the C runtime
sprintfs support, including float/double, 64-bit integers, hex floats, field
parameters (%%*.*d stuff), length reads backs, etc.

Why would you need this if sprintf already exists? Well, first off, it’s *much*
faster (see below). It’s also much smaller than the CRT versions
code-space-wise. We’ve also added some simple improvements that are super handy
(commas in thousands, callbacks at buffer full, for example). Finally, the
format strings for MSVC and GCC differ for 64-bit integers (among other small
things), so this lets you use the same format strings in cross platform code.

It uses the standard single file trick of being both the header file and the
source itself. If you just include it normally, you just get the header file
function definitions. To get the code, you include it from a C or C++ file and
define STB_SPRINTF_IMPLEMENTATION first.

It only uses va_args macros from the C runtime to do its work. It does cast
doubles to S64s and shifts and divides U64s, which does drag in CRT code on
most platforms.

It compiles to roughly 8K with float support, and 4K without. As a comparison,
when using MSVC static libs, calling sprintf drags in 16K.


%package -n stb_textedit-devel
Summary:        Guts of a text editor for games etc., implementing them from scratch
Version:        %{stb_textedit_version}%{snapinfo}

Provides:       stb_textedit-static = %{stb_textedit_version}%{snapinfo}-%{release}

%description -n stb_textedit-devel
This C header file implements the guts of a multi-line text-editing widget; you
implement display, word-wrapping, and low-level string insertion/deletion, and
stb_textedit will map user inputs into insertions & deletions, plus updates to
the cursor position, selection state, and undo state.

It is intended for use in games and other systems that need to build their own
custom widgets and which do not have heavy text-editing requirements (this
library is not recommended for use for editing large texts, as its performance
does not scale and it has limited undo).

Non-trivial behaviors are modeled after Windows text controls.


%package -n stb_tilemap_editor-devel
Summary:        Embeddable tilemap editor
Version:        %{stb_tilemap_editor_version}%{snapinfo}

Provides:       stb_tilemap_editor-static = %{stb_tilemap_editor_version}%{snapinfo}-%{release}

%description -n stb_tilemap_editor-devel
Embeddable tilemap editor for C/C++.


%package -n stb_truetype-devel
Summary:        Parse, decode, and rasterize characters from TrueType fonts
Version:        %{stb_truetype_version}%{snapinfo}

Provides:       stb_truetype-static = %{stb_truetype_version}%{snapinfo}-%{release}

%description -n stb_truetype-devel
%{summary}.
=======================================================================

   NO SECURITY GUARANTEE -- DO NOT USE THIS ON UNTRUSTED FONT FILES

This library does no range checking of the offsets found in the file,
meaning an attacker can use it to read arbitrary memory.

=======================================================================

This library processes TrueType files:
  • parse files
  • extract glyph metrics
  • extract glyph shapes
  • render glyphs to one-channel bitmaps with antialiasing (box filter)
  • render glyphs to one-channel SDF bitmaps (signed-distance field/function)


%package -n stb_vorbis-devel
Summary:        Decode Ogg Vorbis files from file/memory to float/16-bit signed output
Version:        %{stb_vorbis_version}%{snapinfo}

Provides:       stb_vorbis-static = %{stb_vorbis_version}%{snapinfo}-%{release}

%description -n stb_vorbis-devel
Ogg Vorbis audio decoder.


%package -n stb_voxel_render-devel
Summary:        Helps render large-scale “voxel” worlds for games
Version:        %{stb_voxel_render_version}%{snapinfo}

Provides:       stb_voxel_render-static = %{stb_voxel_render_version}%{snapinfo}-%{release}

%description -n stb_voxel_render-devel
This library helps render large-scale “voxel” worlds for games, in this case,
one with blocks that can have textures and that can also be a few shapes other
than cubes.

   Video introduction:
      http://www.youtube.com/watch?v=2vnTtiLrV1w

   Minecraft-viewer sample app (not very simple though):
      http://github.com/nothings/stb/tree/master/tests/caveview

It works by creating triangle meshes. The library includes

   - converter from dense 3D arrays of block info to vertex mesh
   - vertex & fragment shaders for the vertex mesh
   - assistance in setting up shader state

For portability, none of the library code actually accesses the 3D graphics
API. (At the moment, it’s not actually portable since the shaders are GLSL
only, but patches are welcome.)

You have to do all the caching and tracking of vertex buffers yourself.
However, you could also try making a game with a small enough world that it’s
fully loaded rather than streaming. Currently the preferred vertex format is 20
bytes per quad. There are designs to allow much more compact formats with a
slight reduction in shader features, but no roadmap for actually implementing
them.


%package doc
Summary:        Documentation for stb
BuildArch:      noarch

%description doc
Documentation for stb.


%prep
%autosetup -n stb-%{commit} -p1

# Append to OS build flags rather than overriding them
#
# Instead of hard-coding C++ standard and calling the C compiler, defer to the
# default and call the C++ compiler.
#
# When upstream says CPPFLAGS, they
# mean C++ flags, i.e. CXXFLAGS, not “C PreProcessor Flags” as is common in
# autoconf-influenced projects.
sed -r -i \
    -e 's/([[:alpha:]]+FLAGS[[:blank:]]*)=/\1+=/' \
    -e 's/(\$\(CC\))(.*)-std=[^[:blank:]]+/\$\(CXX\)\2/' \
    -e 's/CPPFLAGS/CXXFLAGS/' tests/Makefile

# Add a dummy main(); how does this one work upstream?! Note that omitting
# parameter names is a C++-ism.
echo 'int main(int, char *[]) { return 0; }' >> tests/test_cpp_compilation.cpp

# Remove any pre-compiled Windows executables
find . -type f -name '*.exe' -print -delete

# Remove some unused parts of the source tree that could contribute different
# (but acceptable) license terms if they were used—just to prove that we do not
# use them.
rm -rvf tests/caveview
find deprecated -type f ! -name 'stb_image_resize.h' -print -delete

%if %{without stb_include}
sed -r -i '/#include[[:blank:]]+"stb_include.h"/d' tests/test_c_compilation.c
%endif


%build
# There is no compiled code to install, since all stb libraries are
# header-only. We do need to build the tests.
%make_build -C tests


%install
# Installing a “.c” file in /usr/include is unconventional, but correct and not
# unprecedented. Any .c file in stb is meant to be #include’d and used as a
# header-only library, just as the “.h” files in the other stb libraries. The
# only difference is the file extension.
#
# Since these are designed to be copied into dependent package source trees,
# there is no convention on include paths. Most projects end up using “#include
# <stb_foo.h>” or “#include <stb/stb_foo.h>”, so we install to
# %%{_includedir}/stb/stb_foo.h and %%{_includedir}/stb_foo.h, with the latter
# as a symbolic link to the former. This means most projects can unbundle the
# library without having to make their own local symlinks or patch their
# sources.
install -t '%{buildroot}%{_includedir}/stb' -p -m 0644 -D \
    stb_*.h stb_*.c deprecated/stb_image_resize.h
%if %{without stb_include}
rm -vf '%{buildroot}%{_includedir}/stb/stb_include.h'
%endif
pushd '%{buildroot}%{_includedir}'
ln -sv stb/stb_*.? .
popd


%check
# The tests in tests/Makefile are largely just “will it compile” tests. There
# are some other files with main routines under tests/, but they have neither
# Makefile targets nor instructions on how to build or run them or what to
# expect them to do. We don’t dig through these sources to try to guess what to
# do with them.

# We can run image_write_test and confirm the output images are valid.
rm -vf output
mkdir -p output
./tests/image_write_test
# We assume that if ImageMagick can read the output images, then they are valid.
for img in wr6x5_flip.bmp wr6x5_flip.jpg wr6x5_flip.tga wr6x5_regular.hdr \
    wr6x5_regular.png wr6x5_flip.hdr wr6x5_flip.png wr6x5_regular.bmp \
    wr6x5_regular.jpg wr6x5_regular.tga
do
  convert "output/${img}" 'output/dummy.bmp'
done

# As a sanity check, verify that all of the subpackage version numbers appear
# in the corresponding headers.
while read -r version header
do
  %{?!with_stb_include:if [ "${header}" = 'stb_include.h' ]; then continue; fi}
  # The minor version may be zero-padded in the header.
  grep -E "$(
    echo "${version}" |
    sed -r 's/([[:digit:]]+)\.([[:digit:]]+)/\\bv\1\\.0*\2\\b/'
  )" "%{buildroot}%{_includedir}/${header}" >/dev/null
done <<'EOF'
%{stb_c_lexer_version} stb_c_lexer.h
%{stb_connected_components_version} stb_connected_components.h
%{stb_divide_version} stb_divide.h
%{stb_ds_version} stb_ds.h
%{stb_dxt_version} stb_dxt.h
%{stb_easy_font_version} stb_easy_font.h
%{stb_herringbone_wang_tile_version} stb_herringbone_wang_tile.h
%{stb_hexwave_version} stb_hexwave.h
%{stb_image_version} stb_image.h
%{stb_image_resize_version} stb_image_resize.h
%{stb_image_resize2_version} stb_image_resize2.h
%{stb_image_write_version} stb_image_write.h
%{stb_include_version} stb_include.h
%{stb_leakcheck_version} stb_leakcheck.h
%{stb_perlin_version} stb_perlin.h
%{stb_rect_pack_version} stb_rect_pack.h
%{stb_sprintf_version} stb_sprintf.h
%{stb_textedit_version} stb_textedit.h
%{stb_tilemap_editor_version} stb_tilemap_editor.h
%{stb_truetype_version} stb_truetype.h
%{stb_vorbis_version} stb_vorbis.c
%{stb_voxel_render_version} stb_voxel_render.h
EOF


%files devel
# Empty metapackage


%files doc
%license LICENSE
%doc docs
%doc README.md
%doc tests/tilemap_editor_integration_example.c


%files -n stb_c_lexer-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_c_lexer.h
%{_includedir}/stb_c_lexer.h


%files -n stb_connected_components-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_connected_components.h
%{_includedir}/stb_connected_components.h


%files -n stb_divide-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_divide.h
%{_includedir}/stb_divide.h


%files -n stb_ds-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_ds.h
%{_includedir}/stb_ds.h


%files -n stb_dxt-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_dxt.h
%{_includedir}/stb_dxt.h


%files -n stb_easy_font-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_easy_font.h
%{_includedir}/stb_easy_font.h


%files -n stb_herringbone_wang_tile-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_herringbone_wang_tile.h
%{_includedir}/stb_herringbone_wang_tile.h


%files -n stb_hexwave-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_hexwave.h
%{_includedir}/stb_hexwave.h


%files -n stb_image-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_image.h
%{_includedir}/stb_image.h


%files -n stb_image_resize-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_image_resize.h
%{_includedir}/stb_image_resize.h


%files -n stb_image_resize2-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_image_resize2.h
%{_includedir}/stb_image_resize2.h


%files -n stb_image_write-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_image_write.h
%{_includedir}/stb_image_write.h


%if %{with stb_include}
%files -n stb_include-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_include.h
%{_includedir}/stb_include.h
%endif


%files -n stb_leakcheck-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_leakcheck.h
%{_includedir}/stb_leakcheck.h


%files -n stb_perlin-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_perlin.h
%{_includedir}/stb_perlin.h


%files -n stb_rect_pack-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_rect_pack.h
%{_includedir}/stb_rect_pack.h


%files -n stb_sprintf-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_sprintf.h
%{_includedir}/stb_sprintf.h


%files -n stb_textedit-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_textedit.h
%{_includedir}/stb_textedit.h


%files -n stb_tilemap_editor-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_tilemap_editor.h
%{_includedir}/stb_tilemap_editor.h


%files -n stb_truetype-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_truetype.h
%{_includedir}/stb_truetype.h


%files -n stb_vorbis-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_vorbis.c
%{_includedir}/stb_vorbis.c


%files -n stb_voxel_render-devel
%license LICENSE
# Directory has shared ownership across stb subpackages:
%dir %{_includedir}/stb
%{_includedir}/stb/stb_voxel_render.h
%{_includedir}/stb_voxel_render.h


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 0^20251025gitf1c79c0-4
- test: add initial lock files

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0^20251025gitf1c79c0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Nov 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20251025gitf1c79c0-2
- Patch two newly-reported memory-safety bugs in stb_image
- https://github.com/nothings/stb/issues/1860
- https://github.com/nothings/stb/issues/1861

* Sat Oct 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20251025gitf1c79c0-1
- stb_image_resize2 2.17

* Sun Sep 07 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20250907gitfede005-1
- stb_image_resize2 2.15

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0^20250512git802cd45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 12 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20250512git802cd45-1
- stb_image_resize2 2.14

* Sun Mar 16 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20250314gitf056911-1
- stb_image_resize2 2.13

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0^20241002git31707d1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20241002git31707d1-5
- Patch root cause of CVE-2021-45340

* Sun Dec 15 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20241002git31707d1-4
- Add a SourceLicense field

* Tue Nov 26 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20241002git31707d1-3
- Remove spec-file conditionals for Fedora 39 and EPEL7 (end-of-life)

* Tue Oct 22 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20241002git31707d1-2
- Revert "Conditionalize a test that uses ImageMagick"

* Wed Oct 02 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20241002git31707d1-1
- stb_image_resize2 2.11

* Mon Aug 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20240531git013ac3b-3
- Conditionalize a test that uses ImageMagick
- EPEL10 does not yet have ImageMagick

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0^20240531git013ac3b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 31 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20240531git013ac3b-1
- stb_image 2.30

* Sat May 25 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20240525git449758b-1
- stb_image_resize2 2.07

* Thu May 02 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20240213gitae721c5-7
- Patch for GHSL-2023-171/CVE-2023-45681/CVE-2023-47212

* Thu May 02 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20240213gitae721c5-6
- Patch for GHSL-2023-171/CVE-2023-45681/CVE-2023-47212

* Wed Apr 03 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20240213gitae721c5-5
- Fix a description to use American English orthography

* Wed Feb 14 2024 David Abdurachmanov <davidlt@rivosinc.com> - 0^20240213gitae721c5-2
- Fix compile error on riscv64

* Tue Feb 13 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20240213gitae721c5-1
- Update to 0^20240213gitae721c5
- stb_image_resize2-devel is updated to 2.06

* Sun Feb 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20240208gitb7cf124-1
- Update to 0^20240208gitb7cf124
- stb_image-devel is updated to 2.29
- stb_image_resize2-devel is updated to 2.05

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0^20231011gitbeebb24-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231011gitbeebb24-12
- stb_vorbis: fix GHSL-2023-165 / fix CVE-2023-45675

* Wed Oct 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231011gitbeebb24-11
- stb_image: fix GHSL-2023-151 / fix CVE-2023-45667

* Wed Oct 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231011gitbeebb24-10
- stb_image: fix GHSL-2023-150 / fix CVE-2023-45666

* Wed Oct 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231011gitbeebb24-9
- Document another bug, PR, and name (GHSL-2023-149) for CVE-2023-43898

* Wed Oct 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231011gitbeebb24-8
- stb_image: fix GHSL-2023-148 / fix CVE-2023-45664

* Wed Oct 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231011gitbeebb24-7
- stb_image: fix GHSL-2023-147 / fix CVE-2023-45663

* Wed Oct 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231011gitbeebb24-6
- stb_image: fix GHSL-2023-146 / fix CVE-2023-45662

* Wed Oct 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231011gitbeebb24-5
- stb_image: fix GHSL-2023-145 / fix CVE-2023-45661

* Wed Oct 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231011gitbeebb24-4
- Document that 1454.patch fixes CVE-2023-43898

* Wed Oct 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231011gitbeebb24-3
- Backport a PR fixing undefined behavior in stb_image_resize2

* Wed Oct 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231011gitbeebb24-2
- Backport three PR’s fixing undefined behavior in stb_image

* Wed Oct 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231011gitbeebb24-1
- Update to 0^beebb24git20231011 (minor C99 fixes)

* Tue Oct 10 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231009gitc4bbb6e-2
- Fedora, EPEL9+: drop the initial “0.” from the Release

* Tue Oct 10 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20231009gitc4bbb6e-0.1
- Update to 0^20231009gitc4bbb6e
- A new stb_image_resize2 library is introduced
- Upstream has deprecated stb_image_resize, but we still package it

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0^20230129git5736b15-0.7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 18 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20230129git5736b15-0.6
- Use new (rpm 4.17.1+) bcond style

* Sat Jun 03 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20230129git5736b15-0.5
- Remove explicit %%set_build_flags, not needed since F36

* Sat Feb 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20230129git5736b15-0.2
- Fix null pointer dereference in stb_image

* Mon Jan 30 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20230129git5736b15-0.1
- Update to 5736b1 (version history and README updates)

* Sun Jan 29 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20230129git6199bf7-0.1
- Update to 6199bf7 (stb_image 2.28)
- Security-related patches for stb_image have been merged upstream, and
  there are other bugfixes.

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0^20220908git8b5f1f3-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 30 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20220908git8b5f1f3-0.4
- Patch in a candidate fix for ossfuzz issue 24232
- Improves handling of certain invalid PNGs by stb_image

* Sat Sep 10 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20220908git8b5f1f3-0.3
- A few improved descriptions

* Sat Sep 10 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20220908git8b5f1f3-0.2
- Improved summaries based on upstream’s README.md

* Fri Sep 09 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20220908git8b5f1f3-0.1
- Update to 8b5f1f3
- The stb_perlin-devel subpackage has been restored, as upstream believes
  all relevant patents are now expired.

* Fri Sep 09 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20210910gitaf1a5bc-0.5
- Update License to SPDX

* Thu Jul 28 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20210910gitaf1a5bc-0.4
- Reword spec file note on stb_include

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0^20210910gitaf1a5bc-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Apr 20 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20210910gitaf1a5bc-0.2
- Security fix for CVE-2022-28041 (fix RHBZ#2077020, fix RBHZ#2077019)

* Sat Apr 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0^20210910gitaf1a5bc-0.1
- Switch to modern snapshot versioning

* Sat Apr 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0-0.10
- Stop numbering patches

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0-0.8
- Apply a patch for warnings in stb_herringbone_wang_tile

* Fri Oct 22 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0-0.7
- Security fix for CVE-2021-42715 and CVE-2021-42716

* Fri Oct 22 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0-0.6
- Update to af1a5bc

* Fri Oct 22 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0-0.5
- Reduce macro indirection in the spec file

* Thu Sep 09 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0-0.4
- Update to c0c9826 (fix RHBZ#2002436)

* Tue Aug 24 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0-0.3
- Fix signature of dummy realloc() for STB_VORBIS_NO_CRT

* Mon Aug 23 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0-0.2
- Use symlinks so including "stb_foo.h" and "stb/stb_foo.h" both work

* Mon Aug 23 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0-0.1
- Initial package
## END: Generated by rpmautospec
