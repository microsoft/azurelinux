# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _mintlibdir %{_prefix}/lib/linuxmint/

Name:           mintlocale
Version:        1.4.7
Release:        20%{?dist}
Summary:        Language selection tool

# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            https://github.com/linuxmint/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# Revert https://github.com/linuxmint/mintlocale/commit/0206bbf7c12058999e701bb11f9012be54da2cbb
# Using non utf8 breaks gnome apps
Patch0:         show_utf8_only.patch
Patch1:         %{url}/pull/56.patch#/add_apt_checking.patch
Patch2:         %{url}/commit/7041982b69fa9fea065098e7b33f306df1dcac91.patch#/fix_signal_name.patch
Patch3:         fix_gdk_import.patch

BuildArch:      noarch

BuildRequires:  desktop-file-utils

Requires:       accountsservice
Requires:       %{name}-set-default-locale = %{version}-%{release}
Requires:       xapps

%description
Language selection tool for Cinnamon.

%package set-default-locale
Summary:        Language selection tool

%description set-default-locale
Language selection tool for Cinnamon.


%prep
%autosetup -p1


%build
echo 'nothing to build'


%install
%{__cp} -pr .%{_prefix} %{buildroot}
%{__rm} %{buildroot}%{_bindir}/add-remove-locales \
  %{buildroot}%{_datadir}/applications/%{name}-im.desktop \
  %{buildroot}%{_mintlibdir}/mintlocale/add.py \
  %{buildroot}%{_mintlibdir}/mintlocale/install_remove.py
%{__chmod} -c 0755 %{buildroot}%{_mintlibdir}/mintlocale/mintlocale.py

echo 'LANG=$locale' > %{buildroot}%{_datadir}/linuxmint/mintlocale/templates/default_locale.template

%{_bindir}/desktop-file-install \
  --add-only-show-in=X-Cinnamon \
  --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%doc debian/changelog
%license COPYING debian/copyright
%{_bindir}/%{name}
%{_mintlibdir}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/linuxmint
%{_datadir}/polkit-1/actions/com.linuxmint.mintlocale.policy

%files set-default-locale
%{_bindir}/set-default-locale


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 1.4.7-18
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 12 2021 Leigh Scott <leigh123linux@gmail.com> - 1.4.7-9
- Fix (rhbz#1971037)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 02 2020 leigh123linux <leigh123linux@googlemail.com> - 1.4.7-6
- Fix rhbz#1819715

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.4.7-2
- Drop EPEL/RHEL support

* Thu Aug 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.4.7-1
- New upstream release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.4.5-1
- New upstream release

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 27 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.4.4-1
- New upstream release

* Mon Sep 11 2017 Björn Esser <besser82@fedoraproject.org> - 1.4.2-11
- Require xapps for iso-flag-png

* Thu Aug 31 2017 Björn Esser <besser82@fedoraproject.org> - 1.4.2-10
- Preserve mode of files when changing hashbang

* Thu Aug 31 2017 Björn Esser <besser82@fedoraproject.org> - 1.4.2-9
- Fix regex for EPEL

* Thu Aug 31 2017 Björn Esser <besser82@fedoraproject.org> - 1.4.2-8
- Fix hashbang in regex

* Tue Aug 29 2017 Björn Esser <besser82@fedoraproject.org> - 1.4.2-7
- Use Python2 on EPEL <= 7

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 09 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.4.2-5
- Remove the add and remove bits

* Tue May 09 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.4.2-4
- Split package (bz 1449122)
- Remove python3-devel build requires

* Tue May 09 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.4.2-3
- Show UTF8 Lang only

* Sun May 07 2017 Björn Esser <besser82@fedoraproject.org> - 1.4.2-2
- Fix template for system locale

* Sun May 07 2017 Björn Esser <besser82@fedoraproject.org> - 1.4.2-1
- New upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-0.9.gitfb4118d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Apr 28 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.1.6-0.8.gitfb4118d
- rebuilt for bz 1292296

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-0.7.gitfb4118d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 09 2015 Leigh Scott <leigh123linux@googlemail.com> - 1.1.6-0.6.gitfb4118d
- fix some deprecation warnings

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-0.5.gitfb4118d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Nov 08 2014 Leigh Scott <leigh123linux@googlemail.com> - 1.1.6-0.4.gitfb4118d
- fix locale path

* Fri Jun 27 2014 Leigh Scott <leigh123linux@googlemail.com> - 1.1.6-0.3.gitfb4118d
- only show in cinnamon menu

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-0.2.gitfb4118d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Leigh Scott <leigh123linux@googlemail.com> - 1.1.6-0.1.gitfb4118d
- update to the latest git snapshot

* Sat May 10 2014 Leigh Scott <leigh123linux@googlemail.com> - 1.1-4
- fix system wide settings

* Sat May 03 2014 Leigh Scott <leigh123linux@googlemail.com> - 1.1-3
- more fixes

* Sat May 03 2014 Leigh Scott <leigh123linux@googlemail.com> - 1.1-2
- fix ui so it looks better
- add pkexec support for setting system
  locale (needs group adm,sudo,wheel to show)

* Mon Apr 14 2014 Leigh Scott <leigh123linux@googlemail.com> - 1.1-1
- Inital build
