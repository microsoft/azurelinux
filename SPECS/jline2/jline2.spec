# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           jline2
Version:        2.14.6
Release:        16%{?dist}
Summary:        Java library for handling console input
License:        BSD-3-Clause
URL:            http://jline.github.io/jline2/

Source0:        https://github.com/jline/jline2/archive/jline-%{version}.tar.gz

BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.easymock:easymock)
BuildRequires:  mvn(org.fusesource.jansi:jansi:1)

%description
JLine is a Java library for handling console input.  It is similar in
functionality to BSD editline and GNU readline.  People familiar with
the readline/editline capabilities for modern shells (such as bash and
tcsh) will find most of the command editing features of JLine to be
familiar.

%{?javadoc_package}

%prep
%autosetup -n jline2-jline-%{version}

# remove unnecessary dependency on parent POM
%pom_remove_parent

# Remove maven-shade-plugin usage
%pom_remove_plugin "org.apache.maven.plugins:maven-shade-plugin"
# Remove animal sniffer plugin in order to reduce deps
%pom_remove_plugin "org.codehaus.mojo:animal-sniffer-maven-plugin"

# Remove unavailable and unneeded deps
%pom_xpath_remove "pom:build/pom:extensions"
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-javadoc-plugin

# Makes the build fail on deprecation warnings from jansi
%pom_xpath_remove 'pom:arg[text()="-Werror"]'

# Do not import non-existing internal package
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions/pom:Import-Package"
%pom_xpath_inject "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions" "<Import-Package>javax.swing;resolution:=optional,org.fusesource.jansi,!org.fusesource.jansi.internal</Import-Package>"

# Be sure to export jline.internal, but not org.fusesource.jansi.
# See https://bugzilla.redhat.com/show_bug.cgi?id=1317551
%pom_xpath_set "pom:build/pom:plugins/pom:plugin[pom:artifactId = 'maven-bundle-plugin']/pom:executions/pom:execution/pom:configuration/pom:instructions/pom:Export-Package" "jline.*;-noimport:=true"

# Update required version of jansi 1.x
%pom_xpath_set //pom:jansi.version 1.18

# drop a nondeterministic test
find -name TerminalFactoryTest.java -delete
# it's also the only test that uses powermock, so drop the powermock dependency
%pom_remove_dep org.powermock:

# Fix javadoc generation on java 11
%pom_xpath_inject pom:build/pom:plugins "<plugin>
<artifactId>maven-javadoc-plugin</artifactId>
<configuration><source>1.8</source></configuration>
</plugin>"

%build
%mvn_build -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8

%install
%mvn_install

%files -f .mfiles
%doc CHANGELOG.md README.md
%license LICENSE.txt

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 2.14.6-16
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.14.6-12
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 14 2023 Jerry James <loganjerry@gmail.com> - 2.14.6-8
- Convert License tag to SPDX

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 2.14.6-6
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.14.6-5
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 Jerry James <loganjerry@gmail.com> - 2.14.6-1
- Unretire jline2 due to introduction of jline 3.x

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 12 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-7
- Remove unneeded animal-sniffer BR.

* Tue Mar 12 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-6
- Fix OSGi metadata. Don't export packages which aren't in this
  package. Fixes RHBZ#920756.

* Mon Mar 11 2013 Severin Gehwolf <sgehwolf@redhat.com> 2.10-5
- Provide %{_javadir}/%{name}.jar symlink. Fix RHBZ#919640.

* Thu Feb 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10-4
- Install versioned JAR and POM
- Add missing BR: animal-sniffer
- Resolves: rhbz#911559

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.10-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Feb 01 2013 Marek Goldmann <mgoldman@redhat.com> - 2.10-2
- Do not import non-existing org.fusesource.jansi.internal package

* Fri Feb 01 2013 Marek Goldmann <mgoldman@redhat.com> - 2.10-1
- Upstream release 2.10
- Removed patches, using pom macros now

* Fri Oct 19 2012 Severin Gehwolf <sgehwolf@redhat.com> 2.5-7
- Fix OSGi Import-Package header so as to not import non existing
  org.fusesource.jansi.internal package.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 15 2011 Marek Goldmann <mgoldman@redhat.com> 2.5-4
- jline.console.ConsoleReader.back should be protected instead of private [rhbz#751208]

* Wed Sep 21 2011 Marek Goldmann <mgoldman@redhat.com> 2.5-3
- Updated license
- Removed unnecessary add_to_maven_depmap

* Thu Sep 08 2011 Marek Goldmann <mgoldman@redhat.com> 2.5-2
- Cleaned spec

* Tue May 31 2011 Marek Goldmann <mgoldman@redhat.com> 2.5-1
- Initial packaging
