Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package xerces-j2
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


%global cvs_version 2_12_0
%define __requires_exclude system.bundle
Name:           xerces-j2
Version:        2.12.0
Release:        5%{?dist}
Summary:        Java XML parser
License:        ASL 2.0 and Public Domain and W3C
Group:          Development/Libraries/Java
URL:            https://xerces.apache.org/xerces2-j/
Source0:        https://archive.apache.org/dist/xerces/j/source/Xerces-J-src.%{version}.tar.gz
Source1:        %{name}-version.sh
Source2:        %{name}-constants.sh
Source3:        %{name}-version.1
Source4:        %{name}-constants.1
Source5:        https://repo.maven.apache.org/maven2/xerces/xercesImpl/%{version}/xercesImpl-%{version}.pom
# Patch the build so that it doesn't try to use bundled xml-commons source
# Also remove the use of the special taglets and xjavac task
Patch0:         %{name}-build.patch
Patch1:         xerces-2_11_0-jdk7.patch
Patch2:         %{name}-manifest.patch
Patch3:         ant-build-fix.patch
BuildRequires:  ant
BuildRequires:  dos2unix
BuildRequires:  fdupes
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  xalan-j2-bootstrap >= 2.7.1
BuildRequires:  xml-commons-apis >= 1.4.01
BuildRequires:  xml-commons-resolver >= 1.2
#!BuildIgnore:  xerces-j2 osgi(org.apache.xerces) jaxp_parser_impl
# Explicit javapackages-tools requires since scripts use
# /usr/share/java-utils/java-functions
Requires:       javapackages-tools
Requires:       xalan-j2 >= 2.7.1
Requires:       xml-commons-apis >= 1.4.01
Requires:       xml-commons-resolver >= 1.2
Provides:       %{name}-scripts = %{version}-%{release}
Provides:       jaxp_parser_impl = 1.4
Obsoletes:      %{name}-scripts < %{version}-%{release}
BuildArch:      noarch

%description
Xerces2 is an XML parser in the Apache Xerces family. This version is the
reference implementation of the Xerces Native Interface (XNI), a modular
framework for building parser components and configurations.

Xerces2 implements the Document Object Model Level 3 Core and Load/Save W3C
Recommendations, the XML Inclusions (XInclude) W3C Recommendation, and supports
OASIS XML Catalogs v1.1. It can parse documents conforming to the XML 1.1
Recommendation, except that it does not yet provide an option to enable
normalization checking as described in section 2.13 of this specification. It
handles name spaces according to the XML Namespaces 1.1 Recommendation, and
serializes XML 1.1 documents if the DOM level 3 load/save APIs are in use.

%package        javadoc
Summary:        Javadocs for %{name}
Group:          Documentation/HTML

%description    javadoc
This package contains the API documentation for %{name}.

%package        demo
Summary:        Demonstrations and samples for %{name}
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}-%{release}

%description    demo
%{summary}.

%prep
%setup -q -n xerces-%{cvs_version}
find "(" -name "*.class" -o -name "*.jar" ")" -delete
find -type f -exec dos2unix {} \;
%patch 0 -p1
%patch 1 -p1
%patch 2
%patch 3 -p1

%build
mkdir -p tools
pushd tools
ln -sf $(build-classpath xalan-j2-serializer) serializer.jar
ln -sf $(build-classpath xml-commons-apis) xml-apis.jar
ln -sf $(build-classpath xml-commons-resolver) resolver.jar
popd

# Build everything
export ANT_OPTS="-Xmx256m -Djava.awt.headless=true -Dbuild.sysclasspath=first -Ddisconnected=true"
ant -Djavac.source=1.6 -Djavac.target=1.6 \
    -Dbuild.compiler=modern \
    clean jars javadocs

%install
# jar
install -dm 755 %{buildroot}%{_javadir}
install -pm 644 build/xercesImpl.jar %{buildroot}%{_javadir}/%{name}.jar
(cd %{buildroot}%{_javadir} && ln -s %{name}.jar jaxp_parser_impl.jar)

# pom
install -dm 755 %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE5} %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a xerces:xerces,xerces:xmlParserAPIs,apache:xerces-j2

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
mkdir -p %{buildroot}%{_javadocdir}/%{name}/impl
mkdir -p %{buildroot}%{_javadocdir}/%{name}/xs
mkdir -p %{buildroot}%{_javadocdir}/%{name}/xni
mkdir -p %{buildroot}%{_javadocdir}/%{name}/other

cp -pr build/docs/javadocs/xerces2/* %{buildroot}%{_javadocdir}/%{name}/impl
cp -pr build/docs/javadocs/api/* %{buildroot}%{_javadocdir}/%{name}/xs
cp -pr build/docs/javadocs/xni/* %{buildroot}%{_javadocdir}/%{name}/xni
cp -pr build/docs/javadocs/other/* %{buildroot}%{_javadocdir}/%{name}/other

%fdupes -s %{buildroot}%{_javadocdir}

# scripts
install -pD -m755 -T %{SOURCE1} %{buildroot}%{_bindir}/%{name}-version
install -pD -m755 -T %{SOURCE2} %{buildroot}%{_bindir}/%{name}-constants

# manual pages
install -d -m 755 %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE4} %{buildroot}%{_mandir}/man1

# demo
install -pD -T build/xercesSamples.jar %{buildroot}%{_datadir}/%{name}/%{name}-samples.jar
cp -pr data %{buildroot}%{_datadir}/%{name}

%post
update-alternatives --remove jaxp_parser_impl %{_javadir}/%{name}.jar >/dev/null 2>&1 || :
# it deletes the link, set it up again
ln -sf %{name}.jar %{_javadir}/jaxp_parser_impl.jar

%files
%license LICENSE LICENSE.DOM-documentation.html LICENSE.DOM-software.html LICENSE.resolver.txt LICENSE-SAX.html LICENSE.DOM-documentation.html LICENSE.serializer.txt
%doc NOTICE README
%{_bindir}/*
%{_javadir}/*
%{_mandir}/*/*
%{_mavenpomdir}/*
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif

%files javadoc
%{_javadocdir}/%{name}

%files demo
%{_datadir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.12.0-5
- Converting the 'Release' tag to the '[number].[distribution]' format.
- License verified.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 2.12.0-4.9
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Build with a bootstrap version of xalan-j2.
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Apr 17 2019 Fridrich Strba <fstrba@suse.com>
- Remove bogus dependency
* Tue Apr  9 2019 Fridrich Strba <fstrba@suse.com>
- BuildIgnore another provider of this package to avoid unresolved
  cycle
* Tue Feb  5 2019 Fridrich Strba <fstrba@suse.com>
- BuildIgnore oneself to avoid unresolved cycle
* Fri Feb  1 2019 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * xerces-j2-manifest.patch
  - add OSGi metadata required by Eclipse
* Tue Dec 11 2018 Jan Engelhardt <jengelh@inai.de>
- Remove rhetorics from description, and then compact its verbose
  grammar.
- Do away with xargs when find has some better options.
* Thu Dec  6 2018 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 2.12.0
  * This release expands on Xerces-J's experimental support for
    XML Schema 1.1 by providing a fully compliant XML Schema 1.1
    implementation. It fixes several bugs which were present in
    Xerces-J 2.11.0 and also includes a few other enhancements and
    performance improvements.
    + add: Report all id/idref problems when validating XML against
    DTD or XML Schema.
    + add: Implemented improvements to XML Schema 1.1 CTA
    implementation and inheritable attributes.
    + update: Implemented improved error/warning message reporting
    for various XML Schema use cases.
    + update: Implemented few performance enhancements (affecting
    parsing/validation latency and memory footprint) to the
    implementation.
    + fix: Fixed minor bugs in Xerces-J's regex support in XML
    Schema <pattern> facet.
    + fix: Implemented various fixes to XML Schema 1.1
    assert/assertion implementation.
    + fix: Fixed possible security issue: an implementation of the
    NamedNodeMapImpl class in the JAXP component did not limit the
    amount of memory allocated when creating object instance from
    a serialized form. A specially-crafted input could cause a
    java application to use an excessive amount of memory when
    deserialized.
    + fix: Implemented minor and major fixes in certain areas, to
    XML Schema 1.0 and 1.1 implementations.
    + fix: Fixed the issue related to, XIncludeTextReader doesn't
    handle null Content Types properly.
    + fix: Fixed minor problems in the DOM (Level 3 Core)
    implementation.
    + fix: Fixed few errors related to Xerces-J's build component.
    + fix: Solved a minor bug in SoftReferenceSymbolTable
    implementation component.
    + fix: Fixed various bugs and made various improvements.
- Removed patches:
  * arrays-doubling.patch
  * scan-pseudo-attribute.patch
    + integrated upstream
- Added patches:
  * xerces-j2-build.patch
    + Don't use the bundled xml-apis, but depend on an existing
    package
    + Don't use custom taglets and ant tasks
- Do not bundle the xml-apis and xml-resolver and stop using
  alternatives
- Install as a maven artifact
* Tue Oct  3 2017 fstrba@suse.com
- Added patch:
  * xerces-2_11_0-jdk7.patch
    + Dummy implementation of the getContentDocument() in common
    DOM API, in order to be able to build with jdk >= 1.6
- Specify java source and target level 1.6 and don't depend on gcj
* Fri May 19 2017 tchvatal@suse.com
- BuildIgnore more main java versions to stick to gcj
* Thu Feb 11 2016 tchvatal@suse.com
- Add patches for bnc#814241 upstream#1616
  * arrays-doubling.patch
  * scan-pseudo-attribute.patch
* Mon Jul 21 2014 tchvatal@suse.com
- Fixup man page permissions
* Mon Jul 21 2014 tchvatal@suse.com
- Sort out update-alternatives
* Fri Jun  6 2014 tchvatal@suse.com
- Version bump to 2.11.0:
  * This release expands on Xerces' experimental support for XML
    Schema 1.1 by providing implementations for the simplified
    complex type restriction rules (also known as subsumption),
    xs:override and a few other XML Schema 1.1 features. This
    release also introduces experimental support for XML Schema
    Component Designators (SCD). It fixes several bugs which were
    present in Xerces-J 2.10.0 and also includes a few other minor
    enhancements.
  * As of this release, Xerces and Xalan now share a common
    serialization codebase. The DOM Level 3 serialization support
    which was in Xerces was migrated into the Xalan serializer and
    Xerces' native serializer was deprecated. In this release we
    also upgraded the xml-commons resolver to v1.2 (which provides
    support for OASIS XML Catalogs v1.1), introduced a few minor
    features and fixed several bugs.
- Obsoleted patches no longer needed:
  * xerces-j2-parsing.patch
  * xerces-j2-2.8.1_new_unsupported_dom_methods.patch
  * xerces-build.patch
  * xerces-j2-gcj-switch-constants-bug.patch
  * java150_build.patch
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Fri Aug 23 2013 mvyskocil@suse.com
- drop javadoc packages
- drop antlr-bootstrap from BR as javadoc is not built
* Fri Jan 11 2013 mvyskocil@suse.com
- removed the -boostrap package
* Fri Sep 16 2011 andrea.turrini@gmail.com
- fixed typos in xerces-j2.spec
* Mon Mar 14 2011 mvyskocil@suse.cz
- build ignore openjdk
* Tue Sep 21 2010 mvyskocil@suse.cz
- use antlr-bootstrap for javadoc build
* Mon Sep 13 2010 mvyskocil@suse.cz
- remove unecessary xerces-j2-build.patch
* Thu Sep  2 2010 mvyskocil@suse.cz
- ignore antlr(-java) to reduce build cycles
* Mon Aug 17 2009 mvyskocil@suse.cz
- fixed bnc#530717: VUL-0: xerces-j2: XML parsing vulnerability
- Removed non used patch xerces-build.patch
- Fixed some rpmlint warnings and errors
- Removed javadoc postinstall scripts
- Removed %%%%release from subpackages requires
* Wed Nov 12 2008 mvyskocil@suse.cz
- use gcj for build as this version is not compatible with INM Java6
- added a jpackage-utils to BuildRequires
* Fri Feb 29 2008 coolo@suse.de
- adding prereq for xml-apis and xml-resolver
* Wed Jan 23 2008 prusnak@suse.cz
- removed comma between symbols in PreReq
* Wed May  2 2007 dbornkessel@suse.de
- added unzip to BuildRequires
* Tue Jan 23 2007 dbornkessel@suse.de
- added dummy methods for not yet supported new dom methods
* Tue Jan 16 2007 dbornkessel@suse.de
- created sub-packages xml-apis and xml-resolver to avoid Bug #232127
* Wed Nov 15 2006 dbornkessel@suse.de
- Changed
    PreReq: /usr/sbin/update-alternatives
  to
    PreReq: update-alternatives
* Fri Sep 22 2006 dbornkessel@suse.de
- update to 2.8.1
- added source="1.4" target="1.4" to [x]javac & javadoc ant tasks
* Mon Jan 30 2006 dbornkessel@suse.de
- changed update alternatives prios
- corrected update-alternatives name for 'xml-commons-resolver'
* Fri Jan 27 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Jan 24 2006 dbornkessel@suse.de
- added missing jar file (xml-apis & resolver)
- added xml-apis and resolver to alternative system, so they can be
  interchanged with xml-commons-apis and commons-resolver
* Wed Jan 18 2006 dbornkessel@suse.de
- Update to version 2.7.1
* Wed Sep 28 2005 dmueller@suse.de
- add norootforbuild
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 2.6.2 (JPackage 1.5)
