Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package plexus-sec-dispatcher
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
Name:           plexus-sec-dispatcher
Version:        1.4
Release:        3%{?dist}
Summary:        Plexus Security Dispatcher Component
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://github.com/codehaus-plexus/plexus-sec-dispatcher
# svn export http://svn.sonatype.org/spice/tags/plexus-sec-dispatcher-1.4/
# tar jcf plexus-sec-dispatcher-1.4.tar.bz2 plexus-sec-dispatcher-1.4/
Source0:        %{name}-%{version}.tar.bz2
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
Source100:      %{name}-build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local
BuildRequires:  modello
BuildRequires:  plexus-cipher
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-metadata-generator
BuildRequires:  plexus-utils
Requires:       mvn(org.codehaus.plexus:plexus-utils)
Requires:       mvn(org.sonatype.plexus:plexus-cipher)
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
%endif

%description
Plexus Security Dispatcher Component

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q

cp %{SOURCE1} .
cp %{SOURCE100} build.xml

%pom_remove_parent
%pom_change_dep -r -f ::::: ::::: 

%build
mkdir -p lib
build-jar-repository -s lib plexus/utils plexus/plexus-cipher plexus-containers/plexus-container-default
%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
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
%license LICENSE-2.0.txt

%files javadoc
%license LICENSE-2.0.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4-3
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Sat Oct  5 2019 Fridrich Strba <fstrba@suse.com>
- Avoid version-less dependencies
* Tue Mar 12 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of plexus-sec-dispatcher 1.4
- Generate and customize ant build.xml file
