# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}

Name:             jboss-logging-tools
Version:          2.2.1
Release:          20%{?dist}
Summary:          JBoss Logging I18n Annotation Processor
# Not available license file https://issues.jboss.org/browse/LOGTOOL-107
# ./annotations/src/main/java/org/jboss/logging/annotations/*.java: Apache (v2.0)
License:          Apache-2.0 and LGPL-2.0-or-later
URL:              https://github.com/jboss-logging/jboss-logging-tools
Source0:          %{url}/archive/%{namedversion}/%{name}-%{namedversion}.tar.gz
Source1:          http://www.apache.org/licenses/LICENSE-2.0.txt
Patch1:           0001-Add-getEnclosingMethod-to-DelegatingExecutableElemen.patch

BuildArch:        noarch
ExclusiveArch:    %{java_arches} noarch

BuildRequires:    maven-local-openjdk25
BuildRequires:    mvn(junit:junit)
BuildRequires:    mvn(org.jboss:jboss-parent:pom:)
BuildRequires:    mvn(org.jboss.jdeparser:jdeparser)
BuildRequires:    mvn(org.jboss.logging:jboss-logging)

%description
This pacakge contains JBoss Logging I18n Annotation Processor

%prep
%autosetup -n %{name}-%{namedversion} -p 1

cp %{SOURCE1} .

# roaster is not packaged for Fedora, so:
# - Remove the dependency
# - Remove the test that requires it
%pom_remove_dep -r org.jboss.forge.roaster:
rm processor/src/test/java/org/jboss/logging/processor/generated/GeneratedSourceAnalysisTest.java

# Skip docs module
%pom_disable_module docs

%build
%mvn_build -f -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE-2.0.txt
%doc README.adoc

%changelog
* Tue Jul 29 2025 jiri vanek <jvanek@redhat.com> - 2.2.1-20
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb 29 2024 Chris Kelley <ckelley@redhat.com> - 2.2.1-16
- Patched to work with java-21-openjdk as system jdk

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2.2.1-15
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 2.2.1-9
- Rebuilt for Drop i686 JDKs

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.2.1-8
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Dogtag PKI Team <pki-devel@redhat.com> - 2.2.1-5
- Drop jboss-logmanager dependency
- Drop jboss-logging-tools-javadoc

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 2.2.1-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Sat May 09 2020 Fabio Valentini <decathorpe@gmail.com> - 2.2.1-1
- Update to version 2.2.1.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Dogtag PKI Team <pki-devel@redhat.com> - 2.2.0-1
- Rebuilt as part of revival process
- BZ#1758293

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 21 2016 gil cattaneo <puntogil@libero.it> 2.0.1-3
- disable test failure

* Mon May 30 2016 gil cattaneo <puntogil@libero.it> 2.0.1-2
- fix license field

* Fri May 27 2016 gil cattaneo <puntogil@libero.it> 2.0.1-1
- update to 2.0.1.Final
- fix BR list and use BR mvn()-like
- fix some rpmlint problem

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-0.4.Beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.3.Beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.2.Beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 09 2013 Marek Goldmann <mgoldman@redhat.com> - 1.2.0-0.1.Beta1
- Upstream release 1.2.0.Beta1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 29 2013 Marek Goldmann <mgoldman@redhat.com> - 1.1.0-1
- Upstream release 1.1.0.Final
- Using new guidelines

* Fri Feb 22 2013 Marek Goldmann <mgoldman@redhat.com> - 1.0.2-1
- Upstream release 1.0.2.Final

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.0-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jul 20 2012 Marek Goldmann <mgoldman@redhat.com> 1.0.0-3
- Fixed BR

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 16 2012 Marek Goldmann <mgoldman@redhat.com> 1.0.0-1
- Upstream release 1.0.0.Final

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.2.CR4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Marek Goldmann <mgoldman@redhat.com> 1.0.0-0.1.CR4
- Upstream release 1.0.0.CR4

* Sun Oct 02 2011 Marek Goldmann <mgoldman@redhat.com> 1.0.0-0.1.CR1
- Upstream release 1.0.0.CR1

* Thu Aug 04 2011 Marek Goldmann <mgoldman@redhat.com> 1.0.0-0.1.Beta7
- Initial packaging

