# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without dom4j

Name:           jaxen
Summary:        An XPath engine written in Java
Epoch:          0
Version:        1.2.0
Release:        22%{?dist}
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD

URL:            https://github.com/jaxen-xpath/jaxen
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(jdom:jdom)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(xerces:xercesImpl)
BuildRequires:  mvn(xml-apis:xml-apis)
%if %{with dom4j}
BuildRequires:  mvn(dom4j:dom4j)
%endif

%description
Jaxen is an open source XPath library written in Java. It is adaptable
to many different object models, including DOM, XOM, dom4j, and JDOM.
Is it also possible to write adapters that treat non-XML trees such as compiled
Java byte code or Java beans as XML, thus enabling you to query these trees
with XPath too.


%package        demo
Summary:        Samples for %{name}
Requires:       %{name} = 0:%{version}-%{release}

%description    demo
%{summary}.


%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
%{summary}.


%prep
%setup -q

# remove unnecessary maven plugins
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-source-plugin

# remove maven-compiler-plugin configuration that is broken with Java 11
%pom_xpath_remove 'pom:plugin[pom:artifactId="maven-compiler-plugin"]/pom:configuration'

%if %{without dom4j}
rm -rf src/java/main/org/jaxen/dom4j
%pom_remove_dep dom4j:dom4j
%endif

rm -rf src/java/main/org/jaxen/xom
%pom_remove_dep xom:xom

%mvn_file : %{name}


%build
%mvn_build -f -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8


%install
%mvn_install

# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}/samples
cp -pr src/java/samples/* %{buildroot}%{_datadir}/%{name}/samples


%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%files demo
%{_datadir}/%{name}


%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 0:1.2.0-22
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 0:1.2.0-19
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 0:1.2.0-17
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 0:1.2.0-11
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 0:1.2.0-10
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Fabio Valentini <decathorpe@gmail.com> - 0:1.2.0-5
- Drop unnecessary dependency on maven-javadoc-plugin.
- Fix javac source / target versions for Java 11.

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 0:1.2.0-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Fabio Valentini <decathorpe@gmail.com> - 0:1.2.0-1
- Update to version 1.2.0.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.1.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.6-18
- Allow conditionally building with dom4j

* Wed Jul 18 2018 Michael Simacek <msimacek@redhat.com> - 0:1.1.6-17
- Fix license tag to include W3C

* Tue Jul 17 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.6-16
- Remove support for dom4j

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.1.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0:1.1.6-14
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.1.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.1.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar  7 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.6-11
- Don't hardcode package name

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.6-9
- Add missing build-requires
- Remove old obsoletes/provides

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:1.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Michal Srb <msrb@redhat.com> - 0:1.1.6-6
- Rebuild to regenerate R

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.6-5
- Fix build-requires on sonatype-oss-parent

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.1.6-3
- Use Requires: java-headless rebuild (#1067528)

* Wed Jan 29 2014 Michal Srb <msrb@redhat.com> - 0:1.1.6-2
- Remove saxpath provides (Resolves: rhbz#1059229)

* Mon Sep 02 2013 Michal Srb <msrb@redhat.com> - 0:1.1.6-1
- Update to upstream version 1.1.6
- Build with Maven
- Update description
- Adapt to current guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 28 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.3-8
- Remove xom dependency from POM
- Resolves: rhbz#880970

* Tue Nov 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.3-7
- Remove unneeded dependency from POM: maven-cobertura-plugin
- Remove unneeded dependency from POM: maven-findbugs-plugin
- Resolves: rhbz#880692

* Fri Nov  2 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.1.3-6
- Add maven POM

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 29 2012 Tomas Radej <tradej@redhat.com> - 0:1.1.3-4
- Removed xom dep from pom

* Mon Feb 27 2012 Tomas Radej <tradej@redhat.com> - 0:1.1.3-3
- Removed XOM support (bz #785007)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.1.3-1
- Update to latest upstream version.
- Adapt to current guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.1-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov 25 2008 Devrim GUNDUZ <devrim@gunduz.org> - 0:1.1.1-1
- Update to 1.1.1, to fix #465987 .

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.1-1.3
- drop repotag

* Tue Feb 20 2007 Vivek Lakshmanan <vivekl@redhat.com> 0:1.1-1jpp.2.fc7
- Add build-requires on ant-junit

* Mon Feb 19 2007 Andrew Overholt <overholt@redhat.com> 0:1.1-1jpp.1
- Add explicit version-release on Provides and Obsoletes
- Untabify
- Remove %%ghost on versioned javadoc dir
- Just include %%{_javadocdir}/* for javadoc package

* Wed Feb 14 2007 Andrew Overholt <overholt@redhat.com> 0:1.1-1jpp.1
- Bump to 1.1 final
- Make release Xjpp.Y%%{?dist}
- Remove Distribution, Vendor
- Fix Group
- Remove cleaning of buildroot from beginning of %%prep
- Add cleaning of buildroot to beginning of %%install
- Remove %%section free
- Use Fedora buildroot

* Sun Feb 26 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.1-0.b7.4jpp
- Rebuild for JPP 1.7

* Wed Feb 15 2006 Ralph Apel <r.apel@r-apel.de> 0:1.1-0.b7.3jpp
- Insert Copyright notice

* Mon Feb 13 2006 Ralph Apel <r.apel@r-apel.de> 0:1.1-0.b7.2jpp
- Adapt to maven-1.1
- Create option to build without maven

* Wed Aug 17 2005 Ralph Apel <r.apel@r-apel.de> 0:1.1-0.b7.1jpp
- Upgrade to 1.1-beta-7
- Now mavenized
- Requiring dom4j >= 1.6.1
- rpmbuild option to inhibit build of manual (needs newer maven)

* Thu Sep 09 2004 Ralph Apel <r.apel@r-apel.de> 0:1.1-0.b2.1jpp
- Upgrade to 1.1-beta-2
- Drop saxpath requirement as saxpath is now included in jaxen

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.0-4jpp
- Rebuild with ant-1.6.2
* Mon Jan 19 2004 Ralph Apel <r.apel@r-apel.de> 0:1.0-3jpp
- build against dom4j-1.4-1jpp
- introduce manual and demo subpackages
- patch org.jaxen.dom4j.DocumentNavigatorTest
- include LICENSE in main package
- run tests during build

* Thu Jan 15 2004 Ralph Apel <r.apel@r-apel.de> 0:1.0-2jpp
- activate support for dom4j by renaming lib/dom4j-core.jar to .zip

* Sun May 04 2003 David Walluck <david@anti-microsoft.org> 0:1.0-1jpp
- release

