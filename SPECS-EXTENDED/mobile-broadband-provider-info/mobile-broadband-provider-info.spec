Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: Mobile broadband provider database
Name: mobile-broadband-provider-info
Version: 20190618
Release: 4%{?dist}
URL: https://wiki.gnome.org/Projects/NetworkManager/MobileBroadband/ServiceProviders
License: Public Domain
Source: https://download.gnome.org/sources/%{name}/%{version}/%{name}-%{version}.tar.xz

BuildArch: noarch
BuildRequires: /usr/bin/xmllint
BuildRequires: /usr/bin/xsltproc

%description
The mobile-broadband-provider-info package contains listings of mobile
broadband (3G) providers and associated network and plan information.


%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains files necessary for
developing developing applications that use %{name}.


%prep
%autosetup


%build
%configure
%make_build


%check
make check


%install
%make_install


%files
%{_datadir}/%{name}
%doc README
%license COPYING

	
%files devel
%{_datadir}/pkgconfig/%{name}.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20190618-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190618-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190618-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 18 2019 Lubomir Rintel <lkundrak@v3.sk> - 20190618-1
- Update to latest upstream release
- Use correct upstream version number
- SPEC file cleanup

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20170310-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20170310-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 10 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.20170310-1
- Update to latest upstream snapshot 20170310
- Spec cleanups, use %%license

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20170105git-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20170105git-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20170105git-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan  5 2017 Jiří Klimeš <blueowl@centrum.cz> - 1.20170105git-1
- Update to latest upstream git snapshot 20170105git

* Wed Feb  3 2016 Jiří Klimeš <blueowl@centrum.cz> - 1.20151214-1
- Update to latest upstream release 20151214

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20150421git-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 21 2015 Jiří Klimeš <jklimes@redhat.com> - 1.20150421git-1
- Update to latest upstream git snapshot 20150421git

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120614-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120614-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120614-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20120614-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Jiří Klimeš <jklimes@redhat.com> - 1.20120614-1
- Update to latest upstream release 20120614

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20110218-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Feb 18 2011 Matěj Cepl <mcepl@redhat.com> - 1.20110218-1
- Update to latest upstream checkout including:
	* south africa: add 8.ta (Telkom) provider (bgo #641916),
	  remove username for Cell-C (bgo #640794)
	* switzerland: update Orange plans and APNs (bgo #638115)
	* tanzania: add Sasatel and TTCL, add CDMA for Zantel (bgo #634609)
	* india: new unified BSNL APNs (rh #667280)
	* ec: add Movistar Ecuador (bgo #638223)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20101231-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.20101231-2
- Own the %%{_datadir}/%%{name} dir.
- Remove duplicate "make check".

* Fri Dec 31 2010 Matěj Cepl <mcepl@redhat.com> - 1.20101231-1
- Update to latest upstream checkout including:
	Afghanistan, Argentina, Armenia, Australia, Austria, Bahrain, Canada,
	Croatia, Denmark, Dominican Republic, Finland, France, French Polynesia,
	Germany, Greece, Hong Kong, Hungary, China, Iceland, India, Indonesia,
	Iran, Israel, Israel, Italy, Latvia, Luxembourg, Mexico, Montenegro,
	Netherlands, New Zealand, Nicaragua, Norway, Paraguay, Philippines,
	Poland, Portugal, Romania, Rwanda/Burundi, Slovakia, Slovenia, Spain,
	Sudan, Sweden, Switzerland, Thailand, Tunisia, Uganda, United Arab
, 
* Fri Jan 22 2010 Dan Williams <dcbw@redhat.com> - 1.20100122-1
- Update to latest upstream release including:
- Cyprus, Austria, Ireland, Ukraine, Romainia, Cambodia (rh #530981), 
- Iraq, India, Sri Lanka, UK, Australia, Singapore,
- South Korea, Italy, United States, China (rh #517253), Nigeria,
- Tanzania, Germany, Qatar, Russia, and Finland (rh #528988)

* Fri Sep 18 2009 Dan Williams <dcbw@redhat.com> - 1.20090918-1
- Update to latest upstream release including:
- Algeria, Australia, Belarus, Belgium, Brazil
- Brunei, Bulgaria, Egypt, Finland, Ghana, Greece
- India, Italy, Kazakhstan, Korean CDMA operators
- Kuwait, Mali, Netherlands, Paraguay, Serbia
- Spain, Sweden, UK

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 1.20090707-3
- Add -devel sub-package with pkg-config file (#511318)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20090707-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 7 2009 Dan Williams <dcbw@redhat.com> - 1.20090707-1
- Update to latest upstream release including:
- T-Mobile USA
- Brazil
- Bangladesh
- Sweden
- Spain
- Moldova

* Wed Jun 3 2009 Dan Williams <dcbw@redhat.com> 0.20090602-2
- Package review fixes

* Tue Jun 2 2009 Dan Williams <dcbw@redhat.com> 0.20090602-1
- Initial version

