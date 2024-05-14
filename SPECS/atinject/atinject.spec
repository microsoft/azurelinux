#
# spec file for package atinject
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
%global base_version 1
%global git_tag 1f74ea7bd05ce4a3a62ddfe4a2511bf1b4287a61
%global git_version 20100611git1f74ea7
Summary:        Dependency injection specification for Java (JSR-330)
Name:           atinject
Version:        %{base_version}
Release:        6%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Libraries/Java
URL:            https://javax-inject.github.io/javax-inject/
# git clone --bare git@github.com:javax-inject/javax-inject
# git --git-dir=javax-inject.git archive --prefix %{name}-%{base_version}/ --format tar %{git_tag} | xz >%{name}-%{base_version}.tar.xz
Source0:        %{_distro_sources_url}/%{name}-%{base_version}.tar.xz
# These manifests based on the ones shipped by eclipse.org
Source1:        MANIFEST.MF
Source2:        MANIFEST-TCK.MF
Source3:        https://www.apache.org/licenses/LICENSE-2.0.txt
BuildRequires:  fdupes
BuildRequires:  java-devel > 1.6
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  junit
BuildRequires:  xz
BuildArch:      noarch

%description
This package specifies a means for obtaining objects in such a way as
to maximize reusability, testability and maintainability compared to
traditional approaches such as constructors, factories, and service
locators (e.g., JNDI). This process, known as dependency injection, is
beneficial to most nontrivial applications.

%package        tck
Summary:        TCK for testing %{name} compatibility with JSR-330
Group:          Development/Libraries/Java
Requires:       %{name} = %{version}-%{release}
Requires:       junit

%description    tck
%{summary}.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{base_version}
cp %{SOURCE3} LICENSE
rm -rf lib/*
build-jar-repository -p lib junit

# Fix dep in TCK pom
sed -i -e 's/pom\.groupId/project.groupId/' tck-pom.xml

%build
set -e
alias rm=:
alias xargs=:
alias javadoc='javadoc -source 7 -notimestamp -Xdoclint:none'
alias javac='javac -source 7 -target 7'
. ./build.sh

# Inject OSGi manifests required by Eclipse.
jar umf %{SOURCE1} build/dist/javax.inject.jar
jar umf %{SOURCE2} build/tck/dist/javax.inject-tck.jar

mv build/tck/javadoc build/javadoc/tck

%install
# jars
install -dm 755 %{buildroot}%{_javadir}/javax.inject
install -m 0644 build/dist/javax.inject.jar %{buildroot}%{_javadir}/%{name}.jar
(cd %{buildroot}%{_javadir}/javax.inject && ln -s ../%{name}.jar .)
install -m 0644 build/tck/dist/javax.inject-tck.jar %{buildroot}%{_javadir}/%{name}-tck.jar

# poms
install -dm 755 %{buildroot}%{_mavenpomdir}
install -m 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
install -m 0644 tck-pom.xml %{buildroot}%{_mavenpomdir}/%{name}-tck.pom
%add_maven_depmap %{name}.pom %{name}.jar
%add_maven_depmap %{name}-tck.pom %{name}-tck.jar -f tck

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr  build/javadoc/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}/%{name}/

%files -f .mfiles
%license LICENSE
%{_javadir}/javax.inject

%files tck -f .mfiles-tck

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Fri Mar 22 2024 Jon Slobodzian <joslobo@microsoft.com> - 1-6
- Updated to build with Java 7.  Modified version

* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1+20100611git1f74ea7-5
- Updating naming for 3.0 version of Azure Linux.

* Fri Mar 17 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1+20100611git1f74ea7-4
- Moved from extended to core

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1+20100611git1f74ea7-3
- Updating source URLs.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1+20100611git1f74ea7-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Nov 16 2020 Ruying Chen <v-ruyche@microsoft.com> - 1+20100611git1f74ea7-1.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Set javadoc Xdoclint:none.

* Wed Oct 24 2018 Fridrich Strba <fstrba@suse.com>
- Initial packaging of atinject adapted from Fedora rpm
