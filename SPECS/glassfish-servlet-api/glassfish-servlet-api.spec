#
# spec file for package glassfish-servlet-api
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
%global artifactId javax.servlet-api
Summary:        Java Servlet API
Name:           glassfish-servlet-api
Version:        3.1.0
Release:        4%{?dist}
License:        (CDDL-1.0 OR GPL-2.0-only WITH Classpath-exception-2.0) AND Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/Java
URL:            https://servlet-spec.java.net
Source0:        https://github.com/javaee/servlet-spec/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
Source2:        glassfish-servlet-api-build.xml
Source3:        glassfish-servlet-api-build.properties
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch

%description
The javax.servlet package contains a number of classes
and interfaces that describe and define the contracts between
a servlet class and the runtime environment provided for
an instance of such a class by a conforming servlet container.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n servlet-spec-%{version}
%pom_remove_plugin :maven-remote-resources-plugin
%pom_remove_plugin :maven-javadoc-plugin
cp -p %{SOURCE1} src/main/resources/META-INF/
cp -p %{SOURCE2} build.xml
cp -p %{SOURCE3} build.properties

# README contains also part of javax.servlet-api license
cp -p src/main/resources/META-INF/README .

%pom_remove_parent .

%build
ant package javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{artifactId}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a javax.servlet:servlet-api,org.apache.geronimo.specs:geronimo-servlet_3.0_spec,org.eclipse.jetty.orbit:javax.servlet
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc README
%license src/main/resources/META-INF/LICENSE-2.0.txt

%files javadoc
%{_javadocdir}/%{name}
%doc README
%license src/main/resources/META-INF/LICENSE-2.0.txt

%changelog
* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 3.1.0-4
- Moved from extended to core
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.0-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 3.1.0-2.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Apr  8 2019 Fridrich Strba <fstrba@suse.com>
- Do not depend at all on the parent pom, since we are not building
  with maven.

* Tue Jan 29 2019 Fridrich Strba <fstrba@suse.com>
- Initial package of javax.servlet-api 3.1.0
