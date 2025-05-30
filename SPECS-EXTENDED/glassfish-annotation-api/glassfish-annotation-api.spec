Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package glassfish-annotation-api
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


%global groupId javax.annotation
%global artifactId javax.annotation-api
Name:           glassfish-annotation-api
Version:        1.3.2
Release:        4%{?dist}
Summary:        Common Annotations API Specification (JSR 250)
License:        CDDL-1.0 OR GPL-2.0-only WITH Classpath-exception-2.0
Group:          Development/Libraries/Java
URL:            https://github.com/javaee/
Source0:        https://github.com/javaee/%{groupId}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-build.xml
Source2:        https://raw.githubusercontent.com/javaee/%{groupId}/master/LICENSE
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildArch:      noarch

%description
Common Annotations APIs for the Java Platform (JSR 250).

%package javadoc
Summary:        Javadoc for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{groupId}-%{version}
cp %{SOURCE1} build.xml
cp %{SOURCE2} .

%pom_remove_parent .

%build
%{ant}

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{artifactId}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar
# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}
install -pdm 0755 target/site/apidocs %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%license LICENSE

%files javadoc
%license LICENSE
%{_javadocdir}/%{name}

%changelog
* Fri Feb 28 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 1.3.2-4
- Build error fix, bump up the java source version from 1.6 to 1.8.
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.2-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Nov 17 2020 Ruying Chen <v-ruyche@microsoft.com> - 1.3.2-2.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Apr  8 2019 Fridrich Strba <fstrba@suse.com>
- Do not depend on the parent pom at all, since we don't build
  with maven.
* Tue Jan 29 2019 Fridrich Strba <fstrba@suse.com>
- Initial package of glassfish-annotation-api 1.3.2
