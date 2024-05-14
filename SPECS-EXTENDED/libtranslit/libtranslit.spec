Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		libtranslit
Version:	0.0.3
Release:	27%{?dist}
Summary:	ASCII to Unicode transliteration library with multiple backends

License:	GPLv3+
URL:		https://github.com/ueno/libtranslit
Source0:	https://du-a.org/files/libtranslit/%{name}-%{version}.tar.gz

BuildRequires:	gobject-introspection-devel
BuildRequires:	intltool
BuildRequires:	vala

%description
ASCII to Unicode transliteration library with multiple backends.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	m17n
Summary:	Transliteration module using m17n-lib for %{name}
BuildRequires:	pkgconfig(m17n-shell)
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	m17n
The %{name}-m17n package contains a transliteration module using
m17n-lib for %{name}.

%package	icu
Summary:	Transliteration module using m17n-lib for %{name}
BuildRequires:	pkgconfig(icu-io)
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	icu
The %{name}-icu package contains a transliteration module using
ICU for %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f '{}' ';'


%ldconfig_scriptlets


%files
%{_libdir}/*.so.*
%dir %{_libdir}/libtranslit
%dir %{_libdir}/libtranslit/modules
%{_libdir}/girepository-1.0/*.typelib

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/*.vapi
%{_datadir}/vala/vapi/*.deps

%files m17n
%{_libdir}/libtranslit/modules/*m17n.so*

%files icu
%{_libdir}/libtranslit/modules/*icu.so*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.0.3-27
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 0.0.3-25
- Rebuild for ICU 65

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 0.0.3-23
- Co-own /usr/share/vala and /usr/share/vala/vapi instead of requiring vala

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 0.0.3-21
- Rebuild for ICU 63

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 0.0.3-19
- Rebuild for ICU 62

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 0.0.3-18
- Rebuild for ICU 61.1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 0.0.3-16
- Rebuild for ICU 60.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 0.0.3-12
- rebuild for ICU 57.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 0.0.3-10
- rebuild for ICU 56.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 0.0.3-8
- rebuild for ICU 54.1

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 0.0.3-7
- rebuild for ICU 53.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.0.3-5
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 14 2014 David Tardon <dtardon@redhat.com> - 0.0.3-3
- rebuild for new ICU

* Tue Aug 27 2013 Daiki Ueno <dueno@redhat.com> - 0.0.3-2
- fix libtranslit.vapi installation

* Tue Aug 27 2013 Daiki Ueno <dueno@redhat.com> - 0.0.3-1
- new upstream release
- install libtranslit.vapi

* Tue Aug 13 2013 Daiki Ueno <dueno@redhat.com> - 0.0.2-6
- own %%{_libdir}/libtranslit directory (Closes:#986672)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jan 29 2013 Daiki Ueno <dueno@redhat.com> - 0.0.2-4
- rebuild with new icu

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Daiki Ueno <dueno@redhat.com> - 0.0.2-2
- rebuild with new icu

* Mon Mar  5 2012 Daiki Ueno <dueno@redhat.com> - 0.0.2-1
- initial packaging for Fedora
