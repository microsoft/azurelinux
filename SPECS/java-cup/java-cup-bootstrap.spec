#
# spec file for package java-cup
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

%define cvs_version    11b
%define real_name      java-cup
%define pub_date       20210814

Summary:        LALR Parser Generator in Java
Name:           java-cup-bootstrap
Version:        0.11
Release:        31%{?dist}
License:        HPND
Group:          Development/Libraries/Java
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            http://www2.cs.tum.edu/projects/cup/
Source0:        https://versioncontrolseidl.in.tum.de/parsergenerators/cup/-/archive/master/cup-master.tar.gz#/java-cup-%{cvs_version}.tar.gz
Source1:        java-cup-generated-files.tar.xz
Source2:        java-cup.license
# From          http://www2.cs.tum.edu/projects/cup/
Patch1:         java-cup-no-classpath-in-manifest.patch
Patch2:         java-cup-no-cup-no-jflex.patch
Patch3:         java-cup-classpath.patch
BuildRequires:  ant
BuildRequires:  git
BuildRequires:  java-cup-bootstrap
BuildRequires:  java-devel
BuildRequires:  jflex-bootstrap
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  xml-commons-apis-bootstrap
BuildRequires:  xml-commons-resolver-bootstrap
#!BuildIgnore:  xalan-j2
#!BuildIgnore:  xerces-j2
#!BuildIgnore:  xml-commons-apis
#!BuildIgnore:  xml-commons-resolver
Obsoletes:      java-cup-bootstrap < %{version}-%{release}
Provides:       java-cup-bootstrap = %{version}-%{release}
Conflicts:      java-cup
BuildArch:      noarch

%description
java-cup is a LALR Parser Generator in Java. With v0.11, you can: 
* use CUP in an Ant-Target
* start CUP by a simple command like java -jar java-cup-11a.jar
   myGrammar.cup
* use generic parametrized classes (since Java 1.5) as datatypes for
   non terminals and terminals
* have Your own symbol classes

%prep
%setup -q -n cup-master
%patch1 -p1
%setup -q -T -D -a 1 -n cup-master
%patch2 -p1
# remove all binary files
find -name "*.class" -delete
find -name "*.jar" -delete
mkdir -p target/classes

%build
export CLASSPATH=
export OPT_JAR_LIST=:
ant

cp %{SOURCE2} license.txt

%install
# jar
mkdir -p %{buildroot}%{_javadir}
cp -a target/dist/%{real_name}-%{cvs_version}.jar %{buildroot}%{_javadir}/%{real_name}-%{version}.jar
cp -a target/dist/%{real_name}-%{cvs_version}-runtime.jar %{buildroot}%{_javadir}/%{real_name}-runtime-%{version}.jar

pushd %{buildroot}%{_javadir}
for jar in *-%{version}*; do
  ln -s ${jar} ${jar/-%{version}/};
done
# compatibility symlinks
ln -s %{real_name}.jar java_cup.jar
ln -s %{real_name}-runtime.jar java_cup-runtime.jar
popd

mkdir -p %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE1} %{buildroot}%{_bindir}/%{real_name}

%files
%doc changelog.txt license.txt
%attr(0755,root,root) %{_bindir}/%{real_name}
%{_javadir}/*

%changelog
* Thu Mar 24 2022 Cameron Baird <cameronbaird@microsoft.com> - 0.11-31
- Update to version 0.11b, published 20210814
- Clean up old/deprecated patches 
- separate into bootstrap and non-bootstrap specs
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.11-30
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 19 2020 Joe Schmitt <joschmit@microsoft.com> - 0.11-29.7
- Provide bootstrap version of this package.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 0.11-29.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Turn on bootstrap mode.

* Fri Feb  1 2019 Fridrich Strba <fstrba@suse.com>
- BuildIgnore xml-commons-apis xml-commons-resolver xalan-j2
  and xerces-j2 in order to solve build cycle
* Fri Sep 15 2017 fstrba@suse.com
- Do not depend on java-gcj-compat
- Fix build with jdk9: specify source and target 1.6
* Thu Aug 29 2013 mvyskocil@suse.com
- Add conflicts for each variant
- Sync .changes
- Drop weird jpackage-prepare script and use standard pre_checkin.sh
* Fri Aug 23 2013 mvyskocil@suse.com
- Disable build of javadoc
  * drop java-cup-javadoc.patch
* Fri Jan 25 2013 coolo@suse.com
- sync licenses
* Mon Jun  4 2012 cfarrell@suse.com
- license update: HPND
  SPDX syntax
* Mon Nov  8 2010 mvyskocil@suse.cz
- Build ignore xml-comons-jax-1.3-apis
* Mon May 11 2009 mvyskocil@suse.cz
- Fixed bnc#501635: Added a lincense file
* Tue May  5 2009 mvyskocil@suse.cz
- Build using gcj (for proper bootstrap of openjdk)
* Wed Apr 29 2009 mvyskocil@suse.cz
- Initial packaging of java-cup-bootstrap 0.11 in SUSE (from jpp5)
