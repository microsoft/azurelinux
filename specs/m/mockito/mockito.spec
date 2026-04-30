## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 21;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with bootstrap

Name:           mockito
Version:        5.8.0
Release:        %autorelease
Summary:        Tasty mocking framework for unit tests in Java
License:        MIT
URL:            https://site.mockito.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
Source1:        generate-tarball.sh
# A custom build script to allow building with maven instead of gradle
Source2:        aggregator.pom
# Maven central POMs for subprojects
Source3:        https://repo1.maven.org/maven2/org/mockito/mockito-core/%{version}/mockito-core-%{version}.pom
Source4:        https://repo1.maven.org/maven2/org/mockito/mockito-junit-jupiter/%{version}/mockito-junit-jupiter-%{version}.pom

# Mockito expects byte-buddy to have a shaded/bundled version of ASM, but
# we don't bundle in Fedora, so this patch makes mockito use ASM explicitly
Patch:          use-unbundled-asm.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.bytebuddy:byte-buddy)
BuildRequires:  mvn(net.bytebuddy:byte-buddy-agent)
BuildRequires:  mvn(net.bytebuddy:byte-buddy-dep)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.objenesis:objenesis)
BuildRequires:  mvn(org.opentest4j:opentest4j)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 5.8.0-16

%description
Mockito is a mocking framework that tastes really good. It lets you write
beautiful tests with clean & simple API. Mockito doesn't give you hangover
because the tests are very readable and they produce clean verification
errors.

%package junit-jupiter
Summary:        Mockito JUnit 5 support
Requires:       %{name} = %{version}-%{release}

%description junit-jupiter
Mockito JUnit 5 support.

%prep
%autosetup -p1 -C

cp %{SOURCE2} aggregator.pom
cp %{SOURCE3} pom.xml
cp %{SOURCE4} subprojects/junit-jupiter/pom.xml

# Disable failing test
# TODO check status: https://github.com/mockito/mockito/issues/2162
sed -i '/add_listeners_concurrently_sanity_check/i @org.junit.Ignore' src/test/java/org/mockitousage/debugging/StubbingLookupListenerCallbackTest.java

# Workaround easymock incompatibility with Java 17 that should be fixed
# in easymock 4.4: https://github.com/easymock/easymock/issues/274
%pom_add_plugin :maven-surefire-plugin . "<configuration>
    <argLine>--add-opens=java.base/sun.reflect.generics.reflectiveObjects=ALL-UNNAMED</argLine></configuration>"

# Compatibility alias
%mvn_alias org.%{name}:%{name}-core org.%{name}:%{name}-all

%pom_add_dep junit:junit
%pom_add_dep net.bytebuddy:byte-buddy-dep
%pom_remove_dep org.objenesis:objenesis
%pom_add_dep org.objenesis:objenesis
%pom_add_dep org.opentest4j:opentest4j

%pom_remove_dep org.junit.jupiter:junit-jupiter-api subprojects/junit-jupiter
%pom_add_dep org.junit.jupiter:junit-jupiter-api subprojects/junit-jupiter

mkdir -p src/main/resources/mockito-extensions
echo 'member-accessor-module' > src/main/resources/mockito-extensions/org.mockito.plugins.MemberAccessor
echo 'mock-maker-subclass' > src/main/resources/mockito-extensions/org.mockito.plugins.MockMaker

# see gradle/mockito-core/inline-mock.gradle
%pom_xpath_inject 'pom:project/pom:build/pom:plugins' '
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-antrun-plugin</artifactId>
  <version>any</version>
  <executions>
    <execution>
      <phase>process-classes</phase>
      <configuration>
        <target>
          <copy file="${project.build.outputDirectory}/org/mockito/internal/creation/bytebuddy/inject/MockMethodDispatcher.class"
            tofile="${project.build.outputDirectory}/org/mockito/internal/creation/bytebuddy/inject/MockMethodDispatcher.raw"/>
        </target>
      </configuration>
      <goals>
        <goal>run</goal>
      </goals>
    </execution>
  </executions>
</plugin>
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-jar-plugin</artifactId>
  <version>any</version>
  <configuration>
    <excludes>
      <exclude>org/mockito/internal/creation/bytebuddy/inject/*.class</exclude>
    </excludes>
  </configuration>
</plugin>
'

%mvn_package :aggregator __noinstall

%build
%mvn_build -j -f -- -Dmaven.compiler.release=11 -Dproject.build.sourceEncoding=UTF-8 -f aggregator.pom

%mvn_package org.mockito:mockito-junit-jupiter junit-jupiter

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc README.md doc/design-docs/custom-argument-matching.md

%files junit-jupiter -f .mfiles-junit-jupiter

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 5.8.0-21
- test: add initial lock files

* Tue Jul 29 2025 Jiri Vanek <jvanek@redhat.com> - 5.8.0-20
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.8.0-18
- Build with OpenJDK 25

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.8.0-17
- Switch javapackages test plan to f43 ref

* Wed Mar 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.8.0-16
- Switch to javapackages tests from CentOS Stream GitLab

* Mon Mar 03 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.8.0-15
- Remove javadoc subpackage

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 29 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 5.8.0-11
- Update javapackages test plan to f42

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 5.8.0-5
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 5.8.0-4
- bump of release for for java-21-openjdk as system jdk

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 13 2023 Marian Koncek <mkoncek@redhat.com> - 5.8.0-1
- Update to upstream version 5.8.0

* Fri Sep 01 2023 Marian Koncek <mkoncek@redhat.com> - 5.5.0-1
- Update to upstream version 5.5.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Apr 09 2022 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 3.12.4-4
- Set javac compiler release to Java 8

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 3.12.4-3
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 27 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.12.4-2
- Don't build mockito-junit-jupiter in bootstrap mode

* Sat Jan 22 2022 Jerry James <loganjerry@gmail.com> - 3.12.4-1
- Version 3.12.4
- Add inline and junit-jupiter subpackages
- Drop OpenJDK 17 workarounds

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 03 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.7.13-4
- Workaround build issue with OpenJDK 17

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.7.13-2
- Bootstrap build
- Non-bootstrap build

* Thu Feb 04 2021 Marian Koncek <mkoncek@redhat.com> - 3.7.13-1
- Update to upstream version 3.7.13

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct  9 2020 Stuart Gathman <stuart@gathman.org> - 3.5.13-1
- Update to version 3.5.13

* Wed Sep 30 2020 Marian Koncek <mkoncek@redhat.com> - 3.5.13-1
- Update to ustream version 3.5.13

* Sun Aug 23 2020 Jerry James <loganjerry@gmail.com> - 3.5.5-1
- Update to version 3.5.5

* Fri Aug 14 2020 Jerry James <loganjerry@gmail.com> - 2.28.2-1
- Update to version 2.28.2

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Marian Koncek <mkoncek@redhat.com> - 3.4.5-1
- Update to upstream version 3.4.5

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 2.23.9-7
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1.2-2
- Mass rebuild for javapackages-tools 201902

* Wed Oct 16 2019 Marian Koncek <mkoncek@redhat.com> - 3.1.2-1
- Update to upstream version 3.1.2

* Thu Sep 19 2019 Marian Koncek <mkoncek@redhat.com> - 3.0.8-1
- Update to upstream version 3.0.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.23.9-4
- Mass rebuild for javapackages-tools 201901

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.23.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Mat Booth <mat.booth@redhat.com> - 2.23.9-3
- Set the source encoding for the build

* Wed Dec 05 2018 Mat Booth <mat.booth@redhat.com> - 2.23.9-2
- Re-add compatibility alias for 'mockito-all'

* Tue Dec 04 2018 Mat Booth <mat.booth@redhat.com> - 2.23.9-1
- Update to latest upstream version
- Switch to maven build system using a custom pom to avoid a dep on gradle

* Fri Aug 03 2018 Michael Simacek <msimacek@redhat.com> - 1.10.19-17
- Remove bundled minified js from javadoc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.19-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.10.19-15
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.19-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.19-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 16 2017 Michael Simacek <msimacek@redhat.com> - 1.10.19-12
- Remove conditional for EOL Fedora

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.19-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 22 2016 Mat Booth <mat.booth@redhat.com> - 1.10.19-10
- Explicitly import more cglib packages in OSGi metadata to prevent mockito
  failing under certain circumstances during Eclipse test suites

* Fri Feb 12 2016 Mat Booth <mat.booth@redhat.com> - 1.10.19-9
- Require hamcrest explicitly in OSGi metadata

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 25 2015 Raphael Groner <projects.rg@smart.ms> - 1.10.19-7
- introduce License tag

* Fri Dec 25 2015 Raphael Groner <projects.rg@smart.ms> - 1.10.19-6
- reenable osgi

* Fri Dec 18 2015 Raphael Groner <projects.rg@smart.ms> - 1.10.19-5
- workaround rhbz#1292777 stylesheet.css not found

* Thu Jul 16 2015 Michael Simacek <msimacek@redhat.com> - 1.10.19-4
- Use aqute-bnd-2.4.1

* Mon Jun 22 2015 Mat Booth <mat.booth@redhat.com> - 1.10.19-3
- Switch to mvn_install

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Michal Srb <msrb@redhat.com> - 1.10.19-1
- Update to 1.10.19

* Mon Aug 25 2014 Darryl L. Pierce <dpierce@redhat.com> - 1.9.0-18
- First build for EPEL7
- Resolves: BZ#1110030

* Mon Jun 09 2014 Omair Majid <omajid@redhat.com> - 1.9.0-17
- Use .mfiles to pick up xmvn metadata
- Don't use obsolete _mavenpomdir and _mavendepmapfragdir macros
- Fix FTBFS

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1.9.0-16
- Use junit R/BR over junit4.

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.9.0-15
- Use Requires: java-headless rebuild (#1067528)

* Wed Dec 11 2013 Michael Simacek <msimacek@redhat.com> - 1.9.0-14
- Workaround for NPE in setting NamingPolicy

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Tomas Radej <tradej@redhat.com> - 1.9.0-12
- Patched LocalizedMatcher due to hamcrest update, (bug upstream)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 6 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.9.0-10
- More Import-Package fixes. Note that fix-cglib-refs.patch is
  not suitable for upstream: issue id=373

* Tue Sep 4 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.9.0-9
- Fix missing Import-Package in manifest.

* Mon Aug 27 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.9.0-8
- Add aqute bnd instructions for OSGi metadata

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-6
- Place JavaDoc in directly under %%{_javadocdir}/%%{name} instead
  of %%{_javadocdir}/%%{name}/javadoc

* Wed Apr 25 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-5
- Removed post/postun hook for update_maven_depmap

* Tue Apr 24 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-4
- Fix groupId of cglib dependency
- Add additional depmap for mockito-all
- Update depmap on post and postun
- Fix version in pom

* Wed Feb 22 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-3
- Added cglib dependency to pom

* Tue Feb 21 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-2
- Include upstream Maven pom.xml in package
- Added missing Requires for cglib, junit4, hamcrest, objenesis
- Added source tarball generating script to sources

* Thu Feb 16 2012 Roman Kennke <rkennke@redhat.com> 1.9.0-1
- Initial package

## END: Generated by rpmautospec
