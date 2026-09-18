# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: mythes-eo
Summary: Esperanto thesaurus
%global upstreamid 20180330
Version: 0.%{upstreamid}
Release: 17%{?dist}
Source: http://esperanto.mv.ru/Download/dict-eo.oxt
URL: http://esperanto.mv.ru/Download/
License: GPL-3.0-or-later
BuildArch: noarch

%description
Esperanto thesaurus.

%package -n hyphen-eo
Summary: Esperanto hyphen rules
Requires: hyphen
Supplements: (hyphen and langpacks-eo)

%description -n hyphen-eo
Esperanto hyphenation rules.

%prep
%autosetup -c

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hyphen
cp -p dictionaries/hyph_eo.dic $RPM_BUILD_ROOT/%{_datadir}/hyphen/

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mythes
cp -p dictionaries/th_eo.dat $RPM_BUILD_ROOT/%{_datadir}/mythes/th_eo.dat
cp -p dictionaries/th_eo.idx $RPM_BUILD_ROOT/%{_datadir}/mythes/th_eo.idx

%files
%doc description/desc_en.txt
%license licenses/license-en.txt
%{_datadir}/mythes/*

%files -n hyphen-eo
%doc description/desc_en.txt
%license licenses/license-en.txt
%{_datadir}/hyphen/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 23 2023 Caolán McNamara <caolanm@redhat.com> - 0.20180330-11
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180330-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Nov 23 2018 Carmen Bianca Bakker <carmen@carmenbianca.eu> - 0.20180330-2
- Renamed from super-eo to mythes-eo.
- Minor fixes according to package reviews.

* Wed Oct 31 2018 Carmen Bianca Bakker <carmen@carmenbianca.eu> - 0.20180330-1
- Initial package

