Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-invoker
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
Name:           maven-invoker
Version:        3.0.1
Release:        2%{?dist}
Summary:        An API for firing a maven build in a clean environment
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/shared/maven-invoker/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        %{name}-build.xml
# Patch rejected upstream
Patch1:         %{name}-MSHARED-279.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  maven-shared-utils
BuildRequires:  plexus-containers-component-annotations
BuildRequires:  plexus-metadata-generator
BuildRequires:  plexus-utils
BuildRequires:  unzip
Requires:       mvn(org.apache.maven.shared:maven-shared-utils)
Requires:       mvn(org.codehaus.plexus:plexus-component-annotations)
Requires:       mvn(org.codehaus.plexus:plexus-utils)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-clean-plugin)
%endif

%description
This API is concerned with firing a Maven build in a new JVM. It accomplishes
its task by building up a conventional Maven command line from options given in
the current request, along with those global options specified in the invoker
itself. Once it has the command line, the invoker will execute it, and capture
the resulting exit code or any exception thrown to signal a failure to execute.
Input/output control can be specified using an InputStream and up to two
InvocationOutputHandlers.

This is a replacement package for maven-shared-invoker

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q
cp %{SOURCE1} build.xml
%patch1 -p1

%pom_remove_parent .
%pom_xpath_inject pom:project "<groupId>org.apache.maven.shared</groupId>" .

%build
mkdir -p lib
build-jar-repository -s lib plexus/utils plexus-containers/plexus-component-annotations maven-shared-utils/maven-shared-utils
%if %{with tests}
  export M2_HOME=%{_datadir}/xmvn
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
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.0.1-1.6 
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Thu Nov 21 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 3.0.1
  * needed by xmvn-tools >= 3.1.0
- Modified patch:
  * maven-invoker-MSHARED-279.patch
    + rediff to changed context
* Mon Apr  1 2019 Jan Engelhardt <jengelh@inai.de>
- Use noun phrase in summary.
* Thu Mar 14 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-invoker 2.2
- Generate and customize ant build.xml file
