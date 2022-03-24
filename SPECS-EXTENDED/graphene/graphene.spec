Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           graphene
Version:        1.10.4
Release:        3%{?dist}
Summary:        Thin layer of types for graphic libraries

License:        MIT
URL:            https://github.com/ebassi/graphene
Source:         %{url}/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  %{_bindir}/xsltproc
BuildRequires:  gcc
BuildRequires:  gobject-introspection-devel
BuildRequires:  meson >= 0.50.1
BuildRequires:  pkgconfig(gobject-2.0) >= 2.30.0

%description
Graphene provides a small set of mathematical types needed to implement graphic
libraries that deal with 2D and 3D transformations and projections.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        tests
Summary:        Tests for the %{name} package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -p1

%build
%meson -Dgtk_doc=false
%meson_build

%install
%meson_install

%files
%license LICENSE.txt
%doc README.md
%{_libdir}/girepository-1.0/
%{_libdir}/libgraphene-1.0.so.0*

%files devel
%{_includedir}/graphene-1.0/
%dir %{_libdir}/graphene-1.0
%{_libdir}/graphene-1.0/include/
%{_libdir}/libgraphene-1.0.so
%{_libdir}/pkgconfig/graphene-1.0.pc
%{_libdir}/pkgconfig/graphene-gobject-1.0.pc
%{_datadir}/gir-1.0/

%files tests
%{_libexecdir}/installed-tests/
%{_datadir}/installed-tests/

%changelog
* Mon Mar 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10.4-3
- Adding BR on '%%{_bindir}/xsltproc'.
- Disabled gtk doc generation to remove network dependency during build-time.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10.4-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Feb 10 2021 Kalev Lember <klember@redhat.com> - 1.10.4-1
- Update to 1.10.4

* Mon Jun 22 2020 Kalev Lember <klember@redhat.com> - 1.10.2-1
- Update to 1.10.2
- Enable gtk-doc support

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Sep 08 2019 Kalev Lember <klember@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Tue Aug 13 10:06:51 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.6-1
- Update to 1.9.6

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 19 2019 Kalev Lember <klember@redhat.com> - 1.9.4-1
- Update to 1.9.4

* Tue May 14 2019 Kalev Lember <klember@redhat.com> - 1.9.2-1
- Update to 1.9.2

* Tue May 07 2019 Kalev Lember <klember@redhat.com> - 1.9.1-0.1.git5a4531b
- Update to 1.9.1 git snapshot

* Tue Mar 05 2019 Kalev Lember <klember@redhat.com> - 1.8.6-1
- Update to 1.8.6

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.4-1
- Update to 1.8.4

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Kalev Lember <klember@redhat.com> - 1.8.2-1
- Update to 1.8.2

* Fri Feb 23 2018 Kalev Lember <klember@redhat.com> - 1.8.0-1
- Update to 1.8.0
- Drop ldconfig scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 02 2017 Kalev Lember <klember@redhat.com> - 1.6.0-1
- Update to 1.6.0

* Mon Feb 27 2017 Kalev Lember <klember@redhat.com> - 1.5.4-3
- Build for ppc64 again now that gcc ICE is fixed

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Kalev Lember <klember@redhat.com> - 1.5.4-1
- Update to 1.5.4

* Mon Jan 02 2017 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.5.2-1
- Update to 1.5.2

* Tue Nov 22 2016 Kalev Lember <klember@redhat.com> - 1.5.1-0.2.git8a7a4a3
- Install installed tests to libexecdir (#1397317)

* Tue Nov 22 2016 Kalev Lember <klember@redhat.com> - 1.5.1-0.1.git8a7a4a3
- Initial Fedora packaging
