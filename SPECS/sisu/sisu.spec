%bcond_without bootstrap
Summary:        Eclipse dependency injection framework
Name:           sisu
Version:        0.3.5
Release:        6%{?dist}
# sisu is EPL-1.0, the bundled asm is BSD
License:        EPL-1.0 AND BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://eclipse.org/sisu/
Source0:        https://github.com/eclipse/sisu.inject/archive/refs/tags/releases/%{version}.tar.gz#/org.eclipse.sisu.inject-%{version}.tar.gz
Source1:        https://github.com/eclipse/sisu.plexus/archive/refs/tags/releases/%{version}.tar.gz#/org.eclipse.sisu.plexus-%{version}.tar.gz
Source100:      sisu-parent.pom
Source101:      sisu-inject.pom
Source102:      sisu-plexus.pom
Patch0:         sisu-OSGi-import-guava.patch
Patch2:         sisu-ignored-tests.patch
Patch3:         sisu-osgi-api.patch
Patch4:         0001-Remove-dependency-on-glassfish-servlet-api.patch
BuildRequires:  javapackages-bootstrap
BuildRequires:  javapackages-local-bootstrap
Provides:       %{name}-inject = %{version}-%{release}
Provides:       %{name}-plexus = %{version}-%{release}
Provides:       bundled(objectweb-asm)
BuildArch:      noarch

%description
Java dependency injection framework with backward support for plexus and bean
style dependency injection.

%{?javadoc_package}

%prep
%setup -q -c -T
tar xf %{SOURCE0} && mv sisu.inject-releases-* sisu-inject
tar xf %{SOURCE1} && mv sisu.plexus-releases-* sisu-plexus

cp %{SOURCE100} pom.xml
cp %{SOURCE101} sisu-inject/pom.xml
cp %{SOURCE102} sisu-plexus/pom.xml

%patch 0
%patch 2
%patch 3
%patch 4 -p1

%pom_remove_dep :servlet-api sisu-inject

%pom_xpath_set -r /pom:project/pom:version %{version}

%{mvn_file} ":{*}" @1
%{mvn_package} ":*{inject,plexus}"
%{mvn_package} : __noinstall
%{mvn_alias} :org.eclipse.sisu.plexus org.sonatype.sisu:sisu-inject-plexus org.codehaus.plexus:plexus-container-default

%build
%{mvn_build} -X  -- -Dmaven.compiler.source=17 -Dmaven.compiler.target=17 -Dmaven.javadoc.source=17 -Dmaven.compiler.release=17

%install
%{mvn_install}

%files -f .mfiles
%license sisu-inject/LICENSE.txt

%changelog
* Thu Mar 21 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.3.5-6
- Increase Junit version to match with the bootstrap's Junit using Fedora 40 (License: MIT)

* Fri Feb 23 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.3.5-5
- Rebuilt with msopenjdk-17
- change source, target and release version

* Fri Mar 24 2023 Riken Maharjan <rmaharjan@microsoft.com> - 0.3.5-4
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 09 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.5-1
- Update to upstream version 0.3.5

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1:0.3.4-9
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 01 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.4-6
- Fix obsoletes on removed subpackages

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.4-5
- Bootstrap build
- Non-bootstrap build

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1:0.3.4-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Feb 13 2020 Fabio Valentini <decathorpe@gmail.com> - 1:0.3.4-1
- Update to version 0.3.4.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.3.4-2
- Build with OpenJDK 8

* Wed Nov 06 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.3.4-1
- Update to upstream version 0.3.4

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 0.3.3-9
- Mass rebuild for javapackages-tools 201902

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.3-8
- Merge inject and plexus subpackages

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.3-7
- Mass rebuild for javapackages-tools 201901

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 24 2018 Michael Simacek <msimacek@redhat.com> - 1:0.3.3-6
- Declare bundled objectweb-asm
- Fix license tag to include BSD for asm

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul  2 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.3-4
- Update license tag

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 11 2017 Michael Simacek <msimacek@redhat.com> - 1:0.3.3-1
- Update to upstream version 0.3.3

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 29 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.2-6
- Restore alias for org.sonatype.sisu:sisu-inject-plexus

* Sun Jan 29 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.2-5
- Build without Tycho
- Remove sisu-tests subpackage
- Drop old obsoletes

* Mon Feb 22 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.2-4
- Add alias for org.sonatype.sisu:sisu-inject-plexus

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan  7 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.2-2
- Remove unneeded patch

* Wed Sep 16 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.2-1
- Update to upstream version 0.3.2

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.1-1
- Update to upstream version 0.3.1

* Thu Apr 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.0-2
- Install test artifacts

* Mon Feb 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.0-1
- Update to upstream version 0.3.0

* Wed Feb 18 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.0-0.2.M1
- Unbundle ASM
- Resolves: rhbz#1085903

* Wed Feb  4 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.3.0-0.1.M1
- Update to upstream milestone 0.3.0.M1

* Tue Sep 30 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.2.1-10
- Port to plexus-utils 3.0.18

* Thu Sep 18 2014 Michal Srb <msrb@redhat.com> - 1:0.2.1-9
- Rebuild to fix metadata
- Remove explicit Requires

* Fri Sep 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.2.1-8
- Update to latest XMvn version
- Enable tests

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.2.1-7
- Fix build-requires on sonatype-oss-parent

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.2.1-5
- Install JARs and POMs only

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.2.1-4
- Build with XMvn 2.0.0

* Wed May 07 2014 Michael Simacek <msimacek@redhat.com> - 1:0.2.1-3
- Build with Java 8

* Wed Apr 23 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.2.1-2
- Import guava in OSGi manifest

* Tue Apr 22 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.2.1-1
- Update to upstream version 0.2.1
- Remove patch for Eclipse bug 429369

* Wed Apr 16 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.2.0-5
- Update upstream patch for bug 429369
- Force usage of Java 1.7

* Mon Mar  3 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.2.0-4
- Revert upstream feature which introduced a regression
- Resolves: rhbz#1070915

* Thu Feb 20 2014 Michal Srb <msrb@redhat.com> - 1:0.2.0-3
- Remove R on cdi-api

* Thu Feb 20 2014 Michal Srb <msrb@redhat.com> - 1:0.2.0-2
- Update BR/R for version 0.2.0
- Enable tests

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.2.0-1
- Update to upstream version 0.2.0

* Wed Dec  4 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.1.1-1
- Update to upstream version 0.1.1

* Wed Nov 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.1.0-1
- Update to upstream version 0.1.0

* Wed Oct 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.0.0-0.7.M5
- Rebuild to regenerate broken POMs
- Related: rhbz#1021484

* Fri Oct 18 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.0.0-0.6.M5
- Don't inject pom.properties

* Wed Sep 25 2013 Michal Srb <msrb@redhat.com> - 1:0.0.0-0.5.M5
- Update to upstream version 0.0.0.M5
- Install EPL license file
- Inject pom.properties
- Regenerate BR
- Add R

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.0.0-0.4.M4
- Update to XMvn 1.0.0

* Tue Aug 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.0.0-0.3.M4
- Obsolete sisu main package, resolves: rhbz#996288

* Tue Jul 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.0.0-0.2.M4
- Remove unneeded provides and compat symlinks

* Mon Jul 22 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:0.0.0-0.1.M4
- Update to upstream version 0.0.0.M4

* Wed Mar 27 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3.0-8
- Remove unneeded animal-sniffer BuildRequires
- Add forge-parent to BuildRequires to ensure it's present

* Thu Mar 14 2013 Michal Srb <msrb@redhat.com> - 2.3.0-7
- sisu-inject-bean: add dependency on asm
- Fix dependencies on javax.inject and javax.enterprise.inject
- Remove bundled JARs and .class files from tarball

* Thu Feb  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-6
- Add ASM dependency only to a single module, not all of them
- Disable animal-sniffer plugin
- Don't generate auto-requires for optional dependencies

* Wed Feb 06 2013 Tomas Radej <tradej@redhat.com> - 2.3.0-5
- Added BR on animal-sniffer

* Tue Feb 05 2013 Tomas Radej <tradej@redhat.com> - 2.3.0-4
- Split into subpackages
- Build with new macros
- Unbundled objectweb-asm

* Wed Dec  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-3
- Fix OSGi __requires_exclude

* Wed Dec  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-2
- Disable OSGi auto-requires: org.sonatype.sisu.guava

* Mon Dec  3 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.0-1
- Update to upstream version 2.3.0

* Tue Jul 24 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.3-6
- Convert patches to POM macros

* Mon Jul 23 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.2.3-5
- Fix license tag

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 19 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.3-2
- Add backward compatible package path for lifecycles
- Remove temporary BRs/Rs

* Thu Jun 23 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.2.3-1
- Update to latest upstream 2.2.3 (#683795)
- Add forge-parent to Requires
- Rework spec to be more simple, update patches

* Tue Mar  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1.1-2
- Add atinject into poms as dependency

* Mon Feb 28 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.1.1-1
- Update to 2.1.1
- Update patch
- Disable guice-eclipse for now

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.3.2-1
- Update to latest upstream version
- Versionless jars & javadocs

* Mon Oct 18 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.2-2
- Add felix-framework BR

* Thu Oct 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4.2-1
- Initial version of the package
