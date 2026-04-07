# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libass
Version:        0.17.3
Release:        4%{?dist}
Summary:        Portable library for SSA/ASS subtitles rendering
License:        ISC
URL:            https://github.com/libass

Source0:        https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  nasm
BuildRequires:  pkgconfig(fontconfig) >= 2.10.92
BuildRequires:  pkgconfig(freetype2) >= 9.10.3
BuildRequires:  pkgconfig(fribidi) >= 0.19.0
BuildRequires:  pkgconfig(harfbuzz) >= 0.9.5
BuildRequires:  pkgconfig(libpng) >= 1.2.0
%ifnarch %{ix86}
BuildRequires:  pkgconfig(libunibreak) >= 1.1
%endif
BuildRequires:  make

%description
Libass is a portable library for SSA/ASS subtitles rendering.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
make check

%ldconfig_scriptlets

%files
%license COPYING
%doc Changelog
%{_libdir}/*.so.9*

%files devel
%{_includedir}/ass
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Xavier Bachelot <xavier@bachelot.org> - 0.17.3-1
- Update to 0.17.3 (RHBZ#2295523)

* Sat Jun 15 2024 Xavier Bachelot <xavier@bachelot.org> - 0.17.2-1
- Update to 0.17.2 (RHBZ#2281493)
- Add upstream patches to fix %%check
- Add optional dependency on libunibreak

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr 24 2023 Nicolas Chauvet <kwizart@gmail.com> - 0.17.1-1
- Update to 0.17.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 01 2022 Nicolas Chauvet <kwizart@gmail.com> - 0.17.0-1
- Update to 0.17.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun May 15 2022 Nicolas Chauvet <kwizart@gmail.com> - 0.16.0-1
- Update to 0.16.0

* Wed Feb 23 2022 Nicolas Chauvet <kwizart@gmail.com> - 0.15.2-1
- Update to 0.15.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Simone Caronni <negativo17@gmail.com> - 0.14.0-1
- Update to 0.14.0 (fixes glyph bounding box size; this bug causes frames to
  be dropped on 2160p+ displays, as this check is too small for resolutions
  above 1440p).
- Revamp SPEC file.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 07 2016 Martin Sourada <mso@fedoraproject.org> - 0.13.4-1
- Update to 0.13.4
- Fixes CVE-2016-7969, CVE-2016-7970, CVE-2016-7972


* Tue Sep 27 2016 Martin Sourada <mso@fedoraproject.org> - 0.13.3-1
- Update to 0.13.3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Martin Sourada <mso@fedoraproject.org> - 0.13.1-1
- Update to 0.13.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 26 2015 Martin Sourada <mso@fedoraproject.org> - 0.12.1-1
- Update to 0.12.1

* Thu Nov 06 2014 Martin Sourada <mso@fedoraproject.org> - 0.12.0-1
- Codebase moved from google code to github.
- Update to 0.12.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.2-1
- Update to 0.10.2
- Run make check

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Martin Sourada <mso@fedoraproject.org> - 0.10.1-2
- Fix a mistake in minimal required version of harfbuzz

* Wed Oct 17 2012 Martin Sourada <mso@fedoraproject.org> - 0.10.1-1
- New upstream release
  - various improvements and fixes
  - improved compatibility with vsfilter
- Build with harfbuzz from F18 onward for advanced opentype shaping

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Martin Sourada <mso@fedoraproject.org> - 0.10.0-1
- New upstream release
  - various improvements and fixes
- BuildRequires: fribidi-devel (bidirectional text suport)
- Fixes some wierd memory allocation related crash with freetype 2.4.6
  - rhbz 753017, rhbz 753065

* Tue May 31 2011 Martin Sourada <mso@fedoraproject.org> - 0.9.12-1
- New upstream release
  - Licence changed to ISC
  - Fixed word-wrapping
  - Improved charmap fallback matching
  - Various other improvements and fixes

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.9.11-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Martin Sourada <mso@fedoraproject.org> - 0.9.11-1
- Fixes rhbz #630432
- New upstream release
  - Various fixes
  - Performance improvements
  - Calculate drawing bounding box like VSFilter
  - Better PAR correction if text transforms are used
  - Improved fullname font matching
  - Add ass_flush_events API function
  - Basic support for @font vertical text layout

* Fri Jul 30 2010 Martin Sourada <mso@fedoraproject.org> - 0.9.9-1
- Fixes rhbz #618733
- New upstream release
  - Parse numbers in a locale-independent way
  - Disable script file size limit
  - Match fonts against the full name ("name for humans")
  - Reset clip mode after \iclip
  - Improve VSFilter compatibility
  - A couple of smaller fixes and cleanups

* Sun Jan 10 2010 Martin Sourada <mso@fedoraproject.org> - 0.9.8-2
- Fix source URL

* Sun Oct 25 2009 Martin Sourada <mso@fedoraproject.org> - 0.9.8-1
- New upstream release
- See http://repo.or.cz/w/libass.git?a=blob;f=Changelog for changes

* Mon Aug 10 2009 Martin Sourada <mso@fedoraproject.org> - 0.9.7-1
- New upstream release
- Upstream changed from sourceforge to code.google

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 24 2009 Martin Sourada <mso@fedoraproject.org> - 0.9.6-2
- remove glibc-devel and freetype-devel BRs, they're already pulled in by the
  rest

* Sun Mar 22 2009 Martin Sourada <mso@fedoraproject.org> - 0.9.6-1
- update to newever version
- drop %%doc from -devel
- update source url to conform with fedora packaging guidelines

* Sun Mar 22 2009 Martin Sourada <mso@fedoraproject.org> - 0.9.5-1
- Initial rpm package
