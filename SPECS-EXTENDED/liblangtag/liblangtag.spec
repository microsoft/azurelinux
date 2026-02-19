%global girname LangTag
%global girapiversion 0.6
%global soversion 1
%global soversion_gobject 0

Name: liblangtag
Version: 0.6.7
Release: 1%{?dist}
Summary: An interface library to access tags for identifying languages

License: LGPLv3+ or MPLv2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://bitbucket.org/tagoh/liblangtag
Source0: https://bitbucket.org/tagoh/%{name}/downloads/%{name}-%{version}.tar.bz2

Requires: %{name}-data = %{version}-%{release}

BuildRequires: glibc-common
BuildRequires: gtk-doc
BuildRequires: pkgconfig(check)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(libxml-2.0)

%description
%{name} is an interface library to access tags for identifying
languages.

Features:
* several subtag registry database supports:
  - language
  - extlang
  - script
  - region
  - variant
  - extension
  - grandfathered
  - redundant
* handling of the language tags
  - parser
  - matching
  - canonicalizing

%package data
Summary: %{name} data files
License: UCD
BuildArch: noarch

%description data
The %{name}-data package contains data files for %{name}.

%package gobject
Summary: GObject introspection for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description gobject
The %{name}-gobject package contains files for GObject introspection for
%{name}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-gobject%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary: Documentation of %{name} API
BuildArch: noarch

%description doc
The %{name}-doc package contains documentation files for %{name}.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --disable-static --enable-shared --enable-introspection
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
export LD_LIBRARY_PATH=`pwd`/liblangtag/.libs:`pwd`/liblangtag-gobject/.libs${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la %{buildroot}/%{_libdir}/%{name}/*.la

%ldconfig_scriptlets

%ldconfig_scriptlets gobject

%check
export LD_LIBRARY_PATH=`pwd`/liblangtag/.libs:`pwd`/liblangtag-gobject/.libs${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make %{?_smp_mflags} check

%files
%doc AUTHORS NEWS README
%{_libdir}/%{name}.so.%{soversion}
%{_libdir}/%{name}.so.%{soversion}.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so

%files data
%license COPYING
%{_datadir}/%{name}

%files gobject
%{_libdir}/%{name}-gobject.so.%{soversion_gobject}
%{_libdir}/%{name}-gobject.so.%{soversion_gobject}.*
%{_libdir}/girepository-1.0/%{girname}-%{girapiversion}.typelib

%files devel
%{_includedir}/%{name}
%{_libdir}/%{name}.so
%{_libdir}/%{name}-gobject.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-gobject.pc
%{_datadir}/gir-1.0/%{girname}-%{girapiversion}.gir

%files doc
%license COPYING
%{_datadir}/gtk-doc/html/%{name}

%changelog
* Tue Nov 19 2024 Kevin Lockwood <v-klockwood@microsoft.com> - 0.6.7-1
- Update to 0.6.7
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.3-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 26 2019 Caolán McNamara <caolanm@redhat.com> - 0.6.3-1
- Resolves: rhbz#1755875 latest available version

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Sep 30 2016 David Tardon <dtardon@redhat.com> - 0.6.2-1
- new upstream release

* Thu Sep 22 2016 David Tardon <dtardon@redhat.com> - 0.6.1-1
- new upstream release

* Wed Mar 23 2016 David Tardon <dtardon@redhat.com> - 0.6.0-1
- new upstream release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 David Tardon <dtardon@redhat.com> - 0.5.8-1
- new upstream release

* Fri Jun 26 2015 David Tardon <dtardon@redhat.com> - 0.5.7-1
- new upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 31 2015 Caolán McNamara <caolanm@redhat.com> - 0.5.6-1
- Resolves: rhbz#1207452 latest available version

* Fri Mar 27 2015 David Tardon <dtardon@redhat.com> - 0.5.5-3
- another header fix

* Fri Mar 27 2015 David Tardon <dtardon@redhat.com> - 0.5.5-2
- fix installation of headers

* Fri Mar 20 2015 David Tardon <dtardon@redhat.com> - 0.5.5-1
- new upstream release

* Tue Jan 20 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.5.4-6
- Let liblangtag package own %%{_libdir}/%%{name} (RHBZ#1183882).

* Fri Sep 05 2014 David Tardon <dtardon@redhat.com> - 0.5.4-5
- split GObject introspection files out of main package

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.5.4-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 David Tardon <dtardon@redhat.com> - 0.5.4-1
- new upstream release

* Fri Apr 11 2014 David Tardon <dtardon@redhat.com> - 0.5.3-1
- new upstream release

* Mon Sep 02 2013 David Tardon <dtardon@redhat.com> - 0.5.2-1
- new release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Eike Rathke <erack@redhat.com> - 0.5.1-2-UNBUILT
- updated .spec with MPLv2.0 and UCD licenses

* Tue Apr 30 2013 David Tardon <dtardon@redhat.com> - 0.5.1-1
- fix ABI breakage

* Mon Apr 29 2013 David Tardon <dtardon@redhat.com> - 0.5.0-1
- new release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 01 2012 David Tardon <dtardon@redhat.com> - 0.4.0-2
- fix build on ppc

* Sun Nov 25 2012 David Tardon <dtardon@redhat.com> - 0.4.0-1
- new upstream release

* Sun Sep 09 2012 David Tardon <dtardon@redhat.com> - 0.3-1
- initial import
