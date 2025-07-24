Summary:        A library for managing OS information for virtualization
Name:           libosinfo
Version:        1.11.0
Release:        2%{?dist}
License:        LGPL-2.1-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://libosinfo.org/
Source:         https://releases.pagure.org/libosinfo/%{name}-1.11.0.tar.xz
BuildRequires:  %{_bindir}/pod2man
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  git
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  hwdata
BuildRequires:  libsoup-devel
BuildRequires:  libxml2-devel >= 2.6.0
BuildRequires:  libxslt-devel >= 1.0.0
BuildRequires:  meson
BuildRequires:  osinfo-db
BuildRequires:  vala
BuildRequires:  perl-podlators
Requires:       hwdata
Requires:       osinfo-db
Requires:       osinfo-db-tools

%description
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.

%package devel
Summary:        Libraries, includes, etc. to compile with the libosinfo library
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel
Requires:       pkgconfig
Provides:       libosinfo-vala = %{version}-%{release}

%description devel
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.

Libraries, includes, etc. to compile with the libosinfo library

%prep
%autosetup -S git

%build
%meson \
    -Denable-gtk-doc=false \
    -Denable-tests=true \
    -Denable-introspection=enabled \
    -Denable-vala=enabled
%meson_build


%install
%meson_install

%find_lang %{name}

%check
%meson_test

%ldconfig_scriptlets

%files -f %{name}.lang
%license COPYING.LIB
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/osinfo-detect
%{_bindir}/osinfo-query
%{_bindir}/osinfo-install-script
%{_mandir}/man1/osinfo-detect.1*
%{_mandir}/man1/osinfo-query.1*
%{_mandir}/man1/osinfo-install-script.1*
%{_libdir}/%{name}-1.0.so.*
%{_libdir}/girepository-1.0/Libosinfo-1.0.typelib

%files devel
%{_libdir}/%{name}-1.0.so
%dir %{_includedir}/%{name}-1.0/
%dir %{_includedir}/%{name}-1.0/osinfo/
%{_includedir}/%{name}-1.0/osinfo/*.h
%{_libdir}/pkgconfig/%{name}-1.0.pc
%{_datadir}/gir-1.0/Libosinfo-1.0.gir

%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libosinfo-1.0.deps
%{_datadir}/vala/vapi/libosinfo-1.0.vapi

%changelog
* Wed Dec 28 2022 Muhammad Falak <mwani@microsoft.com> - 1.10.0-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified

* Mon Feb 14 2022 Victor Toso <victortoso@redhat.com> - 1.10.0-1
- Update to 1.10.0 release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Cole Robinson <crobinso@redhat.com> - 1.9.0-3
- Fix build with glib 2.70

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 Fabiano Fidêncio <fidencio@redhat.com> - 1.9.0-1
- Update to 1.9.0 release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 30 2020 Fabiano Fidêncio <fidencio@redhat.com> - 1.8.0-1
- Update to 1.8.0 release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Fabiano Fidêncio <fidencio@redhat.com> - 1.7.1-2
- Fix OsinfoList ABI breakage

* Wed Dec 04 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.7.1-1
- Update to 1.7.1 release

* Fri Nov 29 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.7.0-1
- Update to 1.7.0 release

* Fri Nov 08 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.6.0-2
- Improve ISO detection mechanism

* Fri Jul 26 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.6.0-1
- Update to 1.6.0 release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.5.0-3
- rhbz#1727767 - CVE-2019-13313 libosinfo: osinfo-install-script
                 option leaks password via command line argument

* Mon Jun 03 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.5.0-2
- Fix coverity issues

* Thu May 09 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.5.0-1
- Update to 1.5.0 release

* Thu Apr 11 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.4.0-3
- rhbz#1698845: Require GVFS

* Wed Apr 10 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.4.0-2
- Fix usage of application ID
- Fix images' load
- Remove tests depending on osinfo-db

* Fri Mar 01 2019 Fabiano Fidêncio <fidencio@redhat.com> 1.4.0-1
- Update to 1.4.0 release

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 1.3.0-3
- Use standard vala packaging pattern where vapi files are in -devel

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Daniel P. Berrangé <berrange@redhat.com> - 1.3.0-1
- Update to 1.3.0 release

* Thu Oct 11 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 1.2.0-5
- Do not force anchored patterns on libosinfo, leave it for osinfo-db

* Thu Sep 20 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 1.2.0-4
- Require osinfo-db >= 20180920-1

* Thu Sep 20 2018 Fabiano Fidêncio <fabiano@fidencio.org> - 1.2.0-3
- Force anchored patterns when matching regex

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 20 2018 Daniel P. Berrangé <berrange@redhat.com> - 1.2.0-1
- Update to 1.2.0 release

* Tue Feb 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.0-2
- Switch to %%ldconfig_scriptlets

* Tue Aug 15 2017 Daniel P. Berrange <berrange@redhat.com> 1.1.0-1
- New upstream release 1.1.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct  7 2016 Daniel P. Berrange <berrange@redhat.com> 1.0.0-1
- New upstream release 1.0.0

* Fri Jul  1 2016 Daniel P. Berrange <berrange@redhat.com> 0.3.1-1
- New upstream release 0.3.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan  8 2016 Zeeshan Ali <zeenix@redhat.com> 0.3.0-1
- New upstream release 0.3.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Zeeshan Ali <zeenix@redhat.com> 0.2.12-1
- New upstream release 0.2.12

* Mon Sep 22 2014 Cole Robinson <crobinso@redhat.com> - 0.2.11-2
- os: Add Fedora 21

* Tue Aug 26 2014 Christophe Fergeau <cfergeau@redhat.com> 0.2.11-1
- New upstream release 0.2.11

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.2.9-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 18 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.2.9-1
- New upstream release 0.2.9

* Thu Nov 28 2013 Zeeshan Ali <zeenix@redhat.com> - 0.2.8-1
- New upstream release 0.2.8

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Zeeshan Ali <zeenix@redhat.com> - 0.2.7-1
- New upstream release 0.2.7

* Thu Mar 21 2013 Zeeshan Ali <zeenix@redhat.com> - 0.2.6-1
- New upstream release 0.2.6

* Wed Mar 06 2013 Christophe Fergeau <cfergeau@redhat.com> - 0.2.5-2
- BuildRequires /usr/bin/pod2man as this will automatically pick the right
  package rather than conditionally requiring a package that is only
  available in f19+
- Do not Requires: udev when building libosinfo without its udev rule
  (which is done on f19+)

* Tue Mar 05 2013 Christophe Fergeau <cfergeau@redhat.com> 0.2.5-1
- New upstream release 0.2.5
- Disable udev rule as it's no longer required with newer
  systemd/util-linux

* Tue Feb 12 2013 Cole Robinson <crobinso@redhat.com> - 0.2.3-2
- Fix osinfo-detect crash with non-bootable media (bz #901910)

* Mon Jan 14 2013 Zeeshan Ali <zeenix@redhat.com> - 0.2.3-1
- New upstream release 0.2.3

* Thu Dec 20 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.2.2-1
- New upstream release 0.2.2

* Fri Oct 12 2012 Zeeshan Ali <zeenix@redhat.com> - 0.2.1-1
- Fix and simplify udev rule.
- Fedora:
  - Fix minimum RAM requirements for F16 and F17.
- Add data on:
  - Fedora 18
  - GNOME 3.6
  - Ubuntu 12.10
- Fixes to doc build.
- Install script:
  - Add get_config_param method.
  - Differenciate between expected/output script names.
  - Add more utility functions.
- Add 'installer-reboots' parameter to medias.
- osinfo-detect does not die of DB loading errors anymore.
- More type-specific entity value getters/setters.
- Fixe and update RNG file.
- Add 'subsystem' property/attribute to devices.

* Mon Sep 03 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.2.0-1
- Update to 0.2.0 release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Zeeshan Ali <zeenix@redhat.com> - 0.1.2-1
- Update to 0.1.2 release.

* Thu Apr 12 2012 Zeeshan Ali <zeenix@redhat.com> - 0.1.1-1
- Update to 0.1.1 release.

* Wed Mar 14 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-2
- Remove obsolete perl based scripts (rhbz #803086)

* Wed Feb 08 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.1.0-1
- Update to 0.1.0 release

* Tue Jan  17 2012 Zeeshan Ali <zeenix@redhat.com> - 0.0.5-1
- Update to 0.0.5 release

* Tue Jan  3 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.4-2
- Remove pointless gir conditionals

* Wed Dec 21 2011 Daniel P. Berrange <berrange@redhat.com> - 0.0.4-1
- Update to 0.0.4 release

* Thu Nov 24 2011 Daniel P. Berrange <berrange@redhat.com> - 0.0.2-1
- Initial package
