Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           jlex
Version:        1.2.6
Release:        286%{?dist}
Summary:        A Lexical Analyzer Generator for Java
License:        BSD
Group:          Development/Libraries
URL:            http://www.cs.princeton.edu/~appel/modern/java/JLex
Source0:        %{url}/Archive/%{version}/Main.java
Source1:        %{name}-%{version}.build.xml
Source2:        %{url}/Archive/%{version}/manual.html
Source3:        %{url}/Archive/%{version}/sample.lex
Patch0:         %{name}-%{version}.static.patch

BuildRequires: ant
BuildRequires: java-devel
BuildRequires: jpackage-utils

Requires:      java
Requires:      jpackage-utils

BuildArch:     noarch

%description
JLex is a Lexical Analyzer Generator for Java.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -c -T
cp %{SOURCE0} .
cp %{SOURCE2} .
cp %{SOURCE3} .
%patch 0
cp %{SOURCE1} build.xml

%build
ant

%install
# jar
install -pD -T dist/lib/%{name}.jar \
  %{buildroot}%{_javadir}/%{name}.jar

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}.jar
%doc manual.html sample.lex

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

%changelog
* Mon Feb 24 2025 Sumit Jena <v-sumitjena@microsoft.com> - 1.2.6-286
- Build fix for 1.2.6
- License verified

* Tue Apr 12 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.6-285
- Adding missing BR on 'javapackages-tools'.

* Fri Dec 10 2021 Thomas Crain <thcrain@microsoft.com> - 1.2.6-284
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
