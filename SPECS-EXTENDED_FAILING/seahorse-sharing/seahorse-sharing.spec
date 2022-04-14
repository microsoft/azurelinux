Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           seahorse-sharing
Version:        3.8.0
Release:        21%{?dist}
Summary:        Sharing of PGP public keys via DNS-SD and HKP
# daemon is GPLv2+
# libegg is LGPLv2+
License:        GPLv2+ and LGPLv2+
URL:            https://live.gnome.org/Seahorse
Source0:        http://ftp.gnome.org/pub/gnome/sources/seahorse-sharing/3.8/%{name}-%{version}.tar.xz

Provides:       bundled(egglib)

BuildRequires:  gcc
BuildRequires:  perl(File::Find)
BuildRequires:  gtk3-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gnupg2
BuildRequires:  gpgme-devel >= 1.0
BuildRequires:  libsoup-devel
BuildRequires:  pkgconfig(avahi-client) pkgconfig(avahi-glib)
BuildRequires:  intltool
BuildRequires:  libSM-devel

Obsoletes: seahorse < 3.1.4

%description
This package ships a session daemon that allows users to share PGP public keys
via DNS-SD and HKP.


%prep
%setup -q
# Hack around gnupg2 version requirement
sed -i "s:1.2 1.4 2.0:1.2 1.4 2.0 2.2:" configure


%build
%configure
make %{?_smp_mflags}


%install
%make_install

desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/%{name}.desktop

%find_lang %{name} --with-gnome


%files -f %{name}.lang
%license COPYING
%doc AUTHORS NEWS README
%{_sysconfdir}/xdg/autostart/%{name}.desktop
%{_bindir}/%{name}
%{_datadir}/pixmaps/seahorse/
%{_mandir}/man1/%{name}.1.gz


%changelog
* Wed Feb 16 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.8.0-21
- License verified.

* Tue Feb 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.8.0-20
- Adding missing BRs on Perl modules.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.8.0-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Karsten Hopp <karsten@redhat.com> - 3.8.0-13
- update gnugpg2 version

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.8.0-9
- Rebuild for gpgme 1.18

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 01 2015 Kalev Lember <klember@redhat.com> - 3.8.0-7
- Fix the build with gnupg2 2.1.x
- Use make_install macro
- Use license macro for COPYING

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 26 2013 Rex Dieter <rdieter@fedoraproject.org> 3.8.0-3
- add explicit avahi build deps

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.5-1
- Update to 3.7.5

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Wed Sep 26 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Rui Matos <rmatos@redhat.com> - 3.4.0-1
- Update to 3.4.0
- Added Provides: bundled(egglib)

* Mon Mar 19 2012 Rui Matos <rmatos@redhat.com> - 3.3.92-1
- Update to 3.3.92
- Don't ship MAINTAINERS
- Own %%{_datadir}/pixmaps/seahorse/

* Tue Mar  6 2012 Rui Matos <rmatos@redhat.com> - 3.2.1-1
- initial packaging for Fedora

