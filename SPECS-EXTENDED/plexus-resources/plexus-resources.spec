Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-resources
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


%global base_ver 1.0
%global alpha_ver 7
%global namedversion %{base_ver}-alpha-%{alpha_ver}
Name:           plexus-resources
Version:        %{base_ver}~a%{alpha_ver}
Release:        2%{?dist}
Summary:        Plexus Resource Manager
License:        MIT
Group:          Development/Libraries/Java
URL:            https://github.com/codehaus-plexus/plexus-resources
# svn export http://svn.codehaus.org/plexus/plexus-components/tags/plexus-resources-1.0-alpha-7/
# tar caf plexus-resources-1.0-alpha-7-src.tar.xz plexus-resources-1.0-alpha-7
Source0:        %{name}-%{namedversion}-src.tar.xz
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-metadata-generator
BuildRequires:  plexus-utils
Requires:       mvn(org.codehaus.plexus:plexus-container-default)
Requires:       mvn(org.codehaus.plexus:plexus-utils)
BuildArch:      noarch

%description
Plexus contains end-to-end developer tools for writing applications.
At the core is the container, which can be embedded or for an
application server. There are many reusable components for hibernate,
form processing, jndi, i18n, velocity, etc. Plexus also includes an
application server which is like a J2EE application server.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}
cp %{SOURCE1} build.xml

%pom_remove_parent .
%pom_xpath_inject "pom:project" "<groupId>org.codehaus.plexus</groupId>" .

%build
mkdir -p lib
build-jar-repository -s lib plexus/utils plexus-containers/plexus-container-default
%{ant} jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/plexus
install -pm 0644 target/%{name}-%{namedversion}.jar %{buildroot}%{_javadir}/plexus/resources.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/plexus
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/plexus/resources.pom
%add_maven_depmap plexus/resources.pom plexus/resources.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0~a7-2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Apr  1 2019 Jan Engelhardt <jengelh@inai.de>
- Descript package, not the project vision.
* Thu Mar  7 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of plexus-resource 1.0-alpha-7
- Generate and customize ant build file
  * generate the plexus components.xml descriptor using
    plexus-metadata-generator
