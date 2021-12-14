Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package ws-jaxme
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


%define base_name jaxme
Name:           ws-jaxme
Version:        0.5.2
Release:        7%{?dist}
Summary:        Open source implementation of JAXB
License:        Apache-2.0
Group:          Development/Libraries/Java
Url:            http://ws.apache.org
Source0:        ws-jaxme-%{version}-src.tar.bz2
Patch0:         ws-jaxme-docs_xml.patch
Patch1:         ws-jaxme-catalog.patch
Patch2:         ws-jaxme-java6.patch
Patch3:         ws-jaxme-sourcetarget.patch
Patch4:         ws-jaxme-use-commons-codec.patch
Patch5:         ws-jaxme-0.5.2-proxygenerator.patch
Patch6:         ws-jaxme-doclint-ignore.patch
BuildRequires:  ant >= 1.6
BuildRequires:  ant-apache-resolver
BuildRequires:  antlr
BuildRequires:  apache-commons-codec
BuildRequires:  docbook-xsl-stylesheets
BuildRequires:  docbook-dtd-xml
BuildRequires:  hsqldb
BuildRequires:  java-devel >= 1.6
BuildRequires:  javapackages-tools
BuildRequires:  jaxp_transform_impl
BuildRequires:  junit >= 3.8.1
BuildRequires:  log4j12
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-apis
BuildRequires:  xml-commons-resolver
BuildRequires:  xmldb-api
BuildArch:      noarch

%description
A Java/XML binding compiler takes as input a schema description (in
   most cases an XML schema, but it may be a DTD, a RelaxNG schema,
   a Java class inspected via reflection, or a database schema). The
   output is a set of Java classes: * A Java bean class matching the
   schema description. (If the schema was obtained via Java
   reflection, the original Java bean class.)

* Read a conforming XML document and convert it into the equivalent
   Java bean.

* Vice versa, marshal the Java bean back into the original XML
document.

%package        javadoc
Summary:        Open source implementation of JAXB
Group:          Development/Libraries/Java

%description    javadoc
A Java/XML binding compiler takes as input a schema description (in
   most cases an XML schema, but it may be a DTD, a RelaxNG schema,
   a Java class inspected via reflection, or a database schema). The
   output is a set of Java classes: * A Java bean class matching the
   schema description. (If the schema was obtained via Java
   reflection, the original Java bean class.)

* Read a conforming XML document and convert it into the equivalent
   Java bean.

* Vice versa, marshal the Java bean back into the original XML
document.

%package        manual
Summary:        Open source implementation of JAXB
Group:          Development/Libraries/Java

%description    manual
A Java/XML binding compiler takes as input a schema description (in
   most cases an XML schema, but it may be a DTD, a RelaxNG schema,
   a Java class inspected via reflection, or a database schema). The
   output is a set of Java classes: * A Java bean class matching the
   schema description. (If the schema was obtained via Java
   reflection, the original Java bean class.)

* Read a conforming XML document and convert it into the equivalent
   Java bean.

* Vice versa, marshal the Java bean back into the original XML
document.

%prep
%setup -q
find . -name "*.jar" | xargs rm
%patch0 -b .sav
%patch1 -b .sav
%patch2 -b .java6
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
export OPT_JAR_LIST="ant/ant-trax jaxp_transform_impl ant/ant-apache-resolver"
export CLASSPATH=$(build-classpath \
    antlr \
    apache-commons-codec \
    hsqldb \
    log4j12/log4j-12 \
    xalan-j2 \
    xalan-j2-serializer \
    xmldb-api \
    xerces-j2 \
    xml-commons-apis \
    xml-commons-resolver \
    junit)
ant  Docs.all \
    -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 \
    -Dbuild.sysclasspath=first \
    -Ddocbook.home=%{_datadir}/xml/docbook \
    -Ddocbookxsl.home=%{_datadir}/xml/docbook/xsl-stylesheets-1.79.1

%install
install -dm 755 %{buildroot}%{_javadir}/%{base_name}
for jar in dist/*.jar; do
   jbs=`basename ${jar}`
   jnm=`echo ${jbs} | sed -e 's|\.jar||'`
   install -Dpm 644 ${jar} \
     %{buildroot}%{_javadir}/%{base_name}/ws-${jnm}.jar
done
(cd %{buildroot}%{_javadir}/%{base_name} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
(cd %{buildroot}%{_javadir}/%{base_name} && for jar in ws-*.jar; do ln -sf ${jar} `echo $jar| sed  "s|ws-||g"`; done)
#javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr build/docs/src/documentation/content/apidocs %{buildroot}%{_javadocdir}/%{name}
#manual
install -dm 755 %{buildroot}%{_docdir}/%{name}-%{version}
cp -pr build/docs/src/documentation/content/manual %{buildroot}%{_docdir}/%{name}-%{version}

%files
%doc LICENSE
%{_javadir}/%{base_name}

%files javadoc
%{_javadocdir}/%{name}

%files manual
%doc %{_docdir}/%{name}-%{version}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.2-7
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Dec 02 2020 Joe Schmitt <joschmit@microsoft.com> - 0.5.2-6.4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Set javadoc Xdoclint:none with ws-jaxme-doclint-ignore.patch.
- Add dependency on docbook-dtd-xml and update docbook paths.

* Tue Oct  1 2019 Fridrich Strba <fstrba@suse.com>
- Build against new compatibility package log4j12
* Fri Oct  5 2018 Fridrich Strba <fstrba@suse.com>
- Fix for a build breakages on i586 with jdk11
  * Working around a possible race condition
  * Allows building with jdk11
* Fri Sep 28 2018 Fridrich Strba <fstrba@suse.com>
- BuildConflict with java-devel >= 11, since it fails intermitently
  on i586 with jdk11
* Mon Dec  4 2017 thomas.schraitle@suse.com
- Fix catalog paths in ws-jaxme-catalog.patch
  The DocBook XML 4.1.2 DTD cannot be retrieved from SGML catalogs
  (/etc/sgml/catalog) but from XML catalogs (/etc/xml/catalog).
  Corrected path from /etc/sgml/catalog to /etc/xml/catalog.
* Fri Oct  6 2017 fstrba@suse.com
- Allow building with jdk9
- Attached patch:
  * ws-jaxme-0.5.2-proxygenerator.patch
  - Generate correctly proxies even if the interface has static
    methods that are allowed in jdk8+
* Tue Sep 12 2017 fstrba@suse.com
- Upgrade to 0.5.2
- BuildConflict with java-devel >= 1.9, since this package cannot
  be built with jdk9
- BuildRequire java-devel >= 1.6
- Specify java source and target level 1.6
- Modified patch:
  * ws-jaxme-java6.patch
  - Adapt to the new context
- Added patches:
  * ws-jaxme-sourcetarget.patch
  - Build with java source and target level 1.6
  * ws-jaxme-use-commons-codec.patch
  - Use apache-commons-codec for base64 functionality instead
    or private APIs that can disapear any time
* Fri Jul 11 2014 tchvatal@suse.com
- Do not version javadoc dir.
* Tue Jul  8 2014 tchvatal@suse.com
- Do not depend on ant-trax.
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Thu May 14 2009 mvyskocil@suse.cz
- Initial SUSE packaging (based on jpackage.org 5.0)
