Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-interactivity
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
%global alpha_ver 6
%global namedversion %{base_ver}-alpha-%{alpha_ver}
Name:           plexus-interactivity
Version:        %{base_ver}~alpha%{alpha_ver}
Release:        2%{?dist}
Summary:        Plexus Interactivity Handler Component
License:        MIT
Group:          Development/Libraries/Java
URL:            https://github.com/codehaus-plexus/plexus-interactivity
# svn export \
#   http://svn.codehaus.org/plexus/plexus-components/tags/plexus-interactivity-1.0-alpha-6/
# tar caf plexus-interactivity-1.0-alpha-6-src.tar.xz \
#   plexus-interactivity-1.0-alpha-6
Source0:        %{name}-%{namedversion}-src.tar.xz
Source1:        LICENSE.MIT
Source100:      %{name}-build.tar.xz
Patch1:         %{name}-dependencies.patch
Patch2:         %{name}-jline2.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jline >= 2
BuildRequires:  plexus-component-api
BuildRequires:  plexus-utils
BuildArch:      noarch

%description
Plexus contains end-to-end developer tools for writing applications.
At the core is the container, which can be embedded or for an
application server. There are many reusable components for hibernate,
form processing, jndi, i18n, velocity, etc. Plexus also includes an
application server which is like a J2EE application server.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package provides %{summary}.

%package api
Summary:        API for %{name}
Group:          Development/Libraries/Java
Requires:       mvn(org.codehaus.plexus:plexus-component-api)
Requires:       mvn(org.codehaus.plexus:plexus-utils)

%description api
API module for %{name}.

%package jline
Summary:        jline module for %{name}
Group:          Development/Libraries/Java
Requires:       mvn(jline:jline)
Requires:       plexus-interactivity-api = %{version}

%description jline
jline module for %{name}.

%prep
%setup -q -n %{name}-%{namedversion} -a100
%patch1 -p1
%patch2 -p1

cp %{SOURCE1} .

for i in api jline; do
  %pom_xpath_inject "pom:project" "<groupId>org.codehaus.plexus</groupId>" %{name}-${i}
  %pom_remove_parent %{name}-${i}
done

%build
mkdir -p lib
build-jar-repository -s lib jline plexus-component-api plexus/utils
%{ant} package javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/plexus
for i in api jline; do
  install -pm 0644 %{name}-${i}/target/%{name}-${i}-%{namedversion}.jar %{buildroot}%{_javadir}/plexus/interactivity-${i}.jar
done
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/plexus
for i in api jline; do
  install -pm 0644 %{name}-${i}/pom.xml %{buildroot}%{_mavenpomdir}/plexus/interactivity-${i}.pom
  %add_maven_depmap plexus/interactivity-${i}.pom plexus/interactivity-${i}.jar -f ${i}
done
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
for i in api jline; do
  install -dm 0755 %{buildroot}%{_javadocdir}/%{name}/${i}
  cp -pr %{name}-${i}/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/${i}/
done
%fdupes -s %{buildroot}%{_javadocdir}

%files api -f .mfiles-api
%license LICENSE.MIT

%files jline -f .mfiles-jline
%license LICENSE.MIT

%files javadoc
%license LICENSE.MIT
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0~alpha6-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.0~alpha6-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Apr  1 2019 Jan Engelhardt <jengelh@inai.de>
- Describe package, not the project vision.
* Tue Mar 12 2019 Fridrich Strba <fstrba@suse.com>
- Intial packaging of plexus-interactivity 1.0-alpha-6
- Generate and customize ant build files
