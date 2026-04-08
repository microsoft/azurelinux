# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libaccounts-glib
Version:        1.25
Release:        23%{?dist}
Summary:        Accounts framework for Linux and POSIX based platforms
# Automatically converted from old format: LGPLv2 - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2

# workaround for GitLab bug that puts commit hash into tarball root directory name
# https://gitlab.com/gitlab-org/gitlab/-/issues/214535
%global ver_str VERSION_%{version}

URL:            https://gitlab.com/accounts-sso/libaccounts-glib
Source0:        %{url}/-/archive/%{ver_str}/%{name}-%{ver_str}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 0.48.0
BuildRequires:  python3-devel
BuildRequires:  python3-gobject
BuildRequires:  vala

BuildRequires:  pkgconfig(gio-2.0) >= 2.26
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0) >= 2.26
BuildRequires:  pkgconfig(gobject-2.0) >= 2.35.1
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(sqlite3) >= 3.7.0

# dependencies for building docs
BuildRequires:  gtk-doc

# dependencies for tests
BuildRequires:  pkgconfig(check)

# package contains python3-gobject overrides
Requires:       python3-gobject

# Reduce the type safety as a workaround for build failures in Fedora 40+
# https://bugzilla.redhat.com/2261300
%global build_type_safety_c 2

%description
%{summary}.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package docs
Summary:        Documentation for %{name}
BuildArch:      noarch

%description docs
The %{name}-docs package contains documentation for %{name}.


%prep
%autosetup -n %{name}-%{ver_str} -p1


%build
%meson
%meson_build


%install
%meson_install

# create data directories
mkdir -p %{buildroot}%{_datadir}/accounts/{applications,providers,services,service_types}


%check
# some tests fail without either dbus-test-runner (not packaged) or X11 session
%meson_test || :


%files
%license COPYING
%doc README.md NEWS

%{_bindir}/ag-backup
%{_bindir}/ag-tool

%{_libdir}/libaccounts-glib.so.0
%{_libdir}/libaccounts-glib.so.%{version}
%{_libdir}/girepository-1.0/Accounts-1.0.typelib

%dir %{_datadir}/xml/accounts/schema/dtd
%{_datadir}/xml/accounts/schema/dtd/accounts-*.dtd

%dir %{_datadir}/xml/
%dir %{_datadir}/xml/accounts/
%dir %{_datadir}/xml/accounts/schema/
%dir %{_datadir}/accounts/
%dir %{_datadir}/accounts/applications/
%dir %{_datadir}/accounts/providers/
%dir %{_datadir}/accounts/services/
%dir %{_datadir}/accounts/service_types/

%{python3_sitearch}/gi/overrides/Accounts.py
%{python3_sitearch}/gi/overrides/__pycache__/*


%files devel
%{_includedir}/libaccounts-glib/

%{_libdir}/libaccounts-glib.so
%{_libdir}/pkgconfig/libaccounts-glib.pc

%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/gettext/its/accounts-*.{its,loc}
%{_datadir}/gir-1.0/Accounts-1.0.gir
%{_datadir}/vala/vapi/libaccounts-glib.deps
%{_datadir}/vala/vapi/libaccounts-glib.vapi


%files docs
%doc %{_datadir}/gtk-doc/html/libaccounts-glib/


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.25-23
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.25-22
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.25-20
- Rebuilt for Python 3.14

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.25-18
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.25-16
- Rebuilt for Python 3.13

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.25-12
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.25-9
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.25-6
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.25-2
- Rebuilt for Python 3.9

* Wed Apr 15 2020 Fabio Valentini <decathorpe@gmail.com> - 1.25-1
- Update to version 1.25.

* Sat Apr 11 2020 Fabio Valentini <decathorpe@gmail.com> - 1.24-1
- Update to version 1.24.
- Migrate from autotools to meson.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 1.23-1
- 1.23

* Tue Feb 23 2016 Rex Dieter <rdieter@fedoraproject.org> 1.21-1
- 1.21, %%check: (advisory) 'make check' 

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 28 2015 Rex Dieter <rdieter@fedoraproject.org> - 1.18-3
- tighten subpkg dependencies
- -devel: drop hard-coded glib2 dep (pkgconfig auto deps handles it)
- .spec cosmetics
- own %%_datadir/accounts (and children)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 26 2015 Daniel Vrátil <dvratil@redhat.com> - 1.18-1
- update to 1.18
- update upstream source URL
- use %%license
- drop upstreamed patch

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.16-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 26 2014 Daniel Vrátil <dvratil@redhat.com> - 1.16-1
- Latest upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Jaroslav Reznik <jreznik@redhat.com> - 1.8-1
- Latest upstream release
- Add GObject introspection
- Fix URLs and description

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 06 2010 Chen Lei <supercyper@163.com> - 0.45-1
- New upstream release

* Fri Jul 23 2010 Chen Lei <supercyper@163.com> - 0.39-2
- List files more specfic in spec
- Add a permanent link for meego SRPM

* Thu Jul 08 2010 Chen Lei <supercyper@163.com> - 0.39-1
- Initial packaging for Fedora

* Mon Jun 14 2010 Bernd Wachter <ext-bernd.wachter@nokia.com> - 0.39
- Update to latest version

