Vendor:         Microsoft Corporation
Distribution:   Mariner
%global api 1.0
%global __provides_exclude_from ^%{_libdir}/dleyna-%{api}/connectors/.*\\.so$

Name:           dleyna-connector-dbus
Version:        0.3.0
Release:        7%{?dist}
Summary:        D-Bus connector for dLeyna services

License:        LGPLv2
URL:            https://01.org/dleyna/
Source0:        https://01.org/sites/default/files/downloads/dleyna/%{name}-%{version}.tar_2.gz

BuildRequires:  dbus-devel
BuildRequires:  pkgconfig(dleyna-core-1.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig autoconf automake libtool

%description
D-Bus connector for dLeyna services.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
autoreconf -f -i
%configure \
  --disable-silent-rules \
  --disable-static

make %{?_smp_mflags}


%install
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -delete


%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc README
%dir %{_libdir}/dleyna-%{api}
%dir %{_libdir}/dleyna-%{api}/connectors
%{_libdir}/dleyna-%{api}/connectors/libdleyna-connector-dbus.so

%files devel
%{_libdir}/pkgconfig/%{name}-%{api}.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.0-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Oct 05 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Nils Philippsen <nils@redhat.com> - 0.2.0-5
- rebuild for new dleyna-core

* Tue Jan 20 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.2.0-4
- Fix crash when spawned by a call to com.intel.dLeynaRenderer.Manager.Release
  (RH #1154788)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 15 2014 Bastien Nocera <bnocera@redhat.com> 0.2.0-1
- Update to 0.2.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.1.0-3
- Filter out the connector plugin from provides.

* Sun Jul 07 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.1.0-2
- Use %%global instead of %%define.
- Own %%{_libdir}/dleyna-%%{api} and %%{_libdir}/dleyna-%%{api}/connectors.

* Wed Jun 26 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.1.0-1
- Initial spec.
