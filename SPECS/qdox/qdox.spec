#
# spec file for package qdox
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

Summary:        Tool to extract class/interface/method definitions from sources
Name:           qdox
Version:        2.0.0
Release:        2%{?dist}
License:        ASL 2.0
Group:          Development/Libraries/Java
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/paul-hammant/qdox
Source0:        https://github.com/paul-hammant/qdox/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        qdox-MANIFEST.MF
BuildRequires:  byaccj
BuildRequires:  fdupes
BuildRequires:  java-cup-bootstrap
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jflex-bootstrap
BuildArch:      noarch

%description
QDox is a parser for extracting class/interface/method definitions
from source files complete with JavaDoc @tags. It is designed to be
used by active code generators or documentation tools.

%prep
%setup -q -n %{name}-%{name}-%{version}
find -name *.jar -delete
find -name *.class -delete
rm -rf bootstrap

# We don't need these plugins
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-failsafe-plugin
%pom_remove_plugin :maven-jflex-plugin
%pom_remove_plugin :maven-enforcer-plugin

%pom_xpath_set pom:workingDirectory '${basedir}/src/main/java/com/thoughtworks/qdox/parser/impl'

%pom_remove_parent .

%build
# Generate scanners (upstream does this with maven-jflex-plugin)
# Add the --inputstreamctor option if jflex is upgraded to a version 1.6 or higher
CLASSPATH=$(build-classpath java-cup) \
  jflex -d src/main/java/com/thoughtworks/qdox/parser/impl src/grammar/lexer.flex
CLASSPATH=$(build-classpath java-cup) \
  jflex -d src/main/java/com/thoughtworks/qdox/parser/impl src/grammar/commentlexer.flex

# Generate the parsers using the command-line that the exec-maven-plugin uses
GRAMMAR_PATH=$(pwd)/src/grammar/commentparser.y && \
  (cd src/main/java/com/thoughtworks/qdox/parser/impl && \
  byaccj -v -Jnorun -Jnoconstruct -Jclass=DefaultJavaCommentParser \
    -Jpackage=com.thoughtworks.qdox.parser.impl ${GRAMMAR_PATH})
GRAMMAR_PATH=$(pwd)/src/grammar/parser.y && \
  (cd src/main/java/com/thoughtworks/qdox/parser/impl && \
  byaccj -v -Jnorun -Jnoconstruct -Jclass=Parser \
    -Jimplements=CommentHandler -Jsemantic=Value \
	-Jpackage=com.thoughtworks.qdox.parser.impl \
	-Jstack=500 ${GRAMMAR_PATH})

# Build artifact
mkdir -p build/classes
javac -d build/classes -source 6 -target 6 \
  $(find src/main/java -name \*.java)
jar cf build/%{name}-%{version}.jar -C build/classes .

# Inject OSGi manifests
jar ufm build/%{name}-%{version}.jar %{SOURCE1}

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 build/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a qdox:qdox

%files -f .mfiles
%license LICENSE.txt
%doc README.md

%changelog
* Mon Mar 28 2022 Cameron Baird <cameronbaird@microsoft.com> - 2.0.0-2
- Move to SPECS

* Thu Feb 10 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0-1
- Removing docs.
- License verified.
- Updating to version 2.0.0 and GitHub sources.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.M9-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.0.M9-3.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Apr  8 2019 Fridrich Strba <fstrba@suse.com>
- Do not depend on the parent pom, since we are not building
  using Maven.
* Tue Jan 15 2019 Fridrich Strba <fstrba@suse.com>
- BuildRequires: java-cup-bootstrap and jflex-bootstrap to avoid
  build cycle (bsc#1121958)
* Wed Jan  9 2019 Jan Engelhardt <jengelh@inai.de>
- Use noun phrase in summary, and trim bias from descriptions.
* Tue Jan  1 2019 Fridrich Strba <fstrba@suse.com>
- Update to version 2.0-M9
  * Changed API to use Collections and Lists instead of Arrays
  * No upstream changelog provided :/
* Mon Oct 29 2018 Fridrich Strba <fstrba@suse.com>
- Install and package the maven artifact
* Thu Apr  5 2018 fstrba@suse.com
- Build with java source and target version 6 in order to produce
  bytecode understood by all supported java versions
* Fri Jun  9 2017 tchvatal@suse.com
- Remove maven conditionals
- Drop javadoc to bootstrap
* Thu Aug 28 2014 coolo@suse.com
- rename the conditional to junit_test and switch the default,
  bootstrapping factory is more important than a single test
* Tue Aug 12 2014 lnussel@suse.de
- introduce %%with java_bootstrap to allow bootstrapping without junit
* Thu May 15 2014 darin@darins.net
- Added xz build requirement for sles
- no bytecode check on sles
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Fri Nov 30 2012 cobexer@gmail.com
- update to 1.12.1
  * bugfix release, see
  * http://jira.codehaus.org/browse/QDOX/fixforversion/18944
* Wed Nov 28 2012 mvyskocil@suse.com
- require saxon9 for build
* Wed Oct 24 2012 mvyskocil@suse.com
- update to 1.12
  * needed for the fop 1.1 update
  * mostly bugfix release, see
  * http://qdox.codehaus.org/changes-report.html
- disabled tests as they tends to randomly fails
* Tue May  5 2009 mvyskocil@suse.cz
- Initial build in SUSE. Version 1.6.1 from jpp 5.0
