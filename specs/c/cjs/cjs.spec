# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit0 9f89ac464ad879a4eb49bba929476ce50dda012b
%global date 20251023
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

%global glib2_version 2.66.0
%global gobject_introspection_version 1.66.0
%global gtk3_version 3.20
%global mozjs128_version 128.5.1

Name:          cjs
Epoch:         1
Version:       128.1%{!?tag:~%{date}git%{shortcommit0}}
Release: 2%{?dist}
Summary:       Javascript Bindings for Cinnamon

# Automatically converted from old format: MIT and (MPLv1.1 or GPLv2+ or LGPLv2+) - review is highly recommended.
License:       LicenseRef-Callaway-MIT AND (LicenseRef-Callaway-MPLv1.1 OR GPL-2.0-or-later OR LicenseRef-Callaway-LGPLv2+)
# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
URL:           https://github.com/linuxmint/%{name}
%if 0%{?tag:1}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%else
Source0:        %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif

ExcludeArch:   %{ix86}

BuildRequires: gcc-c++
BuildRequires: gettext
BuildRequires: meson
BuildRequires: pkgconfig(cairo-gobject)
BuildRequires: pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gobject-introspection-1.0) >= %{gobject_introspection_version}
BuildRequires: pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires: pkgconfig(mozjs-128) >= %{mozjs128_version}
BuildRequires: pkgconfig(readline)
BuildRequires: pkgconfig(sysprof-capture-4)
# For GTK+ 3 tests
BuildRequires: gtk3
# For dbus tests
BuildRequires: dbus-daemon
# Required for checks
BuildRequires: dbus-x11
BuildRequires: mesa-dri-drivers
BuildRequires: mutter
BuildRequires: xwayland-run

Requires: glib2%{?_isa} >= %{glib2_version}
Requires: gobject-introspection%{?_isa} >= %{gobject_introspection_version}
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: mozjs128%{?_isa} >= %{mozjs128_version}

%description
Cjs allows using Cinnamon libraries from Javascript. It's based on the
Spidermonkey Javascript engine from Mozilla and the GObject introspection
framework.


%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{?epoch}:%{version}-%{release}

%description devel
Files for development with %{name}.


%package tests
Summary: Tests for the cjs package
Requires: %{name}%{?_isa} = %{?epoch}:%{version}-%{release}

%description tests
The cjs-tests package contains tests that can be used to verify
the functionality of the installed cjs package.


%prep
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n %{name}-%{commit0}
%endif


%build
%meson
%meson_build


%install
%meson_install


%check
%{shrink:xwfb-run -c mutter -- %meson_test --timeout-multiplier=5}

%files
%doc NEWS README.md
%license COPYING
%{_bindir}/cjs
%{_bindir}/cjs-console
%{_libdir}/*.so.*
%{_libdir}/cjs/


%files devel
%doc examples/*
%{_includedir}/cjs-1.0/
%{_libdir}/pkgconfig/cjs-*1.0.pc
%{_libdir}/*.so
%{_datadir}/cjs-1.0/


%files tests
%{_libexecdir}/installed-tests/
%{_datadir}/installed-tests/
%{_datadir}/glib-2.0/schemas/org.cinnamon.CjsTest.gschema.xml


%changelog
* Wed Dec 10 2025 Leigh Scott <leigh123linux@gmail.com> - 1:128.1-1
- Update to 128.1

* Fri Sep 12 2025 Leigh Scott <leigh123linux@gmail.com> - 1:128.0-3
- Backport fixes to support GLib 2.86.0 typelibs

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:128.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Mar 28 2025 Leigh Scott <leigh123linux@gmail.com> - 1:128.0-1
- Update to 128.0

* Wed Mar 26 2025 Leigh Scott <leigh123linux@gmail.com> - 1:6.4.0-3
- Switch to mozjs128

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 25 2024 Leigh Scott <leigh123linux@gmail.com> - 1:6.4.0-1
- Update to 6.4.0

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 1:6.2.0-3
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Leigh Scott <leigh123linux@gmail.com> - 1:6.2.0-1
- Update to 6.2.0

* Tue May 14 2024 Leigh Scott <leigh123linux@gmail.com> - 1:6.0.0-4
- Port to mozjs115

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 16 2023 Leigh Scott <leigh123linux@gmail.com> - 1:6.0.0-1
- Update to 6.0.0 release

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 02 2023 Leigh Scott <leigh123linux@gmail.com> - 1:5.8.0-1
- Update to 5.8.0 release

* Tue May 09 2023 Leigh Scott <leigh123linux@gmail.com> - 1:5.7.0-0.1^git20230508.1ef6934
- Update to 5.7.0 git snapshot

* Fri May 05 2023 Leigh Scott <leigh123linux@gmail.com> - 1:5.6.1-1
- Update to 5.6.1 release

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 18 2022 Leigh Scott <leigh123linux@gmail.com> - 1:5.6.0-1
- Update to 5.6.0 release

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 17 2022 Leigh Scott <leigh123linux@gmail.com> - 1:5.4.1-1
- Update to 5.4.1 release

* Fri Jun 10 2022 Leigh Scott <leigh123linux@gmail.com> - 1:5.4.0-1
- Update to 5.4.0 release

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 08 2022 Miro Hrončok <mhroncok@redhat.com> - 1:5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Fri Nov 19 2021 Leigh Scott <leigh123linux@gmail.com> - 1:5.2.0-1
- Update to 5.2.0 release

* Fri Oct 15 2021 Leigh Scott <leigh123linux@gmail.com> - 1:5.0.1-1
- Update to 5.0.1 release

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 Leigh Scott <leigh123linux@gmail.com> - 1:5.0.0-2
- Rebuild against mozjs78-78.12.0-1

* Fri May 28 2021 Leigh Scott <leigh123linux@gmail.com> - 1:5.0.0-1
- Update to 5.0.0 release

* Fri Mar 26 2021 Kalev Lember <klember@redhat.com> - 1:4.8.2-3
- Rebuild to fix sysprof-capture symbols leaking into libraries consuming it

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Leigh Scott <leigh123linux@gmail.com> - 1:4.8.2-1
- Update to 4.8.2 release

* Tue Dec  8 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.8.1-1
- Update to 4.8.1 release

* Wed Nov 25 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.8.0-1
- Update to 4.8.0 release

* Fri Nov 06 2020 Jeff Law <law@redhat.com> - 1:4.7.0-0.3.20201019gitbefc11a
- Fix bogus volatile caught by gcc-11

* Tue Oct 20 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.7.0-0.2.20201019gitbefc11a
- Rebuild against mozjs78-78.4.0-1

* Mon Oct 19 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.7.0-0.1.20201019git974a99b
- update to git snapshot

* Sun Sep 20 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.6.0-3
- Use mozjs78 for f34+

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 12 2020 Leigh Scott <leigh123linux@gmail.com> - 1:4.6.0-1
- Update to 4.6.0 release

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:4.4.0-1
- Update to 4.4.0 release

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 14 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:4.2.0-1
- Update to 4.2.0 release

* Mon Feb 18 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:4.0.0-5
- Rebuild for possible mozjs52 fallout

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:4.0.0-4
- Rebuild for readline 8.0

* Fri Feb 01 2019 Leigh Scott <leigh123linux@googlemail.com> - 1:4.0.0-3
- Fix build with newer autoconf-archive

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 30 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:4.0.0-1
- Update to 4.0.0 release

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:3.8.0-1
- Update to 3.8.0 release

* Wed Feb 21 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:3.6.2-0.2.20180218git5cfcbfd
- update to git snapshot

* Thu Feb 15 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:3.6.2-0.1.20180122git8aee7bb
- update to git snapshot

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Nov 11 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.6.1-1
- update to 3.6.1 release

* Mon Oct 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.6.0-1
- update to 3.6.0 release

* Fri Sep 08 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.4.4-3
- Fix needsPostBarrier crash again (rhbz #1472008)

* Wed Aug 30 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.4.4-2
- Add build fixes for epel7

* Wed Aug 09 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.4.4-1
- update to 3.4.4 release

* Sun Aug 06 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.4.3-4
- Fix needsPostBarrier crash again (rhbz #1472008)
- Drop build requires gnome-common

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 06 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.4.3-1
- update to 3.4.3 release

* Thu Jun 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.4.2-2
- Fix log spam due to missing commit

* Wed Jun 28 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.4.2-1
- update to 3.4.2 release

* Sun Jun 25 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.4.1-3
- Fix needsPostBarrier crash (rhbz #1453008)

* Sun Jun 18 2017 Björn Esser <besser82@fedoraproject.org> - 1:3.4.1-2
- Add patches from upstream for tweener

* Tue May 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.4.1-1
- update to 3.4.1 release

* Wed May 03 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.4.0-1
- update to 3.4.0 release

* Wed Apr 26 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.4.0-0.1.20170426git16347ea
- update to git snapshot

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1:3.2.0-2
- Rebuild for readline 7.x

* Mon Nov 07 2016 Leigh Scott <leigh123linux@googlemail.com> - 1:3.2.0-1
- update to 3.2.0 release

* Sun May 15 2016 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.1-1
- update to 3.0.1 release

* Sat Apr 23 2016 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.0-1
- update to 3.0.0 release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 09 2015 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-2
- rebuilt

* Fri Oct 16 2015 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.0-1
- update to 2.8.0 release

* Sat Jun 27 2015 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.2-1
- update to 2.6.2 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Leigh Scott <leigh123linux@googlemail.com> - 1:2.6.0-1
- update to 2.6.0 release

* Tue May 05 2015 Leigh Scott <leigh123linux@googlemail.com> - 1:2.5.0-0.1.git5821be5
- update to git snapshot

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1:2.4.2-2
- Rebuilt for GCC 5 C++11 ABI change

* Tue Mar 31 2015 Leigh Scott <leigh123linux@googlemail.com> - 1:2.4.2-1
- update to 2.4.2

* Sun Nov 23 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:2.4.1-1
- update to 2.4.1
- move .so files to -devel sub-package
- change requires for -tests sub-package

* Thu Oct 30 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:2.4.0-1
- update to 2.4.0

* Tue Sep 30 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:2.4.0-0.3.git7a65cc7
- add check section to spec

* Tue Sep 30 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:2.4.0-0.2.git7a65cc7
- add build requires gtk3-devel

* Tue Sep 30 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:2.4.0-0.1.git7a65cc7
- update to latest git
- swap to mozjs24

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:2.2.2-1
- update to 2.2.2

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1:2.2.1-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:2.2.1-1
- update to 2.2.1

* Sat Apr 12 2014 Leigh Scott <leigh123linux@googlemail.com> - 1:2.2.0-1
- update to 2.2.0

* Wed Oct 02 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:2.0.0-1
- update to 2.0.0

* Mon Sep 30 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:1.9.1-2
- add epoch to -devel

* Mon Sep 30 2013 Leigh Scott <leigh123linux@googlemail.com> - 1:1.9.1-1
- update to 1.9.1
- add epoch

* Sun Sep 15 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.34.0-0.5.gita30f982
- update to latest git

* Thu Aug 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.34.0-0.4.gitfb472ad
- rebuilt

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.34.0-0.3.gitfb472ad
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.34.0-0.2.gitfb472ad
- add isa tag to -devel sub-package

* Sun Jul 21 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.34.0-0.1.gitfb472ad
- Inital build
