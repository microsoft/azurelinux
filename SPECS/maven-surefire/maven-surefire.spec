%global upstream_version %(echo '%{version}' | tr '~' '-')
%bcond_without bootstrap
Summary:        Test framework project
Name:           maven-surefire
Version:        3.0.0
Release:        1%{?dist}
License:        ASL 2.0 AND CPL
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://maven.apache.org/surefire/
# ./generate-tarball.sh
Source0:        %{_mariner_sources_url}/%{name}-%{version}.tar.gz
Source2:        cpl-v10.html
Patch1:         0001-Port-to-TestNG-6.11.patch
Patch2:         0002-Disable-JUnit-4.8-test-grouping.patch
Patch3:         0003-Port-to-maven-shared-utils-3.3.3.patch
BuildRequires:  javapackages-bootstrap
BuildRequires:  javapackages-local-bootstrap
# PpidChecker relies on /usr/bin/ps to check process uptime
Requires:       procps-ng
BuildArch:      noarch

%description
Surefire is a test framework project.

%package plugin
Summary:        Surefire plugin for maven
Requires:       (%{name}-provider-junit = %{version}-%{release} if junit)
Requires:       (%{name}-provider-junit5 = %{version}-%{release} if junit5)
Requires:       (%{name}-provider-testng = %{version}-%{release} if testng)

%description plugin
Maven surefire plugin for running tests via the surefire framework.

%package provider-junit
Summary:        JUnit provider for Maven Surefire

%description provider-junit
JUnit provider for Maven Surefire.

%package provider-junit5
Summary:        JUnit 5 provider for Maven Surefire

%description provider-junit5
JUnit 5 provider for Maven Surefire.

%package provider-testng
Summary:        TestNG provider for Maven Surefire

%description provider-testng
TestNG provider for Maven Surefire.

%package -n maven-failsafe-plugin
Summary:        Maven plugin for running integration tests

%description -n maven-failsafe-plugin
The Failsafe Plugin is designed to run integration tests while the
Surefire Plugins is designed to run unit. The name (failsafe) was
chosen both because it is a synonym of surefire and because it implies
that when it fails, it does so in a safe way.

If you use the Surefire Plugin for running tests, then when you have a
test failure, the build will stop at the integration-test phase and
your integration test environment will not have been torn down
correctly.

The Failsafe Plugin is used during the integration-test and verify
phases of the build lifecycle to execute the integration tests of an
application. The Failsafe Plugin will not fail the build during the
integration-test phase thus enabling the post-integration-test phase
to execute.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n surefire-%{upstream_version}-M4
cp -p %{SOURCE2} .

%patch1 -p1
%patch2 -p1
%patch3 -p1

# Disable strict doclint
sed -i /-Xdoclint:all/d pom.xml

%pom_disable_module maven-surefire-report-plugin
%pom_disable_module surefire-report-parser
%pom_disable_module surefire-shadefire

%pom_remove_dep :maven-toolchain maven-surefire-common

%pom_disable_module surefire-grouper
%pom_remove_dep :surefire-grouper surefire-providers/common-junit48
%pom_remove_dep :surefire-grouper surefire-providers/surefire-testng-utils
rm surefire-providers/common-junit48/src/main/java/org/apache/maven/surefire/common/junit48/{FilterFactory,GroupMatcherCategoryFilter}.java
rm surefire-providers/surefire-testng-utils/src/main/java/org/apache/maven/surefire/testng/utils/GroupMatcherMethodSelector.java

%pom_remove_dep -r org.apache.maven.surefire:surefire-shadefire

# Help plugin is needed only to evaluate effective Maven settings.
# For building RPM package default settings will suffice.
%pom_remove_plugin :maven-help-plugin surefire-its

# QA plugin useful only for upstream
%pom_remove_plugin -r :jacoco-maven-plugin
# Not wanted
%pom_remove_plugin -r :maven-shade-plugin
# Not in Fedora
%pom_remove_plugin -r :animal-sniffer-maven-plugin
# Complains
%pom_remove_plugin -r :apache-rat-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
# We don't need site-source
%pom_remove_plugin :maven-assembly-plugin maven-surefire-plugin
%pom_remove_dep -r ::::site-source

%build
%{mvn_package} ":*{surefire-plugin}*" @1
%{mvn_package} ":*junit-platform*" junit5
%{mvn_package} ":*{junit,testng,failsafe-plugin}*"  @1
%{mvn_package} ":*tests*" __noinstall
# tests turned off because they need jmock
%{mvn_build} -f -- -DcommonsIoVersion=2.8.0 -DcommonsLang3Version=3.11

%install
%{mvn_install}

%files -f .mfiles
%doc README.md
%license LICENSE NOTICE cpl-v10.html

%files plugin -f .mfiles-surefire-plugin

%files provider-junit -f .mfiles-junit

%files provider-junit5 -f .mfiles-junit5

%files provider-testng -f .mfiles-testng

%files -n maven-failsafe-plugin -f .mfiles-failsafe-plugin

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE cpl-v10.html

%changelog
* Fri Mar 24 2023 Riken Maharjan <rmaharjan@microsoft.com> - 3.0.0-1
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0~M4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0~M4-2
- Bootstrap build
- Non-bootstrap build

* Fri May 14 2021 Marian Koncek <mkoncek@redhat.com> - 3.0.0~M4-1
- Update to upstream version 3.0.0~M4

* Fri Feb 05 2021 Fabio Valentini <decathorpe@gmail.com> - 0:3.0.0~M4-1
- Update to version 3.0.0-M4.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.22.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 15 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.22.0-10
- Add boolean dependencies between plugin and provider subpackages

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.22.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 0:2.22.0-8
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Mar 25 2020 Severin Gehwolf <sgehwolf@redhat.com> - 0:2.22.0-7
- Add maven-compat dependency in maven-surefire-common for ArtifactResolver
  class.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.22.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0~M3-4
- Mass rebuild for javapackages-tools 201902

* Mon Oct 28 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0~M3-3
- Enable JUnit 5 provider

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.22.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0~M3-2
- Mass rebuild for javapackages-tools 201901

* Mon May 13 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0~M3-1
- Switch to tilde versioning

* Sat Apr 13 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.0-0.1.M3
- Update to upstream 3.0.0-M3 milestone snapshot

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.22.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Michael Simacek <msimacek@redhat.com> - 0:2.22.0-3
- Repack the tarball without binaries

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Michael Simacek <msimacek@redhat.com> - 0:2.22.0-1
- Update to upstream version 2.22.0

* Fri Mar 16 2018 Michael Simacek <msimacek@redhat.com> - 0:2.21.0-1
- Update to upstream version 2.21.0

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.20.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 18 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.20.1-3
- Remove temporary build-requires

* Mon Sep 18 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.20.1-2
- Add missing requires on procps-ng

* Mon Sep 18 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.20.1-1
- Update to upstream version 2.20.1

* Tue Sep 12 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.20-1
- Update to upstream version 2.20

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.19.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.19.1-7
- Port to TestNG 6.11
- Resolves: rhbz#1469005

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.19.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.19.1-5
- Don't use Maven 2 toolchain

* Thu Jun 30 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.19.1-4
- Compile against Maven 3 APIs

* Thu May 05 2016 Michael Simacek <msimacek@redhat.com> - 0:2.19.1-3
- Fix FTBFS after doxia 1.7 update

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan  4 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.19.1-1
- Update to upstream version 2.19.1

* Mon Oct 19 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.19-1
- Update to upstream version 2.19

* Mon Jul 13 2015 Michael Simacek <msimacek@redhat.com> - 0:2.18.1-2
- Fix FTBFS

* Thu Jun 25 2015 Michael Simacek <msimacek@redhat.com> - 0:2.18.1-1
- Update to upstream version 2.18.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Oct 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.17-6
- Remove legacy Obsoletes/Provides for maven2 plugin

* Thu Jun 19 2014 Michal Srb <msrb@redhat.com> - 0:2.17-5
- Fix maven-parent BR

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.17-3
- Rebuild to regenerate file lists

* Thu May 22 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.17-2
- Drop junit4 virtual provide

* Mon Mar 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.17-1
- Update to upstream version 2.17

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.16-3
- Use Requires: java-headless rebuild (#1067528)

* Fri Feb 21 2014 Michal Srb <msrb@redhat.com> - 0:2.16-2
- Remove dep on maven-compat

* Mon Aug 19 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.16-1
- Update to upstream version 2.16

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 18 2013 Michal Srb <msrb@redhat.com> - 0:2.15-1
- Update to upstream version 2.15

* Thu May  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.14.1-2
- Remove unneeded BR
- Resolves: rhbz#961467

* Mon Apr 15 2013 Michal Srb <msrb@redhat.com> - 0:2.14.1-1
- Update to upstream version 2.14.1

* Fri Apr 05 2013 Michal Srb <msrb@redhat.com> - 0:2.14-3
- Remove unnecessary dependency on mockito

* Fri Mar 15 2013 Michal Srb <msrb@redhat.com> - 0:2.14-2
- Remove unneeded dependencies

* Fri Mar 15 2013 Michal Srb <msrb@redhat.com> - 0:2.14-1
- Update to upstream version 2.14

* Thu Mar  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.13-4
- Add missing BR: mockito

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0:2.13-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.13-2
- Get rid of custom depmap

* Wed Jan 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.13-1
- Update to upstream version 2.13

* Fri Dec 21 2012 Michal Srb <msrb@redhat.com> - 0:2.12.4-8
- Migrated from maven-doxia to doxia subpackages (Resolves: #889149)

* Fri Dec 14 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-7
- Fix Provides: maven-surefire-provider-junit4

* Fri Dec 14 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-6
- Merge junit3 and junit4 providers
- Disable dependency on shadefire

* Mon Dec 10 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-5
- Enable xmvn auto-requires

* Thu Nov 29 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-4
- Build with xmvn

* Thu Nov 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-3
- Add CPL license

* Mon Oct 22 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-2
- Add maven depmap for org.beanshell:bsh

* Fri Oct  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.4-1
- Update to upstream version 2.12.4

* Tue Sep 25 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.3-1
- Update to upstream version 2.12.3

* Mon Aug 13 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.2-1
- Update to upstream version 2.12.2

* Fri Aug  3 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.12.1-1
- Update to upstream version 2.12.1
- Install LICENSE and NOTICE files
- Remove RPM bug workaround

* Fri Jul 27 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.12-5
- Fix build problem and rebuild with target 1.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 Jaromir Capik <jcapik@redhat.com> - 0:2.12-3
- Removing bootstrap condition for Patch1 inclusion (always needed in SRPM)

* Thu Mar 01 2012 Jaromir Capik <jcapik@redhat.com> - 0:2.12-2
- Update to 2.12

* Thu Mar 01 2012 Jaromir Capik <jcapik@redhat.com> - 0:2.12-1
- Bootstrap for 2.12

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.10-4
- Move poms and depmaps to respective sub-packages
- Add requires on junit provider to maven-plugin

* Wed Oct  5 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.10-3
- Fix junit4 depmap provider macro
- Remove unused patches

* Sun Oct 2 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.10-2
- BR maven-enforcer-plugin.

* Sun Oct 2 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.10-1
- Update to latest upstream - 2.10.
- Use new maven macro.

* Mon Jun 27 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.9-1
- Update to latest upstream (2.9)
- Fix up Requires for juni4 provider

* Tue May 24 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.8.1-4
- Fix up providers artifact and report plugin groupid

* Tue May 24 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.8.1-3
- Fix maven-surefire-plugin group in the depmap.

* Fri May 13 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.8.1-2
- Install testng-utils jar and pom

* Mon Apr 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.8.1-1
- Update to latest upstream version (2.8.1)

* Tue Mar 29 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.8-1
- Update to latest upstream version (2.8)

* Mon Mar  7 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.7.2-1
- Update to latest version (2.7.2)
- Add common-junit* jars to distribution
- Versionless javadocs
- Use maven 3 to build

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 3 2011 Alexander Kurtakov <akurtako@redhat.com> 0:2.7.1-2
- Fix junit3 depmap.

* Wed Dec 29 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.7.1-1
- Update to 2.7.1.

* Wed Dec  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-3
- Add proper Requires on junit/junit4/testng to providers

* Fri Oct 29 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-2
- Add main pom.xml

* Mon Aug 30 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.6-1
- Rename subpackages to not repeat "maven" twice
- Update to latest upstream version
- Add common jar to files
- Introduce maven-failsafe-plugin sub-package
- Cleanups

* Mon Aug 31 2009 Andrew Overholt <overholt@redhat.com> 0:2.3-7.7
- Bump release to rebuild

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.6
- Really remove maven2-plugin-surefire BR.

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.5
- Revert previous change.

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.4
- Disable not needed BRs.

* Mon Aug 31 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.3
- Install JPP.maven2.plugins-surefire-plugin.pom now that we have maven 2.0.8.

* Wed Aug 19 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.2
- Don't install JPP.maven2.plugins-surefire-plugin.pom to fix conflict with maven2 2.0.4.

* Tue Aug 18 2009 Alexander Kurtakov <akurtako@redhat.com> 0:2.3-7.1
- Update to 2.3 - sync with jpackage.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.3-4.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.3-3.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 13 2008 Deepak Bhole <dbhole@redhat.com> 1.5.3-2.8
- Build for ppc64

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.3-2.7
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.3-2jpp.6
- fix license tag

* Thu Feb 28 2008 Deepak Bhole <dbhole@redhat.com> 1.5.3-2jpp.5
- Rebuild

* Fri Sep 21 2007 Deepak Bhole <dbhole@redhat.com> 1.5.3-2jpp.4
- Build with maven
- ExcludeArch ppc64

* Fri Aug 31 2007 Deepak Bhole <dbhole@redhat.com> 0:1.5.3-2jpp.3
- Build without maven (for initial ppc build)

* Tue Mar 20 2007 Deepak Bhole <dbhole@redhat.com> 0:1.5.3-2jpp.2
- Build with maven

* Mon Feb 26 2007 Tania Bento <tbento@redhat.com> 0:1.5.3-2jpp.1
- Fixed %%Release.
- Fixed %%BuildRoot.
- Removed %%Vendor.
- Removed %%Distribution.
- Removed period at the end of %%Summary.
- Removed %%post and %%postun sections for javadoc.
- Removed %%post and %%postun sections for booter-javadoc.
- Added gcj support option.
- Fixed instructions on how to generate source drop.

* Tue Oct 17 2006 Deepak Bhole <dbhole@redhat.com> 1.5.3-2jpp
- Update for maven2 9jpp

* Mon Jun 19 2006 Deepak Bhole <dbhole@redhat.com> - 0:1.5.3-1jpp
- Initial build
