Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package mockito
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


Name:           mockito
Version:        1.10.19
Release:        4%{?dist}
Summary:        A Java mocking framework
License:        MIT
Group:          Development/Libraries/Java
URL:            http://%{name}.org
Source0:        %{name}-%{version}.tar.xz
Patch0:         fixup-ant-script.patch
Patch1:         fix-bnd-config.patch
Patch2:         %{name}-matcher.patch
# Workaround for NPE in setting NamingPolicy in cglib
Patch3:         setting-naming-policy.patch
# because we have old objenesis
Patch4:         fix-incompatible-types.patch
Patch5:         remove-hardcoded-source-target.patch
Patch6:         %{name}-hamcrest.patch
BuildRequires:  ant
BuildRequires:  aqute-bnd
BuildRequires:  cglib
BuildRequires:  dos2unix
BuildRequires:  fdupes
BuildRequires:  hamcrest
BuildRequires:  javapackages-local
BuildRequires:  junit
BuildRequires:  objenesis
BuildRequires:  unzip
Requires:       cglib
Requires:       hamcrest
Requires:       junit
Requires:       objenesis
BuildArch:      noarch

%description
Mockito is a mocking framework. It lets you write tests. Tests
produce clean verification errors.

%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q
dos2unix `find -name *.java`
%patch0
%patch1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%pom_add_dep net.sf.cglib:cglib:3.1 maven/mockito-core.pom
find . -name "*.java" -exec sed -i "s|org\.%{name}\.cglib|net\.sf\.cglib|g" {} +
mkdir -p lib/compile lib/build lib/run lib/repackaged

%pom_xpath_remove 'target[@name="javadoc"]/copy' build.xml

%build
build-jar-repository lib/compile objenesis cglib junit hamcrest/core
ant -Dant.build.javac.source=1.6 -Dant.build.javac.target=1.6 jar javadoc prepare.poms

# Convert to OSGi bundle
bnd wrap \
 --version %{version} \
 --output target/%{name}-core-%{version}.bar \
 --properties conf/%{name}-core.bnd \
 target/%{name}-core-%{version}.jar
mv target/%{name}-core-%{version}.bar target/%{name}-core-%{version}.jar

%{mvn_artifact} target/%{name}-core.pom target/%{name}-core-%{version}.jar
%{mvn_alias} org.%{name}:%{name}-core org.%{name}:%{name}-all

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 target/%{name}-core-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}-core.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 target/%{name}-core.pom %{buildroot}%{_mavenpomdir}/%{name}/%{name}-core.pom
%add_maven_depmap %{name}/%{name}-core.pom %{name}/%{name}-core.jar -a org.%{name}:%{name}-all
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/javadoc/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc
%{_javadocdir}/%{name}
%license LICENSE NOTICE

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.10.19-4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Mar 25 2020 Fridrich Strba <fstrba@suse.com>
- Fetch sources using source service instead of script
* Fri Nov 29 2019 Fridrich Strba <fstrba@suse.com>
- Modified patch:
  * fix-bnd-config.patch
    + allow using objenesis 3.x too
* Sat Mar 23 2019 Jan Engelhardt <jengelh@inai.de>
- Remove nonsense and bias from description.
* Tue Feb 12 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of mockito 1.10.19
