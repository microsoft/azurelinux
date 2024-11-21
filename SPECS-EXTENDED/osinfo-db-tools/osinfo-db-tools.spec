Summary:        Tools for managing the osinfo database
Name:           osinfo-db-tools
Version:        1.10.0
Release:        2%{?dist}
License:        GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://libosinfo.org/
Source:         https://releases.pagure.org/libosinfo/%{name}-1.10.0.tar.xz
BuildRequires:  %{_bindir}/pod2man
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  git
BuildRequires:  glib2-devel
BuildRequires:  json-glib-devel
BuildRequires:  libarchive-devel
BuildRequires:  libsoup-devel
BuildRequires:  libxml2-devel >= 2.6.0
BuildRequires:  libxslt-devel >= 1.0.0
BuildRequires:  meson
BuildRequires:  python3
BuildRequires:  python3-pytest
BuildRequires:  python3-requests

%description
This package provides tools for managing the osinfo database of
information about operating systems for use with virtualization

%prep
%autosetup -S git

%build
%meson
%meson_build

%check
%meson_test

%install
%meson_install

%find_lang %{name}

%files -f %{name}.lang
%doc NEWS README
%license COPYING
%{_bindir}/osinfo-db-export
%{_bindir}/osinfo-db-import
%{_bindir}/osinfo-db-path
%{_bindir}/osinfo-db-validate
%{_mandir}/man1/osinfo-db-export.1*
%{_mandir}/man1/osinfo-db-import.1*
%{_mandir}/man1/osinfo-db-path.1*
%{_mandir}/man1/osinfo-db-validate.1*

%changelog
* Wed Dec 28 2022 Muhammad Falak <mwani@microsoft.com> - 1.10.0-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified

* Mon Feb 14 2022 Victor Toso <victortoso@redhat.com> - 1.10.0-1
- Update to 1.10.0 release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 Fabiano Fidêncio <fidencio@redhat.com> - 1.9.0-1
- Update to 1.9.0 release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 30 2020 Fabiano Fidêncio <fidencio@redhat.com> - 1.8.0-1
- Update to 1.8.0 release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 29 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.7.0-1
- Update to 1.7.0 release

* Fri Jul 26 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.6.0-1
- Update to 1.6.0 release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 03 2019 Fabiano Fidêncio <fidencio@redhat.com> -1.5.0-2
- Fix coverity issues

* Thu May 09 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.5.0-1
- Update to 1.5.0 release

* Thu Apr 11 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.4.0-2
- rhbz#1698845: Require GVFS

* Fri Mar 01 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.4.0-1
- Update to 1.4.0 release

* Fri Feb 01 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.3.0-1
- Update to 1.3.0 release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 20 2018 Daniel P. Berrangé <berrange@redhat.com> - 1.2.0-1
- Update to 1.2.0 release

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 26 2016 Daniel P. Berrange <berrange@redhat.com> - 1.1.0-1
- Update to 1.1.0 release

* Fri Jul 29 2016 Daniel P. Berrange <berrange@redhat.com> - 1.0.0-1
- Initial package after split from libosinfo (rhbz #1361594)
