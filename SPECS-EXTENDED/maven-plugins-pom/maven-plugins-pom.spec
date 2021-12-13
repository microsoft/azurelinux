Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package maven-plugins-pom
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


%global short_name maven-plugins
Name:           %{short_name}-pom
Version:        28
Release:        2%{?dist}
Summary:        Maven Plugins POM
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://maven.apache.org/plugins/
Source:         http://repo.maven.apache.org/maven2/org/apache/maven/plugins/%{short_name}/%{version}/%{short_name}-%{version}-source-release.zip
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  unzip
Requires:       mvn(org.apache.maven:maven-parent:pom:)
BuildArch:      noarch

%description
This package provides Maven Plugins parent POM used by different
Apache Maven plugins.

%prep
%setup -q -n %{short_name}-%{version}
# Enforcer plugin is used to ban plexus-component-api.
%pom_remove_plugin :maven-enforcer-plugin
# maven-scm-publish-plugin is not usable in Fedora.
%pom_remove_plugin :maven-scm-publish-plugin
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-plugin-plugin

%build

%install
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{short_name}.pom
%add_maven_depmap %{name}/%{short_name}.pom

%files -f .mfiles
%license LICENSE
%doc NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 28-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Dec 03 2020 Joe Schmitt <joschmit@microsoft.com> - 28-1.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Sat Feb  9 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of Maven Plugins POM version 28
