Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package xalan-j2
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


%define cvs_version 2_7_2
Name:           xalan-j2
Version:        2.7.2
Release:        10%{?dist}
Summary:        Java XSLT processor
License:        Apache-2.0
Group:          Development/Libraries/Java
Url:            https://xalan.apache.org/index.html
Source0:        https://www.apache.org/dist/xalan/xalan-j/source/xalan-j_%{cvs_version}-src.tar.gz
Source1:        https://repo1.maven.org/maven2/xalan/xalan/%{version}/xalan-%{version}.pom
Source2:        https://repo1.maven.org/maven2/xalan/serializer/%{version}/serializer-%{version}.pom
Source3:        xsltc-%{version}.pom
Source4:        xalan-j2-serializer-MANIFEST.MF
Source5:        xalan-j2-MANIFEST.MF
Source6:        optional-xerces-req.patch
# OSGi manifests
Patch0:         %{name}-noxsltcdeps.patch
Patch1:         %{name}-manifest.patch
Patch2:         %{name}-crosslink.patch
Patch3:         openjdk-build.patch
BuildRequires:  ant
BuildRequires:  bcel
BuildRequires:  dos2unix
BuildRequires:  fdupes
BuildRequires:  java-cup-bootstrap
BuildRequires:  java-devel >= 1.6
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jlex
BuildRequires:  servletapi5
BuildRequires:  xml-commons-apis-bootstrap
Requires:       jaxp_parser_impl
Requires(post): update-alternatives
Requires(postun): update-alternatives
Provides:       jaxp_transform_impl
Conflicts:      %{name}-bootstrap
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
#!BuildIgnore:  xerces-j2 xml-commons xml-commons-resolver xml-commons-apis java-cup
#!BuildIgnore:  xml-commons-jaxp-1.3-apis

%description
Xalan is an XSLT processor for transforming XML documents into HTML,
text, or other XML document types. It implements the W3C
Recommendations for XSL Transformations (XSLT) and the XML Path
Language (XPath). It can be used from the command line, in an applet or
a servlet, or as a module in other program.

%package        bootstrap
Summary:        Bootstrap Java XSLT processor
Group:          Development/Libraries/Java
Conflicts:      %{name}
BuildRequires:  ant
BuildRequires:  bcel
BuildRequires:  dos2unix
BuildRequires:  fdupes
BuildRequires:  java-cup-bootstrap
BuildRequires:  java-devel >= 1.6
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jlex
BuildRequires:  servletapi5
BuildRequires:  xml-commons-apis-bootstrap
Requires(post): update-alternatives
Requires(postun): update-alternatives

%description bootstrap
This is a bootstrap version of Xalan.
Xalan is an XSLT processor for transforming XML documents into HTML,
text, or other XML document types. It implements the W3C
Recommendations for XSL Transformations (XSLT) and the XML Path
Language (XPath). It can be used from the command line, in an applet or
a servlet, or as a module in other program.


%package        xsltc
Summary:        Java XSLT compiler
Group:          Development/Libraries/Java
Requires:       bcel
Requires:       java_cup
Requires:       jaxp_parser_impl
Requires:       jlex
Requires:       regexp

%description    xsltc
The XSLT Compiler is a Java-based tool for compiling XSLT stylesheets
into lightweight and portable Java byte codes called translets.

%package        manual
Summary:        Manual for xalan-j2
Group:          Development/Libraries/Java

%description    manual
Xalan is an XSLT processor for transforming XML documents into HTML,
text, or other XML document types. It implements the W3C
Recommendations for XSL Transformations (XSLT) and the XML Path
Language (XPath). It can be used from the command line, in an applet or
a servlet, or as a module in other program.

This package contains the manual for Xalan.

%package        demo
Summary:        Demonstration and samples for xalan-j2
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}-%{release}
Requires:       servlet

%description    demo
Xalan is an XSLT processor for transforming XML documents into HTML,
text, or other XML document types. It implements the W3C
Recommendations for XSL Transformations (XSLT) and the XML Path
Language (XPath). It can be used from the command line, in an applet or
a servlet, or as a module in other program.

This package contains demonstration and sample files for Xalan.

%prep
%setup -q -n xalan-j_%{cvs_version}
patch -u %{SOURCE5} -i %{SOURCE6}

%patch 0 -p1
%patch 1 -p1
%patch 2 -p1
%patch 3 -p1
# Remove all binary libs, except ones needed to build docs and N/A elsewhere.
for j in $(find . -name "*.jar"); do
        mv $j $j.no
done
mv tools/xalan2jdoc.jar.no tools/xalan2jdoc.jar
mv tools/xalan2jtaglet.jar.no tools/xalan2jtaglet.jar
dos2unix KEYS LICENSE.txt NOTICE.txt xdocs/sources/xsltc/README.xsltc xdocs/sources/xsltc/README.xslt

%build
if [ ! -e "$JAVA_HOME" ] ; then export JAVA_HOME="%{java_home}" ; fi
pushd lib
ln -sf $(build-classpath java_cup-runtime) runtime.jar
ln -sf $(build-classpath bcel) BCEL.jar
ln -sf $(build-classpath regexp) regexp.jar
ln -sf $(build-classpath xerces-j2) xercesImpl.jar
ln -sf $(build-classpath xml-commons-apis) xml-apis.jar
popd
pushd tools
ln -sf $(build-classpath java_cup) java_cup.jar
ln -sf $(build-classpath ant) ant.jar
ln -sf $(build-classpath jlex) JLex.jar
ln -sf $(build-classpath stylebook) stylebook-1.0-b3_xalan-2.jar
popd
ant \
  -Dservlet-api.jar=$(build-classpath servletapi5) \
  -Dcompiler.source=1.6 -Dcompiler.target=1.6 \
  -Djava.awt.headless=true \
  -Dapi.j2se=%{_javadocdir}/java \
  -Dbuild.xalan-interpretive.jar=build/xalan-interpretive.jar \
  xalan-interpretive.jar\
  xsltc.unbundledjar \
  docs \
  xsltc.docs \
  samples \
  servlet

# inject OSGi manifests
jar ufm build/serializer.jar %{SOURCE4}
jar ufm build/xalan-interpretive.jar %{SOURCE5}

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 build/xalan-interpretive.jar \
  %{buildroot}%{_javadir}/%{name}-%{version}.jar
install -p -m 644 build/xsltc.jar \
  %{buildroot}%{_javadir}/xsltc-%{version}.jar
install -p -m 644 build/serializer.jar \
  %{buildroot}%{_javadir}/%{name}-serializer-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/%{name}-%{version}.pom
%add_maven_depmap %{name}-%{version}.pom %{name}-%{version}.jar
install -p -m 644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/%{name}-serializer-%{version}.pom
%add_maven_depmap %{name}-serializer-%{version}.pom %{name}-serializer-%{version}.jar
install -p -m 644 %{SOURCE3}  %{buildroot}%{_mavenpomdir}/xsltc-%{version}.pom
%add_maven_depmap xsltc-%{version}.pom xsltc-%{version}.jar -f xsltc

# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -p -m 644 build/xalansamples.jar \
  %{buildroot}%{_datadir}/%{name}/%{name}-samples.jar
install -p -m 644 build/xalanservlet.war \
  %{buildroot}%{_datadir}/%{name}/%{name}-servlet.war
cp -pr samples %{buildroot}%{_datadir}/%{name}
%fdupes -s %{buildroot}%{_datadir}/%{name}

# alternatives
mkdir -p %{buildroot}%{_sysconfdir}/alternatives
ln -sf %{_sysconfdir}/alternatives/jaxp_transform_impl.jar %{buildroot}%{_javadir}/jaxp_transform_impl.jar

# bnc#485299
install -d -m 0755 %{buildroot}/%{_sysconfdir}/ant.d/
echo xalan-j2-serializer > %{buildroot}/%{_sysconfdir}/ant.d/serializer

%post
update-alternatives --install %{_javadir}/jaxp_transform_impl.jar \
  jaxp_transform_impl %{_javadir}/%{name}.jar 30

%preun
{
  [ $1 = 0 ] || exit 0
  update-alternatives --remove jaxp_transform_impl %{_javadir}/%{name}.jar
} >/dev/null 2>&1 || :

%files
%defattr(0644,root,root,0755)
%doc KEYS LICENSE.txt NOTICE.txt
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-serializer-%{version}.jar
%{_javadir}/%{name}-serializer.jar
%config %{_sysconfdir}/ant.d/serializer
%ghost %{_sysconfdir}/alternatives/jaxp_transform_impl.jar
%{_javadir}/jaxp_transform_impl.jar
%{_mavenpomdir}/%{name}*
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif

%files bootstrap
%defattr(0644,root,root,0755)
%doc KEYS LICENSE.txt NOTICE.txt
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-serializer-%{version}.jar
%{_javadir}/%{name}-serializer.jar
%config %{_sysconfdir}/ant.d/serializer
%ghost %{_sysconfdir}/alternatives/jaxp_transform_impl.jar
%{_javadir}/jaxp_transform_impl.jar
%{_mavenpomdir}/%{name}*
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif

%files xsltc
%defattr(0644,root,root,0755)
%{_javadir}/xsltc-%{version}.jar
%{_javadir}/xsltc.jar
%{_mavenpomdir}/xsltc*
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}-xsltc
%else
%{_datadir}/maven-metadata/%{name}-xsltc.xml*
%endif

%files manual
%defattr(0644,root,root,0755)
%doc build/docs/*

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.2-10
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 2.7.2-9.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Add a bootstrap package for xerces-j2 to build with.
- Use javapackages-local-bootstrap to avoid build cycle.
- Apply patch to set osgi xerces requirement optional.

* Fri Feb  1 2019 Fridrich Strba <fstrba@suse.com>
- Add xalan-j2-serializer-MANIFEST.MF and xalan-j2-MANIFEST.MF
  * Contain OSGi metadata required by Eclipse
* Sun Nov 18 2018 Fridrich Strba <fstrba@suse.com>
- Add maven pom file for xsltc
* Wed Nov  7 2018 Fridrich Strba <fstrba@suse.com>
- Add maven pom files for xalan-j2 and the serializer
* Tue Oct  3 2017 fstrba@suse.com
- Added patch:
  * openjdk-build.patch
    + Fix build with different versions of OpenJDK
- Do not require gcc-java any more
- Run fdupes
* Mon Dec  8 2014 tchvatal@suse.com
- Revert last commit, causes cycles.
* Fri Dec  5 2014 p.drouand@gmail.com
- Replace java-1_5_0-gcj-compat-devel with javapackages-tools
* Mon Jul 21 2014 tchvatal@suse.com
- Update-alternatives love.
* Mon Jun 23 2014 tchvatal@suse.com
- Cleanup with spec-cleaner.
* Mon Jun 23 2014 tchvatal@suse.com
- Version bump to 2.7.2 release:
  * various small fixes
  * Fix security bnc#870082 CVE-2014-0107
- Fix few rpmlint warnings
- Deleted xalan-j2-java14compat.patch patch as we don't bother
  with 1.4 java anymore
- Rebased patches on new code:
  * xalan-j2-crosslink.patch
  * xalan-j2-manifest.patch
  * xalan-j2-noxsltcdeps.patch
* Wed Aug 28 2013 mvyskocil@suse.com
- mark all files related to update-alternatives as ghost
- reformat header of spec a bit
* Fri Aug 23 2013 mvyskocil@suse.com
- drop javadoc package
* Mon Jan  7 2013 mvyskocil@suse.com
- remove xerces-j2-bootstrap depenency (bnc#789163)
* Mon Nov  8 2010 mvyskocil@suse.cz
- ignore xml-commons-jaxp-1.3-apis
* Mon May  4 2009 mvyskocil@suse.cz
- build with java-cup-bootstrap instead obsolete java_cup
* Wed Mar 18 2009 mvyskocil@suse.cz
- bnc#485299: Ant <xslt> tasks fail with NoClassDefFoundError:
  org/apache/xml/serializer/SerializerTrace
* Mon Jul 28 2008 ro@suse.de
- use xml-commons-apis-bootstrap instead of xml-commons-apis
* Mon Jul 28 2008 coolo@suse.de
- buildignore xml-commons (ant works without it)
* Mon Jul 21 2008 coolo@suse.de
- build against gcj to avoid bootstrap problems
* Thu Sep 21 2006 skh@suse.de
- update to version 2.7.0 from jpackage.org
- don't use icecream
- use target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Jul 29 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Wed Jul 20 2005 jsmeix@suse.de
- Current version 2.6.0 from JPackage.org
* Mon Jul 18 2005 jsmeix@suse.de
- Current version 2.6.0 from JPackage.org
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 2.6.0 (JPackage 1.5)
