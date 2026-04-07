# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# The presence of this macro ensures the disttag changes
# when set in side tags
%bcond_with bootstrap

%if 0%{?rhel} && 0%{?rhel} < 9
%bcond_with ffmpeg
%else
%bcond ffmpeg %{?_with_bootstrap:0}%{!?_with_bootstrap:1}
%endif
# Globing of libraries is against the packging guidelines
%global sover 1


Name:           chromaprint
Version:        1.6.0
Release:        1%{?dist}
Summary:        Library implementing the AcoustID fingerprinting

# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            http://www.acoustid.org/chromaprint
Source:         https://github.com/acoustid/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  fftw-devel >= 3
BuildRequires:  ninja-build

%description
Chromaprint library is the core component of the AcoustID project. It's a
client-side library that implements a custom algorithm for extracting
fingerprints from raw audio sources.

The library exposes a simple C API. The documentation for the C API can be
found in the main header file.

License for binaries is GPLv2+ but source code is MIT + LGPLv2+

%package -n libchromaprint
Summary:        Library implementing the AcoustID fingerprinting
Obsoletes:      python-chromaprint < 0.6-3

%description -n libchromaprint
Chromaprint library is the core component of the AcoustID project. It's a
client-side library that implements a custom algorithm for extracting
fingerprints from raw audio sources.

The library exposes a simple C API. The documentation for the C API can be
found in the main header file.

License for binaries is GPLv2+ but source code is MIT + LGPLv2+

%package -n libchromaprint-devel
Summary:        Headers for developing programs that will use %{name}
Requires:       libchromaprint%{?_isa} = %{version}-%{release}

%description -n libchromaprint-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.

The library exposes a simple C API. The documentation for the C API can be
found in the main header file.

%if %{with ffmpeg}
%package tools
Summary:        Chromaprint audio fingerprinting tools
BuildRequires:  ffmpeg-free-devel
Requires:       libchromaprint%{?_isa} = %{version}-%{release}

%description tools
Chromaprint library is the core component of the AcoustID project. It's a
client-side library that implements a custom algorithm for extracting
fingerprints from raw audio sources.

This is a set of Chromaprint tools related to acoustic fingerprinting
featuring fpcalc an standalone AcoustID tool used by Picard.

License for binaries is GPLv2+ but source code is MIT + LGPLv2+
%endif

%prep
%autosetup -p1

%build
# examples and cli tools require ffmpeg, so turn off.
%cmake -GNinja \
        -DCMAKE_BUILD_TYPE=Release \
        -DBUILD_TESTS=ON \
        -DBUILD_TOOLS=%{?with_ffmpeg:ON}%{!?with_ffmpeg:OFF}

%cmake_build

%install
%cmake_install

rm  -f %{buildroot}%{_libdir}/lib*.la

%check
%ctest

%files -n libchromaprint
%doc NEWS.txt README.md
%license LICENSE.md
%{_libdir}/lib*.so.%{sover}*

%files -n libchromaprint-devel
%{_includedir}/chromaprint.h
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_libdir}/cmake/Chromaprint/
%{_libdir}/cmake/Chromaprint/*.cmake

%if %{with ffmpeg}
%files tools
%{_bindir}/fpcalc
%endif

%changelog
* Tue Oct 28 2025 Andrew Bauer <zonexpertconsulting@outlook.com> - 1.6.0-1
- 1.6.0 release RHBZ#2391533
- Includes fixes for Cmake 4 RHBZ#2381184 RHBZ#2380497
- re-enable tests. They no longer require external artifacts

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jan 22 2025 Andrew Bauer <zonexpertconsulting@outlook.com> - 1.5.1-24
- Fix fpcalc could not create an audio converter isntance

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 20 2024 Neal Gompa <ngompa@fedoraproject.org> - 1.5.1-22
- Rebuild for ffmpeg 7

* Fri Sep 20 2024 Neal Gompa <ngompa@fedoraproject.org> - 1.5.1-21
- Drop bootstrap bcond in the spec as it is unneeded

* Sat Sep 07 2024 Sérgio Basto <sergio@serjux.com> - 1.5.1-20
- bootstrap chromaprint to break circular dependency with ffmpeg.

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 1.5.1-19
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 12 2024 Fabio Valentini <decathorpe@gmail.com> - 1.5.1-15
- Rebuild post bootstrap build for ffmpeg/dav1d.

* Fri Jan 12 2024 Fabio Valentini <decathorpe@gmail.com> - 1.5.1-14
- Rebuild without ffmpeg to break circular dependency with ffmpeg/dav1d.

* Sun Aug 06 2023 Richard Shaw <hobbes1069@gmail.com> - 1.5.1-13
- Rebuild post bootstrap build for ffmpeg/codec2.

* Sun Aug 06 2023 Richard Shaw <hobbes1069@gmail.com> - 1.5.1-12
- Rebuild without ffmpeg to break circular dependency with ffmpeg/codec2.
- Add %%sover to prevent accidental soname bumps.

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Mar 25 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.5.1-10
- Switch off bootstrap mode
- Simplify bootstrap mode logic

* Tue Mar 14 2023 Sérgio Basto <sergio@serjux.com> - 1.5.1-9_bootstrap
- Add a bootstrap package as suggests in
  https://github.com/acoustid/chromaprint/issues/129#issuecomment-1468612507
- Change to Ninja build

* Sun Mar 12 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.5.1-8
- Rebuild for ffmpeg 6.0

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 22 2022 Sérgio Basto <sergio@serjux.com> - 1.5.1-6
- Backport oficial ffmpeg 5 support

* Mon Aug 29 2022 Neal Gompa <ngompa@fedoraproject.org> - 1.5.1-5
- Rebuild for ffmpeg 5.1 (#2121070)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 21 2022 Neal Gompa <ngompa@fedoraproject.org> - 1.5.1-3
- Build tools on F36+ with ffmpeg-free
- Clean out extra whitespace in the spec file

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 23 2021 Andrew Bauer <zonexpertconsulting@outlook.com> - 1.5.1-1
- Update to 1.5.1 release

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Andrew Bauer <zonexpertconsulting@outlook.com> - 1.5.0-1
- modernize specfile
- Update to 1.5.0 release

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Björn Esser <besser82@fedoraproject.org> - 1.4.2-4
- Append curdir to CMake invokation. (#1668512)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 04 2018 smael Olea <ismael@olea.org> - 1.4.2
- upstream URL changed to github
- updating to 1.4.2
- renamed COPYING.txt LICENSE.md
- binary licenses should be GPLv2+ because linking with fftw (which uses GPLv2+)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.2-2
- Rebuilt for GCC 5 C++11 ABI change

* Tue Mar 17 2015 Ismael Olea <ismael@olea.org> - 1.2-1   
- update to 1.2

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Nov 23 2013 Ismael Olea <ismael@olea.org> - 1.1-1   
- update to 1.1
- CHANGES.txt file removed in upstream

* Mon Sep 16 2013 Ismael Olea <ismael@olea.org> - 1.0-1
- update to 1.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 6 2012 Ismael Olea <ismael@olea.org> - 0.7-1
- update to 0.7

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 7 2012 Ismael Olea <ismael@olea.org> - 0.6-4
- moved the obsoletes python-chromaprint to libchromaprint

* Mon Feb 6 2012 Ismael Olea <ismael@olea.org> - 0.6-3
- cosmetic SPEC changes
- obsoleting python-chromaprint (see #786946)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 27 2011 Ismael Olea <ismael@olea.org> - 0.6-1
- update to 0.6
- python bindings removed
- python not a requirment now

* Wed Dec 07 2011 Ismael Olea <ismael@olea.org> - 0.5-4
- minor spec enhancements

* Mon Dec 05 2011 Ismael Olea <ismael@olea.org> - 0.5-3
- Macro cleaning at spec

* Fri Nov 18 2011 Ismael Olea <ismael@olea.org> - 0.5-2
- first version for Fedora

* Thu Nov 10 2011 Ismael Olea <ismael@olea.org> - 0.5-1
- update to 0.5
- subpackage for fpcalc 

* Sat Aug 06 2011 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.4-1
- Initial package
