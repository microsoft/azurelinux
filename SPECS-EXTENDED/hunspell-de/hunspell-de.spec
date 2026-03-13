Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:          hunspell-de
Summary:       German hunspell dictionaries
Version:       20240224
Release:       1%{?dist}

License:       GPL-2.0-only OR GPL-3.0-only
URL:           https://cgit.freedesktop.org/libreoffice/dictionaries/tree/de
# ./make_source.sh
Source0:       dict-de-%{version}.tar.xz
BuildArch:     noarch

Requires: hunspell-filesystem
Supplements: (hunspell and langpacks-de)

%description
German (Germany, Switzerland, etc.) hunspell dictionaries.

%prep
%autosetup -p1 -n dict-de-%{version}


%build
# Nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/hunspell

install -pm 0644 de_AT_frami.aff %{buildroot}%{_datadir}/hunspell/de_AT.aff
install -pm 0644 de_AT_frami.dic %{buildroot}%{_datadir}/hunspell/de_AT.dic

install -pm 0644 de_CH_frami.aff %{buildroot}%{_datadir}/hunspell/de_CH.aff
install -pm 0644 de_CH_frami.dic %{buildroot}%{_datadir}/hunspell/de_CH.dic
install -pm 0644 de_DE_frami.aff %{buildroot}%{_datadir}/hunspell/de_LI.aff
install -pm 0644 de_DE_frami.dic %{buildroot}%{_datadir}/hunspell/de_LI.dic

install -pm 0644 de_DE_frami.aff %{buildroot}%{_datadir}/hunspell/de_DE.aff
install -pm 0644 de_DE_frami.dic %{buildroot}%{_datadir}/hunspell/de_DE.dic
install -pm 0644 de_DE_frami.aff %{buildroot}%{_datadir}/hunspell/de_BE.aff
install -pm 0644 de_DE_frami.dic %{buildroot}%{_datadir}/hunspell/de_BE.dic
install -pm 0644 de_DE_frami.aff %{buildroot}%{_datadir}/hunspell/de_LU.aff
install -pm 0644 de_DE_frami.dic %{buildroot}%{_datadir}/hunspell/de_LU.dic


%files
%doc README_de_DE_frami.txt README_extension_owner.txt
%license COPYING_GPLv2 COPYING_GPLv3
%{_datadir}/hunspell/*


%changelog
* Tue Mar 18 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 20240224-1
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20240224-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 24 2024 Sandro Mani <manisandro@gmail.com> - 20240224-1
- Pull dictionaries from libreoffice git

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20161207-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20161207-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20161207-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20161207-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20161207-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 22 2022 Parag Nemade <pnemade AT redhat DOT com> - 20161207-3
- Add conditional for new hunspell dir path and update to Requires:
  hunspell-filesystem

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20161207-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 04 2022 Sandro Mani <manisandro@gmail.com> - 20161207-1
- Modernize spec
- Set an actual version

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161207-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161207-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161207-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161207-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161207-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161207-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161207-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Michael Stahl <mstahl@redhat.com> - 0.20161207-1
- Resolves: rhbz#1549640 upgrade to latest release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20160407-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20160407-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20160407-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jul 20 2016 Michael Stahl <mstahl@redhat.com> - 0.20160407-1
- Resolves: rhbz#1344662 upgrade to latest release
- switch source URL to https
- revert the GNU grep 2.23 LANG=C bug workaround
- added explicit build dependency on perl, now required on rawhide

* Fri Apr 01 2016 Michael Stahl <mstahl@redhat.com> - 0.20151222-4
- Resolves: rhbz#1316359 grep 2.23 broke the build

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20151222-3
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20151222-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Michael Stahl <mstahl@redhat.com> - 0.20151222-1
- upgrade to latest version
- upstream removed "OASIS distribution license agreement 0.1", only GPLv2/v3 now
- remove needless use of percent-defattr

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20131206-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20131206-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 10 2014 Michael Stahl <mstahl@redhat.com> - 0.20131206-1
- latest version
- sed refuses to execute bin/dic2iso and iso2dic unless run in ISO8859 locale

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20120607-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20120607-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20120607-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120607-1
- latest version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110609-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 09 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110609-1
- latest version

* Mon Mar 21 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110321-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100727-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 30 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100727-1
- latest version

* Thu Oct 08 2009 Caolán McNamara <caolanm@redhat.com> - 0.20091006-1
- latest version
- drop integrated igerman98-20090107-useaspell.patch

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090107-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090107-3
- tidy spec

* Thu Apr 23 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090107-2
- fix dictionaries

* Thu Feb 26 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090107-1
- latest version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20071211-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 11 2007 Caolán McNamara <caolanm@redhat.com> - 0.20071211-1
- latest version

* Thu Aug 30 2007 Caolán McNamara <caolanm@redhat.com> - 0.20070829-1
- latest version
- build from canonical source

* Fri Aug 03 2007 Caolán McNamara <caolanm@redhat.com> - 0.20051213-2
- clarify license version

* Thu Dec 07 2006 Caolán McNamara <caolanm@redhat.com> - 0.20051213-1
- initial version