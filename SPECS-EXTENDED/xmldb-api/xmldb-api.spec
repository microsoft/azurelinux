Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package xmldb-api
#
# Copyright (c) 2024 SUSE LLC
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

%define bname   xmldb
%global gh_version 1.7
Name:           xmldb-api
Version:        %{gh_version}.0
Release:        1%{?dist}
Summary:        XML:DB API for Java
License:        Apache-1.1
Group:          Development/Libraries/Java
URL:            https://github.com/xmldb-org/%{name}
Source0:        %{url}/archive/%{name}-%{gh_version}.tar.gz
Source1:        build.xml 
BuildRequires:  ant >= 1.6
BuildRequires:  javapackages-tools
BuildRequires:  xalan-j2
Requires:       xalan-j2
BuildArch:      noarch

%description
The API interfaces are what driver developers must implement when
creating a new driver, and are the interfaces that applications are
developed against. Along with the interfaces, a concrete DriverManager
implementation is also provided.

%package sdk
Summary:        SDK for XML:DB API
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}

%description sdk
The reference implementation provides a very simple file system based
implementation of the XML:DB API. This provides what is basically a
native XML database that uses directories to represent
collections, and just stores the XML in files.

The driver development kit provides a set of base classes that can be
extended to simplify and speed the development of XML:DB API drivers.
These classes are used to provide the basis for the reference
implementation, and therefore a simple example of how a driver can be
implemented. Using the SDK classes significantly reduces the amount of
code that must be written to create a new driver.

Along with the SDK base classes, the SDK also contains a set of jUnit
test cases that can be used to help validate the driver while it is
being developed. The test cases are still in development but there are
enough tests currently to be useful.

%package javadoc
Summary:        Documentation for XML:DB API for Java
Group:          Documentation/HTML

%description javadoc
The API interfaces are what driver developers must implement when
creating a new driver, and are the interfaces that applications are
developed against. Along with the interfaces, a concrete DriverManager
implementation is also provided.

%prep
%autosetup -n %{name}-%{name}-%{gh_version}
cp -f %{SOURCE1} build.xml

%build
export CLASSPATH=$(build-classpath xalan-j2)
export OPT_JAR_LIST=:
ant \
    -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8 \
    -Djarname=%{name} -Dsdk.jarname=%{name}-sdk \
    dist javadoc

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 dist/xmldb/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
install -m 644 dist/xmldb/%{name}-sdk.jar %{buildroot}%{_javadir}/%{name}-sdk-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr src/build/javadoc/full/* %{buildroot}%{_javadocdir}/%{name}

%files
%defattr(0644,root,root,0755)
%license LICENSE
%doc {AUTHORS,README.adoc}
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar

%files sdk
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-sdk-%{version}.jar
%{_javadir}/%{name}-sdk.jar

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

%changelog
* Fri Dec 12 2025 Aditya Singh <v-aditysing@microsoft.com> - 1.7.0-1
- Upgrade to version 1.7.0
- License verified. 

* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1-29
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Mateusz Malisz <mamalisz@microsoft.com> - 0.1-28
- Update Source0
- Improve formatting
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1-27
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Sep 11 2017 jengelh@inai.de
- Fix grammar problems in descriptions.
* Mon Sep 11 2017 fstrba@suse.com
- Specify java source and target level 1.6 in order to allow
  building with jdk9
* Fri Jul 11 2014 tchvatal@suse.com
- Cleanup with spec-cleaner and do not version javadoc dir.
* Fri Jun 27 2014 tchvatal@suse.com
- Fix unicode typo in changelog.
* Mon Sep  9 2013 tchvatal@suse.com
- Move from jpackage-utils to javapackage-tools
* Mon Mar 26 2012 cfarrell@suse.com
- license update: Apache-1.1
  SPDX
* Tue May 12 2009 mvyskocil@suse.cz
- Initial packaging of xmldb-api 0.1 in SUSE (from jpp 5.0)
