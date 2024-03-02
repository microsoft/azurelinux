%bcond_without bootstrap

#
# spec file for package cal10n
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
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
Summary:        Compiler assisted localization library (CAL10N)
Name:           cal10n
Version:        0.8.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries/Java
URL:            http://cal10n.qos.ch
Source0:        https://github.com/qos-ch/%{name}/archive/refs/tags/v_%{version}.tar.gz#/%{name}-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
BuildRequires:  javapackages-local-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-artifact-manager)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
%endif

BuildArch:      noarch

%description
Compiler Assisted Localization, abbreviated as CAL10N (pronounced as "calion")
is a java library for writing localized (internationalized) messages.
Features:
    * java compiler verifies message keys used in source code
    * tooling to detect errors in message keys
    * native2ascii tool made superfluous, as you can directly encode bundles
      in the most convenient charset, per locale.
    * good performance (300 nanoseconds per key look-up)
    * automatic reloading of resource bundles upon change

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
%{summary}.
	
%package -n maven-%{name}-plugin
Summary:        CAL10N maven plugin
 
%description -n maven-%{name}-plugin
Maven plugin verifying that the codes defined in
an enum type match those in the corresponding resource bundles. 

%prep
%setup -q -n %{name}-v_%{version}

find . -name "*.jar" -delete

%pom_xpath_remove pom:extensions
%pom_add_dep org.apache.maven:maven-artifact maven-%{name}-plugin
%pom_disable_module %{name}-site
%pom_disable_module maven-%{name}-plugin-smoke
%mvn_package :*-{plugin} @1

# remove maven-compiler-plugin configuration that is broken with Java 11
%pom_xpath_remove 'pom:plugin[pom:artifactId="maven-compiler-plugin"]/pom:configuration'

# Disable default-jar execution of maven-jar-plugin, which is causing
# problems with version 3.0.0 of the plugin.
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-jar-plugin']/pom:executions" "
    <execution>
      <id>default-jar</id>
      <phase>skip</phase>
    </execution>" cal10n-api
 
%build
%mvn_build -- -Dproject.build.sourceEncoding=ISO-8859-1 -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8
 
%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}
%license LICENSE.txt
 
%files -n maven-%{name}-plugin -f .mfiles-plugin
 
%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Wed Feb 14 2024 Mitch Zhu <mitchzhu@microsoft.com> - 0.8.1-1
- Update to version 0.8.1

* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 0.7.7-6
- Moved from extended to core
- Updated source URL

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.7-5
- Converting the 'Release' tag to the '[number].[distribution]' format.
- License verified.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 0.7.7-4.9
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Thu Oct 18 2018 Fridrich Strba <fstrba@suse.com>
- Install the maven pom files in order to generate correctly the
  mvn(...) provides.

* Wed May 16 2018 fstrba@suse.com
- Modified patch:
  * cal10n-0.7.7-sourcetarget.patch
    + Build with source and target 8 to prepare for a possible
    removal of 1.6 compatibility
- Run fdupes on documentation

* Thu Sep  7 2017 fstrba@suse.com
- Added patch:
  * cal10n-0.7.7-sourcetarget.patch
  - Force java source and target levels to 1.6 in order to allow
    building with jdk9

* Thu Dec 25 2014 p.drouand@gmail.com
- Update to version 0.7.7
  + Correctly read escaped ':', '#', '!', '=' characters. The behavior
  is documented in the Properties javadocs (http://tinyurl.com/bprdgnk).
  This fixes CAL-37 (http://jira.qos.ch/browse/CAL-37)
- Update build.xml.tar.bz2, rename it to build.xml-$VERSION and
  recompress it in xz format
- Add a requirement to xz

* Mon Jul  7 2014 tchvatal@suse.com
- Depend on junit not junit4

* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools

* Fri May  4 2012 mvyskocil@suse.cz
- fix bnc#759912 - Manual for cal10n 0.7.4 uses CC-BY-SA-NC-2.5 license

* Fri Apr 27 2012 mvyskocil@suse.cz
- format spec for Factory

* Mon Dec 12 2011 dmacvicar@suse.de
- fix build.xml files to build in openSUSE 12.1 and newer.
  MANIFEST contained an absolute path in maven-build.xml
- Fix group for javadoc subpackage
- remove id generation for buildroot (used in Fedora)

* Wed Jul 27 2011 dmacvicar@suse.de
- Un-mavenize. Build with ant
