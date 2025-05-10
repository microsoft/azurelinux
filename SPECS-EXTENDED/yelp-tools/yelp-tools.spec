%global tarball_version %%(echo %{version} | tr '~' '.')

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:          yelp-tools
Version:       42.1
Release:       7%{?dist}
Summary:       Create, manage, and publish documentation for Yelp

License:       GPL-2.0-or-later
URL:           https://wiki.gnome.org/Apps/Yelp/Tools
Source0:       https://download.gnome.org/sources/%{name}/42/%{name}-%{tarball_version}.tar.xz
BuildArch:     noarch

BuildRequires: meson
BuildRequires: pkgconfig(yelp-xsl)
BuildRequires: python3-lxml
BuildRequires: itstool
BuildRequires: libxslt

Requires: /usr/bin/itstool
Requires: /usr/bin/xmllint
Requires: /usr/bin/xsltproc
Requires: mallard-rng
Requires: python3-lxml
Requires: yelp-xsl

%description
yelp-tools is a collection of scripts and build utilities to help create,
manage, and publish documentation for Yelp and the web. Most of the heavy
lifting is done by packages like yelp-xsl and itstool. This package just
wraps things up in a developer-friendly way.

%prep
%autosetup -p1 -n %{name}-%{tarball_version}

%build
%meson
%meson_build

%install
%meson_install

%files
%doc AUTHORS README.md NEWS
%license COPYING COPYING.GPL
%{_bindir}/yelp-build
%{_bindir}/yelp-check
%{_bindir}/yelp-new
%{_datadir}/yelp-tools
%{_datadir}/aclocal/yelp.m4

%changelog
* Thu Jan 23 2025 Archana Shettigar <v-shettigara@microsoft.com> - 42.1-7
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License Verified

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 42.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Feb 12 2024 Tomas Popela <tpopela@redhat.com> - 42.1-5
- Build for the SPDX license format change

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 42.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 42.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 42.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Oct 31 2022 David King <amigadave@amigadave.com> - 42.1-1
- Update to 42.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 42.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Mar 19 2022 David King <amigadave@amigadave.com> - 42.0-1
- Update to 42.0

* Mon Feb 14 2022 David King <amigadave@amigadave.com> - 42~beta-1
- Update to 42.beta

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 41.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Sep 18 2021 Kalev Lember <klember@redhat.com> - 41.0-1
- Update to 41.0

* Thu Aug 19 2021 Kalev Lember <klember@redhat.com> - 41~beta-1
- Update to 41.beta

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar 22 2021 Kalev Lember <klember@redhat.com> - 40.0-1
- Update to 40.0

* Mon Mar 15 2021 Kalev Lember <klember@redhat.com> - 40~rc-1
- Update to 40.rc

* Tue Feb 23 2021 David King <amigadave@amigadave.com> - 40~beta-2
- Add Requires on python3-lxml (#1932011)

* Thu Feb 18 2021 Kalev Lember <klember@redhat.com> - 40~beta-1
- Update to 40.beta
- Switch to meson build system

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.38.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Sep 12 2020 Kalev Lember <klember@redhat.com> - 3.38.0-1
- Update to 3.38.0

* Mon Aug 17 2020 Kalev Lember <klember@redhat.com> - 3.37.90-1
- Update to 3.37.90

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 20 2019 David King <amigadave@amigadave.com> - 3.32.2-2
- Add xsltproc to Requires

* Wed Jun 12 2019 Kalev Lember <klember@redhat.com> - 3.32.2-1
- Update to 3.32.2

* Tue May 07 2019 Kalev Lember <klember@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Mon Feb 04 2019 David King <amigadave@amigadave.com> - 3.31.90-1
- Update to 3.31.90

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Tue Mar 06 2018 Kalev Lember <klember@redhat.com> - 3.27.90-1
- Update to 3.27.90

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Apr 26 2016 David King <amigadave@amigadave.com> - 3.18.0-3
- Add Requires on mallard-rng for schemas

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0
- Use make_install macro

* Mon Jul 20 2015 David King <amigadave@amigadave.com> - 3.17.4-1
- Update to 3.17.4

* Mon Jun 29 2015 David King <amigadave@amigadave.com> - 3.17.3-1
- Update to 3.17.3

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 David King <amigadave@amigadave.com> - 3.16.1-1
- Update to 3.16.1
- Use license macro for COPYING and COPYING.GPL

* Mon Oct 13 2014 David King <amigadave@amigadave.com> - 3.14.1-1
- Update to 3.14.1

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Tue Jul 01 2014 David King <amigadave@amigadave.com> - 3.13.3-2
- Tidy spec file

* Tue Jun 24 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-1
- Update to 3.13.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Richard Hughes <rhughes@redhat.com> - 3.12.1-1
- Update to 3.12.1

* Tue Mar 25 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Mon Feb 03 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Mon Nov 25 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.1-1
- Update to 3.9.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Depend on itstool and xmllint, which are required by yelp.m4

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.4-1
- Update to 3.3.4

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> 3.1.7-1
- Update to 3.1.7

* Wed Sep 07 2011 Kalev Lember <kalevlember@gmail.com> 3.1.6-1
- Update to 3.1.6

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> 3.1.5-1
- Update to 3.1.5

* Thu Jun 16 2011 Zeeshan Ali <zeenix@redhat.com> 3.1.4-1
- Initial release.
