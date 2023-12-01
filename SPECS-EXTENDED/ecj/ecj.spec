Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package ecj
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%global qualifier R-4.12-201906051800
%global jdk10_revision 45b1d041a4ef
Name:           ecj
Version:        4.12
Release:        5%{?dist}
Summary:        Eclipse Compiler for Java
License:        EPL-2.0
Group:          Development/Libraries/Java
URL:            https://www.eclipse.org
Source0:        http://download.eclipse.org/eclipse/downloads/drops4/%{qualifier}/ecjsrc-%{version}.jar
# Jdk10 sources to build Java API stubs for newer JDKs
# wget http://hg.openjdk.java.net/jdk-updates/jdk10u/archive/45b1d041a4ef.tar.bz2 -O jdk10u.tar.bz2
# tar xf jdk10u.tar.bz2 && rm jdk10u.tar.bz2
# mv jdk10u-45b1d041a4ef/src/java.compiler/share/classes java10api-src && rm -rf jdk10u-45b1d041a4ef
# tar cJf java10api-src.tar.xz java10api-src && rm -rf java10api-src
Source1:        java10api-src.tar.xz
Source2:        https://repo1.maven.org/maven2/org/eclipse/jdt/ecj/3.18.0/ecj-3.18.0.pom
# Simple pom file to declare org.eclipse:java10api artifact
Source3:        java10api.pom
# Extracted from https://www.eclipse.org/downloads/download.php?file=/eclipse/downloads/drops4/%%{qualifier}/ecj-%%{version}.jar
Source4:        MANIFEST.MF
# Always generate debug info when building RPMs
Patch0:         %{name}-rpmdebuginfo.patch
# Fix build with java >= 9
Patch2:         ecj-encoding.patch
# Patch out deprecation annotation not understood by java 8
Patch3:         jdk10u-jdk8compat.patch
BuildRequires:  ant
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  unzip
BuildArch:      noarch

%description
ECJ is the Java bytecode compiler of the Eclipse Platform.  It is also known as
the JDT Core batch compiler.

%prep
%setup -q -c -a 1
%patch0 -p1
%patch2 -p1
%patch3

sed -i -e 's|debuglevel=\"lines,source\"|debug=\"yes\"|g' build.xml

mkdir -p scripts/binary/META-INF/
cp %{SOURCE4} scripts/binary/META-INF/MANIFEST.MF

# JDTCompilerAdapter isn't used by the batch compiler
rm -f org/eclipse/jdt/core/JDTCompilerAdapter.java

%build

mkdir -p build/classes
javac -d build/classes -source 8 -target 8 \
  $(find java10api-src/javax -name \*.java | xargs)
jar -cf java10api.jar -C build/classes .
# Remove everything except the jar, since ant looks for java files in "."
rm -rf java10api-src build/classes

ant build

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 ecj.jar %{buildroot}%{_javadir}/%{name}/ecj.jar
install -pm 0644 java10api.jar %{buildroot}%{_javadir}/%{name}/java10api.jar

# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/%{name}/ecj.pom
%add_maven_depmap %{name}/ecj.pom %{name}/ecj.jar -a "org.eclipse.jdt:core,org.eclipse.jdt.core.compiler:ecj,org.eclipse.tycho:org.eclipse.jdt.core,org.eclipse.tycho:org.eclipse.jdt.compiler.apt"
install -pm 0644 %{SOURCE3} %{buildroot}%{_mavenpomdir}/%{name}/java10api.pom
%add_maven_depmap %{name}/java10api.pom %{name}/java10api.jar -a "org.eclipse:java9api"

# Install the ecj wrapper script
%jpackage_script org.eclipse.jdt.internal.compiler.batch.Main '' '' ecj ecj true

# Install manpage
mkdir -p %{buildroot}%{_mandir}/man1
install -m 644 -p ecj.1 %{buildroot}%{_mandir}/man1/ecj.1

%files -f .mfiles
%license about.html
%{_bindir}/ecj
%{_mandir}/man1/ecj*

%changelog
* Fri Feb 18 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.12-5
- Removing Java < 9 parts.
- License verified.

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 4.12-4
- Remove epoch

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:4.12-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Mar 25 2021 Olivia Crain <oliviacrain@microsoft.com> - 1:4.12-2.5
- Set epoch to 1 to match Fedora's ecj epoch

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 4.12-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Wed Sep 25 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to eclipse 4.12 ecj
- Removed patches:
  * ecj-include-props.patch,
  * eclipse-gcj-compat4.2.1.patch
  * eclipse-gcj-nodummysymbol.patch
    + Unneeded for this version
- Added patches:
  * ecj-encoding.patch
    + Fix build with java >= 9
  * javaAPI.patch
    + When building with java < 9, add the java10api.jar and the
    JRE's rt.jar to bootclasspath
  * jdk10u-jdk8compat.patch
    + Patch out deprecation annotation not understood by the JDK
    when building with java < 9
- Build the java.compiler module's javax.* packages as non-modular
  java10api.jar, so that ecj can be compiled even with java < 9
- Distribute the java10api artifact for packages that might need
  it
* Thu Nov 22 2018 Fridrich Strba <fstrba@suse.com>
- Add one more maven artifact alias:
  * org.eclipse.tycho:org.eclipse.jdt.compiler.apt
* Mon Oct 29 2018 Fridrich Strba <fstrba@suse.com>
- Add two more maven artifact aliases:
  * org.eclipse.jdt.core.compiler:ecj
  * org.eclipse.jdt:ecj
* Mon Sep 18 2017 fstrba@suse.com
- Don't build against the java-bootstrap package; it is gone
* Fri May 19 2017 tchvatal@suse.com
- Fix build with javapackages-tools
* Thu Sep 10 2015 tchvatal@suse.com
- Fix cycles on Leap which is 1315 same as SLE.
- Sort deps with spec-cleaner
* Fri Sep 19 2014 dmacvicar@suse.de
- avoid cycles in Factory with Java 8
* Thu Sep 18 2014 dmacvicar@suse.de
- Remove upstream git URL for MANIFEST.MF as it is not
  versioned. File will change and Factory bots will
  complain.
* Thu Sep 18 2014 dmacvicar@suse.de
- restore bootstrap dependencies
- Restored patches and GCJ Main, as they are used
  to bootstrap other packages.
  * eclipse-gcj-compat4.2.1.patch
  * eclipse-gcj-nodummysymbol.patch
- Removed obsolete ecj-native, as old SUSE package did
  not had it and no package provides it
* Wed Sep 17 2014 dmacvicar@suse.de
- clean spec file
* Mon Sep 15 2014 dmacvicar@suse.de
- export NO_BRP_CHECK_BYTECODE_VERSION
* Mon Sep 15 2014 dmacvicar@suse.de
- Update to ecj 4.2.1 (expected by tomcat 7.0.55+)
- Sync with Fedora ecj-4.4
- Drop gcj patches
  * eclipse-gcj-nodummysymbol.patch
- Drop obsolete patches
  * ecj-generatedebuginfo.patch : now done in spec
  * eclipse-gcj-compat4.2.1.patch
  * ecj-defaultto1.5.patch : we can use 1.6
* Wed Sep  3 2014 tchvatal@suse.com
- Spec-cleaner
- BuildIgnore java-devel pkgs to avoid conflicts
* Wed Sep  3 2014 coolo@suse.com
- on 13.2 and Factory build against bootstrap java
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Fri May 31 2013 varkoly@suse.com
- Fix the spec to avoid fileconflicts with ecj-bootstrap
* Mon Jan 21 2013 mvyskocil@suse.com
- Update to ecj 4.2.1 (expected by tomcat 7.0.34+)
  (no changelog provided, but it's normal for eclipse)
- sync with fedora 4.2.1-3
  * ecj-defaultto1.5.patch - change the default -source to 1.5 to
    match gcc-java capabilities
  * ecj-generatedebuginfo.patch - generate debug info for java sources
  * ecj-include-props.patch - package .props files too
  * ecj-rpmdebuginfo.patch - hack, force debuginfo to be created when
    RPM_BUILD_ROOT variable is defined
  * eclipse-gcj-compat4.2.1.patch - disable all expected warning
  * eclipse-gcj-nodummysymbol.patch - don't generate dummy entry in jars
  * eclipse-jpackage-changelog.txt
* Sun Sep 18 2011 jengelh@medozas.de
- Remove redundant/obsolete tags/sections from specfile
  (cf. packaging guidelines)
* Thu Nov 22 2007 anosek@suse.cz
- new package, initial version 3.3
