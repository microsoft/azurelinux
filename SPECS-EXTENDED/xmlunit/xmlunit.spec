Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package xmlunit
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2000-2008, JPackage Project
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


Name:           xmlunit
Version:        1.5
Release:        10%{?dist}
Summary:        Provides classes to do asserts on XML
License:        BSD-3-Clause
Group:          Development/Libraries/Java
URL:            https://xmlunit.sourceforge.net/
Source0:        https://download.sourceforge.net/%{name}/%{name}-%{version}-src.zip
Source1:        https://repo1.maven.org/maven2/%{name}/%{name}/%{version}/%{name}-%{version}.pom
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  fdupes
# Needed for maven conversions
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  javapackages-tools
BuildRequires:  junit
BuildRequires:  unzip
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-apis >= 1.3
Requires:       junit
Requires:       xalan-j2
Requires:       xerces-j2
Requires:       xml-commons-apis >= 1.3
BuildArch:      noarch

%description
XMLUnit extends JUnit to simplify unit testing of XML. It compares a control
XML document to a test document or the result of a transformation, validates
documents against a DTD, and (from v0.5) compares the results of XPath
expressions.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}. Also contains userguide.

%prep
%setup -q

perl -pi -e 's/
$//g' README.txt LICENSE.txt

# remove all binary libs and javadocs
find . -name "*.jar" -delete

%build

cat > build.properties << EOF
junit.lib=$(build-classpath junit)
xmlxsl.lib=$(build-classpath xalan-j2 xerces-j2 xml-commons-jaxp-1.3-apis)
test.report.dir=test
EOF

cat > docbook.properties <<EOF
db5.xsl=%{_datadir}/xml/docbook/stylesheet/nwalsh/current/
EOF

export CLASSPATH=
export OPT_JAR_LIST="junit ant/ant-junit jaxp_transform_impl ant/ant-trax xalan-j2-serializer"
ant -Djavac.source=1.6 -Djavac.target=1.6 -Dbuild.compiler=modern -Dhaltonfailure=yes jar javadocs

%install
mkdir -p %{buildroot}%{_javadir}
install -m 0644 build/lib/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir}/ && ln -s %{name}-%{version}.jar %{name}.jar)

# Javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr build/doc/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -m 644 %{SOURCE1} \
    %{buildroot}%{_mavenpomdir}/%{name}-%{version}.pom
%add_maven_depmap %{name}-%{version}.pom %{name}-%{version}.jar

%files
%license LICENSE.txt
%doc README.txt
%{_javadir}/*.jar
%{_mavenpomdir}/*
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif

%files javadoc
%doc userguide
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5-10
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.5-9.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Nov  7 2018 Fridrich Strba <fstrba@suse.com>
- Do not depend on a particular xml-commons-apis provider.
* Tue Sep 19 2017 fstrba@suse.com
- Specify java source and target level 1.6 in order to allow build
  with jdk9
- Clean spec file and fix duplicate waste rpmlint error
* Fri May 19 2017 vsistek@suse.com
- Add BuildRequires: javapackages-local (for maven conversions)
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Thu Dec  4 2014 p.drouand@gmail.com
- Remove java-devel dependency; not needed anymore
* Fri Jul 11 2014 tchvatal@suse.com
- Drop xmlunit1.0.zip as it is not used anywhere.
* Tue Jul  8 2014 tchvatal@suse.com
- Cleanup with spec-cleaner a bit.
* Mon Jul  7 2014 tchvatal@suse.com
- Depend on junit not junit4. Replace ant-trax with ant.
* Tue Oct  8 2013 mvyskocil@suse.com
- Build with junit4
* Thu Oct  3 2013 mvyskocil@suse.com
- Update to 1.5
  * If one node in the comparison has children while the other one
    has not, XMLUnit 1.5 will signal a CHILD_NODELIST_LEN GTH
    difference and CHILD_NODE_NOT_FOUND differences for each child
    node of the node that has children in addition to a
    HAS_CHILD_NODES difference.
  1.4:
  * xsi:type attributes now have their value interpreted as a QName and will
    compare as identical if their namespace URI and local
    names match even if they use different prefixes
  1.3:
  * Try to match control Element with first unmatched test one instead of
    creating CHILD_NODE_NOT_FOUND
  1.2:
  * null XPath on missing node
  * SAXParserFactory can be configured
  * new Validator class to validate schema definitions
  1.1:
  * Support for XML Namespaces in XPath processing
  * Support for XML Schema validation using any JAXP compliant parser
- dropped xmlunit-java5-enum.patch, not needed
- dropped xmlunit-no-javac-target.patch, not needed
- put userguide to javadoc package
* Wed Sep 11 2013 mvyskocil@suse.com
- use add_maven_depmap from javapackages-tools
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Thu Dec 15 2011 mvyskocil@suse.cz
- fix the license to BSD-3-Clause (bnc#737022)
* Thu Dec  8 2011 coolo@suse.com
- fix license to be in spdx.org format
* Thu Nov  4 2010 mvyskocil@suse.cz
- Initial SUSE packaging of xmlunit (xmlunit-1.0-6.jpp5.src.rpm)
