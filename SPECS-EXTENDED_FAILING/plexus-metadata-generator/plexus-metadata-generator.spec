Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-metadata-generator
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
%global comp_name component-metadata
%bcond_with tests
Name:           plexus-metadata-generator
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
Source100:      %{base_name}-build.tar.xz
Patch0:         plexus-containers-asm6.patch
Patch1:         plexus-metadata-generator-cli.patch
Patch1000:      %{name}-nomojo.patch
BuildRequires:  ant
BuildRequires:  apache-commons-cli
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jdom2
BuildRequires:  junit
BuildRequires:  objectweb-asm
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-cli
BuildRequires:  plexus-containers-component-annotations
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-utils
BuildRequires:  qdox >= 2
BuildRequires:  xbean
Requires:       apache-commons-cli
Requires:       guava
Requires:       jdom2
Requires:       objectweb-asm
Requires:       plexus-cli
Requires:       plexus-containers-component-annotations = %{version}
Requires:       plexus-containers-container-default = %{version}
Requires:       plexus-utils
Requires:       qdox >= 2
Requires:       xbean
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
%endif

%description
Plexus contains end-to-end developer tools for writing applications.
At the core is the container, which can be embedded or for an
application server. There are many reusable components for hibernate,
form processing, jndi, i18n, velocity, etc. Plexus also includes an
application server which is like a J2EE application server.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
%{summary}.

%prep
%setup -q -n %{base_name}-%{base_name}-%{version} -a100

mkdir -p lib
build-jar-repository -s lib %{base_name} objectweb-asm/asm objectweb-asm/asm-commons plexus/classworlds plexus/utils jdom2/jdom2 commons-cli qdox plexus/cli
%if %{with tests}
build-jar-repository -s lib hamcrest/core
%endif

%patch0 -p1
%patch1 -p1

%patch1000 -p1

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

rm -rf plexus-%{comp_name}/src/main/java/org/codehaus/plexus/maven
rm -rf plexus-%{comp_name}/src/main/resources/META-INF/maven

%pom_remove_dep :maven-core plexus-%{comp_name}
%pom_remove_dep :maven-model plexus-%{comp_name}
%pom_remove_dep :maven-plugin-api plexus-%{comp_name}

%pom_remove_parent plexus-%{comp_name}
%pom_xpath_inject "pom:project" "
  <groupId>org.codehaus.plexus</groupId>
  <version>%{version}</version>
" plexus-%{comp_name}
%pom_xpath_set "pom:project/pom:artifactId" %{name} plexus-%{comp_name}

%build
pushd plexus-%{comp_name}
  ant \
     -f generator-build.xml \
%if %{without tests}
    -Dtest.skip=true \
%endif
    jar javadoc
popd

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 plexus-%{comp_name}/target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 plexus-%{comp_name}/pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr plexus-%{comp_name}/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}
# script
%jpackage_script org.codehaus.plexus.metadata.PlexusMetadataGeneratorCli "" "" %{name}:%{base_name}/plexus-container-default:%{base_name}/plexus-component-annotations:objectweb-asm/asm:plexus-classworlds:plexus/utils:jdom2/jdom2:commons-cli:qdox:plexus/cli:guava/guava:xbean/xbean-reflect %{name}

%files -f .mfiles
%license LICENSE-2.0.txt LICENSE.MIT
%{_bindir}/%{name}

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
- Removed patch:
  * 0001-Port-to-current-qdox.patch
    + integrated upstream
- Added patches:
  * plexus-containers-asm6.patch
    + allow building against asm6
  * plexus-metadata-generator-cli.patch
    + bring back the PlexusMetadataGeneratorCli.java removed by
    upstream, but which we use heavily
* Tue Apr  9 2019 Fridrich Strba <fstrba@suse.com>
- Remove reference to parent pom, since we are not building with
  Maven.
- Clean the classpath of the script to include only neede jars
* Sat Mar 23 2019 Jan Engelhardt <jengelh@inai.de>
- plexus-metadata-generator.spec: Describe package, not project.
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
