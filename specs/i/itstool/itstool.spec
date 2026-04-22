# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           itstool
Version:        2.0.7
Release: 12%{?dist}
Summary:        ITS-based XML translation tool

License:        GPL-3.0-or-later
URL:            http://itstool.org/
Source0:        http://files.itstool.org/itstool/%{name}-%{version}.tar.bz2
# See:  https://github.com/itstool/itstool/issues/25
Patch0:         https://sources.debian.org/data/main/i/itstool/2.0.5-2/debian/patches/fix_crash_912099.patch#/%{name}-2.0.5-fix-crash-wrong-encoding.patch
# Filed upstream at https://github.com/itstool/itstool/pull/51
Patch1:         0001-Fix-insufficiently-quoted-regular-expressions.patch

BuildArch:      noarch

BuildRequires:  python3-libxml2
BuildRequires:  python3-devel
BuildRequires: make
Requires:       python3-libxml2

%description
ITS Tool allows you to translate XML documents with PO files, using rules from
the W3C Internationalization Tag Set (ITS) to determine what to translate and
how to separate it into PO file messages.

%prep
%setup -q
%patch -P0 -p1 -b .encoding
%patch -P1 -p1 -b .py312-regex

%build
export PYTHON=%{__python3}
%configure
%make_build

%install
%make_install

%files
%license COPYING COPYING.GPL3
%doc NEWS
%{_bindir}/itstool
%{_datadir}/itstool
%{_mandir}/man1/itstool.1*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 09 2023 Nils Philippsen <nils@tiptoe.de> - 2.0.7-6
- Fix insufficiently quoted regular expressions which caused excessive warnings
  with Python 3.12

* Mon Aug 21 2023 Parag Nemade <pnemade AT fedoraproject DOT org> - 2.0.7-5
- Migrate to SPDX license expression

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Feb 16 2022 Shaun McCance <shaunm@redhat.com> - 2.0.7-1
- Update to 2.0.7

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Apr 07 2019 Kalev Lember <klember@redhat.com> - 2.0.6-1
- Update to 2.0.6

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 06 2019 Björn Esser <besser82@fedoraproject.org> - 2.0.5-2
- Add a patch from Debian to fix wrong encoding of output message

* Tue Dec 04 2018 Kalev Lember <klember@redhat.com> - 2.0.5-1
- Update to 2.0.5
- Use make_build and make_install macros

* Mon Jul 16 2018 Charalampos Stratakis <cstratak@redhat.com> - 2.0.4-4
- Fix libxml2 related segfaults

* Mon Jul 16 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.4-3
- Switch to Python 3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Kalev Lember <klember@redhat.com> - 2.0.4-1
- Update to 2.0.4
- Use license macro for COPYING

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.0.2-9
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Mon Feb 05 2018 Petr Viktorin <pviktori@redhat.com> - 2.0.2-8
- Be more explicit about Python build dependencies
  (Require python2-devel, tell autotools that PYTHON is python2)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Merlin Mathesius <mmathesi@redhat.com> - 2.0.2-5
- Add BuildRequires: python to fix FTBFS (BZ#1414545).

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 17 2014 Kalev Lember <kalevlember@gmail.com> - 2.0.2-1
- Update to 2.0.2

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 02 2012 Kalev Lember <kalevlember@gmail.com> 1.2.0-1
- Update to 1.2.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> 1.1.2-1
- Update to itstool 1.1.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 19 2011 Shaun McCance <shaunm@gnome.org> 1.1.1-1
- Update to itstool 1.1.1

* Sun Aug 07 2011 Rahul Sundaram <sundaram@fedoraproject.org> 1.1.0-2
- Add requires on libxml2-python since itstool uses it
- Drop redundant defattr
- Add NEWS to doc

* Mon Jun 27 2011 Shaun McCance <shaunm@gnome.org> 1.1.0-1
- Update to itstool 1.1.0

* Sun May 8 2011 Shaun McCance <shaunm@gnome.org> 1.0.1-1
- Initial packaging
