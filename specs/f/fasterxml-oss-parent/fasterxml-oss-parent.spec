# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname oss-parent

Name:          fasterxml-oss-parent
Version:       62
Release:       4%{?dist}
Summary:       FasterXML parent pom
License:       Apache-2.0

URL:           https://github.com/FasterXML/oss-parent
Source0:       %{url}/archive/%{srcname}-%{version}.tar.gz

BuildRequires: maven-local-openjdk25
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.codehaus.mojo:build-helper-maven-plugin)

BuildArch:     noarch
%if 0%{?fedora} || 0%{?rhel} >= 10
ExclusiveArch:  %{java_arches} noarch
%endif

%description
FasterXML is the business behind the Woodstox streaming XML parser,
Jackson streaming JSON parser, the Aalto non-blocking XML parser, and
a growing family of utility libraries and extensions.

FasterXML offers consulting services for adoption, performance tuning,
and extension.

This package contains the parent pom file for FasterXML.com projects.

%prep
%setup -q -n %{srcname}-%{srcname}-%{version}

# Stuff unnecessary for RPM builds
%pom_remove_plugin :jacoco-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-pmd-plugin
%pom_remove_plugin :maven-scm-plugin
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :jdepend-maven-plugin
%pom_xpath_remove "pom:build/pom:extensions"

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.creole
%license LICENSE NOTICE

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 62-4
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Packit <hello@packit.dev> - 62-1
- Update to version 62
- Resolves: rhbz#2336494

* Tue Aug 27 2024 Chris Kelley <ckelley@redhat.com> - 61-1
- Remove %pom_remove_plugin of taglist-maven-plugin

* Tue Aug 27 2024 Packit <hello@packit.dev> - 61-1
- Update to version 61
- Resolves: rhbz#2308074

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 60-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Packit <hello@packit.dev> - 60-1
- Update to version 60
- Resolves: rhbz#2295465

* Tue Apr 30 2024 Chris Kelley <ckelley@redhat.com> - 59-1
- Update to version 59

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 58-2
- Rebuilt for java-21-openjdk as system jdk

* Mon Feb 19 2024 Packit <hello@packit.dev> - 58-1
- [maven-release-plugin] prepare release oss-parent-58 (Tatu Saloranta)
- Add property `version.junit5` (at 5.10.2) (Tatu Saloranta)
- ... (Tatu Saloranta)
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- Resolves rhbz#2265008

* Sat Feb 10 2024 Packit <hello@packit.dev> - 57-1
- [maven-release-plugin] prepare release oss-parent-57 (Tatu Saloranta)
- Prepare for v57 release (Tatu Saloranta)
- Update release notes (Tatu Saloranta)
- Bump version.plugin.surefire from 3.2.3 to 3.2.5 (dependabot[bot])
- Bump org.apache.maven.plugins:maven-jxr-plugin from 3.3.1 to 3.3.2 (dependabot[bot])
- Update release notes wrt `version.plugin.compiler` bump (Tatu Saloranta)
- Bump org.apache.maven.plugins:maven-compiler-plugin (dependabot[bot])
- Update release notes (Tatu Saloranta)
- Bump org.apache.maven.plugins:maven-compiler-plugin (dependabot[bot])
- Update release notes wrt #115 (Tatu Saloranta)
- Bump version.plugin.surefire from 3.2.2 to 3.2.3 (dependabot[bot])
- Update release notes (Tatu Saloranta)
- Bump org.codehaus.mojo:build-helper-maven-plugin from 3.4.0 to 3.5.0 (dependabot[bot])
- Bump org.jacoco:jacoco-maven-plugin from 0.8.10 to 0.8.11 (dependabot[bot])
- Update release notes (Tatu Saloranta)
- Bump org.apache.maven.plugins:maven-project-info-reports-plugin (dependabot[bot])
- Update release notes (Tatu Saloranta)
- Bump org.apache.maven.plugins:maven-javadoc-plugin from 3.6.0 to 3.6.2 (dependabot[bot])
- Bump version.plugin.surefire from 3.2.1 to 3.2.2 (dependabot[bot])
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- Resolves rhbz#2263613

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 56-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 07 2023 Packit <hello@packit.dev> - 56-1
- [maven-release-plugin] prepare release oss-parent-56 (Tatu Saloranta)
- Upgrade `version.plugin.moditect` to 1.1.0 (from 1.0.0-Final) (Tatu Saloranta)
- Update release notes (Tatu Saloranta)
- Bump org.apache.maven.plugins:maven-pmd-plugin from 3.21.0 to 3.21.2 (dependabot[bot])
- Update release notes (Tatu Saloranta)
- Bump org.apache.maven.plugins:maven-clean-plugin from 3.3.1 to 3.3.2 (dependabot[bot])
- Update release notes wrt 3 plugin updates via dependabot PRs. (Tatu Saloranta)
- Bump org.apache.maven.plugins:maven-jxr-plugin from 3.3.0 to 3.3.1 (dependabot[bot])
- Bump version.plugin.surefire from 3.1.2 to 3.2.1 (dependabot[bot])
- Bump org.apache.maven.plugins:maven-dependency-plugin (dependabot[bot])
- update release notes (Tatu Saloranta)
- Bump org.apache.maven.plugins:maven-site-plugin (dependabot[bot])
- Update release notes x (Tatu Saloranta)
- Bump org.ow2.asm:asm from 9.5 to 9.6 (dependabot[bot])
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)
- Resolves rhbz#2248436

* Tue Sep 26 2023 Packit <hello@packit.dev> - 55-1
- [maven-release-plugin] prepare release oss-parent-55 (Tatu Saloranta)
- Prepare for releasing v55 (Tatu Saloranta)
- Bump org.apache.maven.plugins:maven-shade-plugin from 3.5.0 to 3.5.1 (dependabot[bot])
- Bump org.apache.maven.plugins:maven-javadoc-plugin from 3.5.0 to 3.6.0 (dependabot[bot])
- Bump org.apache.maven.plugins:maven-enforcer-plugin from 3.3.0 to 3.4.1 (dependabot[bot])
- Bump maven-site-plugin from 4.0.0-M8 to 4.0.0-M9 (dependabot[bot])
- Update Maven for wrapper (Tatu Saloranta)
- Update release notes (Tatu Saloranta)
- Bump maven-clean-plugin from 3.2.0 to 3.3.1 (dependabot[bot])
- Update release notes (Tatu Saloranta)
- Bump maven-shade-plugin from 3.4.1 to 3.5.0 (dependabot[bot])
- update release notes (Tatu Saloranta)
- Bump version.plugin.surefire from 3.1.0 to 3.1.2 (dependabot[bot])
- Bump maven-project-info-reports-plugin from 3.4.4 to 3.4.5 (dependabot[bot])
- Update release notes (Tatu Saloranta)
- Bump maven-release-plugin from 3.0.0 to 3.0.1 (dependabot[bot])
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 01 2023 Chris Kelley <ckelley@redhat.com> - 54-1
- [maven-release-plugin] prepare release oss-parent-54 (Tatu Saloranta)
- Release 54 (Tatu Saloranta)
- ... (Tatu Saloranta)
- Update release notes (Tatu Saloranta)
- Bump maven-project-info-reports-plugin from 3.4.3 to 3.4.4 (dependabot[bot])
- Bump maven-enforcer-plugin from 3.2.1 to 3.3.0 (dependabot[bot])
- Bump maven-install-plugin from 3.1.0 to 3.1.1 (dependabot[bot])
- [maven-release-plugin] prepare for next development iteration (Tatu Saloranta)

* Tue May 23 2023 Chris Kelley <ckelley@redhat.com> - 53-1
- Update to version 53

* Mon May 22 2023 Chris Kelley <ckelley@redhat.com> - 52-1
- Update to version 52

* Tue May 09 2023 Chris Kelley <ckelley@redhat.com> - 51-1
- Update to version 51

* Mon Mar 06 2023 Chris Kelley <ckelley@redhat.com> - 50-1
- Update to version 50

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 23 2022 Chris Kelley <ckelley@redhat.com> - 49-1
- Update to version 49

* Tue Nov 08 2022 Chris Kelley <ckelley@redhat.com> - 48-1
- Update to version 48
- Update to use SPDX licence

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 41-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 41-6
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 41-5
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 16 2020 Fabio Valentini <decathorpe@gmail.com> - 41-1
- Update to version 41.

* Mon Aug 10 2020 Fabio Valentini <decathorpe@gmail.com> - 40-1
- Update to version 40.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 38-3
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 05 2019 Fabio Valentini <decathorpe@gmail.com> - 38-1
- Update to version 38.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 20 2019 Mat Booth <mat.booth@redhat.com> - 34-1
- Update to latest upstream version

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 26-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 07 2017 Michael Simacek <msimacek@redhat.com> - 26-5
- Fix license tag

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Michael Simacek <msimacek@redhat.com> - 26-2
- Remove site-plugin from build

* Mon Aug 22 2016 gil cattaneo <puntogil@libero.it> 26-1
- update to 26

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Oct 25 2015 gil cattaneo <puntogil@libero.it> 24-2
- disable maven-enforcer-plugin support

* Mon Sep 28 2015 gil cattaneo <puntogil@libero.it> 24-1
- update to 24

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18e-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 31 2015 gil cattaneo <puntogil@libero.it> 18e-1
- update to 18e

* Wed Jul 02 2014 gil cattaneo <puntogil@libero.it> 16-2
- remove com.google.code.maven-replacer-plugin:replacer references 

* Wed Jul 02 2014 gil cattaneo <puntogil@libero.it> 16-1
- update to 16

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 11-3
- Rebuild to regenerate Maven auto-requires

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 gil cattaneo <puntogil@libero.it> 11-1
- update to 11

* Sat Jul 06 2013 gil cattaneo <puntogil@libero.it> 10-2
- switch to XMvn
- minor changes to adapt to current guideline

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 10-1
- update to 10

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 4-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Oct 24 2012 gil cattaneo <puntogil@libero.it> 4-1
- update to 4

* Thu Sep 13 2012 gil cattaneo <puntogil@libero.it> 3-1
- initial rpm
