Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:          msv
Version:       2013.6.1
Release:       18%{?dist}
Summary:       Multi-Schema Validator
License:       BSD and ASL 1.1
URL:           http://msv.java.net/

# To generate tarball from upstream source control:
# $ ./create-tarball
Source0:       %{name}-%{version}-clean.tar.gz

Source2:       http://www.apache.org/licenses/LICENSE-2.0.txt
Source3:       create-tarball.sh

# Use CatalogResolver from xml-commons-resolver package
Patch1:        %{name}-Use-CatalogResolver-class-from-xml-commons-resolver.patch

BuildRequires:  maven-local
BuildRequires:  mvn(isorelax:isorelax)
BuildRequires:  mvn(jdom:jdom)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.java:jvnet-parent:pom:)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(relaxngDatatype:relaxngDatatype)
BuildRequires:  mvn(xerces:xercesImpl)
BuildRequires:  mvn(xml-resolver:xml-resolver)

BuildArch:     noarch

Obsoletes:     %{name}-relames < %{version}-%{release}

%description
The Sun Multi-Schema XML Validator (MSV) is a Java technology tool to validate
XML documents against several kinds of XML schemata. It supports RELAX NG,
RELAX Namespace, RELAX Core, TREX, XML DTDs, and a subset of XML Schema Part 1.
This latest (version 1.2) release includes several bug fixes and adds better
conformance to RELAX NG/W3C XML standards and JAXP masquerading.

%package       msv
Summary:       Multi-Schema Validator Core
# src/com/sun/msv/reader/xmlschema/DOMLSInputImpl.java is under ASL 2.0
# msv/src/com/sun/msv/writer/ContentHandlerAdaptor.java is partially under Public Domain
License:       BSD and ASL 1.1 and ASL 2.0 and Public Domain
# Explicit javapackages-tools requires since scripts use
# /usr/share/java-utils/java-functions
Requires:      javapackages-tools

%description   msv
%{summary}.

%package       rngconv
Summary:       Multi-Schema Validator RNG Converter
# Explicit javapackages-tools requires since scripts use
# /usr/share/java-utils/java-functions
Requires:      javapackages-tools

%description   rngconv
%{summary}.

%package       xmlgen
Summary:       Multi-Schema Validator Generator
# Explicit javapackages-tools requires since scripts use
# /usr/share/java-utils/java-functions
Requires:      javapackages-tools

%description   xmlgen
%{summary}.

%package       xsdlib
Summary:       Multi-Schema Validator XML Schema Library

%description   xsdlib
%{summary}.

%package       javadoc
Summary:       API documentation for Multi-Schema Validator
License:       BSD and ASL 1.1 and ASL 2.0 and Public Domain

%description   javadoc
%{summary}.

%package       manual
Summary:       Manual for Multi-Schema Validator
License:       BSD

%description   manual
%{summary}.

%package       demo
Summary:       Samples for Multi-Schema Validator
License:       BSD
Requires:      msv-msv
Requires:      msv-xsdlib

%description   demo
%{summary}.

%prep
%setup -q

# We don't have this plugin
%pom_remove_plugin :buildnumber-maven-plugin

# javadoc generation fails due to strict doclint in JDK 8
%pom_remove_plugin :maven-javadoc-plugin

# Needed becuase of patch3
%pom_add_dep xml-resolver:xml-resolver

# ASL 2.0 license text
cp %{SOURCE2} Apache-LICENSE-2.0.txt

# Delete anything pre-compiled
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;
find -name '*.zip' -exec rm -f '{}' \;

# Test sources in default package break BND
rm -f testharness/src/*.java

# Delete class-path entries from manifests
for m in $(find . -name MANIFEST.MF) ; do
  sed --in-place -e '/^[Cc]lass-[Pp]ath:/d' $m
done

# Apply patches
%patch1 -p1

# Fix isorelax groupId
%pom_xpath_replace "pom:dependency[pom:groupId[text()='com.sun.xml.bind.jaxb']]/pom:groupId" "<groupId>isorelax</groupId>"
%pom_xpath_replace "pom:dependency[pom:groupId[text()='com.sun.xml.bind.jaxb']]/pom:groupId" "<groupId>isorelax</groupId>" msv

# Change encoding of non utf-8 files
for m in $(find . -name copyright.txt) ; do
  iconv -f iso-8859-1 -t utf-8 < $m > $m.utf8
  mv $m.utf8 $m
done

%mvn_file ":%{name}-core" %{name}-core %{name}-%{name}
%mvn_file ":%{name}-rngconverter" %{name}-rngconverter %{name}-rngconv
%mvn_file ":%{name}-generator" %{name}-generator %{name}-xmlgen
%mvn_file ":xsdlib" xsdlib %{name}-xsdlib

%mvn_alias ":xsdlib" "com.sun.msv.datatype.xsd:xsdlib"

%mvn_package ":*::{tests,javadoc,sources}:" __noinstall
%mvn_package ":%{name}{,-testharness}::{}:" __noinstall
%mvn_package ":%{name}{,-core}::{}:" %{name}-msv

%build
%mvn_build -s

%install
%mvn_install

# Manuals
install -d -m 755 %{buildroot}%{_docdir}/%{name}/msv
install -m 644 msv/doc/*.html     %{buildroot}%{_docdir}/%{name}/msv
install -m 644 msv/doc/*.gif      %{buildroot}%{_docdir}/%{name}/msv
install -m 644 msv/doc/README.txt %{buildroot}%{_docdir}/%{name}/msv

install -d -m 755 %{buildroot}%{_docdir}/%{name}/rngconverter
install -m 644 rngconverter/README.txt %{buildroot}%{_docdir}/%{name}/rngconverter

install -d -m 755 %{buildroot}%{_docdir}/%{name}/generator
install -m 644 generator/*.html     %{buildroot}%{_docdir}/%{name}/generator
install -m 644 generator/README.txt %{buildroot}%{_docdir}/%{name}/generator

install -d -m 755 %{buildroot}%{_docdir}/%{name}/xsdlib
install -m 644 xsdlib/*.html     %{buildroot}%{_docdir}/%{name}/xsdlib
install -m 644 xsdlib/README.txt %{buildroot}%{_docdir}/%{name}/xsdlib

# Examples
install -d -m 755 %{buildroot}%{_datadir}/%{name}/msv
cp -pr msv/examples/* %{buildroot}%{_datadir}/%{name}/msv
install -d -m 755 %{buildroot}%{_datadir}/%{name}/xsdlib
cp -pr xsdlib/examples/* %{buildroot}%{_datadir}/%{name}/xsdlib

# Scripts
%jpackage_script com.sun.msv.driver.textui.Driver "" "" msv-msv:msv-xsdlib:relaxngDatatype:isorelax msv true
%jpackage_script com.sun.msv.generator.Driver "" "" msv-xmlgen:msv-msv:msv-xsdlib:relaxngDatatype:isorelax:xerces-j2 xmlgen true
%jpackage_script com.sun.msv.writer.relaxng.Driver "" "" msv-rngconv:msv-msv:msv-xsdlib:relaxngDatatype:isorelax:xerces-j2 rngconv true

%files msv -f .mfiles-msv-msv
%{_bindir}/msv
%doc License.txt
%doc msv/doc/Apache-LICENSE-1.1.txt
%doc Apache-LICENSE-2.0.txt

%files rngconv -f .mfiles-msv-rngconverter
%{_bindir}/rngconv
%doc msv/doc/Apache-LICENSE-1.1.txt
%doc License.txt

%files xmlgen -f .mfiles-msv-generator
%{_bindir}/xmlgen
%doc msv/doc/Apache-LICENSE-1.1.txt
%doc License.txt

%files xsdlib -f .mfiles-xsdlib
%doc msv/doc/Apache-LICENSE-1.1.txt
%doc License.txt

%files javadoc -f .mfiles-javadoc
%doc License.txt
%doc msv/doc/Apache-LICENSE-1.1.txt
%doc Apache-LICENSE-2.0.txt

%files manual
%doc %{_docdir}/%{name}
%doc License.txt

%files demo
%{_datadir}/%{name}

%changelog
* Fri Oct 29 2021 Muhammad Falak <mwani@microsft.com> - 2013.6.1-18
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:2013.6.1-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2013.6.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2013.6.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2013.6.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Severin Gehwolf <sgehwolf@redhat.com> - 1:2013.6.1-13
- Add explicit javapackages-tools requirement since scripts use
  java-functions.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2013.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2013.6.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2013.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2013.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:2013.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:2013.6.1-7
- Remove testharness sources from default package
- Resolves: rhbz#1263628

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2013.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:2013.6.1-5
- Remove maven-javadoc-plugin execution

* Sun Sep 14 2014 Gerard Ryan <galileo@fedoraproject.org> - 1:2013.6.1-4
- Don't install testharness jar: pulls in ant
- Fix changelog bogus date warning

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:2013.6.1-3
- Remove unneeded build-requires
- Fix build-requires on jvnet-parent

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2013.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 23 2013 Michal Srb <msrb@redhat.com> - 1:2013.6.1-1
- Update to upstream version 2013.6.1

* Mon Sep 23 2013 Michal Srb <msrb@redhat.com> - 1:2013.5.1-7
- Adapt to current guidelines

* Wed Aug 07 2013 Michal Srb <msrb@redhat.com> - 1:2013.5.1-6
- Unversioned doc dir (Resolves: #993980)
- See: http://fedoraproject.org/wiki/Changes/UnversionedDocdirs

* Tue Aug 06 2013 Michal Srb <msrb@redhat.com> - 1:2013.5.1-5
- Provide net.java.dev.msv:msv (Resolves: #993872)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2013.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Aug 01 2013 Michal Srb <msrb@redhat.com> - 1:2013.5.1-3
- Fix license tag (+Public Domain)
- Add create-tarball.sh to SRPM

* Wed Jul 31 2013 Michal Srb <msrb@redhat.com> - 1:2013.5.1-2
- Do not build module with unclear licensing (relames)
- Replace %%add_to_maven_depmap with %%add_maven_depmap

* Fri Jun 07 2013 Michal Srb <msrb@redhat.com> - 1:2013.5.1-1
- Update to latest upstream version 2013.5.1
- Clean up tarball
- Fix BR/R

* Fri Apr 12 2013 Michal Srb <msrb@redhat.com> - 1:2013.2.3-3
- Fix license tags in javadoc, manual, demo subpackages

* Fri Apr 12 2013 Michal Srb <msrb@redhat.com> - 1:2013.2.3-2
- Fix license tag for msv subpackage
- Remove unneeded patches

* Thu Apr 11 2013 Michal Srb <msrb@redhat.com> - 1:2013.2.3-1
- Update to upstream version 2013.2.3
- Resolves: rhbz#876845
- Fix URL and license tag

* Mon Feb 25 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:2009.1-14
- Add missing BR: maven-local

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2009.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2009.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 6 2012 Alexander Kurtakov <akurtako@redhat.com> 1:2009.1-11
- Drop unneeded BR/R.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2009.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Alexander Kurtakov <akurtako@redhat.com> 1:2009.1-9
- Build with maven 3.
- Adapt to current guidelines.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2009.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov  2 2010 Ville Skyttä <ville.skytta@iki.fi> - 1:2009.1-7
- Add msv, relames, xmlgen, and rngconv command line scripts.

* Thu Oct 28 2010 Alexander Kurtakov <akurtako@redhat.com> 1:2009.1-6
- BR junit4.

* Thu Oct 28 2010 Alexander Kurtakov <akurtako@redhat.com> 1:2009.1-5
- Fix depmaps and install jars required by msv.pom.

* Fri Sep 24 2010 Mat Booth <fedora@matbooth.co.uk> - 1:2009.1-4
- Really require a version of xml-commons-resolver that provides the necessary
  maven pom and depmap.

* Sun Sep 19 2010 Mat Booth <fedora@matbooth.co.uk> - 1:2009.1-3
- Require a version of xml-commons-resolver that provides the necessary maven
  pom and depmap.

* Sun Sep 19 2010 Mat Booth <fedora@matbooth.co.uk> - 1:2009.1-2
- Re-patch build to link to local javadocs.
- Install maven poms/depmap.

* Thu Sep 16 2010 Mat Booth <fedora@matbooth.co.uk> - 1:2009.1-1
- Update to latest tagged release.
- Drop support for GCJ ahead of time compilation.
- Fix RHBZ #627688, RHBZ #631076
- This project now builds with maven instead of ant.
- The new build in this release aggregates javadocs, so now we have one javadoc
  package that obsoletes the many javadoc packages we had before.
- Use new jar names that upstream use, provide the old names.
- Misc other changes for guideline compliance.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2-0.4.20050722.3.4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 08 2009 Karsten Hopp <karsten@redhat.com> 1.2-0.3.20050722.3.4.1
- Specify source and target as 1.4 to make it build

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2-0.3.20050722.3.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.2-0.2.20050722.3.4
- drop repotag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.2-0.2.20050722.3jpp.3
- Autorebuild for GCC 4.3

* Wed Sep 12 2007 Matt Wringe <mwringe@redhat.com> 0:1,2-0.1.20050722.3jpp.3
- Make package build with new gcj. Remove .class files from demo package and
  remove demo exclude from aot-compile-rpm 

* Tue Sep 11 2007 Matt Wringe <mwringe@redhat.com> 0:1.2-0.1.20050722.3jpp.2
- Fix unowned directories
- Change copyright files to utf-8 format
- Change license field to BSD (from BSD-Style)

* Fri Feb 16 2007 Andrew Overholt <overholt@redhat.com> 0:1.2-0.1.20050722.3jpp.1
- Remove postun Requires on jpackage-utils
- Set gcj_support to 1
- Fix groups to shut up rpmlint
- Add versions to the Provides and Obsoletes
- Add patch to take out Class-Path in MANIFEST.MF

* Thu Feb 15 2007 Matt Wringe <mwringe at redhat.com> - 0:1.2-0.1.20050722.3jpp.1.fc7
- Extract sources from a fresh CVS export of the given tag and add extra source
  required to build the package not present in the 20050722 tag anymore
- Add a patch to remove compile time dependency on crimson
- Add a patch to enable compression of jar files
- Add jpackage-utils as a requires for the packages/subpackages

* Mon Feb 12 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.2-0.20050722.3jpp
- Add bootstrap option to build without saxon nor jdom
- Add gcj_support option

* Fri Feb 17 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.2-0.20050722.2jpp
- First JPP 1.7 build

* Wed Aug 17 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.2-0.20050722.1jpp
- First JPP from this code base
