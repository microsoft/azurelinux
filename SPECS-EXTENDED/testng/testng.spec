Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package testng
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


Name:           testng
Version:        6.14.3
Release:        2%{?dist}
Summary:        Java-based testing framework
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://testng.org/
# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.xz
Source1:        pom.xml
Source2:        %{name}-build.xml
# Remove bundled binaries to make sure we don't ship anything forbidden
Source3:        generate-tarball.sh
Patch0:         0001-Avoid-accidental-javascript-in-javadoc.patch
Patch1:         0002-Replace-bundled-jquery-with-CDN-link.patch
BuildRequires:  ant
BuildRequires:  beust-jcommander
BuildRequires:  bsh2
BuildRequires:  fdupes
BuildRequires:  google-guice
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  jsr-305
BuildRequires:  junit
BuildRequires:  snakeyaml
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildArch:      noarch

%description
TestNG is a testing framework inspired from JUnit and NUnit but introducing
some new functionality, including flexible test configuration, and
distributed test running.  It is designed to cover unit tests as well as
functional, end-to-end, integration, etc.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

%patch0 -p1
%patch1 -p1

cp %{SOURCE1} .
cp %{SOURCE2} build.xml

# remove any bundled libs, but not test resources
find ! -path "*/test/*" -name *.jar -print -delete
find -name *.class -delete

# these are unnecessary
%pom_remove_plugin :maven-gpg-plugin .
%pom_remove_plugin :maven-source-plugin .
%pom_remove_plugin :maven-javadoc-plugin .

%pom_remove_parent .

sed -i -e 's/DEV-SNAPSHOT/%{version}/' src/main/java/org/testng/internal/Version.java

cp -p ./src/main/java/*.dtd.html ./src/main/resources/.

%{mvn_file} : %{name}
# jdk15 classifier is used by some other packages
%{mvn_alias} : :::jdk15:

%build
mkdir -p lib
build-jar-repository -s lib ant/ant beust-jcommander bsh2/bsh google-guice jsr305 junit snakeyaml
%ant jar javadoc

%mvn_artifact pom.xml target/%{name}-%{version}.jar

%install
%mvn_install
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc CHANGES.txt README.md
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.14.3-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 6.14.3-1.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Sun Mar 17 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of testng 6.14.3
- Generate and customize ant build.xml file
