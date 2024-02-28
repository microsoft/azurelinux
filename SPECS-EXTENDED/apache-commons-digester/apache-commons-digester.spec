%define base_name       digester
%define short_name      commons-%{base_name}
Summary:        Jakarta Commons Digester Package
Name:           apache-%{short_name}
Version:        2.1
Release:        4%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/proper/commons-digester
Source0:        https://dlcdn.apache.org/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  commons-beanutils
BuildRequires:  commons-collections
BuildRequires:  commons-logging
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
Requires:       commons-beanutils
Requires:       commons-logging
Provides:       %{short_name} = %{version}-%{release}
Obsoletes:      %{short_name} < %{version}-%{release}
BuildArch:      noarch
%if 0%{?with_check}
BuildRequires:  ant-junit
%endif

%description
The goal of the Jakarta Commons Digester project is to create and
maintain an XML to Java object mapping package written in the Java
language to be distributed under the ASF license.

%package javadoc
Summary:        Javadoc for apache-commons-digester
Group:          Development/Libraries/Java

%description javadoc
The goal of the Jakarta Commons Digester project is to create and
maintain a XML -> Java object mapping package written in the Java
language to be distributed under the ASF license.

This package contains the javadoc documentation for the Jakarta Commons
Digester Package.

%prep
%setup -q -n %{short_name}-%{version}-src
cp %{SOURCE1} build.xml

mkdir -p lib
build-jar-repository -s lib commons-beanutils commons-logging

%pom_remove_parent

%build
ant jar javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -pm 644 target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -s %{name}.jar %{buildroot}%{_javadir}/%{short_name}.jar
# pom
install -d -m 0755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a org.apache.commons:%{short_name}
# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}/%{name}/

%check
build-jar-repository -s lib commons-collections
ant test

%files -f .mfiles
%license LICENSE.txt
%doc NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/*

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Mon Nov 07 2022 Sumedh Sharma <sumsharma@microsoft.com> - 2.1-4
- Enable check section
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 27 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.1-2.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Mar 27 2019 Fridrich Strba <fstrba@suse.com>
- Use global defines for name

* Mon Feb 25 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to 2.1
  * Breaking changes:
    + The minimum JDK requirement is now JDK 1.5. The provided
    binaries will not work on lower JDKs. The source has been
    updated to leverage Generics and other JDK 1.5 features where
    possible, and requires JDK 1.5 to compile.
    + This release eliminates all dependencies on Commons
    Collections classes. Previously, ArrayStack was used in the
    Digester implementation and was exposed via protected fields
    or inner classes of the following classes:
  - org.apache.commons.digester.Digester,
  - org.apache.commons.digester.CallParamRule, and
  - org.apache.commons.digester.xmlrules.DigesterRuleParser
    These classes now use java.util.Stack instead. Any subclasses
    of the above using protected ArrayStack members will require
    appropriate migration to use java.util.Stack instead before
    they can be used with version 2.0 or later.
  * Important changes:
    + The legacy schema support has been deprecated in favor of
    javax.xml.validation.Schema support.
  * New features:
    + Support for XML Schema validation using
    javax.xml.validation.Schema  has been added to Digester.
    See Digester class Javadoc, and
    Digester#setSchema(javax.xml.validation.Schema) method.
    This allows usage of W3C XML Schema, Relax NG and Schematron
    for validation of XML documents.
    The legacy schema support has been deprecated (details below).
    + The underlying SAXParser factory can now be easily configured
    to be XInclude aware. This allows for general purpose
    inclusion of XML or text documents, for example, and
    facilitates document modularity.
    + Added a new package 'annotations' that provides for Java5
    Annotations  meta-data based definition of rules for Digester.
    This improves maintainability of both Java code and XML
    documents, as  rules are now defined in POJOs and generating
    Digester parsers at  runtime, avoiding manual updates.
  * Bugs from previous release:
    + SetPropertyRule throws java.lang.IllegalArgumentException:
    No name specified when matched element has no attributes.
    [DIGESTER-114]
    + Missing unit tests using Ant and Maven. [DIGESTER-117]
    + Digesting XML content with NodeCreateRule swallows spaces.
    [DIGESTER-120]
    + Potential NullPointerException if debug is enabled in
    Digester#resolveEntity() [DIGESTER-122]
    + Clear inputSources list in method Digester.clear()
    [DIGESTER-125]
    + Potential NullPointerException if debug is enabled in
    FactoryCreateRule#begin() [DIGESTER-126]
  * Improvements from previous release:
    + Null arguments to all Digester#parse() methods now throw an
    IllegalArgumentException. [DIGESTER-111]
    + 'serialVersionUID' fields have been added to Serializable
    classes.
- Generate ant build files that were removed in 2.1 by upstream
- Removed patch:
  * apache-commons-digester-build.patch
    + the generated build is handling the build classpath
    differently

* Fri Dec 21 2018 Fridrich Strba <fstrba@suse.com>
- Renamed package to apache-commons-digester
- Removed patch:
  * jakarta-commons-digester-java16compat.patch
    + no need to patch build.xml to build with source/target 1.6
- Added patch:
  * apache-commons-digester-build.patch
    + add commons-collections to the build classpath

* Mon Sep 18 2017 fstrba@suse.com
- Removed patch:
  * jakarta-commons-digester-java14compat.patch
- Added patch:
  * jakarta-commons-digester-java16compat.patch
  - Build with java source and target 1.6
  - Fixes build with jdk9
- Align the spec file to the way the ant build gets its
  dependencies and fix the javadoc build

* Tue Jul  8 2014 tchvatal@suse.com
- Cleanup with spec cleaner and fix build again.

* Mon Sep 25 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5

* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires

* Wed Jul 27 2005 jsmeix@suse.de
- Current version 1.7 from JPackage.org

* Mon Jul 18 2005 jsmeix@suse.de
- Current version 1.6 from JPackage.org

* Tue Feb 22 2005 skh@suse.de
- enable build of rss package (needed by struts)

* Mon Feb 21 2005 skh@suse.de
- update to version 1.6
- don't use icecream

* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage

* Sun Sep  5 2004 skh@suse.de
- Initial package created with version 1.5 (JPackage version 1.5)
