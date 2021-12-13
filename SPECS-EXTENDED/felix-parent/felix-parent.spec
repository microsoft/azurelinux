Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package felix-parent
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


Name:           felix-parent
Version:        6
Release:        3%{?dist}
Summary:        Parent POM file for Apache Felix Specs
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://felix.apache.org/
Source0:        http://repo1.maven.org/maven2/org/apache/felix/felix-parent/%{version}/%{name}-%{version}-source-release.tar.gz
BuildRequires:  javapackages-local
BuildRequires:  mvn(org.apache:apache:pom:)
Requires:       mvn(org.apache:apache:pom:)
BuildArch:      noarch

%description
Parent POM file for Apache Felix Specs.

%prep
%setup -q -n felix-parent-%{version}
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin org.codehaus.mojo:ianal-maven-plugin
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin

# wagon ssh dependency unneeded
%pom_xpath_remove pom:extensions
%pom_xpath_remove pom:project/pom:parent/pom:relativePath

%build

%install
# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -m 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}-%{version}.pom
%add_maven_depmap %{name}-%{version}.pom -a org.apache.felix:felix

%files -f .mfiles
%license LICENSE
%doc NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6-3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Feb  7 2019 Fridrich Strba <fstrba@suse.com>
- Clean the spec file
* Tue Dec 18 2018 Fridrich Strba <fstrba@suse.com>
- Initial package for felix parent pom
