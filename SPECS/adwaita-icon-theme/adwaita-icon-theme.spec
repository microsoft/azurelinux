# Set boostrap to 1 for initial bootstrapping when gtk3 is not yet built
%global bootstrap 1
%define majmin %(echo %{version} | cut -d. -f1-2)
Summary:        Adwaita icon theme
Name:           adwaita-icon-theme
Version:        3.36.1
Release:        2%{?dist}
License:        LGPLv3+ or CC-BY-SA
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.gnome.org
Source0:        https://download.gnome.org/sources/adwaita-icon-theme/%{majmin}/%{name}-%{version}.tar.xz
BuildRequires:  intltool
BuildRequires:  librsvg2
Requires:       adwaita-cursor-theme = %{version}-%{release}
BuildArch:      noarch
%if ! 0%{bootstrap}
BuildRequires:  %{_bindir}/gtk-encode-symbolic-svg
%endif

%description
This package contains the Adwaita icon theme used by the GNOME desktop.

%package -n     adwaita-cursor-theme
Summary:        Adwaita cursor theme

%description -n adwaita-cursor-theme
The adwaita-cursor-theme package contains a modern set of cursors originally
designed for the GNOME desktop.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains the pkgconfig file for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

touch %{buildroot}%{_datadir}/icons/Adwaita/icon-theme.cache

%transfiletriggerin -- %{_datadir}/icons/Adwaita
gtk-update-icon-cache --force %{_datadir}/icons/Adwaita &>/dev/null || :

%transfiletriggerpostun -- %{_datadir}/icons/Adwaita
gtk-update-icon-cache --force %{_datadir}/icons/Adwaita &>/dev/null || :

%files
%license COPYING*
%dir %{_datadir}/icons/Adwaita/
%{_datadir}/icons/Adwaita/8x8/
%{_datadir}/icons/Adwaita/16x16/
%{_datadir}/icons/Adwaita/22x22/
%{_datadir}/icons/Adwaita/24x24/
%{_datadir}/icons/Adwaita/32x32/
%{_datadir}/icons/Adwaita/48x48/
%if ! 0%{bootstrap}
%{_datadir}/icons/Adwaita/64x64/
%{_datadir}/icons/Adwaita/96x96/
%endif
%{_datadir}/icons/Adwaita/256x256/
%{_datadir}/icons/Adwaita/512x512/
%{_datadir}/icons/Adwaita/scalable/
%{_datadir}/icons/Adwaita/scalable-up-to-32/
%{_datadir}/icons/Adwaita/index.theme
%ghost %{_datadir}/icons/Adwaita/icon-theme.cache

%files -n adwaita-cursor-theme
%license COPYING*
%dir %{_datadir}/icons/Adwaita/
%{_datadir}/icons/Adwaita/cursors/

%files devel
%{_datadir}/pkgconfig/adwaita-icon-theme.pc

%changelog
* Wed May 26 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.36.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Turn on bootstrapping to avoid build cycle with gtk3
- License verified

* Mon Apr 20 2020 Kalev Lember <klember@redhat.com> - 3.36.1-1
- Update to 3.36.1

* Sun Mar 08 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Mon Mar 02 2020 Kalev Lember <klember@redhat.com> - 3.35.92-1
- Update to 3.35.92

* Mon Feb 17 2020 Kalev Lember <klember@redhat.com> - 3.35.91-1
- Update to 3.35.91

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.34.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 08 2019 Kalev Lember <klember@redhat.com> - 3.34.3-1
- Update to 3.34.3

* Wed Nov 06 2019 Kalev Lember <klember@redhat.com> - 3.34.1-2
- Backport a fix to make folder-documents icon visible again

* Tue Nov 05 2019 Kalev Lember <klember@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Thu Sep 12 2019 Kalev Lember <klember@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Fri Sep 06 2019 Kalev Lember <klember@redhat.com> - 3.33.92-1
- Update to 3.33.92

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 18 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 3.31.91-1
- Update to 3.31.91

* Fri Feb 08 2019 Kalev Lember <klember@redhat.com> - 3.31.1-3.git03eae76
- Update to today's git snapshot

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Kalev Lember <klember@redhat.com> - 3.31.1-1
- Update to 3.31.1

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Mon Aug 13 2018 Kalev Lember <klember@redhat.com> - 3.29.90-1
- Update to 3.29.90

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 14 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Mon Mar 05 2018 Kalev Lember <klember@redhat.com> - 3.27.90-1
- Update to 3.27.90

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 01 2017 Kalev Lember <klember@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Thu Sep 14 2017 Kalev Lember <klember@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Fri Aug 25 2017 Kalev Lember <klember@redhat.com> - 3.25.91-1
- Update to 3.25.91

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Kalev Lember <klember@redhat.com> - 3.25.4-1
- Update to 3.25.4

* Thu Jun 22 2017 Kalev Lember <klember@redhat.com> - 3.24.0-2
- Add file triggers for gtk-update-icon-cache

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Thu Mar 02 2017 David King <amigadave@amigadave.com> - 3.23.91.1-1
- Update to 3.23.91.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 David King <amigadave@amigadave.com> - 3.23.91-1
- Update to 3.23.91
- Use make_build macro

* Wed Sep 21 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Fri Sep 02 2016 Kalev Lember <klember@redhat.com> - 3.21.91-1
- Update to 3.21.91

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 3.21.2-1
- Update to 3.21.2

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20-1
- Update to 3.20

* Fri Mar 04 2016 Kalev Lember <klember@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Mon Feb 29 2016 Richard Hughes <rhughes@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Tue Jul 28 2015 Kalev Lember <klember@redhat.com> - 3.17.4-1
- Update to 3.17.4

* Tue Jun 30 2015 Kalev Lember <klember@redhat.com> - 3.17.3-1
- Update to 3.17.3

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2.1-1
- Update to 3.16.2.1
- Use license macro for COPYING files

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Fri Mar 20 2015 MAtthias Clasen <mclasen@redhat.com> - 3.15.92-1
- Update to 3.15.92

* Tue Mar 03 2015 Rex Dieter <rdieter@fedoraproject.org> 3.15.90-2
- own %%{_datadir}/icons/Adwaita/

* Fri Feb 13 2015 Richard Hughes <rhughes@redhat.com> - 3.15.90-1
- Update to 3.15.90

* Thu Oct 30 2014 Richard Hughes <rhughes@redhat.com> - 3.15.1-1
- Update to 3.15.1

* Tue Oct 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-3
- Split out adwaita-cursor-theme subpackage for alternate desktop spins
  (#1157324)

* Tue Oct 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-2
- Add bootstrap toggle for initial boostrapping when gtk3 is not yet built

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Tue Sep 02 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.91-1
- Update to 3.13.91

* Sun Aug 17 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.5-1
- Update to 3.13.5

* Mon Jul 14 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-1
- Update to 3.13.4

* Thu Jun 26 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-1
- Update to 3.13.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-1
- Update to 3.13.2

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-2
- Replace adwaita-cursor-theme subpackage from gnome-themes-standard

* Mon Apr 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-1
- Initial Fedora packaging
