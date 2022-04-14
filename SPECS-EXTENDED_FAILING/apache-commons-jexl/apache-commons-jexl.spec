Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package apache-commons-jexl
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


%global compatver 2.1.0
%define base_name jexl
%define short_name commons-%{base_name}
%bcond_with tests
Name:           apache-%{short_name}
Version:        2.1.1
Release:        2%{?dist}
Summary:        Java Expression Language (JEXL)
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://commons.apache.org/jexl
Source0:        http://www.apache.org/dist/commons/jexl/source/%{short_name}-%{version}-src.tar.gz
Source1:        %{short_name}-%{version}-build.tar.xz
# Patch to fix test failure with junit 4.11
Patch0:         001-Fix-tests.patch
# Fix javadoc build
Patch1:         apache-commons-jexl-javadoc.patch
Patch2:         0001-Port-to-current-javacc.patch
BuildRequires:  ant
BuildRequires:  apache-commons-logging
BuildRequires:  fdupes
BuildRequires:  javacc
BuildRequires:  javapackages-local-bootstrap
Requires:       mvn(commons-logging:commons-logging)
Provides:       %{short_name} = %{version}-%{release}
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildConflicts: java-devel >= 9
%endif

%description
Java Expression Language (JEXL) is an expression language engine which can be
embedded in applications and frameworks.  JEXL is inspired by Jakarta Velocity
and the Expression Language defined in the JavaServer Pages Standard Tag
Library version 1.1 (JSTL) and JavaServer Pages version 2.0 (JSP).  While
inspired by JSTL EL, it must be noted that JEXL is not a compatible
implementation of EL as defined in JSTL 1.1 (JSR-052) or JSP 2.0 (JSR-152).
For a compatible implementation of these specifications, see the Commons EL
project.

JEXL attempts to bring some of the lessons learned by the Velocity community
about expression languages in templating to a wider audience.  Commons Jelly
needed Velocity-ish method access, it just had to have it.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation/HTML
Provides:       %{short_name}-javadoc = %{version}-%{release}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src -a1
%patch0 -p1 -b .test
%patch1 -p1 -b .javadoc
%patch2 -p1

# Java 1.6 contains bsf 3.0, so we don't need the dependency in the pom.xml file
%pom_remove_dep org.apache.bsf:bsf-api
find \( -name '*.jar' -o -name '*.class' \) -delete
# Fix line endings
find -name '*.txt' -exec sed -i 's/\r//' '{}' +

# Drop "-SNAPSHOT" from version
%pom_xpath_set "pom:project/pom:version" %{compatver} jexl2-compat
%pom_xpath_set "pom:dependency[pom:artifactId='commons-jexl']/pom:version" %{version} jexl2-compat

%pom_remove_parent . jexl2-compat

%build
mkdir -p lib
build-jar-repository -s lib commons-logging

# commons-jexl
%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  -Djavacc.home=%{_javadir} \
  jar javadoc
# commons-jexl-compat
%{ant} \
  -f jexl2-compat/build.xml \
  -Dproject.version=%{compatver} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  jar javadoc

%install
# jars
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{short_name}.jar
ln -sf %{name}/%{short_name}.jar %{buildroot}%{_javadir}/%{short_name}.jar
install -pm 0644 jexl2-compat/target/%{short_name}-compat-%{compatver}.jar %{buildroot}%{_javadir}/%{name}/%{short_name}-compat.jar
ln -sf %{name}/%{short_name}-compat.jar %{buildroot}%{_javadir}/%{short_name}-compat.jar
# poms
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{short_name}.pom
%add_maven_depmap %{name}/%{short_name}.pom %{name}/%{short_name}.jar
install -pm 0644 jexl2-compat/pom.xml  %{buildroot}%{_mavenpomdir}/%{name}/%{short_name}-compat.pom
%add_maven_depmap %{name}/%{short_name}-compat.pom %{name}/%{short_name}-compat.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}/jexl2-compat
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
cp -pr jexl2-compat/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/jexl2-compat/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE.txt
%doc NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/%{short_name}*.jar

%files javadoc
%license LICENSE.txt
%doc NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.1.1-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix linebreak in sed command.

* Thu Feb 28 2019 Fridrich Strba <fstrba@suse.com>
- Initial package based on Fedora rpm
- Generate and sanitize ant build files
