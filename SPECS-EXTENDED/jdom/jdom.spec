Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package jdom
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


%define xom_version   1.2b1
%define xom_suffix    %{nil}
%define xom_dir       %{_builddir}/%{name}-%{jdom_version}/XOM
%define xom_included_jaxen_archive jaxen-1.1-src.zip
%define jdom_version      1.1.3
%define jdom_suffix     %{nil}
%define dom4j_version   1.6.1
%define dom4j_suffix    %{nil}
%define dom4j_dir       %{_builddir}/%{name}-%{jdom_version}/dom4j
%define saxpath_version   1.0
%define saxpath_suffix  -FCS
%define saxpath_dir     %{_builddir}/%{name}-%{jdom_version}/saxpath-%{saxpath_version}%{saxpath_suffix}
%define jaxen_version   1.1.1
%define jaxen_suffix    %{nil}
%define jaxen_dir       %{_builddir}/%{name}-%{jdom_version}/jaxen-%{jaxen_version}
%define jdom_dir        %{_builddir}/%{name}-%{jdom_version}/%{name}
%define stage1_build_dir %{_builddir}/build
Name:           jdom
Version:        1.1.3
Release:        34%{?dist}
Summary:        JDOM is a Java Representation of an XML Document
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://www.jdom.org
Source0:        http://jdom.org/dist/binary/archive/%{name}-%{version}.tar.gz
Source1:        saxpath-%{saxpath_version}.tar.bz2
Source2:        xom-%{xom_version}-src.tar.bz2
# svn co svn://svn.debian.org/svn/pkg-java/trunk/dom4j
# rm dom4j/docs/xref/org/dom4j/tree/ConcurrentReaderHashMap.html
# rm dom4j/docs/clover/org/dom4j/tree/ConcurrentReaderHashMap.html
# #bnc501764
# rm dom4j/lib/tools/clover.license
# tar --exclude-vcs -cjf dom4j-1.6.1-debian.tar.bz2 dom4j/
Source3:        dom4j-%{dom4j_version}-debian.tar.bz2
Source4:        jaxen-%{jaxen_version}-src.tar.bz2
Source10:       http://repo.maven.apache.org/maven2/org/%{name}/%{name}/%{jdom_version}%{jdom_suffix}/%{name}-%{jdom_version}%{jdom_suffix}.pom
Source11:       http://repo.maven.apache.org/maven2/saxpath/saxpath/%{saxpath_version}%{saxpath_suffix}/saxpath-%{saxpath_version}%{saxpath_suffix}.pom
Source12:       http://repo.maven.apache.org/maven2/xom/xom/1.2.5/xom-1.2.5.pom
Source13:       http://repo.maven.apache.org/maven2/jaxen/jaxen/%{jaxen_version}%{jaxen_suffix}/jaxen-%{jaxen_version}%{jaxen_suffix}.pom
Patch0:         jdom-1.1-build.xml.patch
Patch1:         jdom-1.1-OSGiManifest.patch
Patch2:         jdom-1.1-xom-get-jaxen.patch
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit
BuildRequires:  relaxngDatatype
BuildRequires:  servletapi5
BuildRequires:  unzip
BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  xpp2
BuildRequires:  xpp3
Requires:       mvn(jaxen:jaxen)
Requires:       mvn(xerces:xercesImpl)
BuildArch:      noarch

%description
JDOM is, quite simply, a Java representation of an XML document. JDOM
provides a way to represent that document for easy and efficient
reading, manipulation, and writing. It has a straightforward API, is
lightweight and fast, and is optimized for the Java programmer. It is
an alternative to DOM and SAX, although it integrates well with both
DOM and SAX.

%package bootstrap
Summary:        A bootstrap version of JDOM.
Requires:       jaxen-bootstrap
Requires:       mvn(xerces:xercesImpl)
BuildArch:      noarch
Conflicts:      %{name}

%description bootstrap
A bootstrap version of JDOM.


%package -n   saxpath
Version:        1.0_FCS
Summary:        SAXPath is an event-based API for XPath parsers
License:        Apache-2.0
Group:          Development/Libraries/Java

%description -n saxpath
SAXPath is an event-based API for XPath parsers, that is, for parsers
which parse XPath  expressions. SAXPath is intended to be for XPath
what SAX is for XML. Note that the SAXPath package only parses XPath
expressions; it does not evaluate them, or even provide an object
structure for representing them once they have been parsed.

%package -n   xom
Version:        1.2b1
Summary:        XOM is a new XML object model
License:        LGPL-2.1-or-later
Group:          Development/Languages/Java
Requires:       mvn(xalan:xalan)
Requires:       mvn(xerces:xercesImpl)
Requires:       mvn(xml-apis:xml-apis)

%description -n xom
XOM is designed to be easy to learn and easy to use. It works very
straight-forwardly, and has a very shallow learning curve. Assuming
you're already familiar with XML, you should be able to get up and
running with XOM very quickly.

XOM is the only XML API that makes no compromises on correctness. XOM
only accepts namespace well-formed XML documents, and only allows you
to create namespace well-formed XML documents. (In fact, it's a little
stricter than that: it actually guarantees that all documents are
round-trippable and have well-defined XML infosets.) XOM manages your
XML so you don't have to. With XOM, you can focus on the unique value
of your application, and trust XOM to get the XML right.

XOM is fairly unique in that it is a dual streaming/tree-based API.
Individual nodes in the tree can be processed while the document is
still being built. The enables XOM programs to operate almost as fast
as the underlying parser can supply data. You don't need to wait for
the document to be completely parsed before you can start working with
it.

XOM is very memory efficient. If you read an entire document into
memory, XOM uses as little memory as possible. More importantly, XOM
allows you to filter documents as they're built so you don't have to
build the parts of the tree you aren't interested in. For instance, you
can skip building text nodes that only represent boundary white space,
if such white space is not significant in your application. You can
even process a document piece by piece and throw away each piece when
you're done with it. XOM has been used to process documents that are
gigabytes in size.

XOM includes built-in support for a number of XML technologies
including Namespaces in XML, XPath, XSLT, XInclude, xml:id, and
Canonical XML. XOM documents can be converted to and from SAX and DOM.

%package -n  jaxen-bootstrap
Version:        1.1.1
Summary:        A bootstrap version of the jaxen project, a Java XPath Engine
License:        Apache-2.0
Group:          Development/Libraries/Java
Requires:       %{name}-bootstrap
Requires:       mvn(xerces:xercesImpl)
Requires:       mvn(xml-apis:xml-apis)
Requires:       mvn(xom:xom)
Conflicts:      jaxen

%description -n jaxen-bootstrap
This is a bootstrap version of Jaxen. Jaxen is a universal object model walker, capable of evaluating XPath
expressions across multiple models. Currently supported are dom4j,
JDOM, and DOM.

%package -n   jaxen
Version:        1.1.1
Summary:        The jaxen project is a Java XPath Engine
License:        Apache-2.0
Group:          Development/Libraries/Java
Requires:       mvn(dom4j:dom4j)
Requires:       mvn(jdom:jdom)
Requires:       mvn(xerces:xercesImpl)
Requires:       mvn(xml-apis:xml-apis)
Requires:       mvn(xom:xom)

%description -n jaxen
Jaxen is a universal object model walker, capable of evaluating XPath
expressions across multiple models. Currently supported are dom4j,
JDOM, and DOM.

%prep
%setup -q -c foo -a 1 -a 2 -a 3 -a 4
rm %{xom_dir}/%{xom_included_jaxen_archive}
mkdir %{stage1_build_dir}
# delete all inlcuded jar files:
find . -name "*.jar" -delete -name "*.class" -delete
%patch0
%patch1
%patch2
cp %{SOURCE10} %{name}-%{jdom_version}.pom
cp %{SOURCE11} saxpath-%{saxpath_version}.pom
cp %{SOURCE12} xom-%{xom_version}.pom
cp %{SOURCE13} jaxen-%{jaxen_version}.pom

%pom_xpath_set pom:project/pom:version "%{xom_version}%{xom_suffix}" xom-%{xom_version}.pom

%build
export JAVA_OPTS="-source 1.6 -target 1.6 -encoding UTF-8 -J-Xss4m"
export JAVAC="javac ${JAVA_OPTS} "
export ANT_OPTS="-Xss4m"
i=0
CLASSPATH="%{stage1_build_dir}:$(build-classpath xerces-j2 xalan-j2 xalan-j2-serializer junit relaxngDatatype servletapi5 xpp2 xpp3)"
SOURCE_DIRS="%{jaxen_dir}/src/java/main/ %{jdom_dir}/src/java/ %{saxpath_dir}/src/java/main/ %{xom_dir}/src/ %{dom4j_dir}/src/java"
SOURCE_PATH=$(echo ${SOURCE_DIRS} | sed 's#\ #:#g')
# Failing files
rm -f \
	XOM/src/nu/xom/tools/XHTMLJavaDoc.java \
	dom4j/src/java/org/dom4j/datatype/SchemaParser.java \
	dom4j/src/java/org/dom4j/datatype/DatatypeAttribute.java \
	dom4j/src/java/org/dom4j/datatype/DatatypeElement.java \
	dom4j/src/java/org/dom4j/datatype/NamedTypeResolver.java \
	dom4j/src/java/org/dom4j/datatype/DatatypeDocumentFactory.java \
	dom4j/src/java/org/dom4j/datatype/DatatypeElementFactory.java \
	dom4j/src/java/org/jaxen/dom4j/DocumentNavigator.java \
	dom4j/src/java/org/jaxen/dom4j/Dom4jXPath.java
${JAVAC} -classpath ${CLASSPATH} -sourcepath ${SOURCE_PATH} -d %{stage1_build_dir} $(find ${SOURCE_DIRS} -name "*.java" | xargs)
unset CLASSPATH SOURCE_DIRS SOURCE_PATH
jar cf %{jdom_dir}/jaxen.jar -C %{stage1_build_dir} .

pushd %{jdom_dir}
ant -Dparser.jar=$(build-classpath xerces-j2) \
    -Dxml-apis.jar=$(build-classpath xml-commons-apis) \
    -Djaxen.lib.dir=%{jdom_dir} \
    -Dcompile.source=1.6 -Dcompile.target=1.6 \
	-Dversion=%jdom_version \
    package
mv build/jdom-%{jdom_version}.jar %{_builddir}/jdom-%{jdom_version}.jar
rm jaxen.jar
popd
pushd %{jaxen_dir}/src/java/main
mkdir build
#mkdir %{_builddir}/jaxen-excluded
#mv org/jaxen/dom4j %{_builddir}/jaxen-excluded
${JAVAC} -classpath %{_builddir}/jdom-%{jdom_version}.jar:%{stage1_build_dir} -d build/ $(find . -name "*.java" | xargs)
jar -cf %{_builddir}/jaxen-%{jaxen_version}.jar -C build .
popd
pushd %{saxpath_dir}
mkdir src/conf
touch src/conf/MANIFEST.MF
CLASSPATH=%{_builddir}/jaxen-%{jaxen_version}.jar:%{_builddir}/jdom-%{jdom_version}.jar:%{stage1_build_dir} ant package
mv build/saxpath.jar %{_builddir}/saxpath-%{saxpath_version}.jar
popd
pushd %{xom_dir}
ant \
-Djaxen.dir=%{stage1_build_dir} \
-Dxml-apis.jar=$(build-classpath xml-commons-apis) \
-Dparser.jar=$(build-classpath xerces-j2) \
-Dxslt.jar=$(build-classpath xalan-j2) \
-Dserializer.jar=$(build-classpath xalan-j2-serializer) \
-Djunit.jar=$(build-classpath junit) \
-Dresolver.jar=$(build-classpath xml-commons-resolver) \
-Ddom4j.jar=%{stage1_build_dir} \
-Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 \
compile compile15 jar
mv build/xom-%{xom_version}.jar %{_builddir}
popd
#<<< build

%install
mkdir -p %{buildroot}/%{_javadir}
mv %{_builddir}/*.jar %{buildroot}/%{_javadir}
ln -sf %{_javadir}/jdom-%{jdom_version}.jar %{buildroot}/%{_javadir}/jdom.jar
ln -sf %{_javadir}/jaxen-%{jaxen_version}.jar %{buildroot}/%{_javadir}/jaxen.jar
ln -sf %{_javadir}/saxpath-%{saxpath_version}.jar %{buildroot}/%{_javadir}/saxpath.jar
ln -sf %{_javadir}/xom-%{xom_version}.jar %{buildroot}/%{_javadir}/xom.jar

mkdir -p %{buildroot}/%{_mavenpomdir}
cp *.pom %{buildroot}/%{_mavenpomdir}/
%add_maven_depmap jdom-%{jdom_version}.pom jdom-%{jdom_version}.jar -a jdom:jdom
%add_maven_depmap xom-%{xom_version}.pom xom-%{xom_version}.jar -f xom
%add_maven_depmap saxpath-%{saxpath_version}.pom saxpath-%{saxpath_version}.jar -f saxpath
%add_maven_depmap jaxen-%{jaxen_version}.pom jaxen-%{jaxen_version}.jar -f jaxen

%files -f .mfiles
%license LICENSE.txt
%{_javadir}/jdom.jar

%files bootstrap -f .mfiles
%license LICENSE.txt
%{_javadir}/jdom.jar

%files -n xom -f .mfiles-xom
%license LICENSE.txt
%{_javadir}/xom.jar

%files -n saxpath -f .mfiles-saxpath
%license LICENSE.txt
%{_javadir}/saxpath.jar

%files -n jaxen-bootstrap -f .mfiles-jaxen
%license LICENSE.txt
%{_javadir}/jaxen.jar

%files -n jaxen -f .mfiles-jaxen
%license LICENSE.txt
%{_javadir}/jaxen.jar

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.3-34
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.1.3-33.4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Add a dedicated jaxen-bootstrap package for dom4j to build with.
- Add a dedicasted jdom-bootstrap package for dom4j to build with.

* Tue Nov 12 2019 Fridrich Strba <fstrba@suse.com>
- Add correct requires for the packages so that they pull all
  required artifacts
- Clean up the packaging a bit
* Tue Mar 26 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade the jdom component to 1.1.3
- Modified patch:
  * jdom-1.1-build.xml.patch
    + Remove unneeded hunk
- Added patch:
  * jdom-1.1-OSGiManifest.patch
    + Make jdom an OSGi bundle
* Tue Nov 20 2018 Fridrich Strba <fstrba@suse.com>
- Removed patch:
  * include-glibj.jar.patch
    + The build works since ages without glibj being present, so
    removing any trace of it
* Tue Nov 20 2018 Fridrich Strba <fstrba@suse.com>
- Add maven pom files for the distributed jars
- Speed-up build by filtering out the failing files beforehand
  and then building all with one javac invocation
* Fri Sep 29 2017 fstrba@suse.com
- Fix build with jdk9: specify java source and target level 1.6
- Modified patch:
  * jdom-1.1-build.xml.patch
    + specify java source and target level 1.6
- Add more BuildRequires, in order to build more java files in
  stage 1
* Thu Sep 14 2017 fstrba@suse.com
- Build with javac whose syntax is compatible with OpenJDK
* Fri May 19 2017 tchvatal@suse.com
- Expand the buildignore lines for newer jdk
* Tue Mar 31 2015 tchvatal@suse.com
- Provide and obsolete jaxen-bootstrap to avoid file conflict
* Tue Mar 24 2015 tchvatal@suse.com
- Fix namespace clash with javapackages-tools on variables
* Tue Mar 24 2015 tchvatal@suse.com
- Cleanup with spec-cleaner and add debug output
* Fri Jun 15 2012 mvyskocil@suse.cz
- ignore jdk7 as well
* Mon Jun  4 2012 coolo@suse.com
- remove stray character from xom summary to fix UTF-8 parsing
* Thu Mar 17 2011 mvyskocil@suse.cz
- move to gcj back - the java.lang.StackOverflow is nothing nice
* Fri Mar 11 2011 mvyskocil@suse.cz
- build using openjdk, split BR one per-line
* Fri Mar 11 2011 mvyskocil@suse.cz
- build using openjdk, write one BuildRequire per line,
  no authors in description
* Wed May 20 2009 mvyskocil@suse.cz
- 'fixed bnc#501764: removed clover.license from source tarball'
* Mon May 18 2009 mvyskocil@suse.cz
- Removed documentation of ConcurrentReaderHashMap (bnc#504663)
  * dom4j-1.6.1/docs/clover/org/dom4j/tree/ConcurrentReaderHashMap.html
  * dom4j-1.6.1/docs/xref/org/dom4j/tree/ConcurrentReaderHashMap.html
* Thu May 14 2009 mvyskocil@suse.cz
- fixed version tag for jaxen and xom
* Tue Jan 20 2009 mvyskocil@suse.cz
- update jdom to 1.1 fixed bnc#467366
- updated jaxen to 1.1.1 (do not use an included jaxen)
- cleaned build requires
- Obsoleted java150 patch
* Fri Nov 21 2008 ro@suse.de
- update check-build.sh
* Wed Jan 23 2008 mvyskocil@suse.cz
- fixed beta build
* Thu Mar 29 2007 dbornkessel@suse.de
- added unzip to build requires
* Mon Jan 15 2007 dbornkessel@suse.de
- removed xml-commons-apis build req. (Bug #232127)
* Thu Sep 28 2006 dbornkessel@suse.de
- first versions
- fixes necessary to compile with Java 1.5.0
  - set source="1.4" and target="1.4" for ant "javac" tasks
  - set source="1.4" for ant "javadoc" tasks
