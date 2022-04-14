Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package easymock
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
Name:           easymock
Version:        3.6
Release:        3%{?dist}
Summary:        Mock objects for interfaces in JUnit tests
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://www.easymock.org
# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.xz
# Remove bundled binaries which cannot be easily verified for licensing
Source1:        generate-tarball.sh
Source2:        %{name}-build.tar.xz
Patch1:         0001-Disable-android-support.patch
Patch2:         0002-Unshade-cglib-and-asm.patch
Patch3:         0003-Fix-OSGi-manifest.patch
BuildRequires:  ant
BuildRequires:  beust-jcommander
BuildRequires:  cglib
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit
BuildRequires:  objectweb-asm
BuildRequires:  objenesis
BuildRequires:  testng
BuildRequires:  xmvn-install
BuildRequires:  xmvn-resolve
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildConflicts: java-devel >= 9
%endif

%description
EasyMock provides Mock Objects for interfaces in JUnit tests by generating
them on the fly using Java's proxy mechanism. Due to EasyMock's unique style
of recording expectations, most refactorings will not affect the Mock Objects.
So EasyMock is a perfect fit for Test-Driven Development.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version} -a2

%patch1 -p1
%patch2 -p1
%patch3 -p1

%pom_remove_plugin :maven-license-plugin
%pom_remove_plugin :maven-timestamp-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin core

# remove android support
rm core/src/main/java/org/easymock/internal/Android*.java
rm core/src/test/java/org/easymock/tests2/ClassExtensionHelperTest.java
%pom_disable_module test-android
%pom_remove_dep :dexmaker core

# unbundle asm and cglib
%pom_disable_module test-nodeps
%pom_remove_plugin :maven-shade-plugin core

# missing test deps
%pom_disable_module test-integration
%pom_disable_module test-osgi

# remove some warning caused by unavailable plugin
%pom_remove_plugin org.codehaus.mojo:versions-maven-plugin

# For compatibility reasons
%{mvn_file} ":easymock{*}" easymock@1 easymock3@1

# ssh not needed during our builds
%pom_xpath_remove pom:extensions

%build
mkdir -p lib
build-jar-repository -s lib \
  beust-jcommander cglib/cglib junit objectweb-asm/asm objenesis/objenesis testng
%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  package javadoc

%{mvn_artifact} pom.xml
%{mvn_artifact} core/pom.xml core/target/easymock-%{version}.jar
%{mvn_artifact} test-java8/pom.xml test-java8/target/easymock-test-java8-%{version}.jar
%{mvn_artifact} test-testng/pom.xml test-testng/target/easymock-test-testng-%{version}.jar

%install
%mvn_install -J core/target/site/apidocs
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license core/LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license core/LICENSE.txt

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 20 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.6-2.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Apr  9 2019 Jan Engelhardt <jengelh@inai.de>
- Summarize description.
* Sun Mar 17 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of easymock 3.6
- Generate and customize ant build files
