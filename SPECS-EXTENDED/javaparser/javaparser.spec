Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:          javaparser
Version:       3.3.5
Release:       4%{?dist}
Summary:       Java 1 to 9 Parser and Abstract Syntax Tree for Java
License:       LGPLv3+ or ASL 2.0
URL:           http://javaparser.org
Source0:       https://github.com/javaparser/javaparser/archive/%{name}-parent-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(biz.aQute.bnd:bnd-maven-plugin)
BuildRequires:  mvn(net.java.dev.javacc:javacc)
BuildRequires:  mvn(org.codehaus.mojo:javacc-maven-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)

BuildArch:     noarch

%description
This package contains a Java 1 to 9 Parser with AST generation and
visitor support. The AST records the source code structure, javadoc
and comments. It is also possible to change the AST nodes or create new
ones to modify the source code.

%package javadoc
Summary: Javadoc for %{name}

%description javadoc
This package contains API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-parent-%{version}

sed -i 's/\r//' readme.md

# Remove plugins unnecessary for RPM builds
%pom_remove_plugin :animal-sniffer-maven-plugin javaparser-core
%pom_remove_plugin :maven-enforcer-plugin javaparser-core
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :coveralls-maven-plugin
%pom_remove_plugin :jacoco-maven-plugin . javaparser-testing

# Compatibility alias
%mvn_alias :javaparser-core com.google.code.javaparser:javaparser

# Fix javacc plugin name
sed -i \
  -e 's/ph-javacc-maven-plugin/javacc-maven-plugin/' \
  -e 's/com.helger.maven/org.codehaus.mojo/' \
  javaparser-core/pom.xml

# Missing plugin
%pom_remove_plugin :templating-maven-plugin javaparser-core

# Missing dep on jbehave for testing
%pom_disable_module javaparser-testing

# Only need to ship the core module
%mvn_package ":javaparser-core-generators" __noinstall
%mvn_package ":javaparser-metamodel-generator" __noinstall
%mvn_package ":javaparser-testing" __noinstall

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc readme.md changelog.md
%license LICENSE LICENSE.APACHE LICENSE.GPL LICENSE.LGPL

%files javadoc -f .mfiles-javadoc
%license LICENSE LICENSE.APACHE LICENSE.GPL LICENSE.LGPL

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.3.5-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 13 2019 Mat Booth <mat.booth@redhat.com> - 3.3.5-1
- Update to javaparser 3.3.5 for Java 9 support
- Correct license field to dual license: LGPLv3+ OR ASL 2.0

* Wed Feb 13 2019 Mat Booth <mat.booth@redhat.com> - 2.5.1-1
- Update to javaparser 2.5.1 for Java 1.8 support

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 31 2015 gil cattaneo <puntogil@libero.it> 1.0.11-1
- update to 1.0.11

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 15 2015 gil cattaneo <puntogil@libero.it> 1.0.8-9
- fix Url tag

* Fri Feb 06 2015 gil cattaneo <puntogil@libero.it> 1.0.8-8
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.0.8-6
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 08 2013 gil cattaneo <puntogil@libero.it> 1.0.8-4
- switch to XMvn
- minor changes to adapt to current guideline

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.8-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 26 2012 gil cattaneo <puntogil@libero.it> 1.0.8-1
- initial rpm
