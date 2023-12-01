%define majmin %(echo %{version} | cut -d. -f1-2)
Summary:        Python bindings for GObject Introspection
Name:           pygobject3
Version:        3.42.0
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://wiki.gnome.org/Projects/PyGObject
Source0:        https://download.gnome.org/sources/pygobject/%{majmin}/pygobject-%{version}.tar.xz
BuildRequires:  cairo-gobject-devel
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  meson
BuildRequires:  python3-devel
BuildRequires:  python3-cairo-devel
BuildRequires:  glib-schemas
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  dbus
BuildRequires:  openssl-devel
BuildRequires:  python3-gobject-introspection
BuildRequires:  python3-pip
%endif


%description
The %{name} package provides a convenient wrapper for the GObject library
for use in Python programs.

%package     -n python3-gobject
Summary:        Python 3 bindings for GObject Introspection
Requires:       python3-gobject-base = %{version}-%{release}
# The cairo override module depends on this
Requires:       python3-cairo

%description -n python3-gobject
The python3-gobject package provides a convenient wrapper for the GObject 
library and and other libraries that are compatible with GObject Introspection, 
for use in Python 3 programs.

%package     -n python3-gobject-base
Summary:        Python 3 bindings for GObject Introspection base package
Requires:       gobject-introspection

%description -n python3-gobject-base
This package provides the non-cairo specific bits of the GObject Introspection
library.

%package     -n python3-gobject-devel
Summary:        Development files for embedding PyGObject introspection support
Requires:       python3-gobject = %{version}-%{release}
Requires:       gobject-introspection-devel
# Old Fedora name for the package, provided for compatibility purposes
Provides:       pygobject3-devel = %{version}-%{release}

%description -n python3-gobject-devel
This package contains files required to embed PyGObject

%prep
%autosetup -n pygobject-%{version} -p1

%build
%meson -Dpython=%{__python3}
%meson_build

%install
%meson_install

%check
pip3 install pytest
python3 setup.py test

%files -n python3-gobject
%{python3_sitearch}/gi/_gi_cairo*.so

%files -n python3-gobject-base
%license COPYING
%doc NEWS
%dir %{python3_sitearch}/gi
%{python3_sitearch}/gi/*
%exclude %{python3_sitearch}/gi/_gi_cairo*.so
%{python3_sitearch}/pygtkcompat/
%{python3_sitearch}/PyGObject-*.egg-info

%files -n python3-gobject-devel
%dir %{_includedir}/pygobject-3.0/
%{_includedir}/pygobject-3.0/pygobject.h
%{_libdir}/pkgconfig/pygobject-3.0.pc

%changelog
* Thu Apr 07 2022 Olivia Crain <oliviacrain@microsoft> - 3.42.0-1
- Upgrade to latest upstream version
- Lint spec

* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.36.1-5
- Replace easy_install usage with pip in %%check sections

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.36.1-4
- Remove unused python-setuptools dependency

* Fri May 14 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.36.1-3
- Move python setuptools and glib schemas to non-check BuildRequires

* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 3.36.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- License verified.

* Thu May 07 2020 Kalev Lember <klember@redhat.com> - 3.36.1-1
- Update to 3.36.1

* Sun Mar 08 2020 Kalev Lember <klember@redhat.com> - 3.36.0-2
- Drop pkgconfig provides filtering as we no longer ship the Python 2 package

* Sun Mar 08 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.34.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Miro Hrončok <mhroncok@redhat.com> - 3.34.0-4
- Subpackages python2-gobject, python2-gobject-base, python2-gobject-devel have been removed
  See https://fedoraproject.org/wiki/Changes/RetirePython2

* Wed Sep 25 2019 Kalev Lember <klember@redhat.com> - 3.34.0-3
- Don't add pkgconfig provides to python2-gobject-devel

* Sat Sep 21 2019 Kalev Lember <klember@redhat.com> - 3.34.0-2
- Drop Python 3 conditionals
- Split pygobject3-devel into python2-gobject-devel and python3-gobject-devel
  (#1749589)

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Mon Aug 19 2019 Kalev Lember <klember@redhat.com> - 3.33.1-1
- Update to 3.33.1

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 3.32.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Kalev Lember <klember@redhat.com> - 3.32.2-1
- Update to 3.32.2

* Tue Jun 18 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.32.1-2
- Fix build under python3.8 (#1717655)

* Mon May 06 2019 Kalev Lember <klember@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Thu Mar 07 2019 Kalev Lember <klember@redhat.com> - 3.31.4-1
- Update to 3.31.4

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 3.31.3-1
- Update to 3.31.3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Kalev Lember <klember@redhat.com> - 3.31.2-1
- Update to 3.31.2

* Sat Dec 01 2018 Kalev Lember <klember@redhat.com> - 3.30.4-1
- Update to 3.30.4

* Tue Nov 27 2018 Kalev Lember <klember@redhat.com> - 3.30.3-1
- Update to 3.30.3

* Mon Nov 12 2018 Kalev Lember <klember@redhat.com> - 3.30.2-1
- Update to 3.30.2

* Fri Sep 14 2018 Kalev Lember <klember@redhat.com> - 3.30.1-1
- Update to 3.30.1

* Fri Sep 14 2018 Dan Horák <dan[at]danny.cz> - 3.30.0-2
- Include temporary big endian fix (#1623547)

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Mon Aug 13 2018 Kalev Lember <klember@redhat.com> - 3.29.2-1
- Update to 3.29.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 3.28.3-2
- Rebuilt for Python 3.7

* Fri Jun 01 2018 Kalev Lember <klember@redhat.com> - 3.28.3-1
- Update to 3.28.3

* Wed Mar 28 2018 Kalev Lember <klember@redhat.com> - 3.28.2-1
- Update to 3.28.2

* Mon Mar 19 2018 Kalev Lember <klember@redhat.com> - 3.28.1-1
- Update to 3.28.1

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Sat Mar 03 2018 Kalev Lember <klember@redhat.com> - 3.27.5-1
- Update to 3.27.5

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.27.1-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.27.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 20 2017 Kalev Lember <klember@redhat.com> - 3.27.1-1
- Update to 3.27.1

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Wed Sep 27 2017 Troy Dawson <tdawson@redhat.com> - 3.26.0-2
- Cleanup spec file conditionals

* Thu Sep 14 2017 Kalev Lember <klember@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Thu Sep 14 2017 Kalev Lember <klember@redhat.com> - 3.24.1-5
- Rename python-gobject-base to python2-gobject-base as well

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.24.1-4
- Python 2 binary package renamed to python2-pygobject3
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 11 2017 Kalev Lember <klember@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.22.0-2
- Rebuild for Python 3.6

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Sun Sep 11 2016 Kalev Lember <klember@redhat.com> - 3.21.92-1
- Update to 3.21.92

* Fri Aug 26 2016 Kalev Lember <klember@redhat.com> - 3.21.91-1
- Update to 3.21.91

* Tue Aug 23 2016 Kalev Lember <klember@redhat.com> - 3.21.1-0.1.git395779e
- Update to 3.21.1 git snapshot

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.21.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 3.21.0-1
- Update to 3.21.0

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Wed Mar 16 2016 Kalev Lember <klember@redhat.com> - 3.19.92-1
- Update to 3.19.92

* Wed Mar 02 2016 Richard Hughes <rhughes@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Mon Feb 29 2016 Richard Hughes <rhughes@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 3.19.2-2
- Rebuilt for Python3.5 rebuild

* Sun Nov 01 2015 Kalev Lember <klember@redhat.com> - 3.19.2-1
- Update to 3.19.2

* Sat Oct 24 2015 Kalev Lember <klember@redhat.com> - 3.18.2-1
- Update to 3.18.2

* Sat Oct 24 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1
- Update project URL and Source download location

* Mon Oct 19 2015 Kalev Lember <klember@redhat.com> - 3.18.0-2
- Backport a fix for Gdk.rectangle_intersect/rectangle_union compatibility
  (#1269901)

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Sat Aug 22 2015 Kalev Lember <klember@redhat.com> - 3.17.90-2
- Rename Python 2 subpackage to python-gobject for consistency with the
  python3-gobject package

* Thu Aug 20 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90
- Use make_install macro
- Use license macro for COPYING

* Tue Jun 30 2015 Kalev Lember <klember@redhat.com> - 3.17.1-3
- Split non-cairo parts python3-gobject into a subpackage

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.1-1
- Update to 3.17.1

* Wed Jun 03 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-2
- Backport a patch for GdkRectangle changes in gtk+ 3.17.2

* Tue Apr 14 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Thu Mar 05 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91-1
- Update to 3.15.91

* Sat Feb 21 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.0-1
- Update to 3.15.0

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-1
- Update to 3.13.92

* Tue Sep 02 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.91-1
- Update to 3.13.91

* Thu Aug 21 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.90-2
- Backport a fix for virt-manager crash (#1130758)

* Tue Aug 19 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.90-1
- Update to 3.13.90

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-1
- Update to 3.13.4

* Tue Jun 24 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-1
- Update to 3.13.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-1
- Update to 3.13.2
- Drop old testsuite patches

* Mon May 12 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Apr 29 2014 Richard Hughes <rhughes@redhat.com> - 3.13.1-1
- Update to 3.13.1

* Tue Apr 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-1
- Update to 3.12.1

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0-2
- Update dep versions
- Tighten deps with %%_isa

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Wed Feb 05 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Tue Jan 14 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Mon Nov 18 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-1
- Update to 3.9.91

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Fri Aug  9 2013 Daniel Drake <dsd@laptop.org> - 3.9.5-1
- Update to 3.9.5

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.2-1
- Update to 3.9.2

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.1-2
- Disable pyflakes tests to avoid failures with too new pyflakes 0.7.2

* Fri May 10 2013 Richard Hughes <rhughes@redhat.com> - 3.9.1-1
- Update to 3.9.1

* Thu Apr 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.8.1-2
- Add upstream patch to fix Sugar (RHBZ 947538)

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Apr  2 2013 David Malcolm <dmalcolm@redhat.com> - 3.8.0-2
- add workarounds for ppc64 (rhbz#924425)

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.92-1
- Update to 3.7.92

* Thu Mar  7 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.90-1
- Update to 3.7.90

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.5.1-1
- Update to 3.7.5.1
- Re-enable tests

* Wed Jan 16 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Fri Dec 28 2012 Dan Horák <dan[at]danny.cz> - 3.7.3-2
- Fix GBytes test (gnome#690837)

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.3-1
- Update to 3.7.3
- Drop upstreamed patches; rebase the ignore-more-pep8-errors patch

* Thu Dec 13 2012 Ray Strode <rstrode@redhat.com> 3.7.1-3
- Split non-cairo parts into a subpackage

* Mon Nov 12 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-2
- Remove lib64 rpaths (#817701)
- Move code examples to the -devel subpackage and fix the multilib
  conflict (#831434)

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Tue Nov  6 2012 Daniel Drake <dsd@laptop.org> - 3.4.1.1-2
- Upstream fix for property lookup; needed for basic Sugar operation.

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1.1-1
- Update to 3.4.1.1

* Thu Sep 13 2012 Daniel Drake <dsd@laptop.org> - 3.3.91-1
- Latest version; upstreamed patches dropped

* Wed Aug 15 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-9
- avoid dragging pyflakes and python-pep8 into RHEL (patch 7)

* Fri Aug 10 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-8
- add endianness patch (rhbz#841596; attachment 603634)

* Fri Aug 10 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-7
- update endianness patch for rhbz#841596 (to attachment 603367)

* Thu Aug  9 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-6
- fix issues on big-endian 64-bit machines (rhbz#841596, rhbz#842880)

* Thu Aug  9 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-5
- use xvfb-run in selftests; update known failures

* Wed Aug  8 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-4
- add a %%check check; add V=1 to all make invocations

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-2
- remove rhel logic from with_python3 conditional

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.3.4-1
- Update to 3.3.4

* Tue Jun 26 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.3.1-2
- fix a segfault when dealing with mismatched .so/typelib files

* Mon Jun 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.3.3.1-1
- Update to 3.3.3.1

* Tue Jun 19 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.2-1
- Update to 3.3.2

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.1-1
- Update to 3.3.1
- Dropped the now unneeded -lm patch

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.2.0-1
- Update to 3.2.0

* Thu Mar 22 2012 Matthias Clasen <mclasen@redhat.com> - 3.1.93-1
- Update to 3.1.93

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.1.92-1
- Update to 3.1.92

* Sun Feb 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.1.0-1
- Update to 3.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.0.3-1
- udpate to 3.0.3

* Sat Oct 22 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.0.2-1
- udpate to 3.0.2

* Fri Sep 30 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.0.1-1
- udpate to 3.0.1

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Thu Sep 15 2011 John (J5) Palmieri <johnp@gnome.org> - 2.90.4-1
- update to 2.90.4
- get rid of packaging cruft that is taken care of by upstream now

* Wed Aug 31 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 2.90.3-1
- udpate to 2.90.3

* Mon Aug 22 2011 John (J5) Palmieri <johnp@redhat.com> - 2.90.2-3
- remove some old requires

* Fri Aug 19 2011 John (J5) Palmieri <johnp@redhat.com> - 2.90.2-2
- fix up issues uncovered during package review
- disable docs because they still reference the static bindings 
  and upstream is working on new documentation

* Thu Aug 18 2011 John (J5) Palmieri <johnp@redhat.com> - 2.90.2-1
- Initial package
