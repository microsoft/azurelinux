#
# spec file for package xml-commons-resolver
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

%global resolverdir %{_sysconfdir}/java/resolver

Name:           xml-commons-resolver
Version:        1.2
Release:        6%{?dist}
Summary:        Resolver subproject of xml-commons
License:        Apache-2.0
Group:          Development/Libraries/Java
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://xerces.apache.org/xml-commons/components/resolver/
Source0:        https://www.apache.org/dist/xerces/xml-commons/%{name}-%{version}.tar.gz
Source1:        %{name}-pom.xml
Source2:        %{name}-resolver.1
Source3:        %{name}-xparse.1
Source4:        %{name}-xread.1
Source5:       %{name}-CatalogManager.properties
Patch0:         %{name}-1.2-crosslink.patch
Patch1:         %{name}-1.2-osgi.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel
BuildRequires:  javapackages-local-bootstrap
#!BuildIgnore:  xerces-j2 xml-apis xml-resolver
# Explicit javapackages-tools requires since scripts use
# /usr/share/java-utils/java-functions
Requires:       javapackages-tools
Provides:       xml-commons
Provides:       xml-commons-resolver-bootstrap = %{version}-%{release}
Provides:       xml-resolver = %{version}-%{release}
Provides:       %{name}10
Provides:       %{name}11
Provides:       %{name}12
Provides:       xerces-j2-xml-resolver
Obsoletes:      %{name}10
Obsoletes:      %{name}11
Obsoletes:      %{name}12
Obsoletes:      xerces-j2-xml-resolver
Obsoletes:      xml-commons
BuildArch:      noarch

%description
Resolver subproject of xml-commons.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%patch 0 -p1
%patch 1 -p1

cp %{SOURCE1} pom.xml

# remove all binary libs and prebuilt javadocs
find . -name "*.jar" -delete
rm -rf docs
sed -i 's/\r//' KEYS LICENSE.resolver.txt NOTICE-resolver.txt

%pom_remove_parent .

%build
%{ant} -f resolver.xml -Dant.build.javac.source=8 -Dant.build.javac.target=8 jar javadocs

%install
# jar
install -d -m 0755 %{buildroot}%{_javadir}
install -pm 644 build/resolver.jar %{buildroot}%{_javadir}/%{name}.jar
pushd %{buildroot}%{_javadir}
  for i in xerces-j2-xml-resolver xml-resolver %{name}10 %{name}11 %{name}12; do
    ln -s %{name}.jar ${i}.jar
  done
popd

# pom
install -d -m 0755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -a build/apidocs/resolver/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

# Scripts
mkdir -p %{buildroot}%{_bindir}
%jpackage_script org.apache.xml.resolver.apps.resolver "" "" %{name} xml-resolver true
%jpackage_script org.apache.xml.resolver.apps.xread "" "" %{name} xml-xread true
%jpackage_script org.apache.xml.resolver.apps.xparse "" "" %{name} xml-xparse true

# Man pages
install -d -m 755 %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man1/xml-resolver.1
install -p -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man1/xml-xparse.1
install -p -m 644 %{SOURCE4} %{buildroot}%{_mandir}/man1/xml-xread.1

# Central CatalogManager.properties
install -d -m 755 %{buildroot}%{resolverdir}
install -m 0644 %{SOURCE5} %{buildroot}%{resolverdir}/CatalogManager.properties

%files -f .mfiles
%license LICENSE.resolver.txt
%doc KEYS NOTICE-resolver.txt
%{_mandir}/man1/*
%{_bindir}/xml-*
%config(noreplace) %{resolverdir}/*
%dir %{resolverdir}
%{_javadir}/*

%files javadoc
%license LICENSE.resolver.txt
%doc NOTICE-resolver.txt
%{_javadocdir}/%{name}

%changelog
* Tue Feb 27 2024 Riken Maharjan <rmaharjan@microsoft.com> - 1.2-6
- build with msopenjdk-17

* Mon Mar 28 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.2-5
- Move to SPECS
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2-4
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 19 2020 Joe Schmitt <joschmit@microsoft.com> - 1.2-3.8
- Provide bootstrap version of this package.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.2-3.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Fix line break in sed command.

* Mon Apr  8 2019 Fridrich Strba <fstrba@suse.com>
- Do not depend on the parent pom since we are not building using
  Maven.
* Fri Feb  1 2019 Fridrich Strba <fstrba@suse.com>
- BuildIgnore xml-apis and xml-resolver, since this does not
  strictly require them for build
* Fri Feb  1 2019 Fridrich Strba <fstrba@suse.com>
- BuildIgnore xerces-j2 to break cycle of OSGi requires
* Thu Dec 13 2018 Fridrich Strba <fstrba@suse.com>
- Obsolete the different other xml-resolver providers
* Tue Dec 11 2018 Jan Engelhardt <jengelh@inai.de>
- Fix RPM groups. Use improved file deletion.
* Thu Dec  6 2018 Fridrich Strba <fstrba@suse.com>
- Initial package of xml-commons-resolver
- Add compatibility symlinks as well as provides
