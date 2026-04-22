# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           args4j
Version:        2.33
Release: 31%{?dist}
Summary:        Java command line arguments parser
License:        MIT
URL:            https://args4j.kohsuke.org
Source0:        https://github.com/kohsuke/%{name}/archive/%{name}-site-%{version}.tar.gz

BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)

# Fix build on Java 11/17
Patch0: 0001-Remove-usage-of-internal-sun-class-removed-in-Java-9.patch

# Stopped shipping these unused subpackages in F34
Obsoletes: %{name}-tools < 2.33-13
Obsoletes: %{name}-parent < 2.33-13

%description
args4j is a small Java class library that makes it easy
to parse command line options/arguments in your CUI application.
- It makes the command line parsing very easy by using annotations
- You can generate the usage screen very easily
- You can generate HTML/XML that lists all options for your documentation
- Fully supports localization
- It is designed to parse javac like options (as opposed to GNU-style
  where ls -lR is considered to have two options l and R)

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-site-%{version}
%patch -P0 -p1

# removing bundled stuff
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

# Not needed for RPM builds
%pom_remove_plugin -r :maven-site-plugin

# we don't need these now
%pom_disable_module args4j-maven-plugin
%pom_disable_module args4j-maven-plugin-example
%pom_disable_module args4j-tools

# Remove reliance on the parent pom
%pom_remove_parent

# Remove hard-coded source/target
%pom_xpath_remove pom:plugin/pom:configuration/pom:target
%pom_xpath_remove pom:plugin/pom:configuration/pom:source

# Don't package the parent pom
%mvn_package :args4j-site __noinstall

# install also compat symlinks
%mvn_file ":{*}" %{name}/@1 @1

%build
%mvn_build -- -Dmaven.compiler.release=11

%install
%mvn_install

%files -f .mfiles
%license %{name}/LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license %{name}/LICENSE.txt

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 2.33-30
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.33-26
- Rebuilt for java-21-openjdk as system jdk

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 2.33-20
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.33-19
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 30 2021 Mat Booth <mat.booth@gmail.com> - 2.33-17
- Fix build on Java 11/17

* Mon Nov 29 2021 Mat Booth <mat.booth@gmail.com> - 2.33-16
- Remove hard-coded source/target

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 12 2020 Mat Booth <mat.booth@redhat.com> - 2.33-13
- Stop shipping unused subpackages for tools and parent pom

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 2.33-11
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Sat Jun 20 2020 Mat Booth <mat.booth@redhat.com> - 2.33-10
- Allow building against Java 11

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 18 2019 Mat Booth <mat.booth@redhat.com> - 2.33-7
- Avoid unnecessary koshuke parent pom, it doesn't add anything to the build

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 2.33-2
- Remove BR on site-plugin

* Tue Jul 19 2016 Michael Simacek <msimacek@redhat.com> - 2.33-1
- Update to upstream version 2.33

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 03 2015 Michael Simacek <msimacek@redhat.com> - 2.32-2
- Remove uberjar generation

* Thu Jul 02 2015 Michal Srb <msrb@redhat.com> - 2.32-1
- Update to upstream release 2.32

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 22 2014 Michal Srb <msrb@redhat.com> - 2.0.30-2
- Move args4j-tools and parent POM into subpackages (Resolves: #1144991)

* Mon Sep 01 2014 Michal Srb <msrb@redhat.com> - 2.0.30-1
- Update to upstream version 2.0.30

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Michal Srb <msrb@redhat.com> - 2.0.28-1
- Update to upstream version 2.0.28

* Wed May 07 2014 Michal Srb <msrb@redhat.com> - 2.0.27-1
- Update to upstream version 2.0.27

* Tue May 06 2014 Michal Srb <msrb@redhat.com> - 2.0.26-4
- Port to JSR-269

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.0.26-3
- Use Requires: java-headless rebuild (#1067528)

* Thu Feb 20 2014 Michal Srb <msrb@redhat.com> - 2.0.26-2
- Adapt to current guidelines

* Thu Feb 20 2014 Michal Srb <msrb@redhat.com> - 2.0.26-1
- Update to latest upstream 2.0.26

* Sat Aug 10 2013 Mat Booth <fedora@matbooth.co.uk> - 2.0.25-1
- Update to latest upstream, fixes #981339

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 27 2013 Mat Booth <fedora@matbooth.co.uk> - 2.0.23-1
- Update to latest upstream, fixes #808703
- Also drop unneeded patches

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.0.16-10
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Dec 13 2012 Roland Grunberg <rgrunber@redhat.com> - 2.0.16-9
- Update to conform with latest Java packaging guidelines.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 31 2012 Ville Skyttä <ville.skytta@iki.fi> - 2.0.16-7
- Apply upstream source encoding patch to fix build with java 1.7.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 13 2011 Jaromir Capik <jcapik@redhat.com> - 2.0.16-4
- OSGi metadata generated

* Mon May 30 2011 Jaromir Capik <jcapik@redhat.com> - 2.0.16-3
- Removal of bundled stuff in args4j/lib

* Wed May 25 2011 Jaromir Capik <jcapik@redhat.com> - 2.0.16-2
- Removal of unused ant dependency

* Tue May 24 2011 Jaromir Capik <jcapik@redhat.com> - 2.0.16-1
- Initial version of the package
