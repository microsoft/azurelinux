Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package isorelax
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


%define	cvsversion	20041111
Name:           isorelax
Version:        0.1
Release:        31%{?dist}
Summary:        Public interfaces useful for applications to support RELAX Core
License:        MIT
Group:          Development/Libraries/Java
URL:            https://iso-relax.sourceforge.net/
Source0:        https://sourceforge.net/projects/iso-relax/files/package/2004_11_11/%{name}.%{cvsversion}.zip
Source1:        %{name}-build.xml
Source2:        isorelax-maven-project.xml
Source3:        isorelax-maven-project.xsd
Source4:        https://repo2.maven.org/maven2/%{name}/%{name}/20030108/%{name}-20030108.pom
Patch0:         isorelax-java5-compatibility.patch
BuildRequires:  ant
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  unzip
BuildRequires:  xerces-j2
BuildRequires:  xml-apis
Requires:       xerces-j2
Requires:       xml-apis
Obsoletes:      isorelax-bootstrap
Provides:       isorelax-bootstrap
Obsoletes:      %{name}-javadoc
BuildArch:      noarch

%description
The ISO RELAX project is started to host the public interfaces useful
for applications to support RELAX Core. But nowadays some of the stuff
we have is schema language neutral.

%prep
%setup -q -T -c
unzip -q %{SOURCE0}
mkdir src
(cd src; unzip -q ../src.zip)
rm -f src.zip
cp %{SOURCE1} build.xml
mkdir test
cp %{SOURCE2} test
cp %{SOURCE3} test
chmod -R go=u-w *
find . -name "*.jar" -exec rm -f {} \;
rm -rf src/jp/gr/xml/relax/swift
%patch 0 -b .sav0

%build
export CLASSPATH=$(build-classpath \
xerces-j2 \
xml-apis \
)
ant -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 \
    -Dbuild.sysclasspath=only release

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 %{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -m 644 %{SOURCE4} %{buildroot}%{_mavenpomdir}/%{name}-%{version}.pom
%add_maven_depmap %{name}-%{version}.pom %{name}-%{version}.jar

%files
%license COPYING.txt
%{_javadir}/*
%{_mavenpomdir}/*
%if %{defined _maven_repository}
%{_mavendepmapfragdir}/%{name}
%else
%{_datadir}/maven-metadata/%{name}.xml*
%endif

%changelog
* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1-31
- Updating source URLs.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1-30
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 0.1-29.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Dec 18 2018 Fridrich Strba <fstrba@suse.com>
- Add maven pom file
- Build against the generic xml-apis provider
* Fri Sep  8 2017 fstrba@suse.com
- Specify java target and source version to 1.6 in order to allow
  building with jdk9
* Fri Jun  9 2017 tchvatal@suse.com
- Drop javadoc to build with gcj and low in the buildphase
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Sat Mar  2 2013 coolo@suse.com
- update license to new format
* Mon Sep 15 2008 mvyskocil@suse.cz
- -target=1.5 -source=1.5
* Wed Aug 20 2008 mvyskocil@suse.cz
- Initial packaging of version 0.1 (based on jpp1.7)
