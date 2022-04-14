%global base_name byte-buddy

Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:          %{base_name}-bootstrap
Version:       1.9.5
Release:       8%{?dist}
Summary:       A bootstrap package for building '%{base_name}'.
License:       ASL 2.0
URL:           http://bytebuddy.net/
Source0:       https://github.com/raphw/byte-buddy/archive/%{base_name}-%{version}.tar.gz

# Patch out use of a unixsocket lib that is not in Fedora
Patch0:         no-unixsocket.patch

# Patch the build to avoid bundling inside shaded jars
Patch1:         avoid-bundling-asm.patch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.eclipse.aether:aether-util)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.ow2.asm:asm-commons)

BuildArch:     noarch

%description
Byte Buddy is a code generation library for creating Java classes during the
runtime of a Java application and without the help of a compiler. Other than
the code generation utilities that ship with the Java Class Library, Byte Buddy
allows the creation of arbitrary classes and is not limited to implementing
interfaces for the creation of runtime proxies.

NOTE: this is only a bootstrap package enabling the build of proper JavaCC!
Please install '%{base_name}' if you're looking for JavaCC.

%package agent
Summary: Byte Buddy Java agent

%description agent
The Byte Buddy Java agent allows to access the JVM's HotSwap feature.

%package parent
Summary: Byte Buddy parent POM

%description parent
The parent artifact contains configuration information that
concern all modules.

%package maven-plugin
Summary: Byte Buddy Maven plugin

%description maven-plugin
A plugin for post-processing class files via Byte Buddy in a Maven build.

%prep
%setup -q -n %{base_name}-%{base_name}-%{version}
%patch0
%patch1

# Remove pre-built jars
find -name *.jar -delete
find -name *.class -delete

# Cause pre-compiled stuff to be re-compiled
mv byte-buddy-dep/src/precompiled/java/net/bytebuddy/build/*.java \
  byte-buddy-dep/src/main/java/net/bytebuddy/build
mkdir -p byte-buddy-dep/src/test/java/net/bytebuddy/test/precompiled/
mv byte-buddy-dep/src/precompiled/java/net/bytebuddy/test/precompiled/*.java \
  byte-buddy-dep/src/test/java/net/bytebuddy/test/precompiled/

# Don't ship android or benchmark modules
%pom_disable_module byte-buddy-android
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
%pom_remove_plugin :clirr-maven-plugin
%pom_remove_plugin :maven-release-plugin

# Not interested in shading sources (causes NPE on old versions of shade plugin)
%pom_xpath_set "pom:createSourcesJar" "false" byte-buddy

# Drop build dep on findbugs annotations, used only by the above check plugins
%pom_remove_dep :findbugs-annotations
sed -i -e '/SuppressFBWarnings/d' $(grep -lr SuppressFBWarnings)

# Plugin for generating Java 9 module-info file is not in Fedora
%pom_remove_plugin -r :modulemaker-maven-plugin

# Remove circular self-dependency to allow bootstrapping
%pom_remove_plugin :byte-buddy-maven-plugin byte-buddy-dep

%build
# Cannot run the test suite in bootstrap mode due to circular dep
# on self and mockito
# We don't need docs for the bootstrap package as well.
%mvn_build -s -f -- -P'java8,!checks' -Dmaven.javadoc.skip=true

%install
%mvn_install

%files -f .mfiles-%{base_name} -f .mfiles-%{base_name}-dep
%doc README.md release-notes.md
%license LICENSE NOTICE

%files agent -f .mfiles-%{base_name}-agent
%license LICENSE NOTICE

%files parent -f .mfiles-%{base_name}-parent
%license LICENSE NOTICE

%files maven-plugin -f .mfiles-%{base_name}-maven-plugin

%changelog
* Mon Aug 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.5-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Splitting out a separate bootstrap package to break cyclic dependencies.
- Disabled javadoc generation.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

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
