Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package apache-commons-collections4
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


%define base_name       collections4
%define short_name      commons-%{base_name}
%bcond_with tests
Name:           apache-%{short_name}
Version:        4.1
Release:        2%{?dist}
Summary:        Extension of the Java Collections Framework
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/proper/commons-collections/
Source0:        https://archive.apache.org/dist/commons/collections/source/commons-collections4-%{version}-src.tar.gz
Patch0:         commons-collections4-4.1-jdk11.patch
Patch1:         commons-collections4-4.1-bundle.patch
Patch2:         commons-collections4-4.1-javadoc.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildRequires:  easymock
%endif

%description
Commons-Collections seek to build upon the JDK classes by providing
new interfaces, implementations and utilities.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n commons-collections4-%{version}-src
%patch 0 -p1
%patch 1 -p1
%patch 2 -p1

%pom_remove_parent

%build
%{ant} \
%if %{with tests}
  -Djunit.jar=$(build-classpath junit) \
  -Dhamcrest.jar=$(build-classpath hamcrest/core) \
  -Deasymock.jar=$(build-classpath easymock) \
  test \
%endif
  jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/%{short_name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc RELEASE-NOTES.txt
%license LICENSE.txt NOTICE.txt
%{_javadir}/%{short_name}.jar

%files javadoc
%license LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.1-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 4.1-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Mar  4 2019 Fridrich Strba <fstrba@suse.com>
- Initial packaging of apache-commons-collections4 4.1
- Added patches:
  * commons-collections4-4.1-bundle.patch
    + Add to the manifest OSGi bundle information
  * commons-collections4-4.1-javadoc.patch
    + Do not try to download web-based resources during the build.
  * commons-collections4-4.1-jdk11.patch
    + Resolve type ambiguity in a toArray(null) call
