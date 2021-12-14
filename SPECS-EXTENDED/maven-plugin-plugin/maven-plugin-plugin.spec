Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-plugin-plugin
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


%global base_name maven-plugin-tools
Name:           maven-plugin-plugin
Version:        3.6.0
Release:        2%{?dist}
Summary:        Maven Plugin Plugin
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/plugin-tools/
Source0:        http://repo2.maven.org/maven2/org/apache/maven/plugin-tools/%{base_name}/%{version}/%{base_name}-%{version}-source-release.zip
Patch0:         0001-Avoid-duplicate-MOJO-parameters.patch
Patch1:         0002-Deal-with-nulls-from-getComment.patch
Patch2:         0003-Port-to-plexus-utils-3.0.24.patch
BuildRequires:  fdupes
BuildRequires:  maven-local
BuildRequires:  unzip
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-tools-annotations)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-tools-api)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-tools-generators)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-tools-java)
BuildRequires:  maven-plugin-plugin-bootstrap
BuildRequires:  maven-plugin-tools-generators
BuildRequires:  maven-plugin-tools-api
BuildRequires:  maven-plugin-tools-java
BuildRequires:  maven-plugin-tools-annotations
BuildRequires:  maven-reporting-impl
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-impl)
BuildRequires:  mvn(org.apache.maven.surefire:maven-surefire-common)
BuildRequires:  mvn(org.apache.maven:maven-artifact:2.2.1)
BuildRequires:  mvn(org.apache.maven:maven-model:2.2.1)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-repository-metadata)
BuildRequires:  mvn(org.apache.velocity:velocity)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus-velocity)
BuildRequires:  mvn(org.codehaus.modello:modello-core)
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-converters)
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-dom4j)
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-java)
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-jdom)
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-sax)
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-snakeyaml)
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-stax)
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-xdoc)
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-xpp3)
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-xsd)
Obsoletes:      %{name}-bootstrap
#!BuildRequires: maven-compiler-plugin-bootstrap
#!BuildRequires: maven-jar-plugin-bootstrap
#!BuildRequires: maven-javadoc-plugin-bootstrap
#!BuildRequires: maven-plugin-plugin-bootstrap
#!BuildRequires: maven-resources-plugin-bootstrap
#!BuildRequires: maven-surefire-plugin-bootstrap
BuildArch:      noarch

%description
The Plugin Plugin is used to create a Maven plugin descriptor for any Mojo's
found in the source tree, to include in the JAR. It is also used to generate
Xdoc files for the Mojos as well as for updating the plugin registry, the
artifact metadata and a generic help goal.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{base_name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%pom_remove_plugin -r :maven-enforcer-plugin

%pom_xpath_inject "pom:project/pom:properties" "
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>"

# Remove test dependencies because tests are skipped anyways.
%pom_xpath_remove "pom:dependency[pom:scope='test']"

# Why on the earth is this dependency there ???
%pom_remove_dep :maven-surefire-common maven-plugin-plugin

%pom_change_dep org.easymock:easymock:: :::test maven-plugin-tools-annotations

%build
pushd %{name}
%{mvn_file} :%{name} %{base_name}/%{name}
%{mvn_build} -f \
%if %{?pkg_vcmp:%pkg_vcmp java-devel >= 9}%{!?pkg_vcmp:0}
	-- -Dmaven.compiler.release=7
%endif

popd

%install
pushd %{name}
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}
popd

%files -f %{name}/.mfiles
%license LICENSE NOTICE

%files javadoc -f %{name}/.mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Dec 09 2020 Joe Schmitt <joschmit@microsoft.com> - 3.6.0-1.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Depend on maven-plugin-plugin-bootstrap, maven-plugin-tools*, modello, and maven-reporting-impl to avoid circular dependency.

* Mon Nov 25 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream 3.6.0
  * allow building with java > 1.8 too against objectweb-asm 7.2
- Removed patch:
  * fix-getPluginsAsMap.patch
    + fix is present in the updated sources
* Sun Nov 24 2019 Fridrich Strba <fstrba@suse.com>
- Specify maven.compiler.release to fix build with jdk9+ and newer
  maven-javadoc-plugin
* Wed Apr  3 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of the non-bootstrap version of
  maven-plugin-plugin 3.5.1
