Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:          xmlstreambuffer
Version:       1.5.4
Release:       12%{?dist}
Summary:       XML Stream Buffer
License:       CDDL or GPLv2 with exceptions
Url:           https://javaee.github.io/metro-xmlstreambuffer/
# svn export https://svn.java.net/svn/xmlstreambuffer~svn/tags/streambuffer-1.5.4/ xmlstreambuffer-1.5.4
# find xmlstreambuffer-1.5.4/ -name '*.class' -delete
# find xmlstreambuffer-1.5.4/ -name '*.jar' -delete
# find xmlstreambuffer-1.5.4/ -name '*.zip' -delete
# tar cJf xmlstreambuffer-1.5.4.tar.xz xmlstreambuffer-1.5.4
# Source0:     https://github.com/javaee/metro-xmlstreambuffer/archive/refs/tags/streambuffer-1.5.4.tar.gz
Source0:       %{name}-%{version}.tar.xz
# wget -O glassfish-LICENSE.txt https://svn.java.net/svn/glassfish~svn/tags/legal-1.1/src/main/resources/META-INF/LICENSE.txt
# xmlstreambuffer package don't include the license file
Source1:       glassfish-LICENSE.txt

BuildRequires: jvnet-parent
BuildRequires: maven-local
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-plugin-bundle
BuildRequires: maven-surefire-provider-junit
BuildRequires: stax-ex >= 1.7.1
# test deps
BuildRequires: junit
BuildRequires: woodstox-core

BuildArch:     noarch

%description
A stream buffer is a stream-based representation of an XML
info-set in Java. Stream buffers are designed to: provide
very efficient stream-based memory representations of XML
info-sets; and be created and processed using any Java-based
XML API.
Conceptually a stream buffer is similar to the representation
used in the Xerces deferred DOM implementation, with the crucial
difference that a stream buffer does not store hierarchical
information like parent and sibling information. The deferred
DOM implementation reduces memory usage when large XML documents
are parsed but only a subset of the document needs to be processed.
(Note that using deferred DOM will be more expensive than
non-deferred DOM in terms of memory and processing if all
the document is traversed.)
Stream buffers may be used as an efficient alternative to DOM where:
* most or all of an XML info-set will eventually get traversed; and/or
* targeted access to certain parts of an XML info-set are required
 and need to be efficiently processed using stream-based APIs like
 SAX or StAX.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

%pom_remove_plugin :maven-deploy-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :glassfish-copyright-maven-plugin
%pom_remove_plugin :cobertura-maven-plugin
%pom_remove_plugin :buildnumber-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin

%pom_xpath_set "pom:dependency[pom:groupId = 'org.codehaus.woodstox']/pom:artifactId" woodstox-core-asl

cp -p %{SOURCE1} LICENSE.txt

rm -r test/com/sun/xml/stream/buffer/stax/InscopeNamespaceTest.java

%mvn_file :streambuffer %{name}

%build

%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.4-12
- Removing license file modification.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 20 2016 gil cattaneo <puntogil@libero.it> 1.5.4-4
- add missing build requires: maven-plugin-bundle

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 04 2015 gil cattaneo <puntogil@libero.it> 1.5.4-1
- update to 1.5.4
- introduce license macro

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.5.1-4
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 29 2013 gil cattaneo <puntogil@libero.it> 1.5.1-2
- switch to XMvn, minor changes to adapt to current guideline

* Tue Oct 30 2012 gil cattaneo <puntogil@libero.it> 1.5.1-1
- update to 1.5.1

* Wed Oct 03 2012 gil cattaneo <puntogil@libero.it> 1.5-1
- update to 1.5

* Sat Mar 31 2012 gil cattaneo <puntogil@libero.it> 1.4-1
- initial rpm
