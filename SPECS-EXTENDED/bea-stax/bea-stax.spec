Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package bea-stax
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


%define section         free
%global apiver  1.0.1
Name:           bea-stax
Version:        1.2.0
Release:        40%{?dist}
Summary:        Streaming API for XML
License:        ASL 2.0
Group:          Development/Libraries/Java
URL:            https://stax.codehaus.org/Home
# https://dist.codehaus.org/stax/distributions/stax-src-%{version}.zip
Source0:        %{_distro_sources_url}/stax-src-%{version}.zip
# https://dist.codehaus.org/stax/jars/stax-%{version}.pom
Source1:        stax-%{version}.pom
# https://dist.codehaus.org/stax/jars/stax-api-%{apiver}.pom
Source2:        stax-api-%{apiver}.pom
Source10:       https://apache.org/licenses/LICENSE-2.0.txt
Patch0:         bea-stax-target8.patch
Patch2:         bea-stax-gcj-build.patch
BuildRequires:  ant
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  unzip
BuildRequires:  xml-apis
BuildRequires:  xml-resolver
#!BuildIgnore:  antlr
#!BuildIgnore:  antlr-java
Requires:       %{name}-api = %{version}-%{release}
BuildArch:      noarch

%description
The Streaming API for XML (StAX) is a groundbreaking new Java API for
parsing and writing XML easily and efficiently.

%package api
Summary:        The StAX API
Group:          Development/Libraries/Java

%description api
Streaming API for XML

%{summary}

%prep
%setup -q -c
%patch 0 -b .target15
%patch 2 -b .gcj-build
cp %{SOURCE10} LICENSE

%build
ant all

%install
# jar
install -d -m 0755 %{buildroot}%{_javadir}
install -p -m 0644 build/stax-api-%{apiver}.jar %{buildroot}%{_javadir}/%{name}-api-%{version}.jar
install -p -m 0644 build/stax-%{version}-dev.jar %{buildroot}%{_javadir}/%{name}-ri-%{version}.jar
ln -s %{name}-api-%{version}.jar %{buildroot}%{_javadir}/%{name}-api.jar
ln -s %{name}-ri-%{version}.jar %{buildroot}%{_javadir}/%{name}-ri.jar
# pom
install -d -m 0755 %{buildroot}%{_mavenpomdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/%{name}-ri-%{version}.pom
%add_maven_depmap %{name}-ri-%{version}.pom %{name}-ri-%{version}.jar
install -p -m 0644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/%{name}-api-%{version}.pom
%add_maven_depmap %{name}-api-%{version}.pom %{name}-api-%{version}.jar -f api -a javax.xml.stream:stax-api

%files
%license LICENSE
%{_javadir}/%{name}-ri-%{version}.jar
%{_javadir}/%{name}-ri.jar
%{_mavenpomdir}/%{name}-ri-%{version}.pom
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif

%files api
%license LICENSE
%{_javadir}/%{name}-api-%{version}.jar
%{_javadir}/%{name}-api.jar
%{_mavenpomdir}/%{name}-api-%{version}.pom
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}-api
%else
%{_datadir}/maven-metadata/%{name}-api.xml*
%endif

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.0-40
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.0-39
- Updating source URLs.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.0-38
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 27 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.2.0-37.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Dec 19 2018 Fridrich Strba <fstrba@suse.com>
- Add LICENSE file to packages
* Mon Dec 17 2018 Fridrich Strba <fstrba@suse.com>
- Upgrade to released bea-stax 1.2.0 and bea-stax-api 1.0.1
- Add maven pom files
* Tue May 15 2018 fstrba@suse.com
- Modified patch:
  * bea-stax-target16.patch -> bea-stax-target8.patch
    + Build with source and target 8 to prepare for a possible
    removal of 1.6 compatibility
* Thu Sep 14 2017 fstrba@suse.com
- Don't require java-1_5_0-gcj-compat and build with source and
  target level 1.6
- Removed patch:
  * bea-stax-target15.patch
- Added patch:
  * bea-stax-target16.patch
  - change the source and target levels and fix a problem with
    the encoding of one file
* Sun May 21 2017 tchvatal@suse.com
- Cleanup a bit and remove unused patch bea-stax-gcj43-build.patch
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Thu Aug 22 2013 mvyskocil@suse.com
- don't build javadoc
* Mon Jan  7 2013 mvyskocil@suse.com
- remove xerces-j2-bootstrap depenency (bnc#789163)
* Sat Sep 17 2011 jengelh@medozas.de
- Remove redundant tags/sections from specfile
* Mon Nov  8 2010 mvyskocil@suse.cz
- build ignore xml-commons-jaxp-1.3-apis
* Thu Sep  2 2010 mvyskocil@suse.cz
- ignore antlr(-java) to reduce build cycles
* Thu May 21 2009 mvyskocil@suse.cz
- fixed build under gcj44:
  * splitted uncompatible part of old gcj patch to gcj43 one
* Wed Oct  1 2008 mvyskocil@suse.cz
- rm of BuildRoot on install was removed
- avoid of another openjdk build cycle:
  - added an explicit BuildRequires on: xerces-j2-bootstrap,
  xml-commons-apis-bootstrap, xml-commons-resolver-bootstrap,
  xml-commons-which-bootstrap
  - and BuildIgnore on: xerces-j2, xml-commons, xml-commons-apis,
  xml-commons-resolver, xml-commons-which
* Fri Sep 12 2008 mvyskocil@suse.cz
- target=1.5 -source=1.5
- build with gcj
- remove a dot in summary to prevent of an rpmlint error
* Wed Mar 12 2008 anosek@suse.cz
- fixed Bea-stax contains a Sun proprietary copyright header (bnc#369318)
  - removed problematic file: src/javax/xml/namespace/QName.java
* Mon Mar 10 2008 anosek@suse.cz
- new package needed to build saxon8, initial version 1.2.0,
  based on the JPackage project
