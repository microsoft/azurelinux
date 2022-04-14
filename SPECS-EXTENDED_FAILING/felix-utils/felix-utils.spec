Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package felix-utils
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


%global bundle org.apache.felix.utils
%bcond_with tests
Name:           felix-utils
Version:        1.11.4
Release:        2%{?dist}
Summary:        Utility classes for OSGi
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://felix.apache.org
Source0:        https://repo1.maven.org/maven2/org/apache/felix/%{bundle}/%{version}/%{bundle}-%{version}-source-release.tar.gz
Source1:        %{name}-build.xml
Patch0:         0000-Port-to-osgi-cmpn.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local
BuildRequires:  osgi-compendium
BuildRequires:  osgi-core
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  hamcrest-core
BuildRequires:  mockito
%endif

%description
Utility classes for OSGi

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{bundle}-%{version}
%patch0 -p1
cp -p %{SOURCE1} build.xml
mkdir -p lib
build-jar-repository -s lib osgi-core osgi-compendium
%if %{with tests}
build-jar-repository -s lib junit hamcrest/core mockito
%endif

%pom_remove_plugin :apache-rat-plugin

%pom_remove_parent .
%pom_xpath_inject "pom:project" "<groupId>org.apache.felix</groupId>" .

%build
%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  package javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/felix
install -pm 0644 target/%{bundle}-%{version}.jar %{buildroot}%{_javadir}/felix/%{bundle}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/felix
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/felix/%{bundle}.pom
%add_maven_depmap felix/%{bundle}.pom felix/%{bundle}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE NOTICE
%doc DEPENDENCIES

%files javadoc
%license LICENSE NOTICE
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.11.4-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Mar 31 2020 Fridrich Strba <fstrba@suse.com>
- Update to upstream release 1.11.4
- Added patch:
  * 0000-Port-to-osgi-cmpn.patch
    + Migrate away from the old felix-osgi implementation
* Tue Apr  9 2019 Fridrich Strba <fstrba@suse.com>
- Remove reference to the parent pom since we are not building
  using Maven.
* Fri Mar  1 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of felix-utils 1.10.4
- Generated and customized ant build file
