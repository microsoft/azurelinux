Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package jlex
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


%define section		free
Name:           jlex
Version:        1.2.6
Release:        285%{?dist}
Summary:        A Lexical Analyzer Generator for Java
License:        MIT
Group:          Development/Libraries/Java
Url:            http://www.cs.princeton.edu/~appel/modern/java/JLex/
Source0:        http://www.cs.princeton.edu/~appel/modern/java/JLex/Archive/1.2.5/Main.java
Source1:        %{name}-%{version}.build.xml
Patch0:         %{name}-%{version}.static.patch
BuildRequires:  ant
BuildRequires:  java-devel
BuildRequires:  javapackages-tools
BuildRequires:  xml-commons-apis-bootstrap
#!BuildIgnore:  xerces-j2
#!BuildIgnore:  xml-commons
#!BuildIgnore:  xml-commons-apis
#!BuildIgnore:  xml-commons-jaxp-1.3-apis
#!BuildIgnore:  xml-commons-resolver
#!BuildIgnore:  xml-commons-resolver12
BuildArch:      noarch

%description
JLex is a lexical analyzer generator for Java.

%prep
%setup -q -c -T
cp %{SOURCE0} .
%patch0
cp %{SOURCE1} build.xml

%build
unset CLASSPATH
ant -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6

%install
# jar
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 dist/lib/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

%files
%license Main.java
%{_javadir}/*

%changelog
* Tue Apr 12 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.6-285
- Adding missing BR on 'javapackages-tools'.

* Fri Dec 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.2.6-284
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.6-283
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Oct  3 2017 fstrba@suse.com
- Build with source and target level 1.6 and do not require
  java-gcj-compat
- Clean spec file
* Fri Aug 23 2013 mvyskocil@suse.com
- don't build javadoc
- use 1.5 source/target
* Mon Nov  8 2010 mvyskocil@suse.cz
- build ignore xml-commons-jaxp-1.3-apis
* Sun Jul 27 2008 coolo@suse.de
- avoid more packages creating bootstrap problems
* Fri Jul 25 2008 coolo@suse.de
- build with gcj to avoid bootstrap problems with openjdk
* Mon Sep 25 2006 skh@suse.de
- don't use icecream
- use source="1.4" and target="1.4" for build with java 1.5
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Jul 28 2005 jsmeix@suse.de
- Adjustments in the spec file.
* Mon Jul 18 2005 jsmeix@suse.de
- Current version 1.2.6 from JPackage.org
* Thu Sep  2 2004 skh@suse.de
- Initial package created with version 1.2.6 (JPackage 1.5)
