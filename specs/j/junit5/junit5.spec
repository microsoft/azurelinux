## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 5;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with bootstrap
# Component versions, taken from gradle.properties
%global platform_version 1.%(v=%{version}; echo ${v:2})
%global jupiter_version %{version}
%global vintage_version %{version}

Name:           junit5
Version:        5.13.3
Release:        %autorelease
Summary:        Java regression testing framework
License:        EPL-2.0
URL:            https://junit.org/junit5/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/junit-team/junit5/archive/r%{version}/junit5-%{version}.tar.gz
# Aggregator POM (used for packaging only)
Source100:      aggregator.pom
# Platform POMs
Source200:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-commons/%{platform_version}/junit-platform-commons-%{platform_version}.pom
Source201:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console/%{platform_version}/junit-platform-console-%{platform_version}.pom
Source202:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/%{platform_version}/junit-platform-console-standalone-%{platform_version}.pom
Source203:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-engine/%{platform_version}/junit-platform-engine-%{platform_version}.pom
Source205:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-launcher/%{platform_version}/junit-platform-launcher-%{platform_version}.pom
Source206:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-runner/%{platform_version}/junit-platform-runner-%{platform_version}.pom
Source207:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-suite-api/%{platform_version}/junit-platform-suite-api-%{platform_version}.pom
Source209:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-testkit/%{platform_version}/junit-platform-testkit-%{platform_version}.pom
Source210:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-suite-commons/%{platform_version}/junit-platform-suite-commons-%{platform_version}.pom
# Jupiter POMs
Source300:      https://repo1.maven.org/maven2/org/junit/jupiter/junit-jupiter/%{jupiter_version}/junit-jupiter-%{jupiter_version}.pom
Source301:      https://repo1.maven.org/maven2/org/junit/jupiter/junit-jupiter-api/%{jupiter_version}/junit-jupiter-api-%{jupiter_version}.pom
Source302:      https://repo1.maven.org/maven2/org/junit/jupiter/junit-jupiter-engine/%{jupiter_version}/junit-jupiter-engine-%{jupiter_version}.pom
Source303:      https://repo1.maven.org/maven2/org/junit/jupiter/junit-jupiter-migrationsupport/%{jupiter_version}/junit-jupiter-migrationsupport-%{jupiter_version}.pom
Source304:      https://repo1.maven.org/maven2/org/junit/jupiter/junit-jupiter-params/%{jupiter_version}/junit-jupiter-params-%{jupiter_version}.pom
# Vintage POM
Source400:      https://repo1.maven.org/maven2/org/junit/vintage/junit-vintage-engine/%{vintage_version}/junit-vintage-engine-%{vintage_version}.pom
# BOM POM
Source500:      https://repo1.maven.org/maven2/org/junit/junit-bom/%{version}/junit-bom-%{version}.pom

Patch:          0001-Drop-transitive-requirement-on-apiguardian.patch
Patch:          0002-Add-missing-module-static-requires.patch
Patch:          0003-Remove-legacy-XML-console-support.patch
Patch:          0004-Add-JRE-class-generated-from-template.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.univocity:univocity-parsers)
BuildRequires:  mvn(info.picocli:picocli)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apiguardian:apiguardian-api)
BuildRequires:  mvn(org.assertj:assertj-core)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.opentest4j:opentest4j)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-guide < 5.10.2-16
Obsoletes:      %{name}-javadoc < 5.10.2-16

%description
JUnit is a popular regression testing framework for Java platform.

%prep
%autosetup -p1 -C
find -name '*.jar' -delete


cp -p %{SOURCE100} pom.xml

for source in $(echo %{sources} | cut -d ' ' -f3-); do
  module=${source}
  module=${module##*/}
  module=${module%%-*}
  if [ -d ${module}/src/module ]; then
    mkdir -p ${module}/src/main/java
    mv -t ${module}/src/main/java ${module}/src/module/*/module-info.java
  fi
  cp -p ${source} ${module}/pom.xml
  %pom_add_parent org.fedoraproject.xmvn.junit5:aggregator:any ${module}
  # OSGi BSN
  bsn=org.${module//-/.}
  %pom_xpath_inject pom:project "<properties><osgi.bsn>${bsn}</osgi.bsn></properties>" ${module}
  # Incorrect scope - API guardian is just annotation, needed only during compilation
  %pom_xpath_set -f "pom:dependency[pom:artifactId='apiguardian-api']/pom:scope" provided ${module}
  %pom_xpath_set -f "pom:dependency[pom:scope='runtime']/pom:scope" compile ${module}
done

%pom_remove_parent junit-bom

# Add deps which are shaded by upstream and therefore not present in POMs.
%pom_add_dep org.junit.platform:junit-platform-commons:%{platform_version} junit-platform-console
%pom_add_dep org.junit.platform:junit-platform-launcher:%{platform_version} junit-platform-console
%pom_add_dep info.picocli:picocli junit-platform-console
%pom_add_dep com.univocity:univocity-parsers:2.5.4 junit-jupiter-params

%pom_disable_module junit-platform-console-standalone
%pom_remove_dep org.junit.platform:junit-platform-reporting junit-platform-console

%mvn_package :aggregator __noinstall

%build
%mvn_build -j -f

%install
%mvn_install

%jpackage_script org.junit.platform.console.ConsoleLauncher "" "" junit5:opentest4j:picocli:junit:hamcrest:univocity-parsers junit-platform-console

%files -f .mfiles
%{_bindir}/junit-platform-console
%license LICENSE.md NOTICE.md

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 5.13.3-5
- test: add initial lock files

* Fri Jan 23 2026 Marian Koncek <mkoncek@redhat.com> - 5.13.3-4
- Add missing univocity-parsers runtime launcher dependency

* Tue Jul 29 2025 Jiri Vanek <jvanek@redhat.com> - 5.13.3-3
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.13.3-1
- Update to upstream version 5.13.3

* Sun Jul 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.10.2-21
- Build with OpenJDK 25

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.10.2-20
- Switch javapackages test plan to f43 ref

* Wed Mar 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.10.2-19
- Switch to javapackages tests from CentOS Stream GitLab

* Tue Mar 11 2025 Marian Koncek <mkoncek@redhat.com> - 5.10.2-18
- Drop dependency on jopt-simple

* Mon Mar 10 2025 Marian Koncek <mkoncek@redhat.com> - 5.10.2-17
- Enable console launcher module

* Mon Mar 03 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.10.2-16
- Remove junit5-guide

* Mon Mar 03 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.10.2-15
- Remove javadoc subpackage

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 29 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.10.2-11
- Update javapackages test plan to f42

* Thu Sep 19 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.10.2-10
- Disable asciidoc generation

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 31 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.10.2-3
- Switch to a newer patch macro syntax

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 5.10.2-2
- Rebuilt for java-21-openjdk as system jdk

* Tue Feb 06 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.10.2-1
- Update to upstream version 5.10.2

* Thu Feb 01 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.10.1-1
- Update to upstream version 5.10.1

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 18 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.10.0-1
- Update to upstream version 5.10.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Feb 23 2023 Marian Koncek <mkoncek@redhat.com> - 5.9.0-3
- Enable module-info generation

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 07 2022 Marian Koncek <mkoncek@redhat.com> - 5.9.0-1
- Update to upstream version 5.9.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 22 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.8.2-1
- Update to upstream version 5.8.2

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 5.7.1-5
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.7.1-2
- Bootstrap build
- Non-bootstrap build

* Fri May 14 2021 Marian Koncek <mkoncek@redhat.com> - 5.7.1-1
- Update to upstream version 5.7.1

* Fri Feb 19 2021 Mat Booth <mat.booth@redhat.com> - 5.7.1-1
- Update to latest upstream release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Oct 24 2020 Fabio Valentini <decathorpe@gmail.com> - 5.7.0-1
- Update to version 5.7.0.

* Mon Sep 21 2020 Marian Koncek <mkoncek@redhat.com> - 5.7.0-1
- Update to upstream version 5.7.0

* Tue Aug 11 2020 Jerry James <loganjerry@gmail.com> - 5.6.2-4
- Add org.junit.jupiter:junit-jupiter, org.junit.platform:junit-platform-testkit

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Marian Koncek <mkoncek@redhat.com> - 5.6.2-1
- Update to upstream version 5.6.2

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 5.6.2-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Sat May 09 2020 Fabio Valentini <decathorpe@gmail.com> - 5.6.2-1
- Update to version 5.6.2.

* Wed Mar 04 2020 Marian Koncek <mkoncek@redhat.com> - 5.6.0-1
- Update to upstream version 5.6.0

* Mon Feb 17 2020 Alexander Scheel <ascheel@redhat.com> - 5.6.0-1
- Update to version 5.6.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.5.2-3
- Mass rebuild for javapackages-tools 201902

* Mon Oct 28 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.5.2-2
- Build and install junit-jupiter aggregator

* Sun Oct 13 2019 Fabio Valentini <decathorpe@gmail.com> - 5.5.2-1
- Update to version 5.5.2.

* Wed Sep 11 2019 Marian Koncek <mkoncek@redhat.com> - 5.5.2-1
- Update to upstream version 5.5.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Marian Koncek <mkoncek@redhat.com> - 5.5.1-1
- Update to upstream version 5.5.1

* Sat Jun 08 2019 Fabio Valentini <decathorpe@gmail.com> - 5.4.2-1
- Update to version 5.4.2

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.4.0-2
- Mass rebuild for javapackages-tools 201901

* Wed Mar 06 2019 Mat Booth <mat.booth@redhat.com> - 5.4.0-1
- Update to latest upstream release
- License switched to EPL only now the surefire provider was moved to the
  Apache Surefire project

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 11 2018 Mat Booth <mat.booth@redhat.com> - 5.3.1-1
- Update to latest upstream release
- Conditionally build the console modules
- Remove stuff for discontinued gradle plugin

* Fri Aug 31 2018 Severin Gehwolf <sgehwolf@redhat.com> - 5.2.0-3
- Add explicit requirement on javapackages-tools since junit5 script
  uses java-functions. See RHBZ#1600426.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Mat Booth <mat.booth@redhat.com> - 5.2.0-1
- Update to latest upstream release

* Wed Jun 27 2018 Mat Booth <mat.booth@redhat.com> - 5.0.0-4
- Add java 9 automatic module name headers to jar files
- License correction EPL -> EPL-2.0

* Thu Mar 15 2018 Michael Simacek <msimacek@redhat.com> - 5.0.0-3
- Disable gradle plugin to fix FTBFS

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Sep 14 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.0.0-1
- Initial packaging

## END: Generated by rpmautospec
