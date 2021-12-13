Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-component-metadata
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


%global base_name plexus-containers
%global comp_name plexus-component-metadata
%bcond_with tests
Name:           %{comp_name}
Version:        2.1.0
Release:        2%{?dist}
Summary:        Component metadata from %{base_name}
# Most of the files are either under ASL 2.0 or MIT
# The following files are under xpp:
# plexus-component-metadata/src/main/java/org/codehaus/plexus/metadata/merge/Driver.java
# plexus-component-metadata/src/main/java/org/codehaus/plexus/metadata/merge/MXParser.java
License:        Apache-2.0 AND MIT AND xpp
Group:          Development/Libraries/Java
URL:            https://github.com/codehaus-plexus/plexus-containers
Source0:        https://github.com/codehaus-plexus/%{base_name}/archive/%{base_name}-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
Source2:        LICENSE.MIT
Patch0:         plexus-containers-asm6.patch
BuildRequires:  fdupes
BuildRequires:  maven-local
BuildRequires:  mvn(com.thoughtworks.qdox:qdox)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
BuildRequires:  mvn(org.jdom:jdom2)
BuildRequires:  mvn(org.ow2.asm:asm)
#!BuildRequires: maven-compiler-plugin-bootstrap
#!BuildRequires: maven-jar-plugin-bootstrap
#!BuildRequires: maven-javadoc-plugin-bootstrap
#!BuildRequires: maven-plugin-plugin-bootstrap
#!BuildRequires: maven-resources-plugin-bootstrap
#!BuildRequires: maven-surefire-plugin-bootstrap
BuildArch:      noarch

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
%{summary}.

%prep
%setup -q -n %{base_name}-%{base_name}-%{version}

%patch0 -p1

cp %{SOURCE1} .
cp %{SOURCE2} .

rm -rf plexus-container-default/src/test/java/org/codehaus/plexus/hierarchy

%pom_remove_plugin -r :maven-site-plugin

# For Maven 3 compat
%pom_add_dep org.apache.maven:maven-core plexus-component-metadata

%pom_change_dep -r :google-collections com.google.guava:guava:20.0

# ASM dependency was changed to "provided" in XBean 4.x, so we need to provide ASM
%pom_add_dep org.ow2.asm:asm:5.0.3:runtime plexus-container-default
%pom_add_dep org.ow2.asm:asm-commons:5.0.3:runtime plexus-container-default

# Generate OSGI info
%pom_xpath_inject "pom:project" "
    <packaging>bundle</packaging>
    <build>
      <plugins>
        <plugin>
          <groupId>org.apache.felix</groupId>
          <artifactId>maven-bundle-plugin</artifactId>
          <extensions>true</extensions>
          <configuration>
            <instructions>
              <_nouses>true</_nouses>
              <Export-Package>org.codehaus.plexus.component.annotations.*</Export-Package>
            </instructions>
          </configuration>
        </plugin>
      </plugins>
    </build>" plexus-component-annotations

# to prevent ant from failing
mkdir -p plexus-component-annotations/src/test/java

%build
pushd %{comp_name}
%{mvn_file} :%{comp_name} %{base_name}/%{comp_name}
%{mvn_build} \
%if %{without tests}
	-f \
%endif
%if %{?pkg_vcmp:%pkg_vcmp java-devel >= 9}%{!?pkg_vcmp:0}
	-- -Dmaven.compiler.release=6
%endif

# empty line, keep
popd

%install
pushd %{comp_name}
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}
popd

%files -f %{comp_name}/.mfiles
%license LICENSE-2.0.txt LICENSE.MIT

%files javadoc -f %{comp_name}/.mfiles-javadoc
%license LICENSE-2.0.txt LICENSE.MIT

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.0-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Sun Nov 24 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 2.1.0
- Removed patch:
  * 0001-Port-to-current-qdox.patch
    + integrated upstream
- Added patch:
  * plexus-containers-asm6.patch
    + allow building against asm6
- Specify maven.compiler.release to fix build with jdk9+ and newer
  maven-javadoc-plugin
* Thu Apr 11 2019 Fridrich Strba <fstrba@suse.com>
- Require for build the mvn(org.codehaus.plexus:plexus:pom:)
  instead of mvn(org.codehaus.plexus:plexus-containers:pom:)
  provided in the sources
* Wed Apr  3 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of the plexus-component-metadata 1.7.1 maven
  plugin
  * Generates META-INF/plexus/components.xml during maven build
