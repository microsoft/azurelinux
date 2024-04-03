
Summary:        Maven Resources Plugin
Name:           maven-javadoc-plugin
Version:        3.6.2
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://maven.apache.org/plugins/maven-javadoc-plugin
Source0:        https://repo1.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip
BuildRequires:  javapackages-bootstrap
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch

%description
The Javadoc Plugin uses the Javadoc tool to generate javadocs for the specified
project

%prep
%setup -q
 
%build
%{mvn_build}

%install
%{mvn_install}

%files -f .mfiles
%license LICENSE NOTICE

%files -f .mfiles
%license LICENSE NOTICE

%changelog
* Mon Nov 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.3.1-1
- Auto-upgrade to 3.3.1 - Azure Linux 3.0 - package upgrades
