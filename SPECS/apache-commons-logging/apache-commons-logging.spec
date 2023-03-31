#
# spec file for package apache-commons-logging
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2000-2007, JPackage Project
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
%define base_name  logging
%define short_name commons-%{base_name}
Summary:        Apache Commons Logging
Name:           apache-%{short_name}
Version:        1.2
Release:        11%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://commons.apache.org/%{base_name}
Source0:        http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source4:        http://central.maven.org/maven2/%{short_name}/%{short_name}-api/1.1/%{short_name}-api-1.1.pom
Patch0:         commons-logging-1.1.3-src-junit.diff
Patch1:         commons-logging-1.2-sourcetarget.patch
Patch2:         commons-logging-manifests.patch
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  glassfish-servlet-api
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit
Requires:       java >= 1.8
Provides:       jakarta-%{short_name} = %{version}-%{release}
Provides:       mvn(commons-logging:commons-logging) = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < %{version}
Provides:       %{short_name} = %{version}-%{release}
Obsoletes:      %{short_name} < %{version}
BuildArch:      noarch

%description
The commons-logging package provides a simple, component oriented
interface (org.apache.commons.logging.Log) together with wrappers for
logging systems. The user can choose at runtime which system they want
to use. In addition, a small number of basic implementations are
provided to allow users to use the package standalone.
commons-logging was heavily influenced by Avalon's Logkit and Log4J. The
commons-logging abstraction is meant to minimize the differences between
the two, and to allow a developer to not tie himself to a particular
logging implementation.

%prep
%setup -q -n %{short_name}-%{version}-src
%patch0 -p1
%patch1 -p1
%patch2 -p1

sed -i 's/\r//' RELEASE-NOTES.txt LICENSE.txt

#FIXME
rm ./src/test/java/org/apache/commons/logging/servlet/BasicServletTestCase.java

%pom_remove_parent .

# Remove log4j12 and components not provided in CBL-Mariner.
%pom_remove_dep -r :avalon-framework
%pom_remove_dep -r :logkit
%pom_remove_dep -r :log4j
rm src/main/java/org/apache/commons/logging/impl/AvalonLogger.java
rm src/main/java/org/apache/commons/logging/impl/Log4JLogger.java
rm src/main/java/org/apache/commons/logging/impl/LogKitLogger.java
rm -r src/test/java/org/apache/commons/logging/{avalon,log4j,logkit}
rm src/test/java/org/apache/commons/logging/pathable/{Parent,Child}FirstTestCase.java

# Remove log4j12 tests
rm -rf src/test/java/org/apache/commons/logging/log4j/log4j12

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

export CLASSPATH=$(build-classpath \
                   plexus/ \
                   junit \
                  ):target/classes:target/test-classes
ant \
  -Dmaven.mode.offline=true -lib %{_javadir} \
  -Dservletapi.jar=%{_javadir}/glassfish-servlet-api.jar \
  dist

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
install -p -m 644 target/%{short_name}-api-%{version}.jar %{buildroot}%{_javadir}/%{name}-api.jar
install -p -m 644 target/%{short_name}-adapters-%{version}.jar %{buildroot}%{_javadir}/%{name}-adapters.jar

pushd %{buildroot}%{_javadir}
for jar in %{name}*; do
    ln -sf ${jar} `echo $jar| sed "s|apache-||g"`
done
popd

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}/%{_mavenpomdir}/%{short_name}-%{version}.pom
sed 's#<version>1.1</version>#<version>1.2</version>#g' < %{SOURCE4} > tmp.pom
install -pm 644 tmp.pom %{buildroot}/%{_mavenpomdir}/%{short_name}-api-%{version}.pom
sed -e 's#<version>1.1</version>#<version>1.2</version>#g' -e "s#%{short_name}-api#%{short_name}-adapters#g" < %{SOURCE4} > tmp.pom
install -pm 644 tmp.pom %{buildroot}/%{_mavenpomdir}/%{short_name}-adapters-%{version}.pom
%add_maven_depmap %{short_name}-%{version}.pom %{short_name}.jar -a "org.apache.commons:%{short_name}","apache:%{short_name}"
%add_maven_depmap %{short_name}-api-%{version}.pom %{short_name}-api.jar -a "org.apache.commons:%{short_name}-api","apache:%{short_name}-api"
%add_maven_depmap %{short_name}-adapters-%{version}.pom %{short_name}-adapters.jar -a "org.apache.commons:%{short_name}-adapters","apache:%{short_name}-adapters"

%files -f .mfiles
%{_javadir}/%{name}*.jar
%license LICENSE.txt
%doc PROPOSAL.html RELEASE-NOTES.txt NOTICE.txt

%changelog
* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.2-11
- Fixing maven provides

* Fri Jan 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2-10
- Removing 'log4j12' dependency.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2-9
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.2-8.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix linebreak in sed command.

* Tue Oct  1 2019 Fridrich Strba <fstrba@suse.com>
- Build against the new compatibility log4j12-mini package

* Mon Mar 25 2019 Fridrich Strba <fstrba@suse.com>
- Remove pom parent, since we don't use it when not building with
  maven
- Use the pom.xml distributed with the package instead of
  downloading the same file as a separate source

* Wed Feb  6 2019 Fridrich Strba <fstrba@suse.com>
- Build against glassfish-servlet-api

* Mon Jan 28 2019 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * commons-logging-manifests.patch
    + Different Bundle-SymbolicName for different jars

* Fri Oct 19 2018 Fridrich Strba <fstrba@suse.com>
- Cleanup of maven pom files installation

* Tue May 15 2018 fstrba@suse.com
- Modified patch:
  * commons-logging-1.2-sourcetarget.patch
    + Build with source and target 8 to prepare for a possible
    removal of 1.6 compatibility

* Thu Sep  7 2017 fstrba@suse.com
- Added patch:
  * commons-logging-1.2-sourcetarget.patch
  - set java source and target versions to 1.6 in order to allow
    build with jdk9

* Fri May 19 2017 tchvatal@suse.com
- Remove bootstrap conditional

* Fri May 19 2017 pcervinka@suse.com
- New build dependency: javapackages-local
- Fixed requires

* Sun Jan 24 2016 p.drouand@gmail.com
- Update to version 1.2
  see http://commons.apache.org/proper/commons-logging/changes-report.html
  or RELEASE-NOTES.txt for details

* Wed Mar 25 2015 tchvatal@suse.com
- Drop maven conditionals that were never triggered.

* Wed Mar 25 2015 tchvatal@suse.com
- Drop gpg offline and rely on service

* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools

* Wed Mar  4 2015 tchvatal@suse.com
- Use log4j-mini to hopefully avoid build-cycle

* Fri Feb 20 2015 dmacvicar@suse.de
- add the log4j adapter to commons-logging-adapters
  (bnc#918852)

* Tue Aug 12 2014 lnussel@suse.de
- add bcond java_bootstrap to build without unit tests
  (commons-logging-1.1.3-src-junit.diff)

* Fri Jun 27 2014 tchvatal@suse.com
- Provides obsoletes to be versioned

* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools

* Tue Aug 27 2013 mvyskocil@suse.com
- update to 1.1.3 (bugfix release)
  see http://commons.apache.org/proper/commons-logging/changes-report.html
  or RELEASE-NOTES.txt for details
- add gpg verification
- use new add_maven_depmap from javapackages-tools
- dropped unecessary patches/sources
  * build.xml.patch
  * commons-logging-eclipse-manifest.patch
  * commons-logging-maven-release-plugin.patch
  * and commons-logging.depmap

* Mon Apr  2 2012 mvyskocil@suse.cz
- provide commons-logging

* Tue Feb 28 2012 mvyskocil@suse.cz
- fix build cycle, do not require avalon-* for build and use servletapi5
  instead of tomcat6 package

* Wed Feb  8 2012 mvyskocil@suse.cz
- rename to apache-commons-logging to follow jpackage and Fedora
- update to 1.1.1 (bugfix release)
  * usable under security policy (catches SecurityException)
  * show content of chained exceptions
  * fix unit tests on linux an java6
  * provide maven2 pom file
  * fix thread-safety bug

* Sat Aug 27 2011 andrea.turrini@gmail.com
- fixed typos in jakarta-commons-logging.spec

* Wed Jul 16 2008 coolo@suse.de
- trying to reduce build requires

* Tue May  8 2007 kesselborn@suse.de
- remove avalon references ... avalon is dropped and support for it hence not needed

* Mon Sep 25 2006 skh@suse.de
- fix BuildRequires
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5

* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires

* Wed Jul 27 2005 jsmeix@suse.de
- Adjustments in the spec file.

* Mon Jul 18 2005 jsmeix@suse.de
- Current version 1.0.4 from JPackage.org

* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage

* Sun Sep  5 2004 skh@suse.de
- Initial package created with version 1.0.4 (JPackage 1.5)
'????;