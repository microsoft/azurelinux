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
Source1:        build.xml
Source2:        common.xml
Source3:        xbean-asm-util-build.xml
Source4:        xbean-finder-build.xml
Source5:        xbean-reflect-build.xml
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
%autosetup -p1

mkdir -p xbean-asm-util xbean-finder xbean-reflect
cp -f %{SOURCE1} . 
cp -f %{SOURCE2} .
cp -f %{SOURCE3} xbean-asm-util/build.xml
cp -f %{SOURCE4} xbean-finder/build.xml
cp -f %{SOURCE5} xbean-reflect/build.xml
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
  mv %{buildroot}/%{_javadocdir}/%{name}/${i}/legal/ADDITIONAL_LICENSE_INFO .
  mv %{buildroot}/%{_javadocdir}/%{name}/${i}/legal/LICENSE .
done
%fdupes -s %{buildroot}/%{_javadocdir}/%{name}

%files -f .mfiles
%license LICENSE
%license NOTICE

%files javadoc
%license LICENSE
%license ADDITIONAL_LICENSE_INFO
%{_javadocdir}/%{name}

%changelog
* Mon Dec 08 2025 Aditya Singh <v-aditysing@microsoft.com> - 4.20-1
- Upgrade to version 4.20.
- License verified.

* Mon Jan 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.18-1
- Updating to version 4.18.
- Removing dependency on "log4j12".
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.5-6
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 4.5-5.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Disable javadoc Xdoclint.

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
