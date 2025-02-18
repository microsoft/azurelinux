# first two digits of version
%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

%ifarch %{valgrind_arches}
%global has_valgrind 1
%endif

%bcond_without gnutls

Name:           libsecret
Version:        0.21.4
Release:        3%{?dist}
Summary:        Library for storing and retrieving passwords and other secrets

# libsecret/mock/aes.py is Apache-2.0
# libsecret/mock/hkdf.py is GPL-2.0-or-later OR TGPPL-1.0
# part of libsecret/mock/dh.py is LicenseRef-Fedora-Public-Domain
License:        LGPL-2.1-or-later AND Apache-2.0 AND (GPL-2.0-or-later OR TGPPL-1.0) AND LicenseRef-Fedora-Public-Domain
URL:            https://wiki.gnome.org/Projects/Libsecret
Source0:        https://download.gnome.org/sources/libsecret/%{release_version}/libsecret-%{version}.tar.xz

BuildRequires:  docbook-style-xsl
BuildRequires:  gettext
BuildRequires:  gi-docgen
BuildRequires:  meson
BuildRequires:  vala
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
%if %{with gnutls}
BuildRequires:  pkgconfig(gnutls) >= 3.8.2
%else
BuildRequires:  pkgconfig(libgcrypt) >= 1.2.2
%endif
BuildRequires:  python3-devel
BuildRequires:  /usr/bin/xsltproc
%if 0%{?has_valgrind}
BuildRequires:  valgrind-devel
%endif

Provides:       bundled(egglib)

%description
libsecret is a library for storing and retrieving passwords and other secrets.
It communicates with the "Secret Service" using DBus. gnome-keyring and
KSecretService are both implementations of a Secret Service.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        mock-service
Summary:        Python mock-service files from %{name}
# This subpackage does not need libsecret installed,
# but this ensure that if it is installed, the version matches (for good measure):
Requires:       (%{name} = %{version}-%{release} if %{name})
BuildArch:      noarch

%description    mock-service
The %{name}-mock-service package contains testing Python files from %{name},
for testing of other similar tools, such as the Python SecretStorage package.


%prep
%autosetup -p1

# Use system valgrind headers instead
%if 0%{?has_valgrind}
rm -rf build/valgrind/
%endif


%build
%meson \
%if %{with gnutls}
-Dcrypto=gnutls \
%else
-Dcrypto=libgcrypt \
%endif
%{nil}

%meson_build


%install
%meson_install

%find_lang libsecret

# For the mock-service subpackage
mkdir -p %{buildroot}%{_datadir}/libsecret/mock
cp -a libsecret/mock/*.py %{buildroot}%{_datadir}/libsecret/mock/
cp -a libsecret/mock-service*.py %{buildroot}%{_datadir}/libsecret/
%py_byte_compile %{python3} %{buildroot}%{_datadir}/libsecret/mock/


%files -f libsecret.lang
%license COPYING
%doc NEWS README.md
%{_bindir}/secret-tool
%{_libdir}/libsecret-1.so.0*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Secret-1.typelib
%{_mandir}/man1/secret-tool.1*

%files devel
%license COPYING docs/reference/COPYING
%{_includedir}/libsecret-1/
%{_libdir}/libsecret-1.so
%{_libdir}/pkgconfig/libsecret-1.pc
%{_libdir}/pkgconfig/libsecret-unstable.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Secret-1.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libsecret-1.deps
%{_datadir}/vala/vapi/libsecret-1.vapi
%doc %{_docdir}/libsecret-1/

%files mock-service
%license COPYING
%dir %{_datadir}/libsecret
%{_datadir}/libsecret/mock/
%{_datadir}/libsecret/mock-service*.py


%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Apr 05 2024 Nieves Montero <nmontero@redhat.com> - 0.21.4-1
- Update to 0.21.4

* Wed Apr 03 2024 Miro Hrončok <mhroncok@redhat.com> - 0.21.3-2
- Package the mock-service files

* Mon Feb 19 2024 David King <amigadave@amigadave.com> - 0.21.3-1
- Update to 0.21.3

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.21.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 10 2023 Daiki Ueno <dueno@redhat.com> - 0.21.2-2
- Use GnuTLS as the default crypto backend

* Sat Dec 09 2023 Kalev Lember <klember@redhat.com> - 0.21.2-1
- Update to 0.21.2

* Tue Sep 19 2023 Kalev Lember <klember@redhat.com> - 0.21.1-1
- Update to 0.21.1

* Fri Aug 11 2023 Kalev Lember <klember@redhat.com> - 0.21.0-1
- Update to 0.21.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Feb 21 2022 David King <amigadave@amigadave.com> - 0.20.5-1
- Update to 0.20.5

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 10 2020 Kalev Lember <klember@redhat.com> - 0.20.4-1
- Update to 0.20.4

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Kalev Lember <klember@redhat.com> - 0.20.3-1
- Update to 0.20.3

* Mon Apr 06 2020 Kalev Lember <klember@redhat.com> - 0.20.2-2
- Drop gnome-keyring recommends again (#1781864)

* Wed Mar 11 2020 Kalev Lember <klember@redhat.com> - 0.20.2-1
- Update to 0.20.2

* Tue Jan 28 2020 Kalev Lember <klember@redhat.com> - 0.20.1-1
- Update to 0.20.1

* Tue Jan 14 2020 Kalev Lember <klember@redhat.com> - 0.20.0-1
- Update to 0.20.0

* Fri Sep 06 2019 Kalev Lember <klember@redhat.com> - 0.19.1-1
- Update to 0.19.1

* Fri Sep 06 2019 Kalev Lember <klember@redhat.com> - 0.19.0-2
- Recommend gnome-keyring (#1725412)

* Thu Sep 05 2019 Kalev Lember <klember@redhat.com> - 0.19.0-1
- Update to 0.19.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Mar 02 2019 Kalev Lember <klember@redhat.com> - 0.18.8-1
- Update to 0.18.8

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 29 2018 Kalev Lember <klember@redhat.com> - 0.18.7-1
- Update to 0.18.7
- Fix unowned gir and vala directories
- Tighten soname glob to avoid unnoticed soname bumps

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 29 2018 Kalev Lember <klember@redhat.com> - 0.18.6-1
- Update to 0.18.6
- Use valgrind_arches macro instead of hardcoding valgrind arch list

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.18.5-6
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 0.18.5-2
- BR vala instead of obsolete vala-tools subpackage

* Fri Mar 25 2016 Kalev Lember <klember@redhat.com> - 0.18.5-1
- Update to 0.18.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Kalev Lember <klember@redhat.com> - 0.18.4-1
- Update to 0.18.4

* Thu Dec 31 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.18.3-2
- Fix URL (#1294934)

* Tue Sep 15 2015 Kalev Lember <klember@redhat.com> - 0.18.3-1
- Update to 0.18.3
- Use make_install macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 21 2015 Kalev Lember <kalevlember@gmail.com> - 0.18.2-1
- Update to 0.18.2
- Use license macro for the COPYING file

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.18-7
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Sep 29 2014 Dan Horák <dan[at]danny.cz> - 0.18-6
- valgrind available only on selected arches

* Tue Sep 16 2014 Debarshi Ray <rishi@fedoraproject.org> - 0.18-5
- Use system valgrind headers (#1141474)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.18-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 08 2014 Richard Hughes <rhughes@redhat.com> - 0.18-1
- Update to 0.18

* Wed Aug 28 2013 Kalev Lember <kalevlember@gmail.com> - 0.16-1
- Update to 0.16

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.15-1
- Update to 0.15

* Wed Mar 06 2013 Debarshi Ray <rishi@fedoraproject.org> - 0.14-1
- Update to 0.14

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 0.13-1
- Update to 0.13

* Fri Nov 23 2012 Debarshi Ray <rishi@fedoraproject.org> - 0.12-1
- Update to 0.12

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 0.11-1
- Update to 0.11

* Wed Sep 19 2012 Tomas Bzatek <tbzatek@redhat.com> - 0.10-1
- Update to 0.10
- Enable vala

* Mon Aug 06 2012 Stef Walter <stefw@redhat.com> - 0.8-1
- Update to 0.8

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Debarshi Ray <rishi@fedoraproject.org> - 0.7-1
- Update to 0.7

* Sat Jul 14 2012 Kalev Lember <kalevlember@gmail.com> - 0.6-1
- Update to 0.6

* Thu Jun 28 2012 Kalev Lember <kalevlember@gmail.com> - 0.3-1
- Update to 0.3

* Mon Apr 16 2012 Kalev Lember <kalevlember@gmail.com> - 0.2-1
- Update to 0.2
- Enable parallel make

* Fri Mar 30 2012 Kalev Lember <kalevlember@gmail.com> - 0.1-2
- Add provides bundled(egglib) (#808025)
- Use global instead of define

* Thu Mar 29 2012 Kalev Lember <kalevlember@gmail.com> - 0.1-1
- Initial RPM release
