Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package glassfish-el
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


%global reltag b08
%global verbase 3.0.1
%bcond_with tests
Name:           glassfish-el
Version:        %{verbase}~%{reltag}
Release:        2%{?dist}
Summary:        J2EE Expression Language Implementation
License:        CDDL-1.1 OR GPL-2.0-only WITH Classpath-exception-2.0
Group:          Development/Libraries/Java
URL:            http://uel.java.net
# svn export https://svn.java.net/svn/uel~svn/tags/javax.el-%{verbase}-%{reltag}/ glassfish-el-%{verbase}-%{reltag}
# rm -r glassfish-el-%{verbase}-%{reltag}/fonts
# rm -r glassfish-el-%{verbase}-%{reltag}/parent-pom
# rm -r glassfish-el-%{verbase}-%{reltag}/repo
# rm -r glassfish-el-%{verbase}-%{reltag}/spec
# rm -r glassfish-el-%{verbase}-%{reltag}/uel
# rm -r glassfish-el-%{verbase}-%{reltag}/www
# tar cJf glassfish-el-%{verbase}-%{reltag}.tar.xz glassfish-el-%{verbase}-%{reltag}
Source0:        %{name}-%{verbase}-%{reltag}-clean.tar.xz
Source1:        %{name}-%{verbase}-%{reltag}-build.tar.xz
Source2:        http://www.apache.org/licenses/LICENSE-2.0.txt
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javacc
BuildRequires:  javapackages-local-bootstrap
Requires:       %{name}-api = %{version}
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
%endif

%description
This project provides an implementation of the Expression Language (EL).
The main goals are:
 * Improves current implementation: bug fixes and performance improvements
 * Provides API for use by other tools, such as Netbeans

%package api
Summary:        Expression Language 3.0 API
License:        (CDDL-1.0 OR GPL-2.0-only WITH Classpath-exception-2.0) AND Apache-2.0
Group:          Development/Libraries/Java

%description api
Expression Language 3.0 API.

%package javadoc
Summary:        Javadoc for %{name}
License:        (CDDL-1.0 OR GPL-2.0-only WITH Classpath-exception-2.0) AND Apache-2.0
Group:          Documentation/HTML

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{verbase}-%{reltag} -a1

cp -p %{SOURCE2} .

%pom_remove_plugin -r :findbugs-maven-plugin
%pom_remove_plugin -r :findbugs-maven-plugin api
%pom_remove_plugin -r :glassfish-copyright-maven-plugin

# Useless tasks
%pom_remove_plugin -r :maven-release-plugin
%pom_remove_plugin -r :maven-release-plugin api
%pom_remove_plugin -r :maven-source-plugin
%pom_remove_plugin -r :maven-source-plugin api

# Fix javadoc task
%pom_xpath_remove "pom:plugin[pom:artifactId ='maven-javadoc-plugin']/pom:executions/pom:execution/pom:goals"
%pom_xpath_remove "pom:plugin[pom:artifactId ='maven-javadoc-plugin']/pom:executions/pom:execution/pom:goals" api
%pom_xpath_remove "pom:plugin[pom:artifactId ='maven-javadoc-plugin']/pom:executions/pom:execution/pom:configuration/pom:sourcepath"

# Fix apis version
%pom_xpath_set "pom:project/pom:version" %{verbase}-%{reltag} api
# Add missing build dep
%pom_add_dep javax.el:javax.el-api:'${project.version}'

%{mvn_file} javax.el:javax.el-api %{name}-api
%{mvn_alias} javax.el:javax.el-api "javax.el:el-api" "org.glassfish:javax.el-api"

%{mvn_file} org.glassfish:javax.el %{name}
%{mvn_alias} org.glassfish:javax.el "org.eclipse.jetty.orbit:com.sun.el" "org.glassfish.web:javax.el" "org.glassfish:javax.el-impl"

%pom_remove_parent . api

# Let javacc regenerate this one to avoid some type incompatibilities
rm impl/src/main/java/com/sun/el/parser/TokenMgrError.java

%build
mkdir -p lib
%{ant} \
  -Djavacc.home=%{_javadir} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  all

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 api/target/javax.el-api-%{verbase}-%{reltag}.jar %{buildroot}%{_javadir}/%{name}-api.jar
install -pm 0644 target/javax.el-%{verbase}-%{reltag}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 api/pom.xml %{buildroot}%{_mavenpomdir}/%{name}-api.pom
%add_maven_depmap %{name}-api.pom %{name}-api.jar -a "javax.el:el-api,org.glassfish:javax.el-api" -f api
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a "org.eclipse.jetty.orbit:com.sun.el,org.glassfish.web:javax.el,org.glassfish:javax.el-impl"
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}/api
cp -pr api/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/api/
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

cp -p api/src/main/javadoc/doc-files/*-spec-license.html .

%files -f .mfiles

%files api -f .mfiles-api
%license LICENSE-2.0.txt *-spec-license.html

%files javadoc
%license LICENSE-2.0.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.1~b08-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.0.1~b08-1.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Mar  5 2019 Fridrich Strba <fstrba@suse.com>
- Intial package for glassfish-el 3.0.1-b08
- Generate and customize the ant build system
