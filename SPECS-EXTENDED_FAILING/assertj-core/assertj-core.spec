Vendor:         Microsoft Corporation
Distribution:   Mariner
%bcond_with memoryfilesystem

Name:           assertj-core
Version:        3.8.0
Release:        8%{?dist}
Summary:        Library of assertions similar to fest-assert
License:        ASL 2.0
URL:            http://joel-costigliola.github.io/assertj/
Source0:        https://github.com/joel-costigliola/assertj-core/archive/assertj-core-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(cglib:cglib-nodep)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
%if %{with memoryfilesystem}
BuildRequires:  mvn(com.github.marschall:memoryfilesystem)
%endif
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(org.ow2.asm:asm)

%description
A rich and intuitive set of strongly-typed assertions to use for unit testing
(either with JUnit or TestNG).

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

%pom_remove_parent
%pom_xpath_inject "pom:project" "<groupId>org.assertj</groupId>"

%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-shade-plugin
%pom_remove_plugin :maven-dependency-plugin
%pom_remove_plugin org.jacoco:jacoco-maven-plugin

# package org.mockito.internal.util.collections does not exist
rm -rf ./src/test/java/org/assertj/core/error/ShouldContainString_create_Test.java

%if %{without memoryfilesystem}
%pom_remove_dep :memoryfilesystem
rm -r src/test/java/org/assertj/core/internal/{Paths*.java,paths}
%endif

# test lib not in Fedora
%pom_remove_dep com.tngtech.java:junit-dataprovider

%build
%mvn_build -f -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc README.md CONTRIBUTING.md
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc CONTRIBUTING.md
%license LICENSE.txt

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.8.0-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 13 2019 Fabio Valentini <decathorpe@gmail.com> - 3.8.0-6
- Remove dependency on memoryfilesystem.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jul 28 2017 Mat Booth <mat.booth@redhat.com> - 3.8.0-1
- Update to latest version of assertj
- Disable tests due to missing deps in Fedora

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 2.2.0-3
- Add conditional for memoryfilesystem

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 02 2015 Roman Mohr <roman@fenkhuber.at> - 2.2.0-1
- Initial packaging
