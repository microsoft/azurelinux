Vendor:         Microsoft Corporation
Distribution:   Mariner
# Conditionally build with a minimal dependency set
%bcond_with jp_minimal

Name:           glassfish-jaxb
Version:        2.2.11
Release:        17%{?dist}
Summary:        JAXB Reference Implementation

License:        CDDL-1.1 and GPLv2 with exceptions
URL:            https://javaee.github.io/jaxb-v2

# Source0:      https://github.com/javaee/jaxb-v2/archive/refs/tags/jaxb-2_2_10.tar.gz
#               jabx-ri is part of the src code (no jaxb-ri-%{version}.src.zip file)
Source0:        https://github.com/javaee/jaxb-v2/archive/refs/tags/jaxb-ri-%{version}.src.zip
Patch0:         0001-Avoid-unnecessary-dep-on-istack-commons.patch
Patch1:         0002-Port-to-latest-version-of-args4j.patch

BuildRequires:  maven-local
BuildRequires:  mvn(javax.xml.bind:jaxb-api)
BuildRequires:  mvn(net.java:jvnet-parent:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
%if %{without jp_minimal}
BuildRequires:  mvn(args4j:args4j)
BuildRequires:  mvn(com.sun.istack:istack-commons-runtime)
BuildRequires:  mvn(com.sun.istack:istack-commons-tools)
BuildRequires:  mvn(com.sun:tools)
BuildRequires:  mvn(com.sun.xml.dtd-parser:dtd-parser)
BuildRequires:  mvn(com.sun.xml.fastinfoset:FastInfoset)
BuildRequires:  mvn(com.sun.xsom:xsom)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.jvnet.staxex:stax-ex)
BuildRequires:  mvn(relaxngDatatype:relaxngDatatype)
%endif

Requires:       %{name}-core                          = %{version}-%{release}
Requires:       %{name}-runtime                       = %{version}-%{release}
Requires:       %{name}-txw2                          = %{version}-%{release}
%if %{without jp_minimal}
Requires:       %{name}-bom                           = %{version}-%{release}
Requires:       %{name}-bom-ext                       = %{version}-%{release}
Requires:       %{name}-codemodel                     = %{version}-%{release}
Requires:       %{name}-codemodel-annotation-compiler = %{version}-%{release}
Requires:       %{name}-codemodel-parent              = %{version}-%{release}
Requires:       %{name}-external-parent               = %{version}-%{release}
Requires:       %{name}-jxc                           = %{version}-%{release}
Requires:       %{name}-parent                        = %{version}-%{release}
Requires:       %{name}-rngom                         = %{version}-%{release}
Requires:       %{name}-runtime-parent                = %{version}-%{release}
Requires:       %{name}-txwc2                         = %{version}-%{release}
Requires:       %{name}-txw-parent                    = %{version}-%{release}
Requires:       %{name}-xjc                           = %{version}-%{release}
%endif

Obsoletes:      glassfish-jaxb1-impl                  < 2.2.11-12

BuildArch:      noarch

%description
GlassFish JAXB Reference Implementation.

%package core
Summary:        JAXB Core

%description core
JAXB Core module. Contains sources required by XJC, JXC and Runtime
modules.

%package runtime
Summary:        JAXB Runtime

%description runtime
JAXB (JSR 222) Reference Implementation

%package txw2
Summary:        TXW2 Runtime

%description txw2
TXW is a library that allows you to write XML documents.

%if %{without jp_minimal}
%package codemodel
Summary:        Codemodel Core

%description codemodel
The core functionality of the CodeModel java source code generation
library.

%package codemodel-annotation-compiler
Summary:        Codemodel Annotation Compiler

%description codemodel-annotation-compiler
The annotation compiler ant task for the CodeModel java source code
generation library.

%package bom
Summary:        JAXB BOM

%description bom
JAXB Bill of Materials (BOM)

%package bom-ext
Summary:        JAXB BOM with all dependencies

%description bom-ext
JAXB Bill of Materials (BOM) with all dependencies.

%package codemodel-parent
Summary:        Codemodel parent POM

%description codemodel-parent
This package contains codemodel parent POM.

%package external-parent
Summary:        JAXB External parent POM

%description external-parent
JAXB External parent POM.

%package jxc
Summary:        JAXB schema generator

%description jxc
The tool to generate XML schema based on java classes.

%package parent
Summary:        JAXB parent POM

%description parent
This package contains parent POM.

%package runtime-parent
Summary:        JAXB Runtime parent POM

%description runtime-parent
This package contains Runtime parent POM.

%package txw-parent
Summary:        JAXB TXW parent POM

%description txw-parent
This package contains TXW parent POM.

%package xjc
Summary:        JAXB XJC

%description xjc
JAXB Binding Compiler. Contains source code needed for binding
customization files into java sources. In other words: the tool to
generate java classes for the given xml representation.

%package rngom
Summary:        RELAX NG Object Model/Parser

%description rngom
This package contains RELAX NG Object Model/Parser.

%package txwc2
Summary:        TXW2 Compiler

%description txwc2
JAXB schema generator. The tool to generate XML schema based on java
classes.
%endif

%package javadoc
Summary:        Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -c

%if %{with jp_minimal}
%patch0 -p1
%endif
%patch1 -p1

# Disable unneeded OSGi bundles
%pom_disable_module xjc bundles
%pom_disable_module jxc bundles
%pom_disable_module ri bundles
%pom_disable_module osgi bundles
%pom_disable_module core bundles

# Fix jar plug-in usage for OSGi bundles
%pom_xpath_replace "pom:useDefaultManifestFile" "
<archive>
  <manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
</archive>" bundles/core bundles/runtime

# Make javax.activation an optional dep
%pom_xpath_inject "pom:configuration/pom:instructions" "
<Import-Package>javax.activation;resolution:=optional,*</Import-Package>" bundles/runtime

# Disable ancient jaxb1 runtime
%pom_disable_module jaxb1 runtime

# Fix hard-coded tools location
%pom_remove_dep com.sun:tools
%pom_add_dep_mgmt com.sun:tools
%pom_remove_dep com.sun:tools jxc
%pom_add_dep com.sun:tools jxc

# Plug-ins not useful for RPM builds
%pom_remove_plugin :buildnumber-maven-plugin
%pom_remove_plugin :gfnexus-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-source-plugin jxc
%pom_remove_plugin :maven-source-plugin xjc

%if %{with jp_minimal}
# For minimal build disable all modules with extra deps
%pom_disable_module codemodel
%pom_disable_module external
%pom_disable_module jxc
%pom_disable_module compiler txw
%pom_disable_module xjc
# For minimal build of impl module, don't compile in support for extra deps
%pom_remove_dep org.jvnet.staxex:stax-ex runtime/impl
%pom_remove_dep com.sun.xml.fastinfoset:FastInfoset runtime/impl
rm runtime/impl/src/main/java/com/sun/xml/bind/v2/runtime/unmarshaller/{FastInfoset,StAXEx}Connector.java
rm runtime/impl/src/main/java/com/sun/xml/bind/v2/runtime/output/{FastInfoset,StAXEx}StreamWriterOutput.java
%endif

%mvn_alias org.glassfish.jaxb:jaxb-xjc "com.sun.xml.bind:jaxb-xjc"

# Package OSGi version of runtime with the non-OSGi version
%mvn_package com.sun.xml.bind:jaxb-impl jaxb-runtime

# Don't install bundles parent pom
%mvn_package com.sun.xml.bind.mvn:jaxb-bundles __noinstall

%if %{with jp_minimal}
# Don't install aggregator poms or boms for minimal build
%mvn_package com.sun.xml.bind.mvn: __noinstall
%mvn_package :jaxb-bom* __noinstall
%endif

%build
%mvn_build -f -s -- -Ddev -DbuildNumber=unknown

%install
%mvn_install

%files
%license License.txt licenceheader.txt License.html

%files core -f .mfiles-jaxb-core
%license License.txt licenceheader.txt License.html

%files runtime -f .mfiles-jaxb-runtime
%license License.txt licenceheader.txt License.html

%files txw2 -f .mfiles-txw2
%license License.txt licenceheader.txt License.html

%if %{without jp_minimal}
%files codemodel -f .mfiles-codemodel
%license License.txt licenceheader.txt License.html

%files codemodel-annotation-compiler -f .mfiles-codemodel-annotation-compiler

%files bom -f .mfiles-jaxb-bom
%license License.txt licenceheader.txt License.html

%files bom-ext -f .mfiles-jaxb-bom-ext

%files codemodel-parent -f .mfiles-jaxb-codemodel-parent

%files external-parent -f .mfiles-jaxb-external-parent

%files jxc -f .mfiles-jaxb-jxc
%license License.txt licenceheader.txt License.html

%files parent -f .mfiles-jaxb-parent

%files runtime-parent -f .mfiles-jaxb-runtime-parent

%files txw-parent -f .mfiles-jaxb-txw-parent

%files xjc -f .mfiles-jaxb-xjc

%files rngom -f .mfiles-rngom
%license License.txt licenceheader.txt License.html

%files txwc2 -f .mfiles-txwc2
%license License.txt licenceheader.txt License.html
%endif

%files javadoc -f .mfiles-javadoc
%license License.txt licenceheader.txt License.html


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.11-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 10 2019 Mat Booth <mat.booth@redhat.com> - 2.2.11-14
- Make javax.activation an optional dep in OSGi metadata

* Fri May 10 2019 Mat Booth <mat.booth@redhat.com> - 2.2.11-13
- Add conditional build for reduced dependency set

* Thu May 09 2019 Mat Booth <mat.booth@redhat.com> - 2.2.11-12
- Disable ancient jaxb1 runtime
- Enable OSGi bundle version of the runtime
- Spec file clean up

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 25 2018 Michael Simacek <msimacek@redhat.com> - 2.2.11-9
- Reduce build deps

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 09 2017 Michael Simacek <msimacek@redhat.com> - 2.2.11-7
- Specify CDDL license version

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 20 2015 Michal Srb <msrb@redhat.com> - 2.2.11-2
- Split into subpackages (Resolves: rhbz#1204187)

* Mon Jan 19 2015 Michal Srb <msrb@redhat.com> - 2.2.11-1
- Update to upstream version 2.2.11

* Mon Oct 27 2014 Michal Srb <msrb@redhat.com> - 2.2.5-8
- Fix FTBFS (Resolves: rhbz#1106636)
- Adapt to current packaging guidelines
- Remove R, add BR: javapackages-local (for %%mvn_artifact macro)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.5-6
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.2.5-2
- Add missing xsom and rngom dependencies to the POM files

* Sat Mar 10 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.2.5-1
- Updated to upstream version 2.2.5
- Removed classpath from manifest files

* Wed Mar 7 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.2.4u1-4
- Updated to reflect the change from glassfish-fi to glassfish-fastinfoset

* Wed Feb 22 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.2.4u1-3
- Updated to reflect the changes of the jar names in txw2

* Wed Feb 22 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.2.4u1-2
- Cleanup of the spec file

* Sat Jan 21 2012 Marek Goldmann <mgoldman@redhat.com> 2.2.4u1-1
- Initial packaging
