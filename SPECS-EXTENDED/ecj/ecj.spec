Epoch: 1

%global eclipse_ver 4.23
%global bundle_ver 3.29.0
%global jar_ver %{eclipse_ver}
%global drop R-%{jar_ver}-202203080310

Summary: Eclipse Compiler for Java
Name: ecj
Version: %{eclipse_ver}
Release: 11%{?dist}
URL: https://www.eclipse.org
License: EPL-2.0

Source0: https://download.eclipse.org/eclipse/downloads/drops4/%{drop}/ecjsrc-%{jar_ver}.jar
Source1: https://repo1.maven.org/maven2/org/eclipse/jdt/ecj/%{bundle_ver}/ecj-%{bundle_ver}.pom
# The ecj build does not generate a proper manifest, so use the one from the binary distribution
# Extracted from: https://download.eclipse.org/eclipse/downloads/drops4/%%{drop}/ecj-%%{jar_ver}.jar
Source2: MANIFEST.MF

# Always generate debug info when building RPMs (Andrew Haley)
Patch0: 0001-Always-generate-bytecode-debuginfo.patch

BuildArch: noarch
ExclusiveArch:  %{java_arches} noarch

BuildRequires: ant
BuildRequires: javapackages-local
BuildRequires: java-devel >= 1:11

# Explicit requires for javapackages-tools since ecj
# uses /usr/share/java-utils/java-functions
Requires:       javapackages-tools

%description
ECJ is the Java bytecode compiler of the Eclipse Platform.  It is also known as
the JDT Core batch compiler.

%prep
%autosetup -p1 -c -n %{name}-%{eclipse_ver}

# Specify encoding
sed -i -e '/compilerarg/s/Xlint:none/Xlint:none -encoding cp1252/' build.xml

cp %{SOURCE1} pom.xml
mkdir -p scripts/binary/META-INF/
cp %{SOURCE2} scripts/binary/META-INF/MANIFEST.MF

# Aliases
%mvn_alias org.eclipse.jdt:ecj org.eclipse.jdt:core org.eclipse.jdt.core.compiler:ecj \
  org.eclipse.tycho:org.eclipse.jdt.core org.eclipse.tycho:org.eclipse.jdt.compiler.apt

%build
export JAVA_HOME=/usr/lib/jvm/java
ant

%install
%mvn_artifact pom.xml ecj.jar
%mvn_install

# Install the ecj wrapper script
%jpackage_script org.eclipse.jdt.internal.compiler.batch.Main '' '' ecj ecj true

# Install manpage
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 -p ecj.1 $RPM_BUILD_ROOT%{_mandir}/man1/ecj.1

%files -f .mfiles
%license about.html
%{_bindir}/ecj
%{_mandir}/man1/ecj*

%changelog
* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.23-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 22 2024 Marian Koncek <mkoncek@redhat.com> - 1:4.23-10
- Add Requires on javapackages-tools

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 1:4.23-9
- Rebuilt for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1:4.23-6
- Build with default Java version

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 1:4.23-2
- Rebuilt for Drop i686 JDKs

* Fri Apr 01 2022 Mat Booth <mat.booth@gmail.com> - 1:4.23-1
- Update to latest upstream release

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 1:4.22-3
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 06 2021 Mat Booth <mat.booth@gmail.com> - 1:4.22-1
- Update to latest upstream release

* Wed Sep 15 2021 Mat Booth <mat.booth@gmail.com> - 1:4.21-1
- Update to latest upstream release
- Drop build requirement on Java 8, ecj now requires Java 11

* Wed Aug 25 2021 Stefan Bluhm <stefan.bluhm@clacee.eu> - 1:4.19-3
- Added RHEL8 build.

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 10 2021 Mat Booth <mat.booth@redhat.com> - 1:4.19-1
- Update to latest upstream release

* Mon Mar 01 2021 Mat Booth <mat.booth@redhat.com> - 1:4.18-3
- Allow building against Java 11

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Alexander Kurtakov <akurtako@redhat.com> 1:4.18-1
- Update to latest upstream release.

* Thu Oct 29 2020 Mat Booth <mat.booth@redhat.com> - 1:4.17-1
- Update to latest upstream release

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1:4.16-3
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Fri Jun 19 2020 Mat Booth <mat.booth@redhat.com> - 1:4.16-2
- Restore compiler adaptor

* Thu Jun 18 2020 Mat Booth <mat.booth@redhat.com> - 1:4.16-1
- Update to latest upstream release

* Fri Mar 20 2020 Mat Booth <mat.booth@redhat.com> - 1:4.15-1
- Update to latest upstream release

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 16 2019 Mat Booth <mat.booth@redhat.com> - 1:4.14-2
- Remove upstream code-signatures

* Fri Dec 13 2019 Mat Booth <mat.booth@redhat.com> - 1:4.14-1
- Update to latest upstream version

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 29 2019 Mat Booth <mat.booth@redhat.com> - 1:4.12-1
- Update to latest upstream release

* Thu Mar 07 2019 Mat Booth <mat.booth@redhat.com> - 1:4.11-0.1
- Update to latest release candidate of 4.11

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 11 2018 Mat Booth <mat.booth@redhat.com> - 1:4.10-1
- Update to 2018-12 release

* Wed Sep 12 2018 Mat Booth <mat.booth@redhat.com> - 1:4.9-1
- Update to latest release
- Amend license tag

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.3a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 09 2018 Mat Booth <mat.booth@redhat.com> - 1:4.7.3a-1
- Update to Oxygen.3a release for java 10 support
- Break circular dep on JDT by providing the java API stubs in this package

* Tue Mar 20 2018 Mat Booth <mat.booth@redhat.com> - 1:4.7.3-1
- Update to Oxygen.3

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Sep 21 2017 Mat Booth <mat.booth@redhat.com> - 1:4.7.1-1
- Update to Oxygen.1 release

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 15 2017 Michael Simacek <msimacek@redhat.com> - 1:4.6.3-2
- Update aliases for jetty

* Wed Mar 29 2017 Mat Booth <mat.booth@redhat.com> - 1:4.6.3-1
- Update to Neon.3 release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Mat Booth <mat.booth@redhat.com> - 1:4.6.2-1
- Update to Neon.2 release

* Fri Jul 01 2016 Mat Booth <mat.booth@redhat.com> - 1:4.6-1
- Update to Neon release

* Tue Apr 26 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.5.2-3
- Re-add alias for org.eclipse.jdt:core

* Fri Apr 22 2016 Mat Booth <mat.booth@redhat.com> - 1:4.5.2-2
- Drop aliases that are now provided by eclipse-jdt

* Mon Feb 29 2016 Mat Booth <mat.booth@redhat.com> - 1:4.5.2-1
- Update to Mars.2 release

* Fri Feb 05 2016 Mat Booth <mat.booth@redhat.com> - 1:4.5.1-3
- Allow any compression man pages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 06 2015 Mat Booth <mat.booth@redhat.com> - 1:4.5.1-1
- Update to Mars.1 release

* Thu Jul 2 2015 Alexander Kurtakov <akurtako@redhat.com> 1:4.5-1
- Update to upstream 4.5 release.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 30 2015 Mat Booth <mat.booth@redhat.com> - 1:4.4.2-1
- Update to 4.4.2.
- Install with mvn_install
- Add jetty.orbit alias
- Add compiler.apt aliases
- Drop ancient obsoletes/provides on eclipse-ecj
- Use man page from upstream source

* Thu Jan 8 2015 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.1-1
- Update to 4.4.1.

* Thu Jul 3 2014 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.0-1
- Update to 4.4 final.
- Drop gcj patches as gcj is not in Fedora anymore and ecj now requires 1.6.

* Thu Jun 12 2014 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.0-0.4.git20140430
- Add additional depmap for maven.

* Mon Jun 9 2014 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.0-0.3.git20140430
- Fix FTBFS.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.4.0-0.2.git20140430
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 1 2014 Alexander Kurtakov <akurtako@redhat.com> 1:4.4.0-0.1.git20140430
- Update to 4.4.0 I-build to make it cope with Java 8.

* Mon Apr 14 2014 Mat Booth <mat.booth@redhat.com> - 1:4.2.1-10
- Drop gcj AOT-compilation support.
- Obsolete -native sub-package.

* Wed Oct 09 2013 gil cattaneo <puntogil@libero.it> 1:4.2.1-9
- enable build of org/eclipse/jdt/internal/compiler/[apt,tool]
  (ant build mode only), required by querydsl
- remove some rpmlint problems (invalid date)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Jon VanAlten <jon.vanalten@redhat.com> - 4.2.1-7
- Add manpage for ecj executable
- Resolves: rhbz#948442

* Tue Apr  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.1-6
- Add depmap for org.eclipse.jdt.core.compiler:ecj
- Resolves: rhbz#949938

* Wed Mar 06 2013 Karsten Hopp <karsten@redhat.com> 1:4.2.1-5
- add BR java-devel for !with_gcjbootstrap

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Jon VanAlten <jon.vanalten@redhat.com> 1:4.2.1-3
- Patch GCCMain to avoid dummy symbols.

* Wed Oct 10 2012 Krzysztof Daniel <kdaniel@redhat.com> 1:4.2.1-2
- Add depmap satysfying Tycho req.

* Sun Jul 29 2012 Jon VanAlten <jon.vanalten@redhat.com> 1:4.2.1-1
- Update to 4.2.1 upstream version.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-13
- Add missing epoch to native subpackage requires.

* Tue Apr 17 2012 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-12
- Separate gcj in subpackage.

* Mon Jan 16 2012 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-11
- Patch pom file to better represent ecj and not jdt.core .
- Guidelines fixes.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1:3.4.2-8
- Fix add_to_maven_depmap call (Resolves rhbz#655796)

* Mon Dec 21 2009 Deepak Bhole <dbhole@redhat.com> - 1:3.4.2-7
- Fix RHBZ# 490936. If CLASSPATH is not set, add . to default classpath.

* Wed Sep 9 2009 Alexander Kurtakov <akurtako@redhat.com> 1:3.4.2-6
- Add maven pom and depmaps.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 11 2009 Deepak Bhole <dbhole@redhat.com> 1:3.4.2-4
- Add patch to generate full debuginfo for ecj itself

* Tue Mar 10 2009 Deepak Bhole <dbhole@redhat.com> 1:3.4.2-3
- Add BR for aot-compile-rpm

* Tue Mar 10 2009 Deepak Bhole <dbhole@redhat.com> 1:3.4.2-2
- Add BR for ant

* Fri Mar 6 2009 Andrew Overholt <overholt@redhat.com> 1:3.4.2-1
- 3.4.2

* Tue Dec 9 2008 Andrew Overholt <overholt@redhat.com> 1:3.4.1-1
- 3.4.1
- Don't conditionalize building of gcj AOT bits (we're only building
  this for gcj and IcedTea bootstrapping).

* Mon Jan 22 2007 Andrew Overholt <overholt@redhat.com> 3.2.1-1
- Add eclipse-ecj-gcj.patch.

* Fri Jan 12 2007 Andrew Overholt <overholt@redhat.com> 3.2.1-1
- First version for Fedora 7.
- Add BR: java-devel for jar.

* Thu Nov 02 2006 Andrew Overholt <overholt@redhat.com> 1:3.2.1-1jpp
- First version for JPackage.

* Mon Jul 24 2006 Andrew Overholt <overholt@redhat.com> 1:3.2.0-1
- Add versionless ecj.jar symlink in /usr/share/java.

* Wed Jul 19 2006 Andrew Overholt <overholt@redhat.com> 1:3.2.0-1
- 3.2.0.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Mar 07 2005 Andrew Overholt <overholt@redhat.com> 1:3.1.0.M4.9
- Don't build for ppc or ia64.

* Sun Feb 20 2005 Andrew Overholt <overholt@redhat.com> 1:3.1.0.M4.6
- Upgrade back to 3.1M4.
- Don't build for i386 and x86_64.
- Provide eclipse-ecj until we can deprecate this package.

* Fri Jan 14 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.4
- build for all but x86

* Thu Jan 13 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.3
- build for ppc exclusively

* Wed Jan 12 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.2
- Add RPM_OPT_FLAGS workaround.

* Tue Jan 11 2005 Andrew Overholt <overholt@redhat.com> 3.1.0.M4.1
- New version.

* Mon Sep 27 2004 Gary Benson <gbenson@redhat.com> 2.1.3-5
- Rebuild with new katana.

* Thu Jul 22 2004 Gary Benson <gbenson@redhat.com> 2.1.3-4
- Build without bootstrap-ant.
- Split out lib-org-eclipse-jdt-internal-compiler.so.

* Tue Jul  6 2004 Gary Benson <gbenson@redhat.com> 2.1.3-3
- Fix ecj-devel's dependencies.

* Wed Jun  9 2004 Gary Benson <gbenson@redhat.com> 2.1.3-2
- Work around an optimiser failure somewhere in ecj or gcj (#125613).

* Fri May 28 2004 Gary Benson <gbenson@redhat.com>
- Build with katana.

* Mon May 24 2004 Gary Benson <gbenson@redhat.com> 2.1.3-1
- Initial Red Hat Linux build.

* Mon May 24 2004 Gary Benson <gbenson@redhat.com>
- Upgraded to latest version.

* Sun Jul 20 2003 Anthony Green <green@redhat.com>
- Add %%doc

* Fri Jul 18 2003 Anthony Green <green@redhat.com>
- Initial RHUG build.
