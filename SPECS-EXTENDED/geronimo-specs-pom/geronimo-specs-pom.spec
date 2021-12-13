Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package geronimo-specs-pom
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


Name:           geronimo-specs-pom
Version:        1.6
Release:        3%{?dist}
Summary:        Parent POM files for geronimo-specs
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://geronimo.apache.org/
# Following the parent chain all the way up ...
Source0:        http://svn.apache.org/repos/asf/geronimo/specs/tags/specs-parent-%{version}/pom.xml
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
BuildRequires:  javapackages-local
BuildRequires:  xmvn-resolve
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-compiler-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-jar-plugin)
Obsoletes:      geronimo-specs-poms
BuildArch:      noarch

%description
The Project Object Model files for the geronimo-specs modules.

%prep
%setup -q -c -T
cp -p %{SOURCE0} .
cp -p %{SOURCE1} LICENSE
%pom_remove_parent
# not really useful for rpm build
%pom_remove_plugin :maven-idea-plugin

%pom_xpath_set "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-compiler-plugin']/pom:configuration/pom:source" 1.6
%pom_xpath_set "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-compiler-plugin']/pom:configuration/pom:target" 1.6

%pom_xpath_set "pom:reporting/pom:plugins/pom:plugin[pom:artifactId='maven-pmd-plugin']/pom:configuration/pom:targetJdk" 1.6

%build

%install
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-geronimo-specs.pom
%add_maven_depmap JPP-geronimo-specs.pom -a org.apache.geronimo.specs:specs

%files -f .mfiles
%license LICENSE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6-3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Dec 12 2019 Fridrich Strba <fstrba@suse.com>
- Set source and target levels to 1.6 in order to make them trickle
  down to all its children
* Mon Apr 15 2019 Fridrich Strba <fstrba@suse.com>
- Split the parent pom from package geronimo-spec to a separate
  package and upgrade the pom to the latest version 1.6
