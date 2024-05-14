Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global source_name	usb-modeswitch-data

Name:		usb_modeswitch-data
Version:	20191128
Release:	3%{?dist}
Summary:	USB Modeswitch gets mobile broadband cards in operational mode
Summary(de):	USB Modeswitch aktiviert UMTS-Karten
License:	GPLv2+
URL:		https://www.draisberghof.de/usb_modeswitch/
Source0:	https://www.draisberghof.de/usb_modeswitch/%{source_name}-%{version}.tar.bz2
BuildArch:	noarch
BuildRequires:	systemd
Requires:	systemd
Requires:	usb_modeswitch >= 2.4.0


%description
USB Modeswitch brings up your datacard into operational mode. When plugged
in they identify themselves as cdrom and present some non-Linux compatible
installation files. This tool deactivates this cdrom-devices and enables
the real communication device. It supports most devices built and
sold by Huawei, T-Mobile, Vodafone, Option, ZTE, Novatel.

This package contains the data files needed for usb_modeswitch to function.

%description	-l de
USB Modeswitch deaktiviert die CDROM-Emulation einiger UMTS-Karten.
Dadurch erkennt Linux die Datenkarte und kann damit Internet-
Verbindungen aufbauen. Die gängigen Karten von Huawei, T-Mobile,
Vodafone, Option, ZTE und Novatell werden unterstützt.

Dieses Paket enthält die Dateien für usb_modeswitch benötigt 
um zu funktionieren.


%prep
%setup -q -n %{source_name}-%{version}

%build

%install
make install \
	DESTDIR=$RPM_BUILD_ROOT \
	RULESDIR=$RPM_BUILD_ROOT%{_udevrulesdir}

%post 
%udev_rules_update

%postun
%udev_rules_update

%files
%{_udevrulesdir}/40-usb_modeswitch.rules
%{_datadir}/usb_modeswitch
%license COPYING
%doc ChangeLog README REFERENCE

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20191128-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20191128-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 29 2019 Lubomir Rintel <lkundrak@v3.sk> - 20191128-1
- Update to a new release

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20170806-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20170806-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170806-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170806-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 18 2017 Lubomir Rintel <lkundrak@v3.sk> - 20170806-1
- Update to a new release

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160803-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160803-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 21 2016 Lubomir Rintel <lkundrak@v3.sk> - 20160803-1
- Update to a new release

* Thu Jul 21 2016 Lubomir Rintel <lkundrak@v3.sk> - 20160612-3
- Bump the release number to be higher than in Fedora 24

* Thu Jul 21 2016 Lubomir Rintel <lkundrak@v3.sk> - 20160612-2
- Install the rules into proper location

* Wed Jun 22 2016 Lubomir Rintel <lkundrak@v3.sk> - 20160612-1
- Update to a new release

* Tue May 03 2016 Lubomir Rintel <lkundrak@v3.sk> - 20160112-1
- Update to a new release

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20151101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 02 2015 Huzaifa Sidhpurwala <huzaifas@redhat.com> 20151101-1
- New upstream release

* Tue Aug 18 2015 Lubomir Rintel <lkundrak@v3.sk> - 20150627-1
- Update to a new release

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20150115-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 Till Maas <opensource@till.name> - 20150115-1
- Update to new release
- Use %%license

* Mon Dec 01 2014 poma <poma@gmail.com> 20140529-2
- Add missed REFERENCE file as complement to device_reference.txt from the base package
- Refer to proper usb_modeswitch version

* Mon Nov 24 2014 Till Maas <opensource@till.name> - 20140529-1
- New upstream release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140327-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> 20140327-1
- New upstream release

* Fri Nov 22 2013 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 20131113-1
- New upstream release

* Mon Aug 26 2013 Dan Williams <dcbw@redhat.com> - 20130807-1
- Fix udev rules path

* Fri Aug 16 2013 Dan Williams <dcbw@redhat.com> - 20130807-1
- New upstream release

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130610-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 12 2013 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 20130610-1
- New upstream release

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20121109-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 20121109-1
- New upstream release. Resolves rhbz#875833

* Fri Aug 24 2012 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 20120815-1
- New upstream release. Resolves rhbz#847681

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120531-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 Dan Williams <dcbw@redhat.com> 20120531-1
- New upstream data release
- Handle failure of udevadm control --reload-rules (rh #824849)

* Tue Apr 24 2012 Dan Williams <dcbw@redhat.com> 20120120-1
- New upstream release.
- Remove dep on TCL since nothing in the package requires it

* Tue Oct 25 2011 Huzaifa Sidhpurwala <huzaifas@redhat.com> 20111023-1
- New upstream release.

* Mon Jul 25 2011 Huzaifa Sidhpurwala <huzaifas@redhat.com> 20110714-1
- New upstream release. Resolves rhbz#714648

* Mon Mar 28 2011 Rahul Sundaram <sundaram@fedoraproject.org> 20110227-1
- New upstream release.  Resolves rhbz#654800
- Update spec to match current guidelines
- Some spec file fixes from Alexander Todorov. Resolves rhbz#632559
- Drop patch

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20101222-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 Dan Williams <dcbw@redhat.com> 20101222-1
- New upstream

* Tue Aug 24 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> 20100817-1
- New upstream

* Thu Aug 12 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> 20100707-1
- New upstream

* Tue Jun 22 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> 20100621-1
- New upstream

* Tue Apr 20 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> 20100418-2
- Remove buildroot, make package noarch

* Tue Apr 20 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> 20100418-1
- First build
