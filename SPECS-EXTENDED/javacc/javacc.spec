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

# Build in bootstrap mode on new architectures
%bcond bootstrap 0

%global giturl  https://github.com/javacc/javacc

Name:           javacc
Version:        7.0.13
Release:        7%{?dist}
Epoch:          0
Summary:        A parser/scanner generator for java

# BSD-3-Clause: the project as a whole
# BSD-2-Clause:
# - src/main/javacc/ConditionParser.jj
# - src/main/java/org/javacc/parser/OutputFile.java
# - src/main/java/org/javacc/utils/OutputFileGenerator.java
License:        BSD-3-Clause AND BSD-2-Clause
URL:            https://javacc.org/
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/%{name}-%{version}.tar.gz
# Fix javadoc errors in the JavaCharStream template
# https://github.com/javacc/javacc/pull/257
Patch:          0001-Fix-javadoc-errors-in-JavaCharStream.template.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  javapackages-local
BuildRequires:  ant
#BuildRequires:  javacc
%endif

# Explicit javapackages-tools requires since scripts use
# /usr/share/java-utils/java-functions
Requires:       javapackages-tools

BuildArch:      noarch
#ExclusiveArch:  %{java_arches} noarch

%description
Java Compiler Compiler (JavaCC) is the most popular parser generator for use
with Java applications. A parser generator is a tool that reads a grammar
specification and converts it to a Java program that can recognize matches to
the grammar. In addition to the parser generator itself, JavaCC provides other
standard capabilities related to parser generation such as tree building (via
a tool called JJTree included with JavaCC), actions, debugging, etc.

%package manual
# BSD-3-Clause: the project license
# GPL-2.0-or-later: docs/grammars/AsnParser.jj
# LGPL-2.1-or-later: docs/grammars/{ChemNumber.jj,RTFParser.jj}
# AFL-2.0 OR BSD-3-Clause: docs/grammars/EcmaScript.jjt
# ISC: docs/grammars/JSONParser.jjt
License:        BSD-3-Clause AND GPL-2.0-or-later AND LGPL-2.1-or-later AND (AFL-2.0 OR BSD-3-Clause) AND ISC
Summary:        Manual for %{name}

%description manual
Manual for %{name}.

%package demo
Summary:        Examples for %{name}
Requires:       %{name} = %{version}-%{release}

%description demo
Examples for %{name}.

%javadoc_package

%prep
%autosetup -n %{name}-%{name}-%{version} -p1

# Remove binary information in the source tar
find . -name "*.jar" -delete
find examples -name .gitignore -delete

fixtimestamp() {
  touch -r $1.orig $1
  rm $1.orig
}

mv examples/JJTreeExamples/cpp/README examples/JJTreeExamples/cpp/README.orig
iconv -f WINDOWS-1252 -t UTF-8 examples/JJTreeExamples/cpp/README.orig > \
  examples/JJTreeExamples/cpp/README
fixtimestamp examples/JJTreeExamples/cpp/README

sed -i.orig 's/\r//' examples/JJTreeExamples/cpp/eg3.jjt
fixtimestamp examples/JJTreeExamples/cpp/eg3.jjt

%build
%if %{with bootstrap}
cp %{_prefix}/lib/javapackages-bootstrap/javacc.jar bootstrap/javacc.jar
%else
build-jar-repository -p bootstrap javacc
%endif

# There is maven pom which doesn't really work for building. The tests don't
# work either (even when using bundled jars).
%ant jar javadoc -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8

# The pom dependencies are also wrong
%mvn_artifact --skip-dependencies pom.xml target/javacc.jar

%install
%mvn_file : %{name}

%mvn_install -J target/javadoc

%jpackage_script javacc '' '' javacc javacc true
ln -s javacc %{buildroot}%{_bindir}/javacc.sh
%jpackage_script jjdoc '' '' javacc jjdoc true
%jpackage_script jjtree '' '' javacc jjtree true

%files -f .mfiles
%license LICENSE
%doc README.md
%{_bindir}/javacc
%{_bindir}/javacc.sh
%{_bindir}/jjdoc
%{_bindir}/jjtree

%files manual
%doc docs/*

%files demo
%doc examples

%changelog
* Tue Jul 30 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:7.0.13-7
- Adjust bootstrap build for javapackages-bootstrap update

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 0:7.0.13-5
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 0:7.0.13-4
- bump of release for for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Nov 17 2023 Jerry James <loganjerry@gmail.com> - 0:7.0.13-1
- Update to 7.0.13
- Drop upstreamed duplicated @Deprecated annotations patch

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:7.0.12-4
- Rebuild

* Sat Aug 26 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:7.0.12-3
- Bootstrap using javapackages-bootstrap

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Apr  1 2023 Jerry James <loganjerry@gmail.com> - 0:7.0.12-1
- Update to 7.0.12
- Convert License tag to SPDX
- Add bootstrap build mode
- Add patch to fix javadoc errors in the JavaCharStream template
- Add patch to remove duplicate @Deprecated annotations

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 0:7.0.4-12
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 0:7.0.4-11
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Mat Booth <mat.booth@redhat.com> - 0:7.0.4-6
- Force generation of 1.8 level bytecode to avoid breaking dependent packages
  that require Java 8

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 0:7.0.4-5
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 26 2018 Marian Koncek <mkoncek@redhat.com> - 0:7.0.4-1
- Update to upstream version 7.0.4
- Resolves: rhbz#1593262

* Tue Jul 31 2018 Severin Gehwolf <sgehwolf@redhat.com> - 0:7.0.2-6
- Add requirement on javapackages-tools for scripts using
  java-functions.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Michael Simacek <msimacek@redhat.com> - 0:7.0.2-1
- Update to upstream version 7.0.2

* Mon Jan 02 2017 Michael Simacek <msimacek@redhat.com> - 0:7.0.1-1
- Update to upstream version 7.0.1

* Tue Sep 06 2016 Michael Simacek <msimacek@redhat.com> - 0:6.1.3-1
- Update to upstream version 6.1.3
- Use new upstream location
- Generate scripts with jpackage_script

* Tue Aug 23 2016 Michael Simacek <msimacek@redhat.com> - 0:6.1.2-1
- Update to upstream version 6.1.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:5.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:5.0-11
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:5.0-10
- Use Requires: java-headless rebuild (#1067528)

* Tue Jul 30 2013 Michal Srb <msrb@redhat.com> - 0:5.0-9
- Generate javadoc
- Drop group tag

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Jaromir Capik <jcapik@redhat.com> 0:5.0-6
- Fixing #835786 - javacc: Invalid upstream URL
- Minor spec file changes according to the latest guidelines

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:5.0-3
- Fix examples line endings.

* Fri Jun 4 2010 Alexander Kurtakov <akurtako@redhat.com> 0:5.0-2
- Apply changes requested in review bug (rhbz#225940).

* Thu Feb 11 2010 Alexander Kurtakov <akurtako@redhat.com> 0:5.0-1
- Update to upstream 5.0 release.

* Tue Nov 24 2009 Alexander Kurtakov <akurtako@redhat.com> 0:4.1-0.6
- Use standard permissions and fix unowned directories.

* Tue Nov 24 2009 Alexander Kurtakov <akurtako@redhat.com> 0:4.1-0.5
- Fix rpmlint warnings.
- Drop gcj support.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 03 2008 Matt Wringe <mwringe@redhat.com> - 0:4.1-0.2
- Update to remove packaged jars in source tar
- Build with bootstrap jar so that required java source 
  files get generated

* Wed Oct 22 2008 Jerry James <loganjerry@gmail.com> - 0:4.1-0.1
- Update to 4.1
- Also ship the jjrun script
- Own the appropriate gcj directory
- Minor spec file changes to comply with latest Fedora guidelines
- Include the top-level index.html file in the manual

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:4.0-4.5
- drop repotag

* Fri Feb 22 2008 Matt Wringe <mwringe at redhat.com> - 0:4.0-4jpp.4
- Rename javacc script file to javacc.sh as this confuses the makefile

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:4.0-4jpp.3
- Autorebuild for GCC 4.3

* Thu Aug 10 2006 Matt Wringe <mwringe at redhat.com> - 0:4.0-3jpp.3
- Rebuilt with new naming convention

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:4.0-3jpp_2fc
- Rebuilt

* Tue Jul 18 2006 Matthew Wringe <mwringe at redhat.com> - 0:4.0-3jpp_1fc
- Merged with upstream version
- Changed directory locations to rpm macros
- Added conditional native compiling

* Thu Apr 20 2006 Fernando Nasser <fnasser@redhat.com> - 0:4.0-2jpp
- First JPP 1.7 build

* Fri Mar 31 2006 Sebastiano Vigna <vigna at acm.org> - 0:4.0-1jpp
- Updated to 4.0

* Mon Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:3.2-2jpp
- Rebuild with ant-1.6.2

* Fri Jan 30 2004 Sebastiano Vigna <vigna at acm.org> 0:3.2-1jpp
- First JPackage version
