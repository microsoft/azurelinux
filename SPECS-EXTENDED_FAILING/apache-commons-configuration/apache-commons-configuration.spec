Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package apache
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


%global base_name       configuration
%global short_name      commons-%{base_name}
Name:           apache-%{short_name}
Version:        1.10
Release:        4%{?dist}
Summary:        Commons Configuration Package
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://commons.apache.org/%{base_name}/
Source0:        http://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  apache-commons-beanutils
BuildRequires:  apache-commons-codec
BuildRequires:  apache-commons-collections
BuildRequires:  apache-commons-digester
BuildRequires:  apache-commons-jexl
BuildRequires:  apache-commons-jxpath
BuildRequires:  apache-commons-lang
BuildRequires:  apache-commons-logging
BuildRequires:  apache-commons-vfs2
BuildRequires:  fdupes
BuildRequires:  glassfish-servlet-api
BuildRequires:  javacc
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  xml-resolver
Requires:       mvn(commons-lang:commons-lang)
Requires:       mvn(commons-logging:commons-logging)
BuildArch:      noarch

%description
Configuration is a project to provide a generic Configuration
interface and allow the source of the values to vary. It
provides easy typed access to single, as well as lists of
configuration values based on a 'key'.
Right now you can load properties from a simple properties
file, a properties file in a jar, an XML file, JNDI settings,
as well as use a mix of different sources using a
ConfigurationFactory and CompositeConfiguration.
Custom configuration objects are very easy to create now
by just subclassing AbstractConfiguration. This works
similar to how AbstractList works.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description    javadoc
%{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src
cp %{SOURCE1} build.xml
sed -i 's/\r//' LICENSE.txt NOTICE.txt

%pom_remove_parent

%build
mkdir -p lib
build-jar-repository -s -p lib \
  commons-beanutils commons-codec commons-collections commons-digester \
  commons-jexl commons-jxpath commons-lang commons-logging commons-vfs2 \
  glassfish-servlet-api xml-resolver \
  javacc
# We skip tests because we don't have test deps (dbunit in particular).
ant \
  -Dtest.skip=true \
  jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{short_name}.jar
ln -sf %{short_name}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{short_name}.pom
%add_maven_depmap %{short_name}.pom %{short_name}.jar -a org.apache.commons:%{short_name}
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%{_javadir}/%{name}.jar

%files javadoc
%license LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.10-3.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix linebreak in sed command.

* Tue Oct  1 2019 Fridrich Strba <fstrba@suse.com>
- Remove the bogus log4j dependency
* Wed Mar 27 2019 Fridrich Strba <fstrba@suse.com>
- Remove pom parent, since we don't use it when not building with
  maven
* Mon Mar  4 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of apache-commons-configuration 1.10
- Generate and customze ant build file
