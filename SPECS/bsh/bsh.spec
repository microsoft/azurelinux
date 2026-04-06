# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Copyright (c) 2000-2007, JPackage Project
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

Name:           bsh
Version:        2.1.0
Release:        17%{?dist}
Epoch:          0
Summary:        Lightweight Scripting for Java
URL:            https://beanshell.github.io/
# bundled asm is BSD
# bsf/src/bsh/util/BeanShellBSFEngine.java is public-domain
License:        Apache-2.0 AND BSD-3-Clause AND LicenseRef-Fedora-Public-Domain

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
# Remove bundled jars which cannot be easily verified for licensing
# Remove code marked as SUN PROPRIETARY/CONFIDENTAIL
Source2:        generate-tarball.sh

# compatibility with Java 11:
# - set javac / javadoc source and target values to 1.8
Patch0:         0000-source-target-1.8.patch
# - remove references to invisible symbols and methods
Patch1:         0001-java-11-compatibility.patch

BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires:  ant-openjdk25 
BuildRequires:  bsf
BuildRequires:  glassfish-servlet-api
BuildRequires:  javacc
BuildRequires:  javapackages-local-openjdk25
BuildRequires:  junit

Requires:       bsf
Requires:       java-25-headless
Requires:       jline2

# Explicit javapackages-tools requires since scripts use
# /usr/share/java-utils/java-functions
Requires:       javapackages-tools

Provides:       %{name}-utils = %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-utils < 0:2.0
Obsoletes:      %{name}-demo < 0:2.0

# bsh uses small subset of modified (shaded) classes from ancient version of
# objecweb-asm under asm directory
Provides:       bundled(objectweb-asm) = 1.3.6

%description
BeanShell is a small, free, embeddable, Java source interpreter with
object scripting language features, written in Java. BeanShell
executes standard Java statements and expressions, in addition to
obvious scripting commands and syntax. BeanShell supports scripted
objects as simple method closures like those in Perl and
JavaScript(tm). You can use BeanShell interactively for Java
experimentation and debugging or as a simple scripting engine for your
applications. In short: BeanShell is a dynamically interpreted Java,
plus some useful stuff. Another way to describe it is to say that in
many ways BeanShell is to Java as Tcl/Tk is to C: BeanShell is
embeddable - You can call BeanShell from your Java applications to
execute Java code dynamically at run-time or to provide scripting
extensibility for your applications. Alternatively, you can call your
Java applications and objects from BeanShell; working with Java
objects and APIs dynamically. Since BeanShell is written in Java and
runs in the same space as your application, you can freely pass
references to "real live" objects into scripts and return them as
results.

%package manual
Summary:        Manual for %{name}

%description manual
Documentation for %{name}.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n beanshell-%{version}
%patch 0 -p1
%patch 1 -p1

sed -i 's,org.apache.xalan.xslt.extensions.Redirect,http://xml.apache.org/xalan/redirect,' docs/manual/xsl/*.xsl

%mvn_alias :bsh bsh:bsh bsh:bsh-bsf org.beanshell:bsh

%mvn_file : %{name}

%build
mkdir lib
build-jar-repository lib bsf javacc junit glassfish-servlet-api

ant test dist

%install
%mvn_artifact pom.xml dist/%{name}-%{version}.jar

%mvn_install -J javadoc

install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -d -m 755 %{buildroot}%{_datadir}/%{name}/webapps
install -m 644 dist/bshservlet.war %{buildroot}%{_datadir}/%{name}/webapps
install -m 644 dist/bshservlet-wbsh.war %{buildroot}%{_datadir}/%{name}/webapps

# scripts
install -d %{buildroot}%{_bindir}

%jpackage_script bsh.Interpreter "\${BSH_DEBUG:+-Ddebug=true}" jline.console.internal.ConsoleRunner %{name}:jline2/jline %{name} true
%jpackage_script bsh.Console "\${BSH_DEBUG:+-Ddebug=true}" "" bsh bsh-console true

echo '#!%{_bindir}/bsh' > %{buildroot}%{_bindir}/bshdoc
cat scripts/bshdoc.bsh >> %{buildroot}%{_bindir}/bshdoc

%files -f .mfiles
%license LICENSE NOTICE
%doc README.md src/Changes.html src/CodeMap.html docs/faq/faq.html

%attr(0755,root,root) %{_bindir}/%{name}*
%{_datadir}/%{name}/

%files manual
%doc docs/manual/html
%doc docs/manual/images/*.jpg
%doc docs/manual/images/*.gif
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Mon Jul 28 2025 jiri vanek <jvanek@redhat.com> - 0:2.1.0-17
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 22 2024 Marian Koncek <mkoncek@redhat.com> - 0:2.1.0-13
- Fix license field

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 0:2.1.0-12
- Rebuilt for java-21-openjdk as system jdk

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 0:2.1.0-6
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 0:2.1.0-5
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec  2 2021 Hans de Goede <hdegoede@redhat.com> - 0:2.1.0-3
- Fix building with Java 17

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 01 2021 Fabio Valentini <decathorpe@gmail.com> - 0:2.1.0-1
- Update to version 2.1.0.

* Wed Jan 27 2021 Tomas Popela <tpopela@redhat.com> - 0:2.0-22.b6
- Don't build the desktop support on RHEL 8+ as ImageMagick isn't available there.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0-21.b6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 Jerry James <loganjerry@gmail.com> - 0:2.0-20.b6
- Change jline Requires to jline2

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0-19.b6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Fabio Valentini <decathorpe@gmail.com> - 0:2.0-18.b6
- Make adjustments for Java 11 compatibility.

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 0:2.0-17.b6
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0-16.b6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0-15.b6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0-14.b6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 03 2018 Michael Simacek <msimacek@redhat.com> - 0:2.0-13.b6
- Remove proprietary files from tarball

* Mon Jul 30 2018 Severin Gehwolf <sgehwolf@redhat.com> - 0:2.0-12.b6
- Add requirement on javapackages-tools for script's usage of
  java-functions.

* Mon Jul 30 2018 Michael Simacek <msimacek@redhat.com> - 0:2.0-11.b6
- Repack the tarball without binaries

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0-10.b6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0-9.b6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Sep 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.0-8.b6
- Properly conditionalize build-requires

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.0-7.b6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Michael Simacek <msimacek@redhat.com> - 0:2.0-6.b6
- Add conditional for desktop file

* Fri Mar  3 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.0-5.b6
- Install desktop icon to pixmaps instead of icons

* Fri Mar  3 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.0-4.b6
- Fix directory ownership

* Tue Feb 07 2017 Michael Simacek <msimacek@redhat.com> - 0:2.0-3.b6
- Build against glassfish-servlet-api

* Thu Nov 24 2016 Michael Simacek <msimacek@redhat.com> - 0:2.0-2.b6
- Install into expected location

* Thu Nov 24 2016 Michael Simacek <msimacek@redhat.com> - 0:2.0-1.b6
- Update to upstream version 2.0.b6

* Wed Oct 12 2016 Ville Skyttä <ville.skytta@iki.fi> - 0:1.3.0-36
- Switch to jline 2.x in -utils
- Mark License.txt as %%license

* Thu Jul 21 2016 Michael Simacek <msimacek@redhat.com> - 0:1.3.0-35
- Replace perl usage with sed

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.3.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Nov  5 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3.0-32
- Remove workaround for RPM bug #646523

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3.0-30
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.3.0-29
- Use Requires: java-headless rebuild (#1067528)

* Wed Oct 30 2013 Michal Srb <msrb@redhat.com> - 0:1.3.0-28
- Switch to jline1 (Resolves rhbz#1023018)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3.0-26
- Use %%add_maven_depmap instead of legacy macros
- Install versionless javadocs
- Remove old Obsoletes
- Update and format descriptions
- Install license file with manual and javadoc packages
- Fix Requires and BuildRequires on java
- Fix calls to %%jpackage_script

* Wed Jul 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3.0-26
- Remove arch-specific conditionals
- Remove group tags
- Remove Requires on jpackage-utils
- Remove Requires on coreutils
- Generate custom scripts with %%jpackage_script
- Install versionless JARs only
- Install POM files to %%{_mavenpomdir}

* Thu Jun 06 2013 Michal Srb <msrb@redhat.com> - 0:1.3.0-25
- Enable tests
- Fix BR

* Thu Feb 14 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0:1.3.0-24
- remove vendor tag from desktop file. https://fedorahosted.org/fpc/ticket/247
- clean up spec to follow current guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 David Tardon <dtardon@redhat.com> - 0:1.3.0-22
- Resolves: rhbz#850008 bsh - Should not own /usr/share/maven-fragments
  directory
- Resolves: rhbz#878163 bsh - javadoc subpackage doesn't require
  jpackage-utils
- Resolves: rhbz#878166 bsh: Public Domain not listed in license tag

* Thu Nov  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3.0-21
- Add additional maven depmap

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 25 2010 Ville Skyttä <ville.skytta@iki.fi> - 0:1.3.0-17
- Rename -desktop to -utils, move shell scripts and menu entry to it (#417491).
- Bring icon cache scriptlets up to date with current guidelines.
- Use jline in bsh script for command history support.
- Prefer JRE over SDK when finding JVM to invoke in scripts.
- Build with -source 1.5.

* Thu Nov 25 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.3.0-16
- Fix pom filenames (Resolves rhbz#655791)
- Fix xsl errors when building docs

* Sat Jan 9 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.3.0-15.2
- Drop gcj_support.
- Fix rpmlint warnings.

* Mon Sep 21 2009 Permaine Cheung <pcheung@redhat.com> 0:1.3.0-15.1
- Do not build manual and faq for ppc64 or s390x as the style task is disabled

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.3.0-13
- drop repotag
- fix license tag

* Mon Mar 10 2008 Permaine Cheung <pcheung@redhat.com> 0:1.3.0-12jpp.3
- Fix bugzilla 436675. Separate menu entry into desktop subpackage.

* Thu Mar 06 2008 Permaine Cheung <pcheung@redhat.com> 0:1.3.0-12jpp.2
- Fix bugzilla 417491. Thanks Ville Skytta for the patch.
- Add menu entry and startup script for bsh desktop.
- Ensure scriptlets exit with zero exit status.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.3.0-12jpp.1
- Autorebuild for GCC 4.3

* Mon Jan 21 2008 Permaine Cheung <pcheung@redhat.com> 0:1.3.0-11jpp.1
- Merge with upstream

* Thu Jul 12 2007 Ralph Apel <r.apel at r-apel.de> 0:1.3.0-11jpp
- Fix aot build
- Add pom and depmap frags
- Restore all jars
- Add webapps

* Fri Mar 16 2007 Permaine Cheung <pcheung@redhat.com> 0:1.3.0-10jpp.1
- Merge with upstream
- Removed unapplied patch and moved buildroot removal from prep to install,
  and other rpmlint cleanup

* Mon Mar 12 2007 Karsten Hopp <karsten@redhat.com> 1.3.0-9jpp.2
- add buildrequirement ant-trax for documentation

* Fri Aug 04 2006 Deepak Bhole <dbhole@redhat.com> 0:1.3.0-9jpp.1
- Added missing requirements

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> 0:1.3.0-8jpp_3fc
- Rebuilt

* Fri Jul 21 2006 Deepak Bhole <dbhole@redhat.com> 0:1.3.0-8jpp_2fc
- Removing vendor and distribution tags.

* Thu Jul 20 2006 Deepak Bhole <dbhole@redhat.com> 0:1.3.0-8jpp_1fc
- Add conditional native compilation.

* Thu May 04 2006 Ralph Apel <r.apel at r-apel.de> 0:1.3.0-7jpp
- First JPP-1.7 release

* Fri Aug 20 2004 Ralph Apel <r.apel at r-apel.de> 0:1.3.0-6jpp
- Build with ant-1.6.2

* Mon Jan 26 2004 David Walluck <david@anti-microsoft.org> 0:1.3.0-5jpp
- really drop readline patch

* Sun Jan 25 2004 David Walluck <david@anti-microsoft.org> 0:1.3.0-4jpp
- drop readline patch

* Wed Jan 21 2004 David Walluck <david@anti-microsoft.org> 0:1.3.0-3jpp
- port libreadline-java patch to new bsh

* Tue Jan 20 2004 David Walluck <david@anti-microsoft.org> 0:1.3.0-2jpp
- add Distribution tag

* Tue Jan 20 2004 David Walluck <david@anti-microsoft.org> 0:1.3.0-1jpp
- 1.3.0
- remove bsf patch (fixed upstream)
- add epoch to demo package Requires

* Sat Apr 12 2003 David Walluck <david@anti-microsoft.org> 0:1.2-0.b8.4jpp
- fix strange permissions

* Fri Apr 11 2003 David Walluck <david@anti-microsoft.org> 0:1.2-0.b8.3jpp
- rebuild for JPackage 1.5
- add bsf patch

* Sat Feb 01 2003 David Walluck <david@anti-microsoft.org> 1.2-0.b8.2jpp
- remove servlet dependency (if anyone wants to add this as a separate
  package and do the tomcat integration, be my guest)

* Thu Jan 23 2003 David Walluck <david@anti-microsoft.org> 1.2-0.b8.1jpp
- rename to bsh
- add manual
- add Changes.html to %%doc
- add bsh and bshdoc scripts
- add %%dir %%{_datadir}/%%{name} to main package
- correct test interpreter and make bsh files executable

* Mon Jan 21 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.01-3jpp
- really section macro

* Sun Jan 20 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.01-2jpp
- additional sources in individual archives
- versioned dir for javadoc
- no dependencies for javadoc package
- stricter dependency for demo package
- section macro

* Tue Dec 18 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.01-1jpp
- first JPackage release
