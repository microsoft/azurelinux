Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-surefire-plugins
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


%global base_name maven-surefire
Name:           %{base_name}-plugins
Version:        2.22.0
Release:        4%{?dist}
Summary:        Test framework project
License:        Apache-2.0 AND CPL-1.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/surefire/
# ./generate-tarball.sh
Source0:        %{base_name}-%{version}.tar.gz
# Remove bundled binaries which cannot be easily verified for licensing
Source1:        generate-tarball.sh
Source2:        http://junit.sourceforge.net/cpl-v10.html
Patch0:         0001-Maven-3.patch
Patch1:         0002-Port-to-current-doxia.patch
Patch2:         0003-Port-to-TestNG-6.11.patch
Patch3:         0004-Port-to-current-maven-shared-utils.patch
BuildRequires:  fdupes
BuildRequires:  maven-local
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-impl)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-utils)
BuildRequires:  mvn(org.apache.maven.surefire:maven-surefire-common)
BuildRequires:  mvn(org.apache.maven.surefire:surefire-logger-api)
BuildRequires:  mvn(org.apache.maven.surefire:surefire-report-parser)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.fusesource.jansi:jansi)
#!BuildRequires: maven-compiler-plugin-bootstrap
#!BuildRequires: maven-jar-plugin-bootstrap
#!BuildRequires: maven-javadoc-plugin-bootstrap
#!BuildRequires: maven-plugin-plugin-bootstrap
#!BuildRequires: maven-resources-plugin-bootstrap
#!BuildRequires: maven-surefire-plugin-bootstrap
BuildArch:      noarch

%description
Surefire is a test framework project.

%package -n maven-surefire-plugin
Summary:        Surefire plugin for maven
Group:          Development/Libraries/Java

%description -n maven-surefire-plugin
Maven surefire plugin for running tests via the surefire framework.

%package -n maven-surefire-report-plugin
Summary:        Surefire reports plugin for maven
Group:          Development/Libraries/Java

%description -n maven-surefire-report-plugin
Plugin for generating reports from surefire test runs.

%package -n maven-failsafe-plugin
Summary:        Maven plugin for running integration tests
Group:          Development/Libraries/Java

%description -n maven-failsafe-plugin
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
Group:          Development/Libraries/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n surefire-%{version}
cp -p %{SOURCE2} .

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

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
find . -name dependency-reduced-pom.xml -delete

%pom_add_dep org.apache.commons:commons-lang3::runtime maven-surefire-plugin
%pom_add_dep commons-io:commons-io::runtime maven-surefire-plugin

%build
%{mvn_package} ":*tests*" __noinstall
%{mvn_package} ":{surefire,surefire-providers}" __noinstall
%{mvn_package} ":*{surefire-plugin,report-plugin}*" @1
%{mvn_package} ":*junit-platform*" junit5
%{mvn_package} ":*{junit,testng,failsafe-plugin,report-parser}*"  @1

%mvn_artifact pom.xml
mkdir -p target/site/apidocs
for i in \
   maven-failsafe-plugin \
   maven-surefire-plugin \
   maven-surefire-report-plugin; do
  pushd ${i}
    %mvn_build -f \
%if %{?pkg_vcmp:%pkg_vcmp java-devel >= 9}%{!?pkg_vcmp:0}
	-- -Dmaven.compiler.release=6
%endif

  popd
  %mvn_artifact ${i}/pom.xml ${i}/target/${i}-%{version}.jar
  if [ -d ${i}/target/site/apidocs ]; then
    cp -r ${i}/target/site/apidocs target/site/apidocs/${i}
  fi
done

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -n maven-surefire-plugin -f .mfiles-surefire-plugin

%files -n maven-surefire-report-plugin -f .mfiles-report-plugin

%files -n maven-failsafe-plugin -f .mfiles-failsafe-plugin

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE cpl-v10.html

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.22.0-4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Sun Nov 24 2019 Fridrich Strba <fstrba@suse.com>
- Specify maven.compiler.release to fix build with jdk9+ and newer
  maven-javadoc-plugin
* Wed Apr  3 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of the non-bootstrap versions of maven plugins
  distributed with surefire 2.22.0
