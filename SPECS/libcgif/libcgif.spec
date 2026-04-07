# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# remirepo/fedora spec file for libcgif
#
# SPDX-FileCopyrightText:  Copyright 2021-2026 Remi Collet
# SPDX-License-Identifier: CECILL-2.1
# http://www.cecill.info/licences/Licence_CeCILL_V2-en.txt
#
# Please, preserve the changelog entries
#

%global gh_commit   f54941864e8976dc73987e2eccadf2436a172a95
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
#global gh_date     20211001
%global gh_owner    dloebl
%global gh_project  cgif
%global libname     libcgif
%global soname      0

Name:          %{libname}
Summary:       A fast and lightweight GIF encoder
Version:       0.5.1
Release:       1%{?dist}
License:       MIT

URL:           https://github.com/%{gh_owner}/%{gh_project}
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRequires: gcc
BuildRequires: meson >= 0.56


%description
A fast and lightweight GIF encoder that can create GIF animations and images.

Summary of the main features:

- user-defined global or local color-palette with up to 256 colors
  (limit of the GIF format)
- size-optimizations for GIF animations:
  - option to set a pixel to transparent if it has identical color in the
    previous frame (transparency optimization)
  - do encoding just for the rectangular area that differs from the previous
    frame (width/height optimization)
- fast: a GIF with 256 colors and 1024x1024 pixels can be created in below
  50 ms even on a minimalistic system
- MIT license (permissive)
- different options for GIF animations: static image, N repetitions, infinite
  repetitions
- additional source-code for verifying the encoder after making changes
- user-defined delay time from one frame to the next (can be set independently
  for each frame)
- source-code conforms to the C99 standard


%package devel
Summary:    Header files and development libraries for %{libname}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{libname}.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
%meson
%meson_build


%install
%meson_install


%check
%meson_test


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/%{libname}.so.%{soname}*

%files devel
%doc README.md
%{_libdir}/pkgconfig/%{gh_project}.pc
%{_libdir}/%{libname}.so
%{_includedir}/%{gh_project}.h


%changelog
* Tue Jan 20 2026 Remi Collet <remi@remirepo.net> - 0.5.1-1
- update to 0.5.1

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Feb 10 2025 Remi Collet <remi@remirepo.net> - 0.5.0-1
- update to 0.5.0
- re-license spec file to CECILL-2.1

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul  2 2024 Remi Collet <remi@remirepo.net> - 0.4.1-1
- update to 0.4.1

* Tue Jul  2 2024 Remi Collet <remi@remirepo.net> - 0.4.1-1
- update to 0.4.1

* Thu Apr  4 2024 Remi Collet <remi@remirepo.net> - 0.4.0-1
- update to 0.4.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 23 2023 Remi Collet <remi@remirepo.net> - 0.3.2-1
- update to 0.3.2 (no change)

* Thu Apr  6 2023 Remi Collet <remi@remirepo.net> - 0.3.1-1
- update to 0.3.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Apr 25 2022 Remi Collet <remi@remirepo.net> - 0.3.0-1
- update to 0.3.0

* Thu Mar  3 2022 Remi Collet <remi@remirepo.net> - 0.2.1-1
- update to 0.2.1

* Wed Feb 16 2022 Remi Collet <remi@remirepo.net> - 0.2.0-1
- update to 0.2.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan  2 2022 Remi Collet <remi@remirepo.net> - 0.1.0-1
- update to 0.1.0

* Mon Dec 13 2021 Remi Collet <remi@remirepo.net> - 0.0.4-1
- update to 0.0.4

* Sun Nov 28 2021 Remi Collet <remi@remirepo.net> - 0.0.3-1
- update to 0.0.3

* Tue Nov  9 2021 Remi Collet <remi@remirepo.net> - 0.0.2-1
- update to 0.0.2

* Mon Nov  8 2021 Remi Collet <remi@remirepo.net> - 0.0.1-1
- initial package
- add patch to fix missing version in pc file
  reported as https://github.com/dloebl/cgif/issues/24
  from https://github.com/dloebl/cgif/pull/26
