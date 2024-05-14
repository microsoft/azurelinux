Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           media-player-info
Version:        23
Release:        7%{?dist}
Summary:        Data files describing media player capabilities

License:        BSD
URL:            https://www.freedesktop.org/wiki/Software/media-player-info
Source0:        https://www.freedesktop.org/software/media-player-info/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  pkgconfig(udev)
BuildRequires:  python3
Requires:       udev

%description
media-player-info is a repository of data files describing media player
(mostly USB Mass Storage ones) capabilities. These files contain information
about the directory layout to use to add music to these devices, about the
supported file formats, etc.

The package also installs a udev rule to identify media player devices.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
%make_install


%files
%license COPYING
%doc README NEWS AUTHORS
/usr/share/media-player-info
/usr/lib/udev/rules.d/*
/usr/lib/udev/hwdb.d/20-usb-media-players.hwdb


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 23-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 19 2017 Bastien Nocera <bnocera@redhat.com> - 23-1
+ media-player-info-23-1
- Update to 23

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Aug 22 2015 Kalev Lember <klember@redhat.com> - 22-1
- Update to 22

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Sep  4 2014 Matthias Clasen <mclasen@redhat.com> - 21-1
- Update to 21

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Dan Williams <dcbw@redhat.com> 17-2
- Add HP Veer (fdo #51097)

* Sun Aug 12 2012 Rex Dieter <rdieter@fedoraproject.org> 17-1
- Update to 17

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> 16-1
- Update to 16

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> 15-1
- Update to 15

* Wed Jul 20 2011 Matthias Clasen <mclasen@redhat.com> 14-1
- Update to 14

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> 12-1
- Update to version 12

* Fri Nov 12 2010 Matthias Clasen <mclasen@redhat.com> 11-1
- Update to version 11

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> 10-1
- Update to version 10

* Thu Apr 08 2010 Bastien Nocera <bnocera@redhat.com> 6-1
- Update to version 6

* Thu Mar 18 2010 Bastien Nocera <bnocera@redhat.com> 5-1
- Update to version 5

* Tue Sep  1 2009 Matthias Clasen <mclasen@redhat.com> - 3-1
- New upstream tarball with fixed Copyright headers

* Sat Aug 29 2009 Matthias Clasen <mclasen@redhat.com> - 2-1
- Rename to media-player-info

* Thu Aug 27 2009 Matthias Clasen <mclasen@redhat.com> - 1-1
- Initial packaging
