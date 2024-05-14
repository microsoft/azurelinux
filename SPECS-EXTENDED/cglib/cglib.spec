Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package cglib
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
%global tarball_name RELEASE_3_2_4
Name:           cglib
Version:        3.2.4
Release:        3%{?dist}
Summary:        Code Generation Library
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://cglib.sourceforge.net/
Source0:        https://github.com/cglib/cglib/archive/%{tarball_name}.tar.gz
Source1:        %{name}-%{version}-build.tar.xz
BuildRequires:  ant >= 1.6
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  objectweb-asm >= 5
Provides:       %{name}-nohook = %{version}-%{release}
Obsoletes:      %{name}-nohook < %{version}-%{release}
Requires:       objectweb-asm >= 5
BuildArch:      noarch
%if %{with tests}
BuildConflicts: java-devel >= 9
BuildRequires:  ant-junit
%endif

%description
cglib is a powerful, high performance and quality Code Generation
Library, It is used to extend JAVA classes and implements interfaces at
runtime.

%package javadoc
Summary:        Code Generation Library
Group:          Documentation/HTML

%description javadoc
cglib is a powerful, high performance and quality Code Generation
Library, It is used to extend JAVA classes and implements interfaces at
runtime.

%prep
%setup -q -n %{name}-%{tarball_name} -a1

%pom_disable_module cglib-nodep
%pom_disable_module cglib-integration-test
%pom_disable_module cglib-jmh
%pom_xpath_set pom:packaging 'bundle' cglib
%pom_xpath_inject pom:build/pom:plugins '<plugin>
                                           <groupId>org.apache.felix</groupId>
                                           <artifactId>maven-bundle-plugin</artifactId>
                                           <version>1.4.0</version>
                                           <extensions>true</extensions>
                                           <configuration>
                                             <instructions>
                                               <Bundle-SymbolicName>net.sf.cglib.core</Bundle-SymbolicName>
                                               <Export-Package>net.*</Export-Package>
                                               <Import-Package>org.apache.tools.*;resolution:=optional,*</Import-Package>
                                             </instructions>
                                           </configuration>
                                         </plugin>' cglib
%pom_remove_plugin org.apache.maven.plugins:maven-gpg-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-jarsigner-plugin cglib-sample
%pom_remove_plugin -r :maven-javadoc-plugin

%pom_xpath_inject "pom:dependency[pom:artifactId='ant']" "<optional>true</optional>" cglib

%pom_remove_parent

%build
mkdir -p lib
build-jar-repository -s -p lib objectweb-asm/asm ant/ant ant/ant-launcher
%ant \
%if %{without tests}
    -Dtest.skip=true \
%endif
    -Dcompiler.target=1.8 -Dcompiler.source=1.8 \
    package javadoc

%install

# jars
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 %{name}/target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
install -pm 0644 %{name}-sample/target/%{name}-sample-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}-sample.jar

# poms
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}-parent.pom
%add_maven_depmap %{name}/%{name}-parent.pom
install -pm 0644 %{name}/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar -a "net.sf.cglib:cglib,cglib:cglib-full,cglib:cglib-nodep,org.sonatype.sisu.inject:cglib"
install -pm 0644 %{name}-sample/pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}-sample.pom
%add_maven_depmap %{name}/%{name}-sample.pom %{name}/%{name}-sample.jar

# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -r %{name}/target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Wed Nov 09 2022 Sumedh Sharma <sumsharma@microsoft.com> - 3.2.4-3
- Fix runtime requirements on objectweb-asm instead of mvn(org.ow2.asm:asm)
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.2.4-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.2.4-1.8
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Tue Mar  5 2019 Fridrich Strba <fstrba@suse.com>
- Upgrade to upstream 3.2.4
- Generate and customize ant build system
- Removed patches:
  * cglib-build_xml.patch
  * fix-javadoc.patch
    + Not needed any more
* Tue Dec 11 2018 Fridrich Strba <fstrba@suse.com>
- Build with objectweb-asm >= 5 in order not get stuck on a
  particular asmN dependency
* Mon Oct 29 2018 Fridrich Strba <fstrba@suse.com>
- Upgrade to version 3.1, the last one buildable with ant
- Depend on asm5
- Modified patch:
  * cglib-build_xml.patch
    + rediff to changed context
- Added patch:
  * fix-javadoc.patch
    + Do not import with wildcards a package that has no classes
    + Fixes javadoc generation
* Mon Oct 29 2018 Fridrich Strba <fstrba@suse.com>
- Add aliases to the maven artifact
* Wed Jun 13 2018 fstrba@suse.com
- Depend on asm3 and not objectweb-asm, since the binaries
  are equivalent.
* Wed May 16 2018 fstrba@suse.com
- Build with source and target 8 to prepare for a possible removal
  of 1.6 compatibility
* Mon Sep 18 2017 fstrba@suse.com
- Specify java source and target 1.6 in order to allow building
  with jdk9
- Fix javadoc generation
- Clean spec file
* Fri May 19 2017 mpluskal@suse.com
- Update package dependencies
* Wed Mar 18 2015 tchvatal@suse.com
- Fix build with new javapackages-tools
* Fri Sep 13 2013 mvyskocil@suse.com
- add javapackages-tools to build requires
* Wed Aug 28 2013 mvyskocil@suse.com
- use add_maven_Depmap from javapackages-tools
- fix obsoletes version
* Fri May 18 2012 mvyskocil@suse.cz
- update to 2.2
  * MethodProxy thread race patch
  * Upgrade to ASM 3.1
- remove useless repolib, nohook and demo packages
- fix build with jdk7
* Tue Apr 28 2009 mvyskocil@suse.cz
- Fixed package descriptions
* Thu Apr 23 2009 mvyskocil@suse.cz
- Initial packaging of cglib-nohooks in SUSE (2.1.3 from jpp5)
