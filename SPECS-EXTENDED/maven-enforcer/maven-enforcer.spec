Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-enforcer
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


Name:           maven-enforcer
Version:        1.4.1
Release:        3%{?dist}
Summary:        A build rule execution framework
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/enforcer
Source0:        http://repo1.maven.org/maven2/org/apache/maven/enforcer/enforcer/%{version}/enforcer-%{version}-source-release.zip
# TODO forward upstream
# https://issues.apache.org/jira/browse/MENFORCER-267
Patch0:         0001-Port-to-Maven-3-API.patch
Patch1:         0002-Port-to-artifact-transfer-0.11.0.patch
BuildRequires:  fdupes
BuildRequires:  maven-local
BuildRequires:  unzip
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(commons-lang:commons-lang)
BuildRequires:  mvn(org.apache.maven.plugin-testing:maven-plugin-testing-harness)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.shared:maven-artifact-transfer)
BuildRequires:  mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires:  mvn(org.apache.maven.shared:maven-dependency-tree)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.beanshell:bsh)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-i18n)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildArch:      noarch

%description
Enforcer is a build rule execution framework.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
API documentation for %{name}.

%package api
Summary:        Enforcer API
Group:          Development/Libraries/Java

%description api
This component provides the generic interfaces needed to
implement custom rules for the maven-enforcer-plugin.

%package rules
Summary:        Enforcer Rules
Group:          Development/Libraries/Java

%description rules
This component contains the standard Enforcer Rules.

%package plugin
Summary:        Enforcer Rules
Group:          Development/Libraries/Java

%description plugin
This component contains the standard Enforcer Rules.

%prep
%setup -q -n enforcer-%{version}
%patch0 -p1
%patch1 -p1

# Avoid dependency cycle
%pom_xpath_inject pom:build/pom:pluginManagement/pom:plugins "
    <plugin>
      <artifactId>maven-enforcer-plugin</artifactId>
      <version>SYSTEM</version>
    </plugin>"

# Replace plexus-maven-plugin with plexus-component-metadata
sed -e "s|<artifactId>plexus-maven-plugin</artifactId>|<artifactId>plexus-component-metadata</artifactId>|" \
    -e "s|<goal>descriptor</goal>|<goal>generate-metadata</goal>|" \
    -i enforcer-{api,rules}/pom.xml

%build
%{mvn_build} -s -f \
%if %{?pkg_vcmp:%pkg_vcmp java-devel >= 9}%{!?pkg_vcmp:0}
	-- -Dmaven.compiler.release=6
%endif

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles-enforcer
%license LICENSE
%doc NOTICE

%files api -f .mfiles-enforcer-api
%license LICENSE
%doc NOTICE

%files rules -f .mfiles-enforcer-rules

%files plugin -f .mfiles-maven-enforcer-plugin

%files javadoc -f .mfiles-javadoc
%license LICENSE
%doc NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.1-3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Sun Nov 24 2019 Fridrich Strba <fstrba@suse.com>
- Specify maven.compiler.release to fix build with jdk9+ and newer
  maven-javadoc-plugin
- Added patch:
  * 0002-Port-to-artifact-transfer-0.11.0.patch
    + allow building against maven-artifact-transfer 0.11
* Wed May  1 2019 Jan Engelhardt <jengelh@inai.de>
- Don't just repeat the software name in the summary.
* Tue Apr 30 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-enforcer 1.4.1
