# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global font_util 1.4.1

# Must be kept in sync with xorg-x11-fonts!
%global _x11fontdir %{_datadir}/X11/fonts

Summary:    X.Org X11 font utilities
Name:       xorg-x11-font-utils
Epoch:      1
Version:    7.5
Release:    62%{?dist}
License:    MIT AND BSD-2-Clause AND MIT-open-group AND Unicode-3.0
URL:        http://www.x.org

Source0:    http://www.x.org/pub/individual/font/font-util-%{font_util}.tar.xz
# helper script used in post for xorg-x11-fonts
Source5:    xorg-x11-fonts-update-dirs
Source6:    xorg-x11-fonts-update-dirs.1

BuildRequires:  gcc make libtool
BuildRequires:  pkgconfig(xorg-macros) >= 1.8

Provides:   font-util = %{font_util}

Provides:   font-utils = %{epoch}:%{version}-%{release}
Provides:   ucs2any = %{font_util}

Obsoletes:  bdftopcf < 1.1-1
Obsoletes:  fonttosfnt < 1.2.1-1
Obsoletes:  mkfontdir < 1.2.1-1
Obsoletes:  mkfontscale < 1.2.1-1

%description
X.Org X11 font utilities required for font installation, conversion, and
generation.

%prep
%autosetup -n font-util-%{font_util}

%build
%configure --with-fontrootdir=%{_x11fontdir}
%make_build

%install
%make_install

install -m 744 %{SOURCE5} $RPM_BUILD_ROOT%{_bindir}/xorg-x11-fonts-update-dirs
sed -i "s:@DATADIR@:%{_datadir}:" $RPM_BUILD_ROOT%{_bindir}/xorg-x11-fonts-update-dirs

install -m 744 -p -D %{SOURCE6} $RPM_BUILD_ROOT%{_mandir}/man1/xorg-x11-fonts-update-dirs.1

find $RPM_BUILD_ROOT -name bdftruncate\* -print0 | xargs -0 rm -f

%files
%doc README.md
%license COPYING
%{_bindir}/ucs2any
%{_bindir}/xorg-x11-fonts-update-dirs
%{_datadir}/aclocal/fontutil.m4
%{_libdir}/pkgconfig/fontutil.pc
%{_mandir}/man1/ucs2any.1*
%{_mandir}/man1/xorg-x11-fonts-update-dirs.1*
%dir %{_x11fontdir}
%dir %{_x11fontdir}/util
%{_x11fontdir}/util/map-*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-62
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Peter Hutterer <peter.hutterer@redhat.com> - 7.5-58
- font-utils 1.4.1 with sources this time

* Wed Jan 03 2024 Peter Hutterer <peter.hutterer@redhat.com> - 7.5-57
- font-utils 1.4.1
- SPDX migration: update to SPDX-compatible license terms

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 25 2021 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-51
- Drop bdftopcf, mkfontscale and fonttosfnt, they are in separate packages
  now (#1932731)

* Tue Feb 23 2021 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-50
- Update to mkfontscale 1.2.1 which obsoletes the separate mkfontdir.

* Sun Feb 21 2021 Neal Gompa <ngompa13@gmail.com> - 1:7.5-49
- Add OrderWithRequires for freetype to ensure freetype is installed first
- Move license files to license tag on file list

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 16 2020 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-47
- fonttosfnt 1.2.1

* Thu Nov  5 10:26:37 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 1:7.5-46
- Add BuildRequires for make

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-43
- fonttosfnt 1.1.0

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 01 2018 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-40
- fonttosfnt 1.0.5

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 17 2018 Peter Hutterer <peter.hutterer@redhat.com> 1:7.5-38
- mkfontscale 1.1.3

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Adam Jackson <ajax@redhat.com> - 7.5-36
- bdftopcf 1.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 28 2016 Hans de Goede <hdegoede@redhat.com> - 1:7.5-32
- bdftopcf 1.0.5

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:7.5-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Thu Oct 15 2015 Adam Jackson <ajax@redhat.com> 7.5-30
- Drop bdftruncate utility, nothing in the OS uses it and we don't ship BDF
  fonts in any case.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:7.5-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 01 2015 Simone Caronni <negativo17@gmail.com> - 1:7.5-28
- font-util 1.3.1

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1:7.5-27
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Jan 17 2015 Simone Caronni <negativo17@gmail.com> - 1:7.5-26
- Update mkfontscale to 1.1.2.

* Mon Nov 10 2014 Simone Caronni <negativo17@gmail.com> - 1:7.5-25
- Restore font-utils provider, required by some packages for building.
 examine all platform=3 encodings (fixes #578460)
