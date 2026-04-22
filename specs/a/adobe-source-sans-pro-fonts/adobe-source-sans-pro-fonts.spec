# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Version:        3.052
Release: 8%{?dist}
URL:            https://github.com/adobe-fonts/source-sans

%global foundry adobe
%global fontlicense OFL-1.1
%global fontlicenses LICENSE.md
%global fontdocs README.md
%global fontdocsex %{fontlicenses}

%global fontfamily Source Sans Pro
%global fontsummary A set of OpenType fonts designed for user interfaces
%global fonts OTF/*.otf
%global fontconfs %{SOURCE10}
%global fontdescription %{expand:Source Sans is a set of OpenType fonts that have been designed to work well in
user interface (UI) environments, as well as in text setting for screen and
print.}

Source0:        %{url}/archive/%{version}R/%{fontpkgname}-%{version}.tar.gz
# Adjust as necessary. Keeping the filename in sync with the package name is a good idea.
# See the fontconfig templates in fonts-rpm-templates for information on how to
# write good fontconfig files and choose the correct priority [number].
Source10:       63-%{fontpkgname}.conf

%fontpkg


%prep
%autosetup -n source-sans-%{version}R


%build
%fontbuild


%install
%fontinstall


%check
%fontcheck


%fontfiles


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.052-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 25 2025 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.052-6
- Fix FTBFS thanks to @mavit (RHBZ #2339874)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.052-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.052-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.052-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.052-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Sep 24 2023 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.052-1
- Update to 3.052

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.046-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.046-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.046-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.046-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.046-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.046-1
- Update to 3.046

* Thu Jul 01 2021 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.042-1
- Update to 3.042

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.028-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 08 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.028-1
- Migrate to new font packaging scheme
- Update to 3.028

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.006-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 18 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 3.006-1
- Update to 3.006

* Fri Aug 09 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.045-1
- Update to 2.0.45

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.020-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.020-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.020-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.020-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 17 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.020-1
- Update to 2.020
- Update upstream URL
- Comply with latest packaging guidelines

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.050-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.050-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.050-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.050-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 15 2014 Richard Hughes <richard@hughsie.com> - 1.050-4
- Add a MetaInfo file for the software center; this is a font we want to show.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.050-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.050-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Alexis Lameire <alexisis-pristontale@hotmail.com> - 1.050-1
- update to 1.050-1 upstream release

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.034-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 29 2012 Alexis Lameire <alexisis-pristontale@hotmail.com> - 1.034-1
- update to 1.034-1 upstream release

* Wed Aug 15 2012 Alexis Lameire <alexisis-pristontale@hotmail.com> - 1.033-3
- Drop useless doc file Readme.html

* Sat Aug 04 2012 Alexis Lameire <alexisis-pristontale@hotmail.com> - 1.033-2
- use versionned source

* Fri Aug 03 2012 Alexis Lameire <alexisis-pristontale@hotmail.com> - 1.033-1
- initial release
