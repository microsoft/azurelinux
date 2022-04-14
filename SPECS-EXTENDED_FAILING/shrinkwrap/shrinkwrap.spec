Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:          shrinkwrap
Version:       1.2.6
Release:       3%{?dist}
Summary:       Java API for Archive Manipulation
# Some file are without license headers
# reported @ https://issues.jboss.org/browse/SHRINKWRAP-501
License:       ASL 2.0

URL:           http://arquillian.org/modules/shrinkwrap-shrinkwrap/
Source0:       https://github.com/shrinkwrap/shrinkwrap/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires: mvn(org.jboss:jboss-parent:pom:)

BuildArch:     noarch

%description
Shrinkwrap provides a simple mechanism to assemble archives
like JARs, WARs, and EARs with a friendly, fluent API.

%package api-nio2
Summary:       ShrinkWrap NIO.2 API

%description api-nio2
ShrinkWrap NIO.2 API.

%package bom
Summary:       ShrinkWrap Bill of Materials

%description bom
Centralized dependencyManagement for the ShrinkWrap Project.

%package build-resources
Summary:       Shrinkwrap Build Resources

%description build-resources
Shrinkwrap Build Resources.

%package depchain
Summary:       ShrinkWrap Dependency Chain

%description depchain
Single-POM Definition to export the
ShrinkWrap artifacts in proper scope.

%package depchain-java7
Summary:       ShrinkWrap Dependency Chain for Java7 Environments

%description depchain-java7
Single-POM Definition to export the
ShrinkWrap artifacts in proper scope
for Java 7 Environments.

%package impl-base
Summary:       ShrinkWrap Implementation Base
# Public Domain:
# ./impl-base/src/main/java/org/jboss/shrinkwrap/impl/base/io/tar/InvalidHeaderException.java
# ./impl-base/src/main/java/org/jboss/shrinkwrap/impl/base/io/tar/TarArchive.java
# ./impl-base/src/main/java/org/jboss/shrinkwrap/impl/base/io/tar/TarBuffer.java
# ./impl-base/src/main/java/org/jboss/shrinkwrap/impl/base/io/tar/TarEntry.java
# ./impl-base/src/main/java/org/jboss/shrinkwrap/impl/base/io/tar/TarGzOutputStream.java
# ./impl-base/src/main/java/org/jboss/shrinkwrap/impl/base/io/tar/TarHeader.java
# ./impl-base/src/main/java/org/jboss/shrinkwrap/impl/base/io/tar/TarInputStream.java
# ./impl-base/src/main/java/org/jboss/shrinkwrap/impl/base/io/tar/TarOutputStream.java
# ./impl-base/src/main/java/org/jboss/shrinkwrap/impl/base/io/tar/TarOutputStreamImpl.java
# ./impl-base/src/main/java/org/jboss/shrinkwrap/impl/base/io/tar/TarProgressDisplay.java
# ./impl-base/src/main/java/org/jboss/shrinkwrap/impl/base/io/tar/TarTransFileTyper.java
License:       ASL 2.0 and Public Domain

%description impl-base
Common Base for Implementations of the ShrinkWrap Project.

%package impl-nio2
Summary:       ShrinkWrap NIO.2 Implementation

%description impl-nio2
ShrinkWrap NIO.2 Implementation.

%package parent
Summary:       ShrinkWrap Aggregator and Build Parent

%description parent
ShrinkWrap Aggregator POM.

%package spi
Summary:       ShrinkWrap SPI

%description spi
Generic Service Provider Contract of the ShrinkWrap Project.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%autosetup -p1

%pom_disable_module dist

# remove env.JAVA"x"_HOME
%pom_xpath_remove "pom:requireProperty"
# Option UseSplitVerifier support was removed in 8.0
# <argLine>-XX:-UseSplitVerifier</argLine>
%pom_xpath_remove "pom:configuration/pom:argLine" 
%pom_xpath_remove "pom:configuration/pom:jvm" api
%pom_xpath_remove "pom:configuration/pom:jvm" impl-base
%pom_xpath_remove "pom:profiles" impl-base 

%pom_remove_plugin -r :maven-checkstyle-plugin
%pom_remove_plugin -r :maven-release-plugin
%pom_remove_plugin -r org.eclipse.m2e:lifecycle-mapping

# Convert from dos to unix line ending
sed -i.orig 's|\r||g' LICENSE
touch -r LICENSE.orig LICENSE
rm LICENSE.orig

%mvn_package :%{name}-api::tests: %{name}-api
%mvn_package :%{name}-impl-base::tests: %{name}-impl-base

%build
%mvn_build -s --skip-tests

%install
%mvn_install

%check
mvn test

%files -f .mfiles-%{name}-api
%license LICENSE

%files api-nio2 -f .mfiles-%{name}-api-nio2
%files impl-base -f .mfiles-%{name}-impl-base
%files impl-nio2 -f .mfiles-%{name}-impl-nio2
%files spi -f .mfiles-%{name}-spi

%files bom -f .mfiles-%{name}-bom
%license LICENSE

%files build-resources -f .mfiles-%{name}-build-resources
%license LICENSE

%files depchain -f .mfiles-%{name}-depchain
%license LICENSE

%files depchain-java7 -f .mfiles-%{name}-depchain-java7
%license LICENSE

%files parent -f .mfiles-%{name}-parent
%license LICENSE

%files javadoc -f .mfiles-javadoc
%license LICENSE

%changelog
* Mon Aug 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.6-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Skipping tests in the '%%build' section and running them inside '%%check'.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 11 2019 Fabio Valentini <decathorpe@gmail.com> - 1.2.6-1
- Update to version 1.2.6.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Mar 09 2016 gil cattaneo <puntogil@libero.it> 1.2.3-2
- fix impl-base license field

* Wed Mar 09 2016 gil cattaneo <puntogil@libero.it> 1.2.3-1
- update to 1.2.3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 11 2015 gil cattaneo <puntogil@libero.it> 1.1.2-6
- introduce license macro

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.1.2-4
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 gil cattaneo <puntogil@libero.it> 1.1.2-2
- build with XMvn
- minor changes to adapt to current guideline

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 1.1.2-1
- update to 1.1.2

* Tue Feb 19 2013 gil cattaneo <puntogil@libero.it> 1.0.0-5
- set java.home for enforcer-plugin

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.0-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 21 2012 gil cattaneo <puntogil@libero.it> 1.0.0-1
- initial rpm
