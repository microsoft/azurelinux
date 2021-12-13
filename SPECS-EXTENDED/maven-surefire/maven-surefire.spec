Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-surefire
#
# Copyright (c) 2019 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           maven-surefire
Version:        2.22.0
Release:        4%{?dist}
Summary:        Test framework project
License:        Apache-2.0 AND CPL-1.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/surefire/
# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
# Remove bundled binaries which cannot be easily verified for licensing
Source1:        generate-tarball.sh
Source2:        http://junit.sourceforge.net/cpl-v10.html
Source10:       %{name}-build.tar.xz
Patch0:         0001-Maven-3.patch
Patch1:         0002-Port-to-current-doxia.patch
Patch2:         0003-Port-to-TestNG-6.11.patch
Patch3:         0004-Port-to-current-maven-shared-utils.patch
Patch10:        %{name}-bootstrap-resources.patch
BuildRequires:  ant
BuildRequires:  apache-commons-io
BuildRequires:  apache-commons-lang3
BuildRequires:  fdupes
BuildRequires:  javacc
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jsr-305
BuildRequires:  junit
BuildRequires:  maven-common-artifact-filters
BuildRequires:  maven-doxia-core
BuildRequires:  maven-doxia-logging-api
BuildRequires:  maven-doxia-sink-api
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-lib
BuildRequires:  maven-plugin-annotations
BuildRequires:  maven-reporting-api
BuildRequires:  maven-reporting-impl
BuildRequires:  maven-shared-utils
BuildRequires:  objectweb-asm
BuildRequires:  plexus-languages
BuildRequires:  sisu-plexus
BuildRequires:  testng
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
# PpidChecker relies on /usr/bin/ps to check process uptime
Requires:       procps
BuildArch:      noarch

%description
Surefire is a test framework project.

%package plugin-bootstrap
Summary:        Surefire plugin for maven
Group:          Development/Libraries/Java

%description plugin-bootstrap
Maven surefire plugin for running tests via the surefire framework.

%package report-plugin-bootstrap
Summary:        Surefire reports plugin for maven
Group:          Development/Libraries/Java

%description report-plugin-bootstrap
Plugin for generating reports from surefire test runs.

%package provider-junit
Summary:        JUnit provider for Maven Surefire
Group:          Development/Libraries/Java

%description provider-junit
JUnit provider for Maven Surefire.

%package provider-testng
Summary:        TestNG provider for Maven Surefire
Group:          Development/Libraries/Java

%description provider-testng
TestNG provider for Maven Surefire.

%package report-parser
Summary:        Parses report output files from surefire
Group:          Development/Libraries/Java

%description report-parser
Plugin for parsing report output files from surefire.

%package -n maven-failsafe-plugin-bootstrap
Summary:        Maven plugin for running integration tests
Group:          Development/Libraries/Java

%description -n maven-failsafe-plugin-bootstrap
The Failsafe Plugin is designed to run integration tests while the
Surefire Plugins is designed to run unit. The name (failsafe) was
chosen both because it is a synonym of surefire and because it implies
that when it fails, it does so in a safe way.

If you use the Surefire Plugin for running tests, then when you have a
test failure, the build will stop at the integration-test phase and
your integration test environment will not have been torn down
correctly.

The Failsafe Plugin is used during the integration-test and verify
phases of the build lifecycle to execute the integration tests of an
application. The Failsafe Plugin will not fail the build during the
integration-test phase thus enabling the post-integration-test phase
to execute.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n surefire-%{version} -a10
cp -p %{SOURCE2} .

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch10 -p1

# Disable strict doclint
sed -i /-Xdoclint:all/d pom.xml

%pom_disable_module surefire-shadefire

%pom_disable_module surefire-junit-platform surefire-providers

%pom_remove_dep -r org.apache.maven.surefire:surefire-shadefire

# Help plugin is needed only to evaluate effective Maven settings.
# For building RPM package default settings will suffice.
%pom_remove_plugin :maven-help-plugin surefire-setup-integration-tests

# QA plugin useful only for upstream
%pom_remove_plugin -r :jacoco-maven-plugin

# Not in Fedora
%pom_remove_plugin -r :animal-sniffer-maven-plugin
# Complains
%pom_remove_plugin -r :apache-rat-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
# We don't need site-source
%pom_remove_plugin :maven-assembly-plugin maven-surefire-plugin
%pom_remove_dep -r ::::site-source

%pom_xpath_set pom:mavenVersion 3.3.3
%pom_remove_dep :maven-project maven-surefire-report-plugin
%pom_remove_dep :maven-project maven-surefire-common
%pom_remove_dep :maven-plugin-descriptor maven-surefire-common
%pom_remove_dep :maven-toolchain maven-surefire-common

%pom_xpath_remove -r "pom:execution[pom:id='shared-logging-generated-sources']"

%pom_add_dep com.google.code.findbugs:jsr305 surefire-api

%pom_remove_plugin -r :maven-shade-plugin
%pom_remove_plugin -r :build-helper-maven-plugin

%pom_add_dep org.apache.commons:commons-lang3::runtime maven-surefire-plugin
%pom_add_dep commons-io:commons-io::runtime maven-surefire-plugin

%build
%{mvn_package} ":*tests*" __noinstall
%{mvn_package} ":{surefire,surefire-providers}" __noinstall
%{mvn_package} ":*{surefire-plugin,report-plugin}*" @1
%{mvn_package} ":*junit-platform*" junit5
%{mvn_package} ":*{junit,testng,failsafe-plugin,report-parser}*"  @1

mkdir -p lib
build-jar-repository -s -p lib \
	apache-commons-lang3 \
	commons-io \
	javacc \
	jsr-305 \
	junit \
	maven-common-artifact-filters/maven-common-artifact-filters \
	maven-doxia/doxia-core \
	maven-doxia/doxia-logging-api \
	maven-doxia/doxia-sink-api \
	maven-doxia-sitetools/doxia-site-renderer \
	maven/maven-artifact \
	maven/maven-compat \
	maven/maven-core \
	maven/maven-model \
	maven/maven-plugin-api \
	maven-plugin-tools/maven-plugin-annotations \
	maven-reporting-api/maven-reporting-api \
	maven-reporting-impl/maven-reporting-impl \
	maven-shared-utils/maven-shared-utils \
	objectweb-asm/asm \
	org.eclipse.sisu.plexus \
	plexus-languages/plexus-java \
	testng

%ant \
	-Dtest.skip=true \
	package javadoc

%mvn_artifact pom.xml
%mvn_artifact surefire-providers/pom.xml

mkdir -p target/site/apidocs

for module in \
    surefire-logger-api \
    surefire-api \
    surefire-booter \
    surefire-grouper \
    maven-surefire-common \
    surefire-report-parser \
    maven-surefire-plugin \
    maven-failsafe-plugin \
    maven-surefire-report-plugin; do
  %mvn_artifact ${module}/pom.xml ${module}/target/${module}-%{version}.jar
  if [ -d ${module}/target/site/apidocs ]; then
    cp -r ${module}/target/site/apidocs target/site/apidocs/${module}
  fi
done
for module in \
    common-junit3 \
    common-java5 \
    common-junit4 \
    common-junit48 \
    surefire-junit3 \
    surefire-junit4 \
    surefire-junit47 \
    surefire-testng-utils \
    surefire-testng; do
  %mvn_artifact surefire-providers/${module}/pom.xml \
    surefire-providers/${module}/target/${module}-%{version}.jar
  if [ -d surefire-providers/${module}/target/site/apidocs ]; then
    cp -r surefire-providers/${module}/target/site/apidocs target/site/apidocs/${module}
  fi
done

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc README.md
%license LICENSE NOTICE cpl-v10.html

%files plugin-bootstrap -f .mfiles-surefire-plugin

%files report-plugin-bootstrap -f .mfiles-report-plugin

%files report-parser -f .mfiles-report-parser

%files provider-junit -f .mfiles-junit

%files provider-testng -f .mfiles-testng

%files -n maven-failsafe-plugin-bootstrap -f .mfiles-failsafe-plugin

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE cpl-v10.html

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.22.0-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.22.0-3.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Apr  2 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-surefire 2.22.0
- Generate and customize ant build files
- Build the maven plugins as bootstrap packages
- Added patch:
  * maven-surefire-bootstrap-resources.patch
    + Add to the build of the plugins generated files that
    we cannot generate when building outside maven
