Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package xmvn-mojo
#
# Copyright (c) 2020 SUSE LLC
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


%global parent xmvn
%global subname mojo
Name:           %{parent}-%{subname}
Version:        3.1.0
Release:        3%{?dist}
Summary:        XMvn MOJO
License:        Apache-2.0
Group:          Development/Tools/Building
URL:            https://fedora-java.github.io/xmvn/
Source0:        https://github.com/fedora-java/%{parent}/releases/download/%{version}/%{parent}-%{version}.tar.xz
BuildRequires:  %{parent}-api = %{version}
BuildRequires:  %{parent}-core = %{version}
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  xmvn
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-compiler-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-jar-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-javadoc-plugin)
BuildRequires:  maven-plugin-plugin-bootstrap
BuildRequires:  maven-plugin-tools-generators
BuildRequires:  maven-plugin-tools-api
BuildRequires:  maven-plugin-tools-java
BuildRequires:  maven-plugin-tools-annotations
BuildRequires:  maven-reporting-impl
BuildRequires:  mvn(org.apache.maven.plugins:maven-resources-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-surefire-plugin)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-util)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.easymock:easymock)
#!BuildRequires: maven-compiler-plugin-bootstrap
#!BuildRequires: maven-jar-plugin-bootstrap
#!BuildRequires: maven-javadoc-plugin-bootstrap
#!BuildRequires: maven-plugin-plugin-bootstrap
#!BuildRequires: maven-resources-plugin-bootstrap
#!BuildRequires: maven-surefire-plugin-bootstrap
BuildArch:      noarch

%description
This package provides XMvn MOJO, which is a Maven plugin that consists
of several MOJOs.  Some goals of these MOJOs are intended to be
attached to default Maven lifecycle when building packages, others can
be called directly from Maven command line.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{parent}-%{version}

# Bisect IT has no chances of working in local, offline mode, without
# network access - it needs to access remote repositories.
find -name BisectIntegrationTest.java -delete

# Resolver IT won't work either - it tries to execute JAR file, which
# relies on Class-Path in manifest, which is forbidden in Fedora...
find -name ResolverIntegrationTest.java -delete

%pom_remove_plugin -r :maven-site-plugin

%{mvn_package} ":xmvn{,-it}" __noinstall

# Upstream code quality checks, not relevant when building RPMs
%pom_remove_plugin -r :apache-rat-plugin
%pom_remove_plugin -r :maven-checkstyle-plugin
%pom_remove_plugin -r :jacoco-maven-plugin
# FIXME pom macros don't seem to support submodules in profile
%pom_remove_plugin :jacoco-maven-plugin xmvn-it

# remove dependency plugin maven-binaries execution
# we provide apache-maven by symlink
%pom_xpath_remove "pom:executions/pom:execution[pom:id[text()='maven-binaries']]"

# Don't put Class-Path attributes in manifests
%pom_remove_plugin :maven-jar-plugin xmvn-tools

%pom_remove_dep -r :xmlunit-assertj

pushd %{name}
  %{mvn_file} :{*} %{parent}/@1
popd

%build
pushd %{name}
  xmvn \
    --batch-mode --offline \
    -Dmaven.test.skip=true -Dsource=8 \
    package org.apache.maven.plugins:maven-javadoc-plugin:aggregate

%{mvn_artifact} pom.xml target/%{name}-%{version}.jar

popd

%install
pushd %{name}
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}
popd

%files -f %{name}/.mfiles
%license LICENSE NOTICE
%doc AUTHORS README.md

%files javadoc -f %{name}/.mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.1.0-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 18 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.1.0-2.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Depend on maven-plugin-plugin-bootstrap, maven-plugin-tools*, and maven-reporting-impl to avoid circular dependency.

* Thu Nov 21 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream version 3.1.0
- Removed patches:
  * 0001-Fix-installer-plugin-loading.patch
  * 0001-Port-to-Gradle-4.2.patch
  * 0001-Port-to-Gradle-4.3.1.patch
  * 0001-Support-setting-Xdoclint-none-in-m-javadoc-p-3.0.0.patch
  * 0001-Fix-configuration-of-aliased-plugins.patch
  * 0001-Don-t-use-JAXB-for-converting-bytes-to-hex-string.patch
  * 0001-Use-apache-commons-compress-for-manifest-injection-a.patch
  * 0001-port-to-gradle-4.4.1.patch
  * 0001-Replace-JAXB-parser.patch
    + Integrated in this version
* Wed Mar 27 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of xmvn-mojo 3.0.0
