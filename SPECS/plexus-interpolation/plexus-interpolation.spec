#
# spec file for package plexus-interpolation
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
%bcond_with tests
Summary:        Plexus Interpolation API
Name:           plexus-interpolation
Version:        1.26
Release:        3%{?dist}
License:        Apache-2.0 AND Apache-1.1 AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries/Java
URL:            https://github.com/codehaus-plexus/%{name}
Source0:        https://github.com/codehaus-plexus/%{name}/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
%endif

%description
Plexus interpolator is the outgrowth of multiple iterations of development
focused on providing a more modular, flexible interpolation framework for
the expression language style commonly seen in Maven, Plexus, and other
related projects.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}
cp %{SOURCE1} build.xml
%pom_remove_plugin :maven-release-plugin

%pom_remove_parent

%pom_xpath_inject "pom:project" "<groupId>org.codehaus.plexus</groupId>"

%build
%ant \
%if %{without tests}
  -Dtest.skip=true \
%endif
  jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/plexus
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/plexus/interpolation.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/plexus
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/plexus/interpolation.pom
%add_maven_depmap plexus/interpolation.pom plexus/interpolation.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.26-3
- Moved from extended to core
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.26-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 20 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.26-1.5
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Sun Nov 24 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 1.26

* Wed Mar  6 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of plexus-interpolation 1.22
- Generate and customize ant build.xml file to be able to build
  outside maven
