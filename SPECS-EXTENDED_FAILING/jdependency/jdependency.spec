Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package jdependency
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
Name:           jdependency
Version:        1.2
Release:        4%{?dist}
Summary:        An API to analyse class dependencies
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            http://github.com/tcurdt/%{name}
Source0:        http://github.com/tcurdt/%{name}/archive/%{name}-%{version}.tar.gz
Source1:        %{name}-build.xml
BuildRequires:  ant
BuildRequires:  apache-commons-io
BuildRequires:  fdupes
BuildRequires:  javapackages-local
BuildRequires:  objectweb-asm
Requires:       apache-commons-io
Requires:       objectweb-asm
BuildArch:      noarch
%if %{with tests}
BuildRequires:  ant-junit
BuildConflicts: java-devel >= 9
%endif

%description
%{name} is library that helps analyzing class level
dependencies, clashes and missing classes.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}-%{name}-%{version}
%if %{without tests}
  find . -name \*.jar -print -delete
%endif
cp %{SOURCE1} build.xml
mkdir -p lib
build-jar-repository -s lib commons-io objectweb-asm

%build
%{ant} \
%if %{without tests}
  -Dtest.skip=true \
%endif
  jar javadoc

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar
# javadocdir
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc README.md
%license LICENSE.txt

%files javadoc
%license LICENSE.txt
%{_javadocdir}/%{name}

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2-4
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Sat Mar 16 2019 Jan Engelhardt <jengelh@inai.de>
- Use noun phrase in summary. Generalize main description.
* Wed Mar 13 2019 Fridrich Strba <fstrba@suse.com>
- Add runtime dependencies as Requires
* Tue Mar  5 2019 Fridrich Strba <fstrba@suse.com>
- Initial package for jdependency 1.2
- Generate and customize the ant build file in order to build
  without maven
