Name:           istack-commons
Version:        2.21
Release:        13%{?dist}
Summary:        Common code for some Glassfish projects
License:        CDDL-1.1 and GPLv2 with exceptions
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://istack-commons.java.net
# svn export https://svn.java.net/svn/istack-commons~svn/tags/istack-commons-2.21/ istack-commons-2.21
# find istack-commons-2.21/ -name '*.class' -delete
# find istack-commons-2.21/ -name '*.jar' -delete
# rm -rf istack-commons-2.21/test/lib/*.zip istack-commons-2.21/runtime/lib/*.zip
# tar -zcvf istack-commons-2.21.tar.gz istack-commons-2.21
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(args4j:args4j)
BuildRequires:  mvn(com.sun.codemodel:codemodel)
BuildRequires:  mvn(com.sun:tools)
BuildRequires:  mvn(dom4j:dom4j)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.java:jvnet-parent:pom:)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.ant:ant-junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven:maven-aether-provider)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-project)
BuildRequires:  mvn(org.apache.maven:maven-settings)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.shared:file-management)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-http-lightweight)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-io)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.eclipse.aether:aether-connector-basic)
BuildRequires:  mvn(org.eclipse.aether:aether-impl)
BuildRequires:  mvn(org.eclipse.aether:aether-spi)
BuildRequires:  mvn(org.eclipse.aether:aether-transport-file)
BuildRequires:  mvn(org.eclipse.aether:aether-transport-wagon)
BuildRequires:  mvn(org.eclipse.aether:aether-util)
BuildRequires:  mvn(org.testng:testng)

%description
Code shared between JAXP, JAXB, SAAJ, and JAX-WS projects.

%package maven-plugin
Summary:        istack-commons Maven Mojo
Obsoletes:      maven-istack-commons-plugin < %{version}-%{release}
Provides:       maven-istack-commons-plugin = %{version}-%{release}

%description maven-plugin
This package contains the istack-commons Maven Mojo.

%package -n import-properties-plugin
Summary:        istack-commons import properties plugin

%description -n import-properties-plugin
This package contains the istack-commons import properties Maven Mojo.

%package buildtools
Summary:        istack-commons buildtools
Obsoletes:      %{name} < %{version}-%{release}

%description buildtools
This package contains istack-commons buildtools.

%package runtime
Summary:        istack-commons runtime
Obsoletes:      %{name} < %{version}-%{release}

%description runtime
This package contains istack-commons runtime.

%package soimp
Summary:        istack-commons soimp
Obsoletes:      %{name} < %{version}-%{release}

%description soimp
This package contains istack-commons soimp.

%package test
Summary:        istack-commons test
Obsoletes:      %{name} < %{version}-%{release}

%description test
This package contains istack-commons test.

%package tools
Summary:        istack-commons tools
Obsoletes:      %{name} < %{version}-%{release}

%description tools
This package contains istack-commons tools.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

%pom_remove_plugin org.glassfish.copyright:glassfish-copyright-maven-plugin
%pom_remove_plugin org.codehaus.mojo:findbugs-maven-plugin
%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin

# backward compatibility symlinks
%mvn_file com.sun.istack:%{name}-buildtools %{name}-buildtools %{name}/%{name}-buildtools
%mvn_file com.sun.istack:%{name}-runtime %{name}-runtime %{name}/%{name}-runtime
%mvn_file com.sun.istack:%{name}-soimp %{name}-soimp %{name}/%{name}-soimp
%mvn_file com.sun.istack:%{name}-test %{name}-test %{name}/%{name}-test
%mvn_file com.sun.istack:%{name}-tools %{name}-tools %{name}/%{name}-tools

# Unused & unavailable dep
%pom_remove_dep org.sonatype.sisu:sisu-inject-plexus import-properties-plugin

# get rid of scope "import", our tools don't know how to handle such deps
%pom_remove_dep com.sun:tools tools
%pom_add_dep com.sun:tools tools

%build

%mvn_build -s -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles-istack-commons
%dir %{_javadir}/%{name}
%doc Licence.txt

%files -n %{name}-maven-plugin -f .mfiles-%{name}-maven-plugin
%doc Licence.txt

%files -n import-properties-plugin -f .mfiles-import-properties-plugin
%doc Licence.txt

%files buildtools -f .mfiles-istack-commons-buildtools
%doc Licence.txt

%files runtime -f .mfiles-istack-commons-runtime
%doc Licence.txt

%files soimp -f .mfiles-istack-commons-soimp
%doc Licence.txt

%files test -f .mfiles-istack-commons-test
%doc Licence.txt

%files tools -f .mfiles-istack-commons-tools
%doc Licence.txt

%files javadoc -f .mfiles-javadoc
%doc Licence.txt


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.21-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 09 2017 Michael Simacek <msimacek@redhat.com> - 2.21-7
- Specify CDDL license version

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 27 2015 Michal Srb <msrb@redhat.com> - 2.21-2
- Split into subpackages (Resolves: rhbz#1196653)

* Wed Jan 21 2015 gil cattaneo <puntogil@libero.it> 2.21-1
- update to 2.21
- adapt to current guideline

* Sun Aug 03 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 2.17-5
- Fix FTBFS due to F21 XMvn changes (#1106808)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.17-3
- Use Requires: java-headless rebuild (#1067528)

* Fri Jul 26 2013 Ade Lee <alee@rdhat.com> - 2.17-2
- Bugzilla BZ#988933 - Removed unneeded build dependencies.

* Thu May 16 2013 Tom Callaway <spot@fedoraproject.org> - 2.17-1
- update to 2.17

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.6.1-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Juan Hernandez <juan.hernandez@redhat.com> - 2.6.1-5
- Add maven-enforcer-plugin as build time dependency

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 31 2012 Gil Cattaneo <puntogil@libero.it> 2.6.1-3
- Rebuilt with codemodel support
- Enable maven-plugin, test and buildtools modules

* Mon Feb 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.6.1-2
- Minor cleanups of the spec file

* Mon Jan 16 2012 Marek Goldmann <mgoldman@redhat.com> 2.6.1-1
- Initial packaging
