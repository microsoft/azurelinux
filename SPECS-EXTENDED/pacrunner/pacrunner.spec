Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		pacrunner
Version:	0.16
Release:	3%{?dist}
Summary:	Proxy configuration dæmon
License:	GPLv2
URL:		https://connman.net/

Source0:	https://www.kernel.org/pub/linux/network/connman/pacrunner-%{version}.tar.xz

BuildRequires:  gcc-c++
BuildRequires:  gcc
BuildRequires:	pkgconfig(glib-2.0) pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libcurl) pkgconfig(cunit)

Provides:       bundled(duktape) = 2.4.0

%description
PacRunner provides a dæmon for processing proxy configuration
and providing information to clients over D-Bus.

%prep
%setup -q
# The silly way the bundled duktape.c is generated confuses debuginfo
# generator
sed '/#line/d' -i duktape/duktape.c

%build
%configure --disable-libproxy --enable-debug --enable-duktape \
	   --enable-curl --enable-datafiles
make %{?_smp_mflags} V=99

%install
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/pacrunner
make install DESTDIR=$RPM_BUILD_ROOT testdir=%{_libexecdir}/pacrunner

%files
%license COPYING
%doc README AUTHORS ChangeLog
%{_sbindir}/pacrunner
%{_libexecdir}/pacrunner
%{_datadir}/dbus-1/system-services/org.pacrunner.service
%{_sysconfdir}/dbus-1/system.d/pacrunner.conf

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.16-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 30 2019 Lubomir Rintel <lkundrak@v3.sk> - 0.16-1
- Update to 0.16
- Mozjs has been dropped, switch to duktape
- Remove the python2 based test scripts

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 26 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.14-1
- Update to 0.14

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.11-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 26 2017 Peter Robinson <pbrobinson@fedoraproject.org> 0.11-1
- Update to 0.11

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.7-5
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 04 2013 David Woodhouse <David.Woodhouse@intel.com> - 0.7-1
- Update to 0.7

* Fri Jun 07 2013 David Woodhouse <David.Woodhouse@intel.com> - 0.6-1
- Initial package
