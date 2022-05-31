#
# spec file for package objectweb-asm
#
# Copyright (c) 2019 SUSE LLC
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

Name:           objectweb-asm
Version:        7.2
Release:        4%{?dist}
Summary:        Java bytecode manipulation framework
License:        BSD-3-Clause
Group:          Development/Libraries/Java
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://asm.ow2.io/
# ./generate-tarball.sh
Source0:        %{_mariner_sources_url}/%{name}-%{version}.tar.xz
Source1:        %{name}-%{version}-build.tar.xz
Source2:        http://repo1.maven.org/maven2/org/ow2/asm/asm/%{version}/asm-%{version}.pom
Source3:        http://repo1.maven.org/maven2/org/ow2/asm/asm-analysis/%{version}/asm-analysis-%{version}.pom
Source4:        http://repo1.maven.org/maven2/org/ow2/asm/asm-commons/%{version}/asm-commons-%{version}.pom
Source5:        http://repo1.maven.org/maven2/org/ow2/asm/asm-test/%{version}/asm-test-%{version}.pom
Source6:        http://repo1.maven.org/maven2/org/ow2/asm/asm-tree/%{version}/asm-tree-%{version}.pom
Source7:        http://repo1.maven.org/maven2/org/ow2/asm/asm-util/%{version}/asm-util-%{version}.pom
# We still want to create an "all" uberjar, so this is a custom pom to generate it
# TODO: Fix other packages to no longer depend on "asm-all" so we can drop this
Source9:        asm-all.pom
# The source contains binary jars that cannot be verified for licensing and could be proprietary
Source10:       generate-tarball.sh
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  xz
Obsoletes:      %{name}-examples
BuildArch:      noarch

%description
ASM is a Java bytecode manipulation framework.

It can be used to dynamically generate stub classes or other proxy
classes, directly in binary form, or to dynamically modify classes at
load time, i.e., just before they are loaded into the Java Virtual
Machine.

ASM offers similar functionalities as BCEL or SERP, but is much
smaller.

%package javadoc
Summary:        Java bytecode manipulation framework
Group:          Documentation/HTML

%description javadoc
ASM is a Java bytecode manipulation framework.

It can be used to dynamically generate stub classes or other proxy
classes, directly in binary form, or to dynamically modify classes at
load time, i.e., just before they are loaded into the Java Virtual
Machine.

ASM offers similar functionalities as BCEL or SERP, but is much
smaller.

%package examples
Summary:        Java bytecode manipulation framework
Group:          Development/Libraries/Java

%description examples
ASM is a Java bytecode manipulation framework.

It can be used to dynamically generate stub classes or other proxy
classes, directly in binary form, or to dynamically modify classes at
load time, i.e., just before they are loaded into the Java Virtual
Machine.

ASM offers similar functionalities as BCEL or SERP, but is much
smaller.

%prep
%setup -q -a1
cp %{SOURCE2} asm/pom.xml
cp %{SOURCE3} asm-analysis/pom.xml
cp %{SOURCE4} asm-commons/pom.xml
cp %{SOURCE5} asm-test/pom.xml
cp %{SOURCE6} asm-tree/pom.xml
cp %{SOURCE7} asm-util/pom.xml
# Insert asm-all pom
mkdir -p asm-all
sed 's/@VERSION@/%{version}/g' %{SOURCE9} > asm-all/pom.xml

for i in asm asm-analysis asm-commons asm-tree asm-util asm-all; do
  %pom_remove_parent ${i}
done

# We don't want to build modular jars
find . -name module-info.java -print -delete

%build
%ant \
    package javadoc

%install
# jars
install -dm 0755 %{buildroot}/%{_javadir}/%{name}
for i in asm asm-analysis asm-commons asm-tree asm-util asm-all; do
  install -pm 0644 ${i}/target/${i}-%{version}.jar %{buildroot}/%{_javadir}/%{name}/${i}.jar
done

# poms
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
for i in asm asm-analysis asm-commons asm-tree asm-util; do
  install -pm 0644 ${i}/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/${i}.pom
  %add_maven_depmap %{name}/${i}.pom %{name}/${i}.jar
done
install -pm 0644 asm-all/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/asm-all.pom
%add_maven_depmap %{name}/asm-all.pom %{name}/asm-all.jar -a org.ow2.asm:asm-debug-all

# javadoc
install -dm 0755 %{buildroot}/%{_javadocdir}/%{name}
for i in asm asm-analysis asm-commons asm-tree asm-util; do
  cp -pr ${i}/target/site/apidocs %{buildroot}/%{_javadocdir}/%{name}/${i}
done
%fdupes -s %{buildroot}/%{_javadocdir}

# script
%jpackage_script org.objectweb.asm.xml.Processor "" "" %{name}/asm:%{name}/asm-util %{name}-processor true

%files -f .mfiles
%license LICENSE.txt
%{_bindir}/%{name}-processor

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Fri Apr 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.2-4
- Fixing source URL.

* Mon Mar 28 2022 Cameron Baird <cameronbaird@microsoft.com> - 7.2-3
- Move to SPECS
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.2-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 7.2-1.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Nov 25 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 7.2
  * Upstream dropped asm-xml submodule
* Wed Mar  6 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 6.2.1
- Generate and customize the ant build system to be able to build
  without gradle
- Removed patches:
  * objectweb-asm-6.0-no_bnd.patch
  * objectweb-asm-6.0-no_retrofit.patch
  * objectweb-asm-6.0-sourcetarget.patch
  * objectweb-asm-6.0-uberjar.patch
    + not needed in this version
* Tue Dec 11 2018 Jan Engelhardt <jengelh@inai.de>
- Update RPM groups
* Tue Dec 11 2018 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 6.0, the last version buildable with ant
- Removed patches:
  * asm-3.3.1-jdk9.patch
  * asm-3.3.1-sourcetarget.patch
  * objectweb-asm-no-classpath-in-manifest.patch
    + Not corresponding any more to the current state of code
- Added patches:
  * objectweb-asm-6.0-no_bnd.patch
    + Don't use bnd (which we don't have) to create bundles
  * objectweb-asm-6.0-no_retrofit.patch
    + Don't retrofit bytecode, since we build with target > 1.5
  * objectweb-asm-6.0-sourcetarget.patch
    + Build with source/target 8
  * objectweb-asm-6.0-uberjar.patch
    + Bring back the uberjars (asm-all.jar and asm-debug-all.jar)
    since some packages might still depend on them
* Wed May 16 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
- Added patch:
  * asm-3.3.1-jdk9.patch
    + Since JDK9, "_" is reserved keyword
* Wed Oct  4 2017 fstrba@suse.com
- Remove dependency on java-1_5_0-gcj-compat-devel
- Specify java source and target level 1.6 to allow building with
  jdk9
- Added patch:
  * asm-3.3.1-sourcetarget.patch
    + Don't hardcode the source and target levels, allow specifying
    them on command-line
* Fri May 19 2017 dziolkowski@suse.com
- New build dependency: javapackages-local
- cleaned spec using spec-cleaner
- remove "section free" macro
- get rid of %%if 0 blocks
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Wed Sep 25 2013 mvyskocil@suse.com
- Build with gcc-java as openjdk7 (1.7.0_40) fails to build it
- Disable javadoc package
* Wed Sep 11 2013 mvyskocil@suse.com
- use add_maven_depmap from javapackages-tools
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Sun Dec 18 2011 nlminhtl@gmail.com
- 3.3.1 release
  * added new InstructionAdapter class, TryCatchBlockSorter (provided by Adrian Sampson)
  * improved extensibility of analysis package (patch from Markus Heiden)
  * 314119 Provide read access to uninitializedTypes in AnalyzerAdapter
  * 313804 Improve analysis results
  * a lot of bugfixes
* Tue Jun  2 2009 mvyskocil@suse.cz
- Initial SUSE packaging of objectweb-asm (from jpp 5.0)
