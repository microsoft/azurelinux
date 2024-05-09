Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package osgi-core
#
# Copyright (c) 2020 SUSE LLC
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


Name:           osgi-core
Version:        7.0.0
Release:        2%{?dist}
Summary:        OSGi Core API
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://www.osgi.org
Source0:        https://repo1.maven.org/maven2/org/osgi/osgi.core/%{version}/osgi.core-%{version}-sources.jar
Source1:        https://repo1.maven.org/maven2/org/osgi/osgi.core/%{version}/osgi.core-%{version}.pom
Source2:        https://www.apache.org/licenses/LICENSE-2.0
Source3:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  osgi-annotation
BuildRequires:  unzip
BuildArch:      noarch

%description
OSGi Core Release 7, Interfaces and Classes for use in compiling bundles.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package provides %{summary}.

%prep
%setup -q -c
mkdir -p lib
build-jar-repository -s lib osgi-annotation

cp -p %{SOURCE1} pom.xml
cp -p %{SOURCE2} LICENSE
cp -p %{SOURCE3} build.xml
mkdir -p src/main/java
mv org src/main/java/

%pom_xpath_inject pom:project '
<packaging>bundle</packaging>
<properties>
  <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
</properties>
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.felix</groupId>
      <artifactId>maven-bundle-plugin</artifactId>
      <extensions>true</extensions>
      <configuration>
        <instructions>
          <Bundle-Name>${project.artifactId}</Bundle-Name>
          <Bundle-SymbolicName>${project.artifactId}</Bundle-SymbolicName>
        </instructions>
      </configuration>
    </plugin>
  </plugins>
</build>'

%pom_add_dep org.osgi:osgi.annotation::provided

%build
ant jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 target/osgi.core-%{version}.jar %{buildroot}%{_javadir}/%{name}/osgi.core.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/osgi.core.pom
%add_maven_depmap %{name}/osgi.core.pom %{name}/osgi.core.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE

%files javadoc
%license LICENSE
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.0.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 7.0.0-1.4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Apr  1 2020 Fridrich Strba <fstrba@suse.com>
- Update to upstream version 7.0.0
* Mon Feb 11 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of osgi-core 6.0.0
