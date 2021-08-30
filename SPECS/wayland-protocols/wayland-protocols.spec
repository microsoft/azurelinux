Summary:        Wayland protocols that add functionality not available in the core protocol
Name:           wayland-protocols
Version:        1.20
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://wayland.freedesktop.org/
Source0:        https://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz

BuildRequires:  make
BuildRequires:  wayland-devel

BuildArch:      noarch

%description
wayland-protocols contains Wayland protocols that add functionality not
available in the Wayland core protocol. Such protocols either adds
completely new functionality, or extends the functionality of some other
protocol either in Wayland core, or some other protocol in
wayland-protocols.

%package devel
Summary:        Wayland protocols that add functionality not available in the core protocol

Provides:       pkgconfig(wayland-protocols) = %{version}-%{release}

%description devel
wayland-protocols contains Wayland protocols that add functionality not
available in the Wayland core protocol. Such protocols either adds
completely new functionality, or extends the functionality of some other
protocol either in Wayland core, or some other protocol in
wayland-protocols.

%prep
%autosetup

%build
%configure

%install
%make_install

%files devel
%license COPYING
%doc README.md
%{_datadir}/pkgconfig/%{name}.pc
%{_datadir}/%{name}/

%changelog
* Thu Dec 10 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- License verified.
- Added explicit "Provides" for "pkgconfig(*)".

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Feb 29 2020 Jonas Ådahl <jadahl@redhat.com> - 1.20-1
- Update to 1.20

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jul 29 2019 Olivier Fourdan <ofourdan@redhat.com> - 1.18-1
- Update to 1.18

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 21 2018 Kalev Lember <klember@redhat.com> - 1.17-1
- Update to 1.17

* Tue Jul 31 2018 Kalev Lember <klember@redhat.com> - 1.16-1
- Update to 1.16

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Adam Jackson <ajax@redhat.com> - 1.15-1
- Update to 1.15

* Tue May 08 2018 Kalev Lember <klember@redhat.com> - 1.14-1
- Update to 1.14

* Thu Feb 15 2018 Kalev Lember <klember@redhat.com> - 1.13-1
- Update to 1.13

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 07 2017 Kalev Lember <klember@redhat.com> - 1.12-1
- Update to 1.12

* Wed Nov 15 2017 Kalev Lember <klember@redhat.com> - 1.11-1
- Update to 1.11

* Mon Jul 31 2017 Kalev Lember <klember@redhat.com> - 1.10-1
- Update to 1.10

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Kalev Lember <klember@redhat.com> - 1.9-1
- Update to 1.9

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 16 2016 Kalev Lember <klember@redhat.com> - 1.7-1
- Update to 1.7

* Fri Aug 12 2016 Kalev Lember <klember@redhat.com> - 1.6-1
- Update to 1.6

* Tue Jul 26 2016 Kalev Lember <klember@redhat.com> - 1.5-1
- Update to 1.5

* Tue May 24 2016 Kalev Lember <klember@redhat.com> - 1.4-1
- Update to 1.4

* Mon Apr 11 2016 Kalev Lember <klember@redhat.com> - 1.3-1
- Update to 1.3

* Mon Mar 07 2016 Kalev Lember <klember@redhat.com> - 1.2-1
- Update to 1.2

* Thu Feb 18 2016 Kalev Lember <klember@redhat.com> - 1.1-1
- Update to 1.1

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 05 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0-2
- Fix description

* Thu Nov 26 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0-1
- Update to released 1.0
- Move XMLs to devel pkg
- Drop non-interesting part of description

* Sun Nov 22 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.1.0-0.gitf828a43
- Initial package
