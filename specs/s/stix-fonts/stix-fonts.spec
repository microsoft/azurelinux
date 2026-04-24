# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT
%global forgeurl https://github.com/stipub/stixfonts/
Version: 2.13b171
%forgemeta

Release: 10%{?dist}
URL:     http://www.stixfonts.org/

%global foundry           STIX
%global fontlicense       OFL-1.1
%global fontlicenses      OFL.txt
%global fontdocs          README.md FONTLOG.txt
%global fontdocsex        %{fontlicenses}

%global fontfamily        STIX
%global fontsummary       STIX, a scientific and engineering font family
%global fontpkgheader     %{expand:
Obsoletes: stix-math-fonts < %{version}-%{release}
}
%global fonts             fonts/static_otf/STIXTwoText*otf fonts/static_otf/STIXTwoMath*otf
%global fontconfngs       %{SOURCE10}
%global fontdescription   %{expand:
The mission of the Scientific and Technical Information Exchange (STIX) font
creation project is the preparation of a comprehensive set of fonts that serve
the scientific and engineering community in the process from manuscript
creation through final publication, both in electronic and print formats.
}


Source0:  %{forgesource0}
Source10: 65-%{fontpkgname0}.xml

%fontpkg -a

%package doc
Summary:   Optional documentation files of %{source_name}
BuildArch: noarch
%description doc
This package provides optional documentation files shipped with
%{source_name}.

%prep
%forgesetup

%build
%fontbuild -a

%install
%fontinstall -a

%check
%fontcheck -a

%fontfiles -a

%files doc
%doc docs/*pdf docs/*xlsx

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.13b171-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.13b171-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13b171-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue May 21 2024 Akira TAGOH <tagoh@redhat.com> - 2.13b171-6
- Update License field to SPDX

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13b171-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.13b171-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.13b171-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13b171-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 07 2022 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 2.13b171-1
- New upstream release 2.13b171 (rhbz#1909251)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 11 2020 Parag Nemade <pnemade AT redhat DOT com>
- 2.0.2-8
- Fix this spec file to build for F33+

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 27 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.0.2-6
🐞 Workaround Fedora problems created by rpm commit 93604e2

* Thu Apr 02 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.0.2-5
💥 Actually rebuild with fonts-rpm-macros 2.0.4 to make sure fontconfig files are
  valid

* Thu Apr 02 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.0.2-4
👻 Rebuild with fonts-rpm-macros 2.0.4 to make sure fontconfig files are valid

* Mon Mar 02 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.0.2-3
✅ Lint, lint, lint and lint again

* Sat Feb 22 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.0.2-2
✅ Rebuild with fonts-rpm-macros 2.0.2

* Sat Feb 15 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.0.2-1
✅ Convert to fonts-rpm-macros use

* Thu Nov 1 2007 Nicolas Mailhot <nim@fedoraproject.org>
- 0.9-4
✅ Initial packaging
