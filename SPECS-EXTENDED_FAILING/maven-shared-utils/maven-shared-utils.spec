Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-shared-utils
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
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
Name:           maven-shared-utils
Version:        3.2.1
Release:        2%{?dist}
Summary:        Maven shared utility classes
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/shared/maven-shared-utils
Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        %{name}-build.xml
# XXX temporary for maven upgrade
Patch0:         0001-Restore-compatibility-with-current-maven.patch
BuildRequires:  ant
BuildRequires:  apache-commons-io
BuildRequires:  fdupes
BuildRequires:  jansi
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jsr-305
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-utils
BuildRequires:  unzip
Requires:       mvn(commons-io:commons-io)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  apache-commons-lang3
BuildRequires:  maven-lib
BuildRequires:  maven-plugin-testing-harness
BuildRequires:  maven-resolver-api
%endif

%description
This project aims to be a functional replacement for plexus-utils in Maven.

It is not a 100% API compatible replacement though but a replacement with
improvements: lots of methods got cleaned up, generics got added and we dropped
a lot of unused code.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q
cp %{SOURCE1} build.xml

%patch0 -p1

%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin

%pom_remove_parent .
%pom_xpath_inject pom:project "<groupId>org.apache.maven.shared</groupId>" .

%build
mkdir -p lib
build-jar-repository -s lib commons-io jansi/jansi jsr305 \
  plexus/classworlds plexus-containers/plexus-container-default plexus/utils
%if %{with tests}
  build-jar-repository -s lib commons-lang3 maven/maven-artifact maven/maven-core \
    maven/maven-model maven-plugin-testing/maven-plugin-testing-harness \
    maven-resolver/maven-resolver-api
%endif

%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc
%license LICENSE NOTICE
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.2.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.2.1-1.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Thu Mar 14 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-shared-utils 3.2.1
- Generate and customize ant build.xml
