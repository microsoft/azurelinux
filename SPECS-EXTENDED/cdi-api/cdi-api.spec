Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package cdi-api
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


%bcond_with tests
Name:           cdi-api
Version:        1.2
Release:        4%{?dist}
Summary:        Contexts and Dependency Injection for Java EE
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://seamframework.org/Weld
# sh create-tarball.sh %%{version}
Source0:        cdi-%{version}.tar.xz
Source1:        %{name}-build.xml
Source2:        http://www.apache.org/licenses/LICENSE-2.0.txt
BuildRequires:  ant
BuildRequires:  atinject
BuildRequires:  fdupes
BuildRequires:  glassfish-el-api
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jboss-interceptors-1.2-api
Requires:       mvn(javax.el:javax.el-api)
Requires:       mvn(javax.inject:javax.inject)
Requires:       mvn(org.jboss.spec.javax.interceptor:jboss-interceptors-api_1.2_spec)
BuildArch:      noarch

%description
APIs for JSR-299: Contexts and Dependency Injection for Java EE

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -qn cdi-%{version}
pushd api/
cp %{SOURCE1} build.xml
cp %{SOURCE2} LICENSE

# Use newer version of interceptors API
%pom_change_dep "javax.interceptor:javax.interceptor-api" "org.jboss.spec.javax.interceptor:jboss-interceptors-api_1.2_spec"

%pom_remove_parent
popd

%build
pushd api/
mkdir -p lib
build-jar-repository -s lib glassfish-el-api jboss-interceptors-1.2-api javax.inject
%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  jar javadoc
popd

%install
pushd api/
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -dm 0755 %{buildroot}%{_javadir}/javax.enterprise.inject
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
ln -sf ../%{name}/%{name}.jar %{buildroot}%{_javadir}/javax.enterprise.inject/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
popd
%fdupes -s %{buildroot}%{_javadocdir}

%files -f api/.mfiles
%license api/LICENSE
%{_javadir}/javax.enterprise.inject

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.2-3.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Sat Apr  6 2019 Jan Engelhardt <jengelh@inai.de>
- Use _service instead of custom create-tarball.sh.
- Avoid double-shipping license file.
* Wed Apr  3 2019 Fridrich Strba <fstrba@suse.com>
- Generate the tarball and pack only the api part, to avoid
  distributing non-distribuable content
* Wed Mar 27 2019 Jan Engelhardt <jengelh@inai.de>
- Replace summary by something that speaks more than two
  acronyms.
* Wed Mar 27 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of cdi-api 1.2
- Generate and customize the ant build.xml file
