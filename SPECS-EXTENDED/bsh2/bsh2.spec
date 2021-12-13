Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package bsh2
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
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


%define orig_name bsh
%define fversion  2.0b6
Name:           bsh2
Version:        2.0.0.b6
Release:        10%{?dist}
Summary:        Scripting for Java (BeanShell Version 2.x)
License:        SPL-1.0 OR LGPL-2.0-or-later
Group:          Development/Libraries/Java
URL:            http://www.beanshell.org/
Source0:        https://github.com/beanshell/beanshell/archive/%{fversion}.tar.gz#/%{name}-%{fversion}.tar.gz
#PATCH-FIX-OPENSUSE: use html output and JVM's built-in xmlns:redirect
Patch3:         bsh-2.0b5-docs.patch
#PATCH-FIX-OPENSUSE: those two patches fixes a compatibility with a standard javax.script API
Patch1000:      bsh2-fix-tests.patch
Patch1001:      reproducible.patch
Patch1002:      beanshell-2.0b6-target.patch
Patch1003:      beanshell-2.0b6-getpeer.patch
BuildRequires:  ant
BuildRequires:  bsf
BuildRequires:  bsf-javadoc
BuildRequires:  fdupes
BuildRequires:  glassfish-servlet-api
BuildRequires:  java-devel >= 1.8
BuildRequires:  javacc
BuildRequires:  javapackages-local-bootstrap
Requires:       bsf
Requires:       javapackages-tools
BuildArch:      noarch

%description
BeanShell is an embeddable Java source interpreter with object
scripting language features, written in Java. BeanShell executes
standard Java statements and expressions, in addition to obvious
scripting commands and syntax. BeanShell supports scripted objects as
simple method closures like those in Perl and JavaScript. BeanShell
can be used interactively for Java experimentation and debugging or
as a scripting engine for applications.

%package bsf
Summary:        BSF support for bsh2
Group:          Development/Libraries/Java
Requires:       bsf

%description bsf
Scripting for Java (BeanShell Version 2.x) (BSF support).

%package classgen
Summary:        ASM support for bsh2
Group:          Development/Libraries/Java

%description classgen
Scripting for Java (BeanShell Version 2.x) (ASM support).

%package manual
Summary:        Documentation for bsh2
Group:          Documentation/HTML

%description manual
Scripting for Java (BeanShell Version 2.x) (Manual).

%package javadoc
Summary:        Javadoc for bsh2
Group:          Documentation/HTML

%description javadoc
Scripting for Java (BeanShell Version 2.x) (Java Documentation).

%package demo
Summary:        Demonstrations and samples for bsh2
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}-%{release}

%description demo
Scripting for Java (BeanShell Version 2.x) (demo and samples).

%prep
%setup -q -n beanshell-%{fversion}
%patch3 -p1
%patch1000 -p1
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
for j in $(find . -name "*.jar"); do
    mv $j $j.no
done
# Remove bundled javax.script files under Sun's proprietary license
find engine/javax-src/javax/script/ -maxdepth 1 -type 'f' | xargs rm
mv tests/test-scripts/Data/addedCommand.jar.no tests/test-scripts/Data/addedCommand.jar
mv tests/test-scripts/Data/addclass.jar.no tests/test-scripts/Data/addclass.jar

%build
build-jar-repository -s -p lib bsf javacc glassfish-servlet-api
pushd engine/javax-src/
javac -cp $(build-classpath glassfish-servlet-api) -source 8 -target 8 $(find . -name "*.java")
jar cf ../../lib/javaxscript.jar $(find . -name "*.class" -o -name "*.html")
popd
# set VERSION
perl -p -i -e 's|VERSION =.*;|VERSION = "%{version}";|' src/bsh/Interpreter.java
ant \
    -Dbsf.javadoc=%{_javadocdir}/bsf \
    -Djava.javadoc=%{_javadocdir}/java \
    dist
(cd docs/faq && ant)
(cd docs/manual && ant)
%fdupes -s docs/

%install
# jars
mkdir -p %{buildroot}%{_javadir}/%{name}
rm -f dist/%{orig_name}-%{fversion}-src.jar
rm -f dist/%{orig_name}-%{fversion}-sources.jar
for jar in dist/*.jar; do
  install -m 644 ${jar} %{buildroot}%{_javadir}/%{name}/`basename ${jar} -%{fversion}.jar`-%{version}.jar
done
(cd %{buildroot}%{_javadir}/%{name} && for jar in *-%{version}*; do ln -s ${jar} ${jar/-%{version}/}; done)

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -m 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.%{name}-bsh.pom
%add_maven_depmap JPP.%{name}-bsh.pom %{name}/bsh.jar -a org.beanshell:%{name},bsh:bsh,bsh:bsh-bsf,org.beanshell:bsh

# manual
find docs "(" -name ".cvswrappers" -o -name "*.xml" -o -name "*.xsl" -o -name "*.log" ")" -delete
(cd docs/manual && mv -f html/* . && rm -Rf html xsl)

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -a javadoc/* %{buildroot}%{_javadocdir}/%{name}

# demo
for i in `find tests -name "*.bsh"`; do
  perl -p -i -e 's,^
?#!(/(usr/)?bin/java bsh\.Interpreter|/bin/sh),#!%{_bindir}/%{name},' $i
done

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a tests %{buildroot}%{_datadir}/%{name}
find %{buildroot}%{_datadir}/%{name} -type d \
  | sed 's|'%{buildroot}'|%dir |' >  %{name}-demo-%{version}.files
find %{buildroot}%{_datadir}/%{name} -type f -name "*.bsh" \
  | sed 's|'%{buildroot}'|%attr(0755,root,root) |'      >> %{name}-demo-%{version}.files
find %{buildroot}%{_datadir}/%{name} -type f ! -name "*.bsh" \
  | sed 's|'%{buildroot}'|%attr(0644,root,root) |'      >> %{name}-demo-%{version}.files
# bshservlet
mkdir -p %{buildroot}%{_datadir}/%{name}/bshservlet
(cd %{buildroot}%{_datadir}/%{name}/bshservlet
jar xf $RPM_BUILD_DIR/beanshell-%{fversion}/dist/bshservlet.war
)
# scripts
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh
#
# %{name} script
# JPackage Project (http://jpackage.sourceforge.net)
# Source functions library
. %{_datadir}/java-utils/java-functions
# Source system prefs
if [ -f %{_sysconfdir}/%{name}.conf ] ; then
  . %{_sysconfdir}/%{name}.conf
fi
# Source user prefs
if [ -f \$HOME/.%{name}rc ] ; then
  . \$HOME/.%{name}rc
fi
# Configuration
MAIN_CLASS=bsh.Interpreter
if [ -n "\$BSH_DEBUG" ]; then
  BASE_FLAGS=-Ddebug=true
fi
BASE_JARS="%{name}.jar"
# Set parameters
set_jvm
set_classpath \$BASE_JARS
set_flags \$BASE_FLAGS
set_options \$BASE_OPTIONS
# Let's start
run "\$@"
EOF
cat > %{buildroot}%{_bindir}/%{name}doc << EOF
#!/usr/bin/env %{_bindir}/%{name}
EOF
cat scripts/bshdoc.bsh >> %{buildroot}%{_bindir}/%{name}doc
%fdupes -s %{buildroot}
%fdupes docs/

%files
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0755,root,root) %{_bindir}/%{name}doc
%license LICENSE
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/%{orig_name}-%{version}.jar
%{_javadir}/%{name}/%{orig_name}.jar
%{_javadir}/%{name}/%{orig_name}-classpath*.jar
%{_javadir}/%{name}/%{orig_name}-commands*.jar
%{_javadir}/%{name}/%{orig_name}-core*.jar
%{_javadir}/%{name}/%{orig_name}-engine*.jar
%{_javadir}/%{name}/%{orig_name}-reflect*.jar
%{_javadir}/%{name}/%{orig_name}-util*.jar
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/bshservlet
%{_mavenpomdir}/*
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif

%files bsf
%{_javadir}/%{name}/%{orig_name}-bsf*.jar

%files classgen
%{_javadir}/%{name}/%{orig_name}-classgen*.jar

%files manual
%doc docs/*

%files javadoc
%dir %{_javadocdir}/%{name}
%{_javadocdir}/%{name}

%files demo -f %{name}-demo-%{version}.files

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0.b6-10
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.0.0.b6-9.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Apr 15 2019 Jan Engelhardt <jengelh@inai.de>
- Replace find -exec rm by just -delete.
- Trim BSH 2.x changelog from description, and trim "In other
  words" description repetition. Trim leftover filler wording
  from description.
* Thu Feb  7 2019 Fridrich Strba <fstrba@suse.com>
- Build against javacc and glassfish-servlet-api instead of
  javacc3 and servlet4
* Thu Nov  1 2018 Fridrich Strba <fstrba@suse.com>
- Do not build against an old system asm, but use the few shaded
  files source files distributed in the tarball.
- Removed patches:
  * bsh2-ClassGeneratorUtil.patch
  * bsh2-asm.patch
  - not needed after the above change
- Modified patch:
  * beanshell-2.0b6-target.patch
  - fix source level to correspond to the target
* Thu Oct 18 2018 Fridrich Strba <fstrba@suse.com>
- Use the pom.xml file from the sources to generate maven provides
* Wed May 16 2018 fstrba@suse.com
- Modified patch:
  * beanshell-2.0b6-target.patch
    + Build with source and target 8 to prepare for a possible
    removal of 1.6 compatibility
* Wed Sep 20 2017 fstrba@suse.com
- Build with whatever is the default java-devel provider
- Modified patch:
  * beanshell-2.0b6-target.patch
    + specify target and source consistently
    + fix classpath issue with javadoc generation
- Added patch:
  * beanshell-2.0b6-getpeer.patch
    + fix build with jdk9
  + access the inacessible APIs by reflection
* Thu Sep  7 2017 fstrba@suse.com
- Added patch:
  * beanshell-2.0b6-target.patch
  - Force java target level to 1.6
- Force java source and target levels to 1.6 in order to allow
  building with jdk9
- Force building with java-1_8_0-openjdk-devel since javadoc errors
  are fatal in jdk9
* Fri May 19 2017 mpluskal@suse.com
- Update package dependencies
* Wed Mar 16 2016 bwiedemann@suse.com
- Add reproducible.patch to fix build-compare
* Tue Feb 23 2016 tchvatal@suse.com
- Version update to 2.0b6 bnc#967593 CVE-2016-2510
  * Upstream developement moved to github
  * No obvious changelog apart from the above
- Refreshed/updated patches:
  * bsh-2.0b5-docs.patch
  * bsh2-ClassGeneratorUtil.patch
  * bsh2-asm.patch
  * bsh2-fix-tests.patch
- Delete needless patch:
  * bsh2-standard-script-api.patch
- Update version in .pom files
* Tue Mar 24 2015 tchvatal@suse.com
- Fix the pom's to not require network and thus pass parser validation
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Tue Jul  8 2014 tchvatal@suse.com
- Cleanup with spec-cleaner.
- Fix few rpmlint complaints
- Kill src package as nothing seem to depend on it and it is pointless.
* Tue Jul  8 2014 tchvatal@suse.com
- Change the bytecode stuff.
* Thu May 15 2014 darin@darins.net
- disable bytecode check on sle_11
- disable post-build-check on SLE_11 due to FHS 2.2 errors
* Thu Feb  6 2014 fcrozat@suse.com
- Fix license tag to SPL-1.0 or LGPL-2.0+ (bnc#862426)
- Encure License.txt is part of main package (bnc#862426)
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Wed Aug 28 2013 mvyskocil@suse.com
- use add_maven_depmap from javapackages-tools
- unversioned javadoc dir
* Thu Jul 25 2013 tchvatal@suse.com
- Fix build on factory with new rpm.
* Fri Mar 11 2011 mvyskocil@suse.cz
- Fix build of documentation, remove xalan-j2 dependency
  * add bsh-2.0b5-docs.patch
* Mon Aug  9 2010 mvyskocil@suse.cz
- Add a new bsh2-src subpackage, which will be used for build of jedit
  bnc#629375
* Wed Nov 25 2009 mvyskocil@suse.cz
- Updated to bsh-2.0b5
  * Merged with bsh2-2.0-0.b5.1.jpp5.src.rpm
- Do not use a bundled javax.script API
- Obsoleted patches:
  * bsh2-build.patch
  * bsh2-crosslink.patch
  * bsh2-java14compat.patch
  * bsh2-java15.patch
  * bsh2-jedit.patch
  * bsh2-readline.patch
* Wed Mar 25 2009 mvyskocil@suse.cz
- added xalan-j2 and ant-trax to BR for documentation build
* Fri Mar 30 2007 aj@suse.de
- Add unzip to BuildRequires.
* Mon Sep 25 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Mon Oct 17 2005 jsmeix@suse.de
- Current version 2.0 from JPackage.org
