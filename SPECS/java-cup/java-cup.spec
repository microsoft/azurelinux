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

%define cvs_version    11a
%define real_name      java-cup

Summary:        LALR Parser Generator in Java
Name:           java-cup
Version:        0.11
Release:        33%{?dist}
License:        HPND
Group:          Development/Libraries/Java
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Url:            https://www2.cs.tum.edu/projects/cup/
# TODO the version of our 11a source is no longer published
Source0:        %{_distro_sources_url}/develop.tar.bz2
Source1:        java-cup-generated-files.tar.bz2
Source2:        java-cup.license
# From          https://www2.cs.tum.edu/projects/cup/
Patch1:         java-cup-no-classpath-in-manifest.patch
Patch2:         java-cup-no-cup-no-jflex.patch
Patch3:         java-cup-classpath.patch
# Missing symbolFactory initialization in lr_parser, causes sinjdoc to crash
Patch4:         java-cup-lr_parser-constructor.patch
BuildRequires:  ant
BuildRequires:  git
BuildRequires:  java-cup-bootstrap
BuildRequires:  java-devel
BuildRequires:  jflex-bootstrap
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  javapackages-tools
BuildRequires:  xml-commons-apis-bootstrap
BuildRequires:  xml-commons-resolver-bootstrap
#!BuildIgnore:  xalan-j2
#!BuildIgnore:  xerces-j2
#!BuildIgnore:  xml-commons-apis
#!BuildIgnore:  xml-commons-resolver
# Compatibility 
Obsoletes:      java_cup < %{version}-%{release}
Obsoletes:      java-cup < %{version}-%{release}
Provides:       java_cup = %{version}-%{release}
Provides:       java-cup = %{version}-%{release}
Conflicts:      java-cup-bootstrap
BuildArch:      noarch

%description
java-cup is a LALR Parser Generator in Java. With v0.11, you can: 
* use CUP in an Ant-Target
* start CUP by a simple command like java -jar java-cup.jar
   myGrammar.cup
* use generic parametrized classes (since Java 1.5) as datatypes for
   non terminals and terminals
* have Your own symbol classes

%package manual
Summary:        LALR Parser Generator in Java
Group:          Development/Libraries/Java

%description manual
java-cup is a LALR Parser Generator in Java. With v0.11, you can: 
* use CUP in an Ant-Target
* start CUP by a simple command like java -jar java-cup.jar
   myGrammar.cup
* use generic parametrized classes (since Java 1.5) as datatypes for
   non
* terminals and terminals
* have Your own symbol classes

%prep
%setup -q -n develop
%patch 1 -p1
%patch 3 -p1
# remove all binary files
find -name "*.class" -delete
find -name "*.jar" -delete
%patch 4 -p1
perl -pi -e 's/1\.2/1.8/g' build.xml
mkdir -p classes dist
cp %{SOURCE2} license.txt

%build
export CLASSPATH=$(build-classpath java-cup jflex)
export OPT_JAR_LIST=:
ant

%install
# jar
mkdir -p %{buildroot}%{_javadir}
cp -a dist/%{real_name}-%{cvs_version}.jar %{buildroot}%{_javadir}/%{real_name}-%{version}.jar
cp -a dist/%{real_name}-%{cvs_version}-runtime.jar %{buildroot}%{_javadir}/%{real_name}-runtime-%{version}.jar

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
%license license.txt
%doc changelog.txt
%attr(0755,root,root) %{_bindir}/%{real_name}
%{_javadir}/*

%files manual
%doc manual.html

%changelog
* Tue Feb 27 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.11-33
- rebuild with msopenjdk-17

* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.11-33
- Updating naming for 3.0 version of Azure Linux.

* Fri Apr 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.11-32
- Fixing source URL.

* Thu Mar 24 2022 Cameron Baird <cameronbaird@microsoft.com> - 0.11-31
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
