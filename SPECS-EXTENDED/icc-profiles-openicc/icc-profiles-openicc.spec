Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           icc-profiles-openicc
Version:        1.3.1
Release:        19%{?dist}
Summary:        The OpenICC profiles

License:        zlib
URL:            https://www.freedesktop.org/wiki/OpenIcc
Source0:        https://downloads.sourceforge.net/project/openicc/OpenICC-Profiles/%{name}-%{version}.tar.bz2

BuildArch:      noarch

BuildRequires:  color-filesystem
Requires:       color-filesystem


%description
The OpenICC profiles are provided to serve color managed
applications and services.


%prep
%setup -q


%build
%configure --enable-verbose
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/{pixmaps,mime/packages}

install -pm 0644 *.png $RPM_BUILD_ROOT%{_datadir}/pixmaps



%files
%doc AUTHORS ChangeLog COPYING
%doc default_profiles/base/LICENSE-ZLIB
%doc default_profiles/base/LICENSE-ZLIB-LSTAR
%dir %{_icccolordir}/OpenICC
%{_icccolordir}/OpenICC/compatibleWithAdobeRGB1998.icc
%{_icccolordir}/OpenICC/sRGB.icc
%{_icccolordir}/OpenICC/ProPhoto-RGB.icc
%dir %{_icccolordir}/Oyranos
%{_icccolordir}/Oyranos/Gray-CIE_L.icc
%{_icccolordir}/Oyranos/Gray_linear.icc
%{_icccolordir}/Oyranos/ITULab.icc
%dir %{_icccolordir}/basICColor
%{_icccolordir}/basICColor/LStar-RGB.icc
%dir %{_icccolordir}/lcms
%{_icccolordir}/lcms/LCMSLABI.ICM
%{_icccolordir}/lcms/LCMSXYZI.ICM
%{_icccolordir}/lcms/Lab.icc
%{_icccolordir}/lcms/XYZ.icc
%dir %{_colordir}/target
%dir %{_colordir}/target/NPES
%{_colordir}/target/NPES/TR002.ti3
%{_colordir}/target/NPES/TR003.ti3
%{_colordir}/target/NPES/TR005.ti3
%{_colordir}/target/NPES/TR006.ti3
%dir %{_colordir}/target/fogra
%{_colordir}/target/fogra/FOGRA28L.ti3
%{_colordir}/target/fogra/FOGRA29L.ti3
%{_colordir}/target/fogra/FOGRA30L.ti3
%{_colordir}/target/fogra/FOGRA39L.ti3
%{_colordir}/target/fogra/FOGRA40L.ti3
%{_datadir}/icons/application-vnd.iccprofile.png
%{_datadir}/icons/text-vnd.cgats.png
%{_datadir}/mime/packages/x-color-cgats.xml
%exclude %{_datadir}/mime/packages/x-color-icc.xml
%{_datadir}/pixmaps/application-vnd.iccprofile.png
%{_datadir}/pixmaps/%{name}_logo.png
%{_datadir}/pixmaps/text-vnd.cgats.png


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.1-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.1-13
- Remove obsolete scriptlets

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 08 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.1-8
- update mime scriptlet

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 28 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.3.1-6
- reported by Kai-Uwe Behrmann <oy@oyraos.org> rhbz#1071180
  omit x-color-icc.xml, as it is already in shared-mime-info

* Tue Oct 08 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.3.1-5
- Fix license tag to zlib - rhbz#982952
- Spec file clean-up

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.3.1-1
- Update to 1.3.1

* Sat Jan 21 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.3.0-1.1
- Drop wrong obsoletes

* Sat Aug 20 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.3.0-1
- Rename to icc-profiles-openicc
- Add scriptlet for icons directory
- Use absolute path for update-mime-database
- Drop README
- Add directory ownership

* Thu Jul 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Tue Jan 25 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-1
- Update to 1.1.0

* Fri Jan 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.1-1
- Spec file rewrite

* Mon Dec 27 2010 - Kai-Uwe Behrmann <ku.b at gmx.de>
- split out a directory package from the mime types

* Fri Aug 28 2010 - Kai-Uwe Behrmann <ku.b at gmx.de>
- new package naming scheme for Oyranos independent installations
