Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-velocity
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
Name:           plexus-velocity
Version:        1.2
Release:        2%{?dist}
Summary:        Plexus Velocity Component
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://codehaus-plexus.github.io/plexus-velocity/
Source0:        https://github.com/codehaus-plexus/%{name}/archive/%{name}-%{version}.tar.gz
Source1:        %{name}-build.xml
Source2:        http://www.apache.org/licenses/LICENSE-2.0.txt
BuildRequires:  ant
BuildRequires:  apache-commons-collections
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  plexus-containers-container-default
BuildRequires:  velocity
Requires:       mvn(commons-collections:commons-collections)
Requires:       mvn(org.codehaus.plexus:plexus-container-default)
Requires:       mvn(velocity:velocity)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  apache-commons-lang
BuildRequires:  guava20
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-utils
BuildRequires:  xbean
%endif

%description
This package provides Plexus Velocity component - a wrapper for
Apache Velocity template engine, which allows easy use of Velocity
by applications built on top of Plexus container.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{name}-%{name}-%{version}

find -name '*.jar' -delete

cp -p %{SOURCE1} build.xml
cp -p %{SOURCE2} LICENSE

%pom_xpath_inject pom:project "<groupId>org.codehaus.plexus</groupId>"
%pom_remove_parent

mkdir -p lib
build-jar-repository -s lib commons-collections plexus-containers/plexus-container-default velocity
%if %{with tests}
build-jar-repository -s lib commons-lang guava20/guava-20.0 plexus/classworlds plexus/utils xbean/xbean-reflect
%endif

%build
ant \
%if %{without tests}
  -Dtest.skip=true \
%endif
  jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE

%files javadoc
%license LICENSE
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.2-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Fri Mar 22 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of plexus-velocity 1.2
- Generate and customize the ant build.xml file
