Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package modello-maven-plugin
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


%global parent modello
%global subname maven-plugin
Name:           %{parent}-%{subname}
Version:        1.10.0
Release:        2%{?dist}
Summary:        Modello Maven Plugin
License:        MIT AND Apache-2.0
Group:          Development/Libraries/Java
URL:            http://codehaus-plexus.github.io/modello/modello-maven-plugin
Source0:        http://repo2.maven.org/maven2/org/codehaus/%{parent}/%{parent}/%{version}/%{parent}-%{version}-source-release.zip
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
BuildRequires:  fdupes
BuildRequires:  maven-local
BuildRequires:  unzip
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  maven-plugin-plugin-bootstrap
BuildRequires:  maven-plugin-tools-generators
BuildRequires:  maven-plugin-tools-api
BuildRequires:  maven-plugin-tools-java
BuildRequires:  maven-plugin-tools-annotations
BuildRequires:  maven-reporting-impl
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.modello:modello-core) = %{version}
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-converters) = %{version}
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-dom4j) = %{version}
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-java) = %{version}
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-jdom) = %{version}
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-sax) = %{version}
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-snakeyaml) = %{version}
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-stax) = %{version}
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-xdoc) = %{version}
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-xpp3) = %{version}
BuildRequires:  mvn(org.codehaus.modello:modello-plugin-xsd) = %{version}
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.sonatype.plexus:plexus-build-api)
#!BuildRequires: maven-compiler-plugin-bootstrap
#!BuildRequires: maven-jar-plugin-bootstrap
#!BuildRequires: maven-javadoc-plugin-bootstrap
#!BuildRequires: maven-plugin-plugin-bootstrap
#!BuildRequires: maven-resources-plugin-bootstrap
#!BuildRequires: maven-surefire-plugin-bootstrap
BuildArch:      noarch

%description
Modello is a Data Model toolkit in use by the Apache Maven Project.

Modello is a framework for code generation from a simple model.
Modello generates code from a simple model format based on a plugin
architecture, various types of code and descriptors can be generated
from the single model, including Java POJOs, XML
marshallers/unmarshallers, XSD and documentation.

Modello Maven Plugin enables the use of Modello in Maven builds.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{parent}-%{version}
cp -p %{SOURCE1} LICENSE
# We don't generate site; don't pull extra dependencies.
%pom_remove_plugin :maven-site-plugin
# Avoid using Maven 2.x APIs
sed -i s/maven-project/maven-core/ modello-maven-plugin/pom.xml

%pom_disable_module modello-plugin-jackson modello-plugins
%pom_disable_module modello-plugin-jsonschema modello-plugins
%pom_remove_dep :modello-plugin-jackson modello-maven-plugin
%pom_remove_dep :modello-plugin-jsonschema modello-maven-plugin

%build
# skip tests because we have too old xmlunit in openSUSE now (1.5)
pushd %{name}
%{mvn_build} -f -- -Dmaven.version=3.1.1 -Dsource=6
popd

%install
pushd %{name}
%mvn_install
popd
%fdupes -s %{buildroot}%{_javadocdir}

%files -f %{name}/.mfiles
%license LICENSE

%files javadoc -f %{name}/.mfiles-javadoc
%license LICENSE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Dec 09 2020 Joe Schmitt <joschmit@microsoft.com> - 1.10.0-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Depend on maven-plugin-plugin-bootstrap, maven-plugin-tools*, and maven-reporting-impl to avoid circular dependency.

* Thu Nov 21 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 1.10.0
* Tue Mar 12 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of modello-maven-plugin separate package
  * Allows building the rest of modello without needing maven
