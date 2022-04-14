#
# spec file for package bnd-maven-plugin
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


Name:           bnd-maven-plugin
Version:        3.5.0
Release:        6%{?dist}
Summary:        BND Maven plugin
# Part of jpm is under BSD, but jpm is not included in binary RPM
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://bnd.bndtools.org/
Source0:        https://github.com/bndtools/bnd/archive/%{version}.REL.tar.gz#/%{name}-%{version}.REL.tar.gz
BuildRequires:  fdupes
BuildRequires:  maven-local
BuildRequires:  mvn(biz.aQute.bnd:biz.aQute.bndlib)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.sonatype.plexus:plexus-build-api)
BuildArch:      noarch

%description
Collection of various Maven plugins provided by the Bnd project.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n bnd-%{version}.REL

rm gradlew*
rm -f $(find | grep -E '\.(.ar|exe|tar\.(gz|bz2|xz)|zip)$' | xargs)

pushd maven
rm bnd-shared-maven-lib/src/main/java/aQute/bnd/maven/lib/resolve/DependencyResolver.java
%pom_remove_dep -r :biz.aQute.resolve
%pom_remove_dep -r :biz.aQute.repository
# Unavailable reactor dependency - org.osgi.impl.bundle.repoindex.cli
%pom_disable_module bnd-indexer-maven-plugin
# Requires unbuilt parts of bnd
%pom_disable_module bnd-export-maven-plugin
%pom_disable_module bnd-resolver-maven-plugin
%pom_disable_module bnd-testing-maven-plugin
# Integration tests require Internet access
%pom_remove_plugin -r :maven-invoker-plugin
%pom_remove_plugin -r :maven-javadoc-plugin
%pom_remove_plugin -r :flatten-maven-plugin
%pom_remove_plugin -r :maven-source-plugin
popd

%{mvn_package} biz.aQute.bnd:bnd-plugin-parent __noinstall

%build
pushd maven
%{mvn_build} -- -Dproject.build.sourceEncoding=UTF-8 -Dsource=7
popd

%install
pushd maven
%mvn_install
popd
%fdupes -s %{buildroot}%{_javadocdir}

%files -f maven/.mfiles
%license LICENSE

%files javadoc -f maven/.mfiles-javadoc
%license LICENSE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.5.0-6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Apr  3 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of the bnd-maven-plugin distributed as a part
  of aqute-bnd 3.5.0
