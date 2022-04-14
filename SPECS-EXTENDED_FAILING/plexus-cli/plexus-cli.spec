Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-cli
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
Name:           plexus-cli
Version:        1.6
Release:        2%{?dist}
Summary:        Command Line Interface facilitator for Plexus
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://github.com/codehaus-plexus/plexus-cli
# git clone git://github.com/codehaus-plexus/plexus-cli.git
# git --git-dir plexus-cli/.git archive --prefix plexus-cli-1.6/ 8927458e81 | xz >plexus-cli-1.6.tar.xz
Source0:        %{name}-%{version}.tar.xz
Source1:        LICENSE-2.0.txt
Source100:      %{name}-build.xml
BuildRequires:  ant
BuildRequires:  apache-commons-cli
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-utils
BuildRequires:  xz
Requires:       mvn(commons-cli:commons-cli)
Requires:       mvn(org.codehaus.plexus:plexus-container-default)
Requires:       mvn(org.codehaus.plexus:plexus-utils)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  guava20
%endif

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
Javadoc for %{name}.

%prep
%setup -q
cp -p %{SOURCE1} .
cp -p %{SOURCE100} build.xml

%{pom_remove_parent}

mkdir -p lib
build-jar-repository -s lib commons-cli plexus/utils plexus/classworlds plexus-containers/plexus-container-default
%if %{with tests}
build-jar-repository -s lib guava20/guava-20.0
%endif

%build
ant \
%if %{without tests}
  -Dtest.skip=true \
%endif
  jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/plexus
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/plexus/cli.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/plexus
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/plexus/cli.pom
%add_maven_depmap plexus/cli.pom plexus/cli.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE-2.0.txt

%files javadoc
%license LICENSE-2.0.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.6-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Sun Mar  3 2019 Jan Engelhardt <jengelh@inai.de>
- Describe package, not project.
* Sat Mar  2 2019 Fridrich Strba <fstrba@suse.com>
- Initial package of plexus-cli 1.6
- Generate and customize the ant build file
