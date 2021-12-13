Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package mojo-parent
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


Name:           mojo-parent
Version:        40
Release:        2%{?dist}
Summary:        Codehaus MOJO parent project pom file
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://www.mojohaus.org/mojo-parent/
Source0:        https://github.com/mojohaus/mojo-parent/archive/%{name}-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
BuildRequires:  javapackages-local
BuildArch:      noarch

%description
Codehaus MOJO parent project pom file

%prep
%setup -q -n %{name}-%{name}-%{version}
# Cobertura plugin is executed only during clean Maven phase.
%pom_remove_plugin :cobertura-maven-plugin
# Not needed
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-checkstyle-plugin

cp %{SOURCE1} .

%build

%install
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom -a org.codehaus.mojo:mojo

%files -f .mfiles
%doc LICENSE-2.0.txt

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 40-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Sun Mar 17 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of mojo-parent 40
