Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# spec file for package beust
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


%global short_name jcommander
Name:           beust-%{short_name}
Version:        1.78
Release:        1%{?dist}
Summary:        Java framework for parsing command line parameters
License:        Apache-2.0
Group:          Development/Libraries/Java
URL:            https://jcommander.org/
Source0:        https://github.com/cbeust/%{short_name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Adapted from earlier version that still shipped poms. It uses kobalt for building now
Source1:        %{name}.pom
Source2:        %{name}-build.xml
Patch0:         0001-ParseValues-NullPointerException-patch.patch
BuildRequires:  ant
BuildRequires:  fdupes
BuildRequires:  java-devel >= 1.8
BuildRequires:  javapackages-local-bootstrap
Requires:       java >= 1.8
Obsoletes:      %{short_name} < %{version}-%{release}
Provides:       %{short_name} = %{version}-%{release}
BuildArch:      noarch

%description
JCommander is a Java framework that allows parsing command line
parameters (with annotations).

%package javadoc
Summary:        API documentation for %{name}
Group:          Development/Libraries/Java

%description javadoc
This package contains the %{summary}.

%prep
%setup -q -n %{name}-%{version}
rm -rf gradle* kobalt* lib
%patch 0 -p1

chmod -x license.txt
cp -p %{SOURCE1} pom.xml
cp -p %{SOURCE2} build.xml
sed -i 's/@VERSION@/%{version}/g' pom.xml build.xml

%pom_remove_parent .

%build
%{ant} jar javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{short_name}-%{version}.jar \
   %{buildroot}%{_javadir}/%{name}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}/
%fdupes -s %{buildroot}%{_javadocdir}/%{name}/

%files -f .mfiles
%license license.txt
%doc notice.md README.markdown

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 1.78-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.
- Upgrade to version 1.78.

* Mon Apr  8 2019 Fridrich Strba <fstrba@suse.com>
- Remove reference to pom parent from pom.xml file, since we are
  not building with maven.
* Thu Feb  7 2019 Jan Engelhardt <jengelh@inai.de>
- Avoid double shipping of documentation.
- Ensure neutrality of descriptions.
* Thu Dec  6 2018 Fridrich Strba <fstrba@suse.com>
- Fix javadoc build with older JDK versions
* Thu Oct 25 2018 Fridrich Strba <fstrba@suse.com>
- Build with java source/target levels 8 since the code uses
  String.join() which does not exist before java 8
* Wed Oct 24 2018 Fridrich Strba <fstrba@suse.com>
- Initial packaging built without maven, adapted from Fedora rpm
