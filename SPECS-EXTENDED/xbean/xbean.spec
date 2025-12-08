Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package xbean
#
# Copyright (c) 2024 SUSE LLC
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


Name:           xbean
Version:        4.20
Release:        1%{?dist}
Summary:        Java plugin based web server
License:        ASL 2.0
Group:          Development/Libraries/Java
URL:            https://geronimo.apache.org/xbean/
Source0:        https://repo1.maven.org/maven2/org/apache/%{name}/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        %{name}-build.tar.xz
Patch2:         0002-Unbundle-ASM.patch
Patch3:         0003-Remove-dependency-on-log4j-and-commons-logging.patch
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  junit
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap >= 6
BuildRequires:  javapackages-tools
BuildRequires:  objectweb-asm >= 9
BuildRequires:  slf4j
BuildRequires:  unzip
BuildRequires:  xml-commons-apis
BuildArch:      noarch

%description
XBean is a plugin-based server analogous to Eclipse being a
plugin-based IDE. XBean is able to discover, download and install
server plugins from an Internet-based repository. Support for
multiple IoC systems, support for running with no IoC system, JMX
without JMX code, lifecycle and class loader management, and a Spring
integration is included.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description    javadoc
This package provides API documentation for xbean.

%prep
%autosetup -p1 -a1

cp xbean-asm-util/src/main/java/org/apache/xbean/asm9/original/commons/AsmConstants.java xbean-reflect/src/main/java/org/apache/xbean/recipe/

%pom_disable_module xbean-classloader
%pom_disable_module xbean-classpath
%pom_disable_module xbean-bundleutils
%pom_disable_module xbean-asm9-shaded
%pom_disable_module xbean-finder-shaded
%pom_disable_module xbean-naming
%pom_disable_module xbean-blueprint
%pom_disable_module xbean-spring
%pom_disable_module xbean-telnet
%pom_disable_module maven-xbean-plugin

%pom_remove_dep :commons-logging-api xbean-reflect
%pom_remove_dep :log4j xbean-reflect
%pom_remove_dep :xbean-asm9-shaded xbean-reflect
find -name CommonsLoggingConverter.java -delete
find -name Log4jConverter.java -delete

# Plugins useful for upstream only
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :maven-source-plugin

%pom_remove_dep :xbean-bundleutils xbean-finder
%pom_remove_dep org.osgi:org.osgi.core xbean-finder
rm -r xbean-finder/src/main/java/org/apache/xbean/finder{,/archive}/Bundle*
%build
mkdir -p lib
build-jar-repository -s lib objectweb-asm slf4j
%{ant} package javadoc

%install
# jars
install -dm 755 %{buildroot}%{_javadir}/%{name}
for i in xbean-asm-util xbean-finder xbean-reflect; do
  install -m 0644 ${i}/target/${i}-%{version}.jar %{buildroot}%{_javadir}/%{name}/${i}.jar
done

# poms
install -dm 755 %{buildroot}%{_mavenpomdir}/%{name}
for i in xbean-asm-util xbean-finder xbean-reflect; do
  install -pm 644 ${i}/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/${i}.pom
  %add_maven_depmap %{name}/${i}.pom %{name}/${i}.jar
done

# javadoc
install -dm 755 %{buildroot}/%{_javadocdir}/%{name}
for i in xbean-asm-util xbean-finder xbean-reflect; do
  cp -r ${i}/target/site/apidocs %{buildroot}/%{_javadocdir}/%{name}/${i}
done
%fdupes -s %{buildroot}/%{_javadocdir}/%{name}

%files -f .mfiles
%license LICENSE
%doc NOTICE

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Mon Dec 08 2025 Aditya Singh <v-aditysing@microsoft.com> - 4.20-1
- Initial Azure Linux import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified.

* Wed Feb 21 2024 Gus Kenion <gus.kenion@suse.com>
- Use %%patch -P N instead of deprecated %%patchN.
* Wed Oct 25 2023 Fridrich Strba <fstrba@suse.com>
- Build with source/target 8 to fix build with jdk 21
* Mon Mar  7 2022 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 4.20
  * Bugs
    + XBEAN-298: FileArchive can lead to NPE
    + XBEAN-326: NullpointerException in BundleAssignableClassFinder
    + XBEAN-327: ASM9 bundle
    + XBEAN-328: Upgrade to asm 9.0
    + XBEAN-329: trunk does not build due to unused import
    + XBEAN-330: Wrong OSGi manifests in xbean-asm9-shaded
    + XBEAN-331: Upgrade to asm 9.1
  * Improvements
    + XBEAN-301: Add Automatic-Module-Name to xbean manifest
    + XBEAN-303: asm shade NOTICE file shouldnt exist
    + XBEAN-306: MultiJar release support enhancements
    + XBEAN-309: Support Constructors and Static Factory Methods
    in xbean-reflect
    + XBEAN-310: Provide a PropertyEditorRegistry
    + XBEAN-312: Ensure multi-jar are not scanned twice
    + XBEAN-318: xbean-finder should log the class name on errors
    + XBEAN-319: Enable xbean-finder to not store classes without
    annotations
    + XBEAN-320: Enable xbean-finder to not track some annotations
    + XBEAN-322: Upgrade to ASM 7.2
  * New Features
    + XBEAN-305: Asm 6.1.1 upgrade
    + XBEAN-313: Create asm7 bundle
  * Tasks
    + XBEAN-296: upgrade to asm 6
    + XBEAN-302: Upgrade to asm 6.1
    + XBEAN-308: ASM 6.2 upgrade
    + XBEAN-311: ASM 6.2.1
    + XBEAN-314: ASM 7.0 upgrade
    + XBEAN-316: Upgrade ASM to 7.1
    + XBEAN-321: Upgrade to asm 7.2-beta
    + XBEAN-323: Upgrade ASM to 7.3.1
    + XBEAN-325: Upgrade to asm 8
- Removed patch:
  * 0003-Port-to-QDox-2.0.patch
    + not needed in modules that we build
- Changed patch:
  * 0001-Unshade-ASM.patch -> 0002-Unbundle-ASM.patch
    + Different ASM version and code structure
- Added patch:
  * 0003-Remove-dependency-on-log4j-and-commons-logging.patch
    + Remove unnecessary dependency on log4j and commons-logging
* Tue Feb 22 2022 Fridrich Strba <fstrba@suse.com>
- Do not build against the log4j12 packages, use the new reload4j
* Mon Jan 27 2020 Fridrich Strba <fstrba@suse.com>
- On supported platforms, avoid building with OpenJ9, in order to
  prevent build cycles
* Sat Oct  5 2019 Fridrich Strba <fstrba@suse.com>
- Remove references to parent from all pom files
- Avoid version-less dependencies
* Tue Oct  1 2019 Fridrich Strba <fstrba@suse.com>
- Build against the new log4j12 compat package
* Thu Apr  4 2019 Fridrich Strba <fstrba@suse.com>
- Do not require optional dependencies
* Thu Feb  7 2019 Jan Engelhardt <jengelh@inai.de>
- Trim future goals from description.
- Avoid double-shipping documentation.
* Thu Oct 25 2018 Fridrich Strba <fstrba@suse.com>
- Initial packaging of xbean version 4.5
- Spec file inspired by Fedora rpm package
