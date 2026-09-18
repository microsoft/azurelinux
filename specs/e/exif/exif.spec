# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           exif
Version:        0.6.22
Release:        12%{?dist}
Summary:        Utility to show EXIF information hidden in JPEG files
Summary(fr):    Outil pour afficher les informations EXIF masquées dans les fichiers JPEG

License:        LGPL-2.1-or-later
URL:            http://libexif.sourceforge.net/
Source0:        https://github.com/libexif/exif/archive/exif-0_6_22-release/%{name}-%{version}.tar.gz
Patch0:         f6334d9d32437ef13dc902f0a88a2be0063d9d1c.patch

BuildRequires:  gcc
BuildRequires:  libexif-devel
BuildRequires:  popt-devel
BuildRequires: make
BuildRequires: autoconf automake gettext-devel libtool

%description
Small command-line utility to show EXIF information hidden
in JPEG files.

%description -l fr
Petit utilitaire en ligne de commande pour afficher les informations
EXIF masquées dans les fichiers JPEG.


%prep
%setup -qnexif-exif-0_6_22-release

%patch -P0 -p1

# Convert to UTF8 AUTHORS doc file :
iconv -f iso-8859-1 -t utf8 AUTHORS >AUTHORS.tmp
touch -r AUTHORS AUTHORS.tmp
mv AUTHORS.tmp AUTHORS


%build
autoreconf -if
%configure
%make_build


%install
%make_install
%find_lang %{name}

%ifnarch s390x
%check
make check
%endif


%files -f %{name}.lang
%doc ABOUT-NLS AUTHORS COPYING NEWS README ChangeLog
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.22-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.22-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.22-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Mar 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.6.22-6
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 10 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.6.22-1
- 0.6.22, patch for CVE-2021-27815.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.21-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.21-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 0.6.21-18
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.21-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.21-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.21-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.21-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.21-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.21-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.21-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.21-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.21-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 16 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 0.6.21-3
- Add French translation in spec file

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 0.6.21-1
- Update to 0.6.21
  - Fix CVE-2012-2845 (RHBZ #840002,#840003)
- Update scriplet in %%prep section of spec file

* Fri Apr 13 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 0.6.20-3
- fix license in spec file (again)

* Wed Feb 24 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 0.6.20-2
- fix license in spec file
- remove %%{_datadir}/locale/* lines in %%files section
- fix man file extension in %%files section
- add %%check section

* Mon Feb 13 2012 Matthieu Saulnier <fantom@fedoraproject.org> - 0.6.20-1
- Initial Release
