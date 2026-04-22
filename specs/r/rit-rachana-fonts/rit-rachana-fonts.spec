# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT
Version:    1.5.2
Release: 5%{?dist}
URL:        https://gitlab.com/rit-fonts/%{fontsource}

%global foundry        RIT
%global fontlicense    OFL-1.1
%global fontlicenses   fonts/LICENSE.txt
%global fontdocs       fonts/*.md

%global fontfamily     RIT Rachana
%global fontsource     RIT-Rachana
%global fontsummary    OpenType font for Malayalam traditional script

%global fonts          fonts/otf/*.otf
%global fontconfs      fonts/65-0-rit-rachana-fonts.conf
%global fontappstreams fonts/in.org.rachana.rit-rachana.metainfo.xml

%global fontdescription %{expand:
RIT Rachana is OpenType font for Malayalam traditional script designed by Hussain K H.
It covers Unicode 13.0 and entire character set in 'definitive character set' of Malayalam. 
}

# https://gitlab.com/rit-fonts/%%{fontsource}/-/jobs/artifacts/%%{version}/download?job=build-tag
Source0:    %{fontsource}-%{version}.zip

%fontpkg

%prep
%setup -qc

%build
%fontbuild

%install
%fontinstall

%check
%fontcheck

%fontfiles


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Rajeesh KV <rajeeshknambiar@gmail.com> - 1.5.2-2
- Fix RHBZ#2338102, use `zip` file of prebuilt fonts

* Sun Jan 12 2025 Rajeesh KV <rajeeshknambiar@gmail.com> - 1.5.2-1
- Bugfix update, version 1.5.2

* Sun Aug 25 2024 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.5.1-1
- New release 1.5.1

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Parag Nemade <pnemade AT redhat DOT com> - 1.5.0-1
- Previous build packaged only otf and xml files but not docs and conf files
  Let's rebuild this to make sure all packaged files available for installation

* Sun Jul 07 2024 Rajeesh K V <rajeeshknambiar@fedoraproject.org> - 1.5.0-0
- New upstream version 1.5.0
- Use prebuilt binary fonts instead of building from source
- Fixes RHBZ #2293815

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.4.7-2
- Fix typo: RHBZ #2258579

* Sat Jan 06 2024 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.4.7-1
- Bugfix update, version 1.4.7

* Sat Sep 30 2023 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.4.6-1
- Bugfix update, version 1.4.6

* Sun Sep 03 2023 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.4.5-1
- Bugfix update, version 1.4.5

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 18 2023 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.4.4-1
- Bugfix update, version 1.4.4

* Wed May 10 2023 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.4.3-1
- Bugfix update, version 1.4.3

* Sat Feb 18 2023 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.4.2-1
- Bugfix update, version 1.4.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Nov 27 2022 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.4.1-1
- New version with many improvements (Unicode 15.0, size reduction, shaping...)
- Spec update for SPDX license tag

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Feb 06 2022 Rajeesh K V <rajeeshknambiar@gmail.com> - 1.3.1-1
- New bugfix release 1.3.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Rajeesh KV <rajeeshknambiar@fedoraproject.org> - 1.3-2
- Address review comments on RHBZ#2031365

* Mon Dec 06 2021 Rajeesh KV <rajeeshknambiar@fedoraproject.org> - 1.3-1
- Obsoletes SMC Rachana fonts

* Sun Oct 10 2021 Rajeesh KV <rajeeshknambiar@fedoraproject.org> - 1.3-0
- New upstream release 1.3

* Fri Jun 25 2021 Rajeesh KV <rajeeshknambiar@fedoraproject.org> - 1.2-0
- New upstream release 1.2

* Thu Dec 17 2020 Rajeesh KV <rajeeshknambiar@fedoraproject.org> - 1.1-0
- Initial packaging
