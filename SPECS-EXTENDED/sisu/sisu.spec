Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package sisu
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


%global reltype release
#global reltag .M1
Name:           sisu
Version:        0.3.3
Release:        2%{?dist}
Summary:        Eclipse dependency injection framework
# sisu is EPL-1.0, bundled asm is BSD
License:        EPL-1.0 AND BSD-3-Clause
Group:          Development/Libraries/Java
URL:            http://eclipse.org/sisu
Source0:        http://git.eclipse.org/c/%{name}/org.eclipse.%{name}.inject.git/snapshot/%{reltype}s/%{version}%{?reltag}.tar.xz#/org.eclipse.%{name}.inject-%{version}%{?reltag}.tar.xz
Source1:        http://git.eclipse.org/c/%{name}/org.eclipse.%{name}.plexus.git/snapshot/%{reltype}s/%{version}%{?reltag}.tar.xz#/org.eclipse.%{name}.plexus-%{version}%{?reltag}.tar.xz
Source2:        %{name}-build.tar.xz
Source100:      %{name}-inject.pom
Source101:      %{name}-plexus.pom
Patch0:         %{name}-OSGi-import-guava.patch
Patch2:         %{name}-ignored-tests.patch
Patch3:         %{name}-osgi-api.patch
BuildRequires:  ant
BuildRequires:  atinject
BuildRequires:  cdi-api
BuildRequires:  fdupes
BuildRequires:  glassfish-annotation-api
BuildRequires:  glassfish-servlet-api
BuildRequires:  google-guice
BuildRequires:  guice-servlet
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit
BuildRequires:  osgi-core
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-containers-component-annotations
BuildRequires:  plexus-utils
BuildRequires:  slf4j
BuildRequires:  testng
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildRequires:  xz
Provides:       bundled(objectweb-asm)
BuildArch:      noarch

%description
Java dependency injection framework with backward support for plexus and bean
style dependency injection.

%package        inject
Summary:        Sisu inject
Group:          Development/Libraries/Java

%description    inject
This package contains %{summary}.

%package        plexus
Summary:        Sisu Plexus
Group:          Development/Libraries/Java

%description    plexus
This package contains %{summary}.

%package        javadoc
Summary:        API documentation for Sisu
Group:          Documentation/HTML

%description    javadoc
This package contains %{summary}.

%prep
%setup -q -c -T
tar -xf %{SOURCE0} && mv %{reltype}s/* sisu-inject && rmdir %{reltype}s
cp %{SOURCE100} sisu-inject/pom.xml
tar -xf %{SOURCE1} && mv %{reltype}s/* sisu-plexus && rmdir %{reltype}s
cp %{SOURCE101} sisu-plexus/pom.xml
tar -xf %{SOURCE2}

%patch0
%patch2
%patch3

for i in inject plexus; do
  %pom_xpath_set -r /pom:project/pom:version %{version} %{name}-${i}
done

%{mvn_file} ":{*}" @1
%{mvn_package} ":*{inject,plexus}" @1
%{mvn_alias} :org.eclipse.sisu.plexus org.sonatype.sisu:sisu-inject-plexus

%build
mkdir -p lib
build-jar-repository -s lib \
  glassfish-annotation-api \
  glassfish-servlet-api \
  google-guice-no_aop \
  guice/guice-servlet \
  javax.enterprise.inject/cdi-api \
  javax.inject/atinject \
  junit \
  osgi-core/osgi.core \
  plexus/utils \
  plexus/classworlds \
  plexus-containers/plexus-component-annotations \
  slf4j/api \
  testng
%ant package javadoc

for i in inject plexus; do
  %mvn_artifact %{name}-${i}/pom.xml %{name}-${i}/target/org.eclipse.sisu.${i}-%{version}.jar
done

%install
%mvn_install

for i in inject plexus; do
  install -dm 0755 %{buildroot}%{_javadocdir}/%{name}/%{name}-${i}
  cp -pr %{name}-${i}/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/%{name}-${i}/
done
%fdupes -s %{buildroot}%{_javadocdir}

%files inject -f .mfiles-inject
%license sisu-inject/LICENSE.txt

%files plexus -f .mfiles-plexus

%files javadoc
%license sisu-inject/LICENSE.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.3-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.3.3-1.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Apr  1 2019 Jan Engelhardt <jengelh@inai.de>
- Use modern tar options.
* Tue Mar 19 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of sisu-inject and sisu-plexus 0.3.3
- Generate and customize ant build files
