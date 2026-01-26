Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file
#
# Copyright (c) 2023 SUSE LLC
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
Version:        4.4
Release:        1%{?dist}
Summary:        Extension of the Java Collections Framework
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://commons.apache.org/proper/commons-collections/
Source0:        https://archive.apache.org/dist/commons/collections/source/commons-collections4-%{version}-src.tar.gz
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap >= 6
BuildArch:      noarch

%description
Commons-Collections seek to build upon the JDK classes by providing
new interfaces, implementations and utilities.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package provides %{summary}.

%prep
%autosetup -n commons-collections4-%{version}-src
cp %{SOURCE1} build.xml

%build
%{ant} jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{short_name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/%{short_name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
# Remove LICENSE from javadoc directory to avoid duplicate license warning
mv %{buildroot}%{_javadocdir}/%{name}/legal/ADDITIONAL_LICENSE_INFO .
mv %{buildroot}%{_javadocdir}/%{name}/legal/LICENSE .
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc RELEASE-NOTES.txt
%license LICENSE.txt NOTICE.txt
%license ADDITIONAL_LICENSE_INFO
%{_javadir}/%{short_name}.jar

%files javadoc
%license LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Thu May 15 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 4.4-1
- Initial Azure Linux import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified

   + Updates the platform requirement from Java 6 to 8
    + Add Automatic-Module-Name MANIFEST entry for Java 9
      compatibility
    + Added a few new APIs.
  * Builds with java 21 out of the box
  * Generated ant build system with maven-ant-plugin in order to
    build with ant like before.
- Removed patches:
  * commons-collections4-4.1-bundle.patch
  * commons-collections4-4.1-javadoc.patch
  * commons-collections4-4.1-jdk11.patch
    + All changes factored into the generated build.xml

* Fri Mar 18 18:14:43 UTC 2022 - Fridrich Strba <fstrba@suse.com>
- Build with source/target levels 8

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
