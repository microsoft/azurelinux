Vendor:         Microsoft Corporation
Distribution:   Mariner
%global oname jaxb-api
Name:          glassfish-jaxb-api
Version:       2.2.12
Release:       15%{?dist}
Summary:       Java Architecture for XML Binding
License:       CDDL-1.1 or GPLv2 with exception
URL:           http://jaxb.java.net/
# jaxb api and impl have different version
# svn export https://svn.java.net/svn/jaxb~version2/tags/jaxb-2_2_6/tools/lib/redist/jaxb-api-src.zip

Source0:       http://repo1.maven.org/maven2/javax/xml/bind/%{oname}/%{version}/%{oname}-%{version}-b141001.1542-sources.jar
Source1:       http://repo1.maven.org/maven2/javax/xml/bind/%{oname}/%{version}/%{oname}-%{version}-b141001.1542.pom


BuildRequires:  java
BuildRequires:  maven-local
BuildRequires:  mvn(net.java:jvnet-parent:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)

BuildArch:     noarch

# The Fedora Packaging Committee granted openjdk a bundling exception to carry JAXP and
# JAX-WS (glassfish doesn't need one, since it is the upstream for these files).
# Reference: https://fedorahosted.org/fpc/ticket/292

%description
Glassfish - JAXB (JSR 222) API.

%package javadoc
Summary:       Javadoc for %{oname}
Requires:      %{name} = %{version}-%{release} 

%description javadoc
Glassfish - JAXB (JSR 222) API.

This package contains javadoc for %{name}.

%prep
%setup -T -q -c

# fixing incomplete source directory structure
mkdir -p src/main/java

(
  cd src/main/java
  unzip -qq %{SOURCE0}
  rm -rf META-INF
)

cp -p %{SOURCE1} pom.xml

%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin
%pom_remove_plugin org.glassfish.copyright:glassfish-copyright-maven-plugin
%pom_remove_plugin org.glassfish.build:gfnexus-maven-plugin
%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :maven-gpg-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :cobertura-maven-plugin

%pom_xpath_set "pom:instructions/pom:Import-Package" "javax.activation;resolution:=optional,*"

sed -i 's|<location>${basedir}/offline-javadoc</location>|<location>%{_javadocdir}/java</location>|' pom.xml

%build
%mvn_file :%{oname} %{oname}
%mvn_build

%install
%mvn_install

%files -f .mfiles

%files javadoc -f .mfiles-javadoc

%changelog
* Wed Dec 09 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.2.12-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Change java-javadoc build requirement to equivalent parent package java.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Mat Booth <mat.booth@redhat.com> - 2.2.12-12
- Update license tag

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 11 2018 Mat Booth <mat.booth@redhat.com> - 2.2.12-10
- Fix OSGi metadata

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jul 23 2016 Mat Booth <mat.booth@redhat.com> - 2.2.12-5
- Regenerate BRs

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 20 2015 gil cattaneo <puntogil@libero.it> 2.2.12-2
- Update to 2.2.12-b141001.1542

* Tue Jan 20 2015 gil cattaneo <puntogil@libero.it> 2.2.12-1
- Update to 2.2.12

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.9-5
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 gil cattaneo <puntogil@libero.it> 2.2.9-3
- switch to XMvn
- minor changes to adapt to current guideline

* Mon Jun 10 2013 Orion Poplawski <orion@cora.nwra.com> 2.2.9-2
- Add requires jvnet-parent

* Thu May 02 2013 gil cattaneo <puntogil@libero.it> 2.2.9-1
- update to 2.2.9

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.7-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Aug 04 2012 gil cattaneo <puntogil@libero.it> 2.2.7-1
- update to 2.2.7

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 gil cattaneo <puntogil@libero.it> 2.2.6-1
- update to 2.2.6
- remove Build/Requires: bea-stax-api

* Tue Jan 24 2012 gil cattaneo <puntogil@libero.it> 2.2.3-2
- revert to 2.2.3 (stable release)
- fix License field

* Fri Jul 22 2011 gil cattaneo <puntogil@libero.it> 2.2.3-1
- initial rpm
