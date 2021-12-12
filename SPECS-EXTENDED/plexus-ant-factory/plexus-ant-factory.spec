Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-ant-factory
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
# Copyright (c) 2000-2005, JPackage Project
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


%global parent plexus
%global subname ant-factory
%global base_ver 1.0
%global alpha_ver 2.1
%global namedversion %{base_ver}-alpha-%{alpha_ver}
%bcond_with tests
Name:           %{parent}-%{subname}
Version:        %{base_ver}~a%{alpha_ver}
Release:        2%{?dist}
Summary:        Plexus Ant component factory
# Email from copyright holder confirms license.
# See plexus-ant-factory_license_and_copyright.txt
License:        Apache-2.0
Group:          Development/Tools/Building
URL:            https://codehaus-plexus.github.io
# sources are here https://mvnrepository.com/artifact/org.codehaus.plexus/plexus-ant-factory 
# jar or pom files that need to be changed into tarball
Source0:        %{name}-src.tar.bz2
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
Source2:        %{name}-build.xml
Source100:      plexus-ant-factory_license_and_copyright.txt
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-utils
Requires:       mvn(org.apache.ant:ant)
Requires:       mvn(org.apache.ant:ant-launcher)
Requires:       mvn(org.codehaus.plexus:plexus-container-default)
Requires:       mvn(org.codehaus.plexus:plexus-utils)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
%endif

%description
Ant component class creator for Plexus.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}
cp %{SOURCE1} LICENSE
cp %{SOURCE2} build.xml

%pom_remove_parent .
%pom_xpath_inject "pom:project" "<groupId>org.codehaus.plexus</groupId>" .

%build
mkdir -p lib

build-jar-repository -s lib plexus/classworlds plexus/utils plexus-containers/plexus-container-default
%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  jar

build-jar-repository -s lib ant/ant
%{ant} javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{parent}
install -pm 0644 target/%{name}-%{namedversion}.jar %{buildroot}%{_javadir}/%{parent}/%{subname}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{parent}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{parent}/%{subname}.pom
%add_maven_depmap %{parent}/%{subname}.pom %{parent}/%{subname}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE
%dir %{_javadir}/plexus

%files javadoc
%license LICENSE
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0~a2.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0~a2.1-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Fri Mar  8 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of plexus-ant-factory 1.0-alpha-2.1
- Generate and customize ant build.xml file
