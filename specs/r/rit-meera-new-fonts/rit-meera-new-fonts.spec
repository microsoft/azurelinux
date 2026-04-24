# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT
Version:    1.6.2
Release: 5%{?dist}
URL:        https://gitlab.com/rit-fonts/%{fontsource}

Patch1:     %{name}-add-monospace-fallback.patch

%global foundry         RIT
%global fontlicense     OFL-1.1
%global fontlicenses    fonts/LICENSE.txt
%global fontdocs        fonts/*.md

%global fontfamily      Meera New
%global fontsource      MeeraNew
%global fontsummary     OpenType sans-serif font for Malayalam traditional script

%global fonts           fonts/otf/*.otf
%global fontconfs       fonts/65-meera-new-fonts.conf
%global fontappstreams  fonts/in.org.rachana.meera-new.metainfo.xml

%global fontdescription %{expand:
MeeraNew is a sans-serif font for Malayalam traditional script designed\
by KH Hussain and developed by Rachana Institute of Typography.
}


# https://gitlab.com/rit-fonts/%%{fontsource}/-/jobs/artifacts/%%{version}/download?job=build-tag
Source0:    %{fontsource}-%{version}.zip

%fontpkg

%prep
%setup -qc
%patch -P1 -p1

%build
%fontbuild

%install
%fontinstall

%check
%fontcheck

%fontfiles


%changelog
* Thu Jul 31 2025 Akira TAGOH <tagoh@redhat.com> - 1.6.2-4
- Add fallback rule of monospace.
  See https://fedoraproject.org/wiki/Changes/SetDefaultMonospaceFallbackFont

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Aug 25 2024 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.6.2-1
- New release 1.6.2

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 12 2024 Rajeesh KV <rajeeshknambiar@gmail.com> - 1.6.1-0
- Fix name in fontconfig

* Sun Jul 07 2024 Rajeesh K V <rajeeshknambiar@fedoraproject.org> - 1.6-0
- New upstream version 1.6
- Use prebuilt binary fonts instead of building from source

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Sep 30 2023 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.5.2-1
- New release, version 1.5.2

* Tue Aug 22 2023 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.5.1-2
- Change fontconfig priority from 67 to 65

* Sun Aug 20 2023 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.5.1-1
- New release, version 1.5.1

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Nov 27 2022 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.4.1-1
- New version 1.4.1 with many improvements
- SPDX license

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun May 15 2022 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.3-1
- New version improving x-height to match RIT Rachana and many kerning pairs

* Mon Feb 07 2022 Stephen Gallagher <sgallagh@redhat.com> - 1.2.1-2
- Fix Obsoletes: smc-meera-fonts

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Rajeesh KV <rajeeshknambiar@fedoraproject.org> - 1.2.1-0
- New release
- Address comments at RHBZ#2031370

* Mon Dec 06 2021 Rajeesh KV <rajeeshknambiar@fedoraproject.org> - 1.2-1
- Obsoletes SMC Meera fonts

* Sun Dec 05 2021 Rajeesh KV <rajeeshknambiar@fedoraproject.org> - 1.2-0
- Update to new upstream release
- Major improvements to OpenType layoutt rules

* Fri Jan 01 2021 Rajeesh KV <rajeeshknambiar@fedoraproject.org> - 1.0-0
- Initial packaging
