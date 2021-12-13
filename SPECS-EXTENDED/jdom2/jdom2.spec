Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package jdom2
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


Name:           jdom2
Version:        2.0.6
Release:        3%{?dist}
Summary:        Java manipulation of XML
License:        Saxpath
Group:          Development/Libraries/Java
URL:            http://www.jdom.org/
Source0:        https://github.com/hunterhacker/jdom/archive/JDOM-%{version}.tar.gz
# originally taken from http://repo1.maven.org/maven2/org/jdom/jdom-contrib/1.1.3/jdom-contrib-1.1.3.pom
Source1:        jdom-contrib-template.pom
Source2:        jdom-junit-template.pom
# Use system libraries
# Disable gpg signatures
# Process contrib and junit pom files
Patch0:         0001-Adapt-build.patch
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  fdupes
BuildRequires:  isorelax
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jaxen
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  xml-apis
BuildArch:      noarch

%description
JDOM is a Java-oriented object model which models XML documents.
It provides a Java-centric means of generating and manipulating
XML documents. While JDOM inter-operates well with existing
standards such as the Simple API for XML (SAX) and the Document
Object Model (DOM), it is not an abstraction layer or
enhancement to those APIs. Rather, it provides a means of
reading and writing XML data.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n jdom-JDOM-%{version}
rm -r lib */lib
find -name '*.jar' -delete
find -name '*.class' -delete

%patch0 -p1

cp -p %{SOURCE1} maven/contrib.pom
cp -p %{SOURCE2} maven/junit.pom

sed -i 's/\r//' LICENSE.txt README.txt

# Unable to run coverage: use log4j12 but switch to log4j 2.x
sed -i.coverage "s|coverage, jars|jars|" build.xml

mkdir lib
build-jar-repository lib xerces-j2 xml-commons-apis jaxen junit isorelax xalan-j2 xalan-j2-serializer

%build
ant -Dversion=%{version} -Dcompile.target=6 -Dcompile.source=6 -Dj2se.apidoc=%{_javadocdir}/java maven

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 build/package/jdom-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
install -pm 0644 build/package/jdom-%{version}-contrib.jar %{buildroot}%{_javadir}/%{name}/%{name}-contrib.jar
install -pm 0644  build/package/jdom-%{version}-junit.jar %{buildroot}%{_javadir}/%{name}/%{name}-junit.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 build/maven/core/%{name}-%{version}.pom %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar
install -pm 0644 build/maven/core/%{name}-%{version}-contrib.pom %{buildroot}%{_mavenpomdir}/%{name}/%{name}-contrib.pom
%add_maven_depmap %{name}/%{name}-contrib.pom %{name}/%{name}-contrib.jar
install -pm 0644 build/maven/core/%{name}-%{version}-junit.pom  %{buildroot}%{_mavenpomdir}/%{name}/%{name}-junit.pom
%add_maven_depmap %{name}/%{name}-junit.pom %{name}/%{name}-junit.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr build/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc CHANGES.txt COMMITTERS.txt README.txt TODO.txt
%license LICENSE.txt

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.6-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 2.0.6-2.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix linebreak in sed command.

* Tue Oct  1 2019 Fridrich Strba <fstrba@suse.com>
- Remove unnecessary dependency on log4j
* Wed Feb 13 2019 Jan Engelhardt <jengelh@inai.de>
- Trim filler wording from description.
* Sat Feb  9 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of jdom2 version 2.0.6
