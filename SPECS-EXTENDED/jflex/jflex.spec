
#
# spec file for package jflex
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define with()          %{expand:%%{?with_%{1}:1}%%{!?with_%{1}:0}}
%define without()       %{expand:%%{?with_%{1}:0}%%{!?with_%{1}:1}}
%define bcond_with()    %{expand:%%{?_with_%{1}:%%global with_%{1} 1}}
%define bcond_without() %{expand:%%{!?_without_%{1}:%%global with_%{1} 1}}
%define _without_bootstrap 1
%define section            free
Name:           jflex
Vendor:         Microsoft Corporation
Distribution:   Mariner
Version:        1.4.3
Release:        30%{?dist}
Summary:        Lexical Analyzer Generator for Java
License:        GPL-2.0+
Group:          Development/Libraries/Java
Url:            http://www.jflex.de/
Source0:        http://www.jflex.de/jflex-%{version}.tar.bz2
Source1:        jflex.script
Source100:      jpackage-bootstrap-prepare.sh
Patch0:         jflex-javac-no-target.patch
Patch1:         jflex-no-cup-no-jflex.patch
Patch2:         jflex-classpath.patch
Patch4:         jflex-byaccj-utl.patch
#PATCH-FIX-OPENSUSE: make AllTests.main empty, code was not compatible with junit 4
Patch5:         jflex-junit4.patch
BuildRequires:  ant
BuildRequires:  java-cup-bootstrap
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
Requires:       java_cup
Requires:       javapackages-tools
BuildArch:      noarch
%if %without bootstrap
BuildRequires:  jflex-bootstrap
BuildRequires:  junit
Conflicts:      jflex-bootstrap
%else
Conflicts:      jflex
%endif

%description
JFlex is a lexical analyzer generator for Java written in Java. It is
also a rewrite of the very useful tool JLex which was developed by
Elliot Berk at Princeton University. As Vern Paxson states for his C/C++
tool flex: they do not share any code though.

Design goals The main design goals of JFlex are:

    * Full unicode support
    * Fast generated scanners
    * Fast scanner generation
    * Convenient specification syntax
    * Platform independence
    * JLex compatibility

%if %without bootstrap
%package doc
Summary:        Documentation and examples for %{name}
Group:          Development/Libraries/Java

%description doc
JFlex is a lexical analyzer generator for Java written in Java. It is
also a rewrite of the very useful tool JLex which was developed by
Elliot Berk at Princeton University. As Vern Paxson states for his C/C++
tool flex: they do not share any code though.

Design goals The main design goals of JFlex are:

    * Full unicode support
    * Fast generated scanners
    * Fast scanner generation
    * Convenient specification syntax
    * Platform independence
    * JLex compatibility

This package contains documentation and examples for %{name}
%endif

%prep
%setup -q -n jflex-%{version}
perl -pi -e 's/
$//g' examples/standalone/sample.inp
rm -rf src/java_cup
find . -name '*.jar' | xargs -t rm
%if %without bootstrap
export CLASSPATH=$(build-classpath java-cup java-cup-runtime junit jflex)
export OPT_JAR_LIST=:
pushd src
%{ant} realclean
%{ant} -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 jflex
popd
%endif
%patch0 -p1

%if %with bootstrap
%patch1 -p1

echo `pwd`
rm -rf src/JFlex/tests
%else # with bootstrap
# You must use Re jflex.spec and have a java-cup and jflex installed
%patch2 -p1
%patch4 -p1
%patch5 -p1
%endif

%build
pushd src
%if %without bootstrap
export CLASSPATH=$(build-classpath java-cup java-cup-runtime junit jflex antlr-bootstrap)
%else
export CLASSPATH=$(build-classpath java-cup java-cup-runtime junit antlr-bootstrap)
%endif
export OPT_JAR_LIST=:
echo `pwd`
%{ant} -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 jar
popd

%install
# jar
mkdir -p %{buildroot}%{_javadir}
cp -a lib/JFlex.jar %{buildroot}%{_javadir}/jflex-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -s ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# compatibility symlink
(cd %{buildroot}%{_javadir} && ln -s jflex.jar JFlex.jar)

mkdir -p %{buildroot}%{_bindir}
install -p -m 0755 %{SOURCE1} %{buildroot}%{_bindir}/jflex

%files
%doc COPYRIGHT src/README src/changelog
%attr(0755,root,root) %{_bindir}/jflex
%{_javadir}/jflex.jar
%{_javadir}/jflex-%{version}.jar
%{_javadir}/JFlex.jar

%if %without bootstrap
%files doc
%doc examples doc
%endif

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.3-30
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.4.3-29.10
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Turn on bootstrap mode.
- Remove bootstrap generation code on eval.
- Add buildrequires on javapackages-local-bootstrap

* Wed Oct  4 2017 fstrba@suse.com
- Removed a jflex-lex-scan.patch again, so that bot is happy
* Tue Oct  3 2017 fstrba@suse.com
- Don't BuildRequire java-1_5_0-gcj-compat-devel, since it will be
  soon gone; BuildRequire java-devel
- Build with java source and target level 1.6 to allow building
  with jdk9
- Sync the bootstrap and non-bootstrap spec files using the
  jpackage-bootstrap-prepare.sh script and clean spec file
* Mon Dec  2 2013 mvyskocil@suse.com
- conflict the non-bootstrap variant with the bootstrap variant
* Thu Nov 14 2013 mvyskocil@suse.com
- Fix build with junit 4
  * jflex-junit4.patch
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Mon Aug 26 2013 mvyskocil@suse.com
- don't build tests when bootstrapping
- properly synchronized both spec files
- drop antlr-bootstrap dependency, it's pointless withouth javadoc
* Fri Aug 23 2013 mvyskocil@suse.com
- don't build javadoc
* Wed Feb 16 2011 mvyskocil@suse.cz
- fix build with antlr-bootstrap
* Thu May 21 2009 mvyskocil@suse.cz
- Removed a jflex-lex-scan.patch
* Tue May  5 2009 mvyskocil@suse.cz
- Update to 1.4.3 (bugfix release)
- Build using java-1_5_0-gcj to allow openjdk bootstrap
- Recreated jflex-lex-scan.patch
* Wed Apr 29 2009 mvyskocil@suse.cz
- Initial packaging of jflex-bootstrap 1.4.2 in SUSE (from jpp5)
