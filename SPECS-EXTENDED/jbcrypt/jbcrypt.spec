Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package jbcrypt
#
# Copyright (c) 2024 SUSE LLC
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


Name:           jbcrypt
Version:        1.0.2
Release:        1%{?dist}
Summary:        An implementation the OpenBSD Blowfish password hashing algorithm
License:        ISC
Group:          Development/Libraries/Java
URL:            https://github.com/kruton/%{name}
Source0:        https://github.com/kruton/%{name}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-build.xml
Source2:        https://repo1.maven.org/maven2/org/connectbot/%{name}/%{version}/%{name}-%{version}.pom
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap >= 6
BuildRequires:  javapackages-tools
BuildArch:      noarch

%description
jBCrypt is an implementation the OpenBSD Blowfish password hashing
algorithm.

This system hashes passwords using a version of Bruce Schneier's
Blowfish block cipher with modifications designed to raise the cost of
off-line password cracking. The computation cost of the algorithm is
parameterised, so it can be increased as computers get faster.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries/Java

%description javadoc
This package contains API documentation for %{name}.

%prep
%setup -q
cp %{SOURCE1} build.xml

%build
%{ant} -Dtest.skip=true package javadoc

%install
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar -a org.connectbot.jbcrypt:jbcrypt

install -dm 0755 %{buildroot}%{_javadocdir}
cp -r target/site/apidocs %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}

%files -f .mfiles
%doc README
%license LICENSE

%files javadoc
%{_javadocdir}/%{name}
%license LICENSE

%changelog
* Tue Dec 16 2025 BinduSri Adabala <v-badabala@microsoft.com> - 1.0.2-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified

* Tue Mar 12 2024 Fridrich Strba <fstrba@suse.com>
- Initial packaging of version 1.0.2
