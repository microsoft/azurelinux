Summary:        Bean Scripting Framework
Name:           bsf
Version:        2.4.0
Release:        20%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/bsf/
Source0:        https://downloads.apache.org/commons/%{name}/source/%{name}-src-%{version}.tar.gz
Source1:        bsf-pom.xml
Patch0:         build-file.patch
Patch1:         build.properties.patch
Patch2:         bsf-doclint-ignore.patch
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  apache-commons-logging
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  rhino
BuildRequires:  xalan-j2
BuildArch:      noarch

%description
Bean Scripting Framework (BSF) is a set of Java classes that provides
scripting language support within Java applications and access to Java
objects and methods from scripting languages. BSF allows writing JSPs
in languages other than Java while providing access to the Java class
library. In addition, BSF permits any Java application to be
implemented in part (or dynamically extended) by a language that is
embedded within it. This is achieved by providing an API that permits
calling scripting language engines from within Java as well as an
object registry that exposes Java objects to these scripting language
engines.

This BSF package currently supports several scripting languages: *
   Javascript (using Rhino ECMAScript, from the Mozilla project)
* XSLT Stylesheets (as a component of Apache XML project's Xalan and
   Xerces)

In addition, the following languages are supported with their own
   BSF engines: * Java (using BeanShell, from the BeanShell project)
* JRuby
* JudoScript

%package javadoc
Summary:        Javadoc for bsf
Group:          Development/Libraries/Java

%description javadoc
Bean Scripting Framework (BSF) is a set of Java classes which provides
scripting language support within Java applications, and access to Java
objects and methods from scripting languages. BSF allows one to write
JSPs in languages other than Java while providing access to the Java
class library. In addition, BSF permits any Java application to be
implemented in part (or dynamically extended) by a language that is
embedded within it. This is achieved by providing an API that permits
calling scripting language engines from within Java, as well as an
object registry that exposes Java objects to these scripting language
engines.

This package contains the javadoc documentation for the Bean Scripting
Framework.

%prep
%autosetup -p1
find -name \*.jar -delete

%build
mkdir -p lib
build-jar-repository -s -p lib apache-commons-logging rhino xalan-j2
%{ant} -Dant.build.javac.source=8 -Dant.build.javac.target=8 jar javadocs

%install
# jar
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 build/lib/%{name}.jar \
            %{buildroot}%{_javadir}/%{name}.jar

# pom and depmap frag
install -DTm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "org.apache.bsf:%{name}"

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr build/javadocs/* %{buildroot}%{_javadocdir}/%{name}
mv %{buildroot}%{_javadocdir}/%{name}/legal/ADDITIONAL_LICENSE_INFO .
mv %{buildroot}%{_javadocdir}/%{name}/legal/LICENSE .
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc AUTHORS.txt CHANGES.txt README.txt TODO.txt RELEASE-NOTE.txt

%files javadoc
%license LICENSE LICENSE.txt NOTICE.txt ADDITIONAL_LICENSE_INFO
%{_javadocdir}/%{name}

%changelog
* Fri Jan 02 2026 Sumit Jena <v-sumitjena@microsoft.com> - 2.4.0-20
- Fixed License Warnings.
- Added additional License file.

* Tue Jan 03 2023 Sumedh Sharma <sumsharma@microsoft.com> - 2.4.0-19
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.0-18
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.4.0-17.4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Set javadoc Xdoclint:none with bsf-doclint-ignore.patch.

* Wed Jan  8 2020 Fridrich Strba <fstrba@suse.com>
- BuildIgnore jline1 instead of jline, since the dependency of
  rhino changed

* Tue Apr  9 2019 Fridrich Strba <fstrba@suse.com>
- Remove reference to parent pom, since we do not use Maven to
  build this package

* Tue Feb 12 2019 Fridrich Strba <fstrba@suse.com>
- BuildIgnore jline to avoid a build cycle

* Tue Feb  5 2019 Fridrich Strba <fstrba@suse.com>
- Clean the spec file and sanitize dependencies

* Tue Nov 27 2018 Fridrich Strba <fstrba@suse.com>
- Modified patch:
  * build-file.patch
    + Fix build of script providers

* Wed May 16 2018 fstrba@suse.com
- Build with source and target 8 to anticipate a possible removal
  of 1.6 compatibility
- Modified patch:
  * build.properties.patch
    + specify source level 8

* Fri Dec 22 2017 fstrba@suse.com
- Assure that we build with java source and target level 1.6

* Wed Sep 20 2017 fstrba@suse.com
- Fix javadoc errors with jdk9: use build-jar-repository instead
  of system-wide CLASSPATH environmental variable
- Clean spec file and run fdupes on documentation

* Thu Sep  7 2017 fstrba@suse.com
- Force java source and target levels to 1.6 in order to allow
  building with jdk9
- Force using of java-1_8_0-openjdk-devel, since javadoc errors are
  fatal in jdk9

* Sat May 20 2017 tchvatal@suse.com
- Remove jython from dependencies, not needed

* Fri May 19 2017 pcervinka@suse.com
- New build dependency: javapackages-local
- Spec file cleaned

* Wed Mar 25 2015 tchvatal@suse.com
- Remove gpg-offline dep and cleanup with spec-cleaner

* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools

* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools

* Wed Aug 28 2013 mvyskocil@suse.com
- update to 2.4.0
  * can be used as an extension package to Java by placing it into
    "jre/lib/ext" [using the thread's context classloader, ie. the result
    of 'Thread.currentThread().getContextClassLoader()']
  * rely on commons-logging or log4j
  * removed jpython engine, supperseeded by jython
  * and more, see CHANGES.txt
- add gpg verification
- drop bsf-disable-rhino.patch
- add build-file.patch and build.properties.patch
- use add_maven_depmap from javapackages-tools

* Tue Feb 28 2012 mvyskocil@suse.cz
- ignore mysql-connector-java from build to break a build cycle

* Sat Sep 17 2011 jengelh@medozas.de
- Remove redundant tags/sections from specfile

* Mon Aug 31 2009 coolo@novell.com
- fix last change

* Wed Aug 26 2009 mls@suse.de
- make patch0 usage consistent

* Tue Aug  4 2009 mvyskocil@suse.cz
- Remove rhino dependency at all
- Added pom and maven depmap files from jpackage 5.0
- Removed javadoc %%%%post/un scripts

* Mon Aug  3 2009 mvyskocil@suse.cz
- Build using rhino
- Used bzip2 archive

* Wed Nov  5 2008 ro@suse.de
- buildignore rhino to fix build

* Mon Sep 25 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5

* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires

* Wed Jul 27 2005 jsmeix@suse.de
- Adjustments in the spec file.

* Mon Jul 18 2005 jsmeix@suse.de
- Current version 2.3.0 from JPackage.org

* Thu Sep 16 2004 skh@suse.de
- Fix prerequires in javadoc subpackage

* Sat Sep  4 2004 skh@suse.de
- Initial package created with version 2.3.0 (JPackage 1.5)
