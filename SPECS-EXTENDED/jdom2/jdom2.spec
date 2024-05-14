Summary:        Java manipulation of XML made easy
Name:           jdom2
Version:        2.0.6
Release:        29%{?dist}
# Sam as the "Saxpath" license but restricts the use of the name "JDOM" instead of "SAXPath".
License:        JDOM
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.jdom.org/
# ./generate-tarball.sh
Source0:        https://github.com/hunterhacker/jdom/archive/JDOM-%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Remove bundled jars that might not have clear licensing
Source4:        generate-tarball.sh
# Use system libraries
# Disable gpg signatures
# Process contrib and junit pom files
Patch0:         0001-Adapt-build.patch
#
# Security patches
# P100 -> ...
#
# CVE-2021-33813
Patch100:       bd3ab78370098491911d7fe9d7a43b97144a234e.patch
Patch101:       dd4f3c2fc7893edd914954c73eb577f925a7d361.patch
Patch102:       07f316957b59d305f04c7bdb26292852bcbc2eb5.patch

BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap

%description
JDOM is a Java-oriented object model which models XML documents.
It provides a Java-centric means of generating and manipulating
XML documents. While JDOM inter-operates well with existing
standards such as the Simple API for XML (SAX) and the Document
Object Model (DOM), it is not an abstraction layer or
enhancement to those APIs. Rather, it seeks to provide a robust,
light-weight means of reading and writing XML data without the
complex and memory-consumptive options that current API
offerings provide.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%autosetup -p1 -n jdom-JDOM-%{version}

sed -i 's/\r//' LICENSE.txt README.txt

# Unable to run coverage: use log4j12 but switch to log4j 2.x
sed -i.coverage "s|coverage, jars|jars|" build.xml

# XPath functionality is not needed
rm -rf core/src/java/org/jdom2/xpath/
sed -i '/import org.jdom2.xpath.XPathFactory/d' core/src/java/org/jdom2/JDOMConstants.java

%build
mkdir lib
%ant -Dversion=%{version} -Dcompile.source=1.7 -Dcompile.target=1.7 -Dj2se.apidoc=%{_javadocdir}/java maven

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 build/package/jdom-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 build/maven/core/%{name}-%{version}.pom %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr build/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE.txt
%doc CHANGES.txt COMMITTERS.txt README.txt TODO.txt

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Fri Apr 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.6-29
- Fixing source URL.

* Tue Feb 22 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.6-28
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.0.6-27
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 02 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.6-25
- Bump Java compiler source/target levels to 1.7

* Thu Oct 14 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.6-24
- Add patches to address DoS security vulnerability
- Resolves: CVE-2021-33813

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.6-22
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 10 2020 Fabio Valentini <decathorpe@gmail.com> - 2.0.6-20
- Drop log4j12 dependency and switch junit module to log4j 1.2 API shim.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 19 2020 Fabio Valentini <decathorpe@gmail.com> - 2.0.6-18
- Set javac source and target to 1.8 to fix Java 11 builds.

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 2.0.6-17
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu May 07 2020 Fabio Valentini <decathorpe@gmail.com> - 2.0.6-16
- Drop optional isorelax verifier support from contrib.

* Mon Apr 20 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.6-15
- Disable contrib module

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.6-14
- Mass rebuild for javapackages-tools 201902

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.6-13
- Mass rebuild for javapackages-tools 201901

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Michael Simacek <msimacek@redhat.com> - 2.0.6-12
- Repack tarball without bundled jars
- The repacked jar contains slightly different source (force push by upstream?)
- Correct license tag

* Tue Jul 17 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.6-11
- Remove unneeded buildrequires

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 31 2017 Michael Simacek <msimacek@redhat.com> - 2.0.6-7
- Avoid hardcoded jar paths

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Apr 14 2016 Mat Booth <mat.booth@redhat.com> - 2.0.6-6
- Add OSGi metadata to main jar
- Fix file listed twice warning

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.6-3
- Remove unneeded BR on cobertura

* Fri Feb 06 2015 gil cattaneo <puntogil@libero.it> 2.0.6-2
- introduce license macro

* Tue Oct 21 2014 gil cattaneo <puntogil@libero.it> 2.0.6-1
- update to 2.0.6 (rhbz#1118627)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.0.5-3
- Use Requires: java-headless rebuild (#1067528)

* Thu Nov 14 2013 gil cattaneo <puntogil@libero.it> 2.0.5-2
- use objectweb-asm3

* Thu Sep 12 2013 gil cattaneo <puntogil@libero.it> 2.0.5-1
- initial rpm
