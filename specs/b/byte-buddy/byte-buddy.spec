## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 30;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with bootstrap

Name:           byte-buddy
Version:        1.14.2
Release:        %autorelease
Summary:        Runtime code generation for the Java virtual machine
License:        Apache-2.0
URL:            https://bytebuddy.net
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/raphw/byte-buddy/archive/refs/tags/byte-buddy-%{version}.tar.gz

# Patch the build to avoid bundling inside shaded jars
Patch:          0001-Avoid-bundling-asm.patch
Patch:          0002-Remove-dependencies.patch
Patch:          0003-Fix-broken-modular-jars.patch

BuildRequires:  jurand
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(codes.rafael.modulemaker:modulemaker-maven-plugin)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.bytebuddy:byte-buddy)
BuildRequires:  mvn(net.bytebuddy:byte-buddy-dep)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-testing:maven-plugin-testing-harness)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.eclipse.aether:aether-util)
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.ow2.asm:asm-analysis)
BuildRequires:  mvn(org.ow2.asm:asm-commons)
BuildRequires:  mvn(org.ow2.asm:asm-util)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.14.2-25

%description
Byte Buddy is a code generation library for creating Java classes during the
runtime of a Java application and without the help of a compiler. Other than
the code generation utilities that ship with the Java Class Library, Byte Buddy
allows the creation of arbitrary classes and is not limited to implementing
interfaces for the creation of runtime proxies. 

%package agent
Summary:        Byte Buddy Java agent

%description agent
The Byte Buddy Java agent allows to access the JVM's HotSwap feature.

%package maven-plugin
Summary:        Byte Buddy Maven plugin

%description maven-plugin
A plugin for post-processing class files via Byte Buddy in a Maven build.

%prep
%autosetup -p1 -C


find -name '*.class' -delete

rm byte-buddy-agent/src/test/java/net/bytebuddy/agent/VirtualMachineAttachmentTest.java\
   byte-buddy-agent/src/test/java/net/bytebuddy/agent/VirtualMachineForOpenJ9Test.java\
   byte-buddy-agent/src/test/java/net/bytebuddy/test/utility/JnaRule.java\
;

# Don't ship android or benchmark modules
%pom_disable_module byte-buddy-android
%pom_disable_module byte-buddy-android-test
%pom_disable_module byte-buddy-benchmark

# Don't ship gradle plugin
%pom_disable_module byte-buddy-gradle-plugin

# Remove check plugins unneeded by RPM builds
%pom_remove_plugin :jacoco-maven-plugin
%pom_remove_plugin :license-maven-plugin
%pom_remove_plugin :pitest-maven
%pom_remove_plugin :coveralls-maven-plugin
%pom_remove_plugin :spotbugs-maven-plugin
%pom_remove_plugin :jitwatch-jarscan-maven-plugin
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :nexus-staging-maven-plugin

# Avoid circural dependency
%pom_remove_plugin :byte-buddy-maven-plugin byte-buddy-dep

# Not interested in shading sources (causes NPE on old versions of shade plugin)
%pom_xpath_set "pom:createSourcesJar" "false" byte-buddy

# Drop build dep on findbugs annotations, used only by the above check plugins
%pom_remove_dep -r :findbugs-annotations
%java_remove_annotations byte-buddy-agent byte-buddy-dep byte-buddy-maven-plugin -n SuppressFBWarnings

%pom_remove_dep org.ow2.asm:asm-deprecated

%pom_remove_plugin -r :maven-shade-plugin
%pom_remove_dep -r net.java.dev.jna:jna
%pom_remove_dep -r net.java.dev.jna:jna-platform

%mvn_package :byte-buddy-parent __noinstall

%build
# Ignore test failures, there seems to be something different about the
# bytecode of our recompiled test resources, expect 6 test failures in
# the byte-buddy-dep module

# NOTE you can obtain valid profiles for precompilation by:
# xmllint --xpath '//*[local-name()="profile"]/*[local-name()="id"]/text()' byte-buddy-dep/pom.xml | grep 'precompile$' | grep -v 'no-precompile$' | sed 's/\(.*\)/-P\1/'
profiles='-Pjava-8-precompile -Pjava-8-parameters-precompile -Pjava-11-precompile -Pjava-16-precompile -Pjava-17-precompile'
%mvn_build -j -s -- -P'java8,!checks' "${profiles}" -Dsourcecode.main.version=8 -Dsourcecode.test.version=8 -Dmaven.test.failure.ignore=true

%install
%mvn_install

%files -f .mfiles-%{name} -f .mfiles-%{name}-dep
%doc README.md release-notes.md
%license LICENSE NOTICE

%files agent -f .mfiles-%{name}-agent
%license LICENSE NOTICE

%files maven-plugin -f .mfiles-%{name}-maven-plugin

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 1.14.2-30
- Latest state for byte-buddy

* Tue Jul 29 2025 Jiri Vanek <jvanek@redhat.com> - 1.14.2-29
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.14.2-27
- Build with OpenJDK 25

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.14.2-26
- Switch javapackages test plan to f43 ref

* Wed Mar 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.14.2-25
- Switch to javapackages tests from CentOS Stream GitLab

* Mon Mar 03 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.14.2-24
- Remove javadoc subpackage

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.14.2-22
- Switch upstream URL to https

* Fri Nov 29 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.14.2-17
- Update javapackages test plan to f42

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.14.2-8
- Rebuilt for java-21-openjdk as system jdk

* Tue Feb 20 2024 Marian Koncek <mkoncek@redhat.com> - 1.14.2-7
- Update Java source/target to 8

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.14.2-4
- Convert License tag to SPDX format

* Wed Aug 30 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.14.2-3
- Build with Jurand instead of deprecated javapackages-extra

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Feb 23 2023 Marian Koncek <mkoncek@redhat.com> - 1.14.2-1
- Update to upstream version 1.14.2

* Tue Feb 21 2023 Marian Koncek <mkoncek@redhat.com> - 1.12.10-4
- Enable modulemaker-maven-plugin

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 09 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.12.10-1
- Update to upstream version 1.12.10

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.12.0-3
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 09 2021 Marian Koncek <mkoncek@redhat.com> - 1.12.0-1
- Update to upstream version 1.12.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.20-2
- Bootstrap build
- Non-bootstrap build

* Thu Feb 04 2021 Marian Koncek <mkoncek@redhat.com> - 1.10.20-1
- Update to upstream version 1.10.20

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 29 2020 Marian Koncek <mkoncek@redhat.com> - 1.10.16-1
- Update to upstram version 1.10.16

* Fri Aug 14 2020 Jerry James <loganjerry@gmail.com> - 1.10.14-1
- Version 1.10.14
- Remove no longer needed no-unixsocket.patch
- Add workaround for compiling tests with JDK 11

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1.9.5-8
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Marian Koncek <mkoncek@redhat.com> - 1.10.7-1
- Update to upstream version 1.10.7

* Thu Nov 21 2019 Marian Koncek <mkoncek@redhat.com> - 1.10.3-1
- Update to upstream version 1.10.3

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.10.1-2
- Mass rebuild for javapackages-tools 201902

* Thu Sep 12 2019 Marian Koncek <mkoncek@redhat.com> - 1.10.1-1
- Update to upstream version 1.10.1

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Marian Koncek <mkoncek@redhat.com> - 1.9.13-2
- Remove the dependency on maven-shade-plugin

* Thu Jun 06 2019 Marian Koncek <mkoncek@redhat.com> - 1.9.13-1
- Update to upstream version 1.9.13

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9.5-5
- Mass rebuild for javapackages-tools 201901

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 06 2018 Mat Booth <mat.booth@redhat.com> - 1.9.5-4
- Prevent NPE in maven-shade-plugin

* Wed Dec 05 2018 Mat Booth <mat.booth@redhat.com> - 1.9.5-3
- Enable test suites

* Tue Dec 04 2018 Mat Booth <mat.booth@redhat.com> - 1.9.5-2
- Full, non-bootstrap build

* Fri Nov 30 2018 Mat Booth <mat.booth@redhat.com> - 1.9.5-1
- Update to latest upstream release
- Add a bootstrap mode to break circular self-dependency
- Patch out use of optional external unixsocket library that is not present
  in Fedora
- Patch to avoid bundling ASM inside the shaded jar

* Wed May 25 2016 gil cattaneo <puntogil@libero.it> 1.3.19-1
- update to 1.3.19

* Tue Dec 22 2015 gil cattaneo <puntogil@libero.it> 0.7.7-1
- initial rpm

## END: Generated by rpmautospec
