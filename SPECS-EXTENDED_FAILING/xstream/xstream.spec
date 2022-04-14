Vendor:         Microsoft Corporation
Distribution:   Mariner
# Copyright statement from JPackage this file is derived from:

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

%bcond_with dom4j
%bcond_with hibernate
%bcond_with jdom
%bcond_with jdom2
%bcond_with joda
%bcond_with kxml
%bcond_with stax
%bcond_with woodstox

Name:           xstream
Version:        1.4.14
Release:        2%{?dist}
Summary:        Java XML serialization library
License:        BSD
URL:            http://x-stream.github.io/
BuildArch:      noarch

Source0:        https://repo1.maven.org/maven2/com/thoughtworks/%{name}/%{name}-distribution/%{version}/%{name}-distribution-%{version}-src.zip

# patch pom.xml to target Java 8 / 1.8
Patch0:         xstream-java-8-target.patch

BuildRequires:  maven-local
BuildRequires:  mvn(cglib:cglib)
BuildRequires:  mvn(com.sun.activation:jakarta.activation)
BuildRequires:  mvn(javax.xml.bind:jaxb-api)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(xpp3:xpp3)
BuildRequires:  mvn(xpp3:xpp3_min)


%if %{with dom4j}
BuildRequires:  mvn(dom4j:dom4j)
%endif

%if %{with hibernate}
BuildRequires:  mvn(javassist:javassist)
BuildRequires:  mvn(org.codehaus.jettison:jettison)
BuildRequires:  mvn(org.hibernate:hibernate-core)
BuildRequires:  mvn(org.hibernate:hibernate-envers)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
BuildRequires:  mvn(xom:xom)
%endif

%if %{with jdom}
BuildRequires:  mvn(org.jdom:jdom)
%endif

%if %{with jdom2}
BuildRequires:  mvn(org.jdom:jdom2)
%endif

%if %{with joda}
BuildRequires:  mvn(joda-time:joda-time)
%endif

%if %{with kxml}
BuildRequires:  mvn(net.sf.kxml:kxml2-min)
%endif

%if %{with stax}
BuildRequires:  mvn(stax:stax)
BuildRequires:  mvn(stax:stax-api)
%endif

%if %{with woodstox}
BuildRequires:  mvn(org.codehaus.woodstox:woodstox-core-asl)
%endif


%description
XStream is a simple library to serialize objects to XML
and back again. A high level facade is supplied that
simplifies common use cases. Custom objects can be serialized
without need for specifying mappings. Speed and low memory
footprint are a crucial part of the design, making it suitable
for large object graphs or systems with high message throughput.
No information is duplicated that can be obtained via reflection.
This results in XML that is easier to read for humans and more
compact than native Java serialization. XStream serializes internal
fields, including private and final. Supports non-public and inner
classes. Classes are not required to have default constructor.
Duplicate references encountered in the object-model will be
maintained. Supports circular references. By implementing an
interface, XStream can serialize directly to/from any tree
structure (not just XML). Strategies can be registered allowing
customization of how particular types are represented as XML.
When an exception occurs due to malformed XML, detailed diagnostics
are provided to help isolate and fix the problem.


%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
%{name} API documentation.

%if %{with hibernate}
%package        hibernate
Summary:        hibernate module for %{name}
Requires:       %{name} = %{version}-%{release}

%description    hibernate
hibernate module for %{name}.
%endif

%package        benchmark
Summary:        benchmark module for %{name}
Requires:       %{name} = %{version}-%{release}

%description    benchmark
benchmark module for %{name}.

%package parent
Summary:        Parent POM for %{name}
Requires:       %{name} = %{version}-%{release}

%description parent
Parent POM for %{name}.


%prep
%setup -qn %{name}-%{version}
find . -name "*.class" -print -delete
find . -name "*.jar" -print -delete

%patch0 -p1

# Require org.codehaus.xsite:xsite-maven-plugin
%pom_disable_module xstream-distribution

# missing artifacts:
#  org.openjdk.jmh:jmh-core:jar:1.11.1
#  org.openjdk.jmh:jmh-generator-annprocess:jar:1.11.1
%pom_disable_module xstream-jmh

# Unwanted
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-dependency-plugin
%pom_remove_plugin :maven-eclipse-plugin
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :xsite-maven-plugin

%pom_xpath_set "pom:dependency[pom:groupId = 'org.codehaus.woodstox' ]/pom:artifactId" woodstox-core-asl
%pom_xpath_set "pom:dependency[pom:groupId = 'org.codehaus.woodstox' ]/pom:artifactId" woodstox-core-asl xstream
%pom_xpath_set "pom:dependency[pom:groupId = 'cglib' ]/pom:artifactId" cglib
%pom_xpath_set "pom:dependency[pom:groupId = 'cglib' ]/pom:artifactId" cglib xstream
# Replace old xmlpull dependency with xpp3
%pom_change_dep :xmlpull xpp3:xpp3:1.1.4c xstream
# Require unavailable proxytoys:proxytoys
%pom_remove_plugin :maven-dependency-plugin xstream

%pom_remove_plugin :maven-javadoc-plugin xstream

%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:groupId = 'cglib' ]/pom:artifactId" cglib xstream-hibernate
%pom_xpath_inject "pom:project/pom:dependencies/pom:dependency[pom:groupId = 'junit' ]" "<scope>test</scope>" xstream-hibernate
%pom_remove_plugin :maven-dependency-plugin xstream-hibernate
%pom_remove_plugin :maven-javadoc-plugin xstream-hibernate

%pom_xpath_inject "pom:project/pom:dependencies/pom:dependency[pom:groupId = 'junit' ]" "<scope>test</scope>" xstream-benchmark
%pom_remove_plugin :maven-javadoc-plugin xstream-benchmark

# Fix dep on activation
%pom_change_dep javax.activation:activation com.sun.activation:jakarta.activation . xstream

%if %{without dom4j}
%pom_remove_dep -r dom4j:dom4j
rm xstream/src/java/com/thoughtworks/xstream/io/xml/Dom4JDriver.java
rm xstream/src/java/com/thoughtworks/xstream/io/xml/Dom4JReader.java
rm xstream/src/java/com/thoughtworks/xstream/io/xml/Dom4JWriter.java
rm xstream/src/java/com/thoughtworks/xstream/io/xml/Dom4JXmlWriter.java
rm xstream-benchmark/src/java/com/thoughtworks/xstream/tools/benchmark/products/XStreamDom4J.java
%endif

%if %{without hibernate}
# Don't build hibernate module
%pom_disable_module xstream-hibernate
# Disable support for some lesser used XML backends
%pom_remove_dep -r xom:xom
%pom_remove_dep -r org.codehaus.jettison:jettison
rm xstream/src/java/com/thoughtworks/xstream/io/xml/Xom*
rm xstream/src/java/com/thoughtworks/xstream/io/json/Jettison*
rm xstream-benchmark/src/java/com/thoughtworks/xstream/tools/benchmark/products/XStreamXom.java
%endif

%if %{without jdom}
%pom_remove_dep -r org.jdom:jdom
rm xstream/src/java/com/thoughtworks/xstream/io/xml/JDomDriver.java
rm xstream/src/java/com/thoughtworks/xstream/io/xml/JDomReader.java
rm xstream/src/java/com/thoughtworks/xstream/io/xml/JDomWriter.java
rm xstream-benchmark/src/java/com/thoughtworks/xstream/tools/benchmark/products/XStreamJDom.java
%endif

%if %{without jdom2}
%pom_remove_dep -r org.jdom:jdom2
rm xstream/src/java/com/thoughtworks/xstream/io/xml/JDom2Driver.java
rm xstream/src/java/com/thoughtworks/xstream/io/xml/JDom2Reader.java
rm xstream/src/java/com/thoughtworks/xstream/io/xml/JDom2Writer.java
%endif

%if %{without joda}
%pom_remove_dep -r joda-time:joda-time
rm xstream/src/java/com/thoughtworks/xstream/core/util/ISO8601JodaTimeConverter.java
rm xstream/src/test/com/thoughtworks/acceptance/JodaTimeTypesTest.java
%endif

%if %{without kxml}
%pom_remove_dep -r net.sf.kxml:kxml2-min
rm xstream/src/java/com/thoughtworks/xstream/io/xml/KXml2DomDriver.java
rm xstream/src/java/com/thoughtworks/xstream/io/xml/KXml2Driver.java
rm xstream-benchmark/src/java/com/thoughtworks/xstream/tools/benchmark/products/XStreamKXml2.java
rm xstream-benchmark/src/java/com/thoughtworks/xstream/tools/benchmark/products/XStreamKXml2DOM.java
%endif

%if %{without stax}
%pom_remove_dep -r stax:stax
%pom_remove_dep -r stax:stax-api
rm xstream/src/java/com/thoughtworks/xstream/io/xml/BEAStaxDriver.java
rm xstream/src/test/com/thoughtworks/xstream/io/xml/BEAStaxReaderTest.java
rm xstream/src/test/com/thoughtworks/xstream/io/xml/BEAStaxWriterTest.java
rm xstream-benchmark/src/java/com/thoughtworks/xstream/tools/benchmark/products/XStreamBEAStax.java
%endif

%if %{without woodstox}
%pom_remove_dep -r org.codehaus.woodstox:woodstox-core-asl
rm xstream/src/java/com/thoughtworks/xstream/io/xml/WstxDriver.java
rm xstream-benchmark/src/java/com/thoughtworks/xstream/tools/benchmark/products/XStreamWoodstox.java
%endif

%mvn_file :%{name} %{name}/%{name} %{name}
%mvn_file :%{name}-benchmark %{name}/%{name}-benchmark %{name}-benchmark

%mvn_package :%{name}

%build
# test skipped for unavailable test deps (com.megginson.sax:xml-writer)
%mvn_build -f -s

%install
%mvn_install

%files -f .mfiles
%doc README.txt
%license LICENSE.txt

%files parent -f .mfiles-%{name}-parent

%if %{with hibernate}
%files hibernate -f .mfiles-%{name}-hibernate
%endif

%files benchmark -f .mfiles-%{name}-benchmark

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.14-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Tue Nov 17 2020 Ding-Yi Chen <dchen@redhat.com> - 1.4.14-1
- Upstream update to 1.4.14

* Fri Aug 07 2020 Mat Booth <mat.booth@redhat.com> - 1.4.12-6
- Allow building on JDK11

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1.4.12-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jun 17 2020 Fabio Valentini <decathorpe@gmail.com> - 1.4.12-3
- Disable unused optional dom4j, jdom, jdom2, kxml, and woodstox support.

* Mon Jun 08 2020 Fabio Valentini <decathorpe@gmail.com> - 1.4.12-2
- Disable optional support for joda-time by default.

* Mon Apr 27 2020 Fabio Valentini <decathorpe@gmail.com> - 1.4.12-1
- Update to version 1.4.12.
- Disable optional support for BEA Stax by default.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Fabio Valentini <decathorpe@gmail.com> - 1.4.11.1-4
- Use Java version override compatible with both xmvn 3.0.0 and 3.1.0.

* Fri Jul 26 2019 Fabio Valentini <decathorpe@gmail.com> - 1.4.11.1-3
- Disable hibernate support by default.

* Tue Mar 05 2019 Mat Booth <mat.booth@redhat.com> - 1.4.11.1-2
- Allow building with reduced dependency set

* Thu Feb 14 2019 Mat Booth <mat.booth@redhat.com> - 1.4.11.1-1
- Update to latest upstream release

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 12 2017 Michael Simacek <msimacek@redhat.com> - 1.4.9-5
- Backport fix for void deserialization
- Resolves rhbz#1441542
- Update upstream URL

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 1.4.9-4
- Add conditional for hibernate

* Mon Jul 18 2016 Michael Simacek <msimacek@redhat.com> - 1.4.9-3
- Regenerate buildrequires

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.9-2
- Regenerate build-requires

* Wed Mar 30 2016 Michal Srb <msrb@redhat.com> - 1.4.9-1
- Update to 1.4.9
- Resolves: CVE-2016-3674

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.8-3
- Fix dependency on xpp3

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 19 2015 Michal Srb <msrb@redhat.com> - 1.4.8-1
- Update to upstream version 1.4.8

* Mon Nov 10 2014 Michael Simacek <msimacek@redhat.com> - 1.4.7-9
- Change org.json:json dependency scope to test

* Wed Nov  5 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.7-8
- Remove workaround for RPM bug #646523

* Fri Oct 24 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.7-7
- Fix dependencies in parent POM

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.7-6
- Fix build-requires on codehaus-parent

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 07 2014 Michael Simacek <msimacek@redhat.com> - 1.4.7-4
- Split into subpackages

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.7-3
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Michal Srb <msrb@redhat.com> - 1.4.7-2
- Spec file cleanup
- Fix BR
- Build with kxml2 and json

* Mon Feb 10 2014 Michal Srb <msrb@redhat.com> - 1.4.7-1
- Update to latest upstream release 1.4.7

* Thu Jan 02 2014 Michal Srb <msrb@redhat.com> - 1.4.6-1
- Update to upstream release 1.4.6

* Thu Oct 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.5-3
- Rebuild to move arch-independant JARs out of %%_jnidir

* Wed Oct 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.5-2
- Rebuild to regenerate broken POM files
- Related: rhbz#1021484

* Sun Oct 20 2013 Matt Spaulding <mspaulding06@gmail.com> 1.4.5-1
- update to 1.4.5

* Tue Aug 20 2013 gil cattaneo <puntogil@libero.it> 1.4.4-1
- update to 1.4.4
- switch to XMvn

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.1-7
- Update to current packaging guidelines

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3.1-6
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jun 14 2010 Alexander Kurtakov <akurtako@redhat.com> 1.3.1-1
- Update to 1.3.1.
- Install maven pom and depmap.

* Wed Dec 02 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.2.2-4
- Cosmetic fixes

* Fri Nov 27 2009 Lubomir Rintel <lkundrak@v3.sk> - 0:1.2.2-3
- Drop gcj (suggested by Jochen Schmitt), we seem to need OpenJDK anyway
- Fix -javadoc Require
- Drop epoch

* Sun Nov 01 2009 Lubomir Rintel <lkundrak@v3.sk> - 0:1.2.2-2
- Greatly simplify for Fedora
- Disable tests, we don't have all that's required to run them
- Remove maven build

* Fri Jul 20 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.2.2-1jpp
- Upgrade to 1.2.2
- Build with maven2 by default
- Add poms and depmap frags

* Tue May 23 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.1.3-1jpp
- Upgrade to 1.1.3
- Patched to work with bea

* Mon Sep 13 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0.2-2jpp
- Drop saxpath requirement
- Require jaxen >= 0:1.1

* Mon Aug 30 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0.2-1jpp
- Upgrade to 1.0.2
- Delete included binary jars
- Change -Dbuild.sysclasspath "from only" to "first" (DynamicProxyTest)
- Relax some versioned dependencies
- Build with ant-1.6.2

* Fri Aug 06 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0.1-2jpp
- Upgrade to ant-1.6.X

* Tue Jun 01 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0.1-1jpp
- Upgrade to 1.0.1

* Fri Feb 13 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.3-1jpp
- Upgrade to 0.3
- Add manual subpackage

* Mon Jan 19 2004 Ralph Apel <r.apel at r-apel.de> - 0:0.2-1jpp
- First JPackage release
