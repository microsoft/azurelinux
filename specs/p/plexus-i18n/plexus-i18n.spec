# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           plexus-i18n
Version:        1.0
Release: 1.36.b10.4%{?dist}
Summary:        Plexus I18N Component
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            https://github.com/codehaus-plexus/plexus-i18n
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch
# svn export http://svn.codehaus.org/plexus/plexus-components/tags/plexus-i18n-1.0-beta-10/
# tar cjf plexus-i18n-1.0-beta-10-src.tar.bz2 plexus-i18n-1.0-beta-10/
Source0:        plexus-i18n-1.0-beta-10-src.tar.bz2
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.google.inject:guice)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-components:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)

%description
The Plexus project seeks to create end-to-end developer tools for 
writing applications. At the core is the container, which can be 
embedded or for a full scale application server. There are many 
reusable components for hibernate, form processing, jndi, i18n, 
velocity, etc. Plexus also includes an application server which 
is like a J2EE application server, without all the baggage.

%{?javadoc_package}

%prep
# -n: base directory name
%autosetup -n plexus-i18n-1.0-beta-10
# plexus maven plugin is deprecated
# switched it to plexus-component-metadata
%pom_xpath_set 'pom:plugin[pom:artifactId = "plexus-maven-plugin"]/pom:artifactId' plexus-component-metadata
# set goal to generate-metadata
%pom_xpath_set 'pom:goals[pom:goal = "descriptor"]/pom:goal' generate-metadata
# add missing dependencies
%pom_add_dep org.codehaus.plexus:plexus-container-default::provided
%pom_add_dep com.google.inject:guice::test
%pom_add_dep junit:junit::test
# remove maven-compiler-plugin configuration that is broken with Java 11
%pom_xpath_remove 'pom:plugin[pom:artifactId="maven-compiler-plugin"]/pom:configuration'

%build
%mvn_build -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8

%install
%mvn_install

%files -f .mfiles

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 1.0-0.36.b10.4
- Rebuilt for java-25-openjdk as preffered jdk

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.35.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.34.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1.0-0.33.b10.4
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.32.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1.0-0.31.b10.4
- Rebuilt for java-21-openjdk as system jdk

* Tue Feb 06 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.30.b10.4
- Fix build with plexus-containers 2.2.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.29.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.28.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.27.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.26.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.25.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1.0-0.24.b10.4
- Rebuilt for Drop i686 JDKs

* Sat Feb 26 2022 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 1.0-0.23.b10.4
- Remove patches and use pom_* macros instead
- Use javadoc_package for javadoc subpackage
- Use autosetup macros instead of setup

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1.0-0.22.b10.4
- Rebuilt for java-17-openjdk as system jdk

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.21.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.20.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.19.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.18.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Fabio Valentini <decathorpe@gmail.com> - 1.0-0.17.b10.4
- Set javac source and target to 1.8 to fix Java 11 builds.

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1.0-0.16.b10.4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.15.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.14.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.13.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.12.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.11.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.10.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.9.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.8.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.7.b10.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.6.b10.4
- Update upstream URL

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.6.b10.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.5.b10.3
- Update to current packaging guidelines

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.5.b10.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.4.b10.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-0.3.b10.2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Nov 22 2012 Jaromir Capik <jcapik@redhat.com> - 1.0-0.2.b10.2
- Migration to plexus-containers-container-default

* Mon Nov 12 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.1.b10.2
- Fix Release tag

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.b10.2.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 Jaromir Capik <jcapik@redhat.com> - 1.0-0.b10.2.4
- Missing plexus-container-default dependency added in the pom.xml

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.b10.2.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 28 2011 Jaromir Capik <jcapik@redhat.com> - 1.0-0.b10.2.2
- Migration to maven3
- Migration from plexus-maven-plugin to plexus-containers-component-metadata
- Minor spec file changes according to the latest guidelines

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.b10.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.b10.2
- BR java-devel 1.6.0.

* Wed Dec 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.b10.1
- Update to beta 10.
- Drop gcj and fix BRs.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.b6.5.3.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.b6.5.3.2
- Added pom.xml and components.xml to META-INF

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.b6.5.3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-0.b6.5.3
- drop repotag

* Wed Feb 27 2008 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.b6.5jpp.2
- Build with maven

* Tue Jan 22 2008 Permaine Cheung <pcheung@redhat.com> - 0:1.0-0.b6.5jpp.1
- Update to the same version as upstream

* Thu Apr 26 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b6.5jpp
- Reupload to fix metadata

* Sat Mar 24 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b6.4jpp
- Optionally build without maven
- Add gcj_support option
 
* Mon Feb 19 2007 Tania Bento <tbento@redhat.com> - 0:1.0-0.b6.3jpp.1
- Fixed %%Release tag.
- Changed the svn URL.
- Added instruction on how to tar the files extracted with svn export.
- Fixed %%BuildRoot tag.
- Removed %%post and %%postun sections for javadoc and made necessary changes.
- Added gcj support.

* Wed Oct 25 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b6.3jpp
- Fix components.xml
 
* Tue May 30 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b6.2jpp
- First JPP-1.7 release
- Drop maven support - waiting for maven2

* Mon Nov 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b6.1jpp
- First JPackage build
