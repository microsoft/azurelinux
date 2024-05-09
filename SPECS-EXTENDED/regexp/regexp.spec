Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package regexp
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
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


%define full_name       jakarta-%{name}
%define section         free
Name:           regexp
Version:        1.5
Release:        23%{?dist}
Summary:        Simple regular expressions API
License:        Apache-2.0
Group:          Development/Libraries/Java
Url:            https://jakarta.apache.org/%{name}/
Source0:        https://www.apache.org/dist/jakarta/regexp/jakarta-regexp-%{version}.tar.gz
Source1:        regexp-%{version}.pom
BuildRequires:  ant
BuildRequires:  ant >= 1.6
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  javapackages-tools
BuildRequires:  xml-commons-apis-bootstrap
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#!BuildIgnore:  xml-commons-apis xml-commons-resolver xml-commons xerces-j2
#!BuildIgnore:  xml-commons-jaxp-1.3-apis
BuildArch:      noarch

%description
Regexp is a 100% Pure Java Regular Expression package that was
graciously donated to the Apache Software Foundation by Jonathan Locke.
He originally wrote this software back in 1996 and it has stood up
quite well to the test of time. It includes complete Javadoc
documentation as well as a simple Applet for visual debugging and
testing suite for compatibility.

%prep
%setup -q -n %{full_name}-%{version}
# remove all binary libs
find . -type f -name "*.jar" | xargs -t rm

%build
export OPT_JAR_LIST=:
export CLASSPATH=
mkdir lib
ant -Djakarta-site2.dir=. -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6  jar

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 build/*.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
[ -d docs/api ] && rm -rf docs/api
# pom
mkdir -p %{buildroot}%{_mavenpomdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar -a %{full_name}:%{full_name}

%files
%defattr(0644,root,root,0755)
%doc LICENSE
%{_javadir}/*.jar
%{_mavenpomdir}/*
%{_datadir}/maven-metadata/%{name}.xml*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5-23
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.5-22.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Thu Nov 15 2018 Fridrich Strba <fstrba@suse.com>
- Add jakarta-regexp:jakarta-regexp alias to the maven artifact
* Tue Oct  3 2017 fstrba@suse.com
- Don't depend on java-gcj-compat, since it is bound to go
- Specify java source and target level 1.6
* Fri May 19 2017 dziolkowski@suse.com
- New build dependency: javapackages-local
- spec cleaned using spec-cleaner
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Fri Aug 23 2013 mvyskocil@suse.com
- disable javadoc build
* Mon Nov  8 2010 mvyskocil@suse.cz
- merge with regexp-1.5-1.jpp5.src.rpm
- update to 1.5 bugfix and optimization release
  https://jakarta.apache.org/regexp/changes.html
- ignore also jaxp-1.3-apis
* Sun Jul 27 2008 coolo@suse.de
- build with gcj to avoid bootstrapping problems with openjdk
* Wed Sep 27 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Fri Jul 29 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Mon Jul 18 2005 jsmeix@suse.de
- Current version 1.3 from JPackage.org
* Thu Sep 16 2004 skh@suse.de
- Fix prerequires of javadoc subpackage
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 1.3 (JPackage 1.5)
