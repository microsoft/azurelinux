Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package bcel
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


Name:           bcel
Version:        5.2
Release:        37%{?dist}
Summary:        Byte Code Engineering Library
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/proper/commons-bcel/
Source0:        https://archive.apache.org/dist/commons/bcel/source/%{name}-%{version}-src.tar.gz
Source1:        https://archive.apache.org/dist/commons/bcel/source/%{name}-%{version}-src.tar.gz.asc
Source2:        https://repo.maven.apache.org/maven2/org/apache/%{name}/%{name}/%{version}/%{name}-%{version}.pom
Source3:        bcel.keyring
Patch0:         bcel-5.2-encoding.patch
BuildRequires:  ant
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  regexp
#!BuildIgnore:  xalan-j2 xerces-j2 xml-apis xml-resolver
Requires:       regexp
BuildArch:      noarch

%description
The Byte Code Engineering Library is intended to give users a
convenient way to analyze, create, and manipulate (binary) Java class
files (those ending with .class). Classes are represented by objects
that contain all the symbolic information of the given class: methods,
fields, and byte code instructions, in particular.

Such objects can be read from an existing file, transformed by a
program (such as a class loader at runtime), and dumped to a file
again. An even more interesting application is the creation of classes
from scratch at runtime. The Byte Code Engineering Library (BCEL) may
also be useful if you want to learn about the Java Virtual Machine
(JVM) and the format of Java .class files.

BCEL is already being used successfully in several projects, such as
compilers, optimizers, obfuscators, code generators, and analysis
tools.

It contains a byte code verifier named JustIce, which usually gives you
much better information about what is wrong with your code than the
standard JVM message.

%prep
%setup -q
%patch 0 -p1
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
# very broken build
perl -p -i -e 's| depends=\"examples\"||g;' build.xml
touch manifest.txt

%build
export CLASSPATH=%(build-classpath regexp)
export OPT_JAR_LIST="ant/ant-nodeps"
ant \
    -Dant.build.javac.target=8 -Dant.build.javac.source=8 \
    -Dbuild.dest=./build -Dbuild.dir=./build -Dname=%{name} \
    compile
ant \
    -Dant.build.javac.target=8 -Dant.build.javac.source=8 \
    -Dbuild.dest=./build -Dbuild.dir=./build -Dname=%{name} \
	jar

%install
# jars
mkdir -p %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -s ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

mkdir -p %{buildroot}%{_mavenpomdir}
install -m 644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/%{name}-%{version}.pom

%add_maven_depmap %{name}-%{version}.pom %{name}-%{version}.jar -a "bcel:bcel"

%files -f .mfiles
%license LICENSE.txt
%{_javadir}/*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.2-37
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 5.2-36.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Fri Feb  1 2019 Fridrich Strba <fstrba@suse.com>
- BuildIgnore xalan-j2, xml-apis, xml-resolver, xerces-j2, since
  those packages are not necessary for the build.
* Mon Dec 10 2018 Fridrich Strba <fstrba@suse.com>
- Build against the generic xml-apis provider which allows
  building against bootstrap and non-bootstrap packages according
  of their availability.
* Thu Nov 15 2018 Fridrich Strba <fstrba@suse.com>
- Add maven pom file and generate mvn(...) dependencies for this
  package
* Tue May 15 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
* Wed Sep 27 2017 fstrba@suse.com
- Allow building with any java-devel provider
- Specify java source and target level 1.6 to fix build with jdk9
- Added patch:
  * bcel-5.2-encoding.patch
    + specify the correct encoding of the files
* Fri May 19 2017 tchvatal@suse.com
- Buildignore more java implementations
* Wed Mar 25 2015 tchvatal@suse.com
- Drop gpg-offline
- Drop conditional for manual that is never triggered
* Tue Jul  8 2014 tchvatal@suse.com
- Do not depend on ant-nodeps.
* Tue Sep  3 2013 mvyskocil@suse.com
- use pristine tarballs
- fix source url
- add gpg verification
- format spec file
* Thu Aug 22 2013 mvyskocil@suse.com
- disable javadoc generation
* Mon Jan  7 2013 mvyskocil@suse.com
- remove xerces-j2-bootstrap dependency (bnc#789163)
* Tue May 15 2012 mvyskocil@suse.cz
- ignore openjdk from build
* Sat Sep 17 2011 jengelh@medozas.de
- Remove redundant tags/sections from specfile
- Use %%_smp_mflags for parallel build
* Mon Nov  8 2010 mvyskocil@suse.cz
- build ignore xml-commons-jaxp-1.3-apis
* Mon Jun  1 2009 mvyskocil@suse.cz
- fixed archive name (gz -> bz2) in Source
* Thu May 21 2009 mvyskocil@suse.cz
- update to 5.2
- fixed build under gcj44
- removed javadoc scripplets
* Sun Jul 27 2008 coolo@suse.de
- avoid xerces and xml-commons (ant still works)
* Tue Jul 22 2008 coolo@suse.de
- build with gcj to avoid build cycle
* Mon Sep 25 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Wed Jul 27 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Mon Jul 18 2005 jsmeix@suse.de
- Current version 5.1 from JPackage.org
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage
* Sat Sep  4 2004 skh@suse.de
- Switched to JPackage 1.5 version
- split off subpackages bcel-javadoc and bcel-manual
* Mon Feb  9 2004 pmladek@suse.cz
- package created, version 5.1
- added trigger to create link to the ant lib dir
