# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}

Name:             jboss-logging
Version:          3.6.0
Release:          5%{?dist}
Summary:          The JBoss Logging Framework
License:          Apache-2.0

URL:              https://github.com/jboss-logging/jboss-logging
Source0:          %{url}/archive/%{namedversion}/%{name}-%{namedversion}.tar.gz
Patch1:           0001-Drop-log4j-dependency.patch
Patch2:           0002-Drop-jboss-logmanager-dependency.patch
Patch3:           0003-Drop-TestCase-that-depend-on-retired-package.patch

BuildArch:        noarch
ExclusiveArch:    %{java_arches} noarch

BuildRequires:    maven-local-openjdk25
BuildRequires:    mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:    mvn(org.junit:junit-bom:pom:)
BuildRequires:    mvn(org.apache.logging:logging-parent:pom:)
BuildRequires:    mvn(org.slf4j:slf4j-api)

%description
This package contains the JBoss Logging Framework.

%prep
%autosetup -n %{name}-%{namedversion} -p 1

# Unneeded tasks
%pom_remove_dep ch.qos.logback:logback-classic
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin io.github.dmlloyd.module-info:module-info

%pom_set_parent org.apache.logging:logging-parent

%build
# 1.8 is not valid (8 is the accepted form), but @Deprecated requires >= 9
%mvn_build -j -- -Dmaven.compiler.release=11

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 3.6.0-5
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 14 2024 Chris Kelley <ckelley@redhat.com> - 3.6.0-1
- Rebase to version 3.6.0.Final

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 3.5.3-5
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Chris Kelley <ckelley@redhat.com> - 3.5.3-1
- Rebase to version 3.5.3.Final

* Fri Jun 30 2023 Chris Kelley <ckelley@redhat.com> - 3.5.2-1
- Rebase to version 3.5.2.Final

* Tue Jun 06 2023 Chris Kelley <ckelley@redhat.com> - 3.5.1-1
- Rebase to version 3.5.1.Final

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 3.4.1-12
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 3.4.1-11
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Dogtag PKI Team <pki-devel@redhat.com> - 3.4.1-8
- Drop jboss-logmanager dependency

* Fri Jun 04 2021 Dogtag PKI Team <pki-devel@redhat.com> - 3.4.1-7
- Drop log4j dependency
- Drop jboss-logging-javadoc

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 09 2020 Fabio Valentini <decathorpe@gmail.com> - 3.4.1-5
- Switch from log4j 1.2 compat package to log4j 1.2 API shim.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 3.4.1-3
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 05 2019 Fabio Valentini <decathorpe@gmail.com> - 3.4.1-1
- Update to version 3.4.1.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri May 27 2016 gil cattaneo <puntogil@libero.it> 3.3.0-1
- update to 3.3.0.Final

* Sun Feb 14 2016 gil cattaneo <puntogil@libero.it> 3.1.4-6
- fix FTBFS rhbz#1307647
- fix BR list and use BR mvn()-like
- introduce license macro
- fix some rpmlint problem

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 01 2014 Marek Goldmann <mgoldman@redhat.com> - 3.1.4-3
- Upgrade to SLF4j 1.7

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 14 2014 Marek Goldmann <mgoldman@redhat.com> - 3.1.4-1
- Upstream release 3.1.4.GA

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Marek Goldmann <mgoldman@redhat.com> - 3.1.3-1
- Upstream release 3.1.3.GA

* Tue Feb 26 2013 Marek Goldmann <mgoldman@redhat.com> - 3.1.2-1
- Upstream release 3.1.2.GA
- Move to mvn_build and mvn_install macros
- License change to ASL 2.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 3.1.0-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jul 20 2012 Marek Goldmann <mgoldman@redhat.com> - 3.1.0-4
- Fixed BR

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb 26 2012 Marek Goldmann <mgoldman@redhat.com> 3.1.0-2
- Release bump

* Sun Feb 26 2012 Marek Goldmann <mgoldman@redhat.com> 3.1.0-1
- Upstream release 3.1.0.GA
- Relocated jars to _javadir

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-0.2.CR1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Marek Goldmann <mgoldman@redhat.com> 3.1.0-0.1.CR1
- Upstream release 3.1.0.CR1

* Mon Sep 19 2011 Marek Goldmann <mgoldman@redhat.com> 3.0.1-1
- Upstream release 3.0.1.GA

* Thu Jul 28 2011 Marek Goldmann <mgoldman@redhat.com> 3.0.0-1
- Initial packaging

