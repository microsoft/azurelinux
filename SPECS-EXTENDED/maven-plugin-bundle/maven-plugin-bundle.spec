Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-plugin-bundle
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


%global site_name maven-bundle-plugin
%bcond_with obr
%bcond_without reporting
Name:           maven-plugin-bundle
Version:        3.5.1
Release:        3%{?dist}
Summary:        Maven Bundle Plugin
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://felix.apache.org
Source0:        http://repo2.maven.org/maven2/org/apache/felix/%{site_name}/%{version}/%{site_name}-%{version}-source-release.tar.gz
# Needs polishing to be sent upstream
Patch0:         0001-Port-to-current-maven-dependency-tree.patch
# New maven-archiver removed some deprecated methods we were using
Patch1:         0002-Fix-for-new-maven-archiver.patch
# Port to newer Plexus utils
Patch2:         0003-Port-to-plexus-utils-3.0.24.patch
# Port to newer Maven
Patch3:         0004-Use-Maven-3-APIs.patch
BuildRequires:  fdupes
BuildRequires:  maven-local
BuildRequires:  mvn(biz.aQute.bnd:biz.aQute.bndlib)
BuildRequires:  mvn(org.apache.felix:felix-parent:pom:)
BuildRequires:  mvn(org.apache.felix:org.apache.felix.utils)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.shared:maven-dependency-tree)
BuildRequires:  mvn(org.apache.maven:maven-archiver)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.osgi:osgi.core)
BuildRequires:  mvn(org.sonatype.plexus:plexus-build-api)
BuildArch:      noarch
%if %{with obr}
BuildRequires:  mvn(net.sf.kxml:kxml2)
BuildRequires:  mvn(org.apache.felix:org.apache.felix.bundlerepository)
BuildRequires:  mvn(xpp3:xpp3)
%endif
%if %{with reporting}
BuildRequires:  mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-impl)
%endif

%description
Provides a maven plugin that supports creating an OSGi bundle
from the contents of the compilation classpath along with its
resources and dependencies. Plus a zillion other features.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{site_name}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

find -name '*.jar' -delete

%pom_change_dep :org.osgi.core :osgi.core

# Bundled class from old maven-dependency-tree
rm -r src/main/java/org/apache/maven/shared/dependency

# Bundled classes from old maven
rm -r src/main/java/org/apache/felix/bundleplugin/pom

# There is forked version of maven-osgi in
# src/{main,test}/java/org/apache/maven

%if %{with obr}
# Deps unbundled from felix-bundlerepository
%pom_add_dep xpp3:xpp3
%pom_add_dep net.sf.kxml:kxml2
%else
rm -rf src/main/java/org/apache/felix/obrplugin/
%pom_remove_dep :org.apache.felix.bundlerepository
%endif

%if %{without reporting}
rm -f src/main/java/org/apache/felix/bundleplugin/baseline/BaselineReport.java
%pom_remove_dep :doxia-sink-api
%pom_remove_dep :doxia-site-renderer
%pom_remove_dep :maven-reporting-impl
%endif

%build
%{mvn_build} -f \
%if %{?pkg_vcmp:%pkg_vcmp java-devel >= 9}%{!?pkg_vcmp:0}
	-- -Dmaven.compiler.release=7
%endif

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.5.1-3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Sun Nov 24 2019 Fridrich Strba <fstrba@suse.com>
- Specify maven.compiler.release to fix build with jdk9+ and newer
  maven-javadoc-plugin
* Sat Apr  6 2019 Jan Engelhardt <jengelh@inai.de>
- Add Group: line for documentation.
* Fri Apr  5 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of maven-plugin-bundle 3.5.1
