%bcond_with bootstrap

# Copyright (c) 2000-2009, JPackage Project
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

Summary:        A library for instantiating Java objects
Name:           objenesis
Version:        3.4
Release:        4%{?dist}
License:        Apache-2.0
URL:            http://objenesis.org/
BuildArch:      noarch
#ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/easymock/%{name}/archive/%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter)
%endif
# xmvn-builddep misses this:
%if %{without bootstrap}
BuildRequires:  mvn(org.apache:apache-jar-resource-bundle)
%endif

%description
Objenesis is a small Java library that serves one purpose: to instantiate 
a new object of a particular class.
Java supports dynamic instantiation of classes using Class.newInstance(); 
however, this only works if the class has an appropriate constructor. There 
are many times when a class cannot be instantiated this way, such as when 
the class contains constructors that require arguments, that have side effects,
and/or that throw exceptions. As a result, it is common to see restrictions 
in libraries stating that classes must require a default constructor. 
Objenesis aims to overcome these restrictions by bypassing the constructor 
on object instantiation. Needing to instantiate an object without calling 
the constructor is a fairly specialized task, however there are certain cases 
when this is useful:
* Serialization, Remoting and Persistence - Objects need to be instantiated 
  and restored to a specific state, without invoking code.
* Proxies, AOP Libraries and Mock Objects - Classes can be sub-classed without 
  needing to worry about the super() constructor.
* Container Frameworks - Objects can be dynamically instantiated in 
  non-standard ways.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

%pom_remove_dep :junit-bom

# Enable generation of pom.properties (rhbz#1017850)
%pom_xpath_remove pom:addMavenDescriptor

%pom_remove_plugin :maven-timestamp-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin -r :maven-shade-plugin
%pom_remove_plugin -r org.sonatype.plugins:nexus-staging-maven-plugin
%pom_xpath_remove "pom:dependency[pom:scope='test']" tck

%pom_xpath_remove pom:build/pom:extensions

%pom_disable_module module-test

# Missing dependencies
rm tck/src/test/java/org/objenesis/tck/OsgiTest.java

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Wed Jul 24 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4-4
- Install license files in licensedir instead of docdir

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4-2
- Remove dependency on junit-bom

* Tue May 07 2024 Chris Kelley <ckelley@redhat.com> - 3.4-1
- Update to version 3.4
- Resolves: rhbz#2279242

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 3.3-9
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 3.3-8
- bump of release for for java-21-openjdk as system jdk

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3-4
- Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 08 2022 Marian Koncek <mkoncek@redhat.com> - 3.3-1
- Update to upstream version 3.3

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 3.1-9
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-6
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 3.1-3
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jun 25 2020 Alexander Kurtakov <akurtako@redhat.com> 3.1-2
- Fix build with Java 11.

* Mon May 04 2020 Jiri Vanek <jvanek@fedoraproject.org> - 3.1-1
- bumped  to 3.1
- disabled javadoc generation. It requires maven pomming beyond my skills

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.1-2
- Mass rebuild for javapackages-tools 201902

* Thu Oct 17 2019 Marian Koncek <mkoncek@redhat.com> - 3.1-1
- Update to upstream version 3.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 15 2019 Marian Koncek <mkoncek@redhat.com> - 3.0.1-1
- Update to upstream version 3.0.1

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-3
- Mass rebuild for javapackages-tools 201901

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 18 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.6-1
- Update to upstream version 2.6

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.1-6
- Add missing BR on apache-resource-bundles

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 2.1-5
- Remove wagon extension

* Fri Jun 03 2016 Michael Simacek <msimacek@redhat.com> - 2.1-4
- Fix build with current maven-jar-plugin

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 30 2015 Michal Srb <msrb@redhat.com> - 2.1-1
- Update to 2.1

* Tue Feb  3 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-18
- Add missing BR on maven-wagon-ssh-external
- Resolves: rhbz#1106608

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-16
- Enable generation of pom.properties
- Resolves: rhbz#1017850

* Sun Sep 08 2013 Mat Booth <fedora@matbooth.co.uk> - 1.2-15
- Update for latest guidelines, rhbz #992389

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.2-12
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Guido Grazioli <guido.grazioli@gmail.com> 1.2-10
- Update to current Java packaging guidelines
- Remove maven-eclipse-plugin BR

* Mon Feb 20 2012 Jiri Vanek <jvanek@redhat.com> 1.2-9
- Added patch2 - JRockitInstantntiatorCharacters.patch to fix unmappable characters
- Added build requires  apache-resource-bundles and  maven-remote-resources-plugin

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 09 2011 Guido Grazioli <guido.grazioli@gmail.com> 1.2-7
- Improve project description

* Thu Feb 24 2011 Guido Grazioli <guido.grazioli@gmail.com> 1.2-6
- Build with mvn-rpmbuild
- Fix License
- Comment on skipped tests

* Fri Feb 04 2011 Guido Grazioli <guido.grazioli@gmail.com> 1.2-5
- Build with maven 3

* Sun Jan 23 2011 Guido Grazioli <guido.grazioli@gmail.com> 1.2-4
- Drop buildroot and %%clean section
- Drop use of maven2-settings.xml and jpp-depmap.xml
- Install unversioned jars
- Clean up of needed patch and mvn-jpp execution

* Tue Jan 18 2011 Guido Grazioli <guido.grazioli@gmail.com> 1.2-3
- Fix build in rawhide

* Sat Dec 04 2010 Guido Grazioli <guido.grazioli@gmail.com> 1.2-2
- Fix build in rawhide
- Update to new Java Packaging Guidelines

* Mon May 10 2010 Guido Grazioli <guido.grazioli@gmail.com> 1.2-1
- Update to 1.2

* Thu May 06 2010 Guido Grazioli <guido.grazioli@gmail.com> 1.0-1
- Import from JPackage 

* Fri Feb 27 2009 Ralph Apel <r.apel at r-apel.de> 0:1.0-2.jpp5
- BR xpp3-minimal and fix depmap accordingly
- Disown poms and fragments dirs

* Wed Jun 18 2008 Ralph Apel <r.apel at r-apel.de> 0:1.0-1.jpp5
- First release
