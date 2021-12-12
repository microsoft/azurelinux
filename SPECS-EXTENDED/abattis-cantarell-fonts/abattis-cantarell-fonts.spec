Vendor:         Microsoft Corporation
Distribution:   Mariner
%global fontname cantarell
%global fontconf 31-%{fontname}.conf

Name: abattis-cantarell-fonts
Version: 0.201
Release: 3%{?dist}
Summary: Humanist sans serif font

License: OFL
URL: https://git.gnome.org/browse/cantarell-fonts/
Source0: http://download.gnome.org/sources/cantarell-fonts/0.201/cantarell-fonts-%{version}.tar.xz
Source1: cantarell-fontconfig.conf

BuildArch: noarch

BuildRequires: fontpackages-devel
BuildRequires: gettext
BuildRequires: libappstream-glib-devel
BuildRequires: meson

Requires: fontpackages-filesystem

%description
The Cantarell font family is a contemporary Humanist sans serif
designed for on-screen reading. The fonts were originally designed
by Dave Crossland.

%prep
%autosetup -n cantarell-fonts-%{version}

%build
%meson
%meson_build

%install
%meson_install

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf}

%check
appstream-util validate-relax --nonet \
        %{buildroot}%{_datadir}/metainfo/org.gnome.cantarell.metainfo.xml

%_font_pkg -f %{fontconf} *.otf
%license COPYING
%doc NEWS README.md
%{_datadir}/metainfo/org.gnome.cantarell.metainfo.xml

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.201-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.201-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Kalev Lember <klember@redhat.com> - 0.201-1
- Update to 0.201

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.111-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.111-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 0.111-1
- Update to 0.111

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 15 2018 Kalev Lember <klember@redhat.com> - 0.101-1
- Update to 0.101

* Wed Mar 14 2018 Kalev Lember <klember@redhat.com> - 0.100-1
- Update to 0.100
- Switch to the meson build system
- Use upstream appdata
- Validate appdata file
- Include fontconfig file in packaging as it's no longer included upstream
- Update package summary and description from appdata
- Many thanks to Parag Nemade <pnemade@fedoraproject.org> for the help
  with updating the package!

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 19 2016 Kalev Lember <klember@redhat.com> - 0.0.25-1
- Update to 0.0.25

* Tue Mar 01 2016 Richard Hughes <rhughes@redhat.com> - 0.0.24-1
- Update to 0.0.24

* Fri Feb 26 2016 Adam Williamson <awilliam@redhat.com> - 0.0.23-1
- Update to 0.0.23

* Wed Feb 17 2016 Richard Hughes <rhughes@redhat.com> - 0.0.22-1
- Update to 0.0.22

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Kalev Lember <klember@redhat.com> - 0.0.21-1
- Update to 0.0.21

* Mon Jan 11 2016 Kalev Lember <klember@redhat.com> - 0.0.20.1-1
- Update to 0.0.20.1

* Mon Nov 02 2015 Kalev Lember <klember@redhat.com> - 0.0.18-1
- Update to 0.0.18

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 0.0.17.2-1
- Update to 0.0.17.2

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 0.0.17.1-1
- Update to 0.0.17.1

* Mon Oct 05 2015 Kalev Lember <klember@redhat.com> - 0.0.17-2
- s: provide anchors for accents

* Sun Oct 04 2015 Kalev Lember <klember@redhat.com> - 0.0.17-1
- Update to 0.0.17

* Tue Sep 08 2015 Kalev Lember <klember@redhat.com> - 0.0.16-4
- Fix 'r' hinting
- Use upstream build system rules when regenerating otf files
- Use license macro

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Nov 17 2014 Pravin Satpute <psatpute@redhat.com> - 0.0.16-2
- Added metainfo for gnome-software.

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 0.0.16-1
- Update to 0.0.16

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep 25 2013 Richard Hughes <rhughes@redhat.com> - 0.0.15-1
- Update to 0.0.15

* Fri Aug 23 2013 Kalev Lember <kalevlember@gmail.com> - 0.0.14-1
- Update to 0.0.14

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.0.13-1
- Update to 0.0.13

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 0.0.12-1
- Update to 0.0.12

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 0.0.11-1
- Update to 0.0.11

* Tue Sep 25 2012 Cosimo Cecchi <cosimoc@redhat.com> - 0.0.10.1-1
- Update to 0.0.10.1

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 0.0.10-1
- Update to 0.0.10

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard Hughes <hughsient@gmail.com> - 0.0.9-1
- Update to 0.0.9

* Wed Mar 28 2012 Richard Hughes <hughsient@gmail.com> - 0.0.8-1
- Update to 0.0.8

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 0.0.7-1
- Update to 0.0.7

* Fri Oct 07 2011 Matěj Cepl <mcepl@redhat.com> - 0.0.6-2
- Making the build EL-6 compatible.

* Wed Jul 6 2011 Matthias Clasen <mclasen@redhat.com> - 0.0.6-1
- Update to 0.0.6

* Mon Feb 21 2011 Cosimo Cecchi <cosimoc@redhat.com> - 0.0.3-1
- Update to 0.0.3

* Fri Feb 18 2011 Cosimo Cecchi <cosimoc@redhat.com> - 0.0.1-4
- Include upstream patch for the fontconfig snippet

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  8 2011 Stephen Smoogen <ssmoogen@redhat.com> - 0.0.1-2
- Fixed to meet review standards

* Tue Feb  8 2011 Cosimo Cecchi <cosimoc@redhat.com> - 0.0.1-1
- Initial packaging of abattis-cantarell-fonts

