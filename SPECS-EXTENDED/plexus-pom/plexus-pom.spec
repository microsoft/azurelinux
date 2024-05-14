Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package plexus-pom
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


Name:           plexus-pom
Version:        5.1
Release:        2%{?dist}
Summary:        Root Plexus Projects POM
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://github.com/codehaus-plexus/plexus-pom
Source0:        https://github.com/codehaus-plexus/plexus-pom/archive/plexus-%{version}.tar.gz
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch

%description
The Plexus project provides a full software stack for creating and
executing software projects.  This package provides parent POM for
Plexus packages.

%prep
%setup -q -n plexus-pom-plexus-%{version}
# * require: org.codehaus.plexus plexus-stylus-skin 1.0
# org.apache.maven.wagon wagon-webdav-jackrabbit 1.0
%pom_remove_plugin :maven-site-plugin

%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin
%pom_remove_plugin org.codehaus.mojo:taglist-maven-plugin
#Temporary?
%pom_remove_plugin :maven-enforcer-plugin
cp -p %{SOURCE1} LICENSE

%build

%install
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/plexus.pom
%add_maven_depmap %{name}/plexus.pom

%files -f .mfiles
%license LICENSE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 5.1-1.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Sat Feb  9 2019 Fridrich Strba <fstrba@suse.com>
- Initial package for root plexus projects pom 5.1
