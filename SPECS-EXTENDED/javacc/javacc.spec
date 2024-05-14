Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package javacc
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2000-2005, JPackage Project
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

Summary:        A Parser and Scanner Generator for Java
Name:           javacc
Version:        7.0.4
Release:        3%{?dist}
License:        BSD-3-Clause
Group:          Development/Libraries/Java
URL:            https://javacc.org
Source0:        https://github.com/javacc/javacc/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  ant
BuildArch:      noarch

BuildRequires:  %{name}-bootstrap
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap

Conflicts:      %{name}-bootstrap

Obsoletes:      %{name}-bootstrap <= %{version}-%{release}
# Explicit javapackages-tools requires since scripts use
# /usr/share/java-utils/java-functions
Requires:       javapackages-tools

%description
Java Compiler Compiler (JavaCC) is the most popular parser generator
for use with Java applications. A parser generator is a tool that reads
a grammar specification and converts it to a Java program that can
recognize matches to the grammar. In addition to the parser generator
itself, JavaCC provides other standard capabilities related to parser
generation such as tree building (via a tool called JJTree included
with JavaCC), actions, debugging, etc.

%package manual
Summary:        Manual for %{name}
Group:          Documentation/Other

%description manual
Manual for %{name}.

%package demo
Summary:        Examples for %{name}
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}-%{release}

%description demo
Examples for %{name}.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{version}
rm -f lib/*.jar
rm -f bootstrap/javacc.jar
build-jar-repository -s -p bootstrap javacc

find ./examples -type f -exec sed -i 's/\r//' {} \;

# The pom dependencies are wrong
%pom_xpath_remove pom:project/pom:dependencies

%build
%{ant} \
  -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 \
  jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/javadoc/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}
%fdupes -s www
%fdupes -s examples

%jpackage_script javacc '' '' javacc javacc true
ln -s %{_bindir}/javacc %{buildroot}%{_bindir}/javacc.sh
%jpackage_script jjdoc '' '' javacc jjdoc true
%jpackage_script jjtree '' '' javacc jjtree true

%files -f .mfiles
%{_bindir}/javacc
%{_bindir}/javacc.sh
%{_bindir}/jjdoc
%{_bindir}/jjtree
%license LICENSE
%doc README

%files manual
%doc www/*

%files demo
%doc examples

%files javadoc
%license LICENSE
%{_javadocdir}/%{name}

%changelog
* Sat Jul 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.0.4-3
- Splitting as separate 'javacc' package with a build-time dependency on 'javacc-bootstrap'.
- Switching to using single digit 'Release' tags.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 7.0.4-2.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Switch to bootstrap mode.
- Use javapackages-local-bootstrap to avoid build cycle.in normal mode.
- Fix linebreak in sed command.

* Tue Apr  9 2019 Fridrich Strba <fstrba@suse.com>
- Make this a multibuild package where the bootstrap version is
  built using the included javacc.jar and the non-bootstrap version
  uses the system javacc.jar
* Wed Feb  6 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to 7.0.4
  * No obvious changelog
  * Fixes a number of C++ generation issues
- Generate the scripts during build using jpackage_script
- Build and package the javadoc documentation
- Removed patch:
  * javacc.patch
    + not needed any more in this version
* Mon Sep 18 2017 fstrba@suse.com
- Fix build with jdk9: specify java source and target 1.6
* Thu Jan  5 2017 tchvatal@suse.com
- Do not use gcj as it is getting deprecated
* Thu Jul 30 2015 tchvatal@suse.com
- Version bump to 5.0:
  * No obvious changelog
  * Works better with jdk8
- Updated to match up with fedora version
* Wed Sep 25 2013 mvyskocil@suse.com
- Build with gcc-java as openjdk7 (1.7.0_40) fails to build it
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Mon Jan 28 2008 mmaher@suse.de
- updated to 4.0:
  See the bug list in issue tracker for all the bugs fixed in this release.
    JJTree and JavaCC both now support 1.5 syntax.
    We now support accessing token fields in the grammar like: s=<ID>.image
    Convenient constructors for passing encoding directly to the grammar
    Tabsetting is now customizable.
    SimpleNode can now extend a class using the NODE_EXTENDS option.
    JAVACODE and BNF productions take optional access modifiers.
* Tue Sep 19 2006 ro@suse.de
- set source=1.4 for java
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Tue Oct 18 2005 jsmeix@suse.de
- Current version 3.2 from JPackage.org
* Wed Sep 28 2005 dmueller@suse.de
- add norootforbuild
* Fri Feb 18 2005 skh@suse.de
- initial package
