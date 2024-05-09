Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package jsoup
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


Name:           jsoup
Version:        1.11.3
Release:        4%{?dist}
Summary:        Java library for working with HTML
License:        MIT
Group:          Development/Libraries/Java
URL:            https://jsoup.org/
# ./generate-tarball.sh
# The sources contain non-free scraped web pages as test data
Source0:        %{_distro_sources_url}/%{name}-%{version}.tar.gz
Source1:        %{name}-build.xml
Source100:      generate-tarball.sh
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.7
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch

%description
jsoup is a Java library for working with HTML.
It provides an API for extracting and manipulating data,
using DOM, CSS, and jquery-like methods.

jsoup implements the WHATWG HTML5 specification.

 - scrapes and parses HTML from a URL, file, or string
 - finds and extracts data, using DOM traversal or CSS selectors
 - manipulates the HTML elements, attributes, and text
 - cleans user-submitted content against a safe white-list,
   to prevent XSS attacks
 - outputs tidied HTML

jsoup can deal with invalid HTML tag soup.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}
cp %{SOURCE1} .

%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-javadoc-plugin

%build
%ant -f %{name}-build.xml jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/%{name}
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/%{name}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}/%{name}.pom
%add_maven_depmap %{name}/%{name}.pom %{name}/%{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}
install -pdm 0755 target/site/apidocs %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc README.md CHANGES
%license LICENSE

%files javadoc
%license LICENSE
%{_javadocdir}/%{name}

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.11.3-4
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.11.3-3
- Updating source URLs.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.11.3-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.11.3-1.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Fri Feb 22 2019 Fridrich Strba <fstrba@suse.com>
- Remove from the tarball the non-free test data
* Sat Feb  2 2019 Jan Engelhardt <jengelh@inai.de>
- Ensure neutrality of descriptions.
* Fri Feb  1 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of jsoup version 1.11.3
- Added jsoup-build.xml file to build with ant
