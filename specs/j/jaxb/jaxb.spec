## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 9;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with bootstrap

Name:           jaxb
Version:        4.0.5
Release:        %autorelease
Summary:        JAXB Reference Implementation
License:        BSD-3-Clause
URL:            https://github.com/eclipse-ee4j/jaxb-ri
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        %{url}/archive/%{version}-RI/%{name}-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local-openjdk25
BuildRequires:  mvn(com.github.relaxng:relaxngDatatype)
BuildRequires:  mvn(com.sun.istack:istack-commons-maven-plugin)
BuildRequires:  mvn(com.sun.istack:istack-commons-runtime)
BuildRequires:  mvn(com.sun.istack:istack-commons-tools)
BuildRequires:  mvn(com.sun.xml.dtd-parser:dtd-parser)
BuildRequires:  mvn(com.sun.xml.fastinfoset:FastInfoset)
BuildRequires:  mvn(jakarta.activation:jakarta.activation-api)
BuildRequires:  mvn(jakarta.xml.bind:jakarta.xml.bind-api)
BuildRequires:  mvn(net.java.dev.msv:xsdlib)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.ant:ant-junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.jvnet.staxex:stax-ex)
%endif

%description
GlassFish JAXB Reference Implementation.

%package codemodel
Summary:        Codemodel Core

%description codemodel
The core functionality of the CodeModel java source code generation library.

%package codemodel-annotation-compiler
Summary:        Codemodel Annotation Compiler

%description codemodel-annotation-compiler
The annotation compiler ant task for the CodeModel java source code generation
library.

%package relaxng-datatype
Summary:        RelaxNG Datatype

%description relaxng-datatype
RelaxNG Datatype library.

%package xsom
Summary:        XML Schema Object Model

%description xsom
XML Schema Object Model (XSOM) is a Java library that allows applications to
easily parse XML Schema documents and inspect information in them. It is
expected to be useful for applications that need to take XML Schema as an
input.

%package core
Summary:        JAXB Core

%description core
JAXB Core module. Contains sources required by XJC, JXC and Runtime modules.

%package rngom
# pom.xml and module-info.java are under BSD, rest is MIT
License:        MIT AND BSD-3-Clause
Summary:        RELAX NG Object Model/Parser

%description rngom
This package contains RELAX NG Object Model/Parser.

%package runtime
Summary:        JAXB Runtime

%description runtime
JAXB (JSR 222) Reference Implementation

%package txw2
Summary:        TXW2 Runtime

%description txw2
TXW is a library that allows you to write XML documents.

%package xjc
# jaxb-ri/xjc/src/main/java/com/sun/tools/xjc/reader/internalizer/NamespaceContextImpl.java is under Apache-2.0
License:        BSD-3-Clause AND Apache-2.0
Summary:        JAXB XJC

%description xjc
JAXB Binding Compiler. Contains source code needed for binding customization
files into java sources. In other words: the tool to generate java classes for
the given xml representation.

%package txwc2
Summary:        TXW2 Compiler

%description txwc2
JAXB schema generator. The tool to generate XML schema based on java classes.

%prep
%autosetup -p1 -C

pushd jaxb-ri

# Remove ee4j parent
%pom_remove_parent boms/bom codemodel external xsom

%pom_remove_plugin -r :buildnumber-maven-plugin
%pom_remove_plugin -r :maven-enforcer-plugin

# Skip docs generation because of missing dependencies
%pom_xpath_remove "pom:profiles/pom:profile[pom:id='default-profile']/pom:modules"

# Disable unneeded extra OSGi bundles
%pom_disable_module bundles

# Missing dependency on org.checkerframework:compiler
%pom_disable_module jxc

%pom_remove_dep org.eclipse.angus:angus-activation core

# Don't install aggregator and parent poms
%mvn_package :jaxb-bom __noinstall
%mvn_package :jaxb-bom-ext __noinstall
%mvn_package :jaxb-bundles __noinstall
%mvn_package :jaxb-codemodel-parent __noinstall
%mvn_package :jaxb-docs-parent __noinstall
%mvn_package :jaxb-external-parent __noinstall
%mvn_package :jaxb-parent __noinstall
%mvn_package :jaxb-runtime-parent __noinstall
%mvn_package :jaxb-samples __noinstall
%mvn_package :jaxb-txw-parent __noinstall
%mvn_package :jaxb-www __noinstall

%if %{with bootstrap}
%pom_disable_module core
%pom_disable_module codemodel-annotation-compiler codemodel
%pom_disable_module runtime
%pom_disable_module relaxng-datatype external
%pom_disable_module rngom external
%pom_disable_module xjc
%pom_disable_module xsom
%pom_disable_module txw
%endif
popd

%build
pushd jaxb-ri
%mvn_build -s -f -j -- -Dproject.build.sourceEncoding=UTF-8
popd

%install
pushd jaxb-ri
%mvn_install
popd

%files codemodel -f jaxb-ri/.mfiles-codemodel
%license LICENSE.md NOTICE.md

%if %{without bootstrap}
%files codemodel-annotation-compiler -f jaxb-ri/.mfiles-codemodel-annotation-compiler
%files core -f jaxb-ri/.mfiles-jaxb-core
%files relaxng-datatype -f jaxb-ri/.mfiles-relaxng-datatype
%license LICENSE.md NOTICE.md
%files xsom -f jaxb-ri/.mfiles-xsom
%files rngom -f jaxb-ri/.mfiles-rngom
%files txw2 -f jaxb-ri/.mfiles-txw2
%license LICENSE.md NOTICE.md
%files txwc2 -f jaxb-ri/.mfiles-txwc2
%files runtime -f jaxb-ri/.mfiles-jaxb-runtime
%files xjc -f jaxb-ri/.mfiles-jaxb-xjc
%endif

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 4.0.5-9
- Latest state for jaxb

* Tue Jul 29 2025 Jiri Vanek <jvanek@redhat.com> - 4.0.5-8
- Rebuilt for java-25-openjdk as preffered jdk

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.5-6
- Build with OpenJDK 25

* Thu May 22 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.5-5
- Switch javapackages test plan to f43 ref

* Wed Mar 26 2025 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.5-4
- Switch to javapackages tests from CentOS Stream GitLab

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 29 2024 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.5-2
- Update javapackages test plan to f42

* Thu Sep 05 2024 Marian Koncek <mkoncek@redhat.com> - 4.0.5-1
- Update to upstream version 4.0.5

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 4.0.4-5
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 23 2024 Jiri Vanek <jvanek@redhat.com> - 4.0.4-4
- bump of release for for java-21-openjdk as system jdk

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 29 2023 Marian Koncek <mkoncek@redhat.com> - 4.0.4-1
- Update to upstream version 4.0.4

* Mon Nov 27 2023 Marian Koncek <mkoncek@redhat.com> - 4.0.3-1
- Update to upstream version 4.0.3

* Fri Sep 01 2023 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.0.2-3
- Convert License tag to SPDX format

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 08 2023 Marian Koncek <mkoncek@redhat.com> - 4.0.2-1
- Update to upstream version 4.0.2

* Wed Feb 08 2023 Marian Koncek <mkoncek@redhat.com> - 4.0.1-4
- Change license, remove bootstrap macro

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Marian Koncek <mkoncek@redhat.com> - 4.0.1-2
- Rebuild

* Mon Nov 21 2022 Marian Koncek <mkoncek@redhat.com> - 4.0.1-1
- Update to pstream version 4.0.1

* Thu Oct 27 2022 Marian Koncek <mkoncek@redhat.com> - 2.3.5-8
- Add bootstrap option

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Jiri Vanek <jvanek@redhat.com> - 2.3.5-6
- Rebuilt for Drop i686 JDKs

* Mon Feb 21 2022 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.3.5-5
- Remove subpackage that provides BOM/POM only
- Clean up spec (provides, obsoletes, etc.)

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2.3.5-4
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 17 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.3.5-2
- Remove workaround for SUREFIRE-1897

* Tue Oct 26 2021 Didik Supriadi <didiksupriadi41@fedoraproject.org> - 2.3.5-1
- Update to version 2.3.5
- Remove jp_minimal
- Disable tests

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Feb  5 2021 Mat Booth <mat.booth@redhat.com> - 2.3.3-6
- Add obsoletes/provides and compat aliases for old relaxngDatatype package

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 Mat Booth <mat.booth@redhat.com> - 2.3.3-4
- Restore deps on fi and stax-ex for full build mode

* Mon Aug 17 2020 Mat Booth <mat.booth@redhat.com> - 2.3.3-3
- Add obsoletes/provides and compat aliases for old xsom package

* Tue Aug 11 2020 Mat Booth <mat.booth@redhat.com> - 2.3.3-2
- Fastinfoset and Staxex are optional deps, this should be reflected in the OSGi
  metadata

* Tue Aug 04 2020 Mat Booth <mat.booth@redhat.com> - 2.3.3-1
- Update to latest upstream release
- Disable javadocs for now, due to https://github.com/fedora-java/xmvn/issues/58
- Upstream moved to eclipse-ee4j and implementation license changed to BSD (EDL)
- Enable tests, don't unnecessarily ship parent poms
- Rename package from glassfish-jaxb

## END: Generated by rpmautospec
