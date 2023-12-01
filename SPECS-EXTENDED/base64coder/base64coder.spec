Vendor:         Microsoft Corporation
Distribution:   Mariner
#
# spec file for package base64coder
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


%global long_ver  2010-12-19
%global short_ver 20101219
Name:           base64coder
Version:        %{short_ver}
Release:        4%{?dist}
Summary:        Base64 encoder/decoder Java library
License:        EPL-1.0 OR LGPL-2.1-or-later OR GPL-2.0-or-later OR Apache-2.0 OR BSD-2-Clause
Group:          Development/Libraries/Java
URL:            http://www.source-code.biz/%{name}/java/
Source0:        http://repo2.maven.org/maven2/biz/source_code/%{name}/%{long_ver}/%{name}-%{long_ver}-distribution.zip
Source1:        %{name}-LICENSE.txt
# Remove hardcoded source and target versions, so that we can specify them on command-line
Patch0:         %{name}-sourcetarget.patch
# Don't postprocess javadoc by modifying and moving the html files
Patch1:         %{name}-javadoc.patch
# Add bundle manifest to the jar file
Patch2:         %{name}-manifest.patch
BuildRequires:  ant
BuildRequires:  dos2unix
BuildRequires:  fdupes
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  unzip
BuildArch:      noarch

%description
Base64Coder is a Base64 encoder/decoder class.

There is no Base64 encoder/decoder in the standard Java SDK class
library.  The undocumented classes sun.misc.BASE64Encoder and
sun.misc.BASE64Decoder should not be used.

%package javadoc
Summary:        API documentation for %{name}
Group:          Documentation/HTML

%description javadoc
This package contains %{summary}.

%prep
%setup -q -n %{name}-%{long_ver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
dos2unix README.txt CHANGES.txt

cp %{SOURCE1} ./LICENSE.txt

%pom_remove_parent .

%build
%{ant} -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8 buildAll

%install
# jar
install -dm 0755 %{buildroot}%{_javadir}
install -pm 0644 target/%{name}.jar %{buildroot}%{_javadir}/%{name}.jar
# pom
install -dm 0755 %{buildroot}%{_mavenpomdir}
install -pm 0644 pom.xml %{buildroot}%{_mavenpomdir}/%{name}.pom
%add_maven_depmap %{name}.pom %{name}.jar
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/javadoc/* %{buildroot}%{_javadocdir}/%{name}
%fdupes -s %{buildroot}%{_javadocdir}/%{name}

%files -f .mfiles
%license LICENSE.txt
%doc README.txt CHANGES.txt

%files javadoc
%license LICENSE.txt
%{_javadocdir}/%{name}

%changelog
* Fri Dec 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 20101219-4
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20101219-3
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Nov 12 2020 Joe Schmitt <joschmit@microsoft.com> - 20101219-2.7
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Use javapackages-local-bootstrap to avoid build cycle.

* Mon Apr  8 2019 Fridrich Strba <fstrba@suse.com>
- Do not depend on the parent pom, since we are not building using
  maven.
* Thu Feb  7 2019 Jan Engelhardt <jengelh@inai.de>
- Trim bias from description.
* Tue Feb  5 2019 Fridrich Strba <fstrba@suse.com>
- Initial package of base64coder 20101219
