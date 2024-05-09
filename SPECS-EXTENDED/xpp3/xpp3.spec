Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package xpp3
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
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


Name:           xpp3
Version:        1.1.4c
Release:        6%{?dist}
Summary:        XML Pull Parser
License:        Apache-1.1
Group:          Development/Libraries/Java
Url:            https://www.extreme.indiana.edu/xgws/xsoap/xpp/mxp1/index.html
Source0:        https://www.extreme.indiana.edu/dist/java-repository/xpp3/distributions/xpp3-%{version}_src.tgz
Source1:        https://central.maven.org/maven2/xpp3/xpp3/%{version}/xpp3-%{version}.pom
Source2:        https://central.maven.org/maven2/xpp3/xpp3_min/%{version}/xpp3_min-%{version}.pom
Source3:        https://central.maven.org/maven2/xpp3/xpp3_xpath/%{version}/xpp3_xpath-%{version}.pom
Source4:        %{name}-%{version}-OSGI-MANIFEST.MF
Patch0:         xpp3-sourcetarget.patch
BuildRequires:  ant >= 1.6
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  javapackages-tools
BuildRequires:  junit
BuildRequires:  perl
BuildRequires:  xml-commons-apis
Requires:       java >= 1.4.2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch

%description
Xml Pull Parser 3rd Edition (XPP3) MXP1 is a new XmlPull parsing engine
that is based on ideas from XPP and in particular XPP2 but completely
revised and rewritten to take best advantage of latest JIT JVMs such as
Hotspot in JDK 1.4.

%package minimal
Summary:        XML Pull Parser
Group:          Development/Libraries/Java

%description minimal
Xml Pull Parser 3rd Edition (XPP3) MXP1 is a new XmlPull parsing engine
that is based on ideas from XPP and in particular XPP2 but completely
revised and rewritten to take best advantage of latest JIT JVMs such as
Hotspot in JDK 1.4.

%package javadoc
Summary:        XML Pull Parser
Group:          Development/Libraries/Java

%description javadoc
Xml Pull Parser 3rd Edition (XPP3) MXP1 is a new XmlPull parsing engine
that is based on ideas from XPP and in particular XPP2 but completely
revised and rewritten to take best advantage of latest JIT JVMs such as
Hotspot in JDK 1.4.

%prep
%setup -q
%patch 0 -p1
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
# "src/java/addons_tests" does not exist
sed -i 's|depends="junit_main,junit_addons"|depends="junit_main"|' build.xml

%build
export CLASSPATH=$(build-classpath xml-commons-apis junit)
ant xpp3 junit apidoc

# Add OSGi metadata
jar ufm build/%{name}-%{version}.jar %{SOURCE4}

%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -p build/%{name}-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}-%{version}.jar
cp -p build/%{name}_min-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}-minimal-%{version}.jar
cp -p build/%{name}_xpath-%{version}.jar \
  %{buildroot}%{_javadir}/%{name}-xpath-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr doc/api/* %{buildroot}%{_javadocdir}/%{name}
rm -rf doc/{build.txt,api}

# Install pom file
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/%{name}.pom
install -p -m 644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/%{name}-minimal.pom
install -p -m 644 %{SOURCE3} %{buildroot}%{_mavenpomdir}/%{name}-xpath.pom
%add_maven_depmap %{name}.pom %{name}.jar
%add_maven_depmap %{name}-minimal.pom %{name}-minimal.jar -f minimal
%add_maven_depmap %{name}-xpath.pom %{name}-xpath.jar -f xpath

%files
%defattr(0644,root,root,0755)
%doc README.html LICENSE.txt doc/*
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}-xpath.jar
%{_javadir}/%{name}-xpath-%{version}.jar
%{_mavenpomdir}/%{name}.pom
%{_mavenpomdir}/%{name}-xpath.pom
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%{_mavendepmapfragdir}/%{name}-xpath
%else
%{_datadir}/maven-metadata/%{name}.xml*
%{_datadir}/maven-metadata/%{name}-xpath.xml*
%endif

%files minimal
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-minimal.jar
%{_javadir}/%{name}-minimal-%{version}.jar
%{_mavenpomdir}/%{name}-minimal.pom
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}-minimal
%else
%{_datadir}/maven-metadata/%{name}-minimal.xml*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.4c-6
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.1.4c-5.9
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Fri Nov 23 2018 Fridrich Strba <fstrba@suse.com>
- Add OSGi manifest to xpp3-1.1.4c.jar
* Fri Oct 19 2018 Fridrich Strba <fstrba@suse.com>
- Install maven pom files and generate mvn(...) provides
* Mon Sep 11 2017 fstrba@suse.com
- Added patch:
  * xpp3-sourcetarget.patch
    + Specify java soirce and target level 1.6 in order to allow
    building with jdk9
    + Specify encoding ISO-8859-1 for files with non-ASCII
    characters
* Fri May 19 2017 tchvatal@suse.com
- Do not require javapackage-tools
* Thu Dec  4 2014 p.drouand@gmail.com
- Remove redundant %%clean section
* Thu Dec  4 2014 p.drouand@gmail.com
- Update to version 1.1.4c
  + The changes file doesn't contain an entry for 1.1.4c release
* Fri Jul 11 2014 tchvatal@suse.com
- Do not version java docdir.
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Tue May 12 2009 mvyskocil@suse.cz
- Initial SUSE packaging of xpp3 1.1.3.8 (from jpp 5.0)
