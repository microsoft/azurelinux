Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-build-api
#
# Copyright (c) 2019 SUSE LLC
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


Name:           plexus-build-api
Version:        0.0.7
Release:        3%{?dist}
Summary:        Plexus Build API
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://github.com/sonatype/sisu-build-api
#Fetched from https://github.com/sonatype/sisu-build-api/tarball/plexus-build-api-0.0.7
Source0:        sonatype-sisu-build-api-plexus-build-api-0.0.7-0-g883ea67.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
Source2:        %{name}-build.xml
Patch0:         plexus-build-api-utils-3.3.0.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  plexus-classworlds
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-metadata-generator
BuildRequires:  plexus-utils
Requires:       mvn(org.codehaus.plexus:plexus-utils)
BuildArch:      noarch

%description
Plexus Build API

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n sonatype-sisu-build-api-f1f8849
%patch0 -p1
cp -p %{SOURCE1} .
cp -p %{SOURCE2} build.xml

%pom_remove_parent .

%build
mkdir -p lib
build-jar-repository -s lib plexus/utils plexus/classworlds plexus-containers/plexus-container-default
%{ant} \
  jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}/plexus
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/plexus/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}/plexus
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/plexus/%{name}.pom
%add_maven_depmap plexus/%{name}.pom plexus/%{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc LICENSE-2.0.txt

%files javadoc
%doc LICENSE-2.0.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.0.7-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Nov 13 2020 Ruying Chen <v-ruyche@microsoft.com> - 0.0.7-2.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Thu Nov 21 2019 Fridrich Strba <fstrba@suse.com>
- Added patch:
  * plexus-build-api-utils-3.3.0.patch
    + fix build against plexus-utils 3.3.0
* Fri Mar  8 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of plexus-build-api 0.0.7
- Generate and customize ant build.xml file
