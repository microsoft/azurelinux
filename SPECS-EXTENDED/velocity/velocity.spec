Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package velocity
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


Name:           velocity
Version:        1.7
Release:        11%{?dist}
Summary:        Java-based template engine
License:        ASL 2.0
Group:          Development/Libraries/Java
URL:            https://velocity.apache.org/
Source0:        https://github.com/apache/%{name}-engine/archive/refs/tags/%{version}.tar.gz#/%{name}-engine-%{version}.tar.gz
Patch0:         velocity-build_xml.patch
Patch1:         0001-Port-to-apache-commons-lang3.patch
Patch2:         0002-Force-use-of-JDK-log-chute.patch
Patch3:         0003-CVE-2020-13936.patch

BuildArch:      noarch

BuildRequires:  ant >= 1.6.5
BuildRequires:  ant-junit
BuildRequires:  antlr
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  mvn(commons-collections:commons-collections)
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache:apache:pom:)
BuildRequires:  servletapi4

Requires:       commons-collections
Requires:       commons-lang3
Requires:       java >= 1.6.0

%description
Velocity is a Java-based template engine. It permits anyone to use the
simple yet powerful template language to reference objects defined in
Java code.
When Velocity is used for web development, Web designers can work in
parallel with Java programmers to develop web sites according to the
Model-View-Controller (MVC) model, meaning that web page designers can
focus solely on creating a site that looks good, and programmers can
focus solely on writing top-notch code. Velocity separates Java code
from the web pages, making the web site more maintainable over the long
run and providing a viable alternative to Java Server Pages (JSPs) or
PHP.
Velocity's capabilities reach well beyond the realm of web sites; for
example, it can generate SQL and PostScript and XML (see Anakia for more
information on XML transformations) from templates. It can be used
either as a standalone utility for generating source code and reports,
or as an integrated component of other systems. Velocity also provides
template services for the Turbine web application framework.
Velocity+Turbine provides a template service that will allow web
applications to be developed according to a true MVC model.

%prep
%autosetup -p1 -n %{name}-engine-%{version}
find . -name '*.jar' ! -name 'test*.jar' -print -delete
find . -name '*.class' ! -name 'Foo.class' -print -delete

# Disable unneeded features
rm -r src/java/org/apache/velocity/{anakia,texen,servlet,convert}
rm src/java/org/apache/velocity/runtime/log/{Avalon,Log4J}Log{Chute,System}.java
rm src/java/org/apache/velocity/runtime/log/{CommonsLog,Servlet}LogChute.java
rm src/java/org/apache/velocity/runtime/log/SimpleLog4JLogSystem.java
rm src/java/org/apache/velocity/runtime/log/VelocityFormatter.java
rm src/java/org/apache/velocity/app/event/implement/Escape{Html,JavaScript,Sql,Xml,}Reference.java

%pom_remove_parent pom.xml
%pom_remove_dep :commons-logging
%pom_remove_dep :jdom
%pom_remove_dep :log4j
%pom_remove_dep :logkit
%pom_remove_dep :oro
%pom_remove_dep :servlet-api
%pom_remove_dep :werken-xpath

%build
mkdir -p bin/lib
pushd bin/lib
ln -sf $(build-classpath ant)
ln -sf $(build-classpath antlr)
ln -sf $(build-classpath commons-collections)
ln -sf $(build-classpath commons-lang3)
# Use servletapi4 instead of servletapi5 in CLASSPATH
ln -sf $(build-classpath servletapi4)
popd

export CLASSPATH=$(build-classpath commons-collections commons-lang3 antlr)
export OPT_JAR_LIST="ant/ant-junit junit"
ant \
  -Djavac.source=1.6 -Djavac.target=1.6 \
  -buildfile build/build.xml \
  jar

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 bin/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap -a velocity:velocity

# Remove docs.
rm -rf docs/*

# zero-length file
rm -r test/issues/velocity-537/compare/velocity537.vm.cmp

%files -f .mfiles
%license LICENSE NOTICE
%doc README.txt

%changelog
* Tue Feb 22 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7-11
- Removing dependency on 'jdom', 'oro', 'servlet-api', and 'werken-xpath'.
- Removing 'manual' and 'javadoc' subpackages.

* Mon Jan 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7-10
- Removing dependency on "avalog-logkit" and "log4j12".
- Ported to "commons-lang3".
- License verified.
- Changes done using Fedora 33 (license: MIT) spec as guidance.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.7-9
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.7-8.4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Oct  1 2019 Fridrich Strba <fstrba@suse.com>
- Build against the compatibility package log4j12
* Mon Apr  8 2019 Fridrich Strba <fstrba@suse.com>
- Do not depend on the apache-parent, since we are not building
  using Maven.
* Thu Feb 14 2019 Fridrich Strba <fstrba@suse.com>
- Build against the new plexus-classworlds package
* Mon Nov  5 2018 Fridrich Strba <fstrba@suse.com>
- Add alias "velocity:velocity" to the maven artifact
* Tue Sep 19 2017 fstrba@suse.com
- Fix buid with jdk9: specify java source and target level 1.6
* Fri May 19 2017 tchvatal@suse.com
- Remove unneeded deps
* Fri May 19 2017 dziolkowski@suse.com
- New build dependency: javapackages-local
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Fri Dec  5 2014 p.drouand@gmail.com
- Update to version 1.7
  + No changelog available
- Add requirement to commons-logging; new dependency
- Remove java-devel >= 1.6.0 requirement; not needed anymore
- Do not copy convert folder; doesn't exist anymore
* Fri Jun 27 2014 tchvatal@suse.com
- Fix build on SLE11
* Wed Sep 11 2013 mvyskocil@suse.com
- use add_maven_depmap from javapackages-tools
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Mon Dec 17 2012 mvyskocil@suse.com
- require avalon-logkit
  * drop excalibur from Factory
* Wed Jun  3 2009 mvyskocil@suse.cz
- Initial SUSE packaging
