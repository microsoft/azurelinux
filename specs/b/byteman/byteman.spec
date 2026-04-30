## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autochangelog
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Note to the interested reader:
#   fedpkg mockbuild --without tests
# will make mvn_build macro skip tests.
# See: https://github.com/fedora-java/javapackages/issues/62

%global javacup_or_asm java_cup:java_cup|org\\.ow2\\.asm:asm.*
# Don't have generated mvn()-style requires for java_cup or asm
%global mvn_javacup_or_asm_matcher .*mvn\\(%{javacup_or_asm}\\)
# Don't have generated requires for java-headless >= 1:1.9
%global java_headless_matcher java-headless >= 1:(1\\.9|9)
%global __requires_exclude ^%{mvn_javacup_or_asm_matcher}|%{java_headless_matcher}$

%global homedir %{_datadir}/%{name}
%global bindir %{homedir}/bin

Name:             byteman
Version:          4.0.26
Release: 2%{?dist}
Summary:          Java agent-based bytecode injection tool
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:          LicenseRef-Callaway-LGPLv2+
URL:              http://www.jboss.org/byteman
# wget -O 4.0.16.tar.gz https://github.com/bytemanproject/byteman/archive/4.0.16.tar.gz
Source0:          https://github.com/bytemanproject/byteman/archive/%{version}.tar.gz

BuildArch:        noarch
ExclusiveArch:  %{java_arches} noarch

# Byteman 4.x requires JDK 9+ to build. Require JDK 10 explicitly.
BuildRequires:    java-25-devel >= 1:11
BuildRequires:    maven-local-openjdk25
BuildRequires:    maven-shade-plugin
BuildRequires:    maven-source-plugin
BuildRequires:    maven-plugin-plugin
BuildRequires:    maven-bundle-plugin
BuildRequires:    maven-assembly-plugin
BuildRequires:    maven-failsafe-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-surefire-plugin
BuildRequires:    maven-surefire-provider-testng
BuildRequires:    maven-surefire-provider-junit
BuildRequires:    maven-surefire-provider-junit5
BuildRequires:    maven-verifier-plugin
BuildRequires:    maven-dependency-plugin
BuildRequires:    java_cup
BuildRequires:    objectweb-asm
BuildRequires:    junit
BuildRequires:    junit5
BuildRequires:    testng

Provides:         bundled(objectweb-asm) = 9.1
Provides:         bundled(java_cup) = 1:0.11b-17
# We are filtering java-headless >= 1:1.9 requirement. Add
# JDK 8 requirement here explicitly which shouldn't match the filter.
Requires:         java-25-headless >= 1:1.8

# Related pieces removed via pom_xpath_remove macros
Patch1:           remove_submit_integration_test_verification.patch
Patch2:           testng7_port.patch

%description
Byteman is a tool which simplifies tracing and testing of Java programs.
Byteman allows you to insert extra Java code into your application,
either as it is loaded during JVM startup or even after it has already
started running. The injected code is allowed to access any of your data
and call any application methods, including where they are private.
You can inject code almost anywhere you want and there is no need to
prepare the original source code in advance nor do you have to recompile,
repackage or redeploy your application. In fact you can remove injected
code and reinstall different code while the application continues to execute.

%package javadoc
Summary:          Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%package rulecheck-maven-plugin
Summary:          Maven plugin for checking Byteman rules.

%description rulecheck-maven-plugin
This package contains the Byteman rule check maven plugin.

%package bmunit
Summary:          TestNG and JUnit integration for Byteman.

%description bmunit
The Byteman bmunit jar provides integration of Byteman into
TestNG and JUnit tests.

%package dtest
Summary:          Remote byteman instrumented testing.

%description dtest
The Byteman dtest jar supports instrumentation of test code executed on
remote server hosts and validation of assertions describing the expected
operation of the instrumented methods.

%prep
%setup -q -n byteman-%{version}

# Fix the gid:aid for java_cup
sed -i "s|net.sf.squirrel-sql.thirdparty-non-maven|java_cup|" agent/pom.xml
sed -i "s|java-cup|java_cup|" agent/pom.xml
sed -i "s|net.sf.squirrel-sql.thirdparty-non-maven|java_cup|" tests/pom.xml
sed -i "s|java-cup|java_cup|" tests/pom.xml

# Remove Submit integration test invocations (agent)
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-failsafe-plugin']/pom:executions/pom:execution[pom:id='submit.TestSubmit']" agent
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-failsafe-plugin']/pom:executions/pom:execution[pom:id='submit.TestSubmit.compiled']" agent
%patch -P1 -p2
%patch -P2 -p2

# Remove Submit integration test invocations (tests)
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-failsafe-plugin']/pom:executions/pom:execution[pom:id='submit.TestSubmit']" tests
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-failsafe-plugin']/pom:executions/pom:execution[pom:id='submit.TestSubmit.compiled']" tests

# Remove scope=system and systemPath for com.sun:tools
%pom_xpath_remove "pom:profiles/pom:profile/pom:dependencies/pom:dependency[pom:artifactId='tools']/pom:scope" install
%pom_xpath_remove "pom:profiles/pom:profile/pom:dependencies/pom:dependency[pom:artifactId='tools']/pom:systemPath" install
%pom_xpath_remove "pom:profiles/pom:profile/pom:dependencies/pom:dependency[pom:artifactId='tools']/pom:scope" contrib/bmunit
%pom_xpath_remove "pom:profiles/pom:profile/pom:dependencies/pom:dependency[pom:artifactId='tools']/pom:systemPath" contrib/bmunit

# Some tests fail intermittently during builds. Disable them.
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-surefire-plugin']/pom:executions" contrib/bmunit
%pom_xpath_set "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-surefire-plugin']/pom:configuration" '<skip>true</skip>' contrib/bmunit

# source/target 1.6 is not supported by 17; default is now 1.8
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-compiler-plugin']/pom:configuration/pom:source" pom.xml
%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-compiler-plugin']/pom:configuration/pom:target" pom.xml

# Don't build download, docs modules
%pom_disable_module download


# Don't use javadoc plugin, use XMvn for javadocs
%pom_remove_plugin -r :maven-javadoc-plugin
%pom_remove_plugin -r :central-publishing-maven-plugin
%pom_remove_dep 'org.apache.maven:maven-project' contrib/rulecheck-maven-plugin
%pom_xpath_remove 'pom:execution[pom:id="make-javadoc-assembly"]' byteman

# Put byteman-rulecheck-maven-plugin into a separate package
%mvn_package ":byteman-rulecheck-maven-plugin" rulecheck-maven-plugin

# CNFE being thrown without this for bmunit5 in rawhide and with tests enabled
%pom_add_dep "org.apache.commons:commons-lang3" contrib/bmunit5
# Put byteman-bmunit/byteman-dtest into a separate packages since they
# runtime require junit
%mvn_package ":byteman-bmunit" bmunit
%mvn_package ":byteman-dtest" dtest

%build
export JAVA_HOME=/usr/lib/jvm/java-openjdk
# Use --xmvn-javadoc so as to avoid maven-javadoc-plugin issue
# (fixed in 3.1.0, fedora has 3.0.1):
# See https://issues.apache.org/jira/browse/MJAVADOC-555
#     https://bugs.openjdk.java.net/browse/JDK-8212233
%mvn_build --xmvn-javadoc -f

%install
%mvn_install

install -d -m 755 $RPM_BUILD_ROOT%{_bindir}

install -d -m 755 $RPM_BUILD_ROOT%{homedir}
install -d -m 755 $RPM_BUILD_ROOT%{homedir}/lib
install -d -m 755 $RPM_BUILD_ROOT%{bindir}

install -m 755 bin/bmsubmit.sh $RPM_BUILD_ROOT%{bindir}/bmsubmit
install -m 755 bin/bminstall.sh  $RPM_BUILD_ROOT%{bindir}/bminstall
install -m 755 bin/bmjava.sh  $RPM_BUILD_ROOT%{bindir}/bmjava
install -m 755 bin/bmcheck.sh  $RPM_BUILD_ROOT%{bindir}/bmcheck

for f in bmsubmit bmjava bminstall bmcheck; do
cat > $RPM_BUILD_ROOT%{_bindir}/${f} << EOF
#!/bin/sh

export BYTEMAN_HOME=/usr/share/byteman
export JAVA_HOME=/usr/lib/jvm/java

\$BYTEMAN_HOME/bin/${f} \$*
EOF
done

chmod 755 $RPM_BUILD_ROOT%{_bindir}/*

for m in bmunit dtest install sample submit; do
  ln -s %{_javadir}/byteman/byteman-${m}.jar $RPM_BUILD_ROOT%{homedir}/lib/byteman-${m}.jar
done

# Create contrib/jboss-module-system structure since bminstall expects it
# for the -m option.
install -d -m 755 $RPM_BUILD_ROOT%{homedir}/contrib
install -d -m 755 $RPM_BUILD_ROOT%{homedir}/contrib/jboss-modules-system
ln -s %{_javadir}/byteman/byteman-jboss-modules-plugin.jar $RPM_BUILD_ROOT%{homedir}/contrib/jboss-modules-system/byteman-jboss-modules-plugin.jar

ln -s %{_javadir}/byteman/byteman.jar $RPM_BUILD_ROOT%{homedir}/lib/byteman.jar

%files -f .mfiles
%{homedir}/lib/byteman.jar
%{homedir}/lib/byteman-install.jar
%{homedir}/lib/byteman-sample.jar
%{homedir}/lib/byteman-submit.jar
%{homedir}/contrib/*
%{bindir}/*
%{_bindir}/*
%doc README
%license docs/copyright.txt

%files javadoc -f .mfiles-javadoc
%license docs/copyright.txt

%files rulecheck-maven-plugin -f .mfiles-rulecheck-maven-plugin
%license docs/copyright.txt

%files bmunit -f .mfiles-bmunit
%license docs/copyright.txt
%{homedir}/lib/byteman-bmunit.jar

%files dtest -f .mfiles-dtest
%license docs/copyright.txt
%{homedir}/lib/byteman-dtest.jar

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 4.0.26-3
- test: add initial lock files

* Thu Oct 23 2025 Jiri Vanek <jvanek@redhat.com> - 4.0.26-2
- disabled tests

* Thu Oct 23 2025 Jiri Vanek <jvanek@redhat.com> - 4.0.26-1
- Updated to byteman 4.0.26

* Mon Jul 28 2025 Jiri Vanek <jvanek@redhat.com> - 4.0.16-23
- Rebuilt for java-25-openjdk as preffered jdk

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.16-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.16-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 4.0.16-20
- convert license to SPDX

* Thu Aug 15 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 4.0.16-19
- Update maven-bundle-plugin dependency

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.16-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 30 2024 Software Management Team <packaging-team-maint@redhat.com> - 4.0.16-17
- Eliminate use of obsolete %%patchN syntax (#2283636)

* Sun Mar 03 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 4.0.16-16
- Really rebuild with java-21-openjdk as system jdk

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 4.0.16-15
- Rebuilt for java-21-openjdk as system jdk

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.16-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 4.0.16-12
- Build with Java 17

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.16-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 10 2022 Severin Gehwolf <sgehwolf@redhat.com> - 4.0.16-9
- Rebuild with latest maven-verifier-plugin

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri <jvanek@redhat.com> - 4.0.16-7
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri <jvanek@redhat.com> - 4.0.16-6
- Rebuilt for java-17-openjdk as system jdk

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 29 2021 Severin Gehwolf <sgehwolf@redhat.com> - 4.0.16-2
- Add basic smoke tests

* Fri Jun 18 2021 Severin Gehwolf <sgehwolf@redhat.com> - 4.0.16-1
- Update to latest 4.0.16 release

* Mon May 31 2021 Severin Gehwolf <sgehwolf@redhat.com> - 4.0.15-3
- Fix CNFE for bmunit5 plugin tests

* Mon May 31 2021 Severin Gehwolf <sgehwolf@redhat.com> - 4.0.15-2
- Re-enable tests run during the build

* Mon May 31 2021 Severin Gehwolf <sgehwolf@redhat.com> - 4.0.15-1
- Update to latest upstream 4.0.15 release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri <jvanek@redhat.com> - 4.0.11-2
- Rebuilt for JDK-11

* Tue Apr 07 2020 Jayashree Huttanagoudar <jhuttana@redhat.com> - 4.0.11-1
- Upgraded to latest upstream version 4.0.11

* Tue Jan 28 2020 Severin Gehwolf <sgehwolf@redhat.com> - 4.0.5-6
- Remove jarjar BR which is not needed

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 06 2019 Severin Gehwolf <sgehwolf@redhat.com> - 4.0.5-3
- Use XMvn javadoc so as to fix FTBFS

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 23 2018 Severin Gehwolf <sgehwolf@redhat.com> - 4.0.5-1
- Update to latest upstream 4.0.5 release.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Severin Gehwolf <sgehwolf@redhat.com> - 4.0.4-1
- Update to upstream 4.0.4 release.
- Split subpackages requiring junit at runtime: byteman-dtest, byteman-
  bmunit
- Fix filtering of asm requirements. They shouldn't be there since asm gets
  bundled.
- java-headless >= 1:1.9 would get generated, but byteman 4.x runs on JDK
  6+. Require >= JDK 8
- Properly install structure for jboss-modules-plugin to work: bminstall -m

* Thu Jul 05 2018 Severin Gehwolf <sgehwolf@redhat.com> - 4.0.3-2
- Use Xmvn for javadoc generation.

* Tue Jul 03 2018 Severin Gehwolf <sgehwolf@redhat.com> - 4.0.3-1
- Update to latest upstream 4.0.3 release.

* Fri Apr 27 2018 Severin Gehwolf <sgehwolf@redhat.com> - 4.0.2-1
- Update to latest upstream 4.0.2 release.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Severin Gehwolf <sgehwolf@redhat.com> - 3.0.6-2
- Fix FTBFS.
- Add BRs maven-plugin-bundle, maven-source-plugin, maven-plugin-plugin
- Resolves: RHBZ#1402998

* Tue Jun 14 2016 Severin Gehwolf <sgehwolf@redhat.com> - 3.0.6-1
- Update to latest 3.0.6 release.

* Mon Mar 14 2016 Severin Gehwolf <sgehwolf@redhat.com> - 3.0.4-2
- Some packaging improvements.
- Remove generated requires on bundled libs.
- Split maven rulecheck plugin into separate package
- Run some tests during build

* Thu Feb 18 2016 Severin Gehwolf <sgehwolf@redhat.com> - 3.0.4-1
- Update to latest upstream 3.0.4 release.

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us> - 2.1.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 06 2015 gil <puntogil@libero.it> - 2.1.4.1-7
- Fix FTBFS rhbz#1239392

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 2.1.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 27 2015 Michal Srb <msrb@redhat.com> - 2.1.4.1-5
- Fix FTBFS
- Rebuild to generate new metadata

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 2.1.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 18 2014 Marek Goldmann <marek.goldmann@gmail.com> - 2.1.4.1-3
- Rebuilding for objectweb-asm update, RHBZ#1083570

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.1.4.1-2
- Use Requires: java-headless rebuild (#1067528)

* Fri Feb 14 2014 Marek Goldmann <marek.goldmann@gmail.com> - 2.1.4.1-1
- Upstream release 2.1.4.1

* Sat Aug 03 2013 Dennis Gilmore <dennis@ausil.us> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 04 2013 Marek Goldmann <marek.goldmann@gmail.com> - 2.1.2-1
- Upstream release 2.1.2

* Wed Jun 05 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.0.4-5
- Remove tools.jar from dependencyManagement

* Wed Jun 05 2013 Marek Goldmann <marek.goldmann@gmail.com> - 2.0.4-4
- New guidelines

* Mon Apr 29 2013 Marek Goldmann <marek.goldmann@gmail.com> - 2.0.4-3
- Launch scripts fixed

* Wed Apr 24 2013 Marek Goldmann <marek.goldmann@gmail.com> - 2.0.4-2
- Added bmsubmit, bminstall and bmjava scripts, RHBZ#951560

* Tue Feb 26 2013 Marek Goldmann <marek.goldmann@gmail.com> - 2.0.4-1
- Upstream release 2.0.4 - Switched to Maven - Bundling java_cup and
  objectweb-asm (fpc#226)

* Wed Feb 13 2013 Dennis Gilmore <dennis@ausil.us> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Dennis Gilmore <dennis@ausil.us> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Dennis Gilmore <dennis@ausil.us> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 26 2011 Marek Goldmann <goldmann@fedoraproject.org> - 1.5.2-1
- Initial import.
## END: Generated by rpmautospec
