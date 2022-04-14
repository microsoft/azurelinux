Vendor:         Microsoft Corporation
Distribution:   Mariner
%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}

Name:             jboss-modules
Version:          1.5.2
Release:          9%{?dist}
Summary:          A Modular Classloading System
# XPP3 License: src/main/java/org/jboss/modules/xml/MXParser.java
#  src/main/java/org/jboss/modules/xml/XmlPullParser.java
#  src/main/java/org/jboss/modules/xml/XmlPullParserException.java
License:          ASL 2.0 and xpp
URL:              https://github.com/jbossas/jboss-modules
Source0:          https://github.com/jbossas/jboss-modules/archive/%{namedversion}/%{name}-%{namedversion}.tar.gz
Patch0:           Adjusting-plugin-configuration.patch

BuildArch:        noarch

BuildRequires:    maven-local
BuildRequires:    mvn(junit:junit)
BuildRequires:    mvn(org.jboss:jboss-parent:pom:)
BuildRequires:    mvn(org.jboss.shrinkwrap:shrinkwrap-impl-base)
%if 0%{?fedora}
BuildRequires:    graphviz
BuildRequires:    mvn(jdepend:jdepend)
BuildRequires:    mvn(org.jboss.apiviz:apiviz)
%endif

%description
Ths package contains A Modular Classloading System.

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%autosetup -p1 -n %{name}-%{namedversion}

# Remove dependency on apiviz
%pom_remove_plugin :maven-javadoc-plugin

# Unneeded task
%pom_remove_plugin :maven-source-plugin

# Use not available org.wildfly.checkstyle:wildfly-checkstyle-config:1.0.4.Final
%pom_remove_plugin :maven-checkstyle-plugin

# Tries to connect to remote host
rm src/test/java/org/jboss/modules/MavenResourceTest.java \
 src/test/java/org/jboss/modules/maven/MavenSettingsTest.java

%build
%mvn_build --skip-tests

%install
%mvn_install

%check
mvn test

%files -f .mfiles
%doc README.md
%license LICENSE.txt XPP3-LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt XPP3-LICENSE.txt

%changelog
* Mon Aug 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.2-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Moving tests to the '%%check' section.
- Adding a patch to disable compiling tests during the '%%build' phase.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Aug 20 2016 gil cattaneo <puntogil@libero.it> 1.5.2-1
- update to 1.5.2.Final

* Fri May 27 2016 gil cattaneo <puntogil@libero.it> 1.5.1-1
- update to 1.5.1.Final

* Tue Mar 01 2016 gil cattaneo <puntogil@libero.it> 1.3.3-3
- fix FTBFS rhbz#1307649
- fix BR list and use BR mvn()-like
- fix some rpmlint problem

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 12 2014 Marek Goldmann <mgoldman@redhat.com> - 1.3.3-1
- Upstream release 1.3.3.Final

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 20 2014 Marek Goldmann <mgoldman@redhat.com> - 1.3.0-1
- Upstream release 1.3.0.Final

* Thu Sep 12 2013 Marek Goldmann <mgoldman@redhat.com> - 1.3.0-0.1.Beta3
- Upstream release 1.3.0.Beta3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.1-2
- Remove unneeded BR

* Tue Jun 04 2013 Marek Goldmann <mgoldman@redhat.com> - 1.2.1-1
- Upstream release 1.2.1.Final
- New guidelines

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.1.1-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Sep  3 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.1-7
- Conditionally remove dependency on apiviz

* Mon Sep  3 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.1-6
- Remove unneeded BR: maven-injection-plugin

* Fri Jul 20 2012 Marek Goldmann <mgoldman@redhat.com> 1.1.1-4
- Fixed BR

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 05 2012 Marek Goldmann <mgoldman@redhat.com> 1.1.1-3
- Patch to fix MODULES-128

* Thu Feb 23 2012 Marek Goldmann <mgoldman@redhat.com> 1.1.1-2
- Relocated jars to _javadir

* Sun Feb 19 2012 Marek Goldmann <mgoldman@redhat.com> 1.1.1-1
- Upstream release 1.1.1.GA

* Thu Jan 26 2012 Marek Goldmann <mgoldman@redhat.com> 1.1.0-0.3.CR8
- Upstream release 1.1.0.CR8

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.2.CR4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 02 2011 Marek Goldmann <mgoldman@redhat.com> 1.1.0-0.1.CR4
- Upstream release 1.1.0.CR4

* Tue Aug 02 2011 Marek Goldmann <mgoldman@redhat.com> 1.0.2-1
- Initial packaging

