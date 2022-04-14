Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-containers
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


%bcond_with tests
Name:           plexus-containers
Version:        2.1.0
Release:        2%{?dist}
Summary:        Containers for Plexus
# Most of the files are either under ASL 2.0 or MIT
# The following files are under xpp:
# plexus-component-metadata/src/main/java/org/codehaus/plexus/metadata/merge/Driver.java
# plexus-component-metadata/src/main/java/org/codehaus/plexus/metadata/merge/MXParser.java
License:        Apache-2.0 AND MIT AND xpp
Group:          Development/Libraries/Java
URL:            https://github.com/codehaus-plexus/plexus-containers
Source0:        https://github.com/codehaus-plexus/%{name}/archive/%{name}-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
Source2:        LICENSE.MIT
Source100:      %{name}-build.tar.xz
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  guava
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-utils
BuildRequires:  xbean
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  objectweb-asm
%endif

%description
Plexus contains end-to-end developer tools for writing applications.
At the core is the container, which can be embedded or for an
application server. There are many reusable components for hibernate,
form processing, jndi, i18n, velocity, etc. Plexus also includes an
application server which is like a J2EE application server.

%package component-annotations
Summary:        Component API from %{name}
Group:          Development/Libraries/Java

%description component-annotations
%{summary}.

%package container-default
Summary:        Default Container from %{name}
Group:          Development/Libraries/Java
Requires:       mvn(com.google.guava:guava)
Requires:       mvn(org.apache.xbean:xbean-reflect)
Requires:       mvn(org.codehaus.plexus:plexus-classworlds)
Requires:       mvn(org.codehaus.plexus:plexus-utils)
Requires:       mvn(org.ow2.asm:asm)
Requires:       mvn(org.ow2.asm:asm-commons)

%description container-default
%{summary}.

%package javadoc
Summary:        API documentation for all plexus-containers packages
Group:          Documentation/HTML

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{name}-%{version} -a100

mkdir -p lib
build-jar-repository -s lib plexus/classworlds plexus/utils guava/guava junit xbean/xbean-reflect
%if %{with tests}
build-jar-repository -s lib objectweb-asm/asm objectweb-asm/asm-commons hamcrest/core
%endif

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
for i in plexus-component-annotations plexus-container-default; do
  pushd ${i}
  	%pom_remove_parent .
	%pom_xpath_inject "pom:project" "<groupId>org.codehaus.plexus</groupId><version>%{version}</version>" .
    ant \
%if %{without tests}
      -Dtest.skip=true \
%endif
      jar javadoc
  popd
done

%install
# jars
install -dm 0755 %{buildroot}%{_javadir}/%{name}
for i in plexus-component-annotations plexus-container-default; do
  install -pm 0644 ${i}/target/${i}-%{version}.jar %{buildroot}%{_javadir}/%{name}/${i}.jar
done
install -dm 0755 %{buildroot}%{_javadir}/plexus
# keep compat symlink for maven's sake
ln -sf ../%{name}/plexus-component-annotations.jar %{buildroot}%{_javadir}/plexus/containers-component-annotations.jar

# poms
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
for i in plexus-component-annotations plexus-container-default; do
  install -pm 0644 ${i}/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/${i}.pom
done
%add_maven_depmap %{name}/plexus-component-annotations.pom %{name}/plexus-component-annotations.jar -f component-annotations
%add_maven_depmap %{name}/plexus-container-default.pom %{name}/plexus-container-default.jar -f container-default -a org.codehaus.plexus:containers-component-api

# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
for i in plexus-component-annotations plexus-container-default; do
  cp -pr ${i}/target/site/apidocs %{buildroot}%{_javadocdir}/%{name}/${i}
done
%fdupes -s %{buildroot}%{_javadocdir}

%files component-annotations -f .mfiles-component-annotations
%license LICENSE-2.0.txt LICENSE.MIT
%{_javadir}/plexus

%files container-default -f .mfiles-container-default
%license LICENSE-2.0.txt LICENSE.MIT

%files javadoc
%license LICENSE-2.0.txt LICENSE.MIT
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.1.0-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Sun Nov 24 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 2.1.0
  * Does not build plexus-component-javadoc any more
- Removed patch:
  * 0001-Port-to-current-qdox.patch
    + integrated upstream
- Do not force building with java < 9 any more
* Tue Apr  9 2019 Fridrich Strba <fstrba@suse.com>
- Remove references to parent poms since we are not building with
  Maven.
* Fri Mar 22 2019 Fridrich Strba <fstrba@suse.com>
- Add another spec file to build plexus-metadata-generator in order
  to be able to generate plexus components.xml descriptor
- Added patch:
  * plexus-metadata-generator-nomojo.patch
    + Allow building this command-line tool without needing to use
    exceptions defined in maven-plugin-api
* Sun Mar  3 2019 Jan Engelhardt <jengelh@inai.de>
- Describe package, not project.
* Sat Mar  2 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of plexus-containers 1.7.1
- Generate and customize ant build files
- Leave out the plexus-component-metadata that will be built
  by a different spec file
