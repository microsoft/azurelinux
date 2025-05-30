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
%global debug_package %{nil}

Name:           objectweb-asm
Version:        9.6
Release:        1%{?dist}
Summary:        Java bytecode manipulation framework
License:        BSD-3-Clause
Group:          Development/Libraries/Java
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://asm.ow2.io/
Source0:        %{_distro_sources_url}/%{name}-%{version}.tar.gz
Source1:        aggregator.pom
Source2:        https://repo1.maven.org/maven2/org/ow2/asm/asm/%{version}/asm-%{version}.pom
Source3:        https://repo1.maven.org/maven2/org/ow2/asm/asm-analysis/%{version}/asm-analysis-%{version}.pom
Source4:        https://repo1.maven.org/maven2/org/ow2/asm/asm-commons/%{version}/asm-commons-%{version}.pom
Source5:        https://repo1.maven.org/maven2/org/ow2/asm/asm-test/%{version}/asm-test-%{version}.pom
Source6:        https://repo1.maven.org/maven2/org/ow2/asm/asm-tree/%{version}/asm-tree-%{version}.pom
Source7:        https://repo1.maven.org/maven2/org/ow2/asm/asm-util/%{version}/asm-util-%{version}.pom
Source10:       tools-retrofitter.pom

BuildRequires:  lujavrite
BuildRequires:  javapackages-bootstrap
BuildRequires:  javapackages-local-bootstrap

# Explicit javapackages-tools requires since asm-processor script uses
# /usr/share/java-utils/java-functions
Requires:       javapackages-tools

BuildArch:      noarch
%description
ASM is an all purpose Java bytecode manipulation and analysis
framework.  It can be used to modify existing classes or dynamically
generate classes, directly in binary form.  Provided common
transformations and analysis algorithms allow to easily assemble
custom complex transformations and code analysis tools.
 
%package javadoc
Summary:        API documentation for %{name}
 
%description    javadoc
This package provides %{summary}.
 
%prep
%setup -q
 
# A custom pom to aggregate the build
cp -p %{SOURCE1} pom.xml
 
cp -p %{SOURCE10} tools/retrofitter/pom.xml
 
# Insert poms into modules
for pom in asm asm-analysis asm-commons asm-test asm-tree asm-util; do
  cp -p ${RPM_SOURCE_DIR}/${pom}-%{version}.pom ${pom}/pom.xml
  %pom_add_dep org.fedoraproject.xmvn.objectweb-asm:tools-retrofitter::provided ${pom}
  %pom_add_plugin org.apache.maven.plugins:maven-antrun-plugin ${pom}
  %pom_set_parent org.fedoraproject.xmvn.objectweb-asm:aggregator:any ${pom}
  %pom_xpath_inject pom:parent '<relativePath>..</relativePath>' ${pom}
done
 
%pom_add_dep org.ow2.asm:asm-tree:%{version} asm-analysis
 
# Don't ship poms used for build only
%mvn_package :aggregator __noinstall
%mvn_package :tools-retrofitter __noinstall
 
# Don't ship the test framework to avoid runtime dep on junit
%mvn_package :asm-test __noinstall
 
%build

%mvn_build -f -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8
 
%install
%mvn_install
%jpackage_script org.objectweb.asm.xml.Processor "" "" %{name}/asm:%{name}/asm-attrs:%{name}/asm-util %{name}-processor true
 
%files -f .mfiles
%license LICENSE.txt
%{_bindir}/%{name}-processor
 
%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Thu Apr 04 2024 Mitch Zhu <mitchzhu@microsoft.com> - 9.6-1
- Upgrade to version 9.6
- Import build and install section from Fedora 40 (license: MIT).

* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.2-5
- Updating naming for 3.0 version of Azure Linux.

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
